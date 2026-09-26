---
source_pdf_path: Resources/s41746-025-01920-8.pdf
slug: geddes-2025-hf-twins
ledger_status: TRIAGED
---

# geddes-2025-hf-twins

## Bibliographic
- Title: Digital twins for noninvasively measuring predictive markers of right heart failure
- First author / authors: Justen R. Geddes, Christopher W. Jensen, Cyrus Tanade (et al.)
- Year: 2025
- Venue: npj Digital Medicine (Nature partnership with Seoul National University Bundang Hospital)
- DOI: 10.1038/s41746-025-01920-8

## One-line claim
3D CFD-based digital twins of pulmonary arteries can predict patient-specific hemodynamic metrics (pressure, flow) for early detection of worsening heart failure, with exploration of minimal geometric complexity and boundary condition effects.

## T6 targeted questions
- **Q-A geometry perturbation**: No systematic perturbation study. Uses patient-specific pulmonary artery geometry. NOT REPORTED: inter-observer segmentation disagreement or measurement uncertainty magnitude.
- **Q-B decision flip**: NOT REPORTED. Heart failure context; does not address FFR or 0.80 threshold decision-making.
- **Q-C BC tuning**: YES—Abstract: "explore the effects of varying boundary conditions." "By validating our digital twins against invasively-measured data, we demonstrate their potential." Investigates minimal geometric complexity required for pressure prediction. NOT REPORTED: specific BC tuning protocol, whether changes with geometry perturbation, or compensation for topological error.
- **Q-D fidelity / quantity**: 3D CFD for hemodynamics in pulmonary arteries. NOT REPORTED: WSS/OSI or wall shear stress analysis in front matter.
- **Q-E data**: Patient-specific cohort with invasive right heart catheterization (RHC) and hemodynamic monitors. Cohort size NOT REPORTED in abstract. Invasive pressure data used for validation.
- **Q-F meshing**: YES (implicit)—"strategy to determine the minimal geometric complexity required for accurate pressure prediction" suggests geometry/mesh sensitivity study. NOT REPORTED: segmentation robustness or inter-observer disagreement testing.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Develops 3D CFD digital twins with exploration of geometric simplification and BC effects. Relevant for understanding model sensitivity but limited detail on segmentation uncertainty handling.
- verdict: LIGHT
- revisit-if: Full paper details BC tuning protocol reapplied under geometry perturbation, or demonstrates whether model accuracy degrades with segmentation error.
