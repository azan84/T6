---
source_pdf_path: Resources/Computer aided Civil Eng - 2025 - Han - Pretrained graph neural network for embedding semantic  spatial  and topological.pdf
slug: han-2025-bim-neural
ledger_status: TRIAGED
---

# han-2025-bim-neural

## Bibliographic
- Title: Pretrained graph neural network for embedding semantic, spatial, and topological data in building information models
- First author / authors (first 3 + et al.): Jin Han, Xin-Zheng Lu, Jia-Rui Lin, et al.
- Year: 2025
- Venue: Computer-Aided Civil and Infrastructure Engineering
- DOI: 10.1111/mice.70073

## One-line claim
This paper develops BIGNet, a large-scale pretrained graph neural network to learn and reuse multidimensional design features embedded in BIM (building information modeling) models for automated design checking and lifecycle management.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT APPLICABLE. Paper addresses building component modeling, not vascular/medical geometry or segmentation error.
- **Q-B decision flip**: NOT APPLICABLE. No medical decision thresholds or diagnostic reclassification studied.
- **Q-C BC tuning**: NOT APPLICABLE. No haemodynamic boundary conditions, outlet resistance, or parameter tuning discussed.
- **Q-D fidelity / quantity**: NOT APPLICABLE. No CFD, fluid dynamics, or spatially-resolved hemodynamic fields. Focuses on building design checking.
- **Q-E data**: Dataset: ~1 million nodes and 3.5 million edges in BIM models; domain is architectural/construction, not medical.
- **Q-F meshing**: NOT APPLICABLE. Addresses building component topology, not vascular mesh generation or segmentation robustness.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: This is a civil engineering paper about building design checking using graph neural networks; it has no bearing on coronary artery segmentation, FFR decision-making, digital twin validation in healthcare, or haemodynamic modeling.
- possible-other-project: Building information modeling and semantic-topological design feature learning in construction/civil engineering
- verdict: LIGHT
- revisit-if: None; paper is not applicable to T6 research domain
