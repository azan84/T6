# G3 wording pass: exact OLD/NEW replacements (2026-10-09, night)

Source: FABLE-RESCORE-AUDIT.md, go-list item G3 and §A.2. Files: `main.tex`, `supplement.tex`,
`supplement_tables/tab_thresholds.tex` (the body of Table S3), all as of 2026-10-09 17:04. Nothing has been
edited; this file lists the replacements for G6 to apply.

Every OLD string below was copied from the current file and checked by
`BLIND-RESCORE-2026-10-09/check_wording_pass.py` to occur exactly once (run it from `drafts/manuscript/`; `--apply OUTDIR`
writes patched copies for a trial build). Line breaks inside an OLD block are the file's own line breaks.
Group `required` = the G3 items; `offset` = cuts that pay for them; `house` = zero-cost house-rule fixes (optional).
Typeset-line estimates use 60 characters per line in the two-column main text and 120 in the one-column supplement;
the measured result of a trial build is given below and is the figure that counts.

## Measured result (trial builds in the session scratchpad, same class and bib)

| Build | Main | Page 9, right column, last baseline | Supplement | Abstract words |
|---|---|---|---|---|
| Current files | 9 pp | y = 186 pt | 5 pp, page 5 full (y = 741) | 249 |
| required + house only | 9 pp | y = 276 pt (**+7.5 lines**) | **6 pp** (3 lines spill) | 249 |
| required + house + all offsets | 9 pp | y = 132 pt (**-4.5 lines**) | 5 pp, page 5 full (y = 741), net 0 | 249 |
| as above without M23 | 9 pp | y = 186 pt (net 0) | 5 pp | 249 |
| as above without M23 and M31 | 9 pp | y = 222 pt (+3 lines) | 5 pp | 249 |

So: the required items alone add about 7.5 main-text lines and 2 supplement lines. With the offsets (M19, M23--M26,
M29--M31 in the main text; S03 in the supplement) the main text is 4.5 lines shorter than now and the supplement is
unchanged in length. M23 is the one offset that can be dropped while keeping the net at 0.

Measured now, for the record: the right column of main page 9 ends at y = 186 pt of 742, i.e. about 43 of 61 lines
are free; the constraint "net change 0 or negative" is honoured regardless.

Estimated totals (characters / 60 or 120): main required + house +10.8 lines, with offsets +0.4;
supplement required + house +1.6 lines, with offsets +0.6; Table S3 rows 0.

## Markers for the other agents (not drafted here)

- `[G5 abstract]` main.tex, abstract: "After tuning, a perfusion check stricter than measurement repeatability passed
  models wrong by more than 0.05 in 19--20\% (discrete) and 5--8\% (leaky) of topological-error cases and 57--81\% of
  throat-error cases. Other caliber errors did so in 4--18\% and correct anatomy in 3--4\%." After this pass the abstract
  is at 249 words, so the G5 restatement must be net +1 word or fewer.
- `[G5 III-B]` "Models with correct anatomy, tuned to perfusion targets carrying simulated physiological noise (the second
  floor), passed while materially wrong in 3.1\% ... 7.2\%." and, in the finer-territory sentence, "near the 3--4\% of
  correct anatomy at main-branch level".
- `[G5 III-C]` "The perfusion residual before tuning separated topological errors from correct anatomy with noisy targets in
  the discrete bed only (AUC 0.77 against 0.22), flagging 83\% of them and 48\% of correct models at the 10\% check."
  (matched AUCs 0.82/0.56; an AUC of 0.22 is not "separation").
- `[G5 IV-A]` "Per-territory tuning passes almost every model by design, and in the discrete bed one in five ..." (EIC W5,
  residual error after exact matching) and `[G5 IV-C]` "Third, record the perfusion mismatch before tuning: it marked
  topological errors only in the discrete bed (AUC 0.77), and half of the correct models with noisy targets exceeded 10\%."
