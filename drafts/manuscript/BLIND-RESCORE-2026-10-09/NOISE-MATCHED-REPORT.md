# G1 + G5: matched-noise rerun with a Protocol D floor (2026-10-09)

Status: INTERIM. The 20-draw run is still computing (section 6); sections 3–5 use draws 0–1, which are complete for all 247 instance-beds. When the run finishes, `noise_matched_run.py assemble` followed by `noise_matched_analysis.py` (no argument) regenerates every number below on all 20 draws; the definitions do not change, only the sampling noise.

## 1. Design as run

**Question.** Table I and the abstract compare error models tuned to *noise-free* targets with a correct-anatomy floor tuned to *noisy* targets. This rerun tunes every error model to the same recorded noisy targets as the floor, so that the passes-and-wrong contrast is like-for-like, and adds the Protocol D floor that the paper does not have.

**Targets.** For each cohort instance, bed and recorded draw d = 0..19, the Protocol C and D targets are the clean main-branch territory flows of `ablation.protocol_c_targets` multiplied, territory by territory, by the ratio `terr_target_mls / terr_pred_start_mls` recorded for that draw in `results/a7_detector-2026-10-09/negatives_pretune.csv` (the draws of `negatives.py` as used for Table S11 and Table S8). The corrupted model itself stays nominal, exactly as the floor does in `negatives.py`. Draw -1 is the nominal (noise-free) case and must reproduce the frozen runs.

**Error types.** `T0_identity` (correct anatomy; the floor), T1–T4 from `error_types.py`, and the two half-voxel throat variants `T5_vox_narrow` / `T5_vox_wide` from `t5_throat_error_types.py`. The identity type is in `CALIBRE_ONLY` so the clean node set is kept (same convention as T3/T4/T5). All seven run in one task per instance, bed and draw, so the clean solve is shared.

**Protocols.** A–C from `ablation.run_instance`, D from `ablation_per_territory.run_instance`, frozen modules imported unchanged and patched in memory only (`ablation.protocol_c_targets` replaced; error-type set and insertion function swapped as in `t5_throat_run.py`). Under A and B the targets only enter the perfusion residual (the pass criterion), not the FFR.

