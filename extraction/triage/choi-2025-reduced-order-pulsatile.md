---
source_pdf_path: Resources/1-s2.0-S0169260725004110-main.pdf
slug: choi-2025-reduced-order-pulsatile
ledger_status: TRIAGED
---

# choi-2025-reduced-order-pulsatile

## Bibliographic
- Title: Developing a reduced order model for pulsatile blood flow simulations using minimal three-dimensional simulation data
- First author / authors (first 3 + et al.): Wonjin Choi, Inpyo Lee, Hyun Jin Kim
- Year: 2025
- Venue: Computer Methods and Programs in Biomedicine 271 (2025) 108994
- DOI: 10.1016/j.cmpb.2025.108994

## One-line claim
Proposes a 1D reduced-order model (ROM) that derives parameters directly from three 3D CFD simulations per patient, eliminating empirical constants and enabling automatic adaptation to patient-specific geometries.

## T6 targeted questions

- **Q-A geometry perturbation**: Does NOT perturb segmentation. Validates against full 3D simulations on idealized and patient-specific geometries without perturbation study.

- **Q-B decision flip**: NOT REPORTED in excerpt. Focus is on computational efficiency and accuracy for pressure-flow relationships, not FFR threshold decision-making.

- **Q-C BC tuning**: YES. Core method: "we propose a one-dimensional ROM derived directly from three three-dimensional (3D) simulations per patient, eliminating the need for global empirical constants and enabling automatic adaptation to local anatomical features such as vessel size, curvature, bifurcations, and serial stenoses." Model coefficients "can be adjusted to simulate physiological and geometrical changes." Compared favorably with empirical stenosis model.

- **Q-D fidelity / quantity**: Uses 3D CFD for parameter derivation, 1D ROM for fast prediction. Validates against full 3D CFD. Does NOT explicitly report WSS/OSI but mentions FSI simulations: "fluid–structure interaction (FSI) simulations that account for both blood flow and vessel wall dynamics can provide a more realistic representation."

- **Q-E data**: Patient-specific geometries (coarcted aorta, coronary artery with serial lesions). No invasive ground truth in this excerpt.

- **Q-F meshing**: Discusses patient-specific geometry handling and adaptability to anatomical features (bifurcations, stenoses, curvature) but limited detail on meshing robustness on broken or topologically incorrect geometry.

## Novelty bearing on T6

- bucket: METHOD
- one-line reason: ROM parameter derivation from 3D simulations avoids empirical constants; technique relevant to T6's boundary condition optimization strategy and automated parameter fitting.
- verdict: LIGHT
- revisit-if: Paper demonstrates how ROM parameter tuning compensates for segmentation errors or topological uncertainty in patient-specific models.
