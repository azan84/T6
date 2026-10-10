# A5: tube-model overlap and topology metrics of the corrupted trees (2026-10-09)

## 1. Design as run

Fixed before the full run. Nothing was changed after the outcomes were seen.

- **Trees.** Every corrupted tree (T1–T4) was rebuilt for every cohort instance and both beds. The rebuild used the frozen `ablation.run_instance` path: the same error functions, `trunc_for` truncation (0.50 mm leaky, 0.60 mm discrete), T3/T4 node pinning, lesion insertion, and coordinate node matching (`node_map`). It was compared with the clean lesioned tree of the same bed.
- **Tube model.** Each network element (node v and its parent link) is a cylinder with radius r[v] (the lesioned radius) and length ds[v].
  - Intersection: |A∩B| = Σ over matched nodes of π·min(r_clean, r_corr)²·ds. This is the general formula. For nested trees it reduces to V_corr.
  - Two node sets:
    - **net**: the modelled network of the bed (active nodes). This is the primary set.
    - **full**: every centreline node with no truncation. This is the closest tube analogue of a mask.
- **Metrics** (all labelled "tube-model"):
  - **DSC over the cohort tree.**
  - **DSC over the whole scan.** The contralateral coronary tree is added unchanged to both volumes (same bed truncation for net, full centreline for full).
  - **clDice.** Tprec = corrupted centreline length inside the clean volume / corrupted length. Tsens = clean centreline length inside the corrupted volume / clean length. clDice = 2·Tprec·Tsens/(Tprec+Tsens).
  - **Betti-0** of the clean and corrupted networks.
  - **Volume lost.**
  - **Bed flow lost**: the share of the clean lesioned model's bed outflow on deleted nodes.
- **Outcomes.** Frozen `results/ablation-2026-10-07.csv`, status ok, Protocol A (`flip`, |ΔFFR| > 0.05) and Protocol B. Joined on (scan, side, vessel, loc, L_mm, ds_pct), bed and error type.
  - The discrete arm is restricted to the 97 eligible instances, as in Table I.
  - Topological denominators reproduce Table I: A 137 / 265; B 173 / 267.
- **AUC.** Rank-based (Mann–Whitney) and oriented so that a higher value is more suspicious: −DSC, −clDice, +flow lost.
  - Computed per bed: pooled over T1–T4, within topological errors (T1+T2), and within T1 and T2 alone.
  - 95% CIs from 2000 instance-level bootstrap resamples (all rows of an instance resampled together), seed 20261009.
  - The primary metric is net tree DSC. The secondary metrics are whole-scan DSC, clDice and flow lost.

## 2. Validation

- **Frozen code reproduces.** `ablation.run_instance`, called from the venv on 3 instances × 2 beds, gave Protocol A–C FFR identical to the frozen CSV (73 rows, max |diff| 1.1e-16).
- **Clean FFR.** The A5 script's clean FFR matches the frozen `ffr_clean` for all 298 instance-beds (max |diff| 0).
- **Corrupted trees are identical to the frozen ones.** For all 1,119 corrupted trees, `n_outlets`, `L_resolved_mm`, `w_sum` and `r_ref_root_mm` match the frozen B rows exactly (max relative diff 0). Status (solved or skipped) agrees in 1192/1192 rows.
- **Analytic check.** Coaxial cylinders with k = 0.930 give DSC 0.9276, which matches the 0.928 that T4 was derived from.
- **Nesting.**
  - **Node sets nest in every instance.** No corrupted node lacks a clean match. No matched clean node is inactive, and element lengths are equal.
  - **Radii nest everywhere except in the lesion window of some instances:**
    - T2 in 61/147 discrete and 62/149 leaky instances (max excess 0.041 mm);
    - T4 in 3 instances (max 0.008 mm).
  - **Cause of the exceptions.** All checked excess nodes lie in the lesion window. The corrupted tree re-fits its reference radius on the cut (T2) or partly scaled (T4) host segment (r_fit up to +1–4%). The re-inserted stenosis is therefore marginally milder.
  - **Consequence.** The general min-radius formula was used throughout. The nested formula 2V'/(V+V') differs from it by at most 0.0017.
- **Betti-0.** It is 1 for every clean and corrupted network. The change is 0 in all 1,119 trees. Every deletion removes a whole subtree, so in the tube model no fragment is left behind. A mask break that leaves a distal fragment would raise β0, and that case is not modelled.

## 3. Results

Medians (IQR) of tube-model metrics on the network set; discrete arm = 97 eligible instances. Flip and wrong are under Protocol A, as % with Wilson 95% CIs.

