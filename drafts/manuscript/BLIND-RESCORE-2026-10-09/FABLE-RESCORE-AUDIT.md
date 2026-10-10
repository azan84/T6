# Fable audit of the blind re-score and the fix plan (2026-10-09, evening)

Scope: the five re-score reports and SCORES.md, the current `main.tex` (9 pp) and `supplement.tex` (6 pp), today's FIX-LOG, FABLE-PLAN-AUDIT §9, the noise-model and ablation code, the T5 run, the ×2/×3 demand cohorts, and the result CSVs. Deadline 2026-10-15; today is 10-09. Nothing in the project was modified; all computation was done in the session scratchpad (`scratchpad/pilot_noise/`).

Three things were computed that the reports and the plan did not have:

1. **A scratch pilot of the matched-noise rerun** (plan item 1): 12 instances spread over the six bands, both beds, 5 of the 20 recorded noisy draws each, Protocols A–D, T1–T4 plus an identity "no error" type as the floor. The identity type under Protocol C reproduces the recorded a7 floor draws to 2e-7 in ΔFFR and 4e-9 in residual, so the pairing design is exact. Runtime 228 s for 144 instance-bed-draw tasks on 4 workers.
2. **McNemar tests of the throat error, Protocol A against C and D**, which the T5 run did not include.
3. **The flow through the 3D-case lesion and its throat Reynolds number**, from the frozen pullback and the CFD CSV.

---

## 0. Summary (10 lines)

1. #1 noise asymmetry: VALID; the pilot shows the rerun is exact and cheap, but it also exposes a missing Protocol D floor (correct anatomy tuned per territory to noisy targets is wrong by > 0.05 in about 7–15% of draws).
2. #2 flow regime: VALID in substance (the 3D-case lesion carries about 10 mL/min, half what R2 estimated); T5 at ×2/×3 is the right cheap answer; the discrete ×2 non-replication is a power issue (n = 47), direction holds.
3. #3 magnitude-set ranking: VALID that the abstract lost "for the magnitudes studied"; the dose response stays deferred (existing data give rho 0.03 discrete, 0.24 leaky; not usable).
4. #4 3D throat/Re/steadiness: VALID but deferred; the throat Re is about 110, so one sentence answers the steadiness objection now.
5. #5 tuning as practised: PARTLY. Main-branch territory assignment is not an oracle; the finer-level 100%-mismatch convention is, and needs one limitation sentence. R2's bound-fit expectation is wrong in direction (half-voxel D: at most 6 points either way).
6. #6 Dice: PARTLY. "As high as a taper" is a property of the chosen T4 magnitude; clDice does separate the classes; label "tube-model" and fix the IV-B sentence; voxel Dice deferred.
7. #7 wording: VALID on all six plus "about a third"; tuning raised discrete throat flips (McNemar 15 and 19 created, 0 reversed, p < 1e-4).
8. #8 format: VALID and one item is a hard rule: JBHI's limit is 14 pages including supplementary material; 9 + 6 = 15. Supplement page 6 is 85% empty and main page 9 is half empty, so this is layout, not content.
9. R2's Protocol B oracle: PARTLY (true of the design, not of the passes-and-wrong claim); one limitation sentence; the microvascular-variation arm stays deferred.
10. Plan items 1–2 are feasible (about 5.5 h compute on 4 workers, 2.5 working days in all) but item 1 must add the D floor and must sit beside, not replace, the noise-free run.

---

## A. Validity of the convergent issues and the seats' major weaknesses

### A.1 Convergent issues (SCORES.md #1–#8)

