---
source_pdf_path: Resources/PIIS2405844024064351.pdf
slug: aramburu-2024-fontan-patient-specific
ledger_id: C027
ledger_status: TRIAGED
---

# aramburu-2024-fontan-patient-specific

## Bibliographic
- Title: Patient-specific closed-loop model of the Fontan circulation: Calibration and validation
- First author / authors (first 3 + et al.): Aramburu J, Ruijsink B, Chabiniok R
- Year: 2024
- Venue: Heliyon
- DOI: 10.1016/j.heliyon.2024.e30404

## One-line claim
A patient-specific 1D/0D closed-loop hemodynamic model calibrated with invasive CMR data accurately predicts pulsatile hemodynamics in Fontan circulation and enables virtual testing of clinical interventions.

## T6 targeted questions
- **Q-A geometry perturbation**: Mentions "This approach enables geometrical variations, such as aortic coarctation or compression of the LPA by the aorta." However, these are not about segmentation/lumen uncertainty or inter-observer disagreement. Geometry obtained from "manual measurement directly from the magnetic resonance images." No quantification of measurement error, segmentation uncertainty, or sensitivity to geometry perturbations.
- **Q-B decision flip**: No FFR computation, no diagnostic threshold evaluation. Not applicable to Fontan circulation (different clinical context than coronary disease). NOT REPORTED.
- **Q-C BC tuning**: Uses 0D Windkessel models for peripheral circulation: "the remaining parts of the cardiovascular system—upper body, lower body, lungs, and heart—were lumped into 0-D Windkessel models." Parameters estimated via "physics-based stepwise methodology" and manual adjustment for elastance functions. No statement on whether tuning compensates for anatomical error or re-tuning after geometry change.
- **Q-D fidelity / quantity**: Hybrid 1D/0D: aorta and TCPC in 1D, remaining circulation in 0D. No 3D CFD, no WSS/OSI. Outputs are pressure and flow waveforms.
- **Q-E data**: N=1 patient (10-year-old, anesthetised, hypoplastic left heart syndrome with Fontan circulation). Clinical data from combined cardiac catheterisation and CMR (invasive CMR). Real patient data but congenital heart disease context, no invasive FFR ground truth.
- **Q-F meshing**: 1D model of large vessels with "calibre and length... manually measured, directly from magnetic resonance images." No 3D segmentation→surface→volume meshing, no assessment of robustness to poor or topologically incorrect geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates patient-specific 1D/0D model calibration using combined invasive and imaging data, relevant for T6's methodology of patient-specific parameter estimation and validation against clinical measurements.
- verdict: LIGHT
- revisit-if: If paper discusses geometry measurement error propagation, sensitivity to segmentation variation, or demonstrates that model predictions are robust to plausible changes in manually-measured vessel dimensions.

## Ideation opening (CFD + imaging)
Paper notes that manual measurement directly from MRI images was used and that "ensuring proper alignment of flow and pressure signals in time during model calibration is crucial due to the asynchronous nature of iCMR data acquisition... [which] can introduce inconsistencies in the data." Suggests a gap in how imaging-derived geometry measurement error and temporal acquisition misalignment affect hemodynamic model predictions.
