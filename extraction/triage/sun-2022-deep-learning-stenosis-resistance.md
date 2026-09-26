---
source_pdf_path: Resources/sun-et-al-2022-deep-learning-based-prediction-of-coronary-artery-stenosis-resistance.pdf
slug: sun-2022-deep-learning-stenosis-resistance
ledger_status: TRIAGED
---

# sun-2022-deep-learning-stenosis-resistance

## Bibliographic
- Title: Deep learning-based prediction of coronary artery stenosis resistance
- First author / authors (first 3 + et al.): Hao Sun, Jincheng Liu, Yili Feng et al.
- Year: 2022
- Venue: American Journal of Physiology - Heart and Circulatory Physiology
- DOI: 10.1152/ajpheart.00269.2022

## One-line claim
A back-propagation neural network trained on 3D CFD simulations of stenosis models predicts stenosis resistance rapidly and accurately for non-invasive FFRCT calculation from geometric parameters and blood flow.

## T6 targeted questions
- **Q-A geometry perturbation**: Synthetic perturbation. Training dataset of 3,028 idealized anatomic coronary artery models with stenotic percent range 30–90%, entrance diameter 1–6 mm, stenotic length 2–20 mm, model length 22–120 mm. No inter-observer disagreement.
- **Q-B decision flip**: FFR ≤0.80 revascularization threshold mentioned; BPNN-calculated FFRCT vs invasive FFR validation: 96.67% accuracy, r=0.94, P<0.001.
- **Q-C BC tuning**: Inlet flow rate prescribed (0.8–6 mL/s); outlet static pressure 0 Pa. 3D CFD used to fine-tune resistance coefficients based on Young & Tsai experiments. Vessel elasticity considered; stated to "substantially alter the physics" and "modulate pressure and pressure wave velocity." No explicit statement that tuning is re-done after geometry change.
- **Q-D fidelity / quantity**: 3D CFD simulations (ANSYS-CFX) for training; results compared against 0D analytical model; did not report WSS/OSI.
- **Q-E data**: 30 patient-specific coronary models from Peking University People's Hospital (2021–2022); CCTA + invasive FFR with pressure wire under adenosine-induced hyperemia; invasive FFR < 0.80 considered significant.
- **Q-F meshing**: Hexahedral mesh with 8 nodes; mesh dependency analysis performed; mean mesh elements 865,054 ± 287,368; maximum mesh size 0.892 mm. Boundary layer constructed for each fluid mesh.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates ML surrogate for stenosis resistance calculation; validates accuracy on patient-specific CFD and invasive FFR; relevant for rapid FFRCT without full 3D CFD cost.
- verdict: FULL
- revisit-if: Check whether boundary conditions or resistance model parameters require re-tuning when vessel geometry is perturbed; examine sensitivity analysis for topologically incorrect segmentations.
