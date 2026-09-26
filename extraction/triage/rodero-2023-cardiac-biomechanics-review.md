---
source_pdf_path: Resources/fphy-11-1306210.pdf
slug: rodero-2023-cardiac-biomechanics-review
ledger_id: C030
ledger_status: TRIAGED
---

# rodero-2023-cardiac-biomechanics-review

## Bibliographic
- Title: Advancing clinical translation of cardiac biomechanics models: a comprehensive review, applications and future pathways
- First author / authors (first 3 + et al.): Rodero C, Baptiste TMG, Barrows RK
- Year: 2023
- Venue: Frontiers in Physics
- DOI: 10.3389/fphy.2023.1306210

## One-line claim
A comprehensive review of cardiac biomechanics models (passive/active mechanics, cell models, lumped-parameter circulatory models, electromechanics) and their clinical translation pathways, emphasizing mesh generation, model calibration, validation, and clinical applications.

## T6 targeted questions
- **Q-A geometry perturbation**: Paper discusses mesh generation from CT/MRI imaging but does not address lumen segmentation uncertainty or inter-observer disagreement in coronary vessel diameter/geometry measurement. NOT REPORTED on magnitude of segmentation-induced geometry variation.
- **Q-B decision flip**: No FFR, no diagnostic threshold evaluation. Not applicable to cardiac mechanics focus (heart contraction mechanics, not coronary hemodynamics). NOT REPORTED.
- **Q-C BC tuning**: Extensively discusses boundary conditions in cardiac models: "nonphysiological boundary conditions that require extensive parameter tuning to match the simulated motion with data." Mentions that "four-chamber models... avoid the need for an unphysiological spatial boundary condition on the base or apex." No explicit discussion of BC re-tuning in response to geometry change or whether tuning compensates for measurement error.
- **Q-D fidelity / quantity**: Covers 0D (lumped-parameter), 1D, and 3D finite-element models of cardiac chambers. No direct coronary CFD modeling; focuses on ventricular/atrial mechanics, not coronary hemodynamics or WSS in coronary arteries.
- **Q-E data**: Patient-specific models calibrated with clinical data (CT, MRI, pressure catheters). Cardiac-focused; no invasive FFR ground truth, no coronary patient cohort.
- **Q-F meshing**: Detailed discussion of mesh generation: "generate anatomical meshes ready for simulations." Mentions uncertainties (e.g., "fiber direction... associated with an uncertainty of about 10°"). Discusses segmentation from imaging (CT, MRI) but focused on cardiac chambers, not coronary vessel segmentation robustness to threshold/method variation.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive review of patient-specific computational modeling, mesh generation, boundary condition tuning, and uncertainty quantification in cardiac biomechanics; methods are translatable to hemodynamic modeling but focuses on ventricular/atrial mechanics, not coronary FFR-CT.
- verdict: LIGHT
- revisit-if: If paper discusses geometry measurement uncertainty quantification, mesh sensitivity analysis, or boundary condition compensation strategies relevant to vessel segmentation or CFD model robustness.

## Ideation opening (CFD + imaging)
Paper notes that "medical device" regulatory frameworks and "verification and validation requirements" for computational models are underdeveloped, and emphasizes that "model complexity must be balanced with the associated high computational cost." Suggests a gap in standardized approaches to validating imaging-derived hemodynamic models and assessing model reliability in clinical translation.
