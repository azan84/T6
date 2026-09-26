---
source_pdf_path: Resources/s00330-022-08796-2.pdf
slug: xu-2022-dlr-reconstruction
ledger_status: TRIAGED
---

# xu-2022-dlr-reconstruction

## Bibliographic
- Title: The impact of deep learning reconstruction on image quality and coronary CT angiography-derived fractional flow reserve values
- First author / authors: Cheng Xu, Min Xu, Jing Yan, Yan-Yu Li
- Year: 2022
- Venue: European Radiology
- DOI: 10.1007/s00330-022-08796-2

## One-line claim
Deep learning image reconstruction (DLR) improves coronary CTA image quality (SNR/CNR) but does not significantly alter CT-FFR machine learning values or diagnostic performance across five reconstruction algorithms.

## T6 targeted questions
- **Q-A geometry perturbation**: No—examines five reconstruction algorithms (FBP, SBIR, MBIR Cardiac, MBIR Cardiac sharp, DLR) applied to the same underlying geometry; no perturbation or inter-observer study.
- **Q-B decision flip**: YES—uses FFR ≤0.80 threshold. Diagnostic accuracy (FFR reference): MBIR Cardiac/sharp/DLR AUC=0.82 vs. FBP/SBIR AUC=0.78 (not significant). QFR reference: FBP 0.83, SBIR 0.81, MBIR Cardiac 0.86, MBIR Cardiac sharp 0.84, DLR 0.83 (all p>0.05, no difference).
- **Q-C BC tuning**: NOT ADDRESSED—paper focuses on image reconstruction quality, not boundary condition methodology or tuning.
- **Q-D fidelity / quantity**: 3D CFD. Pressure, velocity, and WSS fields generated; however, paper does not report WSS sensitivity to geometry or reconstruction algorithm.
- **Q-E data**: 33 patients, 182 lesions. Invasive FFR (17 vessels) and QFR (70 vessels) as reference standards.
- **Q-F meshing**: NOT REPORTED—focus on image reconstruction, not segmentation robustness.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Image reconstruction study focused on CTA quality; does not address hemodynamic sensitivity to geometry uncertainty or BC tuning. Confirms that FFR computation is robust to image reconstruction algorithm choice.
- verdict: LIGHT
- revisit-if: Only for CTA acquisition protocol optimization; not relevant to T6's BC tuning or error-ranking framework.
