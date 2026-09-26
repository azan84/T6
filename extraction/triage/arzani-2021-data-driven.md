---
source_pdf_path: Resources/rsif.2020.0802.pdf
slug: arzani-2021-data-driven
ledger_status: TRIAGED
---

# arzani-2021-data-driven

## Bibliographic
- Title: Data-driven cardiovascular flow modelling: examples and opportunities
- First author / authors: Amirhossein Arzani, Scott T. M. Dawson
- Year: 2021
- Venue: Journal of the Royal Society Interface
- DOI: 10.1098/rsif.2020.0802

## One-line claim
Review of data-driven modeling techniques (PCA, DMD, Kalman filter, SINDy, neural networks) for cardiovascular flow reconstruction and reduced-order modeling.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT ADDRESSED—review paper, no empirical geometry perturbation study.
- **Q-B decision flip**: NOT ADDRESSED—no FFR threshold analysis.
- **Q-C BC tuning**: Mentions machine learning for FFR estimation but no explicit BC tuning methodology or discussion of tuning compensating for error. Cites "machine learning-based coronary CT angiography-derived fractional flow reserve (FFR) in coronary artery stenosis" as successful application but does not detail boundary condition protocols.
- **Q-D fidelity / quantity**: Reviews reduced-order modeling (POD, DMD), physics-informed neural networks (PINNs), and data assimilation techniques. Discusses 4D flow MRI, CFD, PIV data. No specific WSS/OSI sensitivity analysis.
- **Q-E data**: NOT APPLICABLE—review/methodology paper; no cohort.
- **Q-F meshing**: Discusses impact of data quality, sparse sensing, and parameter uncertainty on CFD but not specific meshing robustness on poor geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Comprehensive tutorial on reduced-order modeling and data-driven techniques applicable to patient-specific hemodynamics; outlines frameworks for parameter identification and model refinement from noisy data.
- verdict: LIGHT
- revisit-if: When implementing reduced-order models for computational speed-up in the T6 CFD pipeline.
