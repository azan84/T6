---
source_pdf_path: Resources/s10439-024-03453-9.pdf
slug: pelagi-2024-pressure-coronary
ledger_status: TRIAGED
---

# pelagi-2024-pressure-coronary

## Bibliographic
- Title: Personalized Pressure Conditions and Calibration for a Predictive Computational Model of Coronary and Myocardial Blood Flow
- First author / authors (first 3 + et al.): Giovanni Montino Pelagi, Andrea Baggiano, Francesco Regazzoni et al.
- Year: 2024
- Venue: Annals of Biomedical Engineering
- DOI: 10.1007/s10439-024-03453-9

## One-line claim
- Personalized hyperemic pressure waveforms (reconstructed from basic patient data only) enable multiscale coronary-myocardial model calibration without stress-CTP, achieving high FFR and MBF prediction accuracy.

## T6 targeted questions
- **Q-A geometry perturbation**: Does not perturb; uses real patient cCTA geometries with existing coronary stenoses. No inter-observer variation studied.
- **Q-B decision flip**: FFR computed for each vessel; per-vessel sensitivity 100%, specificity 100% against clinical threshold (FFR 0.8). Mean MBF compared to stress-CTP data with 11.3% error in non-ischemic cases.
- **Q-C BC tuning**: KEY: proposes novel inlet pressure waveform reconstruction using age, sex, brachial pressure, HR, LV mass (routine clinical data only). Outlet conditions via 3D multi-compartment Darcy model with source-sink field calibration. Novel "blinded" calibration avoids need for stress-CTP. NO explicit statement about tuning AFTER geometry change or compensating for segmentation error; focus is on initial model setup.
- **Q-D fidelity / quantity**: Multiscale 3D CFD coronaries + 3D Darcy myocardium model (steady-state hyperemia). Computes FFR, pressure, velocity, MBF (3D spatial distribution). WSS and OSI NOT reported; focus on perfusion endpoints.
- **Q-E data**: 8 patients with various CAD conditions (non-obstructive and obstructive); cCTA, stress-CTP, and invasive FFR data. Private clinical data (Centro Cardiologico Monzino, Milan).
- **Q-F meshing**: Semi-automated cCTA segmentation (HeartFlow Inc. methods). Mesh generation details not extensively described. Robustness tested for synthetic network variation; limitations acknowledged for severe stenosis and LV hypertrophy cases.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates multiscale FFR/MBF prediction with personalized BC from routine clinical measures only; validates tissue-level perfusion; highly relevant to T6's frame of boundary condition tuning without extra imaging.
- verdict: FULL
- revisit-if: Always; recent (2024) and directly addresses BC personalization and multiscale prediction without stress imaging—core to T6's diagnostic pathway.
