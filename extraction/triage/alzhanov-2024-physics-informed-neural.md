---
source_pdf_path: Resources/fluids-09-00153.pdf
slug: alzhanov-2024-physics-informed-neural
ledger_status: TRIAGED
---

# alzhanov-2024-physics-informed-neural

## Bibliographic
- Title: Three-Dimensional Physics-Informed Neural Network Simulation in Coronary Artery Trees
- First author / authors (first 3 + et al.): Alzhanov N, Ng EYK, Zhao Y
- Year: 2024
- Venue: Fluids
- DOI: 10.3390/fluids9070153

## One-line claim
3D Physics-Informed Neural Networks (PINNs) enable FFR computation without explicit boundary condition specification, reducing computational burden and improving accuracy over traditional CFD methods.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No geometric perturbation or segmentation uncertainty studied; focus is on computational method improvement.
- **Q-B decision flip**: NOT REPORTED. Validates FFR accuracy (mean error vs invasive FFR: 1.2–2.8%) but does not report FFR ≤0.80 reclassification or decision flip rates.
- **Q-C BC tuning**: YES, DIRECTLY RELEVANT. "Our methodology integrates 3D PINNs without providing customized outflow boundary conditions, ensuring precise diagnostic accuracy without the need for extensive empirical data." Explicitly addresses boundary condition challenge: "Compared to traditional 3D methods that struggle with boundary conditions, our 3D PINN approach provides a flexible, efficient, and physiologically sound solution." States "traditional CFD methods require substantial computational resources and are highly sensitive to initial and boundary conditions, leading to potential errors."
- **Q-D fidelity / quantity**: 3D CFD via PINN. Computes FFR (pressure-based), validated against CFD simulations and invasive FFR. Does NOT report WSS/OSI.
- **Q-E data**: Mixed validation. Tested on patient-specific coronary artery trees from CT scans (N not explicitly stated for patient cohort). Validation against invasive FFR and CFD simulations.
- **Q-F meshing**: NOT DETAILED. Mentions "computational meshes" and CT-derived models but no segmentation→surface→volume workflow or robustness on poor geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Offers alternative computational approach (PINN) that claims to eliminate boundary condition tuning requirement; relevant to T6's Q-C interest in BC-tuning mechanisms but does not study whether tuning compensates for topological error.
- verdict: FULL
- revisit-if: To benchmark PINN FFR accuracy against conventional CFD on segmentation-error test cases.
