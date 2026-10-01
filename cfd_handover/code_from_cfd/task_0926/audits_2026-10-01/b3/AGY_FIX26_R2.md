# Strict Read-Only Post-Fix Audit (Round 2): Task B3 Branch-Aware Smoke Test (`fix26`, Attempt 2)

**Audit Target:** Changed files in [`fix26/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/):
- [`compare_smoke.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py)
- [`reference_result.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/reference_result.json)
- [`test_compare_smoke.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/test_compare_smoke.py)
- [`run_smoke_test.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh)
- [`SETUP.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md)
- [`README_line22_replacement.txt`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/README_line22_replacement.txt)

**Baseline / Originals:** [`code_from_cfd/`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/)  
**Diff Baseline (Attempt 1):** [`fix26_a1_snapshot/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26_a1_snapshot/)  
**Context Documents:** [`B3_DIAGNOSIS.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md), Round-1 Audits [`SOL_FIX26.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/SOL_FIX26.md) and [`AGY_FIX26.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/AGY_FIX26.md), Brief [`OPUS_BRIEF_26b.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/OPUS_BRIEF_26b.md), and Report [`FIX26_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/FIX26_REPORT.md).

---

## 1. Audit Execution Results

All three permitted commands were executed in the test environment without modifying any file:

1. **Unit Test Suite Execution:**
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
   Ran 18 tests in 4.847s

   OK
   ```
   **Result:** 18/18 tests passed (up from 14 in Attempt 1). Zero stray files or directories remained on disk.

2. **Real Run Comparison:**
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
   **Result:** Exit code `0`. Correctly identified the symmetric-jet branch with both flow and FFR stationarity verified. Emitted verdict pointer now refers to `SETUP.md section 4`.

3. **Bash Syntax Verification:**
   ```bash
   bash -n fix26/smoke_test/run_smoke_test.sh
   ```
   **Result:** Exit code `0`. Zero syntax errors.

---

## 2. Round-1 Findings Resolution Matrix

| Finding from Round 1 | Severity in R1 | Status in Attempt 2 | Evidence & Verification |
| :--- | :--- | :--- | :--- |
| **SOL 1: Branch evaluation used $Q$ alone instead of combined $Q$ and $\text{FFR}$** | MAJOR | **RESOLVED** | [`compare_smoke.py:185`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L185) now builds `hit` using `all(in_window(m, r["branches"][k]))`. Auditor probe reproduced in [`test_compare_smoke.py:114-124`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/test_compare_smoke.py#L114-L124) passes. |
| **SOL 2 / AGY 1: Symmetric PASS verdict referred to nonexistent README** | MAJOR / MINOR | **RESOLVED** | [`compare_smoke.py:36`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L36) changed to `see SETUP.md section 4`, matching [`run_smoke_test.sh:120`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L120). Replacement text for root README line 22 provided in [`README_line22_replacement.txt`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/README_line22_replacement.txt). |
| **SOL 3 / AGY 4: Incomplete structural/common-field validation in `load_reference`** | MINOR | **RESOLVED** | [`compare_smoke.py:122-124`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L122-L124) validates `cells == 198252`, `stl_sha256`, `n_iter == 3000`, and `returned_value == RETURNED_Q`. Exits 2 on violation. Asserted in [`test_compare_smoke.py:132-140`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/test_compare_smoke.py#L132-L140). |
| **SOL 4 / AGY 2: `WRITE_REFERENCE=1` in `run_smoke_test.sh` unconditionally refused after 5 min solve** | MAJOR / MINOR | **RESOLVED** | Preflight block in [`run_smoke_test.sh:43-59`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L43-L59) inspects reference branches before sourcing OpenFOAM. Fails fast with exit 2 if both branches exist and `SMOKE_REPLACE_BRANCH` is unset. Forwards `SMOKE_REPLACE_BRANCH` as `--replace-branch` at step 6 ([line 117](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L117)). |
| **AGY 3: Omission of reference governance and replacement instructions in `SETUP.md`** | MINOR | **RESOLVED** | Added explicit section "Reference governance (fix26)" in [`SETUP.md:36`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/SETUP.md#L36). |
| **SOL Sandbox / Test temp isolation: Unit tests failed in read-only environment** | N/A (Brief 5) | **RESOLVED** | [`test_compare_smoke.py:50-53`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/test_compare_smoke.py#L50-L53) `mktmp()` honours `TMPDIR` with fallback to `dir=HERE`. Shipped reference protected by hash verification in `tearDownClass`. |

---

## 3. Technical Audit of Implementation Details

### A. Branch Predicate & Decision Flow
In [`compare_smoke.py:185-194`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L185-L194):
```python
fail, hit, qhit = stability(m), [k for k in BRANCHES if all(in_window(m, r["branches"][k]))], [k for k in BRANCHES if in_window(m, r["branches"][k])[0]]
for k in BRANCHES:
    dq, df = distance(m, r["branches"][k]); print(f"  vs {k} branch ({r['branches'][k]['Q_out_m3s']:.8e} m3/s, FFR {r['branches'][k]['FFR_x56p5']:.5f}): Q {dq:+.5f} %, FFR {df:+.6f}")
if len(hit) > 1: fail.append(f"ambiguous: Q and FFR both in the windows of {len(hit)} branches ({', '.join(hit)}): reference branches too close")
elif not hit and not qhit: fail.append(f"outlet flow in no branch window (+-{TOL_Q_PCT} %): distances above")
elif not hit:
    for k in qhit: fail.append(f"outlet flow in the {k} window but FFR_x56p5 {m['FFR_x56p5']:.6f} differs from {r['branches'][k]['FFR_x56p5']:.6f} by more than {TOL_FFR}")
