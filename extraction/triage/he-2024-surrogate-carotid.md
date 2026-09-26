---
source_pdf_path: Resources/121909_1_5.0239565.pdf
slug: he-2024-surrogate-carotid
ledger_status: TRIAGED
---

# he-2024-surrogate-carotid

## Bibliographic
- Title: Efficiency of a predictive surrogate model for hemodynamic predictions of blood flow in an idealized carotid artery stenosis
- First author / authors (first 3 + et al.): Gang He, Li Zhang, Li-Cai Zhao
- Year: 2024
- Venue: Physics of Fluids
- DOI: 10.1063/5.0239565

## One-line claim
Machine learning (POD-LSTM) surrogate model for rapid prediction of carotid artery hemodynamics (velocity, pressure, WSS, OSI) in stenosis; compares prediction errors across normal and stenotic conditions.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Idealized carotid stenosis geometry; no segmentation uncertainty studies. Note: This paper studies CAROTID artery, not CORONARY.
- **Q-B decision flip**: NOT REPORTED. No FFR calculation or threshold analysis; focuses on hemodynamic parameter prediction.
- **Q-C BC tuning**: NOT REPORTED. Paper describes boundary conditions applied (pulsatile inlet flow, pressure outlet) but does not discuss tuning optimization or compensation strategies.
- **Q-D fidelity / quantity**: 3D CFD (ANSYS-FLUENT) coupled with reduced-order POD-LSTM model. Reports velocity components, pressure, WSS, and OSI in detail. Casson non-Newtonian blood model.
- **Q-E data**: Idealized (not patient-specific) carotid geometry. Simulation study; no patient cohort. No invasive ground truth.
- **Q-F meshing**: Grid independence study performed (92k, 145k, 185k, 290k elements); convergence achieved at 185k cells. "Higher resolution of the generated grid is higher near the stenosis region, reflecting the importance of this area and the higher gradients of key flow parameters in this region."

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: CAROTID artery focus; not CORONARY. POD-LSTM surrogate methodology potentially applicable to coronary WSS prediction but does not address segmentation error, BC sensitivity, or FFR decision-making relevant to T6.
- verdict: LIGHT
- revisit-if: Coronary-specific application of POD-LSTM surrogate model with patient-specific geometry and sensitivity analysis.
