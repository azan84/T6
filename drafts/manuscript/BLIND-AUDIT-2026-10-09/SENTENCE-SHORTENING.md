# Sentence shortening proposals for main.tex

Date: 2026-10-09. Scope: main text, abstract excluded. No number, CI, p-value, citation key or LaTeX math is changed. Scope qualifiers are kept. No sentence in a NEW block starts with "Of".

Each OLD block is copied verbatim from main.tex (line breaks included) and matches by exact string replacement exactly once (checked by script, see end). NEW blocks are single-line; the word count given is per new sentence under the counting rule (figures, tables, equations stripped; \cite removed; `$...$` as one word; split on ". " + capital).

Benchmark: nine JBHI full texts, median 21 words, p90 37, 7.6% above 40 words.

---

### 1. Introduction, last paragraph (91 words)

```latex
It judges each error, in the branching, in the caliber away from the lesion and
at the stenosis throat, by the decision at 0.80 against the variability of repeat invasive FFR; solves the same
corrupted anatomy under fixed, re-derived and tuned boundary conditions in two microvascular bed structures; counts
how often a model passes a perfusion check, at two territory resolutions, while its FFR is materially wrong; and
measures what overlap scores and the pre-tuning mismatch show of these errors, with a 3D computational fluid
dynamics (CFD) case as a check.
```

```latex
It judges each error (branching, caliber away from the lesion, stenosis throat) by the decision at 0.80 against the variability of repeat invasive FFR. It solves the same corrupted anatomy under fixed, re-derived and tuned boundary conditions in two microvascular bed structures and counts how often a model passes a perfusion check, at two territory resolutions, while its FFR is materially wrong. It also measures what overlap scores and the pre-tuning mismatch show of these errors, with a 3D computational fluid dynamics (CFD) case as a check.
```

Words: 24 / 38 / 25.

### 2. Methods II-A, host-vessel eligibility (67 words)

```latex
A host vessel (left anterior descending, LAD; left circumflex, LCx; or right coronary artery, RCA) was eligible
when image quality was at least adequate, the taper-fit radius $r_\mathrm{fit}$ (a linear fit of radius along the vessel) at the
lesion center was at least 1.0~mm, native narrowing was below 40\% diameter stenosis (DS) and the FFR before
insertion was at least 0.90 (full criteria in the Supplementary Material).
```

```latex
A host vessel (left anterior descending, LAD; left circumflex, LCx; or right coronary artery, RCA) was eligible when image quality was at least adequate and native narrowing was below 40\% diameter stenosis (DS). The taper-fit radius $r_\mathrm{fit}$ (a linear fit of radius along the vessel) at the lesion center had to be at least 1.0~mm, and the FFR before insertion at least 0.90 (full criteria in the Supplementary Material).
```

Words: 33 / 36. The four criteria are unchanged; two are moved to the second sentence.

### 3. Methods II-A, cohort draw (58 words; also starts with "Of")

```latex
Of the 6\,944 eligible instances (280 host vessels, 140 patients), we drew 25, at random with a fixed seed, in each of six 0.05-wide bands of
leaky-bed baseline (clean-model) FFR from 0.65 to 0.95, at most two per tree, giving 150 instances (50 each in the LAD, LCx and RCA) in 108 trees from 93
patients (Supplementary Material).
```

```latex
From the 6\,944 eligible instances (280 host vessels, 140 patients), we drew 25 at random (fixed seed, at most two per tree) in each of six 0.05-wide bands of leaky-bed baseline (clean-model) FFR from 0.65 to 0.95. The 150 instances (50 each in the LAD, LCx and RCA) lie in 108 trees from 93 patients (Supplementary Material).
```

Words: 37 / 20.

### 4. Methods II-B, hyperemic demand (57 words)

