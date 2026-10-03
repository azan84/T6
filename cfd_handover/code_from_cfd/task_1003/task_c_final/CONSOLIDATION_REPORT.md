# CONSOLIDATION report: Task C attempt 3 + task-37 P5 changes → `taskFinal/` (Opus 5.5 task 40)

`taskFinal/` = Task C attempt 3 (`taskC/`, audited READY WITH CONDITIONS) + every task-37 change (`taskP5/`, FIX37_REPORT.md).

**Rules followed.**
- I wrote only in `taskFinal/`. Not modified: `taskC/`, `taskP5/`, `taskC_a2_snapshot/`, `taskMerged/`, the live `../pf/`, `../post_case_generic.sh`, `../flow_state_profile.py`, `../b1_settle.py`, `p5/`, `m1/`, `lane2/` and the pool dirs.
- No solver ran on a real case. The only simpleFoam runs were the tests' own: the 1,440-cell blockMesh stub (serial, 2 iterations) and the 41k-cell synthetic tube (2 ranks, 1000 iterations).
- Everything ran niced (`nice -n 10`) with ≤ 2 threads. Calls were foreground, except the ~4-minute synthetic end-to-end test: it ran as a tool-tracked job that I waited for, so a call timeout could not kill it partway.
- No process of mine is left, and the test roots (`.post_test_tmp`, temp dirs) are gone. The simpleFoam processes still on the host are the coordinator's 16-rank A1 solve (`m1/cases/baseline_D7_12p5_resistance`), which I did not touch.

## 1. Key finding: the right merge base is final taskC, not attempt 2

The coordinator's merge (`taskMerged/`, `git merge-file` with base `taskC_a2_snapshot/`) conflicted in four places: `post_case_generic.sh`, `pf/analyze_case.py`, `TEMPLATE_README.md` and `MANIFEST.*`. Those conflicts come from the wrong base. They are not competing edits.

**Evidence that taskP5 was forked from the final attempt-3 taskC.**
- Attempt 3 finished at 13:39–13:40: taskC's last file mtime is 13:39:47, and `opus36_a3.out` was written at 13:40. The unchanged files in `taskP5/` all carry the copy time 15:23:25. So the copy was taken **after** attempt 3 was complete.
- Every attempt-3 file that task 37 did not touch is **byte-identical** in taskC and taskP5:
  - `FIX30_REPORT.md`, including the whole Attempt 3 section;
  - `pf/m1_package.py` (package resolution and hash check);
  - `flow_state_profile.py` (INDETERMINATE);
  - `tests/test_post_guards.py`, `tests/test_flow_state_profile.py`, `tests/test_flow_state_sten70.sh`, `tests/test_post_case_generic.sh`;
  - `b1_settle.py`, `pf/as_meshed_radius.py`, `pf/probe_sections.py`, `pf/sections.py`, `pf/m1_probes.py`, `pf/e0_check.py`, `make_manifest.sh`, `verify_manifest.sh`.
- FIX37_REPORT §1 states: "`taskC/` has not changed since `taskP5/` was copied from it". The check below confirms it.
- **No attempt-3 line is reverted.** I listed every line *removed* in the taskC → taskP5 diff of the four files both sides changed. Each removed line is replaced by an extended version carrying a task-37 feature:
  - `fill(..., mesh_arg)` → `fill(..., mesh_arg, d34_arg)`;
  - `info["outlets"]` → `C.live_outlets(info)`;
  - `geometry_step_ok = ALL_GATES_PASS` → the decisive-gates rule;
  - the extra `${D34_JSON:+--d34 …}` argument;
  - longer print and header lines.
  The guard code itself is untouched: `package-check` step 0b, `run_completion`/`finished`, `--require-finished`, `radius-check`/`radius-commit`, `POST_REUSE_UNCHECKED`, and INDETERMINATE.

**Formal 3-way merge.** Run with `git merge-file -p`, with ours = taskC and theirs = taskP5:

| file | base = taskC (correct) | base = taskC_a2_snapshot (coordinator) |
|---|---|---|
| post_case_generic.sh | clean, = taskP5 | 1 conflict block |
| pf/analyze_case.py | clean, = taskP5 | 1 conflict block |
| TEMPLATE_README.md | clean, = taskP5 | 1 conflict block |
| pf/post_helpers.py | clean, = taskP5 | clean |
| pf/build_m1_case.py, pf/m1_results.py, pf/pf_common.py, pf/pf_roundtrip_build.py | clean, = taskP5 | clean (taskC = a2 for these) |

