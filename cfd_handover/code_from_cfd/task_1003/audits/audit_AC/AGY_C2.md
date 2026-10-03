# Pre-Run Audit Report (Round 2): Task C & Task A Post-Solve Readiness

**Audit Scope & Staging:**
- **Codebase:** [`taskC/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/) (Attempt 2 changes following Opus 5.5 Task 33).
- **Deliverables Audited:** [`post_case_generic.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh), [`flow_state_profile.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/flow_state_profile.py), [`pf/post_helpers.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/post_helpers.py), [`pf/probe_sections.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/probe_sections.py), [`pf/build_m1_case.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/build_m1_case.py), [`pf/pf_common.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/pf_common.py), [`pf/m1_probes.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/m1_probes.py), [`pf/as_meshed_radius.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/as_meshed_radius.py), [`pf/m1_results.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/m1_results.py), [`pf/sections.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/sections.py), [`pf/analyze_case.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/analyze_case.py), [`b1_settle.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/b1_settle.py), [`make_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/make_manifest.sh), [`verify_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/verify_manifest.sh), and the test suite under [`tests/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/).
- **Live Reference:** Running 16-rank solve [`m1/cases/baseline_D7_12p5_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance) (audited read-only).

---

## 1. Resolution of Round-1 Audit Findings

### 1.1 Sol Finding 1 (C) & Sol Finding 5 (A) [BLOCKERS] — End-to-End Post Runner
- **Status:** **RESOLVED**
- **Verification:** [`taskC/post_case_generic.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh) delivers a completely package-driven runner with usage:
  `post_case_generic.sh <case_dir> <package_dir_or_name> <label> <mode> <out_dir>`.
- The runner removes all hard-coded `/tmp/claude...` roots, deriving `$P` from environment or defaulting to `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot`, and resolves helpers via `<script_dir>/pf` or `$P/pf`.
- It executes a strict sequence stopping on any failure:
  1. `post_helpers.py finished`: verifies exact `End` in `log.simpleFoam` (tested against the active D7 solve; correctly refused with exit code 1).
  2. Strict analysis via [`analyze_case.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/analyze_case.py) without importing the 0D twin.
  3. `reconstructPar -latestTime` (ESI v2406), followed immediately by `post_helpers.py reconstruct-check` verifying processor0's latest time matches case, $U$ and $p$ fields are present and non-empty, and `log.reconstructPar` ends with `End`.
  4. Preserves all processor directories and reconstructed fields (**no purge command** exists in `post_case_generic.sh`).
  5. Generates `M1_probes.csv` (all package probes + relocated row when applicable), `as_meshed_radius` contract files (`.csv`, `_inscribed.csv`, `_detail.csv`), fill JSON (discovering gates through hard-link owner inodes and extension source), `M1_outlets.csv`, `M1_results.csv`, monitor history (`M1_monitor_history.csv/.json`), `settle.csv` (B1 settle logic), `flow_state.csv/.json`, and `post_summary.json`.

### 1.2 Sol Finding 2 (C) & AGY Finding 6 (C) [MAJOR / MINOR] — Strict Measurement Section Rule & Package 473 Handling
- **Status:** **RESOLVED**
- **Verification:** Implemented in [`pf/probe_sections.py:171-294`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/probe_sections.py#L171-L294) and [`pf/build_m1_case.py:47-68`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/build_m1_case.py#L47-L68).
- **Rule Formulation:**
  - **S1:** Normal within $20^\circ$ of the local centerline tangent.
  - **S2:** No bifurcation within $1.5 r_{\text{ref}}$ along the vessel path (all nodes degree 2).
  - **S3:** Mesh check passes (exactly 1 connected component in the box, $\ge 0.5$ cell margins, no other vessel inside).
  - **S4:** Bounded section area satisfies $1/1.6 \le A / (\pi r_{\text{ref}}^2) \le 1.6$.
- **Package 473 Assessment:** In `test_section_rule.py` and `test_p5_stub.py`, package `473_left_LCX_prox_20mm_60ds__baseline__real` probe `p011` fails S1 ($36.6^\circ > 20^\circ$) and S2 (degree-3 node 424 at $-0.84\text{ mm} < 1.30\text{ mm}$). It is flagged `FAILED_SECTION_RULE` (never silently accepted) and deterministically relocated to tree node 646 at $+2.853\text{ mm}$ (rejecting candidate nodes 643, 644, 645 due to vessel clearance and 424, 423, 422 due to S2).
- When built, `measurementP` monitors the relocated section, while `measurementOrigP` monitors the original probe only if its bounded box passes the 3D mesh check. `build_info.json` records `measurement_section_rule`, `measurement_probe_used`, and `measurement_probe_relocated`. Package source files are unaltered.

### 1.3 Sol Finding 3 (C) & AGY Finding 5 (C) [MINOR] — Manifest Scripts & Bytecode Exclusion
- **Status:** **RESOLVED**
- **Verification:** [`make_manifest.sh:30`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/make_manifest.sh#L30) and [`verify_manifest.sh:24`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/verify_manifest.sh#L24) now explicitly prune `__pycache__` and `.git`, and exclude `*.pyc` files from manifest generation and extra-file checks.
- Running [`verify_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/verify_manifest.sh) over [`taskC/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/) returned `88 OK, 0 FAILED/MISSING` with zero unlisted files. [`tests/test_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_manifest.sh) verified LF, CRLF, and tamper behaviors cleanly.

