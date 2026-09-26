---
source_pdf_path: Resources/s00366-026-02359-5.pdf
slug: zhang-2026-guide-wire-cfd
ledger_status: TRIAGED
---

# zhang-2026-guide-wire-cfd

## Bibliographic
- Title: A systematic computational study on the impact of pressure guide wires in virtual fractional flow reserve assessment
- First author / authors (first 3 + et al.): Jiyang Zhang, Haizhou Yang, Brahmajee K. Nallamothu et al.
- Year: 2026
- Venue: Engineering with Computers
- DOI: 10.1007/s00366-026-02359-5

## One-line claim
Multi-scale CFD (3D-0D Windkessel coupling) reveals that pressure guide wires significantly reduce FFR, particularly in severe stenoses, and that microvascular resistance modulates wire effects.

## T6 targeted questions
- **Q-A geometry perturbation**: Studied (wire placement effects as perturbation to hemodynamics). Not segmentation error; perturbation is wire artifact, not synthetic error injection.
- **Q-B decision flip**: FFR ≤0.8 threshold discussed as clinical criterion. No reclassification rates, but emphasis on "intermediate stenosis (FFR values between 0.75 and 0.85), where precise differentiation is critical for clinical decision-making."
- **Q-C BC tuning**: Extensive use of lumped parameter models (LPMs) as boundary conditions: "three types of LPMs coupled to different boundaries of the 3D geometries: (1) an aortic model represented by a three-element Windkessel model... (2) a left heart model describing ventricular pumping dynamics... (3) coronary models coupled to the outlets." No evidence of BC re-tuning after geometry change (wire insertion) to compensate for or absorb error. Rather, different wire configurations are simulated with fixed BC parameters.
- **Q-D fidelity / quantity**: Multi-scale 3D-0D CFD using CRIMSON. Navier-Stokes in 3D epicardials, lumped Windkessel at outlets. No WSS/OSI reported; focus on FFR and CFR only.
- **Q-E data**: One patient-specific model (64-year-old female, suspected microvascular disease) with systematic parametric variations (stenosis severity, location, morphology, microvascular resistance).
- **Q-F meshing**: Patient geometry segmented from imaging; wire and catheter added by Boolean subtraction (explicit geometry, not volumetric mesh detail provided).

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates multi-scale CFD methodology and wire-geometry interaction; does not address topological segmentation error, BC re-tuning to mask error, or how BCs absorb geometric changes.
- verdict: LIGHT
- revisit-if: Study includes comparison of FFR under correct vs. topologically incorrect segmentation (e.g., missing branch), with BC held constant vs. re-tuned.

