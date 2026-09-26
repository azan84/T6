#!/bin/bash
# usage: build_mesh_bg.sh <level>   (mesh + gates only; no solver)
cd $(dirname $0); L=$1
( time nice -n 10 python3 make_sten70_mesh.py $L mesh_$L ) > log.mesh_$L 2>&1; echo "$L rc=$?" >> mesh_builds.log
