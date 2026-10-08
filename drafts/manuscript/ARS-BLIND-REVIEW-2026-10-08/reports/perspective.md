contract_role: perspective
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: warn
trigger: "The correspondence to real segmentation failures is argued but only partially evidenced or limited to one error class"

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

I read this manuscript as a medical image segmentation and imaging-informatics researcher who works on topology-aware learning and coronary centerline benchmarks and has an interest in model credibility (ASME V&V 40, FDA in silico evidence). I am not a reduced-order modelling specialist, and I defer to the methodology and domain referees on solver, bed-law and physiology questions.

The paper asks a question that matters to my community: whether the segmentation errors we optimise against are the ones that change a clinical decision downstream. It is unusually readable for non-CFD readers. Its central informatics message, that topology errors matter more than caliber errors and that overlap metrics miss them, is plausible and important. It is not yet substantiated in the terms a segmentation reader would need to act on it, for four reasons. (i) The caliber error model leaves out the caliber error most likely to move CT-FFR: the throat radius at the stenosis. The paper's own 3D twin shows that error is decision-relevant. (ii) The topological error models are design choices, and no observed incidence from real segmentation outputs supports them. The flip rates are therefore conditional impacts, not risks. (iii) No segmentation-QC metric is computed for any corrupted tree. (iv) The practical steps are not operational. The credibility framing ("pass validation") also uses validation in a sense that a V&V 40 reader would call calibration-data reuse. None of these defects invalidates the core in silico result. Together they keep the cross-disciplinary claims at the level of argument rather than evidence, which is the warn condition I committed to.

### S1: Plain-language definitions make the hemodynamics accessible to imaging readers
FFR, lumen, boundary conditions, microvascular bed, caliber, topological error, DSC and HD95 are each defined in one clause at first use. A segmentation researcher can follow Sections I–II without a CFD background.
**Evidence Anchor**: text: §I "the blood-filled channel of the artery"

### S2: Decision-level outcome with a measurement noise floor
Judging an image-processing error by whether it flips the treatment decision at 0.80, against the repeatability of invasive FFR, is the right endpoint for health informatics. Imaging papers rarely do this, and it gives segmentation researchers an outcome-anchored target in place of a geometric proxy.
**Evidence Anchor**: text: §I "segmentation error is judged by whether it"

### S3: Error taxonomy grounded in an open benchmark with inter-observer data
The explicit split into topological and caliber errors uses a public dataset with two-annotator re-annotation, and the caliber magnitudes are tied to measured annotator disagreement. This makes the study a bridge between segmentation benchmarking and hemodynamic modelling.
**Evidence Anchor**: dataset: ImageCAS-X 160-scan test split with second-analyst re-annotation (§II-A, DSC 92.8%, HD95 2.46 mm)

### S4: Direction of the clinical harm is stated
The paper notes that a concealed missed branch raises FFR and therefore biases toward deferral of a lesion that needs treatment. This identifies the patient-safety direction of the failure mode, which is what a risk analysis needs.
**Evidence Anchor**: text: §IV-C "its concealed error biases the"

### S5: Recommendations are explicitly bounded
The four practical steps are labelled as following from the results but not validated. This is appropriate restraint for an in silico study.
**Evidence Anchor**: text: §IV-C "but are not validated decision rules"

### S6: Figure 3 shows the concealment mechanism directly
Plotting ΔFFR against perfusion residual with the pass-while-wrong region shaded lets an informatics reader see the validation gap without parsing the bed equations.
**Evidence Anchor**: figure: Fig. 3, ΔFFR versus territory-perfusion residual, discrete and leaky beds

