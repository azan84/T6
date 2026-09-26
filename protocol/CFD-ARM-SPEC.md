# 3D CFD arm — specification and handover (v0.2, 2026-09-18)

**Status:** v0.2, operator-approved 2026-09-18. Supersedes v0.1 (`archive/CFD-ARM-SPEC-v0.1-superseded-2026-09-18.md`)
after an independent adversarial review (`../references/FABLE-REVIEW-CFD-2026-09-18.md`) returned *MODIFY* and *REJECT*
on v0.1's two design decisions and showed that v0.1's 3D arm did not test the paper's thesis. To be frozen with WP-0.
**Machine:** separate CFD PC, **16 physical cores** (32 threads — plan on 16; OpenFOAM is memory-bandwidth-bound).
Nothing here has been run. This document is a handover: what the analysis side delivers, what the CFD side does, what
comes back.

## 0. Time protection — read this first
The operator's constraint is *do not lose time*. Three rules make that structural rather than hopeful:
1. **The 3D arm is off the critical path.** The 0D experiment (STUDY-PLAN-v2 Phases 1–2, 4) runs on the analysis
   machine regardless of anything below. No 3D result gates a 0D result.
2. **Build on geometry that cannot fail, then swap the geometry.** Stage B (polyball) debugs meshing, the coupled
   outlet BC, in-fidelity tuning and sampling on surfaces that are watertight by construction. Stage C (real lumen)
   reuses all of it and changes only surface generation — the single risky step is isolated.
3. **The risky step is tested first, in parallel, with a hard kill.** Gate M1 (§7) tries real-lumen meshing on three
   cases on day one. Pass → full design. Fail after 5 working days of effort → the fallback in §9, no further debate.

## 1. What this arm is for
**Question:** *does the absorption effect — boundary conditions tuned to match their flow targets while the FFR ≤ 0.80
decision still moves — exist at 3D fidelity, on real lumens?*
It answers the predicted objection "a 0D model of a consensus label is not ground truth." **FFR only**; no WSS/OSI.
v0.1 asked a weaker question (do two solvers agree on pressure drop under identical BCs), which Grande 2021 already
answers in print ("FFR3D = 0.76, FFR1D–3D = 0.78").

## 2. Design — five decisions, each with its reason

### 2.1 A three-rung ladder on the same instances
| Rung | Geometry | Role | What a disagreement with the rung above means |
|---|---|---|---|
| **0D** | centreline + radius network | the primary experiment | — |
| **3D-polyball** | implicit tube from the *same* centreline + radius | **control**: physics only | the 0D lumped physics (Poiseuille + expansion loss) is inadequate |
| **3D-real** | the ImageCAS-X lumen surface | **primary replication** | the reduction lumen → centreline + radius drives the result |
For a paper about *segmentation* error, the second gap is the one that matters, and polyball alone cannot see it: the
0D model and a polyball share the same radius (including the ~10–15 % under-read from an off-axis centreline) and would
agree with each other while both being wrong. Five real cases (v0.1) cannot support a κ estimate.

### 2.2 Protocol C is tuned inside each fidelity
v0.1 tuned in 0D and imposed the parameters on 3D. The 3D outlets were then never matched to anything, and the arm
could not show absorption. In steady state in-fidelity tuning costs **one extra solve**: prescribe the clean model's
outlet flows on the corrupted geometry, read the outlet pressures, set R_i = (p_i − P_v)/Q_i (Fossan's own procedure).
v0.1's "15 solves per condition" was a pulsatile figure misapplied to a steady arm.

### 2.3 Protocol C is flow-matched — by logical necessity
In a steady tree, if outlets distal to the lesion reproduce the baseline's pressure **and** flow, the distal pressure —
and therefore FFR — is the baseline's by construction; no decision can flip. "Validated" therefore means **matched on
outlet flows** (perfusion-type targets), which are also the only targets a clinic has: nobody measures coronary outlet
pressure. This corrects STUDY-PLAN-v2 §E2 and is stated in the paper as the definition of validation, not a caveat.

### 2.4 Discrete Murray outlets on both sides, truncation at 0.60 mm (r_ref)
3D cannot shed flow through the wall, so the replication runs **discrete-outlet** in 0D and 3D alike:
R_i = C′ / r_ref,i³, C′ calibrated on the healthy-equivalent network to the Murray demand Q = k r_inlet³.
Truncate where **r_ref < 0.60 mm** in both fidelities (`r_ref`, not `r_fit` — the monotone, parent-capped reference;
the code and the 3D clipping rule must name the same quantity). `R_RESOLVED` stays 0.75 mm for lesion detection and
reporting. Revised twice: v0.1's 1.0 mm cut was fatal on this small-vessel cohort (measurement node survives in only
82/150 instances, 112/150 have no side branch left to miss, 49/150 single-outlet). A second probe then showed 0.75 mm
is still too aggressive for the **missed-branch error type**.

