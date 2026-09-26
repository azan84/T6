# Adversarial methods review — 3D CFD arm, decisions §2.1 and §2.2

**Reviewer:** Fable 5.1 (adversarial pre-registration review; not a peer review)
**Date:** 2026-09-18
**Under review:** `protocol/CFD-ARM-SPEC.md` v0.1, §2.1 (polyball surfaces) and §2.2 (discrete-outlet replication).
**Read:** CFD-ARM-SPEC, STUDY-PLAN-v2, E0-PREVALENCE-NOTE, SEVERITY-SWEEP-SPEC, `code/zerod_ffr.py`,
`code/severity_sweep.py`, deep notes Gosling 2020, Fossan 2025, Mao 2025, Marcinnò 2026 (FAME), Grande 2021, Gamage 2022.
**Evidence added by this review:** two 0D probes on the 150 selected sweep instances, run with the project's own
solver. Scripts and CSVs: `references/FABLE-REVIEW-CFD-2026-09-18-probe/`. They are **reviewer's probes, not
protocol-grade** (no V-suite, one global tuning scalar, largest downstream branch only). Numbers from them are marked
**[probe]**. Claims resting on literature outside the corpus are marked **UNVERIFIED**.

**Bottom line.** Both decisions are wrong as written. §2.2's 1.0 mm cut is *fatal on this cohort* and needs no
argument, only arithmetic. §2.1 answers half of the reviewer's objection and the less relevant half. And the rule that
sits above both — "3D verifies, never tunes" — means the arm, as specified, does not test the paper's thesis at all.
All three are cheap to fix **now**, because nothing in Phase 1 is frozen.

---

## 0. Four facts the spec did not have  [probe]

| # | Finding | Number |
|---|---|---|
| F1 | **The measurement node is outside the 3D domain.** Hosts need r_fit ≥ 1.0 mm *at the lesion*; the measurement node 20 mm distal needs only ≥ 0.75 mm. Truncating where r < 1.0 mm removes it | retained in **82/150**; r_ref at the measurement node: median **1.02 mm**, IQR 0.93–1.19. Run-off distal to the lesion < 20 mm in 66/150 |
| F2 | **The 1.0 mm cut deletes the side branches T1 needs.** Side branches off the host path, by origin r_ref | ≥ 1.0 mm: **41** · 0.75–1.0: **137** · < 0.75: 67. **112/150 instances have no side branch ≥ 1.0 mm at all**; 122/150 have none downstream of the lesion's proximal edge. Domain outlets at 1.0 mm: median **2**, **49/150 have exactly one** (A/B/C degenerate). At 0.75 mm: all 150 measurement nodes retained, median 4 outlets, 24 single-outlet |
| F3 | **Leaky and discrete are not two dialects of one model.** In the leaky model only a small part of the bed is at leaf outlets; the rest is wall leak | leaf share of total bed weight: median **14 %** (IQR 10–21 %). Same instances, same demand, discrete (0.75 mm) vs leaky: ΔFFR mean **−0.077**, SD 0.084, range −0.35…+0.07; FFR ≤ 0.80 decision **disagrees in 29/150 (19 %)**; r = 0.78. Instances in 0.70–0.90: leaky 100, discrete 73, **both 57** |
| F4 | **The thesis's effect size depends on BC structure, and the leaky model partly self-heals a missed branch.** Largest downstream side branch ≥ 0.75 mm deleted (82 instances; branch/host radius ratio median 0.70) | mean \|ΔFFR\| at the measurement node, A / B / C — **leaky 0.059 / 0.017 / 0.036; discrete 0.112 / 0.051 / 0.120**. Flips A / B / C — leaky 24 / 5 / 15, discrete 32 / 9 / 36 (of 82). Correlation of the error-induced ΔFFR between the two structures: 0.68 (A), 0.48 (B), **0.20 (C)** |

