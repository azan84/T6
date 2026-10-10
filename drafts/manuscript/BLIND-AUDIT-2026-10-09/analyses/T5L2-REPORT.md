# T5-L2 report: throat caliber error with finer perfusion territories (2026-10-09)

## 1. Design as run (written before the full run)

- Error types: the four T5 variants exactly as in T5-REPORT (DS ±10 pp; throat diameter ∓½ voxel), each sign separately and each magnitude pooled over both signs.
- Partition: Level 2 of A6 (each main-branch territory divided again at its first bifurcation; trunk its own territory; zero-target trunks dropped), with the unperfused-territory = 100% mismatch rule (A6 config `L2keep`). Level 1 = A6 `L1drop`, which A6 showed equals the frozen run.
- Protocols: A–C from the frozen `ablation.run_instance`; D from `a6_territory_run.run_d`. The residual of A and B is computed against the configured partition by the frozen code (`protocol_c_targets` serves every protocol), so A and B FFR are unchanged and only their residual moves.
- Endpoints (Table I / A6 conventions): discrete arm = 97 eligible instances; leaky = 150; rows with status ok; pass = residual < 0.10; wrong = |ΔFFR| > 0.05; P&W = both; P(wrong | pass) = P&W / passes; flip at 0.80. Wilson 95% CIs. Exact McNemar (binomial on discordant pairs), paired by model, Level 2 vs Level 1.
- Pairing: comparisons use models with status ok at both levels. A Protocol C fit on its search bound is a failed fit and excluded (frozen rule); Protocol D fits on the ±3-decade bound are kept (frozen rule). The number of D bound fits is reported per level, with P&W excluding them as a sensitivity line.
- The level-1 comparator is this wrapper's `L1drop` run, checked row by row against `results/t5_throat-2026-10-09`.

**Implementation.** `code/t5l2_run.py` imports `t5_throat_error_types` (calls `install()`) and `a6_territory_run` (calls `setup(config)` and `run_d`) in each worker; neither module nor any frozen file was edited. The pending-DS transform is reset before every call. `code/t5l2_summarise.py` uses `summarise_revision.load` and `ci` unchanged.

## 2. Validation (`results/t5l2-2026-10-09/validation.txt`)

1. **(a) T5 at Level 1, every row.** The wrapper's `L1drop` run reproduces `results/t5_throat-2026-10-09` exactly: all 3,874 A–C rows (incl. 298 clean rows) and all 1,192 D rows match on status, and `ffr`, `dFFR`, `flip` and `outlet_flow_residual` are bit-identical (0 differing rows). `fit_at_bound` agrees in every row (97 bound fits in both; the 20 "differing" rows in the log are the 20 skipped rows, NaN in both).
2. **(b) A6 wrapper at Level 2.** With the frozen T1–T4 set routed through this wrapper (T5 insertion patch installed but inert) at `L2keep`, 6 instances × 2 beds (102_left_LAD_mid_20_80, 280_left_LAD_prox_20_80, 306_left_LAD_prox_20_80, 335_left_LAD_prox_10_70, 42_right_RCA_prox_20_70, 69_right_RCA_prox_10_70): 144 A–C rows and 48 D rows are bit-identical to A6's `ablation_L2keep.csv` / `perterritory_L2keep.csv` (0 differing rows, status identical).
3. **Zero magnitude at Level 2.** A T5 type with ΔDS = 0 at `L2keep` on the same 6 × 2: max |ΔFFR| = 0, 0 flips, max residual 4.6e-17 under A, B, C and D.
4. **Health.** All solves converged. A ≡ B at Level 2 in every row (identical FFR and residual). No T5 model had an unperfused territory at either level (`n_empty` = 0), as expected: T5 changes no topology.

## 3. Results

Paired by model (ok at both levels). n: discrete 97 per variant (194 pooled), leaky 150 (300); Protocol C n is 1 lower where a C fit hit the search bound at either level (C failed fits: 11 at Level 1, 7 at Level 2, all rows; the paired n is 89/96 discrete and 149 leaky for the more-severe variants, one below T5-REPORT for DS +10 discrete). Level 2 = median 4 territories per tree (discrete, range 2–5) and 5 (leaky, 2–7), against 2–3 at Level 1.

### 3.1 Passes-and-wrong, % (Wilson 95% CI), Level 1 → Level 2, exact McNemar

