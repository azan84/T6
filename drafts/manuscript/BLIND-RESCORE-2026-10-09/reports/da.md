# Devil's Advocate Report (blind), IEEE JBHI

Manuscript: "Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study"
Reviewer persona: senior skeptic, image-based cardiovascular modelling
Inputs read: manuscript.txt, supplement.txt, ms-page-6/7 images (Figs. 2–5), RUBRIC.md

## Strongest counter-argument

The headline result, that a perfusion-matched model can still be misclassified at 0.80, follows from the structure of the problem. The model is steady, the boundary conditions are free resistances, and the fit matches flow only. A resistance fitted to flow absorbs any geometric error that affects flow, while the pressure-drop error at the stenosis remains. The authors concede this ("Matching flow alone cannot identify a geometric error, because the fitted bed absorbs it"). What the paper adds is the size of the effect, and every term in that size is set by the design: the cohort is stratified so that a third of baselines lie within ±0.05 of the threshold; the topological magnitudes are chosen as worst cases (the largest distal side branch; a break 5 mm past the measurement point); the territories are 2–3 main branches mapped by an oracle that uses the true anatomy; the throat error is a sub-voxel perturbation of an idealised concentric lesion modelled by a lumped Young–Tsai loss; and the "correct anatomy" comparator is tuned to noisy targets while the error models are tuned to noise-free ones. The ranking "topological ≈ throat >> caliber" is therefore a ranking of chosen magnitudes in a chosen flow regime, not of error classes. The one 3D case tests neither the throat error nor tuning, the two parts that carry the paper's practical message.

## Challenges

### C1. The "correct anatomy" comparator is not like-for-like (major, unanswered)
- **Claim:** "...passed models wrong by more than 0.05 in 19–20% (discrete) and 5–8% (leaky) of topological-error cases and 57–81% of throat-error cases. Other caliber errors did so in 4–18% and correct anatomy in 3–4%." (Abstract); also "against 3–4% for correct anatomy" (Conclusion).
- **Why it may fail:** The error models are tuned to error-free clean targets. The correct-anatomy floor is tuned to targets with simulated physiological noise (S9, Table S11). Noise lowers the pass rate (72% pass) and adds its own wrong models, so the two rates do not share a denominator or a target model. Noise-free correct anatomy has a residual below 1e-8 and is never wrong. Error models given the same noisy targets could show higher or lower passes-and-wrong. The 3–4% contrast is therefore not a valid baseline.
- **Answered?** Only partly. The limitation is listed ("Tuning targets were error-free clean-model flows (noise entered only the simulated floor)"), and S8 already runs error models with noisy targets for detection ("With the error models' targets carrying the same noise, the AUC..."). Passes-and-wrong is never recomputed under noisy targets, and the Abstract and Conclusion still set the two rates side by side.
- **Fix:** Recompute passes-and-wrong for T1–T5 under Protocols C and D with the same 20 noisy-target draws per instance, and report both against the floor. Otherwise, remove the "correct anatomy in 3–4%" contrast from the Abstract and Conclusion.

### C2. The class ranking is a ranking of design-chosen magnitudes (major, partly answered)
- **Claim:** "branching (topological) errors changed the decision in 32–33% of models and the half-voxel throat error in 30–36%, against 6–10% for vessel-size (caliber) errors of inter-observer magnitude away from the throat." (Abstract). Also: "Safeguards are therefore most needed at the branching near the lesion and at the throat diameter" (Conclusion).
- **Why it may fail:** T1 removes the *largest* distal side branch (median 27% of bed flow lost, discrete; Table S9). T2 cuts the vessel 25 mm past the lesion, only 5 mm past the measurement point, so in 36 discrete instances every outlet is removed. These are near-worst cases. The caliber errors are set to inter-observer averages, which the authors themselves say likely overstate agreement. The ±10-point DS throat variant flips 40–44% and the half-voxel variant 30–36%, which shows that "caliber" is not intrinsically benign. With no dose–response for the topological errors, the study cannot separate class from magnitude. "Most needed" also needs prevalence data, which the authors state was not measured ("how often current segmentation methods produce each error at a lesion was not measured").
- **Answered?** In part. The authors state: "T1 and T2 have no measured magnitude and are design choices, so the topological results are conditional on them," and "These rates hold for the magnitudes studied." The Abstract and Conclusion still state the ranking without this condition, and the "most needed" sentence goes beyond it.
- **Fix:** Plot ΔFFR (or flip probability) against the fraction of flow lost for T1, using the smallest, median and largest distal branch, and against break distance for T2 (for example 10, 25 and 50 mm past the measurement point). Add the magnitude condition to the Abstract. Change "most needed" to "most consequential per occurrence at the magnitudes tested."

