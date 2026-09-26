---
source_pdf_path: Resources/1-s2.0-S1361841520301973-main.pdf
slug: bertels-2021-volume-bias-soft-dice
ledger_id: C008
ledger_status: FULL
---

# bertels-2021-volume-bias-soft-dice

## Bibliographic
- Title: Theoretical analysis and experimental validation of volume bias of soft Dice optimized segmentation maps in the context of inherent uncertainty
- Authors: Jeroen Bertels, David Robben, Dirk Vandermeulen, Paul Suetens
- Affiliations: Processing Speech and Images, Dept. of Electrical Engineering, KU Leuven; Medical Imaging Research Center, UZ Leuven; icometrix, Leuven; Dept. of Anatomy, University of Pretoria
- Year: 2021 (received 19 Feb 2020, revised 7 Sep 2020, accepted 14 Sep 2020, online 7 Oct 2020)
- Venue: Medical Image Analysis 67 (2021) 101833
- DOI: 10.1016/j.media.2020.101833
- Note: extended version of Bertels et al. (2020), "Optimization with soft dice can lead to a volumetric bias," Brainlesion workshop (MICCAI 2019 satellite).

## Problem & claim
- Task: theoretically and experimentally analyze whether the choice of CNN segmentation loss — cross-entropy (CE) vs. soft Dice (SD) — biases the volume estimate derived from the resulting segmentation, specifically when the segmentation task carries **inherent** (non-reducible, aleatoric) uncertainty.
- Central claim (Abstract, p.1): "We find that, even though soft Dice optimization leads to an improved performance with respect to the Dice score and other measures, it may introduce a volume bias for tasks with high inherent uncertainty. These findings indicate some of the method's clinical limitations and suggest doing a closer ad-hoc volume analysis with an optional re-calibration step."
- Framing (Introduction, p.2): "to the best of our knowledge, there is no research that investigates whether this evolution in preferred loss function [towards soft Dice], in combination with the typical inherent uncertainty present in medical applications, had any influence on the resulting segmentations and the derived volume estimates thereof."

## Method
- Theoretical (Sect. 2): under general empirical-risk-minimization theory, for a voxel/region with true foreground probability p (inherent uncertainty, e.g. ambiguous border), the risk-minimizing soft prediction under **CE** is p̃ = p exactly (Eq. 10) — i.e. CE's soft output map is an unbiased probability estimate and V(ỹ) (sum of soft outputs) is an unbiased estimator of E[V(l)] (Eq. 8-10).
- Under **SD**, the risk-minimizing solution for an uncertain region pushes toward the extremes: "the local minimum of the E[SD] loss function is either at p̃β=0 or p̃β=1... only for pβ={0,1} the predicted foreground probability p̃β is exact... for pβ smaller or larger than 0.5, respectively under- or over-estimation will occur" (p.4-5, Sect. 2.2). With multiple independent uncertain regions (K=4,16 sub-regions vs K=1), "there is a trend towards volume over-estimation... due to a larger range of pβ corresponding to volume over-estimation" (p.5).
- Summary of theory (Sect. 2.3, p.5): "CE and SD optimization will lead to different volume estimators... SD optimization prefers binary output segmentations, with no difference between V(ỹ) and V(l̃), thus producing biased volume estimates when there is inherent uncertainty in the task. More specifically, we expect for SD a trend towards over-estimation due to the larger range of inherent uncertainties that will lead to an over-estimation of the foreground probability."
- Experimental validation: four models of increasing complexity — logistic regression (LR), U-Net S, U-Net M, U-Net L (a "No New-Net"-derived architecture, Isensee et al. 2019) — trained with 5-fold cross-validation under both CE and SD losses, on four public medical segmentation datasets chosen to span low→high inherent uncertainty. Volume computed two ways: V(ỹ) (sum of soft/continuous predictions) and V(l̃) (sum after 0.5-thresholding).
- Re-calibration step (Sect. 3.2.2): "we analyzed for each fold the volume-specific behavior on the training set. We used least-squares regression to fit for each fold the linear model that best explains the volume-specificity and bias on the training set and use this to correct for on the validation set" (p.8).