F4's mechanism is in the code, not an accident: `g(v) = max(r_ref(v)³ − Σ children r_ref³, 0)/C`. Delete a child and the
parent node's leak grows by exactly the child's Murray weight — the model re-inserts the missing branch as a point leak.
That is what Gosling built it for: *"the flow Qin is varied along the centreline to account for flow to branches which
are not explicitly represented."* A model designed to be insensitive to unrepresented branches is a strange primary
instrument for a paper about unrepresented branches — and no deployed pipeline in the corpus uses it (Fossan 2025 Eq. 2–3:
per-outlet resistances; Mao 2025 Eq. 7: Murray on outlet cap areas; Grande 2021: nine outlets; Gamage 2022: a
resistance at every outlet). Gosling's leak lives on a *single-lumen angiographic* vessel with no branches to lose.

A further point surfaced by the probe, stated once because it governs what 3D must tune: **in a steady resistive tree
you cannot match both pressure and flow at outlets distal to the lesion and still get the lesion FFR wrong** — the
measurement point lies on the path between the lesion and those outlets. With a downstream branch missing, a tuner can
match the surviving outlets' *flows* (then distal pressures rise — probe: max outlet-pressure error under C, median
**0.115** FFR units, discrete) or their *pressures* (then flows are wrong), never both. STUDY-PLAN §E2's "reproduces the
clean baseline's outlet flows **and** pressures … residual ≈ 0 by construction" is not achievable for T1/T2 downstream
loss, and with one global scalar C collapses onto A (probe: discrete C ≈ A, 0.120 vs 0.112). The defensible Protocol C
is **flow-matched**, which is also the realistic one: no FFR-CT pipeline has non-invasive outlet pressures to match;
Fossan's own step 2 *prescribes outlet flows* and derives R = (P − Pv)/Q. Freeze that before anything else.

---

## 1. Verdict on §2.1 (polyball surfaces) — **MODIFY: demote polyball to the control rung; make real-lumen surfaces the primary replication**

**What is sound** (one line): polyball is watertight, scriptable, and cleanly isolates the *physics* closure
(Poiseuille + fixed-K_t expansion loss vs Navier–Stokes with curvature, bifurcation and recovery losses); agreement is
not literally guaranteed — the spec itself expects drift at high %DS.

**Why it still fails as the primary (attack A — damaging, not fatal):**

1. *It answers the wrong half of the objection.* "A 0D model is not ground truth" has two parts: (a) reduced physics,
   (b) reduced geometry — a lumen collapsed to a centreline and an inscribed-sphere radius. Polyball tests (a) only. In
   a paper whose subject is **segmentation** error, (b) is the half a TMI/MedIA reviewer cares about. "The 3D geometry
   is the 0D geometry, exactly" will be quoted back as the defect.
2. *What (a) alone shows is already in print.* Grande 2021: *"FFR3D = 0.76, FFR1D–3D = 0.78"*, *"differences below 3 %
   across the models"*; Blanco 2018 sits in Grande's references as a 1D-vs-3D FFR comparison. A polyball-only arm
   replicates that, not C2.
3. *The shared-radius bias is invisible by construction.* E0 records a centreline ~1 voxel off-axis that *"under-reads
   radius by ~10–15 %"*. Both 0D and polyball inherit it; they will agree with each other and both be ~50–90 % high in
   r⁻⁴ resistance (1/0.9⁴ = 1.52, 1/0.85⁴ = 1.92) relative to the real lumen. Five real-surface cases will expose this in the paper's own figure. Fix
   the centring (VMTK centrelines on the real surface, true MISR) or quantify it before any 3D run.
4. *The FAME citation argues the other way.* FAME's 14.8 % (RCA 26.6 %) is self-intersection from *sweeping a circular
   section along a 2-view ICA centreline* — *"primarily in regions where the vessel radius is large relative to the
   local radius of curvature."* That is the failure mode of centreline-plus-radius surface generation, i.e. of §2.1, not
   of CT-mask surfaces. An implicit union cannot self-intersect, but it will **fuse** adjacent vessels and blob the
   carina instead — silently. ImageCAS-X surfaces come from voxel masks and carry no such risk.
