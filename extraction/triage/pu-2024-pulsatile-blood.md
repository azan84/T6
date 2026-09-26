---
source_pdf_path: Resources/Pu_2024_Med._Eng._Phys._130_104193.pdf
slug: pu-2024-pulsatile-blood
ledger_status: TRIAGED
---

# pu-2024-pulsatile-blood

## Bibliographic
- Title: Computing pulsatile blood flow of coronary artery under incomplete boundary conditions
- First author / authors: WenJun Pu, Yan Chen, Shuai Zhao
- Year: 2024
- Venue: Medical Engineering & Physics, vol. 130
- DOI: NOT REPORTED in extracted text

## One-line claim
Proposes a CFD method for computing pulsatile coronary blood flow that combines flow resistance modeling with incomplete (patient-specific outlet pressure) boundary conditions, validated on idealized and 3D reconstructed coronary models.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No inter-observer segmentation error quantified.
- **Q-B decision flip**: NOT REPORTED. FFR threshold analysis not mentioned in extracted sections.
- **Q-C BC tuning**: Yes, core to paper. Title explicitly: "Computing pulsatile blood flow of coronary artery under incomplete boundary conditions." Method: "A flow resistance model based on Pressure-Flow vs. Time curves is proposed to model the resistance of the epicardial artery." Quote: "pulsating blood flow can be calculated by combining the incomplete pressure boundary conditions under pulsating conditions which are easily obtained in clinic." No explicit statement on re-tuning after geometry change; focus is on handling incomplete (sparse) BCs via resistance modeling.
- **Q-D fidelity / quantity**: 3D CFD + reduced resistance model (hybrid 3D/0D approach). Pulsatile flow waveforms extracted. No WSS/OSI reported in abstract/methods.
- **Q-E data**: Idealized and reconstructed 3D coronary artery models (dataset name NOT REPORTED). Validation against simulated pulsating flow. No invasive FFR comparison.
- **Q-F meshing**: Mentions "reconstructed 3D model of coronary artery" but no detail on meshing quality or robustness on poor geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Directly addresses BC incompleteness via resistance model calibration and demonstrates pulsatile flow recovery with only distal pressure (not flow) specified—a practical BC-tuning pattern for coronary flows.
- verdict: FULL
- revisit-if: If paper includes sensitivity to outlet resistance magnitude or demonstrates robustness to geometric perturbations.
