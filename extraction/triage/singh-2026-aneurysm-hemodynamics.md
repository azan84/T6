---
source_pdf_path: Resources/s10278-026-02231-4.pdf
slug: singh-2026-aneurysm-hemodynamics
ledger_status: TRIAGED
---

# singh-2026-aneurysm-hemodynamics

## Bibliographic
- Title: Machine Learning–Based Reduced‑Order Prediction of Rupture‑Related Hemodynamics in Cerebral Aneurysms with Surface Blebs: A Pilot Study
- First author / authors (first 3 + et al.): Narinderjit Singh Sawaran Singh, Mohammed Derea Ali, Seif Al Bustanji et al.
- Year: 2026
- Venue: Journal of Imaging Informatics in Medicine
- DOI: 10.1007/s10278-026-02231-4

## One-line claim
- POD-LSTM reduced-order framework accurately predicts transient CFD-derived hemodynamics in patient-specific cerebral aneurysms with blebs while reducing computational cost.

## T6 targeted questions
- **Q-A geometry perturbation**: Introduces ARTIFICIAL/SYNTHETIC blebs at high-WSS locations identified from baseline CFD. Bleb sizes not specified; geometric perturbation is researcher-controlled, not measured from patient data.
- **Q-B decision flip**: NOT REPORTED — no binary diagnostic outcome (FFR or equivalent) with threshold-based reclassification.
- **Q-C BC tuning**: NOT ADDRESSED — uses prescribed inlet flow waveforms and simple outlet BCs; no tuning of outlet conditions before/after geometry modification (bleb insertion). No evidence of compensation or masking of error by BC adjustment.
- **Q-D fidelity / quantity**: High-fidelity 3D CFD on 4 cases; transient pulsatile non-Newtonian blood flow (Casson model). Computes WSS, OSI, pressure, velocity, vorticity, helicity, relative residence time. Spatial fields reported for post-bleb hemodynamics.
- **Q-E data**: AneuriskWeb database, N=4 patient-specific aneurysm geometries (ACA, MCA, ICA, BAS). Public database. No invasive ground truth or clinical rupture outcomes.
- **Q-F meshing**: Unstructured tetrahedral mesh with local refinement in aneurysm neck, sac, bleb regions. Same procedure applied to original and bleb-modified models for consistent comparison. No explicit robustness testing on poor/broken geometry.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Cerebral aneurysm domain (not coronary); synthetic perturbation (not real inter-observer disagreement); no functional threshold (no FFR equivalent); no BC tuning hypothesis relevant to T6.
- verdict: LIGHT
- revisit-if: Paper extends to coronary arteries or provides evidence that synthetic geometry perturbations bias hemodynamic sensitivity in ways relevant to T6's real-disagreement thesis.
