### Round 2 Pre-Run Audit Report: Work Order 2026-10-10 Setup

**Audited Workspace:** `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010`  
**Auditor Model:** Gemini 3.7 Flash  
**Governing Documents:**
- [`WORK-ORDER-2026-10-10.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/WORK-ORDER-2026-10-10.md)
- [`WORK-ORDER-2026-10-03.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/WORK-ORDER-2026-10-03.md)
- [`PROMPT_R1.txt`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/audit/PROMPT_R1.txt) / [`PROMPT_R2.txt`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/audit/PROMPT_R2.txt)
- Round 1 Audits: [`SOL_R1.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/audit/SOL_R1.md), [`AGY_R1.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/audit/AGY_R1.md)

---

### Part 1: Status of Round-1 Audit Findings

1. **Prescribed-flow jobs rejected by `case_job.sh` (Round 1 Blocker):**
   - **Status:** **RESOLVED**
   - **Evidence:** [`wo1010/case_job.sh#L44-L83`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/case_job.sh#L44-L83) implements `case_mode()` and `prescribed_check()`. For prescribed cases, it verifies `flowRateOutletVelocity` matches `Q_target_m3s` (rel tol $10^{-9}$), `0/p` has `type zeroGradient;`, and no coded BCs exist. Serial smoke verifies `Time = 2`, exact `End`, and confirms `dynamicCode` is absent ([`wo1010/case_job.sh#L263-L264`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/case_job.sh#L263-L264)). For resistance mode, behavior is byte-for-byte identical to `lane2/case_job.sh`. Self-test passed 18/18 completion checks and 11/11 prescribed BC checks. Dry run on `14_T5w_prescribed` succeeded with rc 0. [`wo1010/make_job.py#L30`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/make_job.py#L30) points to `wo1010/case_job.sh`.

2. **Task G iterations table missing probe FFRs (Round 1 Major):**
   - **Status:** **RESOLVED**
   - **Evidence:** In [`wo1010/taskG.py#L21-L33`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L21-L33) and [`#L46-L52`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L46-L52), `taskG.py` parses `p_over_Paorta` for all 29 probes from [`M1_probes_T1_missed_branch_resistance.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_probes_T1_missed_branch_resistance.csv) for $k_1$ and from `<out>/M1_probes_14_T1regen_G<n>_resistance.csv` for $k_n$. Columns `FFR_<probe_id>` are recorded in `taskG_iterations.csv` and `.json`. Verified via `python3 taskG.py --plan-only`.

3. **Task G execution order and missing D14 job (Round 1 Major):**
   - **Status:** **RESOLVED**
   - **Evidence:** [`wo1010_pool/jobs/taskG_14_T1regen.json#L8-L14`](file:///home/azan/paper6_t6_work/wo1010_pool/jobs/taskG_14_T1regen.json#L8-L14) defines `after` with all five Task T jobs (`14_T5n_resistance`, `14_T5n_prescribed`, `14_T5w_resistance`, `14_T5w_prescribed`, `14_T5n_12p5_resistance`). [`wo1010_pool/jobs/14_T5n_12p5_resistance.json`](file:///home/azan/paper6_t6_work/wo1010_pool/jobs/14_T5n_12p5_resistance.json) is generated with priority 1 and declared RAM 9.1 GB.

4. **Task G partial solve acceptance and interruption handling (Round 1 Major):**
   - **Status:** **RESOLVED**
   - **Evidence:** [`wo1010/taskG.py#L75-L85`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L75-L85) `check(n)` verifies `post_summary` verdict is `CONVERGED`, `run_completion.ok` is true, no `missing_outputs`, and verifies the SHA-256 of `M1_outlets_*.csv`. Unaccepted attempts are moved to `cases/_failed/<name>_<ts>` and retried once ([`wo1010/taskG.py#L102-L110`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L102-L110)). Completed but unconverged solves stop the driver with exit 3 and refer to D15 fallback instead of deterministic re-solving ([`wo1010/taskG.py#L100`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L100)).

5. **D15 pimpleFoam transient fallback absent (Round 1 Major):**
   - **Status:** **RESOLVED**
   - **Evidence:** [`wo1010/pimple_fallback.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/pimple_fallback.py) implements `check`, `build`, `run`, and `analyse`. Triggers fail-safe on B1/D8 settle criterion (`iter_permanently_settled`, `iterations_run == 3000`). Builds case from reconstructed steady fields with hard-linked mesh (`boundary` copied to prevent corruption), explicit lag resistance BC $p = (P_v + R Q)/\rho$ without relaxation device, constant flow rate for prescribed mode, backward ddt, PISO mode, maxCo 0.8. Window $T_{window} = 6 \tau_{jet}$ averaged over second half $[T/2, T]$.

6. **Task finalisation products and baseline comparisons absent (Round 1 Major):**
   - **Status:** **RESOLVED**
   - **Evidence:** [`wo1010/finalise_task.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/finalise_task.py) implements generation of `summary_<Task>.csv`, `code_provenance_<Task>.csv`, `NOTE.md`, `INDEX.csv`, and LF-normalised `MANIFEST.sha256` via `make_manifest.sh`. Handles baseline comparisons across Task T (M1 baselines + D14 vs A1 / 14_T5n), Task G ($k_1 = 1$), Task M & T2 (P5 baselines with explicit note on prescribed mode lack of baselines), and Task N (306 baseline). Re-issued files receive `_<date>` suffixes; existing files are never overwritten.

7. **Concurrent meshing memory race and unbudgeted RAM (Round 1 Major):**
   - **Status:** **RESOLVED**
   - **Evidence:** [`wo1010/run_geom_mesh.sh#L37-L50`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/run_geom_mesh.sh#L37-L50) serialises mesh admission across queue workers via `flock` on `mesh_admit.lock`, held until `cartesianMesh` has run for 120 s or exited. Fails closed with exit 1 if resources remain unavailable after timeout. Pool restarted with `--ranks 32 --reserve-gb 8`, giving a solve RAM budget of 15.3 GB ($27.4 \times 0.85 - 8.0$), leaving 12.1 GB headroom for meshing and system services. Live verification in [`wo1010/runs.log`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/runs.log) shows `473_T5w` waited 220 s while `473_T5n` meshed before being admitted.

8. **Reusing $k_1$ on regenerated mesh, Task G numerical guards, `--r-scale`:**
   - **Status:** **CONFIRMED & RESOLVED**
   - Mesh equivalence of `14_T1regen` to returned 2026-09-26 mesh remains verified. [`wo1010/taskG.py#L43-L68`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L43-L68) includes guards for non-positive territory flows, coincident $k$ ($|\Delta \log k| \le 10^{-9}$), and edge-of-bracket argmin detection.

---

### Part 2: Numbered Findings

#### Finding 1: Propagation of geometry relative-throat gate exit 3 (`D2_RELATIVE_THROAT_GATE_FAIL`) into `M1_results.csv` and returns verified
- **Severity:** **MINOR (Confirmation & Pipeline Verification)**
- **Evidence:**
  - Cases `139_T1`, `473_T5n`, `473_T5w`, and `306_base` logged exit code 3 from `build_m1_geometry.py` (`REJECTED: relative as-built throat differs from radial_scale by more than 1 %`), e.g. in [`wo1010/logs/geometry_139_T1.log#L36`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/logs/geometry_139_T1.log#L36) and [`wo1010/out/139_T1/gates.json#L1425`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/out/139_T1/gates.json#L1425) (`lesion_relative_throat_gate: false`).
  - Analysis of [`pf/post_helpers.py#L204-L227`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/pf/post_helpers.py#L204-L227) confirms:
    - `"lesion_relative_throat_gate"` is in `GATES_DECISIVE`; its `false` value sets `geometry_step_ok = False`.
    - Maps to flag `"D2_RELATIVE_THROAT_GATE_FAIL"` in [`post_helpers.py#L183`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/pf/post_helpers.py#L183).
    - Populates `fill.json`, which is read by [`pf/m1_results.py#L96-L107`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/pf/m1_results.py#L96-L107) into `M1_results.csv` (`geometry_step_ok: False`, `flags: D2_RELATIVE_THROAT_GATE_FAIL;...`).
    - [`wo1010/finalise_task.py#L228-L230`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/finalise_task.py#L228-L230) extracts `geometry_step_ok` and `flags` into `summary_<Task>.csv` and `NOTE.md`.
  - Solves proceed flagged per Work Order §1 D11 and 09-24 §1 ("Do not repair surfaces. A case that fails a gate is still solved and returned, flagged").

#### Finding 2: High computational cost of D15 pimpleFoam fallback (30–40 h at 16 ranks) is safeguarded by manual invocation design
- **Severity:** **MINOR (Operational Risk Confirmation)**
- **Evidence:**
  - In [`wo1010/pimple_fallback.py#L40-L42`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/pimple_fallback.py#L40-L42), the 6 $\tau_{jet}$ physical window requires ~25,000–30,000 steps at $dt \approx 4 \times 10^{-6}$ s, taking 30–40 wall-clock hours per fallback solve at 16 ranks.
  - Crucially, `pimple_fallback.py` is **not** chained automatically into `case_job.sh` or `taskG.py`. In [`wo1010/taskG.py#L100`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/wo1010/taskG.py#L100), an unconverged solve halts the driver with exit code 3, preventing uncontrolled consumption of CPU resources without explicit operator intervention.

#### Finding 3: Pool jobs for subsequent Tasks M, T2, and N are not yet generated
- **Severity:** **MINOR (Workflow Sequencing)**
- **Evidence:**
  - Directory [`wo1010_pool/jobs/`](file:///home/azan/paper6_t6_work/wo1010_pool/jobs/) contains only the five Task T jobs and `taskG_14_T1regen.json`.
  - While meshes for Task M (`138_T1`, `69_T1`, `473_T1`, `139_T1`) and Task T2 (`138_T5n`, `138_T5w`, `473_T5n`, `473_T5w`) are complete, jobs have not yet been generated with `make_job.py`. Meshing for Task N (`306_base` etc.) is in progress.
  - Per Work Order §4 order ($T \rightarrow G \rightarrow M \rightarrow T2 \rightarrow N$), these jobs should only be generated and queued once Task T and Task G are in progress or completed.

---

### Part 3: Concrete Actions Before Marking Jobs `.audited`

To launch the current launch set:
1. **Task T (Launch Set 1):**
   No further code or configuration changes are required. Mark all five Task T jobs as audited:
   ```bash
   touch /home/azan/paper6_t6_work/wo1010_pool/jobs/14_T5n_resistance.audited
   touch /home/azan/paper6_t6_work/wo1010_pool/jobs/14_T5n_prescribed.audited
   touch /home/azan/paper6_t6_work/wo1010_pool/jobs/14_T5w_resistance.audited
   touch /home/azan/paper6_t6_work/wo1010_pool/jobs/14_T5w_prescribed.audited
   touch /home/azan/paper6_t6_work/wo1010_pool/jobs/14_T5n_12p5_resistance.audited
   ```
2. **Task G (Launch Set 2):**
   `taskG_14_T1regen.json` strictly declares `after` dependencies on the five Task T jobs. You may either:
   - Mark `taskG_14_T1regen.json.audited` immediately; `pool.py` will hold it until all five Task T jobs achieve status `done`.
   - (Recommended) Wait until the five Task T jobs complete and are verified, then mark `taskG_14_T1regen.json.audited`.
3. **Tasks M, T2, N (Launch Set 3):**
   - Wait for Scan 306 meshing to complete.
   - Run `make_job.py` for each package to generate pool job JSONs.
   - For Task N, ensure `306_base_resistance` runs and completes first before launching the remaining 6 solves.

---

### VERDICT

- **Task T (the five `14_T5*` pool jobs):** **READY**
- **Task G (`taskG_14_T1regen`):** **READY WITH CONDITIONS** *(Ready for `.audited` marker; start is conditionally gated by pool on completion of all five Task T jobs)*
- **Later Tasks M / T2 / N:** **NOT READY** *(Meshing in progress for Scan 306; pool job JSON files not yet generated)*