```latex
With $k = 562$~s$^{-1}$, a normal proximal LAD (diameter 3.7~mm \cite{dodge1992}) carries
214~mL/min, within one standard deviation of thermodilution measurements \cite{fournier2021}; because the segmented
arteries were narrower (median inlet radius 1.60~mm), the cohort's median demand was 137~mL/min per tree, and the
pipeline was repeated with $k$ doubled and tripled and with $k$ scaled by 0.7 and 1.3 (Supplementary Material).
```

```latex
With $k = 562$~s$^{-1}$, a normal proximal LAD (diameter 3.7~mm \cite{dodge1992}) carries 214~mL/min, within one standard deviation of thermodilution measurements \cite{fournier2021}. Because the segmented arteries were narrower (median inlet radius 1.60~mm), the cohort's median demand was 137~mL/min per tree, and the pipeline was repeated with $k$ doubled and tripled and scaled by 0.7 and 1.3 (Supplementary Material).
```

Words: 21 / 37.

### 5. Methods II-C, throat error (45 words)

```latex
The throat error (T5) re-inserts the same lesion with its
throat diameter narrowed or widened by half the in-plane voxel size of the scan (median 0.35~mm), each sign a
separate model; a secondary magnitude of $\pm 10$ points of DS is reported in the Supplementary Material.
```

```latex
The throat error (T5) re-inserts the same lesion with its throat diameter narrowed or widened by half the in-plane voxel size of the scan (median 0.35~mm), each sign a separate model. A secondary magnitude of $\pm 10$ points of DS is reported in the Supplementary Material.
```

Words: 31 / 14.

### 6. Methods II-D, Protocol D definition (41 words)

```latex
Under Protocol D (per-territory tuned), the re-derived bed of each territory is scaled by its
own factor, fitted (within $10^{\pm 3}$) so that every territory flow equals its clean target; a fit at this bound keeps a defined residual and is retained.
```

```latex
Under Protocol D (per-territory tuned), the re-derived bed of each territory is scaled by its own factor, fitted (within $10^{\pm 3}$) so that every territory flow equals its clean target. A fit at this bound keeps a defined residual and is retained.
```

Words: 30 / 12.

### 7. Methods II-D, finer territories (45 words)

```latex
Protocols C and D
were also repeated with each main-branch territory divided again at its own first bifurcation (a median of four
territories in the discrete bed and five in the leaky bed), with a territory left without a vessel counted as a
100\% mismatch.
```

```latex
Protocols C and D were also repeated with each main-branch territory divided again at its own first bifurcation (a median of four territories in the discrete bed and five in the leaky bed). A territory left without a vessel counted as a 100\% mismatch.
```

Words: 33 / 12.

### 8. Methods II-E, 3D outlet conditions (41 words)

```latex
Each outlet either set its pressure
to venous pressure plus the clean tree's resistance times its flow (Protocol A), or received a prescribed clean
territory flow, shared over the territory's surviving outlets by bed weight (the per-outlet limit of Protocol D).
```

```latex
Outlets either set pressure to venous pressure plus the clean tree's resistance times their flow (Protocol A), or received prescribed clean territory flows, shared over each territory's surviving outlets by bed weight (the per-outlet limit of Protocol D).
```

Words: 38.

### 9. Methods II-F, McNemar contrasts (59 words)

```latex
Protocol contrasts of flips (B against A, C
against A, C against B) are paired within instance and tested with the exact McNemar test, with Holm adjustment
across the three contrasts of each error type and bed; passes-and-wrong (models passing the check while materially wrong) under tuning (C and D) are compared with
Protocol B by the same test.
```

```latex
Protocol contrasts of flips (B against A, C against A, C against B) are paired within instance and tested with the exact McNemar test, with Holm adjustment across the three contrasts of each error type and bed. Passes-and-wrong (models passing the check while materially wrong) under tuning (C and D) are compared with Protocol B by the same test.
```

Words: 37 / 22.

### 10. Methods II-F, noise floor (49 words)

