---
source_pdf_path: Resources/bio_142_02_021001.pdf
slug: thondapu-2020-contrast-tuning
ledger_status: TRIAGED
---

# thondapu-2020-contrast-tuning

## Bibliographic
- Title: Using Contrast Motion to Generate Patient-Specific Blood Flow Simulations During Invasive Coronary Angiography
- First author / authors: Vikas Thondapu, Sergiy Zhuk, Olivia Smith, Stephen Moore
- Year: 2020
- Venue: Journal of Biomechanical Engineering (ASME)
- DOI: 10.1115/1.4044095

## One-line claim
A novel contrast-based optimization method tunes lumped-parameter arterial resistances (boundary conditions) by matching simulated and observed contrast arrival times during invasive angiography, demonstrating that BC tuning can reconstruct underlying hemodynamic fields with FFR error <0.1%.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED — Uses synthetically generated but anatomically realistic coronary tree; no inter-observer segmentation disagreement.
- **Q-B decision flip**: YES (INDIRECT) — "the relative FFR error is of a similar scale... with all five runs producing errors within 0.1% in all cases" and "when subjected to 5% noise... the error was within 2.0% in all cases." Shows BC tuning maintains FFR accuracy despite resistance reconstruction errors.
- **Q-C BC tuning**: YES, DIRECTLY ADDRESSES — "identifying a noninvasive strategy for tuning (or parameterizing) these boundary conditions probably presents the greatest challenge" (citing Morris et al.). Core contribution: "In this work, we present a novel approach for tuning the coronary microvascular resistances at the outlets of a complex arterial tree. The fundamental idea is that by simulating the contrast transport that occurs during ICA and comparing observations, resistances can be optimized to regulate the flowfield and minimize the mismatch between observed and simulated motion." Shows that BC tuning via contrast matching successfully reconstructs pressure/velocity fields.
- **Q-D fidelity / quantity**: 3D Navier-Stokes (incompressible, unsteady); contrast transport equation solved; NO WSS/OSI; focuses on pressure and flow fields.
- **Q-E data**: Synthetic patient-specific geometry + proof of principle; NO real invasive FFR ground truth.
- **Q-F meshing**: Uses snappyHexMesh (OpenFOAM) with 0.1mm resolution (~1 million cells); no detail on robustness to poor/topologically incorrect geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Direct demonstration of BC tuning methodology using contrast motion matching; proves that BCs can be optimized to match hemodynamic observations and maintain FFR accuracy despite errors in resistance parameters.
- verdict: FULL
- revisit-if: Extended to real patient data with topologically complex geometries or combined with geometric perturbations to demonstrate BC-tuning compensation

