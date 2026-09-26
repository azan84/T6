---
source_pdf_path: Resources/s10237-026-02065-7.pdf
slug: qi-2026-renal-outflow-bc
ledger_status: TRIAGED
---

# qi-2026-renal-outflow-bc

## Bibliographic
- Title: Computational hemodynamic analysis of renal blood flow and the impact of outflow boundary conditions
- First author / authors (first 3 + et al.): Fenfen Qi, Yingzhi Liu, Rongliang Chen et al.
- Year: 2026
- Venue: Biomechanics and Modeling in Mechanobiology
- DOI: 10.1007/s10237-026-02065-7

## One-line claim
Two-element RC Windkessel outflow boundary conditions provide physiologically realistic pulsatile hemodynamics in renal artery CFD simulations; BC choice affects global pressure but minimally affects lesion-specific FFR and WSS when lesion is distant from outlets.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Patient-specific segmentations of normal, stenotic, and aneurysmal renal arteries; no synthetic error injection.
- **Q-B decision flip**: Renal FFR (rFFR) discussed (threshold not explicitly stated as analog to coronary ≤0.80). Pressure drop >10 mmHg for severe stenosis (>87% area) reported as hemodynamically significant. No reclassification rates.
- **Q-C BC tuning**: Extensively studied: "Compared with constant pressure and resistance outflow boundary conditions, the two-element Windkessel model, through adjustments of its resistance and capacitance parameters, can provide more physiological flow and pressure distributions." Sensitivity analysis: "a 20% variation in resistance" yields "<3% for a change in rFFR." Key finding: "When focusing solely on the hemodynamics within stenotic and aneurysmal lesions located far from the outlets, both the constant pressure and Windkessel boundary conditions yield comparable results for key lesion-specific hemodynamic indicators." **No statement that BC re-tuning compensates for or absorbs topological/segmentation error.**
- **Q-D fidelity / quantity**: 3D unsteady Navier-Stokes with stabilized FEM. Pressure drop, rFFR, WSS, and oscillatory shear index (OSI) reported. No sensitivity to geometry fidelity.
- **Q-E data**: Three patient-specific renal artery models (normal, stenotic with 87% area stenosis, aneurysmal with 13.3 mm diameter) from CT imaging.
- **Q-F meshing**: Patient-specific geometries segmented from CT using Mimics, post-processed with smoothing. Main renal artery modeled with branches down to ~1 mm diameter. No robustness analysis for topologically broken geometries.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Systematic BC comparison (constant pressure, resistance, Windkessel) in renal artery CFD; shows BC choice matters globally but lesion indicators (FFR, WSS) are robust when lesion distant from outlets. Does not address segmentation error, topological correctness, or BC tuning to mask error.
- verdict: LIGHT
- revisit-if: Extended to coronary arteries or includes segmentation error scenarios (e.g., branch omission, misalignment) with BC tuning before/after error.

