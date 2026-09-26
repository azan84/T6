---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2021 - Jonášová - On the relevance of boundary conditions and viscosity models in blood flow.pdf
slug: jonasova-2021-relevance
ledger_status: TRIAGED
---

# jonasova-2021-relevance

## Bibliographic
- Title: On the relevance of boundary conditions and viscosity models in blood flow simulations in patient-specific aorto-coronary bypass models
- First author / authors (first 3): Alena Jonášová, Jan Vimmr
- Year: 2021
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3439

## One-line claim
A multiscale hemodynamic study on 3 patient-specific coronary bypass geometries demonstrates that lumped parameter outlet boundary condition models (especially those incorporating intramyocardial pressure) produce physiologically realistic coronary flow patterns superior to constant pressure BCs, and that blood rheology transitions from Newtonian to shear-thinning behavior in regions of geometry disturbance.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb or systematically measure inter-observer segmentation disagreement. Analyzes 3 real patient-specific bypass geometries (single/double/triple grafts) reconstructed from CT with occluded native coronaries (by design, to focus on bypass hemodynamics).
- **Q-B decision flip**: Mentions FFR ≤0.80 as clinical standard for hemodynamically significant lesions in context of bypass assessment. NO explicit FFR ≤0.80 decision classification study or flip-rate analysis reported.
- **Q-C BC tuning**: **CRITICAL FOCUS**. Explicitly states motivation: "the prescribed boundary conditions...have to be chosen very carefully...many studies used constant pressure as an outlet boundary condition...cannot reproduce the unique coronary haemodynamics and...yields physiologically unrealistic results." Systematically compares 5 types of outlet BCs: (1) mean arterial pressure, (2) three-element Windkessel, (3) lumped parameter model 1 (LPM-1), (4) LPM-2, (5) LPM-3. Conclusion: "the best option in terms of physiological characteristics...the lumped parameter models...notably superior...in comparison to the constant outlet pressure, which...gave overestimated and physiologically misleading results." BCs chosen to match known physiological intramyocardial pressure effects (diastolic coronary flow dominance). Does NOT explicitly state BC tuning compensates for geometric error, but strong emphasis on BC choice being critical for correct FFR/hemodynamic prediction.
- **Q-D fidelity / quantity**: 3D CFD with fluid-structure interaction (deformable vessel walls); multiscale approach coupling 3D domain with 0D lumped parameter network. Reports pressure, flow, wall shear stress (WSS), and wall deformation. Compares Newtonian and two non-Newtonian viscosity models (Carreau-Yasuda, modified Cross).
- **Q-E data**: 3 patient-specific aorto-coronary bypass geometries from clinical cases; no explicit cohort size or invasive ground-truth validation reported in extracted text.
- **Q-F meshing**: Geometries from CT angiography using Mimics segmentation and CATIA refinement (same as Tajeddini 2020). Unstructured tetrahedral meshing (362k–879k elements). NO explicit robustness analysis on poor/broken geometries.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Direct evidence that outlet BC choice (lumped parameter vs. constant pressure) critically affects hemodynamic realism and FFR accuracy in coronary models; multiscale modeling framework with physiologically appropriate BCs (incorporating intramyocardial pressure) produces superior coronary flow predictions.
- verdict: FULL
- revisit-if: Already highly relevant; demonstrates BC importance for coronary FFR accuracy.