**How the three a2-base conflicts were resolved by hand.** The conflicting a2-base outputs are kept as evidence in `test_output/consolidation40/merge_check/*.baseA2`. In each block the P5 side is the taskC side plus the task-37 additions, so the resolution is the P5 side, and nothing from attempt 3 is lost:
- **`post_case_generic.sh`:**
  - Header item 5: taskC's text, extended by the D3/D4, flags, decisive-gates (D10) and OUTLET_LOST_IN_MESH description.
  - The `fill` call: taskC's call plus `${D34_JSON:+--d34 $D34_JSON}`.
- **`pf/analyze_case.py`:** the docstring keeps the attempt-3 `--require-finished` paragraph, with the task-37 lost-outlet paragraph inserted after it. The code hunks were not in conflict.
- **`TEMPLATE_README.md`:** the attempt-3 "Incomplete profiles (attempt 3)" bullet stays, followed by the new task-37 section "Outlets lost in the mesh, flags, decisive geometry gates".
- **`MANIFEST.*`:** not merged. They are regenerated (§4).

## 2. What came from where

| file in taskFinal | source | content |
|---|---|---|
| `pf/m1_package.py`, `flow_state_profile.py`, `b1_settle.py`, `pf/as_meshed_radius.py`, `pf/probe_sections.py`, `pf/sections.py`, `pf/m1_probes.py`, `pf/e0_check.py`, `make_manifest.sh`, `verify_manifest.sh`, `FIX30_REPORT.md` | taskC attempt 3 (identical in taskP5) | **Attempt-3 guards:**<ul><li>package resolution without the /tmp root, and the build_info hash verification;</li><li>STATES INDETERMINATE on incomplete profiles;</li><li>B1/D8.</li></ul> |
| `post_case_generic.sh`, `pf/analyze_case.py`, `pf/post_helpers.py`, `TEMPLATE_README.md` | taskC attempt 3 + task-37 hunks (merge, §1) | **Attempt 3:**<ul><li>package-check step 0b;</li><li>last-run completion guard (`run_completion`, `finished`, `--require-finished`);</li><li>radius provenance.</li></ul>**Task 37:**<ul><li>`fill --d34`, D3/D4 columns, `flags` (FLAG_ORDER);</li><li>decisive `geometry_step_ok` and `geometry_all_gates_pass_including_reported`;</li><li>manual-repair from a pipeline record only;</li><li>lost-outlet handling in the analysis;</li><li>`flags` / `outlets_lost_in_mesh` in post_summary.</li></ul> |
| `pf/pf_common.py`, `pf/build_m1_case.py`, `pf/pf_roundtrip_build.py`, `pf/m1_results.py` | task 37 (taskC = a2 for these files) | **Zero-face outlet handling:**<ul><li>no monitors and no zerod_reference entry for the lost outlet;</li><li>`outlets_lost_in_mesh` and `bc_bookkeeping`;</li><li>`lost_outlets` / `live_outlets`.</li></ul>**M1_outlets:** lost-outlet row (Q 0, p N/A, closed, flag).<br>**M1_results:** new columns `flags`, D3/D4, `outlets_lost_in_mesh`; `NOT_CONVERGED` merge. |
| `p5/build_m1_geometry.py`, `p5/summarise_p5.py` | task 37 (staging copies) | **D10 gate bookkeeping:** `GATES_DECISIVE` / `GATES_REPORTED_NON_DECISIVE`; `ALL_GATES_PASS` covers decisive gates only; `ALL_GATES_PASS_INCLUDING_REPORTED`.<br>Each copy differs from its `p5/` original only by these changes; the originals (mtime 11:34 / 11:53) are older than the copies. |
| `tests/test_empty_patch_coded_bc.py`, `tests/test_flags_p5.py`, `FIX37_REPORT.md`, `test_output/fix37/` | task 37 | new tests and their evidence |
| all other `tests/*` and `test_output/*` | taskC attempt 3 (identical in taskP5) | the evidence dirs `post_case_generic_synthetic/` and `flow_state_sten70/` were refreshed by the runs below |
| `tests/run_all_consolidation40.sh`, `test_output/consolidation40/`, `CONSOLIDATION_REPORT.md` | new (task 40) | runner for every test, the outputs of both runs, merge evidence |

**Not copied:** `__pycache__`, `*.pyc`, `.post_test_tmp`, `tmp37`. The last two were not present in taskP5 anyway.

**Live install.** The live `../pf/*.py` (the taskC files), `../post_case_generic.sh`, `../flow_state_profile.py` and `../b1_settle.py` are byte-identical to taskC. The live `pf/` also has `build_pf_item1.py` and `pf_roundtrip_analyse.py`, which are not part of the template. So installing taskFinal over the live files means exactly the task-37 diff.

## 3. Tests: every test of both lineages, run twice against taskFinal

