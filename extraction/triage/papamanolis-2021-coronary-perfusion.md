---
source_pdf_path: Resources/s10439-020-02681-z.pdf
slug: papamanolis-2021-coronary-perfusion
ledger_status: TRIAGED
---

# papamanolis-2021-coronary-perfusion

## Bibliographic
- Title: Myocardial Perfusion Simulation for Coronary Artery Disease: A Coupled Patient-Specific Multiscale Model
- First author / authors (first 3 + et al.): Lazaros Papamanolis, Hyun Jin Kim, Clara Jaquet et al.
- Year: 2021
- Venue: Annals of Biomedical Engineering, Vol. 49, No. 5, May 2021
- DOI: 10.1007/s10439-020-02681-z

## One-line claim
- Multiscale 1D coronary + Darcy myocardium model applied to human cCTA data predicts myocardial blood flow (MBF) at tissue level and identifies perfusion deficits in CAD.

## T6 targeted questions
- **Q-A geometry perturbation**: Does not perturb; measures/models existing disease (LAD stenosis). Real patient data from invasive coronary angiography (gold standard diagnosis). Synthetic vasculature generated for arterioles (not real inter-segmenter disagreement).
- **Q-B decision flip**: Does not report FFR or ischemic threshold explicitly; reports MBF values in hyperemia with comparison to [15O]H2O PET data. Identifies perfusion deficit regions but no binary treatment decision flip rate.
- **Q-C BC tuning**: Terminal outlets modeled by synthetic tree generation with diameter-based flow allocation (area ratio rule). Aortic pressure fixed at 93 mmHg (population average). NO re-tuning after geometry change shown. No statement about tuning compensating for geometric error. Limitation acknowledged: synthetic network generation may be suboptimal for severe stenosis cases.
- **Q-D fidelity / quantity**: Hybrid 1D/0D/3D multiscale: 1D Poiseuille in coronaries + single-compartment porous Darcy model for myocardium (steady-state). Computes MBF, pressure, velocity. No WSS/OSI reported; perfusion is spatially resolved at AHA segment level.
- **Q-E data**: cCTA + invasive FFR from PACIFIC trial (NCT01521468); PET ([15O]H2O) perfusion data for validation. N=6 patients (5 non-obstructive CAD, 1 obstructive). Private (PACIFIC trial data).
- **Q-F meshing**: Patient cCTA segmented by HeartFlow Inc. methods. Synthetic coronary trees generated via space-filling algorithm with competitive growth and target flow constraints. Robustness mentioned (dilatation of synthetic trees in response to stenosis); no explicit testing on poor/topologically broken geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: First multiscale model coupling coronary arteries to myocardial tissue-level perfusion on human cCTA data; validates against PET; demonstrates link between epicardial stenosis and perfusion deficit, central to T6's diagnostic frame.
- verdict: FULL
- revisit-if: Always; core reference for multiscale methodology and tissue-level perfusion quantification.