- `[G5 Conclusion]` "Up to one in five tuned topological-error models (discrete bed; 5--8\% leaky) and 57--81\% of
  throat-error models passed a main-branch perfusion check while materially wrong, against 3--4\% for correct anatomy."
  M21 adds the sentence that follows it and opens with "These proportions hold at the primary demand", so the G5 rewrite
  must keep the passes-and-wrong proportions as the subject of the sentence immediately before.
- `[G5 Limitations]` "Tuning targets were error-free clean-model flows (noise entered only the simulated floor)."
- `[G4 III-D]` the demand paragraph "With the hyperemic demand constant $k$ doubled and tripled, ..." takes the one
  Robustness sentence on T5 at higher demand; the supplement row block goes in Table S5 or S7.
- `[G5 supplement]` S8 text (matched AUCs) and S9/Table S11 (Protocol D floor). After this pass supplement page 5 is full
  again, so the new table needs its own offset (G6).

## Numbers that G7 must confirm from the CSVs

- M09: McNemar for T5, A against C and D, from the audit's scratch computation (half-voxel, both signs pooled): discrete
  C 15 created / 0 reversed, p = 1e-4 (n = 193); D 19 / 0, p < 1e-4 (n = 194); leaky C 5 / 1, p = 0.22; D 6 / 0,
  p = 0.031. Holm over the two contrasts: leaky 0.22 and 0.062. The text quotes p < 0.001 (discrete) and 0.22 and 0.06
  (leaky).
- S04: 3D-case flows from the frozen pullback and `cfd_M1`: cohort-model inflow 0.649 (discrete) and 0.672 (leaky) mL/s;
  lesion flow 0.173 and 0.153 mL/s; 3D baseline inflow 0.682 mL/s, about 10--11 mL/min through the lesion; mean throat
  velocity 0.73 m/s at r = 0.276 mm; Re = 1060 x 0.73 x 0.552e-3 / 0.004 = 107.

## A. Main text, required (G3 items)

### M01 (Abstract)

File: `main.tex` | Group: required

OLD:
```text
In this threshold-stratified cohort, with fixed boundary conditions,
```

NEW:
```text
For the error magnitudes studied, in this threshold-stratified cohort with fixed boundary conditions,
```

Delta: +33 characters, about +0.6 typeset lines.

Note: Magnitude qualifier restored (+5 words).

### M02 (Abstract)

File: `main.tex` | Group: required

OLD:
```text
discrete and leaky (distributed-outflow) microvascular beds
```

NEW:
```text
discrete and leaky microvascular beds
```

Delta: -22 characters, about -0.4 typeset lines.

Note: Cut (-1 word); the leaky bed is defined in II-B.

### M03 (Abstract)

File: `main.tex` | Group: required

OLD:
```text
with one global or per-territory parameter fitted to clean flows of main-branch territories.
```

NEW:
```text
with one global or per-territory parameter fitted to clean main-branch territory flows.
```

Delta: -5 characters, about -0.1 typeset lines.

Note: Cut (-1 word).

### M04 (Abstract)

File: `main.tex` | Group: required

OLD:
```text
(missed side branch, vessel
break, longer lesion, narrowed taper, half-voxel throat diameter)
```

NEW:
```text
(missed branch, vessel break, longer lesion, narrowed taper, half-voxel throat diameter)
```

Delta: -5 characters, about -0.1 typeset lines.

Note: Cut (-1 word); 'missed branch' is the term used for T1 in II-C.

### M05 (Abstract)

File: `main.tex` | Group: required

OLD:
```text
Re-derived or tuned boundary conditions reduced topological flips to 5--19\% but not throat flips.
```

NEW:
```text
Re-derived or tuned boundary conditions reduced topological flips to 5--19\% but did not reduce throat flips.
```

Delta: +11 characters, about +0.2 typeset lines.

Note: Throat flips rose under tuning (Table I); 'did not reduce' is the direction-safe claim for both beds (+2 words). 5--19% = pooled B--D, the one basis used in the Conclusion (M22).

### M06 (Abstract)

File: `main.tex` | Group: required

OLD:
```text
A missed branch kept a near-perfect Dice score (0.97, as high as a taper) yet changed the decision twice as often.
```

