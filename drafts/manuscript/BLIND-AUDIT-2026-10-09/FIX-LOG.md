# Fix log: blind audit 2026-10-09 (A2 wording + A3 abstract)

Backups: `main-backup-2026-10-09-pre-blind-audit-A2A3.tex` and `supplement-backup-2026-10-09-pre-blind-audit-A2A3.tex`.
Build: main is 8 pp with about 3 lines free on p. 8; supplement is 6 pp. The abstract is 250 words. No numbers were changed.

| Plan ID | Register | Change | Where |
|---|---|---|---|
| A3 | V4, V10, V15, V37 | Abstract rewritten word-neutral. It now has: "threshold-stratified" before the first rate; "for the error magnitudes studied"; "two or three main-branch territories"; 3D shift given against the clean reference (0.074 → 0.022); the exact demand statement (tuned excess significant only at baseline demand, discrete bed); a closing finding instead of an instruction. Removed: "(pooled)" and "none for caliber errors with re-derived BCs" | Abstract |
| T1-1 | V1 | Fig. 3 caption: "below 0.01 in all but two models" | III-B |
| T1-14 | V26 | S2: states why bound-hitting D fits are retained and C fits at a bound are failures | Supplement S2 |
| T1-2 | V2 | "about half" replaced with 20 of 39 (discrete) against 14 of 154 (leaky) | IV-A |
| T1-3 | V4 | III-E already exact; abstract fixed | Abstract |
| T1-4 | V10 | Qualifier in abstract and Conclusion; IV-A adds "no error type perturbed the stenosis throat alone" | Abstract, IV-A, Conclusion |
| T1-5 | V7, V8 | 3D: −0.0007 against the prescribed-flow clean geometry and +0.022 against the clean tree with resistances, with the reason; Fig. 4 caption: "by 0.074 at the measurement point" | III-D, Fig. 4 |
| T1-6 | V28 | Strict residual limit not met on the finest mesh | III-D |
| T1-7 | V9 | Territories: median two, at most three per tree; Limitations: a segment-level check could detect errors within a main-branch territory; Conclusion: "main-branch perfusion check" | II-D, IV-D, Conclusion |
| T1-8 | V11 | The viscous loss of a lesion grows with its length (Poiseuille elements) | II-B |
| T1-9 | V12 | HD95 "used as a proxy for" lesion-extent disagreement | II-C |
| T1-10 | V22 | Flip: "and hence potentially in referral or treatment" | II-F |
| T1-11 | V23 | Protocol A: "outlet resistances obtained independently of the segmented tree" | II-D |
| T1-13 | V6 | "Holm-adjusted p = 0.24" | III-A |
| T1-15 | V24, V25 | Pointer to the ×0.7/×1.3 runs (II-B); 13% and 16% described as "between 10% and this bound" (the protocol's RC/√2 derivation rests on a conference abstract not cited in the paper, so it is not quoted) | II-B, II-F |
| T1-16 | V17 | Limitations: the radius offset was 0.045 mm at the throat; a caliber error of this size at the throat may matter as much as a topological one | IV-D |
| T1-17 | V37 | The abstract ends with a finding | Abstract |
| T1-18 | V38, I W2(iii) | Caliber errors one-directional; microvascular dysfunction, collaterals and error–morphology links not modeled | IV-D |
| missed | V36 | Conclusion: re-derived BCs lowered topological decision changes to 5–18% per error type | Conclusion |
| missed | D C5 | IV-C first consideration: "especially with fixed boundary conditions" | IV-C |
| V21 | V21 | Lower-bound inference replaced with descriptive rates (taper 13%/14% discrete, 9% leaky) | III-A |

Cuts made to hold 8 pp:
- Introduction novelty paragraph condensed.
- Navier–Stokes gloss removed (II-E).
- Cohort-model 3D sentence shortened.
- IV-A bed paragraph merged.
- IV-B reduced to one paragraph.
- IV-C fourth consideration shortened.
- Conclusion last sentence shortened.

Pending, not in A2/A3:
- Overlap-score wording in IV-B, IV-C and the Conclusion (A5).
- The detector in IV-C's third consideration (A7).
- Denominator harmonisation and Table S3 columns (A4).
- Fig. 3 0.10 line (A8).
- Data statement (A1, operator decision).
- Funding statement (operator).
- Vardhan reference (verify first).
- Portal abstract.txt and cover letter to be synced at the upload rebuild.

## A1: code release (2026-10-09)
- The repository is public at https://github.com/zulhilmi-ismadi/ctffr-segmentation-ablation (MIT).
  - Contents: 13 analysis scripts and the cohort list.
  - Source folder: `Paper6-T6/github-repo/`.
  - It reproduces the frozen results.
- Data and Code Availability statement: "on request" replaced by the analysis-code and cohort-list sentence with the URL. Main text still 8 pp.
- Cover letter: same change, plus `\usepackage{url}`. Still 1 page.
- Backups: `main-backup-2026-10-09-pre-code-url.tex` and `cover_letter-backup-2026-10-09-pre-code-url.tex`.
- Addresses V18 / E W4, M W10, C W12, I W9, D S8.

## A4 and A8 (2026-10-09)
- **A4, Table S3:**
  - Protocol D rows added.
  - New columns: "Pass" (n passing at 10%) and "Wrong among passing, %" (P(wrong | pass), Wilson CI). This fixes V3.
  - The A–C rows are unchanged; the new generator `code/supplement_table_thresholds.py` reproduces them exactly.
  - Footnote: Protocol D passes-and-wrong equals its materially wrong proportion.
- **A4, supplement S2 (T2-6):** Protocol A vessel breaks with no outflow, scored as flips, give 40% → 43% (41/96) discrete and 43% (64/149) leaky, unchanged.
- **A4, denominators (V5):**
  - Table S5 now uses the defined-residual denominators of Table I and S3. `code/replication_table.py` was changed by one line.
  - Only the B topological column moved, by 1 point at most.
  - Caption updated.
  - Main-text III-E range: B "2–5%" → "2–6%".
  - The per-cell repeat floor was not added: V21 was resolved in A2 by replacing the lower-bound inference with descriptive rates.
- **A8:** Fig. 3 has a dashed line at the 0.10 threshold, and the caption says so. Figs. 2 and 4 regenerate unchanged from the same script, so `fig_results.py` reproduces the frozen figures.
- **Build:** main 8 pp, supplement 6 pp.
- **Backups:** `*-backup-2026-10-09*` (tables, figure, scripts, supplement).

## Supplement layout (2026-10-09)
- The journal title block, logo and running header were replaced by a compact centred title: "Supplementary Material", then the paper title, then the authors. Plain page numbers.
- This follows the two published JBHI supplements the operator supplied: 10.1109/jbhi.2024.3397589 and 10.1109/jbhi.2024.3516613.
- Still 6 pp; page 6 now has about 75% free.
- Backup: `supplement-backup-2026-10-09-pre-compact-title.tex`.

## Integration of A5/A6/A7/T5/T5L2 and supplement trim (2026-10-09)
- Integration: Fable's INTEGRATION-DRAFT applied (30 blocks); decisions D1–D5 as recommended.
- Main-text cuts: 1–9, 11, 12, 16, (a) and (b). Moved content went to the supplement.
- Main text: 9 pp. The A/B decision with the operator is pending: move Fig. 2, or pay $250 for page 9.
- Supplement trimmed 9 → 6 pp, benchmarked on JBHI supplements (3397589, 3516613, 3383610: tables and figures with brief captions, 1–4 pp).
  - Removed:
    - the stenosis schematic (it duplicates Fig. 1 and eq. 1);
    - the side-branch-loss figure (no longer cited; the medians are in the main text);
    - the mixed-model paragraph;
    - the ±10 %DS per-sign rows of the throat and granularity tables (the pooled ±10 rows are kept).
  - Every lead-in condensed to 1–5 sentences. Every number the main text points to remains.
- Backups: `backup-2026-10-09-pre-integration/` (pre-integration main/supp/bib/cover/tables + post-integration pre-trim supplement).
- Supplement format (operator request):
  - The author line is \small, the same size as the title line.
  - Every section heading is kept with its content (needspace). The S3 heading no longer sits alone at a page bottom.
  - Captions read "Table S1. ..." / "Fig. S1. ..." on one line with a bold label, as in the JBHI samples.
  - Still 6 pp.
- Data and Code Availability shortened to 'The analysis code is available at <URL>.' (main + cover letter); URL set in the body font (\urlstyle{same}), following the JBHI template, which prints URLs in roman.
- Results III-D and III-E merged as 'Robustness to Model Fidelity and Hyperemic Demand'; demand paragraph opens by naming k.
- Conclusion sentence on flip rates split in two (operator: too long).
- Operator decisions applied (2026-10-09):
  - (1) Last two Conclusion sentences tightened; the pre-tuning-mismatch safeguard was removed from the Conclusion and stays in IV-C.
  - (2) Fig. 2 legend "Repeat-FFR floor" → "Expected from repeat FFR". The caption explains the band as measurement variability, i.e. repeated invasive FFR, SD 0.018. The figure was regenerated; Fig. 3 is unchanged.
  - (3) Option B: main text 9 pp ($250 overlength charge). Results subsection "Overlap Scores and the Pre-Tuning Mismatch" restored.
- Page 9 holds about half a column of references; the right column is free.
- Correction: decision (2) reverted at operator request. The Fig. 2 legend and caption are back to the original; decision (1) is kept.
- Supplement orphan lines removed:
  - grey-zone sentence ('lie within');
  - demand-sensitivity paragraph condensed;
  - throat bound-fit sentence.
- A scan of the PDF finds no paragraph ending in a short line; still 6 pp.
- Long sentences shortened (Fable, 29 pairs applied).
  - Before: median 24, p90 45, max 91 words; 28 of 208 sentences over 40.
  - After: median 22, p90 35, max 40; none over 40.
  - JBHI benchmark (9 papers): median 21, p90 37; 7.6% over 40.
  - No sentence starts with 'Of'. Main text still 9 pp.
- Remaining long sentences fixed:
  - abstract: two sentences split; 'DSC' → 'Dice overlap'; the per-territory sentence dropped; 249 words;
  - Fig. 1 and Fig. 2 captions;
  - Table I note;
  - supplement eligibility and mesh sentences.
- Supplement: three remaining sentences of 42–46 words split (demand calibration, throat magnitude, granularity rule).
- Supplement: three remaining sentences of 42–46 words split (demand calibration, throat magnitude, granularity rule).
- Abstract: 'Dice overlap' → 'Dice score' (the most common term in JBHI full texts, 7 of 10 papers that mention Dice).
- Spare-space use:
  - IV-A non-identifiability sentence (E W11, DA);
  - two limitations: rates conditional on error presence (E W1, I W2); distance-map radius inside meshed lumen (C W1, D C3).
  - Still 9 pp.
- New main-text figures (operator: important images belong in the main text; JBHI papers carry about 6–9 figures, the CfP stresses segmentation errors):
  - Fig. 2 gains a T5 column (half-voxel throat, both signs pooled; script code/fig2_t5.py; legend unchanged);
  - new Fig. 4: tube-model whole-scan Dice score against Protocol A ΔFFR per error type (code/fig_overlap.py), in III-C.
  - Still 9 pp; page 9 now full.
- Cover letter rewritten:
  - new title; five error types incl. throat;
  - three updated findings bullets (throat, tuning and the finer check, Dice and detector);
  - significance states practical impact without clinical overclaim; 1 page.
- Impact statements in the manuscript:
  - abstract closing sentence (Dice and perfusion match do not certify branching or caliber; 246 words);
  - one Introduction sentence on what the results identify;
  - Conclusion closing on calibration versus validation evidence for digital twins, and reuse of the open test.
- Operator feedback:
  - abstract Dice sentence now explains the impact (near-perfect Dice yet twice the decision risk); 249 words;
  - Introduction 'results identify...' sentence simplified.
- Cover letter third bullet: near-perfect Dice (above inter-observer 0.93) yet twice the decision changes.
- Number check (Fable, about 1,470 values, 203 rows): 188 MATCH, 4 MISMATCH (wording/basis), all fixed:
  - M1: III-B class label 'caliber away from the throat, almost all taper';
  - M3: caliber mean |ΔFFR| range 0.006–0.044 (includes D);
  - M2: S2 bound-fit count aligned with S5 (64; 43 fail, 21 pass and wrong);
  - M4: |ln C| defined in Table S10 note.
  - Optional N3 ('flip counts … per cell') and N4 ('about 40- (cont.) Optional N3 ('flip counts ... per cell') and N4 ('about 40 percent') applied; N1 (5-19 class-level vs 5-18 per type) left as is, since each is correct on its basis.
- boogers2010 bib: author corrected to 'Joop H. M. Schreur' (verified via Crossref/PubMed); gouya2009, norgaard2014, taylor2013 verified correct.
- Limitations: the expert-review claim (not supported by NXT or Taylor 2013 methods, checked verbatim) is replaced by the supported fact that NXT screened image quality, and states our assumption that the error reaches the simulation uncorrected.
- Limitations: added that a half-voxel error is below the image resolution and so can reach the simulation uncorrected (pre-empts 'analysts would catch it').
- Fig. S1 simplified to a single-row pipeline plus a 3D branch (JBHI papers carry a one-glance overview figure, not detailed pipeline boxes); about a third of its former height.
- Table S12 (3D mesh test) folded into the S10 text (all values kept); S10 heading spacing relaxed; supplement now 5 pp, so main 9 + supplement 5 = 14.
- S1 text reduced to the eligibility criteria; removed the seed number, solver relaxation detail, selection mechanics and exponent sentence (in the main text or the code).
- G3 wording pass applied (43 items, Fable).
  - Covers: throat flips raised by tuning (McNemar); taper vs floor; 'at most five per cell'; 'about a third' on the pooled basis; one 5–19% basis; Table S3 T1–T4; 'all but two'; 'fewest among A–C'; tube-model Dice; clDice sentence; 'for the error magnitudes studied'; two limitation sentences; 3D lesion flow and Re in S10; competing-interests line.
  - Main 9 pp, supplement 5 pp, abstract 249.
- G4 integrated: Robustness subsection gains two sentences (throat error at ×2/×3: 27–29% flips fixed, 31–35% tuned, 52–75% passes-and-wrong; less than topological in discrete ×2, as often in leaky). Table S7 gains the ×2/×3 rows plus a footnote.
- Supplement trim to stay at 5 pp:
  - Table S7 per-sign half-voxel rows dropped (pooled rows kept).
  - Table S3 reduced to topological rows; the "All" rows are dropped and the lead-in states it.
