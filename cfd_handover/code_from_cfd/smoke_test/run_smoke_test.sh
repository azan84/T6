#!/bin/bash
# Smoke test (Task B3, work order 2026-09-26): a second machine proves it reproduces one returned result in well under 30 minutes.
# Case: Stage A sten70 (70 % diameter stenosis, straight tapered vessel), A5 coarse mesh (198,252 cells), steady laminar simpleFoam, coded resistance outlet (R = 6.974826e9 Pa s/m3, fixed relax 0.2), 2000 iterations.
# Returned result it reproduces: outlet flow 1.17392231e-06 m3/s (stageA_A5_ladders.csv, A5 sten70 coarse; also reference_result.json of this folder from a fresh run of THIS script).
# usage: ./run_smoke_test.sh [NPROC=8] [WORKDIR=./smoke_work]      needs: OpenFOAM ESI v2406 (source $FOAM_BASHRC, default /usr/lib/openfoam/openfoam2406/etc/bashrc; cartesianMesh = cfMesh is part of it; wmake + g++ for the coded BC), OpenMPI, python3 + numpy.
# PASS = complete run (End, 2000 iterations, 2000 finite rows per monitor), same mesh (STL sha256, checkMesh OK, exactly 2 wall->patch rewrites, cells EQUAL to the reference) and outlet flow within 0.1 % of reference_result.json (and of the returned value), see compare_smoke.py.
# Timing claim: about 10 minutes on 8 PHYSICAL cores of a workstation (see reference_result.json); the 30-minute claim needs 8 physical cores (NPROC > physical cores is refused unless SMOKE_ALLOW_FEWER_CORES=1).
# env: WRITE_REFERENCE=1 = reference run: step 6 writes $HERE/reference_result.json from this run (no comparison; only if the run is complete and the mesh checks hold) and exits 0; without it, reference_result.json must exist (checked before any expensive step).
#      GEN = path of make_stageA_geometry.py (default $HERE/../stageA/make_stageA_geometry.py); OMP_NUM_THREADS (default 8) for cartesianMesh (cfMesh cell count depends on the thread count).
#      SMOKE_ALLOW_FEWER_CORES=1: allow NPROC > physical cores (a warning; the timing claim does not hold).
# writes <WORKDIR>/smoke_checks.json: stl_sha256, checkMesh_ok, cells, patch_rewrites, omp_num_threads (read by compare_smoke.py).
# exit codes: 0 PASS (or reference written); 1 FAIL (flow criterion); 2 setup error (preflight: python3/numpy, OpenFOAM commands, wmake/g++, NPROC, physical cores; workdir, reference file, geometry generator missing);
#             3 NON-COMPARABLE: geometry/mesh step failed, STL hash differs, checkMesh failed, patch rewrite not exactly 2, different cell count, or run incomplete (never PASS); 4 simpleFoam failed.
set -u
HERE=$(cd "$(dirname "$0")" && pwd); NP=${1:-8}; W=${2:-$HERE/smoke_work}
FOAM_BASHRC=${FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}; GEN=${GEN:-$HERE/../stageA/make_stageA_geometry.py}; REF="$HERE/reference_result.json"
STL_SHA256=47178798e1052ddb7d23d8b318a934baaf42d93d5555b9568eddcabdf9ef8ef2
if [ "${WRITE_REFERENCE:-0}" = 1 ]; then echo "WRITE_REFERENCE=1: reference run, step 6 writes $REF (no comparison)"
else [ -f "$REF" ] || { echo "no reference: $REF missing. Run once with WRITE_REFERENCE=1 to write it (reference machine), or copy the reference_result.json of the reference machine here"; exit 2; }; fi
[ -f "$GEN" ] || { echo "geometry generator not found: $GEN (copy the folder stageA/ next to smoke_test/, or set GEN=<path of make_stageA_geometry.py>)"; exit 2; }
# --- preflight (exit 2, nothing expensive has run) ---
[[ "$NP" =~ ^[1-9][0-9]*$ ]] || { echo "preflight: NPROC '$NP' is not a positive integer"; exit 2; }
command -v python3 > /dev/null || { echo "preflight: python3 not found"; exit 2; }
python3 -c "import numpy" 2> /dev/null || { echo "preflight: python3 cannot import numpy (pip install numpy)"; exit 2; }
[ -f "$FOAM_BASHRC" ] || { echo "OpenFOAM v2406 bashrc not found: $FOAM_BASHRC (set FOAM_BASHRC)"; exit 2; }
source "$FOAM_BASHRC" || exit 2
for c in cartesianMesh checkMesh decomposePar mpirun simpleFoam; do command -v "$c" > /dev/null || { echo "preflight: $c not found after sourcing $FOAM_BASHRC"; exit 2; }; done
for c in wmake g++; do command -v "$c" > /dev/null || { echo "preflight: $c not found (needed to compile the coded resistance BC)"; exit 2; }; done
PHYS=$(lscpu -p=CORE,SOCKET 2> /dev/null | grep -v '^#' | sort -u | wc -l); [ "${PHYS:-0}" -gt 0 ] 2> /dev/null || PHYS=$(nproc)
if [ "$NP" -gt "$PHYS" ]; then
    [ "${SMOKE_ALLOW_FEWER_CORES:-0}" = 1 ] || { echo "preflight: NPROC $NP > $PHYS physical cores (set SMOKE_ALLOW_FEWER_CORES=1 to run anyway)"; exit 2; }
    echo "WARNING: the 30-minute claim needs 8 physical cores (NPROC $NP, physical cores $PHYS)"
