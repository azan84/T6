# Throat error at doubled and tripled hyperemic demand (2026-10-09)

Prefix `throat_demand`. No existing file was modified.

## 1. Design as run (fixed before the full run)

- **Error.** The half-voxel throat error only, both signs: `T5_vox_narrow` (throat diameter −½ voxel) and `T5_vox_wide` (+½ voxel), plus the pooled pair. The definition is unchanged from `t5_throat_error_types.py`: the voxel size is the scan's in-plane spacing; `trunc_ref` is pinned; DS is clipped to 5–95%. The ±10-point DS variant was not run, because the main text reports the half-voxel magnitude.
- **Demand and cohort.** `zerod_ffr.K_MURRAY = 562 × scale` (and `ablation.K_MURRAY`) is set in every worker before any tree is built (Pool initializer, with an assert in each task). Each scale uses its own re-selected cohort, `results/demand-replication-x{2,3}-2026-10-08/sweep_test_selected.csv`, with 150 instances each.
- **Beds.** ×2: leaky and discrete. The discrete arm is restricted to that folder's `discrete_arm_eligibility.csv`, which gives 47 eligible instances. ×3: leaky only, because only 17 instances are discrete-eligible, as in Table S5.
- **Protocols.** A–C use the frozen `ablation.run_instance`. D uses the frozen `ablation_per_territory.run_instance`. Both are called unchanged through the T5 patch, as in `t5_throat_run.one`.
- **Summary conventions.** These are unchanged from `summarise_revision.load/ci` and `t5_throat_summarise.grey/cell/sign_test`:
  - Wilson 95% CIs.
  - Passes-and-wrong (P&W): residual < 0.10 and |ΔFFR| > 0.05, counted over models with a defined residual.
  - Beyond zone: corrupted FFR outside 0.75–0.85.
  - Paired comparison: the exact sign test on per-instance flip proportions, T1+T2 against T5 (one sign, or the mean of both signs when pooled).
  - The topological comparator is the replication run's own T1+T2 at the same demand.
- **Inherited conventions.** C fits on the search bound are excluded. D fits on the bound are kept.

## 2. Validation

**Before the full run** (`results/throat_demand-2026-10-09/x{2,3}/validation.txt`), on 6 instances per scale:
- A zero-magnitude T5 type gave max |ΔFFR| = 0 and 0 flips under A, B, C and D.
- Clean FFR was bit-identical (max |diff| = 0.0) to the replication `ablation.csv`.
- D `ffr_clean` was bit-identical to the replication `ablation-perterritory.csv`.

**Full run** (`run.txt`):
- ×2: all 285 clean rows (150 leaky, 135 discrete) and all 285 D clean values were identical to the ×2 replication files (max |diff| = 0.0; no unmatched rows).
- ×3: all 150 leaky clean rows and 150 D values were identical.
- Because the ×2 and ×3 clean FFRs differ from those at k = 562, the exact match also confirms that the scaled demand took effect in the workers.

**Inserted throats:**
- 1,140 (×2) and 600 (×3) insertions.
- 0 needed clipping, and the realised throat DS equalled the applied DS in every case.

**Consistency check.** The T1+T2 and T3+T4 cells recomputed here reproduce every Table S5 entry, e.g. ×2 discrete topological flip under A = 50 (38–62), ×3 leaky = 33 (28–39).

## 3. Results

**Cohort at each demand:**

| Cohort | Median clean FFR | Median DS | Median \|ΔDS\| for ½ voxel (range) |
|---|---|---|---|
| ×2 discrete | 0.790 | 60% | 6.7 pp (4.6–8.7) |
| ×2 leaky | 0.802 | 55% | 7.3 pp (4.6–9.7) |
| ×3 leaky | 0.800 | 50% | 7.3 pp (4.5–9.8) |

- Every flip under A followed the sign of the error: 0 of 25, 0 of 88 and 0 of 86 flips went the other way.
- Protocol C: 1 failed fit (×2 discrete) was excluded. Protocol D fits on the bound were retained: 17 discrete and 2 leaky at ×2 (all narrowing), none at ×3.

### 3a. Pooled half-voxel throat error, flips / P&W, % (Wilson 95%)

