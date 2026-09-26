---
source_pdf_path: Resources/ahmed-et-al-2021-prognostic-value-of-computed-tomography-derived-fractional-flow-reserve-comparison-with-myocardial.pdf
slug: ahmed-2021-prognostic-value
ledger_status: TRIAGED
---

# ahmed-2021-prognostic-value

## Bibliographic
- Title: Prognostic Value of Computed Tomography-Derived Fractional Flow Reserve Comparison With Myocardial Perfusion Imaging
- First author / authors: Ahmed Ibrahim Ahmed, Yushui Han, Mahmoud Al Rifai
- Year: 2021
- Venue: JACC: Cardiovascular Imaging, vol. 15, no. 2
- DOI: NOT REPORTED in extracted text

## One-line claim
Compares prognostic value of CT-angiography-derived machine-learning FFRct (ML-FFRct) versus SPECT myocardial perfusion imaging (MPI) for predicting incident cardiovascular death/MI and revascularization, finding MPI superior in a high-risk cohort.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No segmentation error or inter-observer variability analysis.
- **Q-B decision flip**: FFR threshold 0.80 used. Text: "ML-FFRct was <0.8 in at least 1 proximal/midsegment was present in 41.6% of patients." Reclassification metric reported: "the model with SPECT ischemia had higher global chi-square result and significantly improved reclassification." Implies FFR-based reclassification occurred but rate not explicitly quantified as a flip percentage.
- **Q-C BC tuning**: NOT REPORTED. ML-FFRct is a black-box machine-learning method; no BC parameterization or tuning strategy disclosed.
- **Q-D fidelity / quantity**: Machine-learning FFRct (data-driven, no explicit CFD/ROM). No spatially-resolved fields or WSS/OSI.
- **Q-E data**: Retrospective cohort from Houston Methodist (471 patients, N stated). Clinical data. Invasive FFR not mentioned as ground truth; outcomes (death, MI, revascularization) over 18-month follow-up.
- **Q-F meshing**: NOT APPLICABLE (machine-learning method, no mesh).

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Provides clinical outcome evidence that FFR-based decision thresholds (0.80) and reclassification matter for patient risk stratification; demonstrates that FFR estimation method (ML vs. physics) affects prognostic power—relevant to T6's hypothesis that segmentation error + BC tuning interact to influence clinical decisions.
- verdict: LIGHT
- revisit-if: If paper includes analysis of how segmentation or geometry quality impacts ML-FFRct accuracy, or sensitivity of ML-FFRct to inlet/outlet boundary conditions.
