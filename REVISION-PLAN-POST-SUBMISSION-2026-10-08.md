# Paper 6 (T6) — analyses deferred to the revision (plan saved 2026-10-08)

Context: the JBHI SI submission is due 2026-10-15. The limit is 14 pages including the supplement; we are at main 8 + supplement 6 = 14.
These two items are the most likely major-revision requests (blind ARS review 2026-10-08: EIC W3, perspective W1–W3). Start them as soon as the paper is submitted, so the results are ready when reviews arrive. A revision may exceed 8 pages: pp. 9–10 cost $250/page, and the 14-page total still applies.

The grey-zone analysis (third deferred item) was **done 2026-10-08**: `code/grey_zone.py`, Table S6, one sentence in III-A.

---

## 1. Real segmentation-failure frequency (turns "impact" into "risk")

**Reviewer point.** The 32–33% decision-change rate is conditional on a T1/T2 error having occurred. How often do real segmentation methods produce missed side branches or vessel breaks at the lesion slots?

**Data route (updated 2026-10-08).** The paired inter-observer masks were declined (2026-09-18). The dataset authors will not send predictions: on 2026-10-08 Bransby replied that the model weights are public and the predictions should be generated from them. No training is needed.
- Weights: `pretrained_weights.zip` (1.6 GB) on the ImageCAS-X Zenodo record, DOI 10.5281/zenodo.21887809 (CC BY 4.0, v1). It holds the weights of all six benchmarked methods, trained on the 560-scan train split with the 160-scan test split held out.
- Code: `github.com/kitbransby/ImageCAS-X` (MIT). Disable the post-processing filter (`min_size = 100` in `postprocessing/steps.py`) and keep the **raw** output; the filter deletes the fragments and breaks being counted. Keep the filtered output as well, to report what the filter changes.
- CT volumes: ImageCAS on Kaggle (Apache 2.0), tens of GB. Download the 160 test scans at minimum.
- Methods: nnU-Net and CAS-Net first; add the other four benchmarked methods if time allows.
- GPU: inference only, a few hours for 160 scans × 2–6 methods.
- Store weights, volumes and predictions outside Drive: `~/Documents/Datasets/imagecas-x/weights/`, `~/Documents/Datasets/imagecas/`, `~/Documents/Datasets/imagecas-x/predictions/<method>/{raw,filtered}/`.
- Limitation to state: the methods are tested in-distribution, so the failure frequencies are a lower bound for scans from other centres.

**Analysis (new script `code/seg_failure_frequency.py`).**
1. Extract centerlines from the predicted masks with the same tool chain as ImageCAS-X (or VMTK). Match the predicted trees to the ground-truth trees by coordinate.
2. For every eligible host vessel / lesion slot in the swept set (6 944 instances; at minimum the 150-instance cohort), check two things:
   - T1-type: does the largest side branch beyond the lesion slot (r_ref ≥ 0.50/0.60 mm) exist in the prediction?
   - T2-type: does the host vessel continue at least 25 mm past the distal lesion edge?
3. Report per method and per vessel:
   - the frequency of each failure, with Wilson CIs
   - the DSC/HD95 of the same scans, to show that overlap does not predict them
   - clDice / Betti-0 error as a topology metric
4. Combine with the ablation:

   expected decision-change rate per case = P(error) × P(flip | error)

   Compute it separately for T1, T2, T3 and T4, using the inter-observer caliber error as the reference.

**Paper changes.**
- One paragraph in Results.
- One sentence in the abstract: "missed branches occurred in X% of slots for method M".
- A supplement table.
- Discussion IV-B gains real-data support for "overlap metrics do not measure".

**Effort.** About 2–3 days: the Kaggle download, a few hours of GPU inference, and the centerline extraction and tree matching, which carries most of the work.

**Risk.** If real failure rates are very low (< 2%), the clinical-risk framing weakens. Report it either way. The conditional finding (impact) stands regardless.

---

## 2. Throat-radius caliber error (T5)

**Reviewer point.** T3 (lesion +2.46 mm) and T4 (taper ×0.93) never perturb the throat, the most FFR-sensitive caliber quantity. The 3D twin already hints at this: an area-equivalent throat radius 0.045 mm wider (0.276 vs 0.231 mm) moved the baseline FFR from 0.761 to about 0.87, across 0.80.

**Magnitude (decide before running; record in the plan file with citations).**
- Primary: a throat-diameter error equal to the published inter-observer / CT-vs-QCA stenosis-grading variability, expressed as ±ΔDS. Candidate values to verify: about ±10 %DS or a ±0.1–0.2 mm diameter at the throat.
- Secondary: ±1/2 voxel (about ±0.16–0.2 mm diameter at ImageCAS resolution), which is defensible from the image alone.
- Run both signs, since an under-read throat (more severe) and an over-read throat (less severe) are both plausible.

**Implementation.**
- Add `T5_throat` to a copy of the error-type set in a new module (`error_types_t5.py`). Do not edit the frozen `error_types.py`.
- Re-insert the lesion with DS ± ΔDS, keeping the same length, centre and node set (trunc_ref pinned like T3/T4).
- Run A/B/C/D on the frozen cohort, about 15 min with the existing scripts:
  - `ablation.py` via a wrapper that swaps ERROR_TYPES
  - `ablation_per_territory.py`
- Analyse with `summarise_revision.py` and `grey_zone.py`. Both work unchanged once the error type is present.

**Expected outcome and how to report it.** T5 will likely flip decisions at rates near the topological errors, especially for under-read throats near 0.80. This refines the headline rather than overturning it: "branching and the throat carry the decision risk; caliber elsewhere does not". Report it whatever the result.
- Abstract and Conclusion change from "caliber errors" to "caliber errors away from the throat".
- Fix the denominators of the 3–6× ratio accordingly.

**Effort.** About 0.5 day of code plus runs, and about 0.5 day to find and cite the magnitude.

---

## Order of work after submission
1. T5 throat error. Cheap, and it removes the most obvious technical objection.
2. Download the ImageCAS test volumes and the ImageCAS-X pretrained weights; run nnU-Net and CAS-Net inference (raw and filtered output).
3. Segmentation-frequency analysis.
4. Hold both until the reviews arrive. Add them in the revision, with the response mapped in a fix log (simulated-review rule: no response letter for ARS findings; a real response letter only for real reviewers).