print(...)
if fail: print("FAIL: " + "; ".join(fail)); print("SMOKE TEST FAIL"); return 1
print(f"SMOKE TEST PASS ({VERDICT[hit[0]]})"); return 0
```
- Branch classification strictly enforces the conjunction: candidate must fall within $\pm 0.1\%$ in flow ($Q$) **and** $\pm 0.0005$ in $\text{FFR}_{x56.5}$.
- If reference entries drift towards each other such that their flow windows overlap, $\text{FFR}$ uniquely resolves the branch. This is verified by `test_overlapping_q_windows_ffr_separates_pass` in [`test_compare_smoke.py:114-124`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/test_compare_smoke.py#L114-L124).
- When a candidate matches flow but fails $\text{FFR}$, every matching candidate in `qhit` is detailed in the failure message.

### B. Structural Validation in `load_reference`
In [`compare_smoke.py:122-124`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L122-L124):
- The dictionary must be schema 2.
- Top-level common fields `cells`, `stl_sha256`, `n_iter`, and `returned_value_stageA_A5_ladders_Q_out_m3s` are strictly checked for existence and exact equality with `CELLS_A5` (198,252), `STL_SHA256`, `N_ITER` (3000), and `RETURNED_Q`.
- The defensive check `type(r[k]) is bool` prevents Python's boolean inheritance from aliasing `True == 1`.
- Any missing or corrupted common field immediately returns `(None, error_msg)` which yields exit code 2 (reference unusable) in compare mode, `--write-reference` mode, and the shell preflight.

### C. `run_smoke_test.sh` Preflight Ordering and Governance
In [`run_smoke_test.sh:31-62`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L31-L62):
- Execution ordering is fail-fast:
  1. Early sanity on environment variables (`SMOKE_REPLACE_BRANCH` without `WRITE_REFERENCE=1` exits 2; missing reference file in compare mode exits 2).
  2. Geometry generator and NPROC syntax checked (exit 2).
  3. Python3 / NumPy availability (exit 2).
  4. Consistency between `controlDict` `endTime` and `compare_smoke.py` `N_ITER` (exit 2).
  5. Reference governance via `compare_smoke.load_reference`: validates reference integrity, checks existing branch entries, validates `SMOKE_REPLACE_BRANCH`, and halts before OpenFOAM is sourced if `WRITE_REFERENCE=1` would fail replacement (exit 2).
  6. OpenFOAM environment sourced, command availability checked, hardware/core count checked, workdir checked.
- All preflight failures consistently yield exit code 2.
- Step 6 parameter expansion `${SMOKE_REPLACE_BRANCH:+--replace-branch "$SMOKE_REPLACE_BRANCH"}` operates safely under `set -u` without generating unbound variable errors.

---

## 4. Numbered Findings

### Finding 1: Unclosed Parenthesis in Root `README.md` Line 22 Replacement Text
- **Severity:** **MINOR**
- **Evidence:** [`fix26/README_line22_replacement.txt:1`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/README_line22_replacement.txt#L1)
- **Description:** Item (12) opens an outer parenthesis at `... and smoke_test/ (Task B3: ...` (character offset 208). At the end of item (12), the text reads:
  ```text
  ... (`WRITE_REFERENCE=1`, replacing an existing branch entry only with `SMOKE_REPLACE_BRANCH=deflected|symmetric`; the other branch is always kept). (13)
  ```
  The single closing parenthesis `)` closes only the inner sub-clause opened at `(`WRITE_REFERENCE=1`...`. The outer parenthesis for `(Task B3: ...)` is left unclosed before the period and `(13)`.
- **Remediation:** In [`README_line22_replacement.txt:1`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/README_line22_replacement.txt#L1), replace `always kept). (13)` with `always kept)). (13)` when applying the edit to [`code_from_cfd/README.md:22`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md#L22).

### Finding 2: Preflight in `run_smoke_test.sh` Omits Single-Branch Check for Compare Mode
- **Severity:** **MINOR**
- **Evidence:** [`fix26/smoke_test/run_smoke_test.sh:43-59`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L43-L59), [`fix26/smoke_test/compare_smoke.py:182-183`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L182-L183)
- **Description:** The preflight block in [`run_smoke_test.sh:44-48`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh#L44-L48) queries the reference file's populated branches into `$BR`. Lines 53–55 assert `[ "$BR" = "deflected symmetric" ]` specifically when `WRITE_REFERENCE=1` without `SMOKE_REPLACE_BRANCH`. However, when running in default comparison mode (`WRITE_REFERENCE` unset), the preflight does not assert that `$BR` contains both branches. If an operator provides a schema-2 reference holding only one branch, preflight allows the expensive 5-minute OpenFOAM simulation to run to completion, only to abort at step 6 with exit code 2 at [`compare_smoke.py:183`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/compare_smoke.py#L183) (`reference lacks the ... branch (compare needs both)`).
- **Remediation:** While fail-safe (the exit code is properly 2) and non-blocking for repository distribution (since shipped [`reference_result.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/reference_result.json) contains both branches), [`run_smoke_test.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh) should fail fast in preflight if `[ "${WRITE_REFERENCE:-0}" != 1 ] && [ "$BR" != "deflected symmetric" ]`.

---

## 5. Conditions for Promotion to Production

1. **Typo Correction in README Replacement:** When merging [`fix26/README_line22_replacement.txt`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/README_line22_replacement.txt) into [`code_from_cfd/README.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/README.md), ensure the closing parenthesis for `(Task B3: ...))` is doubled at the end of item (12).
2. **(Optional Polish):** Add preflight assertion in [`run_smoke_test.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test/run_smoke_test.sh) requiring both branches for compare mode to prevent running CFD on single-branch reference files.

VERDICT: READY WITH CONDITIONS