NEW:
```text
A missed branch shared the taper's tube-model Dice score (0.97) yet changed the decision twice as often.
```

Delta: -10 characters, about -0.2 typeset lines.

Note: 'tube-model' labels the Dice level (-4 words).

### M07 (II-F Outcomes and Statistical Analysis)

File: `main.tex` | Group: required

OLD:
```text
Protocol contrasts of flips (B against A, C against A, C against B) are paired within instance and tested with the exact McNemar test, with Holm adjustment across the three contrasts of each error type and bed.
```

NEW:
```text
Protocol contrasts of flips (B against A, C against A, C against B) are paired within instance and tested with the exact McNemar test, with Holm adjustment across the contrasts of each error type and bed. For the throat error the contrasts are C and D against A.
```

Delta: +52 characters, about +0.9 typeset lines.

Note: Declares the throat-error contrasts that M09 reports.

### M08 (II-F, last paragraph)

File: `main.tex` | Group: required

OLD:
```text
Because the cohort was stratified to span 0.80, its rates are conditional
on that design and are not clinical prevalences. The analysis pipeline is shown in the Supplementary Material.
```

NEW:
```text
The cohort was stratified to span 0.80, so its rates are conditional on that design and are not clinical prevalences (analysis pipeline in the Supplementary Material).
```

Delta: -17 characters, about -0.3 typeset lines.

Note: House rule (no 'Because' opening) and a half-line cut.

### M09 (III-A, throat error)

File: `main.tex` | Group: required

OLD:
```text
Re-derived boundary conditions coincide with fixed ones for this error by construction, and tuning left its
flip rate at 37--40\%.
```

NEW:
```text
Re-derived boundary conditions coincide with fixed ones for this error by construction. Tuning raised its flip rate from 30\% to 38--40\% in the discrete bed (15 and 19 flips created, none reversed; McNemar $p < 0.001$) and from 36\% to 37--38\% in the leaky bed ($p = 0.22$ and 0.06).
```

Delta: +155 characters, about +2.6 typeset lines.

Note: McNemar from the audit (A.2): discrete A->C 15 created/0 reversed p = 1e-4 (n = 193), A->D 19/0 p < 1e-4 (n = 194); leaky A->C 5/1 p = 0.22, A->D 6/0 p = 0.031, Holm over the two contrasts gives 0.22 and 0.062. VERIFY in G7 from the T5 CSVs.

### M10 (III-A, caliber errors)

File: `main.tex` | Group: required

OLD:
```text
and their flip rates of 1--14\% were of the order of the 5.0--6.5\%
expected from repeat invasive measurement. The taper had the highest rates: 13\% and 14\% in the discrete bed under fixed boundary
conditions and Protocol D, and 9\% in the leaky bed under fixed boundary conditions.
```

NEW:
```text
and their flip rates (1--14\%) were compared with the 5.0--6.5\% expected from repeat invasive measurement. Only the taper's rates in the discrete bed, 13\% and 14\% under fixed boundary conditions and Protocol D, had lower confidence bounds (8\% and 9\%) above that floor; its leaky-bed rate was 9\% (6--15\%).
```

Delta: +28 characters, about +0.5 typeset lines.

Note: Taper against the floor, descriptive (clustered CIs): discrete lower bounds 8 and 9 exceed 6.5; leaky lower bound 6 lies inside 5.0--6.5.

### M11 (III-A, Protocol B)

File: `main.tex` | Group: required

OLD:
```text
Re-deriving the boundary conditions (Protocol B) produced the fewest flips.
```

NEW:
```text
Re-deriving the boundary conditions (Protocol B) produced the fewest flips among Protocols A--C.
```

Delta: +21 characters, about +0.3 typeset lines.

Note: Protocol D gives fewer in the discrete bed (T1 2% vs 9%; pooled 8% vs 14%).

### M12 (III-B, finer territories)

File: `main.tex` | Group: required

OLD:
```text
and flip rates were unchanged (Supplementary Material).
```

