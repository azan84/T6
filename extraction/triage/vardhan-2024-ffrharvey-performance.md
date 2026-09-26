---
source_pdf_path: Resources/vardhan-et-al-2024-diagnostic-performance-of-coronary-angiography-derived-computational-fractional-flow-reserve.pdf
slug: vardhan-2024-ffrharvey-performance
ledger_status: TRIAGED
---

# vardhan-2024-ffrharvey-performance

## Bibliographic
- Title: Diagnostic Performance of Coronary Angiography Derived Computational Fractional Flow Reserve
- First author / authors (first 3 + et al.): Madhurima Vardhan, Cyrus Tanade, S. James Chen et al.
- Year: 2024
- Venue: Journal of the American Heart Association
- DOI: 10.1161/JAHA.123.029941

## One-line claim
FFRHARVEY, a high-resolution angiography-derived CFD solver using lattice Boltzmann methods, computes FFR and intravascular hemodynamic phenomarkers (WSS, longitudinal vorticity, velocity) with diagnostic accuracy comparable to invasive FFR and identifies high-risk unrevascularized gray-zone cases.

## T6 targeted questions
- **Q-A geometry perturbation**: Patient-specific 3D coronary geometries reconstructed from angiography pairs (≥45 degree separation); no synthetic perturbation. Reconstruction validated by interventional cardiologist for anatomical validity.
- **Q-B decision flip**: FFR ≤0.80 threshold for revascularization; FFRHARVEY vs invasive FFR: AUC 0.91, PPV 90.2%, NPV 89.6%, sensitivity 79.3%, specificity 95.4%; percentage discrepancy 6.63%. Gray-zone defined as 0.75–0.85 FFR; study focused on unrevascularized gray-zone (UGZ) cases 0.80–0.85 with MACE prediction.
- **Q-C BC tuning**: "CFD framework had the flexibility to parameterize inlet and outlet boundary conditions to resting or hyperemic state"; clinical measurements (coronary velocity, heart rate, hematocrit, resistance) used as inputs; robustness check: ±10%, ±20%, ±30% changes in parameters yield <2% impact on computed FFR. No explicit re-tuning after geometry change; focuses on "accurate 3D reconstruction" and "accurate determination of distal location."
- **Q-D fidelity / quantity**: Ultra-high-resolution 3D CFD (HARVEY lattice Boltzmann method); full coronary tree with up to second/third generation side branches; reports velocity, WSS, and longitudinal vorticity as biomarkers; identified longitudinal vorticity as predictor of MACE in UGZ.
- **Q-E data**: Retrospective, 2-center, blinded cohort; 160 patients with 166 lesions; CA + invasive FFR with adenosine; follow-up 3 years; invasive FFR ≤0.80 abnormal, >0.80 normal.
- **Q-F meshing**: 3D model reconstruction from angiography using 4-step algorithm (vessel identification, feature extraction, transformation matrix, 3D tree calculation); no explicit mesh details provided for CFD domain; validated against expert interventional cardiologist analysis.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: High-fidelity ultra-high-resolution 3D CFD (lattice Boltzmann) recovers complex intracoronary hemodynamics; demonstrates that complete coronary tree models (full side branches) improve accuracy vs simplified 1D/2D models; identifies novel hemodynamic biomarkers (longitudinal vorticity) for risk stratification in ambiguous cases.
- verdict: FULL
- revisit-if: Check whether CFD parameters require re-tuning when vessel geometry is topologically altered; examine sensitivity to segmentation errors in side branch anatomy; validate approach on intentionally perturbed geometries.
