# Independent verification of A5, A6, A7 and T5 (Fable, 2026-10-09)

Scope: plan §5 steps 1–4, plus a flag list. T5L2 had not landed at the time of writing (its report file still holds only the design section); §7 is reserved for it. No project file was modified. All recomputation was done with my own script (`/private/tmp/claude-501/fable_verify/recompute.py`, outputs `recompute*.out`) reading only the result CSVs; none of the agents' summary scripts was called.

Conventions used throughout, taken from `summarise_revision.py` and Table I: status `ok`; discrete arm restricted to the 97 eligible instances of `results/discrete_arm_eligibility.csv`; pass = residual < 0.10; wrong = |ΔFFR| > 0.05; P&W = both; flip at 0.80; Wilson 95% CIs; "beyond zone" = flip with corrupted FFR outside 0.75–0.85.

## 1. Recomputation from the CSVs

| Analysis | Cell | Report | Recomputed | Verdict |
|---|---|---|---|---|
| T5 | ±½ voxel pooled, A, discrete: flip / P&W | 30 (24–37) / 29 (23–36), n 194 | 30 (24–37) / 29 (23–36), n 194 | match |
| T5 | ±½ voxel pooled, A, leaky | 36 (31–42) / 42 (37–48), n 300 | 36 (31–42) / 42 (37–48), n 300 | match |
| T5 | ±10 %DS pooled, A, discrete | 40 (33–47) / 20 (15–26), n 194 | 40 (33–47) / 20 (15–26), n 194 | match |
| T5 | ±10 %DS pooled, A, leaky | 42 (37–48) / 40 (34–45), n 300 | 42 (37–48) / 40 (34–45), n 300 | match |
| T5 | ±10 %DS pooled, C, discrete (C cell) | 44 (37–52) / 51 (44–58), n 187 | 44 (37–52) / 51 (44–58), n 187 | match |
| T5 | ±½ voxel pooled, D, leaky (D cell) | 38 (33–44) / 81 (76–85), n 300 | 38 (33–44) / 81 (76–85), n 300 | match |
| T5 | all 48 remaining cells of the T5 table (flip, P&W, beyond zone, median \|ΔFFR\|) | — | all equal | match |
| T5 | sign test T1+T2 vs ½ voxel pooled, A: p | 1.0 (D), 0.46 (L) | 1.0 (34/33), 0.456 (40/48) | match |
| T5 | sign test T1+T2 vs ±10 pooled, A: p | 0.21 (D), 0.012 (L) | 0.207 (32/44), 0.012 (37/63) | match |
| T5 | B ≡ A | asserted | max \|FFR_A − FFR_B\| = 0.0 over every T5 model; B `C_ratio` = 1.0 exactly | confirmed |
| T5 | clean rows vs frozen | identical | 298 of 298, max diff 0.0 | match |
| T5 | spacing / s/4 / \|ΔDS\| | 0.352 (0.295–0.449) mm / 0.088 mm / 7.3 (4.5–9.8) pp | 0.352 (0.295–0.449) / 0.0879 / 7.3 (4.5–9.8) | match |
| T5 | insertions, clipping, realised DS | 2 384 / 0 / equal | 2 384 / 0 / max diff 1e-16 | match |
| A6 | topological P&W, discrete, C: L1 → L2 | 20/104 (19%) → 7/104 (7%), p = 0.0002 | 20 → 7, +0/−13, p = 0.00024 | match |
| A6 | topological P&W, discrete, D: L1 → L2 | 21/104 (20%) → 3/104 (3%), p < 0.0001 | 21 → 3, +0/−18, p = 7.6e-6 | match |
| A6 | the other six class cells (caliber, leaky) and all flip counts | as Table 3.2/3.3 | all equal | match |
| A6 | L1drop vs frozen | bit-identical | 3 728 rows, 0 status mismatches, max diff 0.0 (FFR, residual) | match |
| A5 | median tube DSC, discrete: T1 / T4 | 0.975 (0.947–0.984) / 0.971 (0.947–0.981) | 0.975 (0.947–0.984) / 0.971 (0.947–0.981) | match |
| A5 | paired T1 vs T4, discrete | +0.004, T1 lower in 29/77, Wilcoxon p = 0.027 | +0.0041, 29/77, p = 0.0274 | match |
| A5 | paired T1 vs T4, leaky | +0.000, 59/118, p = 0.59 | +0.0002, 59/118, p = 0.588 | match |
| A5 | decision-changing topological errors with whole-scan DSC ≥ 0.928 | 41/45 = 91% (79–96); 52/84 = 62% (51–72) | 41/45; 52/84 | match |
| A5 | AUC(−tree DSC, flip A), point estimates: pooled / topological | 0.65 / 0.54 (D); 0.79 / 0.70 (L) | 0.648 / 0.541; 0.789 / 0.702 | match |
| A7 | discrete B-residual AUC, topological vs noisy correct anatomy | 0.77, n 137 | 0.767, n 137 (median residual 0.196) | match |
| A7 | false-alarm rate at 0.10 under noise | 48% (D), 50% (L) | 47.5% (1 940 draws), 50.4% (3 000 draws) | match |
| A7 | 5% false-alarm thresholds; sensitivities | 0.22 / 0.23; 83%, 47% | 0.220 / 0.229; 83%, 47% | match |
| A7 | leaky AUC; flip-under-B AUC | 0.22; 0.57 (D), 0.21 (L) | 0.221; 0.571, 0.207 | match |