NEW:
```text
and flip counts changed by at most five per cell (Supplementary Material).
```

Delta: +19 characters, about +0.3 typeset lines.

Note: Matches S6.

### M13 (III-C, Fig. 4 level)

File: `main.tex` | Group: required

OLD:
```text
In a tube model of each tree, the missed branch and the taper had the same median DSC (0.97), although the missed branch changed the decision about twice as often (27\% against 13\% discrete, 18\% against 9\% leaky; Fig.~\ref{fig:overlap}).
```

NEW:
```text
In a tube model of each tree, the missed branch and the taper had the same median DSC (0.97 per tree; 0.98 over the whole scan, Fig.~\ref{fig:overlap}). The missed branch changed the decision about twice as often (27\% against 13\% discrete, 18\% against 9\% leaky).
```

Delta: +26 characters, about +0.4 typeset lines.

Note: Fig. 4 plots whole-scan DSC (T1 0.985/0.983, T4 0.983/0.983; Table S9); the text quoted the tree median.

### M14 (IV-A, first paragraph)

File: `main.tex` | Group: required

OLD:
```text
With fixed boundary conditions, the decision risk of segmentation lay in the branching and at the stenosis throat. A missed branch, a vessel break or a half-voxel error in throat diameter each changed about a third of decisions in this threshold-stratified cohort. Caliber errors of inter-observer magnitude away from the throat changed decisions at rates of the order of repeat invasive measurement.
```

NEW:
```text
With fixed boundary conditions, topological errors (18--43\% per type) and the half-voxel throat error each changed about a third of decisions in this threshold-stratified cohort. Caliber errors of inter-observer magnitude away from the throat changed decisions at rates near repeat invasive measurement, except the taper in the discrete bed (13--14\%).
```

Delta: -47 characters, about -0.8 typeset lines.

Note: 'About a third' now refers to the pooled topological rate (33/32%) and T5 (30/36%); per-type range given (T1 27/18, T2 40/43). Topic sentence folded in (offsets 1.5 lines).

### M15 (IV-A, second paragraph)

File: `main.tex` | Group: required

OLD:
```text
Re-deriving or tuning the bed reduced topological flips from 18--43\% to 2--20\% per error type and left throat
flips unchanged.
```

NEW:
```text
Re-deriving or tuning the bed reduced topological flips from 32--33\% to 5--19\% (pooled over error types) and did not reduce throat flips.
```

Delta: +11 characters, about +0.2 typeset lines.

Note: One basis (pooled B--D: B 14/5, C 19/8, D 8/6) in abstract, IV-A and Conclusion; per-type rates stay in Table I.

### M16 (IV-B, clDice)

File: `main.tex` | Group: required

OLD:
```text
Overlap scores, including the topology-aware clDice \cite{shit2021}, therefore did not rank these errors by decision risk.
```

NEW:
```text
The topology-aware clDice \cite{shit2021} separated topological from caliber errors but is blind to the throat error, which changes no centerline, so overlap scores did not rank these errors by decision risk.
```

Delta: +86 characters, about +1.4 typeset lines.

Note: Table S9: clDice 0.93--0.94 (T1), 0.85 (T2), 1.000 (T3, T4); T5 keeps the node set, so clDice = 1 by construction.

### M17 (IV-D Limitations, Protocol B)

File: `main.tex` | Group: required

OLD:
```text
so their results for these errors describe the left coronary tree. Hyperemic
demand followed
```

NEW:
```text
so their results for these errors describe the left coronary tree. The reference obeys the same bed rule as Protocol B, so re-derivation carries no physiological deviation for tuning to correct. Hyperemic demand followed
```

Delta: +128 characters, about +2.1 typeset lines.

Note: R2 W2 limitation sentence (a).

### M18 (IV-D Limitations, finer check)

File: `main.tex` | Group: required

OLD:
```text
A perfusion check one
branching level finer detected most topological errors that passed at main-branch level, but not throat or taper
errors. Tuning targets
```

NEW:
```text
The finer perfusion check counts a territory without a surviving vessel as a 100\% mismatch, which presumes the territory is known to exist. Tuning targets
```

