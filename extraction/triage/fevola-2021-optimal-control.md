---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2021 - Fevola - An optimal control approach to determine resistance‐type boundary conditions.pdf
slug: fevola-2021-optimal-control
ledger_status: TRIAGED
---

# fevola-2021-optimal-control

## Bibliographic
- Title: An optimal control approach to determine resistance-type boundary conditions from in-vivo data for cardiovascular simulations
- First author / authors (first 3): Elisa Fevola, Francesco Ballarin, Laura Jiménez-Juan
- Year: 2021
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3516

## One-line claim
A variational optimal control method automatically calibrates resistance-type outlet boundary conditions (Windkessel model parameters) from patient-specific 4D-Flow MRI data, outperforming manual tuning via Murray's law or Ohm's law, and enabling accurate patient-specific hemodynamic simulation without expensive manual parameter estimation.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb coronary geometry. Uses patient-specific aortic arch models reconstructed from clinical CT images; focus is on BC parameter estimation, not segmentation error.
- **Q-B decision flip**: NOT focus. Paper addresses aortic arch hemodynamics; FFR (FFR context mentioned but not central to this aortic application).
- **Q-C BC tuning**: **CENTRAL FOCUS**. Explicit motivation: "The choice of appropriate boundary conditions is a fundamental step in computational fluid dynamics simulations of the cardiovascular system. Boundary conditions...highly affect the computed pressure and flow rates, and consequently haemodynamic indicators such as wall shear stress (WSS)." States the challenge: "the most common techniques do not automatically assimilate patient-specific data, relying instead on expensive and time-consuming manual tuning." Proposes optimal control method where resistance parameters are control variables tuned to minimize mismatch between simulated and measured 4D-Flow MRI velocity. Compares three BC calibration strategies: Murray's law (physiological scaling), Ohm's law (flow-pressure analogue), and **optimal control (data-assimilation)**. Quote: "optimal control...assimilates a set of patient-specific measurements...tuning the parameters of a three-element Windkessel model." Results demonstrate optimal control assimilates 4D-Flow MRI data more accurately than fixed-parameter methods.
- **Q-D fidelity / quantity**: 3D CFD using steady Stokes equations (linearized Navier-Stokes) on aortic arch; 4D-Flow MRI data (time-resolved 3D velocity) used as ground truth for BC tuning. Outputs include pressure, flow, WSS, and OSI.
- **Q-E data**: 4 patient-specific aortic arch cases from Sunnybrook Health Sciences Centre (Toronto, Canada). 4D-Flow MRI measurements as BC constraint data; invasive pressure measurements. Post-CABG surgery patients. Private institutional data.
- **Q-F meshing**: CT-based vessel reconstruction using SimVascular; tetrahedral mesh generation via TetGen. NO detailed segmentation robustness analysis.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Automated BC parameter calibration via optimal control from patient 4D-Flow MRI data; demonstrates that data-driven tuning outperforms population-based law (Murray's law) for patient-specific hemodynamic accuracy.
- verdict: FULL
- revisit-if: Already directly applicable; extends optimal control framework to coronary-specific BC tuning from invasive/4D-Flow data.

