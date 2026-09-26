---
source_pdf_path: Resources/s40323-020-00186-x.pdf
slug: arthurs-2020-bc-estimation
ledger_status: TRIAGED
---

# arthurs-2020-bc-estimation

## Bibliographic
- Title: A flexible framework for sequential estimation of model parameters in computational hemodynamics
- First author / authors: Christopher J. Arthurs, Nan Xiao, Philippe Moireau (et al.)
- Year: 2020
- Venue: Advanced Modeling and Simulation in Engineering Sciences 7:48
- DOI: 10.1186/s40323-020-00186-x

## One-line claim
A Reduced-Order Unscented Kalman Filter (ROUKF) framework for automated data assimilation can calibrate patient-specific boundary condition parameters (Windkessel, LPN) and wall material properties in 3D hemodynamic models.

## T6 targeted questions
- **Q-A geometry perturbation**: No geometry perturbation. Uses patient-specific geometry. NOT REPORTED: segmentation or inter-observer uncertainty.
- **Q-B decision flip**: NOT REPORTED. Does not address FFR or diagnostic decision thresholds.
- **Q-C BC tuning**: YES—CORE CONTRIBUTION. "A primary challenge in constructing patient-specific models is the determination of parameters (LPN or structural stiffness) which make the simulation results agree with clinical data." Develops ROUKF and ROUKF-CLS methods for automated three-element Windkessel parameter estimation. Abstract: "A constrained least squares augmentation (ROUKF-CLS) for more complex LPNs." Demonstrated on patient-specific aortic data and synthetic coronary LPN. NOT REPORTED: whether tuning changes when geometry is perturbed, or whether tuning can compensate for geometric error.
- **Q-D fidelity / quantity**: 3D Navier–Stokes FSI with coupled LPN boundary conditions. NOT REPORTED: WSS/OSI sensitivity to geometry.
- **Q-E data**: Patient-specific data (anatomy, flow, pressure waveforms, wall motion). Invasive FFR: NOT REPORTED. Demonstrated on healthy volunteer (non-invasive data) and synthetic coronary data.
- **Q-F meshing**: NOT REPORTED. Finite element mesh generation mentioned as part of CRIMSON software; no segmentation robustness details.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Develops automated BC tuning algorithm (ROUKF/ROUKF-CLS) for Windkessel and complex LPN calibration. Core T6 tool if reapplied to geometry-perturbed cases.
- verdict: LIGHT
- revisit-if: Full paper demonstrates ROUKF parameter estimates on real coronary cases with clinically-measured FFR ground truth, or shows parameter stability/changes under geometry uncertainty.
