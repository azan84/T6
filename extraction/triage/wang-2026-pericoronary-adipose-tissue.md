---
source_pdf_path: Resources/fcvm-13-1833189.pdf
slug: wang-2026-pericoronary-adipose-tissue
ledger_status: TRIAGED
---

# wang-2026-pericoronary-adipose-tissue

## Bibliographic
- Title: Pericoronary adipose tissue radiomics enhances prediction of major adverse cardiovascular events beyond CCTA-derived functional parameters in coronary atherosclerosis
- First author / authors (first 3 + et al.): Wang Z, Wu Z, Cao M, et al.
- Year: 2026
- Venue: Frontiers in Cardiovascular Medicine
- DOI: 10.3389/fcvm.2026.1833189

## One-line claim
Radiomics features extracted from pericoronary adipose tissue improve machine learning prediction of MACE beyond CCTA-derived stenosis severity and CT-FFR alone.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No geometric perturbation or lumen/segmentation uncertainty studied.
- **Q-B decision flip**: YES, FFR threshold mentioned. "Integrating the criteria of stenosis ≥ 70% and CT-FFR ≤ 0.80 into the assessment framework can notably enhance the prognostic stratification capability." CT-FFR used as independent predictor of MACE (P < 0.05).
- **Q-C BC tuning**: NOT REPORTED. No boundary condition tuning, Windkessel, resistance, or CFD solver details discussed.
- **Q-D fidelity / quantity**: Reduced-order only. Uses CT-FFR computed via CFD (not specified), stenosis severity, and radiomics from adipose tissue. Does NOT report WSS/OSI or other spatially-resolved fields.
- **Q-E data**: N=171 CAS patients (88M/83F), private clinical data from Third People's Hospital Datong (Nov 2020–Sep 2022), CT-FFR computed (not invasive FFR gold standard validation reported).
- **Q-F meshing**: NOT REPORTED. PCAT segmentation noted ("adipose tissue extending outward from vessel's outer wall by distance equal to one vessel diameter, fat attenuation −190 to −30 Hu") but no meshing details for CFD.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Studies machine learning on imaging biomarkers for MACE prognosis, not segmentation error propagation or BC tuning effects on diagnosis.
- verdict: LIGHT
- revisit-if: If incorporating radiomics as confounder in error-ranking models, though unlikely relevant to core T6 aim.
