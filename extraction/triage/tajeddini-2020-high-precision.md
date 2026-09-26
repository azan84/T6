---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2020 - Tajeddini - High precision invasive FFR  low‐cost invasive iFR  or non‐invasive CFR  .pdf
slug: tajeddini-2020-high-precision
ledger_status: TRIAGED
---

# tajeddini-2020-high-precision

## Bibliographic
- Title: High precision invasive FFR, low-cost invasive iFR, or non-invasive CFR?: optimum assessment of coronary artery stenosis based on patient-specific computational models
- First author / authors (first 3): Farshad Tajeddini, Mohammad Reza Nikmaneshi, Hossein Ali Pakravan
- Year: 2020
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3382

## One-line claim
3D CFD simulations of patient-specific coronary geometries demonstrate that FFR is a more conservative diagnostic index than iFR and CFR for assessing stenosis severity; additionally computes hemodynamic atherosusceptibility markers (TAWSS, OSI, RRT) and evaluates FFR accuracy across different stenosis morphologies.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb or measure inter-observer segmentation disagreement. Reconstructs 7 patient-specific left coronary geometries from CT angiography (LMCA, LAD, LCX with stenoses ranging 28–75% diameter reduction). Each geometry treated as single deterministic model.
- **Q-B decision flip**: YES, reports FFR ≤0.80 as cut-off threshold. Accuracy (86%, 93%, 82% across stenosis ranges), sensitivity, specificity reported for FFR-based classification. Diagnostic performance assessed across FFR ranges including gray-zone (0.75–0.80). NO explicit flip-rate metric but clear documentation of misclassification counts.
- **Q-C BC tuning**: Aortic inlet pressure prescribed as inlet BC; lumped parameter model (LPM) outlet BC. NO statement that BC parameters re-tuned after geometry change or that tuning compensates for segmentation error. BC parameters appear case-independent, based on published physiological values.
- **Q-D fidelity / quantity**: 3D CFD via Navier–Stokes equations (ANSYS FLUENT). Reports FFR, iFR, CFR (diagnostic indices) AND spatially-resolved hemodynamic fields: time-averaged wall shear stress (TAWSS), oscillatory shear index (OSI), relative residence time (RRT). These markers used to identify atherosusceptible sites.
- **Q-E data**: N=7 patients with 9 stenosed coronary arteries (cases with stenosis in LAD, LCX, LMCA) from Tehran Heart Center. Invasive FFR as gold standard. Data source: clinical CT angiography; private institutional data.
- **Q-F meshing**: 3D geometry reconstruction from CT angiography using Mimics software; centerline extraction; manual refinement in CATIA for smoothness. Tetrahedral meshing (245k–410k elements) with mesh sensitivity analysis. NO explicit discussion of handling topologically incorrect geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Direct evaluation of FFR diagnostic accuracy at 0.80 threshold on patient-specific geometries with invasive FFR ground truth; provides benchmark diagnostic performance metrics for FFR-based revascularization decisions.
- verdict: FULL
- revisit-if: Already high relevance; no additional conditions needed.

