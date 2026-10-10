# A6 — Territory granularity of the perfusion check (Protocols C and D)

Prefix `a6_territory`. Scripts: `code/a6_territory_run.py`, `code/a6_territory_compare.py`, `code/a6_territory_summary.py`. Outputs: `results/a6_territory-2026-10-09/`.

## 1. Design as run (fixed and written before the full run)

**Partition.**
- Level 1 (frozen): `ablation.territories()`, the subtree below each child of the first branching node of the clean tree (active children lists).
- Level 2: each level-1 subtree is walked down from its root through single-child nodes to its own first branching node *b*. If no such node exists (unbranched subtree), the level-1 territory is kept whole. Otherwise the trunk (the level-1 root down to and including *b*) is one territory and the subtree below each child of *b* is another. Including *b* in the trunk mirrors level 1, where the first branching node belongs to the (unassigned) root trunk.
- Targets are the clean model's full territory bed outflow, as frozen (decision B1). In the discrete bed non-leaf nodes carry no bed conductance, so a trunk territory has zero target and is dropped by the existing `q_clean > 0` rule, as the root trunk is. In the leaky bed a trunk territory has a positive target (wall outflow) and is a real territory.
- Corrupted nodes are assigned to the territory of their clean counterpart (frozen rule).

**Unperfused-territory rule.** A territory with a positive clean target and no surviving corrupted member enters the residual with predicted flow 0, i.e. relative error −1 (100% mismatch). It is not dropped. Under Protocol C it enters both the fitted loss (as a constant) and the reported residual. Under Protocol D it is excluded from the parameter vector (its multiplier would act on no node) and kept in the residual.

**Definedness.** Unchanged from the frozen run: C and D are computed only if the frozen level-1 rule (`q_clean > 0` and at least one surviving member) yields at least two territories. The wrapper calls the frozen `protocol_c_targets()` first; if it returns fewer than two territories it returns that list unchanged (so C and D are skipped exactly as before); otherwise it returns the configured partition. The set of defined instances is therefore identical and every comparison is paired. A Protocol C fit at the search bound remains a failure (frozen rule).

**Implementation.** `a6_territory_run.py` monkeypatches `ablation.protocol_c_targets` in each worker process and then calls the frozen `ablation.run_instance()` (Protocols A–C, unchanged code path). Protocol D is the frozen `ablation_per_territory.run_instance()` copied with one change: the parameter vector runs over territories with at least one member. With no empty territories this is identical to the frozen code. No frozen file is edited.

**Configurations.**
| Config | Partition | Empty territory | Role |
|---|---|---|---|
| L1drop | level 1 | dropped (frozen) | validation: must equal the frozen run |
| L1keep | level 1 | −1 in residual | isolates the 100%-mismatch rule |
| L2keep | level 2 | −1 in residual | **primary** |
| L2drop | level 2 | dropped | contrast only (shows the frozen rule at finer granularity) |

**Endpoints** (as Table I / Table S3): discrete arm restricted to the 97 eligible instances; rows with status ok (defined residual); pass = residual < 0.10; wrong = |ΔFFR| > 0.05; passes-and-wrong = both; P(wrong | pass) = passes-and-wrong / passes; flip = change of classification at 0.80. Topological = T1+T2, caliber = T3+T4. Wilson 95% intervals; exact McNemar (binomial on discordant pairs) for Level 2 vs frozen Level 1, paired on the same model.


## 2. Validation