Delta: -2 characters, about -0.0 typeset lines.

Note: DA C3 limitation sentence (b) replaces a sentence that restated a result already in IV-A.

### M20 (Conclusion, sentences 3--5)

File: `main.tex` | Group: required

OLD:
```text
With fixed boundary conditions, a missed branch, a vessel break or a half-voxel throat error each changed about a
third of decisions in this threshold-stratified cohort, against rates near repeat measurement for caliber errors
away from the throat. Re-derived boundary conditions reduced topological decision changes to 5--18\% but left
throat errors unchanged. Tuning to perfusion reduced topological changes without making the models correct.
```

NEW:
```text
With fixed boundary conditions, topological errors (18--43\% per type) and a half-voxel throat error each changed about a third of decisions in this threshold-stratified cohort, against 2--13\% for caliber errors away from the throat. Re-derived or tuned boundary conditions reduced topological decision changes to 5--19\% without reducing throat decision changes or making the models correct.
```

Delta: -51 characters, about -0.8 typeset lines.

Note: 'About a third' on the pooled basis; caliber under fixed BCs 2--13% (T3 7/2, T4 13/9); 5--18% -> 5--19% (pooled B--D); two sentences merged (offsets 1 line).

### M21 (Conclusion, after the G5 sentence)

File: `main.tex` | Group: required

OLD:
```text
Safeguards are therefore most
needed at the branching near the lesion and at the throat diameter, which overlap scores do not rank by decision risk.
```

NEW:
```text
These proportions hold at the primary demand; one branching level finer, topological passes-and-wrong fell to 2--7\% and throat passes-and-wrong changed little. At the magnitudes tested, errors at the branching near the lesion and at the throat diameter were the most consequential per occurrence, and tube-model overlap scores did not rank them by decision risk.
```

Delta: +215 characters, about +3.6 typeset lines.

Note: DA C2, C6: 'at the primary demand', the finer 2--7% (S6: 7/3 discrete, 5/2 leaky; throat fell by at most 9 points), 'most consequential per occurrence at the magnitudes tested', 'tube-model'. 'Safeguards are ... needed' was an instruction.

### M22 (Acknowledgment)

File: `main.tex` | Group: required

OLD:
```text
The authors thank the creators of ImageCAS and ImageCAS-X for making their data publicly available. The authors
used Grammarly for language editing.
```

NEW:
```text
The authors thank the creators of ImageCAS and ImageCAS-X for making their data publicly available and used Grammarly for language editing. The authors declare no competing interests.
```

Delta: +35 characters, about +0.6 typeset lines.

Note: Competing-interests line in the back matter; no funding statement (JBHI practice when there is no funding).

## B. Main text, offsetting cuts (apply all; M23 is the one that can be dropped at net 0)

### M19 (IV-D Limitations, 3D offset)

File: `main.tex` | Group: offset

OLD:
```text
The 3D analysis covers one instance, whose meshed lumen was wider than the reduced-order radius. This offset (0.045~mm at the throat) moved the baseline across 0.80 (0.761 against 0.870) and changed the size of the error effect ($+0.127$ against $+0.081$ on the meshed radius), but not its direction or its reduction by prescribed flows.
```

NEW:
```text
The 3D analysis covers one instance, whose meshed lumen was wider than the reduced-order radius; the offset changed the size of the error effect but not its direction or its reduction by prescribed flows.
```

Delta: -133 characters, about -2.2 typeset lines.

Note: Offset cut: the numbers (0.276 vs 0.231 mm, 0.761, +0.127 vs +0.081) are all in III-D.

### M23 (I Introduction, last paragraph)

File: `main.tex` | Group: offset

OLD:
```text
with a 3D computational fluid
dynamics (CFD) case as a check. The results show which segmentation errors change the treatment decision, and whether overlap scores or perfusion
agreement detect them.
```

NEW:
```text
with a 3D computational fluid
dynamics (CFD) case as a check.
```

Delta: -137 characters, about -2.3 typeset lines.

