---
source_pdf_path: Resources/2505.13536v1.pdf
slug: ghosh-2024-arterial-irregularity
ledger_status: TRIAGED
---

# ghosh-2024-arterial-irregularity

## Bibliographic
- Title: Investigating the Impact of Arterial Irregularity On Clinical Parameters Using Reduced Order CFD Models In Stenosed Coronary Artery
- First author / authors (first 3 + et al.): Priyanshu Ghosh, Sayan Karmakar, Disha Mondal
- Year: 2024
- Venue: Proceedings FMFP 2024 conference
- DOI: NOT REPORTED

## One-line claim
A 1D/2D reduced-order CFD model investigates the impact of periodic arterial surface irregularities (based on real atherosclerotic arterial cast data) on FFR and iFR in intermediate-grade coronary stenosis.

## T6 targeted questions
- **Q-A geometry perturbation**: Stenosis characterized via "periodic surface irregularities of the lesion. These irregularities are based on the height measurements obtained from a left circumflex coronary arterial cast, which exhibits mild, diffuse atherosclerotic disease." This is a REAL anatomical perturbation (derived from pathological specimen), not synthetic researcher-chosen amounts. Irregularity height calibrated to cast data; shape assumed periodic. Severity levels: 40%, 50%, 70%.
- **Q-B decision flip**: FFR and iFR calculated across different stenosis severities and smooth vs irregular arteries. Key finding: "The irregular arteries exhibit lower FFR values compared to smooth arteries, suggesting that irregularities in the arterial wall contribute to greater resistance to blood flow, leading to a more significant drop in FFR." FFR thresholds (0.76–0.80 grey zone) mentioned. No actual patient cohort reclassification reported.
- **Q-C BC tuning**: "The boundary conditions generated from the 1D arterial tree model are used in a higher-order 2D axisymmetric model." Uses "resistance model with zero reflection coefficient and realistic pressure waveform inputs applied at the outflow and inflow." BCs derived from 1D model and applied to 2D; no re-tuning after geometry (smooth vs irregular) changes. No analysis of whether BC tuning compensates for surface irregularities.
- **Q-D fidelity / quantity**: Reduced-order: 1D characteristic equations on full arterial tree (61 segments) coupled to 2D axisymmetric local model. Non-Newtonian blood models (power-law, Carreau-Yasuda, Casson). "Wall Shear Stress (WSS)" mentioned as relevant, though detailed WSS sensitivity not reported.
- **Q-E data**: Patient-specific CT scans; intermediate-grade stenosis cases. No invasive FFR validation.
- **Q-F meshing**: Analytical formulation for stenosis with periodic surface irregularities. Grid independence study: ~200,000 elements for 2D axisymmetric model. Stenosed section (segment 4) modeled locally with high detail.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Directly addresses irregularity-induced hemodynamic changes using real anatomical data; relevant to T6's focus on realistic (not synthetic) geometric perturbations and their effect on flow indices.
- verdict: LIGHT
- revisit-if: If full paper reports quantitative inter-observer/inter-segmenter variability magnitudes for intermediate-grade stenosis, or compares smooth vs irregular FFR differences to invasive cohort reclassification rates.