| Bed | Variant | A, B | p | C | p | D | p |
|---|---|---|---|---|---|---|---|
| Discrete | DS +10 | 11 → 8 | 0.25 | 35 (26–45) → 30 (22–41) | 0.12 | 65 (55–74) → 53 (43–62) | 0.0018 |
| Discrete | DS −10 | 29 → 25 | 0.12 | 66 (56–75) → 59 (49–68) | 0.016 | 85 (76–90) → 85 (76–90) | 1.0 |
| Discrete | DS ±10 pooled | 20 (15–26) → 16 (12–22) | 0.016 | 51 (44–58) → 45 (38–52) | <0.001 | 75 (68–80) → 69 (62–75) | 0.0018 |
| Discrete | −½ voxel (narrow) | 26 → 23 | 0.25 | 49 (39–59) → 45 (35–55) | 0.12 | 84 (75–90) → 77 (68–85) | 0.031 |
| Discrete | +½ voxel (wide) | 32 → 28 | 0.12 | 65 (55–74) → 58 (48–67) | 0.039 | 77 (68–85) → 78 (69–85) | 1.0 |
| Discrete | ±½ voxel pooled | 29 (23–36) → 25 (20–32) | 0.016 | 57 (50–64) → 51 (44–58) | 0.0034 | 80 (74–85) → 78 (71–83) | 0.12 |
| Leaky | DS +10 | 31 → 25 | 0.0039 | 49 (41–57) → 40 (32–48) | <0.001 | 91 (86–95) → 86 (80–91) | 0.0078 |
| Leaky | DS −10 | 49 → 42 | 0.0063 | 74 (66–80) → 71 (63–77) | 0.12 | 80 (73–86) → 80 (73–86) | 1.0 |
| Leaky | DS ±10 pooled | 40 (34–45) → 33 (28–39) | <0.001 | 62 (56–67) → 55 (50–61) | <0.001 | 86 (81–89) → 83 (78–87) | 0.0078 |
| Leaky | −½ voxel (narrow) | 43 → 33 | <0.001 | 68 (61–75) → 53 (45–61) | <0.001 | 91 (85–94) → 90 (84–94) | 1.0 |
| Leaky | +½ voxel (wide) | 41 → 38 | 0.12 | 69 (61–76) → 67 (59–74) | 0.5 | 71 (64–78) → 72 (64–79) | 1.0 |
| Leaky | ±½ voxel pooled | 42 (37–48) → 35 (30–41) | <0.001 | 69 (63–74) → 60 (55–66) | <0.001 | 81 (76–85) → 81 (76–85) | 1.0 |

Every change was a loss of a pass: in each cell the P&W models lost equal the passing models lost (e.g. discrete DS pooled C: passes 115 → 104, P&W 95 → 84 counts; D: 165 → 152, 145 → 133). At most one model per cell newly became P&W. The finer check failed some throat-error models; it corrected none (flip rates unchanged, 3.3).

### 3.2 P(wrong | pass), % (Wilson 95% CI), pooled

| Bed | Variant | A, B L1 → L2 | C L1 → L2 | D L1 → L2 |
|---|---|---|---|---|
| Discrete | DS ±10 | 39/60 65 → 32/53 60 (47–72) | 95/115 83 → 84/104 81 (72–87) | 145/165 88 → 133/152 88 (81–92) |
| Discrete | ±½ voxel | 56/90 62 → 49/83 59 (48–69) | 110/141 78 → 99/130 76 (68–83) | 156/186 84 → 151/180 84 (78–89) |
| Leaky | DS ±10 | 119/157 76 → 100/138 72 (64–79) | 184/222 83 → 165/203 81 (75–86) | 257/295 87 → 249/287 87 (82–90) |
| Leaky | ±½ voxel | 127/189 67 → 106/168 63 (56–70) | 205/262 78 → 180/237 76 (70–81) | 243/299 81 → 243/298 82 (77–86) |

Single variants at Level 2: 70–88% (C) and 72–94% (D). For comparison (A6), topological P(wrong | pass) at Level 2 was 29% (C) and 4% (D) discrete, 8% and 3% leaky.

### 3.3 Flip rates under C and D, Level 1 → Level 2 (%, Wilson 95% CI)

