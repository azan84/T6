---
source_pdf_path: Resources/s41598-023-49591-3.pdf
slug: kizhisseri-2023-stroke
ledger_status: TRIAGED
---

# kizhisseri-2023-stroke

## Bibliographic
- Title: Differential sensitivities to blood pressure variations in internal carotid and intracranial arteries: a numerical approach to stroke prediction
- First author / authors: Muhsin Kizhisseri, Saleh Gharaie, Sethu Raman Boopathy (et al.)
- Year: 2023
- Venue: Scientific Reports (Nature)
- DOI: 10.1038/s41598-023-49591-3

## One-line claim
CFD informed by Windkessel models reveals differential hemodynamic sensitivities to blood pressure variations across intracranial artery branches in stenotic patient-specific models, with FFR as a robust predictor of stenosis severity.

## T6 targeted questions
- **Q-A geometry perturbation**: No explicit perturbation study. Uses patient-specific ICA models with introduced stenosis (not inter-observer disagreement). NOT REPORTED: segmentation uncertainty or REAL inter-segmenter variability.
- **Q-B decision flip**: YES—"FFR emerged as a robust predictor of stenosis severity, particularly in the M2 branch." Analyzes FFR in stenotic models. NOT REPORTED: threshold-specific reclassification rates or decision-flip percentages.
- **Q-C BC tuning**: YES—Uses "Windkessel model" (abstract). NOT REPORTED: detailed boundary condition tuning strategy, parameter values, or whether BC tuning changes when geometry (stenosis) is modified.
- **Q-D fidelity / quantity**: CFD (3D). Analyzes "blood flow adjustments," "flow velocity," "flow rate." NOT REPORTED: WSS/OSI or wall shear stress sensitivity specifically stated.
- **Q-E data**: "Patient-specific ICA models." Cohort size NOT REPORTED. Invasive FFR: NOT REPORTED as ground truth (FFR calculated computationally, not compared to invasive wire data).
- **Q-F meshing**: NOT REPORTED. Patient-specific models mentioned but segmentation/meshing robustness not addressed.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Applies CFD + Windkessel + FFR to intracranial stenosis (stroke context, not coronary). Demonstrates FFR sensitivity but does not address segmentation uncertainty, inter-observer disagreement, or topological error. Limited coronary applicability.
- verdict: LIGHT
- revisit-if: Full paper includes real inter-segmenter disagreement dataset for coronary arteries, or compares computational FFR against invasive wire data.
