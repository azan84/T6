# Readability pass on main.tex (2026-10-07)

Request: rewrite the JBHI manuscript so that an educated non-specialist can follow it, in formal English,
without changing any number, result, citation, label, figure/table content or equation meaning.
Backup untouched: `main-backup-2026-10-07-pre-readability.tex`. Only `main.tex` was edited.

## Build

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: exit 0.
- Pages: **8** (was 8). Body ends on page 7; references end about 80% down the right column of page 8.
- main.log: no undefined references or citations, no overfull hbox (none at all; the original build had none
  either). Eight underfull boxes, all cosmetic (table cells, the DOI line).
- Note: `refs.bib` was modified at 23:20 by a separate process (a `refs-backup-2026-10-07.bib` appeared at 23:19)
  which abbreviated journal names to IEEE style. The citation keys are unchanged (verified against the backup bib).
  This shortened the reference list by roughly a third of a column; the page-8 margin reported above includes that
  effect. If the full journal names are restored, the paper will still fit on 8 pages only if that margin is not
  consumed elsewhere.

## Abstract

- **248 words** (limit 250), one paragraph, no abbreviations (no all-capital tokens; "FFR", "CT", "3D" and "CI"
  are spelled out or absent).

## Word count by section (crude LaTeX-stripped count, backup -> new)

| Section | Backup | New | Change |
|---|---|---|---|
| Abstract | 249 | 248 | -1 |
| Introduction | 677 | 671 | -6 |
| Methods | 1979 | 2013 | +34 |
| Results | 967 | 1028 | +61 |
| Discussion | 821 | 842 | +21 |
| Conclusion | 108 | 108 | 0 |
| Back matter | 48 | 48 | 0 |
| **Total** | **4849** | **4958** | **+109 (+2.2%)** |

The small growth comes from plain-language glosses (what a boundary condition, the microvascular bed, perfusion,
a flip, absorption and the noise floor are) and from topic sentences that open each Results paragraph with the
finding. It was offset by removing restatements of numbers that already appear elsewhere (see number check) and
by widening Table I's columns so the table wraps into fewer rows (format only; cell content unchanged).

Sentence statistics (prose only, tables/figures/equation excluded): mean length 20.9 words (was 22.8), longest
75 words (was 89), 22 sentences over 35 words (was 27). The remaining long sentences are enumerations (the
contributions list, the factorial design, the perturbation list for the second noise floor).

## Number check

Every numeric token (`\d+(?:\.\d+)?`) was extracted from the body text, captions and tables of the backup and of
the new file and the multisets compared. Differences, with justification:

| Token | Backup | New | Reason |
|---|---|---|---|
| 0.0007 | 2 | 1 | Discussion restatement of the 3D result removed; value remains in Results (3D case study). |
| 0.006, 0.037 | 2 | 1 | Discussion restatement of the calibre mean |dFFR| range removed; remains in Results. |
| 0.04 | 2 | 1 | Protocol B median residual (leaky) removed from the Protocol B paragraph; remains in the Absorption paragraph ("from 0.04 to 0.03"). |
| 0.36 | 3 | 2 | Same, discrete bed; remains in the Absorption paragraph ("from 0.36 to 0.16") and in the Discussion. |
| 0.074 | 4 | 3 | Discussion restatement removed; remains in Abstract and twice in Results. |
| 8, 22, 6, 15 | -1 each | | The taper 95% CIs "(13%, 8--22%, discrete; 9%, 6--15%, leaky)" moved out of the Results sentence; both intervals are in Table II, row T4/A, and the sentence now points to the table. |
| 0.80 | 13 | 14 | Fig. 5 caption now says "a shift that would move a decision near 0.80" instead of "which would move the decision"; same threshold, no new value. |

No number was added or changed in value. No finding, caveat or departure from the plan was removed
(demand-sensitivity caveat, leaky-bed result, radius-definition gap, 3D mesh-resolution result, both noise
floors, "analysis script written while the ablation ran", the annotator upper-bound caveat, and the RCA
restriction of Protocol C are all present).

- `\cite` keys: identical set and identical count per key (30 keys).
- `\label` keys: identical set and count.
- `\ref` keys: identical set; `tab:results` is referenced three times instead of twice (the new pointer for the
  taper CIs).

## Style checks

