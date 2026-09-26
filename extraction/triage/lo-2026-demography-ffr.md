---
source_pdf_path: Resources/s10439-026-04002-2.pdf
slug: lo-2026-demography-ffr
ledger_status: TRIAGED
---

# lo-2026-demography-ffr

## Bibliographic
- Title: A Novel Demography-Based Approach to Define Patient-Specific Outflow Boundary Conditions in CT-Based FFR Computations
- First author / authors (first 3 + et al.): Ernest W. C. Lo, Francesca Pugliese, Leon Menezes et al.
- Year: 2026
- Venue: Annals of Biomedical Engineering
- DOI: 10.1007/s10439-026-04002-2

## One-line claim
- Multivariate regression model predicting individual microvascular flow response (MFR) from sex, diabetes, smoking status enables accurate CT-FFR computation without perfusion imaging.

## T6 targeted questions
- **Q-A geometry perturbation**: Does not perturb; uses real patient cCTA geometries. No systematic variation of segmentation error tested.
- **Q-B decision flip**: FFR computed with diagnosis at threshold 0.8. Per-vessel sensitivity 95.8%, specificity 100% using demography-based MFR model vs. invasive FFR (N=10, 11 vessels).
- **Q-C BC tuning**: Core focus on outlet BC tuning via Windkessel models. Derives patient-specific microvascular resistance from demographic regression (PET cohort N=101) as function of MFR. Compares three approaches: (1) conventional (constant population MFR), (2) demography-based MFR, (3) CTP-based global MFR. Shows demography model improves FFR by 0.08 average (68→76) vs. conventional; comparable to CTP-based (0.74). NO statement about tuning COMPENSATING for geometric error; focus is improving accuracy of downstream BC without additional imaging.
- **Q-D fidelity / quantity**: 3D CFD with 2-element Windkessel at terminal branches; structured tree model for resistance calculation. Steady-state hyperemia (quasi-transient to reach steady state). Computes FFR (pressure ratio), flow, velocity. No WSS/OSI or tissue perfusion.
- **Q-E data**: PET cohort: 101 patients (age 70±9 yr, 65M/36F) with 82Rb PET perfusion for CFR derivation. CTP cohort (test): 10 patients (age 59±6 yr, all male) with cCTA, CTP, invasive FFR at Barts Heart Centre. Private clinical data.
- **Q-F meshing**: Simpleware ScanIP for segmentation (threshold ~200 HU, no smoothing); branches <2 mm excluded. Tetrahedral mesh (0.2 mm global, 6 prism layers near wall, ~1M elements). Mesh sensitivity tested. No explicit robustness on poor/topologically incorrect geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates that BC tuning via demographic surrogates significantly improves FFR accuracy without perfusion imaging; directly relevant to T6's premise of BC adjustment and diagnostic accuracy.
- verdict: FULL
- revisit-if: Always; recent (2026) and shows practical BC tuning strategy that bridges gap between population averages and patient-specific FFR without stress imaging—key methodological contribution to T6.