No mismatch was found in any headline number. Bootstrap CIs (A5, A7) were not re-drawn; only the point estimates were checked.

One basis discrepancy, not an error, is recorded in §3: the T5 report's bound-fit counts (11 C, 97 D) are over all rows, while every rate in its table is on the Table I basis, where the counts are 10 C and 64 D.

## 2. T5 implementation (`code/t5_throat_error_types.py`)

Confirmed by reading the code and by the CSV checks above:

1. **Only the throat severity changes.** A T5 error function returns `list(segs)` unchanged and registers a pending DS transform. The patched `insert` applies it to the next call only, then clears it. `insert` itself is the frozen cosine insertion with `ds_new` in place of `ds`; the center `c`, length `L`, path and window are those of the clean model. The realised throat DS equals the applied DS in all 2 384 insertions.
2. **Reference radii, bed and node set are unchanged.** The corrupted tree is `Tree(segs2, ...)` built from the unchanged segment list, so `r`, `r_fit`, `r_ref` and the bed weights `w` equal the clean tree's. The T5 names are appended to `ablation.CALIBRE_ONLY`, so `trunc_ref=t` pins the active node set to the clean tree, as for T3/T4. The lesion is applied as an `r_override` in `evaluate`, so it never reaches `r_ref` or `C_b` (main text II-B: "an inserted lesion changes only the epicardial radius"). The log columns `w_sum`, `r_ref_root_mm`, `n_outlets` were not re-checked by me, but the FFR identity below makes any difference impossible.
3. **Protocol B equals Protocol A by construction.** Under A the surviving nodes take `t.w` (all nodes survive, so `t2.w = t.w`) with `C_clean`; under B, `t2.calibrate` on the identical healthy-equivalent network returns the same `C_b`. Verified numerically: `C_ratio` of every B row is exactly 1.0 and max |FFR_A − FFR_B| = 0.0 over all 3 556 T5 models. Table I's T3 rows show the same identity (A = B) for the same reason; the T4 rows differ because the taper scales radii outside the override.
4. **Half-voxel computation.** Spacing = mean of the first two `header.get_zooms()` of the scan's label volume, i.e. the in-plane pixel size in mm, the same header the loader uses for the EDT sampling (`imagecasx_loader._edt`, `sampling=sp`). The radius change is `0.25 × spacing` (diameter ½ voxel) applied at the throat node (`argmin |s − c|`, the node `insert` uses), as a DS change `±(s/4)/r_fit(c)`. Because the throat weight is 1, the throat radius moves by exactly s/4 (median 0.088 mm; r_fit at the throat median 1.23 mm). Sign: `vox_narrow` raises DS (radius − s/4), `vox_wide` lowers it. Correct.
5. **Leak check.** `_PENDING` would persist if a T5 function ran and the following `insert` were skipped; in `run_instance` the only skips between the two are tree construction and the host-vessel and lesion-window checks, which cannot fire for an unchanged segment list, and the run script resets before every instance. The insertion count (4 types × 298 instance-beds × 2 run paths = 2 384) confirms exactly one T5 insertion per model and no leak into a clean insertion (clean rows bit-identical).

