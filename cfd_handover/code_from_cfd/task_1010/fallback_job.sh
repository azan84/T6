#!/bin/bash
# WO 2026-10-10 D15 pool job: pimpleFoam time-average fallback of ONE steady solve that did not settle (pimple_fallback.py README). Style and safety model of case_job.sh.
# usage: fallback_job.sh <steady_case> <Task> <name> [ranks=16]
#   <steady_case>  finished steady case (wo1010/cases/<solve>; reconstructed endTime fields, log.simpleFoam complete); only read
#   <Task>         TaskT | TaskG | TaskM | TaskT2 | TaskN: the steady return is RET/<Task>/<basename steady_case>/ (settle_<L>_<M>.csv, M1_results.csv), the fallback return RET/<Task>/<name>/
#   <name>         the transient case wo1010/cases/<name> (convention <steady solve>_pimple) and the pool job name
# Steps:
#   flock -n wo1010/cases/.<name>.fallback.lock (held for the whole job, inherited by the solver; a second invocation is refused, exit 3)
#   -> disk gate (free disk of the cases filesystem >= DISK_NEED_GB (default 6) + 8 GB reserve, else exit 5)
#   -> settle csv: exactly one RET/<Task>/<steady>/settle_*.csv
#   -> BUILD if wo1010/cases/<name> does not exist: `pimple_fallback.py build ... --settle <csv>`, which REFUSES unless the B1/D8 trigger says NOT_SETTLED (the steady case's .case_job.lock is held
#      (flock -n) during the build, so a steady case that a case_job.sh is (re)running is refused); the build log is kept as <case>/log.fallback_build
#      STALE REFUSAL if the case exists: build_info.json present with flag PIMPLE_FALLBACK, built from THIS steady case with nproc == ranks, no BUILD_FAILED, NOT_FOR_PRODUCTION only in test mode,
#      no time directory other than 0 in the case root (this workflow never reconstructs), processor dirs either none or exactly processor0..ranks-1
#   -> decomposePar (only when no processor dir exists, or when the last decomposePar did not End and no processor holds a time > 0) -> exactly <ranks> processor dirs
#   -> LOOP: `pimple_fallback.py resume-point` (latest time complete in every processor dir; later partial times moved to <case>/_partial_<stamp>/; controlDict endTime = T_run, startFrom latestTime)
#            exit 0: log.pimpleFoam rotated to log.pimpleFoam.<k>, mpirun -np <ranks> pimpleFoam -parallel > log.pimpleFoam; success only if rc 0, the log ends with an exact End after its last Time
#                    line, no FOAM FATAL, and resume-point then reports the run AT T_run (exit 10)
#            exit 10: the run stands at T_run -> `pimple_fallback.py window`: 0 STATIONARY (leave the loop), 10 EXTENDED (T_run += 0.25 T_decl, state + controlDict written: run again),
#                     11 NOT_STATIONARY_AT_CAP (leave the loop; the result will be INCOMPLETE, flag WINDOW_NOT_STATIONARY)
#   -> analyse into RET/<Task>/<name>/ (--label L of the settle file, --steady-results RET/<Task>/<steady>/M1_results.csv when present); exit 0 = COMPLETE, 6 = INCOMPLETE
#   -> COMPLETE only: processor dirs purged (du/df printed), <case>/fallback_done.json written. No reconstructPar: analyse reads only the monitors (postProcessing/), which stay with 0/, constant/,
#      system/, log.* and window_state.json. INCOMPLETE: nothing purged, exit 6.
# RESUME: every failure or interruption (signal, crash, pool restart, reboot, mpirun rc != 0) leaves the case resumable: re-run the SAME command (pool: remove jobs/<name>.status after checking the log).
#   The run continues from the latest time written in every processor dir (writeInterval T_decl/64, purgeWrite 2), the window_state.json (T_run, extensions, decisions) is the source of truth,
#   and a decision already taken is never re-taken. A job that finished COMPLETE is not run again (fallback_done.json: exit 0 with a message); one that finished INCOMPLETE re-analyses and exits 6.
# Exit codes: 0 COMPLETE (or already complete), 1 failure/refusal (resumable), 2 usage, 3 locked, 5 not enough disk, 6 finished INCOMPLETE (window not stationary at the cap / not for production), 130/143 INT/TERM.
# TEST HOOKS (NOT_FOR_PRODUCTION; never set by `pimple_fallback.py make-job`): FALLBACK_TEST_FORCE=TEXT builds an untriggered case (--force-untriggered TEXT), FALLBACK_TEST_WINDOW_S=T replaces T_decl
#   (--window-override-s), FALLBACK_TEST_ZONE=id,id adds zone monitors next to the box ones; the last two need FALLBACK_TEST_FORCE. FALLBACK_CASE_ROOT, FALLBACK_RET_ROOT, FALLBACK_SETTLE_CSV relocate
#   the case root / return root / settle csv (tests under audit_tmp). A case built with a test hook is refused without FALLBACK_TEST_FORCE, and never COMPLETE.
[ $# -ge 3 ] && [ $# -le 4 ] || { echo "usage: fallback_job.sh <steady_case> <Task> <name> [ranks=16]"; exit 2; }
STEADY=$(cd "$1" 2>/dev/null && pwd) || { echo "no steady case dir $1"; exit 2; }
TASK=$2; NAME=$3; NP=${4:-16}
[[ "$TASK" =~ ^Task[A-Za-z0-9]+$ ]] || { echo "bad Task '$TASK'"; exit 2; }
[[ "$NAME" =~ ^[A-Za-z0-9_.-]+$ ]] || { echo "bad name '$NAME'"; exit 2; }
[[ "$NP" =~ ^[1-9][0-9]*$ ]] && [ "$NP" -le 16 ] || { echo "bad ranks '$NP' (1..16, work order rank cap)"; exit 2; }
H=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); PF=$H/pimple_fallback.py
CASE_ROOT=${FALLBACK_CASE_ROOT:-$H/cases}; RET_ROOT=${FALLBACK_RET_ROOT:-/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-10}
CASE=$CASE_ROOT/$NAME; OUT=$RET_ROOT/$TASK/$NAME; SRET=$RET_ROOT/$TASK/$(basename "$STEADY")
NEED=${DISK_NEED_GB:-6}; RESERVE_GB=8
[[ "$NEED" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "bad DISK_NEED_GB '$NEED'"; exit 2; }
TEST=${FALLBACK_TEST_FORCE:-}; WOVR=${FALLBACK_TEST_WINDOW_S:-}; ZT=${FALLBACK_TEST_ZONE:-}
[ -z "$WOVR$ZT" ] || [ -n "$TEST" ] || { echo "REFUSED: FALLBACK_TEST_WINDOW_S / FALLBACK_TEST_ZONE are test hooks and need FALLBACK_TEST_FORCE"; exit 2; }
[ -z "$TEST" ] || echo "TEST MODE (NOT_FOR_PRODUCTION): force '$TEST', window override '${WOVR:-none}', zone test '${ZT:-none}'"
# OpenFOAM environment: as case_job.sh (set -- first, -e/-u/pipefail suspended only around the source)
set -- ; fo=$-; fp=$(shopt -po pipefail || :); set +eu +o pipefail; source "${CASE_JOB_FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}"; rc=$?; eval "$fp"; [[ $fo != *e* ]] || set -e; [[ $fo != *u* ]] || set -u
[ $rc -eq 0 ] || { echo "FAILED: cannot source the OpenFOAM bashrc (rc $rc)"; exit 1; }
for t in decomposePar pimpleFoam mpirun changeDictionary; do command -v $t > /dev/null || { echo "FAILED: $t not on PATH after sourcing the OpenFOAM bashrc"; exit 1; }; done
[ "${WM_PROJECT_VERSION:-}" = v2406 ] || { echo "FAILED: WM_PROJECT_VERSION is '${WM_PROJECT_VERSION:-unset}', expected v2406"; exit 1; }

CHILD=""
fail() { echo "$(date '+%F %T') FAILED: $*"; exit 1; }
kill_child() {   # as case_job.sh: TERM (mpirun forwards it to its ranks), KILL after 60 s
  [ -n "$CHILD" ] && kill -0 "$CHILD" 2> /dev/null || return 0
  kill -TERM "$CHILD" 2> /dev/null; local i
  for i in $(seq 600); do kill -0 "$CHILD" 2> /dev/null || break; sleep 0.1; done
  kill -0 "$CHILD" 2> /dev/null && { pkill -KILL -P "$CHILD" 2> /dev/null; kill -KILL "$CHILD" 2> /dev/null; }
  wait "$CHILD" 2> /dev/null; CHILD=""
}
run_child() { "$@" & CHILD=$!; wait "$CHILD"; local rc=$?; CHILD=""; return $rc; }
on_signal() { trap '' INT TERM; exec 1>&8 2>&8; echo "$(date '+%F %T') FAILED: received SIG$1, stopping the running command (the case stays resumable: re-run the same command)"; kill_child; exit "$2"; }
on_exit() { local rc=$?; trap - EXIT; trap '' INT TERM; exec 1>&8 2>&8; kill_child; exit $rc; }
exec 8>&1
trap 'on_signal INT 130' INT; trap 'on_signal TERM 143' TERM; trap on_exit EXIT

# ---- ownership
mkdir -p "$CASE_ROOT" || fail "cannot create $CASE_ROOT"
exec 9> "$CASE_ROOT/.$NAME.fallback.lock" || fail "cannot open the lock file"
flock -n 9 || { echo "REFUSED: $NAME is locked by another fallback_job.sh invocation ($CASE_ROOT/.$NAME.fallback.lock)"; exit 3; }

# ---- disk gate (READ-ONLY)
free_kb() { df -Pk -- "$CASE_ROOT" | awk 'NR == 2 { print $4 }'; }
gb() { awk -v k="$1" 'BEGIN { printf "%.2f", k / 1048576 }'; }
FREE0=$(free_kb); [[ "$FREE0" =~ ^[0-9]+$ ]] || fail "cannot read the free disk of $CASE_ROOT (df)"
NEED_KB=$(awk -v n="$NEED" -v r="$RESERVE_GB" 'BEGIN { printf "%d", (n + r) * 1048576 }')
[ "$FREE0" -ge "$NEED_KB" ] || { echo "REFUSED: $(gb "$FREE0") GB free on the filesystem of $CASE_ROOT, need DISK_NEED_GB $NEED + reserve $RESERVE_GB GB"; exit 5; }
echo "$(date '+%F %T') disk gate OK: $(gb "$FREE0") GB free >= DISK_NEED_GB $NEED + reserve $RESERVE_GB GB"

# ---- trigger input: the steady solve's settle csv
if [ -n "${FALLBACK_SETTLE_CSV:-}" ]; then SETTLE=$FALLBACK_SETTLE_CSV; else
  SL=("$SRET"/settle_*.csv); [ ${#SL[@]} -eq 1 ] && [ -f "${SL[0]}" ] || fail "expected exactly one settle_*.csv in $SRET, found: ${SL[*]}"; SETTLE=${SL[0]}
fi
[ -f "$SETTLE" ] || fail "settle csv $SETTLE missing"
SMODE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["mode"])' "$STEADY/build_info.json") || fail "cannot read the steady build_info.json"
LABEL=$(basename "$SETTLE" .csv); LABEL=${LABEL#settle_}; LABEL=${LABEL%_"$SMODE"}
echo "$(date '+%F %T') steady $STEADY ($SMODE), settle $SETTLE, label $LABEL, case $CASE, return $OUT, ranks $NP"

# ---- build or stale refusal
if [ ! -e "$CASE" ]; then
  if [ -e "$STEADY/.case_job.lock" ]; then   # the steady case is only read: its lock file is used when case_job.sh created one, never created here
    exec 7< "$STEADY/.case_job.lock" || fail "cannot open $STEADY/.case_job.lock"
    flock -n 7 || fail "the steady case $STEADY is locked by a running case_job.sh: refused"
  fi
  BARGS=(build "$STEADY" "$CASE" --settle "$SETTLE" --nproc "$NP")
  [ -z "$TEST" ] || BARGS+=(--force-untriggered "$TEST"); [ -z "$WOVR" ] || BARGS+=(--window-override-s "$WOVR"); [ -z "$ZT" ] || BARGS+=(--zone-test "$ZT")
  echo "$(date '+%F %T') build: python3 pimple_fallback.py ${BARGS[*]}"
  BLOG=$CASE_ROOT/.$NAME.build.log
  OMP_NUM_THREADS=4 run_child nice -n 5 python3 "$PF" "${BARGS[@]}" > "$BLOG" 2>&1; brc=$?
  exec 7<&- 2> /dev/null
  tail -3 "$BLOG"
  if [ -d "$CASE" ]; then mv "$BLOG" "$CASE/log.fallback_build"; fi
  [ $brc -eq 0 ] || fail "build refused/failed (rc $brc; log $( [ -d "$CASE" ] && echo "$CASE/log.fallback_build" || echo "$BLOG"))"
fi
cd "$CASE" || fail "no case dir $CASE"
SMSG=$(python3 - "$CASE" "$STEADY" "$NP" "$TEST" 2>&1 <<'EOF'
import json, os, re, sys
c, steady, np_, test = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
if os.path.exists(f"{c}/BUILD_FAILED"): sys.exit(f"{c}/BUILD_FAILED exists (half-built case): move the case away first")
if not os.path.exists(f"{c}/build_info.json"): sys.exit(f"{c} exists without build_info.json (half-built): move it away first")
b = json.load(open(f"{c}/build_info.json"))
if b.get("flag") != "PIMPLE_FALLBACK": sys.exit(f"{c} is not a PIMPLE_FALLBACK case")
if os.path.realpath(b.get("steady_case", "")) != os.path.realpath(steady): sys.exit(f"{c} was built from {b.get('steady_case')}, not {steady}")
if int(b.get("nproc", -1)) != np_: sys.exit(f"{c} was built for {b.get('nproc')} ranks, not {np_}")
nfp = os.path.exists(f"{c}/NOT_FOR_PRODUCTION")
if nfp and not test: sys.exit(f"{c} is NOT_FOR_PRODUCTION (test build) and this is not a test invocation")
if not os.path.exists(f"{c}/window_state.json"): sys.exit(f"{c}/window_state.json missing")
bad = []
for n in os.listdir(c):
    try: v = float(n)
    except ValueError: continue
    if os.path.isdir(f"{c}/{n}") and v != 0: bad.append(n)
if bad: sys.exit(f"time directories {sorted(bad)} in the case root (this workflow never reconstructs): stale, refused")
pr = sorted(n for n in os.listdir(c) if re.fullmatch(r"processor\d+", n))
if pr and sorted(pr) != sorted(f"processor{i}" for i in range(np_)): sys.exit(f"processor dirs {pr} do not match {np_} ranks")
print(f"case consistent: built {b.get('built')} from {steady}, nproc {np_}, production_ready {b.get('production_ready')}, {len(pr)} processor dirs")
EOF
) || fail "stale/consistency check: $SMSG"
echo "$(date '+%F %T') $SMSG"
if [ -f fallback_done.json ]; then echo "$(date '+%F %T') already COMPLETE (fallback_done.json: $(tr -d '\n' < fallback_done.json | cut -c1-200)); nothing to do"; exit 0; fi

# ---- decompose
ND=$(ls -d processor[0-9]* 2> /dev/null | wc -l)
latest_any() { local d s m=0; for d in processor[0-9]*; do for s in "$d"/*; do s=${s##*/}; [[ "$s" =~ ^[-+]?([0-9]+[.]?[0-9]*|[.][0-9]+)([eE][-+]?[0-9]+)?$ ]] && awk -v a="$s" 'BEGIN { exit !(a > 0) }' && m=1; done; done; echo $m; }
if [ "$ND" -gt 0 ] && ! grep -qx End log.decomposePar 2> /dev/null; then
  [ "$(latest_any)" = 0 ] || fail "log.decomposePar has no End but processor dirs hold solved times: inconsistent, refused"
  echo "$(date '+%F %T') previous decomposePar did not finish and nothing was solved: decomposing again"; ND=0
fi
if [ "$ND" -eq 0 ]; then
  echo "$(date '+%F %T') decomposePar ($NP subdomains)"
  run_child nice -n 5 decomposePar -force > log.decomposePar 2>&1 || fail "decomposePar failed, see log.decomposePar"
  grep -qx End log.decomposePar || fail "log.decomposePar has no exact 'End' line"
  ND=$(ls -d processor[0-9]* 2> /dev/null | wc -l)
fi
[ "$ND" -eq "$NP" ] || fail "$ND processor dirs, expected $NP"

# ---- run / resume / window loop
NOTSTAT=0
while :; do
  RP=$(python3 "$PF" resume-point "$CASE" "$NP" 2>&1); rrc=$?
  echo "$(date '+%F %T') resume-point (rc $rrc): $RP"
  if [ $rrc -eq 0 ]; then
    k=1; while [ -e "log.pimpleFoam.$k" ]; do k=$((k + 1)); done
    [ ! -e log.pimpleFoam ] || mv log.pimpleFoam "log.pimpleFoam.$k" || fail "cannot rotate log.pimpleFoam"
    echo "$(date '+%F %T') pimpleFoam start ($NP ranks)"
    run_child mpirun -np "$NP" --bind-to none --mca mpi_yield_when_idle 1 pimpleFoam -parallel > log.pimpleFoam 2>&1; rc=$?
    echo "$(date '+%F %T') pimpleFoam end rc=$rc"
    [ $rc -eq 0 ] || fail "mpirun pimpleFoam rc $rc (see log.pimpleFoam); resumable: re-run the same command"
    awk '{ sub(/\r$/, "") } /^Time = / { t = NR } $0 == "End" { e = NR } index($0, "FOAM FATAL") { f = 1 } END { exit !(t && e > t && !f) }' log.pimpleFoam || fail "log.pimpleFoam does not end with End after its last Time line (or has FOAM FATAL); resumable"
    python3 "$PF" resume-point "$CASE" "$NP" > /dev/null 2>&1; [ $? -eq 10 ] || fail "pimpleFoam ended (rc 0) but the latest complete time is not T_run; resumable"
    continue
  fi
  [ $rrc -eq 10 ] || fail "resume-point refused (rc $rrc)"
  WM=$(python3 "$PF" window "$CASE" 2>&1); wrc=$?
  echo "$(date '+%F %T') $WM"
  case $wrc in
    0) break;;
    10) continue;;
    11) NOTSTAT=1; break;;
    *) fail "window decision failed (rc $wrc)";;
  esac