| Bed | Error | n | DSC tree | DSC scan | clDice | Bed flow lost % | n_A | Flip A % | \|ΔFFR\|>0.05 A % |
|---|---|---|---|---|---|---|---|---|---|
| Discrete | T1 | 77 | 0.975 (0.947–0.984) | 0.985 (0.977–0.991) | 0.940 (0.903–0.963) | 27.4 (14.2–43.2) | 77 | 27 (19–38) | 86 (76–92) |
| Discrete | T2 | 96 | 0.893 (0.701–0.937) | 0.935 (0.888–0.960) | 0.847 (0.544–0.907) | 30.1 (15.2–100) | 60 | 40 (29–53) | 88 (78–94) |
| Discrete | T3 | 97 | 0.996 (0.995–0.997) | 0.998 (0.998–0.998) | 1.000 | 0 | 97 | 7 (4–14) | 0 (0–4) |
| Discrete | T4 | 97 | 0.971 (0.947–0.981) | 0.983 (0.974–0.989) | 1.000 | 0 | 97 | 13 (8–22) | 6 (3–13) |
| Leaky | T1 | 118 | 0.969 (0.946–0.980) | 0.983 (0.975–0.990) | 0.930 (0.899–0.957) | 9.1 (5.5–17.2) | 118 | 18 (12–26) | 42 (33–51) |
| Leaky | T2 | 149 | 0.895 (0.721–0.936) | 0.934 (0.886–0.962) | 0.855 (0.517–0.899) | 13.5 (6.6–55.5) | 147 | 43 (35–51) | 80 (73–86) |
| Leaky | T3 | 150 | 0.997 (0.995–0.998) | 0.998 (0.998–0.999) | 1.000 | 0 | 150 | 2 (1–6) | 0 (0–2) |
| Leaky | T4 | 150 | 0.972 (0.951–0.981) | 0.983 (0.976–0.988) | 1.000 | 0 | 150 | 9 (6–15) | 7 (4–12) |

**T2 by host vessel.**

| Bed | Host | n | DSC tree, median (range) | DSC scan, median (range) | clDice | Flip A % |
|---|---|---|---|---|---|---|
| Discrete | RCA | 36 | 0.629 (0.458–0.839) | 0.854 (0.737–0.950) | 0.49 | no A row (no bed left) |
| Discrete | left | 60 | 0.915 (0.799–0.998) | 0.953 (0.898–0.999) | 0.90 | 40 (29–53) |
| Leaky | RCA | 50 | 0.623 (0.439–0.910) | 0.862 (0.740–0.967) | 0.45 | 50 (36–64) |
| Leaky | left | 99 | 0.915 (0.768–0.998) | 0.954 (0.854–0.999) | 0.88 | 39 (30–49) |

For T1, RCA and left hosts have similar DSC (0.96–0.98).

**Full-centreline set (no truncation).** Medians are within 0.006 of the network set in every cell. For example, T1 is 0.969/0.969 and T4 is 0.970/0.972 for discrete/leaky.

**T4 above 0.928.** The tube DSC of T4 is 0.971 (discrete) and 0.972 (leaky). This is because the 0.930 radius scale applies only from the lesion's proximal edge onwards, which covers a median 43% (IQR 28–75%) and 40% (28–69%) of the clean network volume. The proximal tree and the side branches proximal to the lesion keep their radius. Scaling the whole tree would give exactly 0.928.

**T1 against T4 within instance (tree DSC).**
- Discrete: T1 − T4 median +0.004, T1 lower in 29/77 instances, Wilcoxon p = 0.027. T1 is marginally *higher*.
- Leaky: +0.000, T1 lower in 59/118, p = 0.59.
- Meanwhile T1 flips 2× as often as T4 (27 vs 13%, 18 vs 9%). It is materially wrong 7–14× as often (86 vs 6%, 42 vs 7%).

**Decision-changing topological errors that the overlap score rates as good.** Among topological errors that flipped under A, the share with a whole-scan DSC ≥ 0.928 (the inter-observer agreement) was:
- 41/45 = 91% (79–96) in the discrete bed;
- 52/84 = 62% (51–72) in the leaky bed;
- for T1 alone, 21/21 discrete and 19/21 leaky.

**AUC** (instance bootstrap 95% CI), Protocol A flip. Each cell gives the AUC for the leaky bed, then for the discrete bed.

| Subset | DSC tree | DSC scan | clDice | Flow lost |
|---|---|---|---|---|
| Pooled T1–T4 | 0.79 (0.74–0.83) / 0.65 (0.57–0.72) | 0.79 / 0.65 | 0.78 / 0.68 | 0.76 / 0.68 |
| Topological (T1+T2) | 0.70 (0.65–0.76) / 0.54 (0.44–0.65) | 0.70 / 0.53 | 0.67 / 0.51 | 0.63 / 0.55 |
| T1 only | 0.65 (0.50–0.78) / 0.39 (0.23–0.55) | 0.61 / 0.38 | 0.59 / 0.39 | 0.72 / 0.57 |
| T2 only | 0.60 (0.50–0.68) / 0.58 (0.43–0.72) | 0.59 / 0.55 | 0.59 / 0.53 | 0.55 / 0.59 |