`taskC/tests` ⊂ `taskP5/tests` = `taskFinal/tests`: 10 tests, plus the helper `synthetic_tube.py`. Each test resolves its code from its own parent directory (`TC = dirname(tests/)`), so it exercised taskFinal's code. The runner is `bash tests/run_all_consolidation40.sh <run> [tests…]`. Full outputs are in `test_output/consolidation40/run{1,2}/<test>.txt` and `summary.txt`.

**Run 1:**
```
test_b1_settle.py                rc=0    0s  PASS {'A_res_mp': ('B1', '546', '546', 'RUN THE FULL BUDGET (D8 production default: no early stop is authorised); ...
test_flow_state_profile.py       rc=0   20s  PASS: analytic offset/r_eq = a/4 = 0.1 reproduced (x tube and oblique tube, frame-independent), axisymmetric 0, compare AGREE/DIFFER as designed; invalid/missing/unmatched stations -> STATES INDETERMI...
test_post_guards.py              rc=0    1s  PASS: post guards (package resolution + build_info hash verification, last-run completion, radius provenance)
test_manifest.sh                 rc=0    0s  PASS test_manifest
test_flags_p5.py                 rc=0    1s  PASS: 5 cases, expected flag sets reproduced
test_section_rule.py             rc=0   17s  PASS
test_p5_stub.py                  rc=0   21s  PASS: 5 P5 packages built (case files, stub mesh)
test_empty_patch_coded_bc.py     rc=0   79s  PASS: 0-face outlet patch: coded BC accepted on the empty patch (2 serial simpleFoam iterations, End), its monitors omitted (they are fatal: negative control), post path reports Q 0 / p N/A / OUTLET_L...
test_flow_state_sten70.sh        rc=0   67s  PASS: a5_arch8 (deflected) vs smoke_cont (axisymmetric) STATES DIFFER on the full profile; both comparisons with case_S50 INDETERMINATE (invalid x = 52 mm section), never AGREE on a subset
test_post_case_generic.sh        rc=0  258s  PASS: post_case_generic.sh end to end on a synthetic finished solve (evidence in test_output/post_case_generic_synthetic/)
```

**Run 2:**
```
test_b1_settle.py                rc=0    0s  PASS {'A_res_mp': ('B1', '546', '546', 'RUN THE FULL BUDGET (D8 production default: no early stop is authorised); ...
test_flow_state_profile.py       rc=0   21s  PASS: analytic offset/r_eq = a/4 = 0.1 reproduced (...); invalid/missing/unmatched stations -> STATES INDETERMI...
test_post_guards.py              rc=0    0s  PASS: post guards (package resolution + build_info hash verification, last-run completion, radius provenance)
test_manifest.sh                 rc=0    1s  PASS test_manifest
test_flags_p5.py                 rc=0    1s  PASS: 5 cases, expected flag sets reproduced
test_section_rule.py             rc=0   17s  PASS
test_p5_stub.py                  rc=0   18s  PASS: 5 P5 packages built (case files, stub mesh)
test_empty_patch_coded_bc.py     rc=0   67s  PASS: 0-face outlet patch: coded BC accepted on the empty patch (2 serial simpleFoam iterations, End), its monitors omitted (...), post path reports Q 0 / p N/A / OUTLET_L...
test_flow_state_sten70.sh        rc=0   59s  PASS: a5_arch8 (deflected) vs smoke_cont (axisymmetric) STATES DIFFER on the full profile; both comparisons with case_S50 INDETERMINATE (invalid x = 52 mm section), never AGREE on a subset
test_post_case_generic.sh        rc=0  233s  PASS: post_case_generic.sh end to end on a synthetic finished solve (evidence in test_output/post_case_generic_synthetic/)
```

**20/20 PASS.** The outputs of `test_flags_p5` and `test_flow_state_sten70` are byte-identical between the two runs.

**Key lines (run 1, the same in run 2).**
- **`test_flags_p5.py`** (the five real P5 cases, read-only): all five flag sets match the brief-37 expectations.
  ```
   138: flags D3_FAIL;D4_FAIL;CHECKMESH_STANDARD_FAIL | geometry_step_ok True (incl. reported False)
    69: flags LESION_PURITY_GATE_FAIL;POSITIVE_CONTROL_UNDETECTED | geometry_step_ok False | D3 PASS D4 PASS thr 2.596 mm meas 2.040 mm
   473: flags D2_RELATIVE_THROAT_GATE_FAIL;D3_FAIL;D4_FAIL;MEASUREMENT_PROBE_RELOCATED | geometry_step_ok False
   272: flags SELF_INTERSECTION;D3_FAIL;D4_FAIL;OUTLET_LOST_IN_MESH | geometry_step_ok False | lost out_396
   139: flags D2_RELATIVE_THROAT_GATE_FAIL;D3_FAIL;D4_FAIL | geometry_step_ok False
  ```