```latex
For each instance, this is the probability that a repeat invasive FFR falls on the other side of 0.80, following the measurement-certainty approach of \cite{petraco2013}: the repeat is normal about the clean value, taken as the first measurement, with the published standard deviation of the test--retest difference, 0.018 \cite{johnson2015}.
```

```latex
For each instance, this is the probability that a repeat invasive FFR falls on the other side of 0.80, following the measurement-certainty approach of \cite{petraco2013}. The repeat is normal about the clean value, taken as the first measurement, with the published standard deviation of the test--retest difference, 0.018 \cite{johnson2015}.
```

Words: 24 / 24.

### 11. Results III-A, throat error flips (65 words)

```latex
The half-voxel throat error crossed 0.80 in
30\% (24--37\%) and 36\% (31--42\%) of models with fixed boundary conditions, as often as the topological errors on
the same instances (paired sign test, $p = 1.0$ and 0.46) and more often than the other caliber errors ($p < 0.01$
for each sign and bed); every flip followed the sign of the error, and about half ended beyond the 0.75--0.85 grey
zone.
```

```latex
With fixed boundary conditions, the half-voxel throat error crossed 0.80 in 30\% (24--37\%) and 36\% (31--42\%) of models. It flipped as often as the topological errors on the same instances (paired sign test, $p = 1.0$ and 0.46) and more often than the other caliber errors ($p < 0.01$ for each sign and bed). Every flip followed the sign of the error, and about half ended beyond the 0.75--0.85 grey zone.
```

Words: 18 / 33 / 17.

### 12. Results III-B, Protocol C residual (43 words)

```latex
Fitting one bed scaling to the clean territory flows (Protocol C) lowered the median perfusion residual of
topological-error models from 0.22 under Protocol A to 0.14 in the discrete bed and from 0.11 to 0.02 in the
leaky bed, on the same instances.
```

```latex
Protocol C (one bed scaling fitted to the clean territory flows) lowered the median perfusion residual of topological-error models on the same instances from 0.22 under Protocol A to 0.14 (discrete) and from 0.11 to 0.02 (leaky).
```

Words: 37.

### 13. Results III-B, Protocol D correction (44 words)

```latex
Protocol D matched the territory flows within 1\% in all but two models (Supplementary Material) and corrected most of the topological error:
the median $|\Delta\mathrm{FFR}|$ of topological-error models fell to 0.005 in both beds, and their flip rate to 8\%
(discrete) and 6\% (leaky).
```

```latex
Protocol D matched the territory flows within 1\% in all but two models (Supplementary Material) and corrected most of the topological error. The median $|\Delta\mathrm{FFR}|$ of topological-error models fell to 0.005 in both beds, and their flip rate to 8\% (discrete) and 6\% (leaky).
```

Words: 22 / 22.

### 14. Results III-B, missed-branch shift (54 words)

```latex
For the missed branch, which raised FFR by a median of 0.095 (discrete) and 0.047
(leaky) with fixed boundary conditions, Protocol C reduced the shift to 0.077 and 0.015 (Wilcoxon signed-rank,
$p < 0.001$ in both beds) and Protocol D to 0.000 and 0.004, with 10 of 44 and 3 of 71 instances still above 0.05.
```

```latex
With fixed boundary conditions the missed branch raised FFR by a median of 0.095 (discrete) and 0.047 (leaky). Protocol C reduced the shift to 0.077 and 0.015 (Wilcoxon signed-rank, $p < 0.001$ in both beds) and Protocol D to 0.000 and 0.004, with 10 of 44 and 3 of 71 instances still above 0.05.
```

Words: 18 / 34.

### 15. Results III-B, topological passes-and-wrong (56 words)

```latex
After Protocol C, 20 of 104 topological-error
models (19\%, 13--28\%) in the discrete bed and 14 of 171 (8\%, 5--13\%) in the leaky bed passed the perfusion check
while their FFR was materially wrong (more than 0.05 from the clean value); after Protocol D, 21 of 104 (20\%,
14--29\%) and 9 of 171 (5\%, 3--10\%) did.
```

