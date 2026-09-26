---
source_pdf_path: Resources/1-s2.0-S0306987725002622-main.pdf
slug: wang-2025-cybernetic-medicine
ledger_status: TRIAGED
---

# wang-2025-cybernetic-medicine

## Bibliographic
- Title: A hypothesis of Cybernetic Medicine: Redefining health and disease through control theory
- First author / authors: Shiwei Wang, Xiaoyu Li
- Year: 2025
- Venue: Medical Hypotheses
- DOI: 10.1016/j.mehy.2025.111823

## One-line claim
Proposes a theoretical framework for Cybernetic Medicine in which the human body is modeled as an integrated MIMO biological control system whose disease state is characterized by pathological shifts in dynamic stability, with implications for digital twin-based diagnosis and personalized therapeutics.

## T6 targeted questions
- **Q-A geometry perturbation**: Not mentioned; paper addresses whole-body physiological systems, not imaging geometry or segmentation perturbation.
- **Q-B decision flip**: No mention of FFR, coronary diagnostics, or diagnostic reclassification thresholds.
- **Q-C BC tuning**: No boundary condition tuning discussed; focus is on control-theoretic therapeutic design, not CFD solver calibration.
- **Q-D fidelity / quantity**: Mentions digital twin and control system identification but does not distinguish 0D/1D/3D modeling or address hemodynamic fields (WSS, OSI).
- **Q-E data**: Illustrative examples use glucose homeostasis and cardiovascular regulation; no FFR data, coronary datasets, or invasive validation reported.
- **Q-F meshing**: Not addressed.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Provides theoretical foundation for digital twin validation methodology and model credibility assessment, but applied to whole-body physiology rather than coronary hemodynamics.
- verdict: LIGHT
- revisit-if: T6 needs to cite digital twin validation frameworks or the concept of fitting/calibration masking structural errors (paper discusses this as a caveat in systems modeling).
