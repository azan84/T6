# FIX30 report: Task C production template with the D8 probe function objects (Opus 5.5 task 30)

All work is in `taskC/`; nothing has been installed. Each file changed is a copy from `../pf/` or `../b1_settle.py`. No mesh or field was written to Drive. The test case `/home/azan/paper6_t6_work/taskC_test` was removed afterwards, and no background process is left. All runs used nice -n 10 and ≤ 4 threads/ranks.

## 1. Changes
- **`pf/probe_sections.py` (new).** Bounded probe planes. It sizes the box from the centreline, runs the pyvista mesh check (rules in the module docstring and in TEMPLATE_README) and computes the infinite-plane diagnostic.
  - `bounds` is confirmed in ESI v2406 by reading the source:
    - `src/sampling/sampledSurface/sampledPlane/sampledPlane.H` lists `bounds | limit with bounding box`;
    - `sampledPlane.C` has `bounds_(dict.getOrDefault("bounds", boundBox::null()))`;
    - `src/sampling/surface/cutting/cuttingSurfaceBaseSelection.C` selects only cells with `userBounds.contains(cellCentre)`.
  - The keyword is also confirmed by the run: the area the monitor sampled equals the bounded pyvista section, not the unbounded one (section 2).
- **`pf/pf_common.py`.**
  - `monitors(outlets, throat_plane, measurement_plane)` writes `measurementFlux`/`measurementP` next to `throatFlux`/`throatP`. All four use `writeInterval 1` and `writeArea true` and accept bounds.
  - `write_case(..., measurement_plane=)` records both planes with their bounds in build_info.
  - `series()` and the new `value_column()` take the value column from the `.dat` header. With `writeArea` the value moves to column 2; column 1 would have been the Area.
- **`pf/build_m1_case.py`.**
  - Builds both planes from the package and runs the mesh check on the given polyMesh. It **refuses** if the check fails, and refuses an existing outdir before any work.
  - Records `probe_section_check`, `measurement_probe` and `production_ready` in build_info.
  - `--no-mesh-check` is for stub tests only and writes `NOT_FOR_PRODUCTION`.
  - Docstring updated for any package of the format.
- **`pf/m1_package.py`.**
  - `measurement_plane()` and `probe_row()`. The measurement row must match `meta.json` `measurement.tree_node`.
  - Package lookup also searches Drive `packages/M1` and `packages/P5` (read-only, kB files), or accepts a package path.
- **`pf/pf_roundtrip_build.py`.** Inherits both bounded planes and `probe_section_check` from the prescribed case. It warns in build_info if a pre-D8 case has unbounded planes.
- **`b1_settle.py`.**
  - The SETTLED rule runs on `measurementP` when that monitor exists (`b1_label` B1 / `B1 (D8 prescribed-flow variant)`); otherwise the row stays `PROXY_NOT_B1`.
  - 800-iteration floor for prescribed-flow solves (`iter_first_settled_floored`, `iter_permanently_settled_floored`).
  - `stop_recommendation` always reads "RUN THE FULL BUDGET". For B1 rows it adds the iteration at which the rule would stop, marked "not applied".
  - New `--case DIR[:PROXY_OUTLET[:MODE]]` mode for arbitrary (P5) cases.
  - Columns renamed from `FFR_proxy_*` to `FFR_mon_*`.
- **`make_manifest.sh`, `verify_manifest.sh`.** Manifest scripts (section 5).
- **`TEMPLATE_README.md`, `tests/`, `test_output/taskC_test_5iter/`.** The last holds the kB evidence of the real run: monitors, controlDict, build_info and logs.

## 2. Test on the rebuilt scan-14 baseline (real solve)
- **Build.** `build_m1_case.py 14_left_LAD_prox_20mm_80ds__baseline__real m1/cases/baseline_resistance resistance /home/azan/paper6_t6_work/taskC_test 4 --extensions-json m1/out_returns/extensions_baseline.json`
  - The mesh was hard-linked.
  - Identical to the original case: `0/p`, `0/U`, `fvSchemes`, `fvSolution` and `transportProperties` byte for byte, and build_info except for the new keys and nproc.
  - `controlDict` differs only by the bounds lines, `writeArea` and the two new measurement monitors.
- **Mesh check, on the first box tried for both probes:**

| probe | h (mm) | bounded section (pyvista) | / π r_own² | centroid off / r_eq | other components in box | infinite plane (09-26 monitors) |
|---|---|---|---|---|---|---|
| throat p004 | 2.306 | 0.23886 mm² (r_eq 0.2757 mm) | 1.43 (r_target 0.2306 mm) | 0.14 | none (own margin 80 cells) | **4 components, 8.351 mm²** |
| measurement p011 | 1.859 | 3.36956 mm² (r_eq 1.0356 mm) | 1.25 (r 0.926 mm) | 0.09 | none (nearest other cut cell 31 cells outside) | **2 components, 5.309 mm²** |

  So the throat plane had the same defect as the measurement plane: it lies on a straight LAD segment, but the infinite plane also met the centreline at 15 other places. Both planes are now bounded.
