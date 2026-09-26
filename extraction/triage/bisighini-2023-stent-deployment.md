---
source_pdf_path: Resources/fphys-14-1148540.pdf
slug: bisighini-2023-stent-deployment
ledger_status: TRIAGED
---

# bisighini-2023-stent-deployment

## Bibliographic
- Title: Machine learning and reduced order modelling for the simulation of braided stent deployment
- First author / authors (first 3 + et al.): Bisighini B, Aguirre M, Biancolini ME, et al.
- Year: 2023
- Venue: Frontiers in Physiology
- DOI: 10.3389/fphys.2023.1148540

## One-line claim
Machine learning combined with reduced-order modeling accelerates braided stent deployment simulations by replacing high-fidelity FEA with neural network surrogate models, achieving sub-mm accuracy with 5-20x speedup.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Studies stent structural mechanics, not arterial geometry perturbation or segmentation uncertainty.
- **Q-B decision flip**: NOT REPORTED. No FFR or diagnostic classification; focuses on stent-wall contact prediction, not hemodynamic decision outcomes.
- **Q-C BC tuning**: NOT REPORTED. Concerns structural mechanics (stent strut contact, deformation) and boundary conditions on wall compliance, not hemodynamic resistance or flow BCs; no relevance to FFR BC tuning.
- **Q-D fidelity / quantity**: Structural mechanics (FEA) + ML surrogate. Uses high-fidelity FEA coupled with Radial Basis Function (RBF) neural networks for geometry morphing. Does NOT involve CFD or pressure/flow fields.
- **Q-E data**: Synthetic/parametric stent models; no clinical data or cohort size reported.
- **Q-F meshing**: YES, detailed. Discusses mesh generation (triangular mesh STL format, 3,408 nodes example), simplex deformable meshes, and mesh morphing via RBF. Focuses on structural contact mechanics, not flow-domain meshing.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Addresses post-deployment stent mechanics, not pre-deployment coronary artery segmentation, CFD, or hemodynamic error propagation. No overlap with T6 scope.
- verdict: LIGHT
- revisit-if: Only if T6 expands to post-revascularization hemodynamic validation (unlikely).
