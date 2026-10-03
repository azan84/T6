I have launched `test_job.sh` and will wait for it to complete.
I have launched `test_pool.py` and will wait for it to complete.
# Targeted Pre-Run Audit Round 4: Task B Tooling & S25B Re-Run Verification

**Audit Scope**: Targeted verification of the OpenFOAM environment sourcing fix in Task B tooling following the runtime failure on lane2 (2026-10-03 15:24), diff comparison against `taskB_a2_snapshot/u3d_job.sh`, review of [`taskB/FIX31_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/FIX31_REPORT.md) (Attempt 3), test suite execution, and fresh-case safety check for [`u3d/case_S25B`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S25B).

---

## 1. Executive Summary & Verification Matrix

| Component / Check | Prior State / Failure Mode | Round 4 Audit Finding & Verification | Status |
| :--- | :--- | :--- | :--- |
| **`set -u` crash on OpenFOAM `etc/bashrc`** | Died at line 177: `WM_PROJECT_SITE: unbound variable` | Sourcing wrapped in `set +eu +o pipefail` with direct `fo=$-` and `fp=$(shopt -po pipefail)` capture and restoration. Verified with real OpenFOAM v2406. | **RESOLVED** |
| **Argument leak into OpenFOAM `etc/bashrc`** | Bare `source` passed positional parameters `S25B 8` into `config.sh/setup` (exported as `FOAM_SETTINGS`) | `set --` explicitly clears positional parameters before sourcing. `$L` and `$NP` already captured. Verified `FOAM_SETTINGS=unset`. | **RESOLVED** |
| **Post-source PATH sanity checks** | No check that required tools became available | Explicit loop checks `decomposePar`, `simpleFoam`, `reconstructPar`, and `mpirun` one-by-one via `command -v`. | **RESOLVED** |
| **Dry-run hook (`U3D_DRYRUN_STOP`)** | None | Activated strictly when `[ -n "${U3D_DRYRUN_STOP:-}" ]`. Runs environment source and fresh-case gate, sets `finished=1`, and exits 0 before `decomposePar`. | **RESOLVED** |
| **Code integrity across Task B** | N/A | Only [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh), [`tests/test_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_job.sh), [`tests/test_real_env.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh), and report modified. `pool.py`, `u3d_verdict.py`, `jet_offset.py` match Round 3 hashes bit-for-bit. | **VERIFIED** |
| **`case_S25B` freshness & safety** | Potential contamination from failed 15:24 attempt | Failed attempt died at line 22 prior to `cd "$C"`. Case directory untouched (timestamps `11:11`). No time dirs, no processor dirs, no logs. Passes fresh-case gate cleanly. | **VERIFIED** |
| **Test Suites Execution** | Test coverage of real environment | `test_job.sh` (21/21 PASS), `test_verdict.py` (57/57 PASS), `test_pool.py` (26/26 PASS), `test_real_env.sh` (Task B core checks 6/6 PASS). | **PASS (with note)** |

---

## 2. Detailed Evaluation of the Fix in `u3d_job.sh`

### A. Diff Analysis ([`taskB_a2_snapshot/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB_a2_snapshot/u3d_job.sh) vs [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh))
The unified diff shows only the targeted fix:
```diff
--- taskB_a2_snapshot/u3d_job.sh
+++ taskB/u3d_job.sh
@@ -8,3 +8,3 @@
-# Overrides (tests only): U3D_ROOT, U3D_FOAM_BASHRC, U3D_JET_OFFSET, U3D_VERDICT, U3D_LOCK_WAIT_S.
+# Overrides (tests only): U3D_ROOT, U3D_FOAM_BASHRC, U3D_JET_OFFSET, U3D_VERDICT, U3D_LOCK_WAIT_S, U3D_DRYRUN_STOP (non-empty: stop with rc 0 before decomposePar).
 set -u
@@ -22,2 +22,8 @@
-source "${U3D_FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}" || fail "cannot source the OpenFOAM bashrc"
+set -- ; fo=$-; fp=$(shopt -po pipefail); set +eu +o pipefail; source "${U3D_FOAM_BASHRC:-/usr/lib/openfoam/openfoam2406/etc/bashrc}"; rc=$?; eval "$fp"; [[ $fo == *e* ]] && set -e; [[ $fo == *u* ]] && set -u
+[ $rc -eq 0 ] || fail "cannot source the OpenFOAM bashrc (rc=$rc)"
+for t in decomposePar simpleFoam reconstructPar mpirun; do command -v $t > /dev/null || fail "$t not on PATH after sourcing the OpenFOAM bashrc"; done
+[ -n "${U3D_DRYRUN_STOP:-}" ] && { st "dry run: environment sourced (WM_PROJECT_VERSION=${WM_PROJECT_VERSION:-unset}), fresh-case gate next"; }
@@ -33,0 +40,2 @@
+[ -n "${U3D_DRYRUN_STOP:-}" ] && { finished=1; st "dry run: stop before decomposePar"; exit 0; }
```