- **Run.**
  - `decomposePar` to 4 ranks took 66 s, then `mpirun -np 4 simpleFoam -parallel` ran with endTime set to 5 in the test copy only. Total 33 s wall, including loading the coded BCs; the log ends with `End`.
  - Every monitor wrote one row per iteration, 1 to 5.
- **Values** (kinematic p; the ratio is p·1060/11998.98):

| iteration | measurementP | ratio | throatP | ratio | out_600 p | inlet p |
|---|---|---|---|---|---|---|
| 1 | 8.69078 | 0.7678 | 10.11108 | 0.8932 | 8.46193 | 11.31979 |
| 2 | 6.99826 | 0.6182 | 9.34445 | 0.8255 | 8.44587 | 11.31979 |
| 3 | 7.48970 | 0.6616 | 9.56860 | 0.8453 | 8.42999 | 11.31978 |
| 4 | 8.74604 | 0.7726 | 10.14091 | 0.8959 | 8.41436 | 11.31974 |
| 5 | 9.18969 | 0.8118 | 10.33639 | 0.9131 | 8.39906 | 11.31968 |

  - Area column: measurementP 3.36955342e-6 m² and throatP 2.38863110e-7 m² at every iteration. These equal the pyvista bounded sections (3.36956 / 0.23886 mm²) to 6 digits. The 09-26 returned measurement section was 3.3695557 mm².
  - Through-section flux at iteration 5: measurement 5.93e-9 m³/s, throat 2.94e-8 m³/s. The flow is still building up.
  - The values are sane for 5 iterations from a uniform-p start: P_v < p < P_aorta, ordered inlet > throat > measurement. They are not converged. For comparison, the converged 3000-iteration solve of 09-26 gave 0.8698 at the measurement section.
- The test case was removed afterwards. The link count on the original mesh went back from 3 to 2, and no mpirun/simpleFoam process is left.

## 3. B1/D8 analysis
`tests/test_b1_settle.py` runs three synthetic cases (with the Area column) through the `--case` CLI. Result: **PASS**.

| case | b1_label | first settled | floored | stop recommendation |
|---|---|---|---|---|
| resistance with measurementP | B1 | 546 | 546 | full budget; rule would stop at 546 (not applied) |
| prescribed with measurementP | B1 (D8 prescribed-flow variant) | 500 | 800 | full budget; would stop at 800 (not applied) |
| prescribed, proxy only | PROXY_NOT_B1 | — | — | full budget |

The FFR at the end is 0.85 exactly, which shows the Area column was not read as the value. The retained 09-26 solves are not on this host, so this script was not re-run against the returned `settle_iterations.csv`.

## 4. Package-driven / P5
- **`tests/test_p5_stub.py`** builds the case files for all five P5 packages against a stub polyMesh (`--no-mesh-check`). Result: **PASS**. For each package:
  - E0 MEMBER;
  - patches equal the package outlet_ids, with a coded resistance BC and inletOutlet per outlet;
  - 4 bounded plane monitors, and `foamDictionary` parses `functions` and `measurementP/.../bounds`;
  - a stub with the wrong patch list is refused.
- **Box half-widths from the centreline** (h in mm, then the number of other crossings of the infinite plane):

| package | measurement probe | throat probe |
|---|---|---|
| 138 | p010: 2.105, 11 | p004: 2.684, 17 |
| 139 | p009: 2.023, 12 | p004: 2.032, 6 |
| 272 | p009: 3.107, 0 | p004: 3.149, 16 |
| 473 | p011: 2.375 (= h_min), 15 | p004: 3.016, 10 |
| 69 | p012: 1.767, 10 | p004: 2.975, 0 |

  The mesh check of these boxes can only run once the P5 meshes exist.
- **Scan-14 assumptions checked:**
  - patch names come from the package and closed outlets from bc_A (none in P5);
  - the E0 guard reads scan and side from meta.json;
  - exactly one throat and one measurement probe exist in every P5 package;
  - the centreline graph (root 0, single parents) and tree_node lookup work for all five;
  - fluid constants are identical;
  - the `T1_missed_branch` PILOT label is harmless for P5.

## 5. Manifest
- `make_manifest.sh <dir>` writes:
  - `MANIFEST.sha256`: sorted `hash  path` lines with no `#` lines;
  - `MANIFEST.README`: the statement of the rule. Text files (no NUL byte) are hashed with every CR removed, binary files raw. It also lists any text file that contains CR bytes on the writing machine.
- `verify_manifest.sh <dir>` applies the same rule. It skips `#` and blank lines, ignores CR in the manifest, reports MISSING/FAILED and lists extra files, and exits non-zero on any failure. It uses `shasum -a 256` if `sha256sum` is not installed (macOS).
- `tests/test_manifest.sh`: **PASS**.
  - On an LF copy, both plain `sha256sum -c` and verify pass.
  - On a CRLF copy, with the manifest itself converted too, verify passes. Plain `sha256sum -c` fails there, as expected.
  - A tampered file fails.
- `taskC/MANIFEST.sha256` and `MANIFEST.README` were generated over this folder as a demonstration.