Note: Offset cut of a forward pointer; the paragraph still states what the test judges, solves, counts and measures.

### M24 (II-D, Protocol C/D flexibility)

File: `main.tex` | Group: offset

OLD:
```text
One parameter against two or more targets makes the fit over-determined, so this is the least flexible tuning tested. Under Protocol D
```

NEW:
```text
Under Protocol D
```

Delta: -118 characters, about -2.0 typeset lines.

Note: Offset cut; paired with M25, which keeps both flexibility statements in one sentence.

### M25 (II-D, Protocol D)

File: `main.tex` | Group: offset

OLD:
```text
With one parameter per target the fit is
exactly determined, the most flexible tuning to territory flows.
```

NEW:
```text
With one parameter per target the fit is exactly determined, the most flexible tuning tested; Protocol C, with one parameter against two or more targets, is the least.
```

Delta: +62 characters, about +1.0 typeset lines.

Note: Goes with M24.

### M26 (IV-C, first consideration)

File: `main.tex` | Group: offset

OLD:
```text
First, check that the side branches
beyond the lesion are present and that no vessel ends early, because a missed branch leaves the overlap score as high as a taper does.
```

NEW:
```text
First, check that the side branches beyond the lesion are present and that no vessel ends early.
```

Delta: -74 characters, about -1.2 typeset lines.

Note: Offset cut; the overlap point is made in IV-B two sentences earlier.

### M29 (IV-A, non-identifiability)

File: `main.tex` | Group: offset

OLD:
```text
the results give the size of this non-identifiability
at the decision level and show that it depends on the error type and on the resolution of the check.
```

NEW:
```text
the results give the size of this non-identifiability at the decision level, by error type and check resolution.
```

Delta: -42 characters, about -0.7 typeset lines.

Note: Offset cut.

### M30 (IV-A, throat result and sensitivity analyses)

File: `main.tex` | Group: offset

OLD:
```text
The throat result agrees with sensitivity analyses
in which the computed pressure index responds most to the minimal lumen, increasingly so with stenosis severity
\cite{sankaran2015tmi,fernandez2024}; the present test adds the effect on the decision and the interaction with
tuning.
```

NEW:
```text
The throat result agrees with sensitivity analyses in which the pressure index responds most to the minimal lumen \cite{sankaran2015tmi,fernandez2024}; the present test adds the decision and the interaction with tuning.
```

Delta: -63 characters, about -1.1 typeset lines.

Note: Offset cut; the severity dependence is stated in the Introduction.

### M31 (IV-C, second consideration)

File: `main.tex` | Group: offset

OLD:
```text
Second, check the lumen caliber, above all the throat diameter. Caliber errors of inter-observer size away from the throat flipped decisions at rates near repeat invasive measurement (the taper up to 14\%), a half-voxel throat error flipped 30--36\%, and after tuning both produced passing models with a wrong FFR.
```

NEW:
```text
Second, check the lumen caliber, above all the throat diameter: a half-voxel throat error flipped 30--36\%, and after tuning both throat and taper errors produced passing models with a wrong FFR.
```

Delta: -119 characters, about -2.0 typeset lines.

Note: Offset cut; the caliber rates are in III-A and IV-A.

## C. Main text, house-rule fixes at zero cost (optional)

### M27 (II-B, demand)

File: `main.tex` | Group: house

OLD:
```text
Because the segmented arteries were narrower (median inlet radius 1.60~mm), the cohort's median demand was 137~mL/min per tree, and the pipeline was repeated
```

NEW:
```text
The segmented arteries were narrower (median inlet radius 1.60~mm), so the cohort's median demand was 137~mL/min per tree; the pipeline was repeated
```

Delta: -9 characters, about -0.1 typeset lines.

Note: House rule: no sentence opening with 'Because'.

### M28 (II-C, inter-observer DSC)

File: `main.tex` | Group: house

OLD:
```text
Because both annotators edited the same automatically
generated centerlines, the dataset authors describe
```

NEW:
```text
Both annotators edited the same automatically generated centerlines, so the dataset authors describe
```

