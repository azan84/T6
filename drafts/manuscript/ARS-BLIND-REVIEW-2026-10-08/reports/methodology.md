contract_role: methodology

## Dimension Scores

### D1: methodology_rigor
score: warn
trigger: "Methods are sound in principle but incompletely reported"

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: block
trigger: "the abstract states a stronger or differently directed effect than the reported statistics support"
block_class: repairable

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

The manuscript reports a paired in silico ablation: 150 inserted stenoses in 108 ImageCAS-X trees, four segmentation error types, three boundary-condition protocols (fixed, re-derived, one-parameter tuned to clean territory flows) in two microvascular bed structures, plus one 3D CFD case. I recomputed the internal arithmetic. The flip counts reconcile across the text and Table I (for example, 45/137 discrete topological flips under Protocol A = 21 missed-branch + 24 vessel-break; 14 of 21 missed-branch flips reversed under B leaves 7/77 = 9%). The Wilson intervals I checked reproduce (45/137 gives 25.5–41.1%; 20/104 gives 12.8–27.8%; 36/150 gives 17.9–31.4%). The Holm-adjusted exact McNemar p-values in Section III reproduce exactly from the reported discordant counts (raw two-sided 0.050 for 22 vs 10, times 3, gives 0.15; raw 0.121 for 22 vs 12, times 2, gives 0.24; raw 0.125 for 4 vs 0, times 2, gives 0.25). The 2 599 solved-model total reconciles with Table I and Table S1. The core ablation is therefore well executed and transparently reported.

My concerns are about inference rather than arithmetic. (i) The 3D case, presented as confirming concealment, shows that per-outlet flow prescription removes the FFR error, which by the paper's own definition is not concealment. (ii) The one-parameter tuning is described as the least flexible and implicitly conservative choice, but the pass-while-wrong rate is not monotone in tuning flexibility. (iii) The attribution of concealment to tuning does not hold against fixed boundary conditions in the leaky bed, where the leaky-bed tuned rate also sits close to the simulated noise floor. (iv) Caliber error under tuning produces the largest pass-while-wrong cell in Table I, which contradicts the "minor risk" guidance. (v) The protocol comparisons in Table I and the abstract mix instance sets. (vi) The hyperemic demand and radius definition appear to put the cohort at sub-physiological flow, and the 3D twin verifies the model at a different radius from the one used for the cohort. Each issue is repairable with analyses the existing pipeline can run.

### S1: Paired ablation isolates the error-by-protocol factor
Each corrupted model is compared with the same instance's clean model in the same bed, so ΔFFR, flips and residuals are within-instance contrasts. Segmentation error and boundary-condition handling are crossed rather than confounded, and the reference is used only as a counterfactual. It is not offered as a validation of model accuracy, so the design is not circular.
**Evidence Anchor**: text: §I "The correct (clean) model of each tree serves as the reference"

### S2: Paired tests with multiplicity control, verified on recomputation
Protocol contrasts use exact McNemar tests within instance with Holm adjustment per error type and bed, and the reported p-values reproduce from the stated discordant counts. Directional claims are restricted to effects that agree in both beds, which is a sensible replication rule for a two-model-structure design.
**Evidence Anchor**: text: §II-F "tested with the exact McNemar test, with Holm adjustment"

### S3: Two explicit noise floors, including a simulated physiological floor
Besides the repeat-FFR floor (SD 0.018), the authors simulate correct anatomy tuned to noisy perfusion. This gives an empirical null for both flip rate (6.2%, 7.2%) and pass-while-wrong rate (3.1%, 3.9%). Few CT-FFR sensitivity studies provide such a floor.
**Evidence Anchor**: table: Table S5 — flip 6.2 (5.2–7.3) and 7.2 (6.3–8.2); pass-and-wrong 3.1 (2.4–4.0) and 3.9 (3.2–4.6)

### S4: Complete exclusion accounting
Every excluded cell is listed with its reason and count. The solved counts reconcile with Table I and with the 2 599 total (2 964 possible models minus 365 exclusions).
**Evidence Anchor**: table: Table S1 — Solved and Excluded (reason: count) columns for T1 and T2 in both beds

### S5: Correct Wilson intervals on headline proportions
The headline proportions carry Wilson intervals that recompute correctly.
**Evidence Anchor**: text: §III-A "45 of 137 topological-error models (33%, 95% CI 26–41%)"

