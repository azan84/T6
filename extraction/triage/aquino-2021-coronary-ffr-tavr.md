---
source_pdf_path: Resources/aquino-et-al-2021-coronary-ct-fractional-flow-reserve-before-transcatheter-aortic-valve-replacement-clinical-outcomes.pdf
slug: aquino-2021-coronary-ffr-tavr
ledger_status: TRIAGED
---

# aquino-2021-coronary-ffr-tavr

## Bibliographic
- Title: Coronary CT Fractional Flow Reserve before Transcatheter Aortic Valve Replacement: Clinical Outcomes
- First author / authors: Gilberto J. Aquino, Andres F. Abadia, U. Joseph Schoepf
- Year: 2022
- Venue: Radiology
- DOI: 10.1148/radiol.2021210160

## One-line claim
On-site machine learning–based CT-FFR was associated with major adverse cardiac events in candidates for transcatheter aortic valve replacement and improved the predictive value of coronary CT angiography assessment.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED — No mention of segmentation uncertainty or geometry perturbations. Study uses real clinical CCTA data without synthetic perturbations.
- **Q-B decision flip**: YES — Reports FFR threshold-based reclassification using 0.75 cutoff (lower than standard 0.80). "CT-FFR was predictive of MACE (hazard ratio [HR], 4.1; 95% CI: 1.6, 10.8; P = .01)"; 16% MACE rate at 18-month follow-up.
- **Q-C BC tuning**: NOT REPORTED — Uses on-site machine learning CFD approach. No mention of BC tuning, Windkessel parameters, or re-tuning after geometry changes.
- **Q-D fidelity / quantity**: 3D CFD (machine learning based, not full Navier-Stokes); NO WSS/OSI or spatially-resolved fields reported.
- **Q-E data**: N=196 TAVR patients (2014-2019); private institutional cohort; NO invasive FFR ground truth reported as present.
- **Q-F meshing**: NOT REPORTED — Mentions semiautomatic segmentation and "3D mesh of the coronary tree" but no detail on meshing robustness to poor/topologically incorrect geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Validates CT-FFR for clinical decision-making in TAVR patients, supporting T6's premise that FFR-based decisions matter clinically, but does not test geometric robustness or BC tuning.
- verdict: LIGHT
- revisit-if: Paper addressed sensitivity to segmentation uncertainty or documented BC re-tuning effects on decision accuracy

