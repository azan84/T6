---
source_pdf_path: Resources/2025.02.04.25321638v1.full.pdf
slug: criseo-2025-digital-twin
ledger_status: TRIAGED
---

# criseo-2025-digital-twin

## Bibliographic
- Title: Development of a digital twin for the diagnosis of cardiac perfusion defects
- First author / authors (first 3 + et al.): Elisabetta Criseo, Andrea Baggiano, Giovanni Montino Pelagi
- Year: 2025
- Venue: medRxiv preprint
- DOI: https://doi.org/10.1101/2025.02.04.25321638

## One-line claim
A digital twin coupling 3D coronary Navier-Stokes with a three-compartment myocardial Darcy model, blindly calibrated on 6 patients, predicts myocardial blood flow on 28 validation patients with reasonable accuracy.

## T6 targeted questions
- **Q-A geometry perturbation**: The paper does NOT perturb or measure inter-observer/inter-segmenter segmentation uncertainty. It uses AI methods (U-Net) for automatic coronary and myocardial geometry reconstruction. NOT REPORTED regarding synthetic vs real uncertainty magnitudes.
- **Q-B decision flip**: NOT REPORTED. The paper focuses on myocardial blood flow (MBF) classification (at-risk vs non-at-risk based on MBF < 230 ml/min/100g), not FFR-based revascularization decisions.
- **Q-C BC tuning**: The paper employs a region and volume-based blinded calibration approach: "We calibrate such computational model with a region and volume based approach using anatomical data from six representative patients; then we apply the calibration to the remaining 28 patients." Uses patient-specific aortic pressure as boundary condition input. No explicit re-tuning after geometry perturbations; does not address whether tuning compensates for geometric error.
- **Q-D fidelity / quantity**: Coupled 3D coronary Navier-Stokes with three-compartment compliant Darcy myocardial microvasculature model (reduced-order for tissue). Does NOT report WSS/OSI sensitivity to geometry changes.
- **Q-E data**: 34 patients total (6 for calibration, 28 validation); stress-CTP imaging data; NOT REPORTED whether invasive FFR ground truth available.
- **Q-F meshing**: Non-uniform tetrahedral mesh with element size scaled to vessel radius. Geometry smoothing and manual branching corrections applied. Computational mesh reconstruction time ~30 minutes per case. No detailed robustness analysis on poor/topologically incorrect geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates blinded boundary condition calibration on patient-specific data and coupling 3D/reduced-order models for functional prediction, relevant to T6's BC tuning strategy.
- verdict: LIGHT
- revisit-if: If paper reports results of perturbing geometry and re-calibrating BC parameters; or addresses whether calibration transfers across different stenosis severities.