elif [ "$PHYS" -lt 8 ] || [ "$NP" -lt 8 ]; then echo "WARNING: the 30-minute claim needs 8 physical cores (NPROC $NP, physical cores $PHYS)"; fi
[ ! -e "$W" ] || { echo "$W exists: remove it or choose another WORKDIR"; exit 2; }
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-8}
T0=$(date +%s); step() { echo "$(date +%T) [+$(( $(date +%s) - T0 )) s] $*"; }
SHA=""; CHK_OK=null; CELLS=null; REWRITES=null
write_checks() { python3 -c 'import json, sys; a = sys.argv[1:]; j = lambda s: json.loads(s)
json.dump(dict(stl_sha256=a[0] or None, stl_sha256_expected=a[1], checkMesh_ok=j(a[2]), cells=j(a[3]), patch_rewrites=j(a[4]), omp_num_threads=a[5]), open("smoke_checks.json", "w"), indent=1)' \
    "$SHA" "$STL_SHA256" "$CHK_OK" "$CELLS" "$REWRITES" "$OMP_NUM_THREADS"; }
mkdir -p "$W/constant/triSurface" "$W/geo" && cd "$W" || exit 2
step "1/6 geometry (analytic, numpy only): sten70.stl"
python3 "$GEN" geo --ds 70 > log.geometry 2>&1 || { echo "geometry failed, see $W/log.geometry"; exit 3; }
mv geo/sten70.stl constant/triSurface/sten70.stl; rm -rf geo; sha256sum constant/triSurface/sten70.stl | tee stl.sha256; SHA=$(cut -d' ' -f1 stl.sha256)
[ "$SHA" = "$STL_SHA256" ] || { write_checks; echo "NON-COMPARABLE: STL sha256 $SHA != expected $STL_SHA256"; exit 3; }
cp -r "$HERE/case_files/0" "$HERE/case_files/system" "$HERE/case_files/constant" . 2>/dev/null; mv system/decomposeParDict.template system/decomposeParDict; sed -i "s/@NPROC@/$NP/" system/decomposeParDict
step "2/6 mesh (cfMesh cartesianMesh, 4 boundary layers, OMP_NUM_THREADS=$OMP_NUM_THREADS)"; cartesianMesh > log.cartesianMesh 2>&1 || { write_checks; echo "cartesianMesh failed, see $W/log.cartesianMesh"; exit 3; }
step "3/6 checkMesh"; checkMesh > log.checkMesh 2>&1; CRC=$?; grep -E "cells:|Mesh OK|Failed" log.checkMesh | head -5
CELLS=$(grep -m1 -E "^\s*cells:\s+[0-9]+" log.checkMesh | tr -dc 0-9); CELLS=${CELLS:-null}
if [ $CRC -eq 0 ] && grep -q "Mesh OK" log.checkMesh; then CHK_OK=true; else CHK_OK=false; write_checks; echo "NON-COMPARABLE: checkMesh failed (rc $CRC, 'Mesh OK' $(grep -q 'Mesh OK' log.checkMesh && echo present || echo absent)), see $W/log.checkMesh"; exit 3; fi
# cfMesh writes the inlet and outlet patches as type wall in constant/polyMesh/boundary: patch types must be 'patch' for inlet and outlet (exactly one rewrite each, reported)
RW=$(python3 - <<'PY'
import re
f = "constant/polyMesh/boundary"; s = open(f).read(); n = {}
for p in ("inlet", "outlet"): s, n[p] = re.subn(r"(\b%s\s*\{[^}]*?type\s+)wall(\s*;)" % p, r"\1patch\2", s, flags=re.S)
open(f, "w").write(s); print(n["inlet"], n["outlet"])
PY
); read -r RW_IN RW_OUT <<< "$RW"; echo "wall -> patch rewrites: inlet ${RW_IN:-?}, outlet ${RW_OUT:-?}"
[[ "${RW_IN:-x}${RW_OUT:-x}" =~ ^[0-9]+$ ]] && REWRITES=$(( RW_IN + RW_OUT ))
write_checks
[ "${RW_IN:-}" = 1 ] && [ "${RW_OUT:-}" = 1 ] || { echo "NON-COMPARABLE: wall -> patch rewrites must be exactly 2 (inlet 1, outlet 1): inlet ${RW_IN:-?}, outlet ${RW_OUT:-?}"; exit 3; }
step "4/6 decomposePar ($NP subdomains)"; decomposePar -force > log.decomposePar 2>&1 || { echo "decomposePar failed"; exit 3; }
step "5/6 simpleFoam -parallel (2000 iterations; the coded BC is compiled on first use: about 1-2 minutes)"
mpirun -np "$NP" --bind-to core --map-by core simpleFoam -parallel > log.simpleFoam 2>&1; RC=$?
[ $RC -eq 0 ] || { echo "simpleFoam failed (rc $RC), see $W/log.simpleFoam"; exit 4; }
if [ "${WRITE_REFERENCE:-0}" = 1 ]; then
    step "6/6 write reference"; python3 "$HERE/compare_smoke.py" "$W" "$REF" --wall $(( $(date +%s) - T0 )) --write-reference "$REF"; exit $?
fi
step "6/6 compare"; echo "solver rc=$RC"; python3 "$HERE/compare_smoke.py" "$W" "$REF" --wall $(( $(date +%s) - T0 )); exit $?
