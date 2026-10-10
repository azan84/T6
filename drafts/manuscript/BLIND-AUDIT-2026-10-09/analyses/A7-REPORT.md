# A7 report: pre-tuning residual and fitted scaling as detectors (T2-4), 2026-10-09

## 1. Design as run (fixed before the full run)

**Detectors**
- (a) **Pre-tuning residual.** This is the Protocol B perfusion residual, `outlet_flow_residual` of the `B_rederived` rows in `ablation-2026-10-07.csv`. The bed is re-derived on the corrupted tree and there is no tuning. The targets are the error-free clean territory flows, as in Table I.
- (b) **Fitted scaling relative to its start, |ln(C_C / C_B)|.**
  - Column semantics: in the frozen CSV, `C_ratio = C / C_clean`, where C_clean is the calibration of the *clean* tree. It is not the corrupted tree's own start.
  - The start of the Protocol C fit is C_start = the Protocol B calibration of the corrupted tree. The factor a pipeline actually observes is therefore C_ratio(C row) / C_ratio(B row).
  - For the negatives, C_start = C_clean (verified: the difference is 0), so |ln C_ratio| is already relative to the start.
  - Fable's "0.047 vs 0.015" is log10 of C/C_clean. I report it as a secondary row only (`abs_ln_C_vs_clean` in the CSV).

**Negatives**
- Correct anatomy, 20 draws per instance, seed 20260919, with the physiological noise model of `negatives.py` (unchanged).
- Pre-tuning residual = sqrt(loss at log10 C_start), which equals sqrt(lv[30]) of the 61-point grid. Both values were recorded and are identical.
- |ln C| uses fits with status ok, so the 10 leaky draws whose fit hit the search bound are excluded, as in Table S7.

**Positives**
- Error models with a defined residual. The discrete arm is restricted to the 97 eligible instances.
- Target (i), error class: T1 or T2 models.
- Target (ii), decision change:
  - for (a), any error type (T1–T4) that flips under B;
  - for (b), any error type that flips under C or passes and is wrong under C (residual < 0.10 and |ΔFFR| > 0.05), with C defined.
  - The topological-only variants are in the CSV.

**Secondary comparison: same noise on the error models' targets**
- The primary design compares error models scored against noise-free targets with correct models scored against noisy targets. This follows the paper's convention (tuning targets are error-free), but it is asymmetric.
- I therefore also scored each B error model against each of the 20 noisy target draws of its own instance and bed. I recomputed the residual from `ablation-2026-10-07_territory.csv` and matched territories by clean root node.

**Metrics**
- AUC by Mann–Whitney, alarm = higher score.
- 95% CI from an instance-level cluster bootstrap: 2000 resamples, seed 20261009, keeping all models and draws of each resampled instance.
- Sensitivity and false-alarm rate (FAR) at 0.10, with alarm when score ≥ 0.10. For |ln C|, 0.10 is a 10.5% scaling change, not a check threshold.
- Sensitivity and FAR at the 95th percentile of the negative draws in each bed (the 5% FAR threshold).
- Wilson 95% CIs. These are descriptive because they ignore clustering.

## 2. Validation

- **Wrapper:** `code/a7_detector_negatives_pretune.py` monkeypatches `fit_global_scaling` and `run_instance` only. These functions use no random numbers, so the random stream is untouched.
  - Pilot on 2 instances (80 draws): identical to the frozen file.
  - Full run, all **5,860 of 5,860** rows match `negatives-2026-10-07.csv` by run_id: maximum |difference| = 0 for the post-tuning residual, ΔFFR, C_ratio and FFR. Status is identical, with 10 failed fits as before.
- **Recomputed B residual:** recomputing it from the territory rows reproduces `outlet_flow_residual` to 8.9e-16.
- **Pure clean anatomy, no noise:** the B residual of the correct model against its own targets has a maximum of 3.8e-9 and a median of 9.6e-10 over 247 instance-beds. It is effectively 0, as expected.
- **Frozen IV-C numbers reproduce:**
  - re-derived topological models passing where C is defined: 23/104 = 22% (discrete) and 152/171 = 89% (leaky);
  - B residual medians: 0.196 topological vs 0.021 caliber (discrete) and 0.027 vs 0.012 (leaky).

## 3. Results

**False-alarm rate under physiological noise (correct anatomy, before tuning)**
- Pre-tuning residual median: 0.097 (IQR 0.063–0.139) discrete; 0.101 (0.065–0.142) leaky.
- At the 0.10 check, **48% (46–50%) of correct-anatomy draws in the discrete bed and 50% (49–52%) in the leaky bed would be flagged.**
- The 5% FAR threshold is 0.22 (discrete) and 0.23 (leaky).
- For comparison, 28% of the same draws fail after tuning (Table S7).
- The fitted scaling |ln C| of correct models has a median of 0.07 in both beds, and its 5% FAR threshold is 0.24. Tuning to noisy targets moves C by about as much as most errors do.

**Table: detection per bed.** n is the number of positives. Negatives: 1,940 draws on 97 instances (discrete); 3,000 draws (2,990 for |ln C|) on 150 instances (leaky).

