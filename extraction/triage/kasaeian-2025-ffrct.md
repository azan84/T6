---
source_pdf_path: Resources/jcdd-12-00279.pdf
slug: kasaeian-2025-ffrct
ledger_status: TRIAGED
---

# kasaeian-2025-ffrct

## Bibliographic
- Title: Fractional Flow Reserve from Coronary CT: Evidence, Applications, and Future Directions
- First author / authors (first 3 + et al.): Arta Kasaeian, Mohadese Ahmadzade, Taylor Hoffman
- Year: 2025
- Venue: Journal of Cardiovascular Development and Diseases
- DOI: 10.3390/jcdd12080279

## One-line claim
Clinical review of FFR-CT diagnostic accuracy and emerging applications in stable and acute CAD, with emphasis on reducing unnecessary invasive procedures.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No discussion of segmentation uncertainty or inter-observer disagreement quantification.
- **Q-B decision flip**: IMPLICIT. FFR-CT Class IIa recommendation for ≥40–90% stenosis; FFR ≤0.80 threshold is standard but no reclassification rates reported.
- **Q-C BC tuning**: NOT REPORTED. No discussion of boundary condition setting, tuning protocols, or sensitivity to BC variation.
- **Q-D fidelity / quantity**: YES. Mentions 3D CFD and CFD computation but focus is diagnostic accuracy and clinical applications; no detail on meshing or solver specifics, no WSS/OSI extraction mentioned.
- **Q-E data**: SCOT-HEART (23% treatment change with CT vs 5% with standard care) and DISCHARGE trials cited; cohort sizes for single studies not systematically reported.
- **Q-F meshing**: NOT REPORTED. Mentions image quality requirements and access/cost limitations but no technical detail on meshing or robustness.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Clinical review of FFR-CT without novel methodology or detailed technical discussion of BC tuning or error characterization; primarily addresses diagnostic gatekeeping role.
- verdict: LIGHT
- revisit-if: New data on FFR-CT accuracy in specific subgroups or with poor image quality; segmentation error quantification.