- No contractions (the apostrophes are possessives: tree's, model's, Murray's, dataset's, instance's,
  segmentation's).
- No em dashes. Seven semicolons in prose (was nine), all in enumerations or parenthetical lists.
- No "should" in Methods. No mention of OSF, pre-registration, registered hypotheses, or future work.
- One name per concept throughout: Protocol A "fixed", B "re-derived", C "tuned"; T1 missed branch, T2 vessel
  break, T3 lesion length, T4 taper; "perfusion check", "materially wrong" (|dFFR| > 0.05), "flip",
  "noise floor", "leaky bed" / "discrete bed", "absorption" (defined at the start of Results III-B).
- The registered-hypothesis phrasing "the prediction that tuning leaves the flip rate at or above ... did not hold"
  is now "We had expected tuning to leave the flip rate at or above that of fixed boundary conditions. Instead ...",
  which keeps the stated departure without referring to a registration.

## Main readability changes (before -> after)

1. Abstract opening.
   Before: "Fractional flow reserve computed from coronary computed tomography angiography depends on the
   segmented lumen and on outlet boundary conditions that are derived from it and are often tuned to match
   perfusion."
   After: "Fractional flow reserve, the pressure ratio that decides whether a coronary narrowing is treated, can be
   computed from computed tomography angiography. The computation depends on the segmented artery and on outlet
   boundary conditions derived from it, often tuned to match measured perfusion."

2. Introduction, boundary conditions.
   Before: "Every such model needs boundary conditions: the pressures, flows or resistances imposed where the
   model ends, which stand in for the vessels the image does not resolve. ... Its resistance is not measured but
   derived from the segmented lumen through scaling laws ... and it is increasingly tuned so that the model
   reproduces perfusion measured by imaging."
   After: adds "the blood flow to each region of heart muscle" as the gloss for perfusion, splits the sentence,
   and explains the microvascular bed as the vessels "which set how much blood each region of heart muscle
   draws".

3. Introduction, the gap. The three cited observations are followed by a one-sentence bridge: "If the boundary
   conditions are tuned until the model matches measured perfusion, a topological error may therefore disappear
   from the validation check while it remains in the pressure along the vessel."

4. Methods, eligibility. One 70-word sentence with five comma-separated conditions became "Five conditions made
   a host vessel ... eligible." followed by five short sentences.

5. Methods, bed structures. Added why two beds are used ("because they treat a deleted vessel differently") and
   kept the mechanism sentence that the Discussion later relies on (deleted-branch conductance reappears as wall
   outflow at the parent node).

6. Methods, protocols. Each protocol now ends with what it stands for in practice: A, "the case in which the
   boundary conditions were obtained correctly despite the segmentation error"; B, "as an automated pipeline does
   with whatever anatomy it receives"; C, one scaling fitted to the clean territory flows, "the least flexible
   tuning a pipeline could use".

7. Results paragraphs open with the finding, then the numbers.
   Before: "The calibre errors, at the magnitude of inter-observer disagreement, changed FFR by a mean of
   0.006--0.037 in absolute value. Their flip rates (1--13%) were of the order of ..."
   After: "The calibre errors rarely changed the decision. At the magnitude of inter-observer disagreement they
   changed FFR by a mean of 0.006--0.037 in absolute value, and their flip rates of 1--13% were of the order of
   the 5.0--6.5% expected from repeat invasive measurement."
   Likewise "A missed side branch raised the computed FFR, and tuning removed only part of the rise." and
   "The 3D solution showed the same concealment." now open their subsections.

8. "Absorption" defined in plain words at the start of Results III-B: "We call it absorption when tuning removes
   the error from the perfusion check but not from the FFR."

9. Discussion opens for a reader who skipped Methods: "This study asked whether tuning a coronary flow model to
   perfusion can hide a segmentation error that changes the treatment decision. Three findings answer it. First
   ... Second ... Third ...", followed by "The check therefore measured agreement with the targets that were
   fitted, not the correctness of the model."

10. Stacked parentheticals reduced. Example: "(13%, 8--22%, discrete; 9%, 6--15%, leaky)" became "at 13% in the
    discrete bed and 9% in the leaky bed (Table II)"; the intervals stay in Table II.

11. Captions. Fig. 2 now names the quantity ("Flip rate (proportion of models whose classification at FFR 0.80
    changed)"); Fig. 3 says "Each point is one model" and uses "materially wrong"; Fig. 5 is shorter and says
    what the colours mean for the decision.
