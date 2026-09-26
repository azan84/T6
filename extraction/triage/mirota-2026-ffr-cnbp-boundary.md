---
source_pdf_path: Resources/1-s2.0-S0169260726002038-main.pdf
slug: mirota-2026-ffr-cnbp-boundary
ledger_status: TRIAGED
---

# mirota-2026-ffr-cnbp-boundary

## Bibliographic
- Title: Patient-specific continuous non-invasive blood pressure waveform in computed tomography derived fractional flow reserve calculation: Comparison with population-based pressure models
- First author / authors (first 3 + et al.): Kryspin Mirota, Joanna Wicher-Żółtaniecka, Mateusz Rzycki, et al.
- Year: 2026
- Venue: Computer Methods and Programs in Biomedicine 284 (2026) 109449
- DOI: 10.1016/j.cmpb.2026.109449

## One-line claim
Presents Cardiolens FFR-CT Pro method integrating patient-specific continuous non-invasive blood pressure (CNBP) waveforms as boundary conditions for CFD to improve FFR-CT diagnostic accuracy vs. population-based pressure models.

## T6 targeted questions

- **Q-A geometry perturbation**: Does NOT perturb segmentation. Compares patient-specific vs. population-based boundary conditions on same segmented geometry.

- **Q-B decision flip**: YES. Reports FFR threshold 0.80 and diagnostic accuracy: "Cardiolens FFR-CT Pro® demonstrated higher accuracy (88.6%), specificity (87.4%) and sensitivity (92.5%) than population based pressure input FFR-CT accuracy (87.3%), specificity (87.3%) and sensitivity (87.5%)." Gray zone mentioned: "current methods may demonstrate reduced accuracy when evaluating lesions that fall within the gray-zone range."

- **Q-C BC tuning**: **CRITICAL YES**. "The aim of this study is to investigate how pressure morphology affects FFR-CT calculations by comparing the use of patient-specific pressure waveforms versus using systolic and diastolic blood pressure values only, obtained from population based formulas." Key finding: "Incorporating patient-specific pressure waveform morphology into boundary conditions improves diagnostic performance compared with population-based formulas alone." This directly addresses boundary condition tuning and its effect on FFR-CT accuracy.

- **Q-D fidelity / quantity**: Uses CFD-based FFR-CT with hemodynamic calculation. Does NOT report WSS, OSI, or spatially-resolved flow fields. Focus is on outlet pressure boundary condition specification.

- **Q-E data**: 132 patients (167 vessels), prospective multi-center (11 centers), invasive FFR ground truth (yes). Cohort: chronic coronary syndrome, CCTA with ≥50% stenosis in major epicardial vessel.

- **Q-F meshing**: Mentions segmentation but no detail on meshing or robustness on poor geometry. Focus is on boundary condition specification, not segmentation quality.

## Novelty bearing on T6

- bucket: SUPPORT
- one-line reason: Directly demonstrates that boundary condition tuning (patient-specific pressure waveforms vs. population formulas) improves FFR-CT diagnostic accuracy, providing clinical evidence supporting T6's hypothesis that BC tuning can enhance prediction robustness.
- verdict: FULL
- revisit-if: Already high priority; analyzes interaction between segmentation uncertainty and BC tuning strategy.
