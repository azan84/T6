---
source_pdf_path: Resources/gcsp-2021-3-e202120.pdf
slug: torii-2021-ct-ffrcomputation
ledger_status: TRIAGED
---

# torii-2021-ct-ffrcomputation

## Bibliographic
- Title: CT-based fractional flow reserve: development and expanded application
- First author / authors (first 3 + et al.): Ryo Torii, Magdi H. Yacoub
- Year: 2021
- Venue: Global Cardiology Science and Practice
- DOI: 10.21542/gcsp.2021.20

## One-line claim
Comprehensive technical review of CT-based FFR computational methods, assumptions, and challenges including boundary condition setting and expanded applications beyond coronary disease.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Review discusses boundary conditions and model uncertainty but not specifically geometry perturbation measurement or inter-observer disagreement quantification.
- **Q-B decision flip**: NOT REPORTED. No specific FFR 0.80 reclassification rates provided; discusses clinical efficacy in general terms only.
- **Q-C BC tuning**: EXTENSIVELY DISCUSSED. Key quote: "if the boundary conditions are well defined, ideally with intravascular measurement of pressure and flow velocity, the computationally predicted FFR in a short segment of blood vessel closely agrees with the invasively measured FFR. However, in CT-based FFR computations, such data is not likely to exist because of the non-invasive nature of the process, and boundary conditions need to be estimated." Also: "Our study on the impact of outflow conditions indicated that it could considerably affect the predicted FFR more in anatomically severe stenosis, by altering the flow distribution in different coronary vessels, and possibly alter the FFR across the diagnostic threshold. Outflow boundary condition could therefore be one of the areas that could improve CT-based FFR prediction."
- **Q-D fidelity / quantity**: YES, 3D vs 1D (reduced-order) CFD discussed. WSS and derivatives mentioned but focus is pressure/FFR, not spatially-resolved fields. Reduces to 1D for speed (23.9 ± 11.2 min processing).
- **Q-E data**: NOT REPORTED (review article surveying literature, no single cohort).
- **Q-F meshing**: Discusses segmentation limitations (0.5 mm CTCA resolution, 6–8 pixels per 3–4 mm coronary diameter), machine-learning enhancement, but no detail on robustness to topologically broken geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Comprehensive technical review of CT-FFR methods; extensively discusses outflow BC tuning as source of error that alters FFR across diagnostic threshold, relevant to T6's hypothesis that BC tuning can absorb/mask topological error.
- verdict: FULL
- revisit-if: Details on CFD solver robustness under poor segmentation; quantification of BC sensitivity to anatomy.