One wording point: the T5 report lists ±10 pp as primary and ½ voxel as secondary. D2 reverses this. All of its draft text leads with ±10 and must be re-led with ½ voxel.

## 3. Bound-fit handling

**Counts on the Table I basis (eligible discrete + leaky):** Protocol C failed fits 10 (discrete: 7 DS+10, 1 narrow; leaky: 1, 1); Protocol D fits at the 10³ bound 64 of 988 (discrete: 34 DS+10, 20 narrow; leaky: 7, 3). The report's "11" and "97 of 1 172" count ineligible discrete instances too. Use 10 and 64 in the supplement, or say "54 discrete-bed and 10 leaky-bed models"; "97" would be read as "all 97 instances".

**What the 64 D bound fits are.** All are more-severe variants on lesions of 65–80% DS (DS+10 pushes 70–80% lesions to 80–90%). 62 of 64 have a clean-positive FFR (median 0.68); every territory multiplier reached 10³ and the models' FFR has a median of 0.088 (min 0.056), i.e. the throat cannot pass the clean territory flow at any bed conductance. Residual: 43 of 64 ≥ 0.10 (fail), 21 < 0.10, and all 21 are materially wrong, so they count as P&W. Flips: 2, both also flips under A.

**Consistency with the stated rule.** Supplement S2 retains D fits at the bound "because their residuals remain defined and are scored against the check, whereas a Protocol C fit at a bound leaves its single parameter unidentified", and `ablation_per_territory.py` records `fit_at_bound` without changing status. The T5 run applied the frozen rule unchanged in both protocols, so the handling is consistent with the paper. The rationale holds: a D model at the bound is what a per-territory pipeline would actually report (a fit that saturated and a residual the check then scores); a C fit at the bound has no interpretable parameter at all.

**Is keeping them conservative?** For P&W, yes: the bound fits have a lower P&W rate (21/64 = 33%) than the rest, so they dilute the headline. Excluding them raises pooled D P&W from 80% to 83% (½ voxel) and from 75% to 88% (±10) in the discrete bed, and by ≤ 1 point in the leaky bed. For flips, keeping them is also conservative: they contribute 2 flips in 64, and excluding them raises the pooled D flip rate from 40% to 44% (½ voxel) and from 45% to 53% (±10) in the discrete bed, unchanged in the leaky bed. The claim "tuning did not reduce throat flips" (D ≥ A: 40 vs 30, 45 vs 40) holds either way. No headline changes direction or leaves its stated range (51–86% tuned P&W stays 51–88% at most).

**What must change in the text.** Main text II-D says of Protocol C "a fit at the edge of the range was a failure (none occurred)"; supplement S2 says "none did in the ablation" and that the D scaling "reached 10³ in two discrete-bed missed-branch models". Both must be updated with the T5 counts, and the S2 sentence that the two frozen bound fits kept |ΔFFR| < 0.05 must not be left implying the same for the T5 ones. Recommend a supplement sentence of the form: "Protocol D reached its bound in 54 discrete-bed and 10 leaky-bed throat-error models with an increased stenosis, all but two with a clean FFR at or below 0.80; 43 failed the check and the 21 that passed were materially wrong. Excluding them raises the tuned passes-and-wrong rates by 1–13 points." Also note for the operator: with the ½-voxel primary, 20 discrete and 3 leaky bound fits remain in the headline rows; the DS+10 variant, which produces 41 of the 64, moves to the supplement with D3.