5. *The "no repair step exists" premise is overstated.* T1/T2 can be done as **mask edits** — delete the branch's
   voxels, re-run marching cubes. Watertight by construction, no clipping or capping, and it is *literally the error
   the paper is about*. The synthetic lesion, T3 and T4 are **radial deformations** of surface vertices toward the
   centreline with the same cosine weight as SEVERITY-SWEEP §4 — topology untouched, cross-section shape preserved.
   (Lesions cannot be mask edits: 80 %DS on the median 1.22 mm host is a 0.24 mm throat radius, below one voxel.)
6. *Throat resolution in the spec is off by ~5×.* Polyball "image spacing ≤ 0.1 mm" against a 0.24–0.43 mm throat
   radius, with a pass criterion of "< 1 %" (2–4 µm). A 0.02 mm throat error at 70 %DS is ~5 % in r, ~20 % in the
   loss, ~0.03–0.05 FFR — the size of the effect under study. Whatever surface is used, **re-measure the as-meshed
   radius profile and feed it back to a 0D twin** ("0D-as-meshed"); otherwise 0D–3D disagreement is meshing noise.
7. *If D1b lands, polyball cannot serve the paper's strongest arm.* Two annotators' masks are not a common centreline
   edit. The mask → surface path has to exist anyway.

**Is 5 enough?** No. Five cases give no κ (any CI spans the scale); it is an illustration. **Required: ~30 real-lumen
instances on ≥ 25 trees, 10 per vessel, near-threshold, both topological error types present** — see §4.

**The modification.** A three-rung ladder on the *same* instances: **0D → 3D-polyball → 3D-real-lumen**. Rung 1→2
isolates physics; rung 2→3 isolates geometric reduction. The headline replication is 0D vs real-lumen; polyball is the
control that *explains* any disagreement. Polyball keeps every benefit claimed for it, in the role it can defend.

## 2. Verdict on §2.2 (discrete-outlet replication) — **REJECT as written; MODIFY to: 0.75 mm truncation, BC structure as a pre-registered factor of the primary 0D experiment, tuning done in 3D**

**The 1.0 mm cut is fatal (F1, F2) — attack E.** 45 % of measurement nodes fall outside the domain; 75 % of instances
have no side branch left to miss; a third have one outlet. Fossan 2025 segments *"down to a vessel radius of 1 mm"*, so
the number has a precedent — in a cohort with normal-calibre vessels. Here the median host is 1.22 mm at the lesion. By
Gamage's own rule (*"negligible (< 4 %) if the side branch diameter is less than one third of the main vessel
diameter"*) the branches a 1.0 mm cut removes — ratio ~0.6–0.8 of the host — are far above the negligible line; and
Gosling's discussion cites Sturdy 2019 as finding significant vFFR change from neglecting < 1 mm branches (second-hand
via the Gosling note). **Truncate at r_ref < 0.75 mm = `R_RESOLVED`**, the radius the protocol already declares
resolved; require a retained stub ≥ 3 diameters or drop the branch in *both* fidelities.

**"You validated a model you did not use" (attack B) — damaging, and the spec's bridge does not answer it.** The
proposed bridge is "0D-leaky vs 0D-discrete". On absolute FFR that bridge *fails*: 19 % decision disagreement, mean
shift −0.077 (F3). On the thesis's own quantity it fails harder: the error-induced ΔFFR under Protocol C correlates at
0.20 between the two structures (F4). A reviewer handed those numbers concludes the 3D arm validated a different
experiment. Options:

| Option | Paper strength | Against E0 ("leak-free was unphysiological") | Verdict |
|---|---|---|---|
| (i) leaky primary + bridge | Headline stays on the model no deployed pipeline uses and that self-heals T1 under B; 3D never touches it | consistent | **Insufficient** |
| (ii) discrete everywhere | Matches deployed practice; 3D-verifiable end to end | E0's failure was on untruncated 0.3 mm tips before two bug fixes. **[probe]** at 0.75 mm: no-lesion FFR at the measurement node median **0.968**, < 0.90 in 4/150 — physiological where FFR is read. Caveats: hosts were selected under leaky (selection bias — rerun on all 280); leaf r³ is 14 % of inlet r³, so tip flows are ~7× Murray-local and near-tip pressures are not trustworthy | Viable, but discards a real finding |
| (iii) leakage in 3D | A mass sink in `simpleFoam` means a source in the pressure equation, not an `fvOptions` one-liner; unvalidated BC inside the validation arm | — | **Rejection upheld** |
| **(iv) BC structure as a designed factor** | The 0D ablation is minutes of compute. Run **error type × protocol × BC structure {discrete, leaky}** on the full cohort, pre-registered. Headline claims must hold in **both**; the *difference* is reported as a result — F4 already suggests "a side-branch-aware BC structure halves the hazard and nearly removes it under re-derivation", which is a gift to C3's remedy narrative. 3D then verifies a model the paper **does** use | consistent: leaky stays, as the physiological arm | **Recommended** |

