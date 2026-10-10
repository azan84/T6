# Co-author comments on the 2026-10-10 reading copy (Paper 6, JBHI)

Record of the co-authors' critical revision (ICMJE criterion 2). One entry per comment: who, what, and how it was resolved.

| # | Co-author | Location | Comment (verbatim) | Resolution |
|---|---|---|---|---|
| C1 | M. A. Mohammed Sapardi and M. K. Tan (raised independently by both) | Conclusion, last sentence; cover letter, Significance | "The same test, built on public data and open code, can be applied to other segmentation and boundary-condition pipelines. — what does it mean? which open code? what test?" | The sentence now reads: "The released analysis code allows the same test to be replicated for other segmentation errors and boundary-condition pipelines." It refers back to the test defined in the Conclusion's first sentence. "Segmentation pipelines" was an overclaim, since the test injects errors rather than running other segmenters, so it is now "segmentation errors". The cover letter carries the same sentence. The code repository now holds the four scripts behind the noise-matched comparison and the Fig. 4 throat-error overlap, each verified to reproduce the reported results exactly, and its README has the current title and terms. |
