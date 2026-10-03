# Pre-Run Audit Report: Tasks C and A (WORK-ORDER-2026-10-03)

**Audit Scope:**
- **(C) Task C:** Production template with D8 probe function objects in [`taskC/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/) ([`FIX30_REPORT.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/FIX30_REPORT.md), [`TEMPLATE_README.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/TEMPLATE_README.md), [`pf/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/), [`b1_settle.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/b1_settle.py), [`make_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/make_manifest.sh), [`verify_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/verify_manifest.sh), [`tests/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/), [`test_output/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/test_output/)).
- **(A) Task A:** D7 sensitivity test setups for Scan-14 baseline: mesher modifications ([`m1/build_m1_mesh.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/build_m1_mesh.py)), mesh variants [`m1/mesh/baseline_D7_12p5`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/mesh/baseline_D7_12p5) (6,241,438 cells) and [`m1/mesh/baseline_D7_12p5_zoneB`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/mesh/baseline_D7_12p5_zoneB) (8,308,794 cells), gate outputs, and cases [`m1/cases/baseline_D7_12p5_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance) and [`m1/cases/baseline_D7_12p5_zoneB_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_zoneB_resistance).

---

## 1. Audit of (C) Task C: Production Case Template & D8 Function Objects

### 1.1 Bounded Sampled Planes & Verification of 09-26 Infinite-Plane Defect
- **Function Object Definition:** In [`taskC/pf/pf_common.py:70-80`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/pf_common.py#L70-L80), `surface_fo` now writes `bounds (<lo>) (<hi>);` into `sampledSurfaceDict`. OpenFOAM ESI v2406 `sampledPlane` natively parses `bounds` (`sampledPlane.C` and `cuttingSurfaceBaseSelection.C`), selecting only cells whose centroids fall within the axis-aligned bounding box.
- **Mesh Check Implementation:** [`taskC/pf/probe_sections.py:84-154`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/probe_sections.py#L84-L154) sizes the box via centreline clearance (`h_min = 1.3 r_own/|cos| + 0.3 mm`, `h = min(max(2 r_ref, h_min), h_clear)`), performs an authoritative PyVista mesh slice on the actual `polyMesh`, and strictly verifies:
  1. Exactly one connected lumen component in the box;
  2. Margin $\ge 0.5$ local cell sizes between the section and box boundary;
  3. Margin $\ge 0.5$ local cell sizes outside the box for other vessels;
  4. Area factor within $[0.4, 2.5] \times \pi r_{\text{own}}^2$ and centroid offset $< 0.5 r_{\text{eq}}$.
  Cases failing the check are refused (`SystemExit`) by [`build_m1_case.py:44`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/build_m1_case.py#L44).
- **Confirmation of 09-26 Infinite-Plane Defect:** Inspection of [`taskC/test_output/taskC_test_5iter/build_info.json:359-364, 454-459`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/test_output/taskC_test_5iter/build_info.json#L359-L364) and [`baseline_resistance/system/controlDict:104-130`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_resistance/system/controlDict#L104-L130) verifies that the 09-26 monitors had **no bounds** and cut multiple branches:
  - **Throat plane (`p004`):** The infinite plane cut **4 separate components** with a total area of **$8.351\text{ mm}^2$** vs the actual throat lumen area of **$0.239\text{ mm}^2$** (inflated by $35\times$).
  - **Measurement plane (`p011`):** The infinite plane cut **2 components** with a total area of **$5.309\text{ mm}^2$** vs the probe lumen area of **$3.370\text{ mm}^2$**.
  Bounded planes resolve this completely: bounded section area matches single-lumen PyVista section to 6 decimal digits.

### 1.2 Monitor Output & Area Column Handling
- In [`taskC/pf/pf_common.py:84-88`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/pf_common.py#L84-L88), `throatFlux`, `throatP`, `measurementFlux`, and `measurementP` specify `writeInterval 1;` and `writeArea true;`.
- Because `writeArea true` causes OpenFOAM to insert an `Area` column as column 1 (`# Time \t Area \t areaAverage(p)`), [`taskC/pf/pf_common.py:141-152`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/pf_common.py#L141-L152) defines `value_column(path)` which parses the header and dynamically identifies the non-Time/non-Area value column (index 2).
- [`taskC/b1_settle.py:41`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/b1_settle.py#L41) calls `c = C.value_column(f)` to extract pressure values, preventing the area value from corrupting FFR calculations. Confirmed by `taskC/tests/test_b1_settle.py` where synthetic FFR evaluated to exactly $0.850000$.

### 1.3 B1 / D8 Settle Logic
- **`SETTLED` Rule on `measurementP`:** In [`taskC/b1_settle.py:68-74`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/b1_settle.py#L68-L74), when `measurementP` is present, `pin = mp` and the row is labeled `B1` (resistance) or `B1 (D8 prescribed-flow variant)` (prescribed-flow). When absent, it falls back to the proxy LAD outlet and retains `PROXY_NOT_B1`.
- **800-Iteration Floor for Prescribed Runs:** [`taskC/b1_settle.py:35, 88-96`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/b1_settle.py#L35) sets `floor = 800` for prescribed-flow solves, recording `iter_first_settled_floored = max(first, 800)`.
- **Full Budget Default:** `STOP_DEFAULT = "RUN THE FULL BUDGET (D8 production default: no early stop is authorised"`. In [`taskC/b1_settle.py:97-101`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/b1_settle.py#L97-L101), `stop_recommendation` always mandates running the full budget; for `B1` rows, it states the iteration at which D8 would stop, explicitly marked `not applied`.

### 1.4 Package-Driven Builder for P5 Family
- [`taskC/pf/m1_package.py:11-33`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/m1_package.py#L11-L33) supports Drive folders `/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/P5/` and `/packages/M1/`.
- [`taskC/pf/build_m1_case.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/build_m1_case.py) builds resistance and prescribed-flow cases for any package matching the format (reading outlet patches from `outlets.csv`).
- **P5 Package Verification:** Ran [`taskC/tests/test_p5_stub.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_p5_stub.py) against all 5 P5 packages (`138_left_LAD`, `139_right_RCA`, `272_right_RCA`, `473_left_LCX`, `69_left_LCX`). All 5 built successfully; all outlet patches matched; `foamDictionary` successfully validated the generated `controlDict` entries.
- **Package 473 Bifurcation Caveat:** Disclosed in [`taskC/FIX30_REPORT.md:113`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/FIX30_REPORT.md#L113), probe `p011` of `473_left_LCX` sits on a daughter branch origin at a bifurcation, with normal $45^\circ$ off the tangent. When the real 3D mesh is generated, `probe_sections.py` may fail the single-lumen box check unless clarified by the analysis side.

### 1.5 Manifest Scripts
- [`taskC/make_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/make_manifest.sh) normalizes text files by stripping CR (`tr -d '\r'`), leaves binary files raw, and outputs a comment-free `MANIFEST.sha256` that directly passes standard `sha256sum -c`. Descriptive metadata is written to `MANIFEST.README`.
- [`taskC/verify_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/verify_manifest.sh) applies the identical LF-normalization on verification, strips `#` comment lines, and ignores CR in the manifest itself.
- All 35 files in `taskC/` verified clean (`35 OK, 0 FAILED/MISSING`).

### 1.6 Builder Parity & Test Suite Results
- Comparing `pf/` and `taskC/pf/`: aside from bounded probe function objects, probe checks, and P5 package lookup, **no numerics, relaxation equations ($G = R/R_{\text{own}}$), boundary conditions, or solver settings were changed**.
- All tests passed:
  - `bash -n` on all shell scripts: **PASS**
  - `python3 -m py_compile` on all python scripts: **PASS**
  - `python3 taskC/tests/test_b1_settle.py`: **PASS**
  - `bash taskC/tests/test_manifest.sh`: **PASS**
  - `python3 taskC/tests/test_p5_stub.py`: **PASS** (all 5 packages)

---

## 2. Audit of (A) Task A: D7 Sensitivity Test

### 2.1 Meshing Recipe & Script Modifications
- Comparing [`m1/build_m1_mesh.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/build_m1_mesh.py) with [`m1/build_m1_mesh.py.orig_2026-10-03`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/build_m1_mesh.py.orig_2026-10-03):
  The only modifications are the introduction of environment variables `M1_THROAT_REQ`, `M1_THROAT_LO_MM`, `M1_THROAT_HI_MM`, and `M1_ULIMIT_KB`.
  The meshing recipe, boundary layer specification (4 layers, ratio 1.2), spherical patch refinements, surface smoothing (Taubin, 30 it), and gate verification logic are completely unchanged.
- Recipes verified in `recipe.json`:
  - **Variant 1 (`baseline_D7_12p5`):** `throat25` request set to `2e-5` ($12.5\ \mu\text{m}$), zone $[s_t - 4.0, s_t + 4.0]\text{ mm}$.
  - **Variant 2 (`baseline_D7_12p5_zoneB`):** `throat25` request set to `2e-5`, zone $[s_t - 3.0, s_t + 5.0]\text{ mm}$ (shifted by $+1\text{ mm}$ at both ends as in the U3D ladder).

### 2.2 Mesh Gate Measurements & Strict checkMesh D3/D4 Analysis
- Gate evaluation results:
  - **Variant 1 (`m1/mesh/baseline_D7_12p5/mesh_gates.json`):** 6,241,438 cells; `cartesianMesh_finished`: true; `checkMesh_standard_OK`: true; cells across throat: min 66 ($\ge 12$); throat plane area error: $-0.0486\%$ ($< 2\%$); `GATES_PASS`: true.
  - **Variant 2 (`m1/mesh/baseline_D7_12p5_zoneB/mesh_gates.json`):** 8,308,794 cells; `cartesianMesh_finished`: true; `checkMesh_standard_OK`: true; cells across throat: min 66 ($\ge 12$); throat plane area error: $-0.0486\%$ ($< 2\%$); `GATES_PASS`: true.
- **Strict checkMesh D3/D4 Outcomes:**
  - Evaluated via `d34_generic.py` in [`m1/out_returns/d34_D7_12p5.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/out_returns/d34_D7_12p5.json) and [`m1/out_returns/d34_D7_12p5_zoneB.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/out_returns/d34_D7_12p5_zoneB.json).
  - Both meshes exhibit `lowQualityTetFaces` entities whose minimum distance to the throat center is **$0.698199\text{ mm}$** ($< 2.0\text{ mm}$), yielding **`D4_verdict: FAIL`** for both.
  - **Binding Work-Order Rule (WORK-ORDER-2026-10-03 §1 D7 & §2 Task A):** Because both variants have flagged entities within $2\text{ mm}$, **BOTH variants must be solved**.
  - **Acceptance Rule:** The returned baseline measurement-probe FFR is **`0.869757`** ([`returns/2026-09-26/M1_probes_baseline_resistance.csv:14`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_probes_baseline_resistance.csv#L14)).
    - If $|\text{FFR}_{\text{Variant}} - 0.869757| < U_{\text{3D}} = 0.00055$ (i.e. within $[0.869207, 0.870307]$): **PASS WITH DEVIATIONS D2/D3/D4 + D7**.
    - If $|\text{FFR}_{\text{Variant}} - 0.869757| \ge 0.00055$: **FAIL for lesion cases** (initiating §9 fallback).

### 2.3 Case Setup Parity with Audited Baseline Case
- Comparing [`m1/cases/baseline_D7_12p5_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance) and [`baseline_D7_12p5_zoneB_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_zoneB_resistance) against [`baseline_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_resistance):
  - `0/p`, `0/U`, `system/fvSchemes`, `system/fvSolution`, `constant/transportProperties`, and `constant/turbulenceProperties` are **byte-for-byte identical**.
  - Both cases link to their respective meshes via same-filesystem hard links (link count 2).
  - Outlets use identical coded resistance BCs (`codedFixedValue`) with exact matching target flows, reference resistances, and relaxation factors ($\text{relax} \in [0.00360, 0.03988]$, $G \in [24.07, 277.00]$).
  - E0 guard is confirmed: `"status": "MEMBER"`.
  - Both cases use 8 ranks (`decomposeParDict: numberOfSubdomains 8; method scotch;`).
  - `controlDict` difference is strictly limited to the addition of bounded `throatFlux`/`throatP` and `measurementFlux`/`measurementP` monitors with `writeArea true`.

### 2.4 Resource Requirements (RAM and Disk)
- **RAM Estimation:** At $\approx 2.2\text{ GB}$ per million cells for cfMesh Cartesian tree meshes:
  - Variant 1 (6.24M cells): $\approx 13.73\text{ GB}$ peak RAM.
  - Variant 2 (8.31M cells): $\approx 18.28\text{ GB}$ peak RAM.
  - **Host RAM Availability:** Total host RAM is $27.4\text{ GB}$ ($23\text{ GB}$ currently available).
  - **CRITICAL:** If both variants run concurrently, combined RAM exceeds $32\text{ GB}$, which would cause out-of-memory killing or severe swap paging. **The two solves MUST be executed strictly sequentially.**
  - Individually, each fits within available memory ($13.7\text{ GB} < 23\text{ GB}$; $18.3\text{ GB} < 23\text{ GB}$).
- **Disk Space:**
  - Root partition `/` currently has $26\text{ GB}$ available.
  - Each case stores 3 time directories (`purgeWrite 3` in `controlDict`). For 8 ranks, decomposed mesh + 3 times + reconstructed time 3000 will consume $\approx 3.1\text{ GB}$ for Variant 1 and $\approx 4.0\text{ GB}$ for Variant 2 ($\approx 7.1\text{ GB}$ total).
  - $26\text{ GB}$ free is adequate for sequential solves.

### 2.5 Solvability, Reliability & Flow-State Diagnostics
- **Physical Meaning of "Jet State" on Real Coronary Anatomy:**
  - WORK-ORDER-2026-10-03 §2 step 3 asks to report "the flow state (axisymmetric or deflected jet, as in B3)".
  - In Task B / B3 (sten70), the two steady states occurred due to a symmetry-breaking Coanda bifurcation downstream of an abrupt, perfectly axisymmetric constriction in an idealized straight tube.
  - In Scan-14 baseline, the lumen is a **real patient coronary artery** with 3D curvature, tortuosity, an elliptical cross section, and bifurcation branches. Flow is geometrically guided and asymmetric by anatomy; it is **never axisymmetric** in the mathematical sense of an idealized circular tube.
  - Applying the idealized diagnostic [`b3_audit/jet_offset.py:9-12`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/jet_offset.py#L9-L12) directly to scan-14 is physically invalid and syntactically incompatible (it assumes a straight cylinder along the x-axis centered at $y=0, z=0$).
- **Post-Solve Reliability & State Diagnosis Protocol:**
  To ensure Task A results are reliable and reproducible:
  1. Verify convergence to the 3000-iteration budget with stable probe pressures and BC errors $< 0.1\%$.
  2. Compare outlet flows across all 6 outlets against the returned baseline values ([`returns/2026-09-26/M1_results.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_results.csv)).
  3. Verify throat through-flux and Reynolds number ($\text{Re} \approx 123.1$, strictly laminar).
  4. Ensure `reconstructPar -latestTime` is executed and verified **before** purging any processor directories, so that 3D velocity fields are preserved for streamline inspection along the curved LAD centreline.

---

## 3. Numbered Findings

1. **MAJOR — Concurrent execution of the two Task A variants will exceed host RAM and risk OOM failure.**
   [`m1/cases/baseline_D7_12p5_resistance/system/decomposeParDict:2`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance/system/decomposeParDict#L2) and [`baseline_D7_12p5_zoneB_resistance/system/decomposeParDict:2`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_zoneB_resistance/system/decomposeParDict#L2).
   Variant 1 (6.24M cells) requires $\approx 13.7\text{ GB}$ and Variant 2 (8.31M cells) requires $\approx 18.3\text{ GB}$ at $2.2\text{ GB}/\text{M cells}$. Concurrent execution requires $> 32\text{ GB}$, exceeding total host memory ($27.4\text{ GB}$). A runner or job scheduler must enforce strict sequential execution between `baseline_D7_12p5_resistance` and `baseline_D7_12p5_zoneB_resistance`.

2. **MAJOR — The existing post-processing runner is scan-14 specific and hardcodes invalid paths.**
   [`m1/post_case.sh:4`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/post_case.sh#L4).
   WORK-ORDER-2026-10-03 §4 requested updating the case template and the end-to-end runner. [`m1/post_case.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/post_case.sh) hardcodes an obsolete directory (`P=/tmp/claude-1000/...`) and package naming patterns specific to scan 14. Before running Task P5, an end-to-end post-processing runner accepting `--pkg-root` and case directories must be provided.

3. **MAJOR — Direct application of the B3 idealized jet-offset diagnostic to Scan-14 real lumen is invalid.**
   [`b3_audit/jet_offset.py:9-12`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/jet_offset.py#L9-L12).
   WORK-ORDER-2026-10-03 §2 step 3 specifies reporting the jet state ("axisymmetric or deflected jet, as in B3"). Scan-14 is a tortuous, non-axisymmetric patient artery where idealized tube symmetry does not exist. A post-solve reporting script must not attempt to use `jet_offset.py`, but must instead diagnose state equivalence via outlet flow distribution, throat Reynolds number ($\text{Re} \approx 123.1$), and 3D centerline-aligned velocity slices.

4. **MINOR — Missing standalone `e0_check.py` dependency in `taskC/pf/`.**
   [`taskC/pf/build_m1_case.py:18`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/build_m1_case.py#L18).
   `build_m1_case.py` executes `import e0_check`. While `e0_check.py` exists in the parent `pf/` directory and will be present once files are installed, running `build_m1_case.py` directly from `taskC/pf/` without `item3_M1_pilot/pf` in `PYTHONPATH` raises `ModuleNotFoundError`. `e0_check.py` should be copied into `taskC/pf/` if `taskC` is to be standalone.

5. **MINOR — `make_manifest.sh` does not exclude Python bytecode or repository artifacts.**
   [`taskC/make_manifest.sh:30`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/make_manifest.sh#L30).
   `make_manifest.sh` scans with `find . -type f`. If `__pycache__`, `.git`, or temporary files are present when the script is invoked, they are hashed and added to `MANIFEST.sha256`. An explicit ignore filter for `__pycache__` and VCS files should be added.

6. **MINOR — Known package geometry risk on P5 package 473 measurement probe.**
   [`taskC/FIX30_REPORT.md:113`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/FIX30_REPORT.md#L113) and [`taskC/pf/probe_sections.py:53-63`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/probe_sections.py#L53-L63).
   Package `473_left_LCX_prox_20mm_60ds__baseline__real` has measurement probe `p011` located immediately at a bifurcation with its normal $45^\circ$ to the centerline tangent. Sizing reaches `h_min`. Once the 3D mesh is created in Task P5, the authoritative mesh check in `probe_sections.py` may reject the box if adjacent vessels intersect it.

---

## 4. Final Verdicts

### (C) Task C: Production Template
**VERDICT: READY WITH CONDITIONS**
*(Condition: When the coordinator installs the template files into `pf/` and `code_from_cfd/`, include `e0_check.py` if packaged standalone, clean any `__pycache__` before running `make_manifest.sh`, and provide an updated generic runner for P5 that does not depend on obsolete scratchpad paths.)*

### (A) Task A: D7 Sensitivity Test
**VERDICT: READY WITH CONDITIONS**
*(Conditions: (1) The two variants `baseline_D7_12p5_resistance` and `baseline_D7_12p5_zoneB_resistance` MUST be solved sequentially, not concurrently, to avoid exceeding host RAM capacity; (2) Reconstructed fields at time 3000 must be verified before purging processor directories; (3) Flow state must be evaluated using anatomical centerline alignment, through-throat Reynolds number, and outlet flow distribution rather than the idealized tube `jet_offset.py`.)*
