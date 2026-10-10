# manuscriptv2 (created 2026-10-10 from drafts/manuscript)

v1 (`drafts/manuscript/`) is frozen as of 10-10 08:40; v1 holds the audit folders, backups and FIX-LOG.

## Changes in v2
1. **Noise-matched comparison.** Error models and correct anatomy are tuned to the same 20 noisy perfusion targets (G1/G5, Fable).
   - Abstract: tuning sentences rewritten; Dice sentence kept; 250 words.
   - III-B: matched topological passes-and-wrong 21/9% vs a floor of 5/4% (paired excess 18/8 points); a Protocol D floor of 15/9%; matched throat 42–49% (C) and 78–80% (D); caliber 10–14% (C).
   - III-C: matched detector AUC 0.83/0.57.
   - IV-A, IV-C and the Conclusion restated on the matched basis.
   - Supplement:
     - new Table S10 `tab:matched` (body `supplement_tables/tab_noise_matched.tex`);
     - the detector table is replaced by one S8 paragraph;
     - the simulated-floor table is replaced by S9 text.
2. Six long sentences in the new text split (main max 40 words; supplement sentences ≤ 40).
3. Cover letter bullets 2–3 updated to matched numbers (bullet 3: AUC 0.83).

## PENDING
The numbers are INTERIM (draws 0–1; stability check ≤ 3 points). When `noise_matched_run.py` finishes (about 20:00 10-10):
- run its assemble step and `code/noise_matched_analysis.py`;
- refresh every matched number in the abstract, III-B, III-C, IV-A, IV-C, Conclusion, the S8/S9 text, `tab_noise_matched.tex` and the cover letter;
- then run the final number check.

Build: main 9 pp + supplement 5 pp = 14; abstract 250 words.

## 2026-10-10 10:30 — final numbers in (PENDING above closed)
- Run complete: 247 instance-beds x 21 draws (nominal + 0–19), 5,187 parts, no failures; nominal rows identical to the frozen runs. Assemble re-run (identical rows); run's own log kept as `results/noise_matched-2026-10-09/run-final-2026-10-10-0913.txt`. Interim outputs kept in `results/noise_matched-2026-10-09/interim-2026-10-09/`.
- Interim → final (every change ≤ 2 points, so the ≤ 3-point stability check holds):
  - topological C 21/9 → 19/8 %; correct-anatomy floor C 5/4 → 3/4 % (now equal to the simulated floor 3.1/3.9 %); paired excess over floor 18/8 → 17/7, over B 14/6 → 12/5;
  - topological D 38/20 → 36/19 %; excess 17/7 → 16/6; floor D 15/9 unchanged;
  - caliber C 10–14 → 9–12 %, D 14–27 → 13–28 %; throat unchanged (42/49 C, 78/80 D);
  - detector AUC 0.83/0.57 → 0.82/0.56; flagged 86/62 → 85/58 %.
- Edited: abstract, III-B (2 places), III-C, IV-A, IV-C, Conclusion, `tab_noise_matched.tex`, cover letter bullets 2–3. Limitation sentence "Tuning targets were error-free clean-model flows (noise entered only the simulated floor)" was contradicted by the matched comparison → "Outside the noise-matched comparison, tuning targets were error-free clean-model flows."
- Supplement S8 text already read 0.82/0.56; S9 floor (6.2/7.2 %, 72 % pass) unchanged.
- Backups: `backup-pre-final-numbers-2026-10-10/`. Build: main 9 + supplement 5 = 14 pp; cover letter 1 p; abstract 250 words.
- Final number check: `NUMBER-CHECK-2026-10-10.md`.

