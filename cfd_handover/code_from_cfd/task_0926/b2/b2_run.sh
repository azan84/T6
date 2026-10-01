#!/bin/bash
# Task B2 (work order 2026-09-26): uncontended throughput layouts on scan-14 baseline, resistance mode:  L16 = ONE 16-rank job;  L8x2 = TWO 8-rank jobs side by side on disjoint physical cores.
# usage: B2_EXCLUSIVE_OK=1 b2_run.sh <L16|L8x2>       (the jobs run under an umbrella b2_jobs.sh started with setsid: every solver process of the run belongs to its session U)
# Prepared by b2_prepare.sh (cases b2/L16/case, b2/L8/caseA, b2/L8/caseB, decomposed, no field writes; endTime 1600 set by the coordinator after b2_prepare.sh (which writes 1400): the runner refuses any other value). Analysis: b2_analyse.py (settle iteration by the B1 rule, wall clock to it, solves per hour).
# Refuses unless: operator reserved the host (B2_EXCLUSIVE_OK=1), no simpleFoam/mpirun/mesher/queue process, load < 1.5, >= 10 GB free, Windows side idle (powershell.exe; overrides
#   B2_ALLOW_WINDOWS_LOAD=1 / B2_ALLOW_NO_WINDOWS_CHECK=1 are recorded and make the evidence 'unknown'; the measured Windows background is stated in isolation_evidence.json).
# Override B2_ALLOW_STOPPED_FOREIGN=1 (fix 27, paused foreign jobs): an offender is ignored only if EVERY thread is stopped (state T/t in /proc/<pid>/task/*/stat; unreadable -> not ignored) and it is not the runner's;
#   the ignored ones are listed in $OUT/stopped_foreign_prerun.txt (count in host_before.txt); at the end $OUT/stopped_foreign_postrun.txt records which are still stopped / resumed (ran: CPU time grew or not stopped) /
#   vanished and any new foreign offender (pid+start time not in the pre-run list: new_running / new_stopped); resumed or new running -> WARNING and isolation_evidence.json contended=yes ('foreign stopped job resumed
#   during the run'); vanished or new stopped -> contended=unknown unless yes. Running offenders are always refused. Memory evidence (any run): memory_prerun.txt / memory_postrun.txt (MemAvailable, swap, pswpin/out,
#   pgmajfault), dmesg_oom.txt (OOM lines during the run or 'not readable'); the sampler adds owned_majflt.txt (major faults of the owned session).
# Attempt 3: the guard takes ONE proc_info snapshot per candidate (vanished/unreadable/not all T/t -> offender) and the whole offender check runs again immediately before launch (after the Windows
#   precheck and the OpenFOAM env; any running offender or a changed stopped pid:start set -> refuse); post-run exclusions of the runner, its ancestors, the sampler and the session are pid+start based;
#   host_before.txt records the pause watcher and the line count of its log paused.pids; new lines after the run (watcher_new > 0) -> contended=unknown. The sampler adds host_cpu_samples.csv (host-level non-owned CPU, an additional contended criterion).
# Fable attempt 1 (audit SOL_FIX27_R3): with B2_ALLOW_STOPPED_FOREIGN=1 the runner REFUSES (before mkdir of the results directory, and again at the pre-launch recheck) unless a pause watcher is alive
#   ('pause_marissa_light2.sh <s>' (two pgrep calls every 30 s; the operator's watcher since 07:55, Fable attempt 2), 'pause_marissa_light.sh <s>' (every 30 s) or 'pause_marissa.sh --watch <s>' (every 10 s); the script must be argv[0] or argv[1] of the process) and its remaining coverage (<s> minus its elapsed time;
#   the largest over the live watchers) is at least B2_MAX_RUNTIME_S; the watchers, their start times and remaining coverage are recorded in host_before.txt. Calibration hook B2_CALIB_ENDTIME=<n>
#   (b2_calibrate.sh only: accepted only when B2_ROOT lies under /b2_calib/): the endTime guard expects <n> instead of 1600 and host_before.txt / run_status.json mark the run as a calibration (not a measurement).
# Bounded: B2_MAX_RUNTIME_S (default 14400) and B2_NOPROGRESS_S (default 900: no new 'Time =' line in ANY job log) -> bounded stop (SIGTERM, grace, SIGKILL of the session's survivors), run marked INVALID.
# Total solver ranks are 16 in both layouts (work order 09-24 section 6). Test hooks (shim tests only): B2_ROOT, B2_SKIP_FOAM_ENV=1, B2_SKIP_PREREQ=1, B2_POWERSHELL (= TASK4_POWERSHELL), B2_SAMPLE_S, B2_WIN_CHECK_S, B2_WIN_EVERY_S, B2_STOP_GRACE_S, B2_POLL_S, B2_MPIRUN, B2_STOP_BEFORE_LAUNCH=1 (exit 3 after the pre-launch recheck), B2_PAUSED_PIDS (the watcher's log), B2_CALIB_ENDTIME (calibration copies only).
P=/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot
HERE=$(cd "$(dirname "$0")" && pwd); ISO="$HERE/b2_isolation.py"; B=${B2_ROOT:-$P/b2}; LAYOUT=${1:-}
MAXRT=${B2_MAX_RUNTIME_S:-14400}; NOPROG=${B2_NOPROGRESS_S:-900}; SAMPLE=${B2_SAMPLE_S:-5}; WINCHK=${B2_WIN_CHECK_S:-10}; WINEVERY=${B2_WIN_EVERY_S:-60}; GRACE=${B2_STOP_GRACE_S:-30}; POLL=${B2_POLL_S:-5}
MPIRUN=${B2_MPIRUN:-mpirun}; PAUSED=${B2_PAUSED_PIDS:-/home/azan/paper6_t6_work/marissa_pause/paused.pids}; PPL0=""; export TASK4_POWERSHELL=${B2_POWERSHELL:-${TASK4_POWERSHELL:-powershell.exe}}
CALIB=${B2_CALIB_ENDTIME:-}; WATCH_REPORT=""; WATCH_ALIVE=0; WATCH_LEFT=""      # calibration endTime (b2_calibrate.sh; empty = a measurement, endTime 1600); pause watcher record (pause_watchers)
export B2_COMM=simpleFoam; export B2_NRANKS=16
SP=""; U=""; SPK=""; UK=""; U_START=""; SELF=" "; SELFK=" "; END_REASON=""; BOUNDED=none; LAUNCHED=no; T0=""; JOBRC=()
fail() { echo "FAIL: $*" >&2; [ -n "$END_REASON" ] || END_REASON="refused: $*"; exit 1; }
now() { date +%s; }
PAT1="simpleFoam|pimpleFoam|mpirun|orted|cartesianMesh|blockMesh|checkMesh|reconstructPar|decomposePar|snappyHexMesh"; PAT2="run_set.*\.sh|queue.*\.sh|post_case\.sh|m1_probes\.py|u3d_make_csv\.py|reconstructPar|task4_run\.sh"
# --- stopped-foreign helpers (B2_ALLOW_STOPPED_FOREIGN=1) ---
proc_states() {    # the state letters of every thread of <pid> (e.g. TTT); returns 1 if the process has no readable thread or any thread's state cannot be read
    local f s x st=""; for f in /proc/"$1"/task/*/stat; do s=$(cat "$f" 2>/dev/null) || return 1; s=${s##*) }; x=${s%% *}; [[ "$x" == [A-Za-z] ]] || return 1; st="$st$x"; done
    [ -n "$st" ] && echo "$st"
}
is_stopped() { local st; st=$(proc_states "$1") && [[ "$st" =~ ^[Tt]+$ ]]; }
proc_info() {      # "<pid> state=<distinct thread states> threads=<n> cpu_ticks=<utime+stime+cutime+cstime> start=<starttime> rss_kb=<VmRSS> <cmdline>"
    local s r st u; s=$(cat /proc/"$1"/stat 2>/dev/null) || { echo "$1 state=gone"; return 1; }; r=(${s##*) }); st=$(proc_states "$1") || st="?"; u=$(echo "$st" | grep -o . | sort -u | tr -d '\n')
    echo "$1 state=$u threads=${#st} cpu_ticks=$(( r[11] + r[12] + r[13] + r[14] )) start=${r[19]} rss_kb=$(awk '/^VmRSS:/ {print $2}' /proc/"$1"/status 2>/dev/null) $(tr '\0\n\r' '   ' < /proc/"$1"/cmdline 2>/dev/null)"
}
pstart() { local s r; s=$(cat /proc/"$1"/stat 2>/dev/null) || return 1; r=(${s##*) }); echo "${r[19]}"; }     # start time (clock ticks after boot) of <pid>: pid+start identifies a process
offender_scan() {  # sets OFF1/OFF2 (offender lines), STOPPED (proc_info lines), STOPPED_PIDS, STOPPEDK (pid:start of the ignored ones); with the override ONE proc_info snapshot per candidate decides:
    # ignored only if that single read succeeded and every thread state in it is T/t; vanished (state=gone), unreadable (state=?) or any other state -> offender (named with its snapshot)
    local v k pid rest info rc sf st0
    offenders() { pgrep -a "$@" | while read -r pid rest; do [[ "$SELF" == *" $pid "* ]] || echo "  pid $pid: $rest"; done; }
    OFF1=$(offenders -x "$PAT1"); OFF2=$(offenders -f "$PAT2"); STOPPED=""; STOPPED_PIDS=" "; STOPPEDK=" "
    [ "${B2_ALLOW_STOPPED_FOREIGN:-0}" = 1 ] || return 0
    for v in OFF1 OFF2; do
        k=""; while read -r _ pid rest; do
            pid=${pid%:}; [ -n "$pid" ] || continue; [[ "$STOPPED_PIDS" == *" $pid "* ]] && continue
            info=$(proc_info "$pid"); rc=$?; read -r _ sf _ _ st0 _ <<< "$info"
            if [ "$rc" -eq 0 ] && [[ "${sf#state=}" =~ ^[Tt]+$ ]]; then STOPPED_PIDS="$STOPPED_PIDS$pid "; STOPPEDK="$STOPPEDK$pid:${st0#start=} "; STOPPED="$STOPPED$info"$'\n'
            else k="$k  pid $pid: $rest [snapshot: ${info#"$pid" }]"$'\n'; fi
        done <<< "${!v}"; printf -v "$v" '%s' "${k%$'\n'}"
    done
}
stopped_postrun() {   # $OUT/stopped_foreign_postrun.txt: fate of every pre-run stopped process (same pid AND start time) + foreign offenders (pid+start time not in the pre-run list) now running / stopped; WARNING if any ran
    local ex=" $SELFK $SPK $UK " pre=" " prek=" " pid stf thf cf sf rest c0 s0 info n c s k res=0 van=0 still=0 und=0 nrun=0 nstop=0 body=""
    while read -r pid stf thf cf sf rest; do
        [ -n "$pid" ] && [ "${pid:0:1}" != "#" ] || continue; pre="$pre$pid "; c0=${cf#cpu_ticks=}; s0=${sf#start=}; prek="$prek$pid:$s0 "
        info=$(proc_info "$pid"); read -r _ n _ c s _ <<< "$info"; n=${n#state=}; c=${c#cpu_ticks=}; s=${s#start=}      # one snapshot decides (attempt 3)
        if [ "$n" = gone ] || [ "$s" != "$s0" ]; then body="${body}vanished $pid (pre-run: $stf $cf $sf $rest)"$'\n'; van=$((van+1))
        elif [ "$n" = "?" ]; then body="${body}undecided $info (thread states unreadable)"$'\n'; und=$((und+1))
        elif [[ "$n" =~ ^[Tt]+$ ]] && [ "$c" = "$c0" ]; then body="${body}still_stopped $info"$'\n'; still=$((still+1))
        else body="${body}resumed $info (pre-run cpu_ticks=$c0)"$'\n'; res=$((res+1)); fi
    done < "$OUT/stopped_foreign_prerun.txt"
    # own processes are excluded by pid AND start time (recorded while alive: runner ancestors at the guard, sampler and umbrella at launch); session members only while the umbrella U itself
    # is alive with its launch start time (else the sid U may belong to a foreign session whose leader reused pid U)
    if [ -n "$U" ] && [ -n "$U_START" ] && [ "$(pstart "$U")" = "$U_START" ]; then for pid in $(session_pids); do s=$(pstart "$pid") && ex="$ex$pid:$s "; done; fi
    for pid in $( { pgrep -x "$PAT1"; pgrep -f "$PAT2"; } | sort -un); do
        info=$(proc_info "$pid") || continue; read -r _ n _ _ s _ <<< "$info"
        [[ "$ex" == *" $pid:${s#start=} "* ]] && continue         # the runner's own (pid and start time match; a reused pid is foreign)
        [[ "$prek" == *" $pid:${s#start=} "* ]] && continue      # a pre-run process is excluded only if pid AND start time match (a reused pid is a new process)
        if [[ "${n#state=}" =~ ^[Tt]+$ ]]; then body="${body}new_stopped $info"$'\n'; nstop=$((nstop+1)); else body="${body}new_running $info"$'\n'; nrun=$((nrun+1)); fi
    done
    k="summary prerun=$(echo $pre | wc -w) still_stopped=$still resumed=$res vanished=$van undecided=$und new_running=$nrun new_stopped=$nstop"
    if [ -n "$PPL0" ] && { n=$(wc -l < "$PAUSED"); } 2>/dev/null; then k="$k watcher_new=$(( n - PPL0 ))"; [ "$n" -eq "$PPL0" ] || body="${body}# pause log $PAUSED grew by $(( n - PPL0 )) lines during the run:"$'\n'"$(tail -n +$(( PPL0 + 1 )) "$PAUSED" | sed 's/^/#   /')"$'\n'; fi
    { echo "# B2_ALLOW_STOPPED_FOREIGN=1 post-run check $(date '+%F %T'): pre-run stopped foreign processes (still_stopped: same pid and start time, every thread T/t, CPU time unchanged;"
      echo "# resumed: ran during the run (CPU time grew) or not stopped now; vanished: gone or pid reused; undecided: state unreadable) and foreign offenders whose pid+start time is not in the pre-run list (new_running / new_stopped; a reused pid is new)"
      printf '%s' "$body"; echo "$k"; } > "$OUT/stopped_foreign_postrun.txt"
    echo "stopped foreign processes: $k" >&2
    [ $((res + nrun)) -eq 0 ] || echo "WARNING: foreign stopped job resumed during the run ($res resumed, $nrun new running foreign offenders; see $OUT/stopped_foreign_postrun.txt): contended=yes" >&2
    [ "$und" -eq 0 ] || echo "WARNING: $und pre-run stopped processes undecided (state unreadable): contended=unknown" >&2
    [[ "$k" == *watcher_new=* && "${k##*watcher_new=}" != 0 ]] && echo "WARNING: the pause watcher stopped new processes during the run ($k): contended=unknown (unless yes)" >&2
    [ $((van + nstop)) -eq 0 ] || echo "WARNING: $van pre-run stopped processes vanished, $nstop new stopped foreign processes: CPU use not excluded, contended=unknown (unless yes)" >&2
}
mem_snapshot() {     # memory evidence (fix 27 attempt 2, written with or without the override): /proc/meminfo, /proc/vmstat swap and major-fault counters, kernel uptime (for dmesg)
    grep -E '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo; grep -E '^(pswpin|pswpout|pgmajfault) ' /proc/vmstat; echo "uptime_s $(cut -d' ' -f1 /proc/uptime)"; echo "epoch $(date +%s)"
}
dmesg_oom() {        # $OUT/dmesg_oom.txt: kernel OOM lines stamped between memory_prerun.txt and memory_postrun.txt (uptime s), or 'not readable'
    local a b d; a=$(awk '$1 == "uptime_s" {print $2}' "$OUT/memory_prerun.txt" 2>/dev/null); b=$(awk '$1 == "uptime_s" {print $2}' "$OUT/memory_postrun.txt" 2>/dev/null)
    if d=$(dmesg 2>/dev/null) && [ -n "$d" ]; then
        { echo "readable: dmesg lines matching OOM with kernel time in [${a:-0}, ${b:-end}] s (first buffered line: $(printf '%s\n' "$d" | head -1 | cut -c1-16))"
          printf '%s\n' "$d" | awk -v a="${a:-0}" -v b="${b:-1e18}" 'match($0, /^\[ *[0-9.]+\]/) { t = substr($0, 2, RLENGTH - 2) + 0
              if (t >= a + 0 && t <= b + 0 && tolower($0) ~ /out of memory|oom-kill|oom_reaper|invoked oom-killer|killed process/) print }'; } > "$OUT/dmesg_oom.txt"
    else echo "not readable" > "$OUT/dmesg_oom.txt"; fi
}
pause_watchers() {   # sets WATCH_REPORT (lines for host_before.txt), WATCH_ALIVE (live recognised watchers), WATCH_LEFT (largest remaining coverage in s among them; empty if none) and PPL0 (lines of paused.pids)
    # Recognised forms: 'pause_marissa_light2.sh [SECONDS]' (default 36000; two pgrep calls every 30 s, PIDs already seen stopped are skipped; Fable attempt 2), 'pause_marissa_light.sh [SECONDS]'
    # (default 36000; a pgrep scan every 30 s) and 'pause_marissa.sh --watch [SECONDS]' (default 3600; a /proc scan every 10 s). The script must be
    # argv[0] or argv[1] of the process (a shell whose command line merely mentions the name is not a watcher) and the process must not be the runner or one of its ancestors.
    # Remaining coverage = SECONDS - elapsed time of the process (the watcher computes its end as its start + SECONDS). It must cover this layout's B2_MAX_RUNTIME_S (watcher_guard refuses otherwise).
    local pid rest a n e left form t; WATCH_REPORT=""; WATCH_ALIVE=0; WATCH_LEFT=""; t=$(now)
    while read -r pid rest; do
        [ -n "$pid" ] || continue; [[ "$SELF" == *" $pid "* ]] && continue; read -ra a <<< "$rest"; form=""; n=""
        if [[ "${a[0]:-}" == *pause_marissa_light2.sh ]]; then n=${a[1]:-36000}; form="pause_marissa_light2.sh (two pgrep calls every 30 s, seen PIDs skipped)"
        elif [[ "${a[1]:-}" == *pause_marissa_light2.sh ]]; then n=${a[2]:-36000}; form="pause_marissa_light2.sh (two pgrep calls every 30 s, seen PIDs skipped)"
        elif [[ "${a[0]:-}" == *pause_marissa_light.sh ]]; then n=${a[1]:-36000}; form="pause_marissa_light.sh (pgrep scan every 30 s)"
        elif [[ "${a[1]:-}" == *pause_marissa_light.sh ]]; then n=${a[2]:-36000}; form="pause_marissa_light.sh (pgrep scan every 30 s)"
        elif [[ "${a[0]:-}" == *pause_marissa.sh || "${a[1]:-}" == *pause_marissa.sh ]] && [[ " $rest " == *" --watch"* ]]; then n=$(printf '%s\n' "$rest" | sed -n 's/.*--watch *\([0-9][0-9]*\).*/\1/p'); n=${n:-3600}; form="pause_marissa.sh --watch (/proc scan every 10 s)"
        fi
        if [ -z "$form" ] || ! [[ "$n" =~ ^[0-9]+$ ]]; then WATCH_REPORT+="pause watcher candidate ignored (unrecognised form): pid $pid ($rest)"$'\n'; continue; fi
        e=$(ps -o etimes= -p "$pid" 2>/dev/null | tr -d ' '); [[ "$e" =~ ^[0-9]+$ ]] || { WATCH_REPORT+="pause watcher pid $pid ($rest): gone before its elapsed time could be read"$'\n'; continue; }
        left=$(( n - e )); WATCH_ALIVE=$((WATCH_ALIVE + 1)); { [ -n "$WATCH_LEFT" ] && [ "$WATCH_LEFT" -ge "$left" ]; } || WATCH_LEFT=$left
        WATCH_REPORT+="pause watcher alive: pid $pid, form $form, started $(date -d "@$(( t - e ))" '+%F %T') for $n s, running $e s, about $left s left (ends about $(date -d "@$(( t + left ))" '+%F %T')); B2_MAX_RUNTIME_S $MAXRT; cmdline: $rest"$'\n'
        [ "$left" -ge "$MAXRT" ] || echo "WARNING: pause watcher $pid ends before this layout's maximum runtime ($left s < $MAXRT s)" >&2
    done <<< "$(pgrep -af 'pause_marissa(_light2?)?\.sh')"
    [ "$WATCH_ALIVE" -gt 0 ] || { WATCH_REPORT+="pause watcher: no 'pause_marissa_light2.sh <s>', 'pause_marissa_light.sh <s>' or 'pause_marissa.sh --watch <s>' process alive"$'\n'; echo "WARNING: no pause watcher alive (a foreign job started during the run would not be stopped)" >&2; }
    { PPL0=$(wc -l < "$PAUSED"); } 2>/dev/null && WATCH_REPORT+="pause log $PAUSED: $PPL0 lines (compared after the run: any new line = a process stopped during the run)"$'\n' || { PPL0=""; WATCH_REPORT+="pause log $PAUSED: not readable"$'\n'; }
}
watcher_guard() {    # B2_ALLOW_STOPPED_FOREIGN=1 (audit SOL_FIX27_R3 blocker): refuse unless a recognised pause watcher is alive and its remaining coverage is at least B2_MAX_RUNTIME_S; $1 names the stage
    pause_watchers
    [ "$WATCH_ALIVE" -gt 0 ] || fail "$1: B2_ALLOW_STOPPED_FOREIGN=1 needs a live pause watcher (pause_marissa_light2.sh <s>, pause_marissa_light.sh <s> or pause_marissa.sh --watch <s>) so that a foreign job started during the run is stopped: none alive"$'\n'"$WATCH_REPORT"
    [ "$WATCH_LEFT" -ge "$MAXRT" ] || fail "$1: the pause watcher's remaining coverage ($WATCH_LEFT s) is shorter than B2_MAX_RUNTIME_S ($MAXRT s): restart the watcher with a longer time (it must cover BOTH layouts) or lower B2_MAX_RUNTIME_S"$'\n'"$WATCH_REPORT"
}
# --- end of the stopped-foreign helpers ---
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
    TD="$OUT" END_REASON="$END_REASON" BOUNDED="$BOUNDED" LAYOUT="$LAYOUT" T0="$T0" T1="$(now)" RCS="${JOBRC[*]}" LEFT="$(echo $(session_pids))" CALIB="$CALIB" python3 -c 'import json, os; e = os.environ
