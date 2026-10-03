# Production case template with the D8 probe monitors (Task C, work order 2026-10-03)

The files here replace their namesakes in `item3_M1_pilot/pf/` and `item3_M1_pilot/b1_settle.py`. New in attempt 1: `probe_sections.py`. New in attempt 2: `post_case_generic.sh`, `flow_state_profile.py`, `pf/post_helpers.py`, the strict measurement-section rule in `probe_sections.py`, and copies of `pf/{analyze_case,m1_probes,as_meshed_radius,m1_results,sections,e0_check}.py` (generalised; taskC/ now runs standalone).

| file | role |
|---|---|
| `pf/pf_common.py` | case writer. `monitors()` now writes `throatFlux`/`throatP` **and** `measurementFlux`/`measurementP` on **bounded** planes, every iteration (`writeInterval 1`), with `writeArea true`. `series()` reads the value column from the `.dat` header. |
| `pf/probe_sections.py` | sizes the bounding box of each probe plane and **checks** the bounded section on the actual polyMesh (pyvista). |
| `pf/build_m1_case.py` | package-driven builder for M1 / P5 packages (any package of this format). It refuses a case whose bounded sections fail the mesh check. |
| `pf/m1_package.py` | package reader: `measurement_plane()`, `probe_row()`, package lookup: a package path, else the explicit `--pkg-root`/`$PKG_ROOT` alone, else Drive `packages/M1`, `packages/P5`, then the persistent copy `scratchpad/zipcheck/cfd_handover/packages/M1`; `verify_against_build()` checks a package against `build_info.json` `package_hashes` |
| `pf/pf_roundtrip_build.py` | round-trip (stage 2) builder: inherits both bounded planes from the prescribed case |
| `b1_settle.py` | B1/D8 settle analysis on `measurementP` (see below) |
| `make_manifest.sh`, `verify_manifest.sh` | manifest over LF-normalised content (work order section 0) |
| `post_case_generic.sh` | end-to-end post-solve runner for any package (below) |
| `pf/post_helpers.py` | runner helpers: finished check, reconstruction check, generic fill json (gate discovery), measurement-probe history + cross-check, cells, peak RAM, summary |
| `flow_state_profile.py` | pre-registered Task A flow-state diagnostic (`profile`) and the two-solve classification (`compare`) |
| `pf/analyze_case.py`, `pf/m1_probes.py`, `pf/as_meshed_radius.py`, `pf/m1_results.py`, `pf/sections.py`, `pf/e0_check.py` | copies used by the runner. Changes: path lookup of `analyze_solve.py`; relocated measurement row in the probes csv; M1 contract radius files (`--contract`); "measurement probe USED" note in M1_results; `Sectioner(robust=True)` for the diagnostic |
| `tests/` | `test_p5_stub.py`, `test_b1_settle.py`, `test_manifest.sh`, `test_section_rule.py`, `test_flow_state_profile.py`, `test_flow_state_sten70.sh`, `test_post_case_generic.sh` (+ `synthetic_tube.py`), `test_post_guards.py` |

## Probe monitors (D8)
- **measurementP**: area-averaged kinematic p on the section at the `probes.csv` row of kind `measurement`. That row must sit on `meta.json` `measurement.tree_node`. `measurementFlux` holds the through-section flow on the same plane.
- **throatP / throatFlux**: the same on the `throat` row.
- Each `.dat` has the columns `Time  Area  value`. Area is in m² and lets you check the section on every run. Multiply p by 1060 to get Pa, and divide by `P_aorta_Pa` to get the FFR at the measurement probe.
- **Bounded planes.** An unbounded `pointAndNormal` plane cuts every vessel that crosses it. On scan 14 the throat plane cut 4 sections (8.35 mm² in total against 0.239 mm² of lumen) and the measurement plane cut 2 (5.31 against 3.37 mm²). So the builder adds the v2406 sampledPlane keyword `bounds (lo) (hi);`, an axis-aligned box around the probe. Only cells whose centre lies in the box are cut (`sampledPlane.C`, `cuttingSurfaceBaseSelection.C`).
- **Box sizing** comes from `r_ref_mm` and `centreline.vtp`: half-width h = min(max(2 r_ref, h_min), h_clear), with h_min = 1.3 r_own/|cos| + 0.3 mm. h_clear keeps every other place where the centreline meets the infinite plane outside the box.
- **Mesh check.** The builder refuses the case unless the bounded cut:
  - is exactly one connected component, the one at the probe;
  - lies wholly inside the box, with ≥ 0.5 cells of margin;
  - has every other component outside the box, with ≥ 0.5 cells of margin;
  - has an area within [0.4, 2.5] × π r_own² and a centroid within 0.5 r_eq of the probe.

  r_own is the centreline `r_target_mm` at the probe node, i.e. the lesioned lumen at a throat. Each attempt is recorded in `build_info.json` → `probe_section_check`, together with the infinite-plane diagnostic.
