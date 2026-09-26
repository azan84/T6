---
source_pdf_path: Resources/fphys-13-830925.pdf
slug: munneke-2022-coronary-coupling
ledger_id: C031
ledger_status: TRIAGED
---

# munneke-2022-coronary-coupling

## Bibliographic
- Title: A Closed-Loop Modeling Framework for Cardiac-to-Coronary Coupling
- First author / authors (first 3 + et al.): Munneke AG, Lumens J, Arts T
- Year: 2022
- Venue: Frontiers in Physiology
- DOI: 10.3389/fphys.2022.830925

## One-line claim
A multi-scale closed-loop model integrating coronary mechanics (1D conduit arteries, 0D lumped microcirculation with three transmural layers) into the CircAdapt cardiovascular model enables realistic simulation of cardiac-to-coronary coupling and coronary hemodynamics in pathophysiological conditions.

## T6 targeted questions
- **Q-A geometry perturbation**: Paper describes anatomical configuration of coronary circulation model but does not address segmentation uncertainty, lumen measurement error, or sensitivity to geometric variations. NOT REPORTED on magnitude or source of geometry perturbation.
- **Q-B decision flip**: No FFR computation, no diagnostic threshold evaluation, no reclassification analysis. Paper focuses on coronary flow velocity and diameter waveforms, not FFR-based decision-making. NOT REPORTED.
- **Q-C BC tuning**: Lumped parameter model for microcirculation with resistances (Ra, Rv) and compliances (C1, C2). States "level of detail was based on data availability and the model could capture the main dynamic features of coronary hemodynamics." No explicit discussion of BC re-tuning after geometry change or whether model parameters compensate for measurement/segmentation error.
- **Q-D fidelity / quantity**: Multi-scale: 1D network for major conduit arteries (LM, LAD, LCx, RCA), 0D lumped for microcirculation with three transmural layers (subepicardium, mid, subendocardium). Outputs are flow velocity, pressure, and diameter waveforms. No 3D CFD, no WSS/OSI field computation.
- **Q-E data**: Model validated against published in vivo measurements of flow velocity and diameter in epicardial coronary arteries and subendocardial vessels (Doppler echocardiography, intravascular ultrasound). Application shown for aortic valve stenosis; no patient-specific FFR ground truth.
- **Q-F meshing**: 1D network description of coronary arteries and veins; no 3D segmentation or mesh generation discussed.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Presents a validated multi-scale 1D/0D coronary hemodynamic model coupled to cardiac mechanics that T6 could use or reference for coronary flow simulation framework, but does not address imaging-derived geometry uncertainty or its impact on FFR predictions or clinical decisions.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity analysis showing how plausible variations in vessel diameter, length, or wall properties affect predicted flow/pressure, or demonstrates how segmentation-based geometry perturbations affect model predictions.

## Ideation opening (CFD + imaging)
Paper notes that "level of detail was based on data availability" and mentions that "due to the modular design of the CircAdapt model, the anatomical detail can be easily altered when needed" — suggesting that model anatomy is not patient-specific imaging-derived. Implies a gap in how patient-specific imaging-derived coronary geometry and its measurement uncertainty are incorporated into hemodynamic simulations.
