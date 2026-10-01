# FIX27 report: B2 runner accepts SIGSTOPped foreign jobs (explicit, recorded override B2_ALLOW_STOPPED_FOREIGN=1)
Work only in fix27/ (copies of b2_run.sh, b2_isolation.py, b2_analyse.py, b2_design.md; new test_fix27.sh, test_fix27.out). b2_run.sh was not run for real, no solver/mpirun was started, and no signal went to any process except the shims the test started itself. The host's paused processes were only read through /proc and pgrep.

## Changes
**b2_run.sh**
- Header: documents the override.
- The offender patterns are now variables `PAT1` (pgrep -x) and `PAT2` (pgrep -f), unchanged, so the post-run check reuses them.
- Helpers:
  - `proc_states` returns the state letter of every thread from `/proc/<pid>/task/*/stat`. It returns 1 if the process has no readable thread or any thread's state is unreadable or malformed.
  - `is_stopped` is true only if every thread is `T` or `t`.
  - `proc_info` prints one line: pid, distinct thread states, thread count, cpu_ticks = utime+stime+cutime+cstime, starttime, VmRSS and cmdline. NUL, newline and CR in the cmdline become spaces.
  - `stopped_postrun` does the post-run check.
- Offender guard: with `B2_ALLOW_STOPPED_FOREIGN=1`, each offender line from OFF1 and OFF2 goes through `is_stopped`.
  - A stopped process is dropped from the offender lists and collected in `$STOPPED`, de-duplicated by pid.
  - All other processes stay offenders. That includes unreadable ones and mixed-thread ones.
  - The runner's own ancestors are still excluded by the existing `SELF` filter. Nothing of the run exists before launch, so "not owned" = not in `SELF`.
  - The refusal message states how many stopped processes were ignored. Without the override the code path is identical to before.
- After `mkdir $OUT`: `$OUT/stopped_foreign_prerun.txt` is written. It has a header, the RSS sum and one `proc_info` line per ignored process. A WARNING line goes to stderr.
- `host_before.txt` gets one more line, `stopped foreign processes ignored (B2_ALLOW_STOPPED_FOREIGN=1): N (RSS X MB; ...)`, only when the override is used. The `load at start` line is unchanged, so b2_analyse's regex still works.
- The load, disk, Windows and exclusivity guards are unchanged.
- End of run: after the session stop and the sampler exit, and before `evidence`, `stopped_postrun` runs if the pre-run list exists. It writes `$OUT/stopped_foreign_postrun.txt`:
  - Each pre-run process is one of:
    - `still_stopped`: same pid and start time, every thread T/t, and CPU ticks unchanged.
    - `resumed`: CPU ticks grew (it ran even if it is stopped again now), or it is not stopped now.
    - `vanished`: gone, or the pid was reused (start time differs).
    - `undecided`: state unreadable.
  - Then a fresh PAT1/PAT2 scan, excluding SELF, the sampler, the run's session and the pre-run pids, gives `new_running` and `new_stopped`.
  - Last line: `summary prerun= still_stopped= resumed= vanished= undecided= new_running= new_stopped=`.
  - If resumed + new_running > 0, it prints `WARNING: foreign stopped job resumed during the run ... contended=yes`. If undecided > 0, it prints a WARNING that contended is unknown.

**b2_isolation.py (evidence)**
- New keys: `stopped_foreign_override` (true if the pre-run list exists), `stopped_foreign_count`, `stopped_foreign_postrun` (the parsed summary) and `stopped_foreign_note`.
- These add entries to the existing `contended_reasons` mechanism:
  - resumed or new_running > 0 → **yes**: `foreign stopped job resumed during the run (N resumed, M new running foreign offenders)`
  - postrun file missing → **unknown**: `foreign stopped job resumed during the run: not decidable (stopped_foreign_postrun.txt missing)`
  - undecided > 0 → **unknown**: `...: not decidable (k with unreadable state)`
- `contended_rule` text is extended. The sampler is unchanged.

**b2_analyse.py**
- `stopped_foreign_override` and `stopped_foreign_count` are added to every job row and every layout summary row, as a note only.
- The new reasons are not in `WINDOWS_REASONS`, so a resumed stopped job makes the layout INVALID through the existing rule. No new validity criterion.
- The docstring has one line about this.

**b2_design.md**
- New paragraph "Paused foreign jobs (2026-10-01)": what the override does; stopped processes hold memory (about 5.5 GB RSS; MemAvailable is recorded) but use no CPU; the post-run check and how it reaches `contended`; vanished processes are not decided by the post-run check.

## Tests
- `bash -n` passes on b2_run.sh, test_fix27.sh, ../b2_jobs.sh and ../b2_rank.sh.
- `python3 -m py_compile` passes on b2_isolation.py and b2_analyse.py.

How test_fix27.sh works:
- It uses a fake `B2_ROOT` holding a minimal prepared L16 case, with `B2_SKIP_FOAM_ENV=1`.
- `B2_POWERSHELL=/bin/false` without `B2_ALLOW_NO_WINDOWS_CHECK`, so the runner exits at the Windows guard. That guard comes after the offender, load and disk guards and after mkdir. The runner never launches.
- Shims:
  - A copy of `sleep` named `simpleFoam`. `exec -a` would not work because `pgrep -x` matches the comm, which comes from the file name, not argv[0].
  - A script `t_queue_shim.sh`, which matches `queue.*\.sh`.