## 2026-10-10 midday — after final number check (NUMBER-CHECK-2026-10-10.md: 0 mismatches)
- L1 fixed: II-F gains "In a noise-matched comparison, each error model was tuned under Protocols C and D to the same 20 noisy target sets as its correct anatomy; rates are means over draws (Supplementary Material)."
- Terminology: "flip" → "reclassification" everywhere (main, supplement, tab_demand.tex; table headers "Reclass."; Fig. 2 y-axis "reclassified (%)", script code/fig2_t5.py, backup fig2_t5-backup-2026-10-10.py). Basis: PubMed CT-FFR abstracts use reclassif* 16×, flip 0×; JBHI has no FFR papers on PubMed.
- Table I: Error column now names each error and its class (T1 missed branch / topological … T5 throat ±½ voxel / throat caliber); note lists Protocols A–D.
- New ref owusu2026 (STACOM 2026, arXiv:2607.28327): one sentence in the Introduction (bifurcation connectedness tracked FFR-CT decision agreement, outlet resistances set on the reference tree), one in IV (insensitive to caliber-only errors; the throat error is of this kind).
- Supplement trimmed to stay at 5 pp (captions S2/S7 shortened, S5 note and S7/S9 sentences tightened; no content removed).
- cover_letter_portal.txt regenerated from cover_letter.tex (body identical to the PDF).
- Checks: numbers unchanged by the edits (only new numerals: 20, ½, 2026); abstract 250 words; main 9 + supplement 5 = 14 pp; no undefined refs.
- Backups: backup-pre-terminology-2026-10-10/.

## 2026-10-10 afternoon — Fig. 4 gains T5
- New analysis: `code/a5_overlap_t5.py` (a5 overlap metrics for T5_vox_narrow/wide, frozen modules patched in memory) → `results/a5_overlap_t5-2026-10-10/overlap_metrics.csv` (254 s); `code/a5_overlap_t5_join.py` joins to the frozen T5 A/B outcomes → `overlap_joined_T1-T5.csv`, `medians_T5.csv`. Checks: clean FFR reproduced exactly (n 298); T5 Protocol A reclassification 30/36% = Table I.
- T5 result: DSC tree 0.998/0.999, DSC scan 0.999, clDice 1.000 (min 1.0), no connected-component change; |ΔFFR_A| median 0.112/0.105, range −0.354 to 0.267.
- Fig. 4 (`code/fig_overlap.py`, backup `fig_overlap-backup-2026-10-10.py`): T5 series added, y-axis −0.45 to 0.56, legend lower left. Caption + III-C sentence added; Table S9 gains T5 rows; S7 AUC sentence now says "over T1–T4".
- Main trimmed back to 9 pp (Methods noise-matched sentence shortened; "(analysis pipeline in the Supplementary Material)" pointer dropped; Table I protocol note shortened).
- OPEN: supplement now 6 pp (total 15 > 14): awaiting operator decision on the supplement cuts.

## 2026-10-10 afternoon — supplement back to 5 pp
- Table S7 (throat): half-voxel primary-demand rows removed (duplicated Table I); their beyond-zone proportions moved to the note (14/22/26% discrete, 21/29/29% leaky for A-B/C/D).
- Layout: \Needspace 16 → 6 lines (removed large blank areas at the foot of pp 3–4).
- Prose tightened, no content removed: S2 Exclusions absorbs the Protocol D bound-fit detail that S5 repeated (S5 now points to S2, label sec:excl); S5 drops the "B equals A" sentence (in the note); S3 and S4A notes shortened.
- Build: main 9 + supplement 5 = 14 pp; page 5 about 60% full. Backup: backup-pre-terminology-2026-10-10/supplement-pre-trim.tex.

## 2026-10-10 evening — submission check fixes + readability pass
- Submission check run: `submission-JBHI/checks/2026-10-10/` (FINAL_REPORT.md with addendum, OPEN.md, conformance.md).
- Abstract without abbreviations (guide rule); 249 words. IV-B semicolon; "whole-scan DSC of 0.999".
- Cover letter: throat Dice sentence added to bullet 3; long sentences split; portal copy regenerated (body identical).
- Readability pass applied (see FINAL_REPORT addendum); main still 9 pp, supplement 5 pp.
- Upload set rebuilt in `submission-JBHI/upload/`; co-author reading copy in `submission-JBHI/coauthor-read-2026-10-10/`.
