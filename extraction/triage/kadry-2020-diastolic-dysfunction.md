---
source_pdf_path: Resources/kadry-et-al-2020-biomechanics-of-diastolic-dysfunction-a-one-dimensional-computational-modeling-approach.pdf
slug: kadry-2020-diastolic-dysfunction
ledger_id: C033
ledger_status: TRIAGED
---

# kadry-2020-diastolic-dysfunction

## Bibliographic
- Title: Biomechanics of diastolic dysfunction: a one-dimensional computational modeling approach
- First author / authors: Karim Kadry, Stamatia Pagoulatou, Quentin Mercier (et al.)
- Year: 2020
- Venue: Am J Physiol Heart Circ Physiol 319: H882–H892
- DOI: 10.1152/ajpheart.00172.2020

## One-line claim
Develops a coupled 1D arterial network and 0D four-chamber cardiac model with biphasic relaxation delay and passive stiffness parameters to replicate three phenotypes of diastolic dysfunction.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No geometry perturbation or segmentation uncertainty addressed. Uses pre-validated model with fixed geometry.
- **Q-B decision flip**: NOT REPORTED. No FFR or diagnostic decision thresholds discussed. Focuses on mitral flow phenotypes (E/A ratios, deceleration times).
- **Q-C BC tuning**: Indirect relevance. Model uses "five-segment lumped parameter model (2-element Windkessel models connected in series)" for pulmonary circulation. NOT REPORTED: whether BC tuning changes with geometry changes, or whether tuning compensates for geometric error.
- **Q-D fidelity / quantity**: Reduced-order 0D/1D model (not 3D CFD). 1D arterial network coupled to 0D cardiac model. NOT REPORTED: WSS/OSI sensitivity to geometry. Focus is on pressure-volume relations, mitral flow patterns, and hemodynamic phenotypes.
- **Q-E data**: Uses patient-specific data (flow, pressure waveforms). Demonstrates on "healthy volunteer (non-invasive data) and synthetic coronary data." NOT REPORTED: invasive FFR ground truth, cohort size, or dataset name.
- **Q-F meshing**: NOT REPORTED. No segmentation or meshing details provided.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Develops 0D/1D reduced-order cardiac hemodynamics model for diastolic dysfunction, but does not address geometry uncertainty, FFR decision-flip classification, or CFD meshing robustness relevant to T6.
- verdict: LIGHT
- revisit-if: Full paper demonstrates how 0D/1D model parameter sensitivity extends to coronary CFD outlet BC selection, or shows validation against invasive coronary pressure/flow with FFR ground truth.

## Ideation opening (CFD + imaging)
- None stated. Paper focuses on cardiac chamber mechanics and diastolic dysfunction phenotypes, not coronary hemodynamics, imaging-derived segmentation, or CFD sensitivity.