> **REPRODUCED PROTOCOL-GRADE 2026-09-19** on all **108 trees of the frozen cohort**, and the choice of 0.60 mm
> stands (`references/TRUNCATION-PROBE-2026-09-19/`):
>
> | cut | trees left single-outlet | lesion slots keeping a deletable downstream branch |
> |---|---|---|
> | **0.60 mm** | **5 / 108** | **349 / 470 = 74 %** |
> | 0.75 mm | 20 / 108 | 258 / 468 = 55 % |
> | 1.00 mm | 39 / 108 | 51 / 275 = 19 % |
>
> The deletable-branch figures the decision actually rested on reproduce closely (74 % vs the claimed 77 %; 55 % vs
> 54 %). The single-outlet counts are lower here (5/108 and 20/108 against 18/140 and 43/140) because the reviewer's
> 140 trees were not the frozen cohort — the cohort has already been filtered for eligibility, so fewer marginal
> trees remain. **Run twice, by two independently written scripts with different loop orders: 324 tree-cut rows and
> ZERO disagreements** on outlet count, slot count or deletable-branch count. The numbers are not an artefact of one
> implementation.
>
> Both runs and both scripts: `references/TRUNCATION-PROBE-2026-09-19/`.

Pre-registered fallback to 0.75 mm if Gate M1 cannot mesh 1.2 mm-diameter outlets; stub rule ≥ 3 diameters.
**Outlet weights: leaf `r_ref^2.66`** (empirical coronary Murray exponent), C calibrated to Q = k·r_inlet³ on the
healthy-equivalent network, and the resulting resistances handed unchanged to 3D. A top-down Murray share was
implemented first and rejected on evidence: it gives the same flow at the lesion and measurement nodes and the same
65 %DS offset, but a larger and more variable tree-level offset (−0.056 ± 0.077 vs −0.044 ± 0.054; 17 vs 11 decision
disagreements in 140 trees) and is discontinuous at the truncation radius.
**Discrete-arm eligibility:** the healthy-equivalent discrete network must have FFR ≥ 0.90 at every resolved
main-vessel node (`Tree.healthy_main_ffr()`); this predicts the leaky/discrete offset with corr 0.92 and keeps
112/140 trees with offset −0.025 ± 0.026 and 1/112 decision disagreements. Additionally **≥ 2 outlets** for
missed-branch/truncation instances and for any Protocol C run — a single-outlet tree has no flow split to match.
Wall-leakage in 3D (fvOptions mass sink) stays rejected: non-standard, and no reviewer asks for it.

### 2.5 BC structure is a factor of the 0D experiment, not a bridge
Leaky and discrete 0D disagree on the ≤ 0.80 decision in **19 of the 97 discrete-eligible instances** (mean shift
−0.051 ± 0.071), and the leaky bed
**re-inserts a deleted branch as a point leak at its parent node** — a consequence of
w(v) = max(r_ref(v)³ − Σ children r_ref³, 0) — damping the missed-branch error by construction
(probe: mean |ΔFFR| under A/B/C 0.059/0.017/0.036 leaky vs 0.112/0.051/0.120 discrete). So the primary 0D ablation runs
under **both** structures, pre-registered, and a claim is made only where it holds in both. The 3D arm replicates the
discrete structure. Optional bridge back to leaky: fit ΔP(Q) laws per segment from the 3D runs and substitute them into
the leaky network.
*These probe numbers are the reviewer's quick checks (`../references/FABLE-REVIEW-CFD-2026-09-18-probe/`), not
protocol-grade. **Reproduce them through the verification suite before freezing** (§10).*

