---
source_pdf_path: Resources/jcdd-13-00308.pdf
slug: ayx-2026-ctffr-stenosis
ledger_status: TRIAGED
---

# ayx-2026-ctffr-stenosis

## Bibliographic
- Title: Feasibility of On-Site CT-FFR Analysis in Ruling Out In-Stent Restenosis on Cardiac PCCT
- First author / authors (first 3 + et al.): Isabelle Ayx, Felix Waßmer, Lena Lichti
- Year: 2026
- Venue: Journal of Cardiovascular Development and Diseases
- DOI: 10.3390/jcdd13070308

## One-line claim
Feasibility study of on-site (rapid) CT-FFR analysis using photon-counting detector CT to detect in-stent restenosis with sensitivity/NPV 100%.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Studies post-stent segments but does not measure inter-segmenter disagreement or synthetic perturbation.
- **Q-B decision flip**: YES. Uses FFR ≤0.80 threshold and Delta CT-FFR ≥0.06 cutoff; reports sensitivity 100%, specificity 76.5% for post-stent CT-FFR in 19 patients (2 ISR confirmed by ICA).
- **Q-C BC tuning**: NOT REPORTED. No description of how boundary conditions are set or adjusted; only mentions use of reduced-order models and machine learning for speed.
- **Q-D fidelity / quantity**: PARTIAL. Reduced-order or machine-learning methods for speed (on-site processing); no detail on CFD setup or spatially-resolved field extraction (WSS/OSI).
- **Q-E data**: 19 patients with prior coronary stents, PCCT imaging, ICA follow-up; pathological CT-FFR in 6/19 (31.6%), pathological Delta CT-FFR in 14/19 (73.7%).
- **Q-F meshing**: NOT REPORTED. Mentions metal artifact challenges and altered intra-coronary anatomy post-stent but no meshing strategy detail.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Rapid on-site CT-FFR methodology (reduced-order or ML-based) applicable to stented segments; high NPV for ISR exclusion may be reusable for T6's decision-flip assessment.
- verdict: LIGHT
- revisit-if: Details on reduced-order or ML method; sensitivity analysis of post-stent FFR to BC variation; robustness under poor image quality or metal artifact.
