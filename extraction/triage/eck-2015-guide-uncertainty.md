---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2015 - Eck - A guide to uncertainty quantification and sensitivity analysis for cardiovascular.pdf
slug: eck-2015-guide-uncertainty
ledger_status: TRIAGED
---

# eck-2015-guide-uncertainty

## Bibliographic
- Title: A guide to uncertainty quantification and sensitivity analysis for cardiovascular applications
- First author / authors (first 3): Vinzenz Gregor Eck, Wouter Paulus Donders, Jacob Sturdy
- Year: 2015
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.2755

## One-line claim
A practical guide to global uncertainty quantification (UQ) and variance-based sensitivity analysis (SA) using Monte Carlo and polynomial chaos methods, demonstrated on FFR and arterial compliance models for clinical decision-making in cardiovascular applications.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT measure or study geometric perturbation in this paper. Review/methodology paper. Example uses parametric uncertainty in FFR model (input uncertainties) but NOT segmentation error or inter-observer disagreement.
- **Q-B decision flip**: FFR ≤0.80 threshold mentioned as example in Section 7.3 (FFR model-based estimation), but NO explicit study of decision flip rates or reclassification due to input uncertainty. FFR used as example quantity of interest for UQ/SA demonstration.
- **Q-C BC tuning**: Boundary conditions (lumped parameter models, outlet resistances) discussed as model inputs subject to uncertainty. Mentions "outlet boundary conditions" as critical for patient-specific models but NO emphasis on automated tuning procedures or compensation for geometric error. BC parameters treated as uncertain inputs in sensitivity analysis.
- **Q-D fidelity / quantity**: Covers both reduced-order (0D/1D) and 3D CFD models. Example uses 0D Huo model for FFR; 0D Windkessel for arterial compliance. NO local hemodynamic field outputs (WSS/OSI) in examples.
- **Q-E data**: NOT a data study. Methodology paper using synthetic and literature-based parameter uncertainties. No experimental validation on patient cohorts.
- **Q-F meshing**: NOT applicable. General methodology review; no patient-specific geometries analyzed.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive reference for UQ/SA methodology applicable to cardiovascular models; framework can be applied to study impact of segmentation uncertainty on FFR but does not address coronary error ranking or BC-compensation effects.
- verdict: LIGHT
- revisit-if: Paper extends to quantify FFR uncertainty induced by segmentation error or demonstrates SA on patient-specific coronary models.

