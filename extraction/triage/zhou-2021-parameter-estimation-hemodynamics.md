---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2021 - Zhou - A method of parameter estimation for cardiovascular hemodynamics based on deep.pdf
slug: zhou-2021-parameter-estimation-hemodynamics
ledger_status: TRIAGED
---

# zhou-2021-parameter-estimation-hemodynamics

## Bibliographic
- Title: A method of parameter estimation for cardiovascular hemodynamics based on deep learning and its application to personalize a reduced-order model
- First author / authors (first 3 + et al.): Yang Zhou, Beibei Sun, Yuan He, et al.
- Year: 2021
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3533

## One-line claim
Deep neural networks combined with transfer learning can efficiently estimate patient-specific parameters for 1D reduced-order hemodynamic models from clinical pressure waveforms and discrete measurements.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. The paper focuses on parameter estimation methodology, not on geometry perturbation or segmentation uncertainty.
- **Q-B decision flip**: NOT REPORTED. No mention of FFR thresholds or diagnostic reclassification.
- **Q-C BC tuning**: 1D reduced-order model uses three-element Windkessel model at distal boundaries. Paper emphasizes personalized model parameters (arterial stiffness, peripheral resistance) estimated via DL; NOT REPORTED whether BC tuning is re-done after geometry changes. No explicit statement on tuning compensating for geometric error.
- **Q-D fidelity / quantity**: Reduced-order 1D model only. No WSS/OSI or spatially-resolved fields reported.
- **Q-E data**: Synthetic and in vitro data only; no human cohort, no invasive FFR ground truth.
- **Q-F meshing**: NOT REPORTED. No discussion of segmentation-to-mesh robustness or geometric quality gates.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: DL-based parameter estimation methodology could support T6's inverse problem (estimating BC parameters from measured FFR), but does not address segmentation error or BC compensation for topology changes.
- verdict: LIGHT
- revisit-if: Paper extends to real patient data with invasive FFR validation and analyzes sensitivity of parameters to geometry changes.