## 6. Open points
1. **P5 473 measurement probe.** p011, tree_node 642, sits on the first node of a daughter branch, right at a bifurcation (bif_prox p010 at 47.0 mm, bif_dist p012 at 52.2 mm). Its normal is 45° off the centreline tangent (|cos| 0.71), and r_target 1.13 mm is larger than r_ref 0.87 mm. The box comes out at h_min. The mesh check may refuse this probe once the mesh exists, and a section there is not a clean single-vessel section. This is a package question for the analysis side; the builder will not move the probe.
2. **Unbounded planes in returned data.** `throatP`/`throatFlux` of every 09-26 scan-14 solve came from the infinite plane: 4 sections, 35 × the lumen area at the throat. `b1_settle.py` flags them via `throat_plane_bounded = False`. `m1_results.py` already takes Re_throat from the probes CSV, not from the monitor, so it is unaffected; its docstring still describes the old plane.
3. **End-to-end runner not changed.** The work order mentions it, but this brief did not include it. `m1/post_case.sh` is scan-14 specific: it hard-codes `P=/tmp/claude-1000/...`, which no longer exists here, and the package name pattern. P5 needs a runner that calls `build_m1_case.py` with `--pkg-root packages/P5` and the as-built extension JSON from the geometry stage. Without that JSON the R_own relaxation falls back to the flagged 3 D default.
4. **Box check tolerance.** The mesh check uses pyvista point-mean cell centres, while OpenFOAM selects by cell centroid. This is covered by the 0.5-cell margins, and on scan 14 the margins were 8 to 80 cells.
5. **Code not pushed.** Push to `code_from_cfd/` and regenerate the manifest with `make_manifest.sh` after the audits; the coordinator does this.

---

# Attempt 2 (Opus 5.5 task 33): audit findings of `../audit_AC/SOL.md` (C: 1, 2, 3; A: 5, 7, 8) and `../audit_AC/AGY.md`

All work is in `taskC/`. `taskC_a1_snapshot/`, `p5/`, `m1/` and the package files were not modified. Nothing was installed.
- **Host etiquette.** Everything ran with nice -n 10 and ≤ 2 threads (synthetic solve: 2 ranks).
- **No solver on a real case.** The only solve was the synthetic 41k-cell test tube below.
- **Clean up.** No process is left, and the test root `/home/azan/paper6_t6_work/taskC_post_test` was removed.
- **Live Task A solve not touched.** `m1/cases/baseline_D7_12p5_resistance` had a running 16-rank solve (Time 273 when I looked). I only read its `build_info.json`, `log.decomposePar` and the owner header.

## A2.1 Changes
**`post_case_generic.sh` (new; Sol C1 BLOCKER, Sol A5 BLOCKER, AGY 2)**
- End-to-end post-solve runner for any Gate-M1-format package. Usage: `post_case_generic.sh <case_dir> <package_dir_or_name> <label> <mode> <out_dir>`.
- No scan-14 assumption and no `/tmp/claude…` root. P comes from `$P`, default `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot`. Helpers come from `<script dir>/pf`, else `$P/pf`. Packages come from `$PKG_ROOT` or the package lookup.
- Steps, each logged to `<out>/post_<label>_<mode>.log`; it stops at the first failure:
  1. **Finished check.** An exact `End` line in `log.simpleFoam`.
  2. **`analyze_case.py`** (strict checks). The verdict is reported, not a stop; `POST_REQUIRE_CONVERGED=1` makes it one.
  3. **`reconstructPar -latestTime`**, then the **reconstruction check**: the latest reconstructed time equals processor0's latest, U and p are non-empty, and `log.reconstructPar` ends with End. It runs **before anything else**. Fields are kept, and **processor directories are never removed** by the runner.
  4. **`M1_probes`.**
  5. **`as_meshed_radius`**: detail file plus the two contract files, area-equivalent and inscribed, in the format of `returns/2026-09-26/as_meshed_radius_baseline*.csv`.
  6. **Generic fill json.** Gate discovery is recorded with its source.
  7. **`M1_outlets` + `M1_results` row.** The notes state the measurement probe used.
  8. **Measurement-probe history.** Every iteration of measurementP/Flux, throatP/Flux and measurementOrig*, plus a cross-check against the reconstructed section; an area difference > 0.5 % is flagged `AREA MISMATCH`. Then `b1_settle.py --case`.
  9. **`flow_state_profile.py`.**
  10. **`post_summary_*.json`**: verdict, wall clock, cells, peak RAM when available (`PEAK_RAM_GB` or a `MEMLOG` sampler), probe used, sha256 of every output.
      - With `REF_FFR` set it adds the Sol A7 comparison, like with like: p_over_Paorta of the package `measurement` row of `M1_probes` (reconstructed final fields) − REF_FFR, against |ΔFFR| < `REF_TOL` (default 0.00055).
      - The measurementP last-100 mean is reported next to it for B1 and is not used.
      - For Task A: `REF_FFR=0.8697574904997768`.
- **Idempotent.** A second run reuses a verified reconstruction, the radius files and the provenance-checked analysis.

