# FIX37 report: P5 pre-run audit findings 1, 2, 5, 6 (Opus 5.5 task 37, P5 builder/runner, attempt 1)

Scope: GPT-5.6 Sol audit `../audit_P5/SOL.md`, findings 1, 2, 5 and 6. Findings 3, 4 and 7 (scheduler and job script) belong to other agents. Gemini's `../audit_P5/AGY.md` is **empty**: the run failed on a DNS error (`AGY.err`), so it contains nothing to address.

Constraints followed:
- All edits are in `taskP5/`. Nothing in `p5/`, `m1/`, `taskC/` or the pool directories was modified, and `TASK_A_DESIGN.md` is unchanged.
- No solver ran on a real case. The only simpleFoam runs were on a 1,440-cell blockMesh stub (serial) and on the existing synthetic test (2 ranks).
- Everything ran niced with ≤ 2 threads, in the foreground. The ~9.5-minute geometry regression was a tool-tracked background job that I waited for.
- No process of mine is left, and the temp dirs were removed.

## 1. Changes

`taskC/` has not changed since `taskP5/` was copied from it. The diff `taskC → taskP5` is therefore exactly the list below; merge it file by file.

| file | change |
|---|---|
| `pf/pf_common.py` | **Lost-outlet handling in `write_case`.** An outlet patch with **0 faces** gets **no** `surfaceFieldValue` monitor and no `zerod_reference` entry. Its 0/p and 0/U entries stay: in resistance mode the coded BC, in prescribed mode `zeroGradient` p + `noSlip` U, because no flow can be imposed on an empty patch. build_info `outlets` lists only the outlets that have faces. `outlets_lost_in_mesh` records reason, R, bc_C target, flag and BCs written. `bc_bookkeeping` records the bc_C totals (in mesh, lost) and states the lost territory is **CLOSED**. New helpers: `lost_outlets(info)`, which falls back to `mesh_patches` nFaces 0 for cases built earlier; `live_outlets(info)`; `outlet_record`; `bc_bookkeeping`. If every outlet is lost, the builder refuses. |
| `pf/build_m1_case.py` | Passes `lost_reasons`, taken from the mesh stage: `mesh_gates.json` `patches_missing_or_empty` plus the `log.cartesianMesh` "unconnected regions" warning. Prints an `OUTLET_LOST_IN_MESH` line. |
| `pf/pf_roundtrip_build.py` | Derives R over the live outlets only and carries lost outlets through (bc_A R on the empty patch; plan entry flagged). |
| `pf/analyze_case.py` | Provenance and last-100 means cover the live outlets only. New keys: `outlets_lost_in_mesh` (Q 0, p `N/A`, flag), `bc_error_criteria_over_outlets`, `bc_bookkeeping`. A case built **before** this fix whose `zerod_reference` still contains a 0-face outlet is refused with "rebuild". |
| `pf/m1_results.py` | **M1_outlets:** a lost outlet is written as a row with `Q_mls 0`, p `N/A`, `closed 1`, `lost_in_mesh 1`, `flag OUTLET_LOST_IN_MESH` and R_source "not applied". New columns `lost_in_mesh` and `flag`. **M1_results:** new columns `flags`, `geometry_all_gates_pass_including_reported`, `D3_verdict`, `D4_verdict`, `D34_min_dist_throat_mm`, `D34_min_dist_measurement_mm`, `D34_checks_within_2mm`, `outlets_lost_in_mesh`. `flags` merges the fill json's flags with the build_info ones (relocation, lost outlet) and adds `NOT_CONVERGED` from the adjusted verdict / finished flag. When an outlet is lost, the notes carry the territory bookkeeping. |
| `pf/post_helpers.py` | **`fill`:** `geometry_step_ok` now follows the **decisive** gates. For a gates.json written before this fix, GATES is split minus `lesion_literal_absolute_r_target_check`. `geometry_all_gates_pass_including_reported` is written too. Decisive and reported-only failures are listed separately. **D3/D4:** read from `d34.json`, found by `--d34`, `$D34_JSON`, next to the mesh gates, `mesh_source_dir`, the hard-linked mesh dir, or `p5/mesh/<scan>`. **`manual_repair_needed`:** true only from a pipeline record (`manual_repair_needed` / `manual_repair` key in gates, mesh gates or build_info), with the source written. **Flags:** assembled in a fixed order (`FLAG_ORDER`, `NONE` if empty). `summary` writes `flags` and `outlets_lost_in_mesh` into `post_summary`. |
| `post_case_generic.sh` | Passes `${D34_JSON:+--d34 …}` to `fill`; header comment updated. |
| `p5/build_m1_geometry.py` (new copy) | `gate_bookkeeping()`: `GATES` is unchanged (same keys and values). Added `GATES_DECISIVE`, `GATES_REPORTED_NON_DECISIVE`, `ALL_GATES_PASS` (**decisive only**), `FAILED_GATES` (decisive), `ALL_GATES_PASS_INCLUDING_REPORTED`, `FAILED_GATES_INCLUDING_REPORTED`, `FAILED_REPORTED_GATES` and `GATES_BOOKKEEPING`. The status text names decisive and reported failures separately. A staging path fallback lets it run from `taskP5/p5/`; it is a no-op once installed in `p5/`. |
| `p5/summarise_p5.py` (new copy) | Reports `all_gates_pass_decisive` and `all_gates_pass_including_reported`. `failed_gates` is now decisive only, with the including-reported list beside it. Older gates.json files are split the same way. Staging fallback for inputs. |
| `tests/test_empty_patch_coded_bc.py` (new) | Real OpenFOAM test of a 0-face outlet (section 2). |
| `tests/test_flags_p5.py` (new) | Flags, decisive geometry and D3/D4 columns on the five real P5 cases (section 3). |
| `TEMPLATE_README.md` | New section on lost outlets, flags and decisive gates. |
| `test_output/fix37/` | Evidence (188 kB): test outputs, regression jsons, temp-rebuild files of 272. |

