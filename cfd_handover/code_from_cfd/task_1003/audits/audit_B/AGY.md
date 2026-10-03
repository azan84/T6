# Pre-Run Audit Report: Task B (U3D Ladder Re-run with Fields Kept)
**Target**: Task B of [WORK-ORDER-2026-10-03.md](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/WORK-ORDER-2026-10-03.md#L72-L77) (Section 3)  
**Cases Under Review**: `case_S25B`, `case_S12A`, `case_S12B` under `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/`  
**Meshes**: `mesh_S25B`, `mesh_S12A`, `mesh_S12B` (`mesh_gates.json`)  
**Job Runner & Scheduler**: `/home/azan/paper6_t6_work/pool/u3d_job.sh`, `/home/azan/paper6_t6_work/pool/pool.py`  
**Diagnostic Tools**: `/home/azan/paper6_t6_work/jet_offset.py`, `/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/post_level.sh`

---

## 1. Executive Summary & Verification Matrix

| Audit Item | Specification / Original Baseline | Audit Finding | Status |
| :--- | :--- | :--- | :--- |
| **Mesh: S25B Cells** | 3,299,948 cells ([U3D_sten70.csv](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/U3D_sten70.csv#L5)) | `mesh_S25B/mesh_gates.json`: 3,299,948 cells; `GATES_PASS: true` | **PASS** |
| **Mesh: S12A Cells** | 6,739,168 cells ([U3D_sten70.csv](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/U3D_sten70.csv#L4)) | `mesh_S12A/mesh_gates.json`: 6,739,168 cells; `GATES_PASS: true` | **PASS** |
| **Mesh: S12B Cells** | 7,649,800 cells ([U3D_sten70.csv](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/U3D_sten70.csv#L6)) | `mesh_S12B/mesh_gates.json`: 7,649,800 cells; `GATES_PASS: true` | **PASS** |
| **Mesh Hard-linking** | Hard-linked `constant/polyMesh` to save disk | Inode matching verified on `points`, `faces`, `owner`, `neighbour` (link count 2) | **PASS** |
| **Budgets (`endTime`)** | S25B: 4000, S12A: 6000, S12B: 3000 | `system/controlDict` and `build_info.json` match budgets exactly | **PASS** |
| **Inlet BC** | `totalPressure; p0 uniform 11.3198;` | Identical across all cases and matches audited reference | **PASS** |
| **Outlet BC** | `codedFixedValue; R=6.974826e9, relax=0.2, Pv=666.61, rho=1060` | Identical across all cases and matches audited reference | **PASS** |
| **Velocity BC (`0/U`)** | `pressureInletOutletVelocity` (inlet), `inletOutlet` (outlet), `noSlip` (wall) | Identical across all cases and matches audited reference | **PASS** |
| **Fluid Properties** | Newtonian `nu = 3.7735849e-06`, laminar | Identical across `constant/transportProperties` and `turbulenceProperties` | **PASS** |
| **Discretization Schemes** | Second-order bounded (`linearUpwind grad(U)`), linear laplacian/interpolation | Identical across all cases and matches audited `fvSchemes` | **PASS** |
| **Linear Solvers** | `p: GAMG (tol 1e-8, relTol 0.01)`, `U: smoothSolver (tol 1e-9, relTol 0.1)`, `relax: p 0.3, U 0.7` | Identical across all cases and matches audited `fvSolution` | **PASS** |
| **Monitors** | `measurementP` (x=56.5 mm), `throatFlux`/`throatP` (x=31.503 mm), `inlet/outletFlux/Pressure` | All 7 function objects write at `writeInterval 1;` in all cases | **PASS** |
| **8-rank Scotch Decomposition** | Invariant numerics | Verified on 2026-10-02 (S50 & S25A re-runs match 16-rank FFR to within $4\times 10^{-7}$ and $2\times 10^{-9}$) | **PASS** |
| **Jet-State Diagnostic** | `jet_offset.py` $|U_x|$-weighted radial centroid offset across 8 axial slabs | PyVista 0.47.3 verified; discriminates axisymmetric ($<10\ \mu\text{m}$) vs wall-deflected ($\ge 30\ \mu\text{m}$) | **PASS** |
| **Field Preservation** | `reconstructPar -latestTime` keeps full final fields, purges only `processor*` | Reconstructed `3000/` and `4000/` preserved in S50/S25A; `rm -rf processor*` only targets partitioned slices | **PASS** |
| **Script Syntax** | `bash -n` and `python3 -m py_compile` | All shell scripts and python scripts passed without error | **PASS** |

---

## 2. Numbered Findings

### Finding 1: Unchecked `reconstructPar` Exit Code Before Processor Directory Purging
- **Severity**: **MAJOR**
- **File:Line**: [/home/azan/paper6_t6_work/pool/u3d_job.sh:13](file:///home/azan/paper6_t6_work/pool/u3d_job.sh#L13)
- **Description**: In `u3d_job.sh`, line 13 executes `reconstructPar -latestTime > log.reconstructPar 2>&1; touch case.foam` without verifying the exit code of `reconstructPar`. Line 16 then invokes `post_level.sh $L unknown purge`, which runs `rm -rf "$D"/processor*`. Because `analyze_solve.py` and `u3d_make_csv.py` only inspect `postProcessing/` monitor data and `log.simpleFoam`, `post_level.sh` will succeed even if reconstruction failed. Consequently, the partitioned fields would be permanently deleted while global reconstructed fields were missing, directly violating the work order requirement ("with fields kept") and wasting hours of compute.
- **Recommended Action**: Guard line 13 with an explicit error handler before proceeding:
  ```bash
  reconstructPar -latestTime > log.reconstructPar 2>&1 || { echo "reconstruct failed" >> $S; exit 4; }
  ```

---

### Finding 2: Missing Error Propagation and `set -e` in Job Script
- **Severity**: **MAJOR**
- **File:Line**: [/home/azan/paper6_t6_work/pool/u3d_job.sh:16-17](file:///home/azan/paper6_t6_work/pool/u3d_job.sh#L16-L17)
- **Description**: `u3d_job.sh` does not enable `set -e`. If `post_level.sh` fails at line 16 (for instance, during strict convergence checking or work CSV generation), the failure is swallowed. The script executes line 17 `echo "$(date '+%F %T') DONE" >> $S` and exits with code `0`. `pool.py` detects exit code 0, marking the task as `done` in `jobs/<name>.status`, masking post-processing failures.
- **Recommended Action**: Explicitly assert the exit status of line 16:
  ```bash
  ( cd $U && bash post_level.sh $L unknown purge > $O/post_$L.txt 2>&1 ) || { echo "post_level failed" >> $S; exit 5; }
  ```

---

### Finding 3: `pool.py` RAM Admission Logic Flaw Permitting Unintended Concurrent Overcommit
- **Severity**: **MAJOR**
- **File:Line**: [/home/azan/paper6_t6_work/pool/pool.py:37](file:///home/azan/paper6_t6_work/pool/pool.py#L37)
- **Description**: The RAM admission check in `pool.py` is:
  ```python
  if memavail_gb() - RESERVE < max(0.0, j["ram_gb"] - 0.0) + 0.0 and ram_committed + j["ram_gb"] > 0.9 * (memavail_gb() + ram_committed) - RESERVE: continue
  ```
  Because the check uses `and`, if a newly launched job has not yet fully populated its physical memory footprint (RSS), `/proc/meminfo` reports high `MemAvailable`. For a subsequent candidate job, `memavail_gb() - RESERVE < j["ram_gb"]` evaluates to `False`, short-circuiting the entire condition to `False`. The scheduler would then admit the second job if ranks fit ($8 + 8 = 16$). For S12A (~13.5 GB) and S12B (~15.3 GB), concurrent execution requires ~29 GB, exceeding host capacity (27 GiB physical), which would induce severe swapping or invoke the Linux OOM-killer.
- **Recommended Action / Mandatory Condition**: Task B pool job JSON files **must** explicitly serialize execution using the `"after"` dependency list (e.g., S12A specifying `"after": ["S25B"]`, and S12B specifying `"after": ["S12A"]`).

---

### Finding 4: Host Rank Budget and External Task Contention
- **Severity**: **MINOR**
- **File:Line**: [/home/azan/paper6_t6_work/pool/pool.py:29](file:///home/azan/paper6_t6_work/pool/pool.py#L29)
- **Description**: `pool.py` only counts MPI ranks from its internal `procs` list (`used = sum(j["ranks"] ...)`). The host currently has Task A background activities running (`python3 build_m1_mesh.py`, Task C/Task A solvers). S25B, S12A, and S12B are configured for 8 ranks with `--bind-to none`. If Task B runs concurrently with external 8-rank solves, host cores (16 physical) are fully utilized ($8 + 8 = 16$).
- **Recommended Action**: Ensure Task B jobs run sequentially at 8 ranks, or wait until Task A background solves conclude as mandated by the order in [WORK-ORDER-2026-10-03.md](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/WORK-ORDER-2026-10-03.md#L125) (Section 7).

---

### Finding 5: Approximated Aortic Pressure Factor in Informational Awk Script
- **Severity**: **MINOR**
- **File:Line**: [/home/azan/paper6_t6_work/pool/u3d_job.sh:15](file:///home/azan/paper6_t6_work/pool/u3d_job.sh#L15)
- **Description**: Line 15 calculates instantaneous FFR via `v=a[i]*1060/11998.98`. In the OpenFOAM setup, kinematic aortic pressure is $P_{aorta} = 11.3198\ \text{m}^2/\text{s}^2$ and density is $\rho = 1060.0\ \text{kg/m}^3$, giving $P_{aorta} \cdot \rho = 11998.988\ \text{Pa}$. Using $11998.98$ introduces a slight relative error of $6.7 \times 10^{-7}$ in `ffr_$L.txt`. Note that the official return pipeline in [u3d_analyse.py](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_analyse.py#L9) directly uses `P_AORTA_KIN = 11.3198` and is unaffected.
- **Recommended Action**: Update line 15 to `v=a[i]/11.3198;` for bitwise consistency.

---

### Finding 6: Default Return Directory Points to Frozen 2026-09-24 Folder
- **Severity**: **MINOR**
- **File:Line**: [/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_returns.py:3](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/u3d/u3d_returns.py#L3)
- **Description**: `u3d_returns.py` defaults to `R = os.environ.get("U3D_RETURNS_DIR", "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24")`. If invoked without setting `U3D_RETURNS_DIR`, it will write directly into the frozen `returns/2026-09-24` directory, violating the standing rule ("Re-issued CSVs get a dated suffix. Do not overwrite.").
- **Recommended Action / Mandatory Condition**: When generating final returns, `U3D_RETURNS_DIR` must be explicitly exported:
  ```bash
  export U3D_RETURNS_DIR=/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03
  ```

---

## 3. Resource Requirements & Capacity Validation

- **Disk Space Analysis**:
  - Current Available on `/`: **23 GB** (93% utilized).
  - Peak Disk Usage during Parallel Run:
    - S25B (3.30 M cells): ~2.5 GB peak (decomposed mesh + writeInterval 250 with purgeWrite 2 + final reconstruct). Post-purge: ~0.5 GB.
    - S12A (6.74 M cells): ~4.5 GB peak. Post-purge: ~1.0 GB.
    - S12B (7.65 M cells): ~5.0 GB peak. Post-purge: ~1.2 GB.
  - Sequentially, with processor dirs purged after each level, cumulative retained reconstructed fields require ~2.7 GB total, well within the 23 GB free disk space.
- **RAM Capacity Analysis**:
  - Host RAM: **27 GiB physical**, MemAvailable: **24 GiB**.
  - Peak RAM Requirement:
    - S25B: ~6.6 GB.
    - S12A: ~13.5 GB.
    - S12B: ~15.3 GB.
  - S12A and S12B individually fit within 24 GiB MemAvailable. They cannot run concurrently.

---

## 4. Operational Conditions for Execution

1. **Serialization**: In `pool/jobs/`, define jobs with strict sequential dependencies using `"after"`:
   - Job `u3d_S25B`: `"after": []`
   - Job `u3d_S12A`: `"after": ["u3d_S25B"]`
   - Job `u3d_S12B`: `"after": ["u3d_S12A"]`
2. **Reconstruction Safeguard**: Ensure `reconstructPar` exit status is verified prior to running `post_level.sh purge`.
3. **Environment**: When executing `u3d_returns.py`, ensure `U3D_RETURNS_DIR=/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03` is set.

---

VERDICT: READY WITH CONDITIONS
