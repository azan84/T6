# Targeted Pre-Run Audit Round 5: Task B Tooling & S25B Re-Run Verification

**Audit Scope**: Targeted verification of the OpenFOAM environment sourcing fix in Task B tooling following Round 4 audit findings ([`audit_B/SOL_R4.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/SOL_R4.md), [`audit_B/AGY_R4.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/AGY_R4.md)) and Fable 5.1 / Attempt 4 ([`taskB/FIX31_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/FIX31_REPORT.md)). Verification includes diff analysis against Attempt 2 snapshot, rigor and negative control analysis of the 8-combination shell options test with the real OpenFOAM v2406 `bashrc`, isolation of the Task B suite from `taskJ/`, execution of all four test suites, lane2 installation confirmation, and freshness verification of [`u3d/case_S25B`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S25B).

---

## 1. Executive Summary & Verification Matrix

| Component / Requirement | Target / Prior State | Round 5 Audit Verification | Status |
| :--- | :--- | :--- | :--- |
| **`taskB/u3d_job.sh` Diff vs Snapshot** | Must touch only the environment block and dry-run hook | Diff against [`taskB_a2_snapshot/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB_a2_snapshot/u3d_job.sh) modifies only documentation header, lines 22–30 (environment sourcing, `set --`, `shopt -po pipefail \|\| :`, tool PATH checks, dry-run log), and line 41 (dry-run exit). | **VERIFIED** |
| **Pipefail Corner Case Fix** | `fp=$(shopt -po pipefail)` returned rc 1 when pipefail was off, aborting `set -e` shells | Sourcing block updated to `fp=$(shopt -po pipefail \|\| :)`. Option evaluation, command substitution status, and restoration verified under all shell option states. | **RESOLVED** |
| **8-Combination Shell Option Test** | Must rigorously test `-e`/`-u`/`pipefail` combinations with real OpenFOAM `bashrc` | [`taskB/tests/test_real_env.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh) runs all $2^3 = 8$ option permutations in `env -i`. Confirms option snapshot identity before/after, tool discovery, and includes negative control against Attempt 3. | **VERIFIED SOUND** |
| **Task B / Task J Decoupling** | Task B test suite previously failed due to regex drift against `taskJ/case_job.sh` | Task J dependency completely removed from [`taskB/tests/test_real_env.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh). No executable references to `taskJ/` remain in Task B. | **VERIFIED** |
| **Test Suites Execution** | Run all 4 suites once in foreground (`nice -n 10`) | `test_real_env.sh` (8/8 PASS), `test_job.sh` (24/24 PASS), `test_verdict.py` (57/57 PASS), `test_pool.py` (26/26 PASS). Total: 115/115 PASS, 0 FAIL. | **PASS** |
| **Installed Code on `lane2`** | [`lane2/u3d_job.sh`](file:///home/azan/paper6_t6_work/lane2/u3d_job.sh) | Still matches failing snapshot `aed3f7a...`. Must be updated to [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh) (`5e39d22...`). `u3d_verdict.py` and `jet_offset.py` are already up to date. | **CONFIRMED** |
| **`u3d/case_S25B` Freshness** | Check for contamination from prior failed attempt | Pristine state (timestamps `11:11`). No time dirs $>0$, no `processor*`, no `postProcessing`, no logs. `controlDict` `endTime` matches `build_info.json` (4000). Passes fresh-case gate cleanly. | **VERIFIED** |

---

## 2. Detailed Technical Verifications

### A. SHA256 Checksums and File Identity
- [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh): `5e39d22c78afccd6f25f1e7830a521ef66bf599589f3038e8e7e11d0025841d8` (Attempt 4)
- [`taskB_a2_snapshot/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB_a2_snapshot/u3d_job.sh): `aed3f7a75bb81302c24957b0d991c634b1dec744c6bba4daf7e69ceb08ef1bda` (Attempt 2)
- [`/home/azan/paper6_t6_work/lane2/u3d_job.sh`](file:///home/azan/paper6_t6_work/lane2/u3d_job.sh): `aed3f7a75bb81302c24957b0d991c634b1dec744c6bba4daf7e69ceb08ef1bda` (**old failing version**)
- [`taskB/u3d_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py): `05fa52cb8dae7872ba012b0151712186225d5d43dc6e3874f78a83dbd9c54e1b` (Identical to `lane2/u3d_verdict.py`)
- [`taskB/jet_offset.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jet_offset.py): `b5d411b35d1da1191c971c4c1c7dcabd84c124563d64101218ac279a3c45eb1a` (Identical to `lane2/jet_offset.py`)
- [`taskB/pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py): `fc5c64ed2e5b03ff34ae058e1dc6f7d8db11493ddf81320b4a39532c12369f14` (Identical to `lane2/pool.py`)

### B. Unified Diff Analysis
Comparing [`taskB_a2_snapshot/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB_a2_snapshot/u3d_job.sh) vs [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh):
```diff
--- taskB_a2_snapshot/u3d_job.sh
+++ taskB/u3d_job.sh
@@ -8,3 +8,3 @@
-# Overrides (tests only): U3D_ROOT, U3D_FOAM_BASHRC, U3D_JET_OFFSET, U3D_VERDICT, U3D_LOCK_WAIT_S.
+# Overrides (tests only): U3D_ROOT, U3D_FOAM_BASHRC, U3D_JET_OFFSET, U3D_VERDICT, U3D_LOCK_WAIT_S, U3D_DRYRUN_STOP (non-empty: stop with rc 0 before decomposePar).
 set -u
@@ -22,2 +22,9 @@
-source "${U3D_FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}" || fail "cannot source the OpenFOAM bashrc"
+# The OpenFOAM v2406 bashrc reads unset variables (line 177: WM_PROJECT_SITE): under `set -u` that kills the shell (failure of 2026-10-03 15:24),
+# and it also has commands returning non-zero (fatal under set -e), so -e/-u/pipefail are suspended ONLY around the source and restored right after
+# ($- read directly: a $(set +o) snapshot runs in a subshell, where bash clears errexit; `|| :` on the pipefail snapshot: `shopt -po` returns 1 when pipefail is off,
+# which would kill a `set -e` shell before the options are suspended). `set --` first: a bare source passes the job's "$@" (S25B 8) to the bashrc as settings/files.
+set -- ; fo=$-; fp=$(shopt -po pipefail || :); set +eu +o pipefail; source "${U3D_FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}"; rc=$?; eval "$fp"; [[ $fo == *e* ]] && set -e; [[ $fo == *u* ]] && set -u
+[ $rc -eq 0 ] || fail "cannot source the OpenFOAM bashrc (rc=$rc)"
+for t in decomposePar simpleFoam reconstructPar mpirun; do command -v $t > /dev/null || fail "$t not on PATH after sourcing the OpenFOAM bashrc"; done
+[ -n "${U3D_DRYRUN_STOP:-}" ] && { st "dry run: environment sourced (WM_PROJECT_VERSION=${WM_PROJECT_VERSION:-unset}), fresh-case gate next"; }
@@ -33,0 +41,2 @@
+[ -n "${U3D_DRYRUN_STOP:-}" ] && { finished=1; st "dry run: stop before decomposePar"; exit 0; }
```
The diff is strictly confined to:
1. Documenting `U3D_DRYRUN_STOP` in the header.
2. Isolating positional arguments (`set --`), safely recording shell options (`fo=$-; fp=$(shopt -po pipefail || :)`), suspending `-e`/`-u`/`pipefail`, sourcing `/usr/lib/openfoam/openfoam2406/etc/bashrc`, checking the return code, restoring pipefail and `-e`/`-u`, checking required binary presence (`command -v`), and logging the dry-run state.
3. Exiting cleanly (`finished=1; exit 0`) before `decomposePar` when `U3D_DRYRUN_STOP` is set.

### C. Soundness Analysis of the All-Combinations Environment Test
Section 4 of [`taskB/tests/test_real_env.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh#L47-L77) was reviewed for structural correctness and robustness:
1. **Permutation Matrix**: Evaluates all combinations of `-e`/`+e`, `-u`/`+u`, and `-o pipefail`/`+o pipefail` inside clean subshells (`clean bash -c ...` using `env -i`).
2. **Vacuous Match Protection**: The test parses the `before` state and explicitly asserts that the options active in the subshell match the exact test permutation before proceeding.
3. **Restoration Verification**: Captures `SNAP='"$-|$(shopt -po pipefail || :)"'` both before and after the sourcing block and requires exact character identity (`[ "$before" = "$after" ]`).
4. **Environment Quality**: Asserts that all 5 required tools (`simpleFoam`, `decomposePar`, `reconstructPar`, `mpirun`, `foamDictionary`) exist on PATH, `WM_PROJECT_VERSION=v2406`, and `FOAM_SETTINGS=unset`.
5. **Negative Control Verification**: Synthesizes the Attempt 3 line (removing `|| :` from `fp=$(shopt -po pipefail)`) and validates that it fails in exactly the 2 combinations where `-e` is active and `pipefail` is disabled (`shell-rc-1`), while passing the remaining 6 combinations.

### D. Decoupling from `taskJ/`
Inspection of the codebase confirms:
- [`taskB/tests/test_real_env.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh) lines 8 and 78 note the intentional removal of the former Task J check.
- `grep -rn "taskJ" taskB/` finds only historical comments and past attempt documentation in `taskB/FIX31_REPORT.md` and test log output files.
- The test suite execution is 100% self-contained within `taskB/` and its control snapshot.

---

## 3. Test Suites Execution Results

All four test suites were executed sequentially with `nice -n 10` and `PYTHONDONTWRITEBYTECODE=1`:

1. [`taskB/tests/test_real_env.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh):
   - **8/8 PASS, 0 FAIL** (`ALL PASS`, rc 0)
   - Real OpenFOAM v2406 sourced successfully in clean and inherited environments.
   - All 8 option combinations passed; Attempt 3 negative control failed in exactly the 2 expected `-e` + `+o pipefail` cases.
2. [`taskB/tests/test_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_job.sh):
   - **24/24 PASS, 0 FAIL** (`ALL PASS`, rc 0)
   - Validated fresh-case gate, Scotch subdomain handling, mock solver/reconstruction fault injection, lock serialization on CSV, and dry-run bypass.
3. [`taskB/tests/test_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_verdict.py):
   - **57/57 PASS, 0 FAIL** (`ALL PASS`, rc 0)
   - Pre-registered classification rules (a, b, c, d), FFR settling filters, NaN checks, and verification against real S50 and S25A benchmark outputs passed.
4. [`taskB/tests/test_pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_pool.py):
   - **26/26 PASS, 0 FAIL** (`ALL PASS`, rc 0)
   - Process group tracking, PID reuse handling, RAM/rank limits, and crash recovery verified under mock workloads.

---

## 4. Numbered Findings

### Finding 1: Candidate Job Script Must Be Installed to `lane2/` Before Queue Re-Admission
- **Severity**: **HIGH / OPERATIONAL PRE-CONDITION**
- **Component**: Deployment ([`/home/azan/paper6_t6_work/lane2/u3d_job.sh`](file:///home/azan/paper6_t6_work/lane2/u3d_job.sh) and [`lane2/jobs/`](file:///home/azan/paper6_t6_work/lane2/jobs/))
- **Description**:
  1. The installed script [`/home/azan/paper6_t6_work/lane2/u3d_job.sh`](file:///home/azan/paper6_t6_work/lane2/u3d_job.sh) has SHA256 `aed3f7a75bb81302c24957b0d991c634b1dec744c6bba4daf7e69ceb08ef1bda`, which is the old failing Attempt 2 version.
  2. [`lane2/jobs/u3d_S25B.status`](file:///home/azan/paper6_t6_work/lane2/jobs/u3d_S25B.status) currently records `failed rc=1` (with stale `.admit`, `.pid`, `.rc`, and `.log` from the 15:24 failure). Because `pool.py` checks `status(n) is not None`, it will not admit `u3d_S25B` while a terminal status file exists. Dependent job `u3d_S12A` remains blocked.
  3. [`u3d_check/run_S25B.status`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/run_S25B.status) retains the failure header from the Attempt 2 run.
- **Required Action**:
  - Copy [`/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh) (`5e39d22...`) to [`/home/azan/paper6_t6_work/lane2/u3d_job.sh`](file:///home/azan/paper6_t6_work/lane2/u3d_job.sh). Note: `lane2/u3d_verdict.py` and `lane2/jet_offset.py` already match the Task B source hashes bit-for-bit and do not require modification.
  - In `lane2/jobs/`, remove or archive `u3d_S25B.status`, `u3d_S25B.rc`, `u3d_S25B.pid`, `u3d_S25B.admit`, and `u3d_S25B.log` (preserving `u3d_S25B.json` and `u3d_S25B.audited`).
  - Clear or move aside [`u3d_check/run_S25B.status`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/run_S25B.status).

### Finding 2: Re-Run Case `u3d/case_S25B` Verified Clean and Gate-Compliant
- **Severity**: **INFO / PASS**
- **Component**: Target Case Directory ([`u3d/case_S25B`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S25B))
- **Description**:
  - The failed Attempt 2 run halted at line 22 prior to executing `cd "$C"`.
  - All files in [`u3d/case_S25B`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S25B) retain their initial `11:11` timestamps (`0/`, `constant/`, `system/`, `build_info.json`, `case.foam`, `zerod_reference.json`).
  - No time directories $>0$, no `processor*`, no `postProcessing`, and no solver logs exist.
  - `controlDict` `endTime` (4000) matches `build_info.json` `endTime` (4000).
  - Executing the script's fresh-case gate logic directly confirms `stale=[]` and exit 0. No cleanup within `u3d/case_S25B` is needed.

### Finding 3: Sourcing Block Pipefail Corner Case Fully Resolved
- **Severity**: **INFO / PASS**
- **Component**: Shell Option Restoration ([`taskB/u3d_job.sh:25`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh#L25))
- **Description**:
  - The use of `fp=$(shopt -po pipefail || :)` prevents premature termination when `pipefail` is disabled under `set -e`.
  - Rigorously confirmed across all 8 permutations with the production OpenFOAM v2406 environment.

### Finding 4: Test Suite Drift and Cross-Task Dependency Completely Removed
- **Severity**: **INFO / PASS**
- **Component**: Test Harness ([`taskB/tests/test_real_env.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh))
- **Description**:
  - Removal of the fragile regex check against `taskJ/case_job.sh` successfully isolates Task B's test harness.
  - All 4 test suites pass sequentially without warnings, errors, or residual background processes.

---

VERDICT: READY WITH CONDITIONS
