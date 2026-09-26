---
source_pdf_path: Resources/fdgth-8-1908794.pdf
slug: vallee-2026-digital-twins
ledger_status: TRIAGED
---

# vallee-2026-digital-twins

## Bibliographic
- Title: From digital twins to clinically trustworthy twins: a clinical-claim-based validation framework for personalized digital health
- First author / authors (first 3 + et al.): Vallée A
- Year: 2026
- Venue: Frontiers in Digital Health 8:1908794
- DOI: 10.3389/fdgth.2026.1908794

## One-line claim
Clinical validity of digital twins is determined not by computational complexity but by matching validation evidence to the specific clinical claim (descriptive, predictive, counterfactual, interventional, or population-health), requiring population calibration and post-deployment monitoring.

## T6 targeted questions
- **Q-A geometry perturbation**: Not addressed in detail. Framework is agnostic to geometry specificity.
- **Q-B decision flip**: Mentions cardiology example of absolute risk prediction; notes that calibration (not discrimination alone) is prerequisite for individualized decision-making when thresholds drive action.
- **Q-C BC tuning**: Not specifically addressed. However, framework explicitly warns: "A model that accurately reconstructs prior trajectories may not be valid for forecasting future trajectories under treatment." Counterfactual claims require explicit assumptions about confounding, treatment assignment, and competing events.
- **Q-D fidelity / quantity**: Framework distinguishes descriptive, predictive, counterfactual, and interventional claims. Discusses 3D cardiac models and their evidentiary burden depending on use case.
- **Q-E data**: No specific FFR-based study reported. Framework is methodological.
- **Q-F meshing**: Not reported.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Defines the evidentiary architecture required for digital twin validation across all clinical claims; directly applicable to establishing T6's methodology for ranking error impact on binary FFR decisions.
- verdict: FULL
- revisit-if: None; this is a core validation-methodology reference.
