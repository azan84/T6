---
source_pdf_path: Resources/s10439-021-02841-9.pdf
slug: antonuccio-2021-aortic-coarctation
ledger_status: TRIAGED
---

# antonuccio-2021-aortic-coarctation

## Bibliographic
- Title: Effects of Uncertainty of Outlet Boundary Conditions in a Patient-Specific Case of Aortic Coarctation
- First author / authors (first 3 + et al.): Maria Nicole Antonuccio, Alessandro Mariotti, Benigno Marco Fanni et al.
- Year: 2021
- Venue: Annals of Biomedical Engineering, Vol. 49, No. 12, December 2021
- DOI: 10.1007/s10439-021-02841-9

## One-line claim
- Generalized polynomial chaos (gPC) stochastic analysis quantifies sensitivity of aortic coarctation hemodynamics to uncertainty in 3-element Windkessel outlet boundary condition tuning parameters.

## T6 targeted questions
- **Q-A geometry perturbation**: Does not perturb; models real patient-specific aortic coarctation from MRI before and after stenting. Geometry is fixed; no inter-observer segmentation variation studied.
- **Q-B decision flip**: NOT REPORTED — pressure gradient (ΔP) measured invasively across CoA; no binary classification threshold or reclassification analysis.
- **Q-C BC tuning**: Central focus: 3-element Windkessel (3WKM) with proximal resistance Rp, distal resistance Rd, compliance C. Proposes optimization + fine-tuning procedure to calibrate resistances. Shows that fine-tuning of 3WKM is "not strictly necessary" for post-stenting (physiological) cases but important pre-stenting (diseased). NO statement that tuning COMPENSATES for geometric error; rather, tunes outlet model itself to match clinical pressure data.
- **Q-D fidelity / quantity**: 3D CFD (Navier-Stokes, incompressible, Newtonian blood) with pulsatile MRI-based inlet waveforms. Computes pressure drop, flow rate, TAWSS (time-averaged wall shear stress). No OSI or spatially-resolved ischemia indices.
- **Q-E data**: Single pediatric patient (12 years old) with aortic coarctation; cMRI with phase-contrast velocity data and invasive catheter pressure pre- and post-stenting (endovascular repair). Private clinical data (Great Ormond Street Hospital).
- **Q-F meshing**: Tetrahedral mesh (1.2 mm element size, ~1.7M elements pre-stenting); prism layer at wall. Mesh sensitivity tested via WSS. Standard processing in ITK-SNAP and SimVascular. No robustness testing on poor/broken geometry.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Aortic (not coronary) domain; focus on outlet BC uncertainty quantification (gPC) rather than error compensation or geometric sensitivity ranking; no tissue-level perfusion or binary decision metrics.
- verdict: LIGHT
- revisit-if: Methodology (gPC for BC uncertainty) is transferable; revisit if T6 adopts similar uncertainty quantification for coronary outlet tuning.
