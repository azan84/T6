---
source_pdf_path: Resources/v1_covered.pdf
slug: yang-2022-coronary-hemodynamics-fsi
ledger_status: TRIAGED
---

# yang-2022-coronary-hemodynamics-fsi

## Bibliographic
- Title: Coronary Hemodynamic Simulation Study
- First author / authors (first 3 + et al.): Fengyuan Yang, Zhenlei Chen, Rongyue Zheng et al.
- Year: 2022
- Venue: Research Square (preprint)
- DOI: 10.21203/rs.3.rs-2295747/v1

## One-line claim
Two-way fluid-structure interaction model with non-Newtonian blood properties and elastic vessel wall predicts coronary hemodynamics and functional parameters (FFR, pressure, WSS) matching invasive FFR measurements.

## T6 targeted questions
- **Q-A geometry perturbation**: Patient-specific geometry from dynamic coronary angiography; not a synthetic perturbation study. Single patient case with typical stenosis.
- **Q-B decision flip**: FFR threshold 0.80; measured invasive FFR data used to fit pressure-time boundary condition function; simulated vs measured error <10%, mean 6.74%.
- **Q-C BC tuning**: "Pressure-time function curve is fitted to ensure the accuracy of the boundary conditions" using measured FFR hyperemia plateau data; error reduced from 40% to 10% by using pressure-time function vs fixed pressure. Quote: "This method can effectively reduce the error." Elasticity of vessel wall and plaque explicitly considered in FSI model.
- **Q-D fidelity / quantity**: Two-way FSI model (FLUENT); reports blood flow, pressure contour, wall shear stress (WSS) contour at multiple time points in cardiac cycle; non-Newtonian fluid properties.
- **Q-E data**: Single patient with CCTA and invasive FFR measurement; benchmark against measured contrast velocity from angiography.
- **Q-F meshing**: 3D reconstruction from angiography; mentions region-growth method to extract vessel contours but notes this "loses some geometric information and is not very accurate"; discusses difficulty of geometric reconstruction for individual cases.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates FSI modeling with patient-specific boundary conditions derived from invasive FFR; shows pressure-time function boundary conditions improve accuracy; relevant for realistic hemodynamic simulation accounting for vessel elasticity.
- verdict: FULL
- revisit-if: Examine whether FSI BC tuning must be re-done when segmentation geometry is altered; check sensitivity to topologically incorrect geometry.
