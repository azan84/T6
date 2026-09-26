---
source_pdf_path: Resources/1-s2.0-S0720048X26002329-main.pdf
slug: moshage-2026-ct-ffr-slice-thickness
ledger_status: TRIAGED
---

# moshage-2026-ct-ffr-slice-thickness

## Bibliographic
- Title: Does slice thickness matter? Diagnostic accuracy of CT-derived fractional flow reserve (CT-FFR) compared with invasive FFR
- First author / authors (first 3 + et al.): Maximilian Moshage, Georg Lind, Rosa Lynn Schmitz, et al.
- Year: 2026
- Venue: European Journal of Radiology 200 (2026) 112884
- DOI: 10.1016/j.ejrad.2026.112884

## One-line claim
Evaluates the effect of reconstructed CT slice thickness (0.5, 0.75, 1.0 mm) on CT-FFR diagnostic accuracy compared to invasive FFR, demonstrating robustness across slice thicknesses with 0.75 mm optimal.

## T6 targeted questions

- **Q-A geometry perturbation**: **YES. CRITICAL**. Directly addresses segmentation uncertainty: "Reconstructed slice thickness directly affects spatial resolution, partial volume effects, and vessel border definition, thereby potentially impacting lumen segmentation and downstream flow estimation." Study systematically varies slice thickness to assess segmentation-related uncertainty impact on CFD-based FFR-CT.

- **Q-B decision flip**: YES. Reports FFR threshold 0.80 classification: "An FFR value ≤ 0.80 was considered indicative of hemodynamically significant coronary artery disease." Provides sensitivity/specificity/accuracy across different slice thicknesses at 0.80 threshold: sensitivity 81% (0.5mm), 86% (0.75mm), 76% (1.0mm); specificity 85-88%.

- **Q-C BC tuning**: Uses CFD-based CT-FFR but does NOT explicitly discuss boundary condition re-tuning or compensation for segmentation uncertainty.

- **Q-D fidelity / quantity**: Uses CFD-based CT-FFR (machine learning prototype, Siemens cFFR). Does NOT report WSS, OSI, or spatially-resolved fields.

- **Q-E data**: 50 patients (81 vessels), single-center prospective, invasive FFR gold standard, intermediate stenosis (50-70% CCTA estimate).

- **Q-F meshing**: **CRITICAL FOR GATE M1**. Core paper addresses segmentation robustness: "Reconstructed slice thickness directly affects spatial resolution, partial volume effects, and vessel border definition, thereby potentially impacting lumen segmentation and downstream flow estimation." Finds that CT-FFR "maintained high diagnostic accuracy, with no significant impact of slice thickness on the overall accuracy" (p=0.51-1.0 across thresholds), suggesting robustness to segmentation quality variation.

## Novelty bearing on T6

- bucket: SUPPORT
- one-line reason: Directly demonstrates real-world segmentation parameter uncertainty (slice thickness) has minimal impact on FFR-CT accuracy at 0.80 threshold, supporting T6's premise that model robustness can compensate for geometric uncertainty.
- verdict: LIGHT
- revisit-if: Paper extends analysis to topological/structural segmentation errors (missed branches, bifurcation misclassification) beyond slice-thickness effects.
