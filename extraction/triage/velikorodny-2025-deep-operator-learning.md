---
source_pdf_path: Resources/s44387-025-00035-5.pdf
slug: velikorodny-2025-deep-operator-learning
ledger_status: TRIAGED
---

# velikorodny-2025-deep-operator-learning

## Bibliographic
- Title: Deep operator learning for blood flow modelling in stenosed vessels
- First author / authors (first 3 + et al.): Alexis Velikorodny, Lu Lu, Vladimir Dudenkov et al.
- Year: 2025
- Venue: npj Artificial Intelligence
- DOI: 10.1038/s44387-025-00035-5

## One-line claim
A multifidelity machine learning framework combining CFD simulations, in vitro experiments, and operator learning enables rapid and accurate prediction of FFR in coronary stenoses without strict boundary condition dependence.

## T6 targeted questions
- **Q-A geometry perturbation**: Combines synthetic (CFD-generated) and experimental data; no inter-segmenter disagreement study. Magnitude not reported.
- **Q-B decision flip**: NOT REPORTED at FFR threshold
- **Q-C BC tuning**: Windkessel outlet boundary conditions; states goal is to "integrate CFD equations into AI framework to reduce non-physical behavior, especially for intermediate plaques" and "guide the training process" but actual re-tuning after geometry change NOT EXPLICITLY REPORTED. Quote: "hybrid approach, based on integration of CFD equations into a global AI framework, requires development and validation of CFD model optimized for this specific task."
- **Q-D fidelity / quantity**: Reduced-order 1D CFD model with full FSI capability; demonstrated on simplified geometry; future work planned for complex 3D stenosis morphologies and full validation with in vivo data.
- **Q-E data**: Synthetic coronary anatomies (12,000 models), in vitro experiments (Young & Tsai setup), N=30 patient-specific models with CCTA and FFR; CCTA invasive FFR comparison reported (r=0.94).
- **Q-F meshing**: NOT EXPLICITLY REPORTED for segmentation→surface→volume robustness; mentions simplified experimental setup to avoid poorly-constrained parameters.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates multifidelity ML + reduced-order CFD for FFR prediction; highlights value of integrating physics-based constraints into data-driven models to guide training and improve generalization without high-fidelity 3D CFD.
- verdict: FULL
- revisit-if: Examine if BC tuning is re-done post-geometry perturbation; check final paper for in vivo validation and comparison with high-fidelity 3D models.
