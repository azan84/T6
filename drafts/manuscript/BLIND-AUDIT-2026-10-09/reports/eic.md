# Referee report: Associate Editor, IEEE JBHI (Computational and in silico medicine / digital twins)

Manuscript: "Topological Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study" (main text 8 pp, supplement 6 pp)

## Summary

The authors insert idealized stenoses (150 instances, 108 trees, 93 patients from ImageCAS-X) and apply one segmentation error at a time. Two errors are topological (missed side branch T1, vessel break T2) and two are caliber errors of inter-observer magnitude (lesion length T3, taper T4). FFR is recomputed with a steady reduced-order network model under four outlet boundary-condition protocols: fixed (A), re-derived (B), globally tuned to clean territory flows (C) and per-territory tuned (D). Two microvascular-bed structures are used (discrete and leaky), and one 3D CFD case serves as a check. With fixed BCs, topological errors flip the 0.80 decision 3–6 times as often as caliber errors. Tuning to perfusion reduces the flips, but 19–20% (discrete) and 5–8% (leaky) of tuned topological-error models, and up to 18% of tuned taper models, pass a perfusion check while |ΔFFR| > 0.05. The authors conclude that a perfusion match does not certify the computed FFR. The question matters for perfusion-calibrated coronary digital twins and the bookkeeping is very careful. The weaker points are the design-chosen size of the topological errors, an asymmetric noise model in the key passes-and-wrong comparison, a health-informatics contribution that is left implicit, and code that is available only on request.

## Strengths

1. **Clear, well-posed ablation design.** Each corrupted model is paired with its own clean model, so ΔFFR is attributable to one error and one BC protocol. Judging error at the 0.80 decision, against a repeat-FFR noise floor ([30], [31]), is clinically more meaningful than the continuous sensitivity indices used in [10]–[16].
2. **Four BC protocols on the same corrupted anatomy.** The comparison of fixed, re-derived and two tuned protocols (with C deliberately over-determined and D exactly determined) is new. It also reconciles [20] and [21] convincingly (Sec. IV-B): the BC protocol alone can produce both behaviours.
3. **Robustness by design.** Two bed structures, with a claim made only where the direction agrees in both. There are also two demand-replication cohorts re-selected at 2x and 3x k (Table S5), a ±30% demand sensitivity (Table S4), perfusion-threshold sensitivities (Table S3), grey-zone analysis (Table S6) and a simulated physiological floor (Table S7).
4. **Exemplary numerical bookkeeping.** I reconciled the solve counts and they add up exactly. The 2 802 defined A–C models are 3 x (77+96+97+97) + 3 x (118+149+150+150). The 203 unsolved models equal the Table S1 exclusions (33+36+36+47+2+49). The 769 Protocol D solves are 298+471. The noise-floor draws are 1 940 + 2 990 = 4 940 − 10 failures. Convergence and mass-conservation errors are reported, and the mesh study with its failed acceptance criterion is disclosed honestly (Table S8).
5. **Honest scoping.** Rates are stated as conditional on the threshold-stratified design, T1/T2 magnitudes are called design choices, and the limitations (Sec. IV-D) are specific rather than generic.
6. **Within the page budget.** The paper is 8 + 6 = 14 pp, the abstract is 250 words, the index terms are in alphabetical order and the references follow IEEE style.

## Weaknesses

**W1 (major): the topological-vs-caliber ranking rests on topological magnitudes that the authors chose and that sit at the severe end.**
Evidence: "T1 and T2 have no measured magnitude and are design choices" (Sec. II-C). T1 deletes "the largest side branch that leaves the host vessel beyond the lesion" and T2 truncates at a single 25 mm distance. The caliber errors, by contrast, are set to inter-observer statistics that are themselves typical rather than worst-case. The headline "three to six times as often" (Abstract, Sec. IV-A, Conclusion; recomputed 45/137 = 32.8% vs 20/194 = 10.3% discrete, 84/265 = 31.7% vs 17/300 = 5.7% leaky) therefore compares a severe topological error with a typical caliber error.
Fix: Add a dose-response sweep for T1 (largest, median and smallest resolvable distal branch, or branch-flow share as a continuous covariate) and for T2 (for example 10/25/50 mm). Report flip rate against the deleted bed fraction. Better still, derive empirical T1/T2 frequencies from the outputs of the segmentation methods benchmarked in ImageCAS-X [18], which the authors cite as producing vessel breaks. State the ranking per unit of lost bed flow, not per error type.

