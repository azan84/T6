#!/bin/bash
# flow_state_profile.py on retained sten70 fields (read only; straight tubes along x: the x axis is the centreline, throat x = 30 mm, measurement station x = 56.5 mm):
#   u3d/case_S50 (U3D 3D level, axisymmetric branch), /home/azan/paper6_t6_work/smoke_cont (axisymmetric branch, 12000 it) and /home/azan/paper6_t6_work/a5_arch8 (archived A5 coarse mesh, DEFLECTED branch,
#   B3 diagnosis). Expected under the pre-registered rule (max over the FULL profile, attempt 3): case_S50 has an invalid section at x = 52 mm (s - s_throat = 22 mm: a cut with holes through cfMesh
#   transition polyhedra), so every comparison involving case_S50 is STATES INDETERMINATE (the subset maximum is reported as information only: smoke_cont vs case_S50 small, a5_arch8 vs case_S50 large);
#   a5_arch8 vs smoke_cont (all 26 stations valid in both) is STATES DIFFER: the profile separates the deflected solve from the axisymmetric one.
# Evidence to test_output/flow_state_sten70/. usage: bash tests/test_flow_state_sten70.sh
set -e -o pipefail
TC=$(dirname "$(dirname "$(readlink -f "$0")")"); P=$(dirname "$TC"); EV=$TC/test_output/flow_state_sten70; mkdir -p "$EV"; F="nice -n 10 python3 $TC/flow_state_profile.py"
export OMP_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1
for c in "$P/u3d/case_S50" /home/azan/paper6_t6_work/smoke_cont /home/azan/paper6_t6_work/a5_arch8; do n=$(basename "$c"); $F profile "$c" --straight-x 30 56.5 --label "$n" --out "$EV/$n.csv" | tail -1; done
cd "$EV"
$F compare smoke_cont.csv case_S50.csv --json cmp_smoke_cont_vs_case_S50.json | tee cmp.txt
$F compare a5_arch8.csv case_S50.csv --json cmp_a5_arch8_vs_case_S50.json | tee -a cmp.txt
$F compare a5_arch8.csv smoke_cont.csv --ffr 0.78397 0.78248 --json cmp_a5_arch8_vs_smoke_cont.json | tee -a cmp.txt
grep -q "^STATES INDETERMINATE" <(sed -n 1p cmp.txt) && grep -q "^STATES INDETERMINATE" <(sed -n 2p cmp.txt) && grep -q "^STATES DIFFER" <(sed -n 3p cmp.txt) \
  && echo "PASS: a5_arch8 (deflected) vs smoke_cont (axisymmetric) STATES DIFFER on the full profile; both comparisons with case_S50 INDETERMINATE (invalid x = 52 mm section), never AGREE on a subset"
