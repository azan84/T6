---
source_pdf_path: Resources/113171J.pdf
slug: sommer-2020-boundary-conditions
ledger_status: TRIAGED
---

# sommer-2020-boundary-conditions

## Bibliographic
- Title: Study of the effect of boundary conditions on fractional flow reserve using patient specific coronary phantoms
- First author / authors (first 3 + et al.): Kelsey N Sommer, Lauren M Shepard, Vijay Iyer et al.
- Year: 2020
- Venue: Medical Imaging 2020: Biomedical Applications in Molecular, Structural, and Functional Imaging (SPIE)
- DOI: 10.1117/12.2548472

## One-line claim
3D-printed patient-specific coronary phantoms used in benchtop flow experiments to systematically study how outflow boundary condition changes (250–500 mL/min) affect FFR measurements and validate CT-FFR algorithms.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Study uses accurate patient-specific 3D-printed models with known geometry; no systematic segmentation uncertainty perturbation.
- **Q-B decision flip**: Yes, critical observation. "We also observed not negligible variations of the B-FFR for small coronary outflow rates changes, implying that slight changes in outflow conditions may result in diagnosis change, especially in the 0.75–0.85 FFR range." Mean difference B-FFR-500 vs I-FFR was negligible (<0.01) but increased to 0.08 at 250 mL/min flow rate.
- **Q-C BC tuning**: Yes, central study focus. Systematically varied distal coronary artery outflow rates (250–500 mL/min via programmable pulsatile pump). Key finding: "overall, we observed that for patients with a clear positive or negative diagnosis, (FFR below 0.75 or above 0.85), the diagnosis will not change even when the boundary conditions changed by more than 25% to 50%. However, for those intermediate conditions, with FFR between 0.75–0.85, a 10% change in the boundary condition may result in a diagnosis change." Critical quote: "benchtop simulations using 3D printed phantoms may become an important tool for initial development of diagnostic software. They may allow optimizations and early determination of the limitations related to a new technology which could alleviate further complications or delays."
- **Q-D fidelity / quantity**: Benchtop phantom experiments (physical 3D printing) coupled with computational CT-FFR validation. Measures pressure and FFR; does not report WSS/OSI.
- **Q-E data**: 52 patient-specific phantoms from 50 unique patients (9 with two measurements each). Mixed US/Japan sites (Gates Vascular Institute Buffalo, Juntendo University Tokyo). Invasive FFR obtained in catheterization lab; good reference standard.
- **Q-F meshing**: Excellent detail on 3D model construction: "direct planimetry and manual segmentation of the centerlines and contours... to ensure high segmentation accuracy." 3D printed with soft rubber polymer (Tango+). Phantom-specific approach bypasses numerical meshing but validates CT-FFR segmentation via physical replication.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Empirically demonstrates that boundary condition (outflow resistance) variation causes FFR reclassification in intermediate range (0.75–0.85), directly supporting T6's hypothesis that BC tuning can mask or correct for anatomical error. Core evidence for Gate N1/M1 relevance.
- verdict: FULL
- revisit-if: Extension to systematically perturb both geometry AND boundary conditions to separate compensation effects.
