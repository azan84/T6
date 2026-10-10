# Audit — pre-submission CFP-fit plan (JBHI SI, deadline 2026-10-15)

**Date:** 2026-10-08 · **Reviewer:** Fable (independent) · **Checked against:** the CFP PDF, `main.tex`/`main.pdf` (8 pp), `supplement.tex` (6 pp), `cover_letter.tex`, `ARS-BLIND-REVIEW-2026-10-08/{EDITORIAL-DECISION-AND-ROADMAP,FIX-LOG,GO-NOGO-CHECK}.md`, `deposit-2026-10-08/`, `protocol/COHORT-FROZEN-2026-09-18.sha256`, `drafts/registration-2026-10-03/`, `STUDY-PLAN-v2.md`. Nothing was edited. Abstract recounted from the PDF text: **250 words**. Page 8 right column has about 8–10 free lines after ref. [33]; the left column is full.

## Verdicts

| # | Item | Verdict |
|---|---|---|
| 1 | Zenodo deposit + DOI + cohort hash in Data and Code Availability | **KEEP, deposit needs repair** |
| 2 | Digital-twin framing (Intro, Index Terms, IV-C, Conclusion, abstract) | **MODIFY** (wording) |
| 3 | Cover letter names two CFP topics | **KEEP, with one wording limit** |
| 4 | Strip `main.tex` line 1 | **MODIFY** (incomplete) |

### 1. Code deposit — KEEP, but `deposit-2026-10-08/` is not ready

Fit: the CFP names "segmentation errors, uncertainty propagation and the need for robust validation frameworks"; R8 is the only Required roadmap item still OPEN (GO-NOGO C-14); the Conclusion offers the test to "any pipeline". A DOI is the cheapest remaining fix. Blinding: `STUDY-PLAN-v2.md` line 23 records JBHI as **single-blind** (verified on embs.org 2026-10-03), so a named Zenodo record before submission is no conflict.

Readiness findings (code copies are comment-free and the leak grep for paths, names and AI strings is clean; cohort CSV hashes match the manifest, `b8fe7909…` and `8e0079a0…`):

- **Missing scripts:** `grey_zone.py` (source of Table S6), `run_prevalence.py` (produces `E0_prevalence_test.csv`, which `severity_sweep.py` line 78 reads), `stageA_benchmark_0d.py`. All three are comment-free and leak-clean in `code/`; copy them.
- **No results at all.** R8 asks for per-instance results. Add `results/ablation-2026-10-07.csv` (1.7 MB), `ablation-perterritory-2026-10-08.csv`, `negatives-2026-10-07.csv` (2.6 MB), `discrete_arm_eligibility.csv`, `sweep_test.csv`, `E0_prevalence_test.csv`, `demand-replication-x{2,3}-2026-10-08/` (3.6 + 3.2 MB), `analysis-ablation-2026-10-07/*.csv`, `analysis-revision-2026-10-08/*.csv`. Leave out `REPORT.md`, the `summary_k*.txt`, all `.log`, smoke and `PRE-*` files. The two `_pullback.csv` files (15 + 29 MB) are optional.
- **3D inputs the scripts hard-code:** `fig5_case3d.py`, `m1_zerod_vs_3d.py` and `supplement_tables.py` line 71 read `cfd_handover/packages/M1/*`, `returns/2026-09-26/M1_probes_*`, `M1_outlets_*`, and `returns/2026-10-03/M1_D7_sensitivity_2026-10-06.csv`. Ship only those CSV/JSON files. **Do not ship any `.md` from `cfd_handover/returns/`**: `2026-10-03/` holds `AUDIT_*gemini*.md` and `AUDIT_*gpt*.md`, and `2026-09-26/` holds `NOTE*.md`, `failures_NOTES.md`.
- **Do not ship `protocol/COHORT-FROZEN-2026-09-18.sha256`.** It carries internal commentary ("there is no version control here…") and code hashes that no longer match the comment-stripped copies. Write a fresh `SHA256SUMS` over the deposit.
- **Absent:** `README.md`, `LICENSE` (MIT is already in the 10-03 `.zenodo.json`; the CSVs derived from ImageCAS-X need CC BY 4.0 attribution), `requirements.txt` (the project file also **lacks `statsmodels`**, imported by `analyse_ablation.py` and `summarise_revision.py`), `.zenodo.json` (reuse the 10-03 one with a new title; its "deposited before the ablation is run" wording is now false). Delete `code/__pycache__/`.
- **Google Drive placeholders:** `du` reported several result files as 0 B on first read and full size minutes later. Verify every file is local (non-zero) before hashing and zipping.
- **Pre-specification claim.** No `osf.io` link exists anywhere in the folder; the last recorded status is "not lodged yet". A Zenodo record dated 10-09 does not prove the cohort was frozen before the 10-07 run. Keep the Methods sentence as it is (it claims freezing, not registration). If the OSF registration *was* lodged, cite it in II-F and the data statement; that outranks the hash. If not, do not add any registration wording.
- Reserve the DOI first (Zenodo "reserve DOI"), cite the **version** DOI, publish before submission.
- The 64-character hash will overflow a two-column line in `\texttt`; use `\seqsplit` or `\allowbreak` every 16 characters.

