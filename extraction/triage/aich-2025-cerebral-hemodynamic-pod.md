---
source_pdf_path: Resources/1-s2.0-S073519332501259X-main.pdf
slug: aich-2025-cerebral-hemodynamic-pod
ledger_status: TRIAGED
---

# aich-2025-cerebral-hemodynamic-pod

## Bibliographic
- Title: Pulsatile hemodynamic prediction in cerebral fusiform aneurysms using proper orthogonal decomposition model and long short-term memory networks
- First author / authors: Walid Aich, Joy Djuansjah, Ali B.M. Ali
- Year: 2025
- Venue: International Communications in Heat and Mass Transfer
- DOI: https://doi.org/10.1016/j.icheatmasstransfer.2025.109833

## One-line claim
Hybrid POD-LSTM surrogate model efficiently predicts transient hemodynamic parameters (WSS, OSI, pressure) in cerebral aneurysms as a computationally efficient alternative to full CFD.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper does not address geometry uncertainty or segmentation error.
- **Q-B decision flip**: NOT REPORTED. This is a CFD surrogate model paper, not clinical decision/FFR-based study.
- **Q-C BC tuning**: Outlet boundary conditions are specified as zero-pressure (traction-free) but NO statement about re-tuning after geometry change or whether tuning compensates for geometric error. BC strategy is standard and fixed, not adaptive.
- **Q-D fidelity / quantity**: High-fidelity 3D CFD (ANSYS-Fluent, unsteady Navier-Stokes with Casson non-Newtonian model). WSS and OSI are core outputs. Reduced-order surrogate (POD-LSTM) used post-hoc, not for filtering geometry. Spatial resolution preserved in reconstruction.
- **Q-E data**: Single patient-specific geometry (cerebral aneurysm), N=1 case shown. CFD simulations over 2+ cardiac cycles. No clinical cohort, no invasive FFR ground truth.
- **Q-F meshing**: Unstructured tetrahedral mesh with local refinement near aneurysmal dome, bifurcations, inflow/outflow. Inflation layers for wall boundary layer. Grid independence verified. No discussion of robustness to topologically incorrect or degenerate geometries.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: POD-LSTM temporal surrogate modeling is a computational efficiency technique potentially useful for T6's full-3D CFD arm, but paper does not address segmentation error, BC compensation, or decision-flip ranking.
- verdict: LIGHT
- revisit-if: Paper includes evaluation of model sensitivity to geometry perturbation or demonstrates that boundary condition tuning adapts to segmentation errors.