### B. Verification of Shell Option Handling & Argument Isolation
1. **Positional Arguments Isolation**: `set --` clears `$@` immediately before sourcing. Because `$L` and `$NP` were assigned at line 10 (`L=${1:-}; NP=${2:-8};`), positional parameters are no longer needed. OpenFOAM's `etc/config.sh/setup` evaluates `$@` and exports arguments as `FOAM_SETTINGS`; clearing them prevents parameter leak into OpenFOAM's config system.
2. **Options Suspension & Restoration**:
   - `fo=$-` reads options directly from the current shell (bypassing subshell commands where `set -e` would be cleared).
   - `fp=$(shopt -po pipefail)` saves pipefail state.
   - `set +eu +o pipefail` suspends `-e`, `-u`, and `pipefail` while sourcing OpenFOAM's `/usr/lib/openfoam/openfoam2406/etc/bashrc`.
   - `eval "$fp"` restores pipefail.
   - `[[ $fo == *e* ]] && set -e; [[ $fo == *u* ]] && set -u` restores `-e` and `-u` based on the original state.
3. **PATH Checks**: All tools invoked by [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh) (`decomposePar`, `simpleFoam`, `reconstructPar`, `mpirun`) are validated one-by-one with `command -v`.
4. **Dry-Run Hook**: `U3D_DRYRUN_STOP` allows executing the environment source and the fresh-case gate, setting `finished=1` to satisfy the exit trap, and exiting 0 before any write or solver execution. When unset, the script executes normally.
5. **No Unintended Changes**: Checksums of all other Task B files are identical to Round 3:
   - `pool.py`: `fc5c64ed2e5b03ff34ae058e1dc6f7d8db11493ddf81320b4a39532c12369f14`
   - `u3d_verdict.py`: `05fa52cb8dae7872ba012b0151712186225d5d43dc6e3874f78a83dbd9c54e1b`
   - `jet_offset.py`: `b5d411b35d1da1191c971c4c1c7dcabd84c124563d64101218ac279a3c45eb1a`

---

## 3. Test Suites Audit

All four suites were run under `nice -n 10` without running solvers:
1. [`tests/test_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_job.sh): **21 PASS, 0 FAIL (`ALL PASS`)**. Section 7 validates that the attempt-2 snapshot fails under nounset on the fake bashrc, whereas the fixed script succeeds under nounset, isolates arguments, and halts on missing PATH tools.
2. [`tests/test_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_verdict.py): **57 PASS, 0 FAIL (`ALL PASS`)**. All settling and classification tests pass.
3. [`tests/test_pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_pool.py): **26 PASS, 0 FAIL (`ALL PASS`)**.
4. [`tests/test_real_env.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh):
   - **Task B checks (Lines 1–45)**: **6 PASS, 0 FAIL**.
     - Real OpenFOAM v2406 sourced in clean environment (`rc 0`, all 5 tools found, `WM_PROJECT_VERSION=v2406`, `FOAM_SETTINGS=unset`).
     - Options correctly restored (`$- ehuBc`, `pipefail on`).
     - Control attempt-2 fails with `line 177: WM_PROJECT_DIR: unbound variable` (or `WM_PROJECT_SITE` in inherited env).
     - Dry runs under clean and inherited environments both pass the fresh-case gate and stop before `decomposePar` without modifying the case.
   - **External check on Task J (Lines 47–54)**: Failed with rc 2 due to an external test dependency (see Finding 2).

---

## 4. Safety Audit of the Re-Run Case (`u3d/case_S25B`)