### S6: Honest reporting of a falsified expectation and of a failed mesh criterion
The authors state that tuning reduced flips, contrary to their expectation. They also report that the throat-refinement test missed their own acceptance criterion and that one variant did not reach the residual limit, instead of omitting either result.
**Evidence Anchor**: text: §III-B "We had expected tuning to leave the flip rate at or above that of fixed boundary conditions."

### W1: The 3D case shows correction, not concealment, under prescribed flows
**Problem**: Section II-D defines concealment as tuning that removes the error "from the perfusion check but not from the FFR". In the 3D case, prescribing clean territory flows gives a perfusion residual of zero by construction and changes FFR by −0.0007. The reduced-order twin gives −0.0005. Fig. 5f shows the two pressure traces overlapping. The error is therefore removed from both the check and the FFR. Yet §III-D opens "The 3D solution showed the same concealment", §IV-A says the 3D case "showed the same mechanism", and the Conclusion states "A three-dimensional case reproduced this concealment". In the reduced-order discrete bed, which the paper says matches 3D outlets, one-scaling tuning kept 84% of the shift. The 3D result contradicts that, because the 3D used a different, more flexible protocol (per-outlet flow prescription).
**Evidence Anchor**: text: §III-D "The 3D solution showed the same concealment."
**Why it matters**: The 3D case is advertised in the Introduction as confirming the mechanism and appears in the abstract and Conclusion. As reported, it supports the opposite reading: with per-territory flow matching, a missed branch distal to the lesion does not produce a material FFR error.
**Suggestion**: Reframe the 3D result as showing that per-outlet flow prescription restores FFR for a distal missed branch, while fixed resistances do not. Remove "same concealment" from §III-D, §IV-A, the abstract and the Conclusion. To test concealment in 3D, run the 3D case under a one-global-scaling condition equivalent to reduced-order Protocol C, or use a case where some redistributed territory flow exits proximal to the lesion.
**Severity**: Major
**Confidence**: 5 — core expertise: coronary boundary-condition modelling; follows directly from the reported numbers

### W2: The one-parameter tuning is not a conservative choice for the pass-while-wrong outcome
**Problem**: Protocol C fits a single global scaling of C to two or more territory targets. The paper calls this "the least flexible tuning a pipeline could use" and treats the 10% threshold as conservative. But tuning flexibility moves the two components of "passes and wrong" in opposite directions. More flexible tuning (per-territory or per-outlet scaling, as in perfusion-personalised pipelines) increases the pass rate. It also restores flow through the lesion and so reduces |ΔFFR|. The 3D per-outlet result (ΔFFR −0.0007) is the limiting case: 100% pass, 0% wrong. The reported 8–19% concealment is therefore specific to an under-parameterised fit, and its direction of bias relative to realistic pipelines is unknown.
**Evidence Anchor**: text: §II-D "so this is the least flexible tuning a pipeline could use"
**Why it matters**: The headline claim, "A perfusion-matched coronary model can thus pass validation with a material error", generalises to perfusion-matched models in general. The design tests one tuning parameterisation, and that parameterisation determines the outcome.
**Suggestion**: Add a Protocol C′ with one scaling per territory (and, if feasible, per-outlet flow prescription in the reduced-order model). Report pass, wrong and pass-and-wrong rates for each. Characterise when residual error survives flexible tuning, for example when redistributed territory flow exits proximal to the lesion. Restrict the abstract claim to the parameterisation tested until this is done.
**Severity**: Major
**Confidence**: 4 — core expertise: calibration of reduced-order coronary models

