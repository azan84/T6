---
source_pdf_path: Resources/2501.08340v1.pdf
slug: mao-2025-coronaryhemodynamics
ledger_status: TRIAGED
---

# mao-2025-coronaryhemodynamics

## Bibliographic
- Title: CoronaryHemodynamics: An Automated Simulation Framework for Coronary Artery Hemodynamics Using OpenFOAM
- First author / authors (first 3 + et al.): Yijin Mao, Yuwen Zhang
- Year: 2025
- Venue: Preprint submitted to Computer Physics Communications
- DOI: NOT REPORTED

## One-line claim
An open-source OpenFOAM-based software package that automates the full CFD pipeline for coronary hemodynamics, including automatic boundary condition setup via Windkessel models parameterized by physiological metrics.

## T6 targeted questions
- **Q-A geometry perturbation**: The package handles "automatic geometry handling (e.g., STL file compatibility)." No discussion of systematic perturbation or inter-observer/inter-segmenter uncertainty quantification.
- **Q-B decision flip**: FFR is mentioned as "a gold-standard metric for assessing the functional severity of coronary artery stenosis" and vFFR (virtual FFR) is discussed. The software does NOT report decision-flip analysis or FFR reclassification results; it is a computational framework, not a validation study.
- **Q-C BC tuning**: CRITICAL FOR T6: The package "implements Windkessel boundary conditions at the aorta outlet and all coronary vessel outlets, with outlet parameters automatically derived from physiological metrics such as heart rate, systolic blood pressure, and myocardial volume." This is automatic, physiologically-informed BC setting. The software provides a unified pipeline but does NOT report whether re-tuning BCs after geometry perturbations compensates for errors.
- **Q-D fidelity / quantity**: Full 3D incompressible Navier-Stokes solver (steady-state via SIMPLE, transient via PIMPLE). "Flow rate and pressure data are recorded at all boundaries during the simulation, and outputs such as wall shear stress, pressure fields, and velocity fields are automatically stored." WSS is explicitly reported as an output.
- **Q-E data**: The package is designed for patient-specific geometries from CCTA. Demonstration and validation data are not reported in the abstract/intro; appears to be a methods/software paper.
- **Q-F meshing**: Uses cfMesh (adapted from third-party software) to generate "body-fitted cartesian mesh for the computational domain." Handles STL geometry files automatically. No detailed analysis of robustness on poor or topologically incorrect geometries.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Automated CFD pipeline with physiologically-informed Windkessel BC parameterization; provides software infrastructure for T6's BC tuning and sensitivity analysis workflow.
- verdict: LIGHT
- revisit-if: If paper reports validation results (FFR predictions vs invasive data) or sensitivity analysis of boundary condition parameters on hemodynamic outputs.
