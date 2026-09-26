---
source_pdf_path: Resources/s10439-025-03810-2.pdf
slug: yu-2025-cerebral-ffr
ledger_status: TRIAGED
---

# yu-2025-cerebral-ffr

## Bibliographic
- Title: A Novel Method for Functional Assessment of the Stenosis of the Anterior Cerebral Circulation
- First author / authors (first 3 + et al.): Long Yu, Deyuan Zhu, Yunhan Cai et al.
- Year: 2025
- Venue: Annals of Biomedical Engineering
- DOI: 10.1007/s10439-025-03810-2

## One-line claim
- Blood fractional flow reserve (BFFR) based on CFD flow ratio (stenosed vs. post-repair geometry) provides functional assessment of cerebral anterior circulation stenosis with better accuracy than diameter-based metrics.

## T6 targeted questions
- **Q-A geometry perturbation**: Creates synthetic post-repair (non-stenosed) geometry by interpolating centerline radii; not real inter-observer data. 9 patient cases with CTA-based segmentation.
- **Q-B decision flip**: Does not compute binary threshold metric; reports BFFR values (flow ratio) and classification into mild vs. moderate-severe stenosis categories. In vitro and CTP validation but no ischemic outcome prediction.
- **Q-C BC tuning**: Develops cerebral microartery bifurcation model to compute patient-specific outlet resistance. Bifurcation coefficient γ calibrated from Doppler ultrasound flow data. Outlet BCs adjust per patient based on microarterial model. NO evidence of re-tuning after geometry repair or compensation hypothesis.
- **Q-D fidelity / quantity**: 3D CFD (Navier-Stokes, steady-state) with microarterial tree model for outlets. Computes total flow, pressure, BFFR (flow ratio). No local WSS/OSI or tissue perfusion fields.
- **Q-E data**: 9 patient cases from Shanghai Fourth People's Hospital with CTA, Doppler ultrasound, brachial pressure, CTP. Retrospective; no invasive FFR ground truth. N=9 (underdeveloped posterior communicating arteries).
- **Q-F meshing**: CTA segmentation (Mimics Research 20.0); surface smoothing (Geomagic Wrap); unstructured tetrahedral mesh (~1.7M elements). No explicit robustness testing; limitation noted: 0.5 mm spatial resolution limits severe stenosis modeling.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Cerebral artery domain, not coronary; BFFR uses flow ratio (not invasively measured pressure like FFR); no relevance to coronary diagnosis or T6's error-ranking hypothesis.
- verdict: LIGHT
- revisit-if: Methodology (microarterial outlet model) may be transferable to coronary if adapted; revisit if T6 pursues bifurcation-based resistance estimation.
