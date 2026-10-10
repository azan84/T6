# Conformance matrix — Paper 6 → IEEE JBHI special issue (2026-10-08)

Guide: "Prepare and Submit Your Manuscript" (PS) and "For Authors" (FA), both retrieved 2026-10-08. The guide text names the journal as "IEEE J-BHI"/"JBHI", not by its full title.

| Requirement, quoted | Where | Status | Evidence | Owed |
|---|---|---|---|---|
| "Manuscripts are normally submitted as regular papers, review papers or special issue papers." | PS | PASS | Special issue paper | Select the SI in the portal |
| "The page limit is 14 pages for regular papers ... including supplementary material." | PS | PASS (at limit) | main 8 + supplement 6 = 14 | none |
| "Regular papers that exceed eight (8) pages will incur mandatory overlength page charges." | PS | RISK | 8 pp in IEEEtran; **9 pp in the official ieeecolor template** (3 references, ~10 lines, spill) | OPEN-1 |
| "The official template of papers submitted to IEEE JBHI is available here" | PS/FA | DEVIATION | Manuscript uses `IEEEtran`; template is `ieeecolor` + `generic.sty` | OPEN-1 |
| "All submissions must be in IEEE single spaced, double column format with embedded figures and tables" | PS | PASS | IEEEtran journal, floats embedded | none |
| "For manuscripts, an abstract of not more than 250 words is allowable." | PS | PASS (thin) | 248–249 words rendered; 252 by the tool's source count (splits 32--33, \textminus) | Check the portal count when pasting |
| "The abstract should indicate the objective of the study, methods, major results, conclusions, and one sentence significance to biomedical research." | PS | PASS | Gap/objective s.3, methods s.4, results s.5–9, conclusion+significance last sentence | none |
| "The abstract should be without abbreviations, footnotes, references, or mathematical equations." | PS | PASS | No abbreviations after the CFP edit; no citations or equations | none |
| "References should appear in a separate reference section ... numerals in square brackets." | PS | PASS | IEEEtran numeric, 33 refs, first-citation order | none |
| "Style for papers: Author(s), first initials followed by last name, title, periodical, volume, inclusive page numbers, month, year." | PS | MINOR | Months omitted (IEEEtran prints them only if the .bib has `month`) | Optional |
| "If the data are derived from a publicly available database, the original source and reference must be provided." | PS | PASS | ImageCAS (zeng2023) and ImageCAS-X (bransby2026, Zenodo DOI) cited | none |
| "...in the case of other than public datasets information regarding their ethical approval ... should be mentioned" | PS | PASS | Acknowledgment: public anonymized dataset, no ethics approval required | none |
| "All submissions must include a cover letter in the text box" | PS | OWED | Letter is a LaTeX PDF with bold and bullets | OPEN-4: plain-text version |
| "Innovation and significance of the work in relation to the scope of JBHI" | PS | PASS | Innovation and Significance paragraphs | none |
| "Confirm that the manuscript is entirely original, has not been copyrighted, published, submitted, or accepted for publication elsewhere" | PS | PARTIAL | Letter says "original, has not been published, and is not under consideration elsewhere" | OPEN-4 |
| "The consent form with a hand-written signature must be uploaded as a supporting document" | PS | OWED | Not on file | OPEN-2 (blocking) |
| "All IEEE journals require an Open Researcher and Contributor ID (ORCID) for all authors." | PS | OWED | Not recorded for the five authors | OPEN-3 |
| "It is obligatory for all the authors to use their institutional email or IEEE email" | PS | OWED | Only the corresponding author's email is in the manuscript | OPEN-3 |
| "Authors are encouraged to suggest 4 potential reviewers" | PS | READY | `SUGGESTED-REVIEWERS-2026-10-08.md`, four primary, guest editors excluded | Confirm no links |
| Single-blind review ("the reviewers know the identities of the authors") | PS | PASS | Named manuscript | none |
| Generative-AI disclosure | not stated in guide; house rule §1 / memory | OWED | No declaration in main.tex | OPEN-5 (blocking under R11) |
| Open access / APC | PS | DECISION | Traditional submission has no APC; OA US$2,800 | Choose at submission |
| Conference precursor | PS | N/A | None | none |
