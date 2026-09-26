---
source_pdf_path: Resources/1-s2.0-S0169260722002097-main.pdf
slug: lee-2022-ffr-gray-zone-ai
ledger_status: TRIAGED
---

# lee-2022-ffr-gray-zone-ai

## Bibliographic
- Title: Optimization of FFR prediction algorithm for gray zone by hemodynamic features with synthetic model and biometric data
- First author / authors (first 3 + et al.): Hyeong Jun Lee, Young Woo Kim, Jun Hong Kim, et al.
- Year: 2022
- Venue: Computer Methods and Programs in Biomedicine 220 (2022) 106827
- DOI: 10.1016/j.cmpb.2022.106827

## One-line claim
Develops AI-based FFR estimation system from CT images optimized for gray zone prediction (0.75–0.80) by incorporating both flow and biometric features alongside automated image segmentation.

## T6 targeted questions

- **Q-A geometry perturbation**: Does NOT perturb segmentation directly. Uses patient data with automatic and manual segmentation, not synthetic perturbation study.

- **Q-B decision flip**: YES. Addresses gray zone (0.75–0.80) near 0.80 threshold: "the borderline FFR value for decision-making regarding stent insertion is 0.8 [4]. However, an FFR in the range of 0.75∼0.8 is said to be in the 'gray zone,' which is known as an area of uncertainty [5]." Reports that "approximately 10% of patients diagnosed with FFR-CT exhibited an estimated FFR value within the gray zone."

- **Q-C BC tuning**: Mentions boundary conditions in context of CFD: "FFRCFD does not directly calculate FFR, but performs flow analysis to calculate the energy loss and pressure drop based on the geometry and boundary conditions [14]." Does NOT report specific BC tuning strategy or re-tuning after geometry change.

- **Q-D fidelity / quantity**: Uses LBM CFD and ML for fast FFR prediction. Does NOT report WSS, OSI, or spatially-resolved fields. Focus is on reducing computational cost vs. full 3D CFD.

- **Q-E data**: Uses synthetic models and patient data; mentions "patient-specific data" but no specific cohort size or invasive FFR ground truth reported in this excerpt.

- **Q-F meshing**: Discusses "automatic segmentation and morphological feature extraction" but minimal detail on meshing robustness or handling poor geometry.

## Novelty bearing on T6

- bucket: METHOD
- one-line reason: AI-based FFR prediction focusing on gray zone optimization; reusable ML methodology for handling decision-boundary uncertainty in FFR-based diagnosis.
- verdict: LIGHT
- revisit-if: Paper analyzes how segmentation parameter uncertainty (e.g., slice thickness) affects gray zone misclassification or BC tuning sensitivity.
