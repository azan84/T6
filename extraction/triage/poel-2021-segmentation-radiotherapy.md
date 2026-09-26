---
source_pdf_path: Resources/1-s2.0-S1361841521002073-main.pdf
slug: poel-2021-segmentation-radiotherapy
ledger_id: C009
ledger_status: TRIAGED
---

# poel-2021-segmentation-radiotherapy

## Bibliographic
- Title: The predictive value of segmentation metrics on dosimetry in organs at risk of the brain
- First author / authors: Robert Poel, Elias Rüfenacht, Evelyn Hermann
- Year: 2021
- Venue: Medical Image Analysis, vol. 73
- DOI: 10.1016/j.media.2021.102161

## One-line claim
Investigates correlation between geometric segmentation metrics (Dice, Hausdorff distance) and dosimetric changes for organs at risk in brain radiotherapy planning, finding poor correlation and advocating for clinically oriented metrics.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper studies segmentation quality variation from alternative contours (manual raters, deep learning, contour manipulation) but does not address lumen/segmentation uncertainty in vascular contexts. Focus is radiotherapy, not cardio.
- **Q-B decision flip**: NOT APPLICABLE. Paper focuses on dose distribution changes, not diagnostic thresholds or reclassification.
- **Q-C BC tuning**: NOT APPLICABLE. Radiotherapy planning does not involve BC tuning or hemodynamic boundary conditions.
- **Q-D fidelity / quantity**: NOT APPLICABLE. Radiation dose planning, not CFD/hemodynamics or WSS.
- **Q-E data**: Retrospective glioblastoma multiforme cohort (12 cases selected from database). No invasive ground truth; focus is on dosimetric outcome (dose to organs at risk).
- **Q-F meshing**: NOT APPLICABLE. Radiotherapy segmentation and dose calculation, no CFD meshing.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Paper addresses medical image segmentation metrics in radiotherapy planning (brain OAR contouring), entirely outside cardiovascular CFD and FFR domains.
- verdict: LIGHT
- revisit-if: Paper demonstrates segment quality → clinical impact (dosimetry) but in oncology, not cardio; only relevant if T6 explores *generic* principles of segmentation error propagation.

## Ideation opening (CFD + imaging)
- None stated. Paper is in radiotherapy domain; no CFD or cardiac imaging work mentioned.
