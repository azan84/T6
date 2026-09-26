---
source_pdf_path: Resources/State-of-the-Art_Computational_Models_of_Circle_of_Willis_With_Physiological_Applications_A_Review.pdf
slug: liu-2020-circle-willis-review
ledger_id: C029
ledger_status: TRIAGED
---

# liu-2020-circle-willis-review

## Bibliographic
- Title: State-of-the-Art Computational Models of Circle of Willis With Physiological Applications: A Review
- First author / authors (first 3 + et al.): Liu H, Wang D, Leng X
- Year: 2020
- Venue: IEEE Access
- DOI: 10.1109/ACCESS.2020.3007737

## One-line claim
A comprehensive review of computational models (0D/1D/3D CFD and FSI) of the circle of Willis intracranial circulation, categorizing their structure, innovative techniques (non-Newtonian rheology, multi-scale coupling, FSI), and clinical applications for stroke and aneurysm assessment.

## T6 targeted questions
- **Q-A geometry perturbation**: Paper mentions studies on "estimating the effects of geometric variations on the formation of aneurysms in the CoW" but does not quantify segmentation uncertainty or inter-observer lumen measurement disagreement. NOT REPORTED on magnitude of geometry perturbation from imaging/segmentation error.
- **Q-B decision flip**: No FFR or diagnostic threshold reclassification. Not applicable to CoW clinical decision-making (different clinical context - ischemic stroke, aneurysm, not coronary stenosis). NOT REPORTED.
- **Q-C BC tuning**: Extensive discussion of boundary conditions: Windkessel (R, RC, RCL) models for distal circulation: "The resistance (R), capacitance (C), and inductance (L) elements simulate the effects of vessel resistance, vessel compliance, and blood inertia." Mentions "0D fractal tree model" and "three-element RCR 0D model" as outlet conditions. No explicit discussion of BC re-tuning after geometry change or whether BC tuning compensates for measurement/segmentation error.
- **Q-D fidelity / quantity**: Comprehensive coverage of 0D, 1D, 3D CFD, and FSI models. 3D models report local flow fields, WSS, and pressure. Non-Newtonian blood rheology models (Carreau, power-law, Casson) discussed. Focus on cerebral intracranial arteries, not coronary.
- **Q-E data**: Patient-specific imaging (CT, MRI) and hemodynamic measurement used in reviewed studies. Intracranial circulation focus; no invasive FFR ground truth.
- **Q-F meshing**: Reviews models with "geometry reconstructed from patient-specific imaging data" and in-vitro validation, but does not address robustness of meshing to poor or topologically incorrect geometry, or sensitivity to segmentation threshold/method.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive review of multi-scale hemodynamic modeling techniques (0D/1D/3D coupling, FSI, Windkessel BC, non-Newtonian rheology) applicable to vascular systems; focuses on cerebral circulation but methods are translatable to coronary modeling and FFR-inspired analysis.
- verdict: LIGHT
- revisit-if: If paper contains quantified analysis of how geometric variations (segmentation error, measurement uncertainty) affect hemodynamic predictions or clinical decisions, or if it discusses BC tuning strategies in response to plausible geometry variations.

## Ideation opening (CFD + imaging)
Paper notes that "Patient-specific arterial geometry was widely applied in 3D and FSI models... [but] currently, there are few patient-specific models of CoW that are fully validated by in-vivo measurement" and emphasizes that "the application of patient-specific imaging data and hemodynamic parameters is limited." Implies a gap in validating imaging-derived hemodynamic models and understanding how imaging uncertainty propagates to predictions.
