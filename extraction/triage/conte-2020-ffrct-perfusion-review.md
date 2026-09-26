---
source_pdf_path: Resources/1-s2.0-S0167527319300129-main.pdf
slug: conte-2020-ffrct-perfusion-review
ledger_status: TRIAGED
---

# conte-2020-ffrct-perfusion-review

## Bibliographic
- Title: FFRCT and CT perfusion: A review on the evaluation of functional impact of coronary artery stenosis by cardiac CT
- First author / authors (first 3 + et al.): Edoardo Conte, Jeroen Sonck, Saima Mushtaq, et al.
- Year: 2020
- Venue: International Journal of Cardiology 300 (2020) 289–296
- DOI: 10.1016/j.ijcard.2019.08.018

## One-line claim
Expert review of FFR-CT and CT perfusion techniques for functional assessment of coronary artery disease, covering technical principles, clinical validation, and current evidence.

## T6 targeted questions

- **Q-A geometry perturbation**: Does NOT perturb or analyze segmentation uncertainty. Review focuses on clinical validation and evidence synthesis.

- **Q-B decision flip**: YES. Review covers FFR threshold 0.80 and diagnostic performance. Cites DISCOVER-FLOW, DEFACTO, and other trials using "similar cut-off for lesion significance (<0.80 for both modalities)". SYNTAX-II FFR-CT "confirmed high accuracy with an AUC of 0.85". Meta-analysis: "FFRCT showed 82% diagnostic accuracy [14]."

- **Q-C BC tuning**: Mentions CFD principles: "computational models to standard CCTA datasets...using 3D patient-specific luminal geometries, a volumetric finite element mesh is used to simulate blood flow". References "Virtual PCI" capability but no specific discussion of boundary condition re-tuning after geometry changes or error compensation.

- **Q-D fidelity / quantity**: Reviews 3D CFD-based FFR-CT methods. Does NOT report WSS, OSI, or spatially-resolved flow fields in review scope.

- **Q-E data**: Systematic review of multiple trials (DISCOVER-FLOW, DEFACTO, NXT, SYNTAX-II FFR-CT) with invasive FFR ground truth. Large aggregate cohorts (>1000 patients).

- **Q-F meshing**: Mentions "volumetric finite element mesh" in technical description but no detail on robustness, handling of poor geometry, or segmentation quality impact.

## Novelty bearing on T6

- bucket: BACKGROUND
- one-line reason: Provides clinical context and validation framework for FFR-CT methods; establishes clinical trial evidence for 0.80 threshold decision-making.
- verdict: LIGHT
- revisit-if: Review specifically addresses segmentation parameter uncertainty or BC compensation strategies.