### C3. The territory oracle overstates what a real perfusion check can resolve (major, unanswered)
- **Claim:** "Each corrupted node belongs to the territory of its clean counterpart." (Methods D). This underpins "With finer territories, topological concealment fell to 2–7%" (Abstract).
- **Why it may fail:** In a real perfusion-tuned twin, myocardium is assigned to territories from the segmented tree (Voronoi or nearest-vessel). A missed branch moves its myocardium to neighbouring vessels and so changes both the targets and their spatial assignment. Here the assignment uses the true anatomy, and a territory with no surviving vessel is counted as a 100% mismatch. Both choices make concealment easier to detect at finer resolution than it would be in practice. S6 shows the rule is decisive: without it, "discrete topological passes-and-wrong would have risen to 26%."
- **Answered?** No. The limitations do not mention territory assignment.
- **Fix:** Repeat C and D with territories assigned from the corrupted tree (nearest surviving vessel, applied to the clean bed weights). Report main-branch and finer results under that assignment. State the oracle as a limitation.

### C4. The 3D check does not test the claims that carry the practical message (major, partly answered)
- **Claim:** "...with a 3D computational fluid dynamics (CFD) case as a check" (Introduction). Also: "The 3D case agreed with the reduced-order result in direction." (Results D).
- **Why it may fail:** One instance, one error (T1), and two boundary conditions (A and the limit of D). There is no throat error (T5) in 3D, no Protocol C, and no vessel break. The strongest result of the study is throat concealment (57–81%), and it rests entirely on the lumped expansion loss K ∝ (A0/As − 1)²/A0² with Kt = 1.52 and Poiseuille losses along the throat. That is the regime where reduced-order models are least reliable. In the one 3D case, the cohort reduced-order model and 3D disagreed across 0.80 at baseline (0.761 against 0.870), and the error effect differed by 57% (+0.127 against +0.081).
- **Answered?** In part. The limitation states "The 3D analysis covers one instance, whose meshed lumen was wider than the reduced-order radius," and the meshed-radius counterpart is shown to agree. T5 in 3D is not addressed.
- **Fix:** Solve the same instance in 3D with the half-voxel throat narrowed and widened under Protocol A. Ideally add a second, moderate lesion (for example 60% DS, 10 mm) so that the lumped stenosis loss is checked at more than one geometry.

### C5. The flow regime in the 3D check is asserted, not justified (major, unanswered)
- **Claim:** "Steady laminar Newtonian flow ... was solved with OpenFOAM (simpleFoam) to scaled residuals below 10−5 and a steady pressure at the measurement point." (Methods E).
- **Why it may fail:** An 80% DS throat of radius about 0.23–0.28 mm carrying hyperemic LAD flow gives jet velocities of several m/s and a throat Reynolds number in the high hundreds to about 1000. Post-stenotic jets at this severity are expected to be transitional or unsteady, and SIMPLE can converge to a steady solution that is not physical, which changes pressure recovery. The finest mesh did not meet the residual limit (S10), which hints at a weakly unsteady jet. Neither the throat Reynolds number nor the jet velocity is reported, and no transient or turbulence-model check was run. The flow regime also matters for the reduced-order model: Kt = 1.52 comes from steady laminar experiments.
- **Answered?** No. Only the residual and mesh checks are given.
- **Fix:** Report the throat Re and peak velocity. Run one transient (pimpleFoam) or LES/k-ω SST check on the baseline and T1 geometries and report time-averaged FFR. State that FFR at the measurement point 20 mm downstream is insensitive to this (if it is).