- **`test_empty_patch_coded_bc.py`:**
  ```
  M1_outlets out_2: Q_mls 0.0, p_bar_Pa N/A, closed 1, lost_in_mesh 1, flag OUTLET_LOST_IN_MESH, R_source 'bc_A.csv on a 0-face patch: NOT applied (no flow)'
  M1_results flags: OUTLET_LOST_IN_MESH;NOT_CONVERGED | outlets_lost_in_mesh: out_2
  ```
  The negative control (the old monitors on the 0-face patch) gives the FOAM FATAL in surfaceFieldValue, as in FIX37.
- **`test_post_case_generic.sh`:** every attempt-3 guard still holds together with the task-37 flags.
  - **Completion:** RUN COMPLETE (last Time 1000 = endTime, End at line 46134).
  - **Package:** verified against build_info `package_hashes`.
  - **Radius:** regenerated, provenance written.
  - **Summary flags:** `GEOMETRY_GATES_MISSING;D34_MISSING;MEASUREMENT_PROBE_RELOCATED`.
  - **(d)** reuse.
  - **(f)** `RUN NOT COMPLETE` (appended run).
  - **(g)** `PACKAGE NOT VERIFIED`.
  - **(h)** `--require-finished … exit 4`.
  - **(i)** `mesh sha256 differs` → regenerated; then `REUSED UNCHECKED`; then a verified reuse.

**Not re-run here** (as in FIX37): the scan-14 geometry-builder regression (about 9.5 min). `p5/build_m1_geometry.py` in taskFinal is byte-identical to the taskP5 copy that FIX37 §4 regressed: 1381 leaves vs `m1/out/baseline/gates.json`, the same 5 documented differences, 0 differences vs the p5 regression. Its code is not touched by this consolidation. Likewise, test_flags_p5 was run without the optional temp rebuild of 272: that is a builder run on a real mesh, and the real 272 case is covered through the `mesh_patches` fallback.

## 4. Manifest
`__pycache__` was removed, then `make_manifest.sh .` (LF-normalised hash rule) and `verify_manifest.sh .` were run. The result is in §4a, appended after the manifest was written.

## 5. Open points
1. **Install.**
   - Installing taskFinal = installing the task-37 diff over the live files (§2).
   - The two `p5/` copies replace `p5/build_m1_geometry.py` and `p5/summarise_p5.py`. Their staging path fallback is a no-op once they are installed in `p5/`.
   - The coordinator does this; I did not touch the live files or `p5/`.
2. **Rebuild the real `p5/cases/272_resistance` after installing** (FIX37 open point 1). It still has the fatal `out_396` monitors, and the installed `analyze_case` refuses it until rebuilt. Use the absolute `--extensions-json …/p5/out/272_extensions.json`.
3. **Carried over from FIX37 §6, still open:**
   - the empty-patch BC was tested serially only; the first parallel test is the 272 smoke;
   - the 473 D3/D4 distance is measured to the package probe p011, not to `p011_reloc`;
   - the 69 and 272 measurement distances (2.040 / 2.013 mm) are close to the 2 mm limit;
   - prescribed mode with a lost outlet has not been solved.
4. **Carried over from FIX30 attempt 3 / AGY C2, still open:**
   - the finished guard refuses early-stopped runs, with no override;
   - INDETERMINATE stays the verdict even when the subset max > tol (coordinator decision);
   - run Task A with `REF_FFR=0.8697574904997768` and `PKG_ROOT` unset;
   - the 473 relocation must pass S3/S4 on the P5 mesh.
5. **`taskMerged/` is superseded by taskFinal.** Its files are byte-identical to taskP5, so it is no different in content. It was left untouched.
6. **CRLF test-output CSVs.** Python's csv module writes CRLF, so plain `sha256sum -c` reports those CSVs as FAILED. `verify_manifest.sh` passes them, and they are listed in MANIFEST.README. This predates this task.

### 4a. Manifest result
- `make_manifest.sh .` wrote **148 entries**. MANIFEST.sha256 has no comment lines, and `__pycache__`/`*.pyc` are excluded.
- `verify_manifest.sh .` reports `verify_manifest: 148 OK, 0 FAILED/MISSING (LF-normalised text, raw binary)`, with no unlisted files.
- Plain `sha256sum -c MANIFEST.sha256` reports 12 FAILED. These are exactly the 12 CRLF test-output CSVs listed in MANIFEST.README (open point 6).
- **Write order.** This section was appended after the first manifest. The manifest was then regenerated and verified again with the same result, so it covers this final version of the report.
