# Paper 6: plan to integrate A5, A6, A7 and T5 (2026-10-09)

Inputs:
- the reports `analyses/A5-REPORT.md`, `A6-REPORT.md`, `A7-REPORT.md` and `T5-REPORT.md`;
- `T5L2-REPORT.md`, pending: the throat error under the finer territories.

Constraints:
- **Main text:** 8 pp, the fee threshold. About 3 lines are free now.
- **Abstract:** 250 words.
- **Supplement:** keep main + supplement at about 14–15 pp. Two published JBHI papers exceed 14.
- **Deadline:** 10-15.

## 1. The paper after the new evidence

**Current headline:** "Topological errors flip 3–6× as often as caliber errors; tuning hides them; check the branching and record the mismatch before tuning."

**Problems with it:**
- Five of five blind reviewers called the ranking design-set.
- The devil's advocate attributed the concealment to the coarse check.
- The informatics claims (overlap scores, pre-tuning mismatch) were not measured.

**Headline the evidence now supports:**
1. **Where the risk lies.** Decision-changing segmentation errors sit in the branching and at the stenosis throat.
   - With fixed BCs, a missed branch or a vessel break changes 32–33% of decisions.
   - A throat-diameter error of half a voxel changes 30–36%, and ±10 %DS changes 40–42%.
   - Caliber errors of inter-observer size away from the throat change 6–10%, near repeat-measurement rates.
2. **What the checks see.**
   - Overlap scores do not rank these errors by decision risk: a missed branch and a taper have the same DSC (0.97).
   - A main-branch perfusion check does not see throat errors at all. 20–42% of throat-error models pass it while wrong even before tuning.
3. **What tuning does.**
   - Tuning to perfusion increases the throat-error concealment, to 51–86%. [Confirm at the finer level: T5L2 pending.]
   - It conceals topological errors only when the check is coarse: 19–20% at main-branch level, 3–7% one level finer.
4. **What follows for practice.**
   - Check branching and throat caliber directly, not through overlap scores or through perfusion agreement.
   - The pre-tuning mismatch is a weak screen: AUC 0.77 in the discrete bed with a 48% false-alarm rate at 0.10; uninformative in the leaky bed.

**Why this is stronger:**
- **(a) The asymmetry is gone.** The study now tests the caliber error at the throat, the one clinicians care about, and the critique raised by all five reviewers disappears.
- **(b) The weakest claims are now measured.** The two unmeasured informatics claims and the coarse-check objection are all measured. Two of the results qualify old claims, and qualified claims backed by numbers survive review better than unqualified ones.
- **(c) The central message survives and broadens.** "A perfusion match does not certify the segmented lumen" now rests on throat errors as well as branching errors.
- **(d) The paper now has a concrete informatics result for JBHI.** The quality metrics people actually use, DSC, clDice and the pre-tuning mismatch, are quantified against decision risk.

## 2. Decisions needed (recommendation first)

| # | Decision | Recommendation | Reason |
|---|---|---|---|
| D1 | Title | "Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study" (drop "Topological") | The results now cover the branching and the throat. Keeping "Topological" would invite "why is the throat result not in the title?". |
| D2 | Primary throat magnitude | **±½ voxel** (image-derived; 0.088 mm radius, median 7.3 %DS); ±10 %DS as a secondary | It needs no external citation, and a referee cannot call it design-chosen. ±10 %DS is kept only if a published CT-grading variability reference is verified; otherwise it moves to the supplement as a sensitivity analysis. |
| D3 | Where T5 appears | Four rows in Table I: T5 ±½ voxel pooled, Protocols A–D. ±10 %DS and the sign split go to the supplement. | The throat result is now a headline, so it belongs in the main table. |
| D4 | The finer-territory result (A6) | Report it in the main text (one sentence in III-B plus the abstract qualifier); table in the supplement | It turns the devil's strongest argument into a measured scope statement. |
| D5 | Detector (A7) | One sentence in IV-C plus a supplement table; phrase it as a measurement with its false-alarm rate | It is an honest partial result. Overclaiming it would be caught. |

## 3. Section-by-section changes

Lines are main-text column lines (about 55 characters each). + means added, − means cut.

