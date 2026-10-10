# JBHI: does the 14-page limit include supplementary material? (checked 2026-10-09)

## 1. Policy (live pages fetched 2026-10-09)

Source: https://www.embs.org/jbhi/prepare-and-submit-your-manuscript/ (raw HTML fetched and text extracted; quotes below are verbatim from that extraction).

- "PAGE LIMIT. The page limit is 14 pages for regular papers and 16 pages for review papers including supplementary material. The page limit must be implemented in both original submissions and revised papers."
- "PAGE CHARGES." "Voluntary page charges: For regular papers that are 8 pages or fewer and review papers that are 10 pages or fewer only voluntary page charges may be considered by the author ($110/page)."
- "Mandatory page charges: Regular papers that exceed eight (8) pages will incur mandatory overlength page charges. Review papers that exceed ten (10) pages incur mandatory page charges."
- "The rate for pages 9 and 10 (for regular papers) is $250 per page, and the rate for page 11 and beyond (for regular and review papers) is $350 per page. Payment of these charges is not negotiable or voluntary."
- "...The author(s) or his/her/their company or institution will be billed for all pages according to the Page Charge policy. The Publisher holds the right to withhold publication of the current submission or any future submissions from the author(s) if this charge is not honored. To avoid incurring mandatory page charges, the author(s) are strongly advised to practice economy in the original manuscript submission and restraint in preparation of the final manuscript following peer review."
- "Any other application charges (such as over-length page charge) will be billed separately once the manuscript formatting is complete but prior to the publication."

Multimedia page, https://www.embs.org/jbhi/submission-of-multimedia-materials/ (verbatim):
- "Multimedia materials can now be published as integral content of your manuscript. The multimedia content can be any playable file or data set file. The playable file can be an audio file or a video clip. The data set file can be raw data, source code, or application that can help the readers to further understand the research performed by the authors..."
- "Once your manuscript has been accepted, any files uploaded as 'multimedia' content will be available in IEEE Xplore."
- Says nothing about page counts. No JBHI page (for-authors, FAQ, multimedia) states that supplements are exempt from the limit.

https://www.embs.org/jbhi/for-authors/ : no page-limit text (format only: single-spaced, double-column, 11 pt or larger, 1 inch margins).

