# Pre-Run Audit: Fix 28 Evaluation

**Targets under review**:
- [`fix28/b2_driver.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/b2_driver.sh)
- [`fix28/b2_driver2.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/b2_driver2.sh)
- [`fix28/test_fix27.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix27.sh)
- Compared against originals in [`b2/b2_driver.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_driver.sh), [`b2/b2_driver2.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_driver2.sh), and [`fix27/test_fix27.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix27/test_fix27.sh).
- Brief: [`OPUS_BRIEF_28.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/OPUS_BRIEF_28.md).
- Coordinator test outputs: [`test_fix28_run1.out`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix28_run1.out) (busy host), [`/home/azan/paper6_t6_work/t28_idle.out`](file:///home/azan/paper6_t6_work/t28_idle.out) (idle host).

**Protocol Compliance**: Audit-only inspection. No files modified. `b2_run.sh` and driver scripts were not executed for real. No solvers, MPI, or background processes were signaled. Verification conducted via static diffs, regex inspection, `bash -n`, and analysis of coordinator execution transcripts.

---

## 1. Analysis of Coordinator Test Run Failures

In [`/home/azan/paper6_t6_work/t28_idle.out`](file:///home/azan/paper6_t6_work/t28_idle.out), 45 tests passed and 2 failed (N1 and N5). 

**Judgment: Neither failure is a production code defect.**
The hypothesis that N1 and N5 failed due to reading a non-existent `paused.pids` is **incorrect**. In [`b2_run.sh:105, 119`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_run.sh#L105), `pause_watchers` gracefully handles missing/unreadable `paused.pids` (`PPL0=""; WATCH_REPORT+="pause log $PAUSED: not readable"`), and `host_before.txt` records `paused.pids unreadable lines` without failing the guard or pre-launch rechecks. Both failures are strictly test-harness defects:

1. **Test N1 Failure Analysis ([`fix28/test_fix27.sh:383-384`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix27.sh#L383-L384))**:
   - *Observation*: [`t28_idle.out:248-249`](file:///home/azan/paper6_t6_work/t28_idle.out#L248-L249) shows:
     `started 2026-10-02 20:45:36 for 100000 s, running 0 s, about 100000 s left`
     `pre-launch pause watcher recheck 20:45:37: passed (1 alive, 100000 s left >= B2_MAX_RUNTIME_S 14400 s; paused.pids unreadable lines)`
   - *Cause*: Lines 383 and 384 assert regex `about 9[0-9]* s left` and `1 alive, 9[0-9]* s left`, assuming elapsed time $e \ge 1$. When `lrun` executes in the same second the watcher was spawned ($e = 0$), remaining coverage is exactly `100000 s`. The string `100000` does not match `9[0-9]*`. Production code ([`b2_run.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_run.sh)) functioned properly. This is the exact same elapsed-zero timing flaw that was previously identified and patched for N3.

