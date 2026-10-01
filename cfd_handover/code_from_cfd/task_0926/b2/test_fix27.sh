#!/bin/bash
# fix 27 test: the B2_ALLOW_STOPPED_FOREIGN=1 offender guard of b2_run.sh, with shim processes started (and signalled, and killed) by this script only.
# The runner is stopped before launch: B2_POWERSHELL=/bin/false without B2_ALLOW_NO_WINDOWS_CHECK -> it exits at the Windows guard (after the offender, load and disk guards and after mkdir OUT).
# Fake B2_ROOT with a minimal prepared L16 case, B2_SKIP_FOAM_ENV=1. NOTE: the offender scan is host-wide, so the host's real stopped (paused) processes are listed as well; they are only read, never signalled.
# Supplementary (not the runner's main path): stopped_postrun (helpers extracted from b2_run.sh) and b2_isolation.py evidence on fabricated result directories.
# Attempt 2 (audit SOL_FIX27): A2 pid reuse (+ the attempt-1 regression), C memory snapshot / dmesg filter, D sampler owned_majflt.txt, E evidence outcomes + memory keys, F b2_analyse.py rows and ratio notes.
# Attempt 3 (audit SOL_FIX27_R2): G single-snapshot admission (offender_scan) + the pre-launch recheck through the real runner (fake powershell, B2_STOP_BEFORE_LAUNCH=1), H pid+start post-run exclusions,
#   I host-level CPU (I1 synthetic /proc/stat + ledger unit test, I2 real sampler with owned and non-owned short-lived busy loops between two samples), J analyse MEMK, K pause watcher record + paused.pids growth.
# Fable attempt 1 (audit SOL_FIX27_R3): a shim 'pause_marissa_light.sh 100000' of this test is alive from the start (the runner-path cases with the override need a live watcher covering B2_MAX_RUNTIME_S);
#   L watcher forms, coverage and the REFUSAL through the real runner (a pgrep wrapper on PATH hides the host's real watchers from the runner: FAKE_PGREP_HIDE), M p95 / fork label / informational host mode.
# Fable attempt 2 (FABLE_BRIEF_27b): N the third watcher form pause_marissa_light2.sh <s> through the real runner (N1-N4), the host's live light2 watcher read-only (N5), the calibrated thresholds
#   0.48 / 1.62 reproduced from calibration.json by b2_isolation.calib_rule and its edges (N6), and the evidence at the new max threshold: 1.61 core -> no host-level reason, 1.62 -> yes (N7).
HERE=$(cd "$(dirname "$0")" && pwd); T=$(mktemp -d /tmp/fix27test.XXXXXX); MINE=(); PASS=0; FAILN=0
cleanup() { for p in "${MINE[@]}"; do kill -KILL "$p" 2>/dev/null; done; sleep 0.3; rm -rf "$T"; }
trap cleanup EXIT
ok() { echo "PASS: $*"; PASS=$((PASS+1)); }; bad() { echo "FAIL: $*"; FAILN=$((FAILN+1)); }
st() { cut -d' ' -f3 /proc/"$1"/stat; }
# fake prepared case
C=$T/b2/L16/case; mkdir -p "$C/system" "$T/bin"; echo "endTime 1600;" > "$C/system/controlDict"
for i in $(seq 0 15); do mkdir -p "$C/processor$i/0" "$C/processor$i/constant/polyMesh"; done
cp /bin/sleep "$T/bin/simpleFoam"                                     # comm = simpleFoam (pgrep -x matches the comm, not argv[0])
printf '#!/bin/bash\nsleep 600\n' > "$T/bin/t_queue_shim.sh"; chmod +x "$T/bin/t_queue_shim.sh"     # cmdline matches 'queue.*\.sh'
run() { env B2_ROOT="$T/b2" B2_EXCLUSIVE_OK=1 B2_SKIP_FOAM_ENV=1 B2_POWERSHELL=/bin/false B2_WIN_CHECK_S=1 "$@" bash "$HERE/b2_run.sh" L16 > "$T/out" 2> "$T/err"; echo $? > "$T/rc"; }
OUT=$T/b2/results_L16
# a long shim pause watcher of this test (light form): the runner refuses with the override unless a watcher covers B2_MAX_RUNTIME_S (Fable attempt 1); the host's real watcher may or may not be alive
printf '#!/bin/bash\nsleep 600\n' > "$T/bin/pause_marissa_light.sh"; chmod +x "$T/bin/pause_marissa_light.sh"; bash "$T/bin/pause_marissa_light.sh" 100000 & LW=$!; MINE+=($LW); sleep 0.3; MINE+=($(pgrep -P $LW))
echo "shim light watcher: pid $LW (pause_marissa_light.sh 100000)"
# shims: S1 stopped simpleFoam, S2 stopped queue script, R1 running simpleFoam
"$T/bin/simpleFoam" 600 & S1=$!; MINE+=($S1); "$T/bin/t_queue_shim.sh" & S2=$!; MINE+=($S2); sleep 0.3; kill -STOP $S1 $S2; sleep 0.3
MINE+=($(pgrep -P $S2))
echo "shims: S1 $S1 ($(st $S1)), S2 $S2 ($(st $S2))"

echo "== case 1: stopped shims + override -> passes the offender guard, lists them, exits at the Windows guard"
run B2_ALLOW_STOPPED_FOREIGN=1; cat "$T/err"
if grep -q "Windows check unavailable" "$T/err" && ! grep -q "host busy" "$T/err"; then ok "offender guard passed (rc $(cat $T/rc), stopped at the Windows guard)"; else bad "case 1 did not reach the Windows guard"; fi
for p in $S1 $S2; do grep -q "^$p state=T " "$OUT/stopped_foreign_prerun.txt" 2>/dev/null && ok "pid $p listed in stopped_foreign_prerun.txt" || bad "pid $p not listed"; done
echo "--- stopped_foreign_prerun.txt (head)"; head -4 "$OUT/stopped_foreign_prerun.txt" | cut -c1-200; n=$(grep -vc "^#" "$OUT/stopped_foreign_prerun.txt"); echo "... $n entries"; grep -q "B2_ALLOW_STOPPED_FOREIGN=1: $n stopped" "$T/err" && ok "one line per ignored process ($n)" || bad "entry count $n differs from the ignored count"; rm -rf "$OUT"

echo "== case 2: stopped shims, no override -> refused"
run; cat "$T/err" | grep -E "FAIL|pid ($S1|$S2):"
grep -q "host busy" "$T/err" && grep -q "pid $S1:" "$T/err" && grep -q "pid $S2:" "$T/err" && [ ! -e "$OUT" ] && ok "refused, both shims named, no OUT" || bad "case 2"

echo "== case 3: running shim + override -> refused (the stopped shims are not named as offenders)"
"$T/bin/simpleFoam" 600 & R1=$!; MINE+=($R1); sleep 0.3
run B2_ALLOW_STOPPED_FOREIGN=1; cat "$T/err"
grep -q "host busy" "$T/err" && grep -q "pid $R1:" "$T/err" && ! grep -q "pid $S1:" "$T/err" && [ ! -e "$OUT" ] && ok "refused on running pid $R1 only" || bad "case 3"
kill -KILL $R1; wait $R1 2>/dev/null

echo "== case 4: one stopped (main, ptrace group-stop 't') + one running thread, comm simpleFoam, + override -> counts as running, refused"
python3 - "$T/mixed.pid" <<'PY' &
import ctypes, os, sys, time, threading
libc = ctypes.CDLL(None, use_errno=True); pr, pw = os.pipe()
pid = os.fork()
if pid == 0:
    libc.prctl(15, b"simpleFoam", 0, 0, 0)                  # PR_SET_NAME on the main thread = the process comm
    threading.Thread(target=lambda: [time.sleep(0.2) for _ in iter(int, 1)], daemon=True).start()
    os.write(pw, b"x"); [time.sleep(0.2) for _ in iter(int, 1)]
