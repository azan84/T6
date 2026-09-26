---
source_pdf_path: Resources/s10237-021-01536-3.pdf
slug: mansilla-alvarez-2022-midfidelity-ffr
ledger_status: TRIAGED
---

# mansilla-alvarez-2022-midfidelity-ffr

## Bibliographic
- Title: Feasibility of coronary blood flow simulations using mid-fidelity numeric and geometric models
- First author / authors (first 3 + et al.): L. A. Mansilla Alvarez, C. A. Bulant, G. D. Ares et al.
- Year: 2022
- Venue: Biomechanics and Modeling in Mechanobiology
- DOI: 10.1007/s10237-021-01536-3

## One-line claim
Transversally Enriched Pipe Element Method (TEPEM) mid-fidelity FFR simulations achieve ~1% FFR error and ~5% WSS error vs. 3D-FEM with 30–60× speedup, and branch shortening does not materially affect results.

## T6 targeted questions
- **Q-A geometry perturbation**: Studies geometric fidelity (full vs. shortened side branches), not segmentation uncertainty. Reports error under different geometric simplifications. "This last demands research targeting the definitions of boundary conditions to mimic the physiological regime enforced in the invasive measurement procedure."
- **Q-B decision flip**: FFR values reported (0.71–0.96 range). No reclassification or decision-flip rates. No threshold-based sensitivity.
- **Q-C BC tuning**: Explicitly defers BC question: "This last demands research targeting the definitions of boundary conditions... For this reason, only the position for FFR interrogation (defined by the corresponding angiographic image) is considered of interest... we planned a simulation protocol... that sweeps an incremental range of possible CFR values, to emulate the hyperemic state." Outlets use Murray's law for flow distribution and linear resistance BCs: "pkout = Rk Qk + pref" where Rk computed from Murray law. No statement on tuning BCs to compensate for geometric error.
- **Q-D fidelity / quantity**: TEPEM (mid-fidelity 1D/3D hybrid) vs. conventional FEM (high-fidelity 3D). FFR and WSS reported; no OSI. Compares numeric fidelities, not physical fidelities (geometry quality).
- **Q-E data**: N=17 coronary geometries (15 patients from two Brazilian hospitals) with real invasive FFR ground truth, 20 FFR interrogation locations.
- **Q-F meshing**: Segmentation via level-set, triangulated surface, smoothing (Laplacian), inlet/outlet extensions, adaptive refinement by radius. No robustness analysis for poor/broken geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Validates mid-fidelity numerical approaches (TEPEM) for FFR with geometric simplification (branch shortening). Does not address topological segmentation error or BC re-tuning hypothesis.
- verdict: LIGHT
- revisit-if: Study extends to segmentation quality variations (e.g., branch omission, misalignment) and shows FFR sensitivity and BC calibration strategies.

