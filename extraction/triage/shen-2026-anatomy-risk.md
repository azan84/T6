---
source_pdf_path: Resources/s11831-026-10530-w.pdf
slug: shen-2026-anatomy-risk
ledger_status: TRIAGED
---

# shen-2026-anatomy-risk

## Bibliographic
- Title: The Anatomy of Coronary Risk: How Arterial Geometry Shapes Coronary Artery Disease Through Blood Flow Haemodynamics – Latest Methods, Insights and Clinical Implications
- First author / authors: C. Shen, M. Zhang, H. Keramati et al.
- Year: 2026
- Venue: Archives of Computational Methods in Engineering
- DOI: 10.1007/s11831-026-10530-w

## One-line claim
Comprehensive review of how coronary arterial geometry (anatomy of risk) shapes local hemodynamics through CFD analysis; discusses imaging, segmentation methods, numerical approaches, and their clinical implications for CAD understanding.

## T6 targeted questions

- **Q-A geometry perturbation**: YES, addressed extensively. Review discusses segmentation as critical uncertainty source: "direct haemodynamic assessment is still limited, as any minor luminal boundary uncertainties can significantly affect the efficacy of the resulting analyses." Notes: "Imaging artifacts make it difficult to segment the images and detect the true lumen borders." Also mentions: "Improved (although not yet standardised) segmentation capacities have increased accessibility and streamlined subsequent in-depth computational blood flow analysis efforts." Discusses "Segmentation and 3D model reconstruction" as major step affecting accuracy. However, does NOT quantify inter-observer segmentation disagreement or provide magnitude of error from geometric perturbation.

- **Q-B decision flip**: Discusses FFR conceptually as clinical reference standard but does NOT report reclassification rates or threshold sensitivity.

- **Q-C BC tuning**: YES, discussed. States: "Lumped parameter (0 or 1-order) models can be used as boundary conditions...may be tuned via numerical optimization and sensitivity analysis." Also: "Including an intramyocardial pressure source to impede flow during systole and relax during diastole adjusts the coronary circulation phase." Extensive table (Table 1) reviews CFD methods and boundary conditions. Discusses outlet boundary conditions (resistance models, Windkessel, lumped parameter networks) across many studies. Does NOT explicitly state whether BC tuning is re-done after geometry changes or whether tuning masks/absorbs geometric error.

- **Q-D fidelity / quantity**: Comprehensive review of reduced-order (0D, 1D) and 3D CFD approaches. Extensively discusses WSS (wall shear stress), OSI (oscillatory shear index), TAESS (time-averaged ESS), RRT (relative residence time) as hemodynamic outputs. Reviews steady-state and pulsatile simulations. Discusses Newtonian vs. non-Newtonian blood models.

- **Q-E data**: Review paper with extensive tables (Table 7 spanning 8 pages) summarizing geometric features (tortuosity, bifurcation angle, curvature, diameter, stenosis) and their hemodynamic effects from numerous studies. References clinical cohorts from various invasive imaging studies (IVUS, OCT, ICA, CTCA).

- **Q-F meshing**: Dedicated discussion. States: "Robust fluid solvers have implemented various constitutive non-Newtonian blood simulations require longer computational time to stabilize and models...require finer boundary layers to resolve the flow." Discusses: "Quality control of the generated mesh is challenging and a crucial step." Notes: "Lower spatial resolution for coronary CTA is ~0.3 mm limiting their use to coronary arteries of 1.5 mm or greater in diameter." Also: "Imaging artifacts make it difficult to segment the images and detect the true lumen borders." Discusses adaptive mesh generation and mentions deep learning for segmentation automation.

## Novelty bearing on T6

- **bucket**: SUPPORT
- **one-line reason**: Comprehensive review of geometry-hemodynamics relationships, segmentation challenges, and CFD methodologies; provides foundational context for T6's hypothesis that geometric error interacts with CFD tuning, though does not explicitly test absorption or masking.
- **verdict**: LIGHT
- **revisit-if**: Paper includes quantitative analysis showing BC tuning compensates for geometric error, or reports inter-observer segmentation disagreement impact on FFR predictions.
