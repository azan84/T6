---
source_pdf_path: Resources/2605.00538v1.pdf
slug: palaniappan-2026-vessel-graph-reconstruction
ledger_status: TRIAGED
---

# palaniappan-2026-vessel-graph-reconstruction

## Bibliographic
- Title: Vesselpose: Vessel Graph Reconstruction from Learned Voxel-wise Direction Vectors in 3D Vascular Images
- First author / authors: Rajalakshmi Palaniappan, Christoph Karg, Nemesio Navarro-Arambula
- Year: 2026 (preprint dated May 2026)
- Venue: MIDL 2026 (Medical Image Learning and Diagnosis)
- DOI: NOT REPORTED (arXiv:2605.00538v1)

## One-line claim
Proposes Vesselpose, a method for topologically accurate vascular graph reconstruction from 3D images by predicting voxel-wise direction vectors and applying a modified TEASAR algorithm, with novel topological error metrics (false splits, false merges) for robust evaluation of vessel connectivity and branching.

## T6 targeted questions
- **Q-A geometry perturbation**: Not about FFR simulations or segmentation error measurement; focuses on improving vessel graph topological accuracy.
- **Q-B decision flip**: Not mentioned; no diagnostic decision or threshold-based reclassification.
- **Q-C BC tuning**: Not mentioned; no CFD solver boundary condition tuning.
- **Q-D fidelity / quantity**: Not about CFD; purely 3D vessel segmentation and skeletonization. Mentions rat heart micro-CT vasculature but no hemodynamic modeling or WSS/OSI.
- **Q-E data**: Synthetic vascular datasets (single and multi-tree), Parse2022, Reta benchmark, rat heart micro-CT (3 annotated volumes); no FFR data or invasive coronary diagnostics.
- **Q-F meshing**: Extensive discussion of topological correctness in vessel graph reconstruction; addresses false splits and false merges due to imaging artifacts and close vessel proximity. Describes segmentation→skeletonization→graph extraction pipeline with robustness to challenging geometry. No explicit CFD meshing pipeline discussed.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Vessel graph reconstruction with emphasis on topological accuracy and rigorous evaluation metrics; relevant to segmentation→meshing pipeline robustness for coronary networks, but applied to general vascular imaging without coronary-specific context or FFR outcome linkage.
- verdict: LIGHT
- revisit-if: T6 develops metrics for evaluating how segmentation topological errors propagate to FFR predictions, or implements vessel graph-based meshing for coronary CFD models.
