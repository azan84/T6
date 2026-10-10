# Fix log — blind ARS review 2026-10-08 (major revision)

Simulated review; findings are fixed or declined here, not in a response letter.
Backups: `main-backup-2026-10-08-pre-ars-blind-fixes.tex`, `supplement-backup-…`, `refs-backup-…`, `cover_letter-backup-2026-10-08-pre-ars-blind-fixes.tex`.

## New computation (2026-10-08)

| Run | Code | Output |
|---|---|---|
| Protocol D (per-territory tuning; pre-specified in STATISTICS-PLAN §P2, not run on 10-07) | `code/ablation_per_territory.py` | `results/ablation-perterritory-2026-10-08.csv` |
| Demand replication, k ×2 and ×3, cohort re-selected, A–D | `code/demand_replication.py` | `results/demand-replication-x{2,3}-2026-10-08/` |
| Summary tables + paired McNemar on passes-and-wrong | `code/summarise_revision.py`, `code/replication_table.py` | `results/analysis-revision-2026-10-08/`, `supplement_tables/tab_replication.tex` |

Frozen modules (`ablation.py`, `zerod_ffr.py`, `severity_sweep.py`, `discrete_arm.py`) were imported unchanged.

Key results:
- Protocol D reproduces the 3D case exactly. On the scan-14 instance (discrete bed), D gives ΔFFR −0.0007, against 3D −0.0007 and the 3D twin −0.0005. Protocol C leaves +0.107 with residual 0.30.
- Protocol D corrects the typical topological error: median |ΔFFR| 0.005 in both beds.
- Under Protocol D, passes-and-wrong for topological errors is 20% (discrete) and 5% (leaky). Under B it is 2% and 6%. Tuning exceeds B in the discrete bed only.
- Caliber errors: 0% pass while wrong under B in both beds; tuning gives 4–18%, p ≤ 0.004 in all four comparisons. Almost all are taper models with FFR lowered.
- Demand replication: the directions hold at ×2 (both beds) and ×3 (leaky). Discrete-arm eligibility is 47 instances at ×2 and 17 at ×3.

## Must-fix items

| Item | Status | What changed |
|---|---|---|
| R1 3D interpretation (DA C1) | Fixed | III-D now reads "reproduced the reduced-order result"; per-territory tuning removed the error; cohort-model A/C/D values added. 3D methods: "per-outlet form of Protocol D". Abstract, Discussion and Conclusion reworded. |
| R2 one-scalar tuning | Fixed (new run) | Protocol D added to Methods, Table I, Results, Discussion and Conclusion. |
| R3 "validation" wording | Fixed | "pass validation" removed; "perfusion check" used throughout; Discussion says the check measures agreement with fitted targets. |
| R4 tuned taper / "minor risk" | Fixed | III-B paragraph on caliber passes-and-wrong; practical step 2 rewritten (check caliber when tuning); deferral/treatment bias of both directions stated. |
| R5 tuning attribution test | Fixed | McNemar of C and D against B on passes-and-wrong; tuning excess claimed for the discrete bed only; leaky stated as not significant. |
| R6 conditional rates / ranking | Fixed | Methods: rates conditional on the stratified design, not prevalences. Discussion: ranking holds for the magnitudes studied. Discrete band counts **not added** (space). |
| R7 flow regime | Fixed (new run) | Methods states the segmented arteries were narrower than normal values, cohort median demand 2.1 mL/s (126 mL/min). New III-E plus Table S5. Limitations updated. |
| R8 code / pre-specification | Partial | SHA-256 of the cohort list in Methods. Protocol D and the demand replication declared as run after results were read. **Code stays "on request" (operator decision 10-08); the cover letter offers release during review.** |

## Other corrections

- Methods radius: "less half a voxel" was wrong. The loader uses raw EDT with no half-voxel correction (`imagecasx_loader.radius_from_mask`), and the text now says so.
- The old median demand "1.5 mL/s, inlet radius 1.39 mm" matched neither the sweep nor the cohort. It is replaced by the cohort values (2.1 mL/s, 1.60 mm).
- Supplement §S2:
  - "2 856 attempted" → 2 802 defined (Table S1 sum).
  - "10 of 5 860" floor draws → 10 of 4 940.