- **L1drop vs frozen run, all instances, both beds.** All 3,728 A–C rows (`ablation-2026-10-07.csv`) and all 1,192 D rows (`ablation-perterritory-2026-10-08.csv`) match on status, and `ffr`, `dFFR`, `flip` and `outlet_flow_residual` are bit-identical in every row (0 differences, NaN = NaN). The wrapper and the re-implemented D fit therefore reproduce the frozen C and D exactly.
- **L1keep (100%-mismatch rule alone at Level 1).** Identical to the frozen run in every C and D row (0 differences in `ffr` and residual). No defined C or D model had an empty level-1 territory (`n_empty = 0` in all rows). This also holds for the 4 discrete and 8 leaky trees with three level-1 territories: no topological error in the cohort emptied one of three main-branch territories while leaving the other two. Confirmed: the frozen drop rule never mattered at Level 1.
- **Frozen baseline recomputed** with the summary script: discrete topological P&W 20/104 (C), 21/104 (D); leaky 14/171, 9/171; caliber 5%, 18% (discrete), 12%, 4% (leaky). These equal Table I and the IV-B text.
- **Pairing.** Under L2keep every one of the 921 defined C rows and 921 defined D rows (discrete eligible + leaky) is present in both runs; no Protocol C fit hit the search bound; all solves converged.

## 3. Results (L2keep, paired against frozen Level 1)

### 3.1 Territories per tree (positive clean target; discrete: 97 eligible instances; leaky: 150)

| Bed | Level 1 | Level 2 | Level 2 median (range) |
|---|---|---|---|
| Discrete | 2: 93, 3: 4 | 2: 20, 3: 22, 4: 51, 5: 4 | 4 (2–5) |
| Leaky | 2: 142, 3: 8 | 2: 30, 3: 3, 4: 30, 5: 24, 6: 55, 7: 8 | 5 (2–7) |

In the discrete bed every trunk territory has zero target and is dropped (counts including zero-target trunks: 2/4/6/7). In the leaky bed trunk territories carry wall outflow and count. Trees with 2 territories at Level 2 have unbranched main-branch subtrees.

### 3.2 Class level, % (Wilson 95% CI); n identical at both levels

| Bed | Class | Prot. | n | Pass L1 → L2 | Wrong L1 → L2 | P&W L1 → L2 | P(wrong \| pass) L1 → L2 | Flip L1 → L2 |
|---|---|---|---|---|---|---|---|---|
| Discrete | Topo | C | 104 | 38 → 23 | 62 → 63 | **19 (13–28) → 7 (3–13)** [20 → 7] | 20/39 51 (36–66) → 7/24 29 (15–49) | 19 (13–28) → 21 (14–30) |
| Discrete | Topo | D | 104 | 99 → 71 | 20 → 26 | **20 (14–29) → 3 (1–8)** [21 → 3] | 21/103 20 (14–29) → 3/74 4 (1–11) | 8 (4–14) → 11 (6–18) |
| Discrete | Cal | C | 194 | 88 → 89 | 5 → 5 | 5 (2–9) → 5 (3–9) [9 → 10] | 9/170 5 → 10/172 6 (3–10) | 8 (5–12) → 8 (5–12) |
| Discrete | Cal | D | 194 | 100 → 100 | 18 → 23 | **18 (13–24) → 23 (18–30)** [35 → 45] | 35/194 18 → 45/194 23 (18–30) | 11 (7–16) → 11 (7–16) |
| Leaky | Topo | C | 171 | 90 → 58 | 12 → 18 | 8 (5–13) → 5 (2–9) [14 → 8] | 14/154 9 (5–15) → 8/99 8 (4–15) | 8 (5–13) → 11 (7–16) |
| Leaky | Topo | D | 171 | 100 → 74 | 5 → 13 | 5 (3–10) → 2 (1–6) [9 → 4] | 9/171 5 (3–10) → 4/126 3 (1–8) | 6 (3–10) → 9 (5–14) |
| Leaky | Cal | C | 300 | 98 → 81 | 12 → 14 | 12 (9–17) → 12 (9–17) [37 → 37] | 37/294 13 (9–17) → 37/243 15 (11–20) | 4 (2–7) → 5 (3–8) |
| Leaky | Cal | D | 300 | 100 → 100 | 4 → 9 | **4 (2–7) → 9 (7–13)** [12 → 28] | 12/300 4 (2–7) → 28/300 9 (7–13) | 4 (2–6) → 4 (3–7) |