## Data
Four public binary segmentation tasks, ordered low → high inherent uncertainty (p.6):
- **MO17** (low uncertainty): lower-left third molar segmentation on panoramic dental radiographs; 400 cases, 224x224. Manual delineation defined on the same input images.
- **BR18** (low uncertainty): whole brain tumor segmentation, BRATS 2018 MRI; 285 cases, 120x120x78. Manual delineation on same inputs.
- **IS17** (high uncertainty): post-operative final infarction segmentation predicted from **pre-operative** MRI perfusion, ISLES 2017; 43 cases. Ground truth delineated on different (post-op) images than the input — "results in a large amount of ambiguity ... when only taking into account imaging data and leaving out treatment information."
- **IS18** (high uncertainty): ischemic core segmentation on acute CT perfusion, ISLES 2018; 94 cases. Ground truth on registered pre-op MRI, input is CT perfusion — "CT and MRI provide different, rather complementary, information," and lower CT-perfusion spatial resolution "further increases the level of inherent uncertainty."
- All public challenge datasets; none coronary/vascular; no CFD-relevant geometry.

## Evaluation
- **Table 1 (volume bias E[ΔV], p.7)** — selected numbers, U-Net L (most complex model), CE vs SD:
  - MO17 (10³ pixels): CE V(ỹ) = −0.14, SD V(ỹ) = 0.00 (low-uncertainty task, near-zero bias for both).
  - BR18 (ml): CE V(ỹ) = −3.21, SD V(ỹ) = −3.95 (one strong under-estimating outlier noted, affects sign).
  - IS17 (ml, high uncertainty): CE V(ỹ) = 0.22, SD V(ỹ) = 2.46 — SD bias ~11x larger than CE, both over-estimating.
  - IS18 (ml, high uncertainty): CE V(ỹ) = 3.57, SD V(ỹ) = 6.46 — SD bias roughly 1.8x CE, both over-estimating (SD "highly significant, p<.001" for simple models, "remains significant for U-Net M for IS17 and IS18 and for U-Net L for IS18" per text p.7).
  - Simple LR model shows dramatically larger SD bias, e.g. MO17: CE V(ỹ) = −0.07 vs SD V(ỹ) = **302.29** (10³ pixels); IS17: CE = 15.71 vs SD = 82.42 ml; IS18: CE = 0.77 vs SD = 34.03 ml.
- Verbatim direction statement (p.7, Sect 3.2.1): "the optimization with respect to SD leads to over-estimation. This is highly significant (p<.001) for simple models and remains significant for U-Net M for IS17 and IS18 and for U-Net L for IS18 (and a trend remains for IS17), the two medical tasks having the highest inherent uncertainty. For CE optimized models this bias is almost absent."
- Volume-specific bias (Fig. 7, p.9, Sect 3.2.2), applies to **both** CE and SD: "we notice for both CE and SD optimization a volume-specific bias that over-estimates small volumes and under-estimates large volumes. The transition from under- to over-estimation seems to happen around the average true volume in the dataset." This is a size-dependent (not loss-function-specific) bias layered on top of the uncertainty-dependent SD bias.
- Re-calibration result (p.8): after per-fold linear re-calibration fit on training-set volume-specific errors, "there was no significant bias E[ΔV] remaining after re-calibration, except on BR18 where after SD optimization the bias was reduced from −3.90 to −2.34 ml, but remained significantly different from zero." Volume-specificity slopes also flattened toward unity for most tasks.
- Discussion (p.8-9): despite the SD volume bias, SD optimization gave smaller spread of individual volume errors and better relative/absolute volume-error performance in more complex models on less-uncertain tasks; over-segmentation (not under-segmentation) was the observed SD failure mode (Fig. 6), consistent with the multi-independent-region theory predicting over-estimation.