Flag vocabulary, in fixed order:
- **Geometry:** `GEOMETRY_GATES_MISSING`, `D2_RELATIVE_THROAT_GATE_FAIL`, `LESION_PURITY_GATE_FAIL`, `POSITIVE_CONTROL_UNDETECTED`, `SELF_INTERSECTION`, `GEOMETRY_GATE_FAIL:<gate>` (any other decisive gate).
- **D3/D4:** `D34_MISSING`, `D3_FAIL`, `D4_FAIL`.
- **Mesh:** `MESH_GATES_MISSING`, `CHECKMESH_STANDARD_FAIL`.
- **Case:** `MEASUREMENT_PROBE_RELOCATED`, `OUTLET_LOST_IN_MESH`, `MANUAL_REPAIR_NEEDED`.
- **Solve:** `NOT_CONVERGED`.

The reported-only absolute r_target check is deliberately **not** a flag (D10). It appears in `geometry_all_gates_pass_including_reported` and in the notes.

## 2. Finding 1 (BLOCKER, scan 272, `out_396` with 0 faces)

### 2a. Real tiny OpenFOAM test: `tests/test_empty_patch_coded_bc.py`, run twice, both PASS

Setup:
- blockMesh channel 10 × 1 × 1 mm, 40 × 6 × 6 cells. Patches: `inlet` and `out_1` with 36 faces each, `out_2` declared with no faces (nFaces 0), and `wall`.
- The case was built by the production `pf_common.write_case` with the audited coded resistance BC on **both** outlets.
- simpleFoam ran serially for 2 iterations.