**W2 (major): the key passes-and-wrong comparison is asymmetric, and under Protocol D the check is uninformative by construction.**
Evidence: "Tuning targets were error-free clean-model flows (noise entered only the simulated floor)" (Sec. IV-D). The 19–20% topological rate (noise-free targets) is set against "3–4% for correct anatomy" (Table S7, noisy targets) in the Abstract and Conclusion. Under D, "Protocol D residuals lie below 0.01" (Fig. 3 caption), so passes-and-wrong under D is simply the materially-wrong rate. The phrase "a perfusion check stricter than measurement repeatability" adds nothing for D. Against the proper comparator (B), the topological excess is not significant in the leaky bed ("p ≥ 0.12", Sec. III-B). At 2x demand it is "significant ... in no topological one" (Sec. III-E).
Fix: Run the corrupted models with the same 20 noisy target draws used for the floor, so that error and floor share one noise model. Report passes-and-wrong under D as "residual error after exact flow matching". In the abstract, state that the topological excess over re-derived BCs holds in the discrete bed only.

**W3 (major): the health-informatics contribution is implicit, and a usable detector that the data could support is not evaluated.**
Evidence: The practical output is four qualitative "considerations ... not validated decision rules" (Sec. IV-C). The third ("record the perfusion mismatch before tuning") is undercut by the authors' own figure: "in the leaky bed most did [pass]" (89%, Sec. III-A).
Fix: The authors already hold every number needed for a quantitative QC result for JBHI readers. Report the ROC/AUC, sensitivity and specificity of the pre-tuning (Protocol B) perfusion residual, and of a simple topology check (for example distal outlet count or bed-fraction loss relative to an atlas), as detectors of a decision-changing segmentation error, per bed. A clDice- or Betti-number-type metric computed on the corrupted trees [32] against flip outcome would also tie the work to the segmentation-informatics audience. Without this, the paper fits IJNMBE or Ann Biomed Eng better than JBHI.

**W4 (major): the code is available only on request, for a fully automated pipeline built on public data.**
Evidence: "The code is available from the corresponding author upon reasonable request." The supplement states "every instance ... is solved in one automated run ... and every table and figure is generated from its output" (Sec. S1), and the seed is given (20260918).
Fix: Deposit the reduced-order solver, the lesion-insertion and error-injection scripts, the cohort list (scan IDs, host vessel, c, L, DS) and the OpenFOAM case files in a public archive with a DOI, and cite it in the Data and Code Availability section. This is the cheapest and most valuable change for a digital-twin credibility paper that cites [33].

**W5 (major): the perfusion-territory definition is coarse and unphysiological, so tuning results for the RCA are effectively missing.**
Evidence: "A perfusion territory is the subtree below each child of the first bifurcation of the clean tree" (Sec. II-D). Protocols C/D were "undefined for 33 of 77 (discrete) and 47 of 118 (leaky) missed-branch instances and for 36 of 96 and 49 of 149 vessel breaks, all but four in the RCA". Clinical perfusion data (CTP, PET, CMR; [8], [28], [29]) are regional, mapped to the AHA segments or to voxels via vessel-to-myocardium (Voronoi) assignment. They are not defined by first-bifurcation subtrees.
Fix: Repeat C/D with territories defined by a myocardial-segment or Voronoi mapping (or at minimum the 3-vessel or 17-segment level), so that the RCA is included. Alternatively, restrict all tuned-protocol claims explicitly to the left coronary tree in the abstract, not only in Limitations.

**W6 (minor): the radius definition and the demand are biased low, which shifts the cohort.**
Evidence: The radius is "the Euclidean distance from the point to the nearest background voxel", and "the meshed lumen was wider than the radius used by the reduced-order model (median difference 0.14 mm; throat area-equivalent radius 0.276 against 0.231 mm)". That throat difference is 44% in area and roughly a 2x difference in Poiseuille throat resistance. It also moved the 3D-case baseline from 0.870 to 0.761, across 0.80. Median demand is 137 mL/min per tree (Sec. II-B).
Fix: Apply a sub-voxel (half-voxel) radius correction, or quantify its effect on the cohort's baseline-FFR distribution and flip rates in one sensitivity run. The demand replication (Table S5) partly addresses flow, but not the resistance bias.

**W7 (minor): the 3D case validates direction only, and its two baselines are not explained.**
Evidence: The baseline is 0.870 with fixed resistances but "0.892 in both geometries" with prescribed flows (Sec. III-D). The Fig. 4 caption says the shift "would move a decision near 0.80", yet neither 3D value is near 0.80.
Fix: Explain why the prescribed-flow baseline differs (presumably the targets come from the narrower reduced-order radius). Reword the caption to state that no decision changed in this instance. Present the case as a fidelity check of direction, not of magnitude.

**W8 (minor): the headline flip rates depend on the stratified design, but the first abstract result is not qualified.**
Evidence: "With fixed boundary conditions, branching (topological) errors changed the decision in 32–33% of models" appears before the qualifier "In this threshold-stratified cohort". The authors state that the rates "are not clinical prevalences".
Fix: Move the qualifier before the first rate. Also report a reweighted estimate (bands weighted to a published distribution of clinical CT-FFR or invasive FFR) or make the distribution of |ΔFFR| per error type the primary metric.

