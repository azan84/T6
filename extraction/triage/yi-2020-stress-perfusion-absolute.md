---
source_pdf_path: Resources/1-s2.0-S1934592519305829-main.pdf
slug: yi-2020-stress-perfusion-absolute
ledger_status: TRIAGED
---

# yi-2020-stress-perfusion-absolute

## Bibliographic
- Title: Stress dynamic myocardial CT perfusion for symptomatic patients with intermediate- or high-risk of coronary artery disease: Optimization and incremental improvement between the absolute and relative myocardial blood flow analysis
- First author / authors: Yan Yi, Cheng Xu, Wei Wu
- Year: 2020
- Venue: Journal of Cardiovascular Computed Tomography
- DOI: https://doi.org/10.1016/j.jcct.2020.01.010

## One-line claim
In intermediate-to-high-risk CAD patients, semiautomatic absolute MBF assessment (endocardial layer, AUC 0.955) outperforms relative MBF ratio (AUC 0.906) for detecting ischemia; hybrid approach (absolute + relative) improves accuracy in ambiguous intermediate zones.

## T6 targeted questions
- **Q-A geometry perturbation**: REAL (implicit). Study cohort N=60 with known/suspected CAD; 151 vessels analyzed per invasive FFR. Measures hemodynamic sensitivity in presence of actual stenoses. NO systematic geometry perturbation or inter-segmenter disagreement quantification.
- **Q-B decision flip**: YES, FFR ≤0.80 threshold for ischemia definition. Absolute MBF: sensitivity 82.76%, specificity 98.92%, diagnostic accuracy 92.72%. Relative MBF: sensitivity 74.14%, specificity 93.56%, diagnostic accuracy 86.09%. Hybrid approach improves intermediate-zone accuracy from 79.1% to 88.4% (intermediate zone: 0.66–0.76 relative MBF ratio).
- **Q-C BC tuning**: NOT EXPLICITLY DISCUSSED. Dynamic perfusion imaging uses adenosine stress (vasodilator) rather than explicit BC optimization. Study does not address whether MBF-based FFR surrogates adaptively adjust for geometry variability.
- **Q-D fidelity / quantity**: Dynamic CT perfusion (3D acquisition during stress/rest). Measures absolute myocardial blood flow (mL/100 mL/min) and relative MBF ratios. Tissue-level hemodynamics (endocardial vs. transmural sensitivity). NOT vessel WSS/OSI.
- **Q-E data**: N=60 patients (43 men, 17 women; 61.38±8.01 years); 151 vessels (60 patients). Intermediate-to-high-risk pretest CAD probability. Invasive FFR reference standard (FFR ≤0.80 for ischemia). Prospective Dec 2016–Apr 2018. Private single-center cohort.
- **Q-F meshing**: NOT APPLICABLE. CT perfusion imaging; no 3D mesh generation or meshing robustness evaluation.

## Novelty bearing on T6
- bucket: METHOD | BACKGROUND
- one-line reason: Demonstrates that absolute MBF is more robust than relative MBF ratios for ischemia detection, addressing reference-value dependency; relevant for T6's understanding of surrogate-model sensitivity but does not isolate geometric error effects or BC strategy comparison.
- verdict: LIGHT
- revisit-if: Analysis showing how MBF-based ischemia classification varies with CCTA segmentation uncertainty, especially in multi-vessel disease where "normal" reference zones may be globally reduced.

