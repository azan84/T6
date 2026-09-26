---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2022 - Piccioli - The effect of cardiac properties on arterial pulse waves  An in‐silico study.pdf
slug: piccioli-2022-cardiac-pulse-waves
ledger_id: C025
ledger_status: TRIAGED
---

# piccioli-2022-cardiac-pulse-waves

## Bibliographic
- Title: The effect of cardiac properties on arterial pulse waves: An in-silico study
- First author / authors (first 3 + et al.): Piccioli F, Valiani A, Alastruey J
- Year: 2022
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3658

## One-line claim
A 1D arterial network model coupled to a 0D cardiac contraction model investigates how variability in cardiac properties (contractility, stroke volume, valve function) affects central and peripheral pulse wave morphology and PPG signals.

## T6 targeted questions
- **Q-A geometry perturbation**: Not applicable. Study focuses on cardiac parameter variation (contractility, stroke volume, valve parameters), not lumen geometry perturbation. NOT REPORTED.
- **Q-B decision flip**: No FFR computation, no diagnostic threshold evaluation, no reclassification analysis. NOT REPORTED.
- **Q-C BC tuning**: RCR Windkessel model employed at terminal vessels as outlet boundary condition: "RCR Windkessel model was employed at the terminal vessels as outlet boundary condition (BC), to describe the resistance and compliance of peripheral vascular beds." No statement on re-tuning after geometry change or whether tuning compensates for anatomical error. NOT REPORTED.
- **Q-D fidelity / quantity**: Reduced-order model only: 1D arterial network (116 arterial segments) coupled with 0D cardiac model. No 3D CFD, no WSS/OSI. Outputs are pulse waveforms and PPG signals. No report of WSS sensitivity to geometry or cardiac parameter variation.
- **Q-E data**: In-silico study using computational models. Virtual subjects with haemodynamic variables spanning physiological range. No real patient cohort, no invasive FFR ground truth, no clinical data. Model parameters from literature (Mynard et al. reference values).
- **Q-F meshing**: 1D arterial segments modelled as "thin viscoelastic tubes of linearly tapered diameter". No 3D segmentation→surface→volume meshing, no discussion of topological correctness, no robustness on poor geometry.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Establishes hemodynamic modeling methods (1D/0D coupling, Windkessel BC, cardiac property parametrization) but does not address geometry uncertainty or its effect on clinical decision thresholds.
- verdict: LIGHT
- revisit-if: If paper contains detailed Windkessel tuning protocols or demonstrates BC tuning sensitivity to model assumptions.

## Ideation opening (CFD + imaging)
None stated. Paper addresses cardiac hemodynamics from properties (contractility, valve function) perspective, not imaging-derived geometry uncertainty or CFD model sensitivity.
