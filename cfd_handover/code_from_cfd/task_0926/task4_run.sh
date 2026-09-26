#!/bin/bash
# usage: TASK4_EXCLUSIVE_OK=1 task4_run.sh [NSTEPS=300]   Isolated timing run of the sten60 pulsatile case on 8 cores (design: task4_design.md v1.3).
# Refuses unless: queue4 finished and no queue/solver process (work order line 196), the operator reserved the host (TASK4_EXCLUSIVE_OK=1), Windows side idle (powershell.exe).
# Operator overrides (the run is then contended=unknown, i.e. INVALID for Task 4): TASK4_ALLOW_WINDOWS_LOAD=1 (logs the offenders), TASK4_ALLOW_NO_WINDOWS_CHECK=1 (powershell.exe unavailable).
# Watchdogs: TASK4_MAX_RUNTIME_S (default 5400, from launch), TASK4_NOPROGRESS_S (default 900, no new 'Time =' line); both -> bounded stop, run INVALID.
# Test hooks (shim tests ONLY; defaults = real run): TASK4_SRC, TASK4_ROOT, TASK4_SKIP_FOAM_ENV=1, TASK4_SKIP_PREREQ=1 (skips the queue4.log check and the process/load guards;
# TASK4_MIN_LOAD_CHECK=0 skips only the process/load guards), TASK4_QUEUE_LOG, TASK4_POWERSHELL, TASK4_WIN_CHECK_S (default 10), TASK4_WIN_EVERY_S (default 60),
# TASK4_SAMPLE_S (logger/sampler cadence, default 5), TASK4_STOP_WAIT_S (default 120), TASK4_GRACE_S (SIGTERM grace, default 30), TASK4_POLL_S (default 5).
P=/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot
HERE=$(cd "$(dirname "$0")" && pwd); ISO="$HERE/task4_isolation.py"
SRC=${TASK4_SRC:-/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item6_pulsatile_pilot/sten60_pulsatile}
T=${TASK4_ROOT:-$P/task4}/sten60_timing; N=${1:-300}; STOP_WAIT=${TASK4_STOP_WAIT_S:-120}; POLL=${TASK4_POLL_S:-5}; GRACE=${TASK4_GRACE_S:-30}
MAXRT=${TASK4_MAX_RUNTIME_S:-5400}; NOPROG=${TASK4_NOPROGRESS_S:-900}; SAMPLE=${TASK4_SAMPLE_S:-5}; WINCHK=${TASK4_WIN_CHECK_S:-10}; WINEVERY=${TASK4_WIN_EVERY_S:-60}
QLOG=${TASK4_QUEUE_LOG:-$P/u3d/queue4.log}
MP=""; ML=""; SP=""; END_REASON=""; RC=""; BOUNDED=none; STOP_EDIT=no; LAUNCHED=no; T0=""
fail() { echo "FAIL: $*" >&2; [ -n "$END_REASON" ] || END_REASON="refused: $*"; exit 1; }
now() { date +%s; }
session_pids() { [ -n "$MP" ] && ps -e -o pid=,sid= | awk -v s="$MP" '$2==s {print $1}'; }   # the owned group = mpirun's own session (setsid), incl. ranks that changed pgid
stop_session() {   # bounded: SIGTERM to every member of the owned session, poll ALL survivors for GRACE s, SIGKILL survivors of that session only
    local pids t0; pids=$(session_pids); [ -n "$pids" ] || return 0
    echo "stopping the owned session $MP (SIGTERM): $(echo $pids)" >&2; kill -TERM $pids 2>/dev/null; BOUNDED=SIGTERM
    t0=$(now); while [ -n "$(session_pids)" ] && [ $(( $(now) - t0 )) -lt "$GRACE" ]; do sleep 1; done
    pids=$(session_pids); if [ -n "$pids" ]; then echo "SIGKILL to survivors: $(echo $pids)" >&2; kill -KILL $pids 2>/dev/null; BOUNDED=SIGKILL; fi
    t0=$(now); while [ -n "$(session_pids)" ] && [ $(( $(now) - t0 )) -lt 10 ]; do sleep 1; done
}
write_status() {   # run_status.json: how the run ended (read by task4_analyse.py)
    [ -d "$T" ] && [ "$LAUNCHED" = yes ] || return 0
    TD="$T" END_REASON="$END_REASON" RC="$RC" BOUNDED="$BOUNDED" STOP_EDIT="$STOP_EDIT" MP="$MP" N="$N" T0="$T0" T1="$(now)" \
    STEPS="$(grep -c '^Time = ' "$T/log.pimpleFoam" 2>/dev/null)" LEFT="$(echo $(session_pids))" python3 -c 'import json, os; e = os.environ
json.dump(dict(end_reason=e["END_REASON"], mpirun_rc=int(e["RC"]) if e["RC"].lstrip("-").isdigit() else None, bounded_stop=e["BOUNDED"], stop_edit_applied=e["STOP_EDIT"] == "yes",
  mpirun_pid_and_sid=int(e["MP"]) if e["MP"] else None, steps_requested=int(e["N"]), steps_in_log=int(e["STEPS"] or 0), launch_epoch=int(e["T0"] or 0), end_epoch=int(e["T1"]),
  survivors_of_owned_session=e["LEFT"].split(), controlled_end=e["END_REASON"] in ("stop_honoured", "endTime") and e["BOUNDED"] == "none" and e["RC"] == "0"),
  open(os.path.join(e["TD"], "run_status.json"), "w"), indent=1)' || echo "WARNING: run_status.json not written" >&2
}
cleanup() {        # EXIT trap: stop the owned session, the logger and the sampler; keep the failure status; write run_status.json
    local rc=$?; trap - EXIT INT TERM; trap '' INT TERM
    [ -n "$MP" ] && [ -n "$(session_pids)" ] && { [ -n "$END_REASON" ] || END_REASON="runner_exit_rc$rc"; stop_session; }
    for p in $ML $SP; do kill "$p" 2>/dev/null; done
    for p in $ML $SP; do t=0; while kill -0 "$p" 2>/dev/null && [ $t -lt 10 ]; do sleep 1; t=$((t+1)); done; kill -KILL "$p" 2>/dev/null; done
    if [ -z "$RC" ] && [ -n "$MP" ] && ! kill -0 "$MP" 2>/dev/null; then wait "$MP" 2>/dev/null; RC=$?; fi   # mpirun's own status (dead: bounded)
    write_status
    case "$END_REASON" in stop_honoured|endTime) [ "$BOUNDED" = none ] && [ "$RC" = 0 ] && exit "$rc";; esac
    [ "$rc" -ne 0 ] && exit "$rc"; exit 1
}
trap cleanup EXIT
trap 'END_REASON=${END_REASON:-interrupted_SIGINT}; exit 130' INT
trap 'END_REASON=${END_REASON:-interrupted_SIGTERM}; exit 143' TERM

