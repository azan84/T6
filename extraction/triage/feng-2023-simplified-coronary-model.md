---
source_pdf_path: Resources/1-s2.0-S016926072300528X-main.pdf
slug: feng-2023-simplified-coronary-model
ledger_id: C005
ledger_status: TRIAGED
---

# feng-2023-simplified-coronary-model

## Bibliographic
- Title: A simplified coronary model for diagnosis of ischemia-causing coronary stenosis
- First author / authors: Yili Feng, Bao Li, Ruisen Fu
- Year: 2023
- Venue: Computer Methods and Programs in Biomedicine, vol. 242
- DOI: 10.1016/j.cmpb.2023.107862

## One-line claim
A 0D circuit model combined with machine-learning-predicted stenosis resistance estimates FFR in <2 s from CCTA geometry, achieving 90.7–92.0% diagnostic accuracy against invasive FFR in 75 patients.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. ML is trained on varied geometric parameters but no segmentation error or inter-observer variability analysis conducted.
- **Q-B decision flip**: FFR threshold 0.80 used. Paper reports: "an FFR of < 0.80 was considered hemodynamically significant." Diagnostic accuracy 90.7% (resting) and 92.0% (hyperemic) in 75 patients with invasive FFR ground truth. Specific reclassification/flip rate NOT QUANTIFIED.
- **Q-C BC tuning**: Inlet BC uses aortic pressure (resting and hyperemic, estimated via mean arterial pressure). Outlet BC uses coronary microcirculation resistance estimated via allometric scaling law (Q∝d³). Hyperemia simulated by reducing outlet resistance ("microcirculation resistance is reduced to simulate maximal hyperemia"). Hyperemic aortic pressure estimated as 0.81 times resting MAP. Re-tuning of BC after geometry change NOT REPORTED. No statement on BC masking geometric error.
- **Q-D fidelity / quantity**: 0D circuit model with ML-predicted stenosis resistance (trained on 3D CFD). Output: pressure drop across stenosis, not full 3D flow field. WSS/OSI NOT REPORTED. Sensitivity to geometry variations NOT EXPLICITLY ANALYZED.
- **Q-E data**: 75 patients, CCTA-based, retrospective (March 2019–May 2021), invasive FFR ground truth present. Private institutional data (Peking University People's Hospital). Patient criteria: stable, low-to-intermediate risk, visual stenosis 30–90%, vessel diameter ≥2 mm.
- **Q-F meshing**: Reconstruction via Mimics Research 20.0 under cardiologist guidance; geometric parameters measured manually. No mesh generation (0D model, no CFD solving). Robustness on poor segmentation NOT DISCUSSED.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Combines allometric scaling-based BC with ML-predicted stenosis resistance for rapid FFR; demonstrates 0D+ML can match invasive FFR at 0.80 threshold but does not study how segmentation error affects predictions or BC tuning.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity analysis of FFR predictions to segmentation/geometry variations, or compares how different segmentation methods affect model output and clinical decision at 0.80 threshold.

## Ideation opening (CFD + imaging)
- None stated. Paper addresses computational speed (< 2 s vs 1–6 h) but does not identify a research gap in CFD-imaging integration for segmentation or geometry uncertainty.
