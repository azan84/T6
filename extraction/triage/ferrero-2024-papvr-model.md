---
source_pdf_path: Resources/ivae175.pdf
slug: ferrero-2024-papvr-model
ledger_id: C032
ledger_status: TRIAGED
---

# ferrero-2024-papvr-model

## Bibliographic
- Title: Appraisal of partial anomalous pulmonary venous drainage through a lumped-parameter mathematical model: a new pathophysiological proof of concept
- First author / authors (first 3 + et al.): Ferrero P, Tonini A, Valenti G
- Year: 2024
- Venue: Interdisciplinary CardioVascular and Thoracic Surgery
- DOI: 10.1093/icvts/ivae175

## One-line claim
A zero-dimensional lumped-parameter model of the cardiovascular system demonstrates that anatomic site of anomalous pulmonary venous drainage modulates the Qp/Qs (pulmonary-to-systemic flow) ratio independently of the number of anomalous veins, validated on 49 patients with invasive catheterization and cardiac MR.

## T6 targeted questions
- **Q-A geometry perturbation**: No mention of geometry perturbation, segmentation uncertainty, or measurement disagreement in vessel dimensions. Paper focuses on anatomic classification (RA type vs. VC type) but not quantitative geometry variation or sensitivity analysis. NOT REPORTED.
- **Q-B decision flip**: Paper addresses clinical decision-making for repair indication based on Qp/Qs threshold ("Indication to repair is mainly based on... ratio between pulmonary and systemic flow (Qp/Qs) assessment"). However, no analysis of how geometry uncertainty affects Qp/Qs predictions or decision reclassification; no FFR threshold; different clinical context (congenital heart disease, not coronary stenosis). NOT REPORTED for geometry sensitivity.
- **Q-C BC tuning**: 0D Windkessel circuits model systemic and pulmonary circulations with resistances and compliances. Model parameters based on literature and patient data (cardiac catheterization, CMR). No discussion of BC tuning after geometry change or parameter sensitivity to anatomic variation. NOT REPORTED.
- **Q-D fidelity / quantity**: Reduced-order model only: 0D lumped-parameter model with time-varying elastances for chambers and Windkessel circuits for circulation. No 3D CFD, no spatially-resolved flow fields, no WSS/OSI.
- **Q-E data**: Clinical validation on 49 adult patients with PAPVR (55% female). Data from invasive cardiac catheterization (saturation run) and cardiac magnetic resonance (CMR) with phase-contrast flow quantification. Public or private: institutional center data (IRCCS-Policlinico San Donato). No FFR ground truth.
- **Q-F meshing**: 0D model; no 3D segmentation or mesh generation. Anatomic classification by vessel location but no segmentation-based geometry variation or meshing robustness assessment.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Demonstrates clinical use of 0D hemodynamic models for diagnosis and decision-making in congenital heart disease with threshold-based clinical criteria, but focuses on pulmonary hemodynamics (Qp/Qs), not coronary FFR-CT or imaging-based geometry uncertainty.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity analysis showing how plausible variations in vessel anatomy or size affect Qp/Qs predictions, or demonstrates impact of segmentation-based geometry variation on clinical decision outcomes.

## Ideation opening (CFD + imaging)
Paper notes that "among patients with the same number of lung segments draining anomalously, a great variability is observed in terms of right ventricular overload," implying that anatomic detail beyond simple counts matters for hemodynamic predictions. Suggests that patient-specific geometric characteristics and measurement precision may modulate hemodynamic parameters beyond classical classifications, but paper does not quantify measurement uncertainty.