[ ! -e "$T" ] || fail "$T exists"
# --- prerequisites (work order line 196: Task 4 only after Tasks 0-3; the running queue precludes launch) ---
if [ "${TASK4_SKIP_PREREQ:-0}" != 1 ]; then
    grep -Eq '(^| )queue4 finished$' "$QLOG" 2>/dev/null || fail "$QLOG has no 'queue4 finished' line: the Tasks 0-3 queue is not finished"
fi
if [ "${TASK4_SKIP_PREREQ:-0}" != 1 ] && [ "${TASK4_MIN_LOAD_CHECK:-1}" != 0 ]; then
    SELF=" $$ "; p=$$; while [ "$p" -gt 1 ] 2>/dev/null; do p=$(ps -o ppid= -p "$p" | tr -d ' '); SELF="$SELF$p "; done   # own shell and its ancestors are never offenders
    offenders() { pgrep -a "$@" | while read -r pid rest; do [[ "$SELF" == *" $pid "* ]] || echo "  pid $pid: $rest"; done; }
    OFF1=$(offenders -x "simpleFoam|pimpleFoam|mpirun|orted|cartesianMesh|blockMesh|checkMesh|reconstructPar|decomposePar|snappyHexMesh")
    OFF2=$(offenders -f "run_set.*\.sh|queue.*\.sh|post_case\.sh|m1_probes\.py|u3d_make_csv\.py|reconstructPar")
    [ -z "$OFF1$OFF2" ] || fail "host busy; solver/mesher processes:"$'\n'"${OFF1:-  none}"$'\n'"launcher/queue/heavy post-processing jobs:"$'\n'"${OFF2:-  none}"
    LOAD=$(cut -d' ' -f1 /proc/loadavg); awk -v l="$LOAD" 'BEGIN{exit !(l<1.5)}' || fail "1-min load average $LOAD >= 1.5"
