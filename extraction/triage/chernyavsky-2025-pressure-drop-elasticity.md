---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2025 - Chernyavsky - Investigation of the Pressure Drop in Arterial Models With Stenoses Using.pdf
slug: chernyavsky-2025-pressure-drop-elasticity
ledger_status: TRIAGED
---

# chernyavsky-2025-pressure-drop-elasticity

## Bibliographic
- Title: Investigation of the Pressure Drop in Arterial Models With Stenoses Using Numerical and Experimental In Vitro Approaches: Effect of Elasticity
- First author / authors (first 3 + et al.): B. Chernyavsky, N. Mouzali, V. Glanz
- Year: 2025
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.70099

## One-line claim
In vitro and CFD validation of 1D reduced-order solver with empirical stenosis model (Young-Tsai pressure loss coefficients) calibrated on elastic arteries; demonstrates that elasticity and pulsatile flow substantially affect pressure drop prediction near FFR 0.80.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (synthetic). Experiments on elastic tube models with fixed stenosis (50–80% blockage ratio); no inter-observer segmentation variation studied.
- **Q-B decision flip**: YES, borderline FFR near 0.80 emphasized. "Of particular interest for the main goal of providing decision support for medical practitioners is a flow through stenosis." Intermediate lesions (60% blockage, FFR ~0.80) identified as critical decision zone; fine-tuning resistance coefficients "substantially improve the accuracy of the pressure drop prediction in the intermediate lesions, specifically relevant for clinical applications."
- **Q-C BC tuning**: 1D model with semi-empirical stenosis pressure loss via Young-Tsai coefficients; no Windkessel BC mentioned. Viscous and turbulent resistance coefficients manually tuned via in vitro experiments to calibrate the reduced-order solver. Tuning approach is pre-calibration, not post-geometry-change adaptation.
- **Q-D fidelity / quantity**: Reduced-order 1D solver with empirical stenosis model; NO WSS/OSI. Validates pressure drop only.
- **Q-E data**: 13 in vitro experiments on elastic tube models (no patient data, no invasive FFR).
- **Q-F meshing**: NOT REPORTED. In vitro tests only, no segmentation pipeline.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Provides empirical calibration of reduced-order pressure loss model for intermediate stenosis severity; validates that elasticity effects cannot be ignored in FFR prediction, supporting T6's premise that geometry details matter.
- verdict: LIGHT
- revisit-if: Extends to patient-specific coronary geometries and compares coefficient-tuning robustness under segmentation uncertainty.
