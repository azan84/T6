# Pre-Run Audit Round 4 (Final Evaluation after Fable 5.1 Attempts 1–2)

**Targets under review**:
- [`fix27/b2_run.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh)
- [`fix27/b2_isolation.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py)
- [`fix27/b2_analyse.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py)
- [`fix27/b2_calibrate.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_calibrate.sh)
- [`fix27/b2_design.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_design.md)
- [`fix27/test_fix27.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/test_fix27.sh)
- [`fix27/FIX27_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/FIX27_REPORT.md) (sections *Fable attempt 1+2*)
- Compared against [`fix27_a3_snapshot/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27_a3_snapshot/) and baseline [`b2/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/).
- Briefs: [`FABLE_BRIEF_27.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/FABLE_BRIEF_27.md), [`FABLE_BRIEF_27b.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/FABLE_BRIEF_27b.md).
- Prior audits: [`SOL_FIX27_R3.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/SOL_FIX27_R3.md), [`AGY_FIX27_R3.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/AGY_FIX27_R3.md).
- Calibration run: [`/home/azan/paper6_t6_work/b2_calib/20261001_074246/`](file:///home/azan/paper6_t6_work/b2_calib/20261001_074246/) (`calibration.json`, `calibration.txt`, `results_L16/`).

**Protocol Compliance**: Audit-only inspection. No files modified. `b2_run.sh` and `b2_calibrate.sh` were not executed against real cases. No solvers or `mpirun` instances were started. No external signals sent. `test_fix27.sh` was not executed. Verification conducted via static code inspection, diff analysis, `bash -n`, and `python3 -m py_compile`.

---

## 1. Resolution of Round-3 Findings

1. **Round-3 Finding 1 (SOL R3: BLOCKER — Watcher detection and coverage guard): RESOLVED**
   - In [`fix27/b2_run.sh:98-115`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L98-L115), `pause_watchers()` recognizes all three active/historical watcher forms: `pause_marissa_light2.sh [SECONDS]` (default 36000 s), `pause_marissa_light.sh [SECONDS]` (default 36000 s), and `pause_marissa.sh --watch [SECONDS]` (default 3600 s). It confirms the script is `argv[0]` or `argv[1]` of the candidate process and reads elapsed time `etimes` via `ps` to calculate remaining coverage `left = n - e`.
   - In [`fix27/b2_run.sh:116-121, 171, 200`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L116-L121), `watcher_guard` enforces that when `B2_ALLOW_STOPPED_FOREIGN=1`, execution unconditionally aborts (`fail`) before the results directory is created (and again at the pre-launch recheck) if no recognized watcher is alive or if the remaining coverage is less than `B2_MAX_RUNTIME_S` (14400 s).
   - On the live host, watcher PID `1842239` (`/bin/bash /home/azan/paper6_t6_work/marissa_pause/pause_marissa_light2.sh 43200`, started at 07:52:16) is active with >41,500 s of remaining coverage, successfully satisfying the guard.
   - [`fix27/b2_design.md:19`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_design.md#L19) and [`fix27/FIX27_REPORT.md:389-395`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/FIX27_REPORT.md#L389-L395) accurately describe all three watcher forms and their operational semantics.

2. **Round-3 Finding 2 (SOL R3: MAJOR — Host-level CPU criterion validation & calibration): RESOLVED**
   - [`fix27/b2_calibrate.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_calibrate.sh) was implemented and run by the coordinator on a copy of `b2/L16/case` with a 150-iteration budget, executing through the identical launch path (`setsid b2_jobs.sh` -> `mpirun -np 16 --bind-to none b2_rank.sh`) and identical sampler (`b2_isolation.py`).
   - The threshold rule was explicitly pre-formulated in [`fix27/b2_design.md:20`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_design.md#L20) and coded in [`fix27/b2_isolation.py:22-32`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L22-L32) (`calib_rule`): if `mean < 0.25` and `p95 < 1.0`, subtraction is usable in `criterion` mode with `HOST_MEAN_MAX = max(0.30, ceil_0.01(mean + 0.25))` and `HOST_MAX_MAX = max(1.25, ceil_0.01(max + 1.0))`.
   - The calibration run [`20261001_074246`](file:///home/azan/paper6_t6_work/b2_calib/20261001_074246/calibration.json) (103 samples, 150 steps, controlled end) measured `mean = 0.2256`, `p95 = 0.5079`, and `max = 0.6139`.
   - Applying the pre-stated rule yielded `HOST_MEAN_MAX = 0.48` and `HOST_MAX_MAX = 1.62`. These constants are set in [`fix27/b2_isolation.py:38`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L38) and guarded by an import-time assertion (`RuntimeError` on mismatch, [`b2_isolation.py:40-41`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L40-L41)). Per-PID thresholds (`0.25 / 1.0`) were not loosened.

3. **Round-3 Finding 3 (SOL R3: MINOR — Forks statistic upper bound): RESOLVED**
   - In [`fix27/b2_isolation.py:336-340`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L336-L340), the key was renamed from `forks_minus_owned_seen` to `nonowned_forks_upper_bound`, and its documentation note was explicitly marked `"informational, UPPER BOUND"`.
   - In [`fix27/b2_analyse.py:15, 96`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L15), the field is exported to all layout rows as `host_nonowned_forks_upper_bound`.

---

## 2. Assessment of Coordinator Test Run (N7 Failure Analysis)

During the coordinator test run of `test_fix27.sh`, 46 tests passed and 1 test failed (N7).
- **The Observation**: In test N7 ([`fix27/test_fix27.sh:417-426`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/test_fix27.sh#L417-L426)), synthetic sample rows were injected with max values of `1.61` and `1.62`. When evaluating `run(1.61)`, the coordinator saw the 4-sample mean equal `0.5062`. Because `0.5062 >= HOST_MEAN_MAX (0.48)`, `b2_isolation.py` flagged `"host-level non-owned CPU over threshold"`. Because `h1` was not empty, the test assertion `not h1` failed (`N7BAD`).
- **Judgment**: **N7 is strictly a test-data / test-harness defect; it does NOT expose any code defect.**
  - *Code correctness*: In [`fix27/b2_isolation.py:414-415`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L414-L415), the criterion specifies:
    ```python
    elif HOST_MODE == "criterion":
        if ev["run_host_nonowned_cores"]["mean"] >= HOST_MEAN_MAX or ev["run_host_nonowned_cores"]["max"] >= HOST_MAX_MAX:
            yes.append("host-level non-owned CPU over threshold")
    ```
    If any run has a mean of `0.5062`, it violates the `HOST_MEAN_MAX = 0.48` threshold. Flagging `"host-level non-owned CPU over threshold"` is strictly correct and faithful to design specifications.
  - *Test-data defect*: Test N7 attempted to test the boundary condition of `HOST_MAX_MAX = 1.62` (i.e. verifying that `1.61 < 1.62` does not trip the max threshold). However, instead of constructing a controlled synthetic CSV with zeroed non-offender samples or a sufficiently large sample count $n$, N7 mutated `$T/i2/host_cpu_samples.csv`—a dataset captured live during test I2 with only $n=4$ samples. In an $n=4$ dataset, placing `1.61` in one sample contributes `1.61 / 4 = 0.4025` core directly to the mean, leaving only `0.48 - 0.4025 = 0.0775` cores across all remaining 3 samples (an average of only 0.0258 core per sample). When background noise during test I2 averaged ~0.138 cores on the coordinator's host, the mean mathematically reached `0.5062`. This is a classic test-data coupling defect where the test failed to isolate the variable under test. In production runs ($n \ge 100$), a single 1.61-core peak contributes $<0.016$ core to the mean.

---

## 3. Numbered Findings

1. **MINOR (Test Harness Flaw) — Test N7 in `test_fix27.sh` flakily trips the mean threshold due to test-data coupling with live test I2.**  
   [`fix27/test_fix27.sh:417-426`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/test_fix27.sh#L417-L426)  
   Test N7 mutates the 4-sample live CSV generated in test I2 rather than generating a synthetic dataset with zeroed baseline noise or an adequate sample count. As a result, live host noise fluctuations cause the mean to exceed `HOST_MEAN_MAX = 0.48` when testing a 1.61-core max peak, causing test failure under normal host background levels. This does not impact production execution.

2. **MINOR (Operational Condition) — Deployment to production directory `b2/` required before execution.**  
   [`fix27/b2_run.sh:18`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L18), [`fix27/b2_analyse.py:20`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L20)  
   The audited and verified fixes currently reside in `fix27/`. Before launching the production run, `b2_run.sh`, `b2_isolation.py`, `b2_analyse.py`, and `b2_design.md` must be copied into `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/`.

3. **MINOR (Operational Condition) — Host quiescence requirement to avoid `INVALID` label.**  
   [`fix27/b2_isolation.py:42`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L42), [`fix27/b2_design.md:21`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_design.md#L21)  
   As documented in *Expected validity on this host*, the planned production run (`B2_EXCLUSIVE_OK=1 B2_ALLOW_STOPPED_FOREIGN=1 B2_ALLOW_WINDOWS_LOAD=1`):
   - Will receive Windows-side contention reasons due to WindowsTerminal (~0.5 core), limiting the best achievable result to `CONDITIONALLY_COMPARABLE`.
   - Binds all 16 physical cores (all 32 logical CPUs) for L16 and L8x2. Any non-owned Linux work (active coordinator CLI commands, external scripts) will be attributed to bound CPUs. If `bound_cpus_nonowned` exceeds `SIB_MEAN_MAX = 0.10` mean (as happened in the calibration run where it reached 0.1398 core due to claude + systemd + watcher), the run will be labeled `INVALID` and the ratio `NOT CLAIMED`. Complete quiescence of interactive sessions is required during execution.

4. **MINOR (Operational Condition) — Foreign stopped process population stability.**  
   [`fix27/b2_run.sh:76-85`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_run.sh#L76-L85), [`fix27/b2_isolation.py:403-408`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_isolation.py#L403-L408), [`fix27/b2_analyse.py:121-122`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/b2_analyse.py#L121-L122)  
   The 51 foreign processes in `/home/azan/paper6_t6_work/marissa_pause/paused.pids` must remain stopped across both layouts. Any resumed process, vanished PID, newly spawned foreign job, or growth in `paused.pids` (`watcher_new > 0`) will mark the layout `INVALID`. The `pid:start` set must remain identical between L16 and L8x2.

---

VERDICT: READY WITH CONDITIONS