Under (iv) the bridge to leaky is made with 3D evidence at zero extra CFD cost: extract per-segment ΔP(Q) from the 3D
runs (each geometry is solved at several operating points), fit ΔP = aQ + bQ² for the lesion segment, substitute it for
the 0D element inside the **leaky** network, and re-run A/B/C on those instances — "leaky with 3D-calibrated losses".
Precedent in corpus: Fossan's solver refines 0D/1D segment drops *"using a neural network trained to capture complex
three-dimensional (3-D) fluid dynamics."* For T1/T2 the lesion geometry is unchanged between clean and corrupted; the
error acts only through the flow delivered to it — so the component 3D *can* speak to is exactly this law.

Cohort consequence: membership was defined under leaky. Keep it, report bands under discrete too, and draw the 3D
subset from instances in 0.70–0.90 under **both** (57) with ≥ 1 side branch ≥ 0.75 mm on the host path: **42 instances,
35 trees, LAD 15 / LCx 13 / RCA 14 [probe]** — enough for a balanced 30.

## 3. The attack that matters most — "3D verifies, never tunes" means the arm does not test the thesis

The thesis is *matched at the outlet, wrong in the tree*. The spec tunes in 0D and imposes the parameters on 3D. Then:
the corrupted-3D model's outlets are **not** matched to the clean-3D model's outlets (they differ by the 0D–3D
discrepancy evaluated at two different flow states); no 3D outlet residual is even computed (§11 lists κ, Bland–Altman
and the A/B/C contrast — no residual); and what is demonstrated is that two solvers given identical boundary conditions
return similar pressure drops. Add §2.1 and the arm reduces to "Poiseuille + K_t ≈ Navier–Stokes in a near-axisymmetric
tube" — Grande 2021's result, not C2's *"replicated at 3D fidelity"*. A reviewer writes: *"In 3D the outlets were
never matched, so the concealment was never shown in 3D; a validator with the 3D model would have seen a residual."*
That sentence sinks H4 as evidence for the thesis. **Severity: fatal to the claim, not to the arm.**

**The premise behind the rule is wrong for this arm.** "~15 full solves per condition, infeasible" is a pulsatile
Windkessel number. E3a is steady, and with flow-matched targets (§0) **tuning in 3D costs one solve**: impose the
clean-3D model's outlet flows on the corrupted 3D geometry (`flowRateInletVelocity`, negative — already the spec's
§5 "fallback"), read outlet pressures, set R_i = (p_i − P_v)/Q_i. That *is* Fossan's step 2–3 (*"resting-state
simulation with prescribed inlet pressure and prescribed outlet flows … to find P_out"*; Eq. 2). The Fossan-faithful
variant — tune at rest, divide by k, solve hyperaemia — is **two** solves. A one-global-scalar variant is a 0D-seeded
secant, 2–3 warm-started solves. The transferred-parameter run is kept as a *reported diagnostic* (how large is the 3D
outlet residual if you transfer?), not as Protocol C.

**Cheapest neutralising change:** Protocol C in 3D = prescribe clean-3D outlet flows on the corrupted 3D geometry;
report, per fidelity, the outlet-flow residual (→ 0), the outlet-*pressure* residual (what a validator does not have)
and the lesion FFR error. Net cost: +1 solve per C condition.

## 4. Recommended revised design for the 3D arm

**Instances.** 30, from the 42-instance pool above; 10 per vessel; ≥ 25 trees; baseline FFR 0.70–0.90 under both BC
structures (mostly 60–70 %DS — throat Re stays in the low hundreds, see attack D); each with ≥ 1 side branch ≥ 0.75 mm,
stratified upstream / downstream *on the whole tree* (SEVERITY-SWEEP §8d item 2). Over-sample to 40 for attrition.

