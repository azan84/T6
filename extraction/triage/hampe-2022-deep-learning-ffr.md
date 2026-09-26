---
source_pdf_path: Resources/fcvm-09-964355.pdf
slug: hampe-2022-deep-learning-ffr
ledger_status: TRIAGED
---

# hampe-2022-deep-learning-ffr

## Bibliographic
- Title: Deep learning-based detection of functionally significant stenosis in coronary CT angiography
- First author / authors (first 3 + et al.): Hampe N, van Velzen SGM, Planken RN et al.
- Year: 2022
- Venue: Frontiers in Cardiovascular Medicine
- DOI: 10.3389/fcvm.2022.964355

## One-line claim
Deep learning method predicts FFR from coronary CTA without manual lumen segmentation, achieving AUC 0.78 and outperforming prior methods not requiring segmentation.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb; uses patient-specific CCTA. NOT measuring segmentation uncertainty.
- **Q-B decision flip**: YES—addresses FFR-based decision-making. "To assess the functional significance of FFR" at 0.80 threshold. Shows performance at different FFR ranges (>0.8, 0.75–0.80, <0.75); gray zone analysis implicit but not emphasized. Target label: "presence of a functionally significant stenosis."
- **Q-C BC tuning**: NOT explicitly addressed. Deep learning approach avoids CFD modeling; uses extracted artery characteristics (lumen area, attenuation, calcium) and tree topology. No discussion of BC tuning or how hemodynamic parameters influence predictions.
- **Q-D fidelity / quantity**: Machine learning (CNN + transformer) directly from CCTA; does NOT use CFD. Extracts artery characteristics but not spatially-resolved fields. No WSS/OSI.
- **Q-E data**: N=569 patients, 569 arteries for development/validation, held-out test sets (76 arteries + 600 arteries CCTA-only). Invasive FFR ground truth on test set.
- **Q-F meshing**: No meshing—image-based ML. Mentions extraction of coronary tree and MPR but no volumetric mesh discussion.

## Novelty bearing on T6
- bucket: METHOD | BACKGROUND
- one-line reason: Alternative (non-CFD) approach to FFR prediction; demonstrates segmentation-free FFR assessment but bypasses hemodynamic insight into BC tuning; machine learning method complements but doesn't directly address T6's CFD + BC hypothesis
- verdict: LIGHT
- revisit-if: Deep learning predictions compared to CFD BC-tuning approach OR paper analyzes segmentation error impact on predictions