done

# ---- analyse
mkdir -p "$OUT" || fail "cannot create $OUT"
AARGS=(analyse "$CASE" "$OUT" --label "$LABEL"); [ ! -f "$SRET/M1_results.csv" ] || AARGS+=(--steady-results "$SRET/M1_results.csv")
python3 "$PF" "${AARGS[@]}" > log.analyse 2>&1; arc=$?
cat log.analyse
[ $arc -eq 0 ] || [ $arc -eq 6 ] || fail "analyse failed (rc $arc, log.analyse)"
if [ $arc -eq 6 ]; then
  echo "$(date '+%F %T') FINISHED INCOMPLETE$( [ $NOTSTAT = 1 ] && echo ': WINDOW_NOT_STATIONARY at the cap (2 T_decl)'); result in $OUT; processor dirs KEPT"; exit 6
fi

# ---- COMPLETE: purge the decomposed run (the monitors are the result), mark done
PD=(processor[0-9]*); [ "${#PD[@]}" -eq "$NP" ] && [ -d "${PD[0]}" ] || fail "expected $NP processor dirs before the purge, found ${#PD[@]}: nothing purged"
DU=$(du -skc -- "${PD[@]}" | tail -1 | cut -f1); FREE1=$(free_kb)
rm -rf -- "${PD[@]}"; [ "$(ls -d processor[0-9]* 2> /dev/null | wc -l)" -eq 0 ] || fail "purge incomplete"
python3 - "$CASE" "$OUT" <<'EOF' || fail "cannot write fallback_done.json"
import json, os, sys, datetime
c, o = sys.argv[1], sys.argv[2]; st = json.load(open(f"{c}/window_state.json"))
d = dict(status="COMPLETE", finished=datetime.datetime.now().isoformat(timespec="seconds"), T_run_s=st["T_run_s"], window_final=st["final"], return_dir=o)
open(f"{c}/.fallback_done.json.tmp", "w").write(json.dumps(d, indent=1) + "\n"); os.replace(f"{c}/.fallback_done.json.tmp", f"{c}/fallback_done.json")
EOF
echo "$(date '+%F %T') PURGED: $NP processor dirs, disk released $(gb "$DU") GB (df free $(gb "$FREE1") -> $(gb "$(free_kb)") GB)"
echo "$(date '+%F %T') OK: COMPLETE (window STATIONARY), result in $OUT"
