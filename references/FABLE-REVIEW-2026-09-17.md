# Strategic review — Paper 6 / T6 for IEEE JBHI SI "Integrating Imaging with Personalized Cardiovascular Medicine"

**Reviewer:** Fable 5.1 (strategic pre-submission review, not a peer review)
**Date:** 2026-09-17 — 28 days to the 2026-10-15 deadline
**Inputs read:** STUDY-PLAN.md (incl. §9), N1-SEARCH-LOG.md, all nine deep notes in `extraction/full/`, the FAME
database note, ACQUIRE-T6.txt, the ImageCAS-X email draft, the Phillips 2024 triage note, and the triage ledger
(203 rows; pulled Chan 2024, Sommer 2020, Dalmaso 2025, Mirota 2026, Lo 2020, and the Sankaran 2015 TMI note from
the ideation run's `extraction_mapped/`).
**Stance:** maximise probability of acceptance. Where the plan is weak I say so and rewrite it.

---

## 1. Verdict in three sentences

Attempt it, but only as a **reduced-order-only, hazard-plus-remedy paper** whose headline is a controlled
three-protocol boundary-condition ablation crossed with segmentation-error types, with a cheap detection test as the
closing contribution — not as the "ranking of error types" sensitivity study §1 currently describes, and not with a
WSS/OSI 3D arm. The science is sound and the SI fit is unusually exact, but the novelty margin over Gosling 2020 and
Fossan 2025 is moderate at best and evaporates if the paper is written as "sensitivity numbers plus a mechanism
someone else already published." With nothing yet built (data not on disk, tools not installed, team not agreed),
four weeks is enough for exactly one arm done properly; anything added on top lowers, not raises, the acceptance
probability.

---

## 2. Novelty — honest assessment

**Grade: MODERATE, conditional on the framing in §3. Under the current §1 framing: THIN-to-MODERATE.**

What is already in print, precisely:

- **The absorption mechanism is published.** Gosling 2020: cohort-averaged Rmodel re-normalises 1.23e10 →
  2.42e10 Pa/m³s⁻¹, absorbing a ~65% inflow change; accuracy 75% vs 72%, AUC 0.84 vs 0.82; the authors write that
  "the tuning of boundary conditions may obviate differences in predicted FFR that are expected if models predict
  flows quite different from the unknown physical flow." T6 cannot claim the principle.
- **The aggregate-blind / case-level dissociation is published.** Fossan 2025: AUC 0.845 vs 0.845 (p = 0.915) while
  sensitivity moved 58.1% → 68.6% (p = 0.0033) and R² 0.179 → 0.398. That is the exact "summary metric silent,
  individual cases move" phenomenon T6 wants to headline — from a BC *model* change, not from geometry corruption,
  but the epistemic point is made.
- **Per-section FFR-CT sensitivity to lumen-segmentation uncertainty is published in a top IEEE venue.** Sankaran,
  Grady, Taylor 2015 (IEEE TMI, HeartFlow): stochastic-collocation sensitivity per lumen section on 240 patients,
  "less than a 6% coefficient of variation in lumen area will translate into a sensitivity of FFR_CT of less than
  0.05 with 95% confidence." The plan does not mention this paper at all. It is the one a JBHI reviewer from the
  HeartFlow/Stanford lineage will reach for first, and it makes any "which segmentation error hurts FFR most"
  framing look derivative unless the error *types* are genuinely non-overlapping with dilation/erosion (only the
  topological ones are).
- **The null direction has real evidence, not just Tanade's assertion.** Dalmaso 2025 (52 patients, 81 invasive iFR,
  polynomial-chaos UQ on a 1D-0D model): vascular radius and steady flow dominate; compliance/waveform negligible.
  Tanade's "geometry dominates" is unmeasured (no Sobol index for geometry — geometry was never varied), but
  Dalmaso's is measured. So the "re-tuning cannot rescue geometry" outcome is not a fringe possibility.
