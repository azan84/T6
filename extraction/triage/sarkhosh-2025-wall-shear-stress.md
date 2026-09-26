---
source_pdf_path: Resources/fphys-16-1518732.pdf
slug: sarkhosh-2025-wall-shear-stress
ledger_status: TRIAGED
---

# sarkhosh-2025-wall-shear-stress

## Bibliographic
- Title: Prediction of time averaged wall shear stress distribution in coronary arteries' bifurcation varying in morphological features via deep learning
- First author / authors (first 3 + et al.): Sarkhosh MH, Edrisnia H, Raveshi MR, Sharbatdar M
- Year: 2025
- Venue: Frontiers in Physiology
- DOI: 10.3389/fphys.2025.1518732

## One-line claim
Deep neural networks trained on CFD-derived hemodynamic datasets predict time-averaged wall shear stress (TAWSS) in coronary bifurcations with 2.53% error, enabling rapid surrogate model evaluation.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Studies geometry-to-hemodynamics mapping via ML but does not perturb or measure lumen/segmentation uncertainty.
- **Q-B decision flip**: NOT REPORTED. Predicts TAWSS, not FFR or diagnostic classification; no decision threshold or reclassification analysis.
- **Q-C BC tuning**: PARTIALLY REPORTED. "appropriate boundary conditions, and material properties" mentioned. "flat velocity boundary condition is applied at the inlet...boundary conditions are simulated using the finite volume method." No detail on outlet BC specification, Windkessel tuning, or resistance parameterization.
- **Q-D fidelity / quantity**: 3D CFD (training only). Reference CFD simulations (ANSYS FLUENT) computed on synthetic coronary bifurcation geometries; ML model predicts TAWSS and other spatially-resolved fields. YES, reports WSS (TAWSS).
- **Q-E data**: Synthetic parametric bifurcation geometries generated via CAD; no clinical patient data. Training dataset size not explicitly stated.
- **Q-F meshing**: YES, described. "2D image segmentation and 3D point cloud segmentation...ANSYS meshing...Mesh type" used to create computational fluid domain. Focuses on parametric synthetic geometries; no sensitivity to real segmentation error or topological defects.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates ML-based surrogate for rapid 3D CFD-derived hemodynamic prediction (WSS/TAWSS), potentially useful for T6's secondary 3D OpenFOAM validation arm, but on synthetic geometries only.
- verdict: LIGHT
- revisit-if: If T6 adopts neural-network surrogates for full 3D CFD screening; however, current focus likely on real segmentation error effects, not ML acceleration on healthy synthetic anatomy.
