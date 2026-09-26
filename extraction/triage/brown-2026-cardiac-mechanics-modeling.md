---
source_pdf_path: Resources/s10659-026-10204-5.pdf
slug: brown-2026-cardiac-mechanics-modeling
ledger_id: C037
ledger_status: TRIAGED
---

# brown-2026-cardiac-mechanics-modeling

## Bibliographic
- Title: Cardiac Mechanics Modeling: Recent Developments and Current Challenges
- First author / authors: Aaron L. Brown, Ju Liu, Daniel B. Ennis (et al.)
- Year: 2026
- Venue: Journal of Elasticity 158:28
- DOI: https://doi.org/10.1007/s10659-026-10204-5

## One-line claim
Comprehensive review of patient-specific cardiac mechanics modeling covering anatomical reconstruction, mesostructure, constitutive models, boundary conditions, multiphysics coupling, and numerical methods for developing cardiac digital twins.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT EXPLICITLY REPORTED for coronary stenosis. Review discusses segmentation: "Manual segmentation remains the gold standard, but machine learning has significantly accelerated this process." Broadly discusses parameter uncertainty: "sensitivity analyses, and uncertainty quantification" are important. No testing of segmentation-derived geometry perturbation.
- **Q-B decision flip**: NOT REPORTED. Review focuses on cardiac mechanics, not FFR or diagnostic thresholds. No mention of stenosis classification or decision-making risk.
- **Q-C BC tuning**: Extensively discussed. "Appropriate boundary conditions (BCs) for electrophysiology, tissue mechanics, and blood flow are critical for achieving physiological results." "The parameters of the model should be 'personalized' with the goal of matching model outputs to patient-specific clinical data." "There could be tens or hundreds of model parameters" to optimize. NOT SPECIFIC: BC tuning methodology for coronary stenosis hemodynamics or FFR prediction.
- **Q-D fidelity / quantity**: Review covers multiphysics cardiac modeling spanning mechanics, electrophysiology, blood flow. Discusses "electrical signals propagate through the conduction system, triggering ionic exchanges that cause cellular contraction. This generates stress in the myocardial tissue, leading to mechanical deformation, which in turn drives blood flow within the heart and throughout the circulatory system." NOT FOCUSED: coronary artery WSS/OSI sensitivity analysis or stenosis hemodynamics.
- **Q-E data**: Discusses multi-modality imaging approach: "imaging exam using computed tomography (CT) or magnetic resonance imaging (MRI)... Additional clinical data, such as electrocardiogram, blood pressure readings (either non-invasive cuff-based or invasive catheter-based), and ultrasound measures." NOT REPORTED: invasive FFR ground truth or coronary hemodynamics validation.
- **Q-F meshing**: Extensively discussed in general cardiac context. "Triangulated surface model is constructed, which is then volumetrically meshed using standard meshing software." Discusses "determining the extent of the heart to include... choices between left ventricular models, bi-ventricular models, and four chamber models... significantly impact both model fidelity and computational cost." Covers multi-mesh strategies but NOT specific to robustness on poor segmentation or topologically-incorrect geometry in coronary arteries.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive review of patient-specific cardiac modeling pipeline (imaging, segmentation, mesostructure, BCs, parameter optimization, multiphysics); provides general context for computational cardiology but not specific to coronary stenosis hemodynamics, FFR prediction, or decision-flip risk.
- verdict: LIGHT
- revisit-if: Review extends with dedicated coronary hemodynamics sections, geometry uncertainty quantification, or FFR prediction framework.

## Ideation opening (CFD + imaging)
- Review emphasizes that "Manual segmentation remains the gold standard, but machine learning has significantly accelerated this process" and that "determining which complexities are essential, and which can be safely simplified, will be key to enabling clinical translation of these models." Suggests imaging segmentation fidelity and model robustness remain unresolved challenges for clinical deployment, but does not directly address coronary geometry-error cascading to hemodynamic decision-making.