- Case 4 uses a python child whose comm is simpleFoam and which has 2 threads. Its parent attaches with `PTRACE_SEIZE` + `PTRACE_INTERRUPT` to the main thread only, so `/proc/<pid>/stat` says `t` while the second thread is `S`. This is the case a check of the main thread alone would get wrong.
- Supplementary sections (not the runner's main path):
  - A: `stopped_postrun`, extracted from b2_run.sh.
  - B: `b2_isolation.py evidence` run on fabricated result directories.
- All shims are killed at exit and the temp directory is removed.
- The scan is host-wide, so the host's 31 real paused processes are listed as well, read only. With the 2 stopped shims that makes 33 ignored.

Output (test_fix27.out, trimmed; the runner's own `FAIL:` lines are its expected refusal messages):
```
shims: S1 1406961 (T), S2 1406962 (T)
== case 1: stopped shims + override -> passes the offender guard, lists them, exits at the Windows guard
WARNING: B2_ALLOW_STOPPED_FOREIGN=1: 33 stopped foreign processes ignored by the offender guard (RSS 5626 MB), listed in /tmp/fix27test.MHSqfB/b2/results_L16/stopped_foreign_prerun.txt
{"status": "unavailable", "sum_nonexcluded_cores": null, "max_process_cores": null, "offenders": null, "error": "/bin/false rc 1: "}
FAIL: Windows check unavailable; override B2_ALLOW_NO_WINDOWS_CHECK=1
PASS: offender guard passed (rc 1, stopped at the Windows guard)
PASS: pid 1406961 listed in stopped_foreign_prerun.txt
PASS: pid 1406962 listed in stopped_foreign_prerun.txt
--- stopped_foreign_prerun.txt (head)
# B2_ALLOW_STOPPED_FOREIGN=1 2026-10-01 06:03:38: foreign offender processes ignored by the pre-run guard because every thread is stopped (T/t); they hold memory (RSS sum 5626 MB) but use no CPU
# pid state=<thread states> threads=<n> cpu_ticks=<utime+stime+cutime+cstime> start=<starttime> rss_kb=<VmRSS> cmdline
1323410 state=T threads=1 cpu_ticks=1045044 start=23884552 rss_kb=453684 simpleFoam 
1323417 state=T threads=1 cpu_ticks=1041195 start=23884554 rss_kb=293636 simpleFoam 
... 33 entries
PASS: one line per ignored process (33)
== case 2: stopped shims, no override -> refused
FAIL: host busy; solver/mesher processes:
  pid 1406961: /tmp/fix27test.MHSqfB/bin/simpleFoam 600
  pid 1406962: /bin/bash /tmp/fix27test.MHSqfB/bin/t_queue_shim.sh
PASS: refused, both shims named, no OUT
== case 3: running shim + override -> refused (the stopped shims are not named as offenders)
FAIL: host busy (B2_ALLOW_STOPPED_FOREIGN=1: 33 stopped foreign processes ignored); solver/mesher processes:
  pid 1407916: /tmp/fix27test.MHSqfB/bin/simpleFoam 600
launcher/queue/heavy post-processing jobs:
  none
PASS: refused on running pid 1407916 only
== case 4: one stopped (main, ptrace group-stop 't') + one running thread, comm simpleFoam, + override -> counts as running, refused
mixed pid 1408734: ptrace rc 0/0 errno 0; /proc/1408734/stat state t; thread states tS
FAIL: host busy (B2_ALLOW_STOPPED_FOREIGN=1: 33 stopped foreign processes ignored); solver/mesher processes:
  pid 1408734: python3 - /tmp/fix27test.MHSqfB/mixed.pid
launcher/queue/heavy post-processing jobs:
  none
PASS: mixed-thread process 1408734 (main thread t, one thread running) refused as running
== supplementary A: stopped_postrun (helpers extracted from b2_run.sh)
stopped foreign processes: summary prerun=4 still_stopped=1 resumed=2 vanished=1 undecided=0 new_running=1 new_stopped=32
WARNING: foreign stopped job resumed during the run (2 resumed, 1 new running foreign offenders; see /tmp/fix27test.MHSqfB/postA/stopped_foreign_postrun.txt): contended=yes
still_stopped 1406961 state=T threads=1 cpu_ticks=0 start=24986614 rss_kb=1792 /tmp/fix27test.MHSqfB/bin/simpleFoam 600 
resumed 1409550 state=S threads=1 cpu_ticks=0 start=24987087 rss_kb=1792 /tmp/fix27test.MHSqfB/bin/simpleFoam 600  (pre-run cpu_ticks=0)
resumed 1409551 state=T threads=1 cpu_ticks=130 start=24987087 rss_kb=3072 bash -c while :; do :; done  (pre-run cpu_ticks=30)
vanished 1409552 (pre-run: state=T cpu_ticks=0 start=24987087 rss_kb=1792 /tmp/fix27test.MHSqfB/bin/simpleFoam 600)
new_running 1409869 state=S threads=1 cpu_ticks=0 start=24987275 rss_kb=1792 /tmp/fix27test.MHSqfB/bin/simpleFoam 600 
summary prerun=4 still_stopped=1 resumed=2 vanished=1 undecided=0 new_running=1 new_stopped=32
PASS: postrun: still_stopped / resumed (running) / resumed (stopped again, CPU grew) / vanished / new_running
== supplementary B: b2_isolation.py evidence on fabricated results
ev1 yes True 4 ['foreign stopped job resumed during the run (2 resumed, 1 new running foreign offenders)']
ev2 unknown True 4 []
ev3 unknown True 4 ['foreign stopped job resumed during the run: not decidable (stopped_foreign_postrun.txt missing)']
PASS: evidence: resumed -> yes with the reason; all still stopped -> no stopped-foreign reason; postrun missing -> unknown
== result: 9 passed, 0 failed
```

## Open points
1. **Vanished processes**: a pre-run stopped process that disappears during the run (killed, or resumed and then exited) is listed as `vanished`. It does not set contended, which follows the brief's triggers: running at the end, or a new running offender. Any CPU it used while resumed is in the sampler's non-owned measurement: its own CPU between samples, and via cutime if its non-owned parent reaps it. If the coordinator wants `vanished` to make contended `unknown`, it is one line in `evidence`.
2. **Short resume, then stopped again**: this is caught by the growth of CPU ticks (utime+stime+cutime+cstime), shown in supplementary A with a busy loop. A resume that uses less than one clock tick (10 ms) is not visible that way. The sampler covers the same interval.
3. **New stopped processes** (`new_stopped`): a new foreign process that the watcher stopped during the run is listed but does not set contended. It may have run briefly before being stopped; that CPU is in the sampler's measurement.
4. **Races are conservative.**
   - A process that exits between pgrep and the state read is not ignored (unreadable), so the guard refuses. The next attempt passes.
   - A pre-run process that is resumed between the guard check and the listing is still listed as stopped. The post-run check then shows it as `resumed`.
5. **Not covered by test_fix27.sh**:
   - The `host_before.txt` line and the call to `stopped_postrun` in the real end path. Both are only reached after launch, and the brief forbids reaching launch. Code inspection only.
   - The "state cannot be read → not ignored" branch. It could not be created with an unprivileged shim. It is in `proc_states`: `cat` failure or a malformed state letter → return 1.
6. **Host-wide dependency**: case 1 depends on the host having no running offender and a 1-min load < 1.5 at test time. Here it held: load 0.29, all real offenders in state T. If the pause watcher misses a new Marissa process, case 1 fails the same way the real run would refuse.
7. **Memory**: the stopped processes hold about 5.6 GB RSS, measured 5626 MB at test time. This is recorded, not a criterion. They may be paged out under pressure. `run_memavailable_mb_min` in the evidence shows the margin.

## Attempt 2
This attempt addresses the audit `../SOL_FIX27.md` (VERDICT NOT READY), following `../OPUS_BRIEF_27b.md`.
- Work was done only in fix27/. The attempt-1 state is kept, unedited, in fix27_a1_snapshot/.
- b2_run.sh was not run for real. No solver or mpirun was started.
- Signals went only to shims the test started itself. The host's paused processes were only read, through /proc, pgrep and ps.

### Changes
**1. (MAJOR) Reused pid is a new process (b2_run.sh `stopped_postrun`)**
- The fresh PAT1/PAT2 scan used to exclude every pid in the pre-run list. Now it builds a set of `pid:starttime` keys from the pre-run list.
- A live process is skipped only if its current pid **and** start time match a pre-run entry. SELF, the sampler and the session are still excluded by pid.
- A reused pid is therefore both `vanished` (the pre-run process is gone) and `new_running` or `new_stopped` (the new process). A new running one gives contended=yes.
- Test A2 proves this. The attempt-1 helpers, run on the same input, miss it (`new_running=0`): the regression is reproduced.

**2. (MINOR, conservative option) vanished / new_stopped → unknown (b2_isolation.py `evidence`)**
- The three post-run checks are now independent (no more `elif`):
  - resumed + new_running > 0 → yes (reason unchanged).
  - undecided > 0 → unknown.
  - vanished + new_stopped > 0 → unknown, with the reason `foreign stopped job vanished or new foreign job appeared during the run: CPU use not excluded (N vanished, M new stopped)`.
- The "unknown" entries go to the existing `unk` list, so contended stays **yes** when a yes reason exists. The unknown reason is still listed in `contended_reasons`, for information.
- b2_analyse.py treats the new reason as non-Windows, so the layout is INVALID.
- b2_run.sh prints a matching WARNING. `contended_rule` and `stopped_foreign_note` are updated.

**3. (MINOR) Memory evidence**
- **b2_run.sh**, two new helpers in the helper block:
  - `mem_snapshot` records MemTotal, MemAvailable, SwapTotal and SwapFree (/proc/meminfo); pswpin, pswpout and pgmajfault (/proc/vmstat); uptime_s; epoch.
  - It writes `$OUT/memory_prerun.txt` just before launch and `$OUT/memory_postrun.txt` after the sampler has exited. Both are written with or without the override.
  - `dmesg_oom` writes `$OUT/dmesg_oom.txt`. If dmesg is readable, the first line is `readable: ... [t0, t1] s` and is followed by the OOM lines stamped inside the run window. Otherwise the file says `not readable`. The window is the kernel uptime between the two snapshots.
  - OOM lines are those matching `out of memory|oom-kill|oom_reaper|invoked oom-killer|killed process`.
- **b2_isolation.py sampler** (light, inside the existing loop; the CPU measurement and the CSV columns are unchanged):
  - `_stat` also reads majflt (field 12).
  - Each loop rewrites `owned_majflt.txt`: `owned_session_majflt <sum> processes <n>`, where each owned-session process counts with its majflt at its last sample.
  - MemAvailable was already sampled (`memavailable_mb` → `run_memavailable_mb_min`).
- **b2_isolation.py evidence**, new keys:

  | Key | Content |
  |---|---|
  | `stopped_foreign_rss_mb_pre` | total RSS of the pre-run stopped set |
  | `stopped_foreign_population` | sorted `pid:start` keys of the pre-run stopped set |
  | `stopped_foreign_count_post`, `stopped_foreign_rss_mb_post` | post-run entries whose threads are all T/t: still_stopped, new_stopped, and resumed ones stopped again |
  | `mem_memavailable_mb_start`, `mem_memavailable_mb_end` | MemAvailable at start and end |
  | `mem_swap_used_mb_start`, `mem_swap_used_mb_end` | SwapTotal − SwapFree at start and end |
  | `mem_swap_grew` | end > start; `None` if not measured |
  | `mem_pswpin_delta_host`, `mem_pswpout_delta_host`, `mem_pgmajfault_delta_host` | host-wide deltas |
  | `mem_owned_session_majflt` (+ `_note`) | available cheaply, so it is included |
  | `mem_dmesg_oom` | list of lines, or `"not readable"` |
  | `memory_note` | explanation |

  None of these is a validity criterion.
- **b2_analyse.py**:
  - `MEMK` and `memrow()` add these columns to every job row and layout row: stopped foreign RSS pre, count post, RSS post, min MemAvailable, swap start, swap end, swap grew, pswpout delta, owned majflt and dmesg OOM. Lists are joined; `none` means an empty list.
  - The ratio row has two new columns:
    - `stopped_foreign_population_differs`. When the sets differ, the note says `stopped foreign population differs between layouts (L16 a, L8x2 b, c common pid:start)`.
    - `swap_grew_layouts`. When swap grew, the note says `FLAG: swap grew during <layouts>`; if it was not measured, it says `swap growth not measured for ...`.
  - These notes are added to the ratio note in both branches (computed and not computed). The docstring is updated.
- **b2_design.md**: the "Paused foreign jobs (2026-10-01)" paragraph is rewritten.
  - The result is a throughput comparison on a host with about 5.5 GB held by paused foreign jobs, not an empty-host result.
  - It explains pid+start identity, including a reused pid, and the outcome rules (yes / unknown).
  - It lists every memory quantity that is reported, plus the population and swap notes of the ratio row.

### Tests (test_fix27.sh; full output in test_fix27.out)
- `bash -n` passes on b2_run.sh, test_fix27.sh, ../b2_jobs.sh and ../b2_rank.sh.
- `python3 -m py_compile` passes on b2_isolation.py and b2_analyse.py.
- Cases 1–4, A and B are unchanged and pass. The ptrace mixed-thread case ran here (it was not skipped).
- New sections:

| Section | What it checks |
|---|---|
| A2 | A synthetic pre-run file lists a stopped shim S1 with its real start time, and two live shims whose start time is altered by −1 tick: running R2 and stopped Q2. |
| C | `mem_snapshot` has 9 keys. Host dmesg is readable. A fake `dmesg` on PATH checks the window filter (only the in-window OOM line is kept) and the unreadable case. |
| D | The real sampler runs on a setsid shim acting as "mpirun" and writes `owned_majflt.txt`. CSV column count is still 16. |
| E | A clean fabricated result (B2_NRANKS=2 on cores 0/1, Windows pass, low non-owned CPU) gives contended=no. It is then combined with each stopped-foreign outcome. Memory keys are checked, including swap growth (SwapFree −2 MB) and owned majflt. |
| F | b2_analyse.py on a fake B2_ROOT, with PYTHONPATH pointing at b1_settle. |

```
== supplementary A2: reused pid (pre-run pid alive with another start time) -> vanished AND eligible for new_running / new_stopped
still_stopped 1449239 state=T threads=1 cpu_ticks=0 start=25049148 ... simpleFoam 600
vanished 1452709 (pre-run: state=S cpu_ticks=0 start=25049948 ...)
vanished 1452710 (pre-run: state=T cpu_ticks=0 start=25049949 ...)
new_running 1452709 state=S threads=1 cpu_ticks=0 start=25049949 ...
new_stopped 1452710 state=T threads=1 cpu_ticks=0 start=25049950 ...
summary prerun=3 still_stopped=1 resumed=0 vanished=2 undecided=0 new_running=1 new_stopped=33
PASS: pid reuse: R2 vanished + new_running, Q2 vanished + new_stopped; S1 (pid and start match) excluded from the new scan
PASS: regression reproduced: attempt-1 helpers miss the reused running pid R2 (summary ... vanished=2 undecided=0 new_running=0 new_stopped=32)
== supplementary C: memory snapshot and dmesg OOM filter
readable: dmesg lines matching OOM with kernel time in [250501.89, 250501.90] s (first buffered line: [    0.000000] L)
PASS: memory snapshot has the 9 keys; host dmesg readable
readable: dmesg lines matching OOM with kernel time in [1000, 2000] s (first buffered line: [  500.000001] O)
[ 1500.000001] Out of memory: Killed process 99 (simpleFoam) total-vm:1kB
PASS: dmesg: only the OOM line inside the run window is kept
PASS: dmesg unreadable -> 'not readable'
== supplementary D: sampler writes owned_majflt.txt
owned_session_majflt 0 processes 1
PASS: owned_majflt.txt written (1 session process), CSV columns unchanged (16)
== supplementary E: evidence (clean baseline + stopped-foreign outcomes + memory keys)
c0 no False []
c1 no True []
c2 unknown True ['foreign stopped job vanished or new foreign job appeared during the run: CPU use not excluded (1 vanished, 0 new stopped)']
c3 unknown True ['foreign stopped job vanished or new foreign job appeared during the run: CPU use not excluded (0 vanished, 1 new stopped)']
c4 yes True ['foreign stopped job resumed during the run (1 resumed, 0 new running foreign offenders)', 'foreign stopped job vanished or new ... (1 vanished, 0 new stopped)']
c5 yes True ['foreign stopped job resumed during the run (0 resumed, 1 new running foreign offenders)', 'foreign stopped job vanished or new ... (2 vanished, 33 new stopped)']
PASS: evidence: clean -> no; override all still stopped -> no; vanished -> unknown; new_stopped -> unknown; resumed+vanished -> yes; pid reuse (A2) -> yes
c1 stopped_foreign_count 4 / rss_mb_pre 8 / run_memavailable_mb_min 19000.0 / swap 0.0 -> 2.0 grew True / owned majflt 42 / dmesg_oom []
c5 stopped_foreign_count_post 34 expected 34 rss_mb_post 5628
c0 None None None not available (owned_majflt.txt missing) not readable
PASS: memory keys: ...; missing files -> None / 'not readable'
== supplementary F: b2_analyse.py rows and ratio notes
ratio: True | L16 |  ...; stopped foreign population differs between layouts (L16 4, L8x2 3, 1 common pid:start); FLAG: swap grew during L16; swap growth not measured for L8x2
L16 row: {'stopped_foreign_count': '4', 'stopped_foreign_rss_mb_pre': '8', 'mem_swap_grew': 'True', 'mem_owned_session_majflt': '42', 'mem_dmesg_oom': 'none'}
ratio: False |  | not computed: ...; swap growth not measured for L16 and L8x2
PASS: analyse: population differs + swap-grew flag in the ratio row, memory columns on the rows; same population -> no note
== result: 18 passed, 0 failed
```
(In A2 and c5 the `new_stopped=33` includes the host's real paused processes, because the synthetic pre-run list does not contain them. In a real run they are in the pre-run list.) All shims were killed at exit and the temp directory was removed.

### Open points (attempt 2)
1. **The conservative rule has a price.** If the paused Marissa queue spawns a new process during a B2 run, the watcher stops it. That process is `new_stopped`, so contended becomes unknown and the layout INVALID. The operator should make sure no Marissa launcher can start a new job during the run: its queue scripts are themselves stopped in the pre-run set. The first WARNING in the runner output shows it.
2. **Population across layouts.** The analysis compares the pre-run `pid:start` sets. If any process vanished or appeared inside a layout, that layout is already unknown through finding 2. So two layouts that are both "no" have identical stopped populations throughout, unless the pre-run sets differ, and that case is flagged.
3. **`mem_swap_grew`** is strict (end > start, kB resolution) and only a flag. Swap that grows and shrinks within the run is not seen; `mem_pswpout_delta_host` covers that case (any page-out during the run). The minimum MemAvailable is sampled every B2_SAMPLE_S (5 s).
4. **`mem_owned_session_majflt`** counts faults up to each process's last sample. Faults after that sample, and faults of processes shorter than one interval, are missed. The host-wide `mem_pgmajfault_delta_host` is the upper bound.
5. **dmesg** was readable on this host (dmesg_restrict=0; the buffer starts at 0.0 s, so it has not wrapped). If the ring buffer wraps during a run, early lines would be lost; the header line shows the first buffered timestamp.
6. **Not covered by the tests**: the calls of `mem_snapshot`, `dmesg_oom` and `stopped_postrun` in the real end path are only reached after launch, so they were checked by code inspection only. The helpers themselves and the evidence/analysis code are tested.

## Attempt 3

Scope: the findings of audit SOL_FIX27_R2 (NOT READY) and the conditions of AGY_FIX27_R2 (READY WITH CONDITIONS). Files changed: b2_run.sh, b2_isolation.py, b2_analyse.py, b2_design.md and test_fix27.sh. The attempt-2 state is in ../fix27_a2_snapshot/ and was not edited. pause_marissa.sh was not edited. b2_run.sh was not run for real, and no solver or mpirun was started. Signals went only to shim processes the test started itself, and the test killed them all (no leftovers afterwards).

### Changes

**1. (BLOCKER) Host-level CPU accounting: b2_isolation.py sampler and evidence.**

- **What the sampler reads.** At every sample the sampler reads /proc/stat through `_hoststat`:
  - aggregate and per-CPU busy = user + nice + system + irq + softirq + steal. Guest time is already inside user. Idle and iowait are excluded.
  - the `processes` fork counter.
- **Owned CPU (the ledger).** The ledger (`_owned_ledger`) sums utime + stime + cutime + cstime over the owned processes: the umbrella's session, the runner and its descendants, and the sampler. It is keyed by pid+starttime (`_stat` now returns `start`).
- **Owned delta between two samples (`owned_ticks_delta`).**
  - Alive at both samples: its delta.
  - Newly owned: its delta since the previous sample if it existed then; otherwise all of its CPU (it was born in the interval).
  - Gone, with an owned parent: its previous total is subtracted. The parent's cutime/cstime jump holds the child's final total, so the net counted is the child's unseen tail. A child that was born and exited between two samples is therefore counted once, through the parent's cutime.
  - Gone, with a non-owned parent, or alive but no longer owned: nothing is subtracted. Its later CPU counts as non-owned, which is conservative.
- **Non-owned host CPU.** Per interval: `host_nonowned` = max(0, host busy − owned).
- **New file host_cpu_samples.csv.** Columns: host_busy, owned_ledger, the raw host − owned difference, host_nonowned, forks_delta, owned and non-owned new pids seen at samples, and busy cores per CPU. isolation_samples.csv is unchanged (still 16 columns).
- **Evidence.** New fields `run_host_nonowned_cores` {n, mean, max}, `run_host_busy_cores` and `run_host_minus_owned_raw_cores`.
  - **New criterion:** mean ≥ HOST_MEAN_MAX = 0.30 or max ≥ HOST_MAX_MAX = 1.25 core → contended = yes, reason 'host-level non-owned CPU over threshold'.
  - No host samples → unknown.
- **Why separate thresholds.** HOST_* = the per-PID thresholds (LIN_MEAN_MAX 0.25 / LIN_MAX_MAX 1.0) + a fixed allowance HOST_TOL_MEAN 0.05 / HOST_TOL_MAX 0.25. The two measures are not directly comparable:
  - this WSL2 kernel uses tick-sampled /proc/stat (CONFIG_TICK_CPU_ACCOUNTING, HZ 250), while per-process times come from sum_exec_runtime;
  - the host figure also contains irq/softirq, kernel threads and fork/exec cost that no process is charged for.
- **Where the allowance comes from.** There is no quiet baseline in the evidence (no B2 run exists yet). On 2026-10-01 at about 06:55 I ran the sampler for 60 s on the idle host (Marissa jobs stopped; the watcher and the Claude sessions alive). Host-level minus per-PID non-owned was 0.006 to 0.096 core per 5-s sample (mean about 0.045). This is stated in b2_design.md.
- **Unchanged:** the per-PID measures and their thresholds.
- **Fork counter (information only).** `host_forks` records forks_delta_run, owned_new_pids_seen, nonowned_new_pids_seen and forks_minus_owned_seen. The last is an upper bound on non-owned forks, because the runner forks too.
- **Analysis output.** b2_analyse.py job rows now carry `host_nonowned_cores_mean` / `_max`. The new reason is a non-Windows reason, so a layout it hits is INVALID.

**2. (MAJOR) Post-run exclusions are by pid+start (b2_run.sh).**

- New helper `pstart`.
- Start times are recorded while the processes are alive:
  - `SELFK` (runner and ancestors) at the guard;
  - `UK` / `U_START` right after the umbrella is launched;
  - `SPK` right after the sampler is launched.
- `stopped_postrun` skips a live offender only if its pid:start matches one of these tokens.
- Session members are excluded only while pid U is alive with its launch start time. Otherwise sid U could belong to a foreign session whose leader reused pid U.
- The post-run classification now also comes from one `proc_info` snapshot per process (state=gone / ? / letters).

**3. (MAJOR) Admission (b2_run.sh).**

- **Single snapshot.** New `offender_scan` takes ONE `proc_info` read per candidate. A candidate is ignored only if that read succeeded and every thread state in it is T or t. Anything else makes it an offender, named with its snapshot:
  - vanished (`state=gone`);
  - unreadable (`state=?`);
  - any other state.
  The recorded prerun line is the same snapshot that made the decision.
- **Pre-launch recheck.** The whole check runs again immediately before launch: after the Windows precheck, the OpenFOAM environment, host_before.txt and memory_prerun.txt.
  - Any offender refuses: 'pre-launch recheck: host busy'.
  - A changed stopped pid:start set also refuses.
  - A pass is appended to host_before.txt.
  - The recheck runs with and without the override. Without the override it can only add a refusal.
- **New test hook `B2_STOP_BEFORE_LAUNCH=1`:** exit 3 right after the recheck, so the recheck can be tested without launching anything. Do not set it in production.

**4. (MAJOR, documentation) Pause watcher.** *(superseded by 'Fable attempt 1' below: the operator replaced the 10-s watcher by pause_marissa_light.sh at 07:08, the runner now recognises both forms and refuses without coverage)*

- With the override, `pause_watchers` writes to host_before.txt:
  - each live 'pause_marissa.sh --watch' process: its pid, args, elapsed and remaining time, and the end time;
  - a WARNING if it ends before B2_MAX_RUNTIME_S, or if no watcher is alive;
  - the line count of the watcher's log, paused.pids (`B2_PAUSED_PIDS`, default /home/azan/paper6_t6_work/marissa_pause/paused.pids). The file is only read.
- **Beyond the brief:** the post-run check adds `watcher_new=<new lines>` to the summary line of stopped_foreign_postrun.txt and copies the new lines as comments. If watcher_new ≠ 0, contended = unknown, reason 'pause watcher stopped new processes during the run'. This makes "any process the watcher catches during a layout makes it unknown" hold even for processes outside the offender patterns. For offender-pattern processes, new_stopped already did this.
- **b2_design.md** now says:
  - the operator started the watcher with --watch 36000 at about 06:00 on 2026-10-01, so it covers until about 16:00; the default 3600 s would be too short;
  - it must cover both layouts;
  - anything it catches makes that layout unknown;
  - the watcher is itself non-owned load (next point).

**5. (MINOR)** `MEMK` in b2_analyse.py now also exports `mem_pswpin_delta_host` and `mem_pgmajfault_delta_host`.

### Tests (test_fix27.sh; full output in test_fix27.out): 28 passed, 0 failed

Cases 1–4 and A–F from attempts 1–2 still pass. The mixed-thread ptrace case ran; it was not skipped. The clean fabricated result used by E now includes a host_cpu_samples.csv, because without host samples the evidence is 'unknown'. New sections:

| Section | What it checks | Result |
|---|---|---|
| G1 | `offender_scan` extracted from b2_run.sh, with `pgrep` mocked to name: a stopped shim, a running shim, an unused pid (vanished), and a stopped shim whose `proc_states` is forced to fail. | Only the stopped shim is ignored (with its pid:start). The other three are offenders with snapshots `state=S`, `state=gone` and `state=?`. |
| G2a | Real runner with a fake powershell that passes the Windows precheck, plus `B2_STOP_BEFORE_LAUNCH=1`. | rc 3, 'pre-launch offender recheck ...: passed' and the watcher lines are in host_before.txt. |
| G2b | The fake powershell sends SIGCONT to a stopped shim during the precheck. | Refused: 'pre-launch recheck: host busy', with the shim's `state=S` snapshot. |
| G2c | The fake powershell starts and stops a new shim. | Refused: 'the stopped foreign set (pid:start) changed'. |
| H | `stopped_postrun` with running shims whose pids are in SELFK/SPK/UK or the U session. | Matching start → excluded. Start − 1 (a reused pid) → new_running. The session is excluded only while U has its launch start. Regression: the attempt-2 helpers skip these pids whatever their start time. |
| I1 | Synthetic /proc/stat files and a synthetic ledger. | See below. |
| I2 | Real sampler, interval 4 s. | See below. |
| J | b2_analyse.py rows. | pswpin, pswpout and pgmajfault deltas and the host mean/max are present, and equal the evidence values. |
| K | Shim `pause_marissa.sh --watch 50`, plus the real watcher. | Remaining time and the short-watch WARNING are recorded. No watcher alive → WARNING. One new line in paused.pids → watcher_new=1 → contended=unknown with the watcher reason. |

**I1 (synthetic)** checks:
- the busy formula: steal is added; guest, iowait and idle are not;
- the per-CPU and fork counts;
- the ledger cases: child reaped by an owned parent; child born and gone between samples; child reaped outside the run; pid reuse; a process that becomes owned;
- the clamp at 0.

The ledger delta equals the hand-computed truth (175 ticks; host busy 2.0, non-owned 1.65 core).

I2 test setup:
- The owned session is a setsid bash. After sample 2 it runs 3 × 2.5-s busy loops (`timeout`), reaped inside the session.
- After sample 3, a non-owned python parent that ignores SIGCHLD (so its children are auto-reaped and their CPU enters no cutime) forks 3 × 2.5-s busy loops.
- Both bursts start and end between two samples.

I2 output:

```
row 1: host_busy 0.3599 owned_ledger 0.0300 host_nonowned 0.3299 forks 656 | per-PID owned 0.0075 nonowned 0.2124 top pause_marissa.s(1388484) 0.172
row 2: host_busy 1.9320 owned_ledger 1.8795 host_nonowned 0.0525 forks 51 | per-PID owned 0.0000 nonowned 0.0400 top bash(1626371) 0.020
row 3: host_busy 1.9345 owned_ledger 0.0025 host_nonowned 1.9320 forks 42 | per-PID owned 0.0025 nonowned 0.0450 top bash(1626371) 0.022
row 4: host_busy 0.3199 owned_ledger 0.0000 host_nonowned 0.3199 forks 598 | per-PID owned 0.0000 nonowned 0.2174 top pause_marissa.s(1388484) 0.175
evidence: yes {'n': 4, 'mean': 0.6586, 'max': 1.932} {'n': 4, 'mean': 0.1287, 'max': 0.2174} ['host-level non-owned CPU over threshold', 'no in-run Windows snapshot interval', 'bound-CPU occupancy not measured', 'bindings not verified (report and/or observed affinity)']
```

- Row 2: the owned burst enters the ledger through cutime (1.88 core), and host non-owned stays low (0.05).
- Row 3: the per-PID measure misses the foreign burst (0.045). The host-level measure sees it (1.93 core), and the evidence says contended = yes for the host-level reason only.

**Syntax checks:** `bash -n` passes on b2_run.sh, test_fix27.sh, ../b2_jobs.sh and ../b2_rank.sh. `python3 -m py_compile` passes on b2_isolation.py and b2_analyse.py.

**What is not tested:**
- **Behaviour under a real 16-rank load.** Only shims ran. How large the tick-accounting noise is at full load, and so the false-positive rate of HOST_*, is not measured. The allowance is fixed and comes from an idle-host measurement.
- **Real mpirun/orted process trees in the ledger.** Only bash/timeout/python shims were used.
- **The real launch path:** SPK/UK set right after `setsid` / the sampler start, and the moments between the recheck and `setsid`. These were tested only with synthetic tokens. Nothing may be launched here.
- **The per-PID blind spot was built with a parent that ignores SIGCHLD.** With a normal parent that lives across both samples, the per-PID measure already sees the child through that parent's cutime (unchanged design, not re-tested).

### Open points (attempt 3)

1. **Thin margin; a false 'yes' is possible.** *(superseded: the 10-s watcher is gone, the light watcher's cost and the thresholds are set by the calibration of 'Fable attempt 1')* The pause watcher is non-owned load. In a sample that contains one of its 10-s scans it forks about 600 processes and costs about 0.17–0.21 core per-PID and about 0.33 core host-level. On the idle host (watcher plus Claude sessions) the per-PID mean was about 0.13 core against 0.25, and the host-level mean alternated between about 0.05 and about 0.33 core against 0.30. If the coordinator's sessions are busy during a layout, contended may become yes and the layout INVALID. That error is on the conservative side, but it would waste a layout. The coordinator should stay quiet during the runs. I did not change any threshold for this.
2. **Residual race window.** The recheck runs a few milliseconds before `setsid`. A foreign process that resumes after the recheck is still seen by the in-run measures (per-PID and host-level) and by the post-run check.
3. **paused.pids unreadable.** If paused.pids cannot be read before the run, `watcher_new` is not written and no watcher criterion applies. host_before.txt then says 'not readable'.
4. **An aborted recheck leaves results_<layout>/ behind.** A refusal at the recheck, like a refusal at the Windows guard, leaves results_<layout>/ with the prerun files. The next attempt refuses until the operator moves that directory aside.
5. **AGY conditions still hold:**
   - deploy the fix27 files into b2/ (next to b2_jobs.sh and b2_rank.sh; b2_analyse.py finds b1_settle.py two levels up);
   - keep the stopped foreign population the same across both layouts;
   - the watcher must stay alive through both layouts. host_before.txt now records its remaining time. Today it ends at about 15:58.

## Fable attempt 1+2

Scope: the round-3 audits SOL_FIX27_R3 (NOT READY: blocker watcher detection, major unvalidated host-level criterion, minor fork statistic) and AGY_FIX27_R3 (READY WITH CONDITIONS). Files changed in fix27/: b2_run.sh, b2_isolation.py, b2_analyse.py, b2_design.md, test_fix27.sh, this report; new: b2_calibrate.sh, calibration_run.log. The attempt-3 state is in ../fix27_a3_snapshot/ and was not edited. Neither pause_marissa.sh nor pause_marissa_light.sh was edited. b2_run.sh was NOT run on b2/L16/case or b2/L8/*; the only solver run was the calibration allowed by the brief, on a plain COPY of b2/L16/case under /home/azan/paper6_t6_work/b2_calib/ (the original was only read; its files are unchanged). Signals went only to shim processes the test started (all killed by the test). The host's paused processes and its watcher were only read.

### Changes

**1. (SOL R3 BLOCKER) Pause watcher detection and refusal (b2_run.sh `pause_watchers`, new `watcher_guard`).**
- Recognised forms: `pause_marissa_light.sh [SECONDS]` (default 36000; the operator's replacement, a pgrep scan every 30 s) and `pause_marissa.sh --watch [SECONDS]` (default 3600). The script must be argv[0] or argv[1] of the process (`pgrep -af 'pause_marissa(_light)?\.sh'`, then the token check), so a shell whose command line merely mentions the name is not a watcher; such a candidate is recorded as 'candidate ignored (unrecognised form)'. The runner and its ancestors (SELF) are skipped.
- Remaining coverage = SECONDS minus the process's elapsed time (`ps -o etimes=`), because the watcher computes its end as its start + SECONDS. Per live watcher host_before.txt records pid, form, start time, SECONDS, elapsed, remaining, the end time, B2_MAX_RUNTIME_S and the command line; the largest remaining coverage over the live watchers is the coverage used.
- REFUSAL: with B2_ALLOW_STOPPED_FOREIGN=1 the runner exits 1 ('pause watcher guard') right after the offender and load guards, BEFORE the results directory is created, when no recognised watcher is alive or the coverage is shorter than B2_MAX_RUNTIME_S (default 14400 s). The FAIL message carries the watcher record. The same check runs again at the pre-launch recheck (after the Windows precheck and the OpenFOAM environment) and its pass is appended to host_before.txt ('pre-launch pause watcher recheck ...: passed (N alive, S s left >= B2_MAX_RUNTIME_S ...)'). There is no override for this refusal. Without the override nothing changed.
- paused.pids: its line count (PPL0) is taken at the guard and again at the recheck (the later value is the post-run baseline for watcher_new). Unchanged otherwise.
- Verified against the live host watcher (pid 1662291, `pause_marissa_light.sh 43200`, started 07:08:56): recognised, about 42400 s left at 07:22, and the calibration run's host_before.txt records it (see below).
- b2_design.md paragraph (4) and the b2_run.sh header now describe the light watcher, both forms, the coverage computation and the refusal; the attempt-3 sentences about the 10-s watcher's cost are kept as history and marked superseded.

**2. (SOL R3 MAJOR) Calibration of the host-level criterion under the real 16-rank load (new b2_calibrate.sh; hook B2_CALIB_ENDTIME in b2_run.sh; thresholds in b2_isolation.py).**
- b2_calibrate.sh copies b2/L16/case (plain `cp -a`; the original is only read) to /home/azan/paper6_t6_work/b2_calib/<stamp>/L16/case, sets endTime to the budget (default 150 iterations), copies the deployed script set into <stamp>/bin/ (b2_run.sh and b2_isolation.py from fix27/, b2_jobs.sh and b2_rank.sh from b2/; sha256 in calibration_setup.txt) and runs `B2_ROOT=<stamp> B2_CALIB_ENDTIME=150 B2_MAX_RUNTIME_S=3600 bash <stamp>/bin/b2_run.sh L16` with the caller's B2_EXCLUSIVE_OK / B2_ALLOW_STOPPED_FOREIGN / Windows overrides. So the calibration goes through the SAME runner (all guards, the override, the watcher guard, the pre-launch rechecks, the umbrella session, the watchdogs, the post-run checks and the evidence), the SAME launch path (setsid b2_jobs.sh -> mpirun -np 16 --bind-to none b2_rank.sh, 16 ranks pinned one per physical core) and the SAME sampler (5-s samples, Windows snapshot every 60 s).
- Hook: `B2_CALIB_ENDTIME=<n>` makes the endTime guard expect <n> instead of 1600. It is accepted only for layout L16 with a B2_ROOT under /b2_calib/ (else the runner refuses), and it is marked 'CALIBRATION RUN ... NOT a B2 measurement' in host_before.txt and as `calibration_endtime` in run_status.json. On the real cases it cannot be used (their path is not under /b2_calib/). No other guard or logic changed.
- The report calibration.json / calibration.txt: per sample host busy minus owned (host_nonowned_cores, clamped, and the raw difference) as mean, p95 (nearest rank), max and min over all samples and over the loaded samples (owned ledger >= 12 cores), the per-PID non-owned mean/max, the host-minus-per-PID difference, the evidence outcome and the threshold rule's result.
- Threshold rule, stated in b2_design.md BEFORE the run: with m / p95 / M the mean / 95th percentile / max of host_nonowned_cores over all calibration samples, the subtraction is usable if m < 0.25 and p95 < 1.0 core; then HOST_MODE = criterion with HOST_MEAN_MAX = max(0.30, m + 0.25), HOST_MAX_MAX = max(1.25, M + 1.0) (rounded up to 0.01). Otherwise HOST_MODE = informational (contended 'unknown', never 'yes', only above HOST_GROSS_MEAN 1.0 / HOST_GROSS_MAX 4.0 core). b2_isolation.py implements both modes (`HOST_MODE`, the gross thresholds, the mode and the calibration figures in `host_level_rule` / `host_level_mode` of the evidence); the per-PID thresholds are unchanged. The evidence stats now also carry p95.
- Result: see 'Calibration' below.

**3. (SOL R3 MINOR) Fork statistic.** Computing owned forks properly is not cheap (no per-process fork counter; children that start and exit between two samples are never seen), so the statistic is labelled as an upper bound everywhere it appears: the evidence key is now `host_forks.nonowned_forks_upper_bound` (was forks_minus_owned_seen) with a note saying UPPER BOUND and why, b2_analyse.py exports it on every job row as `host_nonowned_forks_upper_bound`, and b2_design.md says so. It is not a validity criterion.

### Attempt 2 (brief FABLE_BRIEF_27b: finish attempt 1)

The attempt-1 session ended while its calibration ran in the background; that run (b2_calib/20261001_073557) was SIGTERMed at 07:38 and is discarded. The coordinator then ran b2_calibrate.sh UNCHANGED in the foreground (07:42-07:51, run 20261001_074246; log calibration_run3.log). In attempt 2 no solver, calibration or b2_run.sh was started, no background process was left behind, and signals went only to the shims the test starts and kills; the host's paused processes and its watcher were only read (pgrep, ps, /proc). Files changed in attempt 2 (fix27/): b2_isolation.py, b2_calibrate.sh, b2_run.sh, b2_design.md, test_fix27.sh, this report. The attempt-1 state is in ../fix27_f1_snapshot/ (not edited).

### Calibration (run 20261001_074246; calibration.json / calibration.txt in /home/azan/paper6_t6_work/b2_calib/20261001_074246/)

- Setup: plain copy of b2/L16/case, endTime 150, the deployed script set in bin/, `B2_ROOT=<stamp> B2_CALIB_ENDTIME=150 B2_MAX_RUNTIME_S=3600 bash bin/b2_run.sh L16` with B2_EXCLUSIVE_OK=1 B2_ALLOW_STOPPED_FOREIGN=1 B2_ALLOW_WINDOWS_LOAD=1. Host state: 31 stopped foreign processes (RSS 5621 MB), the light watcher pid 1662291 (`pause_marissa_light.sh 43200`, recognised by the guard: 41167 s left at the guard, recheck passed), the coordinator's interactive session idle-ish.
- Windows override and why: the first try (run 20261001_074227, 07:42:27, calibration_run2.log) was REFUSED by the Windows pre-check: WindowsTerminal(16428) 0.476 core (> 0.25 per process), sum 0.758 (> 0.5). The run was therefore made with B2_ALLOW_WINDOWS_LOAD=1 (recorded in host_before.txt / run.err / the evidence; the pre-check at the run saw WindowsTerminal 0.54 core, sum 0.55). The calibration measures the Linux-side subtraction error (host busy minus owned ledger), into which Windows-side CPU does not enter (outside the guest's /proc/stat; steal 0 in all 103 samples), and the operator's terminal hosts the coordinator session.
- Run: 150/150 iterations, runner rc 0, controlled end (all_jobs_finished), ClockTime 511 s, 103 host samples at 4.98 s, bindings verified, all 31 stopped foreign processes still stopped afterwards (resumed 0, vanished 0, new 0), watcher_new 0.
- host_nonowned_cores (host busy minus owned ledger, clamped at 0) over ALL 103 samples: mean 0.2256, p95 0.5079, max 0.6139, min 0.066 core; the raw difference is identical (never negative). Over the 102 loaded samples (owned ledger >= 12 cores): mean 0.2264, p95 0.5079, max 0.6139. host busy mean 16.174 core; owned ledger mean 15.949 core.
- Per-PID non-owned (existing criterion, same run): mean 0.1826, p95 0.408, max 0.45 core. Host-level minus per-PID per sample: mean 0.043, p95 0.114, max 0.176, min -0.170 core (the two measures agree to about 0.2 core per sample).
- Per-PID top non-owned processes (max core in a 5-s sample): claude(1218956) 0.322 (the coordinator session), pause_marissa_l(1662291) 0.312 (the light watcher's scan: ps/readlink on the ~50 stopped PIDs), systemd(1) 0.176. The operator replaced the watcher at 07:55 by `pause_marissa_light2.sh 43200` (pid 1842239 in marissa_pause/watcher.pid; two pgrep calls per 30-s scan, PIDs already seen stopped are skipped in memory).
- The calibration run's own evidence: contended = yes with the reasons 'Windows non-WSL CPU over the run over threshold' (run mean 0.665 core over 9 snapshots), 'non-owned work on the bound CPUs / SMT siblings' (bound_cpus_nonowned mean 0.1398 > SIB_MEAN_MAX 0.10; max 0.336) and the recorded Windows override. Neither the per-PID (0.1826 / 0.45) nor the host-level (0.2256 / 0.6139) criterion was tripped. Forks: 4300 host forks over the run, 116 owned new pids seen, nonowned_forks_upper_bound 4184 (informational, upper bound).

### Threshold rule and values

- Rule (stated in b2_design.md before the run; now the function `b2_isolation.calib_rule(mean, p95, max)`, which b2_calibrate.sh calls on the deployed bin/b2_isolation.py so there is a single source): usable if mean < 0.25 and p95 < 1.0 core; then HOST_MODE = criterion, HOST_MEAN_MAX = max(0.30, mean + 0.25), HOST_MAX_MAX = max(1.25, max + 1.0), each rounded UP to 0.01; otherwise informational (gross thresholds 1.0 / 4.0, contended unknown only).
- Applied: 0.2256 < 0.25 and 0.5079 < 1.0 -> USABLE, criterion mode; HOST_MEAN_MAX = max(0.30, ceil(0.4756)) = **0.48 core**; HOST_MAX_MAX = max(1.25, ceil(1.6139)) = **1.62 core**. Set in b2_isolation.py as `CALIB_MEAN, CALIB_P95, CALIB_MAX, CALIB_RUN = 0.2256, 0.5079, 0.6139, "20261001_074246"` and `HOST_MEAN_MAX, HOST_MAX_MAX = 0.48, 1.62`; the module raises at import if these disagree with calib_rule(CALIB_*). Verified with own code: calib_rule applied to host_nonowned_cores_all of calibration.json gives criterion / 0.48 / 1.62, equal to the file's threshold_rule and to the deployed constants (test N6; also run by hand before the edit). The per-PID thresholds (0.25 / 1.0), the sibling thresholds (0.10 / 0.5) and the Windows thresholds are unchanged.
- Caveat (in b2_design.md): the mean is close to its usability bound (0.2256 of 0.25); the host-level criterion resolves foreign loads of about a quarter core and more; the per-PID criterion remains the finer instrument and contended = no needs both.

### Changes in attempt 2

1. **b2_isolation.py**: `calib_rule()` (the rule as code), the calibrated constants above, the import-time consistency check; the evidence's host_level_rule now names the calibration stamp and 0.48 / 1.62. **b2_calibrate.sh**: calls `I.calib_rule` from the deployed bin/ copy instead of its inline copy of the rule and records `deployed_thresholds` (the constants of the deployed module and whether they equal the rule's result) in calibration.json / calibration.txt. Not re-run.
2. **b2_run.sh `pause_watchers`**: third recognised form `pause_marissa_light2.sh [SECONDS]` (default 36000, as in the script's `${1:-36000}`; label 'two pgrep calls every 30 s, seen PIDs skipped'); pgrep pattern `pause_marissa(_light2?)?\.sh`; the 'none alive' message and the FAIL message name all three forms. The light and --watch forms, the argv[0]/argv[1] rule, the coverage computation and the refusal are unchanged. Checked against the host's live watcher (pid 1842239, `pause_marissa_light2.sh 43200`, started 07:52:16, about 42600 s left, ends about 19:52): recognised (test N5, read only). NOTE: without this change the runner would have REFUSED a measurement with B2_ALLOW_STOPPED_FOREIGN=1 on the current host ('none alive'), because the attempt-1 pattern did not match the light2 name.
3. **b2_design.md**: paragraph (4) describes the three watcher forms and the light form's measured cost; 'Host-level calibration' has the result (stamp, numbers, override and why, per-PID top list, rule application, caveat) in place of the placeholder; new closing paragraph 'Expected validity on this host'.
4. **test_fix27.sh**: section N (N1-N7, below); K's expected 'none alive' message updated to the three-form text.

### Expected validity on this host (summary of the b2_design.md paragraph; no threshold loosened)

For L16 all 16 physical cores (cpus 0-31) are bound, so the strict sibling criterion (mean > 0.10 or max > 0.5 core of non-owned CPU on bound CPUs / SMT siblings) counts ANY non-owned work on ANY logical CPU; for L8x2 the two jobs together bind the same 32 CPUs. In the calibration the coordinator session (0.32 core max), the watcher (0.31) and systemd (0.18) gave a bound-CPU non-owned mean of 0.1398 core and tripped it. A layout with that reason is INVALID (b2_analyse.py gives CONDITIONALLY_COMPARABLE only when the sibling flag is false and every reason is Windows-side), and the ratio is NOT CLAIMED. With WindowsTerminal active the Windows pre-check refuses, B2_ALLOW_WINDOWS_LOAD=1 is needed and is itself a Windows-side reason, and the Windows CPU over the run (0.665 core mean here) is another: the best achievable status is then CONDITIONALLY_COMPARABLE, never VALID. The per-PID and the calibrated host-level criteria were not tripped in the calibration and are expected to pass with the same background. So on this host as it is: INVALID whenever the coordinator session or the watcher is active enough for the sibling criterion, at best CONDITIONALLY_COMPARABLE while WindowsTerminal is active; VALID needs the Windows-side background stopped and an idle Linux side.

### What was tested (test_fix27.sh, TMPDIR=/home/azan/paper6_t6_work/audit_tmp, 2026-10-01 08:01:54-08:02:57; full output in test_fix27.out): 47 passed, 0 failed

New in attempt 2 (section N; N1-N4 go through the real runner with a pgrep wrapper hiding the host's watchers, fake powershell, B2_STOP_BEFORE_LAUNCH=1): N1 a `pause_marissa_light2.sh 100000` shim alone is recognised, its start time and coverage are recorded in host_before.txt, guard and pre-launch recheck pass; N2 a light2 shim with 30 s left is REFUSED before the results directory exists; N3 a light2 shim without argument gets the default 36000 s; N4 with no watcher of any form the runner refuses and both messages name the three forms; N5 the host's LIVE watcher (pid 1842239, `pause_marissa_light2.sh 43200`) is recognised by `pause_watchers` with the real pgrep (read only; skipped with a note if no light2 watcher is alive); N6 `calib_rule` on calibration.json reproduces criterion / 0.48 / 1.62 = the file's threshold_rule = the deployed constants, CALIB_* equal the file's figures, the floor 0.30 / 1.25 at zero noise, informational at mean 0.25 or p95 1.0, None for no samples; N7 the evidence at the new thresholds: a sample of 1.61 core gives no host-level reason, 1.62 gives contended = yes, host_level_rule names 0.48 / 1.62 and the stamp. A first run failed N1 only because the test cut the recorded line at 220 characters before matching the (longer) light2 label; the cut was widened to 400 and the suite re-run in full. The existing I2 case (non-owned burst of about 1.9 core between two samples -> 'host-level non-owned CPU over threshold') still passes with HOST_MAX_MAX 1.62.

```
PASS: offender guard passed (rc 1, stopped at the Windows guard)
PASS: pid 1870960 listed in stopped_foreign_prerun.txt
PASS: pid 1870961 listed in stopped_foreign_prerun.txt
PASS: one line per ignored process (32)
PASS: refused, both shims named, no OUT
PASS: refused on running pid 1871819 only
PASS: mixed-thread process 1872508 (main thread t, one thread running) refused as running
PASS: postrun: still_stopped / resumed (running) / resumed (stopped again, CPU grew) / vanished / new_running
PASS: evidence: resumed -> yes with the reason; all still stopped -> no stopped-foreign reason; postrun missing -> unknown
PASS: pid reuse: R2 vanished + new_running, Q2 vanished + new_stopped; S1 (pid and start match) excluded from the new scan
PASS: regression reproduced: attempt-1 helpers miss the reused running pid R2 (summary prerun=3 still_stopped=1 resumed=0 vanished=2 undecided=0 new_running=0 new_stopped=31)
PASS: memory snapshot has the 9 keys; host dmesg readable
PASS: dmesg: only the OOM line inside the run window is kept
PASS: dmesg unreadable -> 'not readable'
PASS: owned_majflt.txt written (1 session process), CSV columns unchanged (16), host_cpu_samples.csv written
PASS: evidence: clean -> no; override all still stopped -> no; vanished -> unknown; new_stopped -> unknown; resumed+vanished -> yes; pid reuse (A2) -> yes
PASS: memory keys: RSS/population pre, count/RSS post, min MemAvailable, swap start/end/grew, owned majflt, dmesg list; missing files -> None / 'not readable'
PASS: analyse: population differs + swap-grew flag in the ratio row, memory columns on the rows; same population -> no note
PASS: single snapshot: stopped -> ignored (pid:start kept); running, vanished (state=gone), unreadable thread states (state=?) -> offenders named with their snapshot
PASS: unchanged host: recheck passed (recorded in host_before.txt), stopped before launch
PASS: shim resumed during the Windows precheck -> refused by the pre-launch recheck
PASS: new stopped foreign process between guard and launch -> refused (set changed)
PASS: own pid+start -> excluded; same pids with another start time (reused) -> new_running; session members excluded only while U has its launch start time
PASS: regression reproduced: attempt-2 helpers skip pids listed in SELF/SP whatever their start time
PASS: host busy (steal in, guest/iowait/idle out), per-CPU, forks; ledger: reaped by owned parent, born+gone between samples, reaped outside, pid reuse, newly owned; clamp at 0
PASS: owned burst -> owned ledger (via cutime), host non-owned low; non-owned burst between samples -> host-level non-owned >= 1.5 core, per-PID blind, evidence contended=yes 'host-level non-owned CPU over threshold'
PASS: analyse rows carry pswpin / pswpout / pgmajfault deltas and the host-level mean/max
PASS: watcher alive/remaining/short-watch warning (both forms), none alive -> warning; paused.pids +1 line -> watcher_new=1 -> contended=unknown
PASS: L1 light form: recognised, start time + remaining coverage recorded in host_before.txt, guard and pre-launch watcher recheck passed
PASS: L2 old form (--watch) alone: recognised and accepted
PASS: L3 no watcher alive + override -> REFUSED before the results directory exists
PASS: L4a watcher with 50 s left < B2_MAX_RUNTIME_S 14400 -> REFUSED (WARNING names the watcher)
PASS: L4b the same watcher with B2_MAX_RUNTIME_S=20 -> accepted
PASS: L4c watcher dies during the Windows precheck -> REFUSED by the pre-launch watcher recheck (the guard had passed)
PASS: L5 light form without argument -> the script's default 36000 s; a command line that only mentions the name is not a watcher
PASS: L6 only the name-mentioning shell left -> refused, listed as 'candidate ignored (unrecognised form)'
PASS: L7 B2_CALIB_ENDTIME outside /b2_calib/ -> refused
PASS: L8 calibration copy under /b2_calib/ with endTime 150 -> accepted and marked CALIBRATION in host_before.txt
PASS: L9 the same copy without B2_CALIB_ENDTIME -> refused (endTime is not 1600)
PASS: p95 in the evidence stats; host_forks.nonowned_forks_upper_bound labelled UPPER BOUND (also an analyse column); informational mode: 1.93 core -> no host reason, 4.5 core -> unknown (gross), criterion mode -> yes
PASS: N1 light2 form alone: recognised, start time + remaining coverage recorded, guard and pre-launch recheck passed
PASS: N2 light2 form with 30 s left < B2_MAX_RUNTIME_S -> REFUSED before the results directory exists (the coverage rule applies to the new form)
PASS: N3 light2 form without argument -> the script's default 36000 s
PASS: N4 no watcher of any of the three forms -> REFUSED; the messages name all three forms
PASS: N5 the host's live watcher (pid 1842239: pause_marissa_light2.sh 43200) is recognised with its start time and remaining coverage >= 14400 s (read only)
PASS: N6 calib_rule on calibration.json 20261001_074246 -> criterion 0.48 / 1.62 = the file's threshold_rule = the deployed HOST_* constants (CALIB_* = the file's figures); floor 0.30 / 1.25 at zero noise; mean >= 0.25 or p95 >= 1.0 -> informational
PASS: N7 evidence at the calibrated thresholds: a sample of 1.61 core gives no host-level reason, 1.62 core gives contended=yes; host_level_rule names 0.48 / 1.62 and the calibration stamp
== result: 47 passed, 0 failed
```

Syntax: `bash -n b2_run.sh b2_calibrate.sh test_fix27.sh` ok; `python3 -m py_compile b2_isolation.py b2_analyse.py` ok (also the import-time consistency check of b2_isolation.py passes).

### Open points (attempt 2)

- The calibration was made with the light watcher (0.31 core max per sample); the light2 watcher's cost is not calibrated separately. It does strictly less work per scan, and both non-owned criteria measure it in every run, so the thresholds are not loosened for it.
- The host-level mean threshold 0.48 follows from a calibration mean (0.2256) close to the usability bound; a second calibration on a quieter host (idle coordinator session, light2 watcher) would likely give a lower mean and a tighter threshold. Not done (no solver run allowed in this attempt).
- The expected outcome on this host (see above) is INVALID or at best CONDITIONALLY_COMPARABLE unless the coordinator session is idle and the Windows-side background is stopped. This is a property of the strict rules, which were deliberately not loosened.

