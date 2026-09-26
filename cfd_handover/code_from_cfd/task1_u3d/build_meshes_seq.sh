#!/bin/bash
cd $(dirname $0); for L in "$@"; do ( time nice -n 10 python3 make_sten70_mesh.py $L mesh_$L ) > log.mesh_$L 2>&1; echo "$L rc=$?" >> mesh_builds.log; done