Delta: -5 characters, about -0.1 typeset lines.

Note: House rule: no sentence opening with 'Because'.

## D. Supplement text

### S01 (Table S3 footnote)

File: `supplement.tex` | Group: required

OLD:
```text
Protocol D matches every territory flow, so its passes-and-wrong proportion equals its
materially wrong proportion.
```

NEW:
```text
Protocol D matches every territory flow in all but two models, so its passes-and-wrong and materially wrong proportions differ by at most one model.
```

Delta: +33 characters, about +0.3 typeset lines.

Note: Two discrete missed-branch D fits sit at the bound (residual 0.08 and 0.11; S2); one fails the 10% check (pass 103 of 104; 297 of 298).

### S02 (S7, second sentence)

File: `supplement.tex` | Group: house

OLD:
```text
Of the topological errors that
changed the decision, 91\%
```

NEW:
```text
Among the topological errors that changed the decision, 91\%
```

Delta: +3 characters, about +0.0 typeset lines.

Note: House rule: no sentence opening with 'Of'.

### S03 (S9 Noise Floors)

File: `supplement.tex` | Group: offset

OLD:
```text
 The repeat-measurement floor uses
the test--retest standard deviation of invasive FFR, 0.018 (5.0--6.5\% across cells).
```

NEW:
```text

```

Delta: -120 characters, about -1.0 typeset lines.

Note: Offset cut on supplement page 5 (full): the repeat floor is fully stated in II-F and the Table I footnote.

### S04 (S10, 3D-case flow and Reynolds number)

File: `supplement.tex` | Group: required

OLD:
```text
The finest mesh missed the strict residual limit (velocity residual $1.08\times10^{-5}$) with a steady inlet pressure. All 3D-to-0D
comparisons use a reduced-order counterpart rebuilt on the meshed radius.
```

NEW:
```text
The finest mesh missed the strict residual limit (velocity residual $1.08\times10^{-5}$) with a steady inlet pressure. The lesion carried about 10~mL/min (tree inflow 0.68~mL/s in 3D, 0.65--0.67~mL/s in the cohort model). At the meshed throat radius of 0.276~mm the mean velocity is about 0.7~m/s and the Reynolds number about 110, within the laminar regime.
```

Delta: +153 characters, about +1.3 typeset lines.

Note: Audit A.3: cohort-model inflow 0.649/0.672 mL/s, lesion flow 0.173/0.153 mL/s; 3D inflow 0.682 mL/s, lesion about 10--11 mL/min; U = 0.73 m/s, Re = 1060*0.73*0.552e-3/0.004 = 107. The dropped sentence repeats II-E. VERIFY in G7 from the pullback CSV and cfd_M1.

## E. Table S3 body (`supplement_tables/tab_thresholds.tex`): 'All' means T1--T4

### T01 (Table S3 row label)

File: `supplement_tables/tab_thresholds.tex` | Group: required

OLD:
```text
Discrete & All & A & 331 &
```

NEW:
```text
Discrete & T1--T4 & A & 331 &
```

Delta: +3 characters, 0 lines (table row).

Note: 'All' = T1--T4 only (n = 331 = 77+60+97+97; 518 = 118+100+150+150); the throat error is in Table S7.

### T02 (Table S3 row label)

File: `supplement_tables/tab_thresholds.tex` | Group: required

OLD:
```text
Discrete & All & B & 331 &
```

NEW:
```text
Discrete & T1--T4 & B & 331 &
```

Delta: +3 characters, 0 lines (table row).

Note: 'All' = T1--T4 only (n = 331 = 77+60+97+97; 518 = 118+100+150+150); the throat error is in Table S7.

### T03 (Table S3 row label)

File: `supplement_tables/tab_thresholds.tex` | Group: required

OLD:
```text
Discrete & All & C & 298 &
```

NEW:
```text
Discrete & T1--T4 & C & 298 &
```

Delta: +3 characters, 0 lines (table row).

Note: 'All' = T1--T4 only (n = 331 = 77+60+97+97; 518 = 118+100+150+150); the throat error is in Table S7.