By type (L1 → L2 P&W): taper D 36% → 45% (discrete), 8% → 19% (leaky); taper C 9% → 10%, 24% → 24%; T3 0–1% at both levels. T1 discrete C 20% → 7%, D 23% → 2%; T2 discrete C 18% → 7%, D 18% → 3%; T1 leaky C 11% → 10%, D 4% → 0%; T2 leaky C 6% → 1%, D 6% → 4%.

### 3.3 Exact McNemar, Level 2 vs Level 1 (new / lost)

| Bed | Class | Prot. | P&W k L1 → L2 | +new / −lost | p | Flips L1 → L2 | +new / −lost | p |
|---|---|---|---|---|---|---|---|---|
| Discrete | Topo | C | 20 → 7 | 0 / 13 | 0.0002 | 20 → 22 | 3 / 1 | 0.63 |
| Discrete | Topo | D | 21 → 3 | 0 / 18 | <0.0001 | 8 → 11 | 10 / 7 | 0.63 |
| Discrete | Cal | C | 9 → 10 | 2 / 1 | 1.0 | 15 → 15 | 0 / 0 | 1.0 |
| Discrete | Cal | D | 35 → 45 | 10 / 0 | 0.002 | 21 → 21 | 0 / 0 | 1.0 |
| Leaky | Topo | C | 14 → 8 | 1 / 7 | 0.07 | 14 → 18 | 4 / 0 | 0.13 |
| Leaky | Topo | D | 9 → 4 | 2 / 7 | 0.18 | 10 → 15 | 9 / 4 | 0.27 |
| Leaky | Cal | C | 37 → 37 | 0 / 0 | 1.0 | 12 → 16 | 4 / 0 | 0.13 |
| Leaky | Cal | D | 12 → 28 | 17 / 1 | 0.0001 | 11 → 13 | 3 / 1 | 0.63 |

### 3.4 Mechanism (why topological P&W fell)

- **Unperfused territories.** At Level 2, 30 of 104 discrete and 45 of 171 leaky topological models have at least one territory with no surviving vessel (T1: 23/44 and 36/71; T2: 7/60 and 9/100). Their residual is ≥ 0.45 (discrete) and ≥ 0.38 (leaky), so none passes. But these models were mostly already failing or correct at Level 1: they account for only 2 of the 13 lost discrete C cases, 0 of 18 lost discrete D cases, and 1 of 7 lost in each leaky cell.
- **Finer targets within perfused territories** account for the rest. Under C the single global scaling cannot match the finer flow split, so 11 discrete (6 leaky) previously passing-and-wrong models now fail. Under D the extra per-territory parameters redistribute flow closer to the lesion, so 18 discrete (6 leaky) models still pass but are no longer materially wrong.
- So Fable's predicted direction holds, but the stated mechanism ("the missed branch formed its own territory and failed") explains a small minority of the fall. Do not use that sentence.
- **The remaining topological P&W at Level 2** (discrete 7 C, 3 D; leaky 8 C, 4 D) are all left-coronary models with every territory perfused. One instance (scan 812 LCX) remains P&W under both C and D in the discrete bed.
- **Contrast (L2drop, frozen drop rule at Level 2).** Discrete topological P&W 26% under both C and D; leaky 6% (C) and 13% (D, McNemar vs L1 p = 0.015). The drop rule at finer granularity makes the check blinder, as anticipated. The 100%-mismatch convention is therefore necessary for the result above. (Two discrete C fits hit the search bound under L2drop, n = 102.)
- **Taper.** Finer tuning does not help. Under D, more parameters force each sub-territory's clean flow through the narrowed lumen, which raises the pressure drop further. P&W rose significantly in both beds. Under C, P&W was unchanged; in the leaky bed fewer taper models passed (144 → 93) but P(wrong | pass) rose from 25% to 39%.
- **Protocol B at Level 2** (side result, on C-defined instances): discrete topological pass rate 22% → 17% (18/104); leaky 89% → 56% (95/171).
- **Not rerun at Level 2:** the simulated noise floor (3.1–3.9%, `negatives.py`). Compare the Level-2 rates with the floor with that caveat. The floor's own territory definition is Level 1.

