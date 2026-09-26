---
source_pdf_path: Resources/071921_1_5.0273041.pdf
slug: amlani-2025-hemodynamics-fourier
ledger_status: TRIAGED
---

# amlani-2025-hemodynamics-fourier

## Bibliographic
- Title: A high-order space-time Fourier continuation approach for one-dimensional hemodynamics and wave propagation in the entire human circulatory system
- First author / authors: Faisal Amlani, Niema M. Pahlevan
- Year: 2025
- Venue: Physics of Fluids
- DOI: 10.1063/5.0273041

## One-line claim
High-order spectral solver for 1D hemodynamics with coupled heart chambers, valves, and 0D Windkessel boundary conditions, validated against community benchmarks.

## T6 targeted questions
- **Q-A geometry perturbation**: No geometric perturbations studied; pure hemodynamic solver validation.
- **Q-B decision flip**: Not addressed; no FFR or diagnostic threshold studied.
- **Q-C BC tuning**: Yes, extensively—includes 0D heart chamber models, valve ODEs, and ODE-based vascular bed boundary conditions (coronary, hepatic, microvasculature). Section II B details Riemann invariants for boundary coupling. However, NO statement that BC parameters are re-tuned after geometry changes, and no discussion of tuning compensating for anatomical/segmentation error.
- **Q-D fidelity / quantity**: 1D (reduced-order only). Pressure/flow waves computed. No WSS or spatially-resolved fields. "Numerically dispersionless resolution of the complete circulatory system" claimed; no tissue perfusion sensitivity reported.
- **Q-E data**: Benchmark validation only (Alastruey/Boileau community problems). No patient cohort. No invasive reference data.
- **Q-F meshing**: Not applicable (1D solver); no 3D segmentation→meshing discussed.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Provides foundational 1D hemodynamic solver framework with coupled BC models useful as reference for comparison, but does not address segmentation error, decision-flip ranking, or BC compensation for geometric fault.
- verdict: LIGHT
- revisit-if: If T6 uses 1D model for coronary BC tuning benchmarking or if the solver's treatment of closed-loop microvascular coupling becomes critical to understand interaction between topological error and outlet resistance.