### C6. The primary hyperemic demand is non-physiologically low, and the topological tuning result does not survive at higher demand (major, partly answered)
- **Claim:** "Tuning to perfusion reduced topological changes without making the models correct. Up to one in five tuned topological-error models (discrete bed; 5–8% leaky) ... passed a main-branch perfusion check while materially wrong" (Conclusion).
- **Why it may fail:** The median demand is 137 mL/min per *tree*, well below thermodilution LAD values (228–293 mL/min). The distance-map radius also sits 0.14 mm inside the meshed lumen, which lowers demand further. At twice the demand, with reselected cohorts, "the excess of tuned over re-derived passes-and-wrong was not significant in any topological comparison" (Results D; Table S5). In the leaky bed it was not significant even at baseline demand (p ≥ 0.12). By the authors' own rule ("a finding is claimed only where its direction agrees in both"), the tuned-versus-re-derived concealment of topological errors does not meet the rule for significance.
- **Answered?** In part. The Discussion states "their excess of passes-and-wrong over re-derived boundary conditions held only in the discrete bed," and the demand replication is reported. The Abstract and Conclusion do not carry these qualifiers, so "one in five" reads as a robust finding.
- **Fix:** In the Abstract and Conclusion, state that the topological concealment exceeded re-derived boundary conditions only in the discrete bed at the primary demand. Alternatively, make twice the demand the primary analysis, since it is closer to physiology, and report baseline demand as a sensitivity.

### C7. The idealised, concentric inserted lesions exaggerate how clean the throat sensitivity is (minor, partly answered)
- **Claim:** "The lesion is an axisymmetric cosine narrowing" and "a half-voxel throat error ... flipped 30–36%."
- **Why it may fail:** Real CT throat errors come mainly from calcium blooming, partial-volume effects and eccentric plaque. These errors are systematic in sign and not symmetric ±0.088 mm. Concentric, smooth lesions maximise the 1/As² sensitivity of the lumped loss. No native lesion was used as a check.
- **Answered?** In part: "The inserted stenoses are idealized" and "links between error and lesion morphology were not modeled." The reason for inserting lesions is also given ("The dataset contains few lesions near the decision threshold").
- **Fix:** Apply T5 to the native ImageCAS lesions that exist, even if there are few and they lie away from 0.80, as a qualitative check. Discuss that a systematic sign (blooming narrows the throat) would make the narrowing arm the clinically relevant one, with flips of 25–28% (Table S7).

### C8. The stratified cohort inflates every flip rate, and no reweighted estimate is given (minor, answered)
- **Claim:** "...changed the decision in 32–33% of models".
- **Why it may fail:** Six equal 0.05 bands from 0.65 to 0.95 put a third of instances in 0.75–0.85, where flips are concentrated (Fig. 2).
- **Answered?** Yes: "In this threshold-stratified cohort" (Abstract), and "Because the cohort was stratified to span 0.80, its rates are conditional on that design and are not clinical prevalences." The noise floor is computed on the same cohort, so the comparison is fair.
- **Fix (optional):** Add per-band rates reweighted to a published CT-FFR baseline distribution, so that readers can gauge clinical scale.

### C9. The radius definition in the pipeline is itself a caliber error larger than T5 (minor, partly answered)
- **Claim:** "The distance-map radius lies inside the meshed lumen (median 0.14 mm in the 3D case)."
- **Why it may fail:** The clean reference uses a radius convention offset by 0.045 mm at the throat and 0.14 mm elsewhere. In the 3D case, this convention alone moved baseline FFR across 0.80 (0.761 against 0.870). The offset is larger than the 0.088 mm half-voxel throat error, so the "correct" reference is itself convention-dependent. This supports the throat message, but it also means flips relative to the clean model depend on the convention.
- **Answered?** In part, in the limitations, where it is framed only as an effect on demand.
- **Fix:** State explicitly that the choice of radius definition is a throat-level caliber error of the same order as T5. Note that ΔFFR is computed within one convention, so flip rates are relative.

### C10. "As often as" is inferred from a non-significant test (minor, unanswered)
- **Claim:** "It flipped as often as the topological errors on the same instances (paired sign test, p = 1.0 and 0.46)".
- **Why it may fail:** Absence of a significant difference is not equivalence. Pooled T5 (two models per instance) and pooled T1+T2 (two errors per instance) are also given Wilson intervals as if independent.
- **Answered?** CIs are stated to be descriptive ("Instances are clustered within patients, so the confidence intervals are descriptive"). The equivalence wording is not addressed.
- **Fix:** Report the paired difference in flip proportion with a CI (cluster bootstrap by patient), or reword to "at similar rates (difference X, CI ...)".

