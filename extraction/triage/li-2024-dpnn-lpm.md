---
source_pdf_path: Resources/1-s2.0-S0010482524005602-main.pdf
slug: li-2024-dpnn-lpm
ledger_status: TRIAGED
---

# li-2024-dpnn-lpm

## Bibliographic
- Title: Deep-learning-based real-time individualization for reduced-order haemodynamic model
- First author / authors: Bao Li, Guangfei Li, Jincheng Liu
- Year: 2024
- Venue: Computers in Biology and Medicine
- DOI: 10.1016/j.compbiomed.2024.108476

## One-line claim
Neural network predicts patient-specific LPM parameters from non-invasive haemodynamic waveforms in real-time, enabling individualized 0D/3D multi-scale coronary simulations.

## T6 targeted questions
- **Q-A geometry perturbation**: No geometric perturbations; focuses on parameter individualization.
- **Q-B decision flip**: Not addressed; FFR calculation mentioned but no diagnostic reclassification rates reported.
- **Q-C BC tuning**: YES, critical. "When facing medical issues involving haemodynamics... the individual LPM can be used to simulate the response of blood flow and blood pressure when the state of the human circulatory system changes. For example, for the issue of calculating FFR using a 0D/3D model, when the coronary artery converts resting to hyperemia state, the coronary microcirculation resistance decreases to 0.24 times that of resting state, which can be simulated by changing the resistance of LPM." Further: "Individualized 0D models can provide non-fixed, non-artificially determined boundary conditions for 3D models, and blood flow will adaptively change to match the changes in resistance." Coronary 16-segment circuit model developed with closed-loop structure; double Hill functions for ventricle contractility. However, NO explicit statement that boundary conditions are re-tuned AFTER geometry change (e.g., after stenosis injection), and no discussion of BC tuning masking topological error.
- **Q-D fidelity / quantity**: 0D LPM only (reduced-order). No 3D CFD or WSS/OSI in this paper. Multi-scale 0D/3D coupling is mentioned as application but not demonstrated.
- **Q-E data**: N=323 clinical (94 patients with moderate stenosis 40-70% CTA + angiography; 229 healthy controls). Haemodynamic data: BAP waveform, cardiac output, internal carotid flow. NO invasive FFR ground truth. Data expanded to 5000 synthetic cases by perturbation within physiological range.
- **Q-F meshing**: Not applicable (0D model). Multi-center data collection with standard non-invasive measurement techniques.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates efficient, patient-specific LPM parameter personalization for haemodynamic boundary conditions; shows how resistance adaptation enables 0D/3D coupling for FFR prediction. Central to T6's premise that BC tuning must be individualized, but does not test whether tuning can compensate for topological segmentation error.
- verdict: FULL
- revisit-if: This is already a FULL candidate due to Q-C's centrality. T6 should compare: (1) how well BC individualization works when geometry has known topological error, and (2) whether the resistance tuning strategy can absorb/mask such error, as T6 hypothesizes.