- Ref [9] (Arminio, JBHI 2026): the reviewer said "not found". **Declined**: Crossref and IEEE Xplore resolve 10.1109/JBHI.2026.3708991 (doc 11592354).
- Gosling 2020 is now matched to "re-derivation or tuning", not tuning alone (domain W-minor).
- Fig. 4 (side-branch A vs C) moved to Supplement Fig. S3. Fig. 2 and Fig. 3 captions now say they show Protocols A–C.

## Declined / not done (deadline)

- Real segmentation failure frequency for T1/T2 (EIC W3, perspective W2/W3): needs algorithm outputs. Not feasible by 10-15.
- Throat-radius caliber error (perspective W1): not added. Limitation stands that caliber magnitudes come from inter-observer statistics.
- Grey zone / continuous risk framing (domain W6), finer territory partition (domain W4), detector ROC of pre-tuning residual (EIC W4, perspective W5): deferred.
- 3D CFD re-run: none required. The existing prescribed-flow solve already corresponds to Protocol D.

## Page budget

Main 8 pp (abstract 248 words), supplement 6 pp, total 14 = JBHI cap. Cover letter 1 p.

## Go/no-go blind check (GO-NOGO-CHECK.md) → GO WITH FIXES; fixes applied 2026-10-08

Backups: `main-backup-2026-10-08-pre-gonogo-fixes.tex`, `supplement-backup-2026-10-08-pre-gonogo-fixes.tex`.

| Item | Fix |
|---|---|
| C-1 (blocker) "passes by construction" / "whether or not" | IV-A third finding and Conclusion reworded. Per-territory tuning passes almost every model; Protocol C passing models are 51% wrong (discrete). Conclusion: "can pass the perfusion check with a wrong FFR". |
| C-2/C-13 abstract | Per-bed values (19–20% discrete, 5–8% leaky). "In this threshold-stratified cohort". Taper named. "should be checked". 247 words. |
| C-3 B rates | III-B states paired-subset values: B 2%/6% (pass 22%/89%), A 13%/22%. Adds a C-vs-A McNemar (discrete p = 0.07, leaky p < 0.001, lowered). |
| C-4 demand | Corrected to median demand 2.3 mL/s (137 mL/min) = k·r_in³. 2.1 mL/s was the lesioned clean-model inflow. |
| C-5 demand claim | III-E now says ×2 both beds, ×3 leaky only. B rates 2–5% and 0%. Excess over B significant in 3 of 4 caliber comparisons and 0 topological ones. Caliber-B column added to Table S5. |
| C-6 limitations | The lumen offset moved the baseline across 0.80 and changed the effect size, but not its direction. |
| C-7 3D oracle | "per-outlet limit of Protocol D"; "the limit of Protocol D". |
| C-9 | Step 2: caliber flips near the floor (taper up to 13%). "passed while materially wrong". |
| C-10 | II-D gives the D range 10^±3. III-A states 769 D solves converged. S2 bound text separated for C and D. |
| C-11 | Fig. S1 3D-c box now "prescribed flows (D)". S5-A heading and Table S3 caption: "Perfusion-Check Threshold". |
| C-14 | Full SHA-256 in Data and Code Availability. Pre-specified versus post hoc analyses listed in II-F. Code DOI **not** added (operator: on request). |
| B-14 | Residual comparator named: relative to A, same instances, 0.22→0.14 and 0.11→0.02. |
| C-18 Table S2 severity identical? | Checked. Not a copy error: 0.018630 vs 0.018630 differ at 1e-6 (posterior means). |

Not done: C-15, C-16 (half-voxel / radius-bias discussion), C-17 (optional).

## Operator decision 2026-10-08 (late)
Data and Code Availability says only that ImageCAS-X is public (DOI) and that the code is available from the authors on request. The frozen cohort and its hash are not mentioned there; Methods still says the cohort list was hashed before the run. The cover letter matches. This supersedes the C-14 row above.

Comment-free copies of 22 scripts are in `deposit-2026-10-08/code/` for sharing on request. The working `code/` is unchanged. The cleaned copies produced byte-identical output on ablation and Protocol D test runs.

## Grey zone (domain W6) — done 2026-10-08
`code/grey_zone.py` → `results/analysis-revision-2026-10-08/grey_zone.csv`, Table S6 (`supplement_tables/tab_greyzone.tex`), plus one sentence in III-A citing Petraco 2013.

Results under fixed boundary conditions:
- No caliber-error flip ended beyond the 0.75–0.85 zone (0/194 discrete, 0/300 leaky).
- 20% (discrete) and 23% (leaky) of topological-error models flipped beyond it.

