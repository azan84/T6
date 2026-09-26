---
source_pdf_path: Resources/atm-09-17-1390.pdf
slug: li-2021-ct-derived-pda
ledger_status: TRIAGED
---

# li-2021-ct-derived-pda

## Bibliographic
- Title: Diagnostic performance of CT-derived resting distal to aortic pressure ratio (resting Pd/Pa) vs. CT-derived fractional flow reserve (CT-FFR) in coronary lesion severity assessment
- First author / authors: Quan Li, Yang Zhang, Chunliang Wang
- Year: 2021
- Venue: Annals of Translational Medicine
- DOI: 10.21037/atm-21-4325

## One-line claim
CT-derived resting Pd/Pa shows similar or slightly better diagnostic performance than CT-FFR by avoiding errors introduced by the simplified TCRI model used in CT-FFR computations.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED — Study uses real patient CTA data (N=20 patients, 25 vessels); no synthetic perturbations or inter-observer disagreement analysis.
- **Q-B decision flip**: YES — Compares diagnostic accuracy at FFR <0.80 threshold. "CT-(Pd/Pa)rest showed sensitivity of 0.85, specificity of 0.91, PPV of 0.92, and NPV of 0.83" vs CT-FFR sensitivity 0.85, specificity 0.58.
- **Q-C BC tuning**: PARTIAL — Identifies TCRI model as source of error: "uncertainty related to the reduction in peripheral resistance due to vasodilation administration" and "the TCRI model could only be accurately determined by the calibration of coronary flow reserve ahead." Proposes resting Pd/Pa to avoid BC tuning but does NOT demonstrate re-tuning after geometry changes.
- **Q-D fidelity / quantity**: 3D OpenFOAM CFD; NO WSS/OSI reported; focuses on pressure-based outputs only.
- **Q-E data**: N=20 consecutive patients with suspected CAD; invasive FFR ground truth present; private hospital cohort.
- **Q-F meshing**: NOT REPORTED — "detailed 3D model was built to cover the entire coronary artery tree" with semi-automated segmentation; no detail on robustness to poor geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Addresses BC tuning errors (TCRI model) as dominant source of CT-FFR inaccuracy; demonstrates image-derived coronary blood flow calibration as alternative to simplified resistance models.
- verdict: LIGHT
- revisit-if: Paper demonstrated BC re-tuning across different anatomies or showed sensitivity of decision accuracy to BC initialization

