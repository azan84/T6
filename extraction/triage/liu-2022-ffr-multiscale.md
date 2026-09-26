---
source_pdf_path: Resources/fphys-13-881826.pdf
slug: liu-2022-ffr-multiscale
ledger_status: TRIAGED
---

# liu-2022-ffr-multiscale

## Bibliographic
- Title: Non-Invasive Quantification of Fraction Flow Reserve Based on Steady-State Geometric Multiscale Models
- First author / authors (first 3 + et al.): Liu J, Wang X, Li B, et al.
- Year: 2022
- Venue: Frontiers in Physiology
- DOI: 10.3389/fphys.2022.881826

## One-line claim
Steady-state geometric multiscale (1D/0D reduced-order) FFR model using boundary conditions based on coronary flow and microcirculation resistance achieves FFR prediction with comparable diagnostic accuracy to transient 3D CFD at reduced computational cost.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No geometric perturbation studies; focuses on computational method efficiency.
- **Q-B decision flip**: YES, FFR ≤0.80 threshold. N=154 moderately stenotic vessels (40–80% diameter stenosis) from 136 patients. Validates against clinical diagnosis; diagnostic performance reported but specific flip rates not extracted.
- **Q-C BC tuning**: YES, DESCRIBED. "The average pressure was used as the boundary condition for the inlet, and the microcirculation resistance calculated by the coronary flow was used as the boundary condition for the outlet to calculate the patient-specific coronary hyperemia." Uses 0D resistance-based outlet BC calculated from flow. States that "transient boundary condition has a high resource intensity in terms of computational time" and proposes steady-state alternative. Does not address whether re-tuning compensates for geometric error.
- **Q-D fidelity / quantity**: 1D + 0D hybrid. Reduced-order (geometric multiscale): 1D coronary tree coupled to 0D outlet resistances. Does NOT report WSS/OSI.
- **Q-E data**: N=154 vessels (136 patients) with stable angina, CTA-derived geometry. Segmentation accuracy validated against clinical CTA images.
- **Q-F meshing**: Briefly mentioned. "The method was based on the coronary artery model segmented from the patient's coronary CTA image" and "tetrahedral meshes" used, but no detail on robustness or sensitivity to segmentation error.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates steady-state 1D/0D FFR approach with resistance-based outlet BC tuning, relevant to T6's CFD methodology comparison but does not investigate segmentation error or BC compensation.
- verdict: LIGHT
- revisit-if: If T6 considers steady-state vs. transient model trade-offs, though focus is likely on full 3D with topological error, not computational acceleration.
