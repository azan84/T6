---
source_pdf_path: Resources/qims-16-07-560.pdf
slug: wang-2026-smoking-cfd
ledger_status: TRIAGED
---

# wang-2026-smoking-cfd

## Bibliographic
- Title: Effect of smoking on the diagnostic performance of computational fluid dynamics-derived CT-derived fractional flow reserve: a cross-sectional study
- First author / authors: Xinhong Wang, Xiaodan Feng, Shuangxiang Lin, Mengxi Xu
- Year: 2026
- Venue: Quantitative Imaging in Medicine and Surgery
- DOI: 10.21037/qims-2025-aw-2409

## One-line claim
FFRct demonstrates consistent diagnostic accuracy in smokers vs. non-smokers despite smoking-related increases in myocardial volume, supporting utility of FFRct in smoking populations.

## T6 targeted questions
- **Q-A geometry perturbation**: No—uses actual patient CCTA. No geometry perturbation or inter-observer disagreement measurement.
- **Q-B decision flip**: YES—reports FFR ≤0.80 threshold. No significant difference in FFR (0.85 vs. 0.85, P=0.496) or FFRct (0.86 vs. 0.86, P=0.466) between smokers and non-smokers. Diagnostic performance comparable: sensitivity 87.50% (smokers) vs. 90.00% (non-smokers), specificity 89.19% vs. 88.64%, accuracy 88.68% vs. 89.06%, AUC 0.919 vs. 0.928.
- **Q-C BC tuning**: Partial—"myocardial volume, used as a boundary condition in CFD simulations, differs between smoking groups." Smokers had significantly larger myocardial volumes (193.4 vs. 157.9 mL, P<0.01). BC adjustment note: "myocardial volume adjustment used in boundary condition setting is a standard pre-specified component of the algorithm, applied uniformly to all patients regardless of smoking status." The algorithm uses 3D LV segmentation to set microcirculatory resistance boundary conditions, but this is **not smoking-specific tuning**—standard approach applied equally.
- **Q-D fidelity / quantity**: 3D CFD via Newton-Krylov-Schwarz solver. No WSS/OSI fields explicitly reported in abstract/results.
- **Q-E data**: 298 patients (106 smokers, 192 non-smokers) from 6 Chinese medical centers. Invasive FFR as reference. HBFlows trial sub-study (2020–2022).
- **Q-F meshing**: Not reported.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Validation study confirming FFRct reliability in a high-risk subgroup (smokers). No novel BC tuning or error-ranking methodology; primarily diagnostic performance assessment.
- verdict: LIGHT
- revisit-if: If T6 subgroup analysis on smoking-related microvascular dysfunction becomes relevant.
