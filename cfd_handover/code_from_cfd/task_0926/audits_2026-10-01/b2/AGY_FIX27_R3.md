# Pre-Run Audit Round 3: Fix 27 Attempt 3 (Final Opus Attempt)

**Target under review**: [`fix27/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/) ([`b2_run.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh), [`b2_isolation.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py), [`b2_analyse.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py), [`b2_design.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_design.md), [`test_fix27.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/test_fix27.sh), [`FIX27_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/FIX27_REPORT.md) section 'Attempt 3') versus Attempt 2 ([`fix27_a2_snapshot/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27_a2_snapshot/)) and audited originals in [`b2/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/).  
**Briefs & Prior Audits**: [`OPUS_BRIEF_27.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/OPUS_BRIEF_27.md), [`OPUS_BRIEF_27b.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/OPUS_BRIEF_27b.md), [`OPUS_BRIEF_27c.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/OPUS_BRIEF_27c.md); Round 2 audits [`SOL_FIX27_R2.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/SOL_FIX27_R2.md) and [`AGY_FIX27_R2.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/AGY_FIX27_R2.md).  
**Protocol Compliance**: Audit-only. No files modified. `b2_run.sh` was not executed against real cases (`b2/L16`, `b2/L8`). No solvers or `mpirun` started. No external signals sent. `test_fix27.sh` was not executed. Verification was performed via static inspection, diff analysis, `bash -n`, and `python3 -m py_compile`.

---

### 1. Resolution of Round-2 Findings

1. **Round-2 Finding 1 (SOL R2: BLOCKER — Short-lived running foreign offender unrecorded): RESOLVED**
   - In [`fix27/b2_isolation.py:128-135`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L128-L135), `_hoststat()` reads aggregate and per-CPU busy jiffies (`user + nice + system + irq + softirq + steal`, excluding `idle` and `iowait`) from `/proc/stat` and the `processes` fork counter at every sample.
   - In [`fix27/b2_isolation.py:137-151`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L137-L151), an owned process ledger tracks `utime + stime + cutime + cstime` keyed by `(pid, starttime)`. In `owned_ticks_delta()`, when an owned child exits and is reaped, its cumulative CPU is transferred into the parent's `cutime + cstime`, and the child's previous total is subtracted so its unseen execution tail is counted exactly once. Children born and exited entirely between samples are captured through the parent's `cutime + cstime`.
   - In [`fix27/b2_isolation.py:239-242, 305-320, 384`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L239-L242), host-level non-owned CPU is recorded per sample in `host_cpu_samples.csv` (`max(0, host_busy - owned)`). In `evidence()`, `run_host_nonowned_cores` is evaluated against `HOST_MEAN_MAX = 0.30` and `HOST_MAX_MAX = 1.25`. Any exceeded threshold sets `contended = yes` (`host-level non-owned CPU over threshold`), which invalidates the layout in [`b2_analyse.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L52-L56).

2. **Round-2 Finding 2 (SOL R2: MAJOR — Post-run exclusions PID-only): RESOLVED**
   - In [`fix27/b2_run.sh:142, 178, 182`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L142), start times are captured while processes are known to be alive: `SELFK` at pre-run, `UK` (`$U:$U_START`) and `SPK` (`$SP:$SP_START`) immediately upon launch.
   - In [`fix27/b2_run.sh:62-68`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L62-L68), `stopped_postrun()` excludes processes only when both PID and start time match (`[[ "$ex" == *" $pid:${s#start=} "* ]]`). Reused PIDs with different start times are not excluded and are classified as `new_running` or `new_stopped`. Furthermore, session PIDs are queried only if the umbrella PID `U` is still alive with its launch start time.

3. **Round-2 Finding 3 (SOL R2: MAJOR — Admission snapshot & pre-launch recheck): RESOLVED**
   - In [`fix27/b2_run.sh:37-50`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L37-L50), `offender_scan()` takes a single `proc_info` snapshot per candidate. A process is ignored only if `rc == 0` and every thread state in that single read is `T` or `t`. Any unreadable (`state=?`), vanished (`state=gone`), or active state leaves the process in `OFF1`/`OFF2` and halts the runner.
   - In [`fix27/b2_run.sh:169-174`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L169-L174), immediately before launch (after Windows precheck and OpenFOAM environment setup), `offender_scan` is re-executed. If any running offender appears (`OFF1`/`OFF2` non-empty) or the stopped foreign population changes (`$FIRSTK != $NOWK`), execution immediately terminates (`fail "pre-launch recheck: ..."`).

4. **Round-2 Finding 4 (SOL R2: MAJOR — Pause watcher duration): RESOLVED**
   - In [`fix27/b2_design.md:18-19`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_design.md#L18-L19), the design explicitly documents that the watcher must cover both layouts and that the default 3600 s is insufficient.
   - The operator launched `/home/azan/paper6_t6_work/marissa_pause/pause_marissa_light.sh 43200` (12 hours, running until ~19:08), providing ample coverage for both sequential layouts.
   - In [`fix27/b2_run.sh:72, 101`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L72) and [`fix27/b2_isolation.py:377`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L377), any growth in `paused.pids` is detected via `watcher_new` and marks `contended = unknown`. *(See Finding 1 below regarding runner process detection).*

5. **Round-2 Finding 5 (SOL R2: MINOR — Memory export keys): RESOLVED**
   - In [`fix27/b2_analyse.py:26-27`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L26-L27), `MEMK` now includes `mem_pswpin_delta_host` and `mem_pgmajfault_delta_host`, and `memrow(ev)` correctly exports them to all analysis rows.

---

### 2. Soundness of Host-Level CPU Thresholds (0.30 mean / 1.25 max cores)

1. **Allowance and Idle Calibration**:
   - The allowance (`HOST_TOL_MEAN = 0.05`, `HOST_TOL_MAX = 0.25`) was calibrated from an idle-host 60-s measurement where host busy minus per-PID non-owned CPU averaged ~0.045 cores. This accounts for WSL2 tick-accounting discrepancy (`CONFIG_TICK_CPU_ACCOUNTING`), kernel threads, interrupt handling, and runner fork/exec overhead.
2. **Watchdog Load Reduction**:
   - The original `pause_marissa.sh` generated 0.17–0.33 cores of host load due to walking `/proc` every 10 s, which created a tight margin against 0.30.
   - The replacement watcher [`pause_marissa_light.sh`](file:///home/azan/paper6_t6_work/marissa_pause/pause_marissa_light.sh) runs every 30 s using two lightweight `pgrep` calls. Measured live on the host, PID 1662291 has consumed `00:00:00` CPU time across >3 minutes (<0.001 core).
3. **Solver Workload Accounting**:
   - During the 16-rank run, the 16 `simpleFoam` ranks are children of the umbrella session `U` and their `utime + stime` are fully tracked in `_owned_ledger`. Reaped subprocesses of the runner loop are absorbed into the runner's `cutime + cstime`.
   - Because `writeInterval` is 100000 (no field writes), disk I/O and interrupt overhead are minimal.
   - On an idle host with the light watcher and quiescent coordinator, expected non-owned host CPU is ~0.05–0.08 cores mean. This leaves >0.20 cores (>3x) of safety headroom below `HOST_MEAN_MAX = 0.30`. Peak 5-s samples will remain well below `HOST_MAX_MAX = 1.25`.
   - **Conclusion**: The host-level criterion is sound and will **not** trigger a near-certain false positive during a real 16-rank run, provided the coordinator remains idle.

---

### 3. Numbered Findings

1. **MINOR (Operational Discrepancy) — Informational pause watcher detection in `b2_run.sh` does not match `pause_marissa_light.sh`.**  
   [`fix27/b2_run.sh:96-100`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L96-L100)  
   `pause_watchers()` looks for processes matching `pgrep -af 'pause_marissa\.sh --watch'` and parses `--watch <seconds>`. The light watcher deployed at 07:08 is invoked as `/bin/bash /home/azan/paper6_t6_work/marissa_pause/pause_marissa_light.sh 43200`. As a result:  
   - `b2_run.sh` emits a false warning to stderr: `WARNING: no pause watcher alive (new foreign jobs are not stopped during the run)`.  
   - `host_before.txt` records `pause watcher: no 'pause_marissa.sh --watch' process alive`.  
   - The remaining runtime calculation for the watcher is omitted from `host_before.txt`.  
   *Assessment*: This check is purely informational. `b2_run.sh` does not exit or fail on this condition. Furthermore, line 101 unconditionally records the baseline line count `PPL0` from [`paused.pids`](file:///home/azan/paper6_t6_work/marissa_pause/paused.pids), and [`stopped_postrun()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L72) and [`b2_isolation.py:377`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L377) remain fully functional to invalidate the run (`watcher_new > 0 -> contended=unknown`) if any process is paused.

