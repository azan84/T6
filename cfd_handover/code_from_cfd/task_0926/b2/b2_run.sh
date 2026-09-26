#!/bin/bash
# Task B2 (work order 2026-09-26): uncontended throughput layouts on scan-14 baseline, resistance mode:  L16 = ONE 16-rank job;  L8x2 = TWO 8-rank jobs side by side on disjoint physical cores.
# usage: B2_EXCLUSIVE_OK=1 b2_run.sh <L16|L8x2>       (the jobs run under an umbrella b2_jobs.sh started with setsid: every solver process of the run belongs to its session U)
# Prepared by b2_prepare.sh (cases b2/L16/case, b2/L8/caseA, b2/L8/caseB, decomposed, no field writes; endTime 1600 set by the coordinator after b2_prepare.sh (which writes 1400): the runner refuses any other value). Analysis: b2_analyse.py (settle iteration by the B1 rule, wall clock to it, solves per hour).
# Refuses unless: operator reserved the host (B2_EXCLUSIVE_OK=1), no simpleFoam/mpirun/mesher/queue process, load < 1.5, >= 10 GB free, Windows side idle (powershell.exe; overrides
#   B2_ALLOW_WINDOWS_LOAD=1 / B2_ALLOW_NO_WINDOWS_CHECK=1 are recorded and make the evidence 'unknown'; the measured Windows background is stated in isolation_evidence.json).
# Bounded: B2_MAX_RUNTIME_S (default 14400) and B2_NOPROGRESS_S (default 900: no new 'Time =' line in ANY job log) -> bounded stop (SIGTERM, grace, SIGKILL of the session's survivors), run marked INVALID.
# Total solver ranks are 16 in both layouts (work order 09-24 section 6). Test hooks (shim tests only): B2_ROOT, B2_SKIP_FOAM_ENV=1, B2_SKIP_PREREQ=1, B2_POWERSHELL (= TASK4_POWERSHELL), B2_SAMPLE_S, B2_WIN_CHECK_S, B2_WIN_EVERY_S, B2_STOP_GRACE_S, B2_POLL_S, B2_MPIRUN.
P=/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot
HERE=$(cd "$(dirname "$0")" && pwd); ISO="$HERE/b2_isolation.py"; B=${B2_ROOT:-$P/b2}; LAYOUT=${1:-}
MAXRT=${B2_MAX_RUNTIME_S:-14400}; NOPROG=${B2_NOPROGRESS_S:-900}; SAMPLE=${B2_SAMPLE_S:-5}; WINCHK=${B2_WIN_CHECK_S:-10}; WINEVERY=${B2_WIN_EVERY_S:-60}; GRACE=${B2_STOP_GRACE_S:-30}; POLL=${B2_POLL_S:-5}
MPIRUN=${B2_MPIRUN:-mpirun}; export TASK4_POWERSHELL=${B2_POWERSHELL:-${TASK4_POWERSHELL:-powershell.exe}}
export B2_COMM=simpleFoam; export B2_NRANKS=16
SP=""; U=""; END_REASON=""; BOUNDED=none; LAUNCHED=no; T0=""; JOBRC=()
fail() { echo "FAIL: $*" >&2; [ -n "$END_REASON" ] || END_REASON="refused: $*"; exit 1; }
now() { date +%s; }
session_pids() { [ -n "$U" ] && ps -e -o pid=,sid= | awk -v s="$U" '$2==s {print $1}'; }          # the owned group = the umbrella's session (all jobs of this run)
stop_session() {   # bounded: SIGTERM every member of the session (except this runner), poll ALL survivors for GRACE s, SIGKILL survivors only
    local pids t0; pids=$(session_pids); [ -n "$pids" ] || return 0
    echo "stopping the owned session $U (SIGTERM): $(echo $pids)" >&2; kill -TERM $pids 2>/dev/null; BOUNDED=SIGTERM
    t0=$(now); while [ -n "$(session_pids)" ] && [ $(( $(now) - t0 )) -lt "$GRACE" ]; do sleep 1; done
    pids=$(session_pids); if [ -n "$pids" ]; then echo "SIGKILL to survivors: $(echo $pids)" >&2; kill -KILL $pids 2>/dev/null; BOUNDED=SIGKILL; fi
    t0=$(now); while [ -n "$(session_pids)" ] && [ $(( $(now) - t0 )) -lt 10 ]; do sleep 1; done
}
write_status() {
    [ "$LAUNCHED" = yes ] || return 0
    TD="$OUT" END_REASON="$END_REASON" BOUNDED="$BOUNDED" LAYOUT="$LAYOUT" T0="$T0" T1="$(now)" RCS="${JOBRC[*]}" LEFT="$(echo $(session_pids))" python3 -c 'import json, os; e = os.environ
rcs = [int(x) if x.lstrip("-").isdigit() else None for x in e["RCS"].split()]
json.dump(dict(layout=e["LAYOUT"], end_reason=e["END_REASON"], bounded_stop=e["BOUNDED"], job_exit_codes=rcs, launch_epoch=int(e["T0"] or 0), end_epoch=int(e["T1"]), survivors_of_owned_session=e["LEFT"].split(),
  controlled_end=(e["END_REASON"] == "all_jobs_finished" and e["BOUNDED"] == "none" and bool(rcs) and all(r == 0 for r in rcs))), open(os.path.join(e["TD"], "run_status.json"), "w"), indent=1)' || echo "WARNING: run_status.json not written" >&2
}
cleanup() {        # EXIT trap: stop the owned session and the sampler, keep the failure status, write run_status.json
    local rc=$?; trap - EXIT INT TERM; trap '' INT TERM
    [ "$LAUNCHED" = yes ] && [ -n "$(session_pids)" ] && { [ -n "$END_REASON" ] || END_REASON="runner_exit_rc$rc"; stop_session; }
    [ -n "$SP" ] && { kill "$SP" 2>/dev/null; t=0; while kill -0 "$SP" 2>/dev/null && [ $t -lt 10 ]; do sleep 1; t=$((t+1)); done; kill -KILL "$SP" 2>/dev/null; }
    write_status
    [ "$END_REASON" = all_jobs_finished ] && [ "$BOUNDED" = none ] && [ "$rc" -eq 0 ] && exit 0
    [ "$rc" -ne 0 ] && exit "$rc"; exit 1
}
trap cleanup EXIT
trap 'END_REASON=${END_REASON:-interrupted_SIGINT}; exit 130' INT
trap 'END_REASON=${END_REASON:-interrupted_SIGTERM}; exit 143' TERM

