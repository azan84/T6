# Post-Fix Audit Round 3: Task B3 Branch-Aware Smoke Test (`fix26`, Attempt 3)

**Audit Target:** [`fix26/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/)  
**Baseline Snapshot:** [`fix26_a2_snapshot/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26_a2_snapshot/)  
**Context Documents:** [`SOL_FIX26_R2.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/SOL_FIX26_R2.md), [`AGY_FIX26_R2.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/AGY_FIX26_R2.md), [`OPUS_BRIEF_26c.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/OPUS_BRIEF_26c.md), and [`FIX26_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/FIX26_REPORT.md) section 'Attempt 3'.

---

## 1. Prescribed Audit Executions

All three mandatory commands were executed in the target environment:

### A. Unit Test Suite Execution
```bash
TMPDIR=/home/azan/paper6_t6_work/audit_tmp python3 fix26/smoke_test/test_compare_smoke.py
```
```text
test_between_branches_fail (__main__.T) ... ok
test_deflected_pass (__main__.T) ... ok
test_incomplete_run_3 (__main__.T) ... ok
test_other_cell_count_3 (__main__.T) ... ok
test_overlapping_q_windows_ffr_separates_pass (__main__.T) ... ok
test_q_in_window_ffr_out_fail (__main__.T) ... ok
test_real_smoke_ref_symmetric (__main__.T) ... ok
test_reference_cannot_redefine_branch (__main__.T) ... ok
test_reference_common_fields_validated (__main__.T) ... ok
test_schema1_reference_clear_error (__main__.T) ... ok
test_shell_preflight_reference_governance (__main__.T) ... ok
test_shipped_reference_consistent (__main__.T) ... ok
test_symmetric_pass (__main__.T) ... ok
test_two_branches_both_in_window_ambiguous_fail (__main__.T) ... ok
test_unstable_window_fail (__main__.T) ... ok
test_write_reference_new_file (__main__.T) ... ok
test_write_reference_refuses_off_branch_and_unstable (__main__.T) ... ok
test_write_reference_replacement (__main__.T) ... ok

----------------------------------------------------------------------
Ran 18 tests in 4.223s

OK
```
**Exit Code:** `0`. All 18 tests passed. Zero stray files or directories remained on disk or in `/home/azan/paper6_t6_work/audit_tmp`.

### B. Real Reference Run Comparison
```bash
python3 fix26/smoke_test/compare_smoke.py /home/azan/paper6_t6_work/smoke_ref fix26/smoke_test/reference_result.json
```
```text
{
 "iterations": 3000,
 "finished": true,
 "solver_clock_s": 290,
 "Q_out_m3s": 1.17825059e-06,
 "p_measurement_kinematic": 8.85754493,
 "FFR_x56p5": 0.7824829798699555,
 "p_outlet_patch_kinematic": 8.38179515,
 "Q_band_last200_pct": 1.1882022459569742e-05,
 "FFR_band_last200": 2.7385661294232477e-08,
 "cells": 198252,
 "stl_sha256": "47178798e1052ddb7d23d8b318a934baaf42d93d5555b9568eddcabdf9ef8ef2",
 "checkMesh_ok": true,
 "inlet_rewrites": 1,
 "outlet_rewrites": 1,
 "omp_num_threads": "8"
}
  vs deflected branch (1.17392231e-06 m3/s, FFR 0.78396): Q +0.36870 %, FFR -0.001477
  vs symmetric branch (1.17825059e-06 m3/s, FFR 0.78248): Q +0.00000 %, FFR +0.000000
vs the returned Stage A A5 coarse value 1.17392231e-06: +0.36870 %   cells 198252 (reference 198252)   final-window bands: Q 1.19e-05 %, FFR 2.74e-08   wall None s
SMOKE TEST PASS (symmetric-jet branch; not the returned value, see SETUP.md section 4)
```
**Exit Code:** `0`. Symmetic branch identified cleanly with full stability checks verified.

### C. Shell Syntax Check
```bash
bash -n fix26/smoke_test/run_smoke_test.sh
```
**Exit Code:** `0`. Zero syntax errors.

---

## 2. Round-2 Findings Resolution Matrix

| Finding from Round 2 | Severity | Status in Attempt 3 | Location | Details & Verification |
| :--- | :--- | :--- | :--- | :--- |
| **AGY R2-1: Unclosed Parenthesis in Root `README.md` Line 22 Replacement Text** | MINOR | **RESOLVED** | [`fix26/README_line22_replacement.txt:1`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/README_line22_replacement.txt#L1) | The trailing clause in item (12) now terminates with `always kept)). (13)`. All parentheses, brackets, and braces in items (12)–(15) are strictly balanced (depth = 0, no underflow). Byte-level prefix before (12) and suffix from (13) match [`code_from_cfd/README.md:22`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md#L22) identically. |
| **AGY R2-2: Preflight in `run_smoke_test.sh` Omits Single-Branch Check for Compare Mode** | MINOR | **RESOLVED** | [`fix26/smoke_test/run_smoke_test.sh:50-53`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L50-L53) | Preflight now asserts `[ "$BR" = "deflected symmetric" ]` whenever `[ "${WRITE_REFERENCE:-0}" != 1 ]`. Incomplete reference files (holding only 1 branch or 0 branches) trigger exit code 2 before OpenFOAM is sourced. Script header exit codes updated at line 25. Verified by test cases `cmp_one` and `cmp_none` in [`test_compare_smoke.py:168-170`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/test_compare_smoke.py#L168-L170). |
| **SOL R2-1: Prescribed Unit-Test Command Failed with Traceback Under Fully Read-Only Sandbox** | MAJOR | **RESOLVED** | [`fix26/smoke_test/test_compare_smoke.py:51-60`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/test_compare_smoke.py#L51-L60) | Unit tests run cleanly when `TMPDIR` is specified. If both system temp (`TMPDIR`/`TEMP`/`TMP`, `/tmp`, ...) and fallback (`HERE`) raise `OSError`, `mktmp()` cleanly halts with `sys.exit(...)` outputting a single descriptive diagnostic (`test_compare_smoke.py: no writable temporary directory, 0 tests run. Tried ... Set TMPDIR to a writable directory...`), exit code 1, without raising unhandled tracebacks in `setUpClass`. |

---

## 3. Verification Against Regressions and Invariants

1. **Byte Invariance of Deliverables:**
   - [`reference_result.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/reference_result.json) is byte-identical across `fix26/`, `fix26_a2_snapshot/`, and `fix26_a1_snapshot/` (`cmp` exited 0).
   - [`compare_smoke.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py) and [`SETUP.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md) are byte-identical to `fix26_a2_snapshot/`.
   - Solver parameters, mesh dictionaries, and iteration counts (3000) remain unchanged.
2. **Side Effect and Sandbox Cleanliness:**
   - No untracked artifacts, cache directories (`__pycache__`), or leftover directories remain under `fix26/smoke_test/` or `/home/azan/paper6_t6_work/audit_tmp`.

---

## 4. Numbered Findings

No defects, regressions, or syntax errors remain.

VERDICT: READY