**AUC for |ΔFFR| > 0.05 under A, tree DSC.**
- Pooled: 0.86 (0.83–0.89) leaky; 0.75 (0.71–0.79) discrete.
- Topological: 0.76 (0.70–0.82) leaky; 0.47 (0.32–0.63) discrete.
- clDice and flow lost, pooled discrete: 0.93 and 0.94. This mostly separates topological from caliber errors, because T3/T4 have clDice 1 and no flow lost.

**Protocol B flip, tree DSC.**
- Pooled: 0.62 (0.45–0.76) leaky; 0.61 (0.53–0.69) discrete.
- Topological: 0.54 (0.37–0.68) leaky; 0.58 (0.46–0.70) discrete.

All numbers are in `results/a5_overlap-2026-10-09/auc.csv`.

**Answers to the key questions.**
1. **Does DSC separate T1 from T4?** No. The medians are 0.975 vs 0.971 (discrete) and 0.969 vs 0.972 (leaky), and the paired difference is ≈0. T1 changes the decision twice as often and is materially wrong 7–14× as often. Fable's sample (0.977 / 0.974) is confirmed.
2. **Do RCA breaks lower DSC strongly?** Yes. Tree DSC has a median of 0.62–0.63 (range 0.44–0.91). The whole-scan DSC is 0.85–0.86 (0.74–0.97). Left-tree breaks give 0.915 tree and 0.953 whole-scan, which is above inter-observer agreement. Fable's 0.52–0.72 is the central part of the RCA distribution.
3. **Does DSC rank error types by decision risk?** Only at the extremes.
   - Leaky, by DSC: T2 (0.895) < T1 (0.969) ≈ T4 (0.972) < T3 (0.997). By flip rate: T2 43% > T1 18% > T4 9% > T3 2%.
   - Discrete, by DSC: T2 < T4 < T1 < T3. Here T1 is ranked as less damaged than T4 although it flips twice as often.
   - The pooled AUC (0.65–0.79) comes from T2 against T3. Within topological errors DSC is near chance in the discrete bed (0.54) and modest in the leaky bed (0.70). Within T1 it is uninformative.
   - clDice and bed flow lost do no better within topological errors (0.51–0.67).

## 4. What it means for the paper's claims

- **IV-B:** "Vessel breaks occur in the output of current segmentation methods despite high overlap scores [bransby2026], and a missing side branch removes few voxels, so the error types that carried the decision risk here are the ones that the usual overlap metrics do not measure, although topology-aware measures such as clDice exist"
  - "A missing side branch removes few voxels" **stands**: T1 removes 5–6% of tree volume, and the tree DSC is 0.97, equal to the taper's.
  - "Vessel breaks … despite high overlap scores" **must change for our breaks**. A 25-mm-distal break lowers tree DSC to a median of 0.89, and to 0.62 in the RCA. The Bransby observation may stay as a citation about real outputs, but it is not what our numbers show.
  - "The error types that carried the decision risk … are the ones that the usual overlap metrics do not measure" is **half right**. DSC does fall for T2. It does not distinguish T1 from T4, and it does not rank risk within topological errors.
  - "clDice exists" is now measured. clDice flags the topological class (it is 1.000 for T3/T4) but does not rank its risk (within-topological AUC 0.51–0.67).
- **IV-C first consideration:** "because overlap scores do not reveal these errors". This is **too strong for breaks**. It holds for missed branches, whose DSC matches the taper's. Reword to the T1/T4 fact.
- **Conclusion:** "a check of the branching near the lesion, which overlap scores miss". This **stands only in a weaker form**. Most decision-changing topological errors (91% discrete, 62% leaky) still had a whole-scan DSC above inter-observer agreement, but RCA breaks are visible to DSC. Use "which an overlap score does not rank by decision risk".

## 5. Draft text

**(a) Main text** (each the same length or shorter than the current text)

- **IV-B** (replaces the whole sentence, ≈ −10 words). The current `bransby2026` citation can be dropped here; it is already cited in the Introduction and Methods.
  > In a tube model of each tree, the missed branch and the taper had the same median DSC (0.97), although the missed branch changed the decision about twice as often; a vessel break lowered DSC (median 0.89; 0.62 in the right coronary artery), and clDice \cite{shit2021} fell only for topological errors, without ranking their risk.