## Reproducibility
- Architectures fully specified (Fig. 4): LR, U-Net S/M/L (No-New-Net-derived, Isensee et al. 2019), ADAM optimizer, learning-rate schedule, augmentation, stopping criteria all given in text (Sect. 3.1). Statistical testing: non-parametric bootstrap (10,000 resamples), p<.05.
- Datasets: MO17 is a private/shared research dataset (via De Tobel et al. 2017, acknowledged); BR18 (BRATS 2018), IS17 (ISLES 2017), IS18 (ISLES 2018) are public challenge datasets.
- No code URL given in the extracted text.

## Limitations
- Quoted (Sect. 4, "Limitations and future work," p.10): "the analysis was limited to full-image processing. We therefore had to reduce the isotropic pixel- or voxel-sizes and limited the complexity of U-Net L compared to state-of-the-art... patch-wise training may result in substantial improvements. However, this would inevitably lead to inconsistencies between the theoretical analysis and the experimental validation."
- "It is not trivial to what extent the aleatoric or epistemic, respectively non-reducible and reducible, uncertainties play a role here" — the paper cannot cleanly separate the two uncertainty sources in the experimental (as opposed to theoretical) setting.
- Re-calibration parameters were fit and evaluated via cross-validation on the same dataset (no independent held-out test set): "When re-calibration was introduced this restricted the re-calibration parameters to be calculated from the training data, rather than from the validation data itself... We therefore propose further investigation of re-calibration on validation data in situations where one has access to an independent test set."
- Not admitted but evident: no vascular, tubular, or thin/elongated-structure task is among the four evaluated datasets; all four are volumetric "blob"-type structures (molar, tumor, infarct core).

## Openings
- Explicit future work (Sect. 4, p.10-11): investigate whether shape descriptors (not just volume) suffer similar loss-function-induced bias, citing hippocampal shape biomarkers as an example; analyze other loss functions beyond CE/SD; investigate a linear combination of CE and SD (used in practice, e.g. Isensee et al. 2019) which "obscures the de facto optimization objective" and only Pareto-trades-off bias; extend re-calibration to independent test sets rather than cross-validation folds.
- Unresolved for T6/Paper-3 purposes: the paper's theory and four experimental tasks concern **volume** (a 3D scalar) derived from segmentation, not linear or cross-sectional measurements (width, diameter, caliber) of elongated/tubular structures; no vascular segmentation task is tested.

## Key references
- Bertels et al. (2019, MICCAI) — theoretical grounding that SD optimization improves final Dice score vs. CE; this paper extends that line to ask about volume bias.
- Bertels et al. (2020, Brainlesion workshop) — the shorter precursor version of this exact paper.
- Guo et al. (2017) — CNN calibration/temperature-scaling background, cited re: CE producing "no longer well-calibrated" raw outputs at the individual-prediction level despite dataset-level calibration (cross-referenced against Jungo and Reyes 2019).
- Isensee et al. (2019), "No New-Net" — source architecture adapted for U-Net S/M/L.
- Jungo and Reyes (2019) — cited for the observation that CE-based soft maps are well-calibrated at the dataset level but not necessarily at the individual-subject level, used to interpret this paper's own CE spread results.

## T6 targeted questions

- **Q-A geometry perturbation**: NOT a geometry-perturbation study in T6's sense (no synthetic dilation/erosion of a lumen, no measured inter-observer geometric disagreement magnitude reported as a number). The paper instead studies **inherent (aleatoric) segmentation-task uncertainty** — ambiguity in what the "true" label even is — operationalized via four tasks chosen a priori to differ in uncertainty level (MO17/BR18 = low, IS17/IS18 = high, based on qualitative reasoning about whether ground truth was defined on the same or different images as the input). No quantitative inter-observer/inter-segmenter disagreement magnitude (e.g. a Dice or volume-difference number between two human raters) is reported anywhere in the extracted text.

