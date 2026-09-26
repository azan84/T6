---
source_pdf_path: Resources/EIJ-D-20-00905_Westra.pdf
slug: westra-2021-ct-qfr
ledger_status: TRIAGED
---

# westra-2021-ct-qfr

## Bibliographic
- Title: One-step anatomic and function testing by cardiac CT versus second-line functional testing in symptomatic patients with coronary artery stenosis: head-to-head comparison of CT-derived fractional flow reserve and myocardial perfusion imaging
- First author / authors: Jelmer Westra, Zehang Li, Laust Dupont Rasmussen, Simon Winther
- Year: 2021
- Venue: EuroIntervention, vol. 17, pp. 576–583
- DOI: 10.4244/EIJ-D-20-00905

## One-line claim
CT-QFR (quantitative flow ratio from CTA) achieves diagnostic accuracy at least similar to myocardial perfusion imaging and CMR for detecting hemodynamically significant CAD in 358 patients with ≥50% diameter stenosis.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED; study measures natural variation in CTA quality (17% not feasible due to motion, calcium beaming, etc.) but does not systematically perturb geometry
- **Q-B decision flip**: YES – reports FFR classification: "35% of FFR measurements being ≤0.80"; paired CT-QFR and invasive FFR in 239 vessels; cutoff FFR ≤0.80 used
- **Q-C BC tuning**: Mentions "allometric scaling law" for resting flow; "simulated hyperaemic flow modelled from resting flow as boundary condition"; no discussion of re-tuning after geometry change or error masking
- **Q-D fidelity / quantity**: Reduced-order flow model (allometric scaling + Bernoulli); not full 3D CFD
- **Q-E data**: N=358 patients (284 with CT-QFR data), invasive FFR ground truth present
- **Q-F meshing**: NOT REPORTED; mentions semi-automatic lumen segmentation and "hierarchical tree structure" reconstruction but not volume meshing

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: QFR algorithm for fast coronary FFR computation; demonstrates method T6 could adopt, but no study of how BC tuning masks geometric error
- verdict: LIGHT
- revisit-if: Paper addressed sensitivity of QFR to segmentation error or whether BC assumptions absorb topological mistakes
