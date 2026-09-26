---
source_pdf_path: Resources/1-s2.0-S0895611125000734-main.pdf
slug: tian-2025-vestreeformer-vffr
ledger_status: TRIAGED
---

# tian-2025-vestreeformer-vffr

## Bibliographic
- Title: Bi-VesTreeFormer: A bidirectional topology-aware transformer framework for coronary vFFR estimation
- First author / authors: Congyu Tian, Zehua Liu, Linyuan Wang
- Year: 2025
- Venue: Computerized Medical Imaging and Graphics
- DOI: https://doi.org/10.1016/j.compmedimag.2025.102564

## One-line claim
Novel bidirectional transformer (Bi-VesTreeFormer) enables fully automated vFFR estimation from coronary centerlines without manual feature extraction, achieving RMSE 0.048 on real data and 80% intervention prediction accuracy.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper uses real patient CCTA centerlines and synthetic reduced-order model (ROM) data; no explicit perturbation of lumen geometry or measurement of inter-observer disagreement.
- **Q-B decision flip**: YES, binary decision ("intervention necessary/unnecessary") reported. Achieved 80% accuracy predicting intervention eligibility on 43 patients (13 requiring intervention). FFR ≤0.80 is implied decision threshold for clinical intervention; paper does not explicitly report reclassification rate.
- **Q-C BC tuning**: NOT REPORTED. Deep learning model (Bi-VesTreeFormer) infers FFR from centerline morphology without explicit CFD or boundary condition modeling. No statement about BC tuning, adaptation after geometry change, or whether learned mappings mask geometric errors.
- **Q-D fidelity / quantity**: Hybrid: reduced-order lumped-parameter model (LPM) used for synthetic data training (15,000 centerlines). Real validation on CCTA centerlines. NOT full 3D CFD, NOT WSS/OSI. Purely data-driven FFR prediction.
- **Q-E data**: 43 real patients with coronary stenosis + 15,000 synthetic centerline samples (ROM-generated). Invasive FFR reference standard present (subset); public dataset status unclear. Small real-world cohort.
- **Q-F meshing**: NOT APPLICABLE. Centerline-based method; no 3D mesh generation, no surface/volume meshing discussed. No evaluation of robustness to topologically incorrect vessel trees.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Fast surrogate alternative to CFD-based vFFR (clinically useful), but does not address segmentation/geometric error sensitivity or BC tuning strategies central to T6's hypothesis.
- verdict: LIGHT
- revisit-if: Paper includes sensitivity analysis of vFFR predictions to perturbations in centerline radius/geometry, or explicit comparison of ROM-based vFFR accuracy across varying segmentation methods.

