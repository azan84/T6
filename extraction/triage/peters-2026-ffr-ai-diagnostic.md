---
source_pdf_path: Resources/s00330-025-12048-4.pdf
slug: peters-2026-ffr-ai-diagnostic
ledger_status: TRIAGED
---

# peters-2026-ffr-ai-diagnostic

## Bibliographic
- Title: Diagnostic performance of a coronary CT angiography-based deep learning model for the prediction of vessel-specific ischemia
- First author / authors (first 3 + et al.): Benjamin Peters, Rolf Symons, Sanad Oulkadi et al.
- Year: 2026
- Venue: European Radiology
- DOI: 10.1007/s00330-025-12048-4

## One-line claim
A deep learning model (CorEx, SPIMED-AI) achieves high diagnostic accuracy (83%) for predicting vessel-specific ischemia on CCTA compared to invasive FFR/iFR.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Retrospective validation study on real patient CCTA/ICA cohort, no synthetic perturbations.
- **Q-B decision flip**: FFR ≤0.80 and iFR ≤0.89 thresholds used as gold standard. Sensitivity 85% (FFR) / 82% (iFR), specificity 91% / 78%, no reclassification rates by threshold uncertainty.
- **Q-C BC tuning**: NOT REPORTED. Deep learning model trained on segmented curved multiplanar reconstruction (cMPR) images; no CFD, no boundary conditions, no tuning discussion. "Unlike traditional methods that depend on solving the partial differential equations of CFD to model blood flow and pressure, our model learns the relationship between coronary anatomy and FFR directly from the images."
- **Q-D fidelity / quantity**: Deep learning on 2D multiplanar reconstructions (9 cMPR images at 40° intervals). No 3D CFD, no WSS/OSI, no spatially-resolved fields.
- **Q-E data**: N=322 vessels from 275 patients, two centers, CCTA + invasive FFR/iFR within 3 months, prospective design (2017–2022).
- **Q-F meshing**: NOT REPORTED. No segmentation-to-mesh workflow described; AI model works on image reconstructions only.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates AI-based FFR prediction bypass CFD entirely; validates alternative to reduced-order or full 3D solvers. No evidence on geometric sensitivity or BC compensation.
- verdict: LIGHT
- revisit-if: Study reports segmentation quality effects, coronary calcification impact on accuracy, or comparison to CFD-based methods in same cohort.

