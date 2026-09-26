---
source_pdf_path: Resources/1-s2.0-S0010482524000519-main.pdf
slug: liu-2024-ffr-deep-learning
ledger_id: C002
ledger_status: TRIAGED
---

# liu-2024-ffr-deep-learning

## Bibliographic
- Title: A comprehensive approach to prediction of fractional flow reserve from deep-learning-augmented model
- First author / authors: Jincheng Liu, Bao Li, Yang Yang
- Year: 2024
- Venue: Computers in Biology and Medicine, vol. 169
- DOI: 10.1016/j.compbiomed.2024.107967

## One-line claim
A cascade neural network (DP-NN) integrating data-driven geometry and physics-based coronary microcirculatory resistance predicts FFR from CCTA with 85.71% diagnostic accuracy and 3000× speedup over CFD-FFRCT.

## T6 targeted questions
- **Q-A geometry perturbation**: SYNTHETIC. Synthetic training dataset generated with varied coronary artery geometric parameters (diameter reduction 15–90%, minimum stenosis area 0.79–28.26 mm², etc.), guided by clinical experts referencing morphology literature. No measurement of inter-observer or inter-segmenter disagreement; inter-observer variability not reported.
- **Q-B decision flip**: FFR threshold 0.80 used. Paper states "FFR≤0.8 is classified as ischemic, while FFR>0.8 is classified as non-ischemic." Diagnostic accuracy reported: 85.71% (DP-NN) vs. 88.3% (FFRCT) in 77 patients with invasive FFR ground truth. Specific reclassification/flip rate NOT QUANTIFIED.
- **Q-C BC tuning**: Outlet BC uses coronary microcirculatory resistance (CMR) estimated via allometric scaling laws (Murray's law, Itu law, Huo–Kassab law). Flow distributed per vessel diameter. Hyperaemic state simulated by "decreasing the total resistance at each coronary outlet." Re-tuning of BC after geometry change NOT REPORTED. No statement that BC tuning compensates for or masks geometric error.
- **Q-D fidelity / quantity**: 3D CFD (ANSYS-CFX) for training data generation; 0D/3D multiscale model used. Neural network predicts pressure difference (ΔP3D) across stenotic vessels, not full 3D flow field. WSS/OSI NOT REPORTED. Sensitivity of predictions to geometric variations NOT EXPLICITLY REPORTED.
- **Q-E data**: 189 patients retrospectively collected (September 2018–December 2022), underwent CCTA and invasive FFR. Validation cohort: 77 patients. Cohort name: "Biomechanics study on quantitative relationships between coronary artery stenosis and myocardial ischemia." Private institutional data (Peking University People's Hospital). Invasive FFR ground truth present.
- **Q-F meshing**: Tetrahedron-dominated mesh, 0.1 mm (fluid) and 0.01 mm (surface) elements, 1.15–9.45M fluid elements. Five prismatic boundary layers at wall. Mesh dependency test performed. Robustness on poor/topologically-incorrect geometry NOT REPORTED.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Presents cascade NN architecture combining synthetic geometry variation in training with physics-based BC (allometric scaling); relevant to T6's methodology but does not address whether BC tuning masks or propagates segmentation error.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity analysis of DP-NN predictions to segmentation error magnitude, or studies whether fixed BC tuning absorbs geometric/segmentation variations in ground-truth data.

## Ideation opening (CFD + imaging)
- None stated. Paper addresses computational speed as a bottleneck (3.5 h → 4.26 s) but does not identify a research gap in CFD-imaging integration for geometry/segmentation uncertainty quantification.
