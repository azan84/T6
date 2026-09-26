---
source_pdf_path: Resources/s10439-026-04292-6.pdf
slug: choi-2026-pulsatile-ffr
ledger_status: TRIAGED
---

# choi-2026-pulsatile-ffr

## Bibliographic
- Title: Effects of Pulsatile Flow on Fractional Flow Reserve Assessed Using a Reduced-Order Model
- First author / authors: Wonjin Choi, Bon-Kwon Koo, Jung-Kyu Han et al.
- Year: 2026
- Venue: Annals of Biomedical Engineering
- DOI: 10.1007/s10439-026-04292-6

## One-line claim
Quantifies intrinsic variability of FFR under pulsatile physiological boundary condition uncertainty using a 1D reduced-order model coupled with lumped parameter networks and polynomial chaos expansion.

## T6 targeted questions

- **Q-A geometry perturbation**: Does NOT measure segmentation error or inter-observer disagreement. Focuses exclusively on physiological parameter uncertainty (myocardial compression, cardiac output, aortic resistance) via stochastic sampling. NOT REPORTED for geometric perturbation.

- **Q-B decision flip**: YES. Explicitly addresses FFR near clinical threshold 0.80. States: "FFR demonstrated high robustness under broad physiological uncertainty, including cases near clinically relevant decision thresholds" and "The limited variability observed near clinically relevant decision thresholds supports the reliability of cycle-averaged FFR as a functional index." Finds FFR threshold crossed between 70-80% area stenosis but variability near threshold remains limited (small std dev).

- **Q-C BC tuning**: CRITICAL. Uses Windkessel and lumped parameter networks for outlet boundary conditions. KEY FINDING: BC coefficients are calibrated from 3D simulations ONCE and then FIXED: "Once calibrated, ai, bi, and ci are fixed for each 1D segment and are not recalculated when the boundary conditions are changed. During the 1D ROM simulation, the instantaneous flow rate and pressure are computed by solving Eq. 3 using these fixed coefficients. Therefore, the calibrated ROM can be reused across different boundary conditions without re-solving the underlying 3D problem." This means BC tuning is NOT re-done after geometry changes—coefficients remain fixed. Does NOT claim tuning compensates for geometric error.

- **Q-D fidelity / quantity**: Reduced-order modeling (1D ROM) calibrated from 3D simulations with polynomial chaos expansion for uncertainty quantification. Does NOT report WSS or OSI; focus is on FFR and pressure-flow relationships. States: "The computational efficiency of the ROM enables large-scale stochastic analyses that would be infeasible with higher-fidelity models alone."

- **Q-E data**: Synthetic patient-specific geometries (idealized cylindrical stenoses 40–90% area stenosis; subject-specific coronary arteries from healthy subject with synthetic stenoses introduced). No invasive FFR ground truth; uses published clinical FFR ranges for validation only.

- **Q-F meshing**: Centerline extraction mentioned ("extracting the vascular centerline from the 3D geometry") and hierarchical discretization described. No detail on segmentation robustness to poor or topologically incorrect geometry.

## Novelty bearing on T6

- **bucket**: SUPPORT
- **one-line reason**: Demonstrates FFR remains robust near 0.80 threshold despite broad physiological uncertainty; supports T6's premise that decision thresholds are stable, though addresses physiological not geometric uncertainty.
- **verdict**: LIGHT
- **revisit-if**: Paper addresses BC tuning or reports sensitivity of FFR to anatomical/segmentation uncertainty rather than just physiological parameters.