| Bed | Protocol | k×1 (Table I) | k×2 | k×3 |
|---|---|---|---|---|
| Discrete | A, B | 30 / 29 | 27 (19–36) / 35 (26–45), n = 94 | — |
| Discrete | C | 38 / 57 | 31 (22–41) / 52 (42–62), n = 94 | — |
| Discrete | D | 40 / 80 | 34 (25–44) / 73 (64–81), n = 94 | — |
| Leaky | A, B | 36 / 42 | 29 (24–35) / 44 (39–50), n = 300 | 29 (24–34) / 48 (43–54), n = 300 |
| Leaky | C | 37 / 69 | 35 (30–40) / 69 (64–74), n = 300 | 34 (29–40) / 68 (62–73), n = 300 |
| Leaky | D | 38 / 81 | 35 (30–41) / 75 (70–80), n = 300 | 33 (28–39) / 72 (67–77), n = 300 |

Beyond zone, A, B: discrete 14 at ×1 → 12 (7–20) at ×2. Leaky 21 at ×1 → 12 (9–16) at ×2 → 9 (6–13) at ×3.

### 3b. By sign, flips / P&W, %

| Cohort | Protocol | Narrower (DS up) | Wider (DS down) |
|---|---|---|---|
| ×2 discrete | A, B | 15 (7–28) / 32 (20–46) | 38 (26–53) / 38 (26–53) |
| ×2 discrete | C | 15 / 49 | 47 / 55 |
| ×2 discrete | D | 15 / 79 | 53 / 68 |
| ×2 leaky | A, B | 23 (17–30) / 47 (39–55) | 36 (29–44) / 42 (34–50) |
| ×2 leaky | C | 23 / 75 | 46 / 63 |
| ×2 leaky | D | 23 / 85 | 47 / 65 |
| ×3 leaky | A, B | 24 (18–31) / 51 (43–59) | 33 (26–41) / 46 (38–54) |
| ×3 leaky | C | 27 / 69 | 41 / 67 |
| ×3 leaky | D | 27 / 81 | 39 / 63 |

For comparison, at k×1 under A: discrete 28 / 26 (narrower) and 32 / 32 (wider); leaky 25 / 43 and 47 / 41.

### 3c. Topological comparator at the same demand (Table S5; recomputed identically here), %

| Cohort | Flip A | Flip B | Flip C | Flip D | P&W B | P&W C | P&W D |
|---|---|---|---|---|---|---|---|
| ×1 discrete | 33 | 14 | 19 | 8 | 1 | 19 | 20 |
| ×2 discrete | 50 (38–62) | 14 | 20 | 8 | 6 | 14 | 20 |
| ×1 leaky | 32 | 5 | 8 | 6 | 5 | 8 | 5 |
| ×2 leaky | 34 (29–40) | 5 | 7 | 3 | 2 | 5 | 3 |
| ×3 leaky | 33 (28–39) | 5 | 6 | 6 | 4 | 7 | 4 |

The throat error exceeds the topological errors under B, C and D at every demand. Sign tests, pooled: ×2 discrete p ≤ 0.022; leaky p < 1e-15.

### 3d. Paired sign test, T1+T2 against throat (pooled), Protocol A

Columns: instances; mean per-instance flip proportion, topological vs throat; instances with topological > throat vs throat > topological; exact p.

| Demand | Bed | n inst | Topological vs throat | Topo > throat vs throat > topo | p |
|---|---|---|---|---|---|
| ×1 | discrete | 97 | 0.35 vs 0.30 | 34 vs 33 | 1.0 |
| ×1 | leaky | 150 | 0.33 vs 0.36 | 40 vs 48 | 0.46 |
| ×2 | discrete | 46 | 0.47 vs 0.27 | 23 vs 7 | **0.005** |
| ×2 | leaky | 149 | 0.35 vs 0.30 | 54 vs 38 | 0.12 |
| ×3 | leaky | 150 | 0.34 vs 0.29 | 50 vs 38 | 0.24 |

By sign under A:
- Narrower vs topological: p = 0.005 (×2 discrete), 0.001 (×2 leaky), 0.005 (×3 leaky). Topological is higher in each case.
- Wider vs topological: p = 0.06, 1.0, 1.0.

## 4. What it means for the claims

