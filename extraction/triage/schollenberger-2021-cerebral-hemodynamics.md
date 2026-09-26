---
source_pdf_path: Resources/fbioe-09-722445.pdf
slug: schollenberger-2021-cerebral-hemodynamics
ledger_status: TRIAGED
---

# schollenberger-2021-cerebral-hemodynamics

## Bibliographic
- Title: A Combined Computational Fluid Dynamics and Arterial Spin Labeling MRI Modeling Strategy to Quantify Patient-Specific Cerebral Hemodynamics in Cerebrovascular Occlusive Disease
- First author / authors (first 3 + et al.): Schollenberger J, Osborne NH, Hernandez-Garcia L and Figueroa CA
- Year: 2021
- Venue: Frontiers in Bioengineering and Biotechnology
- DOI: 10.3389/fbioe.2021.722445

## One-line claim
Strategy combining CFD with ASL-MRI to calibrate and validate patient-specific cerebral hemodynamic models for assessing stenosis impact on blood flow.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb segmentation; uses patient-specific anatomies from MRA/CTA. NOT measuring segmentation disagreement.
- **Q-B decision flip**: NOT reported. Paper uses fractional flow index (FF ≈ FFR analogue) with 0.80 threshold: "Using a threshold of FF = 0.8, only the RICA stenosis in patient 1 would be deemed to be hemodynamically significant." Shows divergence between anatomic (diameter reduction) and functional metrics but no reclassification rates.
- **Q-C BC tuning**: YES—explicitly calibrates outflow BCs: "Patient-Specific Calibration of Outflow Boundary Conditions for the CFD Models" and "tuning of the outflow boundary conditions to match the estimated flow splits." Tuning done ONCE per patient at baseline; NOT re-tuned after geometry perturbation (no perturbations used). BC tuning is for accuracy, not error compensation.
- **Q-D fidelity / quantity**: 3D CFD with finite element (Navier-Stokes). Reports pressure and flow; collateral flow quantified via Lagrangian particle tracking. No explicit WSS/OSI.
- **Q-E data**: N=3 (2 CVOD patients + 1 control), private dataset, MRI/CTA-based, NO invasive pressure ground truth.
- **Q-F meshing**: Mentions 3D geometric reconstruction using CRIMSON, mesh refinement via gradient-based adaptation. No discussion of robustness to topological errors or broken geometry.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Cerebrovascular (not coronary) model; demonstrates FFR-like thresholding and BC calibration strategy but in different vascular bed; no segmentation error or error-absorption focus
- verdict: LIGHT
- revisit-if: Paper applies method to coronary arteries OR addresses segmentation error robustness

