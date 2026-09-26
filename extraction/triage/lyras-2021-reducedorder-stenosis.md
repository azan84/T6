---
source_pdf_path: Resources/journal.pone.0258047.pdf
slug: lyras-2021-reducedorder-stenosis
ledger_status: TRIAGED
---

# lyras-2021-reducedorder-stenosis

## Bibliographic
- Title: An improved reduced-order model for pressure drop across arterial stenoses
- First author / authors (first 3 + et al.): Konstantinos G. Lyras, Jack Lee
- Year: 2021
- Venue: PLoS ONE
- DOI: 10.1371/journal.pone.0258047

## One-line claim
- An improved reduced-order model for pressure drop across arterial stenoses...

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED - Focus is on modeling pressure drop, not segmentation uncertainty
- **Q-B decision flip**: YES - Mentions FFR threshold; 'FFR calculations based on the proposed model produced zero classification error for three classes comprising positive (≥0.75), negative (≤0.8) and intermediate (0.75−0.8) classes'
- **Q-C BC tuning**: NOT EXPLICIT - Reduced-order model approach as alternative to full 3D CFD; does not discuss BC tuning in detail
- **Q-D fidelity / quantity**: BOTH - Compares with 3D CFD; produces reduced-order model
- **Q-E data**: NOT REPORTED - No dataset information in abstract
- **Q-F meshing**: NOT REPORTED

## Novelty bearing on T6
- bucket: METHOD
- reason: Reduced-order modeling for pressure drop and FFR estimation; alternative to full CFD
- verdict: LIGHT
- revisit-if: If discussing sensitivity of pressure estimates to geometry or BC approximations
