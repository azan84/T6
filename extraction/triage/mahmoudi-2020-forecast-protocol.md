---
source_pdf_path: Resources/1-s2.0-S155383891930805X-main.pdf
slug: mahmoudi-2020-forecast-protocol
ledger_status: TRIAGED
---

# mahmoudi-2020-forecast-protocol

## Bibliographic
- Title: Fractional Flow Reserve Derived from Computed Tomography Coronary Angiography in the Assessment and Management of Stable Chest Pain: Rationale and Design of the FORECAST Trial
- First author / authors: Michael Mahmoudi, Zoe Nicholas, Jacqui Nuttall
- Year: 2020
- Venue: Cardiovascular Revascularization Medicine
- DOI: https://doi.org/10.1016/j.carrev.2019.12.009

## One-line claim
FORECAST is a UK multicenter RCT (N=1400) protocol comparing FFR-CT vs. routine diagnostic pathway (NICE CG95 guidelines) for stable chest pain management; primary outcome is 9-month resource utilization and cost.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT ADDRESSED. Study does not measure segmentation uncertainty or inter-observer disagreement; focuses on clinical outcomes of FFRCT vs. conventional testing strategies.
- **Q-B decision flip**: YES, decision target is revascularization. Primary outcomes include revascularization rates (PCI/CABG), invasive angiography referral rates, and hospitalization. No explicit analysis of FFR ≤0.80 reclassification due to anatomy variation.
- **Q-C BC tuning**: NOT DISCUSSED. Protocol describes HeartFlow FFRCT as black-box analysis; no detail on boundary condition methodology or whether tuning adapts post-segmentation.
- **Q-D fidelity / quantity**: FFR-CT (HeartFlow, computational fluid dynamics applied to CTCA). NOT 3D simulation with WSS/OSI output. Hemodynamic assessment via FFR ≤0.80 only.
- **Q-E data**: N=1400 (planned; RCT). Stable chest pain patients in UK Rapid Access Chest Pain Clinics. Invasive FFR reference standard (performed selectively per protocol). Prospective enrollment 2017–ongoing.
- **Q-F meshing**: NOT DISCUSSED. FORECAST protocol focuses on clinical decision impact, not CFD methodology or meshing robustness.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Large clinical trial establishing resource utilization and clinical outcomes of FFR-CT strategy; provides evidence base for T6's FFR ≤0.80 decision outcome framework, but does not address geometric error sensitivity.
- verdict: LIGHT
- revisit-if: Post-hoc subgroup analysis showing FFR-CT decision accuracy vs. inter-observer CCTA stenosis measurement disagreement, or outcomes stratified by CCTA image quality.

