---
source_pdf_path: Resources/011905_1_5.0180162.pdf
slug: wang-2024-guidewire-ffrct
ledger_status: TRIAGED
---

# wang-2024-guidewire-ffrct

## Bibliographic
- Title: Effect of guidewire on the accuracy of trans-stenotic pressure measurement—A computational study
- First author / authors: Junjie Wang, Chi Zhu, Zhanzhou Hao
- Year: 2024
- Venue: Physics of Fluids
- DOI: 10.1063/5.0180162

## One-line claim
Guidewire insertion increases trans-stenotic pressure drop artificially and can be modeled analytically to align CT-FFR with invasive FFR standards.

## T6 targeted questions
- **Q-A geometry perturbation**: Does not address lumen/segmentation uncertainty; focuses on guidewire obstruction effect only.
- **Q-B decision flip**: Yes, FFR changes from 0.72 (without guidewire, gray zone) to 0.49 (with guidewire, severe ischemia cutoff), demonstrating critical reclassification at threshold. "This FFR value severely overestimated the severity of the stenosis, which could lead to a more pessimistic estimation of the severity of ischemia in clinical practice."
- **Q-C BC tuning**: RCR (three-element Windkessel) boundary conditions applied at coronary outlets; parameters shown in Table IV. NO evidence that tuning was re-done after guidewire insertion (geometry change). Model uses fixed CMVR and outlet resistances. No statement of compensatory tuning.
- **Q-D fidelity / quantity**: 3D CFD (idealized and patient-specific) + reduced-order analytical model for pressure drop. Pressure drop components (viscous, inertial, stenosis) reported. No WSS/OSI reported.
- **Q-E data**: Patient-specific case (case 186_0002 from Vascular Model Repository, healthy 28-year-old). Severity 92% area stenosis. No invasive FFR ground truth (synthetic stenosis).
- **Q-F meshing**: SimVascular used for mesh generation with local refinement. Mesh independence studies performed. No detail on robustness to topologically incorrect geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates that outlet BC parameters must account for guidewire presence; proposes analytical model to bridge CT-FFR (no guidewire assumption) to invasive FFR standards (with guidewire).
- verdict: LIGHT
- revisit-if: Paper reports BC tuning strategy to reconcile two measurement modalities, but does not address segmentation error rank-ordering or decision-flip rates by error type—core to T6's thesis.

