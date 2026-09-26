---
source_pdf_path: Resources/s12880-025-01919-3.pdf
slug: jiang-2025-nafld-coronary-outcomes
ledger_status: TRIAGED
---

# jiang-2025-nafld-coronary-outcomes

## Bibliographic
- Title: Assessment of non-alcoholic fatty liver disease in suspected coronary artery disease patients: prognostic value and incremental predictive utility over cardiovascular risk factors and CCTA
- First author / authors (first 3 + et al.): Jiang C, Yang Q, Hou X, et al.
- Year: 2025
- Venue: BMC Medical Imaging
- DOI: 10.1186/s12880-025-01919-3

## One-line claim
NAFLD independently predicts major adverse cardiovascular events (MACE) in CAD patients, incrementally improving risk stratification when incorporated into models with CCTA and CT-FFR.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (clinical cohort study; no geometry perturbation analysis)
- **Q-B decision flip**: CT-FFR ≤0.80 used as diagnostic threshold; NAFLD group had higher CT-FFR positivity (p<0.05); NAFLD predicted MACE especially in "those with non-obstructive CAD or normal CT-FFR." Implies reclassification potential but not quantified as flip rate.
- **Q-C BC tuning**: NOT REPORTED (commercial CT-FFR software, Siemens Healthineers v3.5; no discussion of BC protocol, tuning procedure, or whether tuning changed with segmentation/geometry error)
- **Q-D fidelity / quantity**: CT-FFR computed from CCTA; reduced-order CFD via vendor software. No 3D CFD, WSS, or OSI reported.
- **Q-E data**: N=2,981 total (737 NAFLD, 2,244 non-NAFLD); 3,122 patients with valid CT-FFR; median 68-month follow-up. Private cohort (Dalian Medical University, Jan 2017–Dec 2018). Invasive FFR not ground truth but MACE events tracked prospectively.
- **Q-F meshing**: NOT REPORTED (commercial CCTA post-processing via syngo.via; no meshing detail)

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Large prospective study validating CT-FFR for prognostic stratification in CAD; documents clinical context and decision thresholds but does not address geometry error or BC sensitivity.
- verdict: LIGHT
- revisit-if: Paper isolates CT-FFR ≤0.80 reclassification rate or analyzes segmentation/geometry error's contribution to outcome misclassification

