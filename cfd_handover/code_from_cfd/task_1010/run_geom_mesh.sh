#!/bin/bash
# usage: run_geom_mesh.sh <package_path> <label> [mesh_env e.g. M1_THROAT_REQ=0.00002] [--variant=N]
# WO1010 geometry -> mesh -> patch types -> D3/D4 with the UNCHANGED p5 builders (package given by path; outputs keyed by <label>, not scan,
# because several packages share a scan). Same resource wait as p5/run_case.sh (MemAvailable >= 12.5 GB, disk >= 12 GB), but FAIL CLOSED: if the wait (360 x 60 s) expires the mesh is NOT built (exit 1, runs.log line).
# Mesh admission is serialised across the workers: flock on wo1010/mesh_admit.lock is held from the resource check until cartesianMesh has run 120 s (or the mesh builder exited), so two workers never pass
# the MemAvailable check together. No solver.
# After the geometry stage (also when it already existed): out/<label>_extensions.json (as-built lengths from gates.json extensions.per_patch, for pf/build_m1_case.py --extensions-json).
# A finished mesh (mesh/<label>/mesh_gates.json present) is not rebuilt; patch types + d34 still run. Exit non-zero if extensions/mesh/d34 fail.
H=/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010; P5=/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5
cd "$H"; export OMP_NUM_THREADS=4
PKD="$1"; lab="$2"; menv="$3"; var="$4"; scan=$(python3 -c "import json;print(json.load(open('$PKD/meta.json'))['instance']['scan'])")
# the geometry builder's own kind rule (p5/build_m1_geometry.py): meta error_type, else from the package name; it writes surface_radius_<scan>_<kind>.csv
kind=$(python3 -c "import json,os;pk=os.path.basename(os.path.normpath('$PKD'));m=json.load(open('$PKD/meta.json'));print(m.get('error_type') or ('T1_missed_branch' if 'T1_missed_branch' in pk else ('baseline' if '__baseline__' in pk else 'clean_nolesion')))")
G=$H/out/$lab; M=$H/mesh/$lab; t0=$(date +%s)
if [ ! -f "$G/case.stl" ]; then
  nice -n 10 /usr/bin/python3 $P5/build_m1_geometry.py "$PKD" "$G" > logs/geometry_$lab.log 2>&1; rcg=$?
  echo "$(date +%F_%T) $lab geometry rc=$rcg $(( $(date +%s)-t0 )) s" >> runs.log
fi
[ -f "$G/case.stl" ] || { echo "$(date +%F_%T) $lab NO case.stl" >> runs.log; exit 1; }
python3 - "$G/gates.json" "$PKD/outlets.csv" "$H/out/${lab}_extensions.json" > logs/extensions_$lab.log 2>&1 <<'EOF'
import json, csv, sys
gj, oc, out = sys.argv[1:4]
pp = json.load(open(gj))["extensions"]["per_patch"]
ext = {p["patch"]: float(p["extension_length_mm"]) for p in pp if p["patch"] != "inlet"}
inl = [float(p["extension_length_mm"]) for p in pp if p["patch"] == "inlet"]
ids = [r["outlet_id"] for r in csv.DictReader(open(oc))]
miss = [i for i in ids if i not in ext]; extra = sorted(set(ext) - set(ids))
if miss or extra or len(inl) != 1: raise SystemExit(f"extensions mismatch: missing {miss}, extra {extra}, inlet entries {len(inl)} ({gj} vs {oc})")
json.dump(dict(extension_lengths_mm={i: ext[i] for i in ids}, inlet_extension_mm=inl[0], source=f"{gj} extensions.per_patch"), open(out, "w"), indent=1)
print("wrote", out, len(ids), "outlets")
EOF
rce=$?; echo "$(date +%F_%T) $lab extensions rc=$rce" >> runs.log
[ $rce -eq 0 ] || exit 1
if [ -f "$M/mesh_gates.json" ]; then
  echo "$(date +%F_%T) $lab mesh exists (mesh_gates.json), not rebuilt" >> runs.log
else
  tw=$(date +%s); exec 7> "$H/mesh_admit.lock"; flock 7; adm=0      # admission turn (the other worker may hold it while its cartesianMesh starts)
  for i in $(seq 360); do
    ma=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo); df_=$(df -BG --output=avail / | tail -1 | tr -dc 0-9)
    [ "$ma" -ge 12500 ] && [ "$df_" -ge 12 ] && { adm=1; break; }; sleep 60
  done
  [ $adm = 1 ] || { echo "$(date +%F_%T) $lab mesh NOT admitted: resource wait expired after $(( $(date +%s)-tw )) s (MemAvailable $ma MB < 12500 or disk $df_ GB < 12), not meshed" >> runs.log; exit 1; }
  echo "$(date +%F_%T) $lab mesh admitted (MemAvailable $ma MB, disk $df_ GB, waited $(( $(date +%s)-tw )) s)" >> runs.log
  cm_age() {   # elapsed s of the cartesianMesh process below pid $1 (empty if none yet)
    local c q; for c in $(pgrep -x cartesianMesh); do q=$c; while [ -n "$q" ] && [ "$q" -gt 1 ] && [ "$q" != "$1" ]; do q=$(ps -o ppid= -p "$q" | tr -d ' '); done; [ "$q" = "$1" ] && { ps -o etimes= -p "$c" | tr -d ' '; return; }; done
  }
  t1=$(date +%s)
  env $menv nice -n 10 python3 $P5/build_m1_mesh.py "$PKD" --geom="$G" --out="$M" $var > logs/mesh_$lab.log 2>&1 7>&- & mp=$!
  while kill -0 $mp 2> /dev/null; do a=$(cm_age $mp); [ -n "$a" ] && [ "$a" -ge 120 ] && break; sleep 5; done
  flock -u 7; exec 7>&-                                               # admission released: cartesianMesh has run 120 s (its memory is visible) or the builder exited
  wait $mp; rcm=$?
  echo "$(date +%F_%T) $lab mesh rc=$rcm $(( $(date +%s)-t1 )) s ${menv}" >> runs.log
fi
[ -f "$M/constant/polyMesh/boundary" ] || exit 1
python3 $P5/fix_patch_types.py "$M" > logs/patchtypes_$lab.log 2>&1; rcp=$?
echo "$(date +%F_%T) $lab patchtypes rc=$rcp" >> runs.log
[ $rcp -eq 0 ] || exit 1
SR="$G/surface_radius_${scan}_${kind}.csv"
[ -f "$SR" ] || { echo "$(date +%F_%T) $lab NO $SR (d34 not run)" >> runs.log; exit 1; }
nice -n 10 python3 $P5/d34_generic.py "$scan" "$PKD" "$M" "$G/gates.json" "$SR" "$M/d34.json" > logs/d34_$lab.log 2>&1; rcd=$?
echo "$(date +%F_%T) $lab d34 rc=$rcd total $(( $(date +%s)-t0 )) s" >> runs.log
exit $rcd
