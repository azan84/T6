---
source_pdf_path: Resources/s10237-026-02063-9.pdf
slug: bonini-2026-lvad-3d-0d
ledger_id: C036
ledger_status: TRIAGED
---

# bonini-2026-lvad-3d-0d

## Bibliographic
- Title: A monolithic patient-specific 3D–0D model for In silico investigation of hemodynamics in patients with left ventricular assist devices
- First author / authors: Mia Bonini, Marc Hirschvogel, Michael Ferguson (et al.)
- Year: 2026
- Venue: Biomechanics and Modeling in Mechanobiology 25:51
- DOI: https://doi.org/10.1007/s10237-026-02063-9

## One-line claim
Develops a monolithic coupled 3D CFD (left ventricle, atrium, aorta, LVAD) and 0D lumped parameter circulation model with automated parameter optimization to simulate patient-specific hemodynamics in LVAD-supported hearts.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Uses patient-specific CT segmentation. Notes segmentation challenges: "Due to pronounced metal-induced artifacts from the LVAD device, automated segmentation using neural networks was unreliable. As a result, semi-automatic and manual segmentation was performed." No uncertainty testing or perturbation analysis.
- **Q-B decision flip**: NOT REPORTED. Focuses on LVAD hemodynamics and valve regurgitation effects, not FFR or diagnostic thresholds.
- **Q-C BC tuning**: YES—EXTENSIVELY DESCRIBED. "Personalization of the model was performed by fitting all 23 parameters, including resistances, compliances, elastances, and areas of the valve regurgitant orifices, to available patient-specific data using a nonlinear least squares optimization framework." "Upon convergence, the optimized 0D parameters provided a patient-specific characterization of global cardiovascular dynamics." Model reproduced "available clinical targets with a mean error of 8.6%." NOT REPORTED: sensitivity of optimized parameters to geometry changes or whether tuning compensates for geometric error.
- **Q-D fidelity / quantity**: 3D CFD (Navier-Stokes) coupled to 0D circulation. Resolves "three-dimensional pressure and velocity fields in the left ventricle (LV), left atrium (LA), aortic root, and LVAD inflow and outflow cannulae." Valve dynamics governed by "transvalvular pressure and flow." NOT REPORTED: WSS/OSI in coronary arteries or sensitivity to geometry.
- **Q-E data**: N=1 case study. "63-year-old female on a LVAD support for 1.3 years" (Heartmate 3, 5400 rpm, 3.7 L/min flow). Data sources: "dynamic cardiac CT imaging, right heart catheterization (RHC), and echocardiography." NOT REPORTED: invasive FFR ground truth.
- **Q-F meshing**: Described. "A tetrahedral volume mesh with boundary layers was generated using SimModeler meshing tools. The resulting mesh had an average edge length of 1.0 mm, a refined mesh size of 0.5 mm at the valves, and refined boundary layers featuring a minimum edge length of 0.15 mm." Discontinuous mesh for pressure field across valves. NOT REPORTED: robustness on poor or topologically-incorrect geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates complete patient-specific 3D-0D CFD pipeline with automated BC parameter optimization (23-parameter fit), clinical validation framework, and hemodynamic interrogation methodology.
- verdict: FULL
- revisit-if: N/A (provides template for methodology, optimization validation, and clinical-to-simulation data integration).

## Ideation opening (CFD + imaging)
- Paper illustrates that manual segmentation was required due to metal artifacts; demonstrates that detailed 3D-0D patient-specific modeling requires "integration of imaging-based measurements of the heart and blood flow and invasive blood pressure measurements," suggesting imaging-derived geometry alone is insufficient and clinical multi-modality data integration is necessary for model personalization.
