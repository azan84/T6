---
source_pdf_path: Resources/rsif.2024.0774.pdf
slug: barzegar-2025-surrogate-carotid
ledger_status: TRIAGED
---

# barzegar-2025-surrogate-carotid

## Bibliographic
- Title: A predictive surrogate model of blood haemodynamics for patient-specific carotid artery stenosis
- First author / authors: Mostafa Barzegar Gerdroodbary, Sajad Salavatidezfouli
- Year: 2025
- Venue: Journal of the Royal Society Interface
- DOI: 10.1098/rsif.2024.0774

## One-line claim
POD + LSTM machine learning predicts blood pressure and wall shear stress in stenotic carotid arteries with clinical-scale stenosis magnitudes, reducing CFD cost.

## T6 targeted questions
- **Q-A geometry perturbation**: No—uses artificially introduced stenosis in patient-specific or idealized carotid geometry, not measured inter-observer disagreement or synthetic error injection.
- **Q-B decision flip**: NOT ADDRESSED—focus is hemodynamics prediction, not FFR binary classification.
- **Q-C BC tuning**: No tuning discussion. Standard approach: "mass flow rate of normal body activity is applied at the inlet while outflow is outlet pressure equivalent to the real condition of the bloodstream exit from the carotid artery."
- **Q-D fidelity / quantity**: 3D CFD via ANSYS FLUENT with URANS k–ω SST turbulence model. Generates pressure, velocity, and WSS fields; then applies POD + LSTM for surrogate prediction across cardiac cycle.
- **Q-E data**: Artificial carotid geometry with single stenosis size (radius 4.2 mm); no patient cohort, no invasive reference.
- **Q-F meshing**: Detailed mesh independence study; grid independence verified with y+~1 and 7 boundary layers near vessel wall. No detail on robustness to segmentation error in real geometries.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates reduced-order surrogate modeling (POD + LSTM) for hemodynamic prediction; applicable to accelerating FFR computation if geometry segmentation is reliable, but limited to idealized geometry.
- verdict: LIGHT
- revisit-if: Only if T6 pursues reduced-order surrogates for speed; note: carotid not coronary, and no topological error robustness assessment.