- **Strict single-lumen rule for the measurement section** (`probe_sections.py`, audit Sol finding 2). On top of the mesh check, the measurement section must have:
  - S1: the plane normal within 20° of the local centreline tangent (chord over ±0.5 mm of the vessel path);
  - S2: no bifurcation within 1.5 r_ref along the vessel path, i.e. every node there has tree degree 2;
  - S3: the mesh check above (one component, not clipped, no other vessel in the box);
  - S4: area within a factor 1.6 of π r_ref² on both sides.

  The thresholds and their justification from the scan-14 values are in the module docstring. A package probe that fails the rule is recorded `FAILED_SECTION_RULE` and **relocated**. The new point is the nearest centreline node of the same vessel path within 3 mm of arc that passes S1–S4 (ties go distal), with the local tangent as normal. Then:
  - `measurementFlux`/`measurementP` sample the relocated plane;
  - `measurementOrigFlux`/`measurementOrigP` sample the package plane, only if its bounded section passes the mesh check;
  - `build_info.json` records `measurement_section_rule`, `measurement_probe_relocated` (original and relocated) and `measurement_probe_used`.

  With no valid node within 3 mm, the builder refuses. Package files are never modified. P5 473 (p011) fails S1 (36.6°) and S2 (bifurcation node 424 at −0.84 mm). On the centreline it is relocated to tree_node 646, +2.853 mm; the mesh check of that box can only run on the P5 mesh. The throat probe keeps the lenient rule (r_own = r_target there); its S1/S2 values are recorded only.
- `--no-mesh-check` exists only for case-file tests against a stub polyMesh. It writes `NOT_FOR_PRODUCTION` and sets `production_ready: false`.

## Stopping rule (D8): run the full budget
- `endTime` stays 3000 (fixed budget, no residualControl). **Every production solve runs the full budget.** D8 says: until a production case has a measurement-probe history, every solve runs to the full budget. The B1 proxy is not authorised as a stopping rule.
- `b1_settle.py` applies the SETTLED rule of 09-26 §5 B1 to `FFR_mon = measurementP·ρ/P_aorta` when the monitor exists. Those rows are labelled `B1`, or `B1 (D8 prescribed-flow variant)` for prescribed-flow solves: outlet-pressure bands replace the flow bands, and the BC-error criterion does not apply. Without the monitor the row stays `PROXY_NOT_B1` (LAD-outlet pressure).
- Prescribed-flow solves keep a **minimum of 800 iterations**. `iter_first_settled_floored = max(first settled, 800)` is applied to the first-settled iteration and to every stop recommendation.
- The column `stop_recommendation` always reads `RUN THE FULL BUDGET …`. For B1 rows it also states the iteration at which the rule *would* stop, marked "not applied".
- Columns renamed from the 09-26 table: `FFR_proxy_*` is now `FFR_mon_*`. The new columns `b1_label` and `ffr_series` say which series was used. Also new: `min_iterations_floor`, `*_floored`, `throat_plane_bounded` and `stop_recommendation`.

