---
source_pdf_path: Resources/s12872-023-03447-w.pdf
slug: farhad-2023-artificial-intelligence-ffr
ledger_status: TRIAGED
---

# farhad-2023-artificial-intelligence-ffr

## Bibliographic
- Title: Artificial intelligence in estimating fractional flow reserve: a systematic literature review of techniques
- First author / authors (first 3 + et al.): Farhad A, Rabiei R, Hosseini A, et al.
- Year: 2023
- Venue: BMC Cardiovascular Disorders
- DOI: 10.1186/s12872-023-03447-w

## One-line claim
Systematic review showing AI methods (ML/DL) can non-invasively estimate FFR from medical imaging, providing clinical performance for CAD diagnosis without invasive procedures.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (systematic review of AI FFR estimation; does not address geometry perturbation or uncertainty quantification)
- **Q-B decision flip**: NOT REPORTED (review focuses on FFR estimation accuracy but does not report reclassification rates at 0.80 threshold)
- **Q-C BC tuning**: NOT REPORTED (no discussion of boundary condition tuning; review is of AI/ML prediction methods, not physics-based CFD)
- **Q-D fidelity / quantity**: Reduced-order via machine learning/deep learning on imaging features; 25 included studies use various modalities (CCTA, XCA, OCT, IVUS). No 3D CFD or WSS/OSI reported.
- **Q-E data**: Five hundred seventy-three articles screened; 25 finally selected for review. Private datasets across studies; invasive FFR used as reference in original studies, not reported here.
- **Q-F meshing**: NOT REPORTED (review of AI methods; no segmentation→surface→volume meshing discussed)

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Surveys AI/ML approaches for non-invasive FFR; relevant as background on ML-based FFR estimation alternatives but not directly on T6's focus on CFD + real-error-driven perturbation.
- verdict: LIGHT
- revisit-if: Paper discusses boundary condition requirements or error propagation in AI-based FFR models