| Section | Change | Lines | Strengthens because | Fixes |
|---|---|---|---|---|
| Title | Drop "Topological" (D1) | 0 | Scope matches the content | — |
| Abstract | Rewrite around the four-point headline (§1), at 250 words. Keep the threshold-stratified qualifier, the magnitude qualifier and the 3D sentence (shortened). | 0 | Leads with the complete risk picture and measured check performance | 5/5 asymmetry; DA C1; V9; I W3; E W3 |
| I. Introduction | Contribution paragraph: add the throat error, the check granularity and the measured quality metrics. One sentence on clinical relevance: CT-FFR is known to be sensitive to the minimal lumen area [10]–[12]. | +2 | Positions the throat result against existing caliber-uncertainty work rather than contradicting it | C W3 |
| II-C Error types | Define T5: same lesion, throat diameter ±½ in-plane voxel, primary; ±10 %DS secondary. Re-derivation equals A by construction. | +4 | Defines the new error precisely | — |
| II-D Protocols | One sentence: the check was repeated with territories one branching level finer (median 4–5 per tree), with an unperfused territory scored as a full mismatch | +2 | Makes the granularity analysis part of the design | DA C1 |
| II-F Outcomes | One sentence: tube-model DSC and clDice of every corrupted tree; AUC for flip | +1.5 | Turns the informatics claim into an outcome | I W3 |
| III-A Decision changes | Throat flip rates vs topological (paired sign test); caliber away from the throat stays near the floor. Table I gains 4 T5 rows. | +3 text, +4 table rows (~8 col-lines, double-column table) | Removes the design-set ranking | 5/5 |
| III-B Passes-and-wrong | Throat errors pass while wrong under A–D (20–42% untuned, 51–86% tuned). At finer territories topological P&W falls to 3–7%, taper and throat do not [T5L2]. | +4 | The concealment claim becomes specific and robust | DA C1, C W2 |
| III-C Side-branch loss | Merge into III-B, which keeps the medians | −4 | Space | — |
| New III-F, or inside IV-B: overlap metrics | DSC T1 ≈ T4 (0.97) though T1 flips about 2× as often; RCA breaks DSC 0.62; 62–91% of decision-changing topological errors keep DSC ≥ 0.928 | +3 | The paper's informatics claim, now measured | I W3, E W3 |
| IV-A | "Three to six times" → "branching and throat errors each changed about a third of decisions; caliber errors away from the throat stayed near repeat measurement" | 0 | Accurate ranking | — |
| IV-B | Overlap sentence replaced by the measured version (A5 draft) | −1 | Measured, shorter | I W3 |
| IV-C Practical use | First: check the branching and the throat caliber directly. Third: pre-tuning mismatch, discrete bed only, AUC 0.77, half of correct models exceed 10% under noise. | 0 | Advice matches the evidence | E W3, I W4 |
| IV-D Limitations | Throat sentence replaced. Granularity sentence replaced by the measured result. Add: throat magnitudes are ±½ voxel; real stenosis-grading variability may be larger. | 0 | Removes limitations that are now answered | — |
| Conclusion | Rewrite to the four-point headline | 0 | — | — |
| Methods cuts | Move to the supplement: eligibility list details (−3), 3D mesh/solver specifics (−4), demand calibration details (−3) | −10 | Space; the detail stays available | — |
| Fig. 2 | Keep. Reduce the height ~10% if needed. | −0 to −3 | JBHI papers carry more figures than ours; do not remove one | — |
| **Net** | | about +2 against 3 free | | |

If the net is still over, shrink Fig. 1 (0.93 → 0.88 textwidth, −2), not Figs. 2–4.

## 4. Supplement (target ≤ 8 pp; currently 6, with about 50 lines free)

| New section | Content | Est. lines |
|---|---|---|
| S-throat | T5 definition, voxel spacing, the full table (each sign, both magnitudes, A–D, flips, P&W, grey zone), and the bound-fit note (C: 11 excluded; D: 97 kept, which is conservative) | 30 |
| S-granularity | A6 partition, the 100%-mismatch rule, validation, and a table (T1+T2, T3+T4, T5 × C/D × Level 1/2) | 25 |
| S-overlap | A5 tube-model DSC and clDice by error type, AUCs, and the reason the taper DSC sits above 0.928 | 18 |
| S-detector | A7 AUCs, false-alarm rate under noise, and the threshold at 5% false alarm | 18 |
| Moved from main | Eligibility details, 3D solver details, demand calibration | 15 |
| **Total** | | about 106 lines ≈ 1.8 pp → supplement about 8 pp; 8 + 8 = 16 combined |

