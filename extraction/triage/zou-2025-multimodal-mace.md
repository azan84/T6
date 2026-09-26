---
source_pdf_path: Resources/s11547-025-01991-3.pdf
slug: zou-2025-multimodal-mace
ledger_status: TRIAGED
---

# zou-2025-multimodal-mace

## Bibliographic
- Title: Multimodal prediction of major adverse cardiovascular events in hypertensive patients with coronary artery disease: integrating pericoronary fat radiomics, CT-FFR, and clinicoradiological features
- First author / authors: Qing Zou, Taichun Qiu, Chunxiao Liang et al.
- Year: 2025
- Venue: La radiologia medica
- DOI: 10.1007/s11547-025-01991-3

## One-line claim
Develops and validates a multimodal predictive model integrating CT-FFR, pericoronary adipose tissue radiomics, and clinical features to predict 2-year major adverse cardiovascular events (MACE) in hypertensive CAD patients.

## T6 targeted questions

- **Q-A geometry perturbation**: NOT REPORTED. Study uses CT-FFR and radiomics features but does not examine geometric perturbation or segmentation variability.

- **Q-B decision flip**: Uses FFR <0.80 threshold implicitly (CT-FFR measurement standard) but does not report reclassification rates or threshold sensitivity analysis.

- **Q-C BC tuning**: NOT DETAILED. Study uses "coronary CT-FFR semiautomatic quantification software (version 1.11.1, Shukun [Beijing] Network Technology)" for CFD-based FFR assessment. States: "The measurement approach varied based on the presence of plaque. For vessels with plaque, the lesion-based method was employed, with CT-FFR measured 20-mm distal to the end of the stenotic lesion." No discussion of boundary condition strategy or tuning.

- **Q-D fidelity / quantity**: 3D CFD-based CT-FFR. Study assesses CT-FFR of LAD, RCA, and LCX but does not report WSS, OSI, or other spatially-resolved hemodynamic fields. CT-FFR used as component of multimodal prediction model.

- **Q-E data**: Retrospective cohort, 237 patients (108 with MACE, 129 without MACE, age-/sex-/risk-matched) from January 2017–April 2021. Invasive FFR NOT explicitly reported as ground truth; study follows clinical outcomes (composite MACE: cardiac death, MI, heart failure, revascularization) over 2-year follow-up.

- **Q-F meshing**: Mentions "Axial and multiplanar reconstruction were performed on an offline workstation (Syngo. Via, version VB20, Siemens Healthineers) to analyze CCTA images" and discusses coronary plaque analysis but does not detail segmentation robustness or mesh generation.

## Novelty bearing on T6

- **bucket**: IRRELEVANT
- **one-line reason**: CT-FFR applied as a feature in a clinical risk prediction model; does not advance FFR computational methodology, boundary condition tuning, or geometric error handling.
- **verdict**: LIGHT
- **revisit-if**: Never—application paper only; no methodological relevance to T6.
