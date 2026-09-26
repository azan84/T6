---
source_pdf_path: Resources/s13239-026-00836-y.pdf
slug: tanade-2026-ffr-ml
ledger_status: TRIAGED
---

# tanade-2026-ffr-ml

## Bibliographic
- Title: Optimizing Non-invasive Fractional Flow Reserve Estimation with Machine Learning-Enhanced 1D Hemodynamic Modeling
- First author / authors: Cyrus Tanade, Japneet Kaur Mavi, Guinevere Ferreira (et al.)
- Year: 2026
- Venue: Cardiovascular Engineering and Technology 17:425–438
- DOI: 10.1007/s13239-026-00836-y

## One-line claim
Machine learning feedback loops applied to steady-state 1D hemodynamic models can improve FFR prediction accuracy without requiring computationally expensive pulsatile flow assumptions.

## T6 targeted questions
- **Q-A geometry perturbation**: No perturbation—uses patient-specific coronary geometry reconstructed from angiography. NOT REPORTED for uncertainty quantification.
- **Q-B decision flip**: YES—Reports FFR 0.80 threshold classification. Diagnostic accuracy: sensitivity 83.3%, specificity 100.0%, PPV 100.0%, NPV 88.2%, overall precision 92.6% on 132 patients with 132 lesions.
- **Q-C BC tuning**: YES, detailed section "Boundary Condition Tuning for Personalized Hemodynamic Simulations". Uses "Two-element Windkessel models, consisting of peripheral resistance (Rp) and compliance (C), were employed at the outlets to account for the effect of microvascular hemodynamics." Boundary conditions adjusted per-patient level using clinical data (pressure, cardiac output, heart rate, hematocrit). NOT REPORTED: whether BC tuning is re-done after geometry changes, or whether it compensates for geometric error.
- **Q-D fidelity / quantity**: 1D CFD reduced-order blood flow simulator. NOT REPORTED: WSS/OSI or spatial fields.
- **Q-E data**: Cohort of 132 patients (two-center, retrospective) with 132 coronary lesions. Invasive FFR ground truth present (wire-based measurements with adenosine hyperemia).
- **Q-F meshing**: NOT REPORTED. Geometry reconstructed via established method from angiography; expert cardiologist verification of topology and anatomy via iterative feedback with imaging.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Describes ML feedback loop to refine BC-tuned 1D hemodynamic models against clinical FFR; demonstrates steady-state adequacy (closes pulsatile vs. steady debate locally). Reusable BC tuning and 1D solver protocol.
- verdict: LIGHT
- revisit-if: Full paper shows decision-flip rates broken by error type (geometry type or magnitude), or evidence that model accuracy degrades under poor geometry / topological error.
