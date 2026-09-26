---
source_pdf_path: Resources/The Journal of Physiology - 2025 - Plappert - Computational model of haemodynamics during atrial fibrillation.pdf
slug: plappert-2025-computational
ledger_status: TRIAGED
---

# plappert-2025-computational

## Bibliographic
- Title: Computational model of haemodynamics during atrial fibrillation
- First author / authors: Felix Plappert, Pim J.A. Oomen, Clara E. Jones
- Year: 2025
- Venue: The Journal of Physiology
- DOI: NOT REPORTED in extracted text

## One-line claim
Develops a patient-specific computational model (electrical + mechanical/reduced-order subsystem) to replicate haemodynamics during both normal sinus rhythm and atrial fibrillation, with model calibration to ECG and echocardiographic data.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No segmentation error or inter-observer variability analysis.
- **Q-B decision flip**: NOT REPORTED. No diagnostic threshold or reclassification analysis (application is AF hemodynamics, not coronary FFR).
- **Q-C BC tuning**: Reduced-order model calibration to clinical measurements (blood pressures from ECG, echo, catheterization). Text: "The model parameters were fitted to individual patients using ECG, transthoracic echocardiographic and arterial and intracardiac pressure measurements." No explicit outlet BC parameterization or tuning strategy stated.
- **Q-D fidelity / quantity**: Reduced-order model (compartmental/lumped-parameter, not spatially resolved). No WSS/OSI (whole-heart application, not coronary).
- **Q-E data**: 17 patients from SMURF study (dataset name stated). Clinical data. No invasive coronary FFR (cardiac hemodynamics only).
- **Q-F meshing**: NOT APPLICABLE (reduced-order model does not use mesh).

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Demonstrates reduced-order model calibration methodology for patient-specific hemodynamics but application is whole-heart AF dynamics, not coronary segmentation error or FFR decision-making. No relevance to coronary BC tuning or segmentation error ranking.
- verdict: LIGHT
- revisit-if: NOT RELEVANT for T6 coronary scope.
