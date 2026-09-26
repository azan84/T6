---
source_pdf_path: Resources/fcvm-11-1398635.pdf
slug: kong-2024-stress-ct-perfusion
ledger_status: TRIAGED
---

# kong-2024-stress-ct-perfusion

## Bibliographic
- Title: Diagnostic efficacy of absolute and relative myocardial blood flow of stress dynamic CT myocardial perfusion for detecting myocardial ischemia in patients with hemodynamically significant coronary artery disease
- First author / authors (first 3 + et al.): Kong W, Long B, Huang H et al.
- Year: 2024
- Venue: Frontiers in Cardiovascular Medicine
- DOI: 10.3389/fcvm.2024.1398635

## One-line claim
Stress dynamic CT myocardial perfusion imaging (MBF-based) shows excellent diagnostic performance (AUC 0.962 for MBF-ratio) for detecting ischemia, comparable to invasive FFR/ICA.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb; uses patient-specific myocardial tissue perfusion imaging. NOT measuring segmentation uncertainty.
- **Q-B decision flip**: YES—uses FFR ≤0.80 as ischemia threshold. Study is motivated by discordance between anatomy and function: "CCTA offers solely anatomical information and does not present a linear correlation between the severity of coronary artery stenosis and myocardial ischemia." Compares MBF-based diagnosis to invasive criteria (ICA ≥80% or FFR ≤0.80).
- **Q-C BC tuning**: NOT ADDRESSED. Study is perfusion-imaging (dynamic CT), not CFD/hemodynamic simulation. Measures myocardial blood flow directly from contrast transit; does NOT use computational boundary conditions.
- **Q-D fidelity / quantity**: CT-based perfusion imaging (dynamic CT myocardial perfusion), NOT CFD. Quantifies absolute myocardial blood flow (MBFa) and relative MBF-ratio. Reports tissue-level perfusion, not vessel hemodynamics (no WSS/OSI, no FFR prediction).
- **Q-E data**: N=46 patients, 120 vessels. Invasive FFR/ICA ground truth present (YES). Retrospective single-center study.
- **Q-F meshing**: No meshing—imaging-based perfusion. Volume-of-interest (VOI) analysis on perfusion maps. No mesh or segmentation detail.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Myocardial perfusion (tissue-level) approach to ischemia detection; ORTHOGONAL to T6's coronary segmentation + CFD framework; does not address vessel anatomy, segmentation error, or BC tuning
- verdict: LIGHT
- revisit-if: Paper compares perfusion-based ischemia detection to segmentation-error-induced FFR variability, or validates patient selection for T6-style CFD analysis

