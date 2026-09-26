---
source_pdf_path: Resources/1-s2.0-S1097664725001012-main.pdf
slug: shergill-2026-concord-protocol
ledger_status: TRIAGED
---

# shergill-2026-concord-protocol

## Bibliographic
- Title: Cardiovascular magnetic resonance versus coronary computed tomography angiography with fractional flow reserve for diagnosing obstructive coronary artery disease in higher risk patients: rationale and design of CONCORD—A prospective, single-center diagnostic accuracy study
- First author / authors: Simran Shergill, Mohamed Elshibly, Kelly S. Parke
- Year: 2026
- Venue: Journal of Cardiovascular Magnetic Resonance
- DOI: https://doi.org/10.1016/j.jocmr.2025.101939

## One-line claim
CONCORD is a prospective study protocol (N=300 patients) comparing diagnostic accuracy of CMR vs. CCTA/FFRCT for detecting obstructive CAD (invasive FFR reference), with secondary outcomes on hybrid imaging and quantitative perfusion.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT ADDRESSED in protocol. Study does not include systematic perturbation or measurement of inter-observer CCTA segmentation variability.
- **Q-B decision flip**: IMPLIED. Study uses invasive FFR ≤0.80 as reference standard for significant CAD; diagnostic accuracy of CMR and CCTA/FFRCT will be compared. No pre-specified analysis of decision reclassification due to segmentation error.
- **Q-C BC tuning**: NOT DISCUSSED. Protocol outlines imaging acquisition and invasive FFR reference, but does not detail FFR-CT algorithm or BC boundary condition strategies, tuning protocols, or adaptation to geometry changes.
- **Q-D fidelity / quantity**: Two modalities: CMR (stress perfusion, myocardial blood flow quantification, scar imaging) and CCTA/FFRCT (coronary anatomy + CFD-based FFR). CMR yields quantitative MBF; CCTA/FFRCT computes FFR. NO explicit WSS/OSI measurement.
- **Q-E data**: N=300 consecutive patients (target); single center (Glenfield Hospital, Leicester, UK). Invasive FFR as gold standard (planned ICA). Study protocol phase; prospective recruitment ongoing.
- **Q-F meshing**: NOT DISCUSSED. Study protocol does not detail CCTA segmentation-to-surface-to-mesh pipeline or meshing robustness assessment.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Diagnostic accuracy comparison study using FFR ≤0.80 as decision threshold; establishes clinical context for T6's FFR-based outcome measures but does not address geometric uncertainty or BC tuning strategies.
- verdict: LIGHT
- revisit-if: Outcomes paper reports correlation between CCTA quality/segmentation variability and FFR-CT vs. invasive FFR disagreement, or subgroup analysis by stenosis morphology.