## 4. Citation for ±10 %DS

Both references were verified verbatim from the Europe PMC record (abstract text), including volume, pages and DOI.

1. **Boogers MJ, Schuijf JD, Kitslaar PH, et al.** "Automated quantification of stenosis severity on 64-slice CT: a comparison with quantitative coronary angiography." *JACC: Cardiovascular Imaging*, 2010;3(7):699–709. doi:10.1016/j.jcmg.2010.01.010. PMID 20633847. Exact statistic (abstract): "Good correlations for diameter stenosis were observed for vessel-based (n = 282; r = 0.83; p < 0.01) and patient-based (n = 93; r = 0.86; p < 0.01) analyses. Mean differences between QCCTA and QCA were −3.0% ± 12.3% and −6.2% ± 12.4%." The standard deviation of the CT–QCA %DS difference is therefore about 12 percentage points per vessel.
2. **Gouya H, Varenne O, Trinquart L, et al.** "Coronary artery stenosis in high-risk patients: 64-section CT and coronary angiography—prospective study and analysis of discordance." *Radiology*, 2009;252(2):377–385. doi:10.1148/radiol.2522081271. PMID 19546426. Exact statistic (abstract): "Bland-Altman analysis showed poor agreement, especially for intermediate stenosis (mean bias, 1.3%; 95% limits of agreement: −27.3%, 29.9%)", i.e. a difference SD of about 14.6 points.

Checked and not usable as the statistic: Miller 2008 (CORE-64, NEJM 359:2324–2336) reports only "well correlated (r = 0.81)"; Arbab-Zadeh and Hoe 2011 (JACC CV Imaging 4:191–202) is a narrative review stating that "disagreement on individual coronary arterial stenosis severity is common" without a number in the abstract; the SCOT-HEART and CONFIRM core-lab papers grade categorically. No pure inter-observer CT %DS statistic with a verified number was found within the time available; the two references above are CT-versus-QCA disagreement, which the task accepted.

**Verdict.** ±10 points is supported: it is below one standard deviation of the published CT–QCA difference in percent diameter stenosis (12–15 points). Keep ±10 %DS as the secondary magnitude, cited as "within the published disagreement between CT and invasive angiography on percent diameter stenosis (difference SD 12–15 points) [Boogers 2010; Gouya 2009]". Per D3 its rows stay in the supplement; the main text may carry the ±10 range in one clause. Caveat to state: on 70–80% lesions, +10 points gives 80–90% DS, beyond the cohort's 40–80% range, and this variant carries 41 of the 64 D bound fits. That is a further reason the ½-voxel magnitude leads.

## 5. Flags on the four reports

### 5.1 Wrong or inconsistent

- **T5, bound-fit counts** (11 C, 97 D): all-rows basis, see §3. Supplement text must use 10 and 64 (or 54 + 10). The T5 draft paragraph says "Protocol D fits reached the parameter bound in 97 such models" and must change.
- **T5, "Primary magnitude ±10 pp"**: contradicts D2; re-lead all draft text with ½ voxel.
- **T5 draft main-text sentence** quotes the untuned P&W as part of the tuned range "51–86%"; correct, but the plan's "20–42% untuned" spans ±10 (20%) to ½ voxel (42%). On the ½-voxel primary the untuned range is 29–42% (A, both beds); use that in the main text and keep 20–40% (±10) for the supplement.
- **Main II-D and supplement S2** state that no Protocol C fit failed and that D reached its bound in two models; both false once T5 is included (§3).
- **A6, floor caveat**: the Level 2 rates (2–7%) are compared with a floor (3–4%) computed at Level 1 only. The A6 report says so; the main-text sentence and the abstract clause must not say "at the floor". "Fell to 3–7%, near the 3–4% of correct anatomy at main-branch level" is the defensible form.
- **A6, convention dependence**: the fall to 3–7% requires the 100%-mismatch rule; under the frozen drop rule it would be 26%. The supplement paragraph carries this (last sentence); keep it, a referee who reads the L2drop number without it will call the result convention-chosen.

