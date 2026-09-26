---
source_pdf_path: Resources/1-s2.0-S0010482525001908-main.pdf
slug: lotfi-2025-pod-coronary
ledger_status: TRIAGED
---

# lotfi-2025-pod-coronary

## Bibliographic
- Title: Computational fluid dynamics model utilizing proper orthogonal decomposition to assess coronary physiology and wall shear stress
- First author / authors: Amir Lotfi, Daniela Caraeni, Omar Haider
- Year: 2025
- Venue: Computers in Biology and Medicine
- DOI: 10.1016/j.compbiomed.2025.109840

## One-line claim
POD-based ROM of patient-specific coronary arteries pre- and post-stent enables rapid assessment of flow patterns and WSS without full CFD, potentially for real-time clinical decision support.

## T6 targeted questions
- **Q-A geometry perturbation**: No segmentation/lumen uncertainty perturbations. Studies stent geometry impact (design variation).
- **Q-B decision flip**: Mentions FFR and iFR in context but does not report reclassification rates. "FFR, defined as the ratio of distal to proximal pressure across a stenosis" noted as gold standard; no FFR threshold decision-flip counts reported in this exploratory study.
- **Q-C BC tuning**: Outflow boundary conditions applied; laminar Newtonian assumption. Pulsatile inlet waveform from reference LCA. No re-tuning of BC after stent insertion reported. No discussion of tuning compensating for error.
- **Q-D fidelity / quantity**: 3D CFD (OpenFOAM pisoFOAM) + POD-based ROM for efficiency. Velocity patterns and WSS analyzed. OSI NOT reported; focus on first 5 POD modes capturing 90% of energy.
- **Q-E data**: N=12 patients (from 24 screened). Combined pressure, Doppler flow velocity, intravascular ultrasound (IVUS). Post-stent immediate outcomes; no long-term follow-up or invasive FFR.
- **Q-F meshing**: "Unstructured mesh created in Ansys Workbench from extracted patient-specific geometry... 50,000 to 100,000 elements." ANSYS meshing automatically generated. No detail on robustness to poor or topologically incorrect geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Applies POD-based ROM reduction to patient-specific coronary CFD for rapid assessment; demonstrates feasibility of reduced-order modeling for interventional planning, but does not address segmentation error robustness or decision-flip rates.
- verdict: LIGHT
- revisit-if: If T6 adopts POD-based ROM strategy for parametric exploration of segmentation error sensitivity, revisit to understand POD mode energy distribution under geometry perturbations.

