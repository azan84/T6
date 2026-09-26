#!/bin/bash
cd $(dirname $0); for k in 0 1 2 3; do nice -n 10 python3 build_wedge_case.py $k > log.build_wedge_W$k 2>&1; echo "W$k rc=$?"; done
