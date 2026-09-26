---
source_pdf_path: Resources/fcvm-08-706628.pdf
slug: franke-2021-aortic-stenosis
ledger_status: TRIAGED
---

# franke-2021-aortic-stenosis

## Bibliographic
- Title: Computed Tomography-Based Assessment of Transvalvular Pressure Gradient in Aortic Stenosis
- First author / authors (first 3 + et al.): Franke B, Brüning J, Yevtushenko P et al.
- Year: 2021
- Venue: Frontiers in Cardiovascular Medicine
- DOI: 10.3389/fcvm.2021.706628

## One-line claim
Reduced-order model from CT data predicts transvalvular pressure gradient in aortic stenosis with good agreement to invasive catheterization.

## T6 targeted questions
- **Q-A geometry perturbation**: Does NOT perturb; uses patient-specific aortic valve geometry and flow from CT.
- **Q-B decision flip**: NOT addressed. Study is aortic valve stenosis (NOT coronary artery disease). No FFR or coronary decision thresholds discussed.
- **Q-C BC tuning**: Reduced-order model with inlet flow boundary condition and outlet constant pressure. Power-law model coefficients fitted from CFD on 58 patients. Not applicable to coronary BC tuning strategy.
- **Q-D fidelity / quantity**: 3D CFD (STAR-CCM+) for model development; reduced-order power-law model for clinical application. Reports pressure gradient only, not flow-resolved fields.
- **Q-E data**: N=84 aortic stenosis patients for validation, split across training (58) and validation (84). Invasive catheterization ground truth present.
- **Q-F meshing**: Polyhedral meshes with base size 0.5–0.8 mm and boundary layer refinement. No discussion of robustness to geometric error.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Aortic valve stenosis, not coronary artery disease; reduced-order modeling not directly applicable to coronary segmentation error or BC-tuning-absorbs-error hypothesis
- verdict: LIGHT
- revisit-if: Paper addresses coronary artery applications OR boundary condition tuning principles transfer to coronary domain

