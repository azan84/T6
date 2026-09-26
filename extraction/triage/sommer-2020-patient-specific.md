---
source_pdf_path: Resources/Sommer_2020_Biomed._Phys._Eng._Express_6_045007.pdf
slug: sommer-2020-patient-specific
ledger_status: TRIAGED
---

# sommer-2020-patient-specific

## Bibliographic
- Title: Patient-specific 3D-printed coronary models based on coronary computed tomography angiography volumes to investigate flow conditions in coronary artery disease
- First author / authors: Kelsey N Sommer, Lauren M Shepard, Dimitrios Mitsouras
- Year: 2020
- Venue: Biomedical Physics & Engineering Express, vol. 6
- DOI: NOT REPORTED in extracted text

## One-line claim
Uses 3D-printed patient-specific coronary models connected to a programmable pulsatile pump to measure benchtop FFR (B-FFR) and compare with CT-FFR and invasive FFR, exploring role of distal resistance adjustment.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No inter-observer segmentation variability; 3D printing embeds specific geometry but no sensitivity to uncertainty reported.
- **Q-B decision flip**: FFR threshold comparison. Text: "Benchtop flow simulations with 3D printed models provide the capability to measure pressure changes at any location in the model, for ultimately emulating the FFR at several simulated outflow rates." Pearson correlations with invasive FFR-0.80 threshold reported (ROC AUC 0.80–0.81) but no reclassification rate.
- **Q-C BC tuning**: Yes, distal resistance tuned. Key quote: "adjusting the model's distal coronary resistance" for two outflow rates ('normal' 250 ml/min, 'hyperemic' 500 ml/min). This is a manual BC parameterization via resistance. No re-tuning after geometry change or discussion of whether tuning compensates for error.
- **Q-D fidelity / quantity**: Physical model (benchtop CFD with 3D-printed geometry). Pressure measurements only; no velocity field or WSS/OSI reported.
- **Q-E data**: Patient-specific coronary models (N, dataset name NOT REPORTED). Private data. Invasive FFR ground truth present (reference for ROC AUC).
- **Q-F meshing**: NOT REPORTED (3D printing bypasses traditional meshing but the geometric fidelity depends on imaging segmentation).

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Provides experimental validation that benchtop FFR can match invasive FFR with resistance tuning, supporting the practical use of distal resistance calibration; demonstrates that outlet resistance is a tunable parameter affecting FFR prediction.
- verdict: LIGHT
- revisit-if: If paper includes analysis of how segmentation uncertainty or geometric variations propagate into benchtop FFR error, or whether resistance can be fit to mask geometric error.