**`pf/post_helpers.py` (new).**
- The runner's helpers.
- `cells` falls back to the per-processor counts of `log.decomposePar`, because cfMesh owner files carry no nCells note. Checked on the D7 case: 6,241,438.
- **Fill-json discovery, tested read-only on `m1/cases/baseline_D7_12p5_resistance`:**
  - It found `m1/mesh/baseline_D7_12p5/mesh_gates.json` through the hard-linked owner inode.
  - It found `m1/out/baseline/gates.json` through the build's extension json.

**Copies of `pf/` scripts (generalised).**
- `analyze_case.py`: finds `analyze_solve.py` via `$P`, the pf parent, the taskC parent or the default.
- `m1_probes.py`: an extra row of kind `measurement_relocated` when build_info records a relocation. The package row stays.
- `as_meshed_radius.py`: `--contract PREFIX`.
- `m1_results.py`:
  - "measurement probe USED: …" note;
  - `--physical-cores` / `$PHYSICAL_CORES`, default 16;
  - docstring no longer calls the D8 planes infinite.
- `sections.py`: `Sectioner(robust=True)` for the diagnostic (see A2.3). The default method is unchanged, so the returned 09-26 probe values stay comparable.
- `e0_check.py`: copied (AGY 4).

**`flow_state_profile.py` (new; Sol A8, AGY 3).**
- Implements the TASK_A_DESIGN diagnostic exactly; the design was not changed.
  - **Sections.** Every 1 mm from throat + 2 mm to the measurement probe, along the lesion-vessel centreline (root → measurement node; the throat node must lie on it). Each section is bounded, connected and normal to the local tangent.
  - **Per section.** r_eq and the flux-weighted axial-velocity centroid offset from the area centroid over r_eq. The offset is signed in a rotation-minimising (normal, binormal) frame. That frame depends only on the centreline, so two solves of one package share it.
- **`compare`** applies the pre-registered rule: STATES AGREE iff max |o_A − o_B| ≤ 0.03 (vector difference) and |FFR_A − FFR_B| < 0.00055; otherwise STATES DIFFER.
- Straight tubes use `--straight-x`.

**`pf/probe_sections.py` + `pf/build_m1_case.py`: strict measurement-section rule (Sol C2, AGY 6).**
- **Rules:**
  - S1: normal within 20° of the tangent;
  - S2: every node within 1.5 r_ref along the vessel path has degree 2;
  - S3: the attempt-1 mesh check (one component, …);
  - S4: 1/1.6 ≤ A/(π r_ref²) ≤ 1.6.
- **Threshold justification**, also in the module docstring:
  - Scan 14 has a measurement section of 1.25 × π r_own², and the as-meshed lumen is about 20 % wider than the package radius, i.e. ×1.44 in area. 1.6 leaves 11 % above that.
  - 1.6 rejects a two-vessel cut (≥ about 2×) and a 45° oblique cut of the widened lumen (1.44/cos 45° = 2.0).
  - 20° keeps the oblique-cut area excess below 6.4 %.
- **Failure handling.** A package probe that fails is recorded `FAILED_SECTION_RULE`, never silently accepted. It is relocated deterministically:
  - the nearest node of the same vessel path within 3 mm of arc that passes S1–S4 (ties distal), normal = local tangent;
  - `measurementP` = the relocated plane;
  - `measurementOrigP` = the package plane, written only if its bounded section passes the mesh check;
  - build_info gets `measurement_section_rule`, `measurement_probe_relocated` (original + relocated + rejected candidates), `measurement_probe_used` and `mesh_source_dir`.
  - With no valid node within 3 mm, the builder refuses.
- **Supporting changes:**
  - `pf_common.monitors/write_case(extra_planes=…)`;
  - `pf_roundtrip_build` inherits the extra plane and the new keys.
- **Throat:** lenient rule as before; the S1/S2 values are recorded only.

**Bugs found by the new tests and fixed.**
- `m1_package.terminal_R_own` raised KeyError when an outlet's terminal segment reaches the root, i.e. a single-vessel tree. The P5/M1 packages are not affected.
- `build_m1_case.py main()` crashed printing the new string entry of `probe_section_check`.

**Manifest (Sol C3, AGY 5).**
- `make_manifest.sh`/`verify_manifest.sh` exclude `__pycache__/`, `*.pyc` and `.git/`. `test_manifest.sh` covers this.
- All `__pycache__` was removed from taskC/ and the manifest regenerated (A2.4).

