---
source_pdf_path: Resources/011910_1_5.0244812.pdf
slug: li-2025-neural-network-coronary
ledger_id: C001
ledger_status: TRIAGED
---

# li-2025-neural-network-coronary

## Bibliographic
- Title: High performance neural network for solving coronary artery flow velocity field based on fluid component concentration
- First author / authors: Bao Li, Hao Sun, Yang Yang
- Year: 2025
- Venue: Physics of Fluids, vol. 37, no. 011910
- DOI: 10.1063/5.0244812

## One-line claim
A dual-path physics-data neural network (PDMNN) trained on 2255 CFD simulations predicts 3D coronary flow velocity fields from 3D point clouds and fluid concentration, achieving 180× speedup over traditional CFD while maintaining clinical accuracy.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No segmentation error or inter-observer variability analysis.
- **Q-B decision flip**: NOT REPORTED. No FFR or diagnostic reclassification analysis.
- **Q-C BC tuning**: NOT REPORTED. Paper states "PDMNN does not require measurement of boundary conditions" and only needs "geometric information and fluid component concentration information," but provides no details on BC parameterization, Windkessel, resistance tuning, or whether tuning is re-done post-geometry change.
- **Q-D fidelity / quantity**: 3D CFD via ANSYS-CFX for training. PDMNN predicts 3D flow velocity field. No WSS/OSI reported. Sensitivity to geometry changes NOT REPORTED.
- **Q-E data**: 205 patients with CCTA, private institutional data. Clinical verification cohort: 26 patients with transthoracic Doppler measurements. No invasive FFR ground truth.
- **Q-F meshing**: Tetrahedron-dominant grid, 0.2 mm (fluid) and 0.02 mm (surface), 5–10M elements. Five prismatic boundary layers near wall. Mesh dependency test performed. Robustness on poor/topologically-incorrect geometry NOT REPORTED.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Presents a deep-learning surrogate for rapid 3D CFD flow prediction with varying boundary conditions; relevant to T6 methodology but does not address segmentation error, geometry perturbation, or error propagation through BC tuning.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity analysis of PDMNN predictions to segmentation/geometry variations, or studies how geometry error affects downstream BC tuning or FFR prediction.

## Ideation opening (CFD + imaging)
- None stated. Paper presents a method for rapid CFD replacement but does not identify a research gap in CFD-imaging integration specific to geometry or segmentation uncertainty.
