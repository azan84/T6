I have launched `test_job.sh` and will wait for it to complete.
I have launched `test_pool.py` and will wait for it to complete.
# Pre-Run Audit Round 3: Task B (U3D Re-Runs S25B, S12A, S12B) Tooling

**Audit Reference**: Task B of [WORK-ORDER-2026-10-03.md](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/WORK-ORDER-2026-10-03.md#L72-L77) (Section 3)  
**Round 1 Audits**: [audit_B/SOL.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/SOL.md) and [audit_B/AGY.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/AGY.md)  
**Round 2 Audits**: [audit_B/SOL_R2.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/SOL_R2.md) (NOT READY, 4 majors) and [audit_B/AGY_R2.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/audit_B/AGY_R2.md) (READY WITH CONDITIONS)  
**Task Briefs & Reports**: [OPUS_BRIEF_31.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/OPUS_BRIEF_31.md), [OPUS_BRIEF_34.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/OPUS_BRIEF_34.md), and [taskB/FIX31_REPORT.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/FIX31_REPORT.md) (Attempt 1 & 2)  
**Files Audited**:
- Job script: [taskB/u3d_job.sh](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh) (SHA256: `aed3f7a75bb81302c24957b0d991c634b1dec744c6bba4daf7e69ceb08ef1bda`)
- Verdict classifier: [taskB/u3d_verdict.py](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py) (SHA256: `05fa52cb8dae7872ba012b0151712186225d5d43dc6e3874f78a83dbd9c54e1b`)
- Job pool scheduler: [taskB/pool.py](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py) (SHA256: `fc5c64ed2e5b03ff34ae058e1dc6f7d8db11493ddf81320b4a39532c12369f14`)
- Jet diagnostic: [taskB/jet_offset.py](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jet_offset.py) (SHA256: `b5d411b35d1da1191c971c4c1c7dcabd84c124563d64101218ac279a3c45eb1a`)
- Draft manifests: [jobs_draft/u3d_S25B.json](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/u3d_S25B.json), [jobs_draft/u3d_S12A.json](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/u3d_S12A.json), [jobs_draft/u3d_S12B.json](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/u3d_S12B.json)
- Cases under test: [u3d/case_S25B](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S25B), [u3d/case_S12A](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S12A), [u3d/case_S12B](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/case_S12B)
- Pre-registered design: [u3d_check/U3D_CHECK_DESIGN.md](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/U3D_CHECK_DESIGN.md) (with dated extension of 2026-10-03)

---

## 1. Executive Summary & Verification Matrix

All unit test suites in [`taskB/tests/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/) were executed in foreground under `nice -n 10` using synthetic mock setups (zero solvers or MPI processes run on real cases):
- [`test_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_verdict.py): 57 passed, 0 failed (`ALL PASS`)
- [`test_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_job.sh): 21 passed, 0 failed (`ALL PASS`)
- [`test_pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/tests/test_pool.py): 26 passed, 0 failed (`ALL PASS`)

Every finding and condition from Round 1 and Round 2 has been comprehensively audited and resolved:

| Verification Item | Source Requirement / Prior Finding | Round 3 Audit Findings & Evidence | Status |
| :--- | :--- | :--- | :--- |
| **Sol 1: Fail-fast & Reconstruct Guard** | Every step checked; purge `processor*` only after reconstruct verified | Explicit checks on `decomposePar`, `mpirun` (`End` line + final `Time`), `reconstructPar` (`End` line + existence/size of `U,p,phi`), `jet_offset.py`, `u3d_verdict.py`, and `post_level.sh`. Purge happens only at lines 66–67 upon full success. Exit traps catch signals and shell errors. | **RESOLVED** |
| **Sol 2: Task-B Job Manifests** | Missing job files in `pool/jobs/` | Complete draft manifests provided in [`jobs_draft/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/) specifying ranks, RAM, disk, priority, and commands. | **RESOLVED** |
| **Sol 3: Unsafe RAM Concurrency** | S12A (~13.5 GB) + S12B (~15.3 GB) could exceed 27.4 GB host memory | `pool.py` enforces `ram_committed + ram_gb <= BUDGET` (20.3 GB budget on 27.4 GB host) and checks instantaneous `MemAvailable`. Manifests also strictly serialize via `"after"`. | **RESOLVED** |
| **Sol 4: Shared CSV Corruption** | Concurrent writes to `U3D_sten70_work.csv` | `post_level.sh` wrapped in `flock -w 7200` on `U3D_sten70_work.csv.lock`. Each job atomically writes its own primary record `result_<L>.json`. | **RESOLVED** |
| **Sol 5: 8-Rank Numerical Equivalence** | 8-rank Scotch decomposition vs original 16-rank runs | Explicit equivalence caveat documented in job header, status lines, stdout, and `result_<L>.json` (`equivalence` field). | **RESOLVED** |
| **Sol 6: Jet-State Verdict Recording** | Missing classification and structured recording | [`u3d_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py) implements full classification logic and records verdict, inference, FFR mean/band, and offsets in `result_<L>.json`. | **RESOLVED** |
| **Sol 7 & AGY 5: Hardened FFR Extractor** | Division constant `11998.98/1060` vs exact `11.3198`; missing sanity guards | Uses exact `P_AORTA_KIN = 11.3198` matching [`u3d_analyse.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_analyse.py#L9). Requires exactly one `surfaceFieldValue.dat`, $\ge 100$ rows, finite values, monotonic iterations, and final iteration matching `controlDict` and `build_info.json`. | **RESOLVED** |
| **Sol R2-1: Unsettled Runs Classified Axisymmetric** | Verdict ignored settling; band `4e-4` was falsely accepted as axisymmetric | [`settled()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py#L54-L59) strictly enforces `SETTLE_DRIFT <= 2e-4` over final 500 and `SETTLE_BAND <= 1e-4` over last 100 rows. [`classify()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py#L78-L87) sends any unsettled run to `inconclusive`. Verified via 11 equality tests against [`u3d_analyse.level()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_analyse.py). | **RESOLVED** |
| **Sol R2-2 & AGY R2-2: Pre-registration Extension** | Extension to S25B/S12A/S12B was not formally appended before runs | Formally appended with date **2026-10-03** in [`u3d_check/U3D_CHECK_DESIGN.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/U3D_CHECK_DESIGN.md#L11-L17) prior to Task B runs. Script text cites "rule of 2026-10-01 extended 2026-10-03". | **RESOLVED** |
| **Sol R2-3: Restart Released Wrong Rank/RAM** | Manifest edits altered recovery resource accounting | [`pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py#L162-L163) writes immutable `jobs/<name>.admit` prior to spawn. Recovery reads resources solely from `.admit` records. | **RESOLVED** |
| **Sol R2-4: Spawn/Recovery Race Window** | Status `running` written before spawn/PID record | Admission order: `.admit` $\to$ status `starting` $\to$ wrapper spawn. Wrapper writes `jobs/<name>.pid` itself before executing child. Recovery adopts young `starting` jobs (<120 s) as alive/unknown. Process verified by start jiffies, session leader, and `POOL_JOB_TOKEN`. | **RESOLVED** |
| **Sol R2-5: Job Dependency Validation** | `after` list allowed non-string/unhashable entries | [`pool.py:85`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py#L85) enforces that every element in `after` is a valid job-name string matching `^[A-Za-z0-9_.-]+$` and $\ne$ `j["name"]`. | **RESOLVED** |
| **AGY Condition 1: Strictly Sequential** | S25B $\to$ S12A $\to$ S12B execution | Specified via `"after"` in `jobs_draft/`: S12A waits for S25B; S12B waits for S12A. Enforced by `pool.py`. | **RESOLVED** |
| **AGY Condition 2: Verified Reconstruction** | Ensure reconstructed fields exist before purging slices | Implemented at [`u3d_job.sh:48-67`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh#L48-L67); tested across 11 fault injection modes. | **RESOLVED** |
| **AGY Condition 3: Return Directory** | Prevent default overwrite of frozen `returns/2026-09-24` | Acknowledged in `FIX31_REPORT.md` (Attempt 2); requires setting `U3D_RETURNS_DIR` during final publication. | **RESOLVED (Operational)** |
| **Case Setups Integrity** | Ensure `case_S25B`, `case_S12A`, `case_S12B` unchanged since Round 1 | Timestamps strictly precede Round 1 (11:11 and 11:20 on 2026-10-03). Meshes, budgets, and scotch decompose settings remain completely fresh and uncorrupted. | **RESOLVED** |

---

## 2. Evaluation of Tooling Fixes & Extensions

### A. Judgment of the Dated Extension in `u3d_check/U3D_CHECK_DESIGN.md`
The dated extension was appended on 2026-10-03 to [`u3d_check/U3D_CHECK_DESIGN.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d_check/U3D_CHECK_DESIGN.md#L11-L17) prior to initiating any Task B re-run.
1. **Physical and Geometric Consistency**: The stenosis throat ($x = 31.5\text{ mm}$) and downstream expansion geometry are invariant across mesh levels. Measuring the jet core centroid at $x = 50.0\text{ mm}$ and $x = 56.5\text{ mm}$ provides identical physical diagnostic sensitivity across all meshes.
2. **Deflection Criterion**: Deflection threshold $\ge 30.0\ \mu\text{m}$ at $x = 50\text{ mm}$ OR $x = 56.5\text{ mm}$ is conservative and physically appropriate: broken symmetry at either axial probe location demonstrates that the jet has attached to the vessel wall.
3. **FFR Baselines & Tolerances**:
   - S25B: `0.791197`
   - S12A: `0.790308`
   - S12B: `0.790418`  
   These values match the original 16-rank deposited dataset ([`returns/2026-09-26/U3D_sten70.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/U3D_sten70.csv)) to all significant digits. Tolerances of $|d\text{FFR}| \le 1\times 10^{-4}$ (for same-state verification) and $> 5\times 10^{-4}$ (for opposite-state inference) cleanly separate numerical discretization jitter from state bifurcation.
4. **SETTLED Criterion Integration**: Incorporating the formal settling rule ($\ge 500$ iterations, final-500 drift $\le 2\times 10^{-4}$, last-100 band $\le 1\times 10^{-4}$) directly into rule (d) guarantees that unfinished or oscillatory runs cannot be falsely certified as steady solutions.
5. **Auditor Judgment**: The extension is scientifically rigorous, completely documented, and pre-registered prior to execution.

### B. Audit of `u3d_verdict.py`
1. **Settling Logic**: Function [`settled()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py#L54-L59) mirrors [`u3d_analyse.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_analyse.py) verbatim using `numpy`. In [`classify()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py#L78-L87), the settling check is evaluated first: any unsettled case immediately yields `("inconclusive", "rule (d): the run is NOT SETTLED...")`.
2. **FFR Extraction Sanity**: Asserts kinematic pressure normalization constant `P_AORTA_KIN = 11.3198`, strictly monotonic iterations, final iteration matching `controlDict` and `build_info.json`, and presence of exactly one `surfaceFieldValue.dat`.
3. **Citation Uniformity**: All citations and json fields cite `"u3d_check/U3D_CHECK_DESIGN.md, rule of 2026-10-01 extended 2026-10-03"`.

### C. Audit of `pool.py` Process & Resource Management
1. **Admission Immutability**:
   - [`pool.py:162-163`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py#L162-L163) writes `jobs/<name>.admit` atomically before writing status `starting` and spawning the job wrapper.
   - Resource accounting in lines 129, 146, 173 reads only `adm["ranks"]` and `adm["ram_gb"]` from the `.admit` file. Modifying a manifest in `jobs/*.json` after admission has zero effect on allocated resources.
2. **Elimination of Spawn / Recovery Race**:
   - The wrapper [`wrap()`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py#L100-L108) runs as a session leader (`setsid`) and writes `jobs/<name>.pid` containing `{pid, sid, start, boot_id, token}` *before* launching the user command.
   - The pool transitions status from `starting` to `running` only after verifying that the `.pid` file exists on disk.
   - On pool restart, jobs in `starting` status without `.pid` that were admitted within `START_GRACE` (120 s) are maintained as `alive/unknown` with committed resources until the wrapper registers or grace expires.
   - Liveness checks verify boot ID, PID start time from `/proc/<pid>/stat`, session leadership, and environment variable `POOL_JOB_TOKEN=<token>`.
3. **Legacy Protection**:
   - Lines 118–122 check for active jobs without `.admit` records. If any unmanaged legacy job exists (e.g. from the unpatched pool), the new pool immediately refuses to start and exits with an informative error rather than marking running jobs lost.
4. **Validation & Locking**:
   - Manifest validation (`valid()`, line 81) requires `ranks` to be integer $\ge 1$ (excluding boolean), `ram_gb` $\ge 0$ (excluding boolean), `cmd` string, and all items in `after` to be valid job-name strings matching `NAME`.
   - Single-instance execution is enforced via non-blocking `fcntl.flock` on `jobs/.pool.lock`.

### D. Case Setups Verification
- Freshness: `case_S25B`, `case_S12A`, and `case_S12B` contain only directory `0`, `constant/`, `system/`, `build_info.json`, `case.foam`, and `zerod_reference.json`. No residual processor directories or old solution logs exist.
- Geometry & Mesh: Cell counts and mesh gates match deposited values:
  - S25B: 3,299,948 cells; `endTime` 4000; Scotch 8 ranks
  - S12A: 6,739,168 cells; `endTime` 6000; Scotch 8 ranks
  - S12B: 7,649,800 cells; `endTime` 3000; Scotch 8 ranks
- Integrity: All case file timestamps date from 11:11 and 11:20 on 2026-10-03, preceding Round 1.

---

## 3. Numbered Findings

### Finding 1: Running Task A Solves Preclude Immediate Tooling Deployment and Task B Execution
- **Severity**: **MAJOR**
- **Component**: Runtime Environment / Process Contention
- **Description**: The host is currently executing a 16-rank Task A OpenFOAM solve (`A1_D7_12p5`, PID 2713128) under an active instance of the legacy `pool.py` (PID 2713127) started at 11:41:28, with `A2_D7_12p5_zoneB` queued after it.
  1. The host's 16 physical cores are 100% occupied by the Task A solve. Launching an 8-rank Task B solve concurrently would oversubscribe CPU cores and create resource contention.
  2. Because the active Task A jobs were spawned by the old `pool.py`, they lack `.admit` and `.pid` tracking files. The new [`taskB/pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py#L118-L122) explicitly includes a safety interlock that refuses to start while legacy jobs are active.
- **Action Required**: The operator/coordinator must wait until all active Task A jobs finish and the old pool process exits (or stop the old pool cleanly when no job is executing) before deploying the new pool tooling and starting Task B.

---

### Finding 2: Deployment Steps for Task B Tooling and Job Manifests
- **Severity**: **MINOR**
- **Component**: Deployment / Staging
- **Description**: The audited fixes reside in `taskB/` and must be staged into the production pool directory `/home/azan/paper6_t6_work/pool/`:
  - [`pool/u3d_job.sh`](file:///home/azan/paper6_t6_work/pool/u3d_job.sh) and [`pool/u3d_verdict.py`](file:///home/azan/paper6_t6_work/pool/u3d_verdict.py) in the live pool directory are still the Attempt-1 versions.
  - [`pool/pool.py`](file:///home/azan/paper6_t6_work/pool/pool.py) is still the unpatched version from 11:29.
  - Job manifests in [`jobs_draft/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/) have not yet been copied to `/home/azan/paper6_t6_work/pool/jobs/`.
- **Action Required**: Once Task A completes and the old pool terminates:
  1. Copy [`taskB/pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py), [`taskB/u3d_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_job.sh), and [`taskB/u3d_verdict.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/u3d_verdict.py) into `/home/azan/paper6_t6_work/pool/`.
  2. Copy [`jobs_draft/u3d_*.json`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/jobs_draft/) into `/home/azan/paper6_t6_work/pool/jobs/`.
  3. Create the corresponding audit marker files in `/home/azan/paper6_t6_work/pool/jobs/`:
     ```bash
     touch /home/azan/paper6_t6_work/pool/jobs/u3d_S25B.audited
     touch /home/azan/paper6_t6_work/pool/jobs/u3d_S12A.audited
     touch /home/azan/paper6_t6_work/pool/jobs/u3d_S12B.audited
     ```

---

### Finding 3: Mandatory Export of `U3D_RETURNS_DIR` for Final Table Publication
- **Severity**: **MINOR**
- **Component**: Pipeline Integration / Post-Processing
- **Description**: As noted in Round 1 and Round 2, [`u3d_returns.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_returns.py#L3) defaults to the frozen directory `/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24`.
- **Action Required**: Prior to generating final publication return tables after all Task B re-runs complete, the operator must explicitly export:
  ```bash
  export U3D_RETURNS_DIR=/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03
  ```

---

VERDICT: READY WITH CONDITIONS