## A2.2 Test output
1. **`tests/test_section_rule.py`: PASS** (`test_output/section_rule_test.txt`).

   A. Centreline only, measurement probe:

   | package | probe | angle to tangent | nearest non-degree-2 node | result |
   |---|---|---|---|---|
   | 138 | p010 | 4.0° | −13.1 mm | PASS |
   | 139 | p009 | 2.6° | root | PASS |
   | 272 | p009 | 9.6° | root | PASS |
   | 69 | p012 | 10.2° | −19.7 mm | PASS |
   | scan 14 | p011 | 7.4° | −6.92 mm | PASS |
   | **473** | **p011** | **36.6°** | **−0.84 mm** (node 424, degree 3; limit 1.30 mm) | **FAILED_SECTION_RULE** |

   473 is relocated to **tree_node 646 at +2.853 mm**. Rejected before it:
   - 643/644/645 (+0.66/+1.38/+2.11 mm): the sibling vessel is too close for a box;
   - 424/423/422: S2.

   Without a mesh there is no original monitor.

   B. On the real scan-14 mesh (`m1/mesh/baseline_v2`, 3,657,147 cells, read only):
   - p011 passes S1–S4: 3.36956 mm² = 1.241 × π r_ref², one component.
   - A **temp copy** of the package, with p011 moved to node 161 just distal of bifurcation 116 and tilted 25°:
     - FAILED_SECTION_RULE (S1, S2 and the box);
     - relocated to node 163 (+0.855 mm), mesh-checked, 3.49178 mm² = 1.286 × π r_ref²;
     - its own bounded plane is not valid, so no original monitor.
2. **`tests/test_p5_stub.py`: PASS** (`test_output/p5_stub_test.txt`). It now also asserts:
   - the 473 relocation, with no `measurementOrigP` without a mesh;
   - PASS + package probe for the other four.
3. **`tests/test_flow_state_profile.py` (analytic): PASS** (`test_output/flow_state_analytic_test.txt`).
   - Imposed axial profile u = U0(1 + a g·r/R) on a structured tube; the expected value is offset/r_eq = a/4 along g.
   - a = 0.4: measured 0.09991 against 0.1, on the x tube (direction 30° reproduced) and on an oblique tube via the polyline interface (frame-independent check).
   - a = 0: 0.
   - compare: identical profiles → AGREE (0); a = 0.4 vs 0 → DIFFER (0.0999); a = 0.4 vs 0.32 → AGREE (0.0200); profile agreeing but FFR apart → DIFFER.
4. **`tests/test_flow_state_sten70.sh`: PASS** (`test_output/flow_state_sten70/`). The x axis is the centreline, throat 30 mm, measurement 56.5 mm, 26 stations.

   | case | max offset/r_eq | valid stations |
   |---|---|---|
   | u3d `case_S50` | 0.0004 | 25/26 |
   | `smoke_cont` | 0.0026 | 26/26 |
   | `a5_arch8` | **0.364** at throat + 10 mm, direction persistence 1.00 | 26/26 |

   Comparisons:
   - smoke_cont vs S50: **STATES AGREE** (0.0026).
   - a5_arch8 vs S50: **STATES DIFFER** (0.364).
   - a5_arch8 vs smoke_cont with the B3 FFRs 0.78397/0.78248: **STATES DIFFER** (0.362; |ΔFFR| 0.00149).

   So the diagnostic separates the deflected from the axisymmetric branch on the same geometry.

   One S50 station (x = 52 mm) is a cut through a band of cfMesh transition polyhedra. The VTK section there has 5 holes, 8.8 % of its area, with through-flux +1.8 %. The cells' own cuts are complete, so this is a VTK representation/cut defect of those polyhedra. Before the hole rule, the station gave a false 0.035 offset. The diagnostic now marks such sections invalid (holes ≥ 0.5 % of the filled area, measured by rasterising), and `compare` excludes them and lists them.
5. **`tests/test_post_case_generic.sh`: PASS** (`test_output/post_case_generic_synthetic/`, incl. `test_run_stdout.txt`).
   - **Set-up.** Synthetic stenosed tube package with the measurement normal tilted 30°, a 40,740-cell blockMesh, and the production builder with mesh checks. The builder relocated p004 → node 33 (+0.5 mm) and kept `measurementOrigP`.
   - **Solve.** 1000 iterations on 2 ranks, 171 s.
   - **Refusal.** The runner refused before the solve, with no End line.
   - **Run.** It then ran end to end:
     - CONVERGED;
     - reconstruction verified;
     - probes csv with the relocated row;
     - contract radius files (39/41 covered: the inlet and outlet nodes are on the end caps);
     - results row with "measurement probe USED: p004_reloc (RELOCATED …)";
     - history of 1000 iterations for all 6 plane monitors;
     - monitor vs reconstructed section: measurementP 0.979376 / 0.979376, measurementOrigP 0.979591 / 0.979591, throatP agrees; area OK;
     - B1 first settled at 527;
     - flow-state max offset 3e-10;
     - summary with 12 hashed outputs;
     - REF_FFR comparison present (test value 0.9796: p004 0.9795912, ΔFFR −8.8e-6).
   - **Second run.** It reused the reconstruction, the radius files and the analysis.
   - **Processor directories** were kept.
   - **Area-flag demonstration** (`area_flag_demo_nx100_history.json`). In a first run with 100 axial cells the probe planes lay exactly on a layer of mesh faces. The OpenFOAM sampledPlane monitors then reported areas 8.3 % (measurement, 3.388 against 3.129 mm²) and 8.3 % (throat) too large, and the cross-check flagged both `AREA MISMATCH`. The test mesh now uses 97 cells.
6. **Unit and syntax checks.**
   - `tests/test_b1_settle.py`: PASS.
   - `tests/test_manifest.sh`: PASS, now including the exclusions.
   - `bash -n` on every .sh: OK.
   - ast parse of every .py: OK.