**Geometries — two tiers on the same instances.**
- **Tier R (primary):** ImageCAS-X mask → T1/T2 as mask edits → marching cubes + volume-preserving smoothing →
  lesion, T3, T4 as radial vertex deformation → clip at r_ref < 0.75 mm → flow extensions. 5 surfaces per instance.
- **Tier P (control):** polyball from the same centreline + radius, per-branch modelling with throat sampling ≤ 0.02 mm.
- Both tiers: re-extract centreline + MISR **and** area-equivalent radius from the final surface → "0D-as-meshed" twin.

**BC structure.** Discrete outlets, Murray R_i = C′/r_ref³, C′ calibrated to the same Murray demand, both fidelities.
0D twin includes the flow extensions, or FFR_3D is referenced to the ostial plane (5 D of inlet extension at 1.5 mL/s is
~0.4 mmHg ≈ 0.005 FFR — the 0D noise floor; not negligible).

**What is tuned where.** A: clean R_i, imposed (1 solve). B: R_i from the geometric deployment rule on the corrupted
tree, imposed (1 solve). **C: tuned in each fidelity against that fidelity's own clean baseline**, flow-matched,
rest → hyperaemia (2 solves). Transferred-0D parameters: diagnostic only, on a subset.

**What is compared with what.**
1. *Primary (continuous):* error-induced ΔFFR (corrupted − clean, within fidelity), 0D-discrete vs 3D-real — slope,
   bias, limits of agreement, per error type × protocol. Common-mode 0D–3D bias cancels here; it does not in κ.
2. *Secondary:* flip indicator, each fidelity against **its own** baseline; κ with cluster-bootstrap CI. Re-word H4 —
   κ on absolute decisions is dominated by baseline bias, and the spec's own M1 tolerance (0.05) equals a band width.
3. *The thesis panel, in 3D:* outlet-flow residual vs lesion FFR error, by protocol.
4. *Ladder:* 0D vs P (physics); P vs R (geometric reduction); 0D-as-meshed vs 0D-production (radius bias).
5. *Bridge:* leaky-0D with 3D-fitted lesion laws, A/B/C re-run on the 30.

**Cost.** Per instance per tier: 2 clean (rest, hyperaemia) + 4 error geometries × (A 1 + B 1 + C 2) = 18 solves.

| Item | Meshes | Steady solves |
|---|---|---|
| Tier R, 30 instances | 150 | 540 |
| Tier P, 30 instances | 150 | 540 |
| Extra operating points for ΔP(Q) fits (2 per clean geometry) | — | 120 |
| Verification §6, mesh independence (3 cases × 3 levels × 2 tiers), Carreau and transient-mean checks | ~20 | ~45 |
| **Total** | **~320** | **~1,250 ≈ 3,300 core-h ≈ 4–5 days on 32 cores** |

E3b pulsatile: cut from 20 runs to **6** (3 instances × {clean, T1 under C}, real lumen only) ≈ 1,150 core-h. It now
does double duty — the mechanism figure, and cycle-mean vs steady FFR on the same cases. The ~2,700 core-h saved pays
for Tier R. Human cost is meshing QA on 320 surfaces; both tiers must be scripted end to end before scaling (Gate M1
becomes: clean + 70 %DS + mask-deleted branch, **on both tiers**, plus the as-meshed radius check).
Minimum credible version if Tier R proves painful: 20 real-lumen instances, T1 + T2 only (the headline error types).

**Should the arm be cut?** No, but know what it buys. For topological errors the flip is a network flow-redistribution
effect; 3D adds the lesion's ΔP(Q) law and the geometric-reduction check, nothing more, and it does **not** answer
"not ground truth" in the clinical sense — only E6 does. With no deadline the restructured arm is worth its ~5 days. If
Tier R cannot be automated, cut to the 20-instance minimum rather than fall back to polyball-only: polyball-only is
worth less than it costs, because it invites attack A without answering it.

## 5. What the paper should claim from the 3D arm — and what it must not

