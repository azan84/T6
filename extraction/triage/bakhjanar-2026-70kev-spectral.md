---
source_pdf_path: Resources/s10554-026-03613-z.pdf
slug: bakhjanar-2026-70kev-spectral
ledger_status: TRIAGED
---

# bakhjanar-2026-70kev-spectral

## Bibliographic
- Title: Improved diagnostic performance of CT-derived FFR using 70-keV monoenergetic spectral CT in coronary artery disease
- First author / authors: Gylymkhan Bakhjanar, Jung-Joon Cha, Dong Hyuk Cho et al.
- Year: 2026
- Venue: The International Journal of Cardiovascular Imaging
- DOI: 10.1007/s10554-026-03613-z

## One-line claim
Demonstrates that 70-keV monoenergetic spectral CT reconstruction improves image contrast-to-noise ratio and diagnostic accuracy of CT-FFR compared to conventional polychromatic CT for hemodynamically significant coronary stenosis.

## T6 targeted questions

- **Q-A geometry perturbation**: NOT REPORTED. Study focuses on imaging acquisition (spectral vs. conventional polychromatic CT) and its effect on CT-FFR accuracy, not on geometric segmentation uncertainty or inter-observer variability.

- **Q-B decision flip**: YES. Uses FFR <0.80 as threshold for hemodynamically significant stenosis. Reports diagnostic performance: "70-keV CT-FFR, the sensitivity was 88%, specificity was 93%, PPV was 88%, NPV was 93%, and overall accuracy was 92%." Compared conventional CT-FFR accuracy 83% vs. 70-keV 92%.

- **Q-C BC tuning**: NOT DETAILED. Study uses "commercially available software (HeartMed+; AiMEDiC)" for automated CT-FFR calculation. States: "CT-FFR was automatically calculated for each CAD lesion." No discussion of boundary condition tuning strategy or whether it is adjusted post-geometry change.

- **Q-D fidelity / quantity**: 3D CFD-based CT-FFR (automated computational method). Does not report WSS, OSI, or spatially-resolved hemodynamic fields; focuses on FFR values only.

- **Q-E data**: Clinical cohort, 32 patients with 47 coronary lesions. Invasive FFR ground truth present (reference FFR measured during cardiac catheterization). Prospective study (January 2023–December 2024).

- **Q-F meshing**: Mentions reduced field-of-view reconstruction "centered on the heart to enhance spatial resolution and segmentation accuracy" and "medium-sharp B kernel with level 3 iterative reconstruction" but does not discuss segmentation robustness or mesh generation from poor-quality geometries.

## Novelty bearing on T6

- **bucket**: METHOD
- **one-line reason**: Technical enhancement to CT-FFR imaging quality via spectral CT reconstruction; improves FFR diagnostic accuracy but does not address geometric uncertainty or BC tuning dynamics.
- **verdict**: LIGHT
- **revisit-if**: Paper analyzes impact of segmentation uncertainty or image artifacts on FFR across different lesion geometries.