### W1: The caliber error model omits throat-radius error, and the paper's own 3D twin shows that error changes the decision
The two caliber errors are lesion lengthening by HD95 (T3) and a 7% radius reduction from the lesion onward (T4). Neither represents the caliber failure that segmentation researchers associate with CT-FFR error: misestimating the minimal lumen at the stenosis, for example through calcium blooming, partial-volume effects or the radius definition itself. At 80% DS the throat radius in Fig. 1(d) is about 0.25 mm, below a CCTA voxel. A one-voxel boundary error there is a relative caliber error far larger than 7%. Section III-D gives the evidence. The meshed throat radius (0.276 mm) and the reduced-order radius (0.231 mm) differ by 0.045 mm, and on the requested radius the reduced-order baseline FFR was 0.761 against about 0.87 on the meshed radius. That throat-caliber difference alone crosses 0.80. The second practical step ("treat diameter errors of inter-observer size as a minor risk") and the Discussion statement that decision risk lies "not in its caliber" therefore rest on a caliber model that excludes the most sensitive location. Mapping whole-tree HD95 to lesion length and whole-tree DSC to a uniform coaxial radius ratio adds further uncertainty: both metrics are dominated by large proximal vessels, not by the stenosis.
Suggestion: add a throat-local caliber error, for example ±0.5 and ±1 voxel on the minimal lumen radius, or a calcium-blooming perturbation confined to the lesion. Report its flip rate beside T3/T4, and limit the "caliber is minor" conclusion to the caliber errors tested.
**Severity**: Major
**Evidence Anchor**: text: §III-D "throat area-equivalent radius 0.276 against" and "on the requested radius the reduced-order"
**Confidence**: 4 — core expertise: coronary lumen segmentation and stenosis quantification

### W2: Correspondence of T1/T2 to real segmentation failures is argued only by citation and design choice
T1 always deletes the largest side branch distal to the lesion. T2 always truncates the host vessel 25 mm beyond the lesion. In automated coronary segmentation, missed branches are typically small distal branches, and a missed diagonal or obtuse marginal of the largest calibre is comparatively uncommon. Breaks also often leave a disconnected distal fragment, which a pipeline may drop, bridge or keep as a separate tree, rather than producing a clean truncation. The paper acknowledges that the T1/T2 magnitudes "are design choices" and supports their realism with two citations ([18], [19]), not with failure data. The same benchmark ([18]) evaluated several methods on this test split. Without an observed distribution of branch omissions and breaks (location relative to stenoses, branch size, distance), a reader cannot tell whether T1/T2 are typical, worst-case or rare.
Suggestion: run one or two standard methods (for example nnU-Net, plus a topology-aware variant) on the ImageCAS-X test split, or use benchmark outputs if they are released. Characterise the observed missed-branch sizes and break positions relative to the inserted lesion sites. Then either resample T1/T2 from that empirical distribution or report where the chosen T1/T2 lie on it, for example as a percentile of omitted-branch radius.
**Severity**: Major
**Evidence Anchor**: text: §II-C "deletes the largest side branch that leaves" and "T1 and T2 have no measured"
**Confidence**: 4 — core expertise: coronary segmentation failure modes and benchmarks

### W3: Flip rates are conditional impacts on an enriched cohort but are read as segmentation risk
The cohort is sampled uniformly across 0.05-wide baseline-FFR bands from 0.65 to 0.95, which concentrates instances near 0.80. Each error is applied with probability one. The 32–33% topological and 6–10% caliber flip rates are therefore the conditional impact of a given error on near-threshold lesions. They are not the frequency with which a segmentation pipeline changes decisions. The Discussion nonetheless says the decision risk of segmentation "lies mainly in the branching structure". For an informatics or regulatory reader, risk is probability of occurrence times impact, and the probability term (incidence of each error type in real outputs) is absent. If caliber errors occur in nearly every segmentation and distal-branch omissions in a minority, the population ranking could differ.
Suggestion: rephrase the claim as conditional impact. If incidence estimates can be obtained (see W2), combine them with the per-error flip rates and a realistic baseline-FFR distribution to give an expected decision-change rate per error class. Otherwise state explicitly that the ranking is per occurrence.
**Severity**: Major
**Evidence Anchor**: text: §IV-A "lies mainly in the branching structure of the"
**Confidence**: 4 — adjacent field: risk framing in imaging-AI evaluation

