# Devil's Advocate report (blind, IEEE JBHI)

Persona: senior skeptic, image-based cardiovascular modelling. Sources read: manuscript.txt, supplement.txt, ms-page-6/7 images (Figs. 2-4), RUBRIC.md. Nothing else opened.

## Strongest counter-argument (one paragraph)

The headline "a perfusion-matched model can be wrong" is close to an identifiability tautology: a check made of two territory flows (subtrees below the first bifurcation, i.e. essentially LAD-vs-LCx) cannot see how flow is redistributed *within* a territory, so any error that reroutes flow inside a territory must be able to pass it, and the paper's 19-20% rate is mostly a function of how coarse that check is, how large the design-chosen topological errors are, and how the cohort was stratified around 0.80. The second headline, "topological errors matter more than caliber errors", is robust only under Protocol A (fixed resistances, which the authors themselves frame as the idealised case), compares worst-case-by-design topological errors (the *largest* distal side branch; a break 25 mm past the lesion) against caliber errors set at an inter-observer magnitude the authors admit "likely overstate[s] agreement", and is never placed on a common scale (no overlap metric of the topological perturbations is reported). The paper's own 3D case undercuts the ranking: a radius-definition difference of 0.045 mm at the throat moved baseline FFR from 0.761 to 0.870, larger than any topological effect reported. Finally, in the leaky bed (arguably the more physiological bed, since it represents unresolved side branches), tuned topological passes-and-wrong (5-8%) is barely distinguishable from the correct-anatomy floor (3.1-3.9%), and at doubled demand the excess over re-derivation was "significant ... in no topological" comparison. What remains is a well-executed existence proof plus conditional rates, which is publishable, but the abstract and conclusion read as if more were shown.

## Challenges

### C1. Coarse territory definition drives passes-and-wrong (MAJOR, unanswered)
- Attacked: "A perfusion territory is the subtree below each child of the first bifurcation of the clean tree." and abstract "tuned models still passed a perfusion check stricter than measurement repeatability while wrong by more than 0.05: 19-20% (discrete bed)".
- Why it may fail: For the left tree this is two territories (LAD vs LCx); clinical perfusion imaging resolves the AHA 17-segment level, and the cited digital-twin approach [8] tunes at much finer resolution. A missed diagonal inside the LAD territory is invisible to a two-territory check by construction. The paper calls the check "stricter than measurement repeatability", but strictness in magnitude is not strictness in spatial resolution. The rate of passes-and-wrong is therefore a property of the chosen granularity, not of "perfusion tuning" in general. The RCA exclusions (Protocols C/D undefined for "most right coronary instances") follow from the same definition.
- Answered? Partly. The paper notes the fit is over-determined (C) or exactly determined (D) and that D "passes almost every model by design", and limitations state the RCA restriction. It never discusses territory granularity or shows how passes-and-wrong changes with finer territories.
- Fix: Repeat C/D with finer territories (e.g., subtree below every branch of radius > 1 mm, or a segment-level mapping), report passes-and-wrong vs number of territories; state explicitly in abstract that the check is at the main-territory level.

### C2. Caliber vs topology ranking rests on non-commensurate magnitudes (MAJOR, partly answered)
- Attacked: "With fixed boundary conditions, branching (topological) errors changed the decision in 32-33% of models, against 6-10% for vessel-size (caliber) errors of inter-observer magnitude." / Conclusion: "missed branches and vessel breaks changed the decision three to six times as often as caliber errors of inter-observer size."
- Why it may fail: T1 deletes "the largest side branch that leaves the host vessel beyond the lesion" (worst case by construction); T2 truncation at 25 mm is arbitrary; T4 converts a whole-test-split DSC (dominated by large proximal lumen) into a uniform 0.930 radius ratio, which is not the local throat error that drives FFR-CT error clinically (blooming, calcium, partial volume at the minimum lumen). No dose-response in caliber magnitude is given, so the ranking could invert at realistic throat errors. Overlap metrics of the T1/T2 corrupted masks are not reported, so the claim that these errors are equally "small" by the usual metrics is untested.
- Answered? Partly: "T1 and T2 have no measured magnitude and are design choices, so the topological results are conditional on them"; "This ranking holds for the magnitudes studied"; limitations: caliber magnitudes "likely overstate agreement". The abstract carries no such qualifier.
- Fix: (i) caliber dose-response (e.g., T4 at 0.90/0.85, throat-only DS error +-5/10 points); (ii) report DSC/HD95/clDice of every corrupted mask vs clean, and compare error classes at matched DSC; (iii) T1 with a random (not largest) distal branch; (iv) add "for the magnitudes studied" to the abstract sentence.

