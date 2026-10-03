### Pre-Run Audit Report (Round 2): Task P5 (Five Cohort Baseline Solves)

---

### 1. Executive Summary & Verification Scope

An exhaustive, non-invasive pre-run audit (Round 2) was conducted across the newly staged Task P5 cases ([`p5/cases_v2/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/cases_v2/)), the consolidated Task C pipeline ([`taskFinal/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskFinal/)), the generic solve runner ([`taskJ/case_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskJ/case_job.sh)), and the production scheduler ([`taskB/pool.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskB/pool.py) running in `lane2/`).

**Audit Protocol Compliance**:
- Read-only audit: no edits to case files, pipeline sources, or existing logs. All synthetic verification scripts and inspect harnesses executed strictly within `/home/azan/paper6_t6_work/audit_tmp/`.
- No solvers (`simpleFoam`), `mpirun`, or `decomposePar` were executed on real production cases.
- All shell scripts passed `bash -n`. All Python modules in `taskFinal/pf/`, `taskB/`, `lane2/`, and `p5/` passed `python3 -m py_compile`.

**Verification Positives Across the Five Staged Cases (`cases_v2`)**:
1. **E0 Membership**: Verified via [`p5/e0_guard.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/e0_guard.py) against [`CFD-SUBSET-FROZEN-2026-09-18.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/CFD-SUBSET-FROZEN-2026-09-18.csv). All five cases (138 left, 69 left, 473 left, 272 right, 139 right) are confirmed `MEMBER`.
2. **Decomposition**: All five cases configure exactly 8 ranks (`numberOfSubdomains 8;`) using `scotch` in [`system/decomposeParDict`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/cases_v2/138_resistance/system/decomposeParDict#L2).
3. **Boundary Setup & Patch Types**: In [`constant/polyMesh/boundary`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/cases_v2/138_resistance/constant/polyMesh/boundary), `inlet` and all `out_<id>` are declared as `patch`; `wall` is declared as `wall`. All patch names match package `outlet_ids`.
4. **Analytical BC Parameters**: $R_{\text{used}}$, $R_{\text{own}}$, $G = R_{\text{used}} / R_{\text{own}}$, and $\text{relax} = \min(0.5, 1 / (1 + G))$ exactly match analytical definitions across all live outlets. In [`0/p`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/cases_v2/138_resistance/0/p), coded resistance BCs match `build_info.json` within numerical precision.
5. **Probe Planes & Relocation**: Bounded probe planes (`bounds_m` enclosing single-lumen cuts) are present in all cases. Package 473 measurement probe relocation to node 646 (+2.853 mm distal along the LCX continuation) correctly preserves `measurementOrigFlux` and `measurementOrigP` for the package probe, satisfying strict section rules S1–S4.
6. **Case 272 Blocker Resolution**: In [`p5/cases_v2/272_resistance/`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/cases_v2/272_resistance/), the fatal `surfaceFieldValue` monitors for zero-face patch `out_396` have been removed from `system/controlDict`, `out_396` is registered in `outlets_lost_in_mesh`, `zerod_reference.json` excludes `out_396` (preventing `stale_lost` exceptions in `analyze_case.py`), and the coded BC `res396` is preserved in `0/p` for compilation safety.
7. **Flag Integrity (`test_flags_p5.py`)**: Tested against all five `cases_v2` instances. All 10/10 test checks pass, reproducing all expected flag sets, including decisive geometry step status (D10).

---

### 2. Analysis & Recommendation on Case 272 Mesh Unconnected Regions

#### Question Evaluated:
> *The mesh log of 272 says 'Mesh has 2 unconnected regions': judge whether an isolated region without any pressure reference is a solver problem (singular pressure system in a closed island) and what the minimal deviation-free handling is, noting the work order forbids repairing the SURFACE but a post-mesh removal of an unconnected cell region with splitMeshRegions-style housekeeping might be acceptable: give a recommendation with its consequences; do not change anything.*

#### Physical & Mathematical Judgment:
1. **Pressure System Singularity**:
   - In incompressible Navier-Stokes solvers using the SIMPLE algorithm ([`simpleFoam`](file:///usr/lib/openfoam/openfoam2406/src/finiteVolume/cfdTools/general/include/simpleFoam.H)), the pressure equation is a Poisson equation $\nabla \cdot \left(\frac{1}{A_P} \nabla p\right) = \nabla \cdot U^*$.
   - If an isolated cell island is completely enclosed by wall faces, every boundary face on that island carries a Neumann boundary condition ($\frac{\partial p}{\partial n} = 0$, via `zeroGradient` or `fixedFluxPressure`).
   - A pure Neumann Poisson problem on an isolated connected component possesses a non-trivial 1D nullspace (constant pressure offset, eigenvalue $\lambda_0 = 0$).
   - In OpenFOAM, when `pRefCell` or `pRefPoint` is assigned in `system/fvSolution`, it pins the pressure at a single cell. That cell belongs to the primary fluid domain (connected to the inlet). Consequently, the isolated closed island remains **unpinned** and mathematically singular.
   - Multigrid (GAMG) and Krylov (PCG) linear solvers will experience residual stagnation or numerical drift on the unpinned component. While velocity inside a rigid no-slip cavity analytically decays to zero, roundoff errors in the unreferenced pressure field can cause spurious velocity spikes or solver divergence.
   - **Conclusion**: An unpinned, isolated closed cell region is indeed a severe solver problem.

2. **Empirical Finding on Case 272**:
   - Examination of the mesh generation log [`p5/mesh/272/log.cartesianMesh:225-228`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/mesh/272/log.cartesianMesh#L225-L228) reveals:
     ```text
     Checking cell connections
     Finished checking cell connections
     --> FOAM Warning : Mesh has 2 unconnected regions
     Removing selected cells from the mesh
     New cells size 5510458
     ```
   - During `cartesianMesh`, cfMesh automatically identified the second unconnected component (the distal R-PDA cavity behind the severe anatomical stenosis) and **pruned it from the mesh**.
   - Inspection of [`p5/mesh/272/log.checkMesh.standard:80-89`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/mesh/272/log.checkMesh.standard#L80-L89) confirms that the resulting `constant/polyMesh/` has:
     ```text
     Number of regions: 1 (OK).
     Patch topology: ".*" 533920 534796 ok (closed singly connected)
     ```
   - **Conclusion**: The disk mesh for Case 272 currently contains **only 1 region**. The warning in `log.cartesianMesh` was an intermediate processing warning during mesh generation; no second unconnected cell region remains in `cases_v2/272_resistance/constant/polyMesh/`. This cell deletion by cfMesh is also the exact physical mechanism why patch `out_396` was left with 0 faces.

3. **Minimal Deviation-Free Handling & Recommendation**:
   - **Work Order Constraint**: Work order Section 2 and Decision D4 strictly forbid repairing or modifying the input CAD/STL surface to open or remove anatomical cavities.
   - **Deviation-Free Protocol**: If an unconnected cell region ever persists into a polyMesh, the minimal deviation-free procedure is post-mesh topological pruning using OpenFOAM mesh manipulation tools (such as `splitMeshRegions -largestRegion` or `cellSet` + `subsetMesh` selecting the component contiguous with the inlet).
   - **Consequences**:
     1. Surface geometry is never modified, fully complying with the work order.
     2. Discarding the disconnected cell component reduces the cell count by the island's volume.
     3. Boundary patches on the discarded island remain in `constant/polyMesh/boundary` with `nFaces 0`, requiring monitor omission and `OUTLET_LOST_IN_MESH` bookkeeping (which `taskFinal` already implements).
     4. `checkMesh` topology checks report `Number of regions: 1 (OK)`, eliminating matrix singularity.
   - **Case 272 Action**: **No mesh intervention is needed for Case 272**. cfMesh already performed this pruning automatically, and `log.checkMesh.standard` validates `Number of regions: 1 (OK)`.

---

### 3. Numbered Audit Findings

#### 1. MAJOR — Post-processing (`post_case_generic.sh`) fails unconditionally if run after `case_job.sh` purges processor directories.
- **File & Line**: [`taskFinal/post_case_generic.sh:62`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskFinal/post_case_generic.sh#L62), [`taskFinal/pf/post_helpers.py:86-96`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskFinal/pf/post_helpers.py#L86-L96), [`taskJ/case_job.sh:214-231`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskJ/case_job.sh#L214-L231)
- **Details**: In [`post_case_generic.sh:62`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskFinal/post_case_generic.sh#L62), the pipeline enforces `post_helpers.py reconstruct-check "$CASE" "$RC"`. In [`post_helpers.py:87-92`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskFinal/pf/post_helpers.py#L87-L92), `reconstruct_check()` inspects `f"{case}/processor0"`. If `processor0` does not exist, it unconditionally appends `"no time directory in processor0"` and fails with rc 1. In [`taskJ/case_job.sh:226-231`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskJ/case_job.sh#L226-L231), the solve job purges all `processor*` directories at the end of the run. If `post_case_generic.sh` is invoked separately after `case_job.sh` finishes, it will abort at step 2, blocking report generation.
- **Remedy / Condition**: Post-processing must be integrated directly into `case_job.sh` via the provided `POST_CMD` hook ([`taskJ/case_job.sh:214-219`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskJ/case_job.sh#L214-L219)). `POST_CMD` executes in the case directory *prior* to processor purging while `processor0` is intact. If `POST_CMD` fails, `case_job.sh` aborts with rc 1 and preserves `processor*` directories for inspection.

#### 2. MAJOR — Pipeline improvements in `taskFinal/` are not yet installed over the live `pf/` and `p5/` directories.
- **File & Line**: [`taskFinal/CONSOLIDATION_REPORT.md:131-135`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskFinal/CONSOLIDATION_REPORT.md#L131-L135), [`pf/post_helpers.py:163`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/pf/post_helpers.py#L163), [`p5/build_m1_geometry.py:585`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/build_m1_geometry.py#L585)
- **Details**: The live script [`pf/post_helpers.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/pf/post_helpers.py#L163) does not contain the Task 37 / Task Final logic (D3/D4 ingestion, `flags` schema, lost-outlet zero-flow handling, and decisive gate evaluation). Similarly, [`p5/build_m1_geometry.py`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/build_m1_geometry.py#L585) in the root `p5/` directory still lacks `gate_bookkeeping()`. If post-processing scripts are executed against the un-updated live `pf/` directory, D3/D4 and lost-outlet columns will be missing from `M1_results.csv`, and Case 138 will be falsely marked as failed geometry.
- **Remedy / Condition**: Prior to running solve post-processing, the operator must deploy `taskFinal/pf/*.py` over live `pf/`, and deploy `taskFinal/p5/build_m1_geometry.py` and `summarise_p5.py` over `p5/`.

#### 3. MAJOR — Solve job script `taskJ/case_job.sh` is not yet installed in `lane2/`.
- **File & Line**: [`lane2/`](file:///home/azan/paper6_t6_work/lane2/)
- **Details**: The execution plan requires running 8 ranks per case in `lane2` via `lane2/case_job.sh`. Directory inspection confirms that `lane2/case_job.sh` does not exist yet.
- **Remedy / Condition**: Install [`taskJ/case_job.sh`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskJ/case_job.sh) as `/home/azan/paper6_t6_work/lane2/case_job.sh` with executable permissions (`chmod +x`).

#### 4. MAJOR — Execution plan specifies 32 ranks on 16 physical cores by operator order, incurring SMT thread contention.
- **File & Line**: [`lane2/pool.py:154`](file:///home/azan/paper6_t6_work/lane2/pool.py#L154), [`WORK-ORDER-2026-09-24.md:209-211`](file:///home/azan/paper6_t6_work/scratchpad/T6_repo/cfd_handover/WORK-ORDER-2026-09-24.md#L209-L211)
- **Details**: The scheduler `lane2/pool.py` now correctly enforces `used + j["ranks"] <= RANKS` (budget: 16 ranks). However, the operator-ordered plan runs `lane2` (8 ranks Task B + 8 ranks P5 = 16 ranks) concurrently with the primary pool running A2 (16 ranks), totalling 32 solver ranks on 16 physical cores (32 logical CPUs). While within OS limits and admitted by both schedulers independently, running 200% physical core capacity causes severe SMT hardware resource contention, L3 cache evictions, and benchmark runtime dilation.
- **Remedy / Condition**: Note the runtime dilation for performance reporting. SMT execution is explicitly authorised by operator order, but solver timings must not be directly compared against dedicated 16-rank physical core baselines.

#### 5. MINOR — Retaining processor directories (`KEEP_PROCESSORS=1`) will exhaust disk space.
- **File & Line**: [`taskJ/case_job.sh:12,71,222`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/taskJ/case_job.sh#L12), [`lane2/pool.py:158`](file:///home/azan/paper6_t6_work/lane2/pool.py#L158)
- **Details**: Available disk space on `/` is 19 GB. Total cell count across the five P5 cases is 26.4M cells (272 alone has 7.64M cells). Decomposed fields require ~3.5–5.5 GB per case. Retaining all decomposed processor directories across 5 cases requires ~20 GB, which exceeds available disk space and would trigger `lane2/pool.py` disk admission stall (`disk_free_gb() < 15`).
- **Remedy / Condition**: Default `KEEP_PROCESSORS=0` in `case_job.sh` must be maintained. Each case must execute sequentially in `lane2`, verify reconstruction, run post-processing via `POST_CMD`, and immediately purge its `processor*` directories before the next P5 case is admitted.

---

### 4. Verification Table of Five Staged Cases (`cases_v2`)

| Case | E0 Status | Ranks | Boundary Patches & Types | Analytical BCs & Relax | Bounded Planes | Probe Relocation | Lost Outlets | M1_results Expected Flags |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **138** | MEMBER | 8 | 1 inlet, 5 outlets (`patch`), 1 wall (`wall`) | Formula verified; $G \in [5.2, 10.1]$, relax $\in [0.09, 0.16]$ | Verified | None | None | `D3_FAIL;D4_FAIL;CHECKMESH_STANDARD_FAIL` |
| **69** | MEMBER | 8 | 1 inlet, 4 outlets (`patch`), 1 wall (`wall`) | Formula verified; $G \in [9.2, 12.3]$, relax $\in [0.07, 0.10]$ | Verified | None | None | `LESION_PURITY_GATE_FAIL;POSITIVE_CONTROL_UNDETECTED` |
| **473** | MEMBER | 8 | 1 inlet, 6 outlets (`patch`), 1 wall (`wall`) | Formula verified; $G \in [7.6, 17.5]$, relax $\in [0.05, 0.12]$ | Verified | Node 646 (+2.853 mm distal); S1–S4 PASS; Orig monitors kept | None | `D2_RELATIVE_THROAT_GATE_FAIL;D3_FAIL;D4_FAIL;MEASUREMENT_PROBE_RELOCATED` |
| **272** | MEMBER | 8 | 1 inlet, 2 live outlets + 1 zero-face outlet (`out_396`), 1 wall (`wall`) | Formula verified; $G \in [9.2, 11.1]$, relax $\in [0.08, 0.10]$ | Verified | None | `out_396` (monitors removed, coded BC kept, territory closed) | `SELF_INTERSECTION;D3_FAIL;D4_FAIL;OUTLET_LOST_IN_MESH` |
| **139** | MEMBER | 8 | 1 inlet, 2 outlets (`patch`), 1 wall (`wall`) | Formula verified; $G \in [8.2, 13.7]$, relax $\in [0.07, 0.11]$ | Verified | None | None | `D2_RELATIVE_THROAT_GATE_FAIL;D3_FAIL;D4_FAIL` |

---

### 5. Final Case-by-Case Verdict

The Round 1 BLOCKER on Case 272 is fully resolved in [`p5/cases_v2/272_resistance`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/cases_v2/272_resistance/). All five cases in `cases_v2` are cleared to run under the operational conditions defined above (deploying `taskFinal`, installing `taskJ/case_job.sh` into `lane2`, using `POST_CMD` before processor purge, and maintaining sequential execution in `lane2`).

VERDICT: 138 READY WITH CONDITIONS; 69 READY WITH CONDITIONS; 473 READY WITH CONDITIONS; 272 READY WITH CONDITIONS; 139 READY WITH CONDITIONS
