---
source_pdf_path: Resources/Personalized_Hemodynamic_Modeling_of_the_Human_Cardiovascular_System_A_Reduced-Order_Computing_Model.pdf
slug: zhang-2020-personalized-hemodynamic
ledger_status: TRIAGED
---

# zhang-2020-personalized-hemodynamic

## Bibliographic
- Title: Personalized Hemodynamic Modeling of the Human Cardiovascular System: A Reduced-Order Computing Model
- First author / authors (first 3 + et al.): Xiangdong Zhang, Dan Wu, Fen Miao, et al.
- Year: 2020
- Venue: IEEE Transactions on Biomedical Engineering
- DOI: 10.1109/TBME.2020.2970244

## One-line claim
Inverse problem solver (Levenberg–Marquardt optimization) personalizes a 55-segment 1D-0D multiscale cardiovascular model by tuning arterial stiffness and 0D Windkessel parameters to match measured brachial pressure waveforms on 62 healthy volunteers.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No segmentation error or geometry variation introduced; arterial geometry (length, radius, wall properties) from literature baseline, adjusted only via inverse optimization.
- **Q-B decision flip**: NOT APPLICABLE. Study on healthy volunteers; no stenosis, no FFR threshold analysis.
- **Q-C BC tuning**: 1D arteries coupled to 0D RCR (Windkessel) models at distal ends. BC parameters (proximal resistance Rp, distal resistance Rd, capacitance C) adjusted via inverse optimization to personalize the model. Arterial stiffness (elastic modulus E) also tuned. Methodology demonstrates BC parameter personalization but does NOT address whether BC re-tuning compensates for geometric error or topology changes.
- **Q-D fidelity / quantity**: 0-1D multiscale (1D on 55 arterial segments, 0D on periphery). Pressure and flow waveforms computed; NO WSS/OSI.
- **Q-E data**: 62 volunteers (ages 20–70), healthy CVS; no disease, no invasive FFR ground truth. Noninvasive ultrasound measurements (pressure, diameter, flow velocity) used for validation.
- **Q-F meshing**: NOT APPLICABLE. No patient-specific segmentation or mesh; uses literature-based arterial tree.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Establishes personalized 0-1D model calibration via inverse optimization; demonstrates that BC/stiffness parameters can be estimated from pressure waveforms. Methodology transferable to patient-specific coronary geometry, but no analysis of geometry error or BC compensation.
- verdict: LIGHT
- revisit-if: Applied to stenotic coronary geometry with segmentation uncertainty; analyzes whether BC re-optimization masks geometric error.
