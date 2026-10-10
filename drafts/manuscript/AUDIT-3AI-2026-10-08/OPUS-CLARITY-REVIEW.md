# Opus clarity review: main text after the audit fixes (2026-10-08)
Written before Fable's review was read, so the two are independent.

| # | Location | Problem | Proposed fix | Words |
|---|---|---|---|---|
| O1 MUST | Methods opening | The audit-fix cut removed the outline, so Methods starts at Data and never states the design first. | Restore a 2-sentence design overview before II-A, citing Fig. 1. | +35 |
| O2 MUST | II-A | "Clean model" and "baseline FFR" are used everywhere but never defined. In this paper the clean model *includes* the inserted lesion. | After "An instance is one lesion in one tree": "Its clean model is the tree with the inserted lesion and no segmentation error, and the FFR of that model is the baseline FFR." | +22 |
| O3 MUST | II-F | "Passes-and-wrong" is used in Results, Table I and Fig. 3 but is never named in Methods. | After the materially-wrong definition: "A model that passes the check while materially wrong is counted as passes-and-wrong." | +14 |
| O4 SHOULD | IV-A third finding | "about half of the passing models were." ends on an elliptical "were". | Spell out: "… were materially wrong". | +2 |
| O5 SHOULD | IV-A bed paragraph | "the leaky bed damping topological errors; their excess …" makes "their" ambiguous. | "Bed structure set the magnitude: the leaky bed damped topological errors, and the excess of passes-and-wrong over re-derived boundary conditions for these errors held only in the discrete bed." | +4 |
| O6 SHOULD | IV-C third consideration | A semicolon, and the evidence does not show why recording the mismatch helps. | "Third, record the perfusion mismatch before tuning. In the discrete bed it flagged 78% of re-derived topological-error models, although in the leaky bed few." | +3 |
| O7 SHOULD | Intro ¶1 | "revascularization" appears twice in two sentences. | "FFR is a pressure ratio that guides the treatment of a coronary narrowing." | 0 |
| O8 SHOULD | Abstract | "a perfusion-matched model can be misclassified" makes it unclear what is misclassified. | "… can misclassify a stenosis at 0.80" | +1 |
| O9 SHOULD | II-B | "where r_in is the inlet radius and the cube law is Murray's [7]" repeats the [7] citation from three sentences earlier. | Drop "and the cube law is Murray's \cite{murray1926}". | −6 |
| O10 SHOULD | II-F | "that is, a change in the treatment decision" says more than "guides" supports. | "that is, a change in the indicated treatment" | 0 |
