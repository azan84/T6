---
source_pdf_path: Resources/s12265-023-10361-1.pdf
slug: guan-2023-angio-vs-ct-ffr
ledger_status: TRIAGED
---

# guan-2023-angio-vs-ct-ffr

## Bibliographic
- Title: Functional Assessment of Coronary Artery Stenosis from Coronary Angiography and Computed Tomography: Angio-FFR vs. CT-FFR
- First author / authors: Xueqiang Guan, Dan Song, Changling Li et al.
- Year: 2023
- Venue: Journal of Cardiovascular Translational Research
- DOI: 10.1007/s12265-023-10361-1

## One-line claim
Prospective observational study comparing diagnostic performance of angiography-derived FFR (angio-FFR) and CT-derived FFR (CT-FFR) against invasive FFR reference standard; angio-FFR shows slightly higher accuracy.

## T6 targeted questions

- **Q-A geometry perturbation**: NOT REPORTED. Study compares two computational methods (angio-FFR vs CT-FFR) but does not examine segmentation uncertainty or inter-observer disagreement. Notes: "Several lesion characteristics that might affect CT-FFR performance" were evaluated (vessel, location, length, bifurcation, calcification) but geometric perturbation sensitivity was not systematic.

- **Q-B decision flip**: YES. Central to study. FFR ≤0.80 used as threshold for hemodynamically significant stenosis. Overall diagnostic accuracy: angio-FFR 94.6%, CT-FFR 91.8%. Sensitivity both 91.4%. Study notes: "For both methods, there is still uncertainty in decision-making when the CT-FFR or angio-FFR values were in the gray zone (0.75–0.80)."

- **Q-C BC tuning**: Addressed but not detailed. Study notes: "Based on the segmented vessel, calculated velocity, and input aortic pressure, AccuFFRangio distribution could be calculated through the pressure drop equations." For CT-FFR: "blood flow and pressure of the coronary artery tree were simulated by using CFD analysis and the resting flow was estimated from the myocardium mass. Hyperemia condition was applied during the CT-FFR calculation to each branch." Does NOT discuss whether BC tuning is re-done after geometry changes or whether it compensates for geometric error. States: "As for boundary conditions, the mean volumetric flow was calculated using TIMI frame count combined with 3D QCA; the coronary pressure was then calculated using the principles of fluid dynamics."

- **Q-D fidelity / quantity**: Both methods use CFD-based approaches. Angio-FFR applies simplified pressure drop equations; CT-FFR solves full Navier-Stokes CFD. Blood modeled as Newtonian fluid (ρ = 1,056 kg/m³, µ = 0.0035 Pa·s for CT-FFR). Does not report WSS, OSI, or other spatially-resolved hemodynamic indices.

- **Q-E data**: Clinical cohort: 110 patients, 139 vessels with stable CAD. Underwent coronary CTA, coronary angiography, and invasive FFR within 2 months (May 2016–July 2019). Invasive FFR ground truth present.

- **Q-F meshing**: Mentions: "Segmentation of the coronary artery lumen" as preprocessing step. Notes calcification challenges: "the accuracy of CT-FFR diagnosis may be low because coronary artery calcification causes difficulties in CT image segmentation and subsequent FFR calculation." However, does NOT quantify segmentation robustness or inter-observer disagreement.

## Novelty bearing on T6

- **bucket**: SUPPORT
- **one-line reason**: Validates both angio-FFR and CT-FFR computational approaches against invasive FFR; identifies calcification and gray-zone uncertainty as ongoing challenges; supports T6's premise that FFR diagnostic robustness is established but does not address BC tuning or geometric error handling.
- **verdict**: LIGHT
- **revisit-if**: Paper quantifies impact of segmentation uncertainty on angio-FFR or CT-FFR, or addresses whether BC optimization varies between methods.
