---
source_pdf_path: Resources/s40323-021-00206-4.pdf
slug: manganotti-2021-energy
ledger_status: TRIAGED
---

# manganotti-2021-energy

## Bibliographic
- Title: Coupling reduced-order blood flow and cardiac models through energy-consistent strategies: modeling and discretization
- First author / authors: Jessica Manganotti, Federica Caforio, François Kimmig (et al.)
- Year: 2021
- Venue: Advanced Modeling and Simulation in Engineering Sciences 8:21
- DOI: 10.1186/s40323-021-00206-4

## One-line claim
Energy-preserving time-discretization schemes enable stable, thermodynamically-consistent coupling of 1D arterial flow models with 0D lumped-parameter heart models.

## T6 targeted questions
- **Q-A geometry perturbation**: No geometry perturbation. Uses 1D reduced-order networks. NOT REPORTED: segmentation or measurement uncertainty.
- **Q-B decision flip**: NOT REPORTED. Does not address FFR, diagnosis, or decision thresholds.
- **Q-C BC tuning**: Uses 0D lumped-parameter models (Windkessel) as boundary conditions for 1D arterial models. Abstract: "lumped-parameter zero-dimensional (0D) models—typically Windkessel models—can provide a general view on the global response, e.g. in pressure and flow." NOT REPORTED: parameter tuning strategy, whether tuning changes with geometry, or compensation for error.
- **Q-D fidelity / quantity**: 1D blood flow models coupled with 0D heart model incorporating reduced actin-myosin interaction. NOT REPORTED: WSS/OSI or 3D spatial fields.
- **Q-E data**: Theoretical / numerical study. Validated against in vitro and in vivo measurements (cited from literature). NOT REPORTED: specific cohort size, invasive FFR ground truth.
- **Q-F meshing**: NOT REPORTED. Focuses on mathematical formulation and stability rather than segmentation/meshing robustness.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Theoretical framework for energy-consistent 1D/0D model coupling. Useful background on reduced-order modeling but does not address geometry uncertainty, BC tuning strategy, or decision-flip sensitivity.
- verdict: LIGHT
- revisit-if: Full paper includes coronary-specific application with patient cohort data, or discusses parameter sensitivity to geometric input errors.