## A2.3 Open points
1. **The real test of the runner is the coordinator's first Task A solve.**
   - Run it after that solve ends, one case at a time. Field loading of a 6–8 M-cell mesh needs several GB, plus the 13.7/18.3 GB of a running solve (AGY 1 / Sol A6).
   - The D7 cases were built by the attempt-1 builder, so their post output says "strict section rule not evaluated (pre-strict-rule build)". p011 passes the strict rule on the scan-14 mesh.
   - The Task A statistic uses `M1_probes` p011, computed with the unchanged default section method.
2. **P5 473.**
   - The relocation to node 646 (+2.853 mm) is centreline-checked only. The box/area check runs when the P5 mesh exists (Opus 32).
   - If 646 fails on the mesh, the next node, 647, is at 3.58 mm > 3 mm, and the builder refuses. The analysis side should then decide on the probe; a larger relocation limit would be a rule change.
   - The P5 returns must quote `measurement_probe_used` (it is in M1_results notes and post_summary).
3. **Section method of `M1_probes`.** The method is kept identical to the 09-26 one for comparability. It can lose area where a plane cuts cfMesh transition polyhedra (sten70 x = 52 mm). The history cross-check (monitor area vs section area, > 0.5 % flagged) detects this for the measurement and throat probes. Check that flag before using a value.
4. **OpenFOAM sampledPlane on a face layer.** The sampledPlane area is wrong when the plane lies exactly on a layer of mesh faces (+8.3 % in the synthetic test). The real probe planes are oblique to the cfMesh grid, so this is unlikely there, and the same cross-check flags it.
5. **Peak RAM** is reported only with `PEAK_RAM_GB` or a `MEMLOG` sampler; otherwise "not available". The geometry-gate columns stay empty if no gates json is found, and the notes name what is missing.
6. **Analyse verdict.** An UNCONVERGED verdict does not stop the runner by default; the result row says it. Set `POST_REQUIRE_CONVERGED=1` for a hard stop.

# Attempt 3 (Opus 5.5 task 36): round-2 audit findings (`../audit_AC/SOL_C2.md` NOT READY, `../audit_AC/AGY_C2.md` READY WITH CONDITIONS)
All work is in `taskC/`. `taskC_a2_snapshot/`, `p5/`, `m1/`, `taskB/`, `taskJ/`, the pool directories, the package files and `../taskA/TASK_A_DESIGN.md` were not modified.
- **Host etiquette.** Everything ran with nice -n 10 and ≤ 2 threads.
- **No solver on a real case.** The only solve was the synthetic 41k-cell tube (2 ranks). Its test root is now `taskC/.post_test_tmp`, which the test removes; it is gone.
- **No process left.** The only simpleFoam processes on the host are the coordinator's 16-rank A1 solve.
- **Live A1 case: read only.** On `m1/cases/baseline_D7_12p5_resistance` I ran only the new `finished` and `package-check` helpers. `finished` refused it (no exact End: still solving). `package-check` verified its package against build_info (resolved to the zipcheck copy, all 8 hashes equal).

