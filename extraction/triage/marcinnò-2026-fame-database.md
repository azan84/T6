---
source_pdf_path: Resources/2026.07.30.741868v1.full.pdf
slug: marcinnò-2026-fame-database
ledger_status: TRIAGED
---

# marcinnò-2026-fame-database

## Bibliographic
- Title: A comprehensive database of simulations and meshes of coronary arteries from the FAME 2 trial
- First author / authors (first 3 + et al.): Fabio Marcinnò, Jochen Hinz, Edward Andò
- Year: 2026
- Venue: bioRxiv preprint
- DOI: https://doi.org/10.64898/2026.07.30.741868

## One-line claim
A public database of 3D unsteady Navier-Stokes simulations and structured hexahedral meshes for 779 coronary artery vessels reconstructed from invasive coronary angiograms in the FAME 2 trial.

## T6 targeted questions
- **Q-A geometry perturbation**: The paper reconstructs coronary arteries from invasive X-ray angiography with manual segmentation by interventional cardiologists. 135 of 914 vessels were discarded because "they exhibited self-intersecting geometry during the reconstruction process." No systematic perturbation or inter-observer disagreement magnitude reported.
- **Q-B decision flip**: FFR ≤ 0.80 revascularization threshold is central to FAME 2 trial design ("current European guidelines recommend revascularisation for stenoses with an FFR ≤ 0.80"). However, the database paper does NOT report FFR reclassification rates or decision-flip analysis; it publishes pre-computed simulations.
- **Q-C BC tuning**: Uses Finite Element Method with "state-of-the-art coronary boundary conditions applied at the outlet." Convergence validation provided but no report of BC re-tuning after geometry reconstruction or exploration of whether BC tuning absorbs/compensates for topological errors.
- **Q-D fidelity / quantity**: 3D unsteady Navier-Stokes simulations. Database includes fluid_dynamics.txt files reporting "energy and turbulence related quantities, such as the total kinetic energy and the enstrophy." Does NOT explicitly report WSS or OSI fields in the published outputs.
- **Q-E data**: FAME 2 trial cohort: 567 patients with 914 vessel geometries reconstructed from invasive coronary angiography (ICA). Invasive FFR ground truth present (core inclusion criterion). Public dataset available.
- **Q-F meshing**: "Hexahedral meshes" with "the same number of vertices and identical connectivity" across all 779 vessels. "Their high quality is demonstrated using standard mesh quality indices." Quality assessment directory provided. 18 vessels had convergence failures. Topological robustness addressed by excluding self-intersecting geometries.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Large-scale public CFD database with invasive FFR ground truth and robust meshing strategy on real patient geometries; supports T6's emphasis on real, not synthetic, data.
- verdict: LIGHT
- revisit-if: If the team performs sensitivity analysis on these simulations (e.g., perturbing geometry and recomputing BC parameters), or provides WSS/OSI fields for hemodynamic endpoint analysis.
