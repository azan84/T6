---
source_pdf_path: Resources/jez160.pdf
slug: kumamaru-2020-deeplearning-ffr
ledger_status: TRIAGED
---

# kumamaru-2020-deeplearning-ffr

## Bibliographic
- Title: Diagnostic accuracy of 3D deep-learning-based fully automated estimation of patient-level minimum fractional flow reserve from coronary computed tomography angiography
- First author / authors (first 3 + et al.): Kanako K. Kumamaru, Shinichiro Fujimoto, Yujiro Otsuka, et al.
- Year: 2020
- Venue: European Heart Journal - Cardiovascular Imaging
- DOI: 10.1093/ehjci/jez160

## One-line claim
- Diagnostic accuracy of 3D deep-learning-based fully automated estimation of patient-level minimum fr...

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED - No explicit measurement of segmentation uncertainty or inter-observer disagreement
- **Q-B decision flip**: YES - Reports FFR <0.8 threshold for abnormal FFR; 72/131 (55%) patients had abnormal invasive FFR
- **Q-C BC tuning**: NOT APPLICABLE - Deep learning model does not use explicit boundary condition tuning; fully automated FFR estimation from unsegmented CCTA
- **Q-D fidelity / quantity**: 3D CNN-based deep learning model; does not report spatially-resolved fields like WSS/OSI
- **Q-E data**: N=131 patients with invasive FFR ground truth (72 abnormal); also 921 unlabeled patients; private dataset
- **Q-F meshing**: NOT REPORTED - No detail on meshing pipeline; model works on unsegmented data

## Novelty bearing on T6
- bucket: METHOD
- reason: Deep learning technique for automated FFR estimation from CCTA; relevant to exploring alternatives to CFD-based approaches
- verdict: LIGHT
- revisit-if: If the paper discusses sensitivity to geometric errors or topological mistakes in CCTA data
