---
source_pdf_path: Resources/J Applied Clin Med Phys - 2023 - Yao - Deep learning‐based motion correction algorithm for coronary CT angiography .pdf
slug: yao-2023-motion-correction
ledger_status: TRIAGED
---

# yao-2023-motion-correction

## Bibliographic
- Title: Deep learning-based motion correction algorithm for coronary CT angiography: Lowering the phase requirement for morphological and functional evaluation
- First author / authors: Xiaoling Yao, Tao Shuai, Sihua Zhong, Zhenlin Li
- Year: 2023
- Venue: Journal of Applied Clinical Medical Physics, vol. 24, e14104
- DOI: 10.1002/acm2.14104

## One-line claim
A deep learning-based motion correction algorithm (CardioCapture) significantly improves CCTA image quality and CT-FFR diagnostic performance at non-optimal cardiac phases, enabling reliable assessment within 4% phase deviation.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED – studies motion artifact effects, not geometric segmentation error
- **Q-B decision flip**: YES – investigates CT-FFR classification: "Functionally significant stenosis was defined as CT-FFR value ≤0.8"; reports sensitivity, specificity, accuracy at various phase deviations; "With MCA, the performance of identifying functionally significant stenosis via CT-FFR was increased"
- **Q-C BC tuning**: NOT REPORTED; no discussion of boundary condition methodology
- **Q-D fidelity / quantity**: CT-FFR (reduced-order flow model from 3D reconstruction); validates against invasive FFR on 24 patients, 38 vessels
- **Q-E data**: 53 patients (HR ≥75 bpm), 24 referred for ICA/invasive FFR within 2 months
- **Q-F meshing**: NOT REPORTED

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Deep learning motion correction technique for CCTA preprocessing; T6 could adopt for segmentation robustness, but does not address error ranking or BC tuning
- verdict: LIGHT
- revisit-if: Paper evaluated sensitivity of CT-FFR to segmentation error or whether motion-corrected geometries change diagnostic classification
