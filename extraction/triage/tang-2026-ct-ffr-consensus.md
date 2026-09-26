---
source_pdf_path: Resources/s00330-025-12313-6.pdf
slug: tang-2026-ct-ffr-consensus
ledger_status: TRIAGED
---

# tang-2026-ct-ffr-consensus

## Bibliographic
- Title: Clinical use of coronary computed tomography angiography-derived fractional flow reserve: expert consensus by an International Working Group
- First author / authors (first 3 + et al.): Chun Xiang Tang, Jonathon A. Leipsic, Bjarne L. Nørgaard et al.
- Year: 2026
- Venue: European Radiology
- DOI: 10.1007/s00330-025-12313-6

## One-line claim
International expert consensus on standardized application of CT-FFR in clinical practice across diagnostic, prognostic, and decision-support roles.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Review/consensus document, no original study of perturbations.
- **Q-B decision flip**: FFR ≤0.80 and gray zone (0.76–0.80) discussed. Consensus recommends gray zone management including delta-FFR (trans-lesional gradient >0.12). No specific reclassification rates.
- **Q-C BC tuning**: Mentions 3D-CFD, reduced-order CFD, and machine learning approaches. "Machine learning (ML) aids in boundary condition extraction and CFD integration." No detailed discussion of BC re-tuning after geometry change or compensation for topological error.
- **Q-D fidelity / quantity**: 3D-CFD (HeartFlow), reduced-order CFD, and ML/deep learning discussed. Accuracy 71–91%, sensitivity 76–98%, specificity 61–94%. No detail on WSS/OSI or spatial field sensitivity to geometry.
- **Q-E data**: Review/consensus; no new cohort data.
- **Q-F meshing**: NOT REPORTED. Consensus document, no methods detail.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive review of CT-FFR methods (3D-CFD, reduced-order, ML) and clinical applications. Does not address segmentation error, topological robustness, or BC tuning hypotheses.
- verdict: LIGHT
- revisit-if: Consensus expanded with specific sections on meshing robustness, segmentation error handling, or boundary condition calibration strategies.

