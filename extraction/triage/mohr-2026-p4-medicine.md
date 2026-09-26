---
source_pdf_path: Resources/s12967-026-08346-0_reference.pdf
slug: mohr-2026-p4-medicine
ledger_status: TRIAGED
---

# mohr-2026-p4-medicine

## Bibliographic
- Title: Aspiration to architecture: multi-omics, AI, digital twins, and blockchain for P4 medicine
- First author / authors (first 3 + et al.): Mohr AE, Bajnath A, King G, Ichim TE, Jasbi P
- Year: 2026
- Venue: Journal of Translational Medicine (Article in Press)
- DOI: 10.1186/s12967-026-08346-0

## One-line claim
P4 medicine (predictive, preventive, personalized, participatory) achieves clinical scalability only when each pillar is anchored to a specific digital technology: multi-omics for prediction, AI for risk stratification, digital twinning for personalized simulation and optimization, and blockchain for patient-controlled data sovereignty.

## T6 targeted questions
- **Q-A geometry perturbation**: Not addressed.
- **Q-B decision flip**: Not reported (non-coronary domain). Framework is general for precision medicine across diseases.
- **Q-C BC tuning**: Directly relevant: digital twin section describes "constrained optimization" where "each recommendation is ranked by importance, adjusted for adherence burden." Explicitly notes: "at retest, new multi-omic data update the twin, and the trajectory cloud narrows as individual response data replace population priors." This is iterative re-calibration after new data.
- **Q-D fidelity / quantity**: Most mature cardiology implementations discussed (patient-specific heart models simulating arrhythmia risk). No specific coronary or FFR domain reported.
- **Q-E data**: Preliminary metabolomic data from 2,072-person cross-sectional cohort; reference to UK Biobank (500,000+), NIH All of Us (245,000+). No invasive-FFR ground truth reported.
- **Q-F meshing**: Not applicable.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Defines staged validation framework for digital twins (technical validation → prospective single-arm → comparative trial), with explicit callout that "the validation paradox" (each patient is unique, no population-level ground truth for individual predictions) requires n-of-1 trial designs and computational model credibility frameworks.
- verdict: LIGHT
- revisit-if: Specific application to coronary hemodynamics or FFR prediction becomes available.
