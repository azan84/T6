---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2020 - Seo - The effects of clinically‐derived parametric data uncertainty in patient‐specific.pdf
slug: seo-2020-effects-parametric
ledger_status: TRIAGED
---

# seo-2020-effects-parametric

## Bibliographic
- Title: The effects of clinically-derived parametric data uncertainty in patient-specific coronary simulations with deformable walls
- First author / authors (first 3): Jongmin Seo, Daniele E. Schiavazzi, Andrew M. Kahn
- Year: 2020
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3351

## One-line claim
Uncertainty quantification applied to a patient-specific left coronary artery model with deformable walls demonstrates that uncertainty in inlet/intramyocardial pressures and morphometry exponent significantly affects FFR, pressure, flow, and wall shear stress predictions.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT systematically perturb coronary geometry or measure inter-observer lumen segmentation disagreement. Instead, studies uncertainty in MODEL PARAMETERS (pressure waveforms, intramyocardial pressure, wall elastic modulus, morphometry exponent for resistance distribution). Geometry assumed fixed from CT reconstruction.
- **Q-B decision flip**: FFR used as benchmark clinical outcome; paper assesses variability in FFR predictions due to input parameter uncertainty. NO explicit reporting of FFR threshold ≤0.80 decision classification or flip rates across uncertain parameter scenarios.
- **Q-C BC tuning**: Lumped parameter network (LPN) outlet boundary conditions prescribed with morphometry exponent controlling resistance distribution. Uncertainty propagation studies effect of morphometry exponent (used to distribute downstream resistance to outlets) on FFR. "Variability in the morphometry exponent...has little effect on coronary hemodynamics or wall mechanics." NO mention of tuning BCs to compensate for segmentation/topological error.
- **Q-D fidelity / quantity**: 3D CFD with deformable walls via ALE framework and fluid-structure interaction (svFSI). Reports branch pressure, flow, wall shear stress, and wall deformation under uncertainty. Multi-wavelet stochastic expansion used for uncertainty propagation.
- **Q-E data**: Single patient-specific left coronary artery model from CT. Clinical parameters (pressure, elastic modulus) gathered from literature or intra-coronary catheterization data. NO invasive FFR ground-truth validation of UQ predictions.
- **Q-F meshing**: SimVascular used for geometry reconstruction from CT. Wall thickness 0.08 mm prescribed. NO study of segmentation robustness to poor/broken geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Applies comprehensive UQ/SA framework to patient-specific coronary FFR under parametric uncertainty; demonstrates that inlet pressure and intramyocardial pressure variability dominate FFR uncertainty. Does not address segmentation error ranking or BC-tuning compensation.
- verdict: LIGHT
- revisit-if: Paper extends to study FFR sensitivity to segmentation-derived geometry uncertainty or compares FFR variability with/without BC tuning to patient-specific data.