else
    LOAD="$(cut -d' ' -f1 /proc/loadavg) (TEST MODE: prerequisite/busy-host/load guards skipped)"
fi
[ "${TASK4_EXCLUSIVE_OK:-0}" = 1 ] || fail "set TASK4_EXCLUSIVE_OK=1 only after the coordinator has announced the exclusive interval (no Linux or Windows job may start until the run ends)"
[ "$(df --output=avail -B1G / | tail -1 | tr -dc 0-9)" -ge 10 ] || fail "less than 10 GB free"
# --- Windows side (invisible to Linux tools) ---
WPRE=$(mktemp); python3 "$ISO" winprecheck "$WPRE" "$WINCHK"; wrc=$?
case $wrc in
    0) ;;
    3) [ "${TASK4_ALLOW_WINDOWS_LOAD:-0}" = 1 ] || { cat "$WPRE" >&2; rm -f "$WPRE"; fail "Windows-side load (offenders above); override TASK4_ALLOW_WINDOWS_LOAD=1 makes the run contended=unknown"; }
       echo "WARNING: Windows-side load overridden by TASK4_ALLOW_WINDOWS_LOAD=1: contended=unknown" >&2;;
    *) [ "${TASK4_ALLOW_NO_WINDOWS_CHECK:-0}" = 1 ] || { cat "$WPRE" >&2; rm -f "$WPRE"; fail "Windows check unavailable (TASK4_POWERSHELL=${TASK4_POWERSHELL:-powershell.exe}); override TASK4_ALLOW_NO_WINDOWS_CHECK=1 makes the run contended=unknown"; }
       echo "WARNING: no Windows check (TASK4_ALLOW_NO_WINDOWS_CHECK=1): contended=unknown" >&2;;
esac
[ "${TASK4_SKIP_FOAM_ENV:-0}" = 1 ] || source /usr/lib/openfoam/openfoam2406/etc/bashrc
cp -a "$SRC" "$T" || fail "copy failed"; mv "$WPRE" "$T/windows_prerun.json"
# old run outputs are removed ONLY inside the fresh copy $T = <task4 root>/sten60_timing (a real directory, not a symlink); decompose.log is kept (cell count)
[ -d "$T" ] && [ ! -L "$T" ] && [ "$(basename "$T")" = sten60_timing ] && [ "$(cd "$T" && pwd -P)" = "$(cd "${TASK4_ROOT:-$P/task4}" && pwd -P)/sten60_timing" ] \
    || fail "copy path $T is not <task4 root>/sten60_timing: nothing removed"
rm -rf "$T"/postProcessing "$T"/log.* "$T"/run_co5.log "$T"/smoketest.log
for d in "$T"/processor*; do   # every time directory (decimal, integer, scientific notation) and any other entry except 0 and constant
    [ -d "$d" ] && [ ! -L "$d" ] || fail "$d is not a real directory"
    find "$d" -mindepth 1 -maxdepth 1 ! -name 0 ! -name constant -exec rm -rf -- {} + || fail "cleanup of $d failed"
