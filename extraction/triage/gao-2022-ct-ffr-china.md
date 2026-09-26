---
source_pdf_path: Resources/fcvm-09-819460.pdf
slug: gao-2022-ct-ffr-china
ledger_status: TRIAGED
---

# gao-2022-ct-ffr-china

## Bibliographic
- Title: Diagnostic Performance of CT FFR With a New Parameter Optimized Computational Fluid Dynamics Algorithm From the CT-FFR-CHINA Trial: Characteristic Analysis of Gray Zone Lesions and Misdiagnosed Lesions
- First author / authors (first 3 + et al.): Gao Y, Zhao N, Song L et al.
- Year: 2022
- Venue: Frontiers in Cardiovascular Medicine
- DOI: 10.3389/fcvm.2022.819460

## One-line claim
Parameter-optimized CFD algorithm for CT-FFR achieves superior diagnostic performance (sensitivity 89.9%, specificity 87.8%) in detecting ischemia-causing lesions vs CTA alone.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb; uses patient-specific CTA geometry. NOT measuring segmentation disagreement.
- **Q-B decision flip**: DIRECTLY RELEVANT—YES. FFR < 0.80 threshold for ischemia. Per-vessel: sensitivity 89.9%, specificity 87.8%, accuracy 88.8% for CT-FFR. Defines "gray zone" (0.75–0.80); accuracy 80% in gray zone. Shows lesion reclassification: "CT-FFR values of >0.90 and ≤0.60 provided almost complete certainty" vs FFR around 0.80 cut-point shows "less certainty."
- **Q-C BC tuning**: CRITICAL—YES. "Parameters used in the boundary conditions for CT-FFR computation were optimized in reduced-order models using retrospective data by minimizing the difference between CT-FFR and known FFR. The parameters were fixed and applied to all subjects during this prospective trial." Quote: "In the reduced order model for blood pressure and flow in coronary arteries, we showed the computed FFR can be expressed as a function of these parameters. Those parameters were optimized by minimizing the mean squared error." No tuning after geometry change; optimization done once on retrospective cohort.
- **Q-D fidelity / quantity**: 3D CFD (customized solver) coupled with reduced-order models. Reports pressure and FFR; no explicit WSS/OSI in excerpt.
- **Q-E data**: N=317 patients, 366 vessels (multicenter trial CT-FFR-CHINA). Invasive FFR ground truth present (YES). Prospective design.
- **Q-F meshing**: Automatic geometric segmentation using deep learning + meshing. Mentions adaptive meshing and vessel enhancement but limited detail on robustness.

## Novelty bearing on T6
- bucket: SUPPORT | METHOD
- one-line reason: Large prospective multicenter trial validating parameter-optimized CFD for coronary FFR; demonstrates that BC parameter optimization is key to FFR accuracy and decision-making at 0.80 threshold; "gray zone" analysis directly relevant to T6's decision-flip metric
- verdict: FULL
- revisit-if: Already FULL—benchmark trial for CT-FFR methodology; gray zone analysis and parameter optimization core to T6 framing

