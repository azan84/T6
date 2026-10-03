#!/bin/bash
# Task B job (WORK-ORDER-2026-10-03 section 3): re-run one U3D level with fields kept, record the jet state (u3d_verdict.py, rule of U3D_CHECK_DESIGN.md: rule of 2026-10-01 extended 2026-10-03, unsettled -> inconclusive), analyse.
# usage: u3d_job.sh <level S25B|S12A|S12B|S50|S25A> [ranks=8] ; the case u3d/case_<level> must exist (built with U3D_END = the original budget), be audited, and be FRESH (only the 0 time dir, no postProcessing, no processor*).
# Every step is checked; any failure -> '<date> FAILED: <reason>' in u3d_check/run_<L>.status (+ job_status FAILED in result_<L>.json if it exists), exit 1, fields kept.
# The processor* directories are removed ONLY after: solve rc 0 + exact 'End' line, reconstructPar rc 0 + reconstructed <endTime> dir == last 'Time =' of the log, jet_offset rc 0 and parsed,
# result_<L>.json written, post_level.sh (analysis + shared CSV row, serialised by flock on u3d/U3D_sten70_work.csv.lock) rc 0. The last line of the status file is 'DONE ...' only on full success.
# Equivalence: the re-run uses <ranks> ranks and a re-generated mesh (originals: 16 ranks); the evidence about the ORIGINAL state is the FFR reproduction within 1e-4 + the jet state, not decomposition identity.
# Overrides (tests only): U3D_ROOT, U3D_FOAM_BASHRC, U3D_JET_OFFSET, U3D_VERDICT, U3D_LOCK_WAIT_S, U3D_DRYRUN_STOP (non-empty: stop with rc 0 before decomposePar).
set -u
L=${1:-}; NP=${2:-8}; M=${U3D_ROOT:-/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot}; U=$M/u3d; C=$U/case_$L; O=$M/u3d_check; S=$O/run_$L.status; R=$O/result_$L.json
HERE=$(dirname "$(readlink -f "$0")"); VERDICT=${U3D_VERDICT:-$HERE/u3d_verdict.py}; JET=${U3D_JET_OFFSET:-/home/azan/paper6_t6_work/jet_offset.py}
case $L in S50|S25A|S25B|S12A|S12B) ;; *) echo "usage: u3d_job.sh <S25B|S12A|S12B|S50|S25A> [ranks]" >&2; exit 2;; esac
[[ $NP =~ ^[1-9][0-9]*$ ]] || { echo "ranks must be a positive integer" >&2; exit 2; }
mkdir -p "$O" || exit 2
finished=0
st() { echo "$(date '+%F %T') $*" >> "$S"; }
fail() { st "FAILED: $*"; [ -f "$R" ] && python3 "$VERDICT" set-status "$R" FAILED "$*"; finished=1; exit 1; }
trap '[ $finished -eq 1 ] || { st "FAILED: unexpected exit (signal or shell error) at line $LINENO"; [ -f "$R" ] && python3 "$VERDICT" set-status "$R" FAILED "unexpected exit"; }' EXIT
trap 'exit 143' TERM INT HUP
st "job start level=$L ranks=$NP (re-run: $NP ranks + re-generated mesh; originals 16 ranks: evidence on the original state = FFR within 1e-4 + jet state, not decomposition identity)"
[ -f "$R" ] && { mv -f "$R" "$R.prev.$(date +%s)" || fail "cannot move the old $R aside"; }
# The OpenFOAM v2406 bashrc reads unset variables (line 177: WM_PROJECT_SITE): under `set -u` that kills the shell (failure of 2026-10-03 15:24),
# and it also has commands returning non-zero (fatal under set -e), so -e/-u/pipefail are suspended ONLY around the source and restored right after
# ($- read directly: a $(set +o) snapshot runs in a subshell, where bash clears errexit; `|| :` on the pipefail snapshot: `shopt -po` returns 1 when pipefail is off,
# which would kill a `set -e` shell before the options are suspended). `set --` first: a bare source passes the job's "$@" (S25B 8) to the bashrc as settings/files.
set -- ; fo=$-; fp=$(shopt -po pipefail || :); set +eu +o pipefail; source "${U3D_FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}"; rc=$?; eval "$fp"; [[ $fo == *e* ]] && set -e; [[ $fo == *u* ]] && set -u
[ $rc -eq 0 ] || fail "cannot source the OpenFOAM bashrc (rc=$rc)"
for t in decomposePar simpleFoam reconstructPar mpirun; do command -v $t > /dev/null || fail "$t not on PATH after sourcing the OpenFOAM bashrc"; done
[ -n "${U3D_DRYRUN_STOP:-}" ] && { st "dry run: environment sourced (WM_PROJECT_VERSION=${WM_PROJECT_VERSION:-unset}), fresh-case gate next"; }
cd "$C" || fail "no case dir $C"

