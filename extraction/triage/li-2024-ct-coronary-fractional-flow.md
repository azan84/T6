---
source_pdf_path: Resources/s12880-024-01465-4.pdf
slug: li-2024-ct-coronary-fractional-flow
ledger_status: TRIAGED
---

# li-2024-ct-coronary-fractional-flow

## Bibliographic
- Title: CT coronary fractional flow reserve based on artificial intelligence using different software: a repeatability study
- First author / authors (first 3 + et al.): Li J, Yang Z, Sun Z, et al.
- Year: 2024
- Venue: BMC Medical Imaging
- DOI: 10.1186/s12880-024-01465-4

## One-line claim
Study assesses consistency and reliability of CT-FFR measurements across different commercial software platforms (K and S vendors), identifying factors influencing measurement discrepancies.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (study measures repeatability across software, not geometry perturbation or inter-observer segmentation uncertainty)
- **Q-B decision flip**: Reported misclassification between software platforms at diagnostic thresholds; "6% of the points (14 out of 216) fell outside the 95% consistency level" in Bland-Altman analysis. Implies potential diagnostic reclassification but not explicitly at FFR 0.80.
- **Q-C BC tuning**: NOT REPORTED (study compares two commercial CFD packages but does not discuss boundary condition tuning protocols or whether tuning is re-done for geometry changes)
- **Q-D fidelity / quantity**: CT-FFR computed from CCTA via K and S commercial software (vendor-specific AI/CFD hybrid approaches). Reduced-order via proprietary algorithms; no detail on 3D CFD, WSS/OSI, or sensitivity to geometry.
- **Q-E data**: 103 participants, 216 vessel segments analyzed. Retrospective; invasive FFR not reported as ground truth. Private cohort (June 2020–July 2021, single hospital).
- **Q-F meshing**: NOT REPORTED (commercial software; no detail on segmentation→mesh workflow or robustness on poor geometry)

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Documents inter-software CT-FFR variability and factors affecting reproducibility (heart rate, image quality, lumen diameter), relevant for clinical context but does not advance T6's methodology or hypothesis on error-BC coupling.
- verdict: LIGHT
- revisit-if: Paper reports how BC tuning or meshing robustness differs between software vendors

