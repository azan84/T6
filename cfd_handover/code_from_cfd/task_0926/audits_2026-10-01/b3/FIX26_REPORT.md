# FIX26 report: branch-aware B3 smoke test (attempt 1)
Scope: only files under fix26/ changed. No OpenFOAM, mpirun, cartesianMesh or run_smoke_test.sh was run. Real evidence dirs were only read.

## What changed
**smoke_test/compare_smoke.py** (header docstring tagged fix26)
- `BRANCHES` constants in the code: deflected Q 1.17392231e-06 / FFR 0.78395964 (returned run, p_meas 8.87426046), symmetric Q 1.17825059e-06 / FFR 0.78248298 (smoke_ref). Tolerances `TOL_Q_PCT=0.1`, `TOL_FFR=0.0005`, final window `WIN=200`, `TOL_QBAND_PCT=0.01`, `TOL_FFRBAND=1e-5`.
- `measure` now also computes `FFR_band_last200` (FFR from measurementP x RHO/P_AORTA over the last 200 iterations). The complete-run checks, mesh checks and re-verification are unchanged.
- The compare verdict is PASS iff the run is complete AND the mesh checks hold AND the cell count equals the reference AND exactly one branch has |Q/Q_b-1| <= 0.1 % AND |FFR-FFR_b| <= 0.0005 for that branch AND the final window is stable. Q_b and FFR_b come from `reference_result.json` `branches`. The verdict line names the branch (the brief's two strings, verbatim). A FAIL always prints the distance (dQ %, dFFR) to each branch plus a reason: no window, Q in window but FFR out, or unstable window.
- `load_reference`: accepts only schema 2. Schema 1 gets a clear error (exit 2) saying the file cannot state which branch it holds and pointing to the shipped schema-2 file. Every branch entry in the file must lie within the window of its `BRANCHES` constant, so an edited or partial file cannot redefine a branch (exit 2). Compare needs both branches (exit 2 if one is missing).
- `--write-reference OUT [--replace-branch NAME]` refuses in these cases:
  - incomplete run or failed mesh checks: exit 3
  - the run lies in no branch window, or in more than one (windows around the constants, not the file), or the final window is unstable: exit 1
  - the base file is schema 1 or inconsistent: exit 2
  - the run's branch already has an entry and `--replace-branch <that branch>` was not given: exit 2
  - `--replace-branch` names the other branch: exit 2

  Otherwise it writes the branch entry (Q, FFR, p_meas, p_outlet, provenance) and keeps the other branch unchanged. The base is the positional reference, if it exists. If it does not exist, a file holding only this branch is written, with a note that compare needs both. Provenance records: run dir, date, mesh origin (recipe, not identity), iterations, solver/wall clock, OMP threads, window bands, sha256 of the retained `constant/polyMesh/points`, processor faces (`Number of processor faces = N` in log.decomposePar), nprocs (count of `Processor i` lines), and decomposition method (system/decomposeParDict).
- `__main__` became `main(argv) -> exit code` so the tests can run it in-process. `--replace-branch` without `--write-reference` exits 2. The reference file is now written with `with open(...)`.
- Exit codes: 0/1/3 keep their meaning. Exit 2 is new in compare_smoke.py, used for "reference unusable / write refused". It matches run_smoke_test.sh's exit 2, which means setup error.

**smoke_test/reference_result.json**: schema 2 (`schema`, `note`, `cells` 198252, `stl_sha256`, `n_iter` 3000, informational `tolerances`, `returned_value_stageA_A5_ladders_Q_out_m3s`, `branches`).
- deflected:
  - Q 1.17392231e-06, p_meas 8.87426046, FFR 0.7839596.
  - p_outlet_patch null for the returned run. The re-run value 8.35318751 (t2_archmesh_patch) is in provenance.
  - Provenance: returned run 2026-09-18, archived mesh, 2000 it, 8 ranks scotch.
  - Points sha256 d59242c7... comes from t2_archmesh_patch (a copy of the archived mesh).
  - Processor faces 2869 come from the t2 re-run's log.decomposePar. The 2026-09-18 log itself was not read.
  - Re-runs on 2026-10-01: a5_arch8 1.17390297e-06 (2000 it) and t2_archmesh_patch 1.17390294e-06 (3000 it).
- symmetric:
  - Values from the old file (Q 1.17825059e-06, p_meas 8.85754493, FFR 0.78248298, p_outlet 8.38179515).
  - Provenance: smoke_ref 2026-10-01, fresh cartesianMesh with OMP 8, 3000 it, 8 ranks scotch, points sha256 a036ad8d... (computed), processor faces 2899 (log.decomposePar), solver 290 s, wall 318 s.

**smoke_test/test_compare_smoke.py** (new; run with `python3 test_compare_smoke.py`, stdlib unittest + numpy)
- Synthetic work dirs contain 1..3000 monitors with a decaying transient (plus an optional drift over the last 200 iterations), a log with `Time =` lines and `End`, controlDict, decomposeParDict, smoke_checks.json, and the retained mesh files that `reverify` reads.
- The only patch is `compare_smoke.STL_SHA256`, set to the dummy STL's hash while the in-process calls run. Re-verification itself runs unpatched.
- The real `/home/azan/paper6_t6_work/smoke_ref` is checked in a subprocess with nothing patched.
- The write tests use temp copies of the reference. A class teardown asserts that the shipped reference_result.json's sha256 is unchanged.

**smoke_test/run_smoke_test.sh**: only header comments and the final message changed (diff below). Numerics, recipe, 3000 iterations, preflight and exit codes are unchanged; the last line still exits with compare_smoke.py's code. `bash -n` passes. The preflight import `compare_smoke.N_ITER` still prints 3000.

**SETUP.md section 4**
- 3000 iterations; about 5-6 min on 8 physical cores (reference 318 s wall).
- Default WORKDIR is `${TMPDIR:-/tmp}/paper6_t6_smoke_work`.
- Two-branch paragraph, and what PASS means: a correct install reaching one of two validated states; only the deflected branch reproduces the returned value.
- The criterion now includes FFR and window stability. Optional unit test command added.

Wording (SOL 8): "same mesh" became "same mesh recipe and cell count (not mesh identity: cfMesh is not bitwise reproducible)" in the compare_smoke header, the run_smoke_test.sh header and final message, and SETUP.md.

## Test output
```
test_between_branches_fail (__main__.T) ... ok
test_deflected_pass (__main__.T) ... ok
test_incomplete_run_3 (__main__.T) ... ok
test_other_cell_count_3 (__main__.T) ... ok
test_q_in_window_ffr_out_fail (__main__.T) ... ok
test_real_smoke_ref_symmetric (__main__.T) ... ok
test_reference_cannot_redefine_branch (__main__.T) ... ok
test_schema1_reference_clear_error (__main__.T) ... ok
test_shipped_reference_consistent (__main__.T) ... ok
test_symmetric_pass (__main__.T) ... ok
test_unstable_window_fail (__main__.T) ... ok
test_write_reference_new_file (__main__.T) ... ok
test_write_reference_refuses_off_branch_and_unstable (__main__.T) ... ok
test_write_reference_replacement (__main__.T) ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.749s

OK
```
Real smoke_ref (`python3 compare_smoke.py /home/azan/paper6_t6_work/smoke_ref reference_result.json --wall 318`, exit 0):
```
  vs deflected branch (1.17392231e-06 m3/s, FFR 0.78396): Q +0.36870 %, FFR -0.001477
  vs symmetric branch (1.17825059e-06 m3/s, FFR 0.78248): Q +0.00000 %, FFR +0.000000
vs the returned Stage A A5 coarse value 1.17392231e-06: +0.36870 %   cells 198252 (reference 198252)   final-window bands: Q 1.19e-05 %, FFR 2.74e-08   wall 318 s
SMOKE TEST PASS (symmetric-jet branch; not the returned value, see README)
```
Sanity check on the real deflected-branch monitors. These are not full smoke work dirs (no smoke_checks.json), so only the distance and band functions were applied:
- t2_archmesh_patch: dQ -0.00165 %, dFFR +7e-06 to deflected; Q band 1.3e-05 %, FFR band 2.4e-08.
- bi_new_from_asym (4000 it): dQ -0.00166 %, dFFR +7e-06; bands 6e-06 % and 1.2e-08.

Both would be identified as deflected with a stable window, and both are about 0.369 % / 0.00148 away from the symmetric branch.

run_smoke_test.sh diff (old vs new):
```
2c2
< # Smoke test (Task B3, work order 2026-09-26): a second machine proves it reproduces one returned result in well under 30 minutes.
---
> # Smoke test (Task B3, work order 2026-09-26; fix26 2026-10-01: branch-aware): a second machine proves that its install reaches one of the two validated steady states of one returned case in well under 30 minutes.
6c6,8
< # Returned result it reproduces: outlet flow 1.17392231e-06 m3/s (stageA_A5_ladders.csv, A5 sten70 coarse; also reference_result.json of this folder from a fresh run of THIS script).
---
> # Two branches (fix26, B3 diagnosis 2026-10-01): the case has two stable steady solutions on the same mesh recipe and cell count (not mesh identity: cfMesh is not bitwise reproducible), a fresh run lands on either,
> #   decided by tiny cfMesh/decomposition perturbations: DEFLECTED jet, outlet flow 1.17392231e-06 m3/s, FFR_x56p5 0.78396 (= the returned value, stageA_A5_ladders.csv, A5 sten70 coarse) and SYMMETRIC jet,
> #   1.17825059e-06 m3/s, FFR_x56p5 0.78248 (reference-machine smoke run 2026-10-01). Both are in reference_result.json (schema 2, 'branches'); only the deflected branch reproduces the returned value.
8,11c10,16
< # PASS = complete run (exact 'End' line, log 'Time =' 1..3000 each once in order, monitors with iterations exactly 1..3000 and finite values), same mesh (STL sha256, checkMesh OK, exactly 1 inlet + 1 outlet wall->patch rewrite,
< #   cells EQUAL to the reference; compare_smoke.py re-verifies STL hash, boundary types and checkMesh log from the retained work directory) and outlet flow within 0.1 % of reference_result.json (and of the returned value), see compare_smoke.py.
< # Timing claim: about 10 minutes on 8 PHYSICAL cores of a workstation (see reference_result.json); the 30-minute claim needs 8 physical cores (NPROC > physical cores is refused unless SMOKE_ALLOW_FEWER_CORES=1).
< # env: WRITE_REFERENCE=1 = reference run: step 6 writes $HERE/reference_result.json from this run (no comparison; only if the run is complete and the mesh checks hold) and exits 0; without it, reference_result.json must exist (checked before any expensive step).
---
> # PASS = complete run (exact 'End' line, log 'Time =' 1..3000 each once in order, monitors with iterations exactly 1..3000 and finite values), same mesh recipe and cell count (STL sha256, checkMesh OK, exactly 1 inlet + 1 outlet
> #   wall->patch rewrite, cells EQUAL to the reference; compare_smoke.py re-verifies STL hash, boundary types and checkMesh log from the retained work directory) and the run on exactly one branch: outlet flow within 0.1 %
> #   and FFR_x56p5 within 0.0005 of that branch, with a stable final window (last 200 iterations: Q band <= 0.01 %, FFR band <= 1e-5); the verdict line names the branch, see compare_smoke.py.
> # Timing claim: about 5-6 minutes on 8 PHYSICAL cores of a workstation (reference run: 318 s wall, see reference_result.json); the 30-minute claim needs 8 physical cores (NPROC > physical cores is refused unless SMOKE_ALLOW_FEWER_CORES=1).
> # env: WRITE_REFERENCE=1 = reference run: step 6 adds this run to $HERE/reference_result.json as the branch it lands on (no comparison; only if the run is complete, the mesh checks hold, the final window is stable
> #      and it lies within 0.1 % Q / 0.0005 FFR of one branch constant; the other branch is kept) and exits 0. fix26: an EXISTING entry of that branch is NOT replaced (step 6 exits 2): to replace it, run
> #      python3 compare_smoke.py <WORKDIR> reference_result.json --write-reference reference_result.json --replace-branch <branch> by hand. Without WRITE_REFERENCE, reference_result.json must exist (checked before any expensive step).
18c23
< # exit codes: 0 PASS (or reference written); 1 FAIL (flow criterion); 2 setup error (preflight: python3/numpy, OpenFOAM v2406 (WM_PROJECT_VERSION), OpenFOAM commands, wmake/g++, NPROC, physical cores; workdir, reference file, geometry generator missing);
---
> # exit codes: 0 PASS (or reference written); 1 FAIL (branch criterion: no branch matched, FFR inconsistent with the matched branch, or unstable final window); 2 setup error (also: reference_result.json unusable, e.g. schema 1, or WRITE_REFERENCE refused to replace a branch entry) (preflight: python3/numpy, OpenFOAM v2406 (WM_PROJECT_VERSION), OpenFOAM commands, wmake/g++, NPROC, physical cores; workdir, reference file, geometry generator missing);
93c98,100
< step "6/6 compare"; echo "solver rc=$RC"; python3 "$HERE/compare_smoke.py" "$W" "$REF" --wall $(( $(date +%s) - T0 )); exit $?
---
> step "6/6 compare"; echo "solver rc=$RC"; python3 "$HERE/compare_smoke.py" "$W" "$REF" --wall $(( $(date +%s) - T0 )); RC=$?
> [ $RC -eq 0 ] && echo "PASS means: a correct install reaching one of the two validated steady states of this case (same mesh recipe and cell count, not mesh identity); only the deflected-jet branch reproduces the returned value 1.17392231e-06 m3/s (SETUP.md section 4)"
> exit $RC
```

## Open points
1. **The deflected entry is not a smoke-script run.** It holds the returned value, not a run of run_smoke_test.sh (its provenance says so). When a reference-machine smoke run lands on the deflected branch, replace it with `compare_smoke.py <W> reference_result.json --write-reference reference_result.json --replace-branch deflected`. Its points hash and processor-face count come from the re-run t2_archmesh_patch on the archived mesh (the same mesh file; decomposition assumed identical, 8 ranks scotch), not from the 2026-09-18 run's own logs, which were not read.
2. **WRITE_REFERENCE=1 cannot replace a branch.** In run_smoke_test.sh it now exits 2 if the run lands on a branch that already has an entry (both do in the shipped file). Replacing must be done by hand with `--replace-branch`. This is intended (no silent replacement), but a reference-machine operator has to know it; it is documented in the script header.
3. **Exit 2 is new in compare_smoke.py.** It is used for reference unusable / write refused. The brief allowed exit codes 0/1/3 only "unchanged in meaning"; 2 already means setup error in run_smoke_test.sh, so the overall meaning is consistent. Please confirm this is acceptable.
4. **No real smoke run was done here.** The brief calls for verification by two real runs. Not done here by instruction.
5. **Minor inconsistency in the reference file.** The FFR consistency window is checked against the reference file's branch values; identification for `--write-reference` uses the code constants. The shipped file's values equal the constants. A replaced deflected entry (e.g. 1.17390297e-06) would differ from the constant by -0.0017 %, well inside the window. The `tolerances` block in reference_result.json is informational only; the code constants govern.
6. **Things this fix does not cover.** Items from the audits outside this brief remain open for the report/NOTE: the U3D branch-consistency caveat (SOL 7), the mesh-difference wording in B3_DIAGNOSIS.md (SOL 3 / AGY 3), and decomposition as a co-cause of branch selection (SOL 1).

---

# Attempt 2 (2026-10-01): post-fix audits SOL_FIX26.md (NOT READY) and AGY_FIX26.md (READY WITH CONDITIONS)
Nothing was run except python3 unit tests, `bash -n` and the read-only comparison of `/home/azan/paper6_t6_work/smoke_ref`. No OpenFOAM, mpirun, cartesianMesh, or full run_smoke_test.sh run. The shell tests stop inside the preflight before OpenFOAM is sourced. No change to numerics, recipe, iteration count (3000) or `case_files/`. `reference_result.json` is byte-identical to attempt 1. Files changed: `smoke_test/compare_smoke.py`, `smoke_test/run_smoke_test.sh`, `smoke_test/test_compare_smoke.py`, `SETUP.md`. New: `README_line22_replacement.txt`. A stray `smoke_test/__pycache__/` (not a deliverable) was removed.

## Per finding
1. **SOL 1 (MAJOR): combined predicate.** `compare_smoke.py` main now sets `hit` = the branches with Q AND FFR both in window, the same predicate `write_reference` uses. Exactly one -> that branch (then the stability check). Two -> FAIL "ambiguous: Q and FFR both in the windows of 2 branches". Zero -> FAIL. Within the zero case: a Q-only hit is reported as "outlet flow in the <b> window but FFR_x56p5 ... differs" (all Q-only hits are listed); no Q hit at all is reported as "outlet flow in no branch window" with the distances. The docstring is updated. New tests:
   - `test_overlapping_q_windows_ffr_separates_pass` reproduces the auditor's case. Reference deflected Q x1.00099 and symmetric Q x0.99901 are both accepted by load_reference, and their Q windows overlap. A run at Q 1.17608e-06 is inside both Q windows (asserted). With the deflected FFR it gives PASS deflected. With the symmetric FFR it gives PASS symmetric. With FFR 0.7832 it gives FAIL, naming both Q-only windows.
   - `test_two_branches_both_in_window_ambiguous_fail`: FFR entries are also moved by 0.00049 towards each other, so the run is in both combined windows -> FAIL (ambiguous).
2. **SOL 2 / AGY 1: verdict string.** It is now `SMOKE TEST PASS (symmetric-jet branch; not the returned value, see SETUP.md section 4)`, matching run_smoke_test.sh's final message. The replacement text for `code_from_cfd/README.md` line 22 is in `fix26/README_line22_replacement.txt`: one paragraph, the full line 22, with only item (12) rewritten. The text before (12) and items (13)-(15) are checked byte-identical to the current line. Item (12) now covers the two branches, what PASS means, schema 2, the governance rules and `test_compare_smoke.py`. It drops the obsolete "reproduces ... within 0.1 %" and "written by one reference run" claims. It has not been applied (outside fix26/).
3. **SOL 3 / AGY 4: common-field validation.** `load_reference` requires schema 2 and the `branches` object (as before), plus: `cells == CELLS_A5`, `stl_sha256 == STL_SHA256`, `n_iter == N_ITER`, `returned_value_stageA_A5_ladders_Q_out_m3s == RETURNED_Q`. A missing field or wrong value returns "reference <path>: common field '<k>' missing / = <value>, expected <constant>". That gives exit 2 in compare and in `--write-reference` (the file is left unchanged). It also gives exit 2 in the shell preflight (see 4). `test_reference_common_fields_validated` covers each field (wrong value, plus missing cells and missing returned value, plus schema 3) in both modes. Because load_reference now checks the STL hash, the in-process synthetic tests use a temp copy of the shipped reference with the dummy STL hash. The shipped file itself is checked unpatched by `test_shipped_reference_consistent`, the subprocess smoke_ref test and the shell tests.
4. **SOL 4 / AGY 2, 3: WRITE_REFERENCE path.** Changes to run_smoke_test.sh (header, preflight, step 6 forwarding only):
   - New env `SMOKE_REPLACE_BRANCH=deflected|symmetric`, forwarded as `--replace-branch` at step 6 (`${SMOKE_REPLACE_BRANCH:+--replace-branch "$SMOKE_REPLACE_BRANCH"}`). `exit $?` is kept, so exit codes still propagate.
   - New preflight block, after the python3/numpy/N_ITER checks and BEFORE the OpenFOAM bashrc is sourced (nothing expensive has run). It reads the reference through `compare_smoke.load_reference` and exits 2 when:
     - the file exists but is unusable (also without WRITE_REFERENCE);
     - WRITE_REFERENCE=1, the file holds both branches and SMOKE_REPLACE_BRANCH is unset (the message names the existing entries and how to replace one);
     - SMOKE_REPLACE_BRANCH is not deflected|symmetric;
     - SMOKE_REPLACE_BRANCH is set without WRITE_REFERENCE=1.
   - The startup message now says what step 6 will do: the existing entries, and either "replaces the <b> entry IF the run lands on <b> (other kept; other branch refused, exit 2, file unchanged)" or "adds this run as the branch it lands on if that branch has no entry yet; an existing entry is not replaced (exit 2; set SMOKE_REPLACE_BRANCH)".
   - The no-reference message no longer suggests writing a reference with WRITE_REFERENCE=1 on a second machine.
   - SETUP.md section 4 has a new "Reference governance (fix26)" paragraph: only the reference machine writes; how to replace a branch; the other branch is kept; the preflight refusal; the manual command; the reference validation.

   Verification: `bash -n` passes. `test_shell_preflight_reference_governance` runs a temp copy of the script with `bash` (script, compare_smoke.py, controlDict, a reference; GEN = dummy; FOAM_BASHRC = a non-existent path, so the script can never get past the OpenFOAM check). It asserts rc 2 and the message for each case below. It also asserts that no WORKDIR was created and that the reference copy is unchanged.

   | case | result |
   |---|---|
   | plain compare | governance passes, stops at "bashrc not found" |
   | WRITE_REFERENCE=1, both branches, no SMOKE_REPLACE_BRANCH | refused before the OpenFOAM check |
   | SMOKE_REPLACE_BRANCH=foo | refused |
   | SMOKE_REPLACE_BRANCH without WRITE_REFERENCE | refused |
   | WRITE_REFERENCE=1 + SMOKE_REPLACE_BRANCH=deflected | "Step 6 replaces the deflected entry IF ...", then stops at the OpenFOAM check |
   | one-branch reference | "Step 6 adds this run ..." |
   | schema-1 reference | "preflight: reference ... not schema 2" |

   The step 6 forwarding line itself is not executed (it needs a full run). The `--replace-branch` behaviour it forwards to is covered by `test_write_reference_replacement`.
5. **Temp directory.** `mktmp()` uses `tempfile.mkdtemp` (honours TMPDIR/TEMP/TMP, then /tmp, /var/tmp). On OSError it falls back to a `fix26_test_*` directory next to the test file, removed in tearDownClass. The fallback was checked by setting `tempfile.tempdir` to a non-existent directory: it created `.../fix26/smoke_test/fix26_test_*`. tearDownClass still asserts that the shipped `reference_result.json` sha256 is unchanged. All writes go to temp copies.

## Test output (`python3 test_compare_smoke.py`)
```
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
Ran 18 tests in 4.735s

OK
```

## bash -n
```
bash -n smoke_test/run_smoke_test.sh: OK (exit 0)
```

## Real smoke_ref comparison (`python3 -B compare_smoke.py /home/azan/paper6_t6_work/smoke_ref reference_result.json --wall 318`)
```
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
vs the returned Stage A A5 coarse value 1.17392231e-06: +0.36870 %   cells 198252 (reference 198252)   final-window bands: Q 1.19e-05 %, FFR 2.74e-08   wall 318 s
SMOKE TEST PASS (symmetric-jet branch; not the returned value, see SETUP.md section 4)
exit 0
```

## Open points (attempt 2)
- README line 22 is not applied: the coordinator applies `README_line22_replacement.txt` (whole line 22).
- Attempt-1 open points 1, 3, 4, 6 still stand: the deflected entry is not a smoke-script run; exit 2 in compare_smoke.py needs confirmation; no real smoke runs were done; audit items are outside this brief. Open point 2 (WRITE_REFERENCE cannot replace) is resolved by SMOKE_REPLACE_BRANCH. Open point 5 is unchanged: identification in compare uses the reference entries with the combined predicate, while write uses the constants.
- With a one-branch reference and no SMOKE_REPLACE_BRANCH, the preflight cannot know which branch the run will land on. If the run lands on the existing branch, step 6 still refuses (exit 2) after the full run. The startup message says so.

## Attempt 3 (OPUS_BRIEF_26c.md: AGY_FIX26_R2 findings 1-2, SOL_FIX26_R2 finding 1)
Changed files vs `fix26_a2_snapshot/`: `README_line22_replacement.txt`, `smoke_test/run_smoke_test.sh`, `smoke_test/test_compare_smoke.py`. Unchanged: `compare_smoke.py`, `reference_result.json` (byte-identical, `cmp`), `SETUP.md`, `case_files/`. No numerics, recipe, iteration count or exit-code meaning changed; no OpenFOAM/mpirun/cartesianMesh/full `run_smoke_test.sh` run.

1. **AGY R2-1 (README replacement parenthesis).** `always kept). (13)` -> `always kept)). (13)`: the second `)` closes the outer `(Task B3: ...`. Checked by script: the bracket depth of every item (12)-(15) returns to 0 at its end and never goes below 0.
2. **AGY R2-2 (compare-mode preflight).** New check in `run_smoke_test.sh`, right after the reference-governance block and before `FOAM_BASHRC` is sourced: if `WRITE_REFERENCE` is not 1 and the reference does not hold both `deflected` and `symmetric`, it prints `preflight: compare mode needs both branch entries (deflected, symmetric) in <ref>, but it holds: <entries>. Copy the shipped schema-2 reference_result.json here ...` and exits 2. The header exit-code comment for code 2 now mentions this. The step-6 check in `compare_smoke.py` is still there as a second guard. The shell-level test `test_shell_preflight_reference_governance` has two new cases: a one-branch reference (symmetric only) and an empty `branches` dict. Both must exit 2 with the new message, must not reach the OpenFOAM bashrc check, and must leave no workdir and an unchanged reference copy. All earlier cases in that test are unchanged and still pass.
3. **SOL R2-1 (read-only sandbox).** `mktmp()` keeps its order: first system temp (`TMPDIR`/`TEMP`/`TMP`, `/tmp`, ...), then the fallback next to the test file. If both fail, the module stops at once in `setUpClass` through `sys.exit(<one message>)`, exit 1. The message names the directories tried and says to set TMPDIR to a writable directory; there is no OSError traceback. No test is skipped or weakened. I could not reproduce a read-only filesystem here, so I simulated it by replacing `tempfile.mkdtemp` with a function that raises EROFS (see below).

### Outputs
Full unit tests (`TMPDIR=/home/azan/paper6_t6_work/audit_tmp python3 smoke_test/test_compare_smoke.py`); afterwards audit_tmp was empty and no files were left in smoke_test/:
```
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
Ran 18 tests in 4.357s

OK
```
Shell preflight test alone (`... test_compare_smoke.py T.test_shell_preflight_reference_governance`):
```
test_shell_preflight_reference_governance (__main__.T) ... ok
----------------------------------------------------------------------
Ran 1 test in 2.965s
OK
```
Direct run of the new preflight (scratch copy under audit_tmp, symmetric-only reference, GEN/FOAM_BASHRC dummies, removed afterwards):
```
preflight: compare mode needs both branch entries (deflected, symmetric) in /home/azan/paper6_t6_work/audit_tmp/tmp.p9RXnTk7P5/reference_result.json, but it holds: symmetric. Copy the shipped schema-2 reference_result.json here (WRITE_REFERENCE=1 adds or replaces one branch, reference machine only)
exit=2
```
Read-only sandbox simulation (every `tempfile.mkdtemp` raises EROFS; module run via runpy as `__main__`):
```
test_compare_smoke.py: no writable temporary directory, 0 tests run. Tried the system temp ['/tmp', '/var/tmp', '/usr/tmp', '/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26'] (Read-only file system) and the fallback /home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/fix26/smoke_test (Read-only file system). Set TMPDIR to a writable directory, e.g. TMPDIR=/path/to/writable/dir python3 test_compare_smoke.py
exit=1
```
(With `TMPDIR=/ro_sandbox_tmp` the list starts with `'/ro_sandbox_tmp'`.)

`bash -n smoke_test/run_smoke_test.sh` -> exit 0.

Real comparison (`python3 smoke_test/compare_smoke.py /home/azan/paper6_t6_work/smoke_ref smoke_test/reference_result.json`), exit 0:
```
  vs deflected branch (1.17392231e-06 m3/s, FFR 0.78396): Q +0.36870 %, FFR -0.001477
  vs symmetric branch (1.17825059e-06 m3/s, FFR 0.78248): Q +0.00000 %, FFR +0.000000
vs the returned Stage A A5 coarse value 1.17392231e-06: +0.36870 %   cells 198252 (reference 198252)   final-window bands: Q 1.19e-05 %, FFR 2.74e-08   wall None s
SMOKE TEST PASS (symmetric-jet branch; not the returned value, see SETUP.md section 4)
```
(The JSON metrics block printed before these lines is identical to Attempt 2.)

### Open points
- The coordinator still has to apply `README_line22_replacement.txt` to `code_from_cfd/README.md` line 22 and copy the fix26 files into `code_from_cfd/`.
- The read-only-sandbox behaviour was checked by simulation, not in the auditor's real sandbox.
