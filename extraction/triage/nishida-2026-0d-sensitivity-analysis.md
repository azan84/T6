---
source_pdf_path: Resources/2601.00027v1.pdf
slug: nishida-2026-0d-sensitivity-analysis
ledger_id: C016
ledger_status: TRIAGED
---

# nishida-2026-0d-sensitivity-analysis

## Bibliographic
- Title: Zero-Dimensional Cardiovascular Modeling: A Personalized Approach to Non-Invasive Measurement and Sensitivity Analysis
- First author / authors: Akio Nishida, Bhagyashree, Jiacheng Liu
- Year: 2026 (MSc project report)
- Venue: University of Sheffield, Department of Computer Science (MSc Data Analytics)
- DOI: NOT REPORTED

## One-line claim
MSc project investigating parameter sensitivity in lumped-parameter cardiovascular models (single-ventricle and four-chamber configurations) using Sobol and Morris methods to identify key physiological parameters (venous return, contractility, resistance, compliance) affecting hemodynamic outputs, with emphasis on non-invasive measurement feasibility.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Study focuses on model parameter sensitivity (R, L, C, E values) in fixed model topology; does not address vascular geometry variability or segmentation uncertainty.
- **Q-B decision flip**: NOT REPORTED. No diagnostic thresholds or reclassification analysis; outputs are pressure, volume, flow waveforms and sensitivity indices.
- **Q-C BC tuning**: PARTIALLY RELEVANT. Paper develops Windkessel-type 0-D models with systemic and pulmonary arterial/venous compartments (R, C, L, E elements). Performs sensitivity analysis to identify which boundary condition parameters (resistances, compliances) most affect ventricular pressures and flows. Text: "Sobol Method Result of Model 1: certain parameters, notably minimal ventricular contractility (Emin) and systemic arterial compliance (Csa), had a substantial influence on the model's outputs." However, no discussion of BC tuning protocols, optimization to patient data, or re-tuning after geometry change.
- **Q-D fidelity / quantity**: 0-D lumped-parameter model only (Windkessel circuits with time-varying elastance). Three model variants explored (single-ventricle, four-chamber, simplified four-chamber). No 3D CFD, no spatially resolved hemodynamic fields (WSS, OSI). Outputs: ventricular/atrial pressures and volumes, arterial pressures, flow rates.
- **Q-E data**: Proof-of-concept modeling study (no patient cohort). Paper includes "non-invasive measurements" comparison: model outputs (e.g., systemic artery pressure) are validated against feasibility of non-invasive clinical measurement (e.g., cuff BP). No invasive FFR or catheter-based ground truth.
- **Q-F meshing**: NOT APPLICABLE. Zero-dimensional lumped model; no geometry, segmentation, or meshing involved.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Applies global sensitivity analysis (Sobol, Morris methods) to characterize parameter influence on 0-D lumped cardiovascular model outputs; relevant to T6's hypothesis that BC parameter uncertainty affects downstream clinical predictions (FFR, diagnostic metrics).
- verdict: LIGHT
- revisit-if: If paper includes uncertainty propagation from parameter ranges to model predictions, or validation against patient-specific clinical measurements, or analysis of how parameter identifiability changes when geometric (anatomical) constraints are imposed.

## Ideation opening (CFD + imaging)
- Paper states: "Zero-dimensional cardiovascular models provide a computationally efficient framework for studying global hemodynamic behavior, yet the influence of model complexity on parameter sensitivity remains insufficiently understood" and notes: "Even parameters deemed unimportant or reliable by the sensitivity analysis might still impact the model's overall performance in certain contexts, particularly when specific parameters are implicitly interconnected." Implies research gap: How do segmentation errors (geometry uncertainty) cascade through parameter identification in 0-D models? Can we use sensitivity analysis to identify BC parameters that are robust vs. fragile to geometric perturbations?
