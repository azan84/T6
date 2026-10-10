#!/bin/bash
# WO 2026-10-10 (Sol R2 finding 12): write ALL pool jobs of the work order with their order dependencies (one machine; the section 6 two-machine split is not used). Re-runnable and idempotent:
# make_job.py leaves an identical job file untouched, rewrites a changed one only if it has neither a .audited marker nor a .status file (else it refuses that job), and refuses a label whose
# mesh / d34.json / mesh_gates.json / extensions json is missing (e.g. Task N labels not meshed yet): that job is skipped and listed, the others are written; run this script again later.
# NO .audited marker is ever written (the pool starts nothing without one).
# Order (T -> G -> M -> T2 -> N), enforced by `after` + fail-closed gate jobs (task_gate.py; a gate passes only when every expected solve is B1-settled or has a COMPLETE D15 fallback):
#   TaskT  (prio 1): 14_T5n_{resistance,prescribed}, 14_T5w_{resistance,prescribed}, 14_T5n_12p5_resistance          after: none
#   gate_TaskT  (1):  after the five Task T jobs
#   taskG_14_T1regen (2): after gate_TaskT;  gate_TaskG (2): after taskG_14_T1regen
#   TaskM  (prio 3): {138,69,473,139}_T1_{resistance,prescribed}                                                     after: gate_TaskG;   gate_TaskM (3): after the eight
#   TaskT2 (prio 4): {138,473}_{T5n,T5w}_{resistance,prescribed}                                                     after: gate_TaskM;   gate_TaskT2 (4): after the eight
#   TaskN  (prio 5): 306_base_resistance after gate_TaskT2; 306_{T1,T5n,T5w}_{resistance,prescribed} after gate_TaskT2 + 306_base_resistance;  gate_TaskN (5): after the seven
# A gate whose job file names a job that does not exist yet simply waits (the pool starts a job only when every `after` job has status done).
# usage: make_all_jobs.sh        exit 0 = every job written/unchanged; 1 = some job refused (listed)
set -u
H=$(cd "$(dirname "$0")" && pwd); MJ="python3 $H/make_job.py"
W=/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/WO1010; M1=/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/pkg
declare -A PK=(
  [14_T5n]=$W/14_left_LAD_prox_20mm_80ds__T5_vox_narrow__real [14_T5n_12p5]=$W/14_left_LAD_prox_20mm_80ds__T5_vox_narrow__real [14_T5w]=$W/14_left_LAD_prox_20mm_80ds__T5_vox_wide__real
  [138_T1]=$W/138_left_LAD_prox_20mm_70ds__T1_missed_branch__real [69_T1]=$W/69_left_LCX_prox_20mm_65ds__T1_missed_branch__real
  [473_T1]=$W/473_left_LCX_prox_20mm_60ds__T1_missed_branch__real [139_T1]=$W/139_right_RCA_prox_10mm_70ds__T1_missed_branch__real
  [138_T5n]=$W/138_left_LAD_prox_20mm_70ds__T5_vox_narrow__real [138_T5w]=$W/138_left_LAD_prox_20mm_70ds__T5_vox_wide__real
  [473_T5n]=$W/473_left_LCX_prox_20mm_60ds__T5_vox_narrow__real [473_T5w]=$W/473_left_LCX_prox_20mm_60ds__T5_vox_wide__real
  [306_base]=$W/306_left_LAD_prox_20mm_80ds__baseline__real [306_T1]=$W/306_left_LAD_prox_20mm_80ds__T1_missed_branch__real
  [306_T5n]=$W/306_left_LAD_prox_20mm_80ds__T5_vox_narrow__real [306_T5w]=$W/306_left_LAD_prox_20mm_80ds__T5_vox_wide__real)
BAD=()
run() { echo "+ make_job.py ${*:2}" | sed "s|$W/||"; "$@" || BAD+=("${*:2}"); }
solve() { local label=$1 mode=$2 task=$3 prio=$4 after=$5; run $MJ "${PK[$label]}" "$label" "$mode" "$task" "$prio" ${after:+--after "$after"}; }
join() { local IFS=,; echo "$*"; }

T=(14_T5n_resistance 14_T5n_prescribed 14_T5w_resistance 14_T5w_prescribed 14_T5n_12p5_resistance)
solve 14_T5n resistance TaskT 1 ""; solve 14_T5n prescribed TaskT 1 ""; solve 14_T5w resistance TaskT 1 ""; solve 14_T5w prescribed TaskT 1 ""; solve 14_T5n_12p5 resistance TaskT 1 ""
run $MJ gate TaskT 1 --after "$(join "${T[@]}")"
run $MJ taskG 2 --after gate_TaskT
run $MJ gate TaskG 2 --after taskG_14_T1regen

M=(); for l in 138_T1 69_T1 473_T1 139_T1; do for m in resistance prescribed; do solve $l $m TaskM 3 gate_TaskG; M+=(${l}_$m); done; done
run $MJ gate TaskM 3 --after "$(join "${M[@]}")"

T2=(); for l in 138_T5n 138_T5w 473_T5n 473_T5w; do for m in resistance prescribed; do solve $l $m TaskT2 4 gate_TaskM; T2+=(${l}_$m); done; done
run $MJ gate TaskT2 4 --after "$(join "${T2[@]}")"

N=(306_base_resistance); solve 306_base resistance TaskN 5 gate_TaskT2
for l in 306_T1 306_T5n 306_T5w; do for m in resistance prescribed; do solve $l $m TaskN 5 gate_TaskT2,306_base_resistance; N+=(${l}_$m); done; done
run $MJ gate TaskN 5 --after "$(join "${N[@]}")"

if [ ${#BAD[@]} -gt 0 ]; then echo "NOT WRITTEN (${#BAD[@]}; re-run this script when their meshes exist / after resolving the refusal):"; printf '  %s\n' "${BAD[@]}" | sed "s|$W/||"; exit 1; fi
echo "all jobs written or unchanged (no .audited marker created)"
