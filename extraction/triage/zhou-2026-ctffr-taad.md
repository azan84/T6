---
source_pdf_path: Resources/jeag052.pdf
slug: zhou-2026-ctffr-taad
ledger_status: TRIAGED
---

# zhou-2026-ctffr-taad

## Bibliographic
- Title: Evaluation of CT-FFR for predicting myocardial ischaemia in patients with type A aortic dissection
- First author / authors (first 3 + et al.): Feifei Zhou, Xinyan Zhou, Lei Yang
- Year: 2026
- Venue: European Heart Journal - Cardiovascular Imaging
- DOI: 10.1093/ehjci/jeag052

## One-line claim
CT-FFR as prognostic tool for post-operative MACE in type A aortic dissection (TAAD) patients; FFR ≤0.80 independently associated with 30-day adverse outcomes.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Studies pathophysiology of coronary compression in TAAD (intimal flap extension, false-lumen pressurization) but does not measure inter-segmenter disagreement or synthetic perturbation.
- **Q-B decision flip**: YES. Uses FFR ≤0.80 threshold; reports adjusted odds ratio 7.18 (95% CI 2.86–18.07, p<0.001) for 30-day MACE; combined model (CT-FFR + CCTA + clinical risk) AUC 0.783 with high sensitivity and NPV.
- **Q-C BC tuning**: NOT REPORTED. No discussion of boundary condition setting, outlet resistance, or BC tuning in TAAD context.
- **Q-D fidelity / quantity**: YES. CT-FFR applied to TAAD cases; no detail on reduced-order vs. 3D CFD; no WSS/OSI extraction.
- **Q-E data**: 154 TAAD patients enrolled, 140 underwent surgery, 34 (24.3%) experienced 30-day MACE; invasive catheterization/angiography not routine (risk of dissection propagation); CCTA primary imaging modality.
- **Q-F meshing**: NOT REPORTED. Mentions technical challenges of TAAD imaging (motion, dissection anatomy) but no meshing detail.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Clinical validation of CT-FFR in TAAD population; demonstrates decision-making value of FFR ≤0.80 in high-risk surgical candidates, but no novel computational methodology or error characterization.
- verdict: LIGHT
- revisit-if: Comparison of CT-FFR vs. CCTA alone for MACE prediction; subgroup analysis by dissection mechanism (ostial involvement, etc.); CFD model sensitivity to dissection geometry.
