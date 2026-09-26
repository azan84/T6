---
source_pdf_path: Resources/s13239-026-00825-1.pdf
slug: tanade-2026-harvi-peripheral-revascularization
ledger_status: TRIAGED
---

# tanade-2026-harvi-peripheral-revascularization

## Bibliographic
- Title: Real-Time Peripheral Revascularization Planning in Chronic Limb Threatening Ischemia Using HarVI: A Digital Twin Approach
- First author / authors (first 3 + et al.): Tanade C, Jensen CW, Ferreira G, Randles A
- Year: 2026
- Venue: Cardiovascular Engineering and Technology
- DOI: 10.1007/s13239-026-00825-1

## One-line claim
HarVI digital twin framework integrates 1D CFD with machine learning for real-time prediction of postoperative hemodynamics in peripheral artery disease revascularization, validated against duplex ultrasound in 7 patients with superficial femoral artery lesions.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (patient-specific PAD geometry; no synthetic perturbation or inter-observer error analysis)
- **Q-B decision flip**: NOT REPORTED (not applicable; study targets peak systolic velocity (PSV) thresholds for restenosis, not FFR 0.80 CAD reclassification)
- **Q-C BC tuning**: **HIGHLY RELEVANT**. "Key components include: (1) automated boundary condition tuning using patient-averaged and optimization-based approaches." BC tuning is central; surrogate ML model enables rapid exploration of intervention scenarios. No explicit statement on whether tuning compensates for topological error, but framework couples BC calibration to patient-specific hemodynamics.
- **Q-D fidelity / quantity**: Reduced-order 1D CFD coupled with machine learning surrogate model for rapid intervention scenario evaluation. No full 3D CFD or WSS/OSI; focuses on peak systolic velocity (PSV) as clinical endpoint. Computational speed enables "near–real-time" intraoperative use.
- **Q-E data**: 7 patients with SFA disease; retrospective validation. Private cohort; postoperative duplex ultrasound PSV as ground truth. No invasive pressure measurement.
- **Q-F meshing**: NOT REPORTED (1D vascular network model; no 3D segmentation→mesh workflow described)

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates automated BC tuning within digital twin framework to predict postoperative hemodynamics rapidly; directly supports T6's hypothesis that BC calibration enables prediction despite anatomical uncertainty, extended to intervention planning context.
- verdict: FULL
- revisit-if: (Already meets criteria; BC tuning methodology and reduced-order CFD+ ML coupling core to T6)

