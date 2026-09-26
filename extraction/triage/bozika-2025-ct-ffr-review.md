---
source_pdf_path: Resources/biomedicines-13-01969.pdf
slug: bozika-2025-ct-ffr-review
ledger_status: TRIAGED
---

# bozika-2025-ct-ffr-review

## Bibliographic
- Title: Clinical Impact of CT-Based FFR in Everyday Cardiology: Bridging Computation and Decision-Making
- First author / authors: Maria Bozika, Anastasios Apostolos, Kassiani-Maria Nastouli
- Year: 2025
- Venue: Biomedicines
- DOI: 10.3390/biomedicines13081969

## One-line claim
Comprehensive review of CT-FFR technology (CFD and machine learning platforms) showing its clinical utility as gatekeeper to invasive angiography, with emphasis on computational methods, validation data, and practical limitations in real-world implementation.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED — No systematic analysis of segmentation uncertainty or inter-observer disagreement in this review.
- **Q-B decision flip**: GENERAL REFERENCE — States "Hemodynamic significance is indicated by a threshold of ≤0.80" and discusses FFR threshold's role but does not report specific reclassification rates for this study.
- **Q-C BC tuning**: MENTIONED BUT NOT DETAILED — States "To determine pressure and flow along the coronary tree, these models use estimates of microcirculatory resistance, aortic inflow, and geometric features." References CFD and machine learning approaches but does NOT discuss whether BC tuning is re-done after geometry changes or whether tuning compensates for anatomical error.
- **Q-D fidelity / quantity**: Reviews both 3D CFD (Navier-Stokes solutions) and reduced-order (0D/1D) solvers; mentions machine learning approaches (cFFRML, DVFFR, uFFRCT); NO WSS/OSI reported in this review.
- **Q-E data**: Review of multiple platforms and studies (HeartFlow, on-site ML); notes "approximately 10–12% of datasets were rejected for FFRCT analysis due to suboptimal imaging."
- **Q-F meshing**: NOT ADDRESSED — Brief mention of "high-quality imaging" requirement but no detail on meshing or robustness to poor/topologically incorrect geometry.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive review of CT-FFR clinical validation and platforms; establishes FFR-based decision-making as clinically relevant, but does not address geometric robustness or BC tuning methodology.
- verdict: LIGHT
- revisit-if: Review included systematic analysis of BC tuning effects on FFR accuracy across different anatomies or geometric error scenarios

