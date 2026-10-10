# Paper 6 (T6) blind audit, 2026-10-09: scores

Input: submission-JBHI/upload Manuscript.pdf + Supplementary_Material.pdf (built 2026-10-08 23:05). Reviewers received only text + page images (input/). Rubric: RUBRIC.md. Reports: reports/.

| Dim | EIC | R1 Method | R2 Clinical | R3 Imaging | DA | Mean |
|---|---|---|---|---|---|---|
| S1 Novelty/contribution | 6 w | 7 p | 7 p | 7 p | 7 p | 6.8 |
| S2 Methodological rigour | 6 w | 6 w | 6 w | 6 w | 6 w | 6.0 |
| S3 Claims vs evidence | 6 w | 6 w | 5 w | 6 w | 6 w | 5.8 |
| S4 Domain/physiology | 7 w | 6 w | 5 w | 6 w | 6 w | 6.0 |
| S5 Internal consistency | 8 p | 8 p | 7 p | 8 p | 8 p | 7.8 |
| S6 Clarity/structure | 7 p | 7 p | 7 p | 7 p | 7 p | 7.0 |
| S7 Venue fit (JBHI) | 6 w | 7 p | 7 p | 6 w | 6 w | 6.4 |
| S8 Reproducibility | 5 w | 6 w | 6 w | 5 w | 6 w | 5.6 |
| Overall /10 | 6.4 | 6.6 | 6.0 | 6.4 | 6.4 | 6.4 |
| Recommendation | major | major | major | major | major | major revision |

No blocks.

## Convergent weaknesses (number of seats)
1. Topology vs caliber ranking (3-6x) is design-set: worst-case T1/T2 vs inter-observer-size caliber, no throat error, T3 loss length-independent (5/5).
2. Passes-and-wrong comparison is unequal: corrupted models tuned to clean targets, floor uses noisy targets; pass rates / P(wrong|pass) not reported (EIC, R1, DA).
3. Tuned excess holds only in discrete bed at x1 demand; abstract "directions held" overstates x2/x3 (R1, R2, DA).
4. Territory = first-bifurcation subtrees; too coarse to detect a missed diagonal (R2, DA).
5. Low flow regime / radius under-read; 3D case 80% DS with FFR 0.87 (R2).
6. Overlap-metric claim not measured (DSC/clDice/Betti on corrupted masks) (R3, EIC).
7. Code on request only; no DOI (EIC, R3).

## Text-level fixes (verified in the upload set)
- Fig. 3 caption "Protocol D residuals lie below 0.01" vs S2 (two models at 0.08, 0.11).
- IV: "After one global scaling, about half of [passers] were materially wrong": impossible in leaky bed (<=~16%).
- Abstract + IV "directions held at doubled ... demand": excess not significant at x2.
- B passes-and-wrong (discrete topological) shown as 1% / 1% / 2% with different denominators (S3, S5, text).
- p = 0.24 is Holm-adjusted (raw 0.121): label it.
- 3D −0.0007 is relative to prescribed-flow baseline 0.892; vs clean 0.870 it is +0.022.
- "LOGO" placeholder in page header (template logo.eps): check JBHI template expectation.
- No funding footnote.
