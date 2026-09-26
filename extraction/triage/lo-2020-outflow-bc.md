---
source_pdf_path: Resources/Lo_2020_Med._Eng._Phys._76_79.pdf
slug: lo-2020-outflow-bc
ledger_status: TRIAGED
---

# lo-2020-outflow-bc

## Bibliographic
- Title: On outflow boundary conditions for CT-based computation of FFR: Examination using PET images
- First author / authors: Ernest WC Lo, Leon J Menezes, Ryo Torii
- Year: 2020
- Venue: Medical Engineering and Physics, vol. 76, pp. 79–87
- DOI: 10.1016/j.medengphy.2019.10.007

## One-line claim
A pilot CFD study comparing morphology-based vs PET perfusion-based outflow boundary conditions for CT-FFR shows that conventional morphology-based BC assumptions overestimate functional severity in patients with reduced vasodilatory response, particularly in presence of microvascular disease.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED – does not systematically perturb geometry; studies functional/physiological assumption sensitivity
- **Q-B decision flip**: Addresses gray zone and sensitivity of FFR classification to BC choice: "the range is across the clinical cutoff of 0.8 (0.74–0.88)"; demonstrates cases where BC assumption changes diagnostic outcome
- **Q-C BC tuning**: YES – HIGHLY RELEVANT: "To better understand the sensitivity of computational FFRs on outflow boundary condition"; two BC approaches compared: "(1) conventional morphology-based and (2) PET perfusion-based conditions"; "the FFRs computed with the morphology-based BC tend to estimate higher functional severity, especially in patients with reduced vasodilatory response under hyperaemia"; "the models with PET-based condition revealed that there are cases in which conventional boundary condition overestimate the functional severity of a stenosis"; varying hyperaemic resistances (30%–90%) shows FFR sensitivity to vasodilatory assumption
- **Q-D fidelity / quantity**: 3D CFD (ANSYS CFX 17.0) with Windkessel 0D outlet models; steady-state incompressible Navier-Stokes; compares anatomically-based vs perfusion-based microvasculature models
- **Q-E data**: 10 patients (6M, 4F; age 61.7±12.2) with mixed stenosis severity; 82Rb PET perfusion + invasive FFR; small cohort, pilot study
- **Q-F meshing**: Mentions tetrahedral elements + 6 prism layers; segmentation from CTCA using ScanIP

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Direct evidence that BC assumptions (specifically hyperaemic resistance assumptions) significantly affect FFR computation and can produce false-negative diagnoses in patients with microvascular disease; validates T6 hypothesis that BC tuning is critical but does not rank geometric error types by their functional impact
- verdict: FULL
- revisit-if: NA