Output, identical in both runs apart from temp names:
```
blockMesh boundary: {'inlet': {'type': 'patch', 'nFaces': 36}, 'out_1': {'type': 'patch', 'nFaces': 36}, 'out_2': {'type': 'patch', 'nFaces': 0}, 'wall': {'type': 'wall', 'nFaces': 960}}
NEGATIVE CONTROL (old monitors on the 0-face patch): simpleFoam rc=1; FATAL excerpt:
FOAM FATAL ERROR: (openfoam-2406 patch=260127)
surfaceFieldValue out_2Flux: patch(out_2):
    The patches: (out_2)
    resulted in 0 faces
    From void Foam::functionObjects::fieldValues::surfaceFieldValue::setPatchFaces()
    in file fieldValues/surfaceFieldValue/surfaceFieldValue.C at line 388.
simpleFoam (fixed case) rc=0, log tail: ... out_1Flux sum(out_1) of phi = 1.2281236e-06 ... areaAverage(out_1) of p = 6.7757992 ... End
dynamicCode: 'Using dynamicCode for patch out_2 on field p ...', 'Creating new library in "dynamicCode/res2/..."', 'wmake libso .../dynamicCode/res2'   (res1 likewise)
M1_outlets rows:
   {'outlet_id': 'out_1', 'Q_mls': '1.13695...', 'Q_target_bcC_mls': '0.5', 'p_bar_Pa': '7104.8357226', 'closed': '0', 'lost_in_mesh': '0', 'flag': '', 'R_source': 'bc_A.csv'}
   {'outlet_id': 'out_2', 'Q_mls': '0.0', 'Q_target_bcC_mls': '0.2', 'p_bar_Pa': 'N/A', 'closed': '1', 'lost_in_mesh': '1', 'flag': 'OUTLET_LOST_IN_MESH', 'R_source': 'bc_A.csv on a 0-face patch: NOT applied (no flow)'}
M1_results flags: OUTLET_LOST_IN_MESH;NOT_CONVERGED | outlets_lost_in_mesh: out_2 | converged: UNCONVERGED
PASS: 0-face outlet patch: coded BC accepted on the empty patch (2 serial simpleFoam iterations, End), its monitors omitted (they are fatal: negative control), post path reports Q 0 / p N/A / OUTLET_LOST_IN_MESH
```

What this shows:
- **Sol's claim is confirmed:** the old monitors on the empty patch are fatal in v2406 (surfaceFieldValue.C:388).
- **The coded BC on the empty patch is harmless:** it compiles, is constructed, and the run ends with `End`.
- **The analysis behaves as specified:** criteria cover `out_1` only, and the lost outlet is reported as Q 0, p `N/A`, flagged.

Full outputs: `test_output/fix37/empty_patch_run{1,2}.txt`.

### 2b. Real 272 rebuilt into a temp dir (not `p5/cases/272_resistance`)

The rebuild used `build_m1_case.py … p5/mesh/272 resistance taskP5/tmp37/272_resistance 8 --extensions-json p5/out/272_extensions.json`, with the full mesh check: 40 s, 2.2 GB RSS, rc 0. Printed:
```
OUTLET_LOST_IN_MESH out_396 (0 faces): no monitors written, BC entries kept (inert); territory closed (bc_C 0.50687 mL/s not delivered). Reason: outlet patch has 0 faces in the polyMesh (the mesher removed
the region holding it); mesh stage mesh_gates.json: patches_missing_or_empty=['out_396'], GATES_PASS=False; log.cartesianMesh: '--> FOAM Warning : Mesh has 2 unconnected regions'
built ... outlets ['out_279', 'out_620'], ranks 8, mesh hard-linked, E0 MEMBER, probe planes: throat CHECKED_ON_MESH h=3.149 mm, measurement CHECKED_ON_MESH (strict single-lumen rule PASS) h=3.107 mm; probe used p009
```

Compared with the real case:
- **controlDict:** the only difference is the removal of the `out_396Flux` / `out_396Pressure` blocks. `out_396` appears 0 times in the new file and 4 times in the real one. foamDictionary parses the functions: `inletFlux inletPressure out_279Flux out_279Pressure out_620Flux out_620Pressure throatFlux throatP measurementFlux measurementP`.
- **Byte-identical:** `0/p` (the `res396` coded BC is kept), `0/U`, `fvSchemes`, `fvSolution`, `decomposeParDict` and `transportProperties`.
- **zerod_reference:** the only difference is that the `out_396` entry is gone.
- **build_info:**
  - `outlets` is out_279 and out_620; their entries equal the old ones, plus tree_node / territory_id / p_init_kin.
  - `outlets_lost_in_mesh` holds out_396.
  - `bc_bookkeeping`: bc_C total 1.60901 mL/s, of which 1.10214 mL/s are in the mesh and 0.50687 mL/s are lost; the territory is closed.
  - The probe planes and their checks are identical.
