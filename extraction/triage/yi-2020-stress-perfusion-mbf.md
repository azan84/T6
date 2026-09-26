---
source_pdf_path: Resources/1-s2.0-S193459251930173X-main.pdf
slug: yi-2020-stress-perfusion-mbf
ledger_status: TRIAGED
---

# yi-2020-stress-perfusion-mbf

## Bibliographic
- Title: Myocardial blood flow analysis of stress dynamic myocardial CT perfusion for hemodynamically significant coronary artery disease diagnosis: The clinical value of relative parameter optimization
- First author / authors: Yan Yi, Cheng Xu, Wei Wu
- Year: 2020
- Venue: Journal of Cardiovascular Computed Tomography
- DOI: https://doi.org/10.1016/j.jcct.2019.10.001

## One-line claim
Comparative study of relative myocardial blood flow (MBF) parameter optimization in stress dynamic CT perfusion shows that highest-segmental-reference-based hi_Ratio (endocardial layer) achieves optimal diagnostic accuracy (AUC 0.906) for detecting hemodynamically significant CAD (FFR ≤0.80).

## T6 targeted questions
- **Q-A geometry perturbation**: REAL (implicit). Study compares diagnostic methods on FFR-positive vs. FFR-negative patients; measures myocardial perfusion in presence of actual hemodynamic lesions. Does NOT systematically perturb geometry or measure segmentation disagreement.
- **Q-B decision flip**: YES, FFR ≤0.80 threshold. Study reports ischemia detection (sensitivity 74.1%, specificity 93.6%, diagnostic accuracy 86.1% for hi_Ratio endocardial with cutoff 0.675). No explicit reclassification rate.
- **Q-C BC tuning**: MINIMAL/IMPLICIT. Dynamic CT perfusion relies on vasodilator stress (ATP infusion) to induce hyperemia; outlet conditions are not explicitly tuned per lesion or re-optimized after geometry assessment.
- **Q-D fidelity / quantity**: 3D dynamic CT perfusion (stress and rest acquisitions). Calculates myocardial blood flow (absolute MBF, mL/100 mL/min) and relative MBF ratios. Reports WSS-like tissue-level hemodynamic sensitivity (endocardial vs. transmural perfusion differences). NOT explicit WSS/OSI of vessel walls.
- **Q-E data**: N=60 patients (86 initially screened, 60 with 151 vessels analyzed), FFR reference standard. Prospective enrollment Dec 2016–Apr 2018. Private cohort.
- **Q-F meshing**: NOT APPLICABLE to CT perfusion; no 3D mesh/volume meshing. Perfusion imaging in 17-segment AHA model.

## Novelty bearing on T6
- bucket: METHOD | BACKGROUND
- one-line reason: Establishes optimal quantitative perfusion parameters (MBF ratios) for FFR-based ischemia classification; relevant for T6's understanding of flow-based decision-making and sensitivity to reference MBF assumptions, but does not address segmentation error or BC adaptation.
- verdict: LIGHT
- revisit-if: Sensitivity analysis showing MBF parameter stability across varying CCTA segmentation methods or analysis of how segmentation uncertainty propagates to MBF cutoff thresholds.