### W4: No segmentation-QC metric is computed for the corrupted trees, so the overlap-metric claim is asserted, not shown
The Discussion's main message to segmentation readers is that the decision-relevant errors are ones "the usual overlap metrics do not measure". It also says a missing branch "removes few voxels". Yet no DSC, HD95, clDice, Betti-number error or centerline-overlap score is reported for any T1–T4 corrupted mask. The study has the clean and corrupted geometry for every instance, so these metrics are cheap to compute. They would let an imaging reader see, in their own units, how a T1 tree with ΔDSC of perhaps under 1% maps to |ΔFFR| > 0.05, and which metric (if any) separates decision-changing from benign errors.
Suggestion: compute DSC, HD95, clDice, Betti-0/Betti-1 error and a centerline overlap-until-first-error measure (Schaap et al. 2009) for each corrupted instance. Plot each against |ΔFFR| and report rank correlation, or an AUC for predicting a flip. This would turn the qualitative claim into a QC threshold.
**Severity**: Major
**Evidence Anchor**: text: §IV-B "branch removes few voxels, so the error types that carried the"
**Confidence**: 5 — core expertise: segmentation evaluation metrics including clDice and topological metrics

### W5: The practical steps are not operational for a pipeline user
Step 1 ("check that the side branches beyond the lesion are present") assumes the user can tell a branch is missing without ground truth. Step 3 ("record the mismatch before tuning") gives no mismatch threshold and no detection performance. The data to make Step 3 actionable are already in the study. Protocol B residuals for corrupted trees, and the simulated noise floor for correct anatomy (72% pass), would together give a sensitivity/specificity or ROC curve for flagging a topological error from the pre-tuning residual. For Step 1, ImageCAS-X provides labelled centerlines. An anatomical-label completeness check (for example against an SCCT-style segment model) or a branch-count prior per territory would be a concrete topology check that an informatics reader could implement.
Suggestion: report the detection performance of the pre-tuning perfusion residual, with the threshold, sensitivity and false-alarm rate on correct anatomy. Name at least one implementable topology check and, ideally, evaluate it on T1/T2.
**Severity**: Major
**Evidence Anchor**: text: §IV-C "to perfusion, record the mismatch before tuning, because a"
**Confidence**: 4 — core expertise: segmentation QC pipeline design

### W6: "Validation" is used for what credibility frameworks call calibration-data reuse, and no context of use is stated
The abstract concludes that a perfusion-matched model "can thus pass validation with a material error". In Protocol C the same territory flows serve as calibration targets and as the validation check. Under ASME V&V 40 and the FDA 2023 guidance on the credibility of computational modelling, such a check is not independent validation evidence. Its failure to detect error is expected in principle, and the paper's own sentence ("the check measured agreement with the fitted targets") says so. The quantitative contribution, how often this happens and by how much, is real. Calling it a validation failure, however, overstates the novelty for credibility readers and may confuse them. The paper also cites credibility requirements [33] without stating a context of use (for example: CT-FFR informing deferral versus revascularisation at 0.80) or a model-risk level, which V&V 40 needs before the observed error can be judged acceptable or not.
Suggestion: reword as "passes a calibration-consistency (perfusion-fit) check". Add one paragraph that places the finding in V&V 40 terms: question of interest, context of use, decision consequence (deferral bias, S4), and the implication that perfusion used for tuning cannot also serve as validation evidence.
**Severity**: Major
**Evidence Anchor**: text: Abstract "pass validation with a material error in its fractional flow reserve"
**Confidence**: 4 — adjacent field: model credibility frameworks (ASME V&V 40, FDA CM&S guidance)

### W7: Topology-aware segmentation and centerline-evaluation literature is reduced to one citation
Only clDice [32] represents topology-aware methods. The implication that pipelines should guard against breaks and omissions would be stronger if linked to the established tools. These include the Rotterdam centerline evaluation framework with its overlap-until-first-error measure, Betti-matching and persistent-homology losses, skeleton-recall loss for thin tubular structures, and the ASOCA coronary segmentation challenge, which reports performance on diseased arteries.
Suggestion: add a short paragraph in §IV-B that cites these and states which metric would have flagged T1/T2 (ties to W4). Candidate references: Schaap et al., Med. Image Anal. 2009 (centerline evaluation framework); Hu et al., NeurIPS 2019 (topology-preserving segmentation); Stucki et al., ICML 2023 (Betti matching); Kirchhoff et al., ECCV 2024 (skeleton recall loss); Gharleghi et al., Comput. Med. Imaging Graph. 2022 (ASOCA challenge).
**Severity**: Minor
**Evidence Anchor**: absence: §IV-B and reference list — expected topology-aware segmentation and centerline-evaluation literature beyond clDice; checked Introduction, §IV-B, §IV-C and references [17]–[19], [32]
**Confidence**: 5 — core expertise: topology-aware segmentation literature

