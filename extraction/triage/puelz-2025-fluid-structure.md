---
source_pdf_path: Resources/Puelz_2025_Med._Eng._Phys._136_104293.pdf
slug: puelz-2025-fluid-structure
ledger_status: TRIAGED
---

# puelz-2025-fluid-structure

## Bibliographic
- Title: Fluid-structure interaction simulations for the prediction of fractional flow reserve in pediatric patients with anomalous aortic origin of a coronary artery
- First author / authors: Charles Puelz, Craig G. Rusin, Dan Lior
- Year: 2025
- Venue: Medical Engineering & Physics, vol. 136
- DOI: NOT REPORTED in extracted text

## One-line claim
Proposes FSI model calibration framework for pediatric AAOCA patients that tunes downstream boundary condition parameters to resting FFR measurements and validates FFR predictions at stress.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No inter-observer segmentation variability analysis.
- **Q-B decision flip**: FFR threshold (resting vs. stress) investigated. Text: "We describe an approach to calibrate downstream boundary condition parameters to clinical measurements of resting FFR. The calibrated models are then used to predict FFR at stress, an invasively measured quantity." No explicit ≤0.80 reclassification rate reported.
- **Q-C BC tuning**: Yes, central focus. Key quote: "parameters for downstream boundary conditions needed for these models are difficult to estimate. Further, important model predictions, like fractional flow reserve (FFR), are sensitive to these parameters. We describe an approach to calibrate downstream boundary condition parameters to clinical measurements of resting FFR." Clear evidence that BC tuning changes predictions. No explicit statement on re-tuning after geometry change or whether tuning absorbs topological error.
- **Q-D fidelity / quantity**: FSI (full 3D, unspecified dimensionality reduction level). No WSS/OSI extraction mentioned in abstract/methods.
- **Q-E data**: Pediatric AAOCA patients (N, cohort name NOT REPORTED). Private clinical data. Invasive FFR ground truth present (resting and stress measurements).
- **Q-F meshing**: NOT REPORTED in extracted sections.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates that downstream BC parameters must be calibrated to resting FFR and that calibration enables reasonable stress FFR prediction—core evidence that BC tuning and FFR are tightly coupled and that model sensitivity to BC is not negligible.
- verdict: FULL
- revisit-if: If paper includes analysis of whether BC-tuning can mask or compensate for geometric error, or sensitivity of calibrated BCs to segmentation input.
