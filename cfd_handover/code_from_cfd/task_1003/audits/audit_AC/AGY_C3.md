I have launched `test_flow_state_profile.py` in the background and will continue as soon as it completes.
I will wait for `test_flow_state_profile.py` to finish.
I have launched `test_flow_state_sten70.sh` and will continue once it completes.
I have launched `test_p5_stub.py` and will continue once it finishes.
I have launched `test_section_rule.py` and will continue once it finishes.
# Pre-Run Audit Report (Round 3): Task C Post-Solve Runner, Flow-State Diagnostic, and Builder Readiness

**Audit Scope:**
- **Codebase:** [`taskC/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/) after Opus 5.5 task 36 (Attempt 3).
- **Prior Audits:** [`audit_AC/SOL_C2.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_AC/SOL_C2.md) (NOT READY: 3 majors, 1 minor) and [`audit_AC/AGY_C2.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_AC/AGY_C2.md) (READY WITH CONDITIONS).
- **Brief & Design:** [`OPUS_BRIEF_36.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/OPUS_BRIEF_36.md) and pre-registered diagnostic [`taskA/TASK_A_DESIGN.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskA/TASK_A_DESIGN.md).
- **Live Solve Reference:** Read-only inspection and dry testing on [`m1/cases/baseline_D7_12p5_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance) (finishing ~18:30).

---

## 1. Resolution of Round-2 Audit Findings

### 1.1 Sol Finding 1 (MAJOR) & AGY Finding 4 (MINOR) — Package Resolution Roots & Verification
- **Status:** **RESOLVED**
- **Verification:**
  - In [`pf/m1_package.py:10-24`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/m1_package.py#L10-L24), the legacy `/tmp/claude-1000/...` root and fallbacks to `$M1_PKG_ROOT` or `<pilot>/m1/pkg` have been completely removed.
  - Resolution precedence is now strictly: explicit argument / `$PKG_ROOT` alone (no fallback when set); otherwise authoritative Drive roots (`packages/M1`, `packages/P5`), then persistent copy `/home/azan/paper6_t6_work/scratchpad/zipcheck/cfd_handover/packages/M1`.
  - Added [`verify_against_build()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/m1_package.py#L32-L43) and `package-check` step at [`post_case_generic.sh:47-50`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh#L47-L50). This step executes **before any outputs are generated** (step 0b), comparing package name, file set, and SHA-256 hashes of all 8 package files (`outlets.csv`, `bc_A.csv`, `bc_C_flows.csv`, `probes.csv`, `inlet.json`, `centreline.vtp`, `meta.json`, `mask_edit.json`) against `build_info.json["package_hashes"]`.
  - The runner passes the verified absolute path `$PKGDIR` to all downstream steps ([`m1_probes.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/m1_probes.py), [`as_meshed_radius.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/as_meshed_radius.py), [`flow_state_profile.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/flow_state_profile.py)).
  - Tested on live solve `m1/cases/baseline_D7_12p5_resistance`: resolves to `scratchpad/zipcheck/.../14_left_LAD_prox_20mm_80ds__baseline__real`; all 8 file hashes verified identically.