### W3: Concealment attributed to tuning is not supported against fixed boundary conditions or robustly in the leaky bed
**Problem**: The abstract states that tuning "removed the perfusion mismatch that marked the error". In the leaky bed, however, fixed boundary conditions already yield more pass-while-wrong topological models (20%, 15–26) than tuning (8%, 5–13). The re-derived missed-branch median residual is 0.04, below the 10% check, so the mismatch did not mark the error before tuning either. The paper's own rule is that "a finding is claimed only where its direction agrees in both" beds, and §III-B correctly declines to claim A against C. The abstract, Discussion ("tuning separated the validation check from the error") and the third practical step ("record the mismatch before tuning") nonetheless rest on that contrast. In addition, the leaky tuned rate (8%) is close to the simulated correct-anatomy floor (3.9%, 3.2–4.6). It falls to 3% at 0.7 times demand, which the supplement itself calls "comparable with the simulated floor". No test of C against B, or of C against the simulated floor, is reported for the concealment endpoint.
**Evidence Anchor**: table: Table S3 — Leaky, T1+T2, 10% column: A 20 (15–26) vs C 8 (5–13)
**Why it matters**: The paper's central novelty is the pass-while-wrong count. Only the C-against-B contrast agrees in direction in both beds. The leaky-bed effect is not clearly above the noise floor across the demand sensitivity.
**Suggestion**: State the concealment claim relative to re-derived boundary conditions only. Add paired exact McNemar tests on the pass-and-wrong indicator (C against B, C against A) with Holm adjustment, and a comparison against the simulated floor. Qualify the leaky-bed figure in the abstract, and revise the "record the mismatch before tuning" recommendation so it reflects that the pre-tuning mismatch flagged the error only in the discrete bed.
**Severity**: Major
**Confidence**: 4 — core expertise: paired binary-outcome analysis; numbers taken from Tables I and S3–S4

### W4: Tuned caliber error yields the largest pass-while-wrong rate, contradicting the "minor risk" guidance
**Problem**: In the leaky bed, 24% (18–31%) of tuned taper models pass the perfusion check while materially wrong. That exceeds every topological cell under Protocol C in that bed (11% and 6%) and exceeds the leaky "All" pooled rate for topological errors (Table S3: All 11 vs T1+T2 8). §III-B reports this ("Tuning also enlarged the taper error"). Yet §IV-C advises users to "treat diameter errors of inter-observer size as a minor risk", and the abstract concludes that detection "requires a check of the segmentation's branching structure". Both judge caliber risk only by flip rate under fixed boundary conditions.
**Evidence Anchor**: table: Table I — T4, Protocol C, leaky bed, Passes and wrong 24 (18–31)
**Why it matters**: For a pipeline that tunes to perfusion, which is the case the paper targets, the data show caliber error to be at least as large a concealment risk as topological error in one bed. A one-sided recommendation can mislead the readers it is meant to guide.
**Suggestion**: Report the concealment endpoint for caliber errors alongside topological errors in the abstract and Discussion. Explain the mechanism: matching clean flows through a narrowed lumen enlarges the stenotic pressure drop. Make the practical guidance conditional on whether boundary conditions are tuned.
**Severity**: Major
**Confidence**: 4 — core expertise: reduced-order hemodynamics; directly from Table I

### W5: Protocol comparisons in Table I and the abstract use different instance sets
**Problem**: The protocols are compared within instance (McNemar), but the headline proportions are not. In the discrete bed, T2 under Protocol A excludes 36 instances in which the break removed every outlet, against 96 under B. Protocol C excludes 33 to 49 instances per cell, nearly all RCA. The abstract and Discussion statement that re-derived or tuned boundary conditions "reduced topological decision changes to 5–20%" from 18–43% therefore compares partly different, differently composed populations. The 36 excluded Protocol A instances are not missing at random. With no outflow, the fixed-boundary model has zero flow and FFR tends to 1, so they are the worst-case outcome of fixed boundary conditions, and excluding them understates the A flip rate. It is also not stated whether the 60 instances under A and C for discrete T2 are the same set.
**Evidence Anchor**: table: Table I — T2, discrete bed, n = 60 (A), 96 (B), 60 (C)
**Why it matters**: Protocol-to-protocol differences in Table I mix a protocol effect with a case-mix effect (left versus right tree). The abstract's ranges inherit that mix.
**Suggestion**: Report every protocol comparison on the common set of instances for which all compared protocols are defined (or add a common-set panel to Table I), and use those numbers in the abstract. State explicitly how no-outflow Protocol A models are treated. Report them as FFR = 1 (decision flip when baseline ≤ 0.80) in a sensitivity analysis, or justify their exclusion.
**Severity**: Major
**Confidence**: 4 — core expertise: paired designs; counts from Tables I and S1