| Bed | Detector | Target | n | AUC (95% CI) | Sens. at 0.10, % | FAR at 0.10, % | Thr. at 5% FAR | Sens. at 5% FAR, % |
|---|---|---|---|---|---|---|---|---|
| Discrete | B residual | Topological | 137 | 0.77 (0.71–0.82) | 83 (76–89) | 48 | 0.22 | 47 (39–55) |
| | | Topological, noisy targets | 137×20 | 0.82 (0.79–0.85) | 85 (84–86) | 48 | 0.22 | 53 (51–55) |
| | | Flip under B (any type) | 36 | 0.57 (0.46–0.69) | 69 (53–82) | 48 | 0.22 | 22 (12–38) |
| | | Flip under B (topological) | 21 | 0.79 (0.67–0.89) | 90 (71–97) | 48 | 0.22 | 38 (21–59) |
| | |ln C| | Topological | 104 | 0.47 (0.40–0.53) | 30 (22–39) | 37 | 0.24 | 9 (5–16) |
| | | Flip or P&W under C (any type) | 61 | 0.53 (0.44–0.62) | 41 (30–54) | 37 | 0.24 | 15 (8–26) |
| Leaky | B residual | Topological | 218 | 0.22 (0.18–0.27) | 19 (15–25) | 50 | 0.23 | 6 (3–9) |
| | | Topological, noisy targets | 218×20 | 0.56 (0.54–0.58) | 58 (57–60) | 50 | 0.23 | 13 (12–14) |
| | | Flip under B (any type) | 16 | 0.21 (0.08–0.36) | 12 (3–36) | 50 | 0.23 | 6 (1–28) |
| | |ln C| | Topological | 171 | 0.12 (0.09–0.15) | 3 (1–7) | 34 | 0.24 | 2 (1–5) |
| | | Flip or P&W under C (any type) | 66 | 0.66 (0.55–0.77) | 61 (49–71) | 34 | 0.24 | 59 (47–70) |

