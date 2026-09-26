---
source_pdf_path: Resources/ssrn-6314078.pdf
slug: shibah-2024-tetra-shield-atherosclerosis
ledger_id: C042
ledger_status: TRIAGED
---

# shibah-2024-tetra-shield-atherosclerosis

## Bibliographic
- Title: Multiscale Credible Systems Framework for the Tetra-Shield Protocol: Integrating ASME V&V 40 Standards for Arterial Rehabilitation and Prevention of Cardiovascular Events
- First author / authors (first 3 + et al.): Shibah SRM
- Year: 2024 (SSRN preprint)
- Venue: SSRN (preprint/independent)
- DOI: NOT REPORTED

## One-line claim
Proposes a computational proof-of-concept combining four pillars (neuromuscular modulation, nanotherapy, hemodynamic optimization, AI biosensing) to address atherosclerosis through mathematically closed-form models verified against numerical solvers and cross-validated with multi-method sensitivity analysis per ASME V&V 40 standards.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Pillar 2 (targeted nanotherapy) models plaque fibrous cap thickness evolution (asymptotic 1.5 mm, 1.132 mm at day 10), but no coronary lumen segmentation uncertainty or inter-observer disagreement. Framework is conceptual; no measured geometric variability.
- **Q-B decision flip**: NOT REPORTED. No diagnostic threshold (e.g., FFR 0.80) or reclassification rate. Pillar 4 classifier reports AUC 0.819 (95% CI [0.758, 0.870]) for synthetic risk categorization, but no clinical decision-flip metrics.
- **Q-C BC tuning**: Pillar 3 (hemodynamic optimization) uses Poiseuille's law with wall shear stress computed algebraically (τ = 3.183 Pa at nominal r = 2 mm). No outlet BC tuning described; no Windkessel, resistance optimization, or statement that BC compensates for geometric/anatomical error. BC is implicit in the lumped-parameter formulation.
- **Q-D fidelity / quantity**: Pillar 3 is 0D algebraic hemodynamics (lumped-parameter wall shear stress model), not 3D CFD. Includes physics-informed neural network (PINN) cross-validation using reduced-order steady Hagen–Poiseuille 1D solution (PINN reproduces Pillar 3 formula to 1.3 × 10−12 % relative error), but this is NOT 3D patient-specific hemodynamics. NO WSS/OSI spatial fields or 3D CFD sensitivity analysis.
- **Q-E data**: Entirely synthetic/computational. Monte Carlo uncertainty quantification N = 10,000; Sobol sampling n = 1024; parameters calibrated to literature ranges (Table 1, physiological ranges). NO clinical cohort, NO invasive FFR ground truth. Author states: "All outcomes are computational. Parameter distributions are assumed uniform for computational convenience."
- **Q-F meshing**: NOT REPORTED. No segmentation→surface→volume meshing workflow discussed. Framework uses simplified first-order ODE models and analytic expressions; Pillar 3's PINN solves reduced-order steady Hagen–Poiseuille problem, not patient-specific 3D mesh construction.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Conceptual multiscale atherosclerosis model using simplified hemodynamics (0D algebraic) and synthetic data; no coronary geometry perturbation analysis, FFR decision-flip quantification, or 3D CFD integration.
- verdict: LIGHT
- revisit-if: If Pillar 3 extended to 3D coronary CFD with patient-specific segmentation meshes and quantified geometry sensitivity, could become METHOD; if Pillar 2 combined with coronary imaging and FFR to model plaque-induced stenosis, could become SUPPORT.

## Ideation opening (CFD + imaging)
"All outcomes are computational... model behavior under defined assumptions and do not constitute clinical predictions" and Pillar 2's evolution of plaque cap thickness suggests a gap in coupling simplified plaque mechanics to patient-specific coronary imaging and 3D hemodynamic models—a potential avenue for CFD-imaging integration to predict lesion progression and flow effects.