| Bed | Variant | C | D |
|---|---|---|---|
| Discrete | DS ±10 pooled | 45 (38–52) → 45 (38–52) | 45 (38–52) → 45 (39–52) |
| Discrete | ±½ voxel pooled | 38 (31–45) → 37 (31–44) | 40 (33–47) → 40 (34–47) |
| Leaky | DS ±10 pooled | 43 (38–49) → 43 (37–48) | 44 (38–49) → 44 (38–50) |
| Leaky | ±½ voxel pooled | 37 (32–43) → 37 (32–43) | 38 (33–44) → 39 (33–44) |

In all 48 single-variant and pooled cells at most 2 models changed flip status (McNemar p ≥ 0.5). A and B flips are identical at both levels by construction.

### 3.4 Protocol D fits on the ±3-decade parameter bound

| | Level 1 | Level 2 |
|---|---|---|
| All rows (both beds, 1,172 ok D fits) | 97 | 153 |
| Discrete, 97 eligible (388 ok D fits) | 54 (DS +10: 34; narrow: 20) | 77 (48; 29) |
| Leaky (600 ok D fits) | 10 (7; 3) | 30 (22; 8) |
| Bound fits that pass the check (all rows) | 29 | 51 |

All bound fits are more-severe variants (DS +10, ½ voxel narrow); none for DS −10 or wide. Kept as in the frozen D run. D P&W excluding bound fits, pooled, L1 → L2: discrete DS 88 → 85%, voxel 83 → 81%; leaky DS 87 → 86%, voxel 81 → 81%. Excluding them therefore raises the rates; keeping them is the conservative choice at both levels.

## 4. What it means for the paper's claims

**Answer: yes. Tuning still hides throat errors when the perfusion check uses finer territories.** At Level 2, 45–51% (discrete) and 55–60% (leaky) of throat-error models pass after one global scaling (C) while materially wrong, and 69–83% after per-territory tuning (D), pooled. Of the passing throat-error models, 76–88% are materially wrong. The finer check removes a minority of throat-error passes (up to 9 points, p ≤ 0.008 in 6 of 8 pooled C/D cells), by failing them, not by correcting the FFR; the decision flip rate under C and D is unchanged (37–45%).

This is the reverse of the topological result in A6, where the finer check cut topological P&W to 2–7% (near the correct-anatomy floor, which was not recomputed at Level 2). A throat error leaves every territory perfused and changes the flow split only through the lesion's own sub-territory, which tuning can restore by forcing the clean flow through the wrong throat. At Level 2 the paper's two error classes therefore separate further: a finer check catches missed branches but not throat or taper errors.

Sentences:
1. **Abstract, last sentence:** "A perfusion match after tuning did not certify the segmented branching or caliber." Stands and is strengthened for caliber: with throat errors it holds at both territory resolutions (45–83% P&W at Level 2).
2. **Limitations:** "A segment-level perfusion check could detect errors within a main-branch territory that this one cannot." Replace with the measured result, now covering both A6 and T5: a finer check detected most topological passes-and-wrong but not throat or taper errors (draft in 5a).
3. **IV-B "After tuning, a passing perfusion check did not show that the FFR was correct."** Stands at both resolutions for throat errors. If T5 enters the main text, the T5 sentence "after tuning 51--86\% of throat-error models passed the perfusion check while materially wrong" can carry "(45--83\% with territories divided again at the next bifurcation)".
4. **Conclusion safeguard list:** "a check of the branching near the lesion ... and a record of the perfusion mismatch before tuning". A finer perfusion check is not a safeguard against throat errors; the throat-diameter check proposed in T5-REPORT remains needed.
5. No number in Table I changes. The A and B P&W for T5 fall by 4–10 points at Level 2 (residual only; FFR unchanged).

## 5. Draft text

**(a) Main text (≤ 2 sentences; IV-B or Limitations):**

> With each main-branch territory divided again at its first bifurcation, 45--60\% of throat-error models still passed the perfusion check while materially wrong after one global scaling and 69--83\% after per-territory tuning, against 51--69\% and 75--86\% at main-branch level, and their decision changes were unchanged (Supplementary Material). A finer perfusion check thus detected most topological errors that passed at main-branch level, but not throat or taper errors.

**(b) Supplement paragraph** (follows the T5 and granularity subsections; uses their labels):

