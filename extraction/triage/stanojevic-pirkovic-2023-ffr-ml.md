---
source_pdf_path: Resources/diagnostics-13-03349.pdf
slug: stanojevic-pirkovic-2023-ffr-ml
ledger_status: TRIAGED
---

# stanojevic-pirkovic-2023-ffr-ml

## Bibliographic
- Title: Fractional Flow Reserve-Based Patient Risk Classification
- First author / authors: Marijana Stanojević Pirković, Ognjen Pavić, Filip Filipović
- Year: 2023
- Venue: Diagnostics
- DOI: 10.3390/diagnostics13213349

## One-line claim
A random forest machine learning ensemble classifies patients into high-risk (FFR <0.80) or low-risk (FFR >0.80) groups using demographic, clinical, and 3D coronary reconstruction data, achieving 76–83% classification accuracy depending on test-set size.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED — Uses simulated FFR values (not measured invasive FFR); no analysis of segmentation uncertainty or inter-observer disagreement.
- **Q-B decision flip**: INDIRECT — Focuses on patient risk classification at FFR 0.80 threshold but does not report reclassification rates or sensitivity to threshold changes.
- **Q-C BC tuning**: NOT REPORTED — No detail on CFD/numerical method used to generate simulated FFR values; machine learning approach does not address BC tuning.
- **Q-D fidelity / quantity**: Mentions "3D reconstruction of the coronary arteries for the purposes of stenosis monitoring" but no detail on CFD fidelity; NO WSS/OSI.
- **Q-E data**: Small dataset with "simulated FFR values" (not real invasive FFR ground truth); demographic and clinical data from limited cohort.
- **Q-F meshing**: NOT REPORTED — 3D reconstruction mentioned but no detail on meshing or robustness methodology.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Machine learning classification study for FFR-based risk prediction; does not address geometric sensitivity, BC tuning, or computational FFR methodology relevant to T6.
- verdict: LIGHT
- revisit-if: Paper used real invasive FFR ground truth and analyzed sensitivity to segmentation or anatomical complexity