**Secondary results**
- **Topological vs caliber (Fable's contrast, no noise on either side):** B residual AUC 0.90 (0.87–0.93) in the discrete bed and 0.56 (0.51–0.60) in the leaky bed. For |ln C|: 0.70 and 0.41.
- **|ln C| relative to the clean calibration (not observable in deployment):** AUC for topological errors 0.62 (0.55–0.69) in the discrete bed and 0.22 in the leaky bed.

**Interpretation**
1. **Discrete bed.** The pre-tuning residual ranks topological errors above noisy correct anatomy (AUC 0.77; 0.82 with noise on both). At the 0.10 check it flags 83% of them, but also 48% of correct models. At a 5% false-alarm rate it catches about half.
2. **Leaky bed.** The detector fails. An AUC below 0.5 means the residual a topological error causes (median 0.027) is smaller than the residual physiological noise alone causes (0.10). With noise on both sides, the AUC is 0.56.
3. **Decision change.** For any error type, the B residual is weak (0.57 discrete, 0.21 leaky). Caliber flips carry no residual.
4. **|ln C| does not detect topological errors.** The AUC is at or below 0.5 in both beds. It does detect tuned taper errors:
   - In the leaky bed, 36 of 38 taper decision changes exceed the 5% FAR threshold (median |ln C| 0.42; taper-only AUC 0.94). This is why the leaky "flip or P&W under C" row reaches 0.66.
   - In the discrete bed, the figure is 7 of 16 (taper-only AUC 0.70).

## 4. What it means for the paper's claims

**IV-C, third consideration**
> "Third, record the perfusion mismatch before tuning, which erases it: in the discrete bed only 22% of re-derived topological-error models passed, although in the leaky bed most did."

- **The numbers are correct (22%, 89%), but the sentence implies a usable signal that is not there under physiological noise.** At 0.10, 52% of correct-anatomy models pass before tuning, so "22% passed" sits against a comparator of 52%, not 100%.
- **The sentence must gain the false-alarm rate and the restriction to the discrete bed.**
- **"which erases it" is too strong for Protocol C in the discrete bed.** The median topological residual falls from 0.22 (A) to 0.14 (C) and is not erased. It is erased only under D (< 1%) and in the leaky bed under C (0.02).

**Conclusion**
> "a record of the perfusion mismatch before tuning, which tuning erases."

- **Restrict it to discrete beds and drop "which tuning erases".** The same reason applies.
- **The claim survives only in the discrete bed, with a high false-alarm rate.** No abstract number changes.

**Not supported**
- **Do not add a claim that the fitted tuning factor is a detector of topological error.** It is not one.
- **It could optionally be mentioned as a flag for tuned caliber (taper) errors in the leaky bed.** That would be a new finding with a supplement line, not a main-text claim; I recommend the supplement only.

## 5. Draft text

### (a) Main text (two replacements, each shorter than the sentence it replaces)

**IV-C third consideration.** The current sentence is 181 characters; the draft is 177.
> Third, record the perfusion mismatch before tuning: it marked topological errors only in the discrete bed (AUC 0.77), and half of correct models with noisy targets exceeded 10\%.

**Conclusion.** The current text is 70 characters; the draft is 68. The preceding "and" is kept.
> for discrete beds, a record of the perfusion mismatch before tuning.

### (b) Supplement paragraph and table

> **Detection before and during tuning.**
> - The perfusion residual before tuning (Protocol B) and the fitted Protocol C scaling relative to its start, $|\ln(C_\mathrm{C}/C_\mathrm{B})|$, were evaluated as detectors.
> - Positives are error models with a defined residual. Negatives are the 20 draws per instance of the simulated floor, evaluated before tuning with the same noise model.
> - The area under the ROC curve (AUC) carries an instance-level bootstrap interval (2000 resamples). Sensitivity and false-alarm rate are given at 0.10 and at the value exceeded by 5\% of the negatives (Table~\ref{tab:detector}).
> - Without noise, correct anatomy has a residual below $10^{-8}$. With physiological noise, its median residual before tuning is 0.10, and 48\% (discrete) and 50\% (leaky) of draws exceed 0.10.
> - In the discrete bed, the residual separated topological errors from correct anatomy (AUC 0.77; 0.82 when the error models' targets carried the same noise). In the leaky bed, the residual caused by a topological error was smaller than that caused by noise (AUC 0.22; 0.56 with noise on both).
> - The fitted scaling did not separate topological errors from correct anatomy in either bed (AUC 0.47 and 0.12). In the leaky bed it exceeded the 5\% false-alarm value in 36 of 38 taper models whose decision changed after tuning.

```latex
\begin{table}[!ht]
\caption{Detection Before and During Tuning Against Correct Anatomy With Noisy Targets}\label{tab:detector}
\centering\small
\begin{tabular}{@{}lllrcccccc@{}}
\toprule
Bed & Quantity & Positives & $n$ & AUC & Sens. at 0.10, \% & FA at 0.10, \% & 5\% FA value & Sens. at 5\% FA, \%\\
\midrule
Discrete & Pre-tuning residual & Topological & 137 & 0.77 (0.71--0.82) & 83 (76--89) & 48 & 0.22 & 47 (39--55) \\
 &  & Topological, noisy targets$^a$ & 137$\times$20 & 0.82 (0.79--0.85) & 85 (84--86) & 48 & 0.22 & 53 (51--55) \\
 &  & Flip under B$^b$ & 36 & 0.57 (0.46--0.69) & 69 (53--82) & 48 & 0.22 & 22 (12--38) \\
 & $|\ln C|$ & Topological & 104 & 0.47 (0.40--0.53) & 30 (22--39) & 37 & 0.24 & 9 (5--16) \\
 &  & Flip or P\&W under C$^b$ & 61 & 0.53 (0.44--0.62) & 41 (30--54) & 37 & 0.24 & 15 (8--26) \\
\midrule
Leaky & Pre-tuning residual & Topological & 218 & 0.22 (0.18--0.27) & 19 (15--25) & 50 & 0.23 & 6 (3--9) \\
 &  & Topological, noisy targets$^a$ & 218$\times$20 & 0.56 (0.54--0.58) & 58 (57--60) & 50 & 0.23 & 13 (12--14) \\
 &  & Flip under B$^b$ & 16 & 0.21 (0.08--0.36) & 12 (3--36) & 50 & 0.23 & 6 (1--28) \\
 & $|\ln C|$ & Topological & 171 & 0.12 (0.09--0.15) & 3 (1--7) & 34 & 0.24 & 2 (1--5) \\
 &  & Flip or P\&W under C$^b$ & 66 & 0.66 (0.55--0.77) & 61 (49--71) & 34 & 0.24 & 59 (47--70) \\
\bottomrule
\end{tabular}

\parbox{\linewidth}{\footnotesize Negatives: 1\,940 (discrete) and 3\,000 (leaky; 2\,990 for $|\ln C|$) correct-anatomy draws on 97 and 150 instances. FA, false alarm; P\&W, passes and wrong. $^a$Each error model against the 20 noisy target draws of its instance. $^b$Any error type.}
\end{table}
```

The body alone is in `results/a7_detector-2026-10-09/tab_detector.tex`, for `\inputtab`. The table has 10 rows. To reach about 8, drop the two "noisy targets" rows and keep their AUCs in the paragraph.

## 6. Runtime and files written

**Runtime**
- Negatives rerun: about 44 min (5,860 draws).
- 2-instance validation: 38 s.
- Analysis: about 1 min.

**Files**
- `code/a7_detector_negatives_pretune.py`: wrapper around `negatives.py`.
- `code/a7_detector_analysis.py`: metrics.
- `results/a7_detector-2026-10-09/`:
  - `negatives_pretune.csv`: frozen columns plus `pretune_resid`, `pretune_resid_grid30`, `C_start`, and per-territory flows at the start and noisy targets;
  - `negatives_pretune_pullback.csv`;
  - `negatives_pretune.log`;
  - `validation_limit2.csv` and its pullback file;
  - `detector_metrics.csv`;
  - `detector_summary.txt`;
  - `tab_detector.tex`.
