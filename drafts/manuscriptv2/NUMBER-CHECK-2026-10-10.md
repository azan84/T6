# Number check: Paper 6 v2 (Fable, 2026-10-10, final pre-submission)

Scope: every quantitative statement in `drafts/manuscriptv2/main.tex` (abstract, text, Table I, captions), `supplement.tex` with `supplement_tables/*.tex`, and `cover_letter.tex`, as of 2026-10-10 10:24 (final noise-matched numbers in). Procedure: (1) diff v1 (`drafts/manuscript/`, frozen 10-10 08:40) against v2, and the v1 text against the snippets quoted in `NUMBER-CHECK-2026-10-09.md`; (2) recompute every statement that is new or changed since the 10-09 check from the result CSVs with my own code; (3) carry forward the 10-09 verdict for statements whose text is unchanged, with spot recomputation of the headline values; (4) cross-location and range checks; (5) abstract length and internal logic. Scripts: `/private/tmp/claude-501/.../scratchpad/numcheck-v2/nm_check.py` (noise-matched, from `matched_rows.csv`), `frozen_check.py`, `frozen_fix.py`, `extra_check.py`, `last_check.py` (frozen runs), `snippet_check.py` (verbatim test of the 10-09 snippets), outputs `*.out`. No project script was called; no project file other than this report was written.