## 3. Instances
**30 instances, 10 per vessel (LAD / LCx / RCA)**, drawn from the selected sweep cohort subject to: baseline FFR_meas in
0.70–0.90 under **both** leaky and discrete 0D; ≥ 1 side branch with r_ref ≥ 0.60 mm (so the missed-branch error
exists); not single-outlet after truncation; and passing the healthy-network gate of §2.4.
**Eligibility on the frozen cohort — MEASURED with the protocol-grade solver, 2026-09-18**
(`code/discrete_arm.py` → `results/discrete_arm_eligibility.csv`; every exclusion logged with its reason):

| stage | n |
|---|---|
| frozen cohort | 150 |
| eligible for the discrete arm | **97** (65 %) |
| …of which a deletable downstream branch survives (missed-branch / truncation types) | **77** |
| …of which the FFR band is also unchanged under the discrete bed | **36** |
| **3D/CFD pool: eligible ∧ deletable branch ∧ band holds in both** | **33** — RCA 22, LCx 6, LAD 5 |

Exclusions: 48 fail the healthy-network gate (FFR < 0.90), 5 have fewer than 2 outlets. The discrete bed shifts FFR by
**−0.051 ± 0.071** (min −0.317, max +0.057) and **disagrees with the leaky bed on the 0.80 decision in 19 of 97**
instances — which is why bed structure is a factor, not a bridge, and why **bands are pre-registered per structure**.
**DECIDED 2026-09-18, before any 3D run: the "band holds in both structures" requirement is DROPPED for the 3D
subset.** Rationale: the 3D arm replicates the **discrete** bed, so the instance's leaky band is irrelevant to it;
the requirement was a convenience for cross-structure interpretation, not a validity condition, and it cost more than
half the pool while leaving LAD at 5. Dropping it restores the pool to **77** (RCA 36, LCx 25, LAD 16).

**Frozen 3D subset: `CFD-SUBSET-FROZEN-2026-09-18.csv`** (hashed in `COHORT-FROZEN-2026-09-18.sha256`) —
**30 instances, 10 per vessel, one per tree** (30 trees, 29 patients), stratified across the **discrete** bands
(0.65–0.70: 5 · 0.70–0.75: 4 · 0.75–0.80: 4 · 0.80–0.85: 7 · 0.85–0.90: 5 · 0.90–0.95: 5), severities 40–80 %DS,
lengths 10 mm × 20 / 20 mm × 10. One instance per tree removes the clustering that would otherwise complicate the
κ estimate. Instances whose discrete FFR falls outside 0.65–0.95 (12 of the pool) were not selected.
Selection is recorded as an explicit hashed instance list, never as "seed 20260918" — `select()` is chaotic: a
16-band perturbation in the sweep produced a cohort sharing only 62/150 instances with the original.

## 4. Runs per instance
Geometries: baseline (lesion, correct anatomy) + 4 error types = **5 surfaces × 2 tiers = 10 meshes**.
Solves per tier: baseline (1) + per error type {A: 1, B: 1, C: 2 — flow-prescribed solve, then resistance solve} =
1 + 4 × 4 = 17, plus resting-state solves for the Fossan constraint on C (+4) = **21 per tier, 42 per instance.**
| | meshes | steady solves | core-hours (≈ 20 min × 8 cores) | wall-clock, 16 cores |
|---|---|---|---|---|
| Stage B polyball, 30 instances | 150 | ~630 | ~1,700 | ~4.4 days |
| Stage C real lumen, 30 instances | 150 | ~630 | ~1,700 | ~4.4 days |
| Stage D pulsatile figure, 6 runs (24 h × 8 cores) | — | — | ~1,150 | ~3 days |
| **Total** | **~300** | **~1,260** | **~4,550** | **~12 days, unattended** |
Run **two 8-core jobs side by side** (~60 k cells/core at 1 M cells) rather than one 16-core job. All figures are
estimates from Mao 2025's published timings; **Gate M1 replaces them with measured numbers.**
> **MEASURED 2026-09-26 (Gate M1, scan 14, `STAGE-A-VALIDATION (3).pdf` §11.8): the table above is about 13× too
> optimistic for the real tier.** A production real-lumen steady solve is 3.5–3.9 M cells (25 µm throat zone, the
> recipe fixed by WO 09-26 D1) and takes ≈ 2.1–2.3 h on 16 ranks with ≈ 6 GB, on a fixed 3000-iteration budget. Geometry
> and meshing add ≈ 10 min. The re-cut real tier (≈ 400 solves) is therefore ≈ 40 machine-days sequential. Re-size after
> WO 09-26 Task B (settle-iteration stopping, 2×8 vs 1×16 layout, multi-PC portability).