case "$LAYOUT" in L16) CASES=("$B/L16/case"); NPJ=16;; L8x2) CASES=("$B/L8/caseA" "$B/L8/caseB"); NPJ=8;; *) fail "usage: b2_run.sh <L16|L8x2>";; esac
OUT="$B/results_$LAYOUT"; [ ! -e "$OUT" ] || fail "$OUT exists (a layout is measured once; move it aside to repeat)"
[ "${B2_EXCLUSIVE_OK:-0}" = 1 ] || fail "set B2_EXCLUSIVE_OK=1 only after the coordinator has announced the exclusive interval (no other Linux or Windows job may start until the run ends)"
for c in "${CASES[@]}"; do
    [ -d "$c" ] || fail "$c missing (run b2_prepare.sh)"; n=$(ls -d "$c"/processor* 2>/dev/null | wc -l); [ "$n" -eq "$NPJ" ] || fail "$c has $n processor directories, expected $NPJ"
    grep -q "^endTime *1600;" "$c/system/controlDict" || fail "$c/system/controlDict: endTime is not 1600 (budget: B1 settle iteration 1229 + 30 %; the coordinator edits the prepared cases)"
    for d in "$c"/processor*; do [ -d "$d/0" ] && [ -d "$d/constant/polyMesh" ] || fail "$d incomplete"; ls "$d" | grep -Eq '^[0-9]' && [ "$(ls "$d" | grep -Ec '^[0-9.e+-]+$')" -eq 1 ] || fail "$d holds time directories other than 0"; done
    [ ! -e "$c/log.simpleFoam" ] || fail "$c/log.simpleFoam exists"
done
if [ "${B2_SKIP_PREREQ:-0}" != 1 ]; then
    SELF=" $$ "; p=$$; while [ "$p" -gt 1 ] 2>/dev/null; do p=$(ps -o ppid= -p "$p" | tr -d ' '); SELF="$SELF$p "; done
    offenders() { pgrep -a "$@" | while read -r pid rest; do [[ "$SELF" == *" $pid "* ]] || echo "  pid $pid: $rest"; done; }
    OFF1=$(offenders -x "simpleFoam|pimpleFoam|mpirun|orted|cartesianMesh|blockMesh|checkMesh|reconstructPar|decomposePar|snappyHexMesh"); OFF2=$(offenders -f "run_set.*\.sh|queue.*\.sh|post_case\.sh|m1_probes\.py|u3d_make_csv\.py|reconstructPar|task4_run\.sh")
    [ -z "$OFF1$OFF2" ] || fail "host busy; solver/mesher processes:"$'\n'"${OFF1:-  none}"$'\n'"launcher/queue/heavy post-processing jobs:"$'\n'"${OFF2:-  none}"
    LOAD=$(cut -d' ' -f1 /proc/loadavg); awk -v l="$LOAD" 'BEGIN{exit !(l<1.5)}' || fail "1-min load average $LOAD >= 1.5"
