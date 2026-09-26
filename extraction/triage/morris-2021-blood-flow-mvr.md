---
source_pdf_path: Resources/cvaa220.pdf
slug: morris-2021-blood-flow-mvr
ledger_status: TRIAGED
---

# morris-2021-blood-flow-mvr

## Bibliographic
- Title: A novel method for measuring absolute coronary blood flow and microvascular resistance in patients with ischaemic heart disease
- First author / authors: Paul D. Morris, Rebecca Gosling, Iwona Zwierzak
- Year: 2021
- Venue: Cardiovascular Research
- DOI: 10.1093/cvr/cvaa220

## One-line claim
A novel CFD method predicts absolute coronary blood flow (QCFD) and microvascular resistance (MVR) from invasive angiography and pressure-wire data, validated in vitro and in vivo, enabling comprehensive assessment of epicardial and microvascular disease without additional catheters or drug infusions.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED — Uses real patient angiograms and 3D-printed coronary models for in vitro validation; no synthetic perturbations or inter-observer disagreement analysis.
- **Q-B decision flip**: NOT REPORTED — No FFR threshold analysis or reclassification rates; focuses on absolute flow measurement rather than binary decision thresholds.
- **Q-C BC tuning**: MENTIONED AS CHALLENGE — "identifying a noninvasive strategy for tuning (or parameterizing) these boundary conditions probably presents the greatest challenge." States that personalized resistances/capacitances/inductances "are also not in general known on a patient-specific basis." Develops flow-based approach to avoid explicit BC tuning but does NOT demonstrate re-tuning after geometry changes.
- **Q-D fidelity / quantity**: 3D Navier-Stokes CFD validated against in vitro flow circuit and in vivo pressure/Doppler data; focuses on flow and resistance; NO WSS/OSI reported.
- **Q-E data**: N=40 patients with coronary disease for in vivo validation; invasive pressure-wire and angiography ground truth present; in vitro validation on 3D-printed models.
- **Q-F meshing**: NOT REPORTED — Uses angiography-derived 3D models but no detail on meshing methodology or robustness to poor geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Addresses BC tuning as unsolved challenge in CFD; develops flow-based measurement method to characterize both epicardial and microvascular disease, providing alternative to pressure-derived FFR indices.
- verdict: LIGHT
- revisit-if: Paper showed how flow-based BC parameterization responds to geometric changes or could discriminate topological errors from functional disease

