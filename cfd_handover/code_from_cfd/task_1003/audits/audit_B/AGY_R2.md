I am running the test suite `tests/test_job.sh` and waiting for it to complete.
I am running `tests/test_pool.py` and waiting for it to complete.
Waiting for `test_pool.py` to finish.
Continuing to wait for `test_pool.py` to finish.
# Pre-Run Audit Round 2: Task B (U3D Re-Runs S25B, S12A, S12B) Tooling

**Audit Reference**: Task B of [WORK-ORDER-2026-10-03.md](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/WORK-ORDER-2026-10-03.md#L72-L77) (Section 3)  
**Round 1 Audits**: [audit_B/SOL.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/SOL.md) and [audit_B/AGY.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/AGY.md)  
**Task Brief & Report**: [OPUS_BRIEF_31.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/OPUS_BRIEF_31.md) and [taskB/FIX31_REPORT.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/FIX31_REPORT.md)  
**Files Audited**:
- Job script: [taskB/u3d_job.sh](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh)
- Verdict classifier: [taskB/u3d_verdict.py](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py)
- Job pool scheduler: [taskB/pool.py](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py)
- Jet diagnostic: [taskB/jet_offset.py](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jet_offset.py)
- Draft manifests: [jobs_draft/u3d_S25B.json](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/u3d_S25B.json), [jobs_draft/u3d_S12A.json](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/u3d_S12A.json), [jobs_draft/u3d_S12B.json](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/u3d_S12B.json)
- Cases under test: [u3d/case_S25B](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S25B), [u3d/case_S12A](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S12A), [u3d/case_S12B](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S12B)
- Pre-registered design: [u3d_check/U3D_CHECK_DESIGN.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/U3D_CHECK_DESIGN.md)

---

## 1. Executive Summary & Verification Matrix

All unit tests provided in [`taskB/tests/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/) were executed in foreground under `nice -n 10` using synthetic mock setups. All suites passed completely (`ALL PASS`). No solvers or MPI processes were run on real cases.

| Verification Item | Requirement / Round-1 Finding | Round-2 Audit Finding | Status |
| :--- | :--- | :--- | :--- |
| **Sol 1: Fail-fast & Reconstruct Guard** | Every step checked; purge `processor*` only after reconstruct verified | Explicit checks on `decomposePar`, `mpirun` (`End` line + final `Time`), `reconstructPar` (`End` line + existence/size of `U,p,phi`), `jet_offset.py`, `u3d_verdict.py`, and `post_level.sh`. Purge happens only at lines 66–67 upon full success. Exit traps catch signals and shell errors. | **RESOLVED** |
| **Sol 2: Task-B Job Manifests** | Missing job files in `pool/jobs/` | Complete draft manifests provided in [`jobs_draft/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/) specifying ranks, RAM, disk, priority, and commands. | **RESOLVED** |
| **Sol 3: Unsafe RAM Concurrency** | S12A (~13.5 GB) + S12B (~15.3 GB) could exceed 27.4 GB host memory | `pool.py` now enforces `ram_committed + ram_gb <= BUDGET` (20.3 GB budget on 27.4 GB host) and checks instantaneous `MemAvailable`. Manifests also strictly serialize via `"after"`. | **RESOLVED** |
| **Sol 4: Shared CSV Corruption** | Concurrent writes to `U3D_sten70_work.csv` | `post_level.sh` wrapped in `flock -w 7200` on `U3D_sten70_work.csv.lock`. Each job atomically writes its own primary record `result_<L>.json`. | **RESOLVED** |
| **Sol 5: 8-Rank Numerical Equivalence** | 8-rank Scotch decomposition vs original 16-rank runs | Explicit equivalence caveat documented in job header, status lines, stdout, and `result_<L>.json` (`equivalence` field). | **RESOLVED** |
| **Sol 6: Jet-State Verdict Recording** | Missing classification and structured recording | [`u3d_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py) implements full classification logic and records verdict, inference, FFR mean/band, and offsets in `result_<L>.json`. | **RESOLVED** |
| **Sol 7 & AGY 5: Hardened FFR Extractor** | Division constant `11998.98/1060` vs exact `11.3198`; missing sanity guards | Uses exact `P_AORTA_KIN = 11.3198` matching [`u3d_analyse.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_analyse.py#L9). Requires exactly one `surfaceFieldValue.dat`, $\ge 100$ rows, finite values, monotonic iterations, and final iteration matching `controlDict` and `build_info.json`. | **RESOLVED** |
| **AGY Condition 1: Strictly Sequential** | S25B $\to$ S12A $\to$ S12B execution | Specified via `"after"` in `jobs_draft/`: S12A waits for S25B; S12B waits for S12A. Enforced by `pool.py`. | **RESOLVED** |
| **AGY Condition 2: Verified Reconstruction** | Ensure reconstructed fields exist before purging slices | Implemented at [`u3d_job.sh:49-67`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh#L49-L67); tested across 11 fault injection modes. | **RESOLVED** |
| **AGY Condition 3: Return Directory** | Prevent default overwrite of frozen `returns/2026-09-24` | Acknowledged in `FIX31_REPORT.md` (Open Point 4); requires setting `U3D_RETURNS_DIR` during final publication. | **RESOLVED (Operational)** |
| **Case Setups Integrity** | Ensure `case_S25B`, `case_S12A`, `case_S12B` unchanged since Round 1 | Verified via filesystem timestamps and directory trees: no case files modified since 11:11/11:20 (pre-Round 1). Cases remain clean and fresh. | **RESOLVED** |

---

## 2. Evaluation of Tooling Fixes & Extensions

### A. Evaluation of `u3d_verdict.py` and the Extension of `U3D_CHECK_DESIGN.md`
The pre-registered protocol in [u3d_check/U3D_CHECK_DESIGN.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/U3D_CHECK_DESIGN.md) was drafted on 2026-10-01 for level S50 (with S25A optional). Opus extended the decision rules to S25B, S12A, and S12B in [`u3d_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py):
1. **Physical & Geometric Stations**: Stations $x = 50.0\text{ mm}$ and $x = 56.5\text{ mm}$ are preserved across all levels. Because the geometry of the stenosis throat ($x = 31.5\text{ mm}$) and post-stenotic vessel is identical across all meshes, probing the core jet at these stations is physically sound.
2. **Deflection & Symmetry Thresholds**: Offset $\le 10.0\ \mu\text{m}$ at both stations for `axisymmetric`; $\ge 30.0\ \mu\text{m}$ at either station for `deflected`. The disjunction for deflected states is conservative and appropriate: deflection at either station indicates broken axisymmetry.
3. **FFR Baselines & Tolerances**: Baselines are taken directly from the official 16-rank deposited dataset ([`returns/2026-09-26/U3D_sten70.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/U3D_sten70.csv)):
   - S25B: `0.791197`
   - S12A: `0.790308`
   - S12B: `0.790418`
   Tolerances ($|d\text{FFR}| \le 1\times 10^{-4}$ for same-state verification; $> 5\times 10^{-4}$ for opposite-state inference) discriminate between the axisymmetric and deflected solution branches while accommodating mesh re-generation discretization jitter.
4. **Pre-registration Protocol Judgment**: The extension is scientifically sound, rigorous, and faithful to the original design principles. Because Opus adhered to task boundaries and did not edit files outside `taskB/`, the study lead / coordinator must formally append this dated extension to [`U3D_CHECK_DESIGN.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/U3D_CHECK_DESIGN.md) before execution starts (see Finding 2).

### B. Evaluation of `pool.py` Process & Resource Management
1. **Crash / Restart Recovery**:
   - Each job runs inside `WRAP` (`setsid`), atomically saving exit code to `jobs/<name>.rc`.
   - The pool maintains `jobs/<name>.pid` recording `pgid`, start jiffies from `/proc/<pid>/stat`, and kernel `boot_id`.
   - On pool startup, any orphan `running` job is verified against `/proc` and its recorded start time. If dead without `.rc`, it is safely classified as `failed rc=lost` instead of hanging or re-executing.
   - Status updates use atomic write-rename (`wr()`).
   - Instance concurrency is guarded with `fcntl.flock` on `jobs/.pool.lock`.
2. **Resource Budgeting**:
   - Ranks are strictly capped: `used + j["ranks"] <= RANKS`.
   - RAM is budgeted against `BUDGET = MemTotal * 0.85 - RESERVE` (20.3 GB). Concurrency between S12A (13.48 GB) and S12B (15.30 GB) is mathematically impossible ($13.48 + 15.30 = 28.78\text{ GB} > 20.3\text{ GB}$).

---

## 3. Numbered Findings

### Finding 1: Running Task A Jobs Preclude Immediate Task B Launch and Pool Replacement
- **Severity**: **MAJOR**
- **Component**: Runtime Environment / Process Contention
- **Description**: The host is currently executing a 16-rank Task A OpenFOAM solve (`A1_D7_12p5`, PID 2713128) under an active instance of the *old* `pool.py` (PID 2713127) started at 11:41:28, with `A2_D7_12p5_zoneB` queued after it.
  1. The host's 16 physical cores are currently 100% occupied by `A1_D7_12p5`. Starting an 8-rank Task B job now would oversubscribe CPU cores ($16 + 8 = 24$ threads) and contend for RAM.
  2. The running Task A job was spawned by the old `pool.py` and lacks `.rc` and `.pid` tracking files. As identified in `FIX31_REPORT.md` (Open Point 7), replacing or restarting `pool.py` while old-pool jobs are active would cause the new pool to erroneously mark `A1_D7_12p5` as `failed rc=lost`.
- **Action Required**: The coordinator must wait until all active Task A jobs complete and the old `pool.py` process terminates before copying [`taskB/pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py) into `/home/azan/paper6_t6_work/pool/` and launching Task B.

---

### Finding 2: Pre-Registration Protocol Extension Must Be Formally Appended to `U3D_CHECK_DESIGN.md`
- **Severity**: **MAJOR**
- **Component**: Governance / Pre-Registration Integrity
- **Description**: [`u3d_check/U3D_CHECK_DESIGN.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/U3D_CHECK_DESIGN.md) was created on 2026-10-01 and pre-registered decision rules for S50 (and S25A). The logic implemented in [`u3d_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py) extends these rules to S25B, S12A, and S12B. To prevent post-hoc bias concerns or audit challenges, the decision rule extension must be formally pre-registered in writing.
- **Action Required**: The study lead or coordinator must append a dated entry to [`U3D_CHECK_DESIGN.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/U3D_CHECK_DESIGN.md) documenting the extension of rules (a)–(d) to levels S25B, S12A, and S12B (with their respective baseline FFR values 0.791197, 0.790308, 0.790418) **before** the first Task B run is initiated.

---

### Finding 3: Coordinator Deployment Steps for Task B Tooling and Manifests
- **Severity**: **MINOR**
- **Component**: Deployment / Staging
- **Description**: The fixes in `taskB/` are staged but require coordinated deployment:
  - [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh) and [`taskB/u3d_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py) are already installed in `/home/azan/paper6_t6_work/pool/` (verified byte-identical).
  - [`pool/pool.py`](file:///home/azan/paper6_t6_work/pool/pool.py) is still the unpatched version from 11:29.
  - Job manifests in [`jobs_draft/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/) have not yet been copied to `/home/azan/paper6_t6_work/pool/jobs/`.
- **Action Required**: Once Task A completes:
  1. Copy [`taskB/pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py) to `/home/azan/paper6_t6_work/pool/pool.py`.
  2. Copy [`jobs_draft/u3d_*.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/) to `/home/azan/paper6_t6_work/pool/jobs/`.
  3. Create the corresponding `.audited` markers in `/home/azan/paper6_t6_work/pool/jobs/`:
     ```bash
     touch /home/azan/paper6_t6_work/pool/jobs/u3d_S25B.audited
     touch /home/azan/paper6_t6_work/pool/jobs/u3d_S12A.audited
     touch /home/azan/paper6_t6_work/pool/jobs/u3d_S12B.audited
     ```

---

### Finding 4: Mandatory Export of `U3D_RETURNS_DIR` for Final Table Publication
- **Severity**: **MINOR**
- **Component**: Pipeline Integration
- **Description**: As noted in Round 1 ([AGY.md Finding 6](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/AGY.md#L85-L93)), [`u3d_returns.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_returns.py#L3) defaults to the frozen directory `/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24`.
- **Action Required**: When post-processing and generating final delivery tables after all Task B runs complete, the operator must explicitly export:
  ```bash
  export U3D_RETURNS_DIR=/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03
  ```

---

VERDICT: READY WITH CONDITIONS
