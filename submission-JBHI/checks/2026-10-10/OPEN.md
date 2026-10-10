# OPEN register — Paper 6 v2 → JBHI (2026-10-10)

OPEN-9  Abstract contains an abbreviation (FFR); the guide forbids abbreviations in the abstract
  why it matters:     "The abstract should be without abbreviations, footnotes, references, or mathematical equations." v2 reintroduced "(FFR)" and "FFR was recomputed". Abstract is exactly 250 words, so the fix must not add words.
  options:            F1 (net 0 words, sentences unchanged in number): s.1 "Fractional flow reserve (FFR), which guides revascularization," → "Fractional flow reserve, which guides revascularization,"; s.5 "FFR was recomputed with a reduced-order model" → "Fractional flow reserve was recomputed with a reduced-order model"; s.5 "fitted to main-branch territory flows" → "fitted to main-branch flows".
  recommendation:     Apply F1; rebuild; re-count (must stay ≤ 250).
  blocking:           yes (guide rule)

OPEN-11  House style: semicolon introduced in IV-B today
  why it matters:     "A bifurcation-connectedness score is insensitive to caliber-only errors [20]; the throat error is of this kind." House style avoids semicolons joining clauses (OPEN-6 of 10-08).
  options:            F2: "...insensitive to caliber-only errors [20], and the throat error is of this kind."
  recommendation:     Apply.
  blocking:           no

OPEN-12  III-C throat Dice value: name the basis
  why it matters:     "kept a DSC of 0.999" is true over the whole scan (both beds) and per tree in the leaky bed; the discrete per-tree median is 0.998. The paragraph reports both bases.
  options:            F3: "kept a whole-scan DSC of 0.999" (+1 word; main stays 9 pp to be confirmed).
  recommendation:     Apply.
  blocking:           no

OPEN-2  Author Consent Form signed by hand by all five authors (carried)
  why it matters:     Required supporting document.
  options:            jbhi-consent_form_v3-1_fixed.pdf (embs.org), five signatures.
  recommendation:     Send with the co-author package.
  blocking:           yes

OPEN-7  ICMJE criterion 2 for M. A. Mohammed Sapardi and M. K. Tan (carried, STUDY-PLAN-v2)
  why it matters:     Project rule: both must critically revise, not only approve.
  options:            Co-author read of the v2 PDF with their changes recorded.
  recommendation:     Combine with OPEN-2.
  blocking:           yes (project rule)

OPEN-10  Funding statement absent from the manuscript
  why it matters:     The letter states "no external funding"; IEEE papers usually carry funding (or its absence) in the first-page footnote. The guide does not require it.
  options:            Add "This work received no external funding." to the first \thanks; or leave it to the portal funding field.
  recommendation:     Portal field only unless a co-author's institution requires otherwise (keeps page fit).
  blocking:           no

OPEN-13  Cover letter: optional mention of the new Fig. 4 throat result
  why it matters:     Bullet 3 argues overlap scores miss decision risk with the missed-branch example; the throat error (Dice 0.999, clDice 1.000, median |ΔFFR| 0.11) is now the strongest instance.
  options:            Add one clause to bullet 3, keeping the letter to one page; or leave.
  recommendation:     Optional.
  blocking:           no

OPEN-8  benchmark.py and venue_fit.py tool limits (carried; tooling, not the manuscript)
  why it matters:     benchmark.py does not recognise IEEE headers (benchmark measured by hand); venue_fit.py misses journal names split across lines in a .bbl (counts 1 JBHI ref, true count 3); refs_integrity.py needs an inline thebibliography.
  options:            Extend the tools in a v3 pipeline.
  recommendation:     Record; change only on operator instruction.
  blocking:           no

Residual (carried from 10-08): the template's "LOGO" placeholder in the page header; publisher sets the header at production.