### C11. Internal inconsistency on which protocol produced the fewest flips (minor, unanswered)
- **Claim:** "Re-deriving the boundary conditions (Protocol B) produced the fewest flips." (Results A).
- **Why it may fail:** In Table I, Protocol D gives fewer topological flips than B in the discrete bed (T1 2% against 9%; T2 12% against 18%; pooled 8% against 14%, Table S6).
- **Answered?** No.
- **Fix:** Write "the fewest flips among Protocols A–C," or state that D gave fewer flips by construction of its targets.

### C12. Minor numerical and figure points (minor)
- Cohort-model Protocol D ΔFFR for the 3D instance (−0.0007) is identical to the 3D value (−0.0007). Please confirm that this is not a transcription error.
- The Abstract cites tree-level DSC ("0.97, as high as a taper"), but Fig. 4 plots whole-scan DSC (0.985 against 0.983). Use the same level throughout.
- Table I footnote: the passes-and-wrong denominators (60, 100) differ from the n column. Add a separate n column for passes-and-wrong.
- Topological flip ranges differ by section: "5–19%" (Abstract, pooled B–C), "2–20%" (Discussion, per type B–D) and "5–18%" (Conclusion, per type B). Use one basis.
- The Bayesian model used variational inference with ±1.96 SD intervals. VI is known to under-cover; report a check with MCMC or a bootstrap.

### Challenges already answered (not counted as weaknesses)
- Clustering within patients and the descriptive CIs; mixed-effects model provided (S3).
- Threshold choice for the perfusion check, with 13% and 16% sensitivities (Table S3).
- Mesh convergence of the 3D case (S10), with discretisation uncertainty about 0.002 against an effect of 0.074.
- Protocol D passes everything by design: stated ("Per-territory tuning passes almost every model by design"; Table S3 footnote).
- The non-identifiability is acknowledged as structural, and the contribution is framed as quantification at the decision level.
- The practical considerations are explicitly hedged: "These considerations are not validated decision rules."
- The perfusion-tuning claim is framed as calibration evidence rather than validation evidence, which is consistent with in silico credibility norms [33].

## Rubric scores

| Code | Dimension | Score | Status | Justification |
|------|-----------|-------|--------|---------------|
| S1 | Novelty and contribution | 7 | pass | Decision-level ablation crossed with fixed, re-derived and tuned BCs is new; the core non-identifiability is near-tautological, so the novelty lies in quantification. |
| S2 | Methodological rigour | 6 | warn | Paired design, two beds, demand replication and floors are strong; there is an asymmetric noise comparator (C1), an oracle territory map (C3) and no topological dose–response (C2). |
| S3 | Claims supported by evidence | 6 | warn | Many hedges are present, but the Abstract and Conclusion keep the 3–4% contrast, the class ranking and "one in five" without the bed/demand qualifiers (C1, C2, C6). |
| S4 | Domain and physiological accuracy | 6 | warn | Low primary demand; steady laminar 3D at an 80% DS jet with no Re or transient check (C5); idealised concentric lesions; T5 relies on a lumped loss. |
| S5 | Internal consistency | 8 | pass | Abstract, Table I and supplement numbers cross-check; minor slips ("B fewest flips", DSC level, range bases, one suspicious repeated value). |
| S6 | Clarity, structure and readability | 6 | warn | Precise but very dense; the Abstract is overloaded with ranges; Table I footnote denominators are hard to follow. |
| S7 | Venue fit (JBHI) | 7 | pass | Segmentation-metric adequacy and digital-twin calibration credibility fit JBHI; the health-informatics angle is clear. |
| S8 | Reproducibility and transparency | 8 | pass | Public data, open code, fixed seed, full pipeline, exclusions table and solver and mesh settings. |

## Overall

**Overall: 6.5 / 10. Recommendation: major revision.**

The work is careful and unusually transparent, and most of the obvious attacks are pre-empted in the text. The remaining weaknesses all concern the comparisons that carry the headline. The correct-anatomy baseline is tuned under different conditions from the error models (C1). The topological-versus-caliber ranking depends on chosen magnitudes (C2). The finer-territory rescue assumes an oracle territory map (C3). The throat result, which is the most clinically consequential, has no 3D or flow-regime check (C4, C5). Each can be fixed with modest extra computation on the existing pipeline.
