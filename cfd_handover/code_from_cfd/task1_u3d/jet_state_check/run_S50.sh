#!/bin/bash
# U3D jet-state check: run the rebuilt S50 (8 ranks, bind-to none, shared host), keep fields, reconstruct the last time, jet offset + FFR.
C=/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S50; O=/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check
source /usr/lib/openfoam/openfoam2406/etc/bashrc; cd $C || exit 2
echo "$(date '+%F %T') decompose" >> $O/run_S50.status
decomposePar -force > log.decomposePar 2>&1 || { echo "decompose failed" >> $O/run_S50.status; exit 3; }
echo "$(date '+%F %T') solve start" >> $O/run_S50.status
mpirun -np 8 --bind-to none simpleFoam -parallel > log.simpleFoam 2>&1; rc=$?
echo "$(date '+%F %T') solve end rc=$rc" >> $O/run_S50.status
reconstructPar -latestTime > log.reconstructPar 2>&1; touch case.foam
python3 /home/azan/paper6_t6_work/jet_offset.py $C > $O/jet_offset_S50.txt 2>&1
echo "$(date '+%F %T') DONE" >> $O/run_S50.status