Replacement for line 481:
> ImageCAS-X is available under CC BY 4.0 (doi:10.5281/zenodo.21887809). The code, error generators, frozen cohort list (SHA-256 `b8fe7909…5e46c`) and per-instance results are deposited at doi:10.5281/zenodo.XXXXXXX.

### 2. Digital-twin framing — MODIFY

The study is a steady reduced-order model with synthetic lesions, no patient data and no invasive FFR, and its "tuning" matches the clean model's own flows. Any sentence that calls *this* model a digital twin overclaims; sentences about the practice in the field are defensible. Also rename **"reduced-order twin"** (main 231, 379; supplement 30, 63, 293) to **"reduced-order counterpart"** so the only "twin" in the paper is the digital one.

- **Intro, para 2** — proposed "This tuning is the step that personalizes a coronary digital twin to the patient" is tautological and implies the anatomy is not personalized. Use, before "The segmentation therefore enters…": *"In a coronary digital twin, this tuning fits the model's physiology to the patient as the segmentation fixes its anatomy."*
- **Index Terms** — add "digital twins" (IEEE thesaurus form), alphabetically after "coronary artery disease". Fine.
- **IV-C first sentence** — "a model, or a digital twin calibrated to perfusion," is awkward. Use: *"Agreement with a fitted quantity does not by itself make a model credible; a coronary digital twin calibrated to perfusion also requires verification, uncertainty quantification and applicability \cite{viceconti2025}."*
- **Conclusion** — "…pipeline, including the calibration of digital twins" mixes a pipeline with a step. Use: *"…pipeline, including those that calibrate coronary digital twins to perfusion."*
- **Abstract** — keep "tuned", not "calibrated" (the paper uses tuned/tuning throughout; one stray synonym invites a terminology comment). Swap: "often tuned to match measured perfusion" → "often tuned to measured perfusion, as in a digital twin" (**+4**, not +3). Cuts (**−5**): "Whether a model that matches perfusion can still assign the wrong treatment at 0.80 has not been tested." → "Whether a perfusion-matched model can still assign the wrong treatment at 0.80 is untested." (−4); "a missed-branch FFR shift" → "a missed-branch shift" (−1). Result **249 words**, and it removes the only abbreviation in the abstract (JBHI: no abbreviations; STUDY-PLAN line 23) — a fix needed regardless.

Guest editors (Colombo, Celi, Marlevi, Sigovan) work on image-based twins and will accept perfusion tuning as the personalization step; they will not accept the paper's model being called a twin. The wording above never does.

### 3. Cover letter — KEEP with one limit

Name the two topics. Do not write "digital-twin validation": the paper validates nothing against patient data (R3 fixed that wording in the text). Say instead that the result *bears on* validation of digital-twin frameworks: a perfusion-fit residual is not validation evidence. Also replace "The code is available from the authors on request" with the DOI sentence, and add one clause naming the JBHI papers the manuscript builds on (Viceconti 2025, Chen 2025, Arminio 2026), which the letter currently omits.

### 4. Upload hygiene — MODIFY (incomplete)

Our own comments are at `main.tex` lines **1–3, 17–18, 268–269** (plus the `% ----` separators at 61, 96, 266, 407) and `supplement.tex` lines **1–3**. `refs.bib` and `supplement_tables/*.tex` are clean. `cover_letter.tex` is clean.

## Missing items, ranked

1. Abstract abbreviation "FFR" (above) — required by the guide, free.
2. OSF status — settle whether it was lodged; cite it if so.
3. Deposit repairs listed in §1 (scripts, results, 3D CSVs, README/LICENSE/requirements with statsmodels, fresh checksums, no internal `.md`).
4. "reduced-order twin" → "counterpart" (5 sites).
5. Cover letter: DOI sentence and JBHI-paper clause.

Not worth the space: S11 left-coronary qualifier in the abstract; C-15–C-17.

## Page and word risk

Main text additions: Intro +1 line (p. 1), Index Terms +0–1, IV-C +1, Conclusion +1, data statement +3 (hash and DOI). About 6–7 lines against roughly 8–10 free on p. 8. Expected to hold at 8 pages, but floats on pp. 2–6 can move; if a ninth page appears, drop the Conclusion clause first, then the Intro sentence. Abstract 249 as specified. Supplement p. 6 is two-thirds full; the rename adds nothing.

## Time (7 days)

- 10-09: assemble the deposit, re-run `ablation.py` and `ablation_per_territory.py` from the deposit copy (FIX-LOG reports byte-identical output for the 22 cleaned scripts; the added files need the same check), reserve the DOI, insert text, compile, check 8 pp / 249 words.
- 10-10: co-author read of the text changes and deposit; publish the Zenodo record; strip comments; rebuild the upload set.
- 10-11/12: submission-check, submit. Three days of slack. Realistic.

## Go / no-go

- GO: item 1 (after the repairs), item 2 (with the wording above), item 3 (with the limit), item 4 (all listed lines).
- NO-GO as proposed: the abstract "+3 words" arithmetic (it is +4), "calibrated" in the abstract, any sentence calling the study's model a digital twin, shipping the `.sha256` manifest or any `cfd_handover` `.md`.
- Unknown: OSF lodging; the operator must confirm before any registration wording is added.
