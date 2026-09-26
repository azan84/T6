---
source_pdf_path: Resources/1-s2.0-S0720048X2600553X-main.pdf
slug: naniwa-2026-ct-mu-fr-stents
ledger_status: TRIAGED
---

# naniwa-2026-ct-mu-fr-stents

## Bibliographic
- Title: Coronary computed tomography angiography–derived quantitative flow ratio of stented coronary vessels: comparison with invasive fractional flow reserve
- First author / authors (first 3 + et al.): Shota Naniwa, Takayoshi Toba, Hiroyuki Kawamori, et al.
- Year: 2026
- Venue: European Journal of Radiology 205 (2026) 113205
- DOI: 10.1016/j.ejrad.2026.113205

## One-line claim
Evaluates CT-μFR (Murray's law-based quantitative flow ratio from CCTA) for assessment of previously stented coronary vessels, addressing challenges of metal artifacts impairing segmentation and computational modeling.

## T6 targeted questions

- **Q-A geometry perturbation**: **YES. CRITICAL FOR M1 GATE**. Paper specifically addresses segmentation degradation in stented vessels: "stent-related blooming, beam-hardening, and partial-volume artifacts may impair lumen segmentation and physiologic computation." Study directly assesses feasibility of computational physiologic assessment despite segmentation challenges.

- **Q-B decision flip**: YES. Reports FFR threshold 0.80 decision: "A hemodynamically significant stenosis was defined as FFR ≤ 0.80." Diagnostic accuracy 80.7% (95% CI 68.1–90.0%) with "high sensitivity and negative predictive value but more modest specificity and positive predictive value."

- **Q-C BC tuning**: Uses CT-μFR (Murray's law-based, not explicit CFD BC discussion). Does NOT report boundary condition re-tuning or compensation strategy for artifact-induced segmentation error.

- **Q-D fidelity / quantity**: Uses CT-μFR computational method based on angiography (not full 3D CFD). Does NOT report WSS, OSI. Focus is on rapid on-site computation feasibility.

- **Q-E data**: 45 patients (57 vessels from stented lesions), single-center retrospective, invasive FFR gold standard, CCS population.

- **Q-F meshing**: **CRITICAL FOR GATE M1**. Extensively addresses segmentation robustness on poor geometry with metallic artifacts: "CCTA image quality was assessed...CT-μFR feasibility was assessed after software-based centerline and lumen-contour generation, visual review, and manual correction by experienced analysts. CT-μFR was considered non-evaluable when reliable lumen delineation or physiologic computation could not be achieved because of severe calcification, motion artifacts, indistinct lumen boundaries, or other major artifacts...Manual contour correction was performed by experienced analysts when blooming artifacts, calcification, image noise, or contour misregistration impaired automated lumen delineation."

## Novelty bearing on T6

- bucket: SUPPORT
- one-line reason: Demonstrates practical challenges and mitigation strategies for computational FFR assessment despite severe segmentation degradation from metallic artifacts in stented vessels; documents systematic approach to handling broken/poor geometry.
- verdict: LIGHT
- revisit-if: Paper analyzes whether computational method's accuracy degrades proportionally with segmentation difficulty or whether model robustness masks segmentation error impact.
