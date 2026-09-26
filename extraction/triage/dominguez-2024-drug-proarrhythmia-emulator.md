---
source_pdf_path: Resources/s41746-024-01370-8.pdf
slug: dominguez-2024-drug-proarrhythmia-emulator
ledger_id: C041
ledger_status: TRIAGED
---

# dominguez-2024-drug-proarrhythmia-emulator

## Bibliographic
- Title: Fast and accurate prediction of drug induced proarrhythmic risk with sex specific cardiac emulators
- First author / authors (first 3 + et al.): Dominguez-Gomez P, Zingaro A, Baldo-Canut L, et al.
- Year: 2024
- Venue: npj Digital Medicine
- DOI: 10.1038/s41746-024-01370-8

## One-line claim
Develops sex-specific 3D cardiac electrophysiological emulators trained on 900 simulations to rapidly predict QT interval prolongation for drug safety assessment, demonstrating superior sensitivity of 3D models to abnormal electrical propagation compared to 0D single-cell models.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Domain is cardiac electrophysiology (QT interval prediction), not coronary lumen geometry or segmentation uncertainty. No mention of inter-observer disagreement or geometric variability quantification.
- **Q-B decision flip**: NOT REPORTED. No diagnostic threshold reclassification (e.g., FFR 0.80 cutoff) discussed. Study focuses on QT prolongation risk stratification, not revascularization decisions.
- **Q-C BC tuning**: NOT REPORTED. Outlet boundary conditions and their tuning are not addressed. Study uses 3D cardiac electrophysiology models, not coronary hemodynamics solvers.
- **Q-D fidelity / quantity**: 3D cardiac electrophysiological simulations using detailed biventricular geometries (male and female). Compares 3D vs. 0D electrical models. Computes ECG signals and QT intervals. NO WSS/OSI, no spatial hemodynamic fields; electrical propagation only.
- **Q-E data**: Training dataset: 900 electrophysiological simulations (450 male, 450 female). Proprietary to ELEM Biotech; NOT publicly available. No invasive FFR ground truth (study uses 0D ORd ion channel model as ground truth). Validation against benchmark drugs uses clinical plasma concentrations and published in vitro channel data.
- **Q-F meshing**: NOT REPORTED. No discussion of segmentation→surface→volume meshing workflows or robustness on poor/topologically complex geometry. Uses pre-defined anatomical geometries from literature for male and female hearts.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Cardiac electrophysiology digital-twin framework for drug safety; orthogonal to coronary CFD geometry sensitivity and FFR decision-flip analysis.
- verdict: LIGHT
- revisit-if: If extended to model coronary electrophysiology or arrhythmia substrate in atherosclerotic coronaries, intersecting T6's clinical domain.

## Ideation opening (CFD + imaging)
"The precise relationship between drug-induced ion channel blockade at the cellular level and QT prolongation at the organ level remains poorly understood" suggests a gap in bridging subcellular electrophysiology to whole-organ imaging phenotypes, but no direct opening for CFD + coronary imaging work is stated.
