---
source_pdf_path: Resources/s10439-026-04269-5.pdf
slug: thakar-2026-surrogate
ledger_status: TRIAGED
---

# thakar-2026-surrogate

## Bibliographic
- Title: Automated Tuning of Cardiovascular Boundary Conditions via Differentiable Surrogate Modeling
- First author / authors (first 3 + et al.): Shridhar Thakar, Mehran Mirramezani
- Year: 2026
- Venue: Annals of Biomedical Engineering
- DOI: 10.1007/s10439-026-04269-5

## One-line claim
- Differentiable hybrid mechanistic/data-driven reduced order model (ROM) enables automated calibration of lumped parameter network boundary conditions and efficient surrogate hemodynamics for cardiovascular simulations.

## T6 targeted questions
- **Q-A geometry perturbation**: Not applied in this paper; framework enables automated BC tuning for existing geometries. No perturbation study reported.
- **Q-B decision flip**: NOT REPORTED — focus is on BC calibration methodology, not diagnostic accuracy or threshold-based outcomes.
- **Q-C BC tuning**: CENTRAL FOCUS: proposes end-to-end differentiable framework for automated model calibration. Hybrid ROM represents vascular domains via nonlinear parameterized lumped parameter networks (Windkessel-like). Calibrates ROM parameters against single high-fidelity 3D CFD simulation. "With its computational efficiency and high fidelity, the framework directly addresses critical bottlenecks that currently limit the clinical adoption of cardiovascular simulations." Enables gradient-based deterministic AND gradient-informed stochastic BC tuning. Key quote: "differentiable surrogate modeling, automated model calibration, and stochastic parameter tuning" are core capabilities. No explicit statement about tuning AFTER geometry change or compensating for segmentation error; methodology is general.
- **Q-D fidelity / quantity**: Hybrid mechanistic (lumped parameter ODE networks) + data-driven (differentiable neural operators). 3D CFD validation substrate (Navier-Stokes). Computes hemodynamic surrogates (pressure, flow, velocity) from BC parameters. No WSS/OSI or tissue-level perfusion in paper.
- **Q-E data**: Methodology paper; no patient data presented. Framework is general and data-agnostic (validated against synthetic CFD data).
- **Q-F meshing**: Framework does not address meshing explicitly; assumes 3D CFD model provided as training target. Mesh independence is responsibility of upstream CFD.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Introduces automated differentiable BC tuning framework; directly applicable to T6's need for efficient boundary condition optimization without manual iteration; enables gradient-based exploration of BC-sensitivity to geometry changes.
- verdict: FULL
- revisit-if: Always; cutting-edge (2026) methodology for automated BC tuning via differentiable computing. Highly relevant to T6's technical toolkit for exploring whether BC tuning can mask/compensate for topological error.
