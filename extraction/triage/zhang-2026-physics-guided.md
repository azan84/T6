---
source_pdf_path: Resources/Physics-Guided_Variational_Method_for_Fractional_Flow_Reserve_Based_on_Coronary_Angiography.pdf
slug: zhang-2026-physics-guided
ledger_status: TRIAGED
---

# zhang-2026-physics-guided

## Bibliographic
- Title: Physics-Guided Variational Method for Fractional Flow Reserve Based on Coronary Angiography
- First author / authors: Qi Zhang, Heye Zhang, Zhifan Gao
- Year: 2026
- Venue: IEEE Transactions on Medical Imaging, vol. 45, no. 3
- DOI: 10.1109/TMI.2025.3618679

## One-line claim
Proposes a physics-guided variational domain progressing method (PVDPM) for non-invasive FFR estimation using coronary angiography that models 1D FSI systems with improved boundary condition handling.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No perturbation analysis or inter-observer disagreement quantified.
- **Q-B decision flip**: Yes, explicit discussion of FFR 0.80 threshold reclassification. Text states: "Underestimating outlet resistance can yield falsely high FFR (evaluated >0.8, measured <0.8), missing ischemic lesions" and "Overestimation can give falsely low FFR (evaluated <0.8, measured >0.8), leading to unnecessary stenting" with 20% and 30% risk increases cited.
- **Q-C BC tuning**: Yes, central to the work. Paper explicitly addresses outlet boundary conditions: "patient-specific outlet boundary data (e.g., distal pressure or flow) are often unavailable." The PVDPM method uses "variational paradigm as a physical constraint" to "represent the fluid–solid boundary condition interaction as energy terms within the FSI system, mitigating inaccuracies from poorly defined boundary coupling." Quote: "it represents the fluid–solid boundary condition interaction as energy terms within the FSI system, mitigating inaccuracies from poorly defined boundary coupling." No explicit statement on re-tuning after geometry change.
- **Q-D fidelity / quantity**: Reduced-order (1D FSI model). No WSS/OSI reported. Abstract: "modelling a 1D FSI system using 240 dynamic coronary angiography images."
- **Q-E data**: Cohort = 240 dynamic coronary angiography images (dataset not named). Private data with informed consent. No invasive FFR ground truth mentioned.
- **Q-F meshing**: NOT REPORTED. No segmentation or meshing detail provided.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Proposes physics-guided variational formulation to handle implicit BC coupling in FSI models, addressing a core T6 challenge about BC parameter sensitivity and model calibration.
- verdict: FULL
- revisit-if: If paper includes sensitivity analysis on outlet resistance changes or demonstrates that tuning can compensate for geometric error.
