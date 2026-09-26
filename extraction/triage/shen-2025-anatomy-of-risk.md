---
source_pdf_path: Resources/2507.17109v1.pdf
slug: shen-2025-anatomy-of-risk
ledger_status: TRIAGED
---

# shen-2025-anatomy-of-risk

## Bibliographic
- Title: The Anatomy of Coronary Risk: How Arterial Geometry Shapes Coronary Artery Disease through Blood Flow Haemodynamics – Latest Methods, Insights and Clinical Implications
- First author / authors (first 3 + et al.): C. Shen, M. Zhang, H. Keramati
- Year: 2025
- Venue: arXiv:2507.17109
- DOI: NOT REPORTED

## One-line claim
A comprehensive review of coronary anatomy, imaging modalities, segmentation methods, computational hemodynamics approaches, and the "anatomy of risk" hypothesis linking vascular geometry to CAD progression.

## T6 targeted questions
- **Q-A geometry perturbation**: Extensive discussion of segmentation challenges. "Blooming artefacts in CTCA images, preventing even the latest neural networks from predicting true luminal boundaries." "Soft plaques have Hounsfield unit values close to the surrounding heart tissues, making it hard for neural networks to differentiate and characterise stenosis severity." Emphasizes that "conventional, manual, or at least semi-manual methods are still considered more accurate when the segmentation and reconstruction have been verified by an expert multiple times (intra-observer) or by two or more experts independently (inter-observer)." No quantified inter-observer disagreement magnitudes reported.
- **Q-B decision flip**: FFR ≤ 0.80 threshold is central to clinical guidelines. Reviews FFR-CT accuracy across trials. "Recent advances in computational modelling have enabled FFR to be calculated from images, i.e. FFR-CT, which has proven diagnostic accuracy in various clinical trials." Does NOT report specific FFR reclassification or decision-flip rates.
- **Q-C BC tuning**: Reviews boundary condition approaches: "To do this, one should carefully consider appropriate dimensional fidelity, numerical approaches and techniques, boundary conditions, and uncertainty analysis." Discusses lumped-parameter models, 1D models, and 3D CFD. Mentions multi-scale models incorporating "0D or 1D models to supply dynamic boundary conditions to the full-scale 3D coronary simulations." Does NOT report explicit BC re-tuning after geometry perturbations or whether tuning masks error.
- **Q-D fidelity / quantity**: Comprehensive review of 0D (lumped-parameter), 1D (distributed-parameter), 2D, and 3D CFD approaches. Discusses WSS (wall shear stress) and OSI (Oscillatory Shear Index). States: "Quantification of time-dependent haemodynamic metrics, e.g. Time-Averaged Endothelial Shear Stress (TAESS), Oscillatory Shear Index (OSI), would require the entire cardiac cycle to be simulated." Reviews neural network and PINN approaches for surrogate modeling.
- **Q-E data**: Comprehensive review of imaging techniques (CCTA, ICA, IVUS, OCT, MRI) and associated datasets/trials (FAME 2, others). Discusses open-access datasets and their limitations. No new primary cohort.
- **Q-F meshing**: Extensive review of segmentation methods: "key segmentation processes relied heavily on manual verification, utilising semi-automated segmentation tools... AI-driven methods, particularly deep learning-based segmentation, have increasingly complemented conventional approaches." Notes "blooming artefacts in CTCA images, preventing even the latest neural networks from predicting true luminal boundaries." Emphasizes inter-observer variability and mesh quality considerations.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Comprehensive review establishing the state-of-the-art in coronary imaging, segmentation challenges (including inter-observer variability and artifacts), and hemodynamic modeling approaches; provides essential background and context for T6's focus on real segmentation error.
- verdict: LIGHT
- revisit-if: If team seeks quantitative data on inter-observer segmentation variability, artifact effects, or comparisons of segmentation impact on hemodynamic indices across published studies.
