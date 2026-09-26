---
source_pdf_path: Resources/On inlet pressure boundary conditions for CT-based computation of fractional flow reserve  clinical measurement of aortic pressure.pdf
slug: liu-2023-inlet-pressure-ffr
ledger_status: TRIAGED
---

# liu-2023-inlet-pressure-ffr

## Bibliographic
- Title: On inlet pressure boundary conditions for CT-based computation of fractional flow reserve: clinical measurement of aortic pressure
- First author / authors (first 3 + et al.): Jincheng Liu, Suqin Huang, Xue Wang, et al.
- Year: 2023
- Venue: Computer Methods in Biomechanics and Biomedical Engineering
- DOI: 10.1080/10255842.2022.2072172

## One-line claim
Inlet aortic pressure boundary conditions (clinically measured vs. physiological-formula-derived) have minimal impact on steady-state FFR-CT (correlation r=0.99 despite 15 mmHg difference), but outlet resistance variation (24–72% vasodilation) significantly alters predicted FFR.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No segmentation uncertainty studied; patient-specific CT geometries analyzed as-is.
- **Q-B decision flip**: YES, FFR 0.80 threshold relevant. FFR crosses 0.80 cutoff for revascularization decision; study compares proximal and distal boundary effects on crossing this threshold.
- **Q-C BC tuning**: Inlet: two approaches tested: (1) clinically measured aortic pressure, (2) physiological mean pressure formula. Outlets: three-element Windkessel with variable microcirculation resistance (RCR model); outlet resistance changed to simulate different coronary vasodilation responses (24%, 48%, 72%). "The microcirculation resistance of the outlet gradually rose as the vasodilation state changed, and the computed FFR increased." Finding: distal BC (outlet resistance) far more sensitive than inlet BC to FFR prediction.
- **Q-D fidelity / quantity**: 3D steady-state CFD coupled to 0D lumped models at outlets. Pressure fields computed; NO WSS/OSI reported.
- **Q-E data**: 15 patients with CAD, invasive FFR measured at catheterization (ground truth present). Real aortic pressure waveforms recorded.
- **Q-F meshing**: 3D reconstruction via Mimics software; segmented vessels >1 mm diameter included; no segmentation robustness detail.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Sensitivity analysis of inlet vs. outlet BCs for FFR-CT; shows outlet resistance tuning dominates, supporting T6's premise that BC parameter choice critically affects output. Demonstrates that CFD BC tuning (not just geometry) is source of variability.
- verdict: LIGHT
- revisit-if: Extends to quantify joint effect of geometry uncertainty + BC tuning on FFR near 0.80 threshold.
