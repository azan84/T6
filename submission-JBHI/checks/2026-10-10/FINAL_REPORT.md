# Submission check — Paper 6 v2 → IEEE JBHI special issue, 2026-10-10

## 1. Verdict
**Ready with the listed fixes.** One guide rule fails (abbreviation in the abstract, OPEN-9), fixable with no change in length. Two small text defects (OPEN-11, -12). Two items outside the manuscript still block the upload: the signed consent form (OPEN-2) and the co-author critical read (OPEN-7).

## 2. Blockers
- OPEN-9 Abstract abbreviation "FFR" (Phase 3, guide rule).
- OPEN-2 Author Consent Form (Phase 3).
- OPEN-7 ICMJE criterion 2 (project rule).

## 3. Length statement
JBHI states length in pages: "The page limit is 14 pages for regular papers ... including supplementary material." Main 9 pp + supplement 5 pp = 14 pp in the official ieeecolor template (clean build). Page 9 incurs the $250 overlength charge (accepted 2026-10-09). Abstract 250 words as rendered (limit 250).

## 4. Guide conformance
Machine rules: abstract_max_words FAIL by the tool's source count (254, splits "32--33") but PASS on the rendered text (250). reference_style REFUSED (PS web layout), PASS on reading. Ten MODEL rows in `conformance.md`: one FAIL (abbreviation), consent form owed, funding not stated by the guide (OPEN-10), all else PASS.

## 5. Engagement with JBHI
3 of 36 references (8.3%), all 2025–2026: Viceconti 2025 (IV-C), Chen 2025 (Introduction), Arminio 2026 (Introduction); each cited once and each supports its sentence. venue_fit.py reports 1 because the other two have the journal name split across lines in main.bbl (OPEN-8). Sample yardstick (5 JBHI papers): 0%. Verdict unchanged from 10-08: **heavy relative to a small sample, justified**; no additions (R7). Framing: no citing sentence faults the authors.

## 6. Benchmark (carried from 10-08, hand-measured; manuscript row updated)
| metric | Paper 6 v2 | sample min | median | max |
|---|---|---|---|---|
| pages | 9 (+5 supp) | 9 | 12 | 14 |
| figures | 5 | 6 | 9 | 16 |
| tables | 1 (+10 supp) | 1 | 3 | 6 |
| references | 36 | 30 | 36 | 40 |
Headings Introduction / Methods / Results / Discussion / Conclusion: conform. Fewer main figures with detail in the supplement: defensible deviation.

## 7. Manuscript defects (seam read of the 10-10 edits)
- OPEN-11 semicolon in IV-B (introduced 10-10).
- OPEN-12 "DSC of 0.999" basis (whole scan).
- Checked and clean: Methods noise-matched sentence; Introduction owusu2026 sentence; Table I error names and protocol note; Fig. 2 axis "reclassified (%)"; Fig. 4 with T5 (rendered and inspected); Table S7 note values (14/22/26, 21/29/29 = removed rows); Table S9 T5 rows (= medians_T5.csv); S2/S5 merged bound-fit text.
- Readability tool: 0 sentences over 40 words, 0 mechanical defects; 27 house-style hits (semicolons in Methods audited earlier, not reopened). Overfull boxes: 10, all in the template's output routine (the unmodified template gives the same set).
- References: 36 cited = 36 listed, first-citation order, no duplicates. New since 10-08: boogers2010 and gouya2009 (DOIs verified against Crossref/PubMed: title, journal, first author, year, volume, pages match); owusu2026 (arXiv API: title, authors, STACOM 2026 acceptance match). The 33 earlier entries were verified on 10-08.

## 8. Cover letter
Tool: journal named exactly, salutation, placeholders PASS; "article type" and "named papers" FAIL are parser misses (the letter says "to the special issue" and names Viceconti et al. (2025), Chen et al. (2025), Arminio et al. (2026), all in the list with matching years). 8.4 read: fit argument tied to the CFP's three challenges and two topics (passes the sister-journal test); the three JBHI papers are described by what they contributed; guide originality wording present; every number matches v2 as built (final number check 10-10 + today's edits, which did not touch the letter's numbers). Optional addition: OPEN-13.