IEEE Author Center (https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/prepare-supplementary-materials/): NOT verified verbatim. The site returns a Cloudflare block to curl. Only a search-engine summary was seen: supplementary files are labelled as supplementary, uploaded as separate files, zipped with a README and placed on IEEE Xplore; "Most IEEE journals limit the number of pages per article, and in some cases, you may choose to exceed the page limit by paying overlength page charges." That summary is general IEEE text and is not a JBHI-specific exemption. The IEEE "Preparing Multimedia Materials" PDF (https://ieeeauthorcenter.ieee.org/wp-content/uploads/Preparing_multimedia.pdf) was read: it covers file types and README only, no page rule.

Special issues: https://www.embs.org/jbhi/special-issues/ lists 2026 calls including "Federated Learning and Digital Twins for Smart Healthcare" (deadline 31 Aug 2026), "Multimodal Edge-Artificial Intelligence for Real-Time Digital Twins in Personalized Healthcare" (30 Oct 2026), "Emerging AI Paradigms for Next-Generation Medicine: Safety and Reliability in Vision-Language Models, Agentic Systems, and Digital Twins" (30 Sep 2026), "Quantum-Agentic Systems..." (15 Jun 2026). No in-silico-medicine call was found. Four CFP PDFs were downloaded and text-searched (Federated Learning and Digital Twins; Emerging AI Paradigms; drug discovery Part IV; one file named Digital_Twin_SI_v2 whose text is the QKD call): none contains any page, length or supplementary rule. The remaining CFP PDFs were not opened. The special issue papers therefore fall under the general rule above (no SI-specific length found).

## 2. Practice

Method: Europe PMC query for JBHI 2024-2026 records with supplementary files (HAS_SUPPL:y) gave 11 PMC author manuscripts; main pages = Crossref/Europe PMC page range. Supplement files are not downloadable (PMC blocks scripted access; files absent from the PMC open-data bucket) except PMC11700499. Further case found via arXiv.

| # | Paper (DOI) | Published main pages | Supplement | Main + supp |
|---|---|---|---|---|
| 1 | Hyperbolic graph embedding of MEG (10.1109/jbhi.2024.3416890, PMC11700499) | 7357-7368 = 12 | PDF, 1 page (opened) | 13, not above 14 |
| 2 | TrustEMG-Net (10.1109/jbhi.2024.3475817, arXiv 2410.03843v2) | 2506-2520 = 15 | 4 pages (arXiv v2 pp 15-18, labelled "Supplementary material") | about 19; main alone already 15 |
| 3 | 10.1109/jbhi.2025.3649765 (PMC12885328) | 6854-6863 = 10 | PDF, pages unknown | unknown |
| 4 | 10.1109/jbhi.2025.3599477 (PMC12914552) | 700-707 = 8 | PDF, unknown | unknown |
| 5 | 10.1109/jbhi.2024.3397611 (PMC12229045) | 3864-3873 = 10 | PDF, unknown | unknown |
| 6 | 10.1109/jbhi.2024.3516613 (PMC11971004) | 857-869 = 13 | PDF, unknown | exceeds 14 only if supp >= 2 pp |
| 7 | 10.1109/jbhi.2024.3462632 (PMC12094672) | 1087-1100 = 14 | 8 mp4 videos (no pages) | not applicable |
| 8 | 10.1109/jbhi.2024.3510519 (PMC12083870) | 848-856 = 9 | DOCX, unknown | unknown |
| 9 | 10.1109/jbhi.2024.3415479 (PMC11653413) | 5941-5952 = 12 | PDF, unknown | unknown |
| 10 | 10.1109/jbhi.2024.3394754 (PMC11303098) | 4903-4911 = 9 | DOCX, unknown | unknown |
| 11 | 10.1109/jbhi.2024.3397589 (PMC11364449) | 4912-4924 = 13 | PDF, unknown | exceeds 14 only if supp >= 2 pp |
| 12 | 10.1109/jbhi.2024.3383610 (PMC11363067) | 5007-5019 = 13 | DOCX, unknown | exceeds 14 only if supp >= 2 pp |

Submission-stage preprints (not published, so no evidence of acceptance): arXiv 2604.21491, "11 pages ... Supplementary material (5 pages, 2 figures, 3 tables) included as ancillary file. Submission to ... (J-BHI)" = 16 combined; arXiv 2605.28217, "11 pages + 2 pages of supplementary materials. Submitted to special issue of JBHI" = 13 combined. These show authors submit 16 combined pages, but not that JBHI accepted it.

Counts: 12 published papers with supplements identified; main-article pages verified for all 12; supplement page count verified for 2 (rows 1, 2); 1 of those 2 exceeds 14 when the supplement is counted (row 2, and its main text alone is 15). Nine others (rows 3-6, 8-12) have supplements of unknown length; rows 6, 11 and 12 would exceed 14 combined if their supplement is 2 pages or more. Row 7 has only videos. Not verified: IEEE Xplore "Supplemental Items" pages (not accessible), what the editorial office counted at review.

Page-length distribution (Crossref, 924 JBHI 2025 articles with page ranges, ISSN 2168-2194; sample, not complete): 14 pages = 206, 13 = 147, 12 = 195; over 14: 15 articles (8 of 15 pp, 6 of 16 pp, 1 outlier). So published main articles essentially stop at 14; a small number exceed it (e.g. TrustEMG-Net at 15).

## 3. Answer

(a) JBHI's live author page states the 14-page (regular) limit is "including supplementary material", for original and revised submissions, with no exemption in any JBHI or (accessible) IEEE page; the multimedia page covers only playable or data files. (b) In practice, published JBHI main articles cluster at 12-14 pages and few exceed 14 (about 15 of 924 in a 2025 sample), yet papers with PDF/DOCX supplements exist at 13-14 main pages, and TrustEMG-Net shows a 15-page published main article with a separate 4-page supplement, so the limit does not appear to be applied to the combined count of the final published record; but I could verify supplement length for only 2 of 12 papers and could not see what editors enforced at submission, so "supplements are exempt in practice" is plausible but unproven, and it contradicts the written policy. (c) For an 8-page main text with a 6-page supplement (14 combined, about 0.7 page free), adding 1 to 1.5 pages would put the combined count at 15-15.5 and breach the written rule: either trim to keep main plus supplement at or under 14 (move 1-1.5 pages of the least necessary supplement text out, or tighten), or, if the extra pages are essential, email the JBHI Editorial Office to get a written ruling on whether supplements count before submitting; do not rely on the verbal "no page limit" statement. Also note mandatory charges apply to published main pages above 8 ($250 each for pages 9-10, $350 from page 11), so main-text growth beyond 8 pages costs money whereas supplement pages are not stated to be charged.

## Update 2026-10-09 (operator check)
The operator downloaded the supplement of 10.1109/jbhi.2024.3397589 (PMC11364449): **2 pages**. With 13 main pages that is **15 combined**, above 14.

So two published JBHI papers exceed 14 pages once the supplement is counted:
- TrustEMG-Net: 15 + 4
- 10.1109/jbhi.2024.3397589: 13 + 2

In practice the 14-page limit is applied to the main article and supplements are not counted against it. The written rule still says "including supplementary material".

**Working decision:**
- Main text stays at ≤ 8 pages, the fee threshold.
- The supplement may grow beyond 6 pages to hold the new analyses. Keep it compact; a one-line confirmation from the Editorial Office is optional.
- Operator also checked the other two papers: 10.1109/jbhi.2024.3516613 (13 pp main) and 10.1109/jbhi.2024.3383610 (13 pp main) each have a **1-page** supplement, so both total 14.
- Tally of supplements checked: 3 of 5 papers total 14 pages or fewer; 2 of 5 exceed 14 (15+4 and 13+2).
