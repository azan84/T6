#!/bin/bash
# usage: run_mesh_seq.sh <package> [--tag=..] [--geom=..] [--out=..]   one mesh, niced, threads capped (build_m1_mesh.py applies ulimit -v 9 GB, OMP_NUM_THREADS=4, nice -n 19 inside, resource guard)
cd "$(dirname "$0")"; export OMP_NUM_THREADS=4; mkdir -p logs
lab="${1%%_*}${2:+_${2#--*=}}"
nice -n 10 python3 build_m1_mesh.py "$@" > "logs/log.mesh_${lab}.txt" 2>&1; echo "$(date +%F_%T) $* rc=$?" >> mesh_runs.log
