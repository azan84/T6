---
source_pdf_path: Resources/1-s2.0-S0933365723002580-main.pdf
slug: feng-2024-reduced-order-coronary
ledger_id: C006
ledger_status: TRIAGED
---

# feng-2024-reduced-order-coronary

## Bibliographic
- Title: Non-invasive fractional flow reserve derived from reduced-order coronary model and machine learning prediction of stenosis flow resistance
- First author / authors: Yili Feng, Ruisen Fu, Hao Sun
- Year: 2024 (online 2023)
- Venue: Artificial Intelligence In Medicine, vol. 147
- DOI: 10.1016/j.artmed.2023.102744

## One-line claim
A closed-loop 0D lumped-parameter model of coronary and cardiovascular system with machine-learning stenosis flow resistance predicts FFR in ~10 min with 91.4% diagnostic accuracy against invasive FFR in 91 patients.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. ML trained on varied geometric parameters; no measurement of segmentation error or inter-observer variability.
- **Q-B decision flip**: FFR threshold 0.80 used. Paper states "FFR ≤ 0.80 was considered hemodynamically significant." Diagnostic accuracy 91.4%, sensitivity 92.6%, specificity 90.9% (91 patients, 93 lesions). Of 93 lesions, 27 (29.0%) showed lesion-specific ischemia. Specific reclassification/flip rate NOT QUANTIFIED.
- **Q-C BC tuning**: 0D Windkessel (RLC circuit) model for coronary vessels. Coronary microcirculation resistance (CMR) personalized via allometric scaling law (Q ∝ d³), flow allocation 60:40 left:right coronary arteries. CMR changes at hyperemia quantified. Re-tuning of BC after geometry change NOT REPORTED. No statement on BC compensating for geometric error.
- **Q-D fidelity / quantity**: 0D LPM with ML-predicted stenosis flow resistance (not 3D CFD). Spatially-resolved fields, WSS, OSI NOT REPORTED. Sensitivity of predictions to geometry variation NOT EXPLICITLY ANALYZED.
- **Q-E data**: 91 patients (93 lesions), CCTA-based, retrospective (November 2017–May 2021), invasive FFR ground truth present. Private institutional data (Peking University People's Hospital). Patients: stable CAD, 30–90% visual stenosis, vessel diameter ≥2 mm.
- **Q-F meshing**: 3D reconstruction via Mimics Research 20.0 under cardiologist guidance; manual cross-sectional area measurements at 3 mm behind bifurcation. No mesh generation (0D model, no CFD solving).

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Presents comprehensive 0D LPM (closed-loop cardiovascular + coronary) with ML stenosis flow resistance, achieving FFR prediction at 0.80 threshold; relevant to computational methodology but does not study segmentation error effects or BC compensation for geometry uncertainty.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity analysis of FFR predictions to segmentation variations, or compares how measurement uncertainty in coronary geometry affects model accuracy and clinical decision at 0.80 threshold.

## Ideation opening (CFD + imaging)
- None stated. Paper addresses computational efficiency (10 min vs 10 h) but does not identify a research gap in CFD-imaging integration for segmentation or geometry uncertainty quantification.