**Cohort basis (fixed before the run).** Leaky bed: all 150 instances. Discrete bed: the 97 eligible instances only (`results/discrete_arm_eligibility.csv`), i.e. the Table I basis; the 53 ineligible discrete instances were not run (saves 18% of compute on today's critical path and are never reported). 21 cases (nominal + 20 draws) per instance-bed: 5 187 tasks.

**Endpoints (fixed before the run).**
- Passes-and-wrong: residual < 0.10 and |ΔFFR| > 0.05; denominator = models with a defined residual (as Table I).
- Matched rate of a class (topological = T1+T2; caliber = T3+T4; throat = ±half-voxel, both signs as separate models; floor = identity): for each model, the passes-and-wrong indicator averaged over its 20 draws (per-model probability); the class rate is the mean over models.
- Matched floor: the identity model's per-model probability, averaged over instances, for C and for D (under A and B the identity has ΔFFR = 0, so its passes-and-wrong is 0 by construction).
- Paired excess over the floor: per model and draw, pw(error model) − pw(identity of the same instance, bed, draw, protocol); averaged over draws, then over models.
- Paired excess over Protocol B on the same draws: pw_C or pw_D (model, draw) − pw_B (model, draw).
- Intervals: patient-level (scan) cluster bootstrap, 2 000 resamples, seed 20261009; Wilson intervals on the pooled model-draws are written to the CSV for reference only (they ignore the clustering).
- Detector: AUC of the Protocol B residual of error models with noisy targets against the identity model's Protocol B residual on the same draws (the quantity Table S8 reports as 0.82/0.56 for topological errors), plus |ln(C_C/C_B)| under C; patient-level cluster bootstrap.

**Code.** `code/noise_matched_run.py` (validate / run / assemble) and `code/noise_matched_analysis.py`. Outputs in `results/noise_matched-2026-10-09/`.

## 2. Validation (6 instances, both beds, nominal + 20 draws; 252 tasks)

Instances (five bands): 306_left_LAD_prox_20mm_80, 812_left_LCX_mid_20mm_80, 937_left_LCX_mid_10mm_75, 832_left_LCX_prox_10mm_75, 211_left_LAD_mid_10mm_65, 890_right_RCA_mid_20mm_50. All seven error types present (1 008 ok rows each; T2 903).

| Check | Result |
|---|---|
| Nominal (draw -1) T1–T4 and ±half-voxel throat, Protocols A–D, against `ablation-2026-10-07.csv`, `ablation-perterritory-2026-10-08.csv`, `t5_throat-2026-10-09/*.csv` | n = 283 rows, 0 unmatched, max abs FFR difference **0.0**, max abs residual difference **0.0** (every protocol) |
| Nominal identity | n = 48, max abs ΔFFR 0.0, max residual 2.2e-16 |
| Identity under C with noisy targets against the recorded floor draws (`negatives_pretune.csv`) | n = 240, max abs ΔFFR difference **1.4e-7**, residual 3.9e-9, C_ratio 6.5e-7 |
| Identity under B against the recorded `pretune_resid` | n = 240, max difference 3.8e-9 |

Both acceptance criteria of the go-list (nominal = frozen at 0.0; identity-C = a7 below 1e-6) are met. A first validation attempt ran only the identity and throat types because `t5_throat_error_types.install()` replaces the error-type set before T1–T4 were copied; this was fixed (types captured before `install`), the cache cleared and the validation repeated in full before the run was launched. File: `results/noise_matched-2026-10-09/validation.txt`, `validation_rows.csv`.

## 3. Results (interim: draws 0–1, all 247 instance-beds; final numbers from the 20-draw run)

Validation on the full cohort (`run.txt`): nominal rows identical to the frozen runs (n = 5 342, max |FFR difference| 0.0 under every protocol; the 8 rows the check lists as unmatched are scan 549's two discrete-bed T2 models, "ok" with an undefined FFR in both runs); identity under C reproduces the recorded floor draws (n = 990, max |ΔFFR difference| 3.9e-7); identity under B reproduces `pretune_resid` (5.4e-9).

### 3.1 Passes-and-wrong, % of models (per-model probability over the draws; patient-level cluster-bootstrap 95% intervals)

Nominal = noise-free targets (Table I basis; reproduces Table I). Matched = error model tuned to the recorded noisy targets. Floor = correct anatomy on the same draws. Excess = paired difference, averaged over draws then models. n = models with a defined residual.

| Bed | Class | Protocol | n | Nominal | Matched | Matched floor | Excess over floor | Excess over B (same draws) |
|---|---|---|---|---|---|---|---|---|
| Discrete | Topological (T1+T2) | C | 104 | 19 | 21 (14–28) | 5 (2–8) | 18 (11–25) | 14 (8–21) |
| Discrete | Topological | D | 104 | 20 | 38 (28–46) | 15 (10–20) | 17 (10–25) | 31 (22–40) |
| Discrete | Caliber (T3+T4) | C | 194 | 5 | 10 (6–14) | 5 (2–8) | 5 (1–9) | 10 (7–14) |
| Discrete | Caliber | D | 194 | 18 | 27 (21–32) | 15 (10–20) | 12 (7–16) | 27 (21–32) |
| Discrete | Throat (±½ voxel) | C | 192 | 57 | 42 (36–49) | 5 (2–8) | 38 (32–44) | 25 (20–31) |
| Discrete | Throat | D | 194 | 80 | 78 (72–85) | 15 (10–20) | 63 (56–70) | 61 (55–67) |
| Leaky | Topological | C | 171 | 8 | 9 (5–14) | 4 (2–7) | 8 (4–12) | 6 (2–9) |
| Leaky | Topological | D | 171 | 5 | 20 (14–26) | 9 (6–13) | 7 (3–11) | 16 (11–21) |
| Leaky | Caliber | C | 300 | 12 | 14 (11–18) | 4 (2–7) | 10 (7–13) | 14 (11–18) |
| Leaky | Caliber | D | 300 | 4 | 14 (11–18) | 9 (6–13) | 5 (2–8) | 14 (11–18) |
| Leaky | Throat | C | 299 | 69 | 49 (43–55) | 4 (2–7) | 45 (39–51) | 27 (22–32) |
| Leaky | Throat | D | 300 | 81 | 80 (74–85) | 9 (6–13) | 71 (65–76) | 58 (53–62) |

Matched floor (correct anatomy, n = 97 / 150 instances): C 4.6% (2.1–7.5) discrete, 4.3% (2.2–6.9) leaky, against 3.1% / 3.9% on all 20 draws (Table S11; the 2-draw subset sits inside those intervals and will converge to them); **D 14.9% (10.4–19.9) and 9.0% (5.5–13.2)**, the floor the paper does not have. Matched flip rates: topological C 22% / 14%, D 16% / 11%; throat 37–38% under C and D in both beds; floor C 8% / 8%, D 8% / 5%.

The excess over the floor is a paired quantity on the error models' own instances, so it is not the difference of the two column means (for example, leaky topological C: 9.4 − 4.3 = 5.1 as a difference of means but 7.9 paired, because the floor is lower on the instances where T1/T2 are defined under C).

### 3.2 Detector on the same draws (pre-tuning Protocol B residual; negatives = correct anatomy, same draws)

| Bed | Positives | n (model-draws) | AUC (95% CI) | Flagged at 10% | Floor flagged at 10% |
|---|---|---|---|---|---|
| Discrete | Topological | 274 | 0.83 (0.79–0.88) | 86% | 47% |
| Discrete | Throat | 388 | 0.72 (0.69–0.76) | 75% | 47% |
| Discrete | Caliber | 388 | 0.54 (0.52–0.57) | 52% | 47% |
| Leaky | Topological | 436 | 0.57 (0.54–0.60) | 62% | 52% |
| Leaky | Throat | 600 | 0.64 (0.61–0.67) | 68% | 52% |
| Leaky | Caliber | 600 | 0.58 (0.56–0.60) | 62% | 52% |

The topological AUCs reproduce Table S8's matched values (0.82 / 0.56 on all 20 draws) within the draw subset. |ln(C_C/C_B)| under C: 0.60 (0.55–0.65) discrete, 0.48 (0.45–0.52) leaky (not separating, as in Table S8).


### 3.3 Stability check (all draws cached at 08:10 on 10-10: 2 761 of 5 187 tasks, 108 instance-beds complete, median 3 draws per model; scratch only)

Topological C 20% / 9% (excess over floor 18 / 7), D 35% / 19% (excess 17 / 5); throat C 42% / 49%, D 78% / 80%; caliber C 8% / 14%, D 26% / 14%; floor C 3.1% / 4.6%, D 13.6% / 9.5%; topological AUC 0.80 (0.76–0.85) / 0.57 (0.54–0.59). Every headline cell is within 3 points of the draws 0–1 basis in 3.1, and the C floor is already at Table S11's 3.1% in the discrete bed. The drafts in section 5 will need only point-level refreshes from the full run.

Files: `results/noise_matched-2026-10-09/{matched_rows.csv, matched_rates.csv, matched_per_model.csv, matched_auc.csv, summary.txt, tab_noise_matched.tex, run.txt, validation.txt, validation_rows.csv}`.

## 4. What it means for the paper's claims

**How the headline changes.** Under Protocol C the contrast survives matching almost unchanged: topological passes-and-wrong 21% (discrete) and 9% (leaky) against a matched floor of 5% and 4%, paired excess 18 and 8 points with intervals excluding zero in both beds (and 14 / 6 points over Protocol B on the same draws). Throat passes-and-wrong under C *fall* on the matched basis, from 57 / 69% to 42 / 49%, because noisy targets make more throat models fail the check (pass rate 55–62% against 70–80% noise-free); the excess over the floor is still 38 / 45 points. Caliber errors away from the throat rise slightly (5 → 10% discrete; 12 → 14% leaky). Under Protocol D everything rises, including correct anatomy: exact matching to noisy targets leaves 15% (discrete) and 9% (leaky) of correct-anatomy models wrong by more than 0.05, topological-error models 38% and 20%, throat 78–80%, caliber 27% and 14%. The paired excess of topological errors over the D floor (17 / 7 points) is the same size as under C; so D does not reduce the residual error relative to its own floor, it raises the floor. The D numbers must therefore be reported as residual error after exact matching, against the D floor, never against the C floor of 3–4%.

| Current sentence | Verdict | Direction |
|---|---|---|
| Abstract: "...passed models wrong by more than 0.05 in 19--20\% (discrete) and 5--8\% (leaky) of topological-error cases and 57--81\% of throat-error cases. Other caliber errors did so in 4--18\% and correct anatomy in 3--4\%." | Must change: the error figures are noise-free and the 3–4% is noisy; 57–81% and 4–18% mix C and D, and D has no floor in the paper. | Restate on the matched basis for C (21 / 9%, 42–49%, 10–14%, floor 4–5%); D as residual error after exact matching with its floor (20–38%, 78–80%, 14–27%, floor 9–15%). |
| III-B: "Models with correct anatomy ... 3.1\% (2.4--4.0\%) and 3.9\% (3.2--4.6\%) of draws ..." | Stands (it is the 20-draw floor) but needs the matched comparison after it. | Add two sentences with the matched C and D figures and paired excesses. |
| III-B: "near the 3--4\% of correct anatomy at main-branch level" (finer territories) | Stands; the finer-level figures are noise-free, like the 3–4% C floor they are compared with. | None now; the 20-draw matched C floor equals 3.1 / 3.9% by construction (same draws). |
| III-B throat sentence "after Protocol C 57\% and 69\%, and after Protocol D 80\% and 81\%" | Stands as the noise-free figure; add the matched figure. | Append "with noisy targets 42 / 49% (C) and 78 / 80% (D), against 15 / 9% for correct anatomy". |
| III-C: "AUC 0.77 against 0.22" | Must change (R3 W3, EIC W1): unequal noise. | Quote the matched AUCs 0.83 / 0.57 with intervals (noise-free values in parentheses). |
| IV-A: "in the discrete bed one in five tuned topological-error models passed while materially wrong under either form of tuning" | Stands on the noise-free basis; for D the matched figure is 38% against a 15% floor. | Add one sentence on the matched basis; "one in five" stays for C. |
| IV-A: "For the throat error ... 57--81\% of models" | Stands; add the matched range. | "(42--80\% with noisy targets)". |
| IV-C: "(AUC 0.77)" | Must change. | "(AUC 0.83 with the same noise on both)". |
| Conclusion: "Up to one in five ... 57--81\% of throat-error models ... against 3--4\% for correct anatomy" | Must change (like-for-like). | Matched basis for C; D as residual error against its floor. |
| Supplement S8 text "0.82 (discrete) and 0.56 (leaky)" | Stands (same quantity, 20 draws). | None. |
| Supplement Table S11 (floor) | Superseded by the new table, which carries its pass-and-wrong column for C and adds D. | Cut; fold flips, median and 95th percentile into one S9 sentence. |

The caveat that remains after the full run: the matched comparison still measures ΔFFR against the nominal clean FFR, so Protocol B carries no physiological deviation that tuning could correct (R2 W2); the Limitations sentence from G3 covers it.

## 5. Draft text (do not apply). Interim numbers; refresh every figure from `matched_rates.csv` / `matched_auc.csv` after the 20-draw run before applying.

### (a) Abstract (250 words after the change; current 249). OLD strings copied from the current `main.tex` (each matches exactly once).

OLD 1:
```
Fractional flow reserve (FFR), which guides coronary revascularization, can be computed from computed tomography
angiography. The computation depends on the segmented artery and on outlet boundary conditions derived from it,
often tuned to measured perfusion, as in a digital twin.
```
NEW 1:
```
Fractional flow reserve (FFR), which guides revascularization, is computed from computed tomography
angiography. The computation depends on the segmented artery and on outlet boundary conditions derived from it and
often tuned to measured perfusion, as in a digital twin.
```
OLD 2:
```
under fixed, re-derived and tuned boundary conditions,
with one global or per-territory parameter fitted to clean main-branch territory flows. For the error magnitudes studied, in this threshold-stratified cohort with fixed boundary conditions,
branching (topological) errors changed the decision in 32--33\% of models and the half-voxel throat error in
30--36\%,
```
NEW 2:
```
under fixed, re-derived and tuned boundary conditions
(one global or per-territory parameter fitted to main-branch territory flows). At the magnitudes studied, with fixed boundary conditions in this threshold-stratified cohort,
branching (topological) errors changed the decision in 32--33\% and the half-voxel throat error in
30--36\%,
```
OLD 3:
```
Re-derived or tuned boundary conditions reduced topological flips to 5--19\% but did not reduce throat flips. After tuning, a perfusion check stricter than measurement repeatability passed models wrong by more than 0.05 in
19--20\% (discrete) and 5--8\% (leaky) of topological-error cases and 57--81\% of throat-error cases. Other caliber
errors did so in 4--18\% and correct anatomy in 3--4\%. With finer territories, topological concealment fell to
2--7\%; throat concealment changed little.
```
NEW 3:
```
Re-derived or tuned boundary conditions reduced topological flips to 5--19\% but not throat flips. After tuning to noisy perfusion targets, a check stricter than measurement repeatability passed models wrong by more than 0.05 in
21\% (discrete) and 9\% (leaky) of topological-error, 42--49\% of throat-error and 10--14\% of other caliber-error cases, against 4--5\% for correct anatomy; exact per-territory matching raised these to 20--38\%, 78--80\%, 14--27\% and 9--15\%. Finer territories cut topological concealment to 2--7\% but not throat concealment.
```
(The word budget needed the trims in OLD 1–2: "coronary" before revascularization, "can be" → "is", "of models", "with one ... clean" → parenthesis; none changes a claim. "clean" is removed because the parameters are now also fitted to noisy flows. The full 250-word abstract is in `scratchpad/nm/abstract_new.tex`.)

### (b) Main text (OLD verbatim from the current `main.tex`, each matching exactly once)

**III-B, floor paragraph.** OLD:
```
Models with
correct anatomy, tuned to perfusion targets carrying simulated physiological noise (the second floor), passed while materially wrong in 3.1\% (2.4--4.0\%) and 3.9\% (3.2--4.6\%) of draws, and their flip rates were 6.2\% and 7.2\%.
```
NEW:
```
Models with
correct anatomy, tuned to perfusion targets carrying simulated physiological noise (the second floor), passed while materially wrong in 3.1\% (2.4--4.0\%) and 3.9\% (3.2--4.6\%) of draws, and their flip rates were 6.2\% and 7.2\%. With the error models tuned to the same noisy targets, topological passes-and-wrong were 21\% (14--28\%) and 9\% (5--14\%) under Protocol C, against 5\% and 4\% for correct anatomy on the same draws (paired excess 18 and 8 points; 14 and 6 points over Protocol B). Exact matching to noisy targets under Protocol D left 38\% and 20\% of topological-error models wrong, against 15\% and 9\% of correct-anatomy models (paired excess 17 and 7 points; Supplementary Material).
```
**III-B, throat sentence.** OLD:
```
With fixed or re-derived boundary conditions 29\% (discrete) and 42\% (leaky) of half-voxel throat-error models passed while materially wrong, after Protocol C 57\% and 69\%, and after Protocol D 80\% and 81\%, with a median $|\Delta\mathrm{FFR}|$ of 0.11--0.16.
```
NEW:
```
With fixed or re-derived boundary conditions 29\% (discrete) and 42\% (leaky) of half-voxel throat-error models passed while materially wrong, after Protocol C 57\% and 69\%, and after Protocol D 80\% and 81\%, with a median $|\Delta\mathrm{FFR}|$ of 0.11--0.16. With noisy targets more throat models failed the check, and the proportions were 42\% and 49\% (C) and 78\% and 80\% (D); caliber errors away from the throat gave 10--14\% (C) and 14--27\% (D), against 4--5\% and 9--15\% for correct anatomy.
```
**III-C.** OLD:
```
The perfusion residual before tuning separated topological errors from correct anatomy with noisy targets in
the discrete bed only (AUC 0.77 against 0.22), flagging 83\% of them and 48\% of correct models at the 10\% check.
```
NEW:
```
With the same noise on both, the perfusion residual before tuning separated topological errors from correct anatomy in
the discrete bed (AUC 0.83, 0.79--0.88) but barely in the leaky bed (0.57, 0.54--0.60), flagging 86\% and 62\% of them and about half of the correct models at the 10\% check (AUC 0.77 and 0.22 with noise-free error models).
```
**IV-A.** OLD:
```
After one global scaling, 20 of the 39 passing topological-error models were materially wrong in the discrete bed, against 14 of 154 in the leaky bed.
```
NEW:
```
After one global scaling, 20 of the 39 passing topological-error models were materially wrong in the discrete bed, against 14 of 154 in the leaky bed. The contrast held when the error models' targets carried the same noise as the floor (21\% against 5\% discrete, 9\% against 4\% leaky); under per-territory matching the floor itself rose to 15\% and 9\%, so the residual error of topological models (38\% and 20\%) is read against it.
```
OLD:
```
For the throat error, which the check did not see even before tuning, it did so in 57--81\% of models.
```
NEW:
```
For the throat error, which the check did not see even before tuning, it did so in 57--81\% of models (42--80\% with noisy targets).
```
**IV-C.** OLD:
```
Third, record the perfusion mismatch before tuning: it marked topological errors only in the discrete bed (AUC 0.77), and half of the correct models with noisy targets exceeded 10\%.
```
NEW:
```
Third, record the perfusion mismatch before tuning: it marked topological errors only in the discrete bed (AUC 0.83 with the same noise on both), and half of the correct models with noisy targets exceeded 10\%.
```
**Conclusion.** OLD:
```
Up to one in five tuned topological-error models (discrete bed; 5--8\% leaky) and 57--81\% of throat-error models passed a main-branch perfusion check while materially wrong, against 3--4\% for correct anatomy.
```
NEW:
```
With error models and correct anatomy tuned to the same noisy perfusion targets, one in five tuned topological-error models (discrete bed; 9\% leaky) and 42--49\% of throat-error models passed a main-branch perfusion check while materially wrong, against 4--5\% for correct anatomy; exact per-territory matching left 20--38\% of topological-error models wrong against a 9--15\% floor.
```

### (c) Supplement: one table (8 rows) with a two-sentence lead-in, and the offsetting cut

Verified in a scratch compile of the current `supplement.tex`: the change below (new table in, Table S11 and Table S8 out) gives **5 pages** (page 5 at 63 lines); keeping Table S8 gives 6 pages, as does any upstream cut (Table S4 "All" rows, S8 rows), because the float barriers keep pages 1–4 fixed. The main text cites nothing from Table S8 that the new S8 sentence does not carry (0.77 / 0.22, 83% / 48%).

**S8 (replace the paragraph and Table S8).** OLD (matches once):
```
Positives are error models; negatives are the correct-anatomy draws of the simulated floor before tuning
(Table~\ref{tab:detector}). Correct anatomy without noise has a residual below $10^{-8}$; with noise its median is
0.10. With the error models' targets carrying the same noise, the AUC for topological errors was 0.82 (discrete) and
0.56 (leaky).
```
plus the whole `\begin{table}[!ht] \caption{Detection Before and During Tuning ...} ... \end{table}` block that follows it (24 lines). NEW:
```
Positives are error models; negatives are the correct-anatomy draws of the simulated floor before tuning. Correct anatomy without noise has a residual below $10^{-8}$; with noise its median is 0.10, and 48\% (discrete) and 50\% (leaky) of draws exceed the 10\% check. With noise-free targets the pre-tuning residual of topological errors gave an AUC of 0.77 (0.71--0.82, discrete) and 0.22 (0.18--0.27, leaky) and flagged 83\% and 19\% at the 10\% check; with the error models' targets carrying the same noise (Table~\ref{tab:matched}), the AUC was 0.82 (discrete) and 0.56 (leaky).
```
**S9 (replace the end of the paragraph and Table S11).** OLD (matches once):
```
territory flow shares (0.10) and the measured territory flows (0.083), then tunes as in Protocol C
(Table~\ref{tab:floor}).
```
plus the `\begin{table}[!ht] \caption{Simulated Floor ...} ... \end{table}` block (15 lines). NEW (lead-in, two sentences, then the table):
```
territory flow shares (0.10) and the measured territory flows (0.083). Tuned as in Protocol C, correct anatomy flipped in 6.2\% (discrete) and 7.2\% (leaky) of draws (median $|\Delta$FFR$|$ 0.012, 95th percentile 0.05) and passed the check in 72\%.
Table~\ref{tab:matched} tunes every error model to the same noisy targets as the floor and adds the Protocol D floor: rates are means over the 20 draws per instance with patient-level cluster-bootstrap intervals, the excess is the per-draw difference from the correct-anatomy model of the same instance, bed and draw, and $n$ counts models with a defined residual.
\begin{table}[!ht]
\caption{Passes and Wrong, \% of Models, With Error Models and Correct Anatomy Tuned to the Same Noisy Targets (Noise-Free: Table I)}\label{tab:matched}
\centering\footnotesize\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}llrrccrrcc@{}}
\toprule
 & & \multicolumn{4}{c}{Discrete bed} & \multicolumn{4}{c}{Leaky bed}\\
\cmidrule(lr){3-6}\cmidrule(l){7-10}
Error & Protocol & $n$ & Noise-free & Matched & Excess over floor & $n$ & Noise-free & Matched & Excess over floor\\
\midrule
\inputtab supplement_tables/tab_noise_matched.tex 
\bottomrule
\end{tabular}
\end{table}
```
Table body (`results/noise_matched-2026-10-09/tab_noise_matched.tex`, to be copied to `supplement_tables/` at integration; interim numbers):
```
Topological (T1+T2) & C & 104 & 19 & 21 (14--28) & 18 (11--25) & 171 & 8 & 9 (5--14) & 8 (4--12) \\
 & D & 104 & 20 & 38 (28--46) & 17 (10--25) & 171 & 5 & 20 (14--26) & 7 (3--11) \\
\addlinespace[2pt]
Caliber (T3+T4) & C & 194 & 5 & 10 (6--14) & 5 (1--9) & 300 & 12 & 14 (11--18) & 10 (7--13) \\
 & D & 194 & 18 & 27 (21--32) & 12 (7--16) & 300 & 4 & 14 (11--18) & 5 (2--8) \\
\addlinespace[2pt]
Throat ($\pm\tfrac12$ voxel) & C & 192 & 57 & 42 (36--49) & 38 (32--44) & 299 & 69 & 49 (43--55) & 45 (39--51) \\
 & D & 194 & 80 & 78 (72--85) & 63 (56--70) & 300 & 81 & 80 (74--85) & 71 (65--76) \\
\addlinespace[2pt]
Correct anatomy & C & 97 & 0 & 5 (2--8) & -- & 150 & 0 & 4 (2--7) & -- \\
 & D & 97 & 0 & 15 (10--20) & -- & 150 & 0 & 9 (6--13) & -- \\
```
Also drop the `\Needspace{5\baselineskip}` before S10 to `\Needspace{3\baselineskip}` (part of the verified 5-page variant, `scratchpad/tex/supplement_v8.tex`).

## 6. Runtime and files

- Validation: 1 088 s for 252 tasks on 5 workers (4.3 s wall per task) while the T5 demand job ran in parallel; load average 60–185 (the parallel job's BLAS threads oversubscribe the 8 cores). The run was pinned to single-threaded BLAS.
- Full run launched 17:39 (5 workers; 5 187 tasks; the 252 validation tasks reused from the parts cache). Tasks are ordered by draw, so a cut-off at any time covers every instance for the first k draws.
- 17:40–17:49: 2.1 s wall per task (nominal tasks). From 17:50 the rate fell to 10–39 s per task: the workers were at 90–95% CPU but the machine (16 GB) had 15 GB in use, swap 7.0 of 8 GB, 5.5 GB compressed, 25% system time; worker RSS grew to 0.4–1.4 GB (per-scan tree caches), so the time went to page faults. Restarted 18:30 with worker recycling (`maxtasksperchild`); the rate did not recover (550 tasks at 2 905 s). Independently, a noisy-target task costs about 21 worker-seconds (the validation's 252 tasks took 1 088 s on 5 workers) against about 10 for a nominal one, because Protocol C's global scan and Protocol D's least-squares work harder when the targets deviate from the clean flows; thrash-free, the remaining 4 370 tasks would still need about 5 h.
- 19:40: with the 20-draw run projected past midnight, the run was restricted to draws 0–4 with 4 workers recycled every 5 tasks; once the stale workers were killed the rate returned to about 1 s per task. 19:43: the coordinator removed the cut-off (deadline 10-15; machine free), so the run was relaunched over all 20 draws with 6 workers recycled every 5 tasks (5 187 tasks, 881 cached), the draw ordering unchanged.
- 20:33: 6 workers thrashed again (121 tasks in 50 min); 20:50: 4 workers recycled every 2 tasks, still about 38 s per task with each worker above 1 GB within seconds of starting. Cause found at 21:40: `imagecasx_loader._edt` computes the scan's 3D distance transform (about 1 GB, several seconds) and caches only the last two masks per process; the draw-ordered task list visited a different scan on every task, so every task recomputed it, and worker recycling made that worse. The frozen runs, the audit pilot and the validation were instance-grouped. 21:43: relaunched with each instance-bed's 21 tasks consecutive in one worker (`chunksize = 21`, `maxtasksperchild = 84`), 4 workers; workers now stay at 180–300 MB and 99% CPU. A stack sample shows the time in the sparse network solves (SuperLU), i.e. genuine solver work: the noisy-target fits need many more network evaluations than the nominal ones. Measured throughput 176 tasks per hour on 4 workers (about 80 worker-seconds per task).
- 08:10 on 10-10: 2 761 tasks done (108 instance-beds complete), about 200 tasks per hour overnight; projected completion about 20:00 on 10-10. Section 3.3 holds the stability check on this cache.
- 23:00: 1 216 of 5 187 tasks done; draws 0 and 1 complete for all 247 instance-beds, draw 2 for 137, all 21 for 20 instance-beds. `assemble` and the analysis on draws 0–1 produced sections 3–5. The run continues in the background from the same cache; at the measured rate the remaining 3 971 tasks need about 22 h (completion around the evening of 10-10 if the machine stays free; sooner if memory is freed by closing other applications, which is what let the earlier runs go 5–10 times faster). To finish: wait for `run.txt`, or at any time run `noise_matched_run.py assemble` then `noise_matched_analysis.py` (optionally `<rows> <max_draw>` to restrict to draws complete for every instance). The draw-ordered fallback is no longer in force; with the grouped order a partial cache holds complete 21-draw sets for some instance-beds and draws 0–1 for all.
- Code: `code/noise_matched_run.py`, `code/noise_matched_analysis.py` (no project file modified). Outputs: `results/noise_matched-2026-10-09/`. Scratch: `scratchpad/nm/` (logs of every attempt), `scratchpad/tex/` (supplement layout variants v1–v8; v8 is the 5-page one), parts cache `/private/tmp/claude-501/noise_matched_parts/`.
