---
source_pdf_path: Resources/ELoThesis21.pdf
slug: lo-2021-ffr-thesis
ledger_status: TRIAGED
---

# lo-2021-ffr-thesis

## Bibliographic
- Title: Integration of Patient-specific Myocardial Perfusion in CT-based FFR Computations
- First author / authors: Ernest Lo (PhD dissertation)
- Year: 2021
- Venue: PhD Thesis, Department of Medical Physics and Biomedical Engineering, University College London
- DOI: NOT REPORTED

## One-line claim
A novel CT-FFR simulation method incorporates patient-specific myocardial vasodilatory response (estimated from perfusion imaging and demographic data) into microvascular boundary conditions, improving diagnostic accuracy from 82% to 91% on 10 validation patients.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED – studies functional assumptions, not geometric segmentation error
- **Q-B decision flip**: Addresses diagnostic accuracy and gray zone (0.75–0.85 FFR) but does not report reclassification rates
- **Q-C BC tuning**: YES – CRITICAL: "The microvasculature is too small to resolve in CT imaging and therefore assumptions are made"; "many assumptions are inevitably needed to define parameters used in the computational method, in particular, boundary conditions"; "The response to hyperaemia assumption is an area to improve on due to the variability of this parameter and how it directly impacts the FFR"; proposes patient-specific resistance tuning based on age, sex, diabetes, smoking
- **Q-D fidelity / quantity**: 3D CFD (ANSYS CFX) with 0D lumped outlet models (Windkessel)
- **Q-E data**: 101 patients with clinically measured CFR (training); 10 patients with PET perfusion + invasive FFR (validation); non-public dataset
- **Q-F meshing**: NOT REPORTED

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Provides evidence that conventional FFR-CT assumptions (ideal vasodilation) are overestimates in real patients and that patient-specific BC tuning improves accuracy; directly supports T6 premise that BC tuning is critical
- verdict: FULL
- revisit-if: NA
