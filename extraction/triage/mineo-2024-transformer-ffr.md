---
source_pdf_path: Resources/A_Convolutional-Transformer_Model_for_FFR_and_iFR_Assessment_From_Coronary_Angiography.pdf
slug: mineo-2024-transformer-ffr
ledger_status: TRIAGED
---

# mineo-2024-transformer-ffr

## Bibliographic
- Title: A Convolutional-Transformer Model for FFR and iFR Assessment From Coronary Angiography
- First author / authors: Raffaele Mineo, F. Proietto Salanitri, G. Bellitto
- Year: 2024
- Venue: IEEE Transactions on Medical Imaging, vol. 43, no. 8, pp. 2866–2877
- DOI: 10.1109/TMI.2024.3383283

## One-line claim
A hybrid CNN-Transformer deep learning model predicts FFR/iFR stenosis severity directly from angiography videos without requiring multiple views or key-frame selection, achieving state-of-the-art performance on 778 exams.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED
- **Q-B decision flip**: Yes, reports binary FFR/iFR classification at clinical thresholds (0.80 FFR, 0.89 iFR); "forces the model to focus on the cut-off region of FFR (around 0.8 FFR value), which is highly critical for decision-making"
- **Q-C BC tuning**: NOT REPORTED
- **Q-D fidelity / quantity**: Angiography-based regression and classification, not 3D CFD
- **Q-E data**: 778 exams from 389 patients, invasive FFR ground truth present
- **Q-F meshing**: NOT REPORTED

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Deep learning technique for FFR estimation from angiography; T6 could adopt similar multi-task learning (regression + classification) on boundary-condition variations
- verdict: LIGHT
- revisit-if: Paper addressed synthetic vs real segmentation error or sensitivity to geometric perturbations in angiographic input
