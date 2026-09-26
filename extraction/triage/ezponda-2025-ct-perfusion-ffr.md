---
source_pdf_path: Resources/1-s2.0-S2173510725000217-main.pdf
slug: ezponda-2025-ct-perfusion-ffr
ledger_status: TRIAGED
---

# ezponda-2025-ct-perfusion-ffr

## Bibliographic
- Title: CT myocardial perfusion and FFR-CT for the assessment of coronary artery disease
- First author / authors (first 3 + et al.): A. Ezponda, F.M. Caballeros Lam, G. Bastarrika Alemañ
- Year: 2025
- Venue: Radiología
- DOI: Not explicitly stated in extract

## One-line claim
Educational review of CT myocardial perfusion and CT-FFR methodologies, their diagnostic accuracy, clinical indications, and technical requirements for functional assessment of coronary lesions.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Review focuses on clinical techniques and diagnostic performance; no segmentation uncertainty quantification.
- **Q-B decision flip**: Yes; FFR ≤0.75 or FFR ≤0.80 thresholds discussed. CT-FFR sensitivity 93%, specificity 82% for detection of functionally significant lesions.
- **Q-C BC tuning**: Briefly mentioned for FFR-CT: "total coronary blood flow at rest can be estimated from myocardial mass, as coronary flow is proportional to myocardium's oxygen demand at rest" and "hyperaemic state is simulated by reducing microvascular resistance values by 0.21, similar to effect observed in vivo after administering adenosine." No discussion of re-tuning after geometry change or error compensation.
- **Q-D fidelity / quantity**: CT-FFR (0D computational model); stress CT perfusion (static and dynamic); discusses myocardial blood flow (MBF) and WSS concepts but no dedicated 3D CFD coronary hemodynamics.
- **Q-E data**: Review article; cites multiple published studies (CORE320, CRESCENT-II, ADVANCE registry). No single cohort. Reference standard: invasive FFR.
- **Q-F meshing**: NOT REPORTED. Mentions automated segmentation of main coronary arteries but no discussion of robustness on poor geometry or topological issues.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Educational summary of existing CT-FFR and perfusion methods; documents clinical use and diagnostic criteria but does not address geometric uncertainty or BC tuning strategies.
- verdict: LIGHT
- revisit-if: Data on sensitivity to segmentation quality or boundary condition uncertainty in borderline FFR cases (0.75–0.85).