## 5. Stages
- **Stage A — setup verification (§8).** Poiseuille pipe, idealised stenosis, resistance BC, mesh independence.
- **Stage B — polyball tier.** Fully scripted. Delivers the working pipeline and the physics-only control.
- **Stage C — real-lumen tier.** Reuses Stage B end to end; only surface generation differs (§6.1b).
- **Stage D — mechanism figure.** 3 instances × 2 (baseline; topological error under Protocol C), pulsatile, real lumen.
Gate M1 (§7) runs **alongside Stage A**, not after it.

## 6. Pipeline (per geometry)
### 6.1a Polyball surface
`vmtkcenterlinemodeller` on the package's centreline + radius. **Sampling must resolve the throat:** spacing ≤ r_throat/8
(an 80 %DS lesion on a 1.2 mm host has r_throat ≈ 0.24 mm → ≤ 0.03 mm locally; v0.1's 0.1 mm could not resolve it) —
use a locally refined image or build the lesion region separately. `vmtkmarchingcubes`; Taubin smoothing; **assert the
as-built throat radius is within 1 % of target.**
### 6.1b Real-lumen surface
From the ImageCAS-X mask, not the shipped `.vtk` surface (so edits and the 0D twin share one source):
- baseline lesion, stenosis-length, taper → **radial deformation of surface vertices** toward/away from the centreline by
  the same cosine law as the 0D insertion (SEVERITY-SWEEP-SPEC §4);
- missed branch, truncation → **delete the branch's voxels in the mask and re-run marching cubes** (no clip-cap-repair);
- then **re-measure the as-meshed radius along the centreline and send it back** — the analysis side rebuilds the 0D twin
  from the geometry that was actually meshed, so 0D-vs-3D-real compares like with like.
Mask-derived surfaces do not have FAME's failure mode (its 14.8 % self-intersections came from sweeping a section along
a centreline); expect instead staircase artefacts (smooth, volume-preserving) and thin-vessel pinch-off below ~2 voxels.
### 6.2 Extensions, mesh, solve, sample — identical for both tiers
- `vmtkflowextensions`: 5 diameters at the inlet, 3 at each outlet; planar caps; patches `inlet`, `outlet_<id>`, `wall`.
- cfMesh `cartesianMesh` (or snappyHexMesh): base ≈ D_local/20; lesion ± 2 lengths refined so the throat has ≥ 12 cells
  across at 80 %DS; 4 boundary layers, growth 1.2; `checkMesh`: non-orthogonality < 70°, skewness < 4, no negative volumes.
- `simpleFoam`, laminar, Newtonian ν = 3.774e-6 m² s⁻¹, rigid no-slip wall. Inlet `totalPressure` = P_aorta/ρ.
- **Outlets, two modes (both needed):** (i) *resistance* p_i = P_v + R_i Q_i as `codedFixedValue` on the patch flux,
  under-relaxation 0.2–0.3 — used for baseline, A, B and the second C solve; (ii) *prescribed flow* — used for the first C
  solve, which is what makes in-fidelity tuning one extra solve.
- Convergence: residuals < 1e-5 **and** inlet flow, each outlet flow and measurement-point pressure stable to < 0.1 % over
  200 iterations; global mass imbalance < 0.1 %.
- Sample **area-averaged** pressure on a cross-section at each probe. FFR = p̄/P_aorta.
- **Laminar is the assumption a reviewer will attack.** Record throat Reynolds number for every solve (expected ~400–450
  at 80 %DS; the 0.70–0.90 instance window keeps most cases to a few hundred). Any case above ~1000 is flagged and
  reported separately — never silently switched to a turbulence model. Steady, rigid-wall and Newtonian are standard for
  FFR and dismissed with citations.