Page count after the change: main 8, supplement 6.

Deferred to the revision: real segmentation-failure frequency and throat-radius error. Plan in `REVISION-PLAN-POST-SUBMISSION-2026-10-08.md`.

## CFP alignment (JBHI SI call) — done 2026-10-08
Audit: `references/FABLE-REVIEW-CFP-PLAN-2026-10-08.md`. Backups: `*-backup-2026-10-08-pre-cfp.tex`.
- Abstract: "tuned to measured perfusion, as in a digital twin"; "perfusion-matched model … is untested"; "missed-branch shift" (FFR removed; no abbreviations left). 249 words.
- Index Terms: "digital twins" added.
- Introduction, paragraph 2: "In a coronary digital twin, this tuning personalizes the physiology." (The audit's longer wording pushed the main text to 9 pages.)
- IV-C, first sentence: credibility of "a coronary digital twin calibrated to perfusion".
- Conclusion, last sentence: "…including those that calibrate coronary digital twins to perfusion."
- "Reduced-order twin" renamed "reduced-order counterpart" (main ×2, supplement ×3).
- Own `%` comments stripped from `main.tex` and `supplement.tex`.
- Cover letter: names the two CFP topics; Significance covers digital twins calibrated to perfusion; one clause on the JBHI work it builds on; margins 1.5 cm to keep one page.
- Data and Code Availability unchanged ("on request"), per the operator decision above.

Page count: main 8, supplement 6, cover letter 1.

## Submission check fixes (JBHI) — done 2026-10-08
Run: `submission-JBHI/checks/2026-10-08/`. Backups: `main-backup-2026-10-08-pre-template.tex`, `cover_letter-backup-2026-10-08-pre-template.tex`.
- Template: switched to the official JBHI class (`ieeecolor` + `generic.sty`, `logo.eps` from `JBHI_LaTex_Template.zip`). In that class the paper had run to 9 pp. The three full-width figures are now set at 0.95\textwidth, which brings it back to 8 pp. No text was cut.
- Author line: the corresponding author's name is kept unbroken (`\mbox`). The second author line stays left-aligned, which is the class's own behaviour.
- AI declaration added to the Acknowledgment: "The authors used Grammarly for language editing."
- IV-C semicolon replaced by a full stop.
- Cover letter: states "special issue paper"; names Viceconti et al. (2025), Chen et al. (2025) and Arminio et al. (2026) with what each contributed; originality statement in the guide's wording; margins reduced to keep one page. Plain-text copy for the portal text box: `cover_letter_portal.txt`.
- Check: no number or citation key lost against the backup. Abstract 249 words rendered. Main 8 pp, supplement 6 pp.
- Supplement switched to the same class (`ieeecolor`, one column) with the manuscript's running header; 6 pp, no undefined references. Backup `supplement-backup-2026-10-08-pre-template.tex`.
- Cross-references checked: all eight manuscript pointers to the Supplementary Material land on existing content (Fig. S1, S2, S3; Tables S2, S3, S6, S8; Sections S5-B/C). The quoted values match the tables (13/16% thresholds; floors 3.1/3.9/6.2/7.2%; 12.5 µm, 0.0021). The supplement's pointers back (Eq. (1), Table I, Section III-D) are correct.
- Cover letter opening names the special issue in full (PDF and portal text).
- Data and Code Availability rewritten in the standard data-availability template form (no IEEE-prescribed wording exists): "The data that support the findings of this study were derived from resources available in the public domain: ImageCAS [22] and ImageCAS-X [23] (CC BY 4.0). The code is available from the corresponding author upon reasonable request." The full-width figures were reduced to 0.93\textwidth to hold 8 pp. The cover letter's code sentence was aligned. Backup `main-backup-2026-10-08-pre-das.tex`.
- Byline: "Mohd-Zulhilmi Ismadi" (operator 2026-10-08); footnote initials "M.-Z. Ismadi"; cover-letter signature to match.
- Author line centring: in journal mode `ieeecolor` sets `\@author\centerline{}`, which puts a full-width empty box on the last author line, so the names wrap and that line sits flush left. Fixed by ending the author paragraph with `\endgraf\vspace{-\baselineskip}` (main and supplement). Authors are now on one centred line; 8 + 6 pp; no author-line overfull.