else LOAD="$(cut -d' ' -f1 /proc/loadavg) (TEST MODE: guards skipped)"; fi
[ "$(df --output=avail -B1G / | tail -1 | tr -dc 0-9)" -ge 10 ] || fail "less than 10 GB free"
mkdir -p "$OUT" || fail "cannot create $OUT"
python3 "$ISO" winprecheck "$OUT/windows_prerun.json" "$WINCHK" > "$OUT/winprecheck.out" 2>&1; wrc=$?
case $wrc in
    0) ;;
    3) [ "${B2_ALLOW_WINDOWS_LOAD:-0}" = 1 ] || { cat "$OUT/winprecheck.out" >&2; fail "Windows-side load (see above); override B2_ALLOW_WINDOWS_LOAD=1 records it and makes the evidence 'unknown'"; }
       export TASK4_ALLOW_WINDOWS_LOAD=1; python3 "$ISO" winprecheck "$OUT/windows_prerun.json" 1 > /dev/null 2>&1; echo "WARNING: Windows-side load overridden (B2_ALLOW_WINDOWS_LOAD=1): contended=unknown" >&2;;
    *) [ "${B2_ALLOW_NO_WINDOWS_CHECK:-0}" = 1 ] || { cat "$OUT/winprecheck.out" >&2; fail "Windows check unavailable; override B2_ALLOW_NO_WINDOWS_CHECK=1"; }
       echo "WARNING: no Windows check: contended=unknown" >&2;;
esac
[ "${B2_SKIP_FOAM_ENV:-0}" = 1 ] || source /usr/lib/openfoam/openfoam2406/etc/bashrc
{ date; uptime; lscpu | grep -E "Model name|Core|Thread|Socket"; echo "layout $LAYOUT; load at start $LOAD"; } > "$OUT/host_before.txt"
# --- launch: the umbrella b2_jobs.sh is the session leader U of every job (per-rank taskset to one physical core each, b2_rank.sh) ---
setsid "$HERE/b2_jobs.sh" "$LAYOUT" "$OUT" > "$OUT/jobs.log" 2>&1 &
U=$!; LAUNCHED=yes; T0=$(now)
t=0; until [ "$(ps -o sid= -p "$U" 2>/dev/null | tr -d ' ')" = "$U" ] || [ $t -ge 50 ]; do sleep 0.1; t=$((t+1)); done
[ "$(ps -o sid= -p "$U" 2>/dev/null | tr -d ' ')" = "$U" ] || { END_REASON="launch: the umbrella is not its own session leader"; kill -TERM "$U" 2>/dev/null; fail "$END_REASON"; }
python3 "$ISO" sample "$U" "$$" "$OUT" "$SAMPLE" "$WINEVERY" 2> "$OUT/sampler.err" &
SP=$!
echo "$(date +%T) launched $LAYOUT: umbrella/session $U"
# --- wait: all jobs finished, bounded by the watchdogs ---
LASTSUM=0; LASTT=$(now)
while :; do
    kill -0 "$U" 2>/dev/null || break
    SUM=0; for c in "${CASES[@]}"; do k=$(grep -c '^Time = ' "$c/log.simpleFoam" 2>/dev/null); SUM=$((SUM + ${k:-0})); done
    [ "$SUM" -gt "$LASTSUM" ] && { LASTSUM=$SUM; LASTT=$(now); }
    if [ $(( $(now) - T0 )) -ge "$MAXRT" ]; then END_REASON="watchdog_max_runtime(${MAXRT}s)"; break; fi
    if [ $(( $(now) - LASTT )) -ge "$NOPROG" ]; then END_REASON="watchdog_no_progress(${NOPROG}s without a new step in any job)"; break; fi
    sleep "$POLL"
done
[ -z "$END_REASON" ] || { echo "WARNING: $END_REASON: bounded stop; the run is INVALID" >&2; stop_session; }
if kill -0 "$U" 2>/dev/null; then JOBRC=(); echo "WARNING: umbrella $U survived the stop" >&2; else wait "$U" 2>/dev/null; JOBRC=($(awk '{print $2}' "$OUT/job_rc.txt" 2>/dev/null)); fi          # bounded: never wait on a live process
if [ -z "$END_REASON" ]; then
    ok=yes; [ "${#JOBRC[@]}" -eq "${#CASES[@]}" ] || ok=no; for k in "${!CASES[@]}"; do [ "${JOBRC[$k]:-x}" = 0 ] && tail -5 "${CASES[$k]}/log.simpleFoam" | grep -qx 'End' || ok=no; done
    if [ "$ok" = yes ]; then END_REASON=all_jobs_finished; else END_REASON="job_exited_early(rc ${JOBRC[*]})"; fi
fi
[ -z "$(session_pids)" ] || stop_session
t=0; while kill -0 "$SP" 2>/dev/null && [ $t -lt 30 ]; do sleep 1; t=$((t+1)); done
python3 "$ISO" winprecheck "$OUT/windows_postrun.json" "$WINCHK" > /dev/null 2>&1; true
cat "${CASES[@]/%//mpirun_bindings.txt}" > "$OUT/mpirun_bindings.txt" 2>/dev/null
python3 "$ISO" evidence "$OUT"
{ date; uptime; echo "layout $LAYOUT; end $END_REASON; bounded stop $BOUNDED; job rc ${JOBRC[*]}"; } > "$OUT/host_after.txt"
for c in "${CASES[@]}"; do echo "$c: $(grep -c '^Time = ' $c/log.simpleFoam) steps, $(grep -E 'ExecutionTime' $c/log.simpleFoam | tail -1)"; done
[ "$END_REASON" = all_jobs_finished ] && [ "$BOUNDED" = none ] && exit 0
echo "FAIL: run not finished normally ($END_REASON, bounded stop $BOUNDED): INVALID" >&2; exit 1
