---
source_pdf_path: Resources/1-s2.0-S0010482524012472-main.pdf
slug: bransby-2024-ivus-segmentation
ledger_status: TRIAGED
---

# bransby-2024-ivus-segmentation

## Bibliographic
- Title: POLYCORE: Polygon-based contour refinement for improved Intravascular Ultrasound Segmentation
- First author / authors: Kit Mills Bransby, Retesh Bajaj, Anantharaman Ramasamy
- Year: 2024
- Venue: Computers in Biology and Medicine
- DOI: 10.1016/j.compbiomed.2024.109162

## One-line claim
POLYCORE combines polygon and dense segmentation representations to achieve both topological correctness and pixel-level accuracy in IVUS vessel wall segmentation, particularly in artefact-ridden regions.

## T6 targeted questions
- **Q-A geometry perturbation**: Not about perturbing geometry or measuring segmentation uncertainty for CFD purposes; focuses on improving segmentation of existing IVUS images rather than measuring inter-observer disagreement magnitudes.
- **Q-B decision flip**: No mention of FFR or diagnostic reclassification at any threshold.
- **Q-C BC tuning**: Not mentioned; no boundary condition or CFD modeling discussed.
- **Q-D fidelity / quantity**: Not about CFD; purely 2D segmentation in IVUS B-mode images. No WSS/OSI or hemodynamic outputs.
- **Q-E data**: NIRS-IVUS and IVUS-2011 datasets mentioned; multiple cardiologists annotated data; invasive FFR ground truth status NOT REPORTED.
- **Q-F meshing**: Addresses topological correctness of contours in segmentation, but does not discuss segmentation-to-surface-to-volume meshing pipeline or robustness to broken/topologically incorrect geometry as input to CFD.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Segmentation improvement technique for IVUS imaging, not about measuring segmentation error effects on FFR decisions or CFD validation.
- verdict: LIGHT
- revisit-if: T6 decides to compare segmentation algorithms, or cites improved IVUS as motivation for better geometry input to CFD models.
