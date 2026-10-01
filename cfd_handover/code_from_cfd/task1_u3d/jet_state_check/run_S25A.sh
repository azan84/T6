#!/bin/bash
# U3D jet-state check, second level (design U3D_CHECK_DESIGN.md: "if (a) holds for S50: the same for S25A, U3D_END=4000"): mesh, case (8 ranks), solve, reconstruct, jet offset.
U=/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d; O=/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check; S=$O/run_S25A.status
cd $U || exit 2; export OMP_NUM_THREADS=8
echo "$(date '+%F %T') mesh" >> $S; bash build_mesh_bg.sh S25A; tail -1 mesh_builds.log >> $S
U3D_END=4000 python3 build_sten70_case.py S25A 8 >> $S 2>&1 || { echo "case build failed" >> $S; exit 3; }
source /usr/lib/openfoam/openfoam2406/etc/bashrc; cd $U/case_S25A || exit 2
decomposePar -force > log.decomposePar 2>&1 || { echo "decompose failed" >> $S; exit 3; }
echo "$(date '+%F %T') solve start" >> $S
mpirun -np 8 --bind-to none simpleFoam -parallel > log.simpleFoam 2>&1; rc=$?
echo "$(date '+%F %T') solve end rc=$rc" >> $S
reconstructPar -latestTime > log.reconstructPar 2>&1; touch case.foam
python3 /home/azan/paper6_t6_work/jet_offset.py $U/case_S25A > $O/jet_offset_S25A.txt 2>&1
echo "$(date '+%F %T') DONE" >> $S