os.read(pr, 1); time.sleep(0.2)
r1 = libc.ptrace(0x4206, pid, 0, 0); r2 = libc.ptrace(0x4207, pid, 0, 0)     # PTRACE_SEIZE + PTRACE_INTERRUPT of the main thread only (tracer = parent, allowed by Yama scope 1)
open(sys.argv[1], "w").write(f"{pid} {os.getpid()} {r1} {r2} {ctypes.get_errno()}\n")
time.sleep(600)
PY
TR=$!; MINE+=($TR); for i in $(seq 50); do [ -s "$T/mixed.pid" ] && break; sleep 0.1; done; sleep 0.3
read -r M _ r1 r2 en < "$T/mixed.pid"; MINE+=($M)
TS=$(for f in /proc/$M/task/*/stat; do s=$(cat $f); s=${s##*) }; printf '%s' "${s%% *}"; done)
echo "mixed pid $M: ptrace rc $r1/$r2 errno $en; /proc/$M/stat state $(st $M); thread states $TS"
if [ "$r1$r2" = 00 ] && [[ "$TS" == *t* ]] && [[ "$TS" =~ [^Tt] ]]; then
    run B2_ALLOW_STOPPED_FOREIGN=1; cat "$T/err"
    grep -q "host busy" "$T/err" && grep -q "pid $M:" "$T/err" && [ ! -e "$OUT" ] && ok "mixed-thread process $M (main thread t, one thread running) refused as running" || bad "case 4"
else echo "SKIP: could not create a mixed-thread process (ptrace not permitted?)"; fi
kill -KILL $TR $M 2>/dev/null; wait $TR 2>/dev/null

echo "== supplementary A: stopped_postrun (helpers extracted from b2_run.sh)"
"$T/bin/simpleFoam" 600 & P2=$!; bash -c 'while :; do :; done' & P3=$!; "$T/bin/simpleFoam" 600 & P4=$!; MINE+=($P2 $P3 $P4); sleep 0.3; kill -STOP $P2 $P3 $P4; sleep 0.2
A=$T/postA; mkdir -p "$A"
( eval "$(sed -n '/^PAT1=/,/^# --- end of the stopped-foreign helpers/p' "$HERE/b2_run.sh")"; OUT=$A; SELF=" $$ $BASHPID "; SP=""; U=""; session_pids() { :; }
  { echo "# test"; for p in $S1 $P2 $P3 $P4; do proc_info $p; done; } > "$OUT/stopped_foreign_prerun.txt"
  kill -CONT $P2; kill -CONT $P3; sleep 1; kill -STOP $P3; kill -KILL $P4; sleep 0.3      # P2 resumed (running now), P3 ran and is stopped again (CPU grew), P4 gone
  "$T/bin/simpleFoam" 600 & N1=$!; echo $N1 > "$T/n1"; sleep 0.3
  stopped_postrun; kill -KILL $N1 )
N1=$(cat "$T/n1"); grep -v '^#' "$A/stopped_foreign_postrun.txt" | grep -E "^[a-z_]+ ($S1|$P2|$P3|$P4|$N1) |^summary" | cut -c1-160
grep -q "^still_stopped $S1 " "$A/stopped_foreign_postrun.txt" && grep -q "^resumed $P2 " "$A/stopped_foreign_postrun.txt" && grep -q "^resumed $P3 state=T " "$A/stopped_foreign_postrun.txt" \
  && grep -q "^vanished $P4 " "$A/stopped_foreign_postrun.txt" && grep -q "^new_running $N1 " "$A/stopped_foreign_postrun.txt" && grep -q "^summary prerun=4 still_stopped=1 resumed=2 vanished=1 undecided=0 new_running=1 " "$A/stopped_foreign_postrun.txt" \
  && ok "postrun: still_stopped / resumed (running) / resumed (stopped again, CPU grew) / vanished / new_running" || bad "postrun classification"

echo "== supplementary B: b2_isolation.py evidence on fabricated results"
E1=$T/ev1; E2=$T/ev2; E3=$T/ev3; mkdir -p $E1 $E2 $E3; cp "$A"/stopped_foreign_*.txt $E1/
cp "$A/stopped_foreign_prerun.txt" $E2/; printf '# x\nsummary prerun=4 still_stopped=4 resumed=0 vanished=0 undecided=0 new_running=0 new_stopped=0\n' > $E2/stopped_foreign_postrun.txt
cp "$A/stopped_foreign_prerun.txt" $E3/
for e in $E1 $E2 $E3; do python3 "$HERE/b2_isolation.py" evidence $e > /dev/null; python3 -c 'import json,sys; e=json.load(open(sys.argv[1]+"/isolation_evidence.json")); print(sys.argv[1][-3:], e["contended"], e["stopped_foreign_override"], e["stopped_foreign_count"], [r for r in e["contended_reasons"] if r.startswith("foreign")])' $e; done > "$T/ev"; cat "$T/ev"
grep -q "^ev1 yes True 4 \['foreign stopped job resumed during the run (2 resumed, 1 new running" "$T/ev" && grep -q "^ev2 unknown True 4 \[\]" "$T/ev" && grep -q "^ev3 unknown True 4 \['foreign stopped job resumed during the run: not decidable" "$T/ev" \
  && ok "evidence: resumed -> yes with the reason; all still stopped -> no stopped-foreign reason; postrun missing -> unknown" || bad "evidence"
kill -KILL $P2 $P3 2>/dev/null

# ---------------- attempt 2 (audit SOL_FIX27) ----------------
withhelpers() {    # withhelpers <b2_run.sh> <OUT> <commands>: run <commands> with the helper block of <b2_run.sh> (PAT1 .. end of the helpers), OUT=<OUT>, no session
    local src=$1 o=$2; shift 2
    ( eval "$(sed -n '/^PAT1=/,/^# --- end of the stopped-foreign helpers/p' "$src")"; OUT=$o; SELF=" $$ $BASHPID "; SELFK=" "; SP=""; SPK=""; U=""; UK=""; U_START=""; PPL0=""; PAUSED=/nonexistent
      MAXRT=14400; now() { date +%s; }; session_pids() { :; }; eval "$@" )
}
fakestart() { proc_info "$1" | awk '{ for (i = 1; i <= NF; i++) if ($i ~ /^start=/) { split($i, a, "="); $i = "start=" (a[2] - 1) } print }'; }    # the pre-run line of a pid, start time altered (= an older process with that pid)

echo "== supplementary A2: reused pid (pre-run pid alive with another start time) -> vanished AND eligible for new_running / new_stopped"
"$T/bin/simpleFoam" 600 & R2=$!; "$T/bin/simpleFoam" 600 & Q2=$!; MINE+=($R2 $Q2); sleep 0.3; kill -STOP $Q2; sleep 0.2
A2=$T/postA2; mkdir -p "$A2"; declare -f fakestart > "$T/fakestart.sh"
withhelpers "$HERE/b2_run.sh" "$A2" 'source $T/fakestart.sh; { echo "# test"; proc_info $S1; fakestart $R2; fakestart $Q2; } > $OUT/stopped_foreign_prerun.txt; stopped_postrun'
grep -v '^#' "$A2/stopped_foreign_postrun.txt" | grep -E "^[a-z_]+ ($S1|$R2|$Q2) |^summary" | cut -c1-160
grep -q "^still_stopped $S1 " "$A2/stopped_foreign_postrun.txt" && grep -q "^vanished $R2 " "$A2/stopped_foreign_postrun.txt" && grep -q "^vanished $Q2 " "$A2/stopped_foreign_postrun.txt" \
  && grep -q "^new_running $R2 " "$A2/stopped_foreign_postrun.txt" && grep -q "^new_stopped $Q2 " "$A2/stopped_foreign_postrun.txt" && ! grep -q "^new_[a-z]* $S1 " "$A2/stopped_foreign_postrun.txt" \
  && grep -q "^summary prerun=3 still_stopped=1 resumed=0 vanished=2 undecided=0 new_running=1 " "$A2/stopped_foreign_postrun.txt" \
  && ok "pid reuse: R2 vanished + new_running, Q2 vanished + new_stopped; S1 (pid and start match) excluded from the new scan" || bad "pid reuse"
A1=$T/postA1; mkdir -p "$A1"; cp "$A2/stopped_foreign_prerun.txt" "$A1/"
withhelpers "$HERE/../fix27_a1_snapshot/b2_run.sh" "$A1" 'stopped_postrun' 2> /dev/null
grep -q "^new_running $R2 " "$A1/stopped_foreign_postrun.txt" && bad "attempt-1 helpers unexpectedly report R2" || ok "regression reproduced: attempt-1 helpers miss the reused running pid R2 ($(grep '^summary' "$A1/stopped_foreign_postrun.txt"))"
kill -KILL $R2 $Q2 2>/dev/null

echo "== supplementary C: memory snapshot and dmesg OOM filter (helpers from b2_run.sh)"
MC=$T/memC; mkdir -p "$MC" "$T/fakebin"
withhelpers "$HERE/b2_run.sh" "$MC" 'mem_snapshot > $OUT/memory_prerun.txt; mem_snapshot > $OUT/memory_postrun.txt; dmesg_oom'
cat "$MC/memory_prerun.txt"; head -1 "$MC/dmesg_oom.txt" | cut -c1-120
[ "$(grep -cE '^(MemTotal|MemAvailable|SwapTotal|SwapFree):|^(pswpin|pswpout|pgmajfault|uptime_s|epoch) ' "$MC/memory_prerun.txt")" -eq 9 ] && head -1 "$MC/dmesg_oom.txt" | grep -q '^readable' \
  && ok "memory snapshot has the 9 keys; host dmesg readable" || bad "memory snapshot / host dmesg"
printf 'uptime_s 1000\n' > "$MC/memory_prerun.txt"; printf 'uptime_s 2000\n' > "$MC/memory_postrun.txt"
printf '#!/bin/sh\necho "[  500.000001] Out of memory: Killed process 11 (early)"\necho "[ 1500.000001] Out of memory: Killed process 99 (simpleFoam) total-vm:1kB"\necho "[ 1500.100000] unrelated line"\necho "[ 2500.000001] oom-kill:constraint=CONSTRAINT_NONE (late)"\n' > "$T/fakebin/dmesg"; chmod +x "$T/fakebin/dmesg"
PATH="$T/fakebin:$PATH" withhelpers "$HERE/b2_run.sh" "$MC" 'dmesg_oom'; cat "$MC/dmesg_oom.txt"
[ "$(grep -vc '^readable' "$MC/dmesg_oom.txt")" -eq 1 ] && grep -q "Killed process 99 (simpleFoam)" "$MC/dmesg_oom.txt" && ok "dmesg: only the OOM line inside the run window is kept" || bad "dmesg window filter"
printf '#!/bin/sh\necho "dmesg: read kernel buffer failed: Operation not permitted" >&2; exit 1\n' > "$T/fakebin/dmesg"
PATH="$T/fakebin:$PATH" withhelpers "$HERE/b2_run.sh" "$MC" 'dmesg_oom'; [ "$(cat "$MC/dmesg_oom.txt")" = "not readable" ] && ok "dmesg unreadable -> 'not readable'" || bad "dmesg not readable"

echo "== supplementary D: sampler writes owned_majflt.txt (a shim session leader as the 'mpirun', TASK4_POWERSHELL=/bin/false)"
MD=$T/samp; mkdir -p "$MD"; setsid "$T/bin/simpleFoam" 2 & SL=$!; MINE+=($SL); sleep 0.2
TASK4_POWERSHELL=/bin/false B2_NRANKS=1 timeout 20 python3 "$HERE/b2_isolation.py" sample $SL $$ "$MD" 0.5 1000; cat "$MD/owned_majflt.txt"
grep -Eq "^owned_session_majflt [0-9]+ processes 1$" "$MD/owned_majflt.txt" && [ "$(head -1 "$MD/isolation_samples.csv" | tr ',' '\n' | wc -l)" -eq 16 ] && [ "$(wc -l < "$MD/host_cpu_samples.csv")" -ge 2 ] \
  && ok "owned_majflt.txt written (1 session process), CSV columns unchanged (16), host_cpu_samples.csv written" || bad "sampler majflt"

echo "== supplementary E: evidence on a clean fabricated result (contended=no baseline; B2_NRANKS=2 on cores 0 and 1) + stopped-foreign outcomes + memory keys"
mkclean() { mkdir -p "$1"; printf '{"status": "pass"}' > "$1/windows_prerun.json"; printf '101 simpleFoam 0-1\n102 simpleFoam 2-3\n' > "$1/rank_affinity.txt"
  { echo "epoch,elapsed_s,owned_cores,nonowned_linux_cores,nonowned_top,procstat_busy_cores,procstat_minus_perprocess_cores,bound_cpus_nonowned_cores,bound_cpus_procstat_minus_ranks_cores,steal_cores,psi_cpu_some_total_us,psi_cpu_some_frac,memavailable_mb,bound_cpu_mhz_mean,win_nonwsl_cores,win_top"
    echo "1,5.0,2.0,0.01,x(1) 0.010,2.0,0,0.0,0,0,,,20000,,0.1,"; echo "2,10.0,2.0,0.02,x(1) 0.020,2.0,0,0.0,0,0,,,19000,,0.1,"; } > "$1/isolation_samples.csv"
  { echo "epoch,elapsed_s,host_busy_cores,owned_ledger_cores,host_minus_owned_raw_cores,host_nonowned_cores,forks_delta,owned_new_seen,nonowned_new_seen"
    echo "1,5.0,2.05,2.0,0.05,0.05,3,1,0"; echo "2,10.0,2.08,2.0,0.08,0.08,2,0,1"; } > "$1/host_cpu_samples.csv"; }
sumline() { printf '# x\nsummary prerun=4 still_stopped=%s resumed=%s vanished=%s undecided=0 new_running=%s new_stopped=%s\n' "$@"; }
for k in 0 1 2 3 4 5; do mkclean $T/c$k; done
for k in 1 2 3 4; do cp "$A/stopped_foreign_prerun.txt" $T/c$k/; done
sumline 4 0 0 0 0 > $T/c1/stopped_foreign_postrun.txt; sumline 3 0 1 0 0 > $T/c2/stopped_foreign_postrun.txt; sumline 4 0 0 0 1 > $T/c3/stopped_foreign_postrun.txt; sumline 2 1 1 0 0 > $T/c4/stopped_foreign_postrun.txt
cp "$A2"/stopped_foreign_*.txt $T/c5/
withhelpers "$HERE/b2_run.sh" "$T/c1" 'mem_snapshot > $OUT/memory_prerun.txt; mem_snapshot > $OUT/memory_postrun.txt; dmesg_oom'
awk '$1 == "SwapFree:" { $2 = $2 - 2048 } 1' "$T/c1/memory_postrun.txt" > "$T/c1/mp" && mv "$T/c1/mp" "$T/c1/memory_postrun.txt"; echo "owned_session_majflt 42 processes 3" > "$T/c1/owned_majflt.txt"
for k in 0 1 2 3 4 5; do B2_NRANKS=2 python3 "$HERE/b2_isolation.py" evidence $T/c$k > /dev/null
  python3 -c 'import json,sys; e=json.load(open(sys.argv[1]+"/isolation_evidence.json")); print(sys.argv[1][-2:], e["contended"], e["stopped_foreign_override"], [r for r in e["contended_reasons"]])' $T/c$k; done > "$T/evE"; cat "$T/evE"
grep -q "^c0 no False \[\]$" "$T/evE" && grep -q "^c1 no True \[\]$" "$T/evE" \
  && grep -q "^c2 unknown True \['foreign stopped job vanished or new foreign job appeared during the run: CPU use not excluded (1 vanished, 0 new stopped)'\]$" "$T/evE" \
  && grep -q "^c3 unknown True \['foreign stopped job vanished or new foreign job appeared during the run: CPU use not excluded (0 vanished, 1 new stopped)'\]$" "$T/evE" \
  && grep -q "^c4 yes True \['foreign stopped job resumed during the run (1 resumed, 0 new running foreign offenders)', 'foreign stopped job vanished or new foreign job appeared" "$T/evE" \
  && grep -q "^c5 yes True \['foreign stopped job resumed during the run (0 resumed, 1 new running foreign offenders)', 'foreign stopped job vanished" "$T/evE" \
  && ok "evidence: clean -> no; override all still stopped -> no; vanished -> unknown; new_stopped -> unknown; resumed+vanished -> yes; pid reuse (A2) -> yes" || bad "evidence outcomes"
python3 - "$T" <<'PY2' > "$T/memE"; cat "$T/memE"
import json, sys, re
T = sys.argv[1]; e = json.load(open(f"{T}/c1/isolation_evidence.json")); e5 = json.load(open(f"{T}/c5/isolation_evidence.json")); e0 = json.load(open(f"{T}/c0/isolation_evidence.json"))
for k in ("stopped_foreign_count", "stopped_foreign_rss_mb_pre", "stopped_foreign_population", "run_memavailable_mb_min", "mem_memavailable_mb_start", "mem_swap_used_mb_start", "mem_swap_used_mb_end", "mem_swap_grew",
          "mem_pswpout_delta_host", "mem_owned_session_majflt", "mem_dmesg_oom"): print("c1", k, e[k])
post = [l for l in open(f"{T}/c5/stopped_foreign_postrun.txt") if re.match(r"(still_stopped|resumed|undecided|new_running|new_stopped) \d+ state=[Tt]+ ", l)]
print("c5 stopped_foreign_count_post", e5["stopped_foreign_count_post"], "expected", len(post), "rss_mb_post", e5["stopped_foreign_rss_mb_post"])
print("c0", e0["stopped_foreign_rss_mb_pre"], e0["mem_swap_grew"], e0["mem_owned_session_majflt"], e0["mem_owned_session_majflt_note"], e0["mem_dmesg_oom"])
ok = (e["stopped_foreign_count"] == 4 and e["run_memavailable_mb_min"] == 19000 and e["mem_swap_grew"] is True and abs(e["mem_swap_used_mb_end"] - e["mem_swap_used_mb_start"] - 2.0) < 1e-6
      and e["mem_owned_session_majflt"] == 42 and isinstance(e["mem_dmesg_oom"], list) and e5["stopped_foreign_count_post"] == len(post) and e0["mem_swap_grew"] is None and e0["mem_dmesg_oom"] == "not readable")
print("MEMOK" if ok else "MEMBAD")
PY2
grep -q MEMOK "$T/memE" && ok "memory keys: RSS/population pre, count/RSS post, min MemAvailable, swap start/end/grew, owned majflt, dmesg list; missing files -> None / 'not readable'" || bad "memory keys"

echo "== supplementary F: b2_analyse.py rows and ratio notes (fake B2_ROOT; the job logs are absent, so throughput is not computed; PYTHONPATH for b1_settle)"
an() {  # an <dir> <L16 evidence src> <L8x2 evidence src>
  for l in L16 L8x2; do mkdir -p "$1/b2/results_$l"; echo '{"controlled_end": true, "launch_epoch": 1}' > "$1/b2/results_$l/run_status.json"; done
  cp "$2/isolation_evidence.json" "$1/b2/results_L16/"; cp "$3/isolation_evidence.json" "$1/b2/results_L8x2/"
  PYTHONPATH="$HERE/../.." B2_ROOT="$1/b2" python3 "$HERE/b2_analyse.py" "$1/out.csv" > /dev/null
  python3 -c 'import csv,sys; r=list(csv.DictReader(open(sys.argv[1]))); x=r[-1]; l=[q for q in r if q.get("layout")=="L16" and q.get("jobs")][0]
print("ratio:", x["stopped_foreign_population_differs"], "|", x["swap_grew_layouts"], "|", x["note"][-230:]); print("L16 row:", {k: l[k][:60] for k in ("stopped_foreign_count", "stopped_foreign_rss_mb_pre", "mem_swap_grew", "mem_owned_session_majflt", "mem_dmesg_oom")})' "$1/out.csv"; }
an $T/anF1 $T/c1 $T/c5 | tee "$T/anF1.txt"; an $T/anF2 $T/c2 $T/c3 | tee "$T/anF2.txt"
grep -q "^ratio: True | L16 | .*stopped foreign population differs between layouts .*FLAG: swap grew during L16; swap growth not measured for L8x2" "$T/anF1.txt" && grep -q "'mem_swap_grew': 'True'" "$T/anF1.txt" \
  && grep -q "^ratio: False |  | .*swap growth not measured for L16 and L8x2" "$T/anF2.txt" && ! grep -q "population differs" "$T/anF2.txt" \
  && ok "analyse: population differs + swap-grew flag in the ratio row, memory columns on the rows; same population -> no note" || bad "analyse notes"


# ---------------- attempt 3 (audit SOL_FIX27_R2) ----------------
echo "== attempt 3 G1: admission, ONE snapshot per candidate (offender_scan from b2_run.sh; pgrep mocked to name chosen pids; proc_states made to fail for one stopped shim)"
"$T/bin/simpleFoam" 600 & G1S=$!; "$T/bin/simpleFoam" 600 & G1R=$!; "$T/bin/simpleFoam" 600 & G1U=$!; MINE+=($G1S $G1R $G1U); sleep 0.3; kill -STOP $G1S $G1U; sleep 0.2
GONE=$(( $(cat /proc/sys/kernel/pid_max) - 1 )); while [ -e /proc/$GONE ]; do GONE=$((GONE-1)); done
cat > "$T/g1.sh" <<'G1'
B2_ALLOW_STOPPED_FOREIGN=1
pgrep() { [ "$1 $2" = "-a -x" ] && for p in $G1S $G1R $GONE $G1U; do echo "$p simpleFoam 600"; done; :; }
eval "orig_$(declare -f proc_states)"; proc_states() { [ "$1" = "$G1U" ] && return 1; orig_proc_states "$1"; }
offender_scan; echo "STOPPEDK=[$STOPPEDK]"; echo "OFF1:"; echo "$OFF1"; echo "OFF2=[$OFF2]"
G1
withhelpers "$HERE/b2_run.sh" "$T" 'source $T/g1.sh' > "$T/g1.out"; cat "$T/g1.out"
grep -q "STOPPEDK=\[ $G1S:[0-9]* \]" "$T/g1.out" && grep -q "pid $G1R: simpleFoam 600 \[snapshot: state=[RS]" "$T/g1.out" && grep -q "pid $GONE: simpleFoam 600 \[snapshot: state=gone\]" "$T/g1.out" \
  && grep -q "pid $G1U: simpleFoam 600 \[snapshot: state=? " "$T/g1.out" \
  && ok "single snapshot: stopped -> ignored (pid:start kept); running, vanished (state=gone), unreadable thread states (state=?) -> offenders named with their snapshot" || bad "offender_scan"
kill -KILL $G1R $G1U 2>/dev/null

echo "== attempt 3 G2: pre-launch recheck through the real runner (fake powershell passes the Windows precheck; B2_STOP_BEFORE_LAUNCH=1 exits 3 before any launch)"
printf '#!/bin/bash\n[ -n "$FAKEPS_ACTION" ] && eval "$FAKEPS_ACTION"\nprintf "ELAPSED\\t1.0\\nSELF\\t1\\nNULLCPU\\t0\\n"\n' > "$T/bin/fakeps.sh"; chmod +x "$T/bin/fakeps.sh"
"$T/bin/simpleFoam" 600 & G2S=$!; MINE+=($G2S); sleep 0.3; kill -STOP $G2S; sleep 0.2
for i in $(seq 60); do awk '{exit !($1 < 1.4)}' /proc/loadavg && break; sleep 5; done; echo "load $(cut -d' ' -f1-3 /proc/loadavg) (the runner's guard needs < 1.5)"
rm -rf "$OUT"; run B2_ALLOW_STOPPED_FOREIGN=1 B2_POWERSHELL="$T/bin/fakeps.sh" B2_STOP_BEFORE_LAUNCH=1; echo "rc $(cat $T/rc)"; grep -v "^WARNING: B2_ALLOW" "$T/err"; grep -E "recheck|pause" "$OUT/host_before.txt" | cut -c1-230
[ "$(cat $T/rc)" = 3 ] && grep -q "^TEST: stopped before launch" "$T/err" && grep -q "^pre-launch offender recheck .*: passed" "$OUT/host_before.txt" && grep -q "^$G2S state=T " "$OUT/stopped_foreign_prerun.txt" \
  && ok "unchanged host: recheck passed (recorded in host_before.txt), stopped before launch" || bad "G2a recheck pass"
rm -rf "$OUT"; run B2_ALLOW_STOPPED_FOREIGN=1 B2_POWERSHELL="$T/bin/fakeps.sh" B2_STOP_BEFORE_LAUNCH=1 FAKEPS_ACTION="kill -CONT $G2S"; echo "rc $(cat $T/rc)"; grep -E "FAIL|pid $G2S:" "$T/err"
[ "$(cat $T/rc)" = 1 ] && grep -q "FAIL: pre-launch recheck: host busy" "$T/err" && grep -q "pid $G2S: .*snapshot: state=[RS]" "$T/err" && ! grep -q "^TEST: stopped" "$T/err" \
  && ok "shim resumed during the Windows precheck -> refused by the pre-launch recheck" || bad "G2b resumed"
kill -STOP $G2S; sleep 0.2
rm -rf "$OUT"; run B2_ALLOW_STOPPED_FOREIGN=1 B2_POWERSHELL="$T/bin/fakeps.sh" B2_STOP_BEFORE_LAUNCH=1 FAKEPS_ACTION="$T/bin/simpleFoam 600 > /dev/null 2>&1 & echo \$! > $T/g2c.pid; sleep 0.3; kill -STOP \$!"    # the sleep: the child must have redirected its stdout (else it holds the capture pipe)
G2N=$(cat "$T/g2c.pid"); MINE+=($G2N); echo "rc $(cat $T/rc) (new stopped shim $G2N)"; grep "FAIL" "$T/err" | cut -c1-200
[ "$(cat $T/rc)" = 1 ] && grep -q "FAIL: pre-launch recheck: the stopped foreign set (pid:start) changed" "$T/err" && grep -q " $G2N:[0-9]*" "$T/err" \
  && ok "new stopped foreign process between guard and launch -> refused (set changed)" || bad "G2c set changed"
kill -KILL $G2N 2>/dev/null; rm -rf "$OUT"

echo "== attempt 3 H: post-run exclusions of the runner/ancestors (SELFK), sampler (SPK), umbrella (UK) and session are pid+start based"
"$T/bin/simpleFoam" 600 & HR=$!; setsid "$T/bin/simpleFoam" 600 & HL=$!; MINE+=($HR $HL); sleep 0.3; HRS=$(cut -d' ' -f22 /proc/$HR/stat); HLS=$(cut -d' ' -f22 /proc/$HL/stat)
hcase() {  # hcase <name> <commands setting the exclusion tokens>
  local d=$T/h_$1; mkdir -p "$d"; withhelpers "$HERE/b2_run.sh" "$d" "{ echo '# test'; proc_info $S1; } > \$OUT/stopped_foreign_prerun.txt; session_pids() { ps -e -o pid=,sid= | awk -v s=\"\$U\" '\$2==s {print \$1}'; }; $2; stopped_postrun" 2> /dev/null
  echo "$1: $(grep -cE "^new_running ($HR|$HL) " "$d/stopped_foreign_postrun.txt") of the two shims reported"; }
{ hcase self_match "SELFK=\" $HR:$HRS \"; SPK=\"$HL:$HLS\""; hcase self_reused "SELFK=\" $HR:$((HRS-1)) \"; SPK=\"$HL:$((HLS-1))\""
  hcase uk_match "UK=\"$HR:$HRS\"; U=$HL; U_START=$HLS"; hcase uk_reused "UK=\"$HR:$((HRS-1))\"; U=$HL; U_START=$((HLS-1))"; } | tee "$T/h.out"
grep -q "^self_match: 0 " "$T/h.out" && grep -q "^self_reused: 2 " "$T/h.out" && grep -q "^uk_match: 0 " "$T/h.out" && grep -q "^uk_reused: 2 " "$T/h.out" \
  && ok "own pid+start -> excluded; same pids with another start time (reused) -> new_running; session members excluded only while U has its launch start time" || bad "pid+start exclusions"
HA=$T/h_a2; mkdir -p "$HA"; withhelpers "$HERE/../fix27_a2_snapshot/b2_run.sh" "$HA" "{ echo '# test'; proc_info $S1; } > \$OUT/stopped_foreign_prerun.txt; SELF=\" $HR \"; SP=$HL; stopped_postrun" 2> /dev/null
grep -qE "^new_running ($HR|$HL) " "$HA/stopped_foreign_postrun.txt" && bad "attempt-2 helpers unexpectedly report the shims" || ok "regression reproduced: attempt-2 helpers skip pids listed in SELF/SP whatever their start time"
kill -KILL $HR $HL 2>/dev/null

echo "== attempt 3 I1: host-level accounting on synthetic /proc/stat files and a synthetic owned ledger (b2_isolation.py functions)"
python3 - "$HERE" "$T" <<'PY' | tee "$T/i1.out"
import sys; sys.path.insert(0, sys.argv[1]); import b2_isolation as I; T = sys.argv[2]
open(f"{T}/stat0", "w").write("cpu  100 10 50 5000 70 5 5 3 7 0\ncpu0 50 5 25 2500 35 2 3 1 7 0\ncpu1 50 5 25 2500 35 3 2 2 0 0\nintr 1\nprocesses 1000\n")
open(f"{T}/stat1", "w").write("cpu  1000 10 50 9000 900 5 5 103 507 0\ncpu0 500 5 25 4500 450 2 3 51 507 0\ncpu1 500 5 25 4500 450 3 2 52 0 0\nintr 1\nprocesses 1040\n")
h0, h1 = I._hoststat(f"{T}/stat0"), I._hoststat(f"{T}/stat1")
print("busy ticks", h0["cpu"], h1["cpu"], "cpu0", h0["cpu0"], "processes", h0["processes"], h1["processes"])
ok1 = h0["cpu"] == 173 and h0["cpu0"] == 86 and h1["cpu"] - h0["cpu"] == 1000 and h1["processes"] - h0["processes"] == 40   # user+nice+system+irq+softirq+steal; guest (inside user), idle, iowait not added
# owned ledger {(pid, start): (utime+stime+cutime+cstime, ppid)}: runner 5, umbrella U 10; A (11) exits and is reaped by U; B (12) was reparented to init (ppid 1) and exits;
# C (13, start 4) exits (reaped by U) and its pid is reused by a new owned process (13, start 9); D is born and gone between the samples (only in U's cutime); E (14) existed, becomes owned now
prev = {(5, 0): (50, 1), (10, 1): (100, 5), (11, 2): (200, 10), (12, 3): (30, 1), (13, 4): (40, 10)}
cur = {(5, 0): (60, 1), (10, 1): (100 + 10 + 260 + 80 + 45, 5), (13, 9): (5, 10), (14, 5): (75, 10)}
prev_all = {**{k: v for k, (v, _) in prev.items()}, (14, 5): 70}; cur_keys = {k: v for k, (v, _) in cur.items()}
d = I.owned_ticks_delta(prev, cur, prev_all, cur_keys)
truth = 10 + 10 + 60 + 80 + 5 + 5 + 5          # runner own, U own, A tail, D, C tail, new (13,9), E since prev
print("owned ledger delta", d, "expected", truth)
b, o, raw, n = I.host_nonowned(h0, h1, d, 5.0); print("host busy", b, "owned", o, "raw", raw, "nonowned", n)
b2, o2, raw2, n2 = I.host_nonowned(h0, h1, 1500, 5.0); print("owned > host busy: raw", raw2, "clamped", n2)
tck = I.TCK; ok2 = d == truth and abs(b - 1000 / tck / 5) < 1e-9 and abs(n - (1000 - truth) / tck / 5) < 1e-9 and raw2 < 0 and n2 == 0.0
print("I1OK" if ok1 and ok2 else "I1BAD")
PY
grep -q I1OK "$T/i1.out" && ok "host busy (steal in, guest/iowait/idle out), per-CPU, forks; ledger: reaped by owned parent, born+gone between samples, reaped outside, pid reuse, newly owned; clamp at 0" || bad "host-level synthetic"

echo "== attempt 3 I2: real sampler (interval 4 s): an OWNED and then a NON-owned burst (3 busy loops of 2.5 s each), each started and ended between two samples"
I2=$T/i2; mkdir -p "$I2"
setsid bash -c "while [ ! -e $T/go_owned ]; do sleep 0.05; done; for i in 1 2 3; do timeout 2.5 sh -c 'while :; do :; done' & done; wait; sleep 60" & IU=$!     # the owned session (its leader = the sampler's 'mpirun')
"$T/bin/simpleFoam" 120 & IR=$!; MINE+=($IU $IR)                                                                                                  # a fake runner without children
TASK4_POWERSHELL=/bin/false B2_NRANKS=1 timeout 60 python3 "$HERE/b2_isolation.py" sample $IU $IR "$I2" 4 100000 & ISP=$!; MINE+=($ISP)
waitrows() { local i=0 L; until { mapfile -t L < "$I2/host_cpu_samples.csv"; } 2>/dev/null && [ ${#L[@]} -ge "$1" ] || [ $i -ge 200 ]; do sleep 0.1; i=$((i+1)); done; }    # builtins + sleep: little non-owned CPU of its own
waitrows 2; sleep 0.2; touch "$T/go_owned"                                             # data row 2 = the interval with the owned burst
waitrows 3; sleep 0.2
python3 -c 'import os, signal, time
signal.signal(signal.SIGCHLD, signal.SIG_IGN)                  # children auto-reaped: their CPU enters no cutime at all (the per-PID measure cannot see them)
for i in range(3):
    if os.fork() == 0:
        t = time.monotonic() + 2.5
        while time.monotonic() < t: pass
        os._exit(0)
time.sleep(12)' & NP=$!; MINE+=($NP)                                                       # data row 3 = the interval with the non-owned burst
waitrows 5; kill -TERM $ISP; wait $ISP 2>/dev/null; pkill -KILL -s $IU; wait $IU 2>/dev/null    # sampler first: the test shell (non-owned) reaps IU and gets its cutime (7.5 core-s)
printf '{"status": "pass"}' > "$I2/windows_prerun.json"; B2_NRANKS=1 python3 "$HERE/b2_isolation.py" evidence "$I2" > /dev/null
python3 - "$I2" <<'PY' | tee "$T/i2.out"
import csv, json, sys
d = sys.argv[1]; h = list(csv.DictReader(open(f"{d}/host_cpu_samples.csv"))); s = list(csv.DictReader(open(f"{d}/isolation_samples.csv")))
for i, (a, b) in enumerate(zip(h, s)): print(f"row {i + 1}: host_busy {a['host_busy_cores']} owned_ledger {a['owned_ledger_cores']} host_nonowned {a['host_nonowned_cores']} forks {a['forks_delta']} | per-PID owned {b['owned_cores']} nonowned {b['nonowned_linux_cores']} top {b['nonowned_top']}")
e = json.load(open(f"{d}/isolation_evidence.json")); print("evidence:", e["contended"], e["run_host_nonowned_cores"], e["run_linux_nonowned_cores"], e["contended_reasons"])
ro, rn = h[1], h[2]; so, sn = s[1], s[2]
ok = (float(ro["owned_ledger_cores"]) >= 1.5 and float(ro["host_nonowned_cores"]) < 0.6 and float(rn["host_nonowned_cores"]) >= 1.5 and float(sn["nonowned_linux_cores"]) < 0.5
      and "host-level non-owned CPU over threshold" in e["contended_reasons"] and "non-owned Linux CPU over threshold" not in e["contended_reasons"])
print("I2OK" if ok else "I2BAD")
PY
grep -q I2OK "$T/i2.out" && ok "owned burst -> owned ledger (via cutime), host non-owned low; non-owned burst between samples -> host-level non-owned >= 1.5 core, per-PID blind, evidence contended=yes 'host-level non-owned CPU over threshold'" || bad "host-level real sampler"
kill -KILL $NP $IR 2>/dev/null

echo "== attempt 3 J: b2_analyse.py exports mem_pswpin_delta_host, mem_pgmajfault_delta_host (and host_nonowned_cores_mean/max)"
python3 - "$T" <<'PY' | tee "$T/j.out"
import csv, json, sys
T = sys.argv[1]; r = list(csv.DictReader(open(f"{T}/anF1/out.csv"))); e = json.load(open(f"{T}/c1/isolation_evidence.json"))
job = [q for q in r if q.get("layout") == "L16" and not q.get("jobs")][0]; lay = [q for q in r if q.get("layout") == "L16" and q.get("jobs")][0]
ks = ("mem_pswpin_delta_host", "mem_pswpout_delta_host", "mem_pgmajfault_delta_host")
print("job row", {k: job.get(k) for k in ks + ("host_nonowned_cores_mean", "host_nonowned_cores_max")}); print("layout row", {k: lay.get(k) for k in ks}); print("evidence", {k: e[k] for k in ks})
ok = all(job.get(k) == str(e[k]) and lay.get(k) == str(e[k]) for k in ks) and job.get("host_nonowned_cores_mean") == "0.065" and job.get("host_nonowned_cores_max") == "0.08"
print("JOK" if ok else "JBAD")
PY
grep -q JOK "$T/j.out" && ok "analyse rows carry pswpin / pswpout / pgmajfault deltas and the host-level mean/max" || bad "analyse MEMK"

echo "== attempt 3 K: pause watcher record (host_before.txt lines) and paused.pids growth -> watcher_new -> contended=unknown"
printf '#!/bin/bash\nsleep 600\n' > "$T/bin/pause_marissa.sh"; chmod +x "$T/bin/pause_marissa.sh"; bash "$T/bin/pause_marissa.sh" --watch 50 & KW=$!; MINE+=($KW); sleep 0.3; MINE+=($(pgrep -P $KW))
printf '1 06:00 a\n2 06:00 b\n3 06:00 c\n' > "$T/paused.pids"; KD=$T/kdir; mkdir -p "$KD"
withhelpers "$HERE/b2_run.sh" "$KD" "PAUSED=$T/paused.pids; pause_watchers 2> $T/k.err; printf '%s' \"\$WATCH_REPORT\" > $T/k.out; echo PPL0=\$PPL0 >> $T/k.out; { echo '# test'; proc_info $S1; } > \$OUT/stopped_foreign_prerun.txt
  echo '4 07:00 simpleFoam caught' >> \$PAUSED; stopped_postrun 2>> $T/k.err"
withhelpers "$HERE/b2_run.sh" "$KD" "pgrep() { :; }; pause_watchers 2> $T/k2.err; printf '%s' \"\$WATCH_REPORT\"" > "$T/k2.out"
cat "$T/k.out" "$T/k.err" "$T/k2.out" "$T/k2.err" | cut -c1-230; grep -E "^#|^summary" "$KD/stopped_foreign_postrun.txt" | tail -3
mkclean "$T/c6"; cp "$KD"/stopped_foreign_*.txt "$T/c6/"; B2_NRANKS=2 python3 "$HERE/b2_isolation.py" evidence "$T/c6" > /dev/null
python3 -c 'import json,sys; e=json.load(open(sys.argv[1]+"/isolation_evidence.json")); print("c6", e["contended"], e["contended_reasons"])' "$T/c6" | tee "$T/k3.out"
grep -q "^pause watcher alive: pid $KW, form pause_marissa.sh --watch (/proc scan every 10 s), started .* for 50 s, running [0-9]* s, about [0-9]* s left" "$T/k.out" && grep -q "WARNING: pause watcher $KW ends before" "$T/k.err" && grep -q "^PPL0=3$" "$T/k.out" \
  && grep -q "^pause watcher alive: pid $LW, form pause_marissa_light.sh (pgrep scan every 30 s), started .* for 100000 s, running [0-9]* s, about 9[0-9]* s left" "$T/k.out" \
  && grep -q "watcher_new=1$" "$KD/stopped_foreign_postrun.txt" && grep -q "pause watcher stopped new processes" "$T/k.err" && grep -q "no 'pause_marissa_light2.sh <s>', 'pause_marissa_light.sh <s>' or 'pause_marissa.sh --watch <s>' process alive" "$T/k2.out" && grep -q "WARNING: no pause watcher alive" "$T/k2.err" \
  && grep -q "^c6 unknown .*'pause watcher stopped new processes during the run: CPU use not excluded (1 new lines in paused.pids)'\]$" "$T/k3.out" \
  && ok "watcher alive/remaining/short-watch warning (both forms), none alive -> warning; paused.pids +1 line -> watcher_new=1 -> contended=unknown" || bad "pause watcher"
kill -KILL $KW 2>/dev/null

# ---------------- Fable attempt 1 (audit SOL_FIX27_R3) ----------------
echo "== Fable L: watcher forms, remaining coverage and the refusal through the real runner (fake powershell passes; B2_STOP_BEFORE_LAUNCH=1 exits 3 after the rechecks; the pgrep wrapper hides the host's real watchers)"
printf '#!/bin/bash\n/usr/bin/pgrep "$@" | grep -Ev -e "^$$"'"'"'( |$)'"'"' -e "${FAKE_PGREP_HIDE:-/marissa_pause/}"\n' > "$T/bin/pgrep"; chmod +x "$T/bin/pgrep"      # the runner sees only the shims of this test; the wrapper hides itself (its own command line holds the offender patterns)
printf '#!/bin/bash\nsleep 600\n' > "$T/bin/pause_marissa.sh"; chmod +x "$T/bin/pause_marissa.sh"
lrun() { rm -rf "$OUT"; run B2_ALLOW_STOPPED_FOREIGN=1 B2_POWERSHELL="$T/bin/fakeps.sh" B2_STOP_BEFORE_LAUNCH=1 PATH="$T/bin:$PATH" "$@"; echo "rc $(cat $T/rc): $(grep -E '^FAIL|^TEST' $T/err | head -1 | cut -c1-200)"; }
for i in $(seq 60); do awk '{exit !($1 < 1.4)}' /proc/loadavg && break; sleep 5; done
lrun; grep -E "pause (watcher|log)|pre-launch pause" "$OUT/host_before.txt" > "$T/l1.txt"; cut -c1-250 "$T/l1.txt"
[ "$(cat $T/rc)" = 3 ] && grep -q "^pause watcher alive: pid $LW, form pause_marissa_light.sh (pgrep scan every 30 s), started .* for 100000 s, running [0-9]* s, about 9[0-9]* s left (ends about 2026-.*); B2_MAX_RUNTIME_S 14400; cmdline: bash $T/bin/pause_marissa_light.sh 100000" "$T/l1.txt" \
  && grep -q "^pre-launch pause watcher recheck .*: passed (1 alive, 9[0-9]* s left >= B2_MAX_RUNTIME_S 14400 s" "$T/l1.txt" && ! grep -q "WARNING: pause watcher" "$T/err" && ! grep -q "cmdline: .*/marissa_pause/" "$OUT/host_before.txt" \
  && ok "L1 light form: recognised, start time + remaining coverage recorded in host_before.txt, guard and pre-launch watcher recheck passed" || bad "L1"
bash "$T/bin/pause_marissa.sh" --watch 100000 & OW=$!; MINE+=($OW); sleep 0.3; MINE+=($(pgrep -P $OW))
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light"; grep -E "pause watcher" "$OUT/host_before.txt" | cut -c1-200 > "$T/l2.txt"; cat "$T/l2.txt"
[ "$(cat $T/rc)" = 3 ] && grep -q "^pause watcher alive: pid $OW, form pause_marissa.sh --watch (/proc scan every 10 s), started .* for 100000 s" "$T/l2.txt" && ! grep -q "pid $LW" "$T/l2.txt" && grep -q "recheck .*: passed (1 alive" "$T/l2.txt" \
  && ok "L2 old form (--watch) alone: recognised and accepted" || bad "L2"
kill -KILL $OW $(pgrep -P $OW) 2>/dev/null
lrun FAKE_PGREP_HIDE="pause_marissa"
[ "$(cat $T/rc)" = 1 ] && grep -q "^FAIL: pause watcher guard: B2_ALLOW_STOPPED_FOREIGN=1 needs a live pause watcher .*: none alive" "$T/err" && [ ! -e "$OUT" ] && ! grep -q "^TEST: stopped" "$T/err" \
  && ok "L3 no watcher alive + override -> REFUSED before the results directory exists" || bad "L3"
bash "$T/bin/pause_marissa_light.sh" 50 & SW=$!; MINE+=($SW); sleep 0.3; MINE+=($(pgrep -P $SW))
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000"
[ "$(cat $T/rc)" = 1 ] && grep -q "^FAIL: pause watcher guard: the pause watcher's remaining coverage ([0-9]* s) is shorter than B2_MAX_RUNTIME_S (14400 s)" "$T/err" && grep -q "^WARNING: pause watcher $SW ends before" "$T/err" && [ ! -e "$OUT" ] \
  && ok "L4a watcher with 50 s left < B2_MAX_RUNTIME_S 14400 -> REFUSED (WARNING names the watcher)" || bad "L4a"
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000" B2_MAX_RUNTIME_S=20
[ "$(cat $T/rc)" = 3 ] && grep -q "^pause watcher alive: pid $SW, form pause_marissa_light.sh .* for 50 s, .* B2_MAX_RUNTIME_S 20;" "$OUT/host_before.txt" && grep -q "recheck .*: passed (1 alive, [0-9]* s left >= B2_MAX_RUNTIME_S 20 s" "$OUT/host_before.txt" \
  && ok "L4b the same watcher with B2_MAX_RUNTIME_S=20 -> accepted" || bad "L4b"
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000" B2_MAX_RUNTIME_S=20 FAKEPS_ACTION="kill -KILL $SW $(pgrep -P $SW)"
[ "$(cat $T/rc)" = 1 ] && grep -q "^FAIL: pre-launch recheck: B2_ALLOW_STOPPED_FOREIGN=1 needs a live pause watcher .*: none alive" "$T/err" && grep -q "^pause watcher alive: pid $SW" "$OUT/host_before.txt" && ! grep -q "^TEST: stopped" "$T/err" \
  && ok "L4c watcher dies during the Windows precheck -> REFUSED by the pre-launch watcher recheck (the guard had passed)" || bad "L4c"
bash "$T/bin/pause_marissa_light.sh" & DW=$!; MINE+=($DW); sleep 0.3; MINE+=($(pgrep -P $DW))                    # no argument: the script's default 36000 s
bash -c "echo pause_marissa_light.sh 99999 > /dev/null; sleep 600; true" & MW=$!; MINE+=($MW); sleep 0.3; MINE+=($(pgrep -P $MW))     # a shell that merely mentions the name, argv[0..1] = bash -c (the trailing true keeps bash from exec-ing sleep)
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000"; grep -E "pause watcher" "$OUT/host_before.txt" | cut -c1-200 > "$T/l5.txt"; cat "$T/l5.txt"
[ "$(cat $T/rc)" = 3 ] && grep -q "^pause watcher alive: pid $DW, form pause_marissa_light.sh .* for 36000 s, running [0-9]* s, about 359[0-9]* s left" "$T/l5.txt" && ! grep -q "alive: pid $MW" "$T/l5.txt" \
  && ok "L5 light form without argument -> the script's default 36000 s; a command line that only mentions the name is not a watcher" || bad "L5"
kill -KILL $DW $SW $(pgrep -P $DW) $(pgrep -P $SW) 2>/dev/null; rm -rf "$OUT"
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000"
[ "$(cat $T/rc)" = 1 ] && grep -q "needs a live pause watcher .*: none alive" "$T/err" && grep -q "pause watcher candidate ignored (unrecognised form): pid $MW" "$T/err" \
  && ok "L6 only the name-mentioning shell left -> refused, listed as 'candidate ignored (unrecognised form)'" || bad "L6"
kill -KILL $MW $(pgrep -P $MW) 2>/dev/null; rm -f "$T/bin/pgrep"
run B2_ROOT="$T/nocalib" B2_CALIB_ENDTIME=150; grep -q "^FAIL: B2_CALIB_ENDTIME=150 is accepted only for layout L16 with a B2_ROOT under /b2_calib/" "$T/err" && ok "L7 B2_CALIB_ENDTIME outside /b2_calib/ -> refused" || bad "L7"
mkdir -p "$T/b2_calib/x/L16"; cp -r "$C" "$T/b2_calib/x/L16/case"; echo "endTime 150;" > "$T/b2_calib/x/L16/case/system/controlDict"
run B2_ROOT="$T/b2_calib/x" B2_CALIB_ENDTIME=150 B2_ALLOW_STOPPED_FOREIGN=1 B2_POWERSHELL="$T/bin/fakeps.sh" B2_STOP_BEFORE_LAUNCH=1 B2_MAX_RUNTIME_S=20
[ "$(cat $T/rc)" = 3 ] && grep -q "^CALIBRATION RUN (B2_CALIB_ENDTIME=150, B2_ROOT $T/b2_calib/x): .* NOT a B2 measurement" "$T/b2_calib/x/results_L16/host_before.txt" && ok "L8 calibration copy under /b2_calib/ with endTime 150 -> accepted and marked CALIBRATION in host_before.txt" || bad "L8"
rm -rf "$T/b2_calib/x/results_L16"; run B2_ROOT="$T/b2_calib/x" B2_ALLOW_STOPPED_FOREIGN=1 B2_POWERSHELL="$T/bin/fakeps.sh" B2_STOP_BEFORE_LAUNCH=1 B2_MAX_RUNTIME_S=20; grep -q "endTime is not 1600" "$T/err" && ok "L9 the same copy without B2_CALIB_ENDTIME -> refused (endTime is not 1600)" || bad "L9"

echo "== Fable M: evidence p95, forks labelled as an upper bound, informational host-level mode (gross thresholds -> unknown, never yes)"
python3 - "$HERE" "$T" <<'PY' | tee "$T/m.out"
import sys, json, os, csv; sys.path.insert(0, sys.argv[1]); import b2_isolation as I; T = sys.argv[2]
e = json.load(open(f"{T}/i2/isolation_evidence.json")); h = list(csv.DictReader(open(f"{T}/i2/host_cpu_samples.csv")))
v = sorted(float(r["host_nonowned_cores"]) for r in h); p95 = v[max(0, -(-95 * len(v) // 100) - 1)]
print("i2 host stat", e["run_host_nonowned_cores"], "p95 expected", round(p95, 4)); print("host_forks", e["host_forks"])
ok1 = e["run_host_nonowned_cores"]["p95"] == round(p95, 4) and "nonowned_forks_upper_bound" in e["host_forks"] and "forks_minus_owned_seen" not in e["host_forks"] and "UPPER BOUND" in e["host_forks"]["note"] and e["host_level_mode"] == "criterion"
I.HOST_MODE = "informational"; I.evidence(f"{T}/i2"); e2 = json.load(open(f"{T}/i2/isolation_evidence.json")); print("informational, max 1.93:", e2["contended"], [r for r in e2["contended_reasons"] if "host-level" in r], e2["host_level_mode"])
rows = list(csv.DictReader(open(f"{T}/i2/host_cpu_samples.csv"))); rows[2]["host_nonowned_cores"] = "4.5"
with open(f"{T}/i2/host_cpu_samples.csv", "w", newline="") as fh: w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
I.evidence(f"{T}/i2"); e3 = json.load(open(f"{T}/i2/isolation_evidence.json")); print("informational, max 4.5:", e3["contended"], [r for r in e3["contended_reasons"] if "host-level" in r])
I.HOST_MODE = "criterion"; I.evidence(f"{T}/i2"); e4 = json.load(open(f"{T}/i2/isolation_evidence.json")); print("criterion, max 4.5:", e4["contended"], [r for r in e4["contended_reasons"] if "host-level" in r])
ok2 = (not [r for r in e2["contended_reasons"] if "host-level" in r] and e2["host_level_mode"] == "informational" and "informational" in e2["host_level_rule"]
       and e3["contended"] == "unknown" and [r for r in e3["contended_reasons"] if r.startswith("host-level non-owned CPU over the gross threshold")] and e4["contended"] == "yes" and "host-level non-owned CPU over threshold" in e4["contended_reasons"])
r = list(csv.DictReader(open(f"{T}/anF1/out.csv"))); job = [q for q in r if q.get("layout") == "L16" and not q.get("jobs")][0]; print("analyse job row host_nonowned_forks_upper_bound", repr(job.get("host_nonowned_forks_upper_bound")))
print("MOK" if ok1 and ok2 and "host_nonowned_forks_upper_bound" in job else "MBAD")
PY
grep -q MOK "$T/m.out" && ok "p95 in the evidence stats; host_forks.nonowned_forks_upper_bound labelled UPPER BOUND (also an analyse column); informational mode: 1.93 core -> no host reason, 4.5 core -> unknown (gross), criterion mode -> yes" || bad "Fable M"

# ---------------- Fable attempt 2 (FABLE_BRIEF_27b) ----------------
echo "== Fable N: the third watcher form pause_marissa_light2.sh <s> (N1-N4, through the real runner, host watchers hidden), the host's live watcher (N5, read only), the calibrated thresholds (N6, N7)"
printf '#!/bin/bash\n/usr/bin/pgrep "$@" | grep -Ev -e "^$$"'"'"'( |$)'"'"' -e "${FAKE_PGREP_HIDE:-/marissa_pause/}"\n' > "$T/bin/pgrep"; chmod +x "$T/bin/pgrep"
printf '#!/bin/bash\nsleep 600\n' > "$T/bin/pause_marissa_light2.sh"; chmod +x "$T/bin/pause_marissa_light2.sh"
bash "$T/bin/pause_marissa_light2.sh" 100000 & XW=$!; MINE+=($XW); sleep 0.3; MINE+=($(pgrep -P $XW))
for i in $(seq 60); do awk '{exit !($1 < 1.4)}' /proc/loadavg && break; sleep 5; done
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000"; grep -E "pause watcher|pre-launch pause" "$OUT/host_before.txt" | cut -c1-400 > "$T/n1.txt"; cat "$T/n1.txt"
[ "$(cat $T/rc)" = 3 ] && grep -q "^pause watcher alive: pid $XW, form pause_marissa_light2.sh (two pgrep calls every 30 s, seen PIDs skipped), started .* for 100000 s, running [0-9]* s, about 9[0-9]* s left (ends about 2026-.*); B2_MAX_RUNTIME_S 14400; cmdline: bash $T/bin/pause_marissa_light2.sh 100000" "$T/n1.txt" \
  && ! grep -q "alive: pid $LW" "$T/n1.txt" && grep -q "^pre-launch pause watcher recheck .*: passed (1 alive, 9[0-9]* s left >= B2_MAX_RUNTIME_S 14400 s" "$T/n1.txt" && ! grep -q "WARNING: pause watcher" "$T/err" \
  && ok "N1 light2 form alone: recognised, start time + remaining coverage recorded, guard and pre-launch recheck passed" || bad "N1"
bash "$T/bin/pause_marissa_light2.sh" 30 & XS=$!; MINE+=($XS); sleep 0.3; MINE+=($(pgrep -P $XS))
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000|pause_marissa_light2.sh 100000"
[ "$(cat $T/rc)" = 1 ] && grep -q "^FAIL: pause watcher guard: the pause watcher's remaining coverage ([0-9]* s) is shorter than B2_MAX_RUNTIME_S (14400 s)" "$T/err" && grep -q "^WARNING: pause watcher $XS ends before" "$T/err" && [ ! -e "$OUT" ] \
  && ok "N2 light2 form with 30 s left < B2_MAX_RUNTIME_S -> REFUSED before the results directory exists (the coverage rule applies to the new form)" || bad "N2"
kill -KILL $XS $(pgrep -P $XS) 2>/dev/null
bash "$T/bin/pause_marissa_light2.sh" & XD=$!; MINE+=($XD); sleep 0.3; MINE+=($(pgrep -P $XD))                   # no argument: the script's default 36000 s (${1:-36000})
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000|pause_marissa_light2.sh 100000"; grep -E "pause watcher" "$OUT/host_before.txt" | cut -c1-200 > "$T/n3.txt"; cat "$T/n3.txt"
[ "$(cat $T/rc)" = 3 ] && grep -q "^pause watcher alive: pid $XD, form pause_marissa_light2.sh .* for 36000 s, running [0-9]* s, about 359[0-9]* s left" "$T/n3.txt" && ok "N3 light2 form without argument -> the script's default 36000 s" || bad "N3"
kill -KILL $XD $XW $(pgrep -P $XD) $(pgrep -P $XW) 2>/dev/null; rm -rf "$OUT"
lrun FAKE_PGREP_HIDE="/marissa_pause/|pause_marissa_light.sh 100000"
[ "$(cat $T/rc)" = 1 ] && grep -q "needs a live pause watcher (pause_marissa_light2.sh <s>, pause_marissa_light.sh <s> or pause_marissa.sh --watch <s>) .*: none alive" "$T/err" && grep -q "no 'pause_marissa_light2.sh <s>', 'pause_marissa_light.sh <s>' or 'pause_marissa.sh --watch <s>' process alive" "$T/err" && [ ! -e "$OUT" ] \
  && ok "N4 no watcher of any of the three forms -> REFUSED; the messages name all three forms" || bad "N4"
rm -f "$T/bin/pgrep"
HW=$(cat /home/azan/paper6_t6_work/marissa_pause/watcher.pid 2>/dev/null); HC=$(tr '\0' ' ' < /proc/${HW:-0}/cmdline 2>/dev/null)     # the host's real watcher: only read (pgrep, ps, /proc)
if [[ "$HC" == *pause_marissa_light2.sh* ]]; then
  ND=$T/n5; mkdir -p "$ND"; withhelpers "$HERE/b2_run.sh" "$ND" "PAUSED=/home/azan/paper6_t6_work/marissa_pause/paused.pids; pause_watchers 2> $T/n5.err; printf '%s' \"\$WATCH_REPORT\"" > "$T/n5.out"; cut -c1-230 "$T/n5.out"
  grep -q "^pause watcher alive: pid $HW, form pause_marissa_light2.sh (two pgrep calls every 30 s, seen PIDs skipped), started 2026-.* for 43200 s, running [0-9]* s, about [0-9]* s left (ends about 2026-.*); B2_MAX_RUNTIME_S 14400; cmdline: /bin/bash /home/azan/paper6_t6_work/marissa_pause/pause_marissa_light2.sh 43200" "$T/n5.out" \
    && ! grep -q "WARNING: pause watcher $HW ends before" "$T/n5.err" && ok "N5 the host's live watcher (pid $HW: pause_marissa_light2.sh 43200) is recognised with its start time and remaining coverage >= 14400 s (read only)" || bad "N5"
else echo "N5 skipped: no live host watcher of the light2 form (watcher.pid '$HW': '${HC:0:80}')"; fi
python3 - "$HERE" <<'PY2' | tee "$T/n6.out"
import sys, json; sys.path.insert(0, sys.argv[1]); import b2_isolation as I
f = "/home/azan/paper6_t6_work/b2_calib/20261001_074246/calibration.json"; c = json.load(open(f)); s = c["host_nonowned_cores_all"]; r = I.calib_rule(s["mean"], s["p95"], s["max"]); j = c["threshold_rule"]
print("calibration.json", c["calibration_run"], "mean/p95/max", s["mean"], s["p95"], s["max"], "-> calib_rule", r["HOST_MODE"], r["HOST_MEAN_MAX"], r["HOST_MAX_MAX"], "| in the file", j["HOST_MODE"], j["HOST_MEAN_MAX"], j["HOST_MAX_MAX"],
      "| deployed", I.HOST_MODE, I.HOST_MEAN_MAX, I.HOST_MAX_MAX, I.CALIB_RUN)
edge = [I.calib_rule(0.0, 0.0, 0.0), I.calib_rule(0.2499, 0.9999, 0.3), I.calib_rule(0.25, 0.5, 0.3), I.calib_rule(0.1, 1.0, 0.3), I.calib_rule(None, None, None)]
print("edges (0,0,0) (0.2499,0.9999,0.3) (0.25,..) (..,1.0,..) (None):", [(e.get("HOST_MODE"), e.get("HOST_MEAN_MAX"), e.get("HOST_MAX_MAX")) for e in edge])
ok = ((r["HOST_MODE"], r["HOST_MEAN_MAX"], r["HOST_MAX_MAX"]) == (j["HOST_MODE"], j["HOST_MEAN_MAX"], j["HOST_MAX_MAX"]) == (I.HOST_MODE, I.HOST_MEAN_MAX, I.HOST_MAX_MAX) == ("criterion", 0.48, 1.62) and r["usable"] is True
      and (I.CALIB_MEAN, I.CALIB_P95, I.CALIB_MAX, I.CALIB_RUN) == (s["mean"], s["p95"], s["max"], c["calibration_run"]) and c["samples"] == 103 and c["controlled_end"] is True and c["iterations_run"] == 150
      and (edge[0]["HOST_MEAN_MAX"], edge[0]["HOST_MAX_MAX"]) == (0.30, 1.25) and (edge[1]["HOST_MODE"], edge[1]["HOST_MEAN_MAX"]) == ("criterion", 0.5) and edge[2]["HOST_MODE"] == edge[3]["HOST_MODE"] == "informational" and edge[4]["usable"] is None)
print("N6OK" if ok else "N6BAD")
PY2
grep -q N6OK "$T/n6.out" && ok "N6 calib_rule on calibration.json 20261001_074246 -> criterion 0.48 / 1.62 = the file's threshold_rule = the deployed HOST_* constants (CALIB_* = the file's figures); floor 0.30 / 1.25 at zero noise; mean >= 0.25 or p95 >= 1.0 -> informational" || bad "N6"
python3 - "$HERE" "$T" <<'PY2' | tee "$T/n7.out"
import sys, json, csv; sys.path.insert(0, sys.argv[1]); import b2_isolation as I; T = sys.argv[2]; d = f"{T}/i2"
def run(mx):
    rows = list(csv.DictReader(open(f"{d}/host_cpu_samples.csv"))); rows[2]["host_nonowned_cores"] = str(mx)
    with open(f"{d}/host_cpu_samples.csv", "w", newline="") as fh: w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    I.evidence(d); e = json.load(open(f"{d}/isolation_evidence.json")); h = [r for r in e["contended_reasons"] if "host-level" in r]; print(f"criterion mode, sample max {mx}: host stat {e['run_host_nonowned_cores']} host reasons {h}"); return e, h
e1, h1 = run(1.61); e2, h2 = run(1.62)
print("N7OK" if not h1 and h2 == ["host-level non-owned CPU over threshold"] and e2["contended"] == "yes" and "0.48" in e1["host_level_rule"] and "1.62" in e1["host_level_rule"] and "20261001_074246" in e1["host_level_rule"] else "N7BAD")
PY2
grep -q N7OK "$T/n7.out" && ok "N7 evidence at the calibrated thresholds: a sample of 1.61 core gives no host-level reason, 1.62 core gives contended=yes; host_level_rule names 0.48 / 1.62 and the calibration stamp" || bad "N7"

echo "== result: $PASS passed, $FAILN failed"; [ $FAILN -eq 0 ]
