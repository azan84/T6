---
source_pdf_path: Resources/2410.21160v2.pdf
slug: zhao-2026-retinal-vessel-segmentation
ledger_status: TRIAGED
---

# zhao-2026-retinal-vessel-segmentation

## Bibliographic
- Title: Kalman Filter Based Linear Deformable for Retinal Vessel Segmentation
- First author / authors: Zhihao Zhao, Yinzheng Zhao, Junjie Yang
- Year: 2026 (preprint dated April 2026)
- Venue: IEEE Transactions on Medical Imaging (inferred)
- DOI: NOT REPORTED (arXiv:2410.21160v2)

## One-line claim
Proposes KaLDeX, a Kalman filter-based linear deformable cross-attention network that combines U-Net++ with topological loss functions to improve retinal vessel segmentation accuracy, particularly for small and faint vascular structures.

## T6 targeted questions
- **Q-A geometry perturbation**: Not about FFR simulations or segmentation error magnitude measurement; focuses on improving retinal segmentation accuracy.
- **Q-B decision flip**: Not mentioned; no diagnostic decision or reclassification at thresholds.
- **Q-C BC tuning**: Not mentioned; no CFD or reduced-order solver boundary conditions.
- **Q-D fidelity / quantity**: Not about CFD; purely retinal vessel segmentation. No WSS/OSI or hemodynamic modeling.
- **Q-E data**: DRIVE, CHASE_BD1, STARE, OCTA-500 datasets (retinal fundus and OCT angiography); no FFR or coronary data; no invasive ground truth.
- **Q-F meshing**: Addresses topological continuity and preservation in segmentation masks using clDice and persistent homology loss, but scope is retinal imaging, not coronary meshing.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Vessel segmentation improvement in retinal imaging; methodologies (topological loss) could inform coronary segmentation but paper is not about coronary arteries, FFR, or hemodynamic modeling.
- verdict: LIGHT
- revisit-if: T6 considers citing topological loss functions for coronary segmentation or compares retinal vs. coronary segmentation challenges.