## 4. What it means for the paper's claims

1. **Abstract, "19–20\% (discrete bed) and 5--8\% (leaky bed) of topological-error models ... passed a perfusion check", with "two or three main-branch territories".** The numbers stand as a conditional on main-branch territories, which the abstract already states in the Methods clause. They do **not** generalise to a finer check: at a once-more-split partition (median 4/5 territories) they fall to 3–7% (discrete) and 2–5% (leaky). The lower end is at the correct-anatomy floor of 3–4% (floor not recomputed at Level 2). Direction of change: the headline must be read, and ideally written, as main-branch-level. Recommended: keep the numbers and add a clause (see 5a). If the word budget forbids it, the Limitations sentence must carry it.
2. **Abstract, "and 4--18\% of caliber-error models, mostly taper".** Stands, and is strengthened: at Level 2 caliber P&W is 5–23%, almost all taper. Under D it rose significantly in both beds.
3. **Abstract last sentence, "A perfusion match after tuning did not certify the segmented branching or caliber."** Stands for caliber at both granularities. For branching it stands at main-branch level; at Level 2 it holds only for a residual 2–7%. Consider "...did not certify the segmented caliber, nor, at main-branch resolution, its branching" only if a rewrite is wanted. The current wording is defensible because residual topological P&W remains above zero in every cell.
4. **Limitations, "A segment-level perfusion check could detect errors within a main-branch territory that this one cannot."** Now measured. Replace it with the result: a finer check removed most topological passes-and-wrong but not taper (5a/5b).
5. **IV-B/Discussion, "in the discrete bed one in five tuned topological-error models passed while materially wrong under either form of tuning" and "20 of the 39 passing topological-error models were materially wrong".** These are main-branch statements. Add nothing there beyond the one Results sentence; the supplement carries the rest.
6. **Practical consideration 3, "only 22\% of re-derived topological-error models in the discrete bed passed"** (89% leaky). Level-1 statement; at Level 2 it is 17% and 56%. No change needed. It supports "record the mismatch before tuning" more strongly.
7. **Flip rates under C and D** do not change significantly at Level 2 (all McNemar p ≥ 0.13). Topological D flips are 11% (discrete) and 9% (leaky) against 8% and 6%. The "Per-territory tuning corrected the typical missed branch" sentence stands: median topological |ΔFFR| under D at Level 2 is 0.003 (discrete) and 0.005 (leaky), against 0.005 in both beds at Level 1.

## 5. Draft text

### (a) Main text (IV-B, after the Protocol D passes-and-wrong sentence; 2 sentences)

> With each main-branch territory divided again at its first bifurcation (a median of four territories in the discrete bed and five in the leaky bed, a territory left without a vessel counted as a 100\% mismatch), topological passes-and-wrong fell to 7\% (C) and 3\% (D) in the discrete bed and to 5\% and 2\% in the leaky bed, whereas caliber passes-and-wrong was unchanged under Protocol C and rose under Protocol D to 23\% and 9\%, almost all taper (Supplementary Material). The finer targets either failed the tuned topological-error model or restored its FFR; a branch left without a vessel accounted for few of these changes.

Limitations replacement for the segment-level sentence:

> A perfusion check with one further level of territories detected most topological errors that passed at main-branch level, but not taper errors (Supplementary Material).

Optional abstract clause (needs ~10 words cut elsewhere): after "against 3--4\% for correct anatomy." insert "; with finer territories, topological but not taper passes-and-wrong fell (2--7\%)". Alternatively insert "main-branch" before "perfusion check" (1 word: "passed a main-branch perfusion check").

### (b) Supplement paragraph and table