> \paragraph{Throat errors with finer territories} The throat errors (Section~\ref{sec:throat}) were repeated with the finer partition of Section~\ref{sec:granularity}, with a territory without a vessel counted as a 100\% mismatch. With the main-branch partition the procedure reproduced the throat-error results exactly. No throat error left a territory without a vessel. Because the residual of Protocols A and B is computed against the territory targets, their passes-and-wrong were recomputed; their FFR is unchanged. With finer territories, pooled passes-and-wrong fell by at most 9 percentage points (Table~\ref{tab:throatgran}). Every model removed from this count failed the finer check; none had its FFR corrected, and flip rates under Protocols C and D changed by at most two models per cell (McNemar $p \geq 0.5$). Of the throat-error models that passed after tuning, 76--88\% remained materially wrong, against 3--29\% for topological errors at the same resolution. Protocol D fits on the parameter bound rose from 54 to 77 in the discrete bed and from 10 to 30 in the leaky bed, all with an increased stenosis; they were retained as in Table~I, and excluding them would raise the Protocol D rates to 81--86\%.

**LaTeX table (6 rows; body also in `results/t5l2-2026-10-09/tab_t5l2.tex`):**

```latex
\begin{table}[!ht]
\caption{Throat Errors: Passes and Wrong, \% (Wilson 95\% Interval), at Main-Branch and Finer Territory Level}\label{tab:throatgran}
\centering\footnotesize\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}llccrccr@{}}
\toprule
 & & \multicolumn{3}{c}{Discrete bed} & \multicolumn{3}{c}{Leaky bed}\\
\cmidrule(lr){3-5}\cmidrule(l){6-8}
Error & Protocol & Main branch & Finer & $p$ & Main branch & Finer & $p$\\
\midrule
DS $\pm10$ & A, B & 20 (15--26) & 16 (12--22) & 0.016 & 40 (34--45) & 33 (28--39) & $<0.001$ \\
 & C & 51 (44--58) & 45 (38--52) & $<0.001$ & 62 (56--67) & 55 (50--61) & $<0.001$ \\
 & D & 75 (68--80) & 69 (62--75) & 0.0018 & 86 (81--89) & 83 (78--87) & 0.0078 \\
\addlinespace[2pt]
Throat $\pm\tfrac12$ voxel & A, B & 29 (23--36) & 25 (20--32) & 0.016 & 42 (37--48) & 35 (30--41) & $<0.001$ \\
 & C & 57 (50--64) & 51 (44--58) & 0.0034 & 69 (63--74) & 60 (55--66) & $<0.001$ \\
 & D & 80 (74--85) & 78 (71--83) & 0.12 & 81 (76--85) & 81 (76--85) & 1.0 \\
\bottomrule
\end{tabular}
\\[3pt]
\parbox{0.95\columnwidth}{\footnotesize Both signs pooled; 194 models (discrete, 97 instances) and 300 (leaky), 186--193 and 299 under Protocol C, where fits on the search bound at either level were excluded. Passes and wrong: perfusion residual below 10\% and $|\Delta\mathrm{FFR}| > 0.05$. Finer: each main-branch territory divided again at its first bifurcation. Protocols A and B give identical results for throat errors. $p$: exact McNemar test, paired by model.}
\end{table}
```

## 6. Runtime and files written

- Validation: check-zero 22 s, check-a6 27 s (4 workers each); check-t5 a few seconds.
- Full runs, concurrently, 4 workers each, machine shared (load average up to ~200): `L2keep` 1,138 s, `L1drop` 1,039 s; about 19 min wall. Summary under 10 s.
- New code (no existing file modified):
  - `code/t5l2_run.py`: wrapper (`check-a6`, `check-zero`, `run --config`, `check-t5`)
  - `code/t5l2_summarise.py`: paired endpoints, Wilson CIs, McNemar, LaTeX body
- Outputs in `results/t5l2-2026-10-09/` (5 MB): `ablation_t5_{L1drop,L2keep}.csv`, `perterritory_t5_{L1drop,L2keep}.csv`, `territory_counts_*.csv`, `t5_insert_log_*.csv`, `run_*.txt`, `validation.txt`, `summary.txt`, `t5l2_cells.csv`, `tab_t5l2.tex`.
- Scratch logs: `/private/tmp/claude-501/t5l2_*.log`.
