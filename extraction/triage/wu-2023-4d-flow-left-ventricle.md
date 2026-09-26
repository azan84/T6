---
source_pdf_path: Resources/s13239-023-00684-0.pdf
slug: wu-2023-4d-flow-left-ventricle
ledger_status: TRIAGED
---

# wu-2023-4d-flow-left-ventricle

## Bibliographic
- Title: 4D Flow Patterns and Relative Pressure Distribution in a Left Ventricle Model by Shake-the-Box and Proper Orthogonal Decomposition Analysis
- First author / authors (first 3 + et al.): Wu X, Saaid H, Voorneveld J, et al.
- Year: 2023
- Venue: Cardiovascular Engineering and Technology
- DOI: 10.1007/s13239-023-00684-0

## One-line claim
Shake-the-Box particle tracking and POD analysis reconstruct 4D velocity and pressure fields in a realistic left ventricle silicone model in vitro, validating non-invasive hemodynamic measurement techniques for clinical biomarker development.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (in vitro model study with biological valves; no geometry perturbation or inter-observer segmentation error)
- **Q-B decision flip**: NOT REPORTED (not applicable; study is on LV hemodynamics, not coronary FFR or stenosis decision-making)
- **Q-C BC tuning**: NOT REPORTED (in vitro experimental validation; no BC tuning or CFD calibration)
- **Q-D fidelity / quantity**: **High-fidelity experimental 4D flow measurement**. Time-resolved particle tracking (Shake-the-Box) in silicone LV model with 3D velocity reconstruction and Poisson-based pressure solver. Provides spatially-resolved pressure and velocity; not computational modeling.
- **Q-E data**: Single LV silicone model with biological valves; experimental in vitro. Maximal pressure difference ~2.7 mmHg base-to-apex (matches in vivo values). No patient cohort; proof-of-concept methodology.
- **Q-F meshing**: NOT REPORTED (experimental optical method, not mesh-based)

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Focuses on LV hemodynamics via particle tracking, not coronary geometry/FFR or BC-tuning methodologies. In vitro experimental validation of measurement techniques; outside T6's coronary CFD/segmentation error scope.
- verdict: LIGHT
- revisit-if: Paper applies to coronary stenosis geometry or discusses error propagation in pressure reconstruction from flow