- **Holds:**
  - The half-voxel throat error flips about a third of decisions under fixed boundary conditions at every demand: 27–36% at k×1, 27–29% at k×2, 29% at k×3.
  - Tuning does not reduce it. It stays at 31–35% under C and D, against 3–20% for topological errors.
  - Tuned throat-error models pass the check while materially wrong in 52–75% (C and D) at higher demand, against 57–81% at k×1.
  - Every flip follows the sign of the error.
- **Does not hold in one cell:** the parity with topological errors. Main text, Results: "It flipped as often as the topological errors on the same instances (paired sign test, $p = 1.0$ and 0.46)". At ×2 the topological flip rate in the discrete bed rose to 50% while the throat rate stayed at 27% (p = 0.005). In the leaky bed parity holds at ×2 and ×3 (p = 0.12 and 0.24), although the throat rate is now numerically lower.
- **Direction of change:**
  - With demand, the narrowing sign flips less often in the discrete bed: 28% at ×1, 15% at ×2. The re-selected cohorts have milder lesions (median DS 60%/50%).
  - Flips beyond the grey zone fall (leaky 21% → 12% → 9%). The throat error's flips concentrate near 0.80 at physiological demand.
- **Wording.** The abstract's "the half-voxel throat error in 30–36%" next to "32–33%" for topological errors remains accurate at k = 562. No change is required at primary demand. The Robustness sentence should report the throat result at higher demand and qualify the parity.

## 5. Draft text (not applied)

**(a) Main-text sentence for the Robustness subsection** (after "...at twice the demand (Supplementary Material)."):

> At twice and three times the demand the half-voxel throat error changed the decision in 27--29\% of models with fixed boundary conditions and in 31--35\% after tuning, and 52--75\% of tuned throat-error models passed the perfusion check while materially wrong; it flipped less often than the topological errors in the discrete bed at twice the demand (27\% against 50\%, $p = 0.005$) and as often in the leaky bed ($p = 0.12$ and 0.24).

**(b) LaTeX row block for Table S7 (`tab:throat`), same column layout.** It is also in `results/throat_demand-2026-10-09/tab_throat_demand.tex`.

```latex
\addlinespace[2pt]
$\pm\tfrac12$ voxel, $k\times2$ & A, B & 94 & 27 (19--36) & 35 (26--45) & 12 (7--20) & 300 & 29 (24--35) & 44 (39--50) & 12 (9--16) \\
 & C & 94 & 31 (22--41) & 52 (42--62) & 13 (7--21) & 300 & 35 (30--40) & 69 (64--74) & 17 (13--21) \\
 & D & 94 & 34 (25--44) & 73 (64--81) & 18 (12--27) & 300 & 35 (30--41) & 75 (70--80) & 18 (14--22) \\
\addlinespace[2pt]
$\pm\tfrac12$ voxel, $k\times3$ & A, B & -- & -- & -- & -- & 300 & 29 (24--34) & 48 (43--54) & 9 (6--13) \\
 & C & -- & -- & -- & -- & 300 & 34 (29--40) & 68 (62--73) & 15 (12--20) \\
 & D & -- & -- & -- & -- & 300 & 33 (28--39) & 72 (67--77) & 14 (10--18) \\
```

The column header reads "Discrete bed (97 instances)", so the footnote needs this addition:

> $k\times2$, $k\times3$: demand constant doubled or tripled with the cohort reselected at that demand (Table~\ref{tab:repl}); discrete bed 47 instances at $k\times2$ and not analyzed at $k\times3$. Topological errors under Protocol A flipped 50\% (38--62\%) and 34\% (29--40\%) at $k\times2$ and 33\% (28--39\%) at $k\times3$.

## 6. Runtime and files written

- **Runtime:** ×2 739 s (300 tasks), ×3 444 s (150 tasks), 3 workers. Validation 21 s.
- **New scripts:**
  - `code/throat_demand_run.py`
  - `code/throat_demand_summarise.py`
- **Outputs in `results/throat_demand-2026-10-09/`:**
  - `x2/` and `x3/`: `validation.txt`, `run.txt`, `ablation_t5vox.csv`, `perterritory_t5vox.csv`, `t5vox_insert_log.csv`
  - `throat_demand_cells.csv`, `throat_demand_sign_tests.csv`, `throat_demand_notes.txt`, `tab_throat_demand.tex`
- **Cache:** `/private/tmp/claude-501/throat_demand_parts_x{2,3}/`
