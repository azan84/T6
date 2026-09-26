---
source_pdf_path: Resources/2505.12485v2.pdf
slug: roy-2024-reduced-order
ledger_status: TRIAGED
---

# roy-2024-reduced-order

## Bibliographic
- Title: A Reduced-Order CFD Approach for Intermediate grade Coronary Arterial Clinical Parameter Assessment
- First author / authors (first 3 + et al.): Oeshee Roy, Priyanshu Ghosh, Sayan Karmakar
- Year: 2024
- Venue: Proceedings FMFP 2024 conference
- DOI: NOT REPORTED

## One-line claim
A 1D/2D hierarchical reduced-order CFD model predicts FFR and iFR for intermediate-grade coronary stenosis (40–70%) using patient-specific CT scans and analytical stenosis geometry.

## T6 targeted questions
- **Q-A geometry perturbation**: Stenosis is modeled using "analytical equations that account for the tapering condition of the artery." NOT real inter-observer/inter-segmenter disagreement; SYNTHETIC analytical perturbation. Severity levels: 40%, 50%, 70%; lesion lengths: 1 cm, 3 cm (researcher-controlled parameters).
- **Q-B decision flip**: FFR and iFR calculated. Reported results: "At a stenosis severity of 40%, all models demonstrate high FFR values exceeding 0.92." At 50%, Newtonian model FFR ≈ 0.91. At higher severities FFR decreases. FFR values between 0.76–0.80 noted as "grey zone" where clinical judgment is essential. No actual patient cohort reclassification reported.
- **Q-C BC tuning**: "Boundary conditions generated from the 1D model, capturing global characteristics, are subsequently used to simulate a 2D axisymmetric model." Uses "resistance model with reflection coefficient set to zero and realistic pressure waveform input applied at the outflow and inflow respectively." The paper does NOT re-tune BCs after geometry changes; BCs are derived from 1D global model and applied uniformly to 2D local model. No exploration of whether BC tuning masks geometric error.
- **Q-D fidelity / quantity**: Reduced-order approach: 1D characteristic equations (full arterial tree, 61 segments) coupled to 2D axisymmetric local model of stenosed section. Blood modeled as Newtonian and non-Newtonian (power-law, Carreau-Yasuda, Casson). Does NOT report WSS or OSI.
- **Q-E data**: Patient-specific CT scan data integrated into CAD models. Intermediate-grade stenosis cases. No invasive FFR validation reported.
- **Q-F meshing**: Analytical stenosis equations used to describe geometry (variation in cross-sectional area). Grid independence study conducted (mesh sizes 50, 100, 150 points per segment). Final model uses 100 grid points per arterial segment.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates 1D/2D hierarchical coupling strategy and analytical stenosis parameterization for FFR prediction; relevant to T6's reduced-order modeling approach, though uses synthetic perturbations not real segmentation error.
- verdict: LIGHT
- revisit-if: If paper or related work reports on inter-observer segmentation variability in intermediate-grade stenosis, or compares analytical vs real anatomical perturbations.
