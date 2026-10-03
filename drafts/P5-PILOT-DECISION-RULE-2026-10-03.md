# P5 pilot: selection and decision rule (analysis side only, written 2026-10-03, before any P5 solve)

**Not for `cfd_handover/`.** This file quotes 0D FFR values for cohort scans (09-24 §7).

## Question
Scan 14 read 0.870 in 3D against 0.761 in 0D (requested radius), because the as-meshed lumen is wider along the whole
tree (median +0.14 mm). The 0D twin rebuilt on the area-equivalent radius gave 0.860, so the gap is the radius
definition, not the physics. If the shift is general, cases that are positive in 0D become negative in 3D, and E3
has few decisions that can flip. The pilot measures the shift on five more cases before the batch is sized.

## Selection (fixed rule, applied once)
From `CFD-SUBSET-FROZEN-2026-09-18.csv`: discrete 0D FFR in [0.70, 0.85), scan 14 excluded, ranked by |FFR − 0.80|.
Take the closest 1 LAD (LAD already has scan 14), 2 LCx and 2 RCA.

| scan | vessel | lesion | 0D FFR (discrete, requested radius) | cohort row |
|---|---|---|---|---|
| 138 | LAD | 20 mm 70 %DS | 0.802 | 100 |
| 69 | LCx | 20 mm 65 %DS | 0.810 | 109 |
| 473 | LCx | 20 mm 60 %DS | 0.850 | 111 |
| 272 | RCA | 10 mm 65 %DS | 0.811 | 68 |
| 139 | RCA | 10 mm 70 %DS | 0.773 | 67 |

Packages were exported 2026-10-03 with `export_cfd_case.py --instance <row> --error baseline --tier real` into
`drafts/packages_P5-2026-10-03/`. The exporter's no-predictions check passed.

## Analysis (run `code/m1_zerod_vs_3d.py`, adapted to resistance mode only, on each returned case)
Per case: Δ_def = FFR_3D − FFR_0D(requested) and Δ_phys = FFR_3D − FFR_0D(as-meshed area-equivalent twin), at the
measurement probe. Pool with scan 14 (n = 6).

## Decision rule
1. **Physics gap.** If |Δ_phys| ≤ 0.02 on at least 5 of 6, the 0D–3D difference is the radius definition and the
   ladder decomposition stands as designed. If not, the physics gap is real, and it becomes a finding to report.
   This does not stop the batch.
2. **Yield.** Let m = the median Δ_def over the 6.
   - **m ≤ 0.03:** keep the frozen subset and the batch design. Size the batch on the measured cost.
   - **m > 0.03:** the 3D bands are shifted. The operator chooses one of these before the batch is sized:
     (a) keep the subset, judge flips within each fidelity as pre-registered, and report the reduced 3D yield;
     (b) change the lesion construction so the as-meshed throat hits the target on the area-equivalent definition,
         which is a protocol amendment declared before the batch;
     (c) re-select the 3D subset on as-meshed twin FFR, which needs an extra mesh per candidate.
   No option is chosen in advance. The operator decides after seeing m and the six Δ_def values.
3. Gate failures (D2–D4) are counted and reported. They do not remove a case from this analysis.
