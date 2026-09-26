---
source_pdf_path: Resources/Toward_Trustworthy_Health_Digital_Twins_A_Proof-of-Concept_Design_and_Validation_Framework_for_Clinical_Decision_Support.pdf
slug: sultana-2026-trustworthy-twins
ledger_status: TRIAGED
---

# sultana-2026-trustworthy-twins

## Bibliographic
- Title: Toward Trustworthy Health Digital Twins: A Proof-of-Concept Design and Validation Framework for Clinical Decision Support
- First author / authors (first 3 + et al.): Shalina Sultana Champa
- Year: 2026
- Venue: 2026 IEEE 14th International Conference on Healthcare Informatics (ICHI)
- DOI: 10.1109/ICHI69079.2026.00268

## One-line claim
This paper proposes a structured multi-level validation framework for AI-driven health digital twins that integrates data harmonization, dynamic patient state modeling, and comprehensive validation protocols (predictive accuracy, temporal stability, robustness under data heterogeneity, clinical plausibility) for clinical decision support.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper addresses patient-level clinical features and risk factors, not vascular geometry or segmentation uncertainty.
- **Q-B decision flip**: YES, stroke risk prediction with binary reclassification reported. Evaluation on 560 patients (28 stroke-positive, 532 stroke-negative); Neural Network achieves 0.71 Recall on minority class under balanced training. "Severe class imbalance (28 stroke-positive vs. 532 stroke-negative)" noted as key validation challenge.
- **Q-C BC tuning**: NOT REPORTED. No haemodynamic boundary condition tuning discussed; focus is on AI model calibration and temporal robustness.
- **Q-D fidelity / quantity**: NOT APPLICABLE to haemodynamics. Paper uses 3-classifier ensemble (Neural Network, Random Forest, Decision Tree) for stroke risk prediction; no CFD or WSS/OSI.
- **Q-E data**: Dataset: 560 patients with stroke outcomes; FHIR-structured electronic health records; invasive FFR not explicitly ground truth; stroke risk is clinical outcome.
- **Q-F meshing**: NOT APPLICABLE. No vascular segmentation or meshing pipelines.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: This paper directly addresses the critical challenge of multi-level validation for health digital twins, distinguishing between model validation and system-level clinical validation. It proposes concrete validation metrics (temporal robustness, robustness under distributional shift, clinical plausibility) and emphasizes that "conventional retrospective benchmarking systematically conceals" early-stage metric instability under data scarcity, which maps to the concern that re-fitting a model to limited calibration data can mask structural errors.
- verdict: FULL
- revisit-if: N/A; strong SUPPORT paper for T6 validation framework design

## Key T6-bearing findings
**(1) What does the paper require before a model/digital twin may be called validated?**

The paper proposes "trustworthiness as a first-class architectural requirement, not a post-hoc evaluation exercise." Multi-level validation includes:
- Predictive accuracy on held-out data
- Temporal stability across sequential data accumulation
- Robustness under missing modalities and distributional shift
- Clinical plausibility in operational workflows
- Zero degradation through semantic orchestration (Manifest protocol validation)

Quote: "Temporal robustness, behavior under missing modalities, subgroup calibration, and clinical plausibility remain critically underexplored. This paper addresses that gap by proposing a structured design and multi-level validation framework..."

**(2) Does it distinguish calibration/fitting from validation?**

YES. The paper explicitly distinguishes between:
- Training on "oversampled balanced cohort"
- Evaluation on "original imbalanced distribution"
- "Elevated scores for RF and DT are attributable to SMOTE oversampling...and should be interpreted as an upper bound under balanced training conditions rather than a claim of clinical-grade generalization. Independent held-out validation is required to confirm generalizability."

**(3) Does it warn that tuning free parameters can mask structural/input error?**

IMPLICITLY YES. The paper states:
> "conventional retrospective benchmarking systematically conceals" early-stage metric instability. "The incremental evaluation strategy surfaces temporal robustness characteristics that conventional retrospective benchmarking systematically conceals."

And critically:
> "Metric fluctuation in early stages reflects limited stroke-positive cases in small cohorts, with measurable stabilization emerging from Stage 5 onward."

This illustrates that a model re-fitted to increasingly large retrospective cohorts may appear stable and well-validated while early signs of distributional shift or poor generalization are hidden until prospective deployment. The inference for T6 is that re-tuning outlet boundary conditions on retrospective haemodynamic data can appear successful (good outlet pressure match) while masking unmodeled segmentation error.

**(4) Does it propose concrete validation tests or metrics for a haemodynamic model?**

NOT SPECIFICALLY FOR HAEMODYNAMICS, but the framework is generalizable:
- Predictive accuracy (precision, recall, F1, AUC)
- Temporal/incremental robustness (metric stability as cohort size grows)
- Robustness under missing data modalities
- Residual independence and whiteness tests (Manifest protocol validation)
- Clinician-in-the-loop plausibility assessment