### C3. The paper's own 3D case shows a caliber-definition effect larger than the topological effect (MAJOR, unanswered in its implication)
- Attacked: "The meshed lumen was wider than the radius used by the reduced-order model (median difference 0.14 mm; throat area-equivalent radius 0.276 against 0.231 mm), and on the reduced-order radius the baseline was 0.761."
- Why it may fail: A 0.045 mm throat-radius difference (radius definition alone: distance-to-nearest-background-voxel vs marching-cubes surface) moved FFR by 0.109 and across 0.80, larger than the T1 effect (+0.074 to +0.127). This is direct evidence that small caliber differences at the throat dominate, contradicting the ranking in C2, and suggests the distance-transform radius is systematically biased low across the entire cohort (which also lowers demand via k r_in^3 and deepens every lesion).
- Answered? Limitations note the offset "moved the baseline across 0.80 ... but not its direction or its removal by prescribed flows". The consequence for the caliber-vs-topology ranking and for systematic radius bias is not addressed.
- Fix: Discuss explicitly; run the cohort with a sub-voxel radius (e.g., +0.5 voxel correction or surface-based radius) as a sensitivity and report whether flip rates and the ranking change.

### C4. In the leaky bed the central passes-and-wrong finding is near the noise floor (MAJOR, partly answered)
- Attacked: Abstract: "19-20% (discrete bed) and 5-8% (leaky bed) of topological-error models ... against 3-4% for correct anatomy"; "The directions held at doubled and, in the leaky bed, tripled demand."
- Why it may fail: Leaky D = 5% (3-10) overlaps the floor 3.9% (3.2-4.6); Table I leaky passes-and-wrong under tuning was not higher than B ("but not in the leaky bed (p >= 0.12)"); Table S5 leaky 3x: D 4% vs B 4% (a tie, not a held direction); at 2x "significant ... in no topological one". The floor is also computed with noisy targets and Protocol C only, while corrupted models get error-free targets, so the comparison is asymmetric. The leaky bed, designed to represent unresolved side branches, is plausibly the more physiological of the two.
- Answered? Partly: "their excess of passes-and-wrong over re-derived boundary conditions held only in the discrete bed"; "Tuning targets were error-free clean-model flows (noise entered only the simulated floor)."
- Fix: In abstract/conclusion, state the topological excess is shown in the discrete bed only; replace "directions held" with the exact statement; run corrupted models with the same noisy targets as the floor (and a D-floor) so comparisons are like-for-like; argue which bed is closer to physiology.

### C5. Headline topological ranking is essentially a Protocol A result (MINOR, answered)
- Attacked: title framing and "the decision risk of segmentation lay mainly in the branching structure".
- Why: Under B leaky the class difference was not significant (p = 0.18), under C leaky p = 0.057, under D "the two classes flipped at similar rates". Protocol A is acknowledged as an idealised case.
- Answered: Yes, the sentence opens "With fixed boundary conditions", and Results report non-significance. Residual issue: Implications ("First, check that the side branches...") is stated without this conditioning. Fix: one clause in Section IV-C.

### C6. Flow regime and lesion-FFR plausibility (MINOR, largely answered)
- Attacked: 3D case "20 mm lesion of 80% DS in the proximal LAD" with FFR 0.870; median demand 137 mL/min.
- Why: An 80% DS, 20 mm proximal LAD lesion with FFR 0.87 implies sub-physiological flow; the 0.80 decision is then applied to lesions that would be far lower clinically. At higher flow the throat Reynolds number makes steady laminar 3D assumptions (simpleFoam laminar) questionable.
- Answered: Largely, by the k x2 and x3 reselected-cohort replication (Table S5) and the stated limitation. Not answered: the 3D case was run at primary demand only, and no throat Reynolds number or transition check is reported. Fix: report throat Re for the 3D case; caption of Fig. 4 should not say the shift "would move a decision near 0.80" (0.870 -> 0.944 never crosses 0.80).

