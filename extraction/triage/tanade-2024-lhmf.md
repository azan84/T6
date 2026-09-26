---
source_pdf_path: Resources/s41746-024-01216-3.pdf
slug: tanade-2024-lhmf
ledger_status: TRIAGED
---

# tanade-2024-lhmf

## Bibliographic
- Title: Establishing the longitudinal hemodynamic mapping framework for wearable-driven coronary digital twins
- First author / authors: Cyrus Tanade, Nusrat Sadia Khan, Emily Rakestraw (et al.)
- Year: 2024
- Venue: npj Digital Medicine (Nature partnership with Seoul National University Bundang Hospital)
- DOI: 10.1038/s41746-024-01216-3

## One-line claim
A longitudinal hemodynamic mapping framework (LHMF) enables efficient computation of 3D coronary hemodynamics over months of wearable-derived physiological data, supporting persistent digital twins that evolve patient physiology.

## T6 targeted questions
- **Q-A geometry perturbation**: No geometry perturbation study. Uses patient-specific geometry from imaging. NOT REPORTED: segmentation uncertainty or inter-observer disagreement.
- **Q-B decision flip**: NOT REPORTED. Does not address FFR thresholds or diagnostic decision-flip rates.
- **Q-C BC tuning**: NOT REPORTED in front matter. Abstract mentions "boundary conditions reflecting varying activity states" but no detail on tuning strategy or Windkessel parameters.
- **Q-D fidelity / quantity**: 3D CFD for hemodynamics. Simulates "750 heartbeats" and "4.5 million heartbeats." NOT REPORTED: WSS/OSI sensitivity or spatial field analysis in front matter.
- **Q-E data**: Digital twins for individual patients with continuous physiological monitoring ("wearable-driven"). Invasive FFR ground truth: NOT REPORTED. "Current models match clinical flow measurements but are limited to single heartbeats" (improving on prior work).
- **Q-F meshing**: NOT REPORTED in front matter. Patient-specific geometry and meshing implied but robustness to segmentation error not addressed.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Develops computationally efficient 3D CFD framework (LHMF) for longitudinal hemodynamic simulation. Relevant for persistent digital twins but does not address geometry uncertainty, segmentation error, or BC-tuning compensation for topological error.
- verdict: LIGHT
- revisit-if: Full paper demonstrates LHMF stability under geometry perturbation, or compares hemodynamic predictions (FFR, pressure) when coronary segmentation varies.
