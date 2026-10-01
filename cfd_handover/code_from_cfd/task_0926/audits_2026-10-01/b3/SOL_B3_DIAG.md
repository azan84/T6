1. **MAJOR — (a) Two stable discrete branches are supported; the claimed cause of branch selection is not fully isolated.**  
   The monitor histories show two distinct plateaus:

   - Symmetric/new mesh: \(Q=1.17825059\times10^{-6}\) at 3000 and \(1.17825058\times10^{-6}\) at 12000 in [smoke_ref outletFlux](/home/azan/paper6_t6_work/smoke_ref/postProcessing/outletFlux/0/surfaceFieldValue.dat) and [smoke_cont outletFlux](/home/azan/paper6_t6_work/smoke_cont/postProcessing/outletFlux/3000/surfaceFieldValue.dat).
   - Deflected/archived mesh: \(Q=1.17390294\times10^{-6}\) at 3000 in [t2 outletFlux](/home/azan/paper6_t6_work/t2_archmesh_patch/postProcessing/outletFlux/0/surfaceFieldValue.dat).
   - Cross-mapped deflected state remains \(1.17390288\times10^{-6}\) on the new mesh through 4000 iterations in [bi_new_from_asym outletFlux](/home/azan/paper6_t6_work/bi_new_from_asym/postProcessing/outletFlux/0/surfaceFieldValue.dat).
   - Cross-mapped symmetric state remains \(1.17825071\times10^{-6}\) on the archived mesh through 4000 iterations in [bi_arch_from_sym outletFlux](/home/azan/paper6_t6_work/bi_arch_from_sym/postProcessing/outletFlux/0/surfaceFieldValue.dat).

   The last-200-iteration Q bands are only \(0.000006\%\)–\(0.000031\%\), and the continued symmetric run remains unchanged to 12000 iterations. Ordinary incomplete convergence is therefore convincingly excluded for Q and the reported pressure metrics.

   However, all runs use eight-way `scotch`. The new and archived meshes produce different partitions—2899 versus 2869 processor faces in [smoke_ref log.decomposePar](/home/azan/paper6_t6_work/smoke_ref/log.decomposePar) and [t2 log.decomposePar](/home/azan/paper6_t6_work/t2_archmesh_patch/log.decomposePar). No serial or alternative-decomposition default-field run isolates mesh realization from decomposition-induced perturbations. The evidence supports “small numerical perturbations select the basin,” but not specifically “mesh differences decide it.”

2. **MINOR — (a) The relaxation scheme does not explain away the two fixed states, but its influence on basin selection remains untested.**  
   Both cross-mapped states persist under the identical SIMPLE settings and coded resistance outlet in [fvSolution](/home/azan/paper6_t6_work/smoke_ref/system/fvSolution) and [0/p](/home/azan/paper6_t6_work/smoke_ref/0/p). At a true fixed point, the coded-BC relaxation \(p=(1-r)p_\text{old}+rp_\text{target}\) reduces to \(p=p_\text{target}\), so relaxation does not create a different converged boundary condition. It could nevertheless affect which basin a default initialization enters. Thus “BC-relaxation artifact” is excluded as an explanation of the two converged values, but not as a branch-selection influence.

3. **MAJOR — Part of the mesh-comparison statement is numerically inaccurate.**  
   Independent nearest-point comparison of [archived points](/home/azan/paper6_t6_work/a5_arch8/constant/polyMesh/points) and [new points](/home/azan/paper6_t6_work/smoke_ref/constant/polyMesh/points) confirms:

   - 214,037 points and identical bounding boxes.
   - 4.0488% have nearest-point displacement \(>0.1\,\mu\mathrm m\).
   - Maximum displacement is \(2.1224\,\mu\mathrm m\).
   - Only 63.96% coincide to \(10^{-12}\,\mathrm m\), not 96%.

   More importantly, points differing by \(>0.1\,\mu\mathrm m\) span \(x=-11.13\) to \(98.47\) mm and radius \(0.552\) to \(1.800\) mm. It is only the differences \(>1\,\mu\mathrm m\) that are confined near the inlet wall (\(x=-0.096\) to \(3.692\) mm, radius \(1.604\)–\(1.800\) mm). The diagnosis should say “95.95% agree within \(0.1\,\mu\mathrm m\), and the largest differences are near the inlet wall.”

