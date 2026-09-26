---
source_pdf_path: Resources/978-3-032-16365-3.pdf
slug: bakas-2025-brats-segmentation
ledger_status: TRIAGED
---

# bakas-2025-brats-segmentation

## Bibliographic
- Title: Segmentation, Classification, and Synthesis for Brain Tumors and Traumatic Brain Injuries (MICCAI 2025 Challenges: BraTS-Lighthouse 2025 and AIMS-TBI 2025)
- First author / authors (first 3 + et al.): Spyridon Bakas, Emily Dennis, Mehdi Astaraki et al.
- Year: 2025
- Venue: MICCAI 2025 Challenges proceedings (LNCS 16376), Daejeon, South Korea
- DOI: NOT REPORTED

## One-line claim
Presents a statistically-aware ranking framework (PermRanker) for fair benchmarking of AI segmentation models via permutation testing, evaluated on brain tumor and traumatic brain injury segmentation challenges.

## T6 targeted questions
- **Q-A geometry perturbation**: Addresses segmentation task on brain tumors and TBI; no measurement of lumen/artery segmentation uncertainty or inter-segmenter disagreement reporting. NOT REPORTED for T6 context.
- **Q-B decision flip**: Segmentation quality metrics (Dice, sensitivity, specificity); no diagnostic threshold-based reclassification (FFR-like) reported. NOT REPORTED.
- **Q-C BC tuning**: Not applicable; no CFD or boundary condition modeling for hemodynamics. NOT REPORTED.
- **Q-D fidelity / quantity**: 3D medical image segmentation with Dice-based evaluation; no CFD or WSS/OSI. NOT REPORTED.
- **Q-E data**: MICCAI brain imaging datasets; no invasive ground truth or FFR data. NOT REPORTED.
- **Q-F meshing**: Segmentation challenges focus on image-level accuracy; meshing robustness on topologically incorrect geometry not explicitly addressed. NOT REPORTED.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Establishes state-of-art medical image segmentation evaluation and fair benchmarking methodology; relevant as background on how segmentation model evaluation is conducted in medical imaging generally, though application domain (brain) differs from coronary arteries.
- verdict: LIGHT
- revisit-if: Upgrade to FULL only if paper's PermRanker framework or statistical testing methodology proves directly applicable to T6's error ranking by decision impact (Gate N1). Check whether permutation testing for model pairs provides template for testing whether error-type leads to FFR reclassification.