### W6: Hyperemic demand and radius definition place the cohort at sub-physiological flow
**Problem**: The demand law Q = k·r_in³ is calibrated so that a 3.7 mm proximal LAD carries 214 mL/min. The cohort's own median inlet radius, however, is 1.39 mm, or 2.8 mm diameter, measured at the tree inlet (left main or RCA ostium), giving a median demand of 1.5 mL/s (about 90 mL/min) per tree. That is well below the 228–293 mL/min the paper cites for the LAD alone. The radius definition subtracts half a voxel, and the 3D section reports the meshed lumen to be wider by a median 0.14 mm. Because demand scales with r³ and resistance with r⁻⁴, the definitional offset matters. On the requested radius the reduced-order baseline was 0.761, against about 0.87 on the meshed radius, a 0.11 shift that exceeds every caliber-error effect studied. An 80% DS, 20 mm proximal-LAD lesion with FFR 0.87 (Fig. 5e) is consistent with low flow.
**Evidence Anchor**: text: §II-B "median demand was 1.5 mL/s"
**Why it matters**: Missed-branch and tuning effects depend on flow. Table S4 shows the pass-while-wrong rate rising monotonically with demand (12/19/25% discrete; 3/8/12% leaky). The ±30% demand sensitivity does not reach a physiological level if the radii are biased low. A radius-definition offset larger than T3/T4 also bears on the claim that caliber error is a minor risk.
**Suggestion**: Report the distribution of inlet and proximal-segment radii against normative values (e.g. Dodge et al.). Either rerun with the radius definition that matches the 3D lumen or calibrate demand to vessel-specific norms. Alternatively, extend the demand sensitivity to the factor implied by the radius bias. Discuss how the cohort's flow regime affects the magnitudes reported.
**Severity**: Major
**Confidence**: 3 — adjacent to core expertise: coronary physiology inferred from the reported radii and flows

### W7: The 3D twin verifies the reduced-order model at a different radius and on the other side of 0.80
**Problem**: The reduced-order twin used for the 3D comparison is rebuilt on the meshed, wider radius, with a baseline of about 0.87. The cohort model for the same instance runs on the narrower requested radius, with a baseline of 0.761, on the other side of the decision threshold. The Limitations assert that this offset "shifts absolute FFR but not the paired differences". No evidence is given, and the cohort's own ΔFFR for this instance under Protocol A on the requested radius is not reported. ΔFFR from a missed branch depends nonlinearly on baseline flow and stenotic loss, so paired differences need not be invariant to the radius offset. Reduced-order fidelity for topological errors is also verified on a single case at a single severity.
**Evidence Anchor**: text: §IV-D "this offset shifts absolute FFR but not the paired differences on which the findings rest"
**Why it matters**: The 3D case is the only check that the reduced-order model represents a topological error correctly. As run, it checks a model configuration that was not used for the cohort.
**Suggestion**: Report the cohort-model ΔFFR for this instance on the requested radius next to the twin's +0.081 and the 3D +0.074. Ideally add a reduced-order-to-3D comparison at a second severity or a second instance near 0.80. Otherwise, remove the invariance assertion.
**Severity**: Major
**Confidence**: 4 — core expertise: 0D/3D coronary model verification

### W8: Cohort enrichment near 0.80 makes absolute flip rates design-specific
**Problem**: Instances were drawn uniformly across six 0.05-wide bands from 0.65 to 0.95, so a third of the cohort lies within 0.05 of the cut-off. Absolute flip rates such as "32–33% of models" in the abstract therefore depend on this sampling design rather than on any clinical distribution of baseline FFR. The discrete-bed band distribution ("bands derived separately for each bed") is not reported. Fig. 2 and the floor comparison partly address this, but the abstract does not qualify the figure.
**Evidence Anchor**: text: §II-A "we drew 25 in each of six 0.05-wide bands of baseline FFR"
**Why it matters**: Readers will take 32–33% as an expected decision-change rate.
**Suggestion**: Qualify the abstract figures as rates in a cohort enriched near 0.80. Report the discrete-bed band counts. Optionally, add rates reweighted to a published clinical FFR distribution.
**Severity**: Minor
**Confidence**: 4 — core expertise: sampling design in sensitivity studies

### W9: The 3D discretisation uncertainty is not established for the case geometry, and the sub-0.001 claim is below it
**Problem**: The quoted discretisation uncertainty (5.5 × 10⁻⁴) comes from an idealised stenosis. On the actual case, throat refinement changed baseline FFR by 0.0019–0.0021, failing the authors' own acceptance criterion, and the finest variant did not reach the residual limit. The abstract's "below 0.001" (−0.0007) is smaller than this case-specific resolution sensitivity.
**Evidence Anchor**: table: Table S6 — ΔFFR +0.0019 (6.24 M cells) and +0.0021 (8.31 M cells), against the 5.5 × 10⁻⁴ criterion
**Why it matters**: The qualitative 3D conclusion survives (0.074 against about 0.002), but the reported precision does not.
**Suggestion**: State the 3D Protocol C effect as zero within a resolution of about 0.002. Run a three-level refinement on the case geometry for the ΔFFR quantity, not only the baseline.
**Severity**: Minor
**Confidence**: 5 — core expertise: CFD verification

