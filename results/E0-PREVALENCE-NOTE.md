# Gate E0 — stenosis prevalence in ImageCAS-X (run 2026-09-18)

**Verdict: add the virtual-stenosis severity sweep.** The natural cohort cannot carry the decision-flip outcome alone.

## What was run
- Data: ImageCAS-X test split, 160 scans → 320 coronary trees (left + right), 73 scans disease-labelled. 0 failures, 391 s.
- Model: `code/zerod_ffr.py` v2 — steady 0D network, node per centreline point; Poiseuille on the actual radius;
  nonlinear expansion loss at resolved lesions; Murray-consistent distributed leakage; outlets calibrated on the
  healthy-equivalent tree; network truncated at r_ref < 0.50 mm; lesions and reported FFR restricted to r ≥ 0.75 mm.
- Radius: Euclidean distance transform of the lumen mask sampled at the centreline (no radius ships with the data).
- Two demand models × three scales: **Murray** Q = k·r_inlet³ (primary) and fixed **territory** flow by dominance.
- Self-test (ideal tapering vessel): FFR 0.967 clean, 0.918 at 50 %DS, 0.848 at 60 %, 0.691 at 70 % — the 0.80
  crossing falls in the 60–70 % band, as invasive FFR puts it.

## Result — min FFR over resolved main vessels, trees per band
| model | scale | median | <0.70 | 0.70–0.75 | 0.75–0.80 | 0.80–0.85 | 0.85–0.90 | ≥0.90 | in 0.70–0.90 |
|---|---|---|---|---|---|---|---|---|---|
| **murray** | **1.0** | **0.948** | 0 | 0 | 2 | 2 | 16 | 298 | **20** |
| murray | 0.7 | 0.964 | 0 | 0 | 0 | 2 | 2 | 314 | 4 |
| murray | 1.3 | 0.933 | 1 | 1 | 2 | 11 | 38 | 265 | 52 |
| territory | 1.0 | 0.905 | 13 | 11 | 28 | 48 | 53 | 165 | 140 |
| territory | 0.7 | 0.933 | 3 | 4 | 9 | 27 | 62 | 213 | 102 |
| territory | 1.3 | 0.876 | 31 | 22 | 42 | 43 | 60 | 120 | 167 |

Primary: **20 trees** in 0.70–0.90 (rule: ≥ 40), 4 in the flip-prone 0.75–0.85 band, 2 at or below 0.80.

> **Numbers refreshed 2026-09-18 (evening)** after two solver corrections — the lesion-cap removal (verification V9)
> and the lesion-placement rule (local maxima on the tree, true tree-distance merge; independent pre-flight review).
> The verdict has now survived both: 22 → 20 trees near threshold, still far below 40, and the flip-prone and
> at-threshold counts are unchanged at 4 and 2. **The conclusion that the severity sweep is required was never an
> artefact of either defect.** Superseded files retained for audit: `E0_prevalence_test_PRE-V9FIX.csv`,
> `E0_prevalence_test_PRE-LESIONRULE.csv`.

## Why — the anatomy, independent of any flow model
Tightest resolved main-vessel lesion per tree (175 of 320 trees have one ≥ 30 %DS):
30–40 %: 108 · 40–50 %: 50 · 50–60 %: 15 · 60–70 %: **2** · ≥ 70 %: **0**. Median 38 %, p90 50 %, max 62 %.
ImageCAS-X's "Disease: yes" is *any* calcified, non-calcified or mixed plaque seen by the analyst — not a
flow-limiting stenosis. Disease-labelled trees sit only slightly lower (median 0.944 vs 0.951). The right coronary
carries the tightest lesions (10 of the 12 lowest trees).

## Second finding — the demand model matters as much as the geometry
Murray vs fixed-territory demand moves the near-threshold count from **20 to 140**. The cohort's vessels are small
(median inlet radius 1.39 mm; Chinese cohort, conservative lumen masks, and a centreline ~1 voxel off-axis that
under-reads radius by ~10–15 %), so a fixed normal-heart flow forced through them inflates every pressure drop. The
truth plausibly lies between the two models. **This is on-theme**: it is a boundary-condition choice changing the
apparent disease prevalence sevenfold, with the anatomy held fixed (cf. Sommer 2020, Fossan 2025). WP-0 must choose
the demand model on principle (Murray self-scales and is consistent with the leakage model) and report sensitivity.

## Consequences for the design
1. **Severity sweep required:** insert controlled stenoses (40/50/60/70/80 %DS, fixed length, standardised
   proximal/mid locations) into real ImageCAS-X trees so baseline FFR densely spans 0.65–0.95. Real anatomy, real
   topology, controlled severity.
2. The natural cohort still carries the realism and the measured inter-observer disagreement.
3. Noise floor matters more than expected: 247/320 trees show ≥ 1 "lesion" ≥ 30 %DS, most of them mild — part of
   that is voxel-quantisation noise in mask-derived radii. Lesion detection thresholds belong in the frozen protocol.

## Data-handling facts established (undocumented upstream)
- Centrelines are **LPS**, NIfTI masks are **RAS** — negate x and y before applying inv(affine). Verified: 100 % of
  centreline points fall inside the lumen mask after the flip.
- **Raw EDT radius is correct**: agrees with the independent distance-to-surface-mesh measure to ~0.03 mm. A
  half-voxel "wall correction" is wrong here and inflates small-vessel resistance ~3.5×.
- **Ostial end-cap artefact:** the mask stops at the aorta, so EDT under-reads radius over the first ~4 mm of each
  tree; uncorrected, it caps the whole tree's healthy reference and halves the Murray demand.
- Polylines are disjoint branch-to-branch pieces; the loader uses a point graph and is indifferent either way.
