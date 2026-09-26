---
source_pdf_path: Resources/1-s2.0-S0010482526001241-main.pdf
slug: mulder-2026-hemodynamic-critical-care
ledger_id: C003
ledger_status: TRIAGED
---

# mulder-2026-hemodynamic-critical-care

## Bibliographic
- Title: Computational physiological models for hemodynamic management in critical care: a systematic literature review focusing on model design, credibility and clinical readiness
- First author / authors: M.P. Mulder, R.S.P. Warnaar, T.F. Arendshorst-Ruuls
- Year: 2026
- Venue: Computers in Biology and Medicine, vol. 205
- DOI: 10.1016/j.compbiomed.2026.111561

## One-line claim
A systematic review of 183 zero-dimensional cardiovascular models for critical care hemodynamic management finds 75% at pre-clinical readiness levels 3–4, only 21% achieving moderate credibility, and identifies need for standardised validation and personalisation frameworks.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT APPLICABLE. This is a systematic review of 0D lumped-parameter hemodynamic models for ICU critical care; no coronary artery segmentation or geometry perturbation studies included.
- **Q-B decision flip**: NOT APPLICABLE. Review focuses on ICU hemodynamic management (fluid, inotropes, ECMO support), not coronary artery FFR diagnosis or reclassification.
- **Q-C BC tuning**: NOT APPLICABLE. 0D models use compartmental resistances but paper does not discuss vascular boundary condition tuning, Windkessel parameterisation, or post-geometry BC re-tuning.
- **Q-D fidelity / quantity**: 0D lumped-parameter models exclusively (not 3D CFD). No spatially-resolved fields, WSS, or OSI discussed. Closed-loop circulatory models only.
- **Q-E data**: NOT APPLICABLE. Systematic review paper; no single dataset. Reviewed studies included clinical trials, observational studies, and in-silico research in critical care hemodynamics.
- **Q-F meshing**: NOT APPLICABLE. 0D models do not use mesh-based CFD; no segmentation-to-mesh pipeline discussed.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Provides landscape of computational models for hemodynamic management but focuses on ICU critical care (fluid/inotrope support, ECMO) and 0D reduced-order models; not relevant to coronary artery imaging, 3D CFD, segmentation error, or FFR decision thresholds.
- verdict: LIGHT
- revisit-if: If review explicitly covers coronary artery models, segmentation-to-mesh workflows, or FFR validation against invasive standards.

## Ideation opening (CFD + imaging)
- None stated. Paper addresses computational model credibility and clinical readiness in ICU hemodynamics but does not identify research gaps in CFD-imaging integration for coronary disease or segmentation uncertainty.
