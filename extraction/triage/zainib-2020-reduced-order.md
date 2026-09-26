---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2020 - Zainib - Reduced order methods for parametric optimal flow control in coronary bypass.pdf
slug: zainib-2020-reduced-order
ledger_status: TRIAGED
---

# zainib-2020-reduced-order

## Bibliographic
- Title: Reduced order methods for parametric optimal flow control in coronary bypass grafts, toward patient-specific data assimilation
- First author / authors (first 3): Zakia Zainib, Francesco Ballarin, Gianluigi Rozza
- Year: 2020
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3367

## One-line claim
An optimal flow control framework combined with reduced-order modeling (POD-Galerkin) automatically tunes outlet boundary condition parameters in patient-specific coronary artery bypass graft models to match known physiological data, solving the challenge of hard-to-quantify BC personalization.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb or study segmentation error. Uses patient-specific CABG geometries reconstructed from clinical CT scans (post-surgery); geometry treated as deterministic.
- **Q-B decision flip**: NOT focus. Paper addresses CABG hemodynamics and BC tuning, not FFR ≤0.80 decision classification on native coronaries.
- **Q-C BC tuning**: **CENTRAL FOCUS**. Paper explicitly states: "Accuracy of boundary conditions is vital...lack of availability of patient-specific outflow waveforms...makes it harder to prescribe outflow boundary conditions." Proposes "optimal flow control" framework where unknown BC parameters (resistances at outlets) are treated as control variables and optimized by minimizing mismatch between simulated and target (patient-specific measured) flow/pressure. Uses both analytical and data-driven targets. Quote: "the unknown control variables...one can solve for problem-specific boundary conditions while matching known data in least-square sense." BCs automatically tuned for each patient; POD-Galerkin reduces cost from "days to seconds" for parametric studies. Three bypass grafts on real CABG cases demonstrated.
- **Q-D fidelity / quantity**: 3D CFD coupled with 0D optimal control over parametrized domain (patient-specific geometry parameterized by anatomical features). Navier-Stokes equations solved via finite element method (FEniCS/multiphenics). Output-driven optimization; hemodynamic quantities of interest include pressure, flow, velocity fields.
- **Q-E data**: Real clinical cases from Sunnybrook Health Sciences Centre (Toronto, Canada). Triple CABG surgery example detailed with post-operative CT imaging. Patient-specific data used to constrain optimization. Private institutional data.
- **Q-F meshing**: Level set segmentation and marching cube algorithm for surface reconstruction from CT; centerline-based smoothing (VMTK) to generate regular geometries. Focus on geometric personalization NOT segmentation robustness analysis.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Presents automated optimal control framework for BC parameter estimation in patient-specific coronary hemodynamics; directly addresses the challenge of BC tuning from patient data using reduced-order methods for computational efficiency.
- verdict: FULL
- revisit-if: Already directly relevant; demonstrates BC-tuning methodology on real patient cases.

