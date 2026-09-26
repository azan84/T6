---
source_pdf_path: Resources/Medical Physics - 2025 - Liang - A novel algorithm for automated analysis of coronary CTA‐derived FFR in identifying.pdf
slug: liang-2025-ct-ffr-deep
ledger_status: TRIAGED
---

# liang-2025-ct-ffr-deep

## Bibliographic
- Title: A novel algorithm for automated analysis of coronary CTA-derived FFR in identifying ischemia-specific CAD: A multicenter study
- First author / authors (first 3): Hongqin Liang, Feng Wen, Zhiguo Sun
- Year: 2025
- Venue: Medical Physics
- DOI: 10.1002/mp.17803

## One-line claim
A novel CT FFR algorithm combining deep learning (nnUNet) and level set segmentation with CFD-based hemodynamic modeling outperforms existing AI platforms in automated on-site identification of ischemia-specific coronary artery disease.

## T6 targeted questions
- **Q-A geometry perturbation**: Uses standard segmentation algorithms (nnUNet encoder-decoder + level set optimization) on real patient geometries; does NOT systematically measure inter-observer/inter-segmenter disagreement on lumen boundaries. Segmentation refined iteratively via level set methods achieving "sub-pixel accuracy" and "accurate coronary artery contours", but no reported inter-rater variability or uncertainty quantification of geometry.
- **Q-B decision flip**: YES. Reports FFR threshold ≤0.80 as cut-off for hemodynamically significant lesions. Achieved "85.9% accuracy" in identifying 24 vessels with FFR 0.75–0.8 ("gray zone") vs. competing platform's 19/24. Reclassification rates reported: models performed "notably better in gray zone lesions" but absolute flip rates not explicitly stated.
- **Q-C BC tuning**: Uses Windkessel model outlet boundary conditions with capacitance 100–300 µF, prescribed via "pressure outlet boundary condition". CFD performed using OpenFOAM with "fully automated" CFD simulation and post-processing. NO statement that BC tuning re-done after geometry change or that tuning compensates for segmentation/topological error. BC parameters appear fixed across cases.
- **Q-D fidelity / quantity**: 3D CFD via OpenFOAM using Navier–Stokes equations and SIMPLE algorithm on patient-specific models. NO reports of WSS, OSI, or spatially-resolved field sensitivity to geometry perturbations.
- **Q-E data**: Multicenter retrospective cohort: 171 patients with 198 vessels across 4 hospitals in China (central, western, eastern, northeastern). Invasive FFR as gold standard. Public/private status NOT reported.
- **Q-F meshing**: Coronary segmentation via nnUNet (deep learning) followed by level set optimization to obtain "accurate coronary artery contour and centerline". Level set module iteratively refines segmentation to handle "calcification and soft plaque". NO discussion of robustness to topologically incorrect geometry or segmentation failure modes.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Combines deep learning segmentation with level set refinement and CFD-based FFR; automated on-site analysis workflow; no study of real inter-segmenter disagreement driving FFR decision flip.
- verdict: LIGHT
- revisit-if: Paper reports inter-segmenter disagreement quantification on same images; or ablates impact of segmentation perturbations on FFR classification at 0.80 threshold.

