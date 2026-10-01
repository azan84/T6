I have started searching for references to the `0.00055` U3D value across the scratchpad files. I will proceed with reviewing the findings once the search completes.
I have initiated a search for `U3D_sten70.csv` and `u3d_final.json` to verify the U3D results and will inspect the output once available.
I have launched a search for `stageA_A5_ladders.csv` to inspect the reported values and will review the output as soon as it completes.
I have started searching for `SETUP.md` to check its section 4 instructions and will inspect the result once found.
# CFD Audit Report: B3 Smoke Test Diagnosis and Proposed Change

**Auditor:** Antigravity (Strict Read-Only Audit)  
**Target Document:** [`/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md)  
**Audit Scope:** Evidence directories under `/home/azan/paper6_t6_work`, original archived case at `/mnt/e/Paper6-T6/cfd_local_only/archive/paper6_t6_cfd_2026-09_bulk_moved/A5_sten70_coarse`, and smoke test scripts at `/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test`.

---

## 1. Verification of the Evidence Table Numbers

Every number in the evidence table of [`B3_DIAGNOSIS.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md#L8-L16) was audited against raw monitor files (`surfaceFieldValue.dat`), mesh files (`constant/polyMesh/boundary`, `points`), logs (`log.simpleFoam`, `log.checkMesh`), and [`jet_offset.py`](file:///home/azan/paper6_t6_work/jet_offset.py).

| Run | Mesh | Boundary Type | Initial State | $Q_{\text{out}}$ ($\text{m}^3/\text{s}$) | $p_{\text{meas}}$ kin. ($x=56.5\text{ mm}$) | $\text{FFR}_{x56.5}$ | Jet Centroid Offset ($x=50 / 56.5\text{ mm}$) | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **original 2026-09-18** (`A5_sten70_coarse`) | archived | wall | default | $1.17392231\times 10^{-6}$ (2000 it) | $8.87426$ | $0.78396$ | $85.0\text{ }\mu\text{m} / 82.8\text{ }\mu\text{m}$ | **VERIFIED EXACT** |
| **`a5_arch8`** (2026-10-01) | archived | wall | default | $1.17390297\times 10^{-6}$ (2000 it) | $8.87434$ | $0.78397$ | $85.1\text{ }\mu\text{m}$ at $x=50$ ($82.7\text{ }\mu\text{m}$ at $56.5$) | **VERIFIED EXACT** |
| **`t2_archmesh_patch`** | archived | patch | default | $1.17390294\times 10^{-6}$ (3000 it) | $8.87434$ | $0.78397$ | Same trajectory as `a5_arch8` ($\Delta \equiv 0.0$ across 2000 it) | **VERIFIED EXACT** |
| **`smoke_ref` / `smoke_cont`** | new | patch | default | $1.17825059\times 10^{-6}$ (3000 it)<br>$1.17825058\times 10^{-6}$ (12000 it) | $8.85754$ (3000 it)<br>$8.85754$ (12000 it) | $0.78248$ | $0.9\text{ }\mu\text{m}$ at $x=50$ ($1.5\text{ }\mu\text{m}$ at $56.5$) | **VERIFIED EXACT** |
| **`t1_newmesh_wall`** | new | wall | default | $1.17825059\times 10^{-6}$ (3000 it) | $8.85754$ | $0.78248$ | Same trajectory as `smoke_ref` ($\Delta \equiv 0.0$ across 3000 it) | **VERIFIED EXACT** |
| **`bi_new_from_asym`** | new | patch | mapped from `t2_archmesh_patch` | $1.17390288\times 10^{-6}$ (4000 it; flat to $2\times 10^{-14}$) | $8.87434$ | $0.78397$ | $85.1\text{ }\mu\text{m} / 82.7\text{ }\mu\text{m}$ | **VERIFIED EXACT** |
| **`bi_arch_from_sym`** | archived | patch | mapped from `smoke_cont` | $1.17825071\times 10^{-6}$ (4000 it; flat to $5.3\times 10^{-13}$ from it 200) | $8.85754$ | $0.78248$ | $0.9\text{ }\mu\text{m} / 1.5\text{ }\mu\text{m}$ | **VERIFIED EXACT** |

### Additional Raw Verifications:
- **Archived A5 Ladder Solutions ([`stageA_A5_ladders.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24/stageA_A5_ladders.csv)):**
  - Coarse (198,252 cells): offset $85.0\text{ }\mu\text{m} / 82.8\text{ }\mu\text{m}$ (deflected).
  - Medium (379,468 cells): offset $2.1\text{ }\mu\text{m} / 3.5\text{ }\mu\text{m}$ (symmetric).
  - Fine (760,480 cells): offset $7.2\text{ }\mu\text{m} / 12.0\text{ }\mu\text{m}$ (weakly off-axis).
- **STL Hash:** [`constant/triSurface/sten70.stl`](file:///mnt/e/Paper6-T6/cfd_local_only/archive/paper6_t6_cfd_2026-09_bulk_moved/A5_sten70_coarse/constant/triSurface/sten70.stl) across all directories matches `47178798e1052ddb7d23d8b318a934baaf42d93d5555b9568eddcabdf9ef8ef2`.
- **Coded Resistance Equilibrium:** At convergence, $p_{\text{target}} = (P_v + R \cdot Q)/\rho$ matches the monitored outlet patch pressure $p_{\text{actual}}$ to $< 5\times 10^{-6}$ kinematic units for both states ($8.35319$ deflected vs $8.38180$ symmetric).

---

## 2. Numbered Findings

### Finding 1: Logical Deadlock in Current Smoke Test Verification Script
- **Severity:** **BLOCKER**
- **Evidence:** [`/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test/compare_smoke.py#L97-L98`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test/compare_smoke.py#L97-L98)
  ```python
  dq = 100 * (m["Q_out_m3s"] / r["Q_out_m3s"] - 1)
  dq_ret = 100 * (m["Q_out_m3s"] / r["returned_value_stageA_A5_ladders_Q_out_m3s"] - 1)
  ok = bool(abs(dq) <= 0.1 and abs(dq_ret) <= 0.1)
  ```
  In [`reference_result.json`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test/reference_result.json), `Q_out_m3s` was overwritten with the symmetric branch value ($1.17825059\times 10^{-6}$), while `returned_value_stageA_A5_ladders_Q_out_m3s` is the deflected branch value ($1.17392231\times 10^{-6}$). These two reference values are separated by $+0.3687\%$. Because `ok` requires both `abs(dq) <= 0.1` AND `abs(dq_ret) <= 0.1`, **no run on either branch can ever pass**. Any future execution of `run_smoke_test.sh` is guaranteed to return exit code 1 (`FAIL`).

### Finding 2: Discrete Bistability Under Identical Discretization and Domain Decomposition
- **Severity:** **MAJOR** (confirms the core diagnostic thesis)
- **Evidence:** 
  1. [`/home/azan/paper6_t6_work/bi_new_from_asym/postProcessing/outletFlux/0/surfaceFieldValue.dat`](file:///home/azan/paper6_t6_work/bi_new_from_asym/postProcessing/outletFlux/0/surfaceFieldValue.dat)
  2. [`/home/azan/paper6_t6_work/bi_arch_from_sym/postProcessing/outletFlux/0/surfaceFieldValue.dat`](file:///home/azan/paper6_t6_work/bi_arch_from_sym/postProcessing/outletFlux/0/surfaceFieldValue.dat)
  3. [`/home/azan/paper6_t6_work/smoke_cont/log.simpleFoam.cont`](file:///home/azan/paper6_t6_work/smoke_cont/log.simpleFoam.cont)
  Cross-mapping proves that both solutions are stable fixed points of the discrete equations. On the new mesh, the deflected state remains steady for 4,000 iterations ($Q_{\text{out}} = 1.173903\times 10^{-6}$). On the archived mesh, the symmetric state remains steady for 4,000 iterations ($Q_{\text{out}} = 1.178251\times 10^{-6}$). Linear solver residuals are at machine limits ($10^{-8}-10^{-9}$), excluding numerical drift. Furthermore, this explains the non-monotonicity in [`stageA_A5_ladders.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24/stageA_A5_ladders.csv): the coarse mesh landed on the deflected branch ($FFR = 0.78396$), whereas medium ($0.78320$) and fine ($0.78791$) were on the symmetric branch.

### Finding 3: Inexact Description of Mesh Coordinate Perturbations
- **Severity:** **MINOR**
- **Evidence:** [`/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md#L17`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md#L17) vs $k$-d tree nearest-neighbor analysis of [`points`](file:///mnt/e/Paper6-T6/cfd_local_only/archive/paper6_t6_cfd_2026-09_bulk_moved/A5_sten70_coarse/constant/polyMesh/points)
  The diagnosis claims that all $4\%$ of points differing by $> 0.1\text{ }\mu\text{m}$ lie "near the wall ($r \in [1.66, 1.80]\text{ mm}$), $x \in [-0.1, 3.7]\text{ mm}$". A rigorous $k$-d tree distance query reveals that the 8,666 points ($4.05\%$) differing by $> 0.1\text{ }\mu\text{m}$ actually span $x \in [-11.13, 98.47]\text{ mm}$ and $r \in [0.55, 1.80]\text{ mm}$. The tight bounding box described in the diagnosis only applies to points differing by $> 1.0\text{ }\mu\text{m}$ ($x \in [-0.10, 3.69]\text{ mm}$) and $> 1.5\text{ }\mu\text{m}$ ($r \in [1.66, 1.80]\text{ mm}$). This does not invalidate the thesis that cfMesh is non-deterministic under multi-threading, but the documentation is imprecise.

### Finding 4: Inconsistent Documentation in SETUP.md
- **Severity:** **MINOR**
- **Evidence:** [`/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/SETUP.md#L25-L28`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/SETUP.md#L25-L28)
  [`SETUP.md`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/SETUP.md) Section 4 still instructs the user to expect 2000 iterations and specifies default workdir `./smoke_work` (which is rejected by preflight in [`run_smoke_test.sh`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test/run_smoke_test.sh#L53-L56)). This must be updated to 3000 iterations and native `/tmp` scratch paths as noted in Item 3 of the proposed changes.

### Finding 5: Uninvestigated SIGFPE Crash Event
- **Severity:** **MINOR**
- **Evidence:** [`/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md#L21`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md#L21)
  The author reports an unreproduced `SIGFPE` at iteration 1301 on an identical setup. While `t2_archmesh_patch` ran 3000 iterations without error, transient linear solver instabilities near the bifurcation point cannot be entirely ruled out during initial transients.

---

## 3. Answers to Auditor Questions (a)–(d)

### (a) Is the diagnosis supported by the evidence, or is an alternative explanation not excluded?
**The diagnosis of discrete bistability is fully supported; alternative explanations are excluded.**
1. **Incomplete Convergence:** Excluded. Run `smoke_cont` reached 12,000 iterations, and `bi_new_from_asym` / `bi_arch_from_sym` ran to 4,000 iterations. Monitors are stationary to $10^{-13}\text{ m}^3/\text{s}$, and linear solver residuals for $U$ and $p$ are converged to $\sim 10^{-8}-10^{-9}$. Neither branch exhibits any secular drift towards the other.
2. **Boundary Condition Relaxation:** Excluded. The coded BC is in exact algebraic equilibrium: $p_{\text{patch}} = (P_v + R \cdot Q)/\rho$ holds to $< 5\times 10^{-6}$ for both branches.
3. **Domain Decomposition:** Excluded as a cause of bistability. Both branches were proven to exist and remain stable on the exact same 8-rank Scotch decomposition (`bi_new_from_asym` vs `smoke_ref`). Scotch partitioning and thread-order perturbations merely determine which basin of attraction the transient solution enters from a uniform zero initial state.
4. **Physical Coanda Bifurcation:** Stenotic expansion flow at $Re_{\text{throat}} \approx 450$ through a 70% diameter stenosis (11:1 area expansion) is physically subject to symmetry-breaking wall attachment.

### (b) Is accept-either-branch a sound smoke-test criterion, or should the case be replaced/forced?
**Accept-either-branch is sound, provided both flow and pressure are jointly validated.**
- **Why it is sound:** The purpose of a smoke test is to verify that a second machine's compiler, MPI environment, cfMesh binary, OpenFOAM libraries, and solver scripts execute correctly. Because both branches are valid, fully converged discrete solutions of the exact same governing equations and geometry, forcing one branch is artificial.
- **Why dual-variable gating is mandatory:** The two branches differ by $0.369\%$ in flow ($1.17390\times 10^{-6}$ vs $1.17825\times 10^{-6}$) and $0.00149$ in FFR ($0.78397$ vs $0.78248$). Checking $|Q/Q_b - 1| \le 0.1\%$ together with $|\text{FFR} - \text{FFR}_b| \le 0.0005$ guarantees that the second machine has converged to a genuine physical branch and prevents spurious passes.
- **Feasibility of forcing without shipping fields:** Forcing a branch would require either shipping the full 198k-cell mesh (which defeats testing cfMesh) or injecting an ad-hoc asymmetric perturbation in `0/U` (which complicates the reference setup). Accept-either-branch with dual-variable checks is superior.

### (c) Is the U3D caveat worded correctly, and is further evidence required before $U_{3D} = 0.00055$ stands?
**The caveat is worded correctly and no further solver runs are required before $U_{3D} = 0.00055$ stands.**
- **Physical Consistency of U3D:** The U3D refinement study ([`STAGE-A-VALIDATION.tex#L1521`](file:///home/azan/paper6_t6_work/scratchpad/T6_repo/drafts/stageA_validation/STAGE-A-VALIDATION.tex#L1521), [`U3D_sten70.csv`](file:///mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24/U3D_sten70.csv)) refines the throat zone down to $12.5\text{ }\mu\text{m}$ (2.6M to 7.6M cells). The finest 3D levels (S12A: $\text{FFR} = 0.79031$; S12B: $\text{FFR} = 0.79042$) agree with the 2D axisymmetric wedge solution (W3: $\text{FFR} = 0.79037$) within $0.00006$. Because a 2D axisymmetric wedge mathematically cannot support a 3D wall-deflected jet, this near-perfect agreement ($< 0.01\%$) proves that the refined 3D meshes in U3D are on the symmetric branch.
- **Caveat Scope:** Because volume fields of S50/S25/S12 were purged to save disk space, direct jet centroid offsets cannot be computed from disk. Acknowledging this as indirect evidence in the report note is scientifically rigorous and sufficient.

### (d) Anything else missing?
1. **Schema and Automation in `reference_result.json`:** The proposed schema must ensure backward compatibility so that automated test runners on the second machine correctly extract the matched branch metadata.
2. **Re-verification of Preflight Limits:** Ensure that `compare_smoke.py` exits with code 0 on matched pass, code 1 on tolerance fail, and code 3 on mesh/run non-comparability.
3. **Precision of Point Deviation in Diagnosis:** Minor revision of line 17 of [`B3_DIAGNOSIS.md`](file:///home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/b3_audit/B3_DIAGNOSIS.md#L17) to accurately distinguish the $> 0.1\text{ }\mu\text{m}$ spatial distribution from the $> 1.0\text{ }\mu\text{m}$ near-wall cluster.

---

## 4. Final Verdict

**DIAGNOSIS SOUND**  
**PROPOSED CHANGE: ACCEPT WITH CONDITIONS**

*(Condition: The implementation of `compare_smoke.py` must eliminate the logical conjunction deadlock identified in Finding 1 and enforce joint gating on both $Q_{\text{out}}$ within $\pm 0.1\%$ and $\text{FFR}_{x56.5}$ within $\pm 0.0005$ for the matched branch).*
