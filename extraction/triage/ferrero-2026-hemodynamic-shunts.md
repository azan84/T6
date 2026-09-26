---
source_pdf_path: Resources/1-s2.0-S266666852600011X-main.pdf
slug: ferrero-2026-hemodynamic-shunts
ledger_id: C013
ledger_status: TRIAGED
---

# ferrero-2026-hemodynamic-shunts

## Bibliographic
- Title: Analytical interpretation of hemodynamic data in patients with intracardiac shunts: Role of mathematical modeling
- First author / authors: Paolo Ferrero, Andrea Tonini, Giulio Valenti
- Year: 2026
- Venue: International Journal of Cardiology Congenital Heart Disease, vol. 24
- DOI: 10.1016/j.ijcchd.2026.100662

## One-line claim
Uses a zero-dimensional lumped-parameter Windkessel model (electric circuit analogue) to analytically explore hemodynamic variables governing shunt fraction (Qp/Qs) in atrial septal defects (ASD), ventricular septal defects (VSD), and combined ASD+VSD, showing differential sensitivity to pulmonary vascular resistance (PVR) and ventricular elastance.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper does not address vascular geometry uncertainty or segmentation variability; focuses on shunt pathophysiology (fixed defect sizes).
- **Q-B decision flip**: NOT REPORTED. No FFR threshold or diagnostic reclassification; analysis is on shunt flow ratios (Qp/Qs) and their sensitivity to PVR and ventricular properties.
- **Q-C BC tuning**: PARTIALLY REPORTED. Paper employs 0-D Windkessel-type boundary conditions (resistances, capacitances, inductances for systemic and pulmonary circulations). States: "Circulatory system is split into arterial and venous compartments, each being described by resistive, capacitive and inductive components." However, no discussion of BC tuning after geometry change, optimization protocol, or how BC parameters interact with anatomical defects.
- **Q-D fidelity / quantity**: 0-D lumped-parameter model only (Windkessel circuits with R, L, C elements). No 3D CFD, no spatially resolved fields (WSS, OSI), no flow pulsatility beyond what lumped model captures.
- **Q-E data**: Proof-of-concept modeling study; no patient cohort. Model parameters (resistances, elastances, compliance) set to reproduce baseline hemodynamic values (SVR=15 WU, PVR=1.9 WU). No invasive ground truth; study is analytical exploration of parameter effects on Qp/Qs.
- **Q-F meshing**: NOT APPLICABLE. Zero-dimensional model; no geometry, segmentation, or meshing involved.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates 0-D lumped-parameter hemodynamic modeling with Windkessel boundary conditions and shows how cardiac/vascular parameter changes propagate to clinically relevant metrics (shunt flow ratios); relevant to T6's frame that BC tuning and hemodynamic parameters interact.
- verdict: LIGHT
- revisit-if: If paper explores how geometric defect size/location affects BC parameter values needed to match clinical observations, or if sensitivity analysis quantifies how BC parameter uncertainty propagates to diagnostic metrics (analogous to FFR sensitivity in T6).

## Ideation opening (CFD + imaging)
- Paper states: "This model analytically illustrates that shunt through an ASD is minimally affected by PVRs. The marginal change of pulmonary flow produced by large variations of PVR appeared mediated by changes in right ventricular elastance." Implies that ventricular mechanical properties confound hemodynamic interpretation in congenital heart disease, raising a gap for imaging-based characterization of RV properties and their coupling to afterload (analogous to T6's hypothesis on how geometry error and BC interact).
