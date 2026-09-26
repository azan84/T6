---
source_pdf_path: Resources/jimaging-12-00196-v2.pdf
slug: lisasi-2026-diffusion-bloodpressure
ledger_status: TRIAGED
---

# lisasi-2026-diffusion-bloodpressure

## Bibliographic
- Title: Computed Fluid Dynamics-Based Blood Pressure Prediction for Coronary Artery Disease Diagnosis Using Coronary Computed Tomography Angiography
- First author / authors (first 3 + et al.): Rene Lisasi, Huan Huang, William Pei, Michele Esposito, Chen Zhao
- Year: 2026
- Venue: J. Imaging
- DOI: 10.3390/jimaging12050196

## One-line claim
- Computed Fluid Dynamics-Based Blood Pressure Prediction for Coronary Artery Disease Diagnosis Using ...

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED - No discussion of segmentation uncertainty measurement
- **Q-B decision flip**: NOT REPORTED - FFR threshold mentioned (≤0.80 indicates hemodynamically significant stenosis) but no reclassification rates reported
- **Q-C BC tuning**: YES - CFD simulations use SimVascular; initial pressure set to 133,300 Pa; tuning/optimization details not extensively discussed; pipeline includes meshing, parameter assignment
- **Q-D fidelity / quantity**: YES - 3D CFD simulations with SimVascular; no explicit WSS/OSI reporting in abstract/introduction but hemodynamic fields discussed
- **Q-E data**: Two CCTA datasets (CCTA1000 and CCTA36); public databases; NO invasive FFR ground truth mentioned
- **Q-F meshing**: YES - Details on segmentation→meshing pipeline: 3D Slicer for segmentation, VMTK for centerline extraction, SimVascular for modeling and meshing; average 62,088 nodes, 321,323 elements

## Novelty bearing on T6
- bucket: METHOD
- reason: CFD-based pressure prediction pipeline using deep learning (diffusion model); relevant to BC tuning and CFD workflow methodology
- verdict: FULL
- revisit-if: None - pursue for BC tuning and meshing robustness details
