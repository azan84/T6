# Severity-sweep cohort — specification (DRAFT v0.1, 2026-09-18)

**Status:** draft for WP-0. To be frozen, hashed and deposited with the rest of the protocol **before any Phase 2
(A/B/C ablation) run**. This document specifies *cohort construction* only — it produces baselines, not results.
**Why it exists:** Gate E0 (`results/E0-PREVALENCE-NOTE.md`) found that ImageCAS-X has no flow-limiting disease —
0 lesions ≥ 70 %DS in 320 trees, only 4 trees in the flip-prone 0.75–0.85 band. Decision flips cannot be studied where
no decision is near the threshold. The sweep inserts controlled stenoses into **real** trees so that baseline FFR
spans 0.65–0.95 densely, while anatomy and topology stay real.

## 1. Principle
One synthetic lesion per instance, inserted analytically into the radius profile of a real main vessel.
**Everything that defines the patient's physiology is computed from the ORIGINAL tree and frozen**: healthy reference
radius, Murray bed weights, and the calibrated bed constant C. The lesion changes the epicardial radius and nothing
else — a stenosis must not alter the microvascular bed or the flow demand. (This is the same separation the A/B/C
ablation later manipulates deliberately; here it is held fixed by construction.)

## 2. Eligible hosts
| Criterion | Value | Reason |
|---|---|---|
| Split | test (160 scans) first; train/val reserved for detector development (C3) | keeps the detector's training data disjoint |
| Image quality | ≥ 2 (of 1–4) | quality 1 = poor; recorded, used as a stratifier |
| Host vessels | LAD, LCx (left tree); RCA (right tree) | the three FFR-interrogated vessels |
| Vessel path | from the vessel's origin, following same-label nodes (largest healthy radius at forks), continuing past the label's end along the largest child to give run-off | |
| Healthy reference at lesion centre | r_fit ≥ 1.0 mm | host must be resolved (≈ 3 voxels) |
| Lesion window | entirely inside the same-label part of the path | |
| Run-off | measurement node exists **20 mm distal to the lesion's distal edge**, with r_fit ≥ 0.75 mm | clinical pressure-wire convention; resolved region only |
| Native disease | max native %DS between (window − 5 mm) and the measurement node < 40 % | the inserted lesion must dominate |
| Baseline | pre-insertion FFR at the measurement node ≥ 0.90 | start from a haemodynamically normal host |

## 3. Factors (full factorial per eligible host)
| Factor | Levels |
|---|---|
| Location (centre, from vessel origin) | proximal 20 mm · mid 45 mm (snapped to the nearest centreline node) |
| Length | 10 mm (focal) · 20 mm (long) |
| Severity, %DS relative to the healthy reference | 40 · 50 · 55 · 60 · 65 · 70 · 75 · 80 |

## 4. Lesion shape
Axisymmetric cosine narrowing, defined against the healthy reference so that %DS carries its clinical meaning:

    w(s)   = ½ [1 + cos(π (s − c) / (L/2))]      for |s − c| < L/2,   else 0
    r_new  = min( r ,  (1 − w) · r  +  w · r_fit · (1 − DS) )

At the centre r_new = r_fit · (1 − DS) exactly; outside the window the vessel is untouched; the vessel is never widened.

## 5. Haemodynamic model (frozen from E0)
`code/zerod_ffr.py` — steady 0D, node per centreline point, Poiseuille on actual radius, expansion loss
K = ρ·1.52/(2A0²)·(A0/As − 1)² at the throat, Murray distributed leakage, **Murray demand Q = k r_inlet³ (k = 562 s⁻¹)**
as primary with scale sensitivity 0.7 / 1.0 / 1.3, P_aorta = 90 mmHg, P_venous = 5 mmHg. C calibrated once per tree on
the healthy-equivalent network of the ORIGINAL geometry and reused for every instance of that tree.

