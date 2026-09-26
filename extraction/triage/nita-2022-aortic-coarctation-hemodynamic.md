---
source_pdf_path: Resources/s13239-021-00552-9.pdf
slug: nita-2022-aortic-coarctation-hemodynamic
ledger_status: TRIAGED
---

# nita-2022-aortic-coarctation-hemodynamic

## Bibliographic
- Title: Personalized Pre- and Post-Operative Hemodynamic Assessment of Aortic Coarctation from 3D Rotational Angiography
- First author / authors (first 3 + et al.): Nita CI, Puiu A, Bunescu D, et al.
- Year: 2022
- Venue: Cardiovascular Engineering and Technology
- DOI: 10.1007/s13239-021-00552-9

## One-line claim
Framework combines hemodynamic modeling and machine learning for parameter estimation to personalize inlet/outlet boundary conditions and wall properties for patient-specific CoA pressure drop prediction from 3D rotational angiography.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (patient-specific modeling study; addresses actual CoA anatomy, not synthetic perturbations)
- **Q-B decision flip**: NOT REPORTED (study evaluates pressure drop relative to clinical decision threshold 20 mmHg for intervention, but does not report reclassification rates)
- **Q-C BC tuning**: **KEY RELEVANCE**. "The key features of our framework are a parameter estimation method for calibrating inlet and outlet boundary conditions, and regional mechanical wall properties, to ensure that the computational results match the patient-specific measurements." Study validates pre- and post-operative BC calibration; catheter-based measurements used to tune BC. No explicit statement on whether tuning compensates for topological error, but framework is centered on BC personalization to match clinical data.
- **Q-D fidelity / quantity**: Reduced-order hemodynamic model (0D/1D) coupled with ML-based pressure drop model; no full 3D CFD or WSS/OSI. Mean absolute error 2.98 mmHg (pre-op), 2.11 mmHg (post-op) for pressure drop.
- **Q-E data**: 6 patient datasets (CoA, pre- and post-operative); invasive catheter-based pressure measurements as ground truth. Private cohort; procedure includes virtual stenting validation.
- **Q-F meshing**: NOT REPORTED (uses 3DRA segmentation but no detail on surface/volume mesh robustness)

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates parameter estimation framework for BC calibration to match patient-specific hemodynamics; directly relevant to T6's BC-tuning methodology and hypothesis that BC calibration can personalize predictions despite anatomical uncertainty.
- verdict: FULL
- revisit-if: (Already meets criteria for FULL review; BC tuning is central to T6)

