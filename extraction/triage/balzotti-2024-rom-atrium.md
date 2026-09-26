---
source_pdf_path: Resources/s10237-024-01847-1.pdf
slug: balzotti-2024-rom-atrium
ledger_status: TRIAGED
---

# balzotti-2024-rom-atrium

## Bibliographic
- Title: A reduced order model formulation for left atrium flow: an atrial fibrillation case
- First author / authors (first 3 + et al.): Caterina Balzotti, Pierfrancesco Siena, Michele Girfoglio et al.
- Year: 2024
- Venue: Biomechanics and Modeling in Mechanobiology
- DOI: 10.1007/s10237-024-01847-1

## One-line claim
Data-driven POD-RBF reduced order model for atrial fibrillation hemodynamics achieves 10^5× speedup with <5% error vs. full order CFD.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Single patient-specific atrial geometry, no perturbations or synthetic error injection.
- **Q-B decision flip**: NOT APPLICABLE. Study focuses on left atrial stasis, not coronary ischemia or FFR thresholds.
- **Q-C BC tuning**: NOT REPORTED. Reduced order modeling context; no specific boundary condition tuning discussion or evidence of tuning to absorb geometric error.
- **Q-D fidelity / quantity**: 3D Navier-Stokes CFD with parametrized hemodynamics (cardiac output, viscosity, hematocrit). WSS and blood residence time reported as outputs; no spatial sensitivity to geometry.
- **Q-E data**: Single patient with atrial fibrillation; data-driven ROM trained on FOM solutions.
- **Q-F meshing**: NOT REPORTED. Patient-specific left atrium segmented from imaging; ROM operates on FOM solution snapshots.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Study addresses atrial fibrillation hemodynamics, not coronary artery disease or FFR-based decision-making. Not relevant to T6 coronary segmentation error and BC tuning hypothesis.
- verdict: LIGHT
- revisit-if: Methods extend to coronary circulation or patient-specific coronary geometry variations.