## 7. Gate M1 — real-lumen pilot (day one, in parallel with Stage A)
Three instances through §6.1b → §6.2: a clean baseline, an **80 %DS** lesion by vertex deformation, a **missed branch** by
mask edit. **Pass:** `checkMesh`-clean mesh and converged solve with **no manual geometry repair**; as-meshed radius
returned; resistance and prescribed-flow BCs both stable; wall-clock recorded. **Kill:** 5 working days of effort without a
scriptable path → §9 fallback.

## 8. Stage A — verification of the CFD setup
| Test | Pass |
|---|---|
| Straight pipe | pressure drop within 1 % of Poiseuille |
| Idealised cosine stenosis 0 / 50 / 70 / 80 %DS (`cfd_handover/stageA/`) | tabulated against the **0D-DISCRETE** values in `expected_0D.csv`: FFR 0.983 / 0.946 / 0.754 / 0.485 at the measurement plane (x = 56.5 mm), flows 1.50 / 1.44 / 1.13 / 0.69 mL/s. (0.919 / 0.693 / 0.427 are the *leaky* self-test numbers from `zerod_ffr.py`'s ideal vessel — a different model and a different geometry; do not compare 3D against those.) The gap is a *result* about the lumped stenosis model, not a failure |
| Resistance BC | p_outlet = P_v + R·Q to 0.1 % at convergence |
| Prescribed-flow → resistance round trip | re-solving with the derived R_i reproduces the prescribed flows to 0.5 % |
| Mesh independence, 2 instances × 3 levels | ΔFFR at the measurement point < 0.005 between the two finest |

## 9. Fallback (pre-agreed; invoked by the M1 kill, not by discussion)
**20 real-lumen instances × the two topological error types only** (missed branch, truncation — both are mask edits and
need no vertex deformation), plus the full polyball tier. **Never polyball-only**: that arm would restate Grande 2021.

## 10. Analysis-side work this spec creates (analysis machine)
- [x] **DONE 2026-09-18.** `bed="discrete"` mode in `zerod_ffr.py` (leaf r_ref^2.66, truncation r_ref < 0.60 mm,
      calibration and zero-outlet guards, `healthy_main_ffr()` gate). Verification suite passes on both beds and both
      disjoint scan sets: V3b clean, V8a 0.0012–0.0030, V10 = 0.0000, tolerance kept at 0.005.
- [x] **DONE 2026-09-19 for the decision disagreement: the "29/150" claim is NOT reproducible and is withdrawn.**
      Its denominator does not exist — **53 of the 150 instances have no discrete FFR at all** (48 fail the
      healthy-network gate, 5 have fewer than 2 outlets), so there is nothing to disagree about on those. The
      protocol-grade figure is **19 of 97 discrete-eligible instances**, which is what `STATISTICS-PLAN` §P3 and §3
      of this document already say. The reviewer's probe evidently used a looser eligibility rule.
- [x] **DONE 2026-09-19: the 0.75 vs 1.00 mm survival counts** — reproduced on all 108 cohort trees, twice, by two
      code paths. §2.4 carries the table. The 0.60 mm choice stands.
- [ ] Still to reproduce protocol-grade: the branch
      re-insertion effect under A/B/C, the 0.75 vs 1.0 mm survival counts. **The eligible-instance count is done**
      (`discrete_arm.py` → 97/150, superseding the reviewer's 42).
- [x] **DONE.** Per-protocol rule for the orphaned bed weight when a branch is deleted (A: clean weights on surviving
      nodes, deleted demand simply lost · B: recomputed from the corrupted geometry · C: flow-matched) —
      `ablation.py:145–155`.
- [x] **DONE.** Flow-matched Protocol C in 0D: ONE global bed scaling against ≥ 2 territory targets, over-determined
      by construction (`ablation.py:156–186`). Fossan constraints partially — resting-state re-simulation with
      autoregulation is **not** implemented and is a declared limitation (this model has no autoregulation).
- [x] **DONE 2026-09-19.** Protocol C minimiser hardened: the loss is **bimodal in log C** and
      `minimize_scalar(bounded)` was returning the wrong basin (scan 341/RCA/leaky/T1: C_ratio 0.077, ΔFFR −0.52,
      recorded as "passes its check and is materially wrong" when the true optimum is C_ratio 1.00, ΔFFR ≈ 0).
      Now a 61-point global log-grid scan → Brent refinement, with `fit_n_basins`, `fit_loss_at_Cstart`,
      `fit_loss`, `fit_at_bound` recorded and a bound hit treated as a **failed fit**.
      Verified on scan 341: `fit_n_basins = 2`, returns C_ratio 0.994, residual 3.3e-5.
      **Smoke re-run done (6 instances × 2 beds, 2026-09-19): 0 of 38 Protocol C rows changed, 0 multi-basin fits,
      0 bound hits.** The smoke set does not contain the pathology — i.e. *the smoke test would not have caught this
      bug*, which is the argument for recording the fit diagnostics on every row of the full run rather than trusting
      a subset. The one extreme value in the pre-fix smoke (scan 335 / discrete / T2, C_ratio 10.1) was checked and is
      **genuine**: unimodal, unchanged by the fix, and it fails the 10 % validation check anyway (residual 0.62), so
      it never enters the positive class. An earlier note here called it "the same pathology"; that was the reviewer's
      suspicion and it is now falsified. Runtime with the 61-point grid: 28 s for 6 instances × 2 beds → ≈ 12 min for
      the full 150.
- [x] **DONE 2026-09-19.** `export_cfd_case.py` — packages per §11, v0.2 after independent review
      (`references/FABLE-REVIEW-EXPORTER-2026-09-19.md`, GO-WITH-CHANGES, MUST 1–8 applied).
- [ ] `ingest_cfd_radius.py` — rebuild the 0D twin from as-meshed radii.
- [ ] **0D twin must run the per-outlet Protocol C procedure** for the ladder comparison (§2.2 is exactly determined
      per outlet; the 0D primary is one global scalar against territory totals — different fits, see §11 `meta.json`).

## 11. Case package (one folder per geometry; BC sets inside)
```
<instance>__<errortype>__<tier>/
  README.md           frame, units, build steps, what to return — so the operator never opens this spec to run a case
  centreline.vtp      mm, LPS; MaximumInscribedSphereRadius (= AS-EDITED radius), r_target_mm, r_source_mm,
                      radial_scale, r_ref_mm, r_fit_mm, segment_name, branch_id, tree_node, resolved
  mask_edit.json      surface_rule + truncation_rule + sub_cut_points_mm; lesion table; for T1/T2 the deletion
                      rule with its deleted/retained point lists and a reference implementation
  outlets.csv         outlet_id, tree_node, x,y,z, normal, r_ref_mm, r_mm, territory_id
  bc_A.csv, bc_B.csv  outlet_id, mode (resistance|closed), R_SI, R_kinematic      (imposed)
  bc_C_flows.csv      outlet_id, mode (prescribed|closed), territory_id, Q_target  (first C solve; R_i derived on
                      the CFD side)
  territories.csv     territory_id, root node, Q_clean_surviving_mls, Q_clean_full_territory_mls, n_outlets
  inlet.json          frame; P_aorta 11999 Pa, P_venous 667 Pa, rho 1060, mu 0.004; inlet position/normal/radius
  probes.csv          inlet; the DETECTOR-SPEC §8 station list (5 mm grid + lesion shoulders, throat, measurement,
                      and stations >= 1 diameter either side of each bifurcation); every outlet
  meta.json           frame, lesion, error type + magnitude, source instance, measurement node, Protocol C variant
                      statement, provenance hashes (centreline vtk, mask, exporter), blinding note
```

**Frame, stated in every file that carries coordinates:** mm, LPS. The ImageCAS-X NIfTI affine is **RAS** — negate
x and y before applying `inv(affine)`. Verified: with the flip 42/42 of a probe's deletion points land inside the
lumen; without it, 0/42.

**`mode = closed` means a wall** (zero conductance), which is what the 0D model does with `w = 0` for an outlet that
has no counterpart in the clean tree — in practice the T2 stump. (It formerly also arose for "T4 new leaves"; since
decision B3 pins the modelled node set for calibre-only errors, T4 creates no new leaves.) It is written explicitly
because the earlier exporter wrote an empty cell there, which a solver would read as a missing boundary condition.

**Both clean territory totals are shipped for audit. DECISION B1 IS SETTLED (2026-09-19): the study targets
`Q_clean_full_territory_mls`** — the clean tree's full outflow including any branch the error deleted, partitioned by
the **clean** tree's territories. `Q_clean_surviving_mls` is retained only so the difference is visible and
checkable: on the Gate M1 instance the two are 0.078 vs 0.173 mL/s, i.e. the deleted branch was **55 % of that
territory's perfusion**.

> **Outstanding for the STUDY BATCH (not for M1): two exporter defects.** (1) The per-outlet split currently uses
> each outlet's own *clean* flow, which is **undefined for a T2 stump** — its clean counterpart is an interior node
> with zero bed weight, so the stump is written as a wall in 3D while the 0D twin gives it a live outlet; on the ten
> RCA subset instances the stump is the only outlet, so every outlet would be `closed` and there would be no case.
> Split by the **corrupted tree's Murray weights** instead, which is what one global scaling does in 0D.
> (2) The exporter still partitions by the *corrupted* tree, so on instances where the 0D twin has no Protocol C cell
> it would still write one — **4 of these are in the frozen 3D subset (scans 196, 272, 341, 928)**. Switch it to
> `ablation.protocol_c_targets`, or refuse to write `bc_C_flows.csv` when the twin has fewer than 2 territories.
Packages are kilobytes — fine through Drive. **Meshes and fields stay on the CFD machine; never to Drive.**
`expected_0D.json` is **withheld** until results are returned (§13).

## 12. What comes back
`cfd_results_<batch>.csv`: case id, tier, error type, protocol, n_cells, checkMesh status, iterations, residuals, mass
imbalance, inlet flow, per-outlet flow and pressure, area-averaged pressure at every probe, **derived R_i for Protocol C**,
throat Re, wall-clock, cores, OpenFOAM version. `as_meshed_radius_<case>.csv` (real tier). `cfd_failures.csv` with the
failure stage — **mesh/solve failure rate by error type is a reportable finding** (none is published).

## 13. Blinding
The CFD operator does not need the 0D predictions to run a case. They are withheld for the study batch and released
after the results CSV is returned, so the 3D numbers are produced blind to what they test.

## 14. Analysis
- **Primary endpoint:** error-induced ΔFFR = FFR(corrupted) − FFR(clean) **within each fidelity**, compared 0D vs
  3D-polyball vs 3D-real per error type × protocol (Bland–Altman; slope and bias).
- **The thesis panel (3D):** outlet-flow residual against lesion-FFR error under A / B / C — absorption is visible as
  C driving the flow residual to ~0 while the FFR error persists.
- **Secondary:** decision flips, each judged against its own fidelity's clean baseline; concordance κ (H4: κ > 0.6).
- **Ladder decomposition:** |0D − polyball| = physics gap; |polyball − real| = geometric-reduction gap. Report both.

## 15. What the paper may and may not claim from this arm
**May:** the error-induced FFR change and the absorption pattern under flow-matched tuning replicate at 3D fidelity on
real lumens, for these error types, in steady hyperaemic flow. **Must not:** claim 3D is ground truth; claim anything
about pulsatile FFR, WSS or OSI; claim validation of the leaky model (the replication is discrete-outlet); generalise
beyond the 0.70–0.90 baseline window the instances were drawn from.

## 16. Residual risks
Real-lumen surface editing cannot be automated (→ §9) · throat resolution drives mesh size up at 80 %DS · coupled
resistance BC unstable on multi-outlet trees (→ lower relaxation; prescribed-flow mode is the fallback for A/B too, reported
as such) · fewer than 30 eligible instances · laminar assumption challenged at the highest severities (→ Re reporting).

## 17. Open items
- [ ] CFD machine: OpenFOAM version, VMTK and cfMesh installed; RAM (≥ 2 GB per million cells per job).
- [ ] Mao 2025 `CoronaryHemodynamics` licence — unstated in the paper; not required by this spec.
- [ ] §10 analysis-side work, then freeze this document with WP-0.
- [x] **DONE — decision B2, 2026-09-19.** `T2_KEEP_BEYOND` raised **15 mm → 25 mm** (= `RUNOFF` + 5 mm), so the
      measurement node is interior with a margin instead of being deleted by the truncation it is supposed to survive.
      Verified: `meas_same_point` 0/36 → **36/36** T2 smoke rows. `ablation.py` now **asserts
      `T2_KEEP_BEYOND > RUNOFF` at import**, because the two constants live in different modules and nothing
      connected them. Every pre-fix T2 number under Protocol A was reading a wall.
- [x] **DONE — decision B1, 2026-09-19.** Protocol C targets the clean tree's **FULL** territory outflow, including
      the deleted branch's share (`STATISTICS-PLAN` §P2 as written). Verified: T1 `C_ratio` 1.049 → **0.928**.
      **The 3D consequence is in the packages:** per-outlet prescribed flows now distribute the full territory total
      across surviving outlets in proportion to their own clean flow, so on the Gate M1 T1 case the surviving outlet
      is prescribed **0.173 mL/s instead of 0.078** — it must carry the missing branch's perfusion.
- [x] **DONE — decision B3, 2026-09-19.** The truncation radius now scales with T4's calibre error (0.60 → 0.558 mm
      discrete, 0.50 → 0.465 leaky). A fixed cut was deleting leaves the error had merely narrowed. Verified:
      T4 × Protocol A discrete **+0.173 (3 flips) → −0.032 (0 flips)**, now agreeing in direction with the leaky bed.
- [ ] §13 blinding needs one sentence of precision: `bc_A × bc_C_flows` reconstructs the **clean** outlet pressures
      exactly, so what is blind is the **corrupted-geometry** prediction and ΔFFR, not every 0D quantity.
- [x] **DONE 2026-09-19.** Real-tier lesion window: subdivision to edge length ≤ r_throat/8 before deformation, and
      the as-built throat check — now steps 4–5 of every package's own `README.md`. (~13× refinement at 80 %DS on a
      0.32 mm voxel; without it the deformation cannot represent the throat at all.)
