# Submission check — Paper 6 (T6) → IEEE JBHI special issue, 2026-10-08

## 1. Verdict
**Ready with the listed fixes.** The science, references and guide limits pass. Four items block the upload: the AI declaration, the author consent form, ORCID and institutional emails, and the cover-letter originality wording. One decision is needed first: whether to typeset in the official template, where the paper runs to 9 pages.

## 2. Blockers
- OPEN-5 Generative-AI declaration missing (Phase 8b, R11).
- OPEN-2 Author Consent Form, hand-signed by all five authors (Phase 3).
- OPEN-3 ORCID and institutional email for every author (Phase 3).
- OPEN-4 Cover letter lacks the guide's "copyrighted, published, submitted, or accepted" wording (Phase 8).
- OPEN-7 ICMJE criterion 2 for two co-authors (project rule).

## 3. Length statement
JBHI states length in pages: "The page limit is 14 pages for regular papers ... including supplementary material." Main 8 pp + supplement 6 pp = 14 pp (IEEEtran). In the official ieeecolor template the main text is 9 pp (OPEN-1). Abstract 248–249 words as rendered (limit 250).

## 4. Guide conformance
Machine rules: abstract_max_words FAIL on the source count (252) but PASS on the rendered text (248–249); the difference is the tool's tokenisation of "32--33" and "\textminus". reference_style REFUSED on the Prepare-and-Submit PDF (its web layout interleaves the menu bar into the sentence); the same rule is quoted cleanly in "For Authors" and PASSES on reading. Ten MODEL rows judged in `conformance.md`: 9 pass or ready, 4 owed (consent form, ORCID/email, cover-letter text box and wording, AI declaration), 1 deviation (template).

## 5. Engagement with JBHI
3 of 33 references (9.1%), all 2025–2026: Viceconti 2025 (credibility, IV-C), Chen 2025 (small-vessel segmentation, Introduction), Arminio 2026 (tuning to measured flows, Introduction). Each is cited once, and each supports the claim at its citing sentence. Sample yardstick (5 JBHI regular papers, 2021–2026): 0 JBHI references in each (0%). Verdict: **heavy relative to a small sample, justified**. All three carry claims, and the special issue invites this conversation. No additions (R7). Framing: none of the three citing sentences faults the authors.

## 6. Benchmark (5 JBHI papers in Imaging-Medical/Resources; measured by hand, OPEN-8)
| metric | Paper 6 | sample min | median | max |
|---|---|---|---|---|
| pages | 8 (+6 supp) | 9 | 12 | 14 |
| figures | 5 | 6 | 9 | 16 |
| tables | 1 (+9 supp) | 1 | 3 | 6 |
| references | 33 | 30 | 36 | 40 |
| JBHI share | 9.1% | 0% | 0% | 0% |
Judgement: shorter than every sample paper, which is the 8-page choice (defensible: no page charges). Headings follow the IEEE register (Introduction, Methods, Results, Discussion, Conclusion), and Limitations is a Discussion subsection, as in Ericsson 2024 and Taskén 2026: **conform**. Fewer main-text figures, with detail moved to the supplement: **defensible deviation**. Closest sample is Ericsson 2024 (in-silico design with physics-based validation); most distant is Peng 2022 (inverse ECG).

## 7. Manuscript defects
- OPEN-6 semicolon in IV-C, introduced by the CFP edit.
- Readability: 16 sentences over 45 words (longest 83, Data and Cohort; 82, Introduction contribution list) and 22 house-style hits, mostly semicolons in Methods. These were audited earlier and are not reopened here (house rule §3).
- No undefined references, no overfull boxes in the main text, one overfull box in the supplement (pre-existing, 13 pt).

## 8. Cover letter
Tool: journal named exactly, salutation, no placeholders PASS. Article type not stated FAIL. Journal papers not named FAIL (the clause describes them without author or year). Advisory: "to our knowledge for the first time" (keep only if the authors stand by it), en-dash ranges (numeric ranges, acceptable).
8.4 read: the fit argument is specific to this call (it quotes the CFP challenges and names two CFP topics), and it passes the sister-journal test. Every number matches the manuscript as built today. The originality declaration is shorter than the guide's wording (OPEN-4). The portal takes the letter as plain text.

## 9. Upload-set hygiene
Manifest: `upload_manifest.txt` (20 files). Scan: 3 FAIL, all false positives on reading. Two are technical prose in the supplement ("every table and figure is generated from its output"), and one is the IEEEtran .bst header in main.bbl, a class comment that stays. 23 ADVISORY are technical uses of "pipeline" and one of "gate", so no fix. Our own % comments were removed earlier today. AI declaration: **not found** (OPEN-5). The cleaned copy with `--verify-build` has not been built. Run it after OPEN-1 and OPEN-5 are settled. Supplement Fig. S1 names code modules (`*.py`), which is acceptable with code on request.

## 10. OPEN register
Blocking: OPEN-2, -3, -4 (wording), -5, -7. Non-blocking: OPEN-1 (decide first), -6, -8. See `OPEN.md`.

## 11. What changed during the run
Nothing in the manuscript, supplement or cover letter. Run files in `submission-JBHI/checks/2026-10-08/`. DOI attribution: 27 DOIs checked against Crossref, all the cited paper (`doi_attribution.tsv`). The six entries without a DOI were verified by query: Viceconti 2025 (10.1109/JBHI.2025.3552320), Chen 2025 (10.1109/JBHI.2024.3450669), Arminio 2026, Shit 2021 (CVPR), the ImageCAS-X arXiv and the Zenodo record. All resolve.

## Addendum, 2026-10-08 (after fixes): upload set built
- Upload folder: `submission-JBHI/upload/`, containing `Manuscript.pdf` (8 pp), `Supplementary_Material.pdf` (6 pp), `LaTeX_source.zip` and `source/` (22 files: main.tex, supplement.tex, refs.bib, main.bbl, ieeecolor.cls, generic.sty, logo.eps, 5 figures, 8 supplement tables, built PDFs).
- `upload_clean.py --fix --verify-build`: build check IDENTICAL for main.tex and supplement.tex. A fresh compile of the cleaned folder (pdflatex, bibtex, pdflatex ×2) gives text identical to the reviewed PDFs, with no undefined references.
- Rescan: 5 FAIL, all reviewed and kept. (1, 2) "The authors used Grammarly for language editing." in main.tex and main.pdf is the AI declaration itself (R11 KEEP); the tool recognises only the Elsevier-template wording. (3, 4) "every table and figure is generated from its output" in the supplement is technical prose about reproducibility. (5) "% Generated by IEEEtran.bst" in main.bbl is a .bst-written comment, kept under the template-comment rule. 23 ADVISORY are technical uses of "pipeline" and "gate".
- PDF metadata: Title, Author, Subject and Keywords are empty; Creator is "LaTeX with hyperref". Figure PDFs carry only Matplotlib creator strings, with no paths.
- Portal text: `submission-JBHI/portal/` (title, abstract of 248 words, keywords, cover letter). These are pasted, not uploaded.
- Still owed before submitting: Author Consent Form (OPEN-2), ORCID and emails (OPEN-3), ICMJE criterion 2 (OPEN-7).