done
[ -s "$T/decompose.log" ] || fail "decompose.log missing"
for d in "$T"/processor*; do ls "$d" | grep -qx 0 || fail "$d has no 0"; done
[ "$(ls -d $T/processor* | wc -l)" -eq 8 ] || fail "not 8 processor directories"
sed -i -e 's/^startFrom .*/startFrom       startTime;/' -e 's/^startTime .*/startTime       0;/' -e 's/^stopAt .*/stopAt          endTime;/' -e 's/^writeInterval .*/writeInterval   100;/' "$T/system/controlDict"
grep -E "^(startFrom|startTime|stopAt|endTime|deltaT|adjustTimeStep|maxCo|maxDeltaT|writeInterval)" "$T/system/controlDict" > "$T/controls_used.txt"
{ date; uptime; lscpu | grep -E "Model name|Core|Thread|Socket"; echo "load at start $LOAD"; } > "$T/host_before.txt"
cd "$T" || fail "cd $T"
# --- launch in an own session: mpirun's PID is the session id of every rank ---
setsid mpirun -np 8 --bind-to core --map-by core --report-bindings pimpleFoam -parallel > log.pimpleFoam 2> mpirun_bindings.txt &
MP=$!; LAUNCHED=yes; T0=$(now)
t=0; until [ "$(ps -o sid= -p "$MP" 2>/dev/null | tr -d ' ')" = "$MP" ] || [ $t -ge 50 ]; do sleep 0.1; t=$((t+1)); done
[ "$(ps -o sid= -p "$MP" 2>/dev/null | tr -d ' ')" = "$MP" ] || { RC=""; END_REASON="launch: mpirun is not its own session leader"; kill -TERM "$MP" 2>/dev/null; fail "$END_REASON"; }
write_status   # early record (end_reason empty = running), holds the session id for a manual `kill -TERM -- -$MP` if the runner itself is SIGKILLed
# light memory logger: every SAMPLE s, epoch and summed RSS (MB) of all pimpleFoam processes; exits by itself when mpirun is gone
( while kill -0 "$MP" 2>/dev/null; do echo "$(date +%s) $(ps -C pimpleFoam -o rss= | awk '{s+=$1} END{printf "%.1f", s/1024}')"; sleep "$SAMPLE"; done ) > mem.log &
ML=$!
python3 "$ISO" sample "$MP" $$ "$T" "$SAMPLE" "$WINEVERY" 2> sampler.err &
SP=$!
# --- wait for N steps; bounded by the watchdogs ---
C=0; LASTC=0; LASTT=$(now)
while :; do
    C=$(grep -c '^Time = ' log.pimpleFoam 2>/dev/null); C=${C:-0}
    [ "$C" -ge "$N" ] && break
    kill -0 "$MP" 2>/dev/null || break
    [ "$C" -gt "$LASTC" ] && { LASTC=$C; LASTT=$(now); }
    if [ $(( $(now) - T0 )) -ge "$MAXRT" ]; then END_REASON="watchdog_max_runtime(${MAXRT}s, $C steps)"; break; fi
    if [ $(( $(now) - LASTT )) -ge "$NOPROG" ]; then END_REASON="watchdog_no_progress(${NOPROG}s without a new step, $C steps)"; break; fi
    sleep "$POLL"
done
if [ -n "$END_REASON" ]; then
    echo "WARNING: $END_REASON: bounded stop; the timing run is INVALID" >&2; stop_session
elif kill -0 "$MP" 2>/dev/null; then
    # stop at the end of the current step WITHOUT writing fields (noWriteNow, OpenFOAM v2406 Time.C: endTime_ = value(), writeTime_ untouched)
    sed -i 's/^stopAt .*/stopAt          noWriteNow;/' system/controlDict; STOP_EDIT=yes
    t0=$(now); while kill -0 "$MP" 2>/dev/null && [ $(( $(now) - t0 )) -lt "$STOP_WAIT" ]; do sleep 1; done
    if kill -0 "$MP" 2>/dev/null || [ -n "$(session_pids)" ]; then
        END_REASON="stop_ignored(${STOP_WAIT}s after noWriteNow)"; echo "WARNING: $END_REASON" >&2; stop_session
    else END_REASON=stop_honoured; fi
fi
if kill -0 "$MP" 2>/dev/null; then RC=""; echo "WARNING: mpirun $MP survived SIGKILL" >&2; else wait "$MP"; RC=$?; fi   # bounded: never wait on a live process
if [ -z "$END_REASON" ]; then     # mpirun ended before N steps without our stop
    if [ "$RC" = 0 ] && tail -5 log.pimpleFoam | grep -qx 'End'; then END_REASON=endTime; else END_REASON="solver_exited_early(rc $RC, $C steps)"; fi
fi
[ -z "$(session_pids)" ] || stop_session      # e.g. mpirun gone, ranks left
for p in $ML $SP; do t=0; while kill -0 "$p" 2>/dev/null && [ $t -lt 30 ]; do sleep 1; t=$((t+1)); done; done   # both end by themselves (mpirun gone); cleanup kills stragglers
python3 "$ISO" winprecheck windows_postrun.json "$WINCHK" > /dev/null; true
python3 "$ISO" evidence "$T"
{ date; uptime; echo "mpirun rc $RC"; echo "end $END_REASON; bounded stop $BOUNDED"; } > host_after.txt
echo "finished rc=$RC steps=$(grep -c '^Time = ' log.pimpleFoam) end=$END_REASON bounded_stop=$BOUNDED"
case "$END_REASON" in stop_honoured|endTime) [ "$BOUNDED" = none ] && [ "$RC" = 0 ] && exit 0;; esac
echo "FAIL: run not ended by the controlled stop ($END_REASON, bounded stop $BOUNDED, rc $RC): the timing run is INVALID" >&2; exit 1
