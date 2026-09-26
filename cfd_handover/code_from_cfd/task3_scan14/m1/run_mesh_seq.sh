#!/bin/bash
# usage: run_mesh_seq.sh <case> [--tag=..]   one mesh, niced, threads capped (build_m1_mesh.py applies ulimit -v 9 GB, OMP_NUM_THREADS=4)
cd "$(dirname "$0")"; export OMP_NUM_THREADS=4
nice -n 19 python3 build_m1_mesh.py "$@" > "log.mesh_$1${2:+_${2#--tag=}}.txt" 2>&1; echo "$1 $2 rc=$?" >> mesh_runs.log