The failed attempt on `lane2` died at line 22 of `u3d_job.sh` (`source ...`) before executing line 23 (`cd "$C"`):
1. **Case Directory State**: Directory [`u3d/case_S25B`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S25B) contains only `0/`, `constant/`, `system/`, `build_info.json`, `case.foam`, and `zerod_reference.json`. All timestamps remain `2026-10-03 11:11`.
2. **Fresh-Case Gate Compliance**:
   - `controlDict` `endTime` (4000) matches `build_info.json` `endTime` (4000).
   - No time directories `[1-9]*`, no `processor*`, no `postProcessing`, and no `log.*` files exist.
   - Directory `0` exists.
   - **Conclusion**: The case is 100% clean and passes the fresh-case gate without requiring any file deletions in `u3d/case_S25B`.

---

## 5. Numbered Findings

### Finding 1: Stale Failure Artifacts in Pool and Status Files Must Be Cleared Before Re-queue
- **Severity**: **MODERATE / OPERATIONAL**
- **Component**: Deployment & Queue Management (`lane2/jobs/` and `u3d_check/`)
- **Description**:
  1. In [`lane2/jobs/`](file:///home/azan/paper6_t6_work/lane2/jobs/), `u3d_S25B.status` contains `failed rc=1`, alongside stale `.admit`, `.pid`, `.rc`, and `.log` files. Because `pool.py` checks `status(n) is not None`, it will never re-launch `u3d_S25B` while its status file is present. Dependent job `u3d_S12A` remains blocked.
  2. The installed script [`lane2/u3d_job.sh`](file:///home/azan/paper6_t6_work/lane2/u3d_job.sh) is still the unpatched Attempt 2 version.
  3. In [`u3d_check/run_S25B.status`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/run_S25B.status), the 2-line failure header from 15:24 remains recorded.
- **Required Action**:
  - Copy updated [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh) to `lane2/u3d_job.sh`.
  - In `lane2/jobs/`, remove or archive `u3d_S25B.status`, `u3d_S25B.rc`, `u3d_S25B.pid`, `u3d_S25B.admit`, and `u3d_S25B.log` (keeping `u3d_S25B.json` and `u3d_S25B.audited`).
  - Clear or move aside [`u3d_check/run_S25B.status`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/run_S25B.status) for a clean run log.

### Finding 2: Brittle External Regex in `test_real_env.sh` Causes False Test Suite Failure
- **Severity**: **LOW**
- **Component**: Test Harness ([`taskB/tests/test_real_env.sh:48`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_real_env.sh#L48))
- **Description**:
  - `test_real_env.sh` line 48 hardcoded a regex `grep -E '^\[ -n "\$\{CASE_JOB_SKIP_FOAM_ENV:-\}" \] \|\| source ' $TJ` to extract the source line from [`taskJ/case_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskJ/case_job.sh).
  - When Task 41 subsequently updated `taskJ/case_job.sh` to fix its own source block, this regex stopped matching (`TLINE=""`). The subsequent command `bash -c "${TOPTS:-:}; $TLINE; $CHECK"` evaluated to `:; ; rc=...`, causing a bash syntax error (`syntax error near unexpected token ';'`) and an exit code 2.
  - This is an artifact of cross-task coupling in the test script; Task B's production code and its own 6 environment checks are completely sound.
- **Recommendation**: In `test_real_env.sh`, make the Task J check resilient by checking `[ -n "$TLINE" ]` before executing.

### Finding 3: `fp=$(shopt -po pipefail)` Lacks `|| :` Guard Under `set -e` with Pipefail Disabled
- **Severity**: **LOW**
- **Component**: Shell Option Restoration ([`taskB/u3d_job.sh:25`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh#L25))
- **Description**:
  - In bash, `shopt -po <opt>` returns exit status 1 if `<opt>` is currently disabled.
  - If `u3d_job.sh` were invoked with `set -e` while `pipefail` is OFF, the command substitution `fp=$(shopt -po pipefail)` would return status 1 during variable assignment, terminating the shell immediately before reaching `set +eu`.
  - In [`taskJ/case_job.sh:80`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskJ/case_job.sh#L80), this was avoided using `fp=$(shopt -po pipefail || :)`.
  - For `u3d_job.sh`, the script starts with `set -u` (not `set -e`) and is invoked as `nice -n 10 bash .../u3d_job.sh <L> 8`, so `set -e` is not active at line 25 in production. The script functions correctly under production invocation.
- **Recommendation**: Adding `|| :` to `fp=$(shopt -po pipefail || :)` is good defensive practice if the file is edited in the future.

---

VERDICT: READY WITH CONDITIONS