2. **Test N5 Failure Analysis ([`fix28/test_fix27.sh:399-404`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix27.sh#L399-L404))**:
   - *Observation*: [`t28_idle.out:262-264`](file:///home/azan/paper6_t6_work/t28_idle.out#L262-L264) shows live watcher PID `2429236` was running `pause_marissa_light2.sh 50000` (`for 50000 s`).
   - *Cause*: Line 402 hardcodes `for 43200 s` and `cmdline: /bin/bash ... pause_marissa_light2.sh 43200`. The entry condition at line 400 (`[[ "$HC" == *pause_marissa_light2.sh* ]]`) evaluated to true, but the assertion failed because `50000 s` did not match the hardcoded `43200 s`. Production code ([`b2_run.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_run.sh)) recognized the watcher and computed coverage correctly.

3. **Busy Host Test Run (19/46 passed)**:
   - In [`test_fix28_run1.out:4-21`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix28_run1.out#L4-L21), the runner's offender guard encountered 19 foreign solver processes (`simpleFoam`, `mpirun -np 8`) and correctly refused admission:
     `FAIL: host busy (B2_ALLOW_STOPPED_FOREIGN=1: 2 stopped foreign processes ignored); solver/mesher processes: ...`
   - This behavior is entirely expected: tests that assert clean admission must be run on an idle host.

---

## 2. Assessment of Driver Fixes

In [`fix28/b2_driver.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/b2_driver.sh) and [`fix28/b2_driver2.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/b2_driver2.sh):
1. **Exit Code Logging**:
   - `bash ./b2_run.sh L16 > ...; rc=$?; echo "... rc=$rc" >> driver.log`
   - In the previous version, `echo "... rc=$?"` executed `$(date)` during parameter expansion before evaluating `$?`, clobbering `$?` with `date`'s return code (always 0). Capturing `rc=$?` immediately after command execution guarantees that the actual exit status of `b2_run.sh` and `b2_analyse.py` is logged.
2. **Bounded Inter-Layout Load Wait**:
   - Replaced fixed `sleep 120` ([`b2_driver.sh:8-10`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/b2_driver.sh#L8-L10)) and unbounded polling ([`b2_driver2.sh:6-8`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/b2_driver2.sh#L6-L8)) with:
     ```bash
     w=0; until awk '{exit !($1 < 0.5)}' /proc/loadavg; do
       if [ $w -ge 1800 ]; then echo "$(date '+%F %T') STOP: 1-min load $(cut -d' ' -f1 /proc/loadavg) still >= 0.5 after 1800 s; ... not started" >> driver.log; exit 4; fi
       sleep 15; w=$((w+15)); done
     ```
   - Logic is robust: if 1-minute load drops below 0.5, awk exits 0 and the loop terminates. If load remains $\ge 0.5$ for 1800 seconds (30 minutes), the driver logs a timeout refusal and cleanly halts with exit code 4 before launching subsequent stages.
3. Syntax check passed (`bash -n`).

---

## 3. Assessment of Test Suite Changes

The changes in [`fix28/test_fix27.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix27.sh) **do not weaken coverage**:
1. **Test N7 Rewrite ([`fix28/test_fix27.sh:418-433`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix27.sh#L418-L433))**:
   - Previously mutated test I2's live 4-sample CSV, causing background noise fluctuations to push the mean $\ge 0.48$ on a 1.61-core peak.
   - Now builds an isolated synthetic CSV ($n=100$, 99 samples at 0.05 core, 1 sample at 1.61 or 1.62). The resulting mean is ~0.066 ($< 0.48$), perfectly isolating the `HOST_MAX_MAX = 1.62` boundary check.
   - Retains all validations: `ctl` confirms $n=100$, mean $< 0.1$, exact max value; verifies `I.HOST_MODE == "criterion"`, `not h1` (1.61 core passes), `h2 == ["host-level non-owned CPU over threshold"]` (1.62 core fails), `e2["contended"] == "yes"`, and threshold rules matching calibration `20261001_074246`.
2. **Test N3 Tolerance ([`fix28/test_fix27.sh:393`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix27.sh#L393))**:
   - Updated regex `about \(359[0-9][0-9]\|36000\) s left` accommodates elapsed time $e = 0$ while strictly constraining elapsed times $1 \le e \le 99$ to `35900..35999`.
3. **Deployment Targeting**:
   - `S=$(cd "$HERE/.." && pwd)` targets the deployed production scripts in [`b2/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/), respects `TMPDIR`, and sets `PYTHONDONTWRITEBYTECODE=1`.

---

## 4. Numbered Findings

1. **MINOR (Test Harness Flaw) — Test N1 flakily fails when sampled at elapsed time zero ($e = 0$).**  
   [`fix28/test_fix27.sh:383-384`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix27.sh#L383-L384)  
   Assertions `about 9[0-9]* s left` and `passed (1 alive, 9[0-9]* s left ...)` assume elapsed time $e \ge 1$. At $e = 0$, remaining coverage is `100000 s`, which fails the regex. The assertion should accept `(9[0-9]*|100000)` similarly to N3. Production runner code is unaffected.

2. **MINOR (Test Harness Brittleness) — Test N5 hardcodes historical watcher duration `43200 s`.**  
   [`fix28/test_fix27.sh:402`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/test_fix27.sh#L402)  
   Test N5 asserts that the live host watcher was launched for `43200 s`. When the host watcher is restarted with another duration (e.g. `50000 s`), `[[ "$HC" == *pause_marissa_light2.sh* ]]` enters the test branch but the regex fails. The test should match `for [0-9]* s` and `cmdline: .* [0-9]*`. Production code correctly detects and verifies coverage.

3. **MINOR (Missing Artifact) — `fix28/FIX28_REPORT.md` was not generated.**  
   [`OPUS_BRIEF_28.md:5`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/OPUS_BRIEF_28.md#L5)  
   The brief requested `fix28/FIX28_REPORT.md` documenting changes and test runs. The file is absent in `fix28/`, though run evidence is preserved in [`t28_idle.out`](file:///home/azan/paper6_t6_work/t28_idle.out).

4. **MINOR (Operational Condition) — Deployment from `fix28/` to production directory `b2/` is required.**  
   [`b2/b2_driver.sh:7-13`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_driver.sh#L7-L13), [`b2/b2_driver2.sh:6-12`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/b2_driver2.sh#L6-L12)  
   The patched driver scripts [`b2_driver.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/b2_driver.sh) and [`b2_driver2.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b2/fix28/b2_driver2.sh) currently reside in `fix28/` and differ from the active files in `b2/`. They must be copied into `b2/` prior to execution.

---

VERDICT: READY WITH CONDITIONS