### C7. Single 3D case (MINOR, answered)
- Attacked: "in one three-dimensional case it reduced a shift of 0.074 to -0.0007".
- Answered: framed as a case study and "check" with caveats in Limitations and Section S7. Residual: the 3D case tests only A vs D-limit, not the passes-and-wrong phenomenon or Protocol C; its inclusion in the abstract gives it more weight than one instance merits. Fix: move the number out of the abstract or label it "one illustrative case".

### C8. Idealised inserted lesions, independence of error and lesion (MINOR, partly answered)
- Attacked: "an axisymmetric cosine narrowing ... The vessel was never widened"; errors applied after lesion insertion.
- Why: Real segmentation error is correlated with lesion morphology (eccentricity, calcium blooming, positive remodelling); inserting smooth lesions into healthy segments and then perturbing independently removes exactly the correlation that matters most for FFR-CT.
- Answered: "The inserted stenoses are idealized"; "Errors were applied one at a time in one dataset." Correlation is not discussed. Fix: one sentence acknowledging error-lesion correlation as untested.

### C9. "Overlap metrics do not measure" these errors is asserted, not measured (MINOR-MAJOR, unanswered)
- Attacked: "the error types that carried the decision risk here are the ones that the usual overlap metrics do not measure"; Implications "because overlap scores do not reveal these errors".
- Why: The study never computes DSC/HD95 for T1/T2; deleting the largest side branch plus subtree may change DSC appreciably. The supporting evidence is cited [18], not shown.
- Fix: report overlap metrics of every corrupted mask (ties to C2).

### C10. Statistical inference on clustered data (MINOR, partly answered)
- Attacked: McNemar/sign/Wilcoxon p-values across many cells.
- Why: Instances clustered within patient/tree; many tests with Holm only within each cell; the Bayesian model covers flips under A-C only (not passes-and-wrong, not D) and uses variational intervals that typically understate posterior width.
- Answered: "the confidence intervals are descriptive"; mixed model agrees. Fix: cluster bootstrap by patient for the passes-and-wrong contrasts; state VI limitation.

### C11. Prescriptive abstract ending (MINOR, partly answered)
- Attacked: "branching and caliber should be checked before tuning."
- Answered in body: "These considerations follow from the results but are not validated decision rules." The abstract lacks this hedge and proposes no check method. Fix: "...suggest checking branching and caliber before tuning".

### C12. Unverifiable figure (MINOR)
- "After one global scaling, about half of the models that passed were materially wrong." Pass rates under C for topological errors are not tabulated in main text or supplement. Fix: give the n/N.

## Rubric scores

| Code | Dimension | Score | Status | Justification |
|---|---|---|---|---|
| S1 | Novelty and contribution | 7 | pass | First paired A/B/C/D protocol comparison on identical corrupted anatomy with a passes-and-wrong metric; core insight is partly an identifiability expectation (C1). |
| S2 | Methodological rigour | 6 | warn | Careful ablation, two beds, demand replication, floors, convergence and mesh checks; but coarse territories, worst-case topological vs single caliber magnitude, asymmetric floor comparison (C1, C2, C4). |
| S3 | Claims supported by evidence | 6 | warn | Body is well hedged; abstract/conclusion overstate leaky-bed and demand robustness and ranking generality (C2, C4, C11); Fig. 4 caption overreach. |
| S4 | Domain / physiological accuracy | 6 | warn | Reasonable 0D model and Murray/Choy-Kassab beds; low hyperemic flow, implausible lesion-FFR pairing, radius bias (C3, C6). |
| S5 | Internal consistency | 8 | pass | Abstract, Table I, Tables S3-S7 and text ranges cross-check; one untabulated claim (C12). |
| S6 | Clarity, structure, readability | 7 | pass | Clear definitions and plain-language glosses; protocol/bed/error combinatorics dense, many ranges per sentence. |
| S7 | Venue fit (JBHI) | 6 | warn | Fits digital-twin/credibility thread; little informatics deliverable (no QC tool or topology metric proposed). |
| S8 | Reproducibility and transparency | 6 | warn | Public data, seed, solver details, exclusions table; code only "upon reasonable request". |

Overall: 6.4 / 10

Recommendation: major revision. The existence result and the protocol comparison are sound and of interest; the paper needs (1) a territory-granularity sensitivity, (2) caliber dose-response and overlap metrics for all perturbations so the ranking is on a common scale, (3) like-for-like noisy targets for corrupted models, and (4) abstract/conclusion wording restricted to what holds in both beds and at all demands.