rcs = [int(x) if x.lstrip("-").isdigit() else None for x in e["RCS"].split()]
json.dump(dict(layout=e["LAYOUT"], end_reason=e["END_REASON"], bounded_stop=e["BOUNDED"], job_exit_codes=rcs, launch_epoch=int(e["T0"] or 0), end_epoch=int(e["T1"]), survivors_of_owned_session=e["LEFT"].split(),
  controlled_end=(e["END_REASON"] == "all_jobs_finished" and e["BOUNDED"] == "none" and bool(rcs) and all(r == 0 for r in rcs)), calibration_endtime=(int(e["CALIB"]) if e["CALIB"] else None)), open(os.path.join(e["TD"], "run_status.json"), "w"), indent=1)' || echo "WARNING: run_status.json not written" >&2
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
[ -z "$CALIB" ] || { [[ "$B" == */b2_calib/* ]] && [[ "$CALIB" =~ ^[0-9]+$ ]] && [ "$LAYOUT" = L16 ]; } || fail "B2_CALIB_ENDTIME=$CALIB is accepted only for layout L16 with a B2_ROOT under /b2_calib/ (a calibration copy made by b2_calibrate.sh), not for a measurement (B2_ROOT $B)"
OUT="$B/results_$LAYOUT"; [ ! -e "$OUT" ] || fail "$OUT exists (a layout is measured once; move it aside to repeat)"
[ "${B2_EXCLUSIVE_OK:-0}" = 1 ] || fail "set B2_EXCLUSIVE_OK=1 only after the coordinator has announced the exclusive interval (no other Linux or Windows job may start until the run ends)"
for c in "${CASES[@]}"; do
    [ -d "$c" ] || fail "$c missing (run b2_prepare.sh)"; n=$(ls -d "$c"/processor* 2>/dev/null | wc -l); [ "$n" -eq "$NPJ" ] || fail "$c has $n processor directories, expected $NPJ"
    grep -q "^endTime *${CALIB:-1600};" "$c/system/controlDict" || fail "$c/system/controlDict: endTime is not ${CALIB:-1600} (budget: B1 settle iteration 1229 + 30 %; the coordinator edits the prepared cases${CALIB:+; calibration copy: B2_CALIB_ENDTIME})"
    for d in "$c"/processor*; do [ -d "$d/0" ] && [ -d "$d/constant/polyMesh" ] || fail "$d incomplete"; ls "$d" | grep -Eq '^[0-9]' && [ "$(ls "$d" | grep -Ec '^[0-9.e+-]+$')" -eq 1 ] || fail "$d holds time directories other than 0"; done
    [ ! -e "$c/log.simpleFoam" ] || fail "$c/log.simpleFoam exists"
done
if [ "${B2_SKIP_PREREQ:-0}" != 1 ]; then
    SELF=" $$ "; p=$$; while [ "$p" -gt 1 ] 2>/dev/null; do p=$(ps -o ppid= -p "$p" | tr -d ' '); SELF="$SELF$p "; done
    for p in $SELF; do s=$(pstart "$p") && SELFK="$SELFK$p:$s "; done          # runner and ancestors by pid AND start time (post-run exclusion)
    offender_scan; SNOTE=""     # with B2_ALLOW_STOPPED_FOREIGN=1 offenders stopped in their single snapshot are ignored (listed after mkdir); all others stay offenders
    [ "${B2_ALLOW_STOPPED_FOREIGN:-0}" = 1 ] && SNOTE=" (B2_ALLOW_STOPPED_FOREIGN=1: $(echo $STOPPED_PIDS | wc -w) stopped foreign processes ignored)"
    [ -z "$OFF1$OFF2" ] || fail "host busy$SNOTE; solver/mesher processes:"$'\n'"${OFF1:-  none}"$'\n'"launcher/queue/heavy post-processing jobs:"$'\n'"${OFF2:-  none}"
    LOAD=$(cut -d' ' -f1 /proc/loadavg); awk -v l="$LOAD" 'BEGIN{exit !(l<1.5)}' || fail "1-min load average $LOAD >= 1.5"
    [ "${B2_ALLOW_STOPPED_FOREIGN:-0}" != 1 ] || watcher_guard "pause watcher guard"      # refuses before the results directory exists (Fable attempt 1)
else LOAD="$(cut -d' ' -f1 /proc/loadavg) (TEST MODE: guards skipped)"; fi
[ "$(df --output=avail -B1G / | tail -1 | tr -dc 0-9)" -ge 10 ] || fail "less than 10 GB free"
mkdir -p "$OUT" || fail "cannot create $OUT"
if [ "${B2_ALLOW_STOPPED_FOREIGN:-0}" = 1 ] && [ "${B2_SKIP_PREREQ:-0}" != 1 ]; then
    NSTOP=$(echo $STOPPED_PIDS | wc -w); RSSMB=$(printf '%s' "$STOPPED" | grep -o 'rss_kb=[0-9]*' | awk -F= '{s+=$2} END {printf "%.0f", s/1024}')
    { echo "# B2_ALLOW_STOPPED_FOREIGN=1 $(date '+%F %T'): foreign offender processes ignored by the pre-run guard because every thread is stopped (T/t); they hold memory (RSS sum $RSSMB MB) but use no CPU"
      echo "# pid state=<thread states> threads=<n> cpu_ticks=<utime+stime+cutime+cstime> start=<starttime> rss_kb=<VmRSS> cmdline"; printf '%s' "$STOPPED"; } > "$OUT/stopped_foreign_prerun.txt"
    echo "WARNING: B2_ALLOW_STOPPED_FOREIGN=1: $NSTOP stopped foreign processes ignored by the offender guard (RSS $RSSMB MB), listed in $OUT/stopped_foreign_prerun.txt" >&2
fi
python3 "$ISO" winprecheck "$OUT/windows_prerun.json" "$WINCHK" > "$OUT/winprecheck.out" 2>&1; wrc=$?
case $wrc in
    0) ;;
    3) [ "${B2_ALLOW_WINDOWS_LOAD:-0}" = 1 ] || { cat "$OUT/winprecheck.out" >&2; fail "Windows-side load (see above); override B2_ALLOW_WINDOWS_LOAD=1 records it and makes the evidence 'unknown'"; }
       export TASK4_ALLOW_WINDOWS_LOAD=1; python3 "$ISO" winprecheck "$OUT/windows_prerun.json" 1 > /dev/null 2>&1; echo "WARNING: Windows-side load overridden (B2_ALLOW_WINDOWS_LOAD=1): contended=unknown" >&2;;
    *) [ "${B2_ALLOW_NO_WINDOWS_CHECK:-0}" = 1 ] || { cat "$OUT/winprecheck.out" >&2; fail "Windows check unavailable; override B2_ALLOW_NO_WINDOWS_CHECK=1"; }
       echo "WARNING: no Windows check: contended=unknown" >&2;;
esac
[ "${B2_SKIP_FOAM_ENV:-0}" = 1 ] || source /usr/lib/openfoam/openfoam2406/etc/bashrc
{ date; uptime; lscpu | grep -E "Model name|Core|Thread|Socket"; echo "layout $LAYOUT; load at start $LOAD"
  [ -z "$CALIB" ] || echo "CALIBRATION RUN (B2_CALIB_ENDTIME=$CALIB, B2_ROOT $B): a copy of the L16 case with endTime $CALIB for the host-level CPU calibration (b2_calibrate.sh); NOT a B2 measurement"
  [ -e "$OUT/stopped_foreign_prerun.txt" ] && echo "stopped foreign processes ignored (B2_ALLOW_STOPPED_FOREIGN=1): $NSTOP (RSS $RSSMB MB; list in stopped_foreign_prerun.txt)"
  [ -e "$OUT/stopped_foreign_prerun.txt" ] && printf '%s' "$WATCH_REPORT"; } > "$OUT/host_before.txt"
mem_snapshot > "$OUT/memory_prerun.txt"
if [ "${B2_SKIP_PREREQ:-0}" != 1 ]; then      # pre-launch recheck (fix 27 attempt 3): the whole offender check again, after the Windows precheck and the OpenFOAM env; any change -> refuse
    FIRSTK=$(echo $STOPPEDK | tr ' ' '\n' | sort | xargs); offender_scan; NOWK=$(echo $STOPPEDK | tr ' ' '\n' | sort | xargs)
    [ -z "$OFF1$OFF2" ] || fail "pre-launch recheck: host busy; solver/mesher processes:"$'\n'"${OFF1:-  none}"$'\n'"launcher/queue/heavy post-processing jobs:"$'\n'"${OFF2:-  none}"
    [ "$FIRSTK" = "$NOWK" ] || fail "pre-launch recheck: the stopped foreign set (pid:start) changed since the guard: before [$FIRSTK] now [$NOWK]"
    echo "pre-launch offender recheck $(date +%T): passed (no running offender; $(echo $NOWK | wc -w) stopped foreign processes, same pid+start set as at the guard)" >> "$OUT/host_before.txt"
    if [ "${B2_ALLOW_STOPPED_FOREIGN:-0}" = 1 ]; then        # the watcher must still be alive and still cover B2_MAX_RUNTIME_S right before the launch (Fable attempt 1)
        watcher_guard "pre-launch recheck"; echo "pre-launch pause watcher recheck $(date +%T): passed ($WATCH_ALIVE alive, $WATCH_LEFT s left >= B2_MAX_RUNTIME_S $MAXRT s; paused.pids ${PPL0:-unreadable} lines)" >> "$OUT/host_before.txt"
    fi
fi
[ "${B2_STOP_BEFORE_LAUNCH:-0}" = 1 ] && { echo "TEST: stopped before launch (B2_STOP_BEFORE_LAUNCH=1)" >&2; exit 3; }
# --- launch: the umbrella b2_jobs.sh is the session leader U of every job (per-rank taskset to one physical core each, b2_rank.sh) ---
setsid "$HERE/b2_jobs.sh" "$LAYOUT" "$OUT" > "$OUT/jobs.log" 2>&1 &
U=$!; LAUNCHED=yes; T0=$(now); U_START=$(pstart "$U"); UK="$U:$U_START"
t=0; until [ "$(ps -o sid= -p "$U" 2>/dev/null | tr -d ' ')" = "$U" ] || [ $t -ge 50 ]; do sleep 0.1; t=$((t+1)); done
[ "$(ps -o sid= -p "$U" 2>/dev/null | tr -d ' ')" = "$U" ] || { END_REASON="launch: the umbrella is not its own session leader"; kill -TERM "$U" 2>/dev/null; fail "$END_REASON"; }
python3 "$ISO" sample "$U" "$$" "$OUT" "$SAMPLE" "$WINEVERY" 2> "$OUT/sampler.err" &
SP=$!; SPK="$SP:$(pstart "$SP")"
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
[ -e "$OUT/stopped_foreign_prerun.txt" ] && stopped_postrun
mem_snapshot > "$OUT/memory_postrun.txt"; dmesg_oom
cat "${CASES[@]/%//mpirun_bindings.txt}" > "$OUT/mpirun_bindings.txt" 2>/dev/null
python3 "$ISO" evidence "$OUT"
{ date; uptime; echo "layout $LAYOUT; end $END_REASON; bounded stop $BOUNDED; job rc ${JOBRC[*]}"; } > "$OUT/host_after.txt"
for c in "${CASES[@]}"; do echo "$c: $(grep -c '^Time = ' $c/log.simpleFoam) steps, $(grep -E 'ExecutionTime' $c/log.simpleFoam | tail -1)"; done
[ "$END_REASON" = all_jobs_finished ] && [ "$BOUNDED" = none ] && exit 0
echo "FAIL: run not finished normally ($END_REASON, bounded stop $BOUNDED): INVALID" >&2; exit 1
