---
source_pdf_path: Resources/1-s2.0-S1361841520301973-main.pdf
slug: bertels-2021-volume-bias-soft-dice
ledger_id: C008
ledger_status: TRIAGED
---

# bertels-2021-volume-bias-soft-dice

## Bibliographic
- Title: Theoretical analysis and experimental validation of volume bias of soft Dice optimized segmentation maps in the context of inherent uncertainty
- First author / authors: Jeroen Bertels, David Robben, Dirk Vandermeulen
- Year: 2021
- Venue: Medical Image Analysis, vol. 67
- DOI: 10.1016/j.media.2020.101833

## One-line claim
Soft Dice loss optimization introduces systematic volume bias in CNN segmentations under high inherent segmentation uncertainty; cross-entropy loss produces unbiased volume estimates but soft Dice bias is reducible via re-calibration.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT EXPLICIT PERTURBATION, but studies inherent segmentation uncertainty (aleatoric and epistemic). Demonstrates that segmentation quality varies with task ambiguity (e.g., post-operative infarction has higher inherent uncertainty than brain tumor segmentation). Quantifies volume bias relative to uncertainty level.
- **Q-B decision flip**: NOT REPORTED. Paper focuses on volume estimation bias, not clinical decision thresholds or reclassification.
- **Q-C BC tuning**: NOT APPLICABLE. Study on CNN segmentation loss functions; no CFD or boundary condition tuning discussed.
- **Q-D fidelity / quantity**: Analyzes how CNN loss functions (cross-entropy vs. soft Dice) affect volume estimation accuracy. No 3D CFD, WSS/OSI, or flow field sensitivity analysis. Focus: voxel-level classification and aggregate volume measures.
- **Q-E data**: Four medical imaging tasks: (1) third molars on dental radiographs (low inherent uncertainty), (2) brain tumors on MRI (BRATS 2018, low uncertainty), (3) post-operative infarction on MRI perfusion (ISLES 2017, high uncertainty), (4) ischemic core on CT perfusion (ISLES 2018, high uncertainty). Public challenge datasets; not coronary-specific.
- **Q-F meshing**: NOT APPLICABLE. CNN-based segmentation; no mesh generation or CFD mesh dependency discussed.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Provides theoretical and experimental evidence that segmentation loss function choice (soft Dice vs. cross-entropy) introduces systematic bias in downstream volume/quantitative measures when inherent segmentation uncertainty is high—directly supporting T6's hypothesis that segmentation error propagates to affect downstream hemodynamic predictions and clinical decisions.
- verdict: FULL
- revisit-if: N/A. This paper is a direct hit on the T6 premise: it proves that (1) different segmentation methods/objectives produce different downstream quantitative errors, and (2) these errors are proportional to the inherent uncertainty in the segmentation task.

## Ideation opening (CFD + imaging)
- Implicit: The paper demonstrates that choice of segmentation optimization objective (soft Dice vs. cross-entropy) systematically affects downstream volume estimates under uncertainty. Extrapolating to CFD+imaging: segmentation method choice may similarly affect downstream hemodynamic predictions (pressure drop, WSS, FFR) and introduce or mask geometric error effects through the CFD pipeline. "Re-calibration" of segmentation bias could parallel BC tuning's role in masking geometric effects.
