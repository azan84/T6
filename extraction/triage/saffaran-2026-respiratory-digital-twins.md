---
source_pdf_path: Resources/s13054-026-06079-6.pdf
slug: saffaran-2026-respiratory-digital-twins
ledger_status: TRIAGED
---

# saffaran-2026-respiratory-digital-twins

## Bibliographic
- Title: Computational tools for personalizing treatment of acute respiratory failure, from machine learning to digital twins: a narrative review
- First author / authors (first 3 + et al.): Sina Saffaran, Hang Yu, Hossein Shamohammadi, et al.
- Year: 2026
- Venue: Critical Care
- DOI: 10.1186/s13054-026-06079-6

## One-line claim
A narrative review of patient-specific computational tools (data-driven models, mechanistic models, and digital twins) for personalizing respiratory support strategies in acute respiratory failure across neonatal, pediatric, and adult populations.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. The paper focuses on respiratory physiology models (lung mechanics, ventilation parameters) rather than geometric/segmentation perturbation studies.
- **Q-B decision flip**: NOT REPORTED. No discussion of threshold-based diagnostic reclassification; focuses on ventilation strategy selection rather than binary diagnostic outcomes.
- **Q-C BC tuning**: NOT REPORTED. Discusses model calibration to patient data (oesophageal pressure, tidal volume, blood gases) but not boundary condition tuning or geometric compensation mechanisms.
- **Q-D fidelity / quantity**: PARTIAL. Mechanistic models integrate cardiopulmonary physiology (0D/1D); no specific mention of spatial CFD fields, WSS, or OSI.
- **Q-E data**: PARTIAL. Mentions patient cohorts (e.g., 58 adult AHRF patients, 10 patients with EIT monitoring) but does not report if invasive ground truth or FFR data present; datasets not named as public/private.
- **Q-F meshing**: NOT REPORTED. No discussion of segmentation, meshing, or robustness to topological errors.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Focuses on respiratory physiology digital twins for ICU ventilation strategy optimization; no bearing on coronary imaging, FFR, or cardiovascular segmentation validation.
- possible-other-project: Digital twins for acute respiratory failure treatment optimization in critical care
- verdict: LIGHT
- revisit-if: If T6 expands to multi-organ digital twin validation frameworks or to general principles of model-patient mismatch masking.