4. **MINOR — The evidence-table scalar values checked are accurate.**  
   The archived result is \(Q=1.17392231\times10^{-6}\) and \(p_\text{meas}=8.87426046\) in the [archived monitors](/mnt/e/Paper6-T6/cfd_local_only/archive/paper6_t6_cfd_2026-09_bulk_moved/A5_sten70_coarse/postProcessing/outletFlux/0/surfaceFieldValue.dat). Using the code’s \(1060/11998.98\) conversion gives FFR \(=0.78395964\), matching 0.78396.

   The other checked FFRs are likewise correct: 0.78396694 for the deflected rerun and 0.78248298 for the symmetric run. The symmetric result is +0.368702% relative to the returned value; the archived-mesh rerun is −0.001647%. The two ±0.1% Q windows do not overlap.

   Read-only reconstruction also reproduces the reported jet offsets: approximately 85.085/82.685 μm for the deflected branch and 0.886/1.520 μm for the symmetric branch at 50/56.5 mm.

5. **MINOR — One stability sentence overstates the available duration.**  
   “Each is stable for ≥4000 iterations on either mesh” is not demonstrated for the deflected branch on the archived mesh: [t2](/home/azan/paper6_t6_work/t2_archmesh_patch/log.simpleFoam) ends at 3000. What is supported is symmetric/new to 12000, symmetric/archived to 4000, deflected/new to 4000, and deflected/archived to 3000. This does not materially weaken the bistability conclusion.

6. **MAJOR — (b) Accept-either-branch is sound only if the smoke test’s purpose is redefined.**  
   It is a reasonable health/regression test for “this implementation reaches one of two validated solutions of a bistable case.” It is not literally a test that “a second machine reproduces one returned result,” because the symmetric \(1.17825059\times10^{-6}\) value is not the returned A5 result. The current [reference_result.json](/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test/reference_result.json) itself records that symmetric value, while the current [compare_smoke.py](/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/smoke_test/compare_smoke.py) correctly fails it against the returned value.

   Accept the proposed criterion only if documentation explicitly calls it a two-branch solver/mesh-pipeline smoke test and the symmetric state is treated as an independently validated reference outcome. If reproduction of the published returned result is mandatory, replace or force the case. Without shipping fields, suitable approaches are:

   - Use a returned case demonstrably away from a bifurcation.
   - Use a deterministic, documented transverse initial perturbation and validate that it selects the deflected state across mesh regenerations, decompositions, and machines.
   - Ship the archived `polyMesh` if testing the solver rather than cfMesh reproducibility is acceptable.

7. **MAJOR — (c) The proposed U3D caveat is directionally correct but still too affirmative.**  
   Because the U3D fields were purged, scalar agreement with two zone families and a wedge solution is “consistent with” but does not establish branch identity. None of the permitted evidence contains the cited U3D per-level fields or source tables, so the \(10^{-4}\) agreements and the value 0.00055 could not be independently audited here.

   The wording should state that branch consistency is unverified, not merely indirect. Before 0.00055 is used as a branch-consistent discretization uncertainty, retain or regenerate at least one branch-sensitive diagnostic at every U3D level—jet centroid/vector, transverse velocity norm, or downstream velocity slices—in addition to Q/FFR. Without that, 0.00055 may stand only as a provisional scalar estimate with an explicit unresolved branch-consistency caveat.

8. **MAJOR — (d) Add convergence and reference-governance safeguards.**  
   The proposed comparison should require a final-window stability test for both Q and FFR, not merely completion plus a final value. This protects against a run crossing an acceptance window during a slow transition. Also:

   - Call the mesh condition “same recipe/cell count,” not “same mesh”; current checks do not establish mesh identity.
   - Prevent `--write-reference` from silently replacing an existing branch reference without an explicit branch/update option.
   - Exercise both branch paths in comparison-code tests even if two real default runs happen to land on the same branch.
   - Record exact mesh hashes or mesh-comparison statistics and decomposition metadata in branch provenance.
   - Correct “same 0/ files” for mapFields cases: their mapped `0/U` and `0/p` necessarily differ from the default initial files.

**DIAGNOSIS SOUND WITH CAVEATS — PROPOSED CHANGE: ACCEPT WITH CONDITIONS**