2. **MINOR (Operational Condition) — Deployment directory for production run.**  
   [`fix27/b2_run.sh:18`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L18), [`fix27/b2_analyse.py:20`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L20)  
   The candidate files reside in `fix27/`. `b2_run.sh` calls `$HERE/b2_jobs.sh` (located in `b2/`), and `b2_analyse.py` resolves `b1_settle.py` relative to two levels above its directory.  
   *Condition*: The files in `fix27/` must be deployed (copied) into `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/` before production execution.

3. **MINOR (Operational Condition) — Foreign queue quiescence and stopped process stability.**  
   [`fix27/b2_isolation.py:374-377`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L374-L377), [`fix27/b2_analyse.py:120-121`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L120-L121)  
   Under the strict isolation model:  
   - Any process caught by `pause_marissa_light.sh` appends to `paused.pids` (`watcher_new > 0`), which marks the layout `contended = unknown` (`INVALID`).  
   - Any foreign process that vanishes or resumes marks the layout `INVALID`.  
   - Any difference in the pre-run stopped `pid:start` set between L16 and L8x2 is flagged in analysis.  
   *Condition*: Foreign job launchers, queue scripts, and cron loops must remain paused, and the stopped process set on the host must not be altered between or during the layout runs.

4. **MINOR (Operational Condition) — Coordinator quiescence during execution.**  
   [`fix27/b2_isolation.py:16-17`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L16-L17)  
   The host-level threshold (`0.30` mean core) accommodates background daemon noise and WSL2 tick accounting, but active interactive agent sessions or external tools could exceed the allowance.  
   *Condition*: The coordinator and operator sessions must remain idle while the layouts run.

---

VERDICT: READY WITH CONDITIONS