### 5.2 Overclaim risk

- **"A perfusion match does not certify the lumen" now rests on throat errors**: supported (P&W 51–86% tuned, 29–42% untuned at ½ voxel), but a referee will note that a tuned throat-error model with FFR 0.3 is "wrong" in a way any reader of the FFR would see. Report the median |ΔFFR| alongside P&W (½ voxel, A: 0.11; flips: median |ΔFFR| 0.12, about half of flips beyond the grey zone: 28/58 discrete, 62/108 leaky) so the claim is "wrong by a clinically material amount", not "wrong by an absurd amount".
- **A5, "the same DSC"**: T1 is marginally *higher* than T4 in the discrete bed (p = 0.027). "The same median DSC (0.97)" is fine; "DSC ranks the missed branch as less damaged than the taper" is the stronger and still-true form. Do not write "lower".
- **A5, 0.928 comparison**: the 91%/62% figures compare a tube-model whole-scan DSC with a voxel-mask inter-observer DSC. Always label it tube-model and say the comparison is indicative; the draft supplement does. The A5 main-text draft drops `bransby2026` from IV-B; keep the observation about real segmentation outputs as a citation, since our breaks are visible to DSC (0.89, RCA 0.62) and the paper should not imply otherwise.
- **A7, "AUC 0.77" as a positive result**: at the 0.10 check it flags 48% of correct models; at 5% false alarm it catches 47%. The IV-C draft sentence states both. Do not describe the pre-tuning mismatch as a "screen" without the false-alarm rate, and keep "uninformative in the leaky bed" (AUC 0.22, i.e. noise exceeds the error signal).
- **A7, asymmetry**: positives use error-free targets, negatives noisy ones; the 0.82 noisy-target variant covers it. Mention in the supplement only.

### 5.3 Framing the half-voxel result

The risk: "a half-voxel throat error flips about a third of decisions" read as "CT-FFR near 0.80 is unreliable". Recommended framing elements, each backed by a number:

