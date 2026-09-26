---
source_pdf_path: Resources/Non-Invasive_Assessment_of_Coronary_Microvascular_Dysfunction_Using_Vascular_Deformation-Based_Flow_Estimation.pdf
slug: xue-2024-vascular-deformation-flow
ledger_status: TRIAGED
---

# xue-2024-vascular-deformation-flow

## Bibliographic
- Title: Non-Invasive Assessment of Coronary Microvascular Dysfunction Using Vascular Deformation-Based Flow Estimation
- First author / authors (first 3): Xiaofei Xue, Dan Deng, Heye Zhang
- Year: 2024
- Venue: IEEE Transactions on Biomedical Engineering, Vol. 71, No. 10
- DOI: 10.1109/TBME.2024.3406416

## One-line claim
A vascular deformation-based flow estimation (VDFE) model uses multi-phase CTA-extracted vascular deformation as an inverse constraint to estimate patient-specific coronary blood flow and compute the index of microcirculatory resistance (IMRCT) non-invasively for CMD diagnosis.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb geometry. Instead, VDFE uses multi-phase CTA to extract vascular deformation (cross-sectional area variation) over the cardiac cycle; inverse problem solving applied to deduce blood flow from observed deformation. No synthetic perturbations; no inter-observer disagreement quantification.
- **Q-B decision flip**: NOT reported. Paper focuses on microvascular dysfunction (CMD) and IMRCT, not FFR ≤0.80 decision classification. IMR threshold NOT discussed in extracted text.
- **Q-C BC tuning**: Uses lumped parameter model (LPM) as outlet boundary condition. Tuning is performed via "simulated annealing algorithm and error weight optimization strategy" to match extracted vascular deformation, but this is for resting coronary flow estimation NOT for compensating for geometric error. BCs tuned to match measured deformation, not re-tuned after perturbation.
- **Q-D fidelity / quantity**: 3D CFD simulations for IMRCT computation after boundary conditions are optimized. Focus on resting and hyperemic coronary blood flow (CBF) rather than spatially-resolved fields like WSS/OSI.
- **Q-E data**: N=106 vessels from 89 subjects; invasive IMR measurement as ground truth. Multi-phase CTA imaging; public/private status NOT reported.
- **Q-F meshing**: Uses tracking and registration techniques to extract coronary centerline and cross-sectional area from multi-phase CTA. No detail on meshing robustness or handling of topologically incorrect segmentations.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Focuses on non-invasive IMRCT for microvascular dysfunction diagnosis; does not address FFR ≤0.80 stenosis classification, segmentation error ranking, or BC tuning to mask geometric error.
- verdict: LIGHT
- revisit-if: Paper extends to FFR-based decision classification or quantifies sensitivity of FFR to segmentation-derived geometry uncertainty.

