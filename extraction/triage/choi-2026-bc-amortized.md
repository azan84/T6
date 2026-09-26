---
source_pdf_path: Resources/2603.19331v1.pdf
slug: choi-2026-bc-amortized
ledger_id: C017
ledger_status: TRIAGED
---

# choi-2026-bc-amortized

## Bibliographic
- Title: FalconBC: Flow matching for Amortized inference of Latent-CONditioned physiologic Boundary Conditions
- First author / authors: Chloe H. Choi, Alison L. Marsden, Daniele E. Schiavazzi
- Year: 2026
- Venue: arXiv:2603.19331v1
- DOI: NOT REPORTED

## One-line claim
Introduces FalconBC, a conditional flow matching framework for amortized inference of physiologic boundary conditions in patient-specific cardiovascular models that jointly handles inflow waveforms, clinical targets, and anatomical features encoded as point cloud embeddings.

## T6 targeted questions
- **Q-A geometry perturbation**: SYNTHETIC. Paper demonstrates handling of aorto-iliac bifurcation with varying stenosis locations and severity; generates point cloud embeddings of stenosis models. Researchers control stenosis severity and location (left/right iliac, 3 locations per side).
- **Q-B decision flip**: NOT REPORTED
- **Q-C BC tuning**: Yes, core focus. Uses RCR-type boundary conditions and three-element Windkessel models. States: "joint estimation of boundary conditions and inflow and/or model anatomy"; demonstrates BC re-tuning with geometry changes ("geometries with left-sided stenosis and right-sided stenosis occupy different regions in output space"); explicitly addresses how segmentation errors and anatomical inaccuracies affect reachability of clinical targets.
- **Q-D fidelity / quantity**: Both 0D and 3D. Zero-dimensional (lumped parameter networks) used for training data generation; 3D CFD mentioned as full-fidelity. No spatial fields (WSS/OSI) reported; focuses on pressure and flow quantities of interest.
- **Q-E data**: Two demonstration models (aorto-iliac bifurcation with stenosis, coronary artery disease model). N = 100, 500, 1000 realizations used for training. No clinical cohort, no invasive-FFR ground truth.
- **Q-F meshing**: NOT REPORTED. Mentions automated LPN creation from 3D model centerlines using SimVascular, but no detail on segmentation-to-surface-to-volume meshing or robustness to poor geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Presents amortized inference framework for physiologic BC tuning that handles joint estimation when geometry changes and explicitly addresses how segmentation/anatomical error prevents target reachability
- verdict: FULL
- revisit-if: Application to FFR decision flip or spatial WSS/OSI sensitivity to geometry variations

## Ideation opening
Paper explicitly states "segmentation uncertainty can influence simulation predictions" and demonstrates how anatomical inaccuracies (stenosis) require joint estimation of BCs and geometry to match clinical targets, directly supporting T6's premise that geometry error propagates through BC tuning to affect hemodynamic predictions.