### W8: Code on request undercuts the proposed pipeline test
Section IV-C invites developers to apply the same four-error test to their own pipelines and compare with Table I. With code available only on request, that benchmark cannot be reproduced or adopted. For a JBHI informatics audience, an open error-injection and evaluation toolkit would be one of the paper's most reusable contributions.
Suggestion: release the error-injection, reduced-order solver and analysis scripts (Fig. S1 modules) with the frozen cohort list in a public archive with a DOI.
**Severity**: Minor
**Evidence Anchor**: text: Data and Code Availability "available from the corresponding author on"
**Confidence**: 4 — adjacent field: reproducibility norms in imaging informatics

### W9: Topological results under tuning describe only the left coronary tree
Protocol C was undefined for most RCA topological instances, so the tuned-concealment finding applies to left-tree lesions. Coronary dominance is not reported. A segmentation reader would expect RCA distal segments and posterior descending branches, which are frequent sites of omission and breaks, to be where the error is most common. The generalisation gap is therefore in the clinically relevant direction.
Suggestion: report dominance for the cohort, state the left-tree scope in the abstract, and consider a territory definition that allows tuning on RCA trees (for example, using the posterior descending and posterolateral territories).
**Severity**: Minor
**Evidence Anchor**: text: §IV-D "results for these errors describe the left coronary tree"
**Confidence**: 3 — adjacent field: coronary anatomy as encountered in segmentation labelling

### W10: The bed structures and Protocols A/B/C lack a schematic for non-CFD readers
The leaky and discrete beds and the three protocols are defined in dense prose with conductance formulas. Fig. 1 illustrates only the errors. For an imaging reader, the leaky bed (outflow along the vessel wall) and the difference between re-derived and tuned beds are the hardest concepts, and they drive the bed-dependent magnitudes.
Suggestion: add a small schematic panel (Fig. 1 or the supplement) showing a toy tree under each bed and each protocol, with arrows for outflow and the tuned parameter.
**Severity**: Minor
**Evidence Anchor**: text: §II-B "In the leaky bed, flow leaves along the vessel"
**Confidence**: 4 — core expertise: communicating to imaging-informatics readers

### Cross-Disciplinary Reading Recommendations
- Schaap M. et al., "Standardized evaluation methodology and reference database for evaluating coronary artery centerline extraction algorithms," Med. Image Anal., 2009. It introduces overlap-until-first-error, a break-sensitive metric (W4, W7).
- Shit S. et al., clDice, CVPR 2021 (already cited [32]); Stucki N. et al., "Topologically faithful image segmentation via induced matching of persistence barcodes," ICML 2023; Hu X. et al., "Topology-preserving deep image segmentation," NeurIPS 2019.
- Kirchhoff Y. et al., "Skeleton Recall Loss for connectivity conserving and resource efficient segmentation of thin tubular structures," ECCV 2024.
- Gharleghi R. et al., "Automated segmentation of normal and diseased coronary arteries – the ASOCA challenge," Comput. Med. Imaging Graph., 2022 [volume and article number UNVERIFIED].
- ASME V&V 40-2018 and US FDA, "Assessing the Credibility of Computational Modeling and Simulation in Medical Device Submissions," final guidance, 2023 (W6).

### Questions for Authors
1. Do the ImageCAS-X benchmark outputs (or a standard model run on the test split) show missed branches and breaks distal to the lesion sites you used, and at what branch sizes?
2. What flip rate results from a ±1-voxel error confined to the throat radius?
3. What are the sensitivity and false-alarm rate of the pre-tuning residual as a detector of a topological error?
