---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2025 - Dalmaso - Uncertainty Quantification and Sensitivity Analysis for Non‐invasive.pdf
slug: dalmaso-2025-uncertainty-ifr
ledger_status: TRIAGED
---

# dalmaso-2025-uncertainty-ifr

## Bibliographic
- Title: Uncertainty Quantification and Sensitivity Analysis for Non-invasive Model-Based Instantaneous Wave-Free Ratio Prediction
- First author / authors (first 3 + et al.): Caterina Dalmaso, Fredrik Eikeland Fossan, Anders Tjellaug Bråten
- Year: 2025
- Venue: International Journal for Numerical Methods in Biomedical Engineering (Special Issue)
- DOI: 10.1002/cnm.3898

## One-line claim
Polynomial chaos UQ on 1D-0D coronary model reveals that iFR predictions are most sensitive to vascular geometry and steady-state flow, but relatively insensitive to inlet pressure waveform or compliance; 1D-0D estimates show −0.036 bias vs. invasive iFR (±0.101).

## T6 targeted questions
- **Q-A geometry perturbation**: SYNTHETIC (parameter ranges). Uncertainty in six parameters: vascular radius, coronary flow, compliance, aortic pressure, LV pressure, inlet pressure waveform. Analyzed via polynomial chaos expansion; no real segmentation disagreement studied.
- **Q-B decision flip**: YES, threshold behavior analyzed. 52 patients, 81 invasive iFR measurements. iFR prevalence 24.69% for cutoff iFR < 0.89. Bias analysis between computational and invasive iFR reported (−0.036 ± 0.101), indicating prediction drift near thresholds.
- **Q-C BC tuning**: 1D distributed stenosis model coupled to 0D Mantero-Windkessel models at outlets. Sensitivity analysis shows that compliance (transient BC parameter) has negligible effect on iFR compared to geometry. No mention of BC re-tuning after geometry changes; boundary conditions appear fixed per patient.
- **Q-D fidelity / quantity**: 1D-0D transient unsteady solver (1D main epicardial arteries + 0D coronary microcirculation). No WSS/OSI. Resting Pd/Pa ratio computed; steady-state simulations shown to adequately replace unsteady for iFR prediction.
- **Q-E data**: 52 patients with stable CAD, 81 invasive iFR measurements (ground truth present). CCTA-derived geometry.
- **Q-F meshing**: NOT REPORTED. Segmentation via stenosis detection algorithm; no mesh or meshing robustness detail.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Large-scale UQ on real patient cohort (52 patients) shows that geometric uncertainty dominates BC parameter uncertainty in iFR prediction; supports T6's focus on geometry error ranking. Identifies geometry/flow as critical vs. transient BC effects.
- verdict: FULL
- revisit-if: N/A – directly relevant to T6's hypothesis that geometry error is the dominant source of iFR/FFR variance.