### W10: Intervals ignore clustering of models within instances, trees and patients
**Problem**: Wilson intervals treat every model as independent. Pooled topological proportions combine T1 and T2 from the same instance (137 models from at most 97 instances), and up to two instances share a tree (150 instances from 93 patients). The intervals are therefore too narrow. The mixed model in the Supplement addresses clustering but is not used for the headline intervals.
**Evidence Anchor**: text: §II-F "Proportions are reported with Wilson 95% confidence intervals"
**Why it matters**: Interval width feeds the comparisons with the noise floor (W12).
**Suggestion**: Use cluster-robust (patient-level bootstrap) intervals for pooled proportions, or report the mixed-model marginal estimates alongside.
**Severity**: Minor
**Confidence**: 4 — core expertise: applied statistics for clustered simulation outputs

### W11: Mixed-model table — identical Severity posteriors across beds and variational intervals
**Problem**: The Severity coefficient is identical to three decimals, including both interval bounds, in two separately fitted models on different cohorts (97 and 150 instances), which suggests a transcription error. Intervals are also mean ± 1.96 SD from a variational approximation, which is known to understate posterior variance.
**Evidence Anchor**: table: Table S2 — Severity (% DS) row, 0.019 (0.016, 0.022) in both beds
**Why it matters**: The model is supporting evidence only, but a possible copy error undermines confidence in the supplement.
**Suggestion**: Verify the Severity row. Refit with MCMC (or report a variational-against-MCMC check) and give the fitted random-effect variances.
**Severity**: Minor
**Confidence**: 3 — inference from the table; cannot rule out coincidence

### W12: Noise-floor comparisons for caliber errors are stated more strongly than the intervals allow
**Problem**: The abstract says caliber flip rates of 6–10% are "close to the variability of repeat invasive measurement". The pooled discrete caliber rate, 20/194 = 10.3% (6.8–15.4% Wilson), however, has a lower bound above the 6.5% upper floor. Conversely, the leaky taper under Protocol A is said to exceed the floor "with its lower confidence bound", but 14/150 has a Wilson lower bound of 5.6%, inside the 5.0–6.5% floor range.
**Evidence Anchor**: text: §III-A "Only the taper under fixed boundary conditions exceeded this noise floor"
**Why it matters**: The caliber-versus-floor comparison underpins the "minor risk" guidance.
**Suggestion**: Report each cell's own floor value next to its interval, and correct both statements.
**Severity**: Minor
**Confidence**: 4 — recomputed Wilson intervals

### W13: Two supplement counts do not reconcile
**Problem**: The noise-floor runs comprise 97 × 20 + 150 × 20 = 4 940 draws, matching Table S5 (1 940 + 2 990 solved + 10 failures). The text says "10 of 5 860". Likewise, "2 856 corrupted models were attempted" does not reconcile with Table S1: 2 964 possible minus 162 not applicable gives 2 802, and 2 599 solved plus 203 Protocol-undefined also gives 2 802.
**Evidence Anchor**: text: §S2 "10 of 5 860 noise-floor draws did"
**Why it matters**: These are minor arithmetic errors, but they sit in the exclusion accounting that supports reproducibility.
**Suggestion**: Correct both counts, or define what "attempted" includes.
**Severity**: Minor
**Confidence**: 4 — direct recomputation

### W14: The leaky-bed damping mechanism conflicts with the Protocol A definition
**Problem**: Under Protocol A, surviving nodes keep their clean conductances and "the bed of deleted vessels is lost". The leaky-bed reappearance of a deleted branch's conductance at its parent node therefore operates only when the bed rule is re-applied (Protocol B). §IV-A nevertheless uses it to explain why the fixed-boundary missed-branch shift is smaller in the leaky bed (0.047 against 0.095).
**Evidence Anchor**: text: §IV-A "damping the error before tuning"
**Why it matters**: The paper's explanation of the bed-structure difference is inconsistent with its methods, so the true driver is unexplained.
**Suggestion**: Clarify how Protocol A is implemented in the leaky bed, or replace the explanation. A candidate is the different distribution of baseline outflow along the host vessel.
**Severity**: Minor
**Confidence**: 3 — inference from the methods text