**May claim**
- The error-induced FFR change and the A/B/C contrast are reproduced when the epicardial pressure-loss model is replaced
  by 3D Navier–Stokes **on the segmented lumen**, with boundary conditions tuned *in the 3D model* to its own targets.
- In 3D, as in 0D, flow-matched tuning drives the outlet-flow residual to ~0 while lesion FFR error persists (the panel).
- A quantified decomposition of 0D–3D disagreement into physics and geometric reduction.
- The hazard holds under both BC structures, with effect sizes that differ — and by how much.
- Mesh/solve failure rate by error type, labelled as pipeline-specific.

**Must NOT claim**
- That 3D is ground truth, or that the arm validates FFR accuracy. Every comparison is model-vs-model on a consensus label.
- "Replicated at 3D fidelity" for anything run with transferred parameters, or on polyball alone.
- That the 3D arm validates the **leaky** results directly; the bridge is 3D-calibrated losses inside the leaky network.
- Anything at ≥ 75 %DS from steady laminar solves unless the convergence and transient-mean checks pass there.
- WSS, flow-split accuracy, or cross-sectional-shape effects beyond the tiers actually run.

## 6. Residual risks after these revisions

1. **Attack D, item by item.** *Steady:* dismissible by practice — Gosling (*"steady, laminar flow assumptions"*),
   Gamage (steady CFX), Mao (`simpleCoronaryFoam`) — but the quadratic loss means steady-at-mean-flow under-reads the
   cycle-mean drop; E3b's six runs supply the number. *Laminar:* **the one that will be attacked.** The spec's "flag if
   throat Re > ~1000" borrows a pipe-transition number; post-stenotic jets destabilise at Re of a few hundred for severe
   constrictions (UNVERIFIED — Ahmed & Giddens 1983; Varghese, Frankel & Fischer 2007; not in corpus). At 80 %DS on a
   1.34 mm host, ~0.7 mL/s gives throat Re ≈ 400–450. Expect `simpleFoam` non-convergence at 75–80 %DS. Mitigation
   already in §4: near-threshold instances only; lower the flag to Re ≈ 300; on failure run `pimpleFoam` with steady BCs
   and time-average — never a turbulence model. *Rigid wall:* dismiss — universal in corpus (Grande, Mao, FAME, Gamage).
   *Newtonian:* dismiss with one Carreau sensitivity on 3 cases (Gamage used Carreau; throat shear is high-shear-limit).
2. **Real-lumen FFR may sit systematically above 0D** (off-axis centreline, MISR < area-equivalent radius). Near-threshold
   in 0D may not be near-threshold in 3D, thinning 3D flips. The continuous primary endpoint is robust to this; κ is not.
   Consider choosing %DS per host from a cheap 3D baseline pair so the *3D* baseline lands in 0.72–0.88.
3. **Protocol C redefinition ripples into the pre-registration** (H2, the "residual ≈ 0" outcome, C3's detector, which
   may turn out to be simply "outlet pressure, if you had it"). This is a plan-level issue the 3D review surfaced; it
   should be settled in WP-0 before either arm is frozen.
4. **Discrete-0D physiology is only probed, on a leaky-selected cohort.** Rerun on all 280 hosts with the V-suite; the
   ~7× tip over-flow (F3) is a stated limitation and a reason FFR is read at r ≥ 0.75 mm only.
5. **Two BC structures double the forking paths.** Pre-register the conjunction rule ("claimed only if it holds in
   both") and Holm across it, or a reviewer will call the second structure a rescue.
6. **Mask-edit T1 leaves a stump or a scar at the ostium** depending on where voxels are cut. Define the cut rule
   (e.g. one parent radius from the carina) and show it; the scar is realistic, but it must be the same in 0D.
7. **24/150 instances are single-outlet even at 0.75 mm** (mostly right trees). Exclude them from the 3D arm and say so;
   with one outlet, protocols A/B/C differ by one number and attack 4 ("one equation, one unknown") returns.
8. **Blinding (§9) is worth keeping** but must now also cover the tuned-in-3D step: the CFD operator receives target
   flows, never 0D FFR predictions.
