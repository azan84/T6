---
source_pdf_path: Resources/1-s2.0-S2590093522000042-main.pdf
slug: chi-2022-multiscale-coupling
ledger_status: TRIAGED
---

# chi-2022-multiscale-coupling

## Bibliographic
- Title: Application of multiscale coupling models in the numerical study of circulation system
- First author / authors (first 3 + et al.): Zhang Chi, Lin Beile, Li Deyu et al.
- Year: 2022
- Venue: Medicine in Novel Technology and Devices
- DOI: Not explicitly stated in extract

## One-line claim
Review of multiscale hemodynamic modeling methods (0D lumped parameter, 1D distributed, 3D finite element) and their applications to cardiovascular disease simulation and clinical assessment.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Review paper on modeling methods; no empirical perturbation studies.
- **Q-B decision flip**: NOT REPORTED. No FFR threshold analysis or reclassification outcomes.
- **Q-C BC tuning**: Yes, discussed in context of multiscale coupling. "Reduced-order models (0D), alone or in combination with higher-dimensional models, are a computer-friendly alternative" and enables "tuned boundary conditions method." However, no specific statement on whether tuning is re-done after geometry change or compensates for error. Mentions "localized mesh, tuned boundary conditions method" for hemodynamic modeling.
- **Q-D fidelity / quantity**: Comprehensive review: 0D lumped parameter models, 1D distributed models, 3D CFD. Discusses WSS and other spatially-resolved hemodynamic parameters.
- **Q-E data**: Review paper; no original cohort. Cites cardiovascular research methodologies.
- **Q-F meshing**: Discusses multiscale mesh strategies and importance of "localized mesh" for reduced computational cost while maintaining accuracy in stenosis region; addresses robustness on complex geometry through coupling approach.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Comprehensive methodological review of 0D/1D/3D coupling strategies for coronary hemodynamics; relevant for understanding BC tuning and reduced-order model implementation but does not specifically address geometric error or topological robustness.
- verdict: FULL
- revisit-if: Case studies demonstrating 0D-3D coupling validation on patient-specific geometries with known segmentation error.