```latex
After Protocol C, 20 of 104 topological-error models (19\%, 13--28\%) in the discrete bed and 14 of 171 (8\%, 5--13\%) in the leaky bed passed the perfusion check while their FFR was materially wrong ($|\Delta\mathrm{FFR}| > 0.05$). After Protocol D, 21 of 104 (20\%, 14--29\%) and 9 of 171 (5\%, 3--10\%) did.
```

Words: 36 / 16. The parenthetical restates the Methods definition in its symbolic form (same 0.05).

### 16. Results III-B, throat passes-and-wrong (57 words)

```latex
With fixed or re-derived boundary
conditions 29\% (discrete) and 42\% (leaky) of half-voxel throat-error models passed while materially wrong, after
Protocol C 57\% and 69\%, and after Protocol D 80\% and 81\%, with a median $|\Delta\mathrm{FFR}|$ of 0.11--0.16;
tuning moved FFR further from the clean value because the clean territory flow was forced through a wrong throat.
```

```latex
With fixed or re-derived boundary conditions 29\% (discrete) and 42\% (leaky) of half-voxel throat-error models passed while materially wrong, after Protocol C 57\% and 69\%, and after Protocol D 80\% and 81\%, with a median $|\Delta\mathrm{FFR}|$ of 0.11--0.16. Tuning moved FFR further from the clean value because the clean territory flow was forced through a wrong throat.
```

Words: 38 / 20.

### 17. Results III-B, finer territories (73 words)

```latex
With each main-branch territory divided again at its first bifurcation, topological passes-and-wrong fell to 7\%
(C) and 3\% (D) in the discrete bed and to 5\% and 2\% in the leaky bed, near the 3--4\% of correct anatomy at
main-branch level, whereas taper passes-and-wrong rose under Protocol D to 23\% and 9\% and throat passes-and-wrong
fell by at most 9 points, to 51--60\% (C) and 78--81\% (D), with flip rates unchanged (Supplementary Material).
```

```latex
With main-branch territories subdivided at their first bifurcation, topological passes-and-wrong fell to 7\% (C) and 3\% (D) in the discrete bed and to 5\% and 2\% in the leaky bed, near the 3--4\% of correct anatomy at main-branch level. Taper passes-and-wrong rose under Protocol D to 23\% and 9\%, throat passes-and-wrong fell by at most 9 points, to 51--60\% (C) and 78--81\% (D), and flip rates were unchanged (Supplementary Material).
```

Words: 39 / 31.

### 18. Results III-C, tube-model DSC (61 words)

```latex
In a tube model of each tree, the missed branch and the taper had the same median DSC (0.97), although the missed
branch changed the decision about twice as often (27\% against 13\% discrete, 18\% against 9\% leaky); a vessel
break lowered the DSC to 0.89, and to 0.62 in the right coronary artery, and clDice fell only for topological
errors.
```

```latex
In a tube model of each tree, the missed branch and the taper had the same median DSC (0.97), although the missed branch changed the decision about twice as often (27\% against 13\% discrete, 18\% against 9\% leaky). A vessel break lowered the DSC to 0.89, and to 0.62 in the right coronary artery; clDice fell only for topological errors.
```

Words: 38 / 22.

### 19. Results III-D, 3D prescribed flows (52 words)

```latex
With the clean
territory flows prescribed at the outlets (the limit of Protocol D), the error changed FFR by $-0.0007$ against the clean geometry under the same flows (0.892 in both) and by $+0.022$
against the clean tree with its resistances (0.870), because sharing territory flow by bed weight moved the baseline.
```

```latex
With the clean territory flows prescribed at the outlets (the limit of Protocol D), the error changed FFR by $-0.0007$ against the clean geometry under the same flows (0.892 in both). It was $+0.022$ against the clean tree with its resistances (0.870), because sharing territory flow by bed weight moved the baseline.
```

