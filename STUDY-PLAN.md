# Paper 6: T6
# Segmentation error types ranked by their effect on reduced-order FFR decisions at 0.80, at matched segmentation quality — with a secondary full-3D-CFD (WSS/OSI) robustness arm

> **SUPERSEDED 2026-09-18 — the live plan is now `STUDY-PLAN-v2.md`. Start there.**
> On 2026-09-18 the operator removed the deadline constraint ("even if we miss the CFP, we will submit it still;
> focus on making the paper strong, novel and impactful") and v2 was written on that basis: deadline-unbound,
> three contributions, pre-registered both directions, 3D arm reframed to FFR-only cross-fidelity replication,
> WSS/OSI and TAG dropped. **This file is retained as the decision log** — §2 (the original CFD-arm case), §9
> (claim positioning after N1) and §10 (the independent review, the Sankaran resolution, the TAG rejection)
> record how v2 was reached and should not be re-litigated. Gate evidence: `references/N1-SEARCH-LOG.md`.
> The ImageCAS-X data request (`drafts/EMAIL-IMAGECAS-X-2026-09-17.md`) was **sent 2026-09-18**; awaiting reply.

**Target:** IEEE JBHI, Special Issue "Integrating Imaging with Personalized Cardiovascular Medicine: Current Advances
and Future Directions." **Submission deadline: 15 October 2026.** Guest editors: Monika Colombo (Aarhus), Simona Celi
(Fondazione Toscana G. Monasterio), David Marlevi (Karolinska), Monica Sigovan (CREATIS). Publication model: HYBRID
(subscription default; optional OA APC ~US$2,800, not required).
- **Tier:** Top 10% (operator-confirmed WoS JCR, 2026-09-17). JIF 6.8 (2024); Scimago Q1 is context only, not the basis.
- **Scope match confirmed 2026-09-17** against the SI's own verbatim CFP (fetched from
  https://www.embs.org/jbhi/wp-content/uploads/sites/18/2025/12/Integrating-Imaging-with-Personalized-Cardiovascular-Medicine-Current-Advances-and-Future.pdf).
  The CFP's own aims paragraph names the exact gap this paper addresses: *"Quantitative analysis must contend with
  uncertainty propagation, segmentation errors, and the need for robust validation frameworks."* Matches topics of
  interest: Quantitative Image Analysis and Uncertainty Management; Digital Twin Frameworks and Experimental
  Validation; Advanced Biomechanical Modelling from Imaging Data; Clinical Translation of Imaging-based Predictive
  Models.

**Status:** plan assembled 2026-09-17 through direct chat-based analysis (CFP fetch, dataset check, head-to-head
comparison against T13, CFD-strengthening addendum). **Not yet run through the research-ideation skill's formal
`pursue T6` resume/rubric-conversion flow** — do that before locking work packages, the way T13 has a converted
pipeline-rubric score (74.5) and this does not yet. Not started.
- **Order:** prioritized ahead of T13 (Paper 5) on 2026-09-17 specifically because of the hard external deadline
  below and lower execution risk (reuses already-built P16/FW1 machinery). T13 continues in parallel with no clock on
  it — see relationship notes below.

**Score:** 7.00/10, Band A, **INCREMENTAL** (2026-09-13 ideation run; tied 2=/13 with T18 and T24). Contrast with
T13's 7.30/10, Band A, the only **NOVEL** candidate in that run. The CFD-strengthening addendum below is aimed
specifically at closing that INCREMENTAL/NOVEL gap.

**Sources:**
- `../Proposal/ideation_run/2026-09-13/candidates.json` (ID T6, merged with T5 "FFR flip rate under lumen
  uncertainty" and T7 "missing communicating arteries and collateral flow")
- `ideation_report.md` §7 (rank 2=; tier flags updated 2026-09-17 after operator confirmation)
- `../Proposal/ALL-STUDIES-RANKED-2026-09-13.md` (row 22, I-T6)
- `../Proposal/ideation_run/2026-09-13/licence_checks.md` (row 18, ImageCAS-X)
- `../Proposal/ideation_run/2026-09-13/landscape.md` (line 96, JBHI SI entry)
- JBHI CFP PDF, fetched 2026-09-17 (URL above) — full text archived in this session's record; re-fetch before
  submission in case guest editors revise scope or dates.

**Relationship to the other papers:**
- **P16 (Paper 1):** T6 generalizes P16's variance-decomposition framework from a geometric biomarker (vessel
  calibre) to a physics-based reduced-order flow output (FFR). Cite P16's methodology; this is an explicit follow-on,
  not an independent flagship — say so in the paper, don't oversell novelty on this axis.
- **T13 (Paper 5):** sibling candidate from the same 2026-09-13 ideation run. Compared head-to-head 2026-09-17: T6
  chosen to run first because of the Oct 15 deadline and lower method risk; T13 remains the higher-ceiling,
  no-deadline flagship attempt (potential Nature Methods route) and should not be rushed to match T6's clock. Do not
  let T6 consume authorship bandwidth T13 needs — see T13's own STUDY-PLAN.md risk register.
- **I-T5, I-T7:** already merged into T6 in the 2026-09-13 run (FFR flip rate under lumen uncertainty; missing
  communicating arteries/collateral flow). Their scope is inside T6, not separate work.

---

## 1. Claim

Prior FFR-CT sensitivity studies (closest prior work: 10.1002/cnm.3822-type single-cohort designs) perturb lumen
radius by researcher-chosen synthetic amounts. T6 instead draws error sizes from **real inter-segmenter disagreement
at matched segmentation quality**, and ranks error types (stenosis-length, off-axis/eccentric lumen, missed
side-branch/topological, taper/undersizing) by their effect on the **binary FFR ≤0.80 revascularization decision**,
not just aggregate error magnitude.

**Headline hypothesis:** boundary-condition re-tuning in the reduced-order solver can *absorb* (mask) topological
segmentation error — a model can look well-validated on outlet pressure/flow while the underlying anatomy is
topologically wrong, because the solver's free parameters silently compensate. This is a validation-methodology
finding, not just a sensitivity number, and it is the exact gap the SI's aims paragraph names.

## 2. CFD-strengthening addendum (added 2026-09-17, operator has multi-PC OpenFOAM capacity)

**Decision: do not replace the reduced-order FFR arm with full 3D CFD.** The 2026-09-13 feasibility gate scoped T6
down to svZeroDSolver specifically because full 3D CFD does not fit a ~1-month window; that constraint is unchanged.
Redoing the FFR analysis itself at full 3D fidelity across the whole cohort reintroduces the infeasibility the gate
was designed to cut.

**Instead: add a secondary, smaller full-3D-CFD arm computing WSS and OSI** — quantities the reduced-order model
structurally cannot produce (spatially-resolved field data). This is additive novelty, not a redundant fidelity
upgrade of the same output:
- Tests whether the BC-absorption finding generalizes across **model fidelity** (0D/1D vs 3D) and **quantity type**
  (binary decision vs spatially-distributed field).
- Ties directly to a second, clinically real downstream use (plaque-vulnerability/rupture-risk stratification via
  WSS/OSI) that the reduced-order arm cannot address at all.
- Directly strengthens the "Advanced Biomechanical Modelling from Imaging Data" topic-of-interest match.
- If it lands, this is the mechanism by which T6 could move from INCREMENTAL toward NOVEL — the same gap currently
  separating it from T13.

**Scope guardrail:** primary reduced-order arm stays at the full N=100 ImageCAS-X subset (deadline-safe, statistical
power). Secondary full-CFD arm is capped at **15–20 representative cases**, chosen to span the injected error types,
not the full cohort.

**Hard gate before committing the CFD arm as a deliverable:** pilot the meshing pipeline (segmentation → surface mesh
→ volume mesh → pulsatile solve with Windkessel-coupled outlets) on 2–3 cases, **including at least one deliberately
error-injected / topologically broken geometry** (the error types are, by design, the hard case for automated
meshers like snappyHexMesh). See Gate M1 below. If meshing fails on error-injected geometries in a way that can't be
fixed quickly, the CFD arm drops to a fast follow-up paper rather than blocking the Oct 15 submission.

## 3. Gates (before code; tracked in `ACQUIRE-T6.txt`)

| Gate | Question | Pass | If it fails |
|---|---|---|---|
| **N1 novelty** | Beyond 10.1002/cnm.3822-type synthetic-perturbation FFR-CT sensitivity studies, has anyone ranked *real* segmenter-disagreement error types by FFR-decision-flip effect, or shown BC-tuning absorbs topological error? | No such paper found | Re-scope claim to what remains distinct |
| ↳ **N1 verdict 2026-09-17** | **PROVISIONAL PASS.** 203-paper corpus triaged; 3 THREAT flags escalated to full-text reads and all 3 downgraded. Closest five (Fernández-Martínez cnm.3822, Gosling 2020, Fossan 2025, Gamage 2022, Tanade 2022) each stop short for a documented, quotable reason. Full evidence: `references/N1-SEARCH-LOG.md` | — | **Not closeable yet:** ACQUIRE-T6 database search strings still unrun; a curated corpus is not a systematic search. Claim positioning must change — see §9 |
| **D1 data** | ImageCAS-X 100-case coronary subset downloaded (CC BY 4.0, zenodo.org/records/21887809 — confirmed open 2026-09-17, **not yet on disk**) | Subset downloaded and verified; note dataset carries **no FFR or clinical ground-truth labels** | Reduce cohort size or seek a supplementary paired-invasive-FFR source for validation framing |
| ↳ **D1 finding 2026-09-17** | Does ImageCAS-X carry **real inter-observer disagreement**? **YES** — 160 test scans each re-annotated by a different analyst, chosen at random, blinded to the first labels, no lead-analyst review. Reported: lumen DSC 92.8±3.1%, HD95 2.46±3.62 mm, **Betti number error 0.2±0.4** (a topological disagreement metric between real humans), clDice 95.4±3.6%, ASSD 0.53±0.33 mm. Per-segment DSC 70.9% (L-PLA) → 95.3% (RCA); side branches 70.9–83.6%. Stratifiers: DSC vs diameter ρ=+0.89, vs lumen attenuation ρ=+0.90, distal decline ρ=−0.36, diseased 91.9% vs healthy 93.6% (p<0.001) | Magnitudes for error injection are now sourceable from **measured** disagreement, not borrowed literature values — this is the differentiator over cnm.3822, which imported its 6%/15% from Schepis 2010 / Leber 2006 | **Open risk:** only consensus labels are released; the **per-annotator masks are not**. Without them, error *types* cannot be derived directly, only magnitudes. Mitigation: request the 160 paired re-annotations from the authors (draft: `drafts/EMAIL-IMAGECAS-X-2026-09-17.md`); fallback is calibrating from the published per-segment tables |
| **T1 tools** | svZeroDSolver installed (BSD-3, open source — confirmed); OpenFOAM available and verified on the operator's multiple PCs | Both run on at least one case | Drop the CFD addendum, ship reduced-order-only |
| **M1 pilot (new, CFD-addendum specific)** | Does the segmentation→mesh→solve pipeline complete on 2–3 pilot cases, including ≥1 deliberately error-injected/topologically broken geometry? | Meshing + pulsatile WSS/OSI solve completes without major manual rework | CFD arm deferred to a fast follow-up paper; primary submission proceeds reduced-order-only (already feasibility-safe) |
| ↳ **M1 evidence 2026-09-17** | Literature now scoped (full notes in `extraction/full/`). **Backbone:** Mao 2025 `CoronaryHemodynamics` (OpenFOAM, cfMesh, Windkessel auto-scaled from outlet cap areas by Murray's law) — PARTIAL-FIT, ~24 h on 8 cores per pulsatile case at ~300k cells. **Base failure rate:** FAME database discarded **135/914 = 14.8%** of geometries for self-intersection (RCA 26.6%), failing at *surface reconstruction* not meshing; once past that check, meshing succeeded 779/779 in 41 min total. **Both shortcuts are dead:** Grande 2021 hybrid 1D–3D **never computes OSI**; Thakar 2026 differentiable surrogate is calibrated **per-geometry** against a high-fidelity CFD run on the same domain, so every corrupted geometry needs its own CFD run first | Pilot still required — no source tests meshing on deliberately broken geometry | **Three gaps must be built, not borrowed:** (1) a surface-repair step (FAME *excluded* bad geometries rather than repairing them); (2) OSI and time-averaged WSS post-processing (Mao outputs raw per-step WSS only); (3) ≥15–27% case attrition budgeted as a floor, since the FAME failure mode — local radius-vs-curvature mismatch — is exactly what eccentric-lumen and taper injection manipulates |

## 4. Design

- **Primary arm (deadline-safe):** ImageCAS-X, 100-case coronary subset, svZeroDSolver. Error types injected from
  real inter-segmenter disagreement distributions, at matched segmentation quality. Outcome: FFR ≤0.80 decision-flip
  rate per error type; BC-retuning absorption test (does re-tuning outlet resistance/capacitance to match target
  pressure/flow mask topological error in the final FFR value?).
- **Secondary arm (gated on M1):** 15–20 cases, same injected error types, OpenFOAM 3D CFD with Windkessel-coupled
  outlets, pulsatile inlet waveform. Outcome: time-averaged WSS and OSI per error type; same BC-absorption test at 3D
  fidelity; cross-fidelity comparison against the primary arm's findings.
- **No independent invasive-FFR ground truth available in ImageCAS-X** — frame claims around *error-induced changes*
  relative to a clean-segmentation baseline, not absolute FFR accuracy; cite published svZeroDSolver validation
  literature to support the reduced-order model's general credibility.

## 5. Work packages (~4 weeks to the 2026-10-15 deadline; compressed relative to T13's 4–5 week pace)

| Days (from plan start) | WP | Output |
|---|---|---|
| 1–3 | Gates N1, D1, T1 | Verdicts written into this file; ImageCAS-X downloaded |
| 3–5 | Gate M1 pilot | Go/no-go on the CFD secondary arm — **hard checkpoint** |
| 5–8 | WP-0 Protocol | Error-injection scheme, BC-tuning protocol, decision thresholds frozen + hashed + third-party deposit (P16/T13 discipline) |
| 8–16 | WP-1 Primary reduced-order arm | Full 100-case sweep, decision-flip rates, BC-absorption test |
| 12–20 (parallel, only if M1 passed) | WP-2 Secondary CFD arm | Mesh + solve 15–20 cases; WSS/OSI per error type |
| 16–22 | WP-3 Analysis | Cross-fidelity comparison; figures; Source Data |
| 22–27 | WP-4 Writing | Manuscript, cover letter, number audit (P16 lesson) |
| 28 | Submit | 2026-10-15 |

## 6. Start condition

- Gates N1, D1, T1 can start any time — reading, downloading, installing.
- Gate M1 (pilot) should run **immediately after** D1/T1 clear, before committing to the CFD-addendum scope in
  writing — this is the single biggest schedule risk in the plan.
- A P16 revision request pre-empts everything (standing rule across all papers).

## 7. Team and authorship

To be agreed.

## 8. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Meshing error-injected (deliberately broken) geometries fails or needs heavy manual rework | Medium-High | Gate M1 pilot on 2–3 cases first, days 3–5; hard go/no-go before WP-0 |
| Full CFD arm (even at 15–20 cases) doesn't finish before Oct 15 | Medium | Scope-capped at 15–20 cases; primary reduced-order arm is independently deadline-safe on its own if the CFD arm slips |
| ImageCAS-X has no FFR/clinical ground truth | Known, not a blocker | Frame around error-induced *change*, not absolute accuracy; cite svZeroDSolver validation literature |
| T13 competes for the same authorship bandwidth | Medium | 2026-09-17 decision: T6 first (hard deadline), T13 in parallel without a clock — do not let T6 slip into T13's runway |
| JBHI reviewers read this as narrow (coronary-only, single decision threshold) | Medium | The WSS/OSI secondary arm, if M1 passes, broadens the claim beyond one clinical decision type |
| Verdict was INCREMENTAL, not NOVEL, in the 2026-09-13 run | Known | Don't oversell; the CFD addendum is the specific lever aimed at closing this gap, not a guarantee |
| **Per-annotator masks unavailable** — ImageCAS-X releases consensus labels only, so error *types* cannot be derived from measured disagreement without them | Medium-High | Author request sent (`drafts/EMAIL-IMAGECAS-X-2026-09-17.md`); fallback calibrates magnitudes from published per-segment/diameter/attenuation tables. **Time-critical: the only item with an external dependency on a 4-week clock** |
| **Physiological-noise confound (Tanade 2022)** — physiological-input uncertainty alone reclassified 50% of RCA / 25% of LCA cases at 1 SD | High | Report every injected-error flip rate **against this baseline**, or a reviewer attributes the flips to physiological noise rather than geometry. Budget a no-injection control sweep in WP-1 |
| **Naive BC re-tuning is physiologically indefensible (Fossan 2025)** — outlet resistance is coupled to stenosis severity via autoregulation, not a free scalar | High | Re-tuning after a geometry change must **re-simulate the resting state first** (coupling variable is pressure-based, x=1−Pd/Pa); severity-to-resistance constants stay population-level, not re-fit per case. Freeze this in the WP-0 protocol |
| **Headline may return null** — Tanade (geometry dominates) and Gosling (tuning absorbs) predict opposite outcomes | Medium | Pre-register **both** directions in WP-0 with one analysis plan. The inverted result ("re-tuning cannot rescue topological error; anatomical fidelity is irreducible") is equally publishable for this SI, but only if committed to in advance |
| **FATAL IF LATE — stenosis prevalence in the ImageCAS-X subset is unknown.** It is a *segmentation* dataset, not a CAD cohort. If most trees compute FFR≈1, there is nothing near 0.80 to flip and the entire decision-flip outcome collapses | **High** | **CHECK ON DAY 1**, before any protocol work: compute baseline FFR on 10–15 trees and inspect the distribution near 0.80. If prevalence is too low, fall back to a virtual-stenosis severity sweep (N=40–50 with controlled stenosis insertion), which the review judges acceptable. Do not freeze WP-0 until this is known |
| **FATAL IF LATE — the mask → centreline → 0D model pipeline is the real build, and is absent from the WP table** | **High** | It is assumed, not scheduled. Run a **5-tree end-to-end pilot before the WP-0 protocol freeze**; the current day 5–8 freeze is premature until that pilot runs. Add the pipeline build explicitly to the WP table |
| **"One equation, one unknown" objection** — if Protocol C re-tunes a single free parameter to match a single target, a reviewer notes the fit is trivially exact and the result is an artefact of the setup | **High (fatal if unaddressed)** | This is a **WP-0 design decision, not a schedule item**: Protocol C must be constrained (Fossan's population-level constants, resting-state re-simulation, more targets than free parameters). Write the constraint into the frozen protocol |

## 9. Claim positioning after N1 (added 2026-09-17 — evidence only; §1–2 prose deliberately left for the operator to rewrite)

The N1 reads did not break the study, but they do move the ground under §1–2. Recorded here rather than edited into
the claim itself, because the central claim sentence should be written in the operator's own voice.

**What is already in print, and must not be claimed as new:**
- **Gosling 2020** demonstrates BC tuning absorbing a large flow discrepancy — cohort-averaged CMVR re-normalises
  1.23e10 → 2.42e10 Pa/m³s⁻¹, absorbing ~65% inflow change with aggregate accuracy 75% vs 72%, AUC 0.84 vs 0.82,
  and states outright that tuning "may obviate differences in predicted FFR." **The mechanism is published.**
- **Fossan 2025** publishes the aggregate-blind-to-case-level dissociation: swapping the outlet BC model left
  **AUC unchanged (0.845 vs 0.845, p=0.915)** while sensitivity moved **58.1%→68.6% (p=0.0033)**.

**The four axes on which T6 remains distinct from Gosling — state these explicitly in the paper:**
1. *Topological* error (missed/misconnected branch), not flow under-representation on an unchanged single-lumen geometry.
2. *Per-case* re-tuning, not a single cohort-averaged constant.
3. *Per-case reclassification* reported, not aggregate accuracy — Gosling reports zero threshold-flip counts.
4. Framed as a *validation hazard*, not as reassurance that simpler models are adequate.

**Recommended lead (stronger than the current §1 framing):** open on the **Gamage 2022 contradiction** — whether a
missed side branch matters depends on whether outlet resistance was re-tuned, and the literature disagrees
accordingly. Gamage held resistance fixed, reported downstream-branch removal shifting FFR 15.5% (idealised) / 13%
(patient) versus upstream 0.002 / 2%, and merely *noted* that a differently-tuned external study reached the opposite
conclusion. Nobody has tested it as a controlled ablation. This makes T6 the resolution of a live disagreement rather
than a speculative hypothesis.

**Design consequence:** the missed-branch arm must **stratify by branch location relative to the stenosis**, or
Gamage's asymmetry averages the effect away. Gamage's analytical "<1/3 main-vessel diameter = negligible" rule is a
ready-made hypothesis to test against.

**Upstream framing gift (ImageCAS-X):** that paper states *"topological errors such as vessel breaks are present in
all model predictions despite high DSC and clDice."* T6 becomes the second link in a chain — overlap metrics hide
topological error at the segmentation stage, and BC re-tuning hides it again at the haemodynamic stage.

**Optional closing contribution — consider seriously.** Phillips 2024 (`extraction/triage/phillips-2024-validation-framework.md`)
supplies system-identification validation apparatus (residual whiteness and independence tests) that distinguishes
"the model fits the outputs" from "the model captures the system." Proposing this as a **detector** for BC-absorption
would turn the paper from a warning into a remedy, and answers the reviewer question "so what should we do about it?"
— valuable for an SI explicitly about validation frameworks. **The §10 review upgrades this from optional to the
recommended closing contribution.**

## 10. Independent strategic review, 2026-09-17 — recommended pivot (full text: `references/FABLE-REVIEW-2026-09-17.md`)

Commissioned to assess plan, novelty and impact, and to frame the paper for **acceptance probability**, not scope fit.
Read the full file before acting; this is the summary and the decisions it forces.

### Verdict
Attempt it, but as a **reduced-order-only, hazard-plus-remedy paper** whose primary experiment is a controlled
**three-protocol boundary-condition ablation** crossed with segmentation-error types, closing with a detection test.
**Not** the "ranking of error types" study §1 currently describes, and **not** with a WSS/OSI 3D arm. Nothing is built
yet — data not on disk, tools not installed, authorship unsettled — and four weeks buys exactly one arm done properly.

### Novelty grade
**MODERATE under the recommended framing; THIN-to-MODERATE under the current §1.** Two prior works matter and one was
missed by the N1 corpus:
- **Sankaran, Grady & Taylor 2015** — "Fast Computation of Hemodynamic Sensitivity to Lumen Segmentation
  Uncertainty," IEEE TMI 34(12):2562–2571, **DOI 10.1109/TMI.2015.2445777** (verified against Crossref and Semantic
  Scholar 2026-09-17; the review's original citation had the title wrong, which is why it appeared to be missing).
  **It was never missing** — PDF already in `Resources/`, extracted in the 2026-09-13 run as
  `sankaran-2015-hemodynamic-sensitivity`, and already listed in `ACQUIRE-T6.txt` item 2 as required reading. The
  N1 log had simply never mined the 624 pre-existing notes; that gap is now recorded and being closed.
  **What it does:** 240 patients, adaptive stochastic collocation + ML surrogate (correlation 0.91, MAE 0.0094),
  ranking *regions* by geometric sensitivity to direct human editing; quantifies allowable lumen-area c.o.v.
  (<6% c.o.v. → FFR sensitivity <0.05 at 95% confidence).
  **What it does NOT do, and this is what T6 keeps:** perturbation is one random variable per section — "the entire
  section dilates or erodes in unison" — so no distinct error types, no local/asymmetric/topological error;
  magnitudes are *assumed* dispersion, never calibrated to measured inter-rater disagreement (no Dice/Hausdorff
  anywhere); the outcome is a continuous standard deviation, never per-case reclassification across 0.80; and BCs
  are never re-tuned after perturbation.
  **It hands T6 its warrant in its own future work:** "if a lumen narrowing is entirely missed in the initial
  segmentation, sensitivity information will not be captured"; "a missed bifurcation could change the sensitivity
  values assigned to different parts of the coronary geometry"; and a call for "a more accurate uncertainty model
  that accounts for image quality and initial lumen segmentation."
  **Net effect:** it wounds a "ranking error types by sensitivity" headline — HeartFlow got there first, at scale,
  in a top venue — but it strengthens the case for the three-protocol BC ablation, which it never attempts.
- **RESOLVED 2026-09-17 (late) — there are FOUR Sankaran papers, all now read, and none blocks T6.**
  MICCAI 2014 (precursor, pp. 30–37 of `Resources/978-3-319-10470-6.pdf`) → **IEEE TMI 2015** (ranks *regions*) →
  **CMAME 2015**, DOI 10.1016/j.cma.2015.08.014 (the methods paper; `Resources/1-s2.0-S0045782515002728-main.pdf`) →
  **J Biomech 2016** (ranks *variables*: MLD > boundary resistance > viscosity > lesion length).
  Every one perturbs lumen radius as a per-section/per-segment scalar with **bifurcations held fixed**, reports
  **continuous** sensitivity rather than threshold reclassification, and **never re-tunes boundary conditions after a
  geometry change**. The CMAME paper is the *weakest* grounded of the four — its perturbation magnitude is "defined
  usually as a percentage of the radius" with no citation to any measurement whatsoever.
  **Quote to use in the paper** — HeartFlow drawing, in print, the exact boundary T6 crosses:
  *"We limit the developments of this paper to uncertainty in lumen radius... The validation of the perturbation
  model is restricted to deformation maps with fixed bifurcation locations."*
  **Also resolved:** Colebank 2019 (R. Soc. Interface) is the closest *structural* precedent — segmentation variation
  through a 1D model, concluding topology dominates — but in mouse pulmonary arteries, with algorithm-parameter
  resampling rather than inter-observer data, no error-type taxonomy, and **no threshold outcome at all**. Cite and
  distinguish; pre-empt the reviewer line "already shown in the pulmonary circulation."

- **Dalmaso 2025** (in corpus, id 061) — 52 patients, polynomial-chaos UQ; supplies the real evidence for
  "geometry dominates" that Tanade 2022 only asserts. Strengthens the null branch.

What remains open and defensible: the A/B/C ablation nobody has run, topological error carried through a re-tuning
pipeline, per-case reclassification, and a detector.

### The three protocols (new primary experiment)
- **A — fixed:** outlet BCs held at baseline values after the geometry is corrupted.
- **B — re-derived:** outlets recomputed from the corrupted geometry (the deployment case — Murray's-law/allometric
  rules applied to wrong anatomy).
- **C — target-matched:** outlets re-tuned to match pressure/flow targets, **physiologically constrained** per Fossan
  (resting-state re-simulated first; population-level severity-to-resistance constants; more targets than free
  parameters — see the "one equation, one unknown" risk in §8).

Spine of the argument: **error absorbed at calibration is error committed at deployment.**

### Recommended title and contribution
> *Matched at the outlet, wrong in the tree: boundary-condition tuning conceals topological segmentation error in
> reduced-order coronary FFR, and a pullback-residual test that exposes it*

(two alternates in the review file)

> **Contribution:** "We show, in a factorial of four segmentation-error types × three boundary-condition protocols on
> 100 ImageCAS-X coronary trees with error magnitudes calibrated to measured inter-observer disagreement, that the
> deployment pipeline's outlet re-derivation and calibration-time target-matching restore single-point FFR agreement
> while individual cases still cross the 0.80 threshold — and we give a pullback-residual / parameter-plausibility
> test that detects the concealed error using outputs the pipeline already computes."

### Acceptance probability
| Scenario | Estimate |
|---|---|
| Current plan as written | **~25%** (reviewer 2: "Gosling/Sankaran already did this"; reviewer 3: "a 0D model of a consensus label is not ground truth"; a half-finished CFD arm hands both a target) |
| Recommended framing | **~45–55%** |
| Rushed/late, pipeline half-validated | ~20% |

**Highest-leverage change:** make the three-protocol ablation the primary experiment and the detector the closing
contribution. **Second:** report reclassification as **P(flip | baseline-FFR band)** with a Tanade-style
physiological-noise floor plotted on the same axes.

### ⚠ DECISION REQUIRED — the 3D CFD arm (this contradicts §2, which is the operator's own 2026-09-17 decision)
The review recommends **cutting the WSS/OSI 3D arm from this submission**. The arithmetic:
- Mao's own figure, 24 h on 8 cores per pulsatile case → 60–120 required runs → **1,400–2,900 wall-hours**.
- FAME's **14.8% surface-failure rate** (RCA 26.6%) is precisely the radius-vs-curvature mechanism that taper and
  eccentric-lumen injection manipulate, and **no source in the corpus has a repair step**.
- Grande never computes OSI; Thakar needs a fresh high-fidelity 3D run per geometry.
- It answers a plaque-vulnerability question **this paper is not asking**.

**If M1 runs at all:** a ≤3-day, steady-state, **FFR-only** concordance check on ~5 clip-and-cap / radial-scaling
pairs, for one supplementary figure, with a hard kill at day 3.

*This reverses §2 and is the operator's call — not actioned. §2 left intact pending that decision.*

### Minimum viable paper (what still gets accepted)
N≈100 (N=40–50 with a virtual-stenosis severity sweep acceptable); **four error types with explicit 0D definitions —
drop eccentric lumen, add vessel break/truncation**; three frozen BC protocols with Fossan's constraints written as
numbered rules; noise-floor Monte Carlo; P(flip | band) and net-reclassification tables; a "matched here, wrong there"
transfer panel; detector ROC; deposited code and hashed protocol; **both directions pre-registered**.

### Citations to verify before use
**Pfaller 2022** (svZeroDSolver lineage) and **Collet 2019** (pullback pressure gradient index) are cited by the
review from outside the corpus and are **unverified** — obtain and check both before they enter the manuscript.

### TAG detector idea — CHECKED AND REJECTED, 2026-09-18

An idea was floated to make the closing detector *imaging-based*: re-tune the BCs to match outlet pressure/flow, then
check an independent imaging-derived target — the transluminal attenuation gradient (TAG), computable from a single
CCTA — on the reasoning that if tuning had absorbed geometric error, the model would still fail the imaging check.
**A novelty and viability sweep was run and the idea does not survive. Do not spend time on it.**

- **TAG already sets boundary conditions.** A published CT-FFR algorithm "uses TAG of each coronary artery to
  determine outlet boundary conditions," and another derives BCs from lumen deformation plus TAG. In those pipelines
  TAG is not independent of the tuning at all — it *is* the tuning input.
- **TAG is a weak discriminator.** Head-to-head on a DISCOVER-FLOW/DeFACTO sub-group analysis: FFR-CT AUC **0.79** vs
  TAG **0.50** (p<0.0001) against invasive FFR. A detector built on a signal at chance level is indefensible.
- **Its incremental value is actively disputed** — including a 2020 paper titled "The transluminal attenuation
  gradient does not add diagnostic accuracy to coronary computed tomography," plus null findings for single-heartbeat
  acquisition. Interpretation is degraded by multi-beat acquisition and calcification.
- **Zero TAG papers in the 827-paper corpus** — this was found outside the collection entirely, which is itself a
  reminder that the corpus is not a systematic search.

**What survives is the principle, not the instance:** tune on target A, validate on an *independent* imaging-derived
target B. A better B would be contrast-arrival dynamics (as Thondapu 2020 optimised against) — but **ImageCAS-X is
single-phase CCTA, so contrast dynamics are not available in this dataset.** That is a hard constraint, not a
scheduling problem.

**Decision: keep the Phillips 2024 residual-whiteness/independence detector as the closing contribution.** It does not
depend on a discredited imaging signal.

**Byproduct of this sweep — see the N1 log's §3 table:** it surfaced **Korte et al. 2023** (Cardiovasc Eng Technol,
10.1007/s13239-023-00675-1), which crosses 22 independent segmentations from 26 groups with 5 outlet BC models and
concludes "segmentation fidelity has a higher influence than outlet BC choice." Intracranial aneurysms, no threshold
outcome, BCs pre-computed from geometry and never target-matched — so it does not occupy T6's ground, but it is now
the **fourth** geometry-vs-BC comparison in a non-coronary bed (with Tanade, Colebank, Sankaran 2016). Pre-empt the
reviewer line "the coronary case is incremental": none of the four has a **decision threshold**, which is precisely
where the comparison stops being academic and becomes a revascularisation decision.
