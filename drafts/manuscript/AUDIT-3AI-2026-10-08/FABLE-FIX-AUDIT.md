# Fix audit of the three-AI revision (Fable, 2026-10-08)

Scope: the 119 findings in `AUDIT-main-2026-10-08.xlsx` (sheet Findings), judged on the current `main.tex` / `supplement.tex` / `refs.bib` and the compiled PDFs (22:14–22:16 builds; the supplement re-read after the operator's pipeline-figure edit). The plan (`FIX-PLAN.md`) was used only to see the intended action. Operator rules applied: hashes, pre-specification and post hoc labels are not reported; code stays on request; net page-neutral.

## Summary verdict: READY WITH MINOR FIXES

Build and limits: main 8 pp, supplement 6 pp, abstract 246 words (whitespace count; 247 counting "−0.0007" separately), no undefined references or citations in either log, overfull count unchanged (9 main, 7 supplement; the 301 pt `\hbox` is the IEEEtran `\output` warning, not text). Citations run [1]–[33] in first-appearance order; multi-citations are sorted and compressed ([3]–[6], [4], [7], [10]–[13], [14]–[16], [18], [22], [23]). Figures and tables are cited in order (Fig. 1 in II-C, Table I and Fig. 2 in III-A, Fig. 3 in III-B, Fig. S3 and Fig. 4 in III-C/III-D). No cite key, `\ref` or number was dropped unintentionally (the only dropped numbers are the planned III-E cut 0.931/0.845/0.776, and 2.3 → 2.28). No residual mention of hash, frozen cohort, pre-specification, post hoc, exploratory or "secondary" remains in either file.

Numbers verified against data and code (all correct):
- Median demand over the 150 selected instances (`sweep_test_selected.csv`, k = 562 s⁻¹): median r_in 1.595 mm, 2.2805 mL/s = 136.8 mL/min → "2.28 mL/s (137 mL/min)".
- Protocol B pass rate where tuning was defined (`ablation-2026-10-07.csv`, discrete arm filtered by `discrete_arm_eligibility.csv`): 23/104 = 22.1 % discrete, 152/171 = 88.9 % leaky → "22 % and 89 %".
- "About half of the passing models were [materially wrong]" after Protocol C, discrete bed: 39 topological-error models passed, 20 were wrong = 51 %.
- Passes-and-wrong on the same instances: A 13/104 and 38/171 (13 %, 22 %); B 2/104 and 10/171 (2 %, 6 %).
- Taper lower bounds: T4/A discrete 13 (8–22), T4/D discrete 14 (9–23) exceed the 5.0–6.5 % floor; T4/A leaky 9 (6–15) does not and is now omitted.
- Protocol C scales the re-derived bed: `ablation.py` l.357 `C_start = t2.calibrate(...)` on the corrupted tree, grid ±1.5 decades, 61 points.
- T2 counts: "skipped: truncation point at segment start" 1 per bed; "no bed left" under A 36 discrete, 2 leaky; B solved 96/149; C and D 60/100.
- Protocol D: 769 solves, all converged, 2 fits at the 10³ bound (scan 984, residuals 0.083 and 0.111), 2 residuals ≥ 0.01 → "within 1 % in all but two".
- 3D case (`cfd_M1`, `ablation-perterritory`): 3D 0.870 → 0.944 (+0.074); prescribed 0.8923/0.8916 (−0.0007, "0.892 in both"); 0D on meshed radius +0.081 and −0.0005, baseline within 0.011; 0D on reduced-order radius 0.761; cohort model A +0.127, C +0.107 with residual 0.30, D −0.000695.
- Demand replication ranges in III-E (33–50 %, 1–5 %, 3–20 %, 1–14 %, 2–5 %, 0 %) match `summary_k2/k3.txt`.
- Grey zone 20 % / 23 % matches `grey_zone.csv`.
- Supplement S1 sampling matches `severity_sweep.select` (shuffle with seed 20260918, scarcest band first, permuted vessel rotation, ≤ 2 per tree, one per host vessel and band, bands on leaky-bed FFR). Solver sentence matches `zerod_ffr._solve` (max_iter 200, tol 10⁻⁸ relative to the largest flow, Q = 0.5(Q + Qn)); the initial guess is Q = 0, whose first linear solve is the Poiseuille solution, so "starts from Poiseuille flow" is acceptable.
- Reference [12] renders "FFR_CT,”" with no space (verified on the rendered page; the "FFRCT ," in extracted text is a pdftotext artefact).

## Must-fix problems (ranked; all length-neutral unless stated)

1. **Limitations, comma splice (new text).** Current: "Errors were applied one at a time in one dataset, tuning targets were error-free clean-model flows (noise entered only the simulated floor)."
   Replace with: "Errors were applied one at a time in one dataset; tuning targets were error-free clean-model flows (noise entered only the simulated floor)."

2. **Abstract, "reduced these to 5–19 % (pooled)" (AG-01/CL-28 fix).** "These" now reads as both error classes, but pooled caliber flips under B–D are 1–11 %, so the range is only correct for the topological class. Current: "Re-derived or tuned boundary conditions reduced these to 5--19\% (pooled)."
   Replace with: "Re-derived or tuned boundary conditions reduced topological changes to 5--19\% (pooled)." (+1 word; abstract 247.)

3. **Abstract, dangling "it" (new text).** "…applied four segmentation errors (…), and recomputed it with a reduced-order model" has no antecedent in the sentence (the previous sentence's subject is "a perfusion-matched model"). Replace "recomputed it" with "recomputed FFR" and define the abbreviation in the first sentence: "Fractional flow reserve (FFR), a pressure ratio that guides coronary revascularization, …" (+1 word; abstract 248 with item 2, within 250.)

4. **III-A, "only … 89 %" (CX-19 fix).** Current: "However, where tuning was defined, only 22\% (discrete) and 89\% (leaky) of re-derived topological-error models passed their own perfusion check."
   Replace with: "However, where tuning was defined, only 22\% of re-derived topological-error models in the discrete bed (89\% in the leaky bed) passed their own perfusion check." (same length.)

5. **II-F noise floor, distribution family dropped (AG-28 fix).** Current: "the probability that a repeat invasive FFR, with the clean value as the first measurement and the published standard deviation of the test--retest difference, 0.018 \cite{johnson2015}, falls on the other side of 0.80".
   Replace "with the clean value as the first measurement and" by "normal about the clean value (the first measurement) with" (same word count): "…a repeat invasive FFR, normal about the clean value (the first measurement) with the published standard deviation of the test--retest difference, 0.018 \cite{johnson2015}, falls on the other side of 0.80…".

Optional (not required for readiness):
- Supplement S6 says "the published standard deviation of repeat invasive FFR, 0.018"; the main text now says "standard deviation of the test–retest difference". For consistency: "the published standard deviation of the test--retest difference in invasive FFR, 0.018" (supplement page 6 has room).
- II-B still contains the forward pointer "(Section~\ref{sec:demand})"; pre-existing, not introduced by the fixes.

## Per-finding verdicts

Legend: R = RESOLVED, P = PARTIAL, N = NOT ADDRESSED, DJ = DECLINED-JUSTIFIED, DU = DECLINED-UNJUSTIFIED.

| ID | Verdict | Current text / note |
|---|---|---|
| AG-01 | R (see must-fix 2) | Abstract "reduced these to 5--19\% (pooled)"; the pooled label resolves the aggregation mismatch, but "these" should read "topological changes". |
| CX-03 | R | Abstract: "one global or per-territory parameter fitted to clean-model territory flows"; II-D: targets "stand in for an error-free perfusion measurement"; Limitations: "tuning targets were error-free clean-model flows". |
| AG-02 | DJ | "corrected the typical missed branch" kept; median D shift 0.000/0.004 and III-C gives "10 of 44 and 3 of 71 … remained above 0.05". |
| AG-03 | DJ | Abstract cap; Table I gives T4/D 36 (27–46). |
| CL-08 | R | Abstract: "The directions held at doubled and, in the leaky bed, tripled demand."; III-E states the non-significant topological excess. |
| CX-01 | R | Abstract: "a pressure ratio that guides coronary revascularization". |
| CX-02 | R | "We tested in silico whether a perfusion-matched model can be misclassified at 0.80." ("untested" removed; JBHI norm, no "to our knowledge"). |
| AG-04 | R | "…vessel radius and length [17]. In a recent coronary benchmark, every evaluated method produced vessel breaks despite high overlap scores [18], and small distal segments remain the hardest to segment [19]." |
| AG-05 | R | "F. Yamin, X. Wang, and M.-Z. Ismadi are with…". |
| AG-06 | R | "the mean blood pressure beyond the narrowing divided by the mean aortic pressure during maximal flow". |
| CL-28 | R | Same as AG-01 ("(pooled)"); IV-A keeps "2--20\% per error type". |
| CL-29 | R | "in discrete and leaky (distributed-outflow) microvascular beds". |
| CL-30 | DJ | Abstract cap; II-B gives "97 instances". |
| CL-31 | R | "in one three-dimensional case it reduced a shift of 0.074 to −0.0007". |
| CL-32 | R | Abstract "guides"; Introduction "a pressure ratio used to decide on coronary revascularization" (wording varied). |
| CL-40 | R | `\usepackage{cite}`: "[4], [7]", "[18], [22], [23]", "[10]–[13]", "[14]–[16]" in the PDF. |
| CL-41 | P | "measured perfusion … [8], or measured flow splits [9]": each source now backs its own clause, but [9] (pulmonary-valve FSI) still sits in a paragraph about coronary bed resistance; defensible as an example of tuning to measured flow splits, kept for JBHI fit. |
| CL-42 | R | "specific implementations of the computed FFR have been validated against invasive measurement in a multicenter trial [2]"; [3] moved to the 3D-form citation. |
| CX-04 | P | Scoped to "specific implementations … in a multicenter trial"; no explicit sentence that the present model is not clinically validated (Limitations say "No invasive FFR was available"). Acceptable. |
| AG-07 | R | The outline sentence with "three boundary-condition protocols" was deleted; II-D: "Each corrupted tree was solved under four protocols." |
| CX-05 | R | "whose FFR serves as the reference value". |
| AG-08 | R | Leaky "0.50 mm, near the mask resolution"; discrete "0.60 mm, the cut that kept a side branch beyond most lesions". |
| AG-09 | R | "for $|s-c|<L/2$ ($r'=r$ elsewhere; DS as a fraction)". r written as scalar on the RHS (minor, unchanged). |
| CL-03 | R | As AG-07. |
| CL-06 | R | II-A "the taper-fit radius $r_\mathrm{fit}$ (a linear fit)"; II-B "a healthy reference radius $r_\mathrm{ref}$, the taper-fit radius $r_\mathrm{fit}$ made non-increasing"; S1 and Fig. S2 say "taper-fit radius". |
| CL-13 | R | "Of the 6\,944 eligible instances"; S1 explains why a host vessel contributes fewer than 32. |
| CX-06 | R | "we drew 25, in random order with a fixed seed, in each of six 0.05-wide bands of leaky-bed baseline FFR"; S1 gives the algorithm and seed (20260918), verified against `severity_sweep.select`. |
| CX-07 | P | "Instances are clustered within patients, so these intervals are descriptive; a Bayesian mixed-effects logistic model … agreed with the paired tests". No cluster bootstrap (JBHI benchmark decision; justified). |
| CX-08 | R | S1: "starts from Poiseuille flow, averages successive flow iterates with a relaxation factor of 0.5, and stops when the largest flow change falls below $10^{-8}$ of the largest flow or after 200 iterations" (matches `_solve`). |
| AG-10 | R | "native narrowing relative to $r_\mathrm{fit}$ was below 40\% diameter stenosis". |
| AG-11 | R | "where 2.66 is close to 8/3". |
| AG-12 | R | "3.7~mm \cite{dodge1992} carries 214~mL/min". |
| AG-13 | DJ | Rejected by both cross-checkers; $r'$ kept. |
| AG-14 | R | "an expansion loss … is lumped at the stenosis". |
| AG-15 | DJ | IEEEtran convention (journal name on even pages, authors on odd); rejected by both cross-checkers. |
| CL-14 | R | "150 instances (50 each in the LAD, LCx and RCA) in 108 trees from 93 patients"; "140 patients" (one scan per patient). |
| CL-35 | R | As AG-04. |
| CL-36 | R | As AG-12. |
| CL-37 | R | "The two annotators agreed with a Dice similarity coefficient". |
| CL-39 | R | As AG-11. |
| CX-09 | P | II-C: "T1 and T2 have no measured magnitude and are design choices, so the topological results are conditional on them."; Limitations repeat it. No sensitivity over branch size/break distance (page cap; justified). |
| CX-10 | R | II-D: "reproduces the clean model's territory flows, which stand in for an error-free perfusion measurement"; Limitations: "(noise entered only the simulated floor)". |
| AG-17 | R | Table I footnote: "T2 was not applicable to one instance per bed"; S2: "the 25~mm truncation point fell at the start of a centerline segment". |
| AG-18 | R | T1 definition: "and is possible only where such a branch exists"; parenthetical removed from the RCA sentence. |
| AG-19 | DJ | Generic territory definition; RCA exclusions stated ("all but four in the RCA"; Limitations). |
| AG-23 | R | "radius ratio $\lambda$ of two coaxial cylinders, $2\lambda^2/(\lambda^2+1) = 0.928$". |
| CL-04 | R | Bed constant is $C_\mathrm{b}$ throughout main and supplement (no bare $C$ left); "(one bed scaling)" deleted. |
| CL-05 | R | As AG-23. |
| CL-15 | P | "bands of leaky-bed baseline FFR" names the bed; band distribution of the 97 discrete instances not reported (minor). |
| CL-18 | R | "HD95 (2.46~mm), which bounds the disagreement in lesion extent, sets T3." (brief justification; no explicit limitation). |
| CX-11 | R | "a fit at the edge of the range was a failure (none occurred)"; D "fitted (within $10^{\pm 3}$)"; S2 reports the two 10³ fits (residuals 0.08, 0.11, retained). Verified in data. |
| CX-12 | R | Fig. 1: "Its clean, lesion and T1 models were also solved in 3D." |
| AG-16 | R | "2.28~mL/s (137~mL/min)" (verified 2.2805 mL/s = 136.8 mL/min). |
| AG-20 | R | "re-inserts the same stenosis 2.46~mm longer about the same center". |
| AG-21 | R | II-E renamed "Three-Dimensional CFD Setup"; III-D keeps "Three-Dimensional Case Study". |
| AG-22 | R | "one global scaling of the re-derived $C_\mathrm{b}$" (verified in `ablation.py`). |
| AG-24 | R | "(a) The tree with the host LAD in blue, an inserted 80\% DS proximal lesion and the measurement point 20~mm beyond it." |
| AG-25 | R | "(c) T2 ends the host vessel 25~mm beyond the distal edge of the lesion; the red part is lost." |
| CL-17 | R | "(none occurred)" plus S2 ("none did in the ablation or in the demand runs … 10 of 4\,940 noise-floor draws did"). |
| CL-19 | R | "The taper (T4), a uniform narrowing, multiplies the radius by 0.930 …". |
| CL-38 | R | As AG-16. |
| CL-48 | R | "so this is the least flexible tuning tested". |
| CX-13 | R | "implies a 95\% bound of about $1.96 \times (10$–$15\%) \approx 20$–29\% … so the 10\% threshold is conservative. Thresholds of 13\% and 16\% were analyzed as sensitivities." Modality not named (minor). |
| AG-28 | R (see must-fix 5) | "with the clean value as the first measurement and the published standard deviation of the test--retest difference, 0.018"; consistent with N(clean, 0.018²) draws, but the normal family is no longer stated. |
| CL-16 | R | Footnote: "under A it removed every bed node in 36 discrete and 2 leaky instances, whereas under B the new vessel end carries outflow"; III-A duplicate clause removed. |
| CL-20 | DJ | Operator rule (JBHI norm): pre-specification and hash sentences removed; "frozen cohort" → "cohort". |
| CL-21 | DJ | Operator rule: no post hoc label; "Protocol D … run after the primary results" sentence removed. |
| CX-14 | P | As CX-07 (caveat added; Wilson intervals labelled descriptive). |
| CX-15 | P | Main text: one-sentence model summary with random effects defined; S4 gives estimates and "Fitted by variational inference", but no priors or convergence diagnostics. Acceptable for JBHI. |
| CX-16 | DJ | As CL-21. |
| CX-17 | DJ | As CL-20. |
| AG-26 | R | "flipped at similar rates (8\% and 11\% discrete, 6\% and 4\% leaky)". |
| AG-27 | R | "Only the taper exceeded this noise floor with its lower confidence bound, in the discrete bed under fixed boundary conditions (13\%) and Protocol D (14\%)." (leaky 9 % dropped; verified). |
| AG-29 | DJ | III-D: "A finer throat zone (12.5~\textmu m) changed the baseline FFR by at most 0.0021" on the patient geometry. |
| AG-30 | DJ | As CL-20. |
| AG-31 | R | "lesion-slot (host vessel, position and length) random effects". |
| CL-22 | R | "$|\Delta\mathrm{FFR}| > 0.05$, half the width of the 0.75--0.85 grey zone \cite{petraco2013}". |
| CL-24 | R | As AG-27. |
| CL-25 | P | "similar rates"; sign-test p for D (0.58, 0.79) not given. Minor. |
| CL-26 | R | "no caliber-error flip under fixed boundary conditions ended outside the zone". |
| AG-32 | R | Footnote: "$n$ is its denominator … over models with a defined residual (T2 under B in the discrete bed, $n = 60$; T2 under A and B in the leaky bed, $n = 100$)" (annotated in the table rather than separate columns; JBHI norm). |
| AG-33 | R | Footnote explains the 36 (and 2) instances with no bed node under A. |
| CL-07 | R | "Of Protocols A--C, re-deriving the boundary conditions (Protocol B) produced the fewest flips." (verified per cell). |
| CL-10 | R | "The 3D case agreed with the reduced-order result in direction, and prescribed flows removed the error in both." |
| CX-18 | R | As AG-32. |
| CX-19 | R (see must-fix 4) | "only 22\% (discrete) and 89\% (leaky) of re-derived topological-error models passed their own perfusion check" (numbers verified: 23/104, 152/171). |
| CX-21 | R | "Almost all were taper models in which tuning lowered FFR: forcing the clean flow through a uniformly narrowed lumen raises its pressure drop". |
| CX-22 | R | As CL-10. |
| CL-11 | DJ | Verified: cohort D ΔFFR = −0.000695; the match with 3D −0.0007 is real. |
| CL-12 | R | "on the reduced-order radius the baseline was 0.761". |
| CL-23 | P | Covered by the generic "intervals are descriptive" sentence; within-instance clustering of the 20 draws not named. Minor. |
| CX-20 | R | "Tuning raised these proportions relative to B in the discrete bed". |
| AG-34 | R | "after one global scaling, about half of the passing models were [materially wrong]" (20 of 39 = 51 %). |
| CL-27 | R | As AG-34 (counts not printed; III-B gives 20 of 104). |
| CX-24 | R | Abstract "doubled and, in the leaky bed, tripled demand"; III-E "the discrete arm is reported at twice the demand only". |
| CL-44 | R | Fig. 2 caption "protocol (A--C; D in Table~I)". |
| CX-23 | DJ | Fig. 3 pools T1 and T2 by design; Table I gives n; caption states Protocols A–C. |
| AG-35 | R | "(the taper up to 14\%)". |
| AG-36 | P | "($+0.127$ against $+0.081$ on the meshed radius)"; the 3D +0.074 is not restated here but is in III-D. Acceptable. |
| CL-09 | R | "are both consistent with our results … so the boundary-condition protocol alone can produce both behaviors". |
| CL-33 | R | Limitations now add one-error-at-a-time, single dataset, error-free clean-model targets; "No invasive FFR was available"; post hoc omitted by operator rule. (See must-fix 1 for the comma splice.) |
| CX-25 | R | "per-territory tuning restored, by construction of the targets, the flow that the missing branch had carried". |
| CX-26 | R | "the results suggest four considerations … These considerations follow from the results but are not validated decision rules." |
| CL-43 | DJ | Verified: `fig5_case3d.py` labels the axis $p/P_\mathrm{a}$; "p/Pa" is an extraction artefact. |
| CL-46 | R | As AG-35. |
| CL-01 | R | Conclusion: "in the discrete bed up to one in five tuned topological-error models (5--8\% in the leaky bed) passed … against 3--4\% for correct anatomy". |
| CL-02 | R | "The results point to where safeguards are likely to matter most". |
| CL-34 | DJ | Operator decision: "The code is available from the corresponding author upon reasonable request." |
| CL-47 | R | "With fixed boundary conditions, missed branches and vessel breaks changed the decision three to six times as often". |
| CX-27 | R | "Applied to 150 inserted stenoses in 108 trees". |
| CX-28 | R | "The same test can be adapted to other segmentation and boundary-condition pipelines". |
| CX-29 | DJ | As CL-34. |
| CX-31 | P | As CL-41. |
| AG-37 | R | Bib title "FFR\textsubscript{CT}"; rendered "FFR_CT,”" with no space (checked on the rendered page). |
| AG-38 | DJ | IEEE thin-space page numbers; rejected by both cross-checkers. |
| AG-39 | DJ | Column balance on the last page; rejected by both cross-checkers. |
| AG-40 | R | DAS cites [22], [23]; [23] carries "Available: https://doi.org/10.5281/zenodo.21887809". |
| CL-45 | R | As AG-37. |
| CX-30 | P | "The study used a public, anonymized dataset \cite{zeng2023} and required no ethics approval." Citation added; no institutional determination (none exists to cite). Acceptable. |

Totals: RESOLVED 83, PARTIAL 14, DECLINED-JUSTIFIED 22, NOT ADDRESSED 0, DECLINED-UNJUSTIFIED 0.

## Checks of changed sentences for new errors

- Grammar: one comma splice (must-fix 1); one dangling pronoun in the abstract (must-fix 3); "only … 89 %" (must-fix 4). Everything else reads cleanly, including the new Fig. 1 caption, the Table I footnote, the IV-A rewrite ("Bed structure set the magnitude, the leaky bed damping topological errors; their excess … held only in the discrete bed") and the Conclusion.
- Terminology: $C_\mathrm{b}$ used consistently in main, Table S1 context and Fig. S1; $\lambda$ used once, no clash with $k$; "taper-fit radius" in II-A, II-B, S1, Fig. S2; "healthy reference radius" reserved for $r_\mathrm{ref}$; "reference value" once in the Introduction, "clean value"/"clean model" elsewhere (consistent).
- Abstract vs body: 32–33 % / 6–10 % (Table I class level 33/32 and 10/6), 5–19 % pooled (B–D topological 14, 5, 19, 8, 8, 6), 19–20 % / 5–8 % (III-B 19, 20 / 8, 5), 4–18 % caliber (5, 18 / 12, 4), 3–4 % floor (3.1, 3.9), 0.074 → −0.0007 (III-D) all agree; Conclusion "three to six times" (33/10, 32/6) and "5–8 %" agree with Results.
- Fig. S1 (operator edit after launch): module filenames absent as instructed; boxes 1–9 consistent with the main text (6 944 instances, 150/97, $C_\mathrm{b}$, Protocols A–D, 10⁻⁸); caption "Analysis pipeline."; supplement still 6 pp.
