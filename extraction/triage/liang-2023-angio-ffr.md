---
source_pdf_path: Resources/s00330-023-09682-1.pdf
slug: liang-2023-angio-ffr
ledger_status: TRIAGED
---

# liang-2023-angio-ffr

## Bibliographic
- Title: Diagnostic performance of angiography-derived fractional flow reserve analysis based on bifurcation fractal law for assessing hemodynamic significance of coronary stenosis
- First author / authors: Hongbin Liang, Qiuxia Zhang, Yiting Gao, Guojun Chen
- Year: 2023
- Venue: European Radiology
- DOI: 10.1007/s00330-023-09682-1

## One-line claim
Bifurcation fractal law (Huo-Kassab's law) enables accurate Angio-FFR calculation from single-view angiography by compensating for side-branch flow without explicit coronary tree segmentation.

## T6 targeted questions
- **Q-A geometry perturbation**: No—uses actual invasive coronary angiography images; no geometry perturbation or inter-observer disagreement measurement.
- **Q-B decision flip**: YES—uses FFR ≤0.80 threshold. Angio-FFR AUC 0.96 (0.92–0.99); correlation with invasive FFR r=0.92 for Angio-FFR vs. r=0.91 for FFR_s vs. r=0.85 for FFR_n (no side-branch compensation).
- **Q-C BC tuning**: Outlet BC methodology—"Side branch flow was quantified using the bifurcation fractal law to correct the blood flow in each vessel segment. To compensate for the side branch flow, we adopt an optimization method based on Huo-Kassab's Law to adjust the inlet blood flow of each segment." Not tuning to absorb error but optimizing outlet boundary condition formulation using geometric scaling laws.
- **Q-D fidelity / quantity**: 1D reduced-order CFD model. Pressure drop along vessel centerline computed; no WSS/OSI reporting.
- **Q-E data**: 159 vessels from 119 patients. Invasive FFR (≤0.80) as reference. Private cohort (Nanfang Hospital, Guangzhou).
- **Q-F meshing**: Segmentation via deep learning (dual-branch multiscale attention network); centerline and radius extraction automated; no detail on robustness to poor segmentation or topological error.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates outlet boundary condition optimization using bifurcation fractal law; reduces computational burden by avoiding full coronary tree reconstruction. Relevant to T6 if coronary-specific fractal scaling differs from general vascular models.
- verdict: LIGHT
- revisit-if: If T6 incorporates side-branch flow compensation; note that method works on 2D angiography, not 3D segmentation, and does not address topological segmentation error (T6 focus).
