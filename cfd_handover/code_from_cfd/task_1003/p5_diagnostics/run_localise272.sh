#!/bin/bash
# After B2: extract the wall patch of the P5 272 mesh (read-only use of the mesh; output outside the case) and localise the deleted region.
set +u; source /usr/lib/openfoam/openfoam2406/etc/bashrc
O=/home/azan/paper6_t6_work/opus_sched/post_b2; mkdir -p $O
nice -n 10 surfaceMeshExtract -case /home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/mesh/272 -constant -patches '(wall)' $O/wall272.vtk > $O/log.surfaceMeshExtract 2>&1 || { echo "surfaceMeshExtract failed"; exit 1; }
ls -la $O
nice -n 10 python3 /home/azan/paper6_t6_work/opus_sched/scripts/localise272.py $(ls $O/wall272*.vtk $O/wall272*.vtp 2>/dev/null | head -1) $O/localise272.json