Words: 31 / 21.

### 20. Results III-D, meshed lumen (46 words)

```latex
The meshed lumen was wider than the reduced-order radius (throat 0.276 against 0.231~mm; baseline
0.761 on the reduced-order radius), and a finer throat zone changed the baseline FFR by at most 0.0021, although the
strict residual limit was not met on the finest mesh (Supplementary Material).
```

```latex
The meshed lumen was wider than the reduced-order radius (throat 0.276 against 0.231~mm; baseline 0.761 on the reduced-order radius). A finer throat zone changed the baseline FFR by at most 0.0021, although the strict residual limit was not met on the finest mesh (Supplementary Material).
```

Words: 20 / 26.

### 21. Results III-D, demand sensitivity (59 words)

```latex
With the hyperemic demand constant $k$ doubled and tripled, the lesion insertion, cohort selection and all four protocols were repeated; the
flip-rate directions held in both beds at twice and in the leaky bed at three times the demand, but the excess of
tuned over re-derived passes-and-wrong was significant at twice the demand in no topological comparison
(Supplementary Material).
```

```latex
With the hyperemic demand constant $k$ doubled and tripled, the lesion insertion, cohort selection and all four protocols were repeated. The flip-rate directions held in both beds at twice and in the leaky bed at three times the demand, but the excess of tuned over re-derived passes-and-wrong was not significant in any topological comparison at twice the demand (Supplementary Material).
```

Words: 20 / 40.

### 22. Discussion IV-A, opening (63 words)

```latex
With fixed boundary conditions, the decision risk of segmentation lay in the branching and at the stenosis throat:
a missed branch, a vessel break or a half-voxel error in throat diameter each changed about a third of decisions in
this threshold-stratified cohort, whereas caliber errors of inter-observer magnitude away from the throat changed
decisions at rates of the order of repeat invasive measurement.
```

```latex
With fixed boundary conditions, the decision risk of segmentation lay in the branching and at the stenosis throat. A missed branch, a vessel break or a half-voxel error in throat diameter each changed about a third of decisions in this threshold-stratified cohort. Caliber errors of inter-observer magnitude away from the throat changed decisions at rates of the order of repeat invasive measurement.
```

Words: 18 / 24 / 20.

### 23. Discussion IV-A, caliber errors after tuning (47 words)

```latex
In both beds tuning turned
caliber errors into passing models with a wrong FFR, because restoring the clean flow through a narrowed lumen enlarges
its pressure drop; for the throat error, which the check did not see even before tuning, it did so in 57--81\% of models.
```

```latex
In both beds tuning turned caliber errors into passing models with a wrong FFR, because restoring the clean flow through a narrowed lumen enlarges its pressure drop. For the throat error, which the check did not see even before tuning, it did so in 57--81\% of models.
```

Words: 27 / 20.

### 24. Discussion IV-B, overlap scores (57 words)

```latex
In our tube model a missed branch left the DSC as high as a taper did while changing the decision twice as often,
and a vessel break lowered the whole-scan DSC below the inter-observer value only in the right coronary artery, so
overlap scores, including the topology-aware clDice \cite{shit2021}, did not rank these errors by decision risk.
```

```latex
In our tube model a missed branch kept the DSC as high as a taper while changing the decision twice as often, and a vessel break lowered the whole-scan DSC below the inter-observer value only in the RCA. Overlap scores, including the topology-aware clDice \cite{shit2021}, therefore did not rank these errors by decision risk.
```

Words: 36 / 16.

### 25. Discussion IV-C, second consideration (49 words)

```latex
Second, check the lumen caliber, above all the throat diameter: caliber errors of
inter-observer size away from the throat flipped decisions at rates near repeat invasive measurement (the taper up to 14\%), a half-voxel throat error flipped 30--36\%, and after
tuning both produced passing models with a wrong FFR.
```

