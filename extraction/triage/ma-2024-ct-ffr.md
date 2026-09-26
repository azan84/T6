---
source_pdf_path: Resources/s41598-024-79243-z.pdf
slug: ma-2024-ct-ffr
ledger_status: TRIAGED
---

# ma-2024-ct-ffr

## Bibliographic
- Title: Dynamic CT myocardial perfusion combined with coronary CT angiography for detecting hemodynamical significance of coronary artery stenosis: a comparative study
- First author / authors: Mengqing Ma, Yumeng Hu, Shimei Shang (et al.)
- Year: 2024
- Venue: Scientific Reports (Nature)
- DOI: 10.1038/s41598-024-79243-z

## One-line claim
Combining dynamic CT perfusion with coronary CTA and CT-FFR (computed via CFD) improves diagnostic accuracy for hemodynamically significant coronary artery disease compared to CTA alone, with FFR 0.80 threshold.

## T6 targeted questions
- **Q-A geometry perturbation**: No explicit perturbation or inter-segmenter disagreement study. Uses patient-specific coronary CTA geometry. NOT REPORTED: segmentation uncertainty or measurement variability.
- **Q-B decision flip**: YES—Reports FFR 0.80 threshold ("Hemodynamic significance, determined by Angio-FFR ≤ 0.80"). Diagnostic performance: CTA alone sensitivity 94.12%, specificity 34.78%; CTA+CTP sensitivity variable, specificity 88.41%; CTA+CTP+CT-FFR sensitivity 88.24%, specificity 88.41%, accuracy 88.37%. Angio-FFR used as ground truth.
- **Q-C BC tuning**: NOT REPORTED. Abstract mentions CT-FFR calculations employing "computational fluid dynamics" but boundary condition tuning details not in front matter.
- **Q-D fidelity / quantity**: 3D CFD for CT-FFR calculation. NOT REPORTED: WSS/OSI or spatial hemodynamic details in front matter.
- **Q-E data**: 33 patients, 86 coronary vessels, 30–90% stenosis range. Invasive FFR ground truth present (Angio-FFR from coronary angiography).
- **Q-F meshing**: NOT REPORTED in front matter. Segmentation from coronary CTA implied but robustness/uncertainty not addressed.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Clinical validation study of CT-FFR for CAD diagnosis using 0.80 threshold. Useful context for FFR-based decision-making but does not address geometry uncertainty, segmentation error, or BC tuning strategy.
- verdict: LIGHT
- revisit-if: Full paper includes sensitivity analysis on segmentation/geometry uncertainty, or compares CT-FFR robustness to inter-segmenter coronary geometry disagreement.