- **Sommer 2020 (benchtop phantoms, 52 models, invasive FFR):** "for those intermediate conditions, with FFR between
  0.75–0.85, a 10% change in the boundary condition may result in a diagnosis change." BC-driven flips in the grey
  zone are empirically established.

What is genuinely open, and defensible as new:

1. **No controlled ablation of BC protocol × geometric error exists.** Gamage held resistance fixed and got a 13–15.5%
   downstream-branch effect; Gosling re-tuned and got nothing; Gamage explicitly attributes the disagreement to the
   tuning choice and *does not test it*. Fernández-Martínez re-tunes via Murray's law on every variant with "no
   untuned control." Nobody has run fixed-vs-re-derived-vs-target-matched on the same corrupted geometries.
2. **No topological error has been passed through a re-tuning pipeline.** Gosling's geometry never changes ("the
   word 'topolog-' does not appear"); Thondapu, Tanade, Fossan never perturb geometry; Sankaran's per-section
   variable "dilates or erodes in unison" and the authors concede missed narrowings are outside the stochastic space.
3. **Per-case reclassification under geometry corruption is unreported anywhere.** Gosling, Fossan, Gamage,
   Fernández-Martínez all stop at aggregate metrics or a single narratively-flagged patient (P9).
4. **A detection test for absorbed error does not exist in this literature.** Phillips 2024 supplies the
   system-identification idea; nobody has built the haemodynamic analogue.

Verdict on the margin: items 1–3 together are a solid *incremental* contribution (the ideation run's INCREMENTAL was
correct). Item 4 is what lifts it. **The lift is cheap** — it is an analysis on outputs the primary arm already
produces (see §3, §7) — and it fits four weeks. The CFD arm does not lift novelty on the paper's own question; it adds
a second, unrelated clinical question (plaque risk via WSS/OSI) and a large execution risk. Adding breadth is not the
same as adding novelty, and reviewers judge the central claim.

---

## 3. The strongest possible framing

### Which of (a) / (b) / (c)?

- **(a) Sensitivity/ranking study — reject this framing.** Sankaran 2015 owns "which part of the segmentation
  matters" in TMI; Fernández-Martínez owns "how much realistic threshold error moves FFR-CT"; Gamage owns the branch
  effect direction. Worse, in a 0D solver the "ranking of error types" is partly an artefact of how each type is
  mapped onto 0D parameters (an eccentric lumen *cannot* be represented in 0D except through an effective-area or
  elliptical-duct correction — see §7). A reviewer who notices that the ranking depends on the modeller's own mapping
  choices will not let it through as a headline.
- **(b) Hazard paper — necessary but not sufficient.** "BC tuning hides topological error" read alone is "Gosling
  for a new error class." A JBHI reviewer will write: "The authors show that a free outlet resistance can match a
  scalar target. This is one equation in one unknown." That objection is *correct* for unconstrained tuning, and it
  is fatal to a hazard-only paper (see §5, attack 1).
- **(c) Hazard-plus-remedy — the right framing.** The SI's aims paragraph asks for "robust validation frameworks."
  A paper that (i) shows the deployment pipeline's own BC-derivation rule silently cancels or amplifies specific
  segmentation-error types, (ii) shows that single-point FFR validation cannot see it while individual decisions
  move, and (iii) hands the reader a test that *does* see it, answers "so what should we do?" That is what gets a
  validation-methodology paper accepted at a top-10% venue rather than parked as "interesting sensitivity numbers."

### Recommended title (and two alternates)

1. **"Matched at the outlet, wrong in the tree: boundary-condition tuning conceals topological segmentation error in
   reduced-order coronary FFR, and a pullback-residual test that exposes it"**
2. "Well-validated but anatomically wrong: how outlet re-tuning absorbs segmentation error in CT-FFR models and how
   to detect it"
3. "Segmentation error that single-point FFR validation cannot see: a controlled boundary-condition ablation on 100
   coronary trees"

