# OPEN register — Paper 6 → JBHI (2026-10-08)

OPEN-1  Format in the official JBHI template, which runs to 9 pages?
  why it matters:     The guide names an official template (ieeecolor). Typeset in it, the paper is 8 pages + ~10 lines. Over-length charges ($250/page for pp. 9–10) follow the final typeset length, and the 14-page total would become 15.
  options:            (a) switch to ieeecolor now and cut ~12 lines (no change to results); (b) submit in IEEEtran at 8 pp and accept a likely 9th page (+$250) at production; (c) submit in IEEEtran and trim at revision.
  recommendation:     (a). The cut is small, and the 14-page cap applies to revisions too, which already need room for the planned revision analyses.
  blocking:           no, but decide before building the upload set

OPEN-2  Author Consent Form signed by hand by all five authors
  why it matters:     Required supporting document; submission cannot be completed without it.
  options:            Download jbhi-consent_form_v3-1_fixed.pdf (embs.org) and collect five signatures.
  recommendation:     Send with the co-author read on 9–10 Oct.
  blocking:           yes

OPEN-3  ORCID and institutional email for every author
  why it matters:     The portal requires an ORCID for all authors and institutional or IEEE emails.
  options:            Collect from co-authors; F. Yamin, X. Wang (Monash), M. A. Mohammed Sapardi (IIUM), M. K. Tan (Monash / Ming Chi).
  recommendation:     Request with the consent form.
  blocking:           yes (portal)

OPEN-4  Cover letter: guide wording, article type, named JBHI papers, plain text
  why it matters:     The guide asks the letter to confirm the manuscript "has not been copyrighted, published, submitted, or accepted for publication elsewhere". The letter has a shorter form. It does not state the article type, and it refers to the Journal's papers without naming them (pipeline 8.1 asks for first author and year). The letter goes into a text box, so bold and bullets are lost.
  options:            Replace the declaration with the guide's wording; add "special issue paper"; name Viceconti et al. (2025), Chen et al. (2025) and Arminio et al. (2026) with what each contributed; produce a plain-text version.
  recommendation:     Do all four (about 15 minutes).
  blocking:           yes for the guide wording; no for the rest

OPEN-5  Generative-AI declaration missing
  why it matters:     House rule R11 and the portfolio memory: the declaration is owed when AI tools were used; IEEE asks for disclosure in the Acknowledgment.
  options:            Add to the Acknowledgment: "The authors used Grammarly for language editing." (portfolio wording, Grammarly only, per operator 2026-10-07)
  recommendation:     Add it; ~1 line, may affect OPEN-1 page fit.
  blocking:           yes

OPEN-6  Semicolon introduced by today's CFP edit (IV-C)
  why it matters:     House style: no semicolons joining clauses.
  options:            "...does not by itself make a model credible. A coronary digital twin calibrated to perfusion also requires..."
  recommendation:     Apply.
  blocking:           no

OPEN-7  ICMJE criterion 2 for M. A. Mohammed Sapardi and M. K. Tan (STUDY-PLAN-v2)
  why it matters:     Recorded as a submission blocker: both must critically revise the draft, not only approve it.
  options:            Co-author read on 9–10 Oct with their changes recorded.
  recommendation:     Combine with OPEN-2 and OPEN-3.
  blocking:           yes (project rule)

OPEN-8  Benchmark tool does not recognise IEEE journal headers
  why it matters:     benchmark.py skipped all five JBHI samples; the benchmark was measured by hand this run.
  options:            Extend the identity check to "IEEE JOURNAL OF ..., VOL." headers in a v3 pipeline.
  recommendation:     Record; change only on operator instruction.
  blocking:           no

## Status after fixes (2026-10-08, same day)
- OPEN-1 RESOLVED: official ieeecolor template, 8 pp (figures at 0.95 width). Residual: the template's placeholder "LOGO" prints above the header. It is the generic IEEE-TJ asset. Leave it, as the publisher sets the header, or blank `logo.eps` if you prefer.
- OPEN-4 RESOLVED: guide wording, article type, three named JBHI papers, plain-text copy `cover_letter_portal.txt`.
- OPEN-5 RESOLVED: Grammarly declaration in the Acknowledgment.
- OPEN-6 RESOLVED.
- Still blocking: OPEN-2 (consent form), OPEN-3 (ORCID, emails), OPEN-7 (ICMJE criterion 2).
- Upload set: add ieeecolor.cls, generic.sty and logo.eps to the manifest; run upload_clean.py --fix --verify-build before upload.

## Update 2026-10-08 (late)
- OPEN-3 RESOLVED. ORCIDs and institutional emails for all five authors are in `portal/authors.txt`, taken from `Imaging-Medical/AuthorsDetails.docx`.
  - Check 1 RESOLVED (operator 2026-10-08): Monash dropped. M. K. Tan is listed under Ming Chi University of Technology only (postcode 243303, as in the docx).
  - Check 2 RESOLVED (operator 2026-10-08): the publication name is "Fadillah Yamin" in the byline, the portal and the consent form.
- Still blocking: OPEN-2 (hand-signed consent form, all five authors) and OPEN-7 (co-author critical read).
