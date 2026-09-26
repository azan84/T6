---
source_pdf_path: Resources/2404.14187v2.pdf
slug: richter-2024-windkessel-bayesian
ledger_id: C015
ledger_status: TRIAGED
---

# richter-2024-windkessel-bayesian

## Bibliographic
- Title: Bayesian Windkessel calibration using optimized 0D surrogate models
- First author / authors: Jakob Richter, Jonas Nitzler, Luca Pegolotti
- Year: 2024 (arXiv preprint)
- Venue: arXiv:2404.14187v2 [cs.CE]
- DOI: N/A (preprint)

## One-line claim
Proposes efficient Bayesian framework for calibrating three-element Windkessel boundary condition parameters in cardiovascular 3D CFD using a high-accuracy zero-dimensional surrogate model optimized from a single 3D simulation, enabling high-dimensional posterior distribution estimation from noisy clinical measurements with minimal computational cost.

## T6 targeted questions
- **Q-A geometry perturbation**: SYNTHETIC GEOMETRY PERTURBATIONS EVALUATED. Paper applies method to "publicly available vascular models" (aorta, aortofemoral, coronary, pulmonary); shows optimized 0-D models generalize to "a wide range of BCs." Does not explicitly perturb geometry, but demonstrates robustness across anatomical variations (72 models tested).
- **Q-B decision flip**: NOT REPORTED. Focus is on pressure/flow predictions and BC posterior uncertainty quantification, not diagnostic reclassification. No FFR thresholds discussed.
- **Q-C BC tuning**: HIGHLY RELEVANT. Core contribution: deterministic least-squares optimization of 0-D Windkessel parameters (resistances, inductances, capacitances, non-linear stenosis factors) to match initial 3D CFD data. Text: "We propose a deterministic least-squares procedure to optimize a 0D model to match an initial 3D model. Our algorithm optimizes all 0D parameters in the model." Windkessel parameters are then re-calibrated via Sequential Monte Carlo (SMC) to infer posterior distribution given noisy clinical observations. Demonstrates: "Optimizing 0D models to match 3D data a priori lowered their median approximation error by nearly one order of magnitude in 72 publicly available vascular models."
- **Q-D fidelity / quantity**: Hybrid 0D/3D approach. Paper solves full 3D CFD once for initial BC choice, then uses optimized 0-D surrogate for uncertainty quantification and BC parameter inference. No spatially resolved 3D outputs (WSS, OSI) analyzed for sensitivity to BC; focus is on bulk flow and pressure at outlets.
- **Q-E data**: 72 publicly available vascular models (aorta, aortofemoral, coronary, pulmonary). No patient cohort; method validated on synthetic data with controlled noise levels (signal-to-noise ratios). No invasive FFR ground truth.
- **Q-F meshing**: NOT REPORTED in extracted text. Paper applies method to existing published vascular geometries; no detail on segmentation→meshing pipeline or robustness to poor geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Presents practical workflow for Windkessel BC calibration and uncertainty quantification in subject-specific CFD using 0-D/3D multiscale coupling; directly relevant to T6's Q-C (BC tuning) and hypothesis that BC parameters are geometry-dependent.
- verdict: FULL
- revisit-if: N/A — paper is a THREAT candidate (demonstrates BC tuning methodology that T6 will cite for numerical protocol) and METHOD (surrogate-based calibration technique T6 could adopt or reference for UQ framework).

## Ideation opening (CFD + imaging)
- Paper states: "Windkessel BC parameters are patient-specific, meaning they must be calibrated for each patient based on clinical measurements" and "accurate representation by a probability distribution over a range of possible values rather than discrete parameter values." Implies T6's research gap: (1) How does segmentation error (geometry uncertainty) propagate into BC calibration? (2) Can we separate measurement noise from geometric error in BC posterior distributions? (3) Does BC posterior change significantly when geometry is perturbed by realistic segmentation error?