| # | Issue | Verdict | Evidence and notes |
|---|---|---|---|
| 1 | Noise asymmetry (error models tuned to noise-free targets; floor and detector negatives tuned to noisy ones) | **VALID** | `ablation.py` builds Protocol C/D targets from `q0_all` (the nominal clean flows, `protocol_c_targets`); `negatives.py` draws CO, MAP, viscosity, territory share (SD 0.10) and measurement noise (CV 0.083) on the truth side. The abstract's "against 3–4%" and III-C's "AUC 0.77 against 0.22" compare the two conditions. S8 already holds the matched AUCs (0.82/0.56). The pilot (§B.1) shows what matching does: under C the topological contrast barely moves; under D everything rises, including correct anatomy. |
| 2 | Flow regime too low; T5 not tested at higher demand; discrete topological excess does not replicate at ×2 | **VALID / PARTLY** | Low flow: valid, and larger than R2 states (§A.3). T5 at ×2/×3: valid, not run (Table S5 has no T5). "Does not replicate": PARTLY. At ×2 the discrete direction holds (topological passes-and-wrong B 6%, C 14%, D 20%, Table S5) but n = 47 instances gives about 4 net discordant pairs, so the McNemar test cannot reach significance; the text says so ("not significant in any topological comparison"). The abstract does not claim the excess, only the rates. |
| 3 | Ranking is magnitude-set; abstract lost "for the magnitudes studied" | **VALID** | The abstract (249 words) has "In this threshold-stratified cohort" but no magnitude qualifier; FIX-LOG A3 added one, and a later word-count pass removed it. IV-A keeps "These rates hold for the magnitudes studied." II-C says T1 and T2 "are design choices". Dose response: deferred, correctly (§C.2). |
| 4 | No 3D throat check; no Reynolds number; steadiness not shown | **VALID (deferred)** | Only T1 was solved in 3D. The throat Re is about 110 (§A.3), which justifies steady laminar flow in one sentence and answers DA C5. The T5 3D solve stays a revision item. |
| 5 | Tuning not as practised (oracle territories, wide bounds, bound fits kept); abstract leads with 19–20% | **PARTLY** | (a) Territories: at main-branch level the partition is the children of the first bifurcation, which every error type leaves intact (T1 deletes a branch beyond the lesion; T2 truncates the host vessel distally), so a corrupted tree's own partition gives the same node assignment; no oracle. At the finer level the 100%-mismatch rule for a territory with no surviving vessel does use knowledge that the territory exists; S6 shows it is decisive (26% without it). This needs one limitation sentence; DA C3 is right for the finer result only. (b) Bounds: ±1.5 decades (C) and 10^±3 (D) are wide. For the half-voxel variant 20 of 194 discrete D fits sit at the bound, all narrowed-throat; 8 fail the check and 12 are passes-and-wrong. Excluding them gives 83%; scoring them as failed QC gives 74%, against 80% reported. R2's expectation that physiological bounds would "reduce throat passes-and-wrong materially" is not supported for this variant (the supplement's "up to 13 points" is the ±10-point variant, 41 bound fits). (c) Prominence: the abstract already carries "With finer territories, topological concealment fell to 2–7%"; the Conclusion does not. Plan item 4 covers it. |
| 6 | Dice: tube vs voxel; T4 DSC partly circular; clDice separates the classes | **PARTLY** | Tube vs voxel: the figure caption and III-C say "tube-model"; the abstract and Conclusion do not, and the 0.928 line is a voxel-mask statistic, so the scale mismatch is real but declared where it is plotted. Circularity: T4's λ = 0.930 was set so that two coaxial cylinders give DSC 0.928; its tree DSC (0.971) follows from that choice and the 40% volume share, and T1's (0.975) from the deleted branch's share (median 4.9% of volume). The equality "0.97, as high as a taper" is therefore a coincidence of two design choices, not an empirical finding; the supported claim is that DSC does not rank these errors by decision risk (AUC within topological errors 0.54/0.70; 91%/62% of flipping topological models keep DSC ≥ 0.928). clDice: Table S9 gives 1.000 for T3/T4 and 0.93–0.94 (T1), 0.85 (T2), so clDice does separate the classes. The IV-B sentence "Overlap scores, including the topology-aware clDice, therefore did not rank these errors by decision risk" overreaches unless T5 (clDice 1.0, flips 30–36%) is named as the reason, and T5 is not in Table S9. |
| 7 | Six wording items plus "about a third" | **VALID (all)** | See §A.2 for each, with the numbers. |
| 8 | Format: LOGO, no funding/COI, 15 pp | **VALID; one hard rule** | Page 1 of `main.pdf` shows the template's "LOGO" placeholder (`logo.eps` from `IEEE-TJ-color-latex-template`). No funding or competing-interests statement. The JBHI guide: "PAGE LIMIT. The page limit is 14 pages for regular papers ... including supplementary material. The page limit must be implemented in both original submissions and revised papers." Main 9 + supplement 6 = 15. Supplement page 6 holds S10's 12 lines and a 3-row table (about 85% free); main page 9 holds half a column of references. |

### A.2 The seven wording items, checked

| Item | Text now | Data | Verdict and replacement |
|---|---|---|---|
| "tuning left its flip rate at 37–40%" (III-A); "left throat flips unchanged" (IV-A); "but not throat flips" (abstract); "left throat errors unchanged" (Conclusion) | Table I T5: discrete A,B 30 → C 38 → D 40; leaky 36 → 37 → 38 | McNemar (computed, half-voxel both signs): discrete A→C 15 created, 0 reversed, p = 1e-4 (n = 193); A→D 19 vs 0, p < 1e-4 (n = 194); leaky A→C 5 vs 1, p = 0.22; A→D 6 vs 0, p = 0.031 | VALID. "Tuning did not reduce throat flips; in the discrete bed it raised them (30% to 38–40%, McNemar p < 0.001)". Abstract: "but did not reduce throat flips". This strengthens the paper's message. |
| taper "of the order of" the 5.0–6.5% floor | T4 A discrete 13 (8–22), D 14 (9–23); leaky A 9 (6–15) | Lower Wilson bounds 8 and 9 exceed 6.5 in the discrete bed; the leaky bound (6) sits inside the floor | VALID. "Only the taper exceeded the floor, in the discrete bed (13–14%)". |
| finer territories: "flip rates were unchanged" (III-B) | S6: "Flip counts changed by at most five per cell" | — | VALID. Use the S6 wording. |
| Table S3 "All" | n = 331 = 77 + 60 + 97 + 97; 518 = 118 + 100 + 150 + 150 | T1–T4 only | VALID. Label "T1–T4". |
| Table S3 footnote "Protocol D matches every territory flow" | Pass 297 of 298; 103 of 104 | Two D fits at the bound (T1; residuals 0.08 and 0.11; S2), one above 10% | VALID. "all but two models". |
| 5–19 (abstract) vs 5–18 (Conclusion) vs 2–20 (IV-A) | Abstract = pooled B–D (B 14/5, C 19/8, D 8/6); Conclusion = B per type (9, 18, 5, 5); IV-A = B–D per type | All correct on their basis | VALID as an inconsistency. One basis; pooled B–D (5–19%) in abstract and Conclusion is the simplest. |
| "each changed about a third of decisions" (IV-A, Conclusion) | T1 27/18; T2 40/43; T5 30/36; pooled topological 33/32 | — | VALID. "topological errors, pooled, and the half-voxel throat error each changed about a third", or per-type ranges. |

Two more wording slips the seats found that the plan omits: DA C11, "Protocol B produced the fewest flips" (III-A) while D gives fewer in the discrete bed (T1 2% vs 9%; pooled 8% vs 14%): write "the fewest flips among Protocols A–C". DA C12, the repeated −0.0007: the cohort-model D value is −0.000695 and the 3D prescribed-flow value is 0.8916 − 0.8923 = −0.00068; a coincidence, confirmed, not a transcription error.

### A.3 Spot checks requested

**R2's "only about 20–30 mL/min through the 3D-case lesion".** The instance is scan 14, left tree, proximal LAD, 20 mm, 80% DS. From the frozen pullback (`ablation-2026-10-07_pullback.csv`): cohort-model tree inflow 0.649 mL/s (discrete) and 0.672 mL/s (leaky), i.e. 39–40 mL/min for the whole left tree; flow through the lesion 0.173 mL/s = 10.4 mL/min (discrete; leaky throat 0.153 mL/s = 9.2 mL/min); flow past the measurement point 0.078 mL/s = 4.7 mL/min. From `cfd_M1`: 3D baseline inflow 0.682 mL/s = 40.9 mL/min, 0.090 mL/s at the measurement node; the deleted branch carried about 0.08–0.10 mL/s, so the 3D lesion flow is also about 10–11 mL/min. **R2 overestimated by a factor of two; the physiological point is stronger than stated.** The inlet radius of this tree is about 1.07 mm (Q = 562 r³), against 1.85 mm for a normal LAD. Throat Reynolds number: Q = 0.174e-6 m³/s through the meshed throat (r = 0.276 mm) gives U = 0.73 m/s and Re = ρUD/μ = 1060 × 0.73 × 0.552e-3 / 0.004 ≈ 107 (about 120 on the reduced-order radius). Steady laminar flow is justified at this flow; one sentence in S10 says so and answers DA C5 and part of R1 W3, at the price of stating the flow explicitly, which the Limitations already concede in words.

**R2's "oracle advantage" of Protocol B.** The clean reference's bed obeys the scaling law exactly (C_b calibrated on the healthy-equivalent network, `t.ffr("murray")`), and Protocol B re-applies the same law to the corrupted tree (`t2.calibrate(t2.demand("murray", 1.0))`). So B is correct by construction except for the segmentation error, and the design has no physiological deviation that tuning could correct and B could not. **PARTLY valid.** It is a true statement about the design, and the paper should say it in Limitations (one sentence). It does not touch the passes-and-wrong rates under C and D, which are properties of the tuned model alone; it touches the B-versus-C/D contrasts and the reader's inference that re-derivation is safer. The matched-noise rerun does not answer it either: the noise perturbs the targets but ΔFFR is still measured against the nominal clean FFR, so no "true physiological deviation" exists in the model. The microvascular-variation arm stays deferred.

**R3's Dice circularity.** Verified as PARTLY (see #6): the T1-vs-T4 equality follows from the magnitude choices; the ranking claim stands; the clDice sentence overreaches.

**"Tuning raised throat flips (30% → 38–40%)".** Verified with McNemar (§A.2): significant in the discrete bed for both C and D; in the leaky bed significant for D only (p = 0.031).

**"Taper CIs exclude the floor".** Verified in the discrete bed (lower bounds 8 and 9 against 5.0–6.5); not in the leaky bed. The floor is a per-cell point value and the CI is descriptive (clustered), so the fair statement is descriptive, not inferential.

### A.4 Per-seat major weaknesses

| Seat | Item | Verdict | Note |
|---|---|---|---|
| EIC W1 | Noise asymmetry | VALID | = #1. |
| EIC W2 | Magnitudes not comparably grounded; abstract unconditional | PARTLY | Qualifier: valid, cheap. Sweep and taper recalibration: revision. Running segmentation networks on the test scans: revision (REVISION-PLAN item 1). |
| EIC W3 | Tube Dice vs voxel Dice; text cites tree median but Fig. 4 plots scan DSC | VALID (labelling) / deferred (voxel) | The text-vs-figure level mismatch (0.97 tree vs 0.985 scan) is a cheap fix: quote the plotted quantity or say "tree-level". |
| EIC W4 | Informatics contribution implicit | PARTLY | The detector (Table S10) and the four considerations are the contribution; the EIC wants a QC rule evaluated. One sentence placing calibration-vs-validation in a credibility workflow is cheap; a tested QC rule is not (R3 W5). Decline for 10-15. |
| EIC W5 | Protocol D check is vacuous; report D as residual error after exact calibration | VALID, cheap | The pilot makes this sharper: under noisy targets D passes everything and is wrong often, even for correct anatomy. Reword D as "wrong after exact matching" in III-B and the abstract. |
| R1 W1 | Sub-physiological demand; discrete concealment not replicated at ×2 | VALID / PARTLY | = #2. "Make a calibrated demand co-primary" is the revision's B3. |
| R1 W2 | Not like-for-like | VALID | = #1, with the right fix (paired excess over the matched draw). |
| R1 W3 | 3D: one instance, no T5, no Re | VALID (deferred) | = #4; the Re sentence now. |
| R2 W1 | Flow regime | VALID | = #2; §A.3 numbers. |
| R2 W2 | Protocol B oracle; tuning cannot correct physiology here | PARTLY | §A.3; limitation sentence now; arm deferred. |
| R2 W3 | Territories not as practised; RCA first bifurcation | PARTLY | Main-branch assignment is not an oracle; the RCA point is acknowledged in Limitations; the finer-level convention needs a sentence; Voronoi territories deferred. |
| R2 W4 | Bounds unphysiological; bound fits retained | PARTLY | Disclosed, and the direction R2 expects is not what the data show (§A.1 #5). A bounded-D sensitivity is a 10-minute run but needs a table; revision. |
| R2 W5 | Clinical framing of a 0.80 flip | PARTLY | The grey-zone table (S6) and the "not clinical prevalences" sentence answer most of it; reweighting to a CT-FFR distribution is declined (the cohort is stratified by design). One clause on CT-FFR-versus-invasive agreement (SD 0.07–0.10) would be fair but needs a reference check; optional. |
| R3 W1 | Synthetic, worst-case errors | PARTLY | Answered in Limitations ("design choices", "not measured"); the realistic-error arm is the revision's item 1. |
| R3 W2 | Tube Dice, circularity, clDice | PARTLY | = #6. |
| R3 W3 | Detector AUCs under unequal noise | VALID | Matched AUCs exist in S8; move them to the main text. An AUC of 0.22 must not be called "separation". |
| R3 W4 | Per-type statements overstate Table I | VALID | = #7. |
| R3 W5 | No QC rule tested | PARTLY | Decline for 10-15 (new analysis); note as revision B8. |
| DA C1 | Comparator not like-for-like | VALID | = #1. |
| DA C2 | Ranking of chosen magnitudes | PARTLY | Qualifier now; dose response deferred; "most needed" → "most consequential per occurrence at the magnitudes tested" is a cheap Conclusion fix. |
| DA C3 | Territory oracle | PARTLY | Finer level only (§A.1 #5). |
| DA C4 | 3D check does not test the throat | VALID (deferred) | = #4. |
| DA C5 | Flow regime in 3D asserted | VALID, cheap | Re ≈ 110 (§A.3). |
| DA C6 | Low demand; "one in five" without qualifiers | PARTLY | IV-A already says "held only in the discrete bed"; the Conclusion's "Up to one in five (discrete bed; 5–8% leaky)" carries the bed. Add "at the primary demand" there. |

---

## B. Feasibility and design of plan items 1 and 2

### B.1 Item 1: noise-matched rerun

**What to run.** The pilot wrapper (`scratchpad/pilot_noise/pilot_v2.py`) is the design: import the frozen `ablation.py` and `ablation_per_territory.py` unchanged; replace `ablation.protocol_c_targets` in memory so that each clean territory target is scaled by `terr_target_mls / terr_pred_start_mls` from the recorded draw in `results/a7_detector-2026-10-09/negatives_pretune.csv`; add an identity error type (the floor) to `ERROR_TYPES` with `CALIBRE_ONLY` so the clean node set is kept; loop draws 0–19 plus the nominal run (draw −1, ratio None) per instance and bed; Protocols A–D come from the two `run_instance` functions. T5 (half-voxel, both signs) runs the same way through `t5_throat_error_types.install()`. The model stays nominal; only the targets carry noise, exactly as in `negatives.py`. Each error model is then paired with the correct-anatomy draw of the same instance, bed and draw.

**Validation already done.** Identity under C with noisy targets reproduces the a7 draws (max |ΔFFR diff| 1.6e-7, residual 4e-9); the Protocol B residual reproduces `pretune_resid` (3.5e-9); the nominal run with ratio None is code-identical to the frozen run (the T5 wrapper's clean-FFR check gives 0.0 against the frozen CSVs, and the same check applies here).

**Runtime (measured).** 144 tasks (instance × bed × draw, five types A–D) in 228 s on 4 workers = 1.6 s per task. Full run: 150 × 2 × 21 = 6 300 tasks ≈ 2.8 h. T5 half-voxel: the T5 run took 1 163 s for 300 tasks with four variants on 4 workers; two variants over 6 300 tasks ≈ 2.5–3 h. Total about 5.5 h on 4 workers (the machine has 8 logical cores, 4 performance; 6 workers may give 4 h). Engineering 3–4 h (T5 integration, per-draw output, summary with paired excess and a patient-level cluster bootstrap), analysis and one supplement table 3 h, text 3 h, number check 2 h. **About 2.5 working days including an overnight run**, not 1 day; feasible if started 10-10 morning with integration on 10-12.

**What the pilot says about the headline (12 instances × 5 draws, both beds; rates in % of models).**

| Class, protocol | Discrete, noise-free | Discrete, matched | Discrete floor, matched | Leaky, noise-free | Leaky, matched | Leaky floor, matched |
|---|---|---|---|---|---|---|
| Topological, C | 22.7 | 24.5 | 3.3 | 9.1 | 7.3 | 0.0 |
| Topological, D | 27.3 | 42.7 | 15.0 | 0.0 | 10.9 | 6.7 |
| Caliber (T3+T4), C | 0.0 | 4.2 | 3.3 | 0.0 | 1.7 | 0.0 |
| Caliber, D | 16.7 | 28.3 | 15.0 | 0.0 | 10.8 | 6.7 |

(The floor's C values match the paper's 3.1%/3.9% in kind; 12 instances is too few for the leaky floor.) Three consequences:

- Under **Protocol C the contrast survives**: topological passes-and-wrong changes little when the targets carry noise, and sits well above the C floor in the discrete bed and near it in the leaky bed, which is what the paper already says ("held only in the discrete bed").
- Under **Protocol D the comparison changes form**. Exact per-territory matching to noisy targets pushes FFR by more than 0.05 in about 15% (discrete) and 7% (leaky) of correct-anatomy draws. **The paper has no Protocol D floor** (Table S11 tunes "as in Protocol C"), so the abstract's D figures (20% topological, 81% throat, 18% caliber) are currently compared with a floor from a different protocol. The rerun must include the D floor or the D numbers remain unmatched.
- Flip rates under matched noise rise by about 5 points under C and D for every class, including correct anatomy (the simulated floor's 6–7%).

**Replace or sit beside?** Beside. The noise-free run isolates the segmentation error and is the upper bound the methodology seat asks to keep; the matched run gives the like-for-like contrast and the paired excess. Concretely: Table I stays; one supplement table gives, per bed, class and protocol, the matched passes-and-wrong of error models, the matched floor, and the paired excess with a cluster-bootstrap interval; the abstract's "against 3–4% for correct anatomy" is restated on the matched basis for Protocol C (and the D sentence reworded per EIC W5 as "wrong after exact matching, against X% for correct anatomy"); III-C and IV-C quote the matched AUCs (0.82/0.56) with the noise-free ones in parentheses or dropped.

**Risks.** (i) The D story needs rewriting within three days; the D floor is a new result that the seats will read as important (and it supports the calibration-vs-validation message, since exact matching to a noisy measurement itself produces wrong FFRs). (ii) The leaky-bed topological excess may disappear on the matched basis; honest, and consistent with the present text. (iii) New numbers create new inconsistencies (today's experience); a full recomputation pass is mandatory after integration. (iv) Compute is on the critical path; start it before the wording pass.

**Drop rule.** If the full run is not validated (nominal run identical to frozen; identity run identical to a7) by 10-11 evening, fall back to the wording fix: delete "and correct anatomy in 3–4%" from the abstract and "against 3–4% for correct anatomy" from the Conclusion, keep the III-B comparison with the Limitations sentence, and move the matched AUCs into III-C.

### B.2 Item 2: T5 on the ×2 and ×3 cohorts

**Compatibility.** The reselected cohorts (`demand-replication-x{2,3}-2026-10-08/sweep_test_selected.csv`) have the same columns as `COHORT-FROZEN-2026-09-18.csv` (scan, side, vessel, loc, c_mm, L_mm, ds_pct, band, ...), which `t5_throat_run.run_all` consumes. Three things must change in a wrapper, not in the frozen files: set `zerod_ffr.K_MURRAY = 562 × scale` and `ablation.K_MURRAY` before any tree is loaded (as `demand_replication.py` and `ablation_per_territory.py --kscale` do); point `COHORT`, `OUT`, `FROZEN_ABL` and `FROZEN_PER` at the replication folder (the clean-FFR check then validates against that folder's `ablation.csv` and `ablation-perterritory.csv`); point the summariser's `ELIG` at that folder's `discrete_arm_eligibility.csv` (47 eligible at ×2; 17 at ×3, so the discrete arm is reported at ×2 only, as Table S5 does). The `PARTS` cache path must be per scale or cleared.

**Runtime.** 1 163 s per demand level on 4 workers for all four variants; about 40 min for ×2 and ×3 together. Engineering 2 h, summary and a row block in Table S7 (or Table S5) 1 h, one sentence in III-D. About 4 h in all; the coordinator's estimate is right.

**What it will show.** Unknown in direction: the reselected cohorts near 0.80 have milder lesions (a smaller relative throat change for ±0.088 mm) but the pressure drop scales with Q², so the sensitivity per radius change rises. Either outcome is reportable; a fall in T5 flips at higher demand would qualify "as often as topological errors" at the primary demand, which the abstract states. The ×3 leaky result is the one R2 asked for.

---

## C. Completeness and priority of the plan

### C.1 Missing items that are cheap and raise scores (or remove a formal fault)

| Missing item | Why it matters | Cost |
|---|---|---|
| **14-page limit including the supplement** (EIC W11c; a stated rule) | 9 + 6 = 15 now, and items 1–2 add about 25 supplement lines. Either main 8 + supplement 6, or main 9 + supplement 5. Page 6 of the supplement is 85% free and page 9 of the main is half a column of references, so one of: fold Table S12 into the S10 text and tighten Fig. S1's box heights (saves about 1/3 page); or move Fig. 4 (overlap) to the supplement and cut the main to 8 pp (saves $250 and absorbs the new material). Operator decision. | 1–2 h |
| Protocol D floor (found by the pilot) | Without it the matched D comparison is impossible and the current D figures have no like-for-like floor. Comes free inside item 1 (identity type under D). | 0 h extra |
| McNemar numbers for T5 A against C and D | They turn "did not reduce" into a tested statement (computed above). | 0 h |
| 3D-case flow and throat Re in S10 | Answers R2 W1 ("report the actual numbers"), DA C5, part of R1 W3, in two sentences. | 0.5 h |
| Limitation sentences: (a) the clean reference obeys the bed rule, so re-derivation carries no physiological error; (b) the finer-territory check assumes a missing territory is known to exist (100% mismatch). | R2 W2, DA C3; the two "unanswered" majors that need no data. | 0.5 h |
| "fewest flips among Protocols A–C" (DA C11); "tube-model Dice" in abstract and Conclusion; clDice sentence; Fig. 4 level (tree vs scan) | Cheap consistency; S5 and S3. | 0.5 h |
| Funding and competing-interests statements; LOGO decision | EIC W11a–b. The logo is the template's own placeholder, replaced at production; remove it for a clean first page. | 15 min (operator fact) |
| Conclusion: "at the primary demand" after "one in five"; "most consequential per occurrence at the magnitudes tested" | DA C2, C6. | 10 min |
| Matched AUCs (0.82/0.56) in III-C and IV-C | Already computed (S8); R3 W3, EIC W1. | 15 min |

### C.2 Deferrals

| Deferred item | Verdict | Reason |
|---|---|---|
| T1/T2 dose response | **Defer, confirmed** | From existing data, ΔFFR_A against flow lost gives Spearman rho 0.03 (p = 0.77) in the discrete bed (flip rate by tertile 35/8/38%) and 0.24 (p = 0.01) in the leaky bed (5/18/31%). Across-instance correlation is not a dose response (baseline proximity to 0.80 dominates); a within-instance graded deletion is needed. Not worth a sentence now; it would invite the question it cannot answer. |
| 3D throat check, Re, steadiness | **Defer the solve; state Re now** | Re ≈ 110 removes the steadiness objection; the T5 3D solve is CFD-machine work (B1 in the revision plan). |
| Tuning as practised (Voronoi territories, bounds, microvascular variation) | **Defer, with the two limitation sentences now** | The bound sensitivity is a 10-minute run but a table and text; the half-voxel effect is ≤ 6 points, so nothing in the headline hinges on it. The microvascular arm changes the design. |
| Voxel-mask Dice | **Defer; label now** | Rasterising 1 500 corrupted trees at native spacing and recomputing DSC/clDice is a day with uncertain gain; "tube-model" in the abstract and Conclusion is the honest fix. |

### C.3 Priority

The plan's order (1, 2, 3, 4) is right for the science but wrong for the calendar: item 1's compute is the critical path and should start first; the wording pass (3, 4) and the format fix should run while it computes; item 2 fits in the same afternoon. The 14-page rule is missing and must be first, because it decides where the new material can go.

---

## D. Why the score barely moved (6.4 → 6.5) against the 6.9 projection

**Where the projection failed.** The morning projection assumed S3 +1.0, S5 +0.7, S7 +0.6 and S8 +1.4. Actual: S3 +0.2, S5 +0.2, S7 0, S8 +2.4. S8 overshot because a concrete artefact (a public repository with a URL) exists that every seat could point to. S3 and S5 undershot because the seats re-anchor on the strongest remaining substantive objection in the abstract, not on the wording improvements; every seat scored S2 and S3 at 6 and named the same two or three majors (noise asymmetry, magnitudes, demand). Wording buys at most +0.2 from a simulated seat. S7 did not move because the detector result is modest (AUC 0.77/0.22 reads as a negative result) and the EIC seat went down one (6 → 5) while the DA went up one (6 → 7) on the same text. S6 fell 0.4 because the integration added a figure, a results subsection and about 15 ranges to the abstract.

**Implication for the remaining work.** The dimensions that can still move are S2 and S3 (a matched comparison is an artefact a seat can cite), S5 (only if the number pass is clean) and S7 (format compliance, informatics sentence). S4 is capped near 6 by the demand and magnitude choices, which are deferred; the clinical seat's "block" will stand until B3. S1, S6 and S8 are at their ceiling for this submission.

**Simulated-panel variance.** The same text received opposite one-point moves on S7 from two seats, and two seats dropped S6 by one for density that the other three did not score. Five seats × eight dimensions at integer resolution give an overall standard error of roughly ±0.2–0.3 for an unchanged paper. A +0.1 move is noise; the +2.4 on S8 is the only signal in today's re-score.

**Churn risk.** Today's integration produced the six wording inconsistencies and the two-AUC problem that the afternoon seats then scored. Each further wording pass has a measurable chance of creating one new inconsistency (S5 −0.2) for no measurable S3 gain. The rule for the remaining days: make the substantive additions (items 1–2), run one full recomputation pass, then freeze; do not re-score for the score's sake.

**Realistic projection for the plan (items 1–4 plus the C.1 additions).** S2 6.0 → 6.4, S3 6.0 → 6.5, S4 6.2 → 6.3, S5 8.0 → 8.0 (±0.2), S6 6.6 → 6.5, S7 6.4 → 6.6 (format compliance), S8 8.0 → 8.0: **overall 6.7 (range 6.5–6.9)**. With the wording-only fallback for item 1: 6.6. The modal recommendation stays "major revision" from the clinical and DA seats whatever is done before 10-15; a "minor" from the methodology seat is plausible if item 1 lands with the paired excess. Real JBHI referees will weigh the hard page limit and the like-for-like contrast more than the panel mean; those two are what the go-list fixes.

---

## E. Final recommendation

### E.1 Ordered go-list to 10-15

| # | When | What | Fixes | Effort | Drop rule |
|---|---|---|---|---|---|
| G1 | 10-10 am | **Launch item 1** (matched-noise rerun as in `pilot_v2.py`: A–D, T1–T4 + identity floor, then T5 half-voxel; 20 recorded draws + nominal; 4–6 workers). Validate first on 6 instances: nominal = frozen (0.0), identity-C = a7 (< 1e-6). | #1; EIC W1, R1 W2, R3 W3, DA C1; D floor | 3 h code + 5.5 h compute | Not validated by 10-11 evening → wording fallback (B.1). |
| G2 | 10-10 am | **Page budget decision** (operator): main 8 + supplement 6, or main 9 + supplement 5. Then fold Table S12 into the S10 text and tighten Fig. S1; or move Fig. 4 to the supplement. Remove the LOGO placeholder; add funding and competing-interests statements. | #8; EIC W11 (hard rule) | 1–2 h | None. |
| G3 | 10-10 pm | **Wording pass** with exact replacements: throat flips (with McNemar), taper floor, "at most five per cell", "about a third" → pooled/per-type, one basis for 5–19%, Table S3 "T1–T4" and "all but two", "fewest among A–C", "tube-model Dice" (abstract, Conclusion), clDice sentence ("clDice separated topological from caliber errors but is blind to the throat"), Fig. 4 level, abstract "for the error magnitudes studied" (+5 words; cut "(distributed-outflow)" and one range), Conclusion pairs "one in five" with the finer 2–7% and "at the primary demand", "most consequential per occurrence at the magnitudes tested", matched AUCs in III-C and IV-C, two limitation sentences (bed-rule reference; finer-territory convention), 3D-case flow (10 mL/min through the lesion; 40 mL/min tree inflow) and Re ≈ 110 in S10. | #3, #5, #6, #7; EIC W3, W5, W7; R2 W2, DA C2, C3, C5, C11 | 3 h | None. |
| G4 | 10-10 pm / 10-11 | **Item 2**: T5 at ×2 and ×3 through a wrapper that sets K_MURRAY and the cohort, eligibility and frozen-check paths; row block in Table S7 or S5; one sentence in III-D. | #2; R2 W1(c), R1 W1 | 4 h | If the clean-FFR check against the ×2 `ablation.csv` is not exact, stop and report the discrepancy instead. |
| G5 | 10-11 | **Analyse item 1**: per bed, class and protocol, matched passes-and-wrong, matched floor (C and D), paired excess with a patient-level cluster bootstrap; one supplement table; abstract contrast restated on the matched basis for C; D sentence reworded as residual error after exact matching with its floor. | #1 | 4 h | — |
| G6 | 10-12 | Integrate G3–G5, rebuild, page count (14 incl. supplement), abstract ≤ 250, portal abstract and cover letter synced. | — | 4 h | — |
| G7 | 10-13 | **Full recomputation pass** of every printed number from the CSVs (the 203-row check, extended to the new tables); fix only what it finds. No re-score. | S5 | 1 day | — |
| G8 | 10-14 | Upload set rebuilt (no comments in .tex/.bib), operator read, submit 10-15. | — | — | — |

Effort: about 2.5 working days of analysis and writing plus one day of checking, inside the five available; G1 and G4 compute overnight 10-10/10-11.

### E.2 Defer to the revision (keep in REVISION-PLAN-POST-SUBMISSION, in this order)

1. Physiologically calibrated demand co-primary (radius correction or k to total flow) with cohort reselection (R1 W1, R2 W1, DA C6).
2. T5 3D solves on the existing instance (± half voxel), transient check (R1 W3, DA C4).
3. Microvascular-variation arm and physiological tuning bounds; Voronoi territories (R2 W2–W4, DA C3).
4. Within-instance T1/T2 dose response (EIC W2, DA C2).
5. Real segmentation-failure frequency at lesion sites (EIC W2c, R3 W1).
6. Voxel-mask DSC and clDice with lesion-ROI metrics (EIC W3, R3 W2).
7. Tested QC rules (∂FFR/∂r × half voxel against |FFR − 0.80|; branch presence) and a V&V40 mapping table (EIC W4, R3 W5).
8. Cluster-bootstrap intervals and an MCMC refit including T5 and D (R1 W6, EIC W10).

### E.3 Decline (log the reason)

- Reweighting flip rates to a clinical CT-FFR distribution (R2 W5a): the cohort is threshold-stratified by design and says so; a reweighted number would be a second headline with its own assumptions.
- Cross-run of bed exponent and truncation (R1 W4, R2 W9): the two beds are presented as two models and claims require both; a third bed does not change the claim.
- Figure cosmetics (symlog axis, colormap, small multiples; R3 W7): proof stage or revision.
- Additional references beyond verification of those cited (R2 W10): the reference policy is quality over quantity; verify [21] Gosling and the Choy–Kassab relation for "flow proportional to mass" (EIC W6a, R2 W9), fix the sentence if the exponent is misquoted, add nothing else.
- A separate "n" column in Table I (EIC W8): the footnote carries it; the supplement's Table S3 has the denominators. Optional if space allows.

### E.4 Risks

1. **Item 1 changes the D story.** The D floor (about 7–15% in the pilot) is new; the abstract's D figures must be restated against it or confined to "wrong after exact matching". Mitigation: decide the D wording before the full run finishes (EIC W5 wording), so integration is mechanical.
2. **The leaky-bed topological contrast may vanish on the matched basis.** Already hedged in IV-A ("held only in the discrete bed"); carry the hedge into the abstract if it happens.
3. **New numbers, new inconsistencies.** G7 is non-negotiable; it is the only step that protects S5.
4. **Page limit.** Items 1–2 add about 25 supplement lines; without G2 the submission breaches a stated rule the EIC seat has already flagged.
5. **Compute on the critical path.** If the machine is shared with other runs (the a7 rerun took 76 min against 44 min for the same job), item 1 may need the full night; start it first.
6. **Score churn.** A re-score after G7 will move by ±0.3 for reasons unrelated to the changes; do not spend 10-13 on it.

---

## Appendix: numbers computed in this audit

- McNemar, T5 half-voxel (both signs as models), flips: discrete A→C n = 193, 58 → 73, created 15, reversed 0, p = 1.0e-4; A→D n = 194, 58 → 77, 19 vs 0, p < 1e-4; leaky A→C n = 299, 108 → 112, 5 vs 1, p = 0.22; A→D n = 300, 108 → 114, 6 vs 0, p = 0.031.
- Half-voxel Protocol D fits at the bound: discrete 20 of 194 (all narrowed-throat), 8 fail the check, 12 passes-and-wrong; leaky 3 of 300. Passes-and-wrong 80% reported; 83% excluding them; 74% scoring them as failed QC.
- 3D instance (scan 14, left, LAD prox, 20 mm, 80% DS): cohort-model inflow 0.649/0.672 mL/s (discrete/leaky) = 39–40 mL/min; lesion flow 0.173 mL/s = 10.4 mL/min (discrete), throat 0.153 mL/s (leaky); 3D inflow 0.682 mL/s, measurement-node flow 0.090 mL/s; throat Re ≈ 107 (meshed radius 0.276 mm, U 0.73 m/s), ≈ 120 on the 0D radius. Cohort-model D ΔFFR −0.000695; 3D prescribed-flow ΔFFR −0.00068.
- T1 dose response from existing data (Protocol A ΔFFR against flow lost): discrete n = 77, rho 0.03, p 0.77, flip by tertile 35/8/38%; leaky n = 118, rho 0.24, p 0.0096, flip by tertile 5/18/31%.
- Pilot v2 (12 instances across six bands, 5 draws, both beds): table in §B.1; validation against a7 max |ΔFFR diff| 1.63e-7, residual 4.1e-9, B pre-tuning residual 3.5e-9; 228 s on 4 workers for 144 tasks.
- Page fill: supplement page 6 has 44 text lines (page 5: 243); main page 9 has 83 lines of references (page 8: 116). Abstract 249 words.
- JBHI guide: "The page limit is 14 pages for regular papers and 16 pages for review papers including supplementary material. The page limit must be implemented in both original submissions and revised papers."
