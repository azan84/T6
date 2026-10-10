# Number check: Paper 6 (Fable, 2026-10-09, final pre-submission)

Scope: every quantitative statement in `main.tex` (abstract, text, Table I, figure captions) and `supplement.tex` with its `supplement_tables/*.tex` fragments, as of 2026-10-09 (post-integration, post sentence-shortening). Every value was recomputed from the result CSVs with my own code (`/private/tmp/claude-501/.../scratchpad/numcheck/recheck1.py` to `recheck4.py`, outputs `recheck*.out`); no project script was called and no project file other than this report was written.

Conventions used (from the paper's own definitions and Table I): rows with status `ok`; discrete arm = the 97 eligible instances of `results/discrete_arm_eligibility.csv`; flip = classification change at 0.80; wrong = |ΔFFR| > 0.05; pass = territory residual < 0.10; passes-and-wrong (P&W) over models with a defined residual; Wilson 95% intervals; exact McNemar paired by model; paired sign test on per-instance class proportions; "beyond the grey zone" = flip with corrupted FFR outside 0.75–0.85; AUC by the Mann–Whitney statistic.

Summary: 203 check rows (172 statement and table rows, 18 cross-location checks, 13 derived claims) covering about 1,470 individual values. 188 rows MATCH in full, 2 rows are ROUNDING (within the stated precision), 9 rows are NOT-RECOMPUTABLE from the CSVs (literature values, Stage-A CFD, figure contents, solver internals; a further 6 rows have one such component), 4 rows are MISMATCH. No headline number, Table I cell, or supplementary table cell is wrong. The four mismatches are wording/denominator statements: (1) "taper" passes-and-wrong at the finer level is the lesion-length-plus-taper class rate; (2) the 23 narrowed-throat bound fits mostly pass, not fail, the check; (3) a caliber mean-|ΔFFR| range excludes Protocol D while the flip-rate range in the same sentence includes it; (4) the |ln C| detector of Table S8 is never defined. Two further basis notes are listed after the mismatches.

## 1. Check table

Abbreviations in Source: `abl` = `results/ablation-2026-10-07.csv`; `per` = `results/ablation-perterritory-2026-10-08.csv`; `elig` = `results/discrete_arm_eligibility.csv`; `t5` = `results/t5_throat-2026-10-09/ablation_t5.csv` + `perterritory_t5.csv`; `t5l2` = `results/t5l2-2026-10-09/*_L2keep.csv`; `a6` = `results/a6_territory-2026-10-09/`; `a5` = `results/a5_overlap-2026-10-09/overlap_metrics.csv`; `a7` = `results/a7_detector-2026-10-09/negatives_pretune.csv`; `neg` = `results/negatives-2026-10-07.csv`; `cfd` = `results/cfd_M1/M1_scan14_0D_vs_3D-2026-10-03.csv`; `d7` = `cfd_handover/returns/2026-10-03/M1_D7_sensitivity_2026-10-06.csv`; `sweep` = `results/sweep_test.csv`; `dem` = `results/ablation-demand{0.7,1.3}-2026-10-07.csv`; `rep` = `results/demand-replication-x{2,3}-2026-10-08/`. "T.I basis" = status ok, eligible discrete, leaky all.

### 1.1 Abstract

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 1 | Abstract "150 stenoses into 108 coronary trees" | 150; 108 | 150 instances; 108 (scan, side) pairs; 93 patients | abl clean rows | MATCH |
| 2 | Abstract "five segmentation errors" | 5 | T1–T4 + T5 | abl, t5 | MATCH |
| 3 | Abstract "changed the decision in 32--33\% of models" | 32–33 | 84/265 = 31.7%; 45/137 = 32.8% | abl A, T.I basis, class level | MATCH |
| 4 | Abstract "half-voxel throat error in 30--36\%" | 30–36 | 58/194 = 29.9%; 108/300 = 36.0% | t5 A, ±½ voxel pooled | MATCH |
| 5 | Abstract "6--10\% for vessel-size (caliber) errors" | 6–10 | 17/300 = 5.7%; 20/194 = 10.3% | abl A, T3+T4 | MATCH |
| 6 | Abstract "reduced topological flips to 5--19\%" | 5–19 | class level B/C: 14, 5, 19, 8 (D: 8, 6) | abl B–D | MATCH (class basis; per error type the range is 5–20%, see note N1) |
| 7 | Abstract "19--20\% (discrete) and 5--8\% (leaky) of topological-error cases" | 19–20; 5–8 | C 20/104 = 19.2, D 21/104 = 20.2; C 14/171 = 8.2, D 9/171 = 5.3 | abl+per, P&W | MATCH |
| 8 | Abstract "57--81\% of throat-error cases" | 57–81 | C 110/193 = 57.0, 205/299 = 68.6; D 156/194 = 80.4, 243/300 = 81.0 | t5 | MATCH |
| 9 | Abstract "Other caliber errors did so in 4--18\%" | 4–18 | C 9/194 = 4.6, D 35/194 = 18.0; C 37/300 = 12.3, D 12/300 = 4.0 | abl+per, T3+T4 | MATCH |
| 10 | Abstract "correct anatomy in 3--4\%" | 3–4 | 60/1940 = 3.1%; 116/2990 = 3.9% | neg, T.I basis | MATCH |
| 11 | Abstract "topological concealment fell to 2--7\%" | 2–7 | L2: C 7/104 = 6.7, D 3/104 = 2.9; C 8/171 = 4.7, D 4/171 = 2.3 | a6 L2keep | MATCH |
| 12 | Abstract "same Dice score (0.97)" | 0.97 | tube-tree DSC median T1 0.975 / T4 0.971 (discrete); 0.969 / 0.972 (leaky) | a5 | MATCH (2 d.p.) |

### 1.2 Methods and figure captions

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 13 | Fig. 1 caption "80\% DS proximal lesion … 20~mm beyond … 25~mm beyond … 2.46~mm … 7\%" | 80; 20; 25; 2.46; 7 | design values; 1 − 0.930 = 7.0% | design | MATCH |
| 14 | II-A "800 CT angiography scans … 160-scan test split … DSC 92.8\% … HD95 2.46~mm" | 800; 160; 92.8; 2.46 | literature (Bransby 2026) | — | NOT-RECOMPUTABLE (cited values) |
| 15 | II-A "image quality was at least adequate … below 40\% DS … $r_\mathrm{fit}$ … at least 1.0~mm … FFR before insertion at least 0.90" | ≥2; <40; ≥1.0; ≥0.90 | sweep: quality min 2; r_fit_c min 1.001; base_ffr_meas min 0.913; disease flag present | sweep | MATCH |
| 16 | II-A "centered 20 or 45~mm … 10 or 20~mm long … 40, 50, 55, 60, 65, 70, 75 or 80\% DS" | as listed | c_mm 19.7–45.5 (prox/mid); L 10, 20; DS {40,50,55,60,65,70,75,80} | sweep | MATCH |
| 17 | II-A "6\,944 eligible instances (280 host vessels, 140 patients)" | 6944; 280; 140 | 6944 rows; 280 (scan, side, vessel); 140 scans | sweep | MATCH |
| 18 | II-A "25 at random (fixed seed, at most two per tree) in each of six 0.05-wide bands … 0.65 to 0.95" | 25 × 6; ≤2/tree | 25 in each of 6 bands; max 2 per tree; all clean FFR in [0.65, 0.95) | abl clean leaky | MATCH |
| 19 | II-A "150 instances (50 each in the LAD, LCx and RCA) lie in 108 trees from 93 patients" | 150; 50/50/50; 108; 93 | 150; LAD 50, LCX 50, RCA 50; 108; 93 | abl | MATCH |
| 20 | II-B "$\mu = 0.004$ … $K_t = 1.52$ … $\rho = 1060$ … 90~mmHg … 5~mmHg … 30\% DS" | model constants | design; draw_mu mean 0.004 in neg | neg | MATCH (constants) |
| 21 | II-B "truncated at $r_\mathrm{ref} = 0.50$~mm … 0.60~mm … $r_\mathrm{ref}^{2.66}$" | 0.50; 0.60; 2.66 | design (3_discrete.log: "truncation r_ref >= 0.60 mm", "leaf r_ref^2.66") | rep logs | MATCH |
| 22 | II-B "$k = 562$ … diameter 3.7~mm … 214~mL/min" | 562; 3.7; 214 | 562 × (1.85 mm)³ = 3.558 mL/s = 213.5 mL/min | arithmetic | MATCH |
| 23 | II-B "median inlet radius 1.60~mm" | 1.60 | r_ref_root median 1.595 mm (150 leaky instances); 1.581 over 108 unique trees | abl clean | MATCH |
| 24 | II-B "median demand was 137~mL/min per tree" | 137 | k·r_in³ median 2.281 mL/s = 136.8 mL/min per instance (133.2 over unique trees) | abl clean | MATCH (instance basis; see note N2) |
| 25 | II-B "97 instances whose healthy-equivalent network gave a main-vessel FFR of at least 0.90 and had at least two outlets" | 97 | 97 eligible of 150; exclusions E3 (FFR < 0.9) 48, E4 (< 2 outlets) 5 | elig | MATCH |
| 26 | II-B "Halving the centerline spacing changed FFR by at most 0.005" | 0.005 | no spacing-halved run in results/ | — | NOT-RECOMPUTABLE |
| 27 | II-C "ends the host vessel 25~mm beyond … 2.46~mm longer … multiplies the radius by 0.930" | 25; 2.46; 0.930 | design; 2λ²/(λ²+1) = 0.928 gives λ = 0.9304 | arithmetic | MATCH |
| 28 | II-C "half the in-plane voxel size of the scan (median 0.35~mm)" | 0.35 | spacing median 0.3516 mm over 93 scans (0.295–0.449) | t5 info_spacing_mm | MATCH |
| 29 | II-C "changed the throat radius by a median of 0.088~mm and DS by 7.3 points (4.5--9.8)" | 0.088; 7.3 (4.5–9.8) | s/4 median 0.0879 mm; |ΔDS| median 7.26, min 4.46, max 9.82 over 298 instance-beds | t5 | MATCH |
| 30 | II-D "a median of two and at most three per tree" (territories) | 2; ≤3 | n_territories median 2, max 3 in both beds | abl clean | MATCH |
| 31 | II-D "excluded (two half-voxel throat-error models, one per bed)" | 2; 1+1 | C failed fits, ½ voxel: discrete narrow 1, leaky narrow 1 (plus 7 + 1 at ±10 points) | t5 status | MATCH |
| 32 | II-D "fitted (within $10^{\pm 3}$)" and "$\pm 1.5$ decades" | design | scale_min/scale_max columns present | per | MATCH (design) |
| 33 | II-D "a median of four territories in the discrete bed and five in the leaky bed" | 4; 5 | positive-target territories at Level 2: median 4 (IQR 3–4) discrete; 5 (4–6) leaky | a6 territory_counts_L2keep | MATCH |
| 34 | II-E "3.5--3.9 million cells … 25~\textmu m … $\pm 4$~mm" | 3.5–3.9; 25; ±4 | control mesh 3.657 M in d7; other meshes not in results/ | d7 | NOT-RECOMPUTABLE (only 3.66 M verifiable) |
| 35 | II-E "scaled residuals below $10^{-5}$" and "50, 25 and 12.5~\textmu m … $5.5\times10^{-4}$" | 1e-5; 5.5e-4 | Stage A values; d7 quotes U3D = 0.00055 | d7 | NOT-RECOMPUTABLE (consistent with d7) |
| 36 | II-F "below 10\% … 95\% bound of 20--29\% … 13\% and 16\% … $|\Delta\mathrm{FFR}| > 0.05$, half the width of the 0.75--0.85 grey zone" | 10; 20–29; 13, 16; 0.05 | 1.96 × 10–15% = 19.6–29.4%; (0.85 − 0.75)/2 = 0.05 | arithmetic | MATCH |
| 37 | II-F "standard deviation of the test--retest difference, 0.018" | 0.018 | literature (Johnson 2015); used as given | — | NOT-RECOMPUTABLE (cited) |
| 38 | Fig. 2 caption "Bands are 0.05 wide … fewer than three models are omitted … standard deviation 0.018" | 0.05; 3; 0.018 | figure content not regenerated | — | NOT-RECOMPUTABLE (figure) |
| 39 | Fig. 3 caption "Protocol D residuals lie below 0.01 in all but two models" | 2 | D residual ≥ 0.01 in exactly 2 of 921 models (0.083, 0.111; both discrete missed-branch) | per | MATCH |
| 40 | Fig. 3 caption "residual $< 0.10$ … $|\Delta\mathrm{FFR}| > 0.05$ … 0.10 threshold … linear below 0.01" | definitions | as used | — | MATCH |
| 41 | Fig. 4 caption "by 0.074 at the measurement point" | 0.074 | 3D resistance: 0.9436 − 0.8698 = +0.0739 | cfd | MATCH |

### 1.3 Table I

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 42 | Table I header "Discrete bed (97 instances)", "Leaky bed (150 instances)" | 97; 150 | 97; 150 | elig, abl | MATCH |
| 43 | Table I, T1 discrete: A 77, 27 (19–38), 13 (7–22); B 77, 9 (4–18), 1 (0–7); C 44, 18 (10–32), 20 (11–35); D 44, 2 (0–12), 23 (13–37) | 24 values | 21/77, 10/77; 7/77, 1/77; 8/44, 9/44; 1/44, 10/44; all CIs identical | abl+per | MATCH |
| 44 | Table I, T1 leaky: A 118, 18 (12–26), 16 (11–24); B 118, 5 (2–11), 5 (2–11); C 71, 8 (4–17), 11 (6–21); D 71, 6 (2–14), 4 (1–12) | 24 values | 21/118, 19/118; 6/118, 6/118; 6/71, 8/71; 4/71, 3/71 | abl+per | MATCH |
| 45 | Table I, T2 discrete: A 60, 40 (29–53), 12 (6–22); B 96, 18 (11–27), 2 (0–9); C 60, 20 (12–32), 18 (11–30); D 60, 12 (6–22), 18 (11–30) | 24 values | 24/60, 7/60; 17/96, P&W 1/60 = 1.7% (0–9); 12/60, 11/60; 7/60, 11/60 | abl+per | MATCH |
| 46 | Table I, T2 leaky: A 147, 43 (35–51), 24 (17–33); B 149, 5 (2–9), 4 (2–10); C 100, 8 (4–15), 6 (3–12); D 100, 6 (3–12), 6 (3–12) | 24 values | 63/147, P&W 24/100; 7/149, 4/100; 8/100, 6/100; 6/100, 6/100 | abl+per | MATCH |
| 47 | Table I, T3 discrete: 97 ×4; flips 7 (4–14) ×4; P&W 0 (0–4) ×4 | 24 values | 7/97 under A–D; 0/97 P&W | abl+per | MATCH |
| 48 | Table I, T3 leaky: 150 ×4; 2 (1–6), 2 (1–6), 3 (1–7), 3 (1–7); 0 (0–2), 0 (0–2), 1 (0–4), 0 (0–2) | 24 values | 3, 3, 4, 4 /150; P&W 0, 0, 1, 0 | abl+per | MATCH |
| 49 | Table I, T4 discrete: 13 (8–22), 6 (3–13); 8 (4–15), 0 (0–4); 8 (4–15), 9 (5–17); 14 (9–23), 36 (27–46) | 24 values | 13, 8, 8, 14 /97; P&W 6, 0, 9, 35 /97 | abl+per | MATCH |
| 50 | Table I, T4 leaky: 9 (6–15), 7 (4–12); 1 (0–4), 0 (0–2); 5 (3–10), 24 (18–31); 5 (2–9), 8 (5–13) | 24 values | 14, 1, 8, 7 /150; P&W 10, 0, 36, 12 /150 | abl+per | MATCH |
| 51 | Table I, T5 "A, B & 194 & 30 (24–37) & 29 (23–36) & 300 & 36 (31–42) & 42 (37–48)" | 8 values | 58/194, 56/194; 108/300, 127/300; A ≡ B exactly (max |FFR_B − FFR_A| = 0 over 988 pairs) | t5 | MATCH |
| 52 | Table I, T5 "C & 193 & 38 (31–45) & 57 (50–64) & 299 & 37 (32–43) & 69 (63–74)" | 8 values | 73/193, 110/193; 112/299, 205/299 | t5 | MATCH |
| 53 | Table I, T5 "D & 194 & 40 (33–47) & 80 (74–85) & 300 & 38 (33–44) & 81 (76–85)" | 8 values | 77/194, 156/194; 114/300, 243/300 | t5 | MATCH |
| 54 | Table I note "reduces $n$ for T2 to 60 under B (discrete bed) and to 100 under A and B (leaky bed)" | 60; 100 | defined-residual rows: 60; 100, 100 | abl | MATCH |
| 55 | Table I note "not applicable to one instance per bed; … 36 discrete and 2 leaky instances" | 1+1; 36; 2 | status "truncation point at segment start": 1 per bed; "no bed left": 36, 2 | abl status | MATCH |
| 56 | Table I note "one Protocol C fit per bed ended at its search bound" | 1+1 | ½-voxel C failures: 1 discrete, 1 leaky | t5 status | MATCH |
| 57 | Table I note "expected flip rate from repeat invasive measurement is 5.0--6.5\% across cells" | 5.0–6.5 | per-cell Φ-floor (SD 0.018): 4.99–6.55% over the 32 T1–T4 cells; 5.1–6.3% over T5 cells | abl, t5 | MATCH |

### 1.4 Results III-A

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 58 | III-A "45 of 137 … (33\%, 95\% CI 26--41\%) … 20 of 194 … (10\%, 7--15\%)" | 45/137; 26–41; 20/194; 7–15 | 45/137 = 32.8 (25.5–41.1); 20/194 = 10.3 (6.8–15.4) | abl A | MATCH |
| 59 | III-A "leaky … 32\% (26--38\%) and 6\% (4--9\%)" | 32 (26–38); 6 (4–9) | 84/265 = 31.7 (26.4–37.5); 17/300 = 5.7 (3.6–8.9) | abl A | MATCH |
| 60 | III-A "paired sign test, $p \leq 0.002$ in both beds" | ≤0.002 | 36/49, p = 0.0014; 63/77, p = 1.4e-8 | abl A | MATCH |
| 61 | III-A "significant in the discrete bed ($p = 0.013$ and 0.002) but not in the leaky bed ($p = 0.18$ and 0.057)" | 0.013; 0.002; 0.18; 0.057 | 0.0127; 0.00235; 0.180; 0.0574 | abl B, C | MATCH |
| 62 | III-A "Under Protocol D … (8\% and 11\% discrete, 6\% and 4\% leaky)" | 8; 11; 6; 4 | 8/104 = 7.7; 21/194 = 10.8; 10/171 = 5.8; 11/300 = 3.7 | per | MATCH |
| 63 | III-A "half-voxel throat error crossed 0.80 in 30\% (24--37\%) and 36\% (31--42\%)" | as stated | 58/194 = 29.9 (23.9–36.6); 108/300 = 36.0 (30.8–41.6) | t5 A | MATCH |
| 64 | III-A "as often as the topological errors on the same instances (paired sign test, $p = 1.0$ and 0.46)" | 1.0; 0.46 | 34/67, p = 1.0; 40/88, p = 0.456 | t5, abl | MATCH |
| 65 | III-A "more often than the other caliber errors ($p < 0.01$ for each sign and bed)" | <0.01 ×4 | narrow 20/20 p = 1.9e-6; wide 31/44 p = 0.0096; narrow 35/35 p = 5.8e-11; wide 70/84 p = 4.1e-10 | t5, abl | MATCH (max 0.0096) |
| 66 | III-A "Every flip followed the sign of the error" | all | narrowed: 65 flips, all to ≤0.80 (max ΔFFR −0.012); widened: 101 flips, all to >0.80 (min ΔFFR +0.0075) | t5 A | MATCH |
| 67 | III-A "about half ended beyond the 0.75--0.85 grey zone" | ≈½ | 28/58 = 48% (discrete); 62/108 = 57% (leaky) | t5 A | MATCH |
| 68 | III-A "tuning left its flip rate at 37--40\%" | 37–40 | C 37.8, D 39.7 (discrete); C 37.5, D 38.0 (leaky) | t5 | MATCH |
| 69 | III-A "maximum mass-conservation error $9\times10^{-9}$" | 9e-9 | max mass_err: 8.84e-9 (frozen A–D), 4.6e-11 (T5); all converged | abl, per, t5 | MATCH |
| 70 | III-A "changed FFR by a mean of 0.006--0.037 in absolute value" | 0.006–0.037 | T3/T4 cell means: A–C 0.0060–0.0366; A–D 0.0060–0.0437 (T4 D discrete 0.0437) | abl+per | MISMATCH (basis, see M3) |
| 71 | III-A "their flip rates of 1--14\% were of the order of the 5.0--6.5\%" | 1–14 | T3/T4 cells A–D: 0.7–14.4% (14 is T4 D discrete) | abl+per | MATCH |
| 72 | III-A "The taper had the highest rates: 13\% and 14\% in the discrete bed under fixed boundary conditions and Protocol D, and 9\% in the leaky bed" | 13; 14; 9 | 13/97 = 13.4; 14/97 = 14.4; 14/150 = 9.3 | abl, per | MATCH |
| 73 | III-A "no caliber-error flip under fixed boundary conditions ended outside the zone, whereas 20\% (discrete) and 23\% (leaky) of topological-error models did" | 0; 20; 23 | beyond-zone caliber A: 0/194, 0/300; topological A: 28/137 = 20.4, 61/265 = 23.0 | abl A | MATCH |
| 74 | III-A "reversed 14--56 topological flips per cell and created none (… Holm-adjusted $p < 0.001$)" | 14–56; 0; <0.001 | B vs A reversed/created: T1 14/0 (Holm 3.7e-4), T1 leaky 15/0 (1.8e-4), T2 leaky 56/0 (8.3e-17) | abl | MATCH |
| 75 | III-A "discrete-bed vessel breaks … (22 reversed, 12 created, $p = 0.24$)" | 22; 12; 0.24 | 22 reversed, 12 created, p = 0.121, Holm 0.243 | abl | MATCH (Holm value) |
| 76 | III-A "only 22\% of re-derived topological-error models in the discrete bed (89\% in the leaky bed) passed" | 22; 89 | B residual < 0.10 on C-defined models: 23/104 = 22.1%; 152/171 = 88.9% | abl | MATCH |

### 1.5 Results III-B

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 77 | III-B "median perfusion residual … from 0.22 under Protocol A to 0.14 (discrete) and from 0.11 to 0.02 (leaky)" | 0.22→0.14; 0.11→0.02 | on the same 104 / 171 models: 0.219→0.140; 0.112→0.020 | abl | MATCH |
| 78 | III-B "significant for leaky vessel breaks, $p < 0.001$" (C vs A) | <0.001 | leaky T2 C–A: 32 reversed, 0 created, Holm p = 9.3e-10 | abl | MATCH |
| 79 | III-B "changed at most two topological-error decisions per cell relative to Protocol B ($p \geq 0.5$)" | ≤2; ≥0.5 | C–B: 2/0, 0/2, 0/0, 2/0; p = 0.5, 0.5, 1, 0.5 | abl | MATCH |
| 80 | III-B "Protocol D matched the territory flows within 1\% in all but two models" | 2 | 2 D models with residual ≥ 0.01 | per | MATCH |
| 81 | III-B "median $|\Delta\mathrm{FFR}|$ of topological-error models fell to 0.005 in both beds, and their flip rate to 8\% (discrete) and 6\% (leaky)" | 0.005; 8; 6 | 0.0050, 0.0051; 8/104 = 7.7; 10/171 = 5.8 | per | MATCH |
| 82 | III-B "missed branch raised FFR by a median of 0.095 (discrete) and 0.047 (leaky)" | 0.095; 0.047 | T1 A on C-defined instances: 0.0948 (n 44); 0.0466 (n 71) | abl | MATCH |
| 83 | III-B "Protocol C reduced the shift to 0.077 and 0.015 (Wilcoxon signed-rank, $p < 0.001$ in both beds)" | 0.077; 0.015; <0.001 | 0.0765; 0.0154; p = 1.6e-11, 2.4e-13 | abl | MATCH |
| 84 | III-B "Protocol D to 0.000 and 0.004, with 10 of 44 and 3 of 71 instances still above 0.05" | 0.000; 0.004; 10/44; 3/71 | 0.0000; 0.0040; 10/44; 3/71 | per | MATCH |
| 85 | III-B "20 of 104 … (19\%, 13--28\%) … 14 of 171 (8\%, 5--13\%)" | as stated | 20/104 = 19.2 (12.8–27.8); 14/171 = 8.2 (4.9–13.3) | abl C | MATCH |
| 86 | III-B "After Protocol D, 21 of 104 (20\%, 14--29\%) and 9 of 171 (5\%, 3--10\%)" | as stated | 21/104 = 20.2 (13.6–28.9); 9/171 = 5.3 (2.8–9.7) | per | MATCH |
| 87 | III-B "On the same instances the proportions were 2\% and 6\% under Protocol B and 13\% and 22\% under Protocol A" | 2; 6; 13; 22 | B 2/104 = 1.9, 10/171 = 5.8; A 13/104 = 12.5, 38/171 = 22.2 | abl | ROUNDING (12.5 → 13, half-up) |
| 88 | III-B "McNemar $p < 0.001$ for C and D … leaky bed ($p \geq 0.12$)" | <0.001; ≥0.12 | C vs B 7.6e-6, D vs B 2.1e-5; leaky 0.125, 1.0 | abl+per | MATCH |
| 89 | III-B "3.1\% (2.4--4.0\%) and 3.9\% (3.2--4.6\%) of draws, and their flip rates were 6.2\% and 7.2\%" | as stated | 60/1940 = 3.09 (2.41–3.96); 116/2990 = 3.88 (3.24–4.63); flips 120/1940 = 6.19, 215/2990 = 7.19 | neg, T.I basis | MATCH |
| 90 | III-B "With re-derived boundary conditions no lesion-length or taper model passed while materially wrong" | 0 | B caliber P&W 0/194, 0/300 | abl B | MATCH |
| 91 | III-B "5\% (C) and 18\% (D) … discrete bed and 12\% and 4\% in the leaky bed (McNemar against B, $p \leq 0.004$)" | 5; 18; 12; 4; ≤0.004 | 9/194 = 4.6, 35/194 = 18.0, 37/300 = 12.3, 12/300 = 4.0; p = 0.0039, 5.8e-11, 1.5e-11, 4.9e-4 | abl+per | MATCH |
| 92 | III-B "29\% (discrete) and 42\% (leaky) … after Protocol C 57\% and 69\%, and after Protocol D 80\% and 81\%" | as stated | 28.9, 42.3; 57.0, 68.6; 80.4, 81.0 | t5 | MATCH |
| 93 | III-B "median $|\Delta\mathrm{FFR}|$ of 0.11--0.16" (throat, A–D) | 0.11–0.16 | A 0.1125, 0.1053; C 0.1414, 0.1280; D 0.1624, 0.1222 | t5 | MATCH |
| 94 | III-B "topological passes-and-wrong fell to 7\% (C) and 3\% (D) in the discrete bed and to 5\% and 2\% in the leaky bed" | 7; 3; 5; 2 | L2: 7/104 = 6.7, 3/104 = 2.9; 8/171 = 4.7, 4/171 = 2.3 | a6 L2keep | MATCH |
| 95 | III-B "Taper passes-and-wrong rose under Protocol D to 23\% and 9\%" | 23; 9 | T3+T4 class at L2: 45/194 = 23.2, 28/300 = 9.3; taper alone: 44/97 = 45.4, 28/150 = 18.7 | a6 L2keep | MISMATCH (label, see M1) |
| 96 | III-B "throat passes-and-wrong fell by at most 9 points, to 51--60\% (C) and 78--81\% (D), and flip rates were unchanged" | 9; 51–60; 78–81; unchanged | ½-voxel falls 3.6, 5.7, 2.6, 7.0, 8.4, 0.0 points (max 69→60); C 51.3, 60.2; D 77.8, 81.0; flips changed by ≤2 models per cell | t5l2 | MATCH (flips: ROUNDING, ≤2 models) |

### 1.6 Results III-C, III-D and Discussion/Conclusion

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 97 | III-C "same median DSC (0.97) … twice as often (27\% against 13\% discrete, 18\% against 9\% leaky)" | 0.97; 27/13; 18/9 | 0.975 / 0.971 and 0.969 / 0.972; flips 27.3 / 13.4; 17.8 / 9.3 | a5, abl A | MATCH |
| 98 | III-C "A vessel break lowered the DSC to 0.89, and to 0.62 in the right coronary artery; clDice fell only for topological errors" | 0.89; 0.62 | T2 tree DSC median 0.893 / 0.895; RCA 0.629 / 0.623; clDice T3, T4 = 1.000 (min 1.000), T1 0.94/0.93, T2 0.85 | a5 | MATCH |
| 99 | III-C "91\% (discrete) and 62\% (leaky) kept a whole-scan DSC at or above … 0.928" | 91; 62 | 41/45 = 91.1; 52/84 = 61.9 | a5 + abl A | MATCH |
| 100 | III-C "AUC of the DSC for a decision change was 0.54 and 0.70" | 0.54; 0.70 | topological, −tree DSC vs flip A: 0.541; 0.702 | a5 | MATCH |
| 101 | III-C "discrete bed only (AUC 0.77 against 0.22), flagging 83\% of them and 48\% of correct models" | 0.77; 0.22; 83; 48 | 0.767; 0.221; 114/137 = 83.2; 922/1940 = 47.5 | a7 + abl B | MATCH |
| 102 | III-D "from 0.870 to 0.944 ($\Delta$FFR $= +0.074$)" | 0.870; 0.944; +0.074 | 0.8698; 0.9436; +0.0739 | cfd | MATCH |
| 103 | III-D "changed FFR by $-0.0007$ … (0.892 in both). It was $+0.022$ against the clean tree with its resistances (0.870)" | −0.0007; 0.892; +0.022; 0.870 | 0.8923 → 0.8916 = −0.0007; 0.8916 − 0.8698 = +0.0218 | cfd | MATCH |
| 104 | III-D "reduced-order counterparts on the meshed radius gave $+0.081$ and $-0.0005$" | +0.081; −0.0005 | 0D_asmeshed_area: 0.8595→0.9402 = +0.0807; 0.8823→0.8818 = −0.0005 | cfd | MATCH |
| 105 | III-D "cohort model of this instance the error gave $+0.127$ (A), $+0.107$ (C, failing the check) and $-0.0007$ (D)" | +0.127; +0.107; −0.0007 | scan 14 LAD prox 20 mm 80% discrete: A +0.1274, C +0.1069 (residual 0.300), D −0.0007 | abl, per | MATCH |
| 106 | III-D "throat 0.276 against 0.231~mm; baseline 0.761" | 0.276; 0.231; 0.761 | 0.2756; 0.2306; 0.7612 | cfd | MATCH |
| 107 | III-D "finer throat zone changed the baseline FFR by at most 0.0021" | 0.0021 | +0.0019, +0.0021 | d7 | MATCH |
| 108 | III-D "flip-rate directions held in both beds at twice and in the leaky bed at three times the demand … not significant in any topological comparison at twice the demand" | directions; n.s. | ×2: topo > cal A (50 > 1; 34 > 5), B, C < A in both beds; ×3 leaky 33 > 5; ×2 topo C/D vs B p = 0.25, 0.07, 0.125, 1.0 | rep | MATCH |
| 109 | IV-A "each changed about a third of decisions" | ≈⅓ | 33, 32; 30, 36 | abl, t5 | MATCH |
| 110 | IV-A "reduced topological flips from 18--43\% to 2--20\% per error type" | 18–43; 2–20 | A: 27, 40, 18, 43; B–D: 9, 18, 5, 5, 18, 20, 8, 6, 2, 12, 6, 6 | abl+per | MATCH |
| 111 | IV-A "one in five … 20 of the 39 passing topological-error models … against 14 of 154" | 20/39; 14/154 | C discrete: 39 pass, 20 wrong; leaky: 154 pass, 14 wrong | abl C | MATCH |
| 112 | IV-A "57--81\% of models" (throat) | 57–81 | as #8 | t5 | MATCH |
| 113 | IV-B "13--15.5\%" (Gamage), IV-A "[sankaran…]" | literature | — | — | NOT-RECOMPUTABLE (cited) |
| 114 | IV-C "the taper up to 14\% … flipped 30--36\% … (AUC 0.77), and half of the correct models … exceeded 10\%" | 14; 30–36; 0.77; ½ | 14.4; 29.9–36.0; 0.767; 47.5% / 50.4% | abl, t5, a7 | MATCH |
| 115 | IV-D "half a voxel and $\pm 10$ points of DS … (0.045~mm at the throat) … (0.761 against 0.870) … ($+0.127$ against $+0.081$)" | 0.045; 0.761; 0.870; +0.127; +0.081 | 0.2756 − 0.2306 = 0.0451; as #102–106 | cfd, abl | MATCH |
| 116 | Conclusion "150 inserted stenoses in 108 trees … about a third … 5--18\% … 57--81\% … 3--4\%" | 150; 108; ⅓; 5–18; 57–81; 3–4 | B per type: 9, 18, 5, 5 → 5–18; others as above | abl, t5, neg | MATCH |

### 1.7 Supplement text and tables

| # | Location, snippet | Stated | Recomputed | Source | Verdict |
|---|---|---|---|---|---|
| 117 | S1 "image quality of at least 2 (0--4 scale) … at least 1.0~mm … below 40\% DS … 20~mm beyond … radius at least 0.75~mm … at least 0.90" | 2; 1.0; 40; 20; 0.75; 0.90 | quality min 2; r_fit min 1.001; base FFR min 0.913; measurement-point radius not in sweep | sweep | MATCH (0.75 mm NOT-RECOMPUTABLE) |
| 118 | S1 "shuffled the 6\,944 instances with a fixed seed (20260918) … six baseline-FFR bands … at most two instances per tree … relaxation 0.5 … $10^{-8}$ … exponent 2.66 is close to 8/3" | 6944; 20260918; 6; 2; 0.5; 1e-8; 2.66 | 6944; seed in rep logs; 6 bands; max 2; 8/3 = 2.667 | sweep, logs | MATCH |
| 119 | Fig. S1 boxes "160 CT angiography scans … 6\,944 instances … 25 per 0.05 band … 150 … Leaky (150) and discrete (97) … $k \times 0.7$, $\times 1.3$ … $\times 2$, $\times 3$ … $+2.46$~mm … $\times 0.930$ … 3.5--3.9~M cells" | as listed | consistent with #17–19, #25, #34 | — | MATCH (3.5–3.9 M as #34) |
| 120 | S2 "two half-voxel throat-error models; 10 of 4\,940 noise-floor draws" | 2; 10/4940 | 1 + 1; 10 failed fits (all leaky) of 1940 + 3000 = 4940 | t5, neg | MATCH |
| 121 | S2 "two missed-branch models, residual 0.08 and 0.11" | 2; 0.08; 0.11 | 0.083, 0.111, both discrete T1 (|ΔFFR| 0.041, 0.026) | per | MATCH |
| 122 | S2 "23 throat-error models with a narrowed throat, most failing the check" | 23; most fail | ½-voxel narrow D bound fits: 20 + 3 = 23; 9 fail, 14 pass (all 14 materially wrong) | t5 | MISMATCH (see M2) |
| 123 | S2 "(36 discrete, 2 leaky); scored as flips (FFR 1), these raise the discrete-bed vessel-break flip rate from 40\% to 43\%" | 36; 2; 40→43 | 36, 2; 17 of the 36 have clean FFR ≤ 0.80: (24 + 17)/96 = 42.7%; leaky (63 + 1)/149 = 43.0% (unchanged) | abl | MATCH |
| 124 | Table S1 (12 rows): 77 of 97 / 20; 44 / 33; 96 of 97 / 1; 60 / 36; 60 / 36; 193 / 1; 118 of 150 / 32; 71 / 47; 149 of 150 / 1; 147 / 2; 100 / 49; 299 / 1 | 24 values | status counts identical in every cell | abl, per, t5 | MATCH |
| 125 | Table S2 GLMM, 14 terms × 2 beds (posterior mean and ±1.96 SD interval) | 84 values | transcription against `P1_glmm_vb_{discrete,leaky}.csv`: all 84 agree at 2 d.p. (3 d.p. for severity); interval = mean ± 1.96 SD verified | analysis-ablation-2026-10-07 | MATCH (transcription; model fit itself NOT-RECOMPUTABLE) |
| 126 | Table S3 thresholds, 16 rows × (n, 10%, 13%, 16%, Pass, Wrong among passing) | 96 values | all identical, e.g. discrete T1+T2 A: 137, 12 (8–19), 23 (17–31), 31 (24–40), 21, 81 (60–92); leaky All D: 471, 4 (3–7) ×3, 471, 4 (3–7) | abl+per | MATCH |
| 127 | Table S3 note "T2 under Protocols A and B in the leaky bed, $n = 100$; T2 under Protocol B in the discrete bed, $n = 60$" | 100; 60 | as #54 | abl | MATCH |
| 128 | S4.2 "214~mL/min … ($228 \pm 71$ to $293 \pm 102$~mL/min) … 2.28~mL/s (137~mL/min)" | 214; 228±71; 293±102; 2.28; 137 | 213.5; literature; 2.281 mL/s = 136.8 | arithmetic, abl | MATCH (thermodilution values NOT-RECOMPUTABLE) |
| 129 | tab_demand text "leaky-bed median 0.869, 0.801 and 0.741 … fell to 3\% (leaky bed, 0.7 times) and stayed at 12--25\% (discrete bed)" | 0.869; 0.801; 0.741; 3; 12–25 | 0.869, 0.801, 0.741; 5/171 = 2.9; 12/104 = 11.5, 20/104 = 19.2, 26/104 = 25.0 | dem, abl | MATCH |
| 130 | Table S4 discrete 0.7: 32 (25–40), 6 (3–10), 12 (8–18), 18 (12–27), 12 (7–19), 0.070 / 0.057 | 12 values | 44/137, 11/194, 21/173, 19/104, 12/104, 0.0704 / 0.0566 | dem 0.7 | MATCH |
| 131 | Table S4 discrete 1.0 and 1.3: 33 (26–41), 10 (7–15), 14 (10–20), 19 (13–28), 19 (13–28), 0.095 / 0.077; 40 (32–48), 5 (2–9), 16 (11–22), 19 (13–28), 25 (18–34), 0.106 / 0.091 | 24 values | identical (1.3: 55/137, 9/194, 27/173, 20/104, 26/104, 0.106 / 0.091) | abl, dem 1.3 | MATCH |
| 132 | Table S4 leaky 0.7, 1.0, 1.3: 20 (16–26), 6 (4–9), 7 (4–10), 9 (5–14), 3 (1–7), 0.032 / 0.010; 32 (26–38), 6 (4–9), 5 (3–8), 8 (5–13), 8 (5–13), 0.047 / 0.015; 37 (32–43), 4 (2–7), 5 (3–9), 8 (4–13), 12 (8–18), 0.057 / 0.021 | 36 values | identical | dem, abl | MATCH |
| 133 | S4.3 "only 17 instances met the discrete-bed criteria … significant in three of four caliber comparisons and in no topological one" | 17; 3 of 4; 0 | ×3 eligible 17; ×2 caliber C/D vs B: p = 1 (discrete C), 2.4e-4, 1.8e-12, 1.2e-4; topological p = 0.25, 0.07, 0.125, 1 | rep | MATCH |
| 134 | Table S5 discrete 1: 97; 33 (26–41), 10 (7–15), 19 (13–28), 8 (4–14), 1 (0–5), 19 (13–28), 20 (14–29), 0 (0–2), 5 (2–9), 18 (13–24) | 11 values | identical (B topological P&W 2/137) | abl+per | MATCH |
| 135 | Table S5 discrete 2: 47; 50 (38–62), 1 (0–6), 20 (11–32), 8 (3–18), 6 (2–15), 14 (7–26), 20 (11–32), 0 (0–4), 1 (0–6), 14 (8–22) | 11 values | 47; 33/66, 1/94, 10/51, 4/51, 4/64, 7/51, 10/51, 0/94, 1/94, 13/94 | rep ×2 | MATCH |
| 136 | Table S5 leaky 1, 2, 3 (three rows × 11) | 33 values | identical (e.g. ×3: 150; 87/262 = 33 (28–39), 16/300, 12/190, 12/190, 10/225, 14/190, 8/190, 1/300, 36/300, 8/300) | abl, rep | MATCH |
| 137 | S4.4 "30\% (discrete) and 33\% (leaky) of clean models lie within" | 30; 33 | 29/97 = 29.9; 50/150 = 33.3 | abl clean | MATCH |
| 138 | Table S6 grey zone, 8 rows × 6 cells (n, flip, beyond; n, flip, beyond) | 48 values | identical, e.g. discrete A: 137, 33 (26–41), 20 (15–28), 194, 10 (7–15), 0 (0–2); leaky D: 171, 6 (3–10), 0 (0–2), 300, 4 (2–6), 0 (0–1) | abl+per | MATCH |
| 139 | S5 "spacing median 0.352~mm; throat radius $\pm 0.088$~mm; 7.3 points of DS, 4.5--9.8" | as stated | 0.3516; 0.0879; 7.26 (4.46–9.82) | t5 | MATCH |
| 140 | S5 "standard deviation 12.3--12.4 points" | 12.3–12.4 | literature (Boogers 2010) | — | NOT-RECOMPUTABLE (cited; verified in FABLE-VERIFY §4) |
| 141 | S5 "Protocol C fits at the search bound were excluded (2 at half a voxel, 8 at $\pm 10$ points)" | 2; 8 | narrow 1 + 1; DS+10 7 + 1 | t5 status | MATCH |
| 142 | S5 "The 64 Protocol D fits at the parameter bound, all with an increased stenosis, were retained; excluding them would raise passes-and-wrong by up to 13 points" | 64; all; 13 | 64 of 988 (discrete 54, leaky 10; narrow 23, DS+10 41); all narrow/DS+10; excl.: 80→83, 75→88 (+13), 81→81, 86→87 | t5 | MATCH |
| 143 | Table S7 throat, discrete ½ voxel rows (−½: 97/28 (20–37)/26 (18–35)/16 (10–25); 96/30/49/23; 97/30/84/25; +½: 32/32/12; 45/65/21; 49/77/28) | 36 values | identical (e.g. −½ A: 27/97, 25/97, 16/97; +½ D: 48/97, 75/97, 27/97) | t5 | MATCH |
| 144 | Table S7 throat, leaky ½ voxel rows (−½: 25/43/15; 26/68/21; 27/91/19; +½: 47/41/26; 49/69/38; 49/71/39, with n and CIs) | 36 values | identical (e.g. −½ D: 41/150, 136/150, 29/150) | t5 | MATCH |
| 145 | Table S7 pooled ½-voxel rows (both beds, A–D) | 24 values | identical to Table I plus beyond-zone 14 (10–20), 22 (17–28), 26 (21–33); 21 (16–26), 29 (25–35), 29 (24–34) | t5 | MATCH |
| 146 | Table S7 "DS $\pm10$ pooled" rows: 194/40 (33–47)/20 (15–26)/27 (22–34); 187/44/51/37; 194/45/75/40; 300/42/40/35; 299/43/62/41; 300/44/86/40 | 24 values | identical (e.g. discrete C: 83/187, 95/187, 69/187) | t5 | MATCH |
| 147 | Table S7 note "topological errors under Protocol A flipped 33\% (26--41\%) and 32\% (26--38\%) … caliber errors away from the throat 10\% (7--15\%) and 6\% (4--9\%)" | as stated | as #58–59 | abl | MATCH |
| 148 | S6 "median four territories, discrete; five, leaky … would have risen to 26\%" | 4; 5; 26 | 4; 5; L2drop discrete topological C and D: 27/102 = 26.5% | a6 | MATCH |
| 149 | S6 "reproduced the original results exactly" (main-branch partition) | exact | L1drop vs frozen: 3368 common rows, max |ΔFFR| = 0, max |Δresidual| = 0, 0 flip differences | a6 L1drop | MATCH |
| 150 | S6 "Throat-error models removed from the count all failed the finer check; none had its FFR corrected, and 76--88\% of tuned throat-error models that passed remained materially wrong" | all; none; 76–88 | every lost P&W model fails at L2 and stays wrong (e.g. 12/12, 26/26); wrong-among-passing at L2, C and D: 76, 84, 81, 88, 76, 82, 81, 87 | t5l2 | MATCH |
| 151 | S6 "Flip rates changed by at most five models per cell" | ≤5 | net change per cell: T1–T4 at most +5 (leaky topological D, 10→15; but 9 created and 4 reversed; discrete topological D: 10 created, 7 reversed, net +3); T5 cells ≤2 | a6, t5l2 | MATCH as net count (see note N3) |
| 152 | Table S8-gran discrete rows: T1+T2 C 104, 19 (13–28), 7 (3–13), <0.001; D 20 (14–29), 3 (1–8), <0.001; T3+T4 C 194, 5 (2–9), 5 (3–9), 1.0; D 18 (13–24), 23 (18–30), 0.002; T5 A,B 194, 29, 25, 0.016; C 193, 57, 51, 0.003; D 194, 80, 78, 0.12 | 35 values | p = 2.4e-4, 7.6e-6, 1.0, 0.00195, 0.0156, 0.0034, 0.125; rates identical | a6, t5l2 | MATCH |
| 153 | Table S8-gran leaky rows: T1+T2 C 171, 8, 5, 0.07; D 5, 2, 0.18; T3+T4 C 300, 12, 12, 1.0; D 4, 9, <0.001; T5 A,B 300, 42, 35, <0.001; C 299, 69, 60, <0.001; D 300, 81, 81, 1.0 | 35 values | p = 0.0703, 0.180, 1.0, 1.4e-4, 1.9e-5, 4.2e-7, 1.0; rates identical | a6, t5l2 | MATCH |
| 154 | S7 "no error changed the number of connected components" | 0 | no component count in a5 CSV; true by construction (T1 removes a subtree, T2 a distal run, T3–T5 change radius only) | — | NOT-RECOMPUTABLE |
| 155 | S7 "91\% (79--96\%, discrete) and 62\% (51--72\%, leaky)" | as stated | 41/45 = 91.1 (79.3–96.5); 52/84 = 61.9 (51.2–71.5) | a5 + abl | MATCH |
| 156 | S7 "AUC … 0.65 (discrete) and 0.79 (leaky) across error types and 0.54 and 0.70 within topological errors" | 0.65; 0.79; 0.54; 0.70 | 0.648; 0.789; 0.541; 0.702 | a5 + abl | MATCH |
| 157 | S7 "(median 40\% of its volume)" (taper) | 40 | t4_scaled_vol_share median: 43% discrete, 40% leaky | a5 | ROUNDING (bed not stated; see note N4) |
| 158 | Table S9 overlap, discrete T1: 77, 0.975 (0.947–0.984), 0.985 (0.977–0.991), 0.940 (0.903–0.963), 27 (14–43), 27 (19–38) | 16 values | identical (flow lost 27.4 (14.2–43.2)) | a5 | MATCH |
| 159 | Table S9 discrete T2–T4, leaky T1–T4 (7 rows × 6 cells) | 112 values | identical, e.g. T2 discrete 96, 0.893 (0.701–0.937), 0.935 (0.888–0.960), 0.847 (0.544–0.907), 30 (15–100), 40 (29–53); leaky T4 150, 0.972 (0.951–0.981), 0.983 (0.976–0.988), 1.000, 0, 9 (6–15) | a5, abl A | MATCH |
| 160 | Table S9 "T2, right coronary artery: 0.62--0.63, 0.85--0.86, 0.45--0.49" and note "$n = 60$" | 6 values; 60 | RCA T2 tree 0.629 / 0.623; scan 0.854 / 0.862; clDice 0.493 / 0.452; flip A n = 60 | a5 | MATCH |
| 161 | S8 "residual below $10^{-8}$; with noise its median is 0.10" | <1e-8; 0.10 | noise-free clean residual 0.0 in abl; A7 summary max 3.8e-9; noisy medians 0.097, 0.101 | abl, a7 | MATCH |
| 162 | S8 "AUC for topological errors was 0.82 (discrete) and 0.56 (leaky)" (noisy targets) | 0.82; 0.56 | noisy-target positives not stored; `detector_metrics.csv` rows 4, 15: 0.8235, 0.5621 | a7 metrics | NOT-RECOMPUTABLE (cross-checked only) |
| 163 | Table S10 discrete "Pre-tuning residual, Topological, 137, 0.77 (0.71–0.82), 83 (76–89), 48, 0.22, 47 (39–55)" | 9 values | AUC 0.767; 114/137 = 83.2 (76.1–88.5); 922/1940 = 47.5; 0.220; 64/137 = 46.7 (38.6–55.1); AUC CI from a7 bootstrap 0.712–0.820 | a7 + abl B | MATCH |
| 164 | Table S10 discrete "Flip under B, 36, 0.57 (0.46–0.69), 69 (53–82), 48, 0.22, 22 (12–38)" | 9 values | 0.571; 25/36 = 69.4; 8/36 = 22.2 | a7 + abl B | MATCH |
| 165 | Table S10 discrete "$|\ln C|$, Topological, 104, 0.47 (0.40–0.53), 30 (22–39), 37, 0.24, 9 (5–16); Flip or P\&W under C, 61, 0.53 (0.44–0.62), 41 (30–54), 37, 0.24, 15 (8–26)" | 18 values | with C = Protocol C scaling relative to the re-derived $C_\mathrm{b}$ (|ln(C_C/C_B)|): 0.466, 30%, 37%, 0.235, 9%; 0.532, 41%, 15% | a7, abl B/C | MATCH (definition absent from text, see M4) |
| 166 | Table S10 leaky rows: 218, 0.22 (0.18–0.27), 19 (15–25), 50, 0.23, 6 (3–9); 16, 0.21 (0.08–0.36), 12 (3–36), 6 (1–28); 171, 0.12 (0.09–0.15), 3 (1–7), 34, 0.24, 2 (1–5); 66, 0.66 (0.55–0.77), 61 (49–71), 59 (47–70) | 32 values | 0.221, 42/218 = 19.3, 1511/3000 = 50.4, 0.229, 12/218 = 5.5; 0.207, 2/16, 1/16; 0.118, 10/171 (vs clean) → 5/171 = 2.9 with |ln(C_C/C_B)|, 1009/2990 = 33.7, 0.237, 3/171; 0.661, 40/66, 39/66 | a7, abl | MATCH |
| 167 | Table S10 note "1\,940 (discrete) and 3\,000 (leaky; 2\,990 for $|\ln C|$) … on 97 and 150 instances" | 1940; 3000; 2990; 97; 150 | 1940 draws / 97 instances; 3000 / 150; 2990 ok fits | a7 | MATCH |
| 168 | S9 "$1.96 \times (10\text{--}15\%) \approx 20$--29\% … 0.018 (5.0--6.5\% across cells) … 20 draws per instance … 0.05 … 0.056 … 0.02 … 0.10 … 0.083" | as listed | 19.6–29.4; floor 4.99–6.55; 20 draws; realised SDs 0.0497, 0.0554, 0.0202, 0.10, 0.083 | neg | MATCH |
| 169 | Table S11 floor: Discrete 97, 1940, 6.2 (5.2–7.3), 0.012, 0.050, 72, 3.1 (2.4–4.0); Leaky 150, 2990, 7.2 (6.3–8.2), 0.012, 0.053, 72, 3.9 (3.2–4.6) | 16 values | 97, 1940, 120/1940 = 6.19 (5.20–7.35), 0.0122, 0.0498, 72.3, 3.09 (2.41–3.96); 150, 2990, 215/2990 = 7.19 (6.32–8.17), 0.0118, 0.0535, 72.3, 3.88 (3.24–4.63) | neg | MATCH |
| 170 | S10 "3.5--3.9 million cells … 25~\textmu m … $\pm 4$~mm … four boundary layers … 3\,000 iterations … $10^{-5}$" | as listed | iterations 3000 in d7; rest Stage A / mesh settings | d7 | MATCH (3000) / NOT-RECOMPUTABLE (others) |
| 171 | S10 "raised the baseline FFR by 0.0019--0.0021, above … $5.5\times10^{-4}$, so the patient-case uncertainty is about 0.002, against an error effect of 0.074 … velocity residual $1.08\times10^{-5}$" | 0.0019–0.0021; 5.5e-4; 0.002; 0.074; 1.08e-5 | +0.00189, +0.00207; U3D 0.00055 quoted in d7; 0.0739; residual value not in d7 | d7, cfd | MATCH (1.08e-5 NOT-RECOMPUTABLE) |
| 172 | Table S12 D7: "3.66, 0.8698, +0.0000, 0.00, 1.43; 6.24, 0.8716, +0.0019, 0.24, 0.70; 8.31, 0.8718, +0.0021, 0.25, 0.70" and caption "8.31~M-cell mesh did not meet the strict residual limit at 3\,000 iterations" | 15 values | 3.657 M, 0.86976, 0, 0.000, 1.430; 6.241 M, 0.87165, +0.00189, 0.241, 0.698; 8.309 M, 0.87183, +0.00207, 0.253, 0.698; A2 UNCONVERGED at 3000 | d7 | MATCH |

### 1.8 Consistency of the same quantity across locations

| # | Quantity | Locations and values | Verdict |
|---|---|---|---|
| 173 | Topological flips under A | abstract 32–33; III-A 33 / 32; Table S7 note 33 (26–41) / 32 (26–38); IV-A "about a third"; Conclusion "about a third" | MATCH |
| 174 | Throat flips under A | abstract 30–36; III-A 30 / 36; Table I 30 / 36; IV-C 30–36; S8-gran 194 / 300 | MATCH |
| 175 | Caliber flips under A | abstract 6–10; III-A 10 / 6; Table S7 note 10 (7–15) / 6 (4–9) | MATCH |
| 176 | Topological flips after re-derivation/tuning | abstract 5–19 (class level B/C); IV-A 2–20 (per type, B–D); Conclusion 5–18 (per type, B) | MATCH on each stated basis (note N1) |
| 177 | Tuned topological P&W | abstract 19–20 / 5–8; III-B 19, 20 / 8, 5; Table S3 19, 20 / 8, 5; S8-gran 19, 20 / 8, 5; IV-A "one in five"; Conclusion "up to one in five (5–8% leaky)" | MATCH |
| 178 | Throat P&W tuned | abstract 57–81; III-B 57, 69, 80, 81; Table I; Table S7; IV-A 57–81; Conclusion 57–81 | MATCH |
| 179 | Caliber P&W tuned | abstract 4–18; III-B 5, 18 / 12, 4; Table S3 (class, 5 / 18, 12 / 4); S8-gran main-branch 5, 18 / 12, 4 | MATCH |
| 180 | Correct anatomy floor | abstract 3–4; III-B 3.1 / 3.9; III-B "3--4\% of correct anatomy"; Conclusion 3–4; Table S11 | MATCH |
| 181 | Level-2 topological P&W | abstract 2–7; III-B 7, 3 / 5, 2; S8-gran 7, 3 / 5, 2 | MATCH |
| 182 | Throat magnitude | II-C 0.35 mm / 0.088 mm / 7.3 (4.5–9.8); S5 0.352 / 0.088 / 7.3 (4.5–9.8); Fig. S1 "±½ voxel" | MATCH |
| 183 | Protocol C bound-fit exclusions | II-D "two … one per bed"; Table I note "one per bed"; S2 "two half-voxel"; S5 "2 at half a voxel, 8 at ±10"; Table S1 "193 / 1", "299 / 1" | MATCH |
| 184 | Protocol D bound fits | S2 "two missed-branch … 23 throat-error models with a narrowed throat"; S5 "The 64 Protocol D fits"; S6 "Protocol D fits on the parameter bound" (counts not restated) | MATCH numerically (23 = ½-voxel subset of 64; wording clarified in M2) |
| 185 | Territories | II-D "median of two and at most three"; II-D "median of four … five"; S6 "median four … five"; Table S8-gran note "two or three … four … five" | MATCH |
| 186 | 3D case values | III-D, Fig. 4, IV-D, S10, Fig. S1: 0.870, 0.944, 0.074, 0.892, −0.0007, +0.022, +0.081, −0.0005, +0.127, 0.276, 0.231, 0.045, 0.761, 0.0021 | MATCH |
| 187 | Repeat-FFR floor | II-F 0.018; Table I note 5.0–6.5; III-A 5.0–6.5; Fig. 2 caption 0.018; S9 0.018, 5.0–6.5 | MATCH |
| 188 | Detector | III-C 0.77 / 0.22 / 83% / 48%; IV-C 0.77, "half … exceeded 10%"; Table S10 0.77, 0.22, 83, 48, 50 | MATCH |
| 189 | DSC statements | abstract 0.97; III-C 0.97, 0.89, 0.62, 91%, 62%, 0.54, 0.70; IV-B "as high as a taper", "only in the RCA"; S7 and Table S9 | MATCH |
| 190 | Demand | II-B 137 mL/min, 214; S4.2 2.28 mL/s (137), 214; III-D (demand paragraph) vs S4.3 | MATCH |

### 1.9 Derived claims (task item 4)

| # | Claim | Check | Verdict |
|---|---|---|---|
| 191 | "Protocols A and B coincide for T5 by construction" (Table I note, II-C, S5, Table S8-gran note) | 988 A/B pairs: max |FFR_B − FFR_A| = 0.0; every B row has C_ratio = 1.0 exactly; same at Level 2 | MATCH |
| 192 | "none over the floor" is not asserted anywhere in the current text; the nearest statements are "rates of the order of / near repeat invasive measurement" for caliber errors (III-A, IV-A, IV-C) | caliber flips 0.7–14.4% against a per-cell floor of 5.0–6.5%; four T3/T4 cells exceed 6.5% (T4 A discrete 13.4, T4 D discrete 14.4, T4 B discrete 8.2, T4 C discrete 8.2, T3 discrete 7.2 ×4, T4 A leaky 9.3) | MATCH as worded ("of the order of"; no "none over the floor" claim) |
| 193 | "rose in neither bed": III-B "Tuning raised these proportions relative to B in the discrete bed … but not in the leaky bed" | leaky C vs B +4/−0 (p = 0.125), D vs B +3/−4 (p = 1.0) | MATCH |
| 194 | "no error changed connected components" (S7) | not in CSV; by construction | NOT-RECOMPUTABLE |
| 195 | "every flip followed the sign" (III-A) | 65 narrowed-throat flips all downward, 101 widened all upward; ΔFFR sign uniform | MATCH |
| 196 | "Protocol D matched the territory flows within 1% in all but two models" (III-B, Fig. 3) | 2 of 921 | MATCH |
| 197 | "Topological errors changed the decision more often than caliber errors away from the throat under Protocols A--C in both beds" (III-A) | point estimates 33>10, 14>8, 19>8; 32>6, 5>1, 8>4 | MATCH |
| 198 | "the excess of tuned over re-derived passes-and-wrong … held only in the discrete bed" (IV-A) | discrete C/D vs B p < 1e-4; leaky p ≥ 0.125 | MATCH |
| 199 | "the error … did so in 57--81% of models" and "A check one branching level finer removed most topological passes-and-wrong but few throat or taper ones" (IV-A) | topological P&W −13/−18 of 20/21 (discrete), −7/−7 of 14/9 (leaky); throat −7 to −26 of 56–243; taper rose | MATCH |
| 200 | "With the main-branch partition the procedure reproduced the original results exactly" (S6) | bit-identical | MATCH |
| 201 | "Excluding them would raise passes-and-wrong by up to 13 points" (S5) and "keeping bound fits is conservative" | 75→88 (+13) is the largest; 80→83, 81→81, 86→87 | MATCH |
| 202 | "all solves converged" (S1) and "All corrupted-model solves converged" (III-A) | converged True on every ok row (abl, per, t5) | MATCH |
| 203 | Denominator consistency (task item 5): Table I basis = status ok, eligible discrete (97), leaky all (150); P&W over defined residual; T5 pools two models per instance (194 / 300) | every table (I, S1, S3, S5, S6, S7, S8-gran, S9, S10, S11) and every text rate reproduces on this basis; the only off-basis counts in the project reports (11 C and 97 D bound fits, all rows) do not appear in the paper (paper uses 10 = 2 + 8 and 64) | MATCH |

## 2. MISMATCH list (OLD → NEW)

**M1. Main III-B, "taper" label on a lesion-length-plus-taper class rate.** The 23% and 9% are 45/194 and 28/300, i.e. the T3+T4 class under Protocol D at the finer level (as Table S8-gran reports under "T3+T4"). The taper alone gives 44/97 = 45% (discrete) and 28/150 = 19% (leaky); T3 contributes 1/97 and 0/150. Either relabel or restate.

OLD (main.tex, line 305):
```
Taper passes-and-wrong rose under Protocol D to 23\% and 9\%, throat passes-and-wrong fell by at most 9 points, to 51--60\% (C) and 78--81\% (D), and flip rates were unchanged (Supplementary Material).
```
NEW (relabel, keeps the supplement's class basis):
```
Caliber passes-and-wrong away from the throat rose under Protocol D to 23\% and 9\%, almost all taper models; throat passes-and-wrong fell by at most 9 points, to 51--60\% (C) and 78--81\% (D), and flip rates were unchanged (Supplementary Material).
```
(Alternative, if the taper figure is wanted: "Taper passes-and-wrong rose under Protocol D to 45\% and 19\%".) The IV-A sentence "removed most topological passes-and-wrong but few throat or taper ones" needs no change.

**M2. Supplement S2, the 23 narrowed-throat Protocol D bound fits "most failing the check".** Of the 23 half-voxel narrowed-throat fits at the bound, 9 fail the check and 14 pass; all 14 are materially wrong. "Most failing" is true of the 64 bound fits that S5 reports (43 of 64 fail) and of the ±10-point subset (34 of 41), not of the 23. S2 and S5 also quote different counts (23 and 64) for what reads as the same set.

OLD (supplement.tex, lines 93–94):
```
Protocol D fits at the $10^{\pm 3}$ bound keep a defined residual and are retained (two
missed-branch models, residual 0.08 and 0.11; 23 throat-error models with a narrowed throat, most failing the check).
```
NEW:
```
Protocol D fits at the $10^{\pm 3}$ bound keep a defined residual and are retained (two
missed-branch models, residual 0.08 and 0.11; 23 half-voxel and 41 ten-point throat-error models with an increased stenosis, of which 43 failed the check and 21 passed while materially wrong).
```
This also makes S2 agree with S5 ("The 64 Protocol D fits at the parameter bound, all with an increased stenosis").

**M3. Main III-A, caliber mean |ΔFFR| range on a narrower protocol set than the flip-rate range in the same sentence.** 0.006–0.037 is the range over Protocols A–C only (T4 under D in the discrete bed has a mean |ΔFFR| of 0.044); the "1–14%" flip range in the same sentence includes Protocol D (the 14% is T4 under D). Either extend the first range or restrict both.

OLD (main.tex, lines 270–271):
```
The caliber errors away from the throat rarely changed the decision. At the magnitude of inter-observer disagreement they changed FFR by
a mean of 0.006--0.037 in absolute value, and their flip rates of 1--14\% were of the order of the 5.0--6.5\%
expected from repeat invasive measurement.
```
NEW:
```
The caliber errors away from the throat rarely changed the decision. At the magnitude of inter-observer disagreement they changed FFR by
a mean of 0.006--0.044 in absolute value, and their flip rates of 1--14\% were of the order of the 5.0--6.5\%
expected from repeat invasive measurement.
```

**M4. Supplement Table S10, the quantity "$|\ln C|$" is not defined.** Neither the S8 text nor the table note says what C is. The table values reproduce only when C is the Protocol C scaling factor applied to the re-derived bed constant (|ln(C_C / C_B)|, and for the negatives |ln(C / C_clean)|, which coincide for correct anatomy); with C taken relative to the clean model the topological AUCs would be 0.62 and 0.22. Add the definition to the table note.

OLD (supplement.tex, line 334):
```
\parbox{0.9\textwidth}{\footnotesize Negatives: 1\,940 (discrete) and 3\,000 (leaky; 2\,990 for $|\ln C|$) correct-anatomy draws on 97 and 150 instances. FA, false alarm; P\&W, passes and wrong; Sens., sensitivity. $^a$Any error type.}
```
NEW:
```
\parbox{0.9\textwidth}{\footnotesize Negatives: 1\,940 (discrete) and 3\,000 (leaky; 2\,990 for $|\ln C|$) correct-anatomy draws on 97 and 150 instances. $|\ln C|$: absolute log of the Protocol C scaling applied to the re-derived bed constant. FA, false alarm; P\&W, passes and wrong; Sens., sensitivity. $^a$Any error type.}
```

## 3. Basis and rounding notes (no text change required; listed for the operator's judgement)

- **N1.** Abstract "5--19\%" is the class-level range (B 14 / 5, C 19 / 8, D 8 / 6); the Conclusion's "5--18\%" is the per-error-type range under B (9, 18, 5, 5) and IV-A's "2--20\%" the per-type range under B–D. All three are correct on their own basis; per type under B and C the range is 5–20% (T2 under C, discrete, 12/60 = 20%). If one basis is preferred for the abstract, "5--20\%" (per type, B and C) or "2--20\%" (per type, B–D) are the alternatives.
- **N2.** "median demand was 137~mL/min per tree" (II-B) and "2.28~mL/s (137~mL/min)" (S4.2) are the medians over the 150 leaky instances (136.8 mL/min); over the 108 distinct trees the median is 133 mL/min. "per tree" reads as "for each tree", which is the instance basis; acceptable.
- **N3.** S6 "Flip rates changed by at most five models per cell" holds for the net count (largest change 10→15, leaky topological D). Individual decisions moved more (discrete topological D: 10 created, 7 reversed; leaky topological D: 9 created, 4 reversed). "Flip counts changed by at most five per cell" would be unambiguous; the T5L2 cells changed by at most two.
- **N4.** S7 "(median 40\% of its volume)": 43% in the discrete-bed tree (truncated at 0.60 mm) and 40% in the leaky-bed tree (0.50 mm). "40--43\%" or "about 40\%" would cover both beds.
- **N5.** III-B "13\%" for Protocol A on the C-defined discrete instances is 13/104 = 12.5%, rounded half-up; the project's generator prints 12 (banker's rounding). Either is defensible; 13 is conventional.
- **N6.** III-B "median $|\Delta\mathrm{FFR}|$ of 0.11--0.16": the leaky Protocol A value is 0.1053, which rounds to 0.11; fine.
- **N7.** III-B "flip rates were unchanged" (throat at the finer level): changed by 0–2 models per cell (73→72, 77→78, 114→116); rounded rates 38→37, 40→40, 37→37, 38→39.

## 4. Counts

- Rows checked: 203 (172 statement and table rows in §1.1–1.7, 18 cross-location checks in §1.8, 13 derived-claim checks in §1.9). Individual values compared, summed from the counts declared in each row: about 1,470 (abstract 24; Methods and captions 94; Table I 228; III-A 57; III-B 72; III-C to Conclusion 64; supplement 929).
- By row: MATCH 188; ROUNDING 2 (#87, #157; smaller rounding remarks inside #12, #96, #151 are noted in N3–N7); NOT-RECOMPUTABLE 9 in full (#14, #26, #34, #35, #37, #38, #113, #154, #162) and 6 in part (#117 the 0.75 mm radius, #125 the model fit, #128 the thermodilution values, #140, #170, #171 the 1.08e-5 residual), about 32 values in all; MISMATCH 4 (#70, #95, #122, #165 = M1–M4), affecting 5 stated values and one missing definition.
- Every Table I cell (218 values), every supplementary table cell (Tables S1–S12, about 800 values) and every headline rate reproduces from the CSVs on the Table I basis.
