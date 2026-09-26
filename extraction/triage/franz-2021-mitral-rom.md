---
source_pdf_path: Resources/An orifice shape-based reduced order model of patient-specific mitral valve regurgitation.pdf
slug: franz-2021-mitral-rom
ledger_status: TRIAGED
---

# franz-2021-mitral-rom

## Bibliographic
- Title: An orifice shape-based reduced order model of patient-specific mitral valve regurgitation
- First author / authors: J. Franz, K. Czechowicz, I. Waechter-Stehle, F. Hellmeier
- Year: 2021
- Venue: Engineering Applications of Computational Fluid Mechanics, vol. 15, no. 1, pp. 1868–1884
- DOI: 10.1080/19942060.2021.1995048

## One-line claim
A reduced-order CFD model predicts patient-specific mitral valve regurgitant flow from orifice geometry and shape parameters, validated against full 3D CFD simulations on 43 patients.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (studies mitral valve, not coronary stenosis)
- **Q-B decision flip**: NOT REPORTED
- **Q-C BC tuning**: Windkessel models used as outlet BCs; no discussion of tuning or compensation
- **Q-D fidelity / quantity**: 3D CFD (ANSYS CFX) on patient-specific mitral geometries; no coronary flow or WSS
- **Q-E data**: 43 patients with 3D TEE reconstructions; clinical MR severity endpoint
- **Q-F meshing**: YES – discusses tetrahedral elements + prism layers; sensitivity to geometric accuracy of regurgitant orifice

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Addresses mitral valve hemodynamics, not coronary artery disease or stenosis-driven ischemia
- verdict: LIGHT
- revisit-if: Reduced-order modeling approach could be adapted for coronary flow, though primary anatomy is not relevant