## 6. Recorded per instance
scan, side, quality, dominance, disease label · vessel, location, snapped centre, length, %DS · r_fit at centre ·
distance to nearest upstream and downstream bifurcation, and whether a bifurcation lies inside the window (Gamage
stratifier for the missed-branch error type) · baseline FFR at the measurement node · post-insertion FFR at the
measurement node (**FFR_meas**, the primary baseline) and minimum over the resolved main vessel · inflow pre/post ·
solver iterations and convergence flag.

## 7. Selection into the Phase 2 cohort (after the sweep; seed fixed and recorded)
Six bands of FFR_meas: 0.65–0.70 … 0.90–0.95. Target 25 instances per band (150 total), sampled without replacement,
**at most 2 instances per tree and 1 per host vessel per band**, balanced across LAD / LCx / RCA as far as supply
allows. Shortfalls are reported, not padded. The natural-cohort trees run alongside unchanged.

## 8. Verification required BEFORE the cohort run (`severity_sweep.py --verify`)
| # | Check | Pass criterion |
|---|---|---|
| V1 | Insertion exactness | r_new(c)/r_fit(c) = 1 − DS to 1e-9; unchanged outside the window; never widened |
| V2 | Physiology frozen | r_ref, r_fit, bed weights and C bit-identical before and after insertion |
| V3 | Self-consistency | detected %DS at the throat equals the inserted %DS; K > 0 there |
| V4 | Severity monotonicity | FFR_meas strictly decreasing in %DS for every host × location × length |
| V5 | Length effect | FFR_meas(20 mm) ≤ FFR_meas(10 mm) at equal %DS |
| V6 | Mass balance | \|inflow − bed outflow\| / inflow < 1e-6 |
| V7 | Convergence | every solve converged; iteration counts reported |
| V8 | Resolution independence | halving the centreline spacing changes FFR_meas by < 0.005 |
| V9 | Demand invariance | inflow never rises after insertion |
| V10 | Regression | natural-cohort min-FFR reproduces `E0_prevalence_test.csv` after the solver refactor |

## 8b. Verification outcome — 2026-09-18
Run twice on disjoint scan sets before any cohort run: scans {3, 9, 14, 30, 41, 42} and {878, 844, 686, 396, 775, 993}
— 12 scans, 66 eligible slots, 528 instances.

**First run FAILED V1 and V3 at 2.9e-08** (tolerance 1e-9). Cause: the distance-transform volume is float32, the
sampled radii inherited that type, and the tree's radius array was silently single-precision while the healthy
reference was double — so writing the exact target r_fit·(1 − DS) rounded it. Physically negligible (~1e-7 in r⁴), but
mixed precision in a solver is a defect; the tolerance was **not** loosened. Fixed at both entry points
(`imagecasx_loader.radius_from_mask`, `zerod_ffr.Tree.__init__`), then the whole suite was re-run.

**Second run: all ten checks pass on both sets.** V1/V3 5.6e-17 and 1.1e-16 · V2 bit-identical · V4 0 violations in
462 steps · V5 0 in 264 pairs · V6 ≤ 5.2e-11 · V7 all converged, ≤ 28 iterations · V9 0 violations · V10 ≤ 0.0028.
**V8 passed marginally: 0.0039 and 0.0047 against 0.005.** It measures the whole pipeline's sensitivity to resampling
the centreline (healthy-reference fit and recalibration included, not solver discretisation alone), so ~0.005 FFR is
the honest noise floor of a single baseline value. Consequences: (i) baseline bands narrower than 0.05 are not
meaningful; (ii) Phase 2 compares protocols *within the same tree at the same discretisation*, so this error cancels to
first order in every paired difference.

## 8c. Scope of the cohort-construction run
The sweep evaluates every instance under the **primary model only** (Murray demand, scale 1.0). Cohort membership must
be defined under one model, otherwise the cohort itself becomes a function of the sensitivity analysis. The 0.7 / 1.3
flow-scale sensitivity of §5 is evaluated afterwards **on the selected instances**, and reported alongside.