(Title 1 is long for IEEE; trim the second clause into the abstract if the editor objects. Keep "boundary-condition
tuning" and "segmentation error" in whichever survives — those are the SI's keywords.)

### Opening paragraph's argument (the hook)

Whether a missed coronary side branch changes a computed FFR depends on a modelling choice the literature has never
tested: Gamage et al. held outlet resistance fixed and found a 13–15.5% FFR shift from a downstream branch; Gosling
et al. re-tuned resistance and found no effect, noting that tuning "may obviate differences in predicted FFR." Both
are right, and that is the problem. Every deployed CT-FFR pipeline derives its outlet boundary conditions from the
segmentation it is given — so when the segmentation is topologically wrong, the boundary conditions are re-derived
from a wrong anatomy, and the error is partly cancelled, partly redistributed, and entirely invisible to a
validation that checks one distal pressure ratio. Fossan et al. have already shown that a boundary-condition change
can leave AUC untouched (0.845 vs 0.845) while moving sensitivity ten points; and the segmentation literature has
shown that "topological errors such as vessel breaks are present in all model predictions despite high DSC and
clDice." We ask, in a controlled ablation on 100 ImageCAS-X coronary trees, which segmentation-error types the
boundary-condition pipeline conceals, at what cost to individual revascularisation decisions, and whether the
concealment leaves a detectable signature.

### The single contribution sentence

"We show, in a factorial of four segmentation-error types × three boundary-condition protocols on 100 ImageCAS-X
coronary trees with error magnitudes calibrated to measured inter-observer disagreement, that the deployment
pipeline's outlet re-derivation and calibration-time target-matching restore single-point FFR agreement while
individual cases still cross the 0.80 threshold — and we give a pullback-residual / parameter-plausibility test that
detects the concealed error using outputs the pipeline already computes."

### Emphasise

- **The calibration-vs-deployment distinction.** Protocol C (target-matched, Gosling/Thondapu-style) is what a
  *validation study* does; Protocol B (BCs re-derived from the corrupted geometry via Murray's law / resting-state
  coupling) is what a *deployed pipeline* does. "Error absorbed at calibration is error committed at deployment" is
  the conceptual spine. Nobody has drawn this line in the FFR literature.
- **Per-case reclassification against a physiological-noise floor**, reported as P(flip | baseline FFR, error type,
  protocol), not as raw cohort flip counts.
- **Branch-location stratification** (Gamage's up/downstream asymmetry) — the most likely place the effect is
  heterogeneous, and heterogeneity is the interesting result.
- **The two-stage invisibility chain**: DSC/clDice hide topological error at segmentation (ImageCAS-X's own
  statement) → BC tuning hides it again at haemodynamics → single-point validation hides it a third time. Report a
  "DSC-invisible, FFR-visible" panel: at matched DSC, which error types move FFR.
- **The detector**, with a proper ROC on synthetic corrupted vs clean cases.
- **Both pre-registered directions.** If re-derived BCs *amplify* rather than absorb missed-branch error, the paper
  still resolves Gamage-vs-Gosling and still delivers the reclassification and detector results.

### De-emphasise or cut

- Cut "ranking error types by effect" as a headline; keep the ranking as one figure inside the factorial.
- Cut the WSS/OSI arm entirely from this submission (§6).
- Cut the "moves from INCREMENTAL toward NOVEL" reasoning — it is internal and it is wrong.
- Cut the P16 lineage from the abstract/introduction; one sentence in Methods ("variance decomposition follows
  [P16]") is enough. Do not describe this as a generalisation of a calibre-biomarker paper — it invites "so this is
  a re-application."
- Drop "eccentric/off-axis lumen" from the 0D arm (§7) unless an explicit elliptical-duct resistance model is used
  and declared.
- Do not use "digital twin" in the title. Use it once in the introduction to tie to the SI.

---

## 4. Impact and acceptance probability

**What makes JBHI reviewers accept this kind of paper:** a clearly stated, falsifiable question; a control that
isolates the mechanism (here: the three-protocol factorial); numbers a clinician can act on (reclassification counts
in the 0.75–0.85 zone, not just ΔFFR); a remedy or at least a recommendation; honest scoping of what the model
cannot see; and code + a public dataset so the result can be reproduced. JBHI is an engineering-in-medicine venue:
"we found a problem and we give you the tool to catch it" is its native register.

**What makes them reject:** "this is a known effect shown on a simpler model"; "the ground truth is the authors' own
model"; "the error types are synthetic"; "0D only, no 3D, no clinical data"; "the paper does not say what to do
about it"; and an unfinished secondary arm that reads as padding. Four of these six are live against the current
plan.

**Estimates (probability of eventual acceptance at JBHI, given submission):**

| Scenario | P(accept) | Reasoning |
|---|---|---|
| Current plan as written (§1 ranking + absorption headline, 0D primary, CFD arm attempted, error types assumed, no detector) | **~25%** | Fits the SI (low desk-reject risk) but reviewer 2 says "Gosling/Sankaran already," reviewer 3 says "0D model of a consensus label is not ground truth," and a half-finished WSS/OSI arm gives both a target. |
| Same, but CFD arm actually ships with 15–20 pulsatile cases | ~30% | Slightly broader, but the central-claim objections are untouched and the schedule risk of getting there is very high. |
| **Recommended framing (§3): 3-protocol factorial, P(flip \| baseline FFR) against a noise floor, branch-location stratification, detector with ROC, pre-registered both directions, code + deposited protocol, optional n≈5 steady-state 3D concordance check** | **~45–55%** | The mechanism is no longer the claim; the controlled ablation, case-level reporting and the remedy are. Remaining risk is "no clinical ground truth," which the SI's own aims paragraph partly absolves, and time. |
| Recommended framing but submitted late/rushed with the pipeline half-validated | ~20% | Number audits fail under review; a reviewer finds one internal inconsistency and the whole paper is distrusted. |

**Single highest-leverage change:** replace the §1 headline with the **three-protocol BC ablation as the primary
experiment** and make the **detector the closing contribution**. Everything else in this review is downstream of
that decision. Second highest: report reclassification as **P(flip | baseline FFR band)** with the Tanade-style
physiological-noise floor drawn on the same axes — this converts a cohort-dependent number into a transferable one
and pre-empts the two most common statistical objections at once.

---

## 5. The reviewer attacks, and the defence

Priority order. "Damage" is how likely this objection alone leads to rejection if unanswered.

**1. "Tuning a free resistance to match a scalar FFR is one equation in one unknown. Absorption is a tautology."**
Damage: fatal to the hazard claim if unaddressed.
Defence: never run unconstrained per-case tuning as the headline protocol. Protocol C must be *physiologically
constrained* exactly as Fossan 2025 requires: resistance derived from a re-simulated resting state, hyperaemic
factor k tied to resting Pd/Pa with population-level constants (khealthy, b = 4) that are **not** re-fit per case.
Under that constraint compensation is *not* guaranteed, and the interesting quantity is the residual error that
survives constrained tuning. Then report the *cost* of compensation: (i) displacement of the tuned parameters
relative to the population distribution (a plausibility score), (ii) non-transfer — tune at the distal point, then
evaluate at the side-branch outlet, at a second pullback location, and at the rest/hyperaemia pair (CFR proxy).
Figure: "matched here, wrong there." This turns the tautology into the paper's mechanism.

**2. "Your ground truth is a 0D model of a consensus segmentation. Nothing here is validated against a patient."**
Damage: high; this is the reflex objection to every synthetic-perturbation study.
Defence: (a) scope the claims explicitly as *error-induced change relative to a clean baseline*, in the abstract,
and say why that is the right quantity for a validation-methodology question (you are asking whether the pipeline
can *see* a change, which is model-internal by construction); (b) cite the SI's own aims paragraph in the
introduction; (c) cite svZeroDSolver's published validation lineage (Pfaller et al. 2022, automated 0D/1D ROM
generation — outside this corpus, verify before citing) and note Grande 2021's 0D/1D-vs-3D FFR agreement within 3%;
(d) the optional steady-state 3D concordance on n≈5 clean/corrupted pairs (§6) — if it shows the same
absorbed/not-absorbed pattern, the "0D artefact" objection is closed cheaply; (e) do NOT reach for FAME/other
invasive-FFR sources in four weeks — a bolted-on clinical comparison with n=3 does more harm than good.

**3. "The error types are synthetic and the magnitudes are assumed — the same weakness you criticise in
Fernández-Martínez."**
Damage: high, and currently *true* because ImageCAS-X releases consensus labels only.
Defence: send the Bransby email today; regardless of reply, the fallback must be made airtight: every magnitude
traced to a published ImageCAS-X number (HD95 2.46 ± 3.62 mm → radial/taper amplitude; Betti number error 0.2 ± 0.4
→ base rate of topological events per case; per-segment DSC 70.9–95.3% and side-branch DSC 70.9–83.6% → which
branches are at risk; DSC-vs-diameter ρ = +0.89 → diameter-dependent miss probability). State in Methods, in one
sentence, "magnitudes are measured; the apportionment across error types is assumed and swept." Then run a
**dose-response** over magnitude for every type so no conclusion hinges on one assumed value. This is still
materially stronger than importing 6%/15% from Schepis 2010 / Leber 2006 on other cohorts, and you can say so.

**4. "Flip rates depend on how many of your cases happen to sit near 0.80. This is a property of the cohort, not the
error type."**
Damage: medium-high; also a real design risk because ImageCAS is a segmentation dataset and many cases may have no
haemodynamically relevant stenosis (FFR ≈ 1 → no flips possible).
Defence: check stenosis prevalence on day 1. Report P(flip | baseline FFR band) with bands 0.70–0.75, 0.75–0.80,
0.80–0.85, 0.85–0.90, and pre-register virtual stenosis insertion with a severity sweep (Grande 2021 did exactly
this on a reference geometry) as the mechanism for populating the grey zone if the natural cohort is thin there.
Report net reclassification per protocol Fossan-style (AUC + sensitivity/specificity + explicit crossing counts in
both directions) so the "AUC unchanged, cases moved" dissociation is shown, not inferred.

**5. "You cannot distinguish geometry-induced flips from physiological-input noise; Tanade reclassified 50% of RCA
cases at 1 SD without touching geometry."**
Damage: medium-high if absent; trivial if present.
Defence: a no-injection Monte Carlo over cardiac output and MAP (Tanade's two dominant inputs) gives the
noise-floor flip probability per baseline-FFR band. Draw it as a shaded band on every flip-rate figure; report every
injected effect as *excess over the floor* with a CI. Budget it in WP-1 — it is a few thousand extra 0D solves.

**6. "The eccentric-lumen error type cannot exist in a 0D model; your 'ranking' is an artefact of the parameter
mapping."**
Damage: medium; it discredits the ranking figure and, by contagion, the rest.
Defence: drop eccentricity from the 0D arm, or represent it explicitly with an elliptical-duct Poiseuille correction
and say so. Replace it with **vessel break / truncation** — the topological error ImageCAS-X says is "present in all
model predictions" — which 0D represents faithfully (the distal subtree is lost and the pipeline places an outlet
with a Murray's-law resistance at the break: a textbook absorption case). Make the error-type table explicit about
what each type is in 0D terms (which block parameters change).

**7. "Gamage found the effect depends on branch location. You averaged over it."**
Damage: medium; easy to lose the effect in the mean.
Defence: stratify every missed-branch result by branch position relative to the stenosis (upstream / at / downstream)
and by branch-to-parent diameter ratio (Gamage's 1/3 rule as a pre-registered hypothesis). Report the interaction,
not the main effect.

(Also expect, lower priority: "why svZeroDSolver rather than 1D," "no compliance/pulsatility," "single dataset,
single scanner site," "no code." Answer the last one by depositing code and the frozen protocol before submission —
the P16/T13 discipline already exists for this.)

---

## 6. Scope decisions for a four-week clock

### The 3D CFD arm (WSS/OSI, 15–20 cases): cut it from this submission.

Argument, from the corpus's own numbers:

- **Compute does not fit.** Mao 2025: ~24 h on 8 cores per pulsatile case at ~300k cells, single reported
  configuration, no scaling data. The arm as designed needs clean + ≥2 corrupted variants × ≥2 BC protocols per
  case → 60–120 pulsatile runs → 1,400–2,900 wall-hours on one 8-core node. Even spread over five PCs that is 12–24
  days of continuous, failure-free compute inside a 28-day window that also has to contain the primary arm, analysis
  and writing.
- **Meshing risk is real and unbudgeted.** FAME database: 14.8% of ordinary reconstructed geometries discarded for
  self-intersection (RCA 26.6%), failing at surface generation, "occur[ring] primarily in regions where the vessel
  radius is large relative to the local radius of curvature" — exactly what taper and eccentricity injection
  manipulates. No repair step exists in any source ("FAME *excluded* bad geometries rather than repairing them").
- **Every shortcut is dead.** Grande 2021 never computes OSI and is validated on one synthetic geometry; Thakar 2026
  needs a fresh 3D CFD run per geometry before its surrogate helps, and never computes FFR. TAWSS/OSI
  post-processing must be built (Mao outputs raw per-step WSS only), plus a mesh-independence study.
- **It does not strengthen the central claim.** WSS/OSI answers a plaque-risk question the paper is not asking. A
  reviewer of the FFR-validation claim will not credit it; a reviewer of the WSS claim will attack n=15 with no mesh
  study and no validation. Two half-defended claims are weaker than one fully defended one.
- **It costs the thing you have least of:** operator attention during the only weeks the primary arm can be built.

Ship it as the follow-up paper it is; say so in one sentence of Future Work. If M1 must run at all, restrict it to
a **time-boxed (≤3 days) steady-state FFR-only 3D concordance check** on ~5 clean/corrupted pairs using only the
meshable error types (missed branch = clip-and-cap; taper/stenosis-length = radial scaling along the centreline;
*no* eccentricity), using Mao's steady solver (31 s single-core on 300k cells) — purpose: one supplementary figure
that closes the "0D artefact" objection. Hard kill if the pipeline is not producing FFR values by end of day 3.

### Minimum viable paper that still gets accepted

1. N ≈ 100 ImageCAS-X trees in svZeroDSolver (if the mask → centreline → 0D pipeline slips, **N = 40–50 with a
   virtual-stenosis severity sweep is acceptable** — the statistics are per-baseline-FFR-band, not per cohort).
2. Four error types with explicit 0D definitions: missed side branch (stratified by location and diameter ratio),
   vessel break/truncation, stenosis length/severity mis-sizing, distal taper/undersizing. Magnitudes traced to
   ImageCAS-X published disagreement; dose-response over magnitude.
3. Three BC protocols, frozen in WP-0: **A** fixed (clean-geometry BCs held) — the counterfactual; **B** re-derived
   from the corrupted geometry (Murray's-law outlet allocation + Fossan resting-state coupling) — the deployment
   pipeline; **C** target-matched under Fossan's physiological constraints — the calibration/validation scenario.
4. Physiological-noise floor (CO, MAP Monte Carlo, no injection).
5. Outputs: ΔFFR distributions; P(flip | baseline FFR band) per type × protocol with floor; net reclassification
   table; "matched here, wrong there" transfer panel for Protocol C; tuned-parameter plausibility distributions.
6. Detector: pullback-residual (spatial Pd/Pa profile of the tuned model vs the clean model, structured residual)
   and/or parameter-plausibility score; ROC for corrupted-vs-clean; report AUC and the operating point.
7. Deposited code, frozen hashed protocol, Source Data. Pre-registered both directions.

That is one figure-set of five main figures plus two tables. It is a complete paper.

### What can be cut with no cost to acceptance

- WSS/OSI arm (above).
- Eccentric-lumen type in 0D.
- Full 100-case cohort if the pipeline slips (see 1).
- Pulsatile 0D runs — steady hyperaemic solves are standard for FFR (Gamage, Sankaran, Dalmaso all steady or
  steady-equivalent); keep pulsatile only if the coronary BC block makes it free.
- The P16 lineage narrative.
- Multi-magnitude sweeps for taper/stenosis-length can be coarse (3 levels); spend resolution on the topological types.

---

## 7. Plan corrections

Things that are wrong, missing, or mis-sequenced. Items marked **[FATAL-IF-LATE]** would sink the submission if
discovered in week 3.

1. **[FATAL-IF-LATE] Stenosis prevalence in the ImageCAS-X subset is unknown.** ImageCAS is a segmentation dataset;
   if most trees give FFR ≈ 1, there are no decisions to flip and the paper has no result. Check on day 1 of D1
   (count cases with ≥ 50% diameter reduction from the centreline radius profile). Pre-register virtual stenosis
   insertion with a severity sweep as the mechanism for populating 0.70–0.90 regardless.

2. **[FATAL-IF-LATE] The mask → centreline → 0D pipeline is the real build, and it is not in the WP table.**
   svZeroDSolver consumes a 0D network, not a voxel mask. Verify on day 1 whether ImageCAS-X ships centrelines and
   surfaces (ACQUIRE item 3 says "verify"). If yes, a week is saved. If not, VMTK centreline extraction on ~100 trees
   with junction detection and radius sampling is the WP-1 critical path, and the WP-0 protocol freeze on days 5–8
   is premature — you cannot freeze injection rules for a tree representation you have not built. Re-sequence:
   pilot pipeline on 5 trees (days 3–7) → freeze protocol (day 8) → full sweep.

3. **Redefine the experiment as three BC protocols (A/B/C) and write the exact rules into WP-0.** The plan's
   "BC-retuning absorption test (does re-tuning outlet resistance/capacitance to match target pressure/flow mask
   topological error?)" is Protocol C only, and unconstrained. Without Protocol B, the paper never tests what a
   deployed pipeline actually does; without Protocol A, there is no counterfactual. Protocol C must obey the five
   Fossan constraints already listed in the risk table — turn them into numbered rules with the constants.

4. **Error-type taxonomy: replace "eccentric/off-axis" with "vessel break/truncation" in the 0D arm.** Define each
   type by which 0D block parameters change (missed branch: delete junction child and its subtree; break: truncate
   subtree at a point, create outlet; stenosis length: change L and stenosis coefficient of the stenosis block;
   taper: scale r(s) distal to a point). Add the Gamage diameter-ratio stratifier to the missed-branch type.

5. **Report P(flip | baseline FFR band) with the physiological-noise floor** (attacks 4 and 5). Add the no-injection
   Monte Carlo to WP-1 explicitly. Add Fossan-style net-reclassification tables (crossings in both directions).

6. **Add the detector to the design, not as an "optional closing contribution."** Concretely: for every corrupted
   case under Protocol C, compute (i) the spatial Pd/Pa profile along the main vessel (0D gives this at every block
   boundary; it is the model analogue of a pressure-wire pullback and of the clinical pullback pressure gradient
   index — Collet et al. 2019, JACC, outside this corpus, verify before citing), (ii) the residual profile against
   the clean model, (iii) the z-score of each tuned parameter against the Protocol-B population distribution. Then
   train nothing — use a fixed rule (e.g., max |residual| or a whiteness/runs statistic on the residual sequence,
   à la Phillips 2024) and report the ROC. This uses only outputs already computed; cost is one afternoon of
   analysis code.

7. **The "matched segmentation quality" phrase needs an operational definition.** Recommend: match on DSC. At equal
   DSC cost, a 1.5 mm missed branch and a 0.1 mm global taper look identical to the overlap metric; if they diverge
   in FFR, that is the "DSC-invisible, FFR-visible" panel that links to ImageCAS-X's own finding. If DSC matching is
   not achievable for all types, say so and match on HD95 instead.

8. **Run the N1 database strings this week (half a day).** The corpus is operator-assembled; a 2025–26 paper doing
   the A/B/C ablation would change everything, and it is better known now. Add Sankaran 2015 (TMI) and Dalmaso 2025
   to the "closest prior" table; both are currently absent from N1-SEARCH-LOG.md.

9. **Send the ImageCAS-X email today**, with the fallback already committed to in writing so a non-reply changes
   nothing on the critical path.

10. **[FATAL-IF-LATE] Authorship "to be agreed" with four weeks left.** Settle it this week. Strongly consider one
    clinical co-author (interventional cardiology or cardiac CT) — the guest editors are clinical/biomedical, and a
    clinician's voice on "what reclassification in the grey zone means for a PCI decision" materially strengthens
    the discussion and the cover letter.

11. **Number-audit and freeze discipline (P16 lesson):** freeze the protocol hash *after* the 5-tree pilot, not
    before; deposit code on Zenodo/OSF before submission; Source Data for every figure.

12. **Cover letter:** name the SI aims sentence verbatim, name Gosling/Fossan/Gamage and say precisely what was
    untested, and name the detector as the practical deliverable. Do not mention P16 or T13.

13. **If slipping past ~Oct 8 with results not final:** email the guest editors for a short extension rather than
    submit a half-validated paper. SI deadlines are routinely extended; a rejected rushed submission is not
    recoverable inside the SI, an extension request usually is. Regular JBHI submission remains open in any case.

---

## 8. The honest downside

**How it fails, in order of likelihood:**

1. **The pipeline is not producing 0D trees from ImageCAS-X masks by ~day 10.** This is the most likely failure and
   the plan does not currently see it because the WP table starts at "protocol." Recovery: drop to N = 40–50 with
   virtual stenosis insertion; the per-band statistics survive. If not producing trees by day 14, request an
   extension (item 13) — do not submit.

2. **No informative cases.** Few trees with grey-zone FFR → no flips. Recovery: virtual stenosis severity sweep,
   pre-registered. Cheap. Must be decided on day 1.

3. **Null on the headline, i.e., constrained re-tuning cannot absorb topological error; re-derived BCs amplify
   missed-branch error (Gamage/Dalmaso direction).** This is *not* a failure if pre-registered. The paper becomes
   "anatomical fidelity is irreducible: re-derivation amplifies rather than cancels topological error, and here is
   the per-case reclassification cost." It still resolves Gamage-vs-Gosling, still delivers reclassification and
   the DSC-invisible panel; the detector section shrinks to "not needed for topological error, needed for taper."
   Acceptance probability drops perhaps five points, not more. The most likely real outcome is heterogeneous
   (absorbed upstream, not downstream; absorbed for taper, not for breaks) — which is the richest result.

4. **The "one equation, one unknown" objection lands because Protocol C was run unconstrained.** Recoverable only if
   caught before submission (attack 1). This is a design error, not a schedule error — fix it in WP-0.

5. **A reviewer produces a 2025–26 paper that ran the ablation.** Probability low but non-zero; the corpus is not a
   systematic search. Recoverable only if found this week (item 8).

6. **Rushed submission with an internal inconsistency.** The P16 number-audit exists for this reason; do not skip
   it because of the clock.

**Realistic worst case:** the deadline is missed. That is recoverable — JBHI regular track, or the SI with an
extension, or another top-10% venue (Annals of Biomedical Engineering, Medical Image Analysis for the segmentation-
facing version). What is *not* recoverable is a rejected SI submission that was rushed to make the date and read as
"known mechanism, 0D only, synthetic errors, no remedy." The deadline is a soft constraint on value; the framing is
a hard constraint on acceptance. Choose accordingly.