- The temp case was removed afterwards. The mesh link count went back from 3 to 2.
- Evidence: `test_output/fix37/rebuild_272_temp/`, holding controlDict, build_info, zerod_reference, 0_p and the two diffs.

## 3. Findings 5 and 6 (flags) and finding 2 in the results row: `tests/test_flags_p5.py`, run twice, both PASS

This test is read-only on the real P5 inputs:
- `post_helpers.py fill` runs on `p5/cases/<scan>_resistance/build_info.json`.
- It discovers `p5/out/<scan>/gates.json`, `p5/mesh/<scan>/mesh_gates.json` and `p5/mesh/<scan>/d34.json` automatically.
- Run 1 also included the new temp rebuild of 272.

The results reproduce the brief's expected flag sets exactly:

| scan | flags (M1_results `flags`) | geometry_step_ok (decisive) / incl. reported | D3 / D4 | nearest strict-checkMesh entity: throat / measurement (mm) |
|---|---|---|---|---|
| 138 | `D3_FAIL;D4_FAIL;CHECKMESH_STANDARD_FAIL` | **True** / False (the absolute check is its only failed gate) | FAIL / FAIL | 0.448 / 1.018 (lowQualityTetFaces) |
| 69 | `LESION_PURITY_GATE_FAIL;POSITIVE_CONTROL_UNDETECTED` | False / False | PASS / PASS | 2.596 / 2.040 |
| 473 | `D2_RELATIVE_THROAT_GATE_FAIL;D3_FAIL;D4_FAIL;MEASUREMENT_PROBE_RELOCATED` | False / False | FAIL / FAIL | 1.319 / 1.070 (to the package probe p011) |
| 272 (real case, old build_info, via the `mesh_patches` fallback) | `SELF_INTERSECTION;D3_FAIL;D4_FAIL;OUTLET_LOST_IN_MESH` | False / False | FAIL / FAIL | 0.831 / 2.013 |
| 272 (temp rebuild, `outlets_lost_in_mesh` record) | same | same | same | same |
| 139 | `D2_RELATIVE_THROAT_GATE_FAIL;D3_FAIL;D4_FAIL` | False / False | FAIL / FAIL | 1.549 / 1.793 |

- `manual_repair_needed` is False for all five, with the source "no manual-repair record in gates.json, mesh_gates.json, build_info.json".
- For every case the reported-only failure is `lesion_literal_absolute_r_target_check`.
- The merge `m1_results.py` applies to an unconverged solve appends `;NOT_CONVERGED`, which the test checks for every case.
- The full M1_results path, including `NOT_CONVERGED` and `OUTLET_LOST_IN_MESH`, is exercised end to end in 2a.
- Outputs: `test_output/fix37/flags_p5_run{1,2}.txt`.

## 4. Finding 2 (D10): geometry builder regression on scan 14, run once, niced

`taskP5/p5/build_m1_geometry.py 14_left_LAD_prox_20mm_80ds__baseline__real` ran in 570 s with rc 0.

| comparison | leaves compared | different | detail |
|---|---|---|---|
| vs `m1/out/baseline/gates.json` (compare_regression.py) | **1381** | 5 | the same 5 `mask_edit/*shipped*` fields that are `None` by design, as in P5_BUILD_REPORT §2; nothing new |
| vs the previous `p5/out/14_regression/gates.json` | 1402 | **0** | — |