- [x] **DONE 2026-09-19.** Two errors in `bc/resistanceOutlet.md` that would have cost the CFD operator days:
      the under-relaxation is a **stability bound** `α < 2/(1 + R_out/R_epi)` (≈ 0.134 on `sten00`, ≈ 0.10 on real
      lumens), so the template's 0.2 **diverges** — default now 0.05, and **A3 runs `sten00` first** because the
      *mildest* case is the hardest for this BC; and "prescribe all but one outlet" was **wrong** — with a
      `totalPressure` inlet every outlet is prescribed, and leaving one free would let it absorb the entire
      discrepancy, invalidating flow-matched Protocol C on every multi-outlet case.
- [x] **DONE 2026-09-19.** Inlet normal: both call sites passed the host vessel's first node instead of the tree
      root, putting the shipped inlet normal **37° off** the ostium in every package. Fixed and re-exported.
- [ ] **Re-cut the study batch before launching it** (pre-flight 2026-09-19, §3.4 of that report): only 407 of 510
      solves per tier have a 0D counterpart; T2 has no A or C cell on any RCA; T1 × C missing on 7/30; T4 discrete is
      the B3 artefact; drop the 240 resting-state solves (this model declares the Fossan resting-state constraint
      unimplemented); run the **real tier before polyball** (polyball on a 10-instance subset). ≈ 5–6 machine-days.
- [ ] **Pre-agree the Re > 300 non-convergence fallback** (pimpleFoam + time-average, reported separately, never a
      silent turbulence-model switch): **17/30 baselines exceed Re 300 and 10/30 exceed 400**. Stage A `sten70`/`sten80`
      are the test of whether steady laminar holds.
- [ ] **Write and validate the station plane-clipping script on Stage A**, where the cut area is exactly πr², and add
      `station_area_ratio` (cut area ÷ πr²_local) to the return template as the QA column.
- [ ] **Stage D** — unspecified, 3 machine-days, and its mechanism figure is already produced by the steady solves.
      Re-specify as a steady-vs-cycle-mean check, or cut.
