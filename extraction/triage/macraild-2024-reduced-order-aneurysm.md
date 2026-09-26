---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2024 - MacRaild - Reduced order modelling of intracranial aneurysm flow using proper orthogonal.pdf
slug: macraild-2024-reduced-order-aneurysm
ledger_status: TRIAGED
---

# macraild-2024-reduced-order-aneurysm

## Bibliographic
- Title: Reduced order modelling of intracranial aneurysm flow using proper orthogonal decomposition and neural networks
- First author / authors (first 3 + et al.): Michael MacRaild, Ali Sarrami-Foroushani, Alejandro F. Frangi, et al.
- Year: 2024
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3848

## One-line claim
Proper orthogonal decomposition combined with neural networks enables non-intrusive reduced-order modeling of parameterized blood flow in intracranial aneurysms with 10^5 speedup and 98%+ accuracy.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No segmentation error or geometry perturbation introduced; only parametric flow variation (inlet FRW scaling factors).
- **Q-B decision flip**: NOT APPLICABLE. Intracranial aneurysm rupture risk; not coronary FFR or diagnostic threshold crossing.
- **Q-C BC tuning**: Inlet boundary: prescribed flow-rate waveform (scaled by parameters). Outlet: zero-pressure boundaries. No mention of BC tuning or whether tuning re-done when geometry changes; not applicable to this vessel type/application.
- **Q-D fidelity / quantity**: 3D Navier–Stokes CFD (full model reduced via POD). WSS computed but NOT reported as sensitivity study outcome; focus is on velocity/pressure ROM accuracy.
- **Q-E data**: Single aneurysm geometry from 3D rotational angiography; no patient cohort, no invasive measurements.
- **Q-F meshing**: Geometry segmented via geodesic active regions algorithm; no robustness analysis on poor or topologically incorrect geometry.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Demonstrates ROM/ML dimensionality reduction methodology applicable to hemodynamics, but in intracranial (non-coronary) context with no relevance to segmentation error, FFR, or revascularization logic.
- verdict: LIGHT
- revisit-if: Applied to coronary FFR with geometry perturbation studies.
