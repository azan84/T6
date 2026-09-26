# 3D CFD arm — specification and handover (DRAFT v0.1, 2026-09-18)

> **⚠ v0.1 IS SUPERSEDED IN PART — read `references/FABLE-REVIEW-CFD-2026-09-18.md` before using this document.**
> The operator agreed to decisions §2.1 and §2.2 on 2026-09-18; an independent adversarial review commissioned the
> same day then returned **§2.1 MODIFY, §2.2 REJECT as written**, plus a flaw in §5/§2's "3D verifies, never tunes"
> rule that means the arm as specified below **does not test the paper's thesis**. Summary of required changes
> (pending operator confirmation, then this spec is rewritten as v0.2):
> 1. **Geometry → three-rung ladder on the same instances:** 0D → 3D polyball (*control*: physics only) → **3D real
>    lumen (*primary replication*, ~30 instances)**. Polyball alone tests solver physics, which is already in print
>    (Grande 2021: FFR3D 0.76 vs FFR1D-3D 0.78) and shares the 0D model's radius bias; the half of "0D is not ground
>    truth" that matters for a segmentation-error paper is the reduction lumen → centreline + radius. Real-lumen errors:
>    topological = delete branch voxels and re-run marching cubes; lesion/length/taper = radial vertex deformation;
>    re-measure the as-meshed radius and feed it back to the 0D twin. Five real cases cannot support a κ estimate.
> 2. **Truncate at 0.75 mm, not 1.0 mm.** Reviewer's probe on the 150 selected instances: at 1.0 mm the measurement node
>    survives in only 82/150, 112/150 have no side branch left to miss, 49/150 are single-outlet. 0.75 mm (already the
>    protocol's "resolved" radius) keeps all 150 measurement nodes.
> 3. **BC structure (leaky vs discrete) becomes a pre-registered FACTOR of the primary 0D experiment**, not a bridge:
>    the two disagree on the ≤ 0.80 decision in 29/150 instances (mean shift −0.077), and the leaky model **partly
>    re-inserts a deleted branch as a point leak at its parent node** (a direct consequence of
>    w(v) = max(r_ref(v)³ − Σ children r_ref³, 0)) — so it dampens the missed-branch error by construction. A result is
>    claimed only if it holds under both structures. Wall leakage in 3D stays rejected.
> 4. **Protocol C is tuned INSIDE each fidelity**, against that fidelity's own clean baseline. In steady state this costs
>    one extra solve: prescribe the clean model's outlet flows on the corrupted geometry, read outlet pressures, set
>    R_i = (p_i − P_v)/Q_i. The "15 solves per condition" that motivated tune-in-0D was a pulsatile figure.
> 5. **Protocol C can only be FLOW-matched.** In a steady tree, if outlets distal to the lesion match the baseline in
>    both pressure and flow, the distal pressure — and therefore FFR — is the baseline's by construction, and no flip is
>    possible. The thesis survives only for flow (perfusion-type) targets, which are also the only clinically available
>    ones. **This corrects STUDY-PLAN-v2 §E2, which specified flows *and* pressures.**
> 6. **Primary endpoint:** error-induced ΔFFR (corrupted − clean) within each fidelity, 0D vs 3D; flips secondary, each
>    against its own fidelity's baseline; plus a 3D "thesis panel" of outlet-flow residual vs lesion-FFR error.
> 7. **Instances:** 30 (10 per vessel) from the 42 in FFR 0.70–0.90 under both BC structures with ≥ 1 side branch
>    ≥ 0.75 mm; exclude single-outlet trees. ~320 meshes, ~1,250 steady solves, ~3,300 core-hours; pulsatile runs 20 → 6.
>    **CFD machine: 16 physical cores (32 threads) → ≈ 8.6 days steady + ≈ 3 days pulsatile.** Fallback if real-lumen
>    meshing cannot be automated: 20 real-lumen instances × the two topological error types — never polyball-only.
> The reviewer's numbers come from quick probes with the project's solver (`references/FABLE-REVIEW-CFD-2026-09-18-probe/`),
> **not protocol-grade** (no verification suite, single-scalar tuning, largest downstream branch only) — reproduce them
> before freezing.

**Status:** draft. Expands STUDY-PLAN-v2 §E3, which was a paragraph. Nothing here has been run — the CFD machine is
separate from the analysis machine, so this document is written as a **handover**: what the analysis side delivers,
what the CFD side does, what comes back. To be frozen with the rest of WP-0.

## 1. What this arm is for — and what it is not
**Question:** *does the 0D decision-flip pattern survive at 3D fidelity?* This answers the predicted reviewer objection
"a 0D model of a consensus label is not ground truth." Outcome: **FFR only.**
**Not** WSS/OSI (dropped — a plaque-vulnerability question this paper does not ask; see STUDY-PLAN-v2 §12).
**Not** an independent 3D study: 3D *verifies* the 0D experiment on a subset; it never tunes anything.

Two deliverables:
- **E3a — steady FFR replication**, 30–50 instances from the selected sweep cohort, all error types × protocols A/B/C.
- **E3b — mechanism figure**, 5 instances, pulsatile, Protocol C: outlets matched, interior pressure field wrong.

## 2. Two design decisions this spec makes (both need the operator's agreement)

### 2.1 Geometry: regenerate the surface from centreline + radius — do not edit the ImageCAS-X surface
The plan assumed surface-level corruption (clip a branch, cap, repair) and flagged that *no source in the corpus has
a repair step* (FAME discarded 14.8 % of geometries for self-intersection rather than repair them).
**Recommended instead:** build every 3D surface by **implicit polyball modelling** from the centreline and radius
profile (VMTK `vmtkcenterlinemodeller` → marching cubes). Consequences:
- An implicit union-of-spheres surface is watertight and manifold **by construction** — it cannot self-intersect.
  This removes most of the Gate M1 risk rather than mitigating it.
- **Every error type becomes the same edit in 3D as in 0D**: missed branch = delete that branch's centreline;
  truncation = cut the centreline; stenosis-length and taper = edit the radius profile. No clipping, no capping, no
  repair. The 3D geometry is the 0D geometry, exactly.
- The comparison isolates **solver fidelity** (0D vs 3D physics) from geometric discrepancy. With the ImageCAS-X
  surface, the 3D lumen and the 0D EDT-radius would differ, and any 0D–3D disagreement would be uninterpretable.
- **Cost, stated plainly:** real lumens are not circular; this reconstruction is. Cross-sectional shape realism is
  given up in E3a. It is recovered in E3b, where the 5 mechanism cases *also* run on the real ImageCAS-X surface.

### 2.2 Boundary-condition structure: 0D and 3D must share it, and currently they do not
The 0D model sheds flow continuously along every vessel (Murray **distributed leakage** — the fix that made real-data
FFR physiological). A standard 3D model has **discrete outlets only**; flow cannot leave through the wall. Comparing
leaky-0D against discrete-3D would confound fidelity with BC structure: the 3D model would push more flow through the
distal vessel and read a lower FFR for a reason that has nothing to do with 3D physics.
**Decision:** the replication subset is run in a **discrete-outlet configuration on both sides**:
- tree truncated where r_fit < 1.0 mm (meshable, resolved); every retained branch end is an outlet;
- outlet resistance R_i = C′ / r_ref,i³ (Murray), C′ calibrated on the healthy-equivalent network so inflow equals the
  Murray demand Q = k r_inlet³ — the same demand as the leaky model;
- the 0D solver gains a `leak=False` mode implementing exactly this (**to build** — one option on the bed weights).
Reported comparisons: **0D-discrete vs 3D-discrete** (fidelity, the point of this arm) and **0D-leaky vs 0D-discrete**
(BC-structure effect — itself on-theme, and cheap since it is 0D only).
*Alternative considered and rejected:* wall mass-sink leakage in OpenFOAM (fvOptions). Non-standard, adds method risk,
and no reviewer asks for it.

## 3. Division of labour
| Analysis machine (this Mac) | CFD machine |
|---|---|
| Select instances; build per-case **packages** (§4) | Install OpenFOAM, VMTK, mesher; verify licences |
| Run the 0D-discrete counterpart of every case | Surface → extensions → mesh → solve → sample |
| Analyse returned CSVs; concordance statistics; figures | Return one results CSV per batch (§8); keep meshes/fields locally |

Packages are kilobytes (centrelines + tables) — safe to pass through Drive. **Meshes and fields never go to Drive.**

## 4. Case package (one folder per run, generated by `code/export_cfd_case.py` — to build)
```
<case_id>/                      case_id = <scan>_<side>_<vessel>_<loc>_<L>_<DS>__<errortype>__<protocol>
  centreline.vtp                polydata, mm, LPS; point arrays: MaximumInscribedSphereRadius (mm), segment_name, branch_id
  outlets.csv                   outlet_id, x,y,z (mm), unit normal, r_ref_mm, R_SI [Pa s m^-3], R_kinematic [m^-1 s^-1]
  inlet.json                    P_aorta = 11999 Pa (90 mmHg), P_venous = 667 Pa (5 mmHg), rho = 1060, mu = 0.004
  probes.csv                    probe_id, x,y,z: inlet; lesion throat; measurement point (20 mm distal to the lesion's
                                distal edge); every outlet
  expected_0D.json              0D-discrete prediction: inflow, per-outlet flow, FFR at every probe  (blind-able: see §9)
  meta.json                     lesion (centre, length, %DS), error type and magnitude, protocol, source instance
```
Geometry per instance: 1 baseline (lesion, correct anatomy) + 4 error types = **5 surfaces/meshes**.
Runs per instance: baseline + 4 × protocols A/B/C = **13 steady solves** (protocols differ only in `outlets.csv`).

## 5. CFD pipeline (per geometry)
1. **Surface:** `vmtkcenterlinemodeller` (polyball, image spacing ≤ 0.1 mm) → `vmtkmarchingcubes` → light Taubin
   smoothing (volume-preserving; verify throat radius unchanged to < 1 %).
2. **Flow extensions:** `vmtkflowextensions`, 5 diameters at the inlet, 3 at each outlet, along the centreline tangent.
   Clip to planar caps; name patches `inlet`, `outlet_<id>`, `wall`.
3. **Mesh:** cfMesh `cartesianMesh` (or snappyHexMesh). Base cell ≈ D_local/20 with refinement in the lesion ±2
   lengths (throat ≥ 12 cells across even at 80 %DS); 4 boundary layers, growth 1.2. Expect 0.5–2 M cells.
   `checkMesh` must pass: non-orthogonality < 70°, skewness < 4, no negative volumes.
4. **Solve (E3a):** `simpleFoam`, laminar, Newtonian (ν = 3.774e-6 m² s⁻¹), rigid no-slip wall. Coronary Re is O(100–600);
   if the throat Re exceeds ~1000 at 80 %DS, flag the case — do not silently switch turbulence models.
   - inlet: `totalPressure` p₀ = P_aorta/ρ (kinematic); velocity `pressureInletOutletVelocity`.
   - outlets: **resistance BC** p_i = P_venous + R_i·Q_i, implemented as `codedFixedValue` reading the patch flux each
     iteration with under-relaxation 0.2–0.3 (or Mao's Windkessel BC in its resistance-only limit).
     *Fallback if unstable:* prescribe the 0D outlet flows (`flowRateInletVelocity`, negative) and report it — 3D then
     predicts pressure drop but not flow split, a weaker but still valid fidelity check.
   - convergence: residuals < 1e-5 **and** inlet flow, every outlet flow and the measurement-point pressure each stable to
     < 0.1 % over the last 200 iterations; global mass imbalance < 0.1 %.
5. **Sample:** area-averaged static pressure on a cross-section at every probe (not a point value); FFR = p/P_aorta.
6. **E3b only:** `pimpleFoam`, physiological aortic pressure waveform at the inlet, RCR outlets (R from the package, C from
   the 0D protocol), 5 cycles, last cycle analysed; write pressure and velocity fields for the figure.

## 6. Verification of the CFD setup itself (before any study case)
| Test | Pass |
|---|---|
| Straight pipe, Poiseuille | pressure drop within 1 % of analytic |
| Idealised cosine stenosis 50/70/80 %DS (the 0D self-test vessel) | trend and magnitude consistent with Young–Tsai; tabulate against the 0D values (0.919 / 0.693 / 0.427) — differences are a *result*, not a failure |
| Resistance BC | outlet pressure equals P_v + R·Q to 0.1 % at convergence |
| Mesh independence, 2 study cases × 3 levels | ΔFFR at the measurement point < 0.005 between the two finest (matches the 0D resolution floor) |

## 7. Gate M1 — re-scoped pilot (run first, on the CFD machine)
Three packages: a clean baseline · an **80 %DS** lesion · a **missed-side-branch** corruption.
**Pass:** all three reach a `checkMesh`-clean mesh and a converged solve **without manual geometry repair**; resistance
BC stable; 3D-discrete FFR within 0.05 of 0D-discrete at the measurement point (a larger gap is not a failure but must
be understood before scaling); wall-clock per case recorded.
**Fail →** E3 is delayed, not cancelled; the primary 0D paper does not depend on it.

## 8. What comes back
`cfd_results_<batch>.csv`: case_id, n_cells, checkMesh status, iterations, final residuals, mass imbalance, inlet flow,
per-outlet flow, area-averaged pressure at every probe, throat Reynolds number, wall-clock, cores, OpenFOAM version,
BC mode (resistance | prescribed-flow), notes. Plus `cfd_failures.csv` with the failure stage — **mesh/solve failure
rate by error type is itself a reportable finding** (nobody has published one).

## 9. Blinding (cheap, and worth doing)
The CFD operator does not need `expected_0D.json` to run a case. Withhold it for the study batch and release it only
after the results CSV is returned: the 3D numbers are then produced blind to the 0D predictions they are testing.

## 10. Compute estimate (to be replaced by M1's measured numbers)
E3a: 40 instances × 5 meshes = 200 meshes; × 13 = **520 steady solves**. At ~1 M cells, ~20 min on 8 cores each →
**~1,400 core-hours** → ~2 days on 32 cores, under a day on 64. Meshing is the human-time cost, not solving.
E3b: 5 instances × 2 (baseline, topological error under C) × 2 surfaces (polyball, real) = 20 pulsatile runs at
~24 h / 8 cores (Mao's figure) → ~3,800 core-hours → ~5 days on 32 cores. Run after E3a.

## 11. Analysis of returned results (analysis machine)
- Concordance of the binary decision (FFR ≤ 0.80), 0D-discrete vs 3D: Cohen's κ, with the pre-registered H4 criterion
  κ > 0.6; per error type and protocol.
- Bland–Altman of FFR at the measurement point; bias and limits of agreement; bias vs %DS (0D lumped stenosis models
  are known to drift at high severity — expect and report it).
- The key test: **is the A/B/C contrast preserved?** For each instance, compare ΔFFR(C − A) and the flip indicator in 0D
  and in 3D. The arm succeeds if the *pattern* replicates even where absolute FFR differs.

## 12. Open items
- [ ] Operator agreement on §2.1 (regenerated surfaces) and §2.2 (discrete-outlet configuration).
- [ ] Mao 2025 `CoronaryHemodynamics`: licence is unstated in the paper — verify on GitHub before depending on it.
      Nothing in this spec requires it; plain OpenFOAM + a coded BC suffices.
- [ ] Build `leak=False` in `zerod_ffr.py` and `export_cfd_case.py`; validate that 0D-discrete is physiological on the
      truncated tree (the leak-free model failed earlier, but on untruncated 0.3 mm tips and before two bugs were fixed).
- [ ] CFD machine: core count dedicated to T6; OpenFOAM version; VMTK install.
- [ ] Decide the E3a instance count after M1 reports wall-clock per case.