### 1.2 Sol Finding 2 (MAJOR) — Incomplete Profiles Yield `INDETERMINATE`
- **Status:** **RESOLVED**
- **Verification:**
  - Implemented in [`flow_state_profile.py:156-200`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/flow_state_profile.py#L156-L200) according to [`taskA/TASK_A_DESIGN.md:11`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskA/TASK_A_DESIGN.md#L11).
  - The comparator verifies that every station specified by the rule ($s \in [s_{\text{throat}} + 2\text{ mm}, s_{\text{meas}}]$ at 1 mm increments) is present and valid on both sides (`complete = bool(diffs) and not (excluded or unmatched or missing or extra)`).
  - Any invalid section (`section_ok == 0`), missing station, or unmatched station unconditionally yields `verdict = "STATES INDETERMINATE"` and `profile_criterion = "INDETERMINATE"`, even with `--ffr`.
  - The subset maximum over valid stations is reported strictly as `subset_max_vector_diff_INFORMATION_ONLY` alongside `subset_max_exceeds_tol`; it is **never** accepted as `STATES AGREE`.
  - Tested on retained sten70 fields in [`tests/test_flow_state_sten70.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_flow_state_sten70.sh): `case_S50` (exhibiting an invalid polyhedral cut section at $x = 52\text{ mm}$, $s - s_{\text{throat}} = 22\text{ mm}$) vs `smoke_cont` and `a5_arch8` correctly returned `STATES INDETERMINATE`. `a5_arch8` (deflected) vs `smoke_cont` (axisymmetric), having all 26 stations valid, correctly returned `STATES DIFFER` ($\max |\Delta\mathbf{o}| = 0.3617 > 0.03$).

### 1.3 Sol Finding 3 (MAJOR) — Finished-Solve Guard on Log Tail & `endTime`
- **Status:** **RESOLVED**
- **Verification:**
  - Implemented in [`pf/post_helpers.py:41-65`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/post_helpers.py#L41-L65) (`run_completion`):
    1. Inspects the log tail from the final run header (`Build :`, `Exec :`, or `Starting time loop`).
    2. Requires that the last run produced a `Time = <t>` line.
    3. Requires that an exact `End` line follows the last `Time = <t>` line (`i_e > i_t` and `i_e > i_h`).
    4. Rejects any trailing lines after `End` containing run headers, time steps, or `FOAM FATAL`.
    5. Enforces that `<t>` equals `endTime` from `system/controlDict` ($|t - \text{endTime}| \le 10^{-9}$), refusing early stops by `residualControl` or manual interrupts.
  - In [`pf/analyze_case.py:112-114`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/analyze_case.py#L112-L114), added `--require-finished`, which exits with code 4 if `strict.log_finished` (`End` + `Finalising parallel run`) is false. [`post_case_generic.sh:52`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh#L52) unconditionally passes `--require-finished`.
  - Tested on live running solve `m1/cases/baseline_D7_12p5_resistance`: exited with code 1 (`RUN NOT COMPLETE: no line that is exactly 'End'`).
  - Tested in [`tests/test_post_guards.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_post_guards.py): synthetic cases for missing End, appended partial runs, appended headers, premature End before final Time, and early stops were all properly refused.

### 1.4 Sol Finding 4 (MINOR) — Radius Provenance & Reuse Verification
- **Status:** **RESOLVED**
- **Verification:**
  - Implemented in [`pf/post_helpers.py:270-293`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/post_helpers.py#L270-L293) (`mesh_hash`, `radius_check`, `radius_commit`).
  - `mesh_hash()` computes a SHA-256 over all files in `constant/polyMesh` (name + streamed contents).
  - Existing radius files are reused at [`post_case_generic.sh:69-70`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh#L69-L70) **only** if `<prefix>_provenance.json` records matching mesh SHA-256, package file hashes, and un-tampered output hashes.
  - If any hash differs or provenance is missing, radius files are regenerated and a new provenance file is committed.
  - Overrides: `POST_FORCE=1` forces regeneration; `POST_REUSE_UNCHECKED=1` explicitly waives provenance check and logs `REUSED UNCHECKED` to `post_summary.json`. Provenance JSON is recorded among the hashed outputs.

---

## 2. Test Suite & Verification Results

All solver-free unit and regression tests executed cleanly with zero errors:
- [`python3 -B taskC/tests/test_b1_settle.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_b1_settle.py): **PASS** (B1 settled rules and floor iterations verified).
- [`bash taskC/tests/test_manifest.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_manifest.sh): **PASS** (LF/CRLF normalisation and tamper detection verified).
- [`bash taskC/verify_manifest.sh taskC`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/verify_manifest.sh): **PASS** (`99 OK, 0 FAILED/MISSING`, zero untracked files).
- [`python3 -B taskC/tests/test_post_guards.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_post_guards.py): **PASS** (all 10 completion, package resolution/tampering, and radius provenance scenarios passed).
- [`python3 -B taskC/tests/test_flow_state_profile.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_flow_state_profile.py): **PASS** (analytic straight and oblique tube checks, frame independence, INDETERMINATE triggers).
- [`bash taskC/tests/test_flow_state_sten70.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_flow_state_sten70.sh): **PASS** (`case_S50` polyhedral cut station flagged; `STATES INDETERMINATE` asserted; `a5_arch8` vs `smoke_cont` `STATES DIFFER`).
- [`python3 -B taskC/tests/test_p5_stub.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_p5_stub.py): **PASS** (all 5 P5 packages validated; package 473 relocation to node 646 verified).
- [`python3 -B taskC/tests/test_section_rule.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/tests/test_section_rule.py): **PASS** (rules S1–S4 evaluated on scan-14 real mesh).
- Live solve dry check on [`baseline_D7_12p5_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/m1/cases/baseline_D7_12p5_resistance):
  - `post_helpers.py finished`: refused incomplete run with exit code 1.
  - `post_helpers.py package-check`: verified package hashes against `build_info.json`.
  - `post_helpers.py fill`: discovered geometry and mesh gates successfully from hard-linked mesh inode.

---

## 3. Numbered Findings

### 1. MINOR — Explicit `REF_FFR` Environment Variable Required for Acceptance Comparison
- **Location:** [`taskC/post_case_generic.sh:23-25`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh#L23-L25), [`taskC/pf/post_helpers.py:255-263`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/post_helpers.py#L255-L263)
- **Description:** `post_helpers.py summary` checks `os.environ.get("REF_FFR")`. If unset, `post_summary.json` outputs `"reference_comparison": "not requested (set REF_FFR)"`.
- **Condition / Recommendation:** When post-processing the upcoming Task A1 solve, the coordinator must invoke the runner with `REF_FFR=0.8697574904997768` (e.g., `REF_FFR=0.8697574904997768 bash taskC/post_case_generic.sh ...`) to ensure the acceptance evaluation $|\Delta\text{FFR}| < U_{\text{3D}} = 0.00055$ is recorded in `post_summary.json`.

### 2. MINOR — Host RAM Contention Boundary Between Post-Runner and Solves
- **Location:** [`taskC/post_case_generic.sh:53-61`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/post_case_generic.sh#L53-L61), [`taskC/TEMPLATE_README.md:55`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/TEMPLATE_README.md#L55)
- **Description:** Reconstruction and pyvista mesh slicing on a 6.2M cell mesh (A1) require ~2–4 GB peak RAM. Host available memory is 24 GB. An active 16-rank solve consumes ~14 GB (A1) or ~18 GB (A2). Running `post_case_generic.sh` concurrently with an active A2 solve would exceed physical host memory.
- **Condition / Recommendation:** The coordinator must post-process A1 strictly after A1 completes (~18:30) and before launching A2, or after both solves finish sequentially.

### 3. MINOR — Pre-registered Flow-State Classification on Polyhedral Cut Sections
- **Location:** [`taskC/flow_state_profile.py:186-195`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/flow_state_profile.py#L186-L195), [`taskA/TASK_A_DESIGN.md:11`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskA/TASK_A_DESIGN.md#L11)
- **Description:** In accordance with the pre-registered specification, if any cross-section cut in either A1 or A2 exhibits holes $\ge 0.5\%$ (typically caused by VTK slicing across cfMesh transition polyhedra), the comparison verdict will be `STATES INDETERMINATE`. The subset statistic is reported for informational purposes only.
- **Condition / Recommendation:** If polyhedral cuts occur in A1 or A2, the comparison will report `STATES INDETERMINATE` as required by the pre-registration protocol; no ad-hoc substitution should be made without coordinator concurrence prior to reviewing results.

### 4. MINOR — P5 Package 473 3D Mesh Gate Remains Pending Volume Mesh Generation
- **Location:** [`taskC/pf/probe_sections.py:275-294`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskC/pf/probe_sections.py#L275-L294)
- **Description:** Centerline checks (S1/S2) deterministically relocated package 473 probe `p011` to tree node 646 (+2.853 mm). Rules S3/S4 (mesh component and section area bounds) will be evaluated when the 3D volume mesh is generated by `taskP5/`.
- **Condition / Recommendation:** Build P5 case 473 with default `mesh_check=True`. The builder will safely refuse the case (`SystemExit`) if node 646 fails on the volume mesh.

---

VERDICT: READY WITH CONDITIONS