> \subsection{Territory Granularity}\label{sec:granularity}
> Protocols C and D were repeated with a finer partition. Each main-branch territory was divided again at its own first bifurcation. The vessel between the two bifurcations formed a territory of its own, and an unbranched main-branch territory was kept whole. A territory with a positive clean target and no surviving vessel entered the residual with a relative error of $-1$; under Protocol D it carried no parameter. Trunk territories had no bed outflow in the discrete bed and were omitted, as is the root trunk. Protocols C and D were run on the same models as at main-branch level, so all comparisons are paired. With the main-branch partition the procedure reproduced the original results exactly. Trees had a median of four (range 2--5) territories in the discrete bed and five (2--7) in the leaky bed, against two or three. Topological passes-and-wrong fell in the discrete bed under both protocols and in neither bed rose (Table~\ref{tab:gran}). A territory left without a vessel failed the check (residual $\geq 0.38$) in 30 of 104 discrete and 45 of 171 leaky topological-error models. Most of these models already failed or were correct at main-branch level. Most of the fall instead came from models with every territory perfused: under Protocol C the single scaling no longer matched the finer targets, and under Protocol D the additional parameters restored the FFR. Taper passes-and-wrong did not fall: under Protocol D it rose from 36\% to 45\% (discrete) and from 8\% to 19\% (leaky). Flip rates under C and D changed by at most five models per cell (McNemar $p \geq 0.13$). Had a territory without a vessel been omitted from the residual, topological passes-and-wrong would have risen to 26\% in the discrete bed.

```latex
\begin{table}[!ht]
\caption{Passes and Wrong, \% (Wilson 95\% Interval), at Main-Branch and Finer Territory Level}\label{tab:gran}
\centering\small
\begin{tabular}{@{}lllrccc@{}}
\toprule
Bed & Errors & Protocol & $n$ & Main branch & Finer & $p$\\
\midrule
Discrete & T1+T2 & C & 104 & 19 (13--28) & 7 (3--13) & $<0.001$ \\
Discrete & T1+T2 & D & 104 & 20 (14--29) & 3 (1--8) & $<0.001$ \\
Discrete & T3+T4 & C & 194 & 5 (2--9) & 5 (3--9) & 1.0 \\
Discrete & T3+T4 & D & 194 & 18 (13--24) & 23 (18--30) & 0.002 \\
Leaky & T1+T2 & C & 171 & 8 (5--13) & 5 (2--9) & 0.07 \\
Leaky & T1+T2 & D & 171 & 5 (3--10) & 2 (1--6) & 0.18 \\
Leaky & T3+T4 & C & 300 & 12 (9--17) & 12 (9--17) & 1.0 \\
Leaky & T3+T4 & D & 300 & 4 (2--7) & 9 (7--13) & $<0.001$ \\
\bottomrule
\end{tabular}
\\[3pt]
\parbox{0.85\textwidth}{\footnotesize Passes and wrong: perfusion residual below 10\% and $|\Delta\mathrm{FFR}| > 0.05$. Main branch: subtrees below each child of the first bifurcation (two or three per tree). Finer: each divided again at its own first bifurcation (median four, discrete; five, leaky). $n$ counts models with a defined residual, identical at both levels. $p$: exact McNemar test, paired by model.}
\end{table}
```

(The table is 8 rows, about 14 lines with caption and note; the paragraph is about 14 lines. Budget per FABLE-PLAN-AUDIT §6: +10 lines was allotted, so trim the paragraph's last two sentences if space is short.)

## 6. Runtime and files written

- Runs (3 workers, machine shared with other analyses): L2keep 1,433 s, L1drop 730 s, L1keep 684 s, L2drop 700 s; total ≈ 59 min.
- Scripts:
  - `code/a6_territory_run.py`: wrapper, monkeypatch and D fit
  - `code/a6_territory_compare.py`: row-level comparison with the frozen run
  - `code/a6_territory_summary.py`: endpoints, Wilson CIs and McNemar
- Outputs in `results/a6_territory-2026-10-09/` (8.4 MB):
  - `ablation_<cfg>.csv` and `perterritory_<cfg>.csv` for the four configurations
  - `territory_counts_<cfg>.csv`
  - `summary.txt`, `summary_by_class.csv`, `summary_by_type.csv`, `mcnemar_vs_frozen.csv`
  - `run_<cfg>.log`
- No frozen file was modified.
