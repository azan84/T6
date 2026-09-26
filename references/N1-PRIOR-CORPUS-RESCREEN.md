# N1 Novelty Gate: Prior Corpus Re-screening Against T6 Research Question

## Background

The N1 novelty gate for study T6 was originally applied only to 203 newly acquired papers. This document re-screens 14 previously extracted papers—drawn from an earlier segmentation-metrics extraction run—against the same four T6 contribution criteria. These papers were originally read for a different project and are now evaluated for whether they report evidence that might overlap with or threaten T6's four claimed contributions.

## Screening Criteria

Study T6 claims four contributions. For each paper, we assess whether it does any of the following:

**(a)** Derives geometric/segmentation error magnitudes from REAL measured inter-observer or inter-segmenter disagreement (as opposed to assumed or researcher-chosen values);

**(b)** Injects DISTINCT segmentation error TYPES separately—stenosis length, eccentric/off-axis lumen, missed side-branch or other TOPOLOGICAL error, taper/undersizing—rather than one global geometric parameter;

**(c)** Reports PER-CASE RECLASSIFICATION across a decision threshold (FFR 0.80 especially)—i.e., how many individual cases flipped side—as opposed to only aggregate accuracy/AUC or continuous error;

**(d)** RE-TUNES boundary conditions after a geometry change and tests whether that tuning absorbs/masks the geometric error (a tuned-vs-untuned comparison on the same corrupted geometry).

---

## Screening Results Table

| Paper Slug | Short Title | (a) | (b) | (c) | (d) | THREAT? | Reason |
|---|---|---|---|---|---|---|---|
| sankaran-2020-realtime-bloodflow | Physics-driven real-time CFD surrogates for FFR prediction | NO | NO | NO | NO | NO | Reduced-order model development; no segmentation error analysis. |
| kadem-2023-hemodynamic-modeling | Review of hemodynamic modeling, imaging, and ML in CVD | NO | NO | NO | NO | NO | Scoping review; acknowledges segmentation as critical but reports no empirical error propagation analysis. |
| donnelly-2018-ffrct-segmentation | On-site CT-FFR with inter-reader segmentation variability | PARTIAL | NO | NO | NO | PARTIAL | Inter-reader segmentation variation measured (ICC 0.90–0.95 on FFR output) but NO quantitative geometric error magnitudes reported; segmentation-level agreement metrics not provided. |
| nikopoulos-2024-coronary | Review of virtual hemodynamic assessment methods | NO | NO | NO | NO | NO | Literature review citing Donnelly et al. but not performing own empirical analysis. |
| yan-2024-ffr-cfd | Multi-dimensional CFD framework with 0D patient-specific BCs | NO | NO | NO | NO | NO | BC optimization via genetic algorithm; no segmentation error injection or sensitivity analysis. |
| menon-2024-coronary-blood-flow | Personalized coronary/myocardial models with CT perfusion | NO | NO | PARTIAL | NO | PARTIAL | Single explicit case-level reclassification reported (case 1 RCA: Murray's-law FFR below 0.80 threshold, MPICT-informed FFR above); full per-case breakdown across 6 cases not systematically tabulated. |
| yu-2021-ivus-ffr | IVUS-based FFR (UFR) diagnostic accuracy validation | NO | NO | NO | NO | NO | End-to-end clinical validation study; no segmentation error quantification. |
| yang-2023-hemodynamics | Angiography-derived FFR for intracranial atherosclerosis | NO | NO | NO | NO | NO | Diagnostic accuracy study; no segmentation sensitivity analysis. |
| liu-2022-coronary-ffr | Physiologically personalized outlet BC model for FFR-CT | NO | NO | NO | NO | NO | Compares patient-specific vs. LVM-based BCs; segmentation-error sensitivity acknowledged but not empirically quantified. |
| zhang-2023-physicsguided | Physics-guided deep learning for hemodynamic parameter regression | NO | NO | NO | NO | NO | ML surrogate for pressure/velocity prediction from morphology features; no segmentation error injection. |
| giannopoulos-2023-ffrct | High-speed on-site deep-learning FFR-CT diagnostic validation | NO | NO | NO | NO | NO | Clinical diagnostic-accuracy study; segmentation failure flagged as exclusion criterion (3.3%) but not analyzed. |
| mahbod-2021-cryonuseg | Nuclei instance segmentation dataset (histopathology) | N/A | N/A | N/A | N/A | NO | Off-topic; histopathology, not vascular/coronary imaging. |
| hu-2023-coronary-blood-flow | FAST: Physics-based fast FFR computation model | NO | NO | NO | NO | NO | Reduced-order hemodynamic model; segmentation used only as preprocessing with no sensitivity analysis. |
| he-2023-pulmonarystenosis | Non-Newtonian CFD simulation of pulmonary stenosis | NO | NO | NO | NO | NO | Single-patient case study of CFD/FSI; off-topic (pulmonary vs. coronary); no segmentation variability assessment. |

---

## Papers Requiring Full Read Before N1 Closes

### donnelly-2018-ffrct-segmentation
**Criterion (a) – PARTIAL**

The paper reports inter-reader (ICC 0.90) and intra-reader (ICC 0.95) agreement on CT-FFR values when two expert cardiologists independently corrected the same automatic segmentation. However, the extracted notes explicitly state: "No quantitative segmentation-difference measure (Dice, Hausdorff distance, mean/max diameter delta, or any direct geometric comparison of the two corrected lumen contours) is reported anywhere in the paper."

**What must be checked in the source PDF:**
Confirm whether the full paper (particularly Methods, Results, or Supplementary Materials) provides any direct quantification of inter-reader segmentation geometric error (e.g., per-point/per-segment contour distance, diameter discrepancy, or area difference), even if not highlighted in the abstract/main text. If found, criterion (a) may upgrade to YES.

### menon-2024-coronary-blood-flow
**Criterion (c) – PARTIAL**

The extracted notes report: "case 1 RCA showed Murray's-law FFR below the 0.80 ischemic threshold while MPICT-informed FFR was above it." This is exactly one explicit case-level reclassification across the FFR 0.80 threshold.

**What must be checked in the source PDF:**
Determine whether the paper systematically reports per-case reclassification counts across all 6 patient cases. Specifically: across the 6 patients, how many individual vessels/lesions flipped classification (above ↔ below 0.80 FFR threshold) when comparing Murray's law vs. MPICT-informed or image-only vs. image+synthetic boundary conditions? If a systematic cross-case tabulation is present, criterion (c) upgrades to YES.

---

## Conclusion

**No screened paper from this prior corpus directly threatens T6's novelty.** 

Two papers warrant full-read verification before N1 gate closure:
- **donnelly-2018**: For potential criterion (a) evidence (quantified geometric segmentation error from real inter-observer disagreement)
- **menon-2024**: For scope of criterion (c) evidence (systematic per-case reclassification across FFR 0.80 threshold)

Neither paper reports evidence of criteria (b) or (d). The corpus contains no study that injects distinct segmentation error types separately, nor any that compares tuned vs. untuned boundary conditions on corrupted geometries.
