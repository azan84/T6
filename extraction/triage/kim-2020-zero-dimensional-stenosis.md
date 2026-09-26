---
source_pdf_path: Resources/1-s2.0-S0021929020305005-main.pdf
slug: kim-2020-zero-dimensional-stenosis
ledger_id: C004
ledger_status: TRIAGED
---

# kim-2020-zero-dimensional-stenosis

## Bibliographic
- Title: A zero-dimensional predictive model for the pressure drop in the stenotic coronary artery based on its geometric characteristics
- First author / authors: Jaerim Kim, Dohyun Jin, Haecheon Choi
- Year: 2020
- Venue: Journal of Biomechanics, vol. 113
- DOI: 10.1016/j.jbiomech.2020.110076

## One-line claim
A 0D model combining curved-pipe theory and machine learning predicts pressure drop across patient-specific coronary stenoses from geometric parameters (curvature, area stenosis), validated against 3D CFD for 33 CCTA-derived cases with R²=0.96–0.98.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Analysis of 33 patient-specific stenoses by geometric characteristics (curvature, area reduction); no measurement of segmentation error, inter-observer variability, or inter-segmenter disagreement.
- **Q-B decision flip**: NOT REPORTED. No FFR reclassification at 0.80 threshold or any diagnostic decision analysis reported.
- **Q-C BC tuning**: Outlet BC uses resistance to represent coronary microcirculation; no Windkessel, Murray's law, or allometric tuning details provided. Re-tuning after geometry change NOT REPORTED. No statement that BC tuning compensates for geometric error.
- **Q-D fidelity / quantity**: 3D CFD (unsteady Navier-Stokes, Reynolds 100–500) for reference; 0D model predicts pressure drop across stenosis only, not full 3D velocity field. WSS/OSI NOT REPORTED. Sensitivity of predictions to segmentation variation NOT EXPLICITLY ANALYZED.
- **Q-E data**: 33 stenoses from 31 patients, CCTA-derived, private institutional data (Asan Medical Center, Seoul). No invasive FFR ground truth used for validation.
- **Q-F meshing**: Tetrahedron-dominant mesh, 1–2 million elements. Manual correction of reference area (Aref) required for a few cases. Robustness on poor or topologically-incorrect geometry NOT REPORTED.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates that vessel geometry (particularly curvature) significantly influences pressure drop via 3D CFD-derived 0D model; relevant to understanding geometric effects but does not address segmentation error sources or error propagation through BC tuning to FFR decisions.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity of 0D model predictions to segmentation variations, or validation against invasive FFR measurements showing how geometry uncertainty affects clinical decision thresholds.

## Ideation opening (CFD + imaging)
- None stated. Paper addresses computational efficiency (0D vs 3D CFD) but does not identify a research gap in CFD-imaging integration for segmentation or geometry uncertainty quantification.
