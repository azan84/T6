---
source_pdf_path: Resources/s13239-021-00580-5.pdf
slug: grande-2021-hybrid-coronary-hemodynamics
ledger_status: TRIAGED
---

# grande-2021-hybrid-coronary-hemodynamics

## Bibliographic
- Title: A 1D–3D Hybrid Model of Patient-Specific Coronary Hemodynamics
- First author / authors (first 3 + et al.): Grande Gutiérrez N, Sinno T, Diamond SL
- Year: 2021
- Venue: Cardiovascular Engineering and Technology
- DOI: 10.1007/s13239-021-00580-5

## One-line claim
Hybrid 1D–3D coupled model of coronary blood flow reduces computational cost 40-fold while accurately predicting FFR and wall shear stress at stenosis, validated against full 3D simulations in healthy and diseased conditions.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (model uses healthy reference CTA and virtually introduced 90% area stenosis; no inter-observer segmentation or realistic error quantification)
- **Q-B decision flip**: NOT REPORTED (study validates FFR computation but does not report reclassification at 0.80 threshold)
- **Q-C BC tuning**: NOT REPORTED (1D–3D hybrid framework; detailed description of 1D boundary conditions and mesh parameters but no explicit discussion of BC tuning/calibration or whether it adjusts for geometry error)
- **Q-D fidelity / quantity**: **HYBRID 1D–3D CFD**. Reduced-order 1D coupled to image-based 3D model of stenotic region. Reports FFR and wall shear stress (WSS) at stenosis; provides spatially-resolved local hemodynamics. Computational cost reduction enables multi-scenario time-dependent modeling (e.g., thrombosis growth).
- **Q-E data**: Baseline healthy coronary tree from public CTA reference (SimVascular); validation against full 3D in synthetic diseased case (90% LAD stenosis). Not patient cohort; proof-of-concept methodology paper.
- **Q-F meshing**: Finite element mesh via Tetgen; boundary layer mesh (3 layers, 70% decreasing ratio); local refinement at stenosis (0.025 cm). No explicit robustness testing on poor or topologically incorrect geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Develops hybrid 1D–3D CFD framework enabling rapid FFR + WSS prediction; directly applicable to T6's reduced-order modeling strategy and multi-scenario exploration (e.g., virtual error injection).
- verdict: FULL
- revisit-if: (Already meets criteria; hybrid coupling and computational efficiency relevant to T6 methods)

