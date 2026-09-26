---
source_pdf_path: Resources/preprints202508.0266.v1.pdf
slug: wang-2025-4d-cta-dynamic
ledger_status: TRIAGED
---

# wang-2025-4d-cta-dynamic

## Bibliographic
- Title: Fractional Flow Reserve Computation Using 4D-CTA: A Computational Framework for Temporal Hemodynamic Assessment
- First author / authors: Shuo Wang, Rong Liu, Li Zhang
- Year: 2025
- Venue: Preprints.org (not peer-reviewed)
- DOI: 10.20944/preprints202508.0266.v1

## One-line claim
Dynamic FFRCT computation using 4D-CTA captures temporal cardiac-cycle variations in FFR, improving accuracy over static methods.

## T6 targeted questions
- **Q-A geometry perturbation**: YES—uses 4D-CTA to capture dynamic geometry changes across the cardiac cycle. The perturbation is temporal (pulsatile vessel motion) rather than synthetic researcher-imposed error or measured inter-observer disagreement.
- **Q-B decision flip**: YES—reports FFR values at the 0.75–0.85 diagnostic threshold (Cases 2 and 3a: invasive FFR 0.78 vs. dynamic FFRct 0.797 and 0.811). No explicit reclassification rate reported beyond individual case errors (0.008–0.033 vs. static 0.021–0.045).
- **Q-C BC tuning**: **KEY FINDING**—"Dynamic boundary conditions were derived from temporal flow measurements extracted from 4D-CTA data throughout the cardiac cycle." Paper explicitly addresses tuning: "Current approaches often require significant manual effort for preprocessing, boundary condition setup, and solver configuration" and proposes "personalized computational frameworks that can dynamically adapt boundary conditions." States: "The ability to incorporate time-varying geometries and flow patterns may contribute to more personalized cardiovascular assessment."
- **Q-D fidelity / quantity**: 3D CFD via OpenFOAM. Generates pressure fields, velocity magnitude, WSS distributions, and wall shear stress maps (Figures A1–A2).
- **Q-E data**: 3 patients (4 vessel assessments total: 1 RCA, 2 LAD, 1 LCX). Invasive FFR ground truth present. Private data (Chinese Academy of Medical Sciences).
- **Q-F meshing**: Body-fitted Cartesian mesh via cfMesh with adaptive refinement at bifurcation regions; no detail on robustness to topological error.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates that patient-specific, time-varying boundary conditions extracted from 4D imaging can improve FFR accuracy in the critical 0.75–0.85 range, supporting the premise that BC tuning can refine hemodynamic assessment despite geometry uncertainty.
- verdict: LIGHT
- revisit-if: Validation study in larger cohort (N > 20) with segmentation perturbations to separate time-varying geometry effects from boundary condition tuning.
