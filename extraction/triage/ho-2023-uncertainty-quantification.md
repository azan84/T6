---
source_pdf_path: Resources/fcvm-10-1164345.pdf
slug: ho-2023-uncertainty-quantification
ledger_status: TRIAGED
---

# ho-2023-uncertainty-quantification

## Bibliographic
- Title: Uncertainty quantification of computational fluid dynamics-based predictions for fractional flow reserve and wall shear stress of the idealized stenotic coronary
- First author / authors (first 3 + et al.): Ho NN, Lee KY and Lee S-W
- Year: 2023
- Venue: Frontiers in Cardiovascular Medicine
- DOI: 10.3389/fcvm.2023.1164345

## One-line claim
Polynomial chaos expansion-based uncertainty quantification demonstrates that stenosis severity, reference lumen diameter, and coronary resistance are the most impactful parameters for FFR prediction.

## T6 targeted questions
- **Q-A geometry perturbation**: YES—uses IDEALIZED stenotic models with SYNTHETIC variations in geometric parameters (proximal/mid/distal stenosis lengths, reference diameter, stenosis severity ±5%) and physiological parameters (aortic pressure ±10%, resistance ±10%). NOT real inter-observer disagreement; designed perturbations.
- **Q-B decision flip**: NOT reported. Study uses synthetic models, not real patient data. No threshold-based reclassification or FFR ≤0.80 decision analysis.
- **Q-C BC tuning**: YES—addresses boundary conditions critically. Uses 0D lumped-parameter network (Windkessel) at outlet with hyperemic conditions (resistance reduced by 4×). States: "To accommodate the speciﬁc time-varying pressure–ﬂow characteristics of coronary ﬂow, the 0D lumped parameter network modeling technique...was integrated into 3D CFD at the outlet." Studies BC uncertainty via microcirculation resistance. NO re-tuning after geometry change—UQ analysis is ONE-SHOT.
- **Q-D fidelity / quantity**: 3D CFD (P2P1 finite element, tetrahedral mesh ~1 million nodes) coupled with 0D LPN. Reports FFR and time-averaged wall shear stress (AWSS). Sensitivity analysis on WSS and FFR outputs.
- **Q-E data**: Idealized synthetic models only; no patient data or invasive FFR validation.
- **Q-F meshing**: Mesh convergence study conducted. ~1 million nodes chosen (difference <0.5% from 1.8M mesh). Quadratic tetrahedral elements. No discussion of robustness to topological errors in real segmentations.

## Novelty bearing on T6
- bucket: METHOD | BACKGROUND
- one-line reason: Uncertainty quantification framework for CFD-based FFR/WSS; identifies stenosis severity and diameter as dominant parameters; demonstrates importance of BC parameters (resistance) but uses idealized geometry, not real segmentation errors
- verdict: LIGHT
- revisit-if: UQ framework applied to real segmentation uncertainty or error scenarios, or paper demonstrates BC tuning can compensate for geometric uncertainty