1. **Conditional on the cohort.** 30% (discrete) and 33% (leaky) of clean models lie inside 0.75–0.85 by design, and all lie in 0.65–0.95; the 30–36% is a flip rate in a threshold-stratified cohort, not a clinical misclassification rate. The paper already says this for Table I; say it again in the throat sentence.
2. **Known sensitivity, measured here in decision terms.** Computed FFR is known to be most sensitive to the minimal lumen: fernandez2024 [12] perturbed the segmentation threshold by ±6% (intra-) and ±15% (inter-operator) and found sensitivity rising with stenosis severity and recommended careful segmentation or invasive FFR when values approach 0.80; sankaran2015tmi [10] defines geometric sensitivity as the SD of the hemodynamic metric under lumen-segmentation uncertainty and shows it is concentrated in specific regions and depends on the downstream boundary conditions, which is exactly the coupling this paper tests; sankaran2015cmame [11] is the companion machine-learning estimate of that sensitivity. Frame the throat result as consistent with [10]–[12] and extending them to the decision at 0.80 and to tuned boundary conditions. (I verified the abstracts of [10] and [12]; [11]'s abstract was not retrievable, so cite it only for the method, not for a number.)
3. **The paper's own 3D case agrees**: a 0.045 mm throat offset moved the baseline FFR by 0.11 (IV-D); the ½-voxel radius change is 0.088 mm.
4. **The contribution is about the check, not the sensitivity**: the perfusion check sees none of it (P&W 29–42% before tuning) and tuning increases concealment (51–86%). That sentence keeps the reader on the paper's thesis.
5. **Scope statement for validated products**: one clause that the result concerns a segmentation error reaching the model unreviewed, and that clinical CT-FFR validation against invasive FFR [norgaard2014] is empirical and includes expert lumen review. This pre-empts "then why does FFR-CT work".
6. Avoid "a third of decisions" in the abstract; give the two numbers with the qualifier, e.g. "a half-voxel throat error changed 30–36% of decisions in this threshold-stratified cohort, as often as a missed branch or vessel break (p ≥ 0.46)".

### 5.4 Other referee-facing points

- **A ≡ B for T5** should be stated once as "by construction" (II-C); listing identical A and B rows in the supplement table is fine but note why.
- **Half a voxel is a sub-voxel error**: a one-voxel boundary error on one wall changes the diameter by a full voxel. State that ½ voxel is below the mask resolution and therefore a lower bound on the error an unreviewed segmentation can carry; this is why the magnitude cannot be called design-chosen.
- **Protocol D under a tight throat**: a referee may ask whether a 10³ bound is physiological. The answer is in §3: the fit saturates, the check fails two thirds of them, and the result is reported with and without them.
- **Headline numbers propagate**: cover letter, portal abstract and GitHub README (plan §8.2).

## 6. Verdicts in one line each

- Step 1: every checked number reproduces (T5, A6, A5, A7); no mismatch.
- Step 2: T5 changes only the throat DS; radii, bed, node set unchanged; B = A exactly; ½-voxel = s/4 in radius from the label-volume in-plane spacing, correctly signed.
- Step 3: bound-fit handling follows the paper's rule; keeping the D bound fits is conservative for both P&W and flips; counts must be stated on the Table I basis (10 C excluded, 64 D kept) and II-D/S2 updated.
- Step 4: ±10 %DS is supported by Boogers 2010 (CT–QCA %DS difference SD 12.3/12.4 points) and Gouya 2009 (95% LoA −27.3 to 29.9); keep as secondary, cited, in the supplement.

## 7. T5L2 verification (added after the report landed)

Recomputed with `/private/tmp/claude-501/fable_verify/recompute_t5l2.py` (output `recompute_t5l2.out`) from `results/t5l2-2026-10-09/*.csv`, Table I basis, pairing by `run_id` on models with status ok at both levels.

**(i) Level 1 reproduces the T5 run.** `ablation_t5_L1drop.csv` vs `t5_throat-2026-10-09/ablation_t5.csv`: 3 874 rows, 0 unmatched, 0 status differences, max |FFR| and |residual| difference 0.0, 0 flip or bound differences. `perterritory_t5_L1drop.csv` vs `perterritory_t5.csv`: 1 192 rows, all identical. Match.

**(ii) Level 2 cells.** A ≡ B at Level 2 (max |FFR| and |residual| difference 0.0); A-row FFR identical at both levels (only the residual moves); `n_empty` = 0 everywhere; Protocol C failed fits 7 (Level 2) vs 11 (Level 1), all rows. Paired Level 1 → Level 2, pooled:

| Bed | Variant | Prot. | n | P&W L1 → L2 | +new/−lost, p | P(wrong\|pass) L1 → L2 | Flips L1 → L2 | D bound L1 → L2 | P&W excl. bound L1 → L2 |
|---|---|---|---|---|---|---|---|---|---|
| Discrete | ½ voxel | A, B | 194 | 29 (23–36) → 25 (20–32) | 0/7, 0.016 | 62 → 59 | 30 → 30 | — | — |
| Discrete | ½ voxel | C | 193 | 57 (50–64) → 51 (44–58) | 1/12, 0.0034 | 78 → 76 | 38 → 37 | — | — |
| Discrete | ½ voxel | D | 194 | 80 (74–85) → 78 (71–83) | 1/6, 0.12 | 84 → 84 | 40 → 40 | 20 → 29 | 83 → 81 |
| Discrete | ±10 | A, B | 194 | 20 → 16 | 0/7, 0.016 | 65 → 60 | 40 → 40 | — | — |
| Discrete | ±10 | C | 186 | 51 → 45 | 0/11, 0.001 | 83 → 81 | 45 → 45 | — | — |
| Discrete | ±10 | D | 194 | 75 → 69 | 1/13, 0.0018 | 88 → 88 | 45 → 45 | 34 → 48 | 88 → 85 |
| Leaky | ½ voxel | A, B | 300 | 42 (37–48) → 35 (30–41) | 2/23, <0.001 | 67 → 63 | 36 → 36 | — | — |
| Leaky | ½ voxel | C | 299 | 69 (63–74) → 60 (55–66) | 1/26, <0.001 | 78 → 76 | 37 → 37 | — | — |
| Leaky | ½ voxel | D | 300 | 81 (76–85) → 81 (76–85) | 1/1, 1.0 | 81 → 82 | 38 → 39 | 3 → 8 | 81 → 81 |
| Leaky | ±10 | A, B | 300 | 40 → 33 | 1/20, <0.001 | 76 → 72 | 42 → 42 | — | — |
| Leaky | ±10 | C | 299 | 62 → 55 | 1/20, <0.001 | 83 → 81 | 43 → 43 | — | — |
| Leaky | ±10 | D | 300 | 86 → 83 | 0/8, 0.0078 | 87 → 87 | 44 → 44 | 7 → 22 | 87 → 86 |

All values equal the T5L2 report (§3.1–3.3 and the exclusion line in §3.4). The report's "DS ±10 pooled C" discrete n is 186 in my pairing and "186--193" in its table note; its §3 text says 89 + 97. Consistent. Flip changes: at most 2 models per cell (McNemar p ≥ 0.5). Match.

**(iii) Headline point 3 survives.** Pooled tuned P&W at Level 2 is 45–60% (C) and 69–83% (D), i.e. 45–83% against 51–86% at Level 1, and P(wrong | pass) after tuning is 76–88% against 3–29% for topological errors at the same level (A6 Level 2: 7/24, 3/74, 8/99, 4/126, recomputed). Every change was a lost pass, not a corrected FFR. So the headline reads: "tuning conceals throat errors at both territory resolutions; a finer check removes most topological but few throat or taper passes-and-wrong", which is the stronger form of plan §8.4, not its fallback.

**Bound fits, Table I basis.** Level 1: 64 of 988 ok D fits (discrete 54, leaky 10; DS+10 41, narrow 23); 21 pass and all 21 are P&W; 2 flips. Level 2: 107 of 988 (discrete 77, leaky 30; DS+10 70, narrow 37); 43 pass, all P&W; 6 flips. All-rows counts 97 → 153 as reported. The coordinator's "64 → 107" is confirmed. Keeping them remains conservative at Level 2: excluding them raises D P&W by 0–3 points and flips by at most 1 point.

**Territories.** Level 2 median 4 (2–5) discrete, 5 (2–7) leaky over the T5 instances. Match.

**Flags on the T5L2 report.** (a) Its draft main-text sentence quotes "45--60\% ... 69--83\%" pooled over both magnitudes; with ½ voxel primary the main text should quote 51–60% (C) and 78–81% (D) and leave the ±10 figures to the supplement. (b) Its supplement paragraph says "Protocol D fits on the parameter bound rose from 54 to 77 ... and from 10 to 30": these are Table I-basis counts and are right; the T5 report's "97" must not appear beside them. (c) "81--86\%" for D excluding bound fits: recomputed 81–86 (81, 85, 81, 86). Correct.