## Post-solve runner: `post_case_generic.sh <case_dir> <package_dir_or_name> <label> <mode> <out_dir>`
- **Use.** Run it once per finished solve, one case at a time: the field steps load the whole mesh, about 1 GB per million cells. Do not run it next to a large solve on this host.
- **Finished check (attempt 3).** It refuses a case unless the **last run** of `log.simpleFoam` completed: an exact `End` line after that run's last `Time = <t>` line, nothing after it that starts another run (`Build:`/`Exec:`/`Starting time loop`), no `Time =` or FOAM FATAL line, and `<t>` equals `endTime` of `system/controlDict` → `run_completion_*.json`.
- **Package check (attempt 3).** Before anything is generated, the resolved package files are verified against `build_info.json` `package_hashes`. A mismatch, a missing or extra hashed file, or no record stops the runner → `package_check_*.json`. Later steps get the verified absolute package directory.
- **Steps.**
  1. `analyze_case.py`, strict, written to `<case>/analysis_pf.json`. The analysis completion flag (`strict.log_finished`) is enforced (`--require-finished`, exit 4). The convergence verdict is reported, not a stop; `POST_REQUIRE_CONVERGED=1` makes it one.
  2. `reconstructPar -latestTime`, then a **reconstruction check**: the latest reconstructed time equals processor0's, `U`/`p` are non-empty, and the log ends with `End`. Fields are kept. **Processor directories are never removed by the runner**: remove them only after `reconstruct_check_*.json` is ok and the outputs are verified.
  3. `M1_probes_<label>_<mode>.csv`, with an extra `measurement_relocated` row when the builder relocated the probe.
  4. `as_meshed_radius_<label>{,_inscribed,_detail}.csv` in the M1 contract format. Existing files are reused only if `as_meshed_radius_<label>_provenance.json` records the same mesh sha256 (case `constant/polyMesh` files), the same package hashes and unchanged outputs; otherwise they are regenerated. `POST_FORCE=1` always regenerates. `POST_REUSE_UNCHECKED=1` reuses without the check. The decision is recorded in the summary (`radius_outputs`).
  5. `fill_<label>_<mode>.json`, the geometry/mesh gate columns. Mesh gates are found via build_info `mesh_source_dir` or the hard-linked mesh inode. Geometry gates are found via the build's extension json, `p5/out/<package>/gates.json`, or (scan 14) `m1/out/<error_type>/gates.json`. `GATES_JSON` and `MESH_GATES_JSON` override; missing values stay empty and are named in the notes.
  6. `M1_outlets_*.csv` and the `M1_results.csv` row. The notes state the measurement probe used.
  7. `M1_monitor_history_*.csv/.json`: every iteration of measurementP/Flux, throatP/Flux and measurementOrig*. The json cross-checks the last monitor value and area against the reconstructed section of the probes csv; an area difference > 0.5 % is flagged `AREA MISMATCH`. Also `settle_*.csv` (b1_settle).
  8. `flow_state_*.csv/.json`.
  9. `post_summary_*.json`: verdict, wall clock, cells, peak RAM (`PEAK_RAM_GB` or a `MEMLOG` sampler file, else "not available"), probe used, sha256 of every output.
- **Paths.** `P` = `$P`, else `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot`. Helpers come from `<script dir>/pf`, else `$P/pf`. Packages: a package directory; else `$PKG_ROOT` alone if set; else Drive `packages/M1`, `packages/P5`, then the persistent copy `scratchpad/zipcheck/cfd_handover/packages/M1`. There is no `/tmp` root. Nothing is scan-14 specific.