To reach about 15 combined: shorten the S1 pipeline text (−8), merge S4/S5 demand tables (−10), and drop the 13% column of Table S3 (−0). That gives about 7 pp of supplement and 15 combined, consistent with the published precedents.

## 5. Verification before integration (Fable, independent)

1. Recompute from the CSVs:
   - T5 flips and P&W (4 cells);
   - the A6 Level 1/2 P&W (4 cells);
   - the A5 DSC medians and the T1-vs-T4 paired test;
   - the A7 AUCs and the 0.10 false-alarm rate.
2. Check that the T5 implementation re-inserts only the throat and that reference radii and the bed are unchanged, so that B = A holds by construction.
3. Check the 97 D bound fits: are they the right rule, and is keeping them conservative?
4. Find and verify a published CT stenosis-grading variability reference for ±10 %DS, or recommend demoting it.
5. Draft the integrated abstract, III-A, III-B, IV and Conclusion text within the line budget in §3, and the supplement sections in §4.

## 6. Schedule

| Date | Work |
|---|---|
| 10-09 evening | T5L2 finishes; Fable verifies and drafts (§5) |
| 10-10 | I integrate the main text and the supplement; rebuild; check every printed number against the CSVs |
| 10-11 | Update the cover letter (contribution paragraph, title); prepare the GitHub repo update (add the T5/A5/A6/A7 analysis scripts if the operator agrees) |
| 10-12 | Fresh blind re-score (same 5 seats and rubric) |
| 10-13 | Fix re-score findings; run submission-check; send to co-authors |
| 10-14 | Rebuild the upload set (portal abstract, title, LaTeX zip without comments); operator read |
| 10-15 | Submit |

## 7. Expected effect on the blind scores (panel mean; estimate ±0.5)

| Dim | Before audit | Plan v1 (Fable) | This plan | Why |
|---|---|---|---|---|
| S1 Novelty | 6.8 | 6.9 | 7.3 | Throat × tuning × check granularity × measured quality metrics is a fuller contribution |
| S2 Rigour | 6.0 | 6.5 | 7.1 | Asymmetry removed; granularity measured; detector quantified |
| S3 Claims vs evidence | 5.8 | 6.8 | 7.3 | Every headline claim is now measured, with its scope stated |
| S4 Physiology | 6.0 | 6.4 | 6.8 | Throat error is the clinically central caliber error. Flow regime and radius bias remain. |
| S5 Consistency | 7.8 | 8.5 | 8.3 | More numbers carry more risk; the 10-10 check guards it |
| S6 Clarity | 7.0 | 7.0 | 7.0 | Denser |
| S7 Venue fit | 6.4 | 7.0 | 7.4 | Overlap metrics and detector are JBHI-relevant measured results |
| S8 Reproducibility | 5.6 | 7.0 | 7.2 | Public code (+ new scripts if added) |
| **Overall** | **6.4** | **6.9** | **≈ 7.3** | Likely minor–major split. Remaining: noisy-target tuning, radius bias, real failure frequency (revision). |

## 8. Risks

1. **A half-voxel throat error flips about a third of decisions.** A referee may read this as "CT-FFR near 0.80 is unreliable".
   - Mitigation: frame it within the threshold-stratified cohort, and cite MLA sensitivity work [10]–[12] as consistent.
   - The grey-zone analysis shows how many flips end beyond 0.75–0.85.
2. **The headline numbers change.** The cover letter, portal text and GitHub README must all follow.
3. **Line budget.** If the cuts are not enough, the fallback is Fig. 1 shrink. A main text of 9 pages would cost $250.
4. **T5L2 may show that throat concealment falls at the finer level.** Then point 3 of the headline becomes "concealment of every error type depends on check granularity, and only the taper survives a finer check". Wait for the result before drafting.
