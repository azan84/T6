---
source_pdf_path: Resources/s42003-020-01638-1.pdf
slug: li-2021-dl-cfd
ledger_status: TRIAGED
---

# li-2021-dl-cfd

## Bibliographic
- Title: Prediction of 3D Cardiovascular hemodynamics before and after coronary artery bypass surgery via deep learning
- First author / authors: Gaoyang Li, Haoran Wang, Mingzi Zhang (et al.)
- Year: 2021
- Venue: Communications Biology (Nature)
- DOI: 10.1038/s42003-020-01638-1

## One-line claim
A deep learning network trained on CFD datasets can predict 3D cardiovascular hemodynamics from geometry alone, achieving ~90% accuracy and 600-fold speedup over traditional CFD, enabling clinical translation.

## T6 targeted questions
- **Q-A geometry perturbation**: No systematic geometry perturbation or segmentation uncertainty study. Uses patient-specific coronary models before and after bypass surgery. NOT REPORTED: inter-segmenter disagreement or REAL measurement variability.
- **Q-B decision flip**: NOT REPORTED. Does not address FFR, diagnostic thresholds, or decision-flip rates.
- **Q-C BC tuning**: NOT REPORTED in front matter. CFD method used to generate training data but boundary condition tuning strategy not mentioned.
- **Q-D fidelity / quantity**: 3D CFD (conventional method for training data). Deep learning predicts full 3D hemodynamics. NOT REPORTED: WSS/OSI sensitivity or spatial field accuracy breakdown in abstract.
- **Q-E data**: Patient-specific coronary models (2+ million nodes). Dataset includes pre and post-bypass cases. Invasive FFR ground truth: NOT REPORTED.
- **Q-F meshing**: NOT REPORTED in front matter. "Over 2 million nodes" in models; segmentation/meshing robustness to geometry error not addressed.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Develops deep learning surrogate for 3D CFD hemodynamic prediction. Useful computational efficiency gain but does not address geometry uncertainty, segmentation error tolerance, or whether DL model learns BC compensation for topological errors.
- verdict: LIGHT
- revisit-if: Full paper shows DL prediction accuracy degrades with geometry perturbation, or compares DL-predicted hemodynamics when coronary segmentation varies.
