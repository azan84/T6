---
source_pdf_path: Resources/s10237-024-01873-z.pdf
slug: montino-pelagi-2024-microcirculation
ledger_status: TRIAGED
---

# montino-pelagi-2024-microcirculation

## Bibliographic
- Title: Modeling cardiac microcirculation for the simulation of coronary flow and 3D myocardial perfusion
- First author / authors (first 3 + et al.): Giovanni Montino Pelagi, Francesco Regazzoni, Jacques M. Huyghe et al.
- Year: 2024
- Venue: Biomechanics and Modeling in Mechanobiology
- DOI: 10.1007/s10237-024-01873-z

## One-line claim
Multi-compartment Darcy model of coronary microcirculation coupled with 3D epicardial flow reproduces hyperemic coronary blood flow and myocardial perfusion heterogeneity including cardiac contraction effects.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Patient-specific models without synthetic perturbations or segmentation uncertainty studies.
- **Q-B decision flip**: NOT REPORTED. Focus on perfusion mapping and myocardial blood flow (MBF), not FFR-based diagnostic classification.
- **Q-C BC tuning**: Multi-compartment Darcy LPMs at microvascular outlets with compliance and resistance parameters. No discussion of BC re-tuning after geometry change or compensation for topological error. "The coronary LPMs at each coronary outlet are coupled to the heart model LPM to reproduce the diastolic-dominated flow waveform arising from myocardial compression." Data-driven calibration of Darcy parameters, but no statement on tuning strategy for absorbing geometric uncertainties.
- **Q-D fidelity / quantity**: Hybrid 3D epicardial Navier-Stokes + 0D multiscale Darcy microcirculation. WSS not explicitly stated; focus on MBF, pressure, flow patterns, and systolic-diastolic flow heterogeneity.
- **Q-E data**: Multiple patient-specific geometries from CT imaging; real invasive FFR ground truth not mentioned for validation.
- **Q-F meshing**: Patient-specific coronary geometries from CT; segmentation and mesh preprocessing not detailed. Multi-compartment Darcy formulation on epicardial domain with microvascular homogenization.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Advanced multiscale CFD method for epicardial+microvascular hemodynamics with cardiac contraction coupling. Does not address segmentation error handling, topological robustness, or BC tuning hypothesis.
- verdict: LIGHT
- revisit-if: Study reports sensitivity of MBF or FFR to segmentation quality variations or discusses robust BC calibration under geometric uncertainty.