### 1.4 Sol Finding 7 (A) [MAJOR] — Acceptance Reference Comparison Statistic
- **Status:** **RESOLVED**
- **Verification:** Implemented in [`pf/post_helpers.py:213-226`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/post_helpers.py#L213-L226).
- Compares like-with-like: the reconstructed iteration-3000 `p011` measurement section $p/\text{P}_{\text{aorta}}$ from `M1_probes.csv` against the returned reference value `0.8697574904997768` ([`returns/2026-09-26/M1_probes_baseline_resistance.csv:14`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_probes_baseline_resistance.csv#L14)).
- Evaluates $|\Delta\text{FFR}| < U_{\text{3D}} = 0.00055$.
- `measurementP` last-100 mean is recorded separately for B1 settle analysis and is not conflated with the acceptance comparison.

### 1.5 Sol Finding 8 (A) & Sol Round-2 Finding 3 (A) [MAJOR / MINOR] — Flow-State Diagnostic & Specification Ambiguities
- **Status:** **RESOLVED**
- **Verification:** Implemented in [`flow_state_profile.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/flow_state_profile.py) according to [`taskA/TASK_A_DESIGN.md:11`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskA/TASK_A_DESIGN.md#L11).
- **Deterministic Frame:** Uses double-reflection rotation-minimizing transport (Wang et al. 2008) along the centerline stations (1 mm spacing from throat + 2 mm to measurement probe). Initial normal $N$ is seeded by the Frenet curvature normal if curvature $\kappa > 0.02\text{ mm}^{-1}$, else the global axis least aligned with the tangent. Frame orientation depends strictly on the centerline geometry, ensuring shared frames between solves.
- **Transverse Offset Metric:** Profile comparison evaluates the Euclidean vector difference of the signed transverse offset vectors:
  $$|\mathbf{o}_A - \mathbf{o}_B| = \sqrt{(o_{N,A} - o_{N,B})^2 + (o_{B,A} - o_{B,B})^2} \le 0.03$$
  It also logs scalar magnitude difference $||\mathbf{o}_A| - |\mathbf{o}_B||$ for reference.
- **Invalid Sections:** Sections exhibiting hole area $\ge 0.5\%$ (e.g. VTK cutting artifacts across cfMesh transition polyhedra) or centroid offset $\ge 0.5 r_{\text{eq}}$ are flagged `section_ok = 0`, excluded from profile comparison, and listed in `stations_excluded_invalid` to prevent false difference classifications.
- **Conjunction Decoupling:** Reports `profile_criterion` (`AGREE`/`DIFFER`) and `ffr_criterion` (`AGREE`/`DIFFER`) separately, with the combined `STATES AGREE` label requiring both.
- **Verification Tests:**
  - Synthetic tube analytic test: verified $a/4 = 0.1$ offset reproduced to $< 0.0001$ on aligned and oblique tubes;
  - Retained sten70 cases: `smoke_cont` vs `case_S50` yielded `STATES AGREE` (max vector diff 0.0026); `a5_arch8` (deflected) vs `smoke_cont` and `case_S50` correctly yielded `STATES DIFFER` (max vector diff 0.362 and 0.364). Station $x = 52\text{ mm}$ was properly detected as a polyhedral cut artifact and excluded.

---

## 2. Safety and Compatibility with Running Task A Solve

- **Live Solve Status:** Case [`m1/cases/baseline_D7_12p5_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance) was inspected read-only at iteration ~470.
  - Bounded monitors are active and functional:
    - `throatFlux` and `throatP` sampled area: $2.39125 \times 10^{-7}\text{ m}^2$ ($0.239\text{ mm}^2$, matching single lumen).
    - `measurementFlux` and `measurementP` sampled area: $3.36955 \times 10^{-6}\text{ m}^2$ ($3.370\text{ mm}^2$, matching single lumen).
  - Residuals and pressure fields are stable.
- **Post-Runner Compatibility:**
  - Tested `post_helpers.py finished` on the active case: exited with code 1, correctly refusing an incomplete run.
  - Tested `post_helpers.py fill`: discovered geometry gates from the build's extension JSON source (`m1/out/baseline/gates.json`) and mesh gates via hard-linked owner inode (`m1/mesh/baseline_D7_12p5/mesh_gates.json`). Extracted cell count 6,241,438 and throat cells across 66.
  - Tested `post_helpers.py history` on current iteration data: parsed all 4 monitors across 447 time steps without error.
  - Tested `b1_settle.py`: evaluated iterations 1–451 and reported `B1` status.
  - Tested `analyze_case.py`: strict check executed without error, generating expected intermediate diagnostics.

---

## 3. Numbered Findings

### 1. MINOR — Explicit `REF_FFR` Environment Variable Required for Acceptance Automation
- **Location:** [`taskC/post_case_generic.sh:18-20`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh#L18-L20) and [`taskC/pf/post_helpers.py:217-225`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/post_helpers.py#L217-L225)
- **Description:** In [`pf/post_helpers.py:217`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/post_helpers.py#L217), `reference_comparison` checks `os.environ.get("REF_FFR")`. If unset, `post_summary.json` outputs `"reference_comparison": "not requested (set REF_FFR)"`.
- **Condition / Recommendation:** When post-processing the Task A solves, the coordinator must invoke the runner with `REF_FFR=0.8697574904997768` (e.g., `REF_FFR=0.8697574904997768 bash taskC/post_case_generic.sh ...`) to ensure the acceptance evaluation against the returned baseline value is recorded in `post_summary.json`.

### 2. MINOR — Post-Processing Host RAM Contention Boundary
- **Location:** [`taskC/post_case_generic.sh:55`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh#L55) and [`taskC/TEMPLATE_README.md:55`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/TEMPLATE_README.md#L55)
- **Description:** Slicing the 6.2M cell mesh during `m1_probes.py`, `as_meshed_radius.py`, and `flow_state_profile.py` requires ~2–4 GB peak RAM. Host available memory is ~23 GiB. While a finished case leaves plenty of headroom when run alone, running `post_case_generic.sh` on A1 concurrently while A2 (8.3M cells, consuming ~18 GB) is actively solving would push peak RAM over host capacity (> 24 GiB).
- **Condition / Recommendation:** Run `post_case_generic.sh` on A1 strictly after A1 finishes and before launching A2, or after both solves finish sequentially.

### 3. MINOR — P5 Package 473 Relocated Section 3D Mesh Gate Remains Pending
- **Location:** [`taskC/pf/probe_sections.py:275-294`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/probe_sections.py#L275-L294) and [`taskC/FIX30_REPORT.md:284-286`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/FIX30_REPORT.md#L284-L286)
- **Description:** The relocation of package 473 measurement probe from `p011` to tree node 646 (+2.853 mm) passes centerline rules S1 and S2. Verification of rules S3 and S4 (bounding box mesh component and area bounds) requires the actual 3D volume mesh for P5 case 473, which is currently being built by the parallel geometry task.
- **Condition / Recommendation:** When building the production case for P5 package 473, execute with default mesh checking (`mesh_check=True`) so that S3/S4 are confirmed on the generated mesh. If node 646 were to fail S3/S4, the builder is programmed to refuse the case (`SystemExit`).

### 4. MINOR — Obsolete Fallback Path in `m1_package.py`
- **Location:** [`taskC/pf/m1_package.py:10`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/m1_package.py#L10)
- **Description:** `ZIP_PKG_ROOT` is assigned a legacy path (`/tmp/claude-1000/...`).
- **Impact:** Harmless, as [`resolve_pkg_root`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/m1_package.py#L17) filters with `if c and os.path.isdir(c)`. The path is ignored. It can be cleaned up during final installation to `code_from_cfd/`.

---

## 4. Test Suite Summary

All pure-Python and manifest tests executed cleanly in `taskC`:
- `python3 -B taskC/tests/test_b1_settle.py`: **PASS** (all settle and proxy conditions verified).
- `python3 -B taskC/tests/test_section_rule.py`: **PASS** (Part A centerline on 6 packages; Part B on 3.66M real mesh).
- `python3 -B taskC/tests/test_p5_stub.py`: **PASS** (all 5 P5 packages validated; package 473 relocation asserted).
- `python3 -B taskC/tests/test_flow_state_profile.py`: **PASS** (analytic straight and oblique tube checks).
- `bash taskC/tests/test_manifest.sh`: **PASS** (LF, CRLF, tamper, and cache exclusions verified).
- Flow-state sten70 verification on retained fields: **PASS** (`smoke_cont` vs `case_S50` agreed; `a5_arch8` deflected separated).
- `verify_manifest.sh taskC`: **PASS** (`88 OK, 0 FAILED/MISSING`).

---

VERDICT: READY WITH CONDITIONS
