---
source_pdf_path: Resources/1-s2.0-S0899707125002591-main.pdf
slug: alabdullah-2026-ffr-ct-meta
ledger_status: TRIAGED
---

# alabdullah-2026-ffr-ct-meta

## Bibliographic
- Title: Clinical value and cost effectiveness of FFR-CT in guiding revascularization and predicting major adverse cardiac events: A meta-analysis
- First author / authors: Ali A. Alabdullah, Ahmed Marey, Yupeng Li
- Year: 2026
- Venue: Clinical Imaging
- DOI: https://doi.org/10.1016/j.clinimag.2025.110659

## One-line claim
Meta-analysis of 15 studies (13,224 patients) demonstrates FFR-CT ≤0.80 predicts MACE and revascularization need with lower unplanned revascularization rates, though heterogeneous cost-effectiveness across healthcare systems.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (meta-analysis). Underlying studies do not systematically address geometric perturbation or inter-observer segmentation variability.
- **Q-B decision flip**: YES, extensively reported. Revascularization rate FFR-CT negative (>0.8): 5.8%; FFR-CT positive (≤0.8): 41.4% (OR 13.02, p<0.0001). MACE: FFR-CT negative 0.9%, positive 2.6% (OR 3.62, p=0.0001). No direct reclassification rate from segmentation error reported.
- **Q-C BC tuning**: NOT REPORTED. Meta-analysis of clinical outcomes, not CFD methodology. No discussion of boundary condition strategies, tuning protocols, or whether anatomical uncertainty is masked by BC optimization.
- **Q-D fidelity / quantity**: CFD-based FFR-CT (HeartFlow algorithm + deep learning variants). Computational approach; NOT 3D simulation with WSS/OSI. Hemodynamically significant CAD defined by invasive FFR ≤0.80.
- **Q-E data**: 15 studies pooled; N=13,224 (revascularization analysis), N=11,814 (MACE analysis). Invasive FFR as gold standard. Studies 2017–2023; mostly private or mixed cohorts; no systematic reporting of public dataset availability.
- **Q-F meshing**: NOT DISCUSSED. FFR-CT uses computational post-processing of CCTA geometry; meshing not detailed in clinical literature.

## Novelty bearing on T6
- bucket: BACKGROUND | SUPPORT
- one-line reason: Establishes clinical evidence that FFR-CT-derived revascularization decisions (FFR ≤0.80) correlate with outcomes and MACE; provides context for T6's hypothesis that segmentation error affects decision outcomes. Does not isolate geometric error sensitivity.
- verdict: LIGHT
- revisit-if: Subgroup analysis showing how revascularization decision variability correlates with segmentation uncertainty or systematic geometry perturbation across sites.