```latex
Second, check the lumen caliber, above all the throat diameter. Caliber errors of inter-observer size away from the throat flipped decisions at rates near repeat invasive measurement (the taper up to 14\%), a half-voxel throat error flipped 30--36\%, and after tuning both produced passing models with a wrong FFR.
```

Words: 10 / 39.

### 26. Limitations, throat magnitudes (42 words)

```latex
The throat magnitudes are half a voxel and $\pm 10$
points of DS \cite{boogers2010,gouya2009}; validated clinical computation of FFR from CT includes an expert review of the lumen before
simulation \cite{norgaard2014}, so the throat rates describe an error that reaches the model unreviewed.
```

```latex
The throat magnitudes are half a voxel and $\pm 10$ points of DS \cite{boogers2010,gouya2009}. Validated clinical computation of FFR from CT includes an expert review of the lumen before simulation \cite{norgaard2014}, so the throat rates describe an error that reaches the model unreviewed.
```

Words: 12 / 29.

### 27. Limitations, 3D instance (54 words)

```latex
The 3D analysis covers one instance, whose
meshed lumen was wider than the reduced-order radius; this offset (0.045~mm at the throat) moved the baseline
across 0.80 (0.761 against 0.870) and changed the size of the error effect ($+0.127$ against $+0.081$ on the meshed radius), but not its
direction or its reduction by prescribed flows.
```

```latex
The 3D analysis covers one instance, whose meshed lumen was wider than the reduced-order radius. This offset (0.045~mm at the throat) moved the baseline across 0.80 (0.761 against 0.870) and changed the size of the error effect ($+0.127$ against $+0.081$ on the meshed radius), but not its direction or its reduction by prescribed flows.
```

Words: 15 / 40.

### 28. Conclusion, tuning sentence (41 words)

```latex
Tuning to perfusion reduced topological changes without making the models correct: up to
one in five tuned topological-error models (discrete bed; 5--8\% leaky) and 57--81\% of throat-error models passed a
main-branch perfusion check while materially wrong, against 3--4\% for correct anatomy.
```

```latex
Tuning to perfusion reduced topological changes without making the models correct. Up to one in five tuned topological-error models (discrete bed; 5--8\% leaky) and 57--81\% of throat-error models passed a main-branch perfusion check while materially wrong, against 3--4\% for correct anatomy.
```

Words: 11 / 30.

### 29. Results III-C, sentence starting with "Of" (rule, not length; 35 words)

The only other sentence in main.tex that starts with "Of". One-word change.

```latex
Of the decision-changing topological errors, 91\% (discrete) and 62\% (leaky) kept a whole-scan DSC at or
```

```latex
Among the decision-changing topological errors, 91\% (discrete) and 62\% (leaky) kept a whole-scan DSC at or
```

Words: unchanged (35).

---

## Verification

Script: scratchpad `apply.py` (parses the OLD/NEW pairs above, applies them to a copy of main.tex, recounts with `sentstats.py`). Run 2026-10-09 against the current main.tex, after the coordinator's III-A edit ("Re-deriving the boundary conditions..." left untouched).

- All 29 OLD strings match main.tex exactly once.
- Characters in the replaced passages: 9,549 before, 9,459 after (-90).
- Compiled copies (latexmk, same cls/sty/figures): 8 pages both; last page 56 text lines before, 55 after; overfull boxes 9 before, 9 after (all pre-existing).
- No sentence in the applied copy starts with "Of".

Sentence statistics, main text excluding the abstract, counting rule as above:

| | n | mean | median | p90 | max | > 40 words |
|---|---|---|---|---|---|---|
| Before | 208 | 25.5 | 24 | 45 | 91 | 28 (13.5%) |
| After | 237 | 22.3 | 22 | 35 | 40 | 0 (0%) |
| JBHI benchmark (9 full texts) | | | 21 | 37 | | 7.6% |

Two new sentences sit at exactly 40 words (#21 second sentence, #27 second sentence); both carry numeric lists.