## A3.1 Changes
**(1) Package resolution and verification (Sol C2-1 MAJOR, AGY C2-4).**
- `pf/m1_package.py`:
  - The hard-coded `/tmp/claude-1000/...` root is removed, and so are the `$M1_PKG_ROOT` and `<pilot>/m1/pkg` fallbacks.
  - Resolution order: an explicit package directory, or the explicit `--pkg-root` (the runner's `$PKG_ROOT`) **alone**, with no fallback when given. Otherwise the Drive `packages/M1`, then `packages/P5`, then the persistent copy `/home/azan/paper6_t6_work/scratchpad/zipcheck/cfd_handover/packages/M1`.
  - The Drive `packages/M1` currently holds only README/desktop.ini, so scan-14 names resolve to the zipcheck copy.
  - New `resolve_pkg_dir`, `package_hashes`, `verify_against_build`. The last compares the package name (basename; build_info records the builder's argument) and the file set and sha256 of every hashed file with build_info `package_hashes`. A missing record counts as a mismatch.
- `post_case_generic.sh` step 0b, `post_helpers.py package-check`, runs **before anything is generated**: after the finished check and before `analyze_case.py`.
  - It writes `package_check_<label>_<mode>.json`.
  - It stops (exit 1) on any mismatch.
  - Every later step (probes, radius, flow-state, fill) gets the **verified absolute package directory**, not the name.

**(2) Flow-state comparison over the full profile (Sol C2-2 MAJOR).**
- `flow_state_profile.py compare`: the statistic is the max over the **full specified profile**.
- The specified stations of each profile are recomputed from its rows: `stations(0, L)`, where L = s_from_throat + s_to_measurement.
- Any of the following makes the comparison **STATES INDETERMINATE**: an invalid section on either side (listed with the side), a missing station, an unmatched station, a station outside the specified profile, or no station valid in both. This holds also with `--ffr`; `profile_criterion = INDETERMINATE`.
  - The reason and the station lists are reported.
  - The maximum over the stations valid in both is reported as `subset_max_vector_diff_INFORMATION_ONLY`, with `subset_max_exceeds_tol`.
  - No replacement rule is applied. The pre-registered rule in TASK_A_DESIGN.md is unchanged.
- AGREE/DIFFER are given only for complete profiles.

**(3) Finished-solve guard (Sol C2-3 MAJOR).** `post_helpers.run_completion` is defined on the log tail.
- **The last run.** It starts at the last header line (`Build :`, `Exec :` or `Starting time loop`). It must contain a `Time = <t>` line.
- **End.** The last such Time line must be followed by a line that is exactly `End`.
- **After End.** No header, `Starting time loop`, `Time =` or `FOAM FATAL` line may follow it: no appended run, partial or complete-header-only.
- **Budget.** `<t>` must equal `endTime` of `system/controlDict`. A residualControl or manual early stop is refused.
- **Where it is used.** Same function in `finished` (runner step 0, writes `run_completion_*.json`), `log_finished` and the summary.
- **Analysis completion flag.** It is enforced: `analyze_case.py --require-finished` (new, exit 4) when `strict.log_finished` (End + `Finalising parallel run` in the last 2000 characters, analyze_solve) is false. The runner always passes it.
- **Convergence.** Non-convergence stays a reported flag; `POST_REQUIRE_CONVERGED=1` (exit 3) still makes it a stop.

**(4) Radius provenance (Sol C2-4 MINOR).**
- `post_helpers.py radius-check` / `radius-commit` maintain `as_meshed_radius_<label>_provenance.json`, which records:
  - the mesh sha256 over every file of the case's `constant/polyMesh` (name + content);
  - the package hashes;
  - the sha256 of the three radius files.
- Existing radius files are reused only if all of these match now. Otherwise they are regenerated and the provenance is rewritten.
- `POST_FORCE=1` always regenerates. `POST_REUSE_UNCHECKED=1` reuses without the check (an explicit waiver).
- The decision is recorded in `post_summary_*.json` → `radius_outputs`, and in the log. The provenance json is one of the hashed outputs.

**Also.**
- `post_summary_*.json` gains `run_completion`, `analysis_log_finished`, `package_check` and `radius_outputs`.
- `TEMPLATE_README.md` is updated (package lookup, runner guards, INDETERMINATE).
- New test: `tests/test_post_guards.py`.

## A3.2 Test output
1. **`tests/test_post_guards.py` (new, solver-free): PASS** (`test_output/post_guards_test.txt`).
   - **run_completion on synthetic logs.**
     - Accepted: complete; restart whose last run completed; CRLF.
     - Refused: no End; appended partial run; appended header only; End before the last Time; residualControl early stop (Time 42 ≠ endTime 50); FOAM FATAL after End; `End of run`; endTime 3000 vs last Time 50.
   - **Resolution.** Scan 14 → zipcheck copy; 473 → Drive P5. An explicit root is used alone. The module has no `/tmp` and no `M1_PKG_ROOT`.
   - **package_check.** A verified copy is OK. Refused: tampered probes.csv, missing mask_edit.json, no recorded hashes, other package name. Order in the runner: package-check < analyze_case < m1_probes.
   - **Radius provenance.** No record, changed mesh file, other package hashes, or an edited radius file → regenerate. Same mesh + package → reuse.
2. **`tests/test_post_case_generic.sh` (synthetic finished solve, end to end): PASS** (`test_output/post_case_generic_synthetic/test_run_stdout.txt`, `post*.txt`).
   - **(a)** Refusal before the solve.
   - **(b)** RUN COMPLETE (last Time 1000 = endTime, End at line 46134); package verified; radius regenerated + provenance; all checks as in attempt 2; the summary now has 15 hashed outputs.
   - **(d)** The second run reuses the reconstruction, the analysis and the radius files (provenance verified).
   - **(f)** One `Build/Exec/Starting time loop/Time = 1001` block appended to the log → `RUN NOT COMPLETE`; exit 1. The output timestamps are unchanged, so nothing was generated.
   - **(g)** A package copy with one byte added to probes.csv (`PKG_ROOT` pointing at it) → `PACKAGE NOT VERIFIED … probes.csv: sha256 …`; exit 1; outputs untouched.
   - **(h)** The log without `Finalising parallel run`: run_completion OK, but the analysis completion flag is false → `--require-finished`, exit 4.
   - **(i)** Provenance recording another mesh sha → `mesh sha256 differs` → regenerated. `POST_REUSE_UNCHECKED=1` → `REUSED UNCHECKED`, recorded in the summary. The next plain run reuses with verified provenance.
   - `area_flag_demo_nx100_history.json` (attempt-2 evidence, deleted by the test's evidence refresh) was copied back from `taskC_a2_snapshot/`.
3. **`tests/test_flow_state_profile.py` (analytic): PASS** (`test_output/flow_state_analytic_test.txt`).
   - Unchanged checks: a/4 reproduced, AGREE/DIFFER on complete profiles.
   - New: one invalid station (either side), a dropped station, an extra unmatched station, and an invalid station with `--ffr` agreeing all give STATES INDETERMINATE.
   - Also INDETERMINATE when the subset max (0.0999) is above the tolerance.
   - Subset max = 0 for the identical profiles with one invalid station: never AGREE.
4. **`tests/test_flow_state_sten70.sh` (retained sten70 fields, profiles recomputed): PASS** (`test_output/flow_state_sten70/cmp.txt`, `test_run_stdout.txt`):
   ```
   STATES INDETERMINATE (profile criterion only: ...): pre-registered statistic = max over the FULL specified profile; not available: invalid section at s-s_throat [22.0] mm. Information only: max |o_A - o_B| over the 25/26 stations valid in both = 0.0026 at s-s_throat 15.0 mm (not above tol 0.03)
   STATES INDETERMINATE (profile criterion only: ...): ... invalid section at s-s_throat [22.0] mm. Information only: max |o_A - o_B| over the 25/26 stations valid in both = 0.3635 at s-s_throat 10.0 mm (above tol 0.03)
   STATES DIFFER: max |o_A - o_B| over the full profile = 0.3617 at s-s_throat 10.0 mm (tol 0.03; all 26 stations valid in both); |FFR_A - FFR_B| = 0.001490 (tol 0.00055, ffr criterion DIFFER)
   ```
   Lines: smoke_cont vs case_S50, a5_arch8 vs case_S50, a5_arch8 vs smoke_cont.

   **Why S50 vs smoke_cont is now INDETERMINATE.**
   - **The x = 52 mm section of case_S50 is invalid.** s − s_throat = 22 mm; 6 boundary loops, holes 8.8 % of the filled area, a VTK cut through cfMesh transition polyhedra.
   - **The pre-registered statistic needs all 26 stations.** It is the max over the full profile, so it does not exist for this pair.
   - **The other 25 stations agree.** Their maximum is 0.0026, far below 0.03, but that is a subset statistic. The rule gives no replacement for an invalid station, so the verdict word is INDETERMINATE.
   - **The defective cut would have flipped the verdict.** At that station the raw values are o = (0.0273, 0.0223) for S50 and (0.0006, −0.0020) for smoke_cont: |Δo| = 0.036 > 0.03. Using the defective section would have produced a false STATES DIFFER, and dropping it would have produced an unlicensed AGREE. INDETERMINATE is the only verdict the rule supports.
   - **a5_arch8 vs case_S50 is INDETERMINATE for the same reason.** Its subset max of 0.3635 exceeds the tolerance. Since the full maximum can only be larger, the data imply the full statistic is above 0.03 as well. The verdict word still follows the brief, with no replacement rule; `subset_max_exceeds_tol: true` is recorded.
   - **The full profile still separates the branches.** a5_arch8 (deflected) vs smoke_cont (axisymmetric) is complete and gives STATES DIFFER (0.3617, and |ΔFFR| 0.00149).
5. **Re-run after the m1_package change: PASS.**
   - `tests/test_section_rule.py` (`test_output/section_rule_test.txt`): 473 → node 646 at +2.853 mm unchanged; scan-14 p011 passes on the real mesh; moved-probe B2 case unchanged.
   - `tests/test_p5_stub.py` (`test_output/p5_stub_test.txt`).
   - `tests/test_b1_settle.py` and `tests/test_manifest.sh` (`test_output/unit_tests_b1_manifest.txt`).
6. `bash -n` on every .sh and ast parse of every .py: OK.

## A3.4 Manifest
`__pycache__` and `*.pyc` were removed from taskC/, then `make_manifest.sh .` was run. `verify_manifest.sh .` reports **99 OK, 0 FAILED/MISSING**, with no unlisted files.

## A3.3 Open points and AGY C2 conditions
1. **Early stop vs endTime.** The finished guard now refuses any run whose last Time ≠ endTime. The production template (`pf_common`) has no `residualControl` and runs the fixed 3000-iteration budget (D8), so a template run ends at endTime. A run stopped early, by hand or by a non-template `residualControl`, is refused. There is deliberately no override; such a run has to be continued to its endTime.
2. **INDETERMINATE vs a subset maximum above the tolerance.** The full-profile maximum is ≥ any subset maximum, so a subset max > 0.03 logically implies the pre-registered statistic > 0.03. The brief nevertheless requires INDETERMINATE whenever a station is invalid. That is what is implemented, with `subset_max_exceeds_tol` reported. Treating that case as DIFFER would be a decision for the coordinator before any Task A result is viewed.
3. **For Task A (AGY C2-1/-2).**
   - Run the runner with `REF_FFR=0.8697574904997768`, and with `PKG_ROOT` unset (the zipcheck copy verifies) or set to the zipcheck root.
   - Run it after A1 finishes and before A2 starts, or after both (RAM).
   - If an A1/A2 flow-state profile has an invalid station, the classification will be INDETERMINATE.
4. **P5 473 (AGY C2-3).** Unchanged: the relocation to node 646 must pass S3/S4 on the P5 mesh (the builder's default `mesh_check`), else the builder refuses.
5. **Radius provenance cost.** The mesh hash reads every polyMesh file: about 1–2 GB for the 6–8 M-cell D7 meshes, a few seconds. It is computed once per run (twice with `POST_FORCE=1`).
