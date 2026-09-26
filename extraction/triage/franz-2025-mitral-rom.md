---
source_pdf_path: Resources/1-s2.0-S0010482525011898-main.pdf
slug: franz-2025-mitral-rom
ledger_status: TRIAGED
---

# franz-2025-mitral-rom

## Bibliographic
- Title: Influences of mitral valve shape on transmitral hemodynamics before and after edge-to-edge repair: development of a reduced-order model
- First author / authors: Juliana Franz, Fabian Barbieri, Marco Barink
- Year: 2025
- Venue: Computers in Biology and Medicine
- DOI: 10.1016/j.compbiomed.2025.110838

## One-line claim
Shape-based ROM equations for mitral valve hemodynamics, incorporating orifice area and orientation, predict transmitral flow and pressure gradients before and after transcatheter edge-to-edge repair.

## T6 targeted questions
- **Q-A geometry perturbation**: Studies mitral valve shape variation (double-orifice post-repair vs. pre-repair), but NOT coronary segmentation uncertainty.
- **Q-B decision flip**: Not relevant (cardiac valve pathology, not coronary diagnostic threshold).
- **Q-C BC tuning**: ROM equations developed from CFD with defined flow pressure gradients across valve. Net vs. maximum pressure gradient discussion. However, this is valve-specific hemodynamics, NOT coronary BC tuning or topological error compensation strategy.
- **Q-D fidelity / quantity**: 3D CFD simulations of mitral valve flow; ROM equations derived relating shape to hemodynamic parameters. No WSS/OSI. Not for coronary application.
- **Q-E data**: N=10 TEER patients with moderate-to-severe mitral regurgitation. 3D TEE reconstructions. No FFR or coronary ground truth.
- **Q-F meshing**: 3D TEE-based valve reconstructions; surface re-meshing in MATLAB GIBBON and Meshmixer. Smoothing steps described. No discussion of segmentation robustness for coronary vessels.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Mitral valve disease; not coronary artery. ROM strategy for valve hemodynamics does not transfer to coronary segmentation error or FFR decision-flip analysis.
- verdict: LIGHT
- revisit-if: Not applicable to T6 coronary focus.

