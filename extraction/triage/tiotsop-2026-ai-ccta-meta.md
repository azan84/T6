---
source_pdf_path: Resources/1-s2.0-S0899707126001981-main.pdf
slug: tiotsop-2026-ai-ccta-meta
ledger_status: TRIAGED
---

# tiotsop-2026-ai-ccta-meta

## Bibliographic
- Title: Diagnostic accuracy of artificial intelligence–enhanced coronary CT angiography for detecting functionally significant coronary artery disease: A systematic review and meta-analysis
- First author / authors: Maurice Tiotsop, Douni O. Roger, Utsab R. Panta
- Year: 2026
- Venue: Clinical Imaging
- DOI: https://doi.org/10.1016/j.clinimag.2026.110906

## One-line claim
Meta-analysis of 35 studies (18 contributing to quantitative analysis, ~8400 participants) demonstrates AI-enhanced CCTA achieves balanced diagnostic accuracy (sensitivity 0.823, specificity 0.820 for FFR ≤0.80) comparable to invasive FFR.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT SYSTEMATICALLY REPORTED. AI-CCTA methods in included studies do not isolate segmentation error or inter-observer variability as independent variables. Some studies use geometric morphometry features, but no synthetic perturbation framework.
- **Q-B decision flip**: YES, implicit. FFR ≤0.80 is the reference standard; diagnostic accuracy translates to reclassification potential. 13 studies with FFR ≤0.80 threshold; pooled sensitivity 0.823 (95% CI 0.761–0.872), specificity 0.820 (95% CI 0.732–0.883). No explicit discussion of decision-flip rates induced by segmentation error.
- **Q-C BC tuning**: NOT REPORTED. AI approaches are black-box or machine-learning based, not physics-informed CFD solvers. No BC tuning discussed; no statement about whether learned FFR surrogates mask anatomical errors.
- **Q-D fidelity / quantity**: Hybrid. Includes CT-FFR (computational hemodynamics) + deep learning FFR surrogates + radiomics features. NOT 3D simulation on real patient geometries. WSS/OSI NOT reported; focus on lesion-level FFR classification.
- **Q-E data**: 35 studies; 18 in quantitative meta-analysis (~8400 total participants); mostly private cohorts or single-center; invasive FFR ≤0.80 as reference standard present; public dataset availability mixed.
- **Q-F meshing**: NOT DISCUSSED in detail. CT-FFR methods use CFD post-processing; individual meshing strategies not synthesized in meta-analysis. No systematic evaluation of robustness to topology errors.

## Novelty bearing on T6
- bucket: BACKGROUND | METHOD
- one-line reason: Establishes that AI-CCTA achieves diagnostic parity with invasive FFR; validates FFR ≤0.80 as decision threshold. Relevant for T6's outcome validation, but does not isolate or quantify segmentation-error-driven decision flips.
- verdict: LIGHT
- revisit-if: Sensitivity analysis showing diagnostic accuracy degradation as CCTA segmentation quality or inter-observer stenosis measurement variability changes.