- **IV-C first consideration** (replaces the "because…" clause):
  > ..., because a missed branch leaves the overlap score as high as a taper does.

- **Conclusion** (replaces "which overlap scores miss"):
  > a check of the branching near the lesion, which overlap scores do not rank by decision risk, and

- **Optional II/III caption clause for T4**, if a reviewer asks about 0.928:
  > the applied taper gives a tube-model DSC of 0.97 because it narrows only the 40\% of tree volume beyond the lesion.

**(b) Supplement paragraph**

> Overlap and topology of the corrupted trees. Each network was represented as cylinders of the node radius and element length, and every corrupted tree was compared with its clean lesioned tree in the same bed (tube model; a voxel mask would differ at partial-volume level). Corrupted node sets were contained in the clean ones for all four error types; radii were contained except in the lesion window of some T2 and T4 trees (at most 0.04~mm), so the intersection was taken as the smaller radius on matched nodes. No error changed the number of connected components. Table~S\ref{tab:overlap} gives the medians. The missed branch and the taper had the same DSC, although the missed branch changed the decision under Protocol A about twice as often; a vessel break in the right coronary artery lowered tree DSC to a median of 0.62. Of the topological errors that changed the decision, 91\% (79--96\%) in the discrete bed and 62\% (51--72\%) in the leaky bed had a whole-scan DSC at or above the inter-observer value of 0.928. With instance-level bootstrap CIs, the AUC of tree DSC for a Protocol A decision change was 0.79 (0.74--0.83) leaky and 0.65 (0.57--0.72) discrete across all error types, and 0.70 (0.65--0.76) and 0.54 (0.44--0.65) within topological errors; clDice and the share of bed flow lost did not exceed these within topological errors. The applied taper gives a DSC above 0.928 because it narrows only the tree beyond the lesion's proximal edge (median 40\% of the tree volume).

**(b) LaTeX table body** (`supplement_tables/tab_overlap.tex` style; caption: "Tube-Model Overlap of Corrupted Trees, Median (IQR), and Protocol A Decision Changes")

```latex
\begin{tabular}{llrcccrr}
\toprule
Bed & Error & $n$ & DSC, tree & DSC, scan & clDice & Flow lost (\%) & Flip A (\%) \\
\midrule
Discrete & T1 & 77 & 0.975 (0.947--0.984) & 0.985 (0.977--0.991) & 0.940 (0.903--0.963) & 27 (14--43) & 27 (19--38) \\
 & T2 & 96 & 0.893 (0.701--0.937) & 0.935 (0.888--0.960) & 0.847 (0.544--0.907) & 30 (15--100) & 40 (29--53)$^a$ \\
 & T3 & 97 & 0.996 (0.995--0.997) & 0.998 (0.998--0.998) & 1.000 & 0 & 7 (4--14) \\
 & T4 & 97 & 0.971 (0.947--0.981) & 0.983 (0.974--0.989) & 1.000 & 0 & 13 (8--22) \\
Leaky & T1 & 118 & 0.969 (0.946--0.980) & 0.983 (0.975--0.990) & 0.930 (0.899--0.957) & 9 (6--17) & 18 (12--26) \\
 & T2 & 149 & 0.895 (0.721--0.936) & 0.934 (0.886--0.962) & 0.855 (0.517--0.899) & 14 (7--56) & 43 (35--51) \\
 & T3 & 150 & 0.997 (0.995--0.998) & 0.998 (0.998--0.999) & 1.000 & 0 & 2 (1--6) \\
 & T4 & 150 & 0.972 (0.951--0.981) & 0.983 (0.976--0.988) & 1.000 & 0 & 9 (6--15) \\
\midrule
\multicolumn{3}{l}{T2, right coronary} & 0.62--0.63 & 0.85--0.86 & 0.45--0.49 & & \\
\bottomrule
\multicolumn{8}{l}{\footnotesize Flip A: Wilson 95\% CI. $^a$ $n = 60$; right coronary breaks leave no discrete outlet under Protocol A.}
\end{tabular}
```

## 6. Runtime and files written

- `code/a5_overlap_metrics.py` computes the metrics. It took 853 s with 3 workers on a heavily loaded machine (load average about 260).
- `code/a5_overlap_analysis.py` does the join, medians and bootstrap AUC, in about 1 min.
- `results/a5_overlap-2026-10-09/`:
  - `overlap_metrics.csv` (1492 rows)
  - `overlap_joined.csv`
  - `medians.csv`
  - `medians_by_host.csv`
  - `auc.csv`
  - `analysis.log`
  - `run.log`
- Scratch checks are in `/private/tmp/claude-501/a5scripts/` (frozen-FFR reproduction and lesion-window excess).