## 8d. Cohort-construction outcome — 2026-09-18 (test split; `results/sweep_test.csv`, `…_rejections.csv`, `…_selected.csv`)
**Sweep:** 6,944 instances on 280 hosts (LAD 95 · LCx 67 · RCA 118) from 140 scans; 0 failures, 0 non-converged,
max mass error 7e-11, 326 s. Baseline FFR_meas median 0.977. Median FFR_meas by inserted severity:
40 % 0.956 · 50 % 0.931 · 55 % 0.909 · 60 % 0.873 · **65 % 0.818** · **70 % 0.733** · 75 % 0.616 · 80 % 0.467; share at or
below 0.80: 0 / 0 / 0 / 1.3 / 41.6 / 69.5 / 84.9 / 97.0 %. The 0.80 crossing sits at 65–70 %DS, where invasive FFR puts it.
**Supply per band** (0.65–0.95 in 0.05 steps): 369 · 355 · 508 · 651 · 991 · 1,604 — every band oversubscribed ≥ 14×.
**Rejections (944 slots):** host r_fit < 1.0 mm 740 · native ≥ 40 %DS 81 · measurement node unresolved 55 · window
outside same-label vessel 47 · run-off < 20 mm 13 · vessel absent 4 · baseline FFR < 0.90 4. Small host vessels are the
dominant constraint — the cohort's character again (E0: median inlet radius 1.39 mm).
**Selection:** **150 instances, 25 per band, no shortfall**; LAD 50 · LCx 50 · RCA 50; **108 trees, 93 patients**,
≤ 2 per tree. Length 10/20 mm: **80/70**. Image quality 2/3/4: **22/40/88**. Disease label no/yes: **89/61**.
Dominance R/L/Co: **125/8/17**. Host r_fit at the lesion: median 1.22 mm (1.00–1.84).

> **Corrected 2026-09-19.** These descriptors previously described the **pre-lesion-rule** cohort (LAD 48 · LCx 51 ·
> RCA 51; 107 trees, 85 scans; 76/74; 16/39/95; 95/55; 128/8/14). The lesion-rule fix of 2026-09-18 replaced 110 of
> the 150 selected instances, and this section was not regenerated with them. The numbers above are re-derived from
> `protocol/COHORT-FROZEN-2026-09-18.csv`, which is the hashed cohort of record. The sweep-level numbers in this
> section (6,944 instances, 280 hosts, supply, rejections) were regenerated and are correct.
> The cohort is identified by its **hashed instance list, never by "seed 20260918"** — `select()` is chaotic, so the
> seed is not a reproducible identifier (`STATISTICS-PLAN` §11). The phrase has been removed from this heading for
> that reason.

**Three things the selection exposes that Phase 1 must settle:**
1. **Location is unbalanced — proximal 104, mid 46.** Mid-vessel hosts more often fall under 1.0 mm. Selection did not
   stratify on location; decide whether it should.
2. **The upstream-branch stratum is thin as currently defined: 37 of 150** have a bifurcation between the vessel origin
   and the lesion, versus 118 with one downstream. But the definition is too narrow: for an LAD or LCx lesion the *sister
   vessel at the left-main bifurcation* is haemodynamically an upstream branch, and the vessel-origin-relative measure
   ignores it. Gamage's upstream/downstream stratification for the missed-branch error type (T1) must be defined on the
   whole tree, not the host vessel's own path.
3. **26 instances have a bifurcation inside the lesion window.** Kept and flagged (`bif_in_window`); decide whether
   bifurcation lesions are a stratum or an exclusion.

## 9. Known limitations (to state in the paper)
- Lesions are axisymmetric and analytic; eccentricity has no 0D representation (3D-only supplementary, if at all).
- One lesion per instance; serial-lesion interaction is out of scope.
- Inserted severity is exact, but the *host* radius is mask-derived at 0.3–0.4 mm voxels; hosts are restricted to
  r_fit ≥ 1.0 mm for that reason.
- Absolute FFR depends on the demand model (E0: 20 vs 140 near-threshold trees, Murray vs territory); the cohort is
  therefore defined on FFR under the frozen primary model and the sensitivity is reported.
