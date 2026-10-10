# Clarity review after the three-AI fix round (Fable, 2026-10-08)

Scope: `main.tex` / `main.pdf` (8 pp) read as a JBHI reader; seams checked against `main-backup-2026-10-08-pre-3ai-audit.tex` and the diff. Items already closed in `FABLE-FIX-AUDIT.md` are not repeated. Nothing was edited.

Rules applied: no numbers changed; no hashes, pre-registration, post hoc labels or script names; code stays on request; figures and tables remain cited in order; no new forward pointers. Word changes are body text unless marked (caption/footnote). "Current" text is quoted with `main.tex` line breaks removed.

Budget: all 25 items together add about 47 body words (about 4 lines) plus 6 caption words and 2 footnote words. The seven MUST items alone add 11 body words. Abstract items are net zero (abstract stays at 249 on the operator's count).

## Seam check (what the fix round changed)

- Methods outline paragraph removed. The study design is still given up front: Introduction ¶5 states one error at a time, fixed / re-derived / tuned boundary conditions, global or per-territory tuning, topological against caliber errors, the passes-and-wrong count and the 3D check. The only design element that no longer appears before II-B is the two bed structures (item 8). Opening II-A with the dataset is standard JBHI practice; no outline is needed.
- Introduction ¶5 last sentence (forward pointer) removed: clean.
- IV-A "Three findings stand out." removed but "First / Second / Third" kept: dangling ordinals (item 1).
- IV-C developer sentence removed: the four considerations still read as a list; clean.
- II-F pre-registration paragraph removed: the remaining two-sentence paragraph stands alone; clean.
- Abstract rewrite, Table I footnote, Limitations, Conclusion: grammatical and consistent with the body; residual clarity points are items 7, 15, 25.
- Results order follows Methods (flips, passes-and-wrong, side-branch magnitude, 3D, demand); each section opens with its point. Discussion ¶3 answers the Introduction's question in the measured terms (materially wrong), while Introduction ¶4 poses it as "misclassified" (item 10).

## Ranked list

### 1. MUST. IV-A, "First, with fixed boundary conditions…" / "Second, re-deriving…" / "Third, after tuning…"
Problem: the fix round deleted the lead-in "Three findings stand out.", so the ordinals now open three paragraphs with no frame.
Replace (three edits):
- `First, with fixed boundary conditions the decision risk of segmentation lay mainly in the branching` → `With fixed boundary conditions, the decision risk of segmentation lay mainly in the branching`
- `Second, re-deriving or tuning the bed reduced topological flips` → `Re-deriving or tuning the bed reduced topological flips`
- `Third, after tuning a passing perfusion check did not show that the FFR was correct.` → `After tuning, a passing perfusion check did not show that the FFR was correct.`
Net: −3 words.

### 2. MUST. II-E, "Three lumens were built: clean, …" and Fig. 1 caption, "Its clean, lesion and T1 models…"
Problem: everywhere else "clean" means the lesioned tree without segmentation error (II-C "clean tree", II-D "clean model", II-F "clean value"). In II-E and the Fig. 1 caption "clean" means the tree without the lesion. A reader who has just learned "clean" from II-A–II-D misreads the 3D design. (The supplement's S7 "the clean, baseline and missed-branch solves" has the same clash; outside this review's scope.)
Replace:
- II-E: `Three lumens were built: clean, with the lesion (baseline), and with the lesion and the missed branch (T1).` → `Three lumens were built: without the lesion, with the lesion (baseline), and with the lesion and the missed branch (T1).`
- Fig. 1 caption: `Its clean, lesion and T1 models were also solved in 3D.` → `This instance was also solved in 3D without the lesion, with the lesion, and with T1.`
Net: +2 body, +6 caption.

### 3. MUST. II-A, "The dataset contains few lesions…" and "Of the 6\,944 eligible instances…"
Problem: "clean" (about 30 uses) and "baseline FFR" (Fig. 2, III-A, III-D, Limitations) are never defined; the selection sentence also stacks four qualifiers ("25, in random order with a fixed seed, in each of six …, at most two per tree, giving …"). Three different unlesioned/lesioned states exist (FFR before insertion, healthy-equivalent network, clean model), so the reader needs the definition at first use.
Replace:
- `An instance is one lesion in one tree.` → `An instance is one lesion in one tree. Its clean model is the lesioned tree with no segmentation error.`
- `we drew 25, in random order with a fixed seed, in each of six 0.05-wide bands of leaky-bed baseline FFR from 0.65 to 0.95, at most two per tree, giving 150 instances` → `we drew 25, at random with a fixed seed, in each of six 0.05-wide bands of leaky-bed baseline (clean-model) FFR from 0.65 to 0.95, at most two per tree, giving 150 instances`
Net: +11 words.

### 4. MUST. II-B, "Each conductance depends on a healthy reference radius…"
Problem: "depends on a healthy reference radius $r_\mathrm{ref}$, the taper-fit radius $r_\mathrm{fit}$ made non-increasing along each path, and is scaled by" reads as a list of two radii; the appositive defines $r_\mathrm{ref}$.
Replace: `Each conductance depends on a healthy reference radius $r_\mathrm{ref}$, the taper-fit radius $r_\mathrm{fit}$ made non-increasing along each path, and is scaled by one bed constant $C_\mathrm{b}$.` → `Each conductance depends on a healthy reference radius $r_\mathrm{ref}$ (the taper-fit radius $r_\mathrm{fit}$ made non-increasing along each path) and is scaled by one bed constant $C_\mathrm{b}$.`
Net: 0.

### 5. MUST. II-F, "passes-and-wrong under tuning (C and D) is compared…"
Problem: the hyphenated noun that names Table I's column, III-B's heading and the Discussion appears here for the first time without a definition. Introduction ¶5 describes the idea but never attaches the term.
Replace: `passes-and-wrong under tuning (C and D) is compared with Protocol B by the same test.` → `passes-and-wrong (models passing the check while materially wrong) under tuning (C and D) are compared with Protocol B by the same test.`
Net: +7 words.

### 6. MUST. Introduction ¶2, "They stand in mainly for the microvascular bed…"
Problem: "Its resistance" follows a sentence whose subject is "They" (the boundary conditions), and "It is increasingly tuned" then has two candidates (resistance, model). "Heart muscle" is defined twice in three sentences.
Replace: `They stand in mainly for the microvascular bed, the arterioles and capillaries that set how much blood each region of heart muscle draws. Its resistance is not measured but derived from the segmented lumen through scaling laws that relate vessel size to the flow it carries \cite{murray1926,kim2010}. It is increasingly tuned so that the model reproduces measured perfusion, the blood flow to each region of heart muscle \cite{menon2024}, or measured flow splits \cite{arminio2026}.` → `They stand in mainly for the microvascular bed, the arterioles and capillaries that set perfusion, the blood flow to each region of heart muscle. The bed resistance is not measured but derived from the segmented lumen through scaling laws that relate vessel size to the flow it carries \cite{murray1926,kim2010}. It is increasingly tuned so that the model reproduces measured perfusion \cite{menon2024} or measured flow splits \cite{arminio2026}.`
Net: −6 words.

### 7. MUST. Abstract, "Re-derived or tuned boundary conditions reduced topological changes…"
Problem: "topological changes" reads as changes to the topology. The quantity is the decision-change rate for topological errors. Paired with a one-word cut so the abstract count is unchanged.
Replace:
- `reduced topological changes to 5--19\% (pooled)` → `reduced topological decision changes to 5--19\% (pooled)`
- `Fractional flow reserve, a pressure ratio that guides coronary revascularization, can be computed` → `Fractional flow reserve, a pressure ratio guiding coronary revascularization, can be computed`
Net: 0 (abstract stays at 249).

### 8. SHOULD. Introduction ¶5, "it solves the same corrupted anatomy under fixed…"
Problem: with the Methods outline gone, the two bed structures are the one design element the reader meets only in II-B, after the abstract has already used them.
Replace: `with one global or one per-territory tuning parameter, and separates topological from caliber errors of inter-observer magnitude;` → `with one global or one per-territory tuning parameter and in two microvascular bed structures, and separates topological from caliber errors of inter-observer magnitude;`
Net: +6 words.

### 9. SHOULD. Introduction ¶4, "None of these studies compares fixed, re-derived and tuned…"
Problem: "re-derived" is used in the abstract, ¶4 and ¶5 before II-D defines it; a non-CFD reader cannot tell it from "tuned".
Replace: `None of these studies compares fixed, re-derived and tuned boundary conditions on the same corrupted anatomy at 0.80,` → `None of these studies compares fixed, re-derived (derived anew from the segmented tree) and tuned boundary conditions on the same corrupted anatomy at 0.80,`
Net: +5 words.

### 10. SHOULD. Introduction ¶4, "…or tests whether a tuned model can pass a perfusion check while misclassified."
Problem: the question is posed as "misclassified" (a flip) but the outcome measured and answered in III-B and IV-A is "materially wrong" (|ΔFFR| > 0.05, not conditional on a flip). ¶5 already uses the measured wording.
Replace: `or tests whether a tuned model can pass a perfusion check while misclassified.` → `or tests whether a tuned model can pass a perfusion check while its FFR is wrong.`
Net: +3 words.

### 11. SHOULD. II-B, "In the discrete bed, flow leaves only at the outlets…"
Problem: one sentence carries the truncation radius, its justification, the conductance law, the exponent, its physiological source and the resulting interpretation.
Replace: `with conductance $r_\mathrm{ref}^{2.66}/C_\mathrm{b}$, where 2.66 is close to 8/3, the inverse of the 3/8 power that relates coronary vessel diameter to the myocardial mass it perfuses \cite{choy2008}, so that outlet flow is taken as proportional to perfused mass.` → `with conductance $r_\mathrm{ref}^{2.66}/C_\mathrm{b}$. The exponent is close to 8/3, the inverse of the 3/8 power that relates coronary vessel diameter to the myocardial mass it perfuses \cite{choy2008}, so outlet flow is proportional to perfused mass.`
Net: −3 words.

### 12. SHOULD. II-F, "For each instance, this is the probability that a repeat invasive FFR, normal about the clean value…"
Problem: the subject "a repeat invasive FFR" is separated from its verb "falls" by a nested qualifier with a parenthesis and a citation.
Replace: `For each instance, this is the probability that a repeat invasive FFR, normal about the clean value (the first measurement) with the published standard deviation of the test--retest difference, 0.018 \cite{johnson2015}, falls on the other side of 0.80, following the measurement-certainty approach of \cite{petraco2013}.` → `For each instance, this is the probability that a repeat invasive FFR falls on the other side of 0.80, following the measurement-certainty approach of \cite{petraco2013}: the repeat is normal about the clean value, taken as the first measurement, with the published standard deviation of the test--retest difference, 0.018 \cite{johnson2015}.`
Net: +3 words.

### 13. SHOULD. II-F, "…so the 10\% threshold is conservative."
Problem: "conservative" has no fixed direction for a pass threshold; the abstract and Conclusion call the same check "stricter than measurement repeatability". One wording throughout. (CX-13 introduced "conservative"; the operator may prefer to keep it.)
Replace: `so the 10\% threshold is conservative.` → `so the 10\% threshold is stricter than measurement repeatability.`
Net: +3 words.

### 14. SHOULD. II-F, "Instances are clustered within patients, so these intervals are descriptive; a Bayesian…"
Problem: semicolon joins two long clauses; "these intervals" is loose.
Replace: `Instances are clustered within patients, so these intervals are descriptive; a Bayesian mixed-effects logistic model` → `Instances are clustered within patients, so the confidence intervals are descriptive. A Bayesian mixed-effects logistic model`
Net: 0.

### 15. SHOULD. Table I footnote, "over models with a defined residual (T2 under B in the discrete bed, $n = 60$; …)"
Problem: the parenthesis lists cells and $n$ values without saying that these are the cells where the passes-and-wrong denominator differs from the flip $n$.
Replace: `over models with a defined residual (T2 under B in the discrete bed, $n = 60$; T2 under A and B in the leaky bed, $n = 100$).` → `over models with a defined residual, which reduces $n$ for T2 to 60 under B in the discrete bed and to 100 under A and B in the leaky bed.`
Net: +2 words (footnote).

### 16. SHOULD. III-A ¶3, "However, where tuning was defined, only 22\% of re-derived topological-error models…"
Problem: "their own perfusion check" suggests each model has a check of its own; the check is the one defined in II-F.
Replace: `passed their own perfusion check.` → `passed the perfusion check.`
Net: −1 word.

### 17. SHOULD. III-B ¶1, "Fitting one bed scaling to the clean territory flows (Protocol C) lowered…"
Problem: "relative to Protocol A" appears twice in one sentence, with "(same instances)" and the flip result attached by a comma.
Replace: `lowered the median perfusion residual of topological-error models relative to Protocol A from 0.22 to 0.14 in the discrete bed and from 0.11 to 0.02 in the leaky bed (same instances), and reversed more topological flips than it created relative to Protocol A (significant for leaky vessel breaks, $p < 0.001$). Relative to Protocol B, it changed at most two topological-error decisions per cell ($p \geq 0.5$).` → `lowered the median perfusion residual of topological-error models from 0.22 under Protocol A to 0.14 in the discrete bed and from 0.11 to 0.02 in the leaky bed, on the same instances. It reversed more topological flips than it created relative to Protocol A (significant for leaky vessel breaks, $p < 0.001$) and changed at most two topological-error decisions per cell relative to Protocol B ($p \geq 0.5$).`
Net: +3 words.

### 18. SHOULD. III-B ¶2, "Models with correct anatomy, tuned to perfusion measured with physiological noise…"
Problem: nothing was measured; this is the second (simulated) noise floor of II-F, and the sentence does not say so.
Replace: `Models with correct anatomy, tuned to perfusion measured with physiological noise, passed while materially wrong` → `Models with correct anatomy, tuned to perfusion targets carrying simulated physiological noise (the second floor), passed while materially wrong`
Net: +4 words.

### 19. SHOULD. III-D, "In the cohort model of the same instance (discrete bed)…"
Problem: "cohort model" is undefined; the reader must infer that it is the reduced-order model on the original radius, as distinct from the "reduced-order counterpart" on the meshed radius in the previous sentence.
Replace: `In the cohort model of the same instance (discrete bed), the error gave` → `In the cohort's reduced-order model of the same instance (discrete bed, reduced-order radius), the error gave`
Net: +3 words.

### 20. SHOULD. III-E, "With $k$ doubled and tripled, the sweep, cohort selection…"
Problem: "the sweep" is never named in the main text (it is the 6 944-instance lesion insertion of II-A).
Replace: `the sweep, cohort selection and all four protocols were repeated` → `the lesion insertion, cohort selection and all four protocols were repeated`
Net: +1 word.

### 21. SHOULD. IV-A ¶2, "…per-territory tuning restored, by construction of the targets, the flow…"
Problem: semicolon joins two long clauses and the parenthetical interrupts verb and object. Applies after item 1.
Replace: `per error type; per-territory tuning restored, by construction of the targets, the flow that the missing branch had carried through the stenosis, in the cohort and in the 3D case.` → `per error type. Per-territory tuning restored the flow that the missing branch had carried through the stenosis, in the cohort and in the 3D case, by construction of its targets.`
Net: 0.

### 22. SHOULD. IV-A ¶3, "…under either form of tuning; after one global scaling, about half of the passing models were. In both beds tuning produced passing models with caliber errors that re-derived models did not…"
Problem: the elliptical "were" leaves the predicate to be recovered across a semicolon; "passing models with caliber errors that re-derived models did not" needs two readings to parse.
Replace: `under either form of tuning; after one global scaling, about half of the passing models were. In both beds tuning produced passing models with caliber errors that re-derived models did not, because` → `under either form of tuning. After one global scaling, about half of the models that passed were materially wrong. In both beds tuning turned caliber errors into passing models with a wrong FFR, which re-derivation did not, because`
Net: +6 words.

### 23. SHOULD. IV-A ¶4, "Bed structure set the magnitude, the leaky bed damping topological errors; their excess…"
Problem: absolute clause plus semicolon; "their" has to reach back past "the leaky bed".
Replace: `Bed structure set the magnitude, the leaky bed damping topological errors; their excess of passes-and-wrong over re-derived boundary conditions held only in the discrete bed.` → `Bed structure set the magnitude. The leaky bed damped topological errors, and their excess of passes-and-wrong over re-derived boundary conditions held only in the discrete bed.`
Net: +1 word.

### 24. SHOULD. IV-C ¶2, "Third, record the perfusion mismatch before tuning; in the discrete bed only 22\%…"
Problem: the recommendation and the statistic after the semicolon are not connected; the reason (tuning erases the mismatch) appears only in the Conclusion.
Replace: `Third, record the perfusion mismatch before tuning; in the discrete bed only 22\% of re-derived topological-error models passed, although in the leaky bed most did.` → `Third, record the perfusion mismatch before tuning, which erases it: in the discrete bed only 22\% of re-derived topological-error models passed, although in the leaky bed most did.`
Net: +3 words.

### 25. SHOULD. Conclusion, "With fixed boundary conditions, missed branches and vessel breaks changed the decision…"
Problem: a 70-word sentence carrying two findings, a colon, a parenthesis and a comparison.
Replace: `as often as caliber errors of inter-observer size, and tuning the boundary conditions to perfusion reduced these changes without making the models correct: in the discrete bed up to one in five` → `as often as caliber errors of inter-observer size. Tuning the boundary conditions to perfusion reduced these changes without making the models correct: in the discrete bed, up to one in five`
Net: −1 word.

## Minor, not ranked (apply only if space remains)

- II-A: "the taper-fit radius $r_\mathrm{fit}$ (a linear fit)" does not say what is fitted; "(a linear fit of radius along the vessel)" would (+4).
- II-D: "Both match flow only" follows a sentence about instances; "Both protocols match flow only" (+1).
- II-D: "It is the quantity a perfusion check compares with the measurement" describes the residual as the input of the check rather than its output; "It is the mismatch that a perfusion check reports" (−3).
- Abstract: "tripled demand" is the only use of "demand" with no noun; "tripled hyperemic demand" (+1) paired with "does not show that the computed value" → "does not show the computed value" (−1).
- Terminology drift, harmless but noticeable: "fixed resistance" (III-C title, IV-B) against "fixed boundary conditions" elsewhere; "the bed" (IV-A ¶2) for the boundary conditions; "perfusion mismatch" (IV-C, Conclusion) for the perfusion residual.
- Limitations last sentence joins two unrelated limitations with a semicolon; a full stop after "dataset" works.