## 9. Upload-set hygiene
- Manifest `upload_manifest.txt`: 21 files (main.tex, supplement.tex, refs.bib, main.bbl, ieeecolor.cls, generic.sty, logo.eps, 5 figures, 7 supplement tables, main.pdf, supplement.pdf).
- Scan: 3 FAIL, all KEEP on reading: the Grammarly declaration in main.tex/main.pdf (R11), and the IEEEtran.bst header in main.bbl. 13 ADVISORY: technical "pipeline". No paths, placeholders or process notes.
- Cleaned copy `upload_clean/` written with --verify-build: **IDENTICAL** for main.tex and supplement.tex.
- `submission-JBHI/upload/` filled from the cleaned copy by `build_upload.sh`: Manuscript.pdf (9 pp), Supplementary_Material.pdf (5 pp), LaTeX_source.zip, source/ (21 files). Fresh compile: 0 undefined references; PDF text identical to v2; PDF Title/Author/Subject/Keywords empty. After F1–F3, re-run the cleaner and `build_upload.sh`. Previous set archived to `submission-JBHI/upload-archive-2026-10-08/`.
- Portal: title.txt and cover_letter.txt refreshed from v2 (10-08 versions in `portal-archive-2026-10-08/`); keywords unchanged; abstract.txt to be regenerated after F1.

## 10. OPEN register
Blocking: OPEN-9, OPEN-2, OPEN-7. Non-blocking: OPEN-11, -12, -10, -13, -8. See `OPEN.md`.

## 11. What changed during the run
No manuscript text changed. Upload folder rebuilt from v2 (10-08 set archived); portal title and cover letter refreshed. Run files in `submission-JBHI/checks/2026-10-10/`.

## Addendum, 2026-10-10 (after fixes; operator authorised the fixes and a readability pass)
- OPEN-9 RESOLVED: the abstract has no abbreviation (249 words rendered). OPEN-11 and OPEN-12 RESOLVED. OPEN-13 applied: the letter's bullet 3 gains the throat-error Dice sentence.
- Readability pass by an independent full read (30 ranked items), all applied except the two that added words without fixing a misreading (protocol phrase in III-C; noun-stack rewording in III-D), which were reverted for page fit. Applied items include:
  - three ambiguous referents;
  - "tube model" defined in II-F; "DS" defined in the supplement; "distance-map radius" → "reduced-order radius";
  - "concealment" → "passes-and-wrong";
  - about 30 clause-joining semicolons → full stops (house style);
  - "grey" → "gray" (US spelling, as in Petraco 2013);
  - IV-C considerations rewritten as facts, not instructions;
  - S2 now lists all eight ten-point Protocol C bound fits; the Table S7 note has bed labels and is split under 40 words; "lesion slot" defined (vessel, position and length; from analyse_ablation.py);
  - letter: three over-length sentences split, the "both" referent fixed, the opening list clarified.
- Page fit, word-neutral or content-free cuts:
  - the "3% and 4%" in III-B repeated the 3.1%/3.9% of the previous sentence;
  - data-availability, acknowledgment, Conclusion opening, limitations and two Discussion sentences tightened;
  - the STACOM venue line shortened.
- Number/citation check against the pre-readability snapshot: only the duplicate "3, 4" removed; every citation key kept. (Note: `snapshot_before/` was refreshed before the readability pass, so it holds the post-F1–F3 state; the F1–F3 diffs carry no numbers.)
- Build: main 9 pp + supplement 5 pp = 14; cover letter 1 p; 0 undefined references. Readability tool: 0 sentences over 40 words; house-style hits 26 → 8 (main), 16 → 4 (supplement).
- Upload rebuilt: scan 2 FAIL, both KEEP (Grammarly declaration; IEEEtran.bst header); verify-build IDENTICAL; `upload/` refilled by `build_upload.sh`; Manuscript.pdf and Supplementary_Material.pdf text = v2.
- Portal: abstract.txt (249 words, plain text) and cover_letter.txt (body = cover_letter.pdf) refreshed.
- Co-author reading copy: `submission-JBHI/coauthor-read-2026-10-10/` (manuscript, supplement, cover letter).
- Still blocking: OPEN-2 (consent form), OPEN-7 (co-author critical read).