- `only_in_new`: just the new bookkeeping keys (`GATES_DECISIVE/*`, `GATES_REPORTED_NON_DECISIVE/*`, `ALL_GATES_PASS_INCLUDING_REPORTED`).
- `case.stl` is byte-identical to both references (sha256 22e22e49e390…), and the radius csv is identical.
- The new gate fields for scan 14:
  - `ALL_GATES_PASS` False, because the decisive `surfaceCheck_not_self_intersecting` fails, so the value is unchanged for 14.
  - `ALL_GATES_PASS_INCLUDING_REPORTED` False.
  - `FAILED_GATES` = [surfaceCheck_not_self_intersecting].
  - `FAILED_REPORTED_GATES` = [lesion_literal_absolute_r_target_check].
  - Status: "DONE: decisive gates FAILED: surfaceCheck_not_self_intersecting; reported (non-decisive) check failed: lesion_literal_absolute_r_target_check".
- Evidence: `test_output/fix37/regression_14/`, holding gates.json, regression_vs_m1.json, regression_vs_p5_14.json and the log. The 628 MB output dir was removed.

The five real P5 gates.json files were **not** regenerated; that would mean re-running the builder on real cases. `post_helpers` and `summarise_p5.py` split them by the same rule. With the copy, `summarise_p5.py` gives decisive PASS for 138 and FAIL for 69, 473, 272 and 139, with "including reported" FAIL for all five.

## 5. Existing tests re-run with the changed code

| test | result |
|---|---|
| `tests/test_post_case_generic.sh` | **PASS** (synthetic solve, 2 ranks, guards (a) to (i)). Its M1_results row now carries `flags = GEOMETRY_GATES_MISSING;D34_MISSING;MEASUREMENT_PROBE_RELOCATED`: the synthetic case has no gates or d34 files, and its probe was relocated. |
| `tests/test_p5_stub.py` | PASS (all five packages) |
| `tests/test_post_guards.py` | PASS |
| `tests/test_b1_settle.py` | PASS |

Outputs are in `test_output/fix37/`. `test_section_rule.py` and the flow-state tests were not re-run: `probe_sections.py`, `sections.py` and `flow_state_profile.py` are unchanged. All Python files compile and `bash -n post_case_generic.sh` is OK. `__pycache__` was removed and the manifest was regenerated (`make_manifest.sh`). `verify_manifest.sh` passes all 121 entries. Plain `sha256sum -c` reports 12 test-output CSVs as FAILED: Python's csv module writes CRLF line endings. This behaviour predates this fix (the flow_state_sten70 CSVs already had it), and `MANIFEST.README` lists those files.

## 6. Open points

1. **Rebuild the real `p5/cases/272_resistance` after the merge.** It still contains the fatal `out_396` monitors, and the fixed `analyze_case` refuses it until rebuilt. Use the same command as the original build with the **absolute** `--extensions-json /home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/out/272_extensions.json`. My temp rebuild used a relative path; `post_helpers.find_gates` opens that path as recorded, so a relative path only works from the pilot root. The other four cases need no rebuild: they have no lost outlet, and their controlDicts are unchanged by this fix.
2. **The empty-patch BC was tested serially only**, as the brief asked. In the 8-rank decomposition `out_396` is empty on every rank. The coded BC's `gSum` is a collective that every rank calls, so the result is consistent. The 272 smoke is the first parallel test.
3. **473 D3/D4 distance is measured to a different probe than the one monitored.** `d34.json` measures it to the package probe p011, but `measurementP` uses the relocated `p011_reloc`. The fill notes say so; no D3/D4 distance to the relocated probe was computed (that would need d34_generic on the real mesh, not in scope).
4. **Two measurement distances are close to the limit:** 69 at 2.040 mm and 272 at 2.013 mm, both above the 2 mm limit, so both PASS on that probe. They are reported as measured.
5. **Prescribed mode with a lost outlet** (`zeroGradient` p + `noSlip` U, no flow imposed) is written and the code path compiles, but no solver run covered it. P5 is resistance only.
6. The new copies `taskP5/p5/build_m1_geometry.py` and `summarise_p5.py` replace the `p5/` originals on merge. I did not create a `P5_summary.json` in staging.
7. Gemini audit: `AGY.md` is empty (run failed), so there is nothing further to address. Sol findings 3, 4 and 7 are out of scope here.
