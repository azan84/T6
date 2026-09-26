---
source_pdf_path: Resources/A_Study_on_the_Effect_of_Electrical_Parameters_of_Zero-Dimensional_Cardiovascular_System_on_Aortic_Waveform.pdf
slug: sooriamoorthy-2020-0d-aortic
ledger_id: C020
ledger_status: TRIAGED
---

# sooriamoorthy-2020-0d-aortic

## Bibliographic
- Title: A Study on the Effect of Electrical Parameters of Zero-Dimensional Cardiovascular System on Aortic Waveform
- First author / authors: Denesh Sooriamoorthy, Audrey Li-Huey Wee, Anandan Shanmugam
- Year: 2020
- Venue: 2020 IEEE Student Conference on Research and Development (SCOReD), 27-28 September 2020, Johor, Malaysia
- DOI: NOT REPORTED

## One-line claim
Performs parameter sensitivity analysis on Vincent Rideout's zero-dimensional cardiovascular model to identify which of 36 parameters (resistance, compliance, inductance) significantly affect aortic pressure waveform.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED
- **Q-B decision flip**: NOT REPORTED
- **Q-C BC tuning**: Partial relevance. Uses lumped-parameter RLC model representing resistance, compliance, and inductance (electrical analogues of fluid dynamics parameters). Varies parameters 0.25–1.75× default values to study aortic pressure response. No explicit discussion of BC tuning strategies, Windkessel circuit tuning, or how tuning changes with geometry.
- **Q-D fidelity / quantity**: 0D only. "Zero-dimensional (0D) models are simplified representations of the components of the cardiovascular system"; Vincent Rideout model coded in MATLAB. Outputs pressure and flow quantities; no spatial fields (WSS/OSI).
- **Q-E data**: No clinical cohort. Pure mathematical model (Vincent Rideout); MATLAB simulation with synthetic parameters. No invasive FFR ground truth.
- **Q-F meshing**: NOT REPORTED

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Parameter sensitivity analysis for 0D cardiovascular modeling; lacks 3D CFD coupling, geometry error quantification, or BC tuning protocols
- verdict: LIGHT
- revisit-if: Paper demonstrates coupling with patient-specific 3D geometry or BC sensitivity to geometric variations

## Ideation opening
Paper states models "can be utilized for further medical informatics development" and emphasizes role of parameter understanding for disease detection and heart condition monitoring, but does not address how segmentation/geometry error affects parameter estimation or model predictions.