# fresh-case gate: a previous run's time dirs / monitors / processor dirs would make the later checks vacuous (OpenFOAM appends surfaceFieldValue_<t>.dat)
ET=$(sed -n 's/^[[:space:]]*endTime[[:space:]]\+\([0-9]\+\)[[:space:]]*;.*/\1/p' system/controlDict)
[[ $ET =~ ^[0-9]+$ ]] || fail "cannot read an integer endTime from system/controlDict (got '$ET')"
BI=$(python3 -c "import json; print(json.load(open('build_info.json'))['endTime'])" 2>/dev/null) || fail "build_info.json has no endTime"
[ "$BI" = "$ET" ] || fail "endTime controlDict $ET != build_info.json $BI"
stale=$(ls -d [0-9]* processor* postProcessing log.simpleFoam log.reconstructPar 2>/dev/null | grep -vx 0)
[ -z "$stale" ] || fail "case not fresh, remove first: $(echo $stale)"
[ -d 0 ] || fail "no 0 directory"

[ -n "${U3D_DRYRUN_STOP:-}" ] && { finished=1; st "dry run: stop before decomposePar"; exit 0; }
st "decompose ($NP)"
sed -i "s/^numberOfSubdomains .*/numberOfSubdomains $NP;/" system/decomposeParDict && grep -q "^numberOfSubdomains *$NP;" system/decomposeParDict || fail "decomposeParDict edit failed"
decomposePar -force > log.decomposePar 2>&1 || fail "decomposePar rc=$? (log.decomposePar)"
for ((i = 0; i < NP; i++)); do [ -d processor$i ] || fail "decomposePar: processor$i missing"; done
[ ! -e processor$NP ] || fail "decomposePar: more than $NP processor dirs"

st "solve start"
mpirun -np "$NP" --bind-to none simpleFoam -parallel > log.simpleFoam 2>&1; rc=$?
st "solve end rc=$rc"
[ $rc -eq 0 ] || fail "simpleFoam rc=$rc"
grep -qx 'End' log.simpleFoam || fail "log.simpleFoam has no exact 'End' line"
LT=$(sed -n 's/^Time = \([0-9]\+\)$/\1/p' log.simpleFoam | tail -1)
[ "$LT" = "$ET" ] || fail "last 'Time =' of log.simpleFoam is '$LT', endTime is $ET"

st "reconstruct"
reconstructPar -latestTime > log.reconstructPar 2>&1 || fail "reconstructPar rc=$? (log.reconstructPar)"
grep -qx 'End' log.reconstructPar || fail "log.reconstructPar has no exact 'End' line"
for f in U p phi; do [ -s "$ET/$f" ] || fail "reconstructed field $C/$ET/$f missing or empty"; done
NEWEST=$(ls -d [0-9]* | sort -n | tail -1)
[ "$NEWEST" = "$ET" ] || fail "newest time dir is $NEWEST, expected $ET"
touch case.foam || fail "cannot touch case.foam"

st "jet offset"
python3 "$JET" "$C" > "$O/jet_offset_$L.txt" 2> "$O/jet_offset_$L.err" || fail "jet_offset.py rc=$? ($O/jet_offset_$L.err)"
python3 "$VERDICT" result --level "$L" --case "$C" --jet "$O/jet_offset_$L.txt" --ranks "$NP" --out "$R" > "$O/verdict_$L.txt" 2>&1 || fail "u3d_verdict.py: $(tail -1 "$O/verdict_$L.txt")"
[ -s "$R" ] || fail "result file $R not written"
st "verdict: $(head -1 "$O/verdict_$L.txt")"

st "post_level (waits for the shared-CSV lock)"
( cd "$U" && flock -w "${U3D_LOCK_WAIT_S:-7200}" "$U/U3D_sten70_work.csv.lock" bash post_level.sh "$L" unknown ) > "$O/post_$L.txt" 2>&1 || fail "post_level.sh rc=$? ($O/post_$L.txt)"

# all results written: only now the decomposed copies go (the reconstructed fields stay)
rm -rf processor* || fail "purging processor* failed"
[ -z "$(ls -d processor* 2>/dev/null)" ] || fail "processor* dirs still present after purge"
python3 "$VERDICT" set-status "$R" DONE || fail "cannot write job_status DONE into $R"
finished=1
st "DONE $(python3 -c "import json; d = json.load(open('$R')); print('verdict', d['verdict'], 'FFR %.6f' % d['FFR_last100_mean'], 'dFFR %+.2e' % d['dFFR'])")"
exit 0