## Flow-state diagnostic (Task A, pre-registered): `flow_state_profile.py`
- `profile <case> --package <pkg>` (or `--straight-x X_THROAT X_MEAS` for straight tubes). It takes connected, bounded sections normal to the centreline tangent, every 1 mm from throat + 2 mm to the measurement probe.
- Per section it gives r_eq and the flux-weighted axial-velocity centroid offset from the area centroid over r_eq, signed in a rotation-minimising (normal, binormal) frame of the centreline.
- `compare A.csv B.csv [--ffr FFR_A FFR_B]`: the statistic is max |o_A − o_B| over the **full** specified profile. **STATES AGREE** iff it is ≤ 0.03 and |FFR_A − FFR_B| < 0.00055; otherwise STATES DIFFER.
- **Incomplete profiles (attempt 3).** If any station is invalid on either side, missing, unmatched or outside the specified profile, the verdict is **STATES INDETERMINATE**. The stations are listed, and the maximum over the stations valid in both is given for information only.
- A section with holes (≥ 0.5 % of its area) is invalid. This was seen at one sten70 station cut through cfMesh transition polyhedra.

## Outlets lost in the mesh, flags, decisive geometry gates (FIX37, audit P5 Sol findings 1, 2, 5, 6)
- **0-face outlet patch** (P5 272 `out_396`): `pf_common.write_case` writes no `surfaceFieldValue` monitor for it, because v2406 treats a patch selection that yields zero faces as fatal. Its 0/p and 0/U entries stay: the coded resistance BC is inert on an empty patch (`tests/test_empty_patch_coded_bc.py`, real serial simpleFoam run). `zerod_reference.json` and build_info `outlets` list only the outlets that have faces. build_info `outlets_lost_in_mesh` gives the reason (from the mesh stage), and `bc_bookkeeping` records that the lost territory is closed: no flow, its bc_C target not delivered, its bc_A R not applied. The analysis criteria (BC error, bands, mass balance) run over the outlets in the mesh only. In `M1_outlets` the lost outlet appears as Q 0, p `N/A`, `closed 1`, `lost_in_mesh 1`, flag `OUTLET_LOST_IN_MESH`.
- **`M1_results` new columns:** `flags` (`;`-joined, fixed order, `NONE` if empty), `geometry_all_gates_pass_including_reported`, `D3_verdict`, `D4_verdict`, `D34_min_dist_throat_mm`, `D34_min_dist_measurement_mm`, `D34_checks_within_2mm`, `outlets_lost_in_mesh`.
  - Flag sources: the geometry gates.json, d34.json (`--d34` / `D34_JSON` / discovered next to the mesh gates), the mesh gates (standard checkMesh) and build_info (probe relocation, lost outlet, manual-repair record), plus `NOT_CONVERGED` from the analysis. The list is in the post_helpers.py docstring.
- **D10:** `geometry_step_ok` follows the **decisive** gates only, i.e. all gates except the literal absolute r_target check, which is reported only. `gates.json` of the fixed geometry builder carries `GATES_DECISIVE`, `GATES_REPORTED_NON_DECISIVE`, `ALL_GATES_PASS` (decisive) and `ALL_GATES_PASS_INCLUDING_REPORTED`. An older gates.json is split the same way by post_helpers.

## Usage
```
# production (P5: baseline, resistance mode, 16 ranks); mesh_dir holds constant/polyMesh with patches inlet, wall, <outlet_id>...
python3 pf/build_m1_case.py <package> <mesh_dir> resistance <case_dir> 16 --pkg-root .../packages/P5 [--extensions-json gates.json]
# after a finished solve (one case at a time): all return files + checks
bash post_case_generic.sh <case_dir> <package> <label> resistance <out_dir>
# flow-state classification of two solves of the same package (Task A)
python3 flow_state_profile.py compare <out>/flow_state_A1_resistance.csv <out>/flow_state_A2_resistance.csv --ffr <FFR_A1> <FFR_A2>
# settle analysis of finished cases
python3 b1_settle.py settle.csv --case <case_dir> [--case ...]
# manifest of a folder (e.g. code_from_cfd/), and its check on any copy
./make_manifest.sh <dir>; ./verify_manifest.sh <dir>
```
`MANIFEST.sha256` contains no `#` lines, so plain `sha256sum -c` / `shasum -a 256 -c` works on an LF copy. The hashing rule is stated in `MANIFEST.README`: text files are hashed with CR bytes removed, binary files (any NUL byte) raw. `verify_manifest.sh` applies the same rule, so it passes on CRLF copies too.