- **Q-B decision flip**: NOT REPORTED. No FFR, no diagnostic threshold, no reclassification analysis of any kind. The clinical framing is limited to volume-estimation accuracy for structures such as tumors and stroke lesions.

- **Q-C BC tuning**: NOT APPLICABLE. This is a CNN segmentation-loss-function study; there is no CFD, no boundary condition, and no boundary-condition tuning of any kind.

- **Q-D fidelity / quantity**: NOT APPLICABLE in the CFD sense (no 3D flow solve, no WSS/OSI). The paper's "spatially-resolved" quantity is the voxel-wise soft segmentation probability map ỹ, and its aggregate quantity of interest is volume V. No downstream hemodynamic or flow-field quantity is computed.

- **Q-E data**: Four public/semi-public medical imaging datasets — MO17 (400 cases, dental radiograph, third-molar; source acknowledged, not a standard public challenge), BR18 (BRATS 2018, 285 cases), IS17 (ISLES 2017, 43 cases), IS18 (ISLES 2018, 94 cases). None are coronary or vascular; no invasive FFR ground truth (not applicable to this paper's domain).

- **Q-F meshing**: NOT APPLICABLE. Pure voxel-based CNN segmentation; no surface/volume meshing pipeline discussed.

## THREAT assessment

**Verdict: SUPPORT.**

Bertels et al. (2021) does not do anything T6 claims as new: it contains no geometry-perturbation experiment with a reported disagreement magnitude (Q-A), no FFR or diagnostic decision-flip analysis (Q-B), no CFD or boundary-condition tuning of any kind (Q-C), and no spatially-resolved flow-field output (Q-D). It operates in a completely different technical register — CNN loss-function choice and its effect on a single scalar (segmentation-derived volume) — with no CFD pipeline downstream of the segmentation at all, so it cannot compete with or pre-empt T6's geometry-perturbation-then-BC-retune-absorption thesis. What it does provide, and why it is SUPPORT rather than BACKGROUND or IRRELEVANT, is a rigorous, quotable, theoretically-derived and experimentally-confirmed mechanism by which a *segmentation method's training objective* (not just its accuracy) introduces a *systematic, direction-predictable bias* in a downstream quantitative measurement, and that this bias scales with the task's inherent (aleatoric) uncertainty and shrinks with model capacity — directly reinforcing T6's premise that "how a structure was segmented" is itself a source of systematic, non-random downstream error, over and above ordinary segmentation inaccuracy, and that this systematic-error idea is a legitimate, previously-published phenomenon T6 can build on (e.g. for framing why BC re-tuning might not compensate for systematic rather than random geometric error) rather than a novel finding T6 needs to defend as its own.

## Relevance to Paper 3 (retinal calibre uncertainty)

The paper never addresses thin or elongated (tubular/vascular) structures, or any linear/cross-sectional measurement such as width, diameter, or calibre; all four evaluated tasks and all reported analyses concern **volume** of roughly compact "blob" structures (molar, brain tumor, infarct core), and the word "vessel"/"thin"/"width"/"calibre"/"diameter" appears nowhere in the paper's body text (confirmed by full-text search). The one size-related finding that is reported and could bear indirectly on vessel width — "we notice for both CE and SD optimization a volume-specific bias that over-estimates small volumes and under-estimates large volumes" (p.9, Sect. 3.2.2) — states plainly that small structures tend to be over-estimated in volume by both loss functions, which is at least directionally consistent with (though not a direct test of) a concern that soft-Dice-trained vessel segmenters could systematically over-estimate a thin structure's width; but this is NOT REPORTED as a thin-structure or vessel-specific result, and the paper's uncertainty-driven SD bias (also over-estimation, per p.7's "leads to over-estimation... highly significant... for tasks with high inherent uncertainty") is likewise never tested on tubular geometry, so any extrapolation to retinal vessel-calibre bias direction is an inference from this paper's compact-structure findings, not a finding the paper itself makes.
