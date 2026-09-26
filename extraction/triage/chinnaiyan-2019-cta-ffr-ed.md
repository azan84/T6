---
source_pdf_path: Resources/chinnaiyan-et-al-2019-clinical-use-of-ct-derived-fractional-flow-reserve-in-the-emergency-department.pdf
slug: chinnaiyan-2019-cta-ffr-ed
ledger_status: TRIAGED
---

# chinnaiyan-2019-cta-ffr-ed

## Bibliographic
- Title: Clinical Use of CT-Derived Fractional Flow Reserve in the Emergency Department
- First author / authors: Kavitha M. Chinnaiyan, Robert D. Safian, Michael L. Gallagher
- Year: 2020
- Venue: JACC: Cardiovascular Imaging
- DOI: 10.1016/j.jcmg.2019.05.025

## One-line claim
FFRCT is feasible in acute chest pain (ACP) triage with no difference in major adverse cardiac events and costs compared to coronary CTA alone; deferral of revascularization is safe with negative FFRCT.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED — Clinical outcomes study using real CTA; no systematic analysis of segmentation uncertainty or inter-observer variability.
- **Q-B decision flip**: YES — Reports FFRCT ≤0.80 as positive for hemodynamically significant stenosis. "No deaths or myocardial infarction occurred with negative FFRCT when revascularization was deferred." Demonstrates safe deferral strategy based on FFRCT threshold.
- **Q-C BC tuning**: NOT REPORTED — No detail on BC method, tuning strategy, or whether parameters are re-optimized after geometry changes.
- **Q-D fidelity / quantity**: 3D CFD (using HeartFlow platform); NO WSS/OSI reported; focuses on pressure-derived FFR values only.
- **Q-E data**: N=555 ACP patients; cohort included 297 with FFRCT (196 negative, 101 positive); private institutional data; invasive FFR ground truth not universally present.
- **Q-F meshing**: NOT REPORTED — Mentions "rejection rate for FFRCT was 1.6%" but no detail on meshing or robustness to poor quality CTA.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Clinical validation of CT-FFR for safe decision-making (deferral of revascularization); supports T6's premise that FFR-based decisions have clinical impact.
- verdict: LIGHT
- revisit-if: Paper analyzed sensitivity of FFR decision accuracy to image quality, segmentation errors, or anatomical complexity