**W9 (minor): figure and table inconsistencies.**
(a) The Fig. 3 caption says "Protocol D residuals lie below 0.01", but Sec. S2 reports two Protocol D models with "perfusion residuals of 0.08 and 0.11".
(b) Table I has a single n column, but the passes-and-wrong denominators differ for T2 (60 under B discrete; 100 under A/B leaky). The same quantity (topological passes-and-wrong under B, discrete) appears as 1% in Table S3 (n = 137), 1% in Table S5 (n = 173, undefined residuals counted as failures) and 2% in Sec. III-B (n = 104). I recomputed all three as 2 models, so they are consistent but confusing.
(c) The page-1 "LOGO" placeholder overlaps the running head in both PDFs.
(d) The tick and legend fonts in Figs. 2–4 and S3 appear smaller than IEEE's 8 pt minimum at print size.
(e) The IEEE first footnote lacks a funding statement.
Fix: Correct the Fig. 3 caption. Add a separate "n (P&W)" column to Table I and use a single denominator convention throughout. Remove the placeholder, enlarge the fonts and add funding.

**W10 (minor): statistics.**
Evidence: The mixed-model intervals are "posterior mean ±1.96 posterior standard deviations from the variational approximation" (Table S2). Mean-field VI is known to understate posterior variance. Protocol D is absent from the model. Dozens of p-values are reported, with Holm adjustment only within triplets.
Fix: Refit with MCMC (or at least report a VI-vs-Laplace check), include D, and state the family-wise testing scope.

**W11 (minor): positioning and references.**
Evidence: For coronary flow-split tuning the authors cite [9], a pulmonary-valve FSI paper ("tuned so that the model reproduces ... measured flow splits [9]"). There is no engagement with identifiability or Bayesian calibration of coronary lumped-parameter BCs (for example the Marsden group's multifidelity UQ work, Fleeter et al., CMAME 2020), even though the central finding is a non-identifiability: flow-only calibration cannot reveal a geometric error.
Fix: Replace or supplement [9] with a coronary flow-split or perfusion-calibration reference. Add a short paragraph that frames passes-and-wrong as an identifiability result and states what is new beyond that expectation, namely its decision-level size and its dependence on error type and bed.

## Rubric scores

| Code | Dimension | Score | Status | Justification |
|---|---|---|---|---|
| S1 | Novelty and contribution | 6 | warn | Decision-level, protocol-paired ablation is new, but the core result (flow-only tuning cannot certify geometry) is close to an expected non-identifiability, and its size depends on the chosen T1/T2 severity (W1, W11). |
| S2 | Methodological rigour | 6 | warn | Numerics, pairing and robustness checks are strong; asymmetric target noise (W2), coarse territories (W5), design-chosen topological magnitudes (W1) and VI intervals (W10) weaken inference. |
| S3 | Claims supported by evidence | 6 | warn | The "stricter than repeatability" framing is uninformative under D. The topological excess over B is not significant in the leaky bed or at 2x demand. Recommendation 3 fails in the leaky bed. The first abstract rate is unqualified (W2, W3, W8). |
| S4 | Domain / physiological accuracy | 7 | warn | The FFR definition, hyperemia, scaling laws and noise floor are sound. First-bifurcation territories, the low-biased distance-map radius and low demand are physiological weak points (W5, W6). |
| S5 | Internal consistency | 8 | pass | Every recomputed count, percentage and Wilson interval reconciles (2 802/2 599/769/4 940; 45/137, 20/194, 84/265, 17/300, 20/104, 21/104, 14/171, 9/171, 9/194, 35/194, 37/300, 12/300). Only the Fig. 3 caption vs S2 conflict and the mixed denominators remain (W9). |
| S6 | Clarity, structure and readability | 7 | pass | Logical IEEE structure and precise definitions; the abstract and Sec. III are very dense with ranges across 2 beds × 4 protocols × 4 errors, and Table I's single n column is confusing. |
| S7 | Venue fit (JBHI) and HI relevance | 6 | warn | The digital-twin credibility framing fits the track, but there is no informatics deliverable (detector, QC metric or tool). As written it fits IJNMBE or ABME better (W3). |
| S8 | Reproducibility and transparency | 5 | warn | Public data, fixed seed, full exclusion accounting and an automated pipeline, but the code is on request only and the cohort list and CFD cases are not deposited (W4). |

**Overall: 6.4 / 10**

**Recommendation: Major revision.** The study is careful and the question is relevant to perfusion-calibrated coronary digital twins. Most of the requested changes (W2 noisy-target rerun, W3 detector ROC, W4 code deposit, W1 magnitude sweep) can be made with the authors' existing automated pipeline and do not need new data. With W1–W4 addressed, I would expect the paper to be acceptable for JBHI.