Conventions (from the paper's definitions, Table I and the `noise_matched_analysis.py` docstring): rows with status `ok`; discrete arm = the 97 eligible instances of `results/discrete_arm_eligibility.csv`; flip = classification change at 0.80; wrong = |ΔFFR| > 0.05; pass = territory residual < 0.10; passes-and-wrong (P&W) over models with a defined residual; Wilson 95% intervals; exact McNemar paired by model, Holm-adjusted across the contrasts of one error type and bed; paired sign test on per-instance class proportions; beyond the grey zone = flip with corrupted FFR outside 0.75–0.85; AUC by the Mann–Whitney statistic. Noise-matched: draws 0–19 (nominal draw −1 reproduces Table I exactly); per-model mean of the P&W indicator over its recorded draws, then mean over models; paired excess = per-draw difference against the correct-anatomy model of the same instance, bed, draw and protocol, or against the same model under Protocol B on the same draw; intervals = patient-level (scan) cluster bootstrap, checked for plausibility only.

Summary: 213 check rows. 80 MATCH (59 recomputed statement and table rows, 21 cross-location rows), 0 ROUNDING, 0 MISMATCH, 1 NOT-RECOMPUTABLE (cover-letter citations), 129 CARRIED from the 10-09 check with text identical or trivially reworded (their 10-09 verdicts: 118 MATCH, 1 ROUNDING (#87, 12.5 → 13), 10 NOT-RECOMPUTABLE), and 3 rows whose text no longer exists (#118, #143, #144). About 330 individual values were recomputed today (all 40 cells of the new Table S10 and every matched number in the abstract, III-B, III-C, IV-A, IV-C, Conclusion, S8, S9 and the cover letter; the 24 new Table S7 ×2/×3 cells and their footnote; the new III-A tuning and taper sentences; the new S8, S9 and S10 text; about 60 headline spot checks). Every one reproduces. No interim (draws 0–1) value remains anywhere in main, supplement, tables or cover letter; the published `tab_noise_matched.tex` is byte-identical to `results/noise_matched-2026-10-09/tab_noise_matched.tex` and differs from the interim file. The four 10-09 MISMATCH items are fixed (M1, M2, M3) or moot (M4: the |ln C| table was removed). The abstract is exactly 250 words. One internal-logic gap remains (L1: the Methods never describe the noise-matched comparison that the abstract, Results, Discussion and Conclusion now rest on); seven basis notes follow. The portal cover letter is an outdated version and disagrees with `cover_letter.tex` in eleven places (Section 4).

## 1. Check table

Source abbreviations: `nm` = `results/noise_matched-2026-10-09/matched_rows.csv` (recomputed; `matched_rates.csv`, `matched_auc.csv`, `summary.txt` used only for comparison); `abl` = `results/ablation-2026-10-07.csv`; `per` = `results/ablation-perterritory-2026-10-08.csv`; `elig` = `results/discrete_arm_eligibility.csv`; `t5` = `results/t5_throat-2026-10-09/ablation_t5.csv` + `perterritory_t5.csv`; `td` = `results/throat_demand-2026-10-09/x{2,3}/ablation_t5vox.csv` + `perterritory_t5vox.csv`; `rep` = `results/demand-replication-x{2,3}-2026-10-08/`; `a6` = `results/a6_territory-2026-10-09/*_L2keep.csv`; `a5` = `results/a5_overlap-2026-10-09/overlap_metrics.csv`; `a7` = `results/a7_detector-2026-10-09/negatives_pretune.csv` (+ `detector_metrics.csv` for CI cross-check); `neg` = `results/negatives-2026-10-07.csv`; `cfd` = `results/cfd_M1/M1_scan14_0D_vs_3D-2026-10-03.csv` + `_outlets`; `d7` = `cfd_handover/returns/2026-10-03/M1_D7_sensitivity_2026-10-06.csv`; `mesh` = `cfd_handover/returns/2026-10-03/TaskA/as_meshed_radius_baseline_A0_25um_detail.csv`. "#n" = row n of the 10-09 check. "NEW" = text added or changed since the 10-09 check.

### 1.1 Abstract

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 1 | Abstract "150 stenoses into 108 coronary trees" (#1) | 150; 108 | 150 instances; 108 (scan, side) trees; 93 patients; LAD/LCx/RCA 50/50/50 | abl | MATCH |
| 2 | "five segmentation errors" (#2) | 5 | T1–T4 + T5 | — | CARRIED |
| 3 | "changed the decision in 32--33\%" (#3, "of models" dropped) | 32–33 | 45/137 = 32.8%; 84/265 = 31.7% | abl A | MATCH |
| 4 | "half-voxel throat error in 30--36\%" (#4) | 30–36 | 58/194 = 29.9%; 108/300 = 36.0% | t5 A | MATCH |
| 5 | "6--10\% for vessel-size (caliber) errors" (#5) | 6–10 | 17/300 = 5.7%; 20/194 = 10.3% | abl A | MATCH |
| 6 | "reduced topological flips to 5--19\%" (#6) | 5–19 | class level B/C/D: 13.9, 19.2, 7.7 (discrete); 4.9, 8.2, 5.8 (leaky) | abl+per | MATCH (one basis now in abstract, IV-A and Conclusion; 10-09 note N1 closed) |
| 7 | NEW "passed 19\% (discrete) and 8\% (leaky) of topological-error models while wrong by more than 0.05" | 19; 8 | matched C: 19.4% (104 models, 2 080 model-draws); 7.8% (171; 3 420) | nm | MATCH |
| 8 | NEW "against 3--4\% of correct models" | 3–4 | floor under C, matched: 3.1%; 3.9% | nm | MATCH |
| 9 | NEW "Throat-error models did so in 42--49\%" | 42–49 | matched C: 42.4%; 49.3% | nm | MATCH |
| 10 | NEW "Per-territory matching raised the correct-anatomy floor to 9--15\%" | 9–15 | floor under D, matched: 15.0%; 8.9% | nm | MATCH |
| 11 | "Finer territories cut topological concealment to 2--7\%" (#11) | 2–7 | L2: 7/104 = 6.7, 3/104 = 2.9; 8/171 = 4.7, 4/171 = 2.3 | a6 | MATCH |
| 12 | "taper's tube-model Dice score (0.97)" (#12) | 0.97 | tree DSC median T1 0.975 / T4 0.971 (discrete); 0.969 / 0.972 (leaky) | a5 | MATCH |
| 13 | Abstract length (JBHI limit 250) | ≤ 250 | 250 words (whitespace tokens after stripping LaTeX; "32--33\%" counted once) | — | MATCH (at the limit, see B7) |

### 1.2 Methods and figure captions

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 14 | #13–#41 (29 rows): II-A to II-F and the Fig. 1–4 captions | — | diff v1→v2 shows no change in lines 55–212 or in any caption; every 10-09 snippet present | — | CARRIED (23 MATCH; 6 NOT-RECOMPUTABLE: #14, #26, #34, #35, #37, #38) |
| 15 | II-B "97 instances whose healthy-equivalent network..." (#25) | 97 | 97 eligible discrete instances; 150 leaky | elig, nm | MATCH |
| 16 | II-D "excluded (two half-voxel throat-error models, one per bed)" (#31) | 2 | Protocol C bound: narrow 1 discrete + 1 leaky (plus 7 + 1 at ±10 points, reported in S5) | t5 status | MATCH |

### 1.3 Table I

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 17 | #42–#57 (16 rows): Table I, all 218 values and the note | — | Table I identical to v1 (diff). Spot-recomputed: T1+T2 and T3+T4 class totals (flip and P&W, A–D, both beds); T3 and T4 flips in all 16 cells (7, 7, 7, 7; 13, 8, 8, 14; 2, 2, 3, 3; 9, 1, 5, 5); all six T5 rows (58/194, 56/194; 73/193, 110/193; 77/194, 156/194; 108/300, 127/300; 112/299, 205/299; 114/300, 243/300); note "5.0--6.5\%" = per-cell floor 4.99–6.55% | abl, per, t5 | CARRIED (spot checks MATCH) |

### 1.4 Results III-A

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 18 | "45 of 137 ... (33\%, 95\% CI 26--41\%) ... 20 of 194 ... (10\%, 7--15\%)" (#58) | as stated | 32.8 (25.5–41.1); 10.3 (6.8–15.4) | abl A | MATCH |
| 19 | "32\% (26--38\%) and 6\% (4--9\%)" (#59) | as stated | 31.7 (26.4–37.5); 5.7 (3.6–8.9) | abl A | MATCH |
| 20 | #60–#62, #64–#67, #69 (9 rows): sign tests, Protocol D rates, "every flip followed the sign", "about half beyond the grey zone", mass error | — | text identical | — | CARRIED |
| 21 | "crossed 0.80 in 30\% (24--37\%) and 36\% (31--42\%)" (#63) | as stated | 29.9 (23.9–36.7); 36.0 (30.8–41.6) | t5 A | MATCH |
| 22 | NEW (replaces #68) "Tuning raised its flip rate from 30\% to 38--40\% in the discrete bed (15 and 19 flips created, none reversed; McNemar $p < 0.001$) and from 36\% to 37--38\% in the leaky bed ($p = 0.22$ and 0.06)" | 30 → 38–40; 15, 19, 0; < 0.001; 36 → 37–38; 0.22, 0.06 | A 29.9, C 37.8 (73/193), D 39.7 (77/194); A→C +15/−0 (raw p 1.2e-4, Holm 2.4e-4), A→D +19/−0 (3.8e-6); leaky A 36.0, C 37.5 (112/299), D 38.0 (114/300); A→C +5/−1 (p 0.219), A→D +6/−0 (raw 0.031, Holm 0.0625) | t5 | MATCH (Holm-adjusted, as II-F specifies; B3) |
| 23 | "changed FFR by a mean of 0.006--0.044 in absolute value" (#70 = 10-09 M3) | 0.006–0.044 | T3/T4 cell means A–D: min 0.0060 (T4 B leaky), max 0.0437 (T4 D discrete) | abl+per | MATCH (M3 fixed) |
| 24 | "their flip rates (1--14\%) were compared with the 5.0--6.5\% expected" (#71 reworded) | 1–14; 5.0–6.5 | 0.7–14.4%; 4.99–6.55% | abl+per | MATCH |
| 25 | NEW (replaces #72) "Only the taper's rates in the discrete bed, 13\% and 14\% under fixed boundary conditions and Protocol D, had lower confidence bounds (8\% and 9\%) above that floor; its leaky-bed rate was 9\% (6--15\%)" | 13, 14; 8, 9; 9 (6–15) | 13/97 = 13.4 (8.0–21.6); 14/97 = 14.4 (8.8–22.8); 14/150 = 9.3 (5.6–15.1); all other caliber cells have lower bounds 0.1–5.6% | abl+per | MATCH (B2 on "that floor") |
| 26 | #73–#76 (4 rows): "20\% (discrete) and 23\%", "14--56 ... Holm-adjusted", "22 reversed, 12 created, $p = 0.24$", "22\% ... 89\%"; #75 now opens "produced the fewest flips among Protocols A--C" | — | topological B 13.9 < C 19.2 < A 32.8; 4.9 < 8.2 < 31.7; caliber B 7.7 = C 7.7 < A 10.3 (tie); 1.3 < 4.0 < 5.7 | abl | CARRIED (MATCH; tie noted, B4) |

### 1.5 Results III-B

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 27 | #77–#84, #88–#90 (11 rows): residual medians, Protocol D "all but two", T1 medians, "no lesion-length or taper model passed" | — | spot: T1 median ΔFFR A 0.095 / 0.047, C 0.077 / 0.015, D 0.000 / 0.004; 10/44 and 3/71 above 0.05; Wilcoxon A–C p 1.6e-11, 2.4e-13 | abl, per | CARRIED (spot MATCH) |
| 28 | "20 of 104 ... (19\%, 13--28\%) ... 14 of 171 (8\%, 5--13\%) ... 21 of 104 (20\%, 14--29\%) and 9 of 171 (5\%, 3--10\%)" (#85–#86) | as stated | 19.2 (12.8–27.8); 8.2 (4.9–13.3); 20.2 (13.6–28.9); 5.3 (2.8–9.7) | abl, per | MATCH |
| 29 | "2\% and 6\% under Protocol B and 13\% and 22\% under Protocol A" (#87) | 2; 6; 13; 22 | 2/104 = 1.9; 10/171 = 5.8; 13/104 = 12.5; 38/171 = 22.2 | abl | CARRIED (ROUNDING, 12.5 → 13 half-up) |
| 30 | "McNemar $p < 0.001$ for C and D ... ($p \geq 0.12$)" (#88) | as stated | C vs B +18/−0, p 7.6e-6; D vs B +20/−1, 2.1e-5; leaky +4/−0 0.125, +3/−4 1.0 | abl+per | MATCH |
| 31 | "3.1\% (2.4--4.0\%) and 3.9\% (3.2--4.6\%) of draws, and their flip rates were 6.2\% and 7.2\%" (#89) | as stated | 60/1940 = 3.1 (2.4–4.0); 116/2990 = 3.9 (3.2–4.6); 120/1940 = 6.2; 215/2990 = 7.2 | neg | MATCH |
| 32 | NEW "topological passes-and-wrong under Protocol C were 19\% (14--25\%) and 8\% (5--11\%), against 3\% and 4\% for correct anatomy" | 19 (14–25); 8 (5–11); 3; 4 | 19.4 (my 1 000-rep cluster bootstrap 13.9–24.6; script 14.1–24.9); 7.8 (5.3–10.6; 5.2–10.6); floor C 3.1, 3.9 | nm | MATCH |
| 33 | NEW "The paired excess was 17 and 7 points over the floor and 12 and 5 points over Protocol B on the same draws" | 17, 7; 12, 5 | 17.1, 6.7; 12.1, 4.5 (4.503) | nm | MATCH |
| 34 | NEW "Exact matching to noisy targets under Protocol D left 36\% and 19\% of topological-error models wrong, against 15\% and 9\% of correct-anatomy models (paired excess 16 and 6 points)" | 36, 19; 15, 9; 16, 6 | matched D: P&W 35.9, 18.6 (pass 99.1 / 100%, so P&W = wrong); floor D 15.0, 8.9; excess 15.9, 5.5 (5.53) | nm | MATCH |
| 35 | "5\% (C) and 18\% (D) ... 12\% and 4\% ... (McNemar against B, $p \leq 0.004$ in all four comparisons)" (#91, wording) | as stated | 9/194 = 4.6; 35/194 = 18.0; 37/300 = 12.3; 12/300 = 4.0; p as #91 | abl+per | MATCH |
| 36 | "29\% (discrete) and 42\% (leaky) ... 57\% and 69\% ... 80\% and 81\%, with a median $|\Delta\mathrm{FFR}|$ of 0.11--0.16" (#92–#93) | as stated | 28.9, 42.3; 57.0, 68.6; 80.4, 81.0; medians 0.112, 0.141, 0.162 / 0.105, 0.128, 0.122 | t5 | MATCH |
| 37 | NEW "With noisy targets more throat models failed the check, and the proportions were 42\% and 49\% (C) and 78\% and 80\% (D)" | more fail; 42, 49; 78, 80 | pass rate nominal → matched: C 73.1 → 53.9, 87.6 → 62.6; D 95.9 → 94.7, 99.7 → 99.6; matched P&W 42.4, 49.3; 78.3, 80.1 | t5, nm | MATCH |
| 38 | NEW "Caliber errors away from the throat gave 9--12\% (C) and 13--28\% (D), against 3--4\% and 9--15\% for correct anatomy" | 9–12; 13–28; 3–4; 9–15 | matched caliber C 8.6, 12.4; D 28.1, 13.2; floor C 3.1, 3.9; D 15.0, 8.9 | nm | MATCH |
| 39 | "topological passes-and-wrong fell to 7\% (C) and 3\% (D) ... 5\% and 2\%" (#94) | as stated | 6.7, 2.9; 4.7, 2.3 | a6 | MATCH |
| 40 | "Caliber passes-and-wrong away from the throat rose under Protocol D to 23\% and 9\%, almost all taper models" (#95 = 10-09 M1) | 23; 9 | T3+T4 at L2 under D: 45/194 = 23.2; 28/300 = 9.3 (taper 44 and 28 of them) | a6 | MATCH (M1 fixed) |
| 41 | "fell by at most 9 points, to 51--60\% (C) and 78--81\% (D), and flip counts changed by at most five per cell" (#96, #151; N3 wording applied) | as stated | as 10-09 | t5l2, a6 | CARRIED (MATCH) |

### 1.6 Results III-C, III-D, Discussion and Conclusion

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 42 | "same median DSC (0.97 per tree; 0.98 over the whole scan ...) ... twice as often (27\% against 13\% discrete, 18\% against 9\% leaky)" (#97 + NEW 0.98) | 0.97; 0.98; 27/13; 18/9 | tree 0.975 / 0.971, 0.969 / 0.972; scan 0.985 / 0.983, 0.983 / 0.983; flips 27.3 / 13.4, 17.8 / 9.3 | a5, abl | MATCH |
| 43 | #98–#100 (3 rows): DSC 0.89, 0.62, clDice; 91% / 62%; AUC 0.54 / 0.70 | — | text identical | — | CARRIED |
| 44 | NEW (replaces #101) "AUC 0.82, 0.79--0.86 ... barely in the leaky bed (0.56, 0.54--0.59). At the 10\% check it flagged 85\% and 58\% of them and about half of the correct models (AUC 0.77 and 0.22 with noise-free error models)" | 0.82 (0.79–0.86); 0.56 (0.54–0.59); 85; 58; ≈½; 0.77; 0.22 | Protocol B residual, noisy draws: 0.824 (my bootstrap 0.788–0.854; script 0.789–0.859); 0.562 (0.542–0.588; 0.539–0.587); flagged 85.2%, 58.2%; floor flagged 47.5%, 50.4%; noise-free error models 0.767, 0.221 | nm, a7, abl | MATCH |
| 45 | #102–#108 (7 rows): 3D values (0.870, 0.944, +0.074, 0.892, −0.0007, +0.022, +0.081, −0.0005, +0.127, +0.107, 0.276, 0.231, 0.761, 0.0021) and the demand paragraph directions | — | text identical | cfd, d7, rep | CARRIED |
| 46 | NEW III-D "27--29\% of models with fixed boundary conditions and in 31--35\% after tuning; 52--75\% of tuned throat-error models passed ... wrong ... (27\% against 50\%, $p = 0.005$) and as often in the leaky bed ($p = 0.12$ and 0.24)" | 27–29; 31–35; 52–75; 27 vs 50, 0.005; 0.12, 0.24 | ×2 discrete A 26.6, C 30.9, D 34.0, P&W 52.1 / 73.4; ×2 leaky A 29.3, C 34.7, D 35.3, P&W 69.0 / 75.0; ×3 leaky A 28.7, C 34.0, D 33.0, P&W 67.7 / 72.0; topological A ×2 discrete 33/66 = 50.0; paired sign test T1+T2 vs T5 under A: ×2 discrete 23 vs 7 of 46, p 0.0052; ×2 leaky 54 vs 38, p 0.117; ×3 leaky 50 vs 38, p 0.241 | td, rep | MATCH |
| 47 | IV-A "each changed about a third of decisions" (#109); "from 32--33\% to 5--19\% (pooled over error types)" (replaces #110) | ⅓; 32–33 → 5–19 | 32.8 / 31.7 → 13.9, 19.2, 7.7 / 4.9, 8.2, 5.8 | abl+per | MATCH |
| 48 | IV-A "except the taper in the discrete bed (13--14\%)" | 13–14 | 13.4 (A), 14.4 (D) | abl, per | MATCH |
| 49 | IV-A "20 of the 39 passing topological-error models ... against 14 of 154" (#111) | 20/39; 14/154 | C: 39 passing, 20 wrong; 154 passing, 14 wrong | abl C | MATCH |
| 50 | NEW IV-A "(19\% against 3\% discrete, 8\% against 4\% leaky). Under per-territory matching the floor itself rose to 15\% and 9\%, and the residual error of topological models (36\% and 19\%)" | as stated | as rows 7, 8, 10, 34 | nm | MATCH |
| 51 | IV-A "57--81\% of models (42--80\% with noisy targets)" (#112 + NEW) | 57–81; 42–80 | 57.0–81.0; matched throat C/D 42.4, 49.3, 78.3, 80.1 | t5, nm | MATCH |
| 52 | IV-B "13--15.5\%" (Gamage) (#113) | literature | — | — | CARRIED (NOT-RECOMPUTABLE) |
| 53 | NEW (replaces #114) IV-C "flipped 30--36\% ... (AUC 0.82 with the same noise on both), and half of the correct models with noisy targets exceeded 10\%" | 30–36; 0.82; ½ | 29.9–36.0; 0.824; 47.5% / 50.4% | t5, nm, a7 | MATCH |
| 54 | Limitations (replaces #115; the 3D offsets 0.045 / 0.761 / +0.127 left IV-D) "the offset changed the size of the error effect but not its direction" and NEW "(median 0.14~mm in the 3D case)" | direction; 0.14 | area-equivalent meshed radius minus requested (distance-map) radius over 731 valid sections: median 0.137 mm (IQR 0.096–0.186; LAD only 0.134); direction as #102–#105 | mesh, cfd | MATCH |
| 55 | Conclusion rewritten (#116): "150 ... 108 ... (18--43\% per type) ... about a third ... 2--13\% for caliber errors ... 5--19\% ... one in five tuned topological-error models (discrete bed; 8\% leaky) and 42--49\% ... Correct anatomy did so in 3--4\%. Exact per-territory matching left 19--36\% ... floor of 9--15\% ... 2--7\%" | as stated | 150 / 108; per type A 17.8, 27.3, 40.0, 42.9; caliber per type A 2.0 (T3 leaky) – 13.4 (T4 discrete); class B–D 4.9–19.2; matched C 19.4 ("one in five"), 7.8; 42.4, 49.3; 3.1, 3.9; matched D 18.6, 35.9; floor D 8.9, 15.0; L2 2.3–6.7 | abl, per, t5, nm, a6 | MATCH |

### 1.7 Supplement text and tables

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 56 | S1 criteria "at least 2 (0--4 scale) ... 1.0~mm ... 40\% DS ... 20~mm ... 0.75~mm ... 0.90" (#117; S1 reduced to these) | as stated | text kept | sweep | CARRIED (0.75 mm NOT-RECOMPUTABLE) |
| 57 | S1 seed, relaxation, tolerance, exponent sentence (#118) | — | removed from v1 after the 10-09 check | — | REMOVED (n/a) |
| 58 | Fig. S1 (simplified): "6\,944 instances", "150 (97 discrete)", "T1--T5", "A--D, two beds" (#119) | 6 944; 150; 97 | 6 944 sweep rows; 150 / 97 | sweep, elig | MATCH |
| 59 | S2 "two half-voxel throat-error models; 10 of 4\,940 noise-floor draws" and "two missed-branch models, residual 0.08 and 0.11" (#120–#121) | 2; 10/4940; 0.08, 0.11 | 1 + 1; 10 failed fits of 1 940 + 3 000; D bound fits T1 discrete 0.083, 0.111 | t5, neg, per | MATCH |
| 60 | S2 "23 half-voxel and 41 ten-point throat-error models with an increased stenosis, of which 43 failed the check and 21 passed while materially wrong" (#122 = 10-09 M2) | 23; 41; 43; 21 | Protocol D fits at bound: vox_narrow 20 + 3 = 23, ds_plus10 34 + 7 = 41 (all increased stenosis); residual ≥ 0.10: 43; pass and wrong: 21; pass and right: 0 | t5 per | MATCH (M2 fixed; agrees with S5's 64) |
| 61 | S2 "40\% to 43\%" (#123); Table S1 (#124); Table S2 GLMM (#125) | — | `tab_exclusions_nz.tex`, `tab_glmm.tex` identical to v1 | — | CARRIED (3 rows) |
| 62 | Table S3, now T1+T2 rows only (8 rows × 7 cells) and its note (#126–#127) | 56 values | all reproduce: discrete A 137, 12 (8–19), 23 (17–31), 31 (24–40), 21, 81 (60–92); B 1 (0–5), 11 (7–17), 20 (14–27), 23, 9 (2–27); C 104, 19 (13–28), 28 (20–37), 38 (30–48), 39, 51 (36–66); D 20 (14–29) ×3, 103, 20 (14–29); leaky A 218, 20 (15–26), 30 (25–37), 38 (31–44), 108, 40 (31–49); B 5 (3–8), 5 (3–9), 6 (3–9), 176, 6 (3–10); C 171, 8 (5–13), 9 (6–15), 9 (6–15), 154, 9 (5–15); D 5 (3–10) ×3, 171, 5 (3–10). Note "differ by at most one model": D passes 103/104 and 171/171 | abl+per | MATCH |
| 63 | S4.2 text, Tables S4–S6, S4.3, S4.4 (#128–#138) | — | `tab_demand.tex`, `tab_replication.tex`, `tab_greyzone.tex` identical to v1; lead-in texts identical or reworded without value change (#129 "0.7 times the demand") | — | CARRIED (11 rows) |
| 64 | S5 text "0.352~mm ... 0.088~mm ... 7.3 points of DS, 4.5--9.8 ... 12.3--12.4 ... (2 at half a voxel, 8 at $\pm 10$ points) ... 64 Protocol D fits ... up to 13 points" (#139–#142) | as stated | 2 + 8 (1+1, 7+1) and 64 recomputed | t5 | CARRIED (spot MATCH; #140 NOT-RECOMPUTABLE) |
| 65 | Table S7 per-sign half-voxel rows (#143–#144) | — | dropped in the v1 trim | — | REMOVED (n/a) |
| 66 | Table S7 pooled ½-voxel and DS ±10 rows (#145–#146) | 48 values | identical to v1 | — | CARRIED |
| 67 | NEW Table S7 "$\pm\tfrac12$ voxel, $k\times2$" and "$k\times3$" rows (24 values + n) | discrete ×2: 94 / 27 (19–36) / 35 (26–45) / 12 (7–20); 94 / 31 (22–41) / 52 (42–62) / 13 (7–21); 94 / 34 (25–44) / 73 (64–81) / 18 (12–27). leaky ×2: 300 / 29 (24–35) / 44 (39–50) / 12 (9–16); 300 / 35 (30–40) / 69 (64–74) / 17 (13–21); 300 / 35 (30–41) / 75 (70–80) / 18 (14–22). leaky ×3: 300 / 29 (24–34) / 48 (43–54) / 9 (6–13); 300 / 34 (29–40) / 68 (62–73) / 15 (12–20); 300 / 33 (28–39) / 72 (67–77) / 14 (10–18) | 26.6 (18.7–36.3), 35.1 (26.2–45.2), 11.7 (6.7–19.8); 30.9 (22.4–40.8), 52.1 (42.1–61.9), 12.8 (7.46–21.0); 34.0 (25.3–44.1), 73.4 (63.7–81.3), 18.1 (11.6–27.1); 29.3 (24.47–34.7), 44.3 (38.8–50.0), 12.0 (8.8–16.2); 34.7 (29.5–40.2), 69.0 (63.6–74.0), 16.7 (12.9–21.3); 35.3 (30.1–40.9), 75.0 (69.8–79.6), 17.7 (13.8–22.4); 28.7 (23.8–34.0), 48.3 (42.7–54.0), 9.0 (6.3–12.8); 34.0 (28.9–39.5), 67.7 (62.2–72.7), 15.3 (11.7–19.8); 33.0 (27.9–38.5), 72.0 (66.7–76.8), 13.7 (10.2–18.0); all residuals defined (n_resid = n) | td | MATCH |
| 68 | Table S7 note (#147 + NEW) "47 instances at $k\times2$ ... flipped 50\% (38--62\%) and 34\% (29--40\%) at $k\times2$ and 33\% (28--39\%) at $k\times3$ ... 33\% (26--41\%) and 32\% (26--38\%) ... 10\% (7--15\%) and 6\% (4--9\%)" | as stated | 47 eligible; 33/66 = 50.0 (38.3–61.7); 89/260 = 34.2 (28.7–40.2); 87/262 = 33.2 (27.8–39.1); primary as rows 18–19 | rep, abl | MATCH |
| 69 | S6 text and Table S8 granularity (#148–#153; #151 now "Flip counts") | — | text identical except N3 wording | a6, t5l2 | CARRIED (6 rows) |
| 70 | S7 text and Table S9 overlap (#154–#160; #157 now "about 40\%") | — | 43% (discrete) / 40% (leaky) → "about 40\%" | a5 | CARRIED (7 rows; #157 now MATCH; #154 NOT-RECOMPUTABLE) |
| 71 | NEW S8 text (replaces #161–#167; Table S10 "|ln C|" removed) "with noise its median is 0.10, and 48\% (discrete) and 50\% (leaky) of draws exceed the 10\% check. With noise-free targets ... AUC of 0.77 (0.71--0.82, discrete) and 0.22 (0.18--0.27, leaky) and flagged 83\% and 19\% ... the AUC was 0.82 (discrete) and 0.56 (leaky)" | 0.10; 48; 50; 0.77 (0.71–0.82); 0.22 (0.18–0.27); 83; 19; 0.82; 0.56 | pre-tuning residual medians 0.097, 0.101; 922/1940 = 47.5%, 1511/3000 = 50.4%; AUC 0.767, 0.221 (a7 bootstrap 0.712–0.820, 0.178–0.268, cross-checked only); 114/137 = 83.2%, 42/218 = 19.3%; matched 0.824, 0.562 | a7, abl, nm | MATCH (10-09 M4 moot: the |ln C| table no longer exists) |
| 72 | S9 text (#168 + NEW; Table S11 folded in, #169) "1.96 × (10--15\%) ≈ 20--29\% ... 0.05 ... 0.056 ... 0.02 ... 0.10 ... 0.083. Tuned as in Protocol C, correct anatomy flipped in 6.2\% (discrete) and 7.2\% (leaky) of draws (median $|\Delta$FFR$|$ 0.012, 95th percentile 0.05) and passed the check in 72\%" | as stated | 19.6–29.4; design SDs carried (#168); 120/1940 = 6.2, 215/2990 = 7.2; medians 0.012, 0.012; 95th pct 0.050, 0.053; pass 72.3, 72.3 | neg | MATCH |
| 73 | NEW S9 "Rates are means over the 20 draws per instance with patient-level cluster-bootstrap intervals; the excess is the per-draw difference from the correct-anatomy model of the same instance, bed and draw, and $n$ counts models with a defined residual" | definition | matches the computation that reproduces the table; draws per model-protocol min 4, median 20 (B1, B5) | nm | MATCH |
| 74 | NEW Table S10 (`tab_noise_matched.tex`): 8 rows × (n, Noise-free, Matched (CI), Excess (CI)) × 2 beds | Topological C: 104, 19, 19 (14–25), 17 (12–22); 171, 8, 8 (5–11), 7 (4–9). D: 104, 20, 36 (28–44), 16 (9–23); 171, 5, 19 (15–23), 6 (3–8). Caliber C: 194, 5, 9 (7–11), 5 (4–7); 300, 12, 12 (10–15), 8 (6–10). D: 194, 18, 28 (24–32), 13 (10–16); 300, 4, 13 (11–16), 4 (3–6). Throat C: 194, 57, 42 (37–47), 39 (35–44); 300, 69, 49 (45–53), 45 (41–49). D: 194, 80, 78 (72–85), 63 (56–70); 300, 81, 80 (75–85), 71 (66–76). Correct anatomy C: 97, 0, 3 (2–4), --; 150, 0, 4 (2–6), --. D: 97, 0, 15 (12–19), --; 150, 0, 9 (7–11), -- | Noise-free (nominal draw): 20/104 = 19.2, 21/104 = 20.2, 9/194 = 4.6, 35/194 = 18.0, 110/193 = 57.0, 156/194 = 80.4; 14/171 = 8.2, 9/171 = 5.3, 37/300 = 12.3, 12/300 = 4.0, 205/299 = 68.6, 243/300 = 81.0; floor 0 — identical to Table I. Matched: 19.4, 35.9, 8.6, 28.1, 42.4, 78.3, 3.1, 15.0; 7.8, 18.6, 12.4, 13.2, 49.3, 80.1, 3.9, 8.9. Excess over floor: 17.1, 15.9, 5.5, 13.1, 39.3, 63.3; 6.7, 5.5, 8.4, 4.3, 45.4, 71.3. Intervals: my 1 000-rep scan-cluster bootstraps lie within 1 point of every printed bound (e.g. topological C discrete 13.9–24.6 vs 14–25; throat D discrete 71.7–84.0 vs 72–85; floor D leaky 6.9–11.1 vs 7–11); pooled-draw Wilson intervals are much narrower, confirming the cluster basis. Published fragment byte-identical to `results/.../tab_noise_matched.tex`; differs from the interim file (which read 21 (14–28), 38 (28–46), 10 (6–14), 27 (21–32), 5 (2–8) ...) | nm | MATCH |
| 75 | S10 text (#170–#172; Table S12 folded in) "3.5--3.9 million cells ... 25~\textmu m ... $\pm 4$~mm ... 3\,000 iterations ... $10^{-5}$ ... (12.5~\textmu m, 6.24 and 8.31 million cells) raised the baseline FFR from 0.8698 to 0.8716 and 0.8718 (0.0019--0.0021). Outlet flows changed by at most 0.25\%, above ... $5.5\times10^{-4}$ ... about 0.002 ... 0.074. The finest mesh missed the strict residual limit (velocity residual $1.08\times10^{-5}$)" | as stated | d7: 6.241 M, 8.309 M cells; 0.86976 → 0.87165, 0.87183 (+0.00189, +0.00207); max outlet flow change 0.241%, 0.253%; A2 UNCONVERGED at 3 000 iterations; 0.0739 | d7, cfd | MATCH (mesh settings, U3D and 1.08e-5 NOT-RECOMPUTABLE, carried) |
| 76 | NEW S10 "The lesion carried about 10~mL/min (tree inflow 0.68~mL/s in 3D, 0.65--0.67~mL/s in the cohort model). At the meshed throat radius of 0.276~mm the mean velocity is about 0.7~m/s and the Reynolds number about 110, within the laminar regime" | ≈ 10; 0.68; 0.65–0.67; 0.276; ≈ 0.7; ≈ 110 | 3D baseline Q_in 0.682 mL/s; cohort clean inflow 0.649 (discrete) and 0.672 (leaky) mL/s; flow through the two outlets beyond the lesion (out_160 + out_600): 0.174 mL/s = 10.4 mL/min with prescribed flows → v 0.72 m/s, Re 106; 0.201 mL/s = 12.0 mL/min with resistance outlets → v 0.84 m/s, Re 123; throat r 0.2756 mm | cfd outlets | MATCH (approximate, prescribed-flow basis; B6) |

### 1.8 Cover letter (`cover_letter.tex`)

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 77 | "150 controlled stenoses into 108 coronary trees ... five segmentation error types, including a half-voxel error in the stenosis throat" | 150; 108; 5 | 150; 108; T1–T5 | abl | MATCH |
| 78 | Bullet 1 "about a third of models in this threshold-stratified cohort (30--36\%), against 6--10\% for caliber errors" | 30–36; 6–10 | topological 31.7–32.8 and throat 29.9–36.0 → 30–36; caliber 5.7–10.3 | abl, t5 | MATCH |
| 79 | Bullet 2 "passed 19\% (discrete bed) and 8\% (leaky bed) of topological-error models and 42--49\% of throat-error models while FFR was wrong by more than 0.05, against 3--4\% of correct models. A check one branching level finer removed most topological cases but few throat cases" | 19; 8; 42–49; 3–4; most / few | matched C 19.4, 7.8; 42.4, 49.3; floor 3.1, 3.9; L2: topological P&W 20 → 7, 21 → 3 (discrete), 14 → 8, 9 → 4 (leaky); throat −7 to −26 of 56–243 (#199) | nm, a6, t5l2 | MATCH |
| 80 | Bullet 3 "(0.97, as high as a taper and above the 0.93 agreement between two expert annotators), yet changed the decision about twice as often ... (area under the curve 0.82 with the same noise on both), with a 48\% false-alarm rate under physiological noise" | 0.97; 0.93; 2×; 0.82; 48 | 0.975 / 0.971; 0.928; 27.3 vs 13.4, 17.8 vs 9.3; 0.824; 922/1940 = 47.5% | a5, abl, nm, a7 | MATCH |
| 81 | "three papers in the Journal" (Viceconti 2025, Chen 2025, Arminio 2026) | citations | — | — | NOT-RECOMPUTABLE |

### 1.9 Consistency of the same quantity across locations

| # | Quantity | Locations and values | Verdict |
|---|---|---|---|
| 82 | Topological flips under A | abstract 32–33; III-A 33 / 32; Table S7 note 33 (26–41) / 32 (26–38); IV-A "about a third", "32--33\%"; Conclusion "about a third" | MATCH |
| 83 | Throat flips under A | abstract 30–36; III-A 30 / 36; Table I; IV-C 30–36; cover letter "(30--36\%)" | MATCH |
| 84 | Caliber flips under A | abstract 6–10 (class); III-A 10 / 6; Table S7 note; cover letter 6–10; Conclusion "2--13\%" (per type: T3 leaky 2.0 to T4 discrete 13.4) | MATCH on each stated basis |
| 85 | Topological flips after re-derivation or tuning | abstract 5–19; IV-A "32--33\% to 5--19\% (pooled over error types)"; Conclusion 5–19; per type in IV-A/Conclusion "18--43\%" is Protocol A | MATCH (single basis, unlike v1) |
| 86 | Matched topological P&W under C | abstract 19 / 8; III-B 19 (14–25) / 8 (5–11); IV-A 19 / 8; Conclusion "one in five" / 8; Table S10 19 / 8; cover letter 19 / 8 | MATCH |
| 87 | Matched correct-anatomy floor under C | abstract 3–4; III-B "3\% and 4\%" and 3.1 / 3.9; IV-A 3 / 4; Conclusion 3–4; Table S10 3 / 4; S9 (6.2 / 7.2 flips, 72% pass); cover letter 3–4 | MATCH (the matched floor is the simulated floor on the same draws; run.txt max |ΔFFR diff| 3.9e-7) |
| 88 | Matched throat P&W | abstract 42–49 (C); III-B 42 / 49 (C), 78 / 80 (D); IV-A 42–80; Conclusion 42–49; Table S10 42, 49, 78, 80; cover letter 42–49 | MATCH |
| 89 | Protocol D floor | abstract 9–15; III-B 15 / 9 and 9–15; IV-A 15 / 9; Conclusion 9–15; Table S10 15 / 9 | MATCH |
| 90 | Matched topological P&W under D | III-B 36 / 19; IV-A 36 / 19; Conclusion 19–36; Table S10 36 / 19 | MATCH |
| 91 | Matched caliber P&W | III-B 9–12 (C), 13–28 (D); Table S10 9 / 12, 28 / 13 | MATCH |
| 92 | Paired excesses | III-B 17 / 7 (floor, C), 12 / 5 (B, C), 16 / 6 (floor, D); Table S10 17 / 7, 16 / 6 | MATCH |
| 93 | Detector | III-C 0.82 (0.79–0.86) / 0.56 (0.54–0.59), 85 / 58, "about half", 0.77 / 0.22; IV-C 0.82, "half"; S8 0.82 / 0.56, 0.77 (0.71–0.82) / 0.22 (0.18–0.27), 83 / 19, 48 / 50; cover letter 0.82, 48% | MATCH |
| 94 | Noise-free P&W (Table I vs Table S10 "Noise-free" column vs III-B counts) | 19, 20, 5, 18, 57, 80 / 8, 5, 12, 4, 69, 81 in all three | MATCH |
| 95 | Level-2 topological P&W | abstract 2–7; III-B 7, 3 / 5, 2; Conclusion 2–7; Table S8 7, 3 / 5, 2; cover letter "removed most topological cases" | MATCH |
| 96 | 3D case values (#186) | III-D, Fig. 4 caption, S10, Fig. S1: 0.870, 0.944, 0.074, 0.892, −0.0007, +0.022, +0.081, −0.0005, +0.127, 0.276, 0.231, 0.761, 0.0021, 0.68 mL/s | MATCH |
| 97 | Repeat-FFR floor (#187) | II-F 0.018; Table I note 5.0–6.5; III-A 5.0–6.5; Fig. 2 caption 0.018 | MATCH |
| 98 | DSC statements (#189) | abstract 0.97; III-C 0.97 / 0.98, 0.89, 0.62, 91 / 62, 0.54 / 0.70; IV-B; S7; Table S9; cover letter 0.97, 0.93 | MATCH |
| 99 | Demand replication | III-D 27–29, 31–35, 52–75, 27 vs 50 (p 0.005), p 0.12 / 0.24; Table S7 ×2/×3 rows and note 50 (38–62), 34 (29–40), 33 (28–39), 47 instances; Table S5 ×2 discrete 47, 50 (38–62); ×2 leaky 34 (29–40); ×3 33 (28–39) | MATCH |
| 100 | Protocol C and D bound fits | II-D "two ... one per bed"; Table I note; S2 "two half-voxel ... 10 of 4 940"; S2 "23 half-voxel and 41 ten-point ... 43 ... 21"; S5 "2 at half a voxel, 8 at ±10", "64 Protocol D fits" | MATCH (23 + 41 = 64; S2 and S5 now agree) |
| 101 | Territories (#185) | II-D "median of two and at most three", "four ... five"; S6; Table S8 note | MATCH |
| 102 | Second floor and noisy targets | II-F "second floor ... tuned as in Protocol C"; III-B 3.1 / 3.9, 6.2 / 7.2; S9 6.2 / 7.2, 0.012, 0.05, 72%, 20 draws; Table S10 floor C 3 / 4 | MATCH (but see L1) |

Range checks (every "a–b" spans exactly the values it summarises): 32–33, 30–36, 6–10, 5–19, 2–7, 42–49, 9–15, 9–12, 13–28, 42–80, 19–36, 2–13, 18–43, 27–29, 31–35, 52–75, 0.006–0.044, 1–14, 57–81, 51–60, 78–81, 0.11–0.16, 20–29, 5.0–6.5, 13–14, 0.65–0.67, 0.0019–0.0021 — all MATCH.

### 1.10 Derived claims (10-09 rows #191–#203)

| # | Claim | Check | Verdict |
|---|---|---|---|
| 103 | #191 A ≡ B for T5; #193 "rose ... but not in the leaky bed" (+4/−0 p 0.125, +3/−4 p 1.0); #195 every flip followed the sign; #196 "all but two"; #197 topological > caliber under A–C; #198 excess held only in the discrete bed; #199 finer check removed most topological but few throat or taper P&W; #200 L1 partition exact; #201 up to 13 points; #202 all solves converged; #203 denominator consistency (Table I basis reproduces every table incl. the new Table S10 nominal column) | text unchanged; #192 now reads "were compared with the 5.0--6.5\%" (descriptive, recomputed row 24) | CARRIED (13 rows: 12 MATCH, #194 NOT-RECOMPUTABLE) |

## 2. MISMATCH list

None. No stated number in main, supplement, tables or `cover_letter.tex` disagrees with the CSVs on the paper's own basis.

Status of the four 10-09 MISMATCH items:
- **M1** (III-B "taper" label on the T3+T4 class rate) — FIXED: now "Caliber passes-and-wrong away from the throat rose under Protocol D to 23\% and 9\%, almost all taper models" (row 40; 45/194, 28/300, of which 44 and 28 are taper).
- **M2** (S2 "23 ... most failing the check") — FIXED: now "23 half-voxel and 41 ten-point throat-error models with an increased stenosis, of which 43 failed the check and 21 passed while materially wrong" (row 60); S2 and S5 agree on 64.
- **M3** (caliber mean |ΔFFR| range excluded Protocol D) — FIXED: "0.006--0.044" (row 23).
- **M4** (|ln C| undefined in Table S10) — MOOT: the detector table was removed in v2 and replaced by the S8 paragraph; no |ln C| quantity appears anywhere.
- Optional 10-09 notes N3 ("flip counts ... per cell") and N4 ("about 40\%") are applied; N1 is closed because the abstract, IV-A and Conclusion now share one 5–19% basis.

Interim-value sweep: none of the interim values (topological C 21 / 9, floor C 5 / 4, excess 18 / 8 and 14 / 6, topological D 38 / 20 with excess 17 / 7, caliber 10–14 and 14–27, AUC 0.83 / 0.57, flagged 86 / 62, interim table CIs) occurs in v2. The string "17 and 7" in III-B is the final C excess (17.1, 6.7), not the interim D excess; "0.57" in Table S2 is a GLMM interval bound; "62\%" is the leaky DSC proportion.

## 3. Logic and basis notes

**L1. Methods do not describe the noise-matched comparison (LOGIC GAP, text change recommended).** The abstract, III-B (two passages), III-C, IV-A, IV-C, the Conclusion, S8, S9, Table S10 and cover-letter bullets 2–3 now rest on error models tuned to the same 20 noisy target sets as the correct-anatomy floor, under both C and D, with per-model means over draws and cluster-bootstrap intervals, plus a Protocol D floor. II-F describes only the clean-anatomy floor "tuned as in Protocol C" and the pre-tuning detector "against correct anatomy with noisy targets", and II-D still says the tuning targets "stand in for an error-free perfusion measurement". The Results therefore introduce a design ("With the error models tuned to the same noisy targets") that the Methods never define; only S9 does. The Limitations sentence was correctly changed to "Outside the noise-matched comparison, tuning targets were error-free clean-model flows", which presupposes a Methods definition that is absent.

CURRENT (main.tex, lines 209–210, end of the noise-floor paragraph):
```
A second floor was simulated on the clean anatomy with physiological
noise in demand, pressure, viscosity and the measured territory flows, tuned as in Protocol C (Supplementary Material).
```
PROPOSED (append one sentence; adds about 45 words to a full page 9, so a compensating cut may be needed):
```
A second floor was simulated on the clean anatomy with physiological
noise in demand, pressure, viscosity and the measured territory flows, tuned as in Protocol C (Supplementary Material). In a noise-matched comparison, every error model was also tuned under Protocols C and D to the same 20 noisy target sets as the correct anatomy of its instance, with a Protocol D floor computed likewise; its rates are per-model means over draws with patient-level bootstrap intervals (Supplementary Material).
```

**L2.** II-D "the clean model's territory flows, which stand in for an error-free perfusion measurement" remains correct for the primary analysis and is reconciled by the Limitations sentence; no change needed once L1 is in.

**L3.** S8 cites `Table~\ref{tab:matched}` for the matched AUC (0.82 / 0.56), but Table S10 carries no AUC; the reference points to the design only. Acceptable; "(matched design, Table~S10)" would be exact.

**B1.** Table S10 gives n = 194 and 300 for the throat error under Protocol C (models with a defined residual in at least one draw), whereas Table I and the "Noise-free" column (57, 69) use 193 and 299 (one nominal Protocol C fit per bed at its bound). The script's definition ("n counts models with a defined residual") is stated in S9; a reader comparing with Table I will see 194 against 193. Optional table note: "n: models with a defined residual in at least one draw; the noise-free column uses the Table I denominators."

**B2.** III-A "Only the taper's rates in the discrete bed ... had lower confidence bounds (8\% and 9\%) above that floor": the leaky taper under A has a lower bound of 5.6%, inside the quoted 5.0–6.5% range but above its own cell's floor (5.1%). The sentence holds on the range reading; "above 6.5\%" would remove the ambiguity.

**B3.** III-A throat tuning "$p = 0.22$ and 0.06" are Holm-adjusted across the two contrasts (raw 0.219 and 0.031), consistent with II-F; the discrete-bed values are < 0.001 either way.

**B4.** III-A "produced the fewest flips among Protocols A--C": true for topological errors in both beds and caliber errors in the leaky bed; for caliber errors in the discrete bed B and C tie (15/194 each). The sentence continues with topological contrasts, so no change needed.

**B5.** S9 "means over the 20 draws per instance": models whose Protocol C fit ended at the bound on some draws (110 of about 138 000 rows) average over fewer draws (minimum 4, median 20). Rates differ by < 0.1 point if those models are dropped.

**B6.** S10 "about 10~mL/min ... about 0.7~m/s ... Reynolds number about 110": the flow through the two outlets beyond the lesion is 10.4 mL/min with prescribed clean flows (Re 106) and 12.0 mL/min with the clean tree's resistances (Re 123). The sentence corresponds to the prescribed-flow case; "within the laminar regime" holds for both.

**B7.** The abstract is exactly 250 words by whitespace count (hyphenated ranges and "0.05" as one word each). Any edit must be word-neutral.

## 4. Portal cover letter (`cover_letter_portal.txt`)

The file is byte-identical in `drafts/manuscript/` and `drafts/manuscriptv2/` (copied 10-10 08:35 but not regenerated) and is an older version of the letter: it predates the T5 (throat) integration, the overlap/detector bullet, the code release and the noise-matched numbers. It must be regenerated from `cover_letter.tex` before upload. Disagreements:

1. **Title.** Portal: "Topological Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study". Manuscript and `cover_letter.tex`: "Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study".
2. **Error count.** Portal: "applied four segmentation error types". Manuscript and tex: five, "including a half-voxel error in the stenosis throat".
3. **Innovation paragraph.** Portal separates "topological errors ... from caliber errors of measured inter-observer size" and names the 3D CFD test as the third point, with "to our knowledge for the first time". Tex: compares "errors in the branching, in the caliber and at the stenosis throat" and the third point is passes-and-wrong plus "what overlap scores reveal of these errors"; no priority claim.
4. **Bullet 1.** Portal: "32–33% of models ... compared with 6–10%" (no throat error). Tex: "about a third of models ... (30--36\%), against 6--10\%". Portal numbers are still correct but omit the throat result that the manuscript leads with.
5. **Bullet 2 (portal only).** "a vessel break changed the decision in 43% of models with fixed boundary conditions and in 5% with re-derived ones" — leaky-bed T2 values (42.9%, 4.7%) without saying so (discrete bed: 40%, 18%); not in the tex letter.
6. **Bullet 3 (portal) vs bullet 2 (tex).** Portal gives the noise-free passes-and-wrong "19–20% (discrete bed) and 5–8% (leaky bed) of tuned topological-error models and 4–18% of tuned caliber-error models ... against 3–4%". Tex and manuscript now give the noise-matched "19\% (discrete bed) and 8\% (leaky bed) of topological-error models and 42--49\% of throat-error models ... against 3--4\% of correct models" and add "A check one branching level finer removed most topological cases but few throat cases". The portal figures are correct for Table I but are no longer the letter's claim.
7. **"per-territory tuning corrected the typical missed branch, as it did in a single three-dimensional case"** (portal) — true (D medians 0.000 / 0.004; 3D −0.0007) but absent from the tex letter.
8. **Missing bullet.** The tex third bullet (Dice 0.97 against 0.93 inter-observer, twice the decision changes, pre-tuning mismatch AUC 0.82, 48% false alarms) has no counterpart in the portal text; the portal only says "overlap-based segmentation metrics do not capture the error types that carry the decision risk".
9. **Significance.** Portal lacks the tex statements that the results "locate where segmentation quality matters ... at the branching near the lesion and at the throat diameter", that perfusion agreement "is calibration evidence rather than validation evidence", and that "The test uses public data and open code and can be applied to other pipelines".
10. **Code availability (contradicts the manuscript).** Portal: "The code is available from the corresponding author upon reasonable request." Tex and main-text Data and Code Availability: "The analysis code is available at https://github.com/zulhilmi-ismadi/ctffr-segmentation-ablation".
11. **Demand wording.** Portal: "a replication at doubled and tripled hyperemic demand"; tex: "a demand replication" (both correct; wording only).

Unchanged and correct in both: addressees and salutation, special-issue title, "150 controlled stenoses into 108 coronary trees", the two CfP topics, the three Journal papers (Viceconti 2025, Chen 2025, Arminio 2026), originality / conflict / funding / ImageCAS-X CC BY 4.0 statements, and the signature block.

## 5. Counts

- Rows: 213 (81 statement, table and cover-letter rows in §1.1–1.8, 21 cross-location rows in §1.9, 13 derived-claim rows in §1.10 counted individually, with grouped CARRIED rows counted by the 10-09 rows they cover: rows 14 (29), 17 (16), 20 (9), 26 (4), 27 (11), 43 (3), 45 (7), 61 (3), 63 (11), 64 (4), 66 (2), 69 (6), 70 (7), 103 (13)).
- By verdict: MATCH 80 (59 recomputed + 21 cross-location); ROUNDING 0 new (1 carried, #87); MISMATCH 0; NOT-RECOMPUTABLE 1 new (row 81) plus 10 carried (#14, #26, #34, #35, #37, #38, #113, #140, #154, #194; parts of #117, #170–#172); CARRIED 129; REMOVED (text no longer exists) 3 (#118, #143, #144).
- Values recomputed today: about 330 (noise-matched table 48 cells incl. n, matched text values about 35, Table S7 ×2/×3 27 incl. note, Table S3 56, Table I spot cells about 60, III-A/III-B/III-C/Conclusion and supplement text about 100). Values carried: about 1 100.
- Logic: 1 gap (L1, Methods omit the noise-matched design; proposed sentence above), 2 minor (L2, L3); basis notes B1–B7, none requiring a number change.