### W15: Caliber error operationalisation is one-signed and loosely mapped from overlap metrics
**Problem**: T3 lengthens the lesion by the HD95 value. HD95 is a whole-tree surface distance usually dominated by branch ends, not by lesion extent. T4 converts whole-tree DSC to a uniform radius ratio. Both errors are applied in one direction only (longer and narrower). Inter-observer disagreement is two-sided, and over-segmentation would lower flips under A but may behave differently under C.
**Evidence Anchor**: text: §II-C "HD95 (2.46 mm) sets"
**Why it matters**: The topological-against-caliber ratio ("three to six times") depends on these magnitude choices.
**Suggestion**: Justify the HD95-to-length mapping, or replace it with a lesion-local measure. Add the opposite-sign caliber errors (shorter lesion, ×1/0.93 taper).
**Severity**: Minor
**Confidence**: 4 — core expertise: geometric uncertainty modelling

### W16: The pre-specification claim is not verifiable
**Problem**: The paper states that the design and analysis plan were fixed and the cohort list hashed before the ablation was run. It does not give a registry, timestamp, hash value or deviations list. It is also not stated whether the 13%/16% thresholds, the demand sensitivity, the simulated floor and the mixed model were pre-specified. The 3D acceptance deviations appear only in the Supplement.
**Evidence Anchor**: text: §II-F "the cohort list hashed, before the ablation was run"
**Why it matters**: Pre-specification is offered as a rigour safeguard but cannot be checked.
**Suggestion**: Report the hash value and the registry or time-stamped record. Mark each analysis as pre-specified or post hoc, and add a deviations table.
**Severity**: Minor
**Confidence**: 4 — standard reporting expectation

### W17: Code and cohort list are available only on request
**Problem**: The ablation runs end to end from a script and a frozen cohort list on a public dataset, but neither is released. Some parameters needed to rerun are absent: the under-relaxation factor, the calibrated C values, territory counts per tree, and the refinement tolerance of the Protocol C fit.
**Evidence Anchor**: text: Data and Code Availability "The code and the frozen cohort list are available from the corresponding author on request."
**Why it matters**: The 150-instance selection cannot be reproduced in principle without the list. Release is cheap for an in silico study on open data.
**Suggestion**: Deposit code and cohort list in an archived repository with a DOI, and add the missing parameters to the Supplement.
**Severity**: Minor
**Confidence**: 5 — standard reproducibility expectation for computational studies

### W18: The ablation perfusion check uses noise-free targets
**Problem**: In the ablation, the perfusion residual is computed against exact clean-model territory flows. Error and measurement noise are never combined: the simulated floor adds noise only to correct anatomy. The 10% check is therefore applied to an idealised target. The paper argues that looser thresholds can only increase passes, but with noisy targets a topological error can also fail where it would have passed, so the net effect on pass-and-wrong is not given.
**Evidence Anchor**: text: §II-D "Its target is the total bed outflow of that subtree in the clean model"
**Why it matters**: The concealment rate is meant to describe what a real perfusion check would miss.
**Suggestion**: Repeat Protocol C for topological errors with the same 20 noisy-target draws used for the simulated floor, and report pass-and-wrong against the floor.
**Severity**: Minor
**Confidence**: 4 — core expertise: UQ design

### W19: "Clean" is ambiguous in the 3D case, and the two 3D baselines differ
**Problem**: In the reduced-order model, "clean" means lesion with no segmentation error. In 3D, the "clean" lumen has no lesion, and the outlet resistances and territory flows are said to be "the clean tree's". The same baseline geometry gives FFR 0.870 with fixed resistances and 0.892 with prescribed flows, so the two outlet conditions do not deliver the same baseline flow. The source of the prescribed flows (3D or reduced-order, which lumen) is not stated.
**Evidence Anchor**: text: §III-D "0.892 in both geometries"
**Why it matters**: The two 3D contrasts are anchored to different references, which complicates comparison with the reduced-order Protocols A and C.
**Suggestion**: Define the source of outlet resistances and prescribed flows in the 3D case, and explain the 0.022 baseline difference.
**Severity**: Minor
**Confidence**: 3 — inference from the reported values
