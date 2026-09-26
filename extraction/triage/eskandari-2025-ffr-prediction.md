---
source_pdf_path: Resources/fbioe-13-1438253.pdf
slug: eskandari-2025-ffr-prediction
ledger_status: TRIAGED
---

# eskandari-2025-ffr-prediction

## Bibliographic
- Title: Enhancing cardiac assessments: accurate and efficient prediction of quantitative fractional flow reserve
- First author / authors (first 3 + et al.): Eskandari A, Malek S, Jabbari A et al.
- Year: 2025
- Venue: Frontiers in Bioengineering and Biotechnology
- DOI: 10.3389/fbioe.2025.1438253

## One-line claim
CFD-based FFR prediction from coronary angiography using patient-specific Windkessel boundary condition tuning achieves high accuracy (R²=0.99) against invasive FFR.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb geometry; uses patient-specific 3D reconstruction from angiography. NOT measuring segmentation uncertainty.
- **Q-B decision flip**: YES—directly relevant. FFR ≤0.80 is threshold for ischemia; validation against invasive FFR with excellent agreement. "The chosen methodology has yielded virtual FFR values that exhibit remarkable proximity to the clinically reported patient-speciﬁc FFR values, with the MSE of 6.186e-7 and R² of 0.99 (p = 0.00434)." Demonstrates decision-making at 0.80 threshold.
- **Q-C BC tuning**: CRITICAL—YES. Paper extensively addresses BC tuning: "Parameters used in the boundary conditions for CT-FFR computation were optimized in reduced-order models using retrospective data by minimizing the difference between CT-FFR and known FFR." Uses patient-specific inlet pressure (AngioBC) or literature-derived flow (LiteratureBC) with multiple Windkessel models (1-4 elements). Emphasizes importance: "The inlet boundary alters the vessel's hemodynamics" and "importance of patient-speciﬁc boundaries." NO tuning after geometry change (no perturbations).
- **Q-D fidelity / quantity**: 3D CFD (ANSYS-CFX) coupled with 0D lumped-parameter Windkessel models. Reports time-averaged wall shear stress (TAWSS) in addition to FFR and pressure.
- **Q-E data**: N=150 patients, 4 showcased, private clinical data from Rajaie Cardiovascular Medical and Research Center, invasive FFR ground truth present (YES).
- **Q-F meshing**: ANSYS meshing with ~90,000 tetrahedral cells, boundary layer treatment. Mesh independence study (coarse ~45k, medium ~90k, fine ~180k): "difference between coarse and medium grids is below the 3.1% threshold."

## Novelty bearing on T6
- bucket: METHOD | SUPPORT
- one-line reason: Patient-specific Windkessel BC tuning for coronary FFR prediction using CTA geometry; demonstrates BC parameter optimization as KEY to accuracy (R²=0.99 vs FFR); relevant to T6's BC-tuning hypothesis
- verdict: FULL
- revisit-if: Already FULL—addresses BC tuning with real patient data and invasive FFR validation; geometry perturbation arm not present but BC methodology directly supports T6 framework

