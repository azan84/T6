#!/bin/bash
# usage: run_case.sh <package_name>   P5 case: geometry (p5/out/<scan>) -> mesh (p5/mesh/<scan>) -> patch types -> D3/D4 distances. One case at a time; nice -n 10, OMP_NUM_THREADS=4. No solver.
# Before the mesh: wait (poll every 60 s, max 3 h) until MemAvailable >= 12.5 GB and free disk >= 12 GB, so the builder's own resource guard (12 GB / 12 GB) does not refuse the case; the guard itself is unchanged.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=4; mkdir -p logs out mesh
pk="$1"; scan="${pk%%_*}"; PKD=/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/P5/$pk
t0=$(date +%s)
nice -n 10 /usr/bin/python3 build_m1_geometry.py "$pk" "out/$scan" > "logs/geometry_$scan.log" 2>&1; rcg=$?; t1=$(date +%s)
echo "$(date +%F_%T) $scan geometry rc=$rcg $((t1-t0)) s" >> runs.log
if [ -f "out/$scan/case.stl" ]; then
  for i in $(seq 180); do
    ma=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo); df_=$(df -BG --output=avail / | tail -1 | tr -dc 0-9)
    [ "$ma" -ge 12500 ] && [ "$df_" -ge 12 ] && break
    [ "$i" = 1 ] && echo "$(date +%F_%T) $scan waiting for resources (MemAvailable ${ma} MB, disk ${df_} GB)" >> runs.log
    sleep 60
  done
  tw=$(date +%s); [ $((tw-t1)) -gt 5 ] && echo "$(date +%F_%T) $scan waited $((tw-t1)) s for resources" >> runs.log
  nice -n 10 python3 build_m1_mesh.py "$pk" > "logs/mesh_$scan.log" 2>&1; rcm=$?; t2=$(date +%s)
  echo "$(date +%F_%T) $scan mesh rc=$rcm $((t2-tw)) s" >> runs.log
  if [ -f "mesh/$scan/constant/polyMesh/boundary" ]; then
    python3 fix_patch_types.py "mesh/$scan" > "logs/patchtypes_$scan.log" 2>&1
    nice -n 10 python3 d34_generic.py "$scan" "$PKD" "mesh/$scan" "out/$scan/gates.json" "out/$scan/surface_radius_${scan}_baseline.csv" "mesh/$scan/d34.json" > "logs/d34_$scan.log" 2>&1
    echo "$(date +%F_%T) $scan d34 rc=$? total $(( $(date +%s)-t0 )) s" >> runs.log
  fi
fi