### T04 (Table S3 row label)

File: `supplement_tables/tab_thresholds.tex` | Group: required

OLD:
```text
Discrete & All & D & 298 &
```

NEW:
```text
Discrete & T1--T4 & D & 298 &
```

Delta: +3 characters, 0 lines (table row).

Note: 'All' = T1--T4 only (n = 331 = 77+60+97+97; 518 = 118+100+150+150); the throat error is in Table S7.

### T05 (Table S3 row label)

File: `supplement_tables/tab_thresholds.tex` | Group: required

OLD:
```text
Leaky & All & A & 518 &
```

NEW:
```text
Leaky & T1--T4 & A & 518 &
```

Delta: +3 characters, 0 lines (table row).

Note: 'All' = T1--T4 only (n = 331 = 77+60+97+97; 518 = 118+100+150+150); the throat error is in Table S7.

### T06 (Table S3 row label)

File: `supplement_tables/tab_thresholds.tex` | Group: required

OLD:
```text
Leaky & All & B & 518 &
```

NEW:
```text
Leaky & T1--T4 & B & 518 &
```

Delta: +3 characters, 0 lines (table row).

Note: 'All' = T1--T4 only (n = 331 = 77+60+97+97; 518 = 118+100+150+150); the throat error is in Table S7.

### T07 (Table S3 row label)

File: `supplement_tables/tab_thresholds.tex` | Group: required

OLD:
```text
Leaky & All & C & 471 &
```

NEW:
```text
Leaky & T1--T4 & C & 471 &
```

Delta: +3 characters, 0 lines (table row).

Note: 'All' = T1--T4 only (n = 331 = 77+60+97+97; 518 = 118+100+150+150); the throat error is in Table S7.

### T08 (Table S3 row label)

File: `supplement_tables/tab_thresholds.tex` | Group: required

OLD:
```text
Leaky & All & D & 471 &
```

NEW:
```text
Leaky & T1--T4 & D & 471 &
```

Delta: +3 characters, 0 lines (table row).

Note: 'All' = T1--T4 only (n = 331 = 77+60+97+97; 518 = 118+100+150+150); the throat error is in Table S7.

## Consistency after the pass

- "About a third" now names its basis everywhere (pooled topological 33/32%, T5 30/36%), with the per-type range 18--43%
  beside it in IV-A and the Conclusion (M14, M20).
- Topological flips after re-derivation or tuning: 5--19% (pooled B--D) in the abstract, IV-A and the Conclusion (M05,
  M15, M20); the per-type rates stay in Table I.
- Throat flips under tuning: "did not reduce" in the abstract, IV-A and the Conclusion; the rise with its McNemar result
  in III-A only (M05, M09, M15, M20), and the Methods declare the C-and-D-against-A contrasts (M07).
- The taper against the floor: III-A (M10), IV-A (M14), IV-C unchanged ("the taper up to 14%"), Conclusion "2--13%"
  (M20). The Table I footnote's "5.0--6.5% across cells" is unchanged.
- "tube-model" Dice: abstract (M06), III-C per-tree against whole-scan (M13), IV-B (already "In our tube model"),
  Conclusion (M21). Fig. 4's caption already says "over the whole scan".
- clDice: III-C "clDice fell only for topological errors" and IV-B (M16) agree; Table S9 unchanged.
- "Fewest flips among Protocols A--C" (M11) matches Table I (D gives fewer in the discrete bed).
- III-B "flip counts changed by at most five per cell" (M12) matches S6 verbatim.
- Table S3: "T1--T4" rows (T01--T08) and the "all but two models" footnote (S01) match S2 (two D fits at the bound,
  residual 0.08 and 0.11) and the pass counts 103/104 and 297/298.
- Three "Because" openings and one "Of" opening in the existing text are removed by M08, M27, M28 and S02; no NEW
  sentence opens with "Of" or "Because", none exceeds 40 words, none says "post hoc", and no cross-reference is added
  (M13 moves the existing Fig. 4 reference within its sentence).
