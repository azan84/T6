# Conformance matrix: Paper 6 v2 → IEEE JBHI special issue (2026-10-10)

Guide: "Prepare and Submit Your Manuscript" (PS) and "For Authors" (FA), retrieved 2026-10-08 (2 days old). Quotes carried from the 2026-10-08 matrix. The guide text names the journal as "IEEE J-BHI"/"JBHI", so guide_check reports "names the journal: False" (it is the journal's own embs.org/jbhi page).

| Requirement, quoted | Where | Status | Evidence | Owed |
|---|---|---|---|---|
| "Manuscripts are normally submitted as regular papers, review papers or special issue papers." | PS | PASS | Special issue paper | Select the SI in the portal |
| "The page limit is 14 pages for regular papers ... including supplementary material." | PS | PASS (at limit) | main 9 + supplement 5 = 14 (ieeecolor, clean build) | none |
| "Regular papers that exceed eight (8) pages will incur mandatory overlength page charges." | PS | ACCEPTED | 9 pp → $250 (operator accepted 2026-10-09) | none |
| "The official template of papers submitted to IEEE JBHI is available here" | PS/FA | PASS | ieeecolor + generic.sty (official template) | none |
| "All submissions must be in IEEE single spaced, double column format with embedded figures and tables" | PS | PASS | ieeecolor journal, floats embedded | none |
| "For manuscripts, an abstract of not more than 250 words is allowable." | PS | PASS (at limit) | 250 words in the rendered PDF; 254 by the tool (splits ranges such as 32--33) | Any abstract edit must keep ≤ 250 |
| "The abstract should indicate the objective of the study, methods, major results, conclusions, and one sentence significance to biomedical research." | PS | PASS | objective s.3, methods s.4–5, results s.6–12, conclusion/significance last sentence | none |
| "The abstract should be without abbreviations, footnotes, references, or mathematical equations." | PS | **FAIL** | v2 abstract: "Fractional flow reserve (FFR)" and "FFR was recomputed" (v1 of 10-08 had none) | F1 (OPEN-9) |
| "References should appear in a separate reference section ... numerals in square brackets." | PS/FA | PASS on reading (REFUSED by tool: PS web layout interleaves menu text; FA wording differs) | IEEEtran numeric, 36 refs, first-citation order | none |
| "Style for papers: Author(s), first initials followed by last name, title, periodical, volume, inclusive page numbers, month, year." | PS | MINOR | Months omitted (IEEEtran prints them only with `month` in .bib) | Optional |
| "If the data are derived from a publicly available database, the original source and reference must be provided." | PS | PASS | ImageCAS (zeng2023), ImageCAS-X (imagecasx_data, Zenodo DOI); Data and Code Availability section | none |
| ethical approval for non-public data | PS | PASS | public, anonymized dataset only | none |
| "All submissions must include a cover letter in the text box" | PS | PASS | portal/cover_letter.txt refreshed from v2 (identical body to cover_letter.pdf) | Paste |
| "Innovation and significance of the work in relation to the scope of JBHI" | PS | PASS | Innovation and Significance paragraphs; CFP challenges and two CFP topics named | none |
| "Confirm that the manuscript is entirely original, has not been copyrighted, published, submitted, or accepted for publication elsewhere" | PS | PASS | guide wording in the letter | none |
| "The consent form with a hand-written signature must be uploaded as a supporting document" | PS | OWED | not on file | OPEN-2 (blocking) |
| "All IEEE journals require an Open Researcher and Contributor ID (ORCID) for all authors." | PS | PASS | portal/authors.txt (five ORCIDs) | none |
| "It is obligatory for all the authors to use their institutional email or IEEE email" | PS | PASS | portal/authors.txt | none |
| "Authors are encouraged to suggest 4 potential reviewers" | PS | READY | drafts/manuscript/SUGGESTED-REVIEWERS-2026-10-08.md | Re-check against refs added since (owusu2026 group not suggested) |
| Single-blind review | PS | PASS | named manuscript | none |
| Generative-AI disclosure | not stated in guide; house rule | PASS | Acknowledgment: "used Grammarly for language editing" | none |
| Funding statement | not stated in guide | NOTE | Letter says no external funding; manuscript has none (IEEE usually puts it in the first footnote) | OPEN-10 (non-blocking) |
| Open access / APC | PS | DECISION | traditional route has no APC; OA US$2,800 | Choose at submission |
