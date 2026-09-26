---
source_pdf_path: Resources/wardhana-et-al-2025-modeling-age-and-sex-variations-of-arterial-pressure-and-cardiac-hemodynamics-in-a-virtual.pdf
slug: wardhana-2025-age-sex-cardiovascular-virtual
ledger_id: C043
ledger_status: TRIAGED
---

# wardhana-2025-age-sex-cardiovascular-virtual

## Bibliographic
- Title: Modeling age and sex variations of arterial pressure and cardiac hemodynamics in a virtual population using a 0D-1D cardiovascular simulator
- First author / authors (first 3 + et al.): Wardhana G, van Loon LM, Potters J-W, et al.
- Year: 2025
- Venue: American Journal of Physiology - Heart and Circulatory Physiology
- DOI: 10.1152/ajpheart.00387.2025

## One-line claim
Develops a 0D-1D cardiovascular model coupling left ventricle elastance with a 55-artery network to generate a virtual population (972 initial, 327 final: 147 males, 180 females) spanning ages 25–75 yr, validated against prospective clinical measurements to capture age- and sex-related hemodynamic and arterial pressure variability.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No coronary lumen segmentation uncertainty or inter-observer/inter-segmenter disagreement quantified. Study uses predefined 55-artery network from literature (Liang et al., 2017) with no discussion of geometric variability or measurement error.
- **Q-B decision flip**: NOT REPORTED. No diagnostic threshold (e.g., FFR 0.80) or decision reclassification. Study focuses on systemic hemodynamics (systolic/diastolic/pulse pressure), not coronary stenosis classification.
- **Q-C BC tuning**: Outlet boundary conditions implemented as three-element Windkessel (R1, R2, Cc) applied at each terminal branch; no explicit tuning protocol described. NO statement that BC tuning is re-done after geometry change or that BC compensates for anatomical error. BC parameters derived from physiological ranges and varied with age/sex as input distributions.
- **Q-D fidelity / quantity**: 0D-1D mixed model: left ventricle elastance (0D time-varying elastance) coupled to 1D arterial network (55 large arteries via Navier–Stokes-derived conservation equations) with 0D Windkessel at terminals. Outputs: blood pressure (P), flow (Q), velocity (u), wave speed (c), vessel area (A). NO WSS/OSI spatial fields; NO 3D CFD. No sensitivity analysis of hemodynamics to geometry perturbations reported.
- **Q-E data**: Virtual population: 972 simulations generated (after parameter sampling: LOWER/MIDDLE/UPPER combinations), 327 retained after six acceptance criteria. N = 147 males, 180 females, ages 25–75 yr. Validated against prospective observational study: 63 healthy subjects (30M, 19F, ages 21–77 yr). NO invasive FFR ground truth. Data from clinical measurements (blood pressure) and literature (cardiovascular parameters); not publicly available (confidentiality with Sonion Nederland B.V.).
- **Q-F meshing**: NOT REPORTED. No segmentation→surface→volume meshing workflow. Uses predefined arterial tree geometry from Liang et al. (2017), representing 55 large arteries with simplified vessel models (linearly elastic, compliant walls, circular cross-section). No discussion of segmentation robustness or topologically incorrect geometry handling.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Systemic circulation 0D-1D hemodynamics with virtual population methodology; orthogonal to coronary-specific geometry uncertainty, FFR decision-flip analysis, and 3D coronary CFD.
- verdict: LIGHT
- revisit-if: If coronary arteries isolated and modeled with explicit geometry perturbation (simulating segmentation uncertainty), or if FFR-based diagnostic decision analysis integrated, or if 0D-1D coupled to 3D coronary CFD for subject-specific simulations, could become METHOD or SUPPORT.

## Ideation opening (CFD + imaging)
Study notes "sex remains underrepresented despite its significant influence on cardiovascular physiology" and proposes 0D-1D models for "supporting the development and testing of new monitoring tools and medical therapies," suggesting an opportunity to incorporate coronary-specific imaging and CFD with sex-stratified geometry models to predict hemodynamic outcomes and support FFR-CT or device design applications.
