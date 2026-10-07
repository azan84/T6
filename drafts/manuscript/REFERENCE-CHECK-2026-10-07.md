# Reference check: main.tex / refs.bib (JBHI, IEEEtran) 2026-10-07

Scope: `refs.bib` (29 entries), `main.tex` (all `\cite`), `main.bbl` (IEEEtran.bst v1.14 output) and the rendered `main.pdf` reference list.

How each record was checked:
- **Metadata.** Every DOI was checked against Crossref (`api.crossref.org/works/<doi>`) and cross-checked against PubMed E-utilities (esummary), which keeps subtitles that Crossref drops. bransby2026 was checked against the arXiv API. imagecasx_data was checked against DataCite and the Zenodo API.
- **Whether each source supports its claim.** Checked against:
  - the Europe PMC abstract for every cited paper;
  - full text where open access: Gamage (PMC efetch), Colebank (Glasgow eprint, via pdftotext), Brown, Korte, Menon, Dalmaso, Tanade (Europe PMC XML), Fournier and Choy (PMC HTML), and Bransby (arXiv, via pdftotext);
  - the project's own full-text extractions in `../../extraction/full/` for fossan2026 and gosling2020, whose publisher pages returned HTTP 403;
  - the project's derivation note `../../references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md` for the 13–16% bound.

**Cited keys vs. bib:** 29 keys cited, 29 entries in refs.bib. **No orphans, no missing keys.**

---

## 1. Summary table

Record = bibliographic status after Crossref/PubMed comparison. Support = whether the source supports the sentence(s) citing it.

| # | Key | Record status | Support status | Where cited (main.tex line) |
|---|-----|---------------|----------------|-----------------------------|
| 1 | tonino2009 | OK data; **initials lost** (Pim A.L. → "P. A.", Nico H.J. → "N. H."); **backtick in "van \`t Veer"** renders as ‘; en-dash pages → "p." | SUPPORTED (FAME used FFR ≤ 0.80 to guide stenting) | 64 |
| 2 | taylor2013 | OK data; **subtitle missing** (": scientific basis"); en-dash pages → "p." | SUPPORTED (review reporting DISCOVER-FLOW/DeFACTO) | 66 |
| 3 | norgaard2014 | OK data; **subtitle missing** (": the NXT trial ..."); en-dash pages → "p."; 20 authors listed | SUPPORTED (multicentre NXT, invasive FFR reference) | 66 |
| 4 | kim2010 | OK; en-dash pages → "p." | L67 SUPPORTED (3D coronary model). L74 (scaling laws) UNVERIFIABLE: paywalled, abstract does not mention scaling laws | 67, 74 |
| 5 | itu2016 | OK; en-dash pages → "p." | SUPPORTED for the ML form (see fix 13: the reduced-order form has no direct citation) | 67 |
| 6 | murray1926 | OK (Crossref omits subtitle; bib correct per PubMed); en-dash pages → "p." | SUPPORTED (cube law; classical) | 74, 164, 172 |
| 7 | menon2024 | OK data; **no article number (9)**; "CT" lower-cased to "ct"; month field inconsistent | L75 SUPPORTED. L471 PARTLY: the paper personalises models, it does not "check" them | 75, 471 |
| 8 | sankaran2015tmi | OK; en-dash pages → "p." | SUPPORTED | 81, 450 |
| 9 | sankaran2015cmame | OK; en-dash pages → "p." | SUPPORTED (states "deformation maps with fixed bifurcation locations") | 81, 450 |
| 10 | fernandez2024 | **Title contains HTML "&lt;sub&gt;CT&lt;/sub&gt;"**: it renders as "ffr¡sub¿ct¡/sub¿" in the PDF. U+2010 hyphens (name lost its hyphen in the PDF: "NogalesAsensio"). **No article number (e3822)**. Month "Apr" is the online date; the print issue is Jun 2024 | SUPPORTED (global threshold shift, branching unchanged) | 81, 450 |
| 11 | dalmaso2025 | OK data; U+2010 hyphens (PDF shows "modelbased"); **no article number (e3898)**; month field | PARTLY: the outcome is **iFR, not FFR** | 81, 450 |
| 12 | sankaran2016 | OK; en-dash pages → "p." | SUPPORTED (MLD > boundary resistance > viscosity > lesion length) | 82, 452 |
| 13 | tanade2022 | OK data; **no article number (1034801)**; month field | SUPPORTED (Sobol ranking: stenosis degree and cardiac output dominate) | 82, 452 |
| 14 | colebank2019 | OK | **NOT SUPPORTED as placed** (L82). It ranks network *connectivity* against radius/length, not geometry against BCs, and its Windkessel BCs are re-derived for each network. It is a *topological*-error precedent and belongs in the next sentence | 82 |
| 15 | korte2023 | OK; en-dash pages → "p." | SUPPORTED (intracranial aneurysms; WSS/velocity outputs) | 82, 452 |
| 16 | bransby2026 | OK (arXiv 2608.30404v1, 31 Aug 2026; title and all 10 authors match) | L122/L126 SUPPORTED (800 scans; 160-scan test split re-annotated by a different analyst; DSC 92.8, HD95 2.46 mm). **L84 PARTLY**: "every evaluated method" rests on three qualitative examples (Fig. 6). **L466 PARTLY**: "Overlap metrics barely register a missing branch" is not shown by this source. **L211–213 (uncited attribution) PARTLY**: the authors call only the *DSC* an upper bound | 84, 123, 126, 466 |
| 17 | gamage2022 | OK | **PARTLY**: 15.5% was an *idealised* model; the two OCT models gave **13% and 2%** | 90, 457 |
| 18 | gosling2020 | OK | SUPPORTED with a precision caveat. The "re-tuning" was a single *cohort-averaged* outlet resistance recalibrated per model variant (accuracy 75% vs 72%, AUC 0.84 vs 0.82), not per-patient tuning | 91, 457 |
| 19 | fossan2026 | OK (vol 330(1) H157–H169, 2026); en-dash pages → "p."; "CT-FFR" lower-cased | SUPPORTED: AUC 0.845 vs 0.845 (P = 0.915), sensitivity 58.1% → 68.6% (P = 0.0033), from the project full-text extraction. Publisher page was 403 to me | 93, 463 |
| 20 | zeng2023 | OK; "ImageCAS" lower-cased to "Imagecas"; article number printed as "p." | SUPPORTED | 123 |
| 21 | imagecasx_data | OK (DataCite: Bransby, Kit Mills; Paulsen, Rasmus Reinhold; 2026; CC BY 4.0). Zenodo record has **no version string**; "version 1" unverified. **DOI not printed** in the reference list | SUPPORTED | 123 |
| 22 | young1973 | OK (6(4):395–410, 1973) | UNVERIFIABLE from primary text (paywalled, no abstract). K_t = 1.52 is the standard secondary attribution to this paper | 153 |
| 23 | choy2008 | OK; en-dash pages → "p." | **PARTLY**. D ∝ m^(3/8) is supported. But the same paper reports Q ∝ m^(3/4), which implies Q ∝ D², not D^(8/3). Setting outlet conductance ∝ r^(8/3) assumes flow ∝ perfused mass, which Choy did not find | 168 |
| 24 | dodge1992 | OK | SUPPORTED (proximal LAD 3.7 ± 0.4 mm). Check: k r³ with r = 1.85 mm gives 213.5 mL/min ✓ | 173 |
| 25 | fournier2021 | OK | SUPPORTED: LAD hyperaemic Q is 228 ± 71 mL/min (non-obstructive atherosclerosis) and 293 ± 102 mL/min (controls). 214 lies within 1 SD of both ✓ | 175 |
| 26 | schindler2023 | OK data; **subtitle missing** (": A JACC: Cardiovascular Imaging Expert Panel Statement"); "PET" lower-cased; en-dash pages → "p."; 23 authors | UNVERIFIABLE by me (publisher 403). Per the project note, it gives a hyperaemic MBF CoV of ~10% same-day and 15–20% different-day, unqualified as to region. It does **not** give the 13–16% bound | 256 |
| 27 | brown2018 | OK data; initials lost (Louise A.E. → "L. A.", James R.J. → "J. R."); curly apostrophe | **PARTLY**: regional RC 30–37% (stress) implies a single-measurement bound of ~21–26%, not 13–16% | 256 |
| 28 | johnson2015 | OK; initials lost (Nico H.J.); en-dash pages → "p." | SUPPORTED (SD 0.018 of paired repeat FFR, 190 pairs) | 272 |
| 29 | petraco2013 | **Subtitle missing** (": practical implications of a diagnostic gray zone and measurement variability on clinical decisions"); en-dash in title; en-dash pages → "p." | SUPPORTED for the method (measurement certainty around 0.80). **PARTLY as placed**: the 0.018 figure is Johnson's, not Petraco's | 272 |

Records with no metadata errors in title, first author, journal, year, volume, issue, pages or DOI: all 29. All Crossref values match the bib. The defects are formatting, missing subtitles and missing article numbers, listed below.

---

## 2. Required fixes

### A. Claim and citation fixes in main.tex

**1. L88–90, gamage2022 (13–15% side-branch effect).** Gamage reports 15.5% (idealised model, side branch distal to the stenosis), 13% (OCT patient 2) and 2% (OCT patient 1). The distal resistance was held at the same value with and without branches. Replace:
> With outlet resistance held fixed, removing a side branch distal to a stenosis changed FFR by 13--15\% in models built from optical coherence tomography \cite{gamage2022}.

with:
> With outlet resistance held fixed, adding a side branch distal to a stenosis lowered FFR by 15.5\% in an idealised model and by 13\% in one of two models reconstructed from optical coherence tomography \cite{gamage2022}.

**2. L456–457, gamage2022 (Discussion).** Replace:
> A side-branch effect of 13--15\% under fixed outlet resistance was reported from optical coherence tomography-based models \cite{gamage2022},

with:
> A side-branch effect of 13--15.5\% under fixed outlet resistance was reported in an idealised model and an optical coherence tomography-based model \cite{gamage2022},

**3. L82, colebank2019 misplaced; L83–85, bransby2026 overstated.** Replace L81–85, from "Studies that set geometry ..." to "... overlap scores \cite{bransby2026}.", with:
> Studies that set geometry against boundary conditions rank the two by their influence on a continuous output \cite{sankaran2016,tanade2022,korte2023}. Topological error, a change in the branching structure such as a missed side branch or a vessel that ends too early, has received less attention. In a one-dimensional model of the mouse pulmonary arteries, network connectivity contributed more to haemodynamic uncertainty than vessel radius and length \cite{colebank2019}, and qualitative examples from a recent coronary benchmark showed vessel breaks in the output of every evaluated method despite high overlap scores \cite{bransby2026}.

**4. L466–467, bransby2026 (Discussion).** Replace:
> Overlap metrics barely register a missing branch, and vessel breaks occur in the output of current coronary segmentation methods despite high overlap scores \cite{bransby2026}.

with:
> Vessel breaks occur in the output of current coronary segmentation methods despite high overlap scores \cite{bransby2026}, and a missing side branch removes few voxels from the tree, so overlap changes little when it is absent.

**5. L211–213, attribution to the dataset authors (no `\cite`).** Bransby et al. state that "the DSC inter-observer variability should be considered the upper-bound of agreement". This covers the DSC only, not the HD95. Replace:
> the dataset authors describe these statistics as an upper bound on agreement.

with:
> the dataset authors describe the inter-observer DSC as an upper bound on agreement.

Also add `\cite{bransby2026}` at the end of that sentence. L481–482 ("calibre magnitudes come from inter-observer statistics that are an upper bound on agreement") is the authors' own inference for HD95. That is acceptable, or reword it to "statistics that likely overstate agreement".

**6. L132, image-quality scale (no `\cite`, attributed to the dataset).** The dataset grades image quality on a five-point Likert scale: 0 = non-diagnostic (excluded), 1 = poor, 2 = adequate, 3 = good, 4 = excellent. Replace "image quality was at least 2 on the dataset's four-point scale" with:
> image quality was at least adequate (grade 2 of 0--4) on the dataset's scale

**7. L255–257, schindler2023 / brown2018 (13–16% bound).** The 13–16% figure cannot be derived from the two cited sources:
- The project note derives it from Lubberink et al. 2024 (EHJ-CVI abstract, regional wCV 8.3%, RC 23%), which is not cited.
- Brown 2018 gives a regional stress RC of 30–37%. Divided by √2, that gives ~21–26%.
- Schindler 2023 gives a CoV of ~10% (same day) and 15–20% (different days), not regional.

The conservative logic still holds, and it is stronger with the cited values. Replace:
> This threshold is stricter than the 13--16\% bound we derive for a comparison of one deterministic model output with one regional perfusion measurement at published repeatability \cite{schindler2023,brown2018}, and a looser threshold can only increase the number of models that pass. Thresholds of 13\% and 16\% were analysed as sensitivities.

with:
> Published repeatability of hyperaemic myocardial blood flow (coefficient of variation about 10\% on the same day and 15--20\% between days \cite{schindler2023}; regional repeatability coefficient 30--37\% \cite{brown2018}) implies a 95\% bound of about 15--26\% for a comparison of one deterministic model output with one regional measurement. The 10\% threshold is therefore strict, and a looser threshold can only increase the number of models that pass. Thresholds of 13\% and 16\% were analysed as sensitivities.

Also delete "bracket the 95% bound implied by the repeatability of regional perfusion measurement" from the supplement Table caption, around supplement.tex L131–132. Replace it with "were analysed as sensitivities". Before submission, re-check the Schindler sentence against the published PDF, as the project note itself advises.

**8. L270–272, johnson2015 / petraco2013.** The SD of 0.018 is Johnson's. Petraco supplies the measurement-certainty method, computed from DEFER with its own SD. Replace:
> ... drawn from a normal distribution centred on the clean value with the published repeat-measurement standard deviation of 0.018, falls on the other side of 0.80 \cite{johnson2015,petraco2013}.

with:
> ... drawn from a normal distribution centred on the clean value with the published standard deviation of the difference between repeat measurements, 0.018 \cite{johnson2015}, falls on the other side of 0.80, following the measurement-certainty approach of \cite{petraco2013}.

**9. L166–168, choy2008 (3/8 exponent).** The 3/8 exponent is correct. However, Choy and Kassab also report that flow scales as m^(3/4), so their data give flow ∝ D². The text should state the assumption. Replace:
> where the exponent approximates 8/3, the inverse of the 3/8 power that relates coronary vessel diameter to the myocardial mass it perfuses \cite{choy2008}.

with:
> where the exponent approximates 8/3, the inverse of the 3/8 power that relates coronary vessel diameter to the myocardial mass it perfuses \cite{choy2008}, so that outlet flow is proportional to perfused mass.

Optionally add: "(the same study reports flow scaling with mass to the 3/4 power, which would give an exponent of 2)". This is a reviewer risk: a reviewer who reads Choy will see it.

**10. L80–81 and L449–450, dalmaso2025 (iFR, not FFR).** At L81 replace "and report a continuous change in FFR" with:
> and report a continuous change in the computed pressure index

At L449 replace "Published sensitivity analyses of computed FFR perturb lumen calibre" with:
> Published sensitivity analyses of computed pressure indices perturb lumen calibre

**11. L90–91 and L457–458, gosling2020 (precision).** These sentences are supported but imprecise about the kind of tuning, which matters because Protocol C is per-case. At L90 replace "When the microvascular resistance was re-tuned, a change in side-branch flow altered diagnostic accuracy little \cite{gosling2020}." with:
> When a cohort-wide outlet resistance was recalibrated for a model with side-branch outflow, diagnostic accuracy changed little \cite{gosling2020}.

At L457 replace "re-tuning the microvascular resistance absorbed a change in side-branch flow" with:
> recalibrating a cohort-wide outlet resistance absorbed a large change in side-branch flow

**12. L471, menon2024.** Replace "Perfusion imaging is used to personalise and check coronary flow models \cite{menon2024}." with:
> Perfusion imaging is used to personalise coronary flow models \cite{menon2024}.

**13. L67, the reduced-order form has no citation.** kim2010 is 3D. itu2016 is ML; its training model is physics-based, but the paper is cited as ML. fossan2026 is a reduced-order (1D/0D) CT-FFR model already in the list. Replace "\cite{kim2010,itu2016}" with:
> \cite{kim2010,fossan2026,itu2016}

**14. L73–74, kim2010 for scaling laws (UNVERIFIABLE).** Confirm from the Kim 2010 full text that outlet resistances were assigned by a size–flow scaling law. If they were not, cite taylor2013 there instead. From my recollection, Taylor 2013 states the form–function principle (outlet resistance inversely related to vessel size), but I did not verify this here.

### B. BibTeX record fixes (refs.bib)

**15. Unicode en-dash in `pages`** makes IEEEtran print "p. 213–224" instead of "pp. 213–224" in 15 entries. In each, replace `–` with `--`:
- `tonino2009 pages={213--224}`
- `taylor2013 pages={2233--2241}`
- `norgaard2014 pages={1145--1155}`
- `kim2010 pages={3195--3209}`
- `itu2016 pages={42--52}`
- `murray1926 pages={207--214}`
- `choy2008 pages={1281--1286}`
- `fossan2026 pages={H157--H169}`
- `sankaran2015tmi pages={2562--2571}`
- `sankaran2015cmame pages={167--190}`
- `sankaran2016 pages={2540--2547}`
- `korte2023 pages={617--630}`
- `johnson2015 pages={1018--1027}`
- `petraco2013 pages={222--225}`
- `schindler2023 pages={536--548}`

**16. fernandez2024 title** (HTML tags; U+2010 hyphens):
```
title={Impact of minimal lumen segmentation uncertainty on patient-specific coronary simulations: {A} look at {FFR$_{\mathrm{CT}}$}},
author={Fern{\'a}ndez-Mart{\'i}nez, Daniel and Gonz{\'a}lez-Fern{\'a}ndez, Mar{\'i}a Reyes and Nogales-Asensio, Juan Manuel and Ferrera, Conrado},
pages={e3822},
```
Also delete `month=Apr`.

**17. dalmaso2025** (U+2010 hyphens; article number):
```
title={Uncertainty quantification and sensitivity analysis for non-invasive model-based instantaneous wave-free ratio prediction},
pages={e3898},
```
Also delete `month=Jan`.

**18. Missing article numbers.** IEEE style prints "Art. no." For entries that have only an article number, use `pages={...}` (IEEEtran prints "p. X") or, preferably for IEEE, remove `pages` and add `note={Art. no. X}`:
- `menon2024`: `note={Art. no. 9}` (delete `month=May`)
- `tanade2022`: `note={Art. no. 1034801}` (delete `month=Dec`)
- `zeng2023`: `note={Art. no. 102287}`
- `gosling2020`: `note={Art. no. 109698}`
- `gamage2022`: `note={Art. no. 5573}`
- `colebank2019`: `note={Art. no. 20190284}`
- `brown2018`: `note={Art. no. 48}`
- `fernandez2024`: `note={Art. no. e3822}`
- `dalmaso2025`: `note={Art. no. e3898}`

Use one approach for all of them.

**19. Missing subtitles** (Crossref drops them; PubMed has them):
- `taylor2013 title={Computational fluid dynamics applied to cardiac computed tomography for noninvasive quantification of fractional flow reserve: {S}cientific basis}`
- `norgaard2014 title={Diagnostic performance of noninvasive fractional flow reserve derived from coronary computed tomography angiography in suspected coronary artery disease: {T}he {NXT} trial ({A}nalysis of {C}oronary {B}lood {F}low {U}sing {CT} {A}ngiography: {N}ext {S}teps)}`
- `petraco2013 title={Fractional flow reserve-guided revascularization: {P}ractical implications of a diagnostic gray zone and measurement variability on clinical decisions}` (this also replaces the en-dash)
- `schindler2023 title={Myocardial perfusion {PET} for the detection and reporting of coronary microvascular dysfunction: {A} {JACC}: {C}ardiovascular {I}maging expert panel statement}`

**20. Capitalisation protection.** IEEEtran sentence-cases titles, and these acronyms currently render in lower case:
- `menon2024`: `... incorporating {CT} perfusion imaging ...`
- `gamage2022`: `title={Fractional flow reserve ({FFR}) estimation from {OCT}-based {CFD} simulations: {R}ole of side branches}`
- `fossan2026`: `... coronary artery disease with {CT-FFR}`
- `zeng2023`: `title={{ImageCAS}: {A} large-scale dataset and benchmark for coronary artery segmentation based on computed tomography angiography images}`
- `schindler2023`: `{PET}` (included in fix 19)
- `young1973`: `title={Flow characteristics in models of arterial stenoses---{I}. {S}teady flow}`. Optional; it matches the journal typography better than the spaced "--".

**21. Initials lost to "A.L."-style given names.** BibTeX reads "A.L." as a single token, so the second initial is lost. Add spaces:
- `tonino2009`: `Tonino, Pim A. L.`; `Pijls, Nico H. J.`; and `van 't Veer, Marcel`, which replaces the backtick that renders as "‘t"
- `johnson2015`: `Pijls, Nico H. J.`
- `brown2018`: `Brown, Louise A. E.`; `Foley, James R. J.`; `Dall'Armellina, Erica` (straight apostrophe)
- `schindler2023`: `Slart, Riemer H. J. A.`

**22. Data citation must show its identifier.** IEEEtran.bst v1.14 ignores `doi`, so the reference list currently shows neither a DOI nor a URL for the dataset. Change imagecasx_data to:
```
@misc{imagecasx_data,
  title={{ImageCAS-X}}, author={Bransby, Kit Mills and Paulsen, Rasmus Reinhold},
  year={2026}, howpublished={Zenodo},
  url={https://doi.org/10.5281/zenodo.21887809}
}
```
I removed "version 1" because the Zenodo record carries no version string. Optionally add `url={https://arxiv.org/abs/2608.30404}` to bransby2026.

### C. IEEE / JBHI reference-list conventions (from main.bbl)

**23. Author-list length.** Norgaard (20), Schindler (23), Brown (16), Fournier (15), Zeng (15) and Tonino (13) list every author. IEEE style lists up to six, then "et al.". Add this as the first entry in refs.bib:
```
@IEEEtranBSTCTL{IEEEexample:BSTcontrol,
  CTLuse_forced_etal = "yes",
  CTLmax_names_forced_etal = "6",
  CTLnames_show_etal = "1" }
```
Then add `\bstctlcite{IEEEexample:BSTcontrol}` immediately after `\begin{document}` in main.tex.

**24. Journal names.** All are spelled in full, whereas IEEE style uses abbreviated titles. One entry, "Journal of The Royal Society Interface", has inconsistent capitalisation. Recommended values:
- J. Amer. Coll. Cardiol.; N. Engl. J. Med.; Ann. Biomed. Eng.; J. Appl. Physiol.
- Proc. Nat. Acad. Sci. USA; Comput. Med. Imag. Graph.; J. Biomech.; Amer. J. Physiol. Heart Circ. Physiol.
- Appl. Sci.; Front. Med. Technol.; Int. J. Numer. Methods Biomed. Eng.; IEEE Trans. Med. Imag.
- Comput. Methods Appl. Mech. Eng.; J. Roy. Soc. Interface; Cardiovasc. Eng. Technol.; npj Imag.
- JACC: Cardiovasc. Interv.; JACC: Cardiovasc. Imag.; J. Cardiovasc. Magn. Reson.; EuroIntervention; Circulation

**25. Months.** Only four entries carry a `month` (menon2024, tanade2022, fernandez2024, dalmaso2025). Remove all four, as in fixes 16–18, or add months to every entry.

**26. DOIs.** None are printed, because IEEEtran v1.14 drops the `doi` field. This is consistent, and JBHI does not require DOIs. If DOIs are wanted, add `url={https://doi.org/<doi>}` to each entry. The dataset is the exception: its identifier must be shown (fix 22).

**27. Non-breaking spaces** (U+00A0) in the author fields of norgaard2014 and johnson2015 are harmless but should be replaced with ordinary spaces.

---

## 3. Summary

- **Metadata and key coverage.**
  - All 29 references exist and match Crossref, arXiv and DataCite on title, first author, journal, year, volume, issue, pages and DOI.
  - There are no orphan entries and no missing keys.
- **BibTeX and rendering defects** (fixes 15–22):
  - Unicode en-dashes make 15 entries print "p." instead of "pp.".
  - An HTML-tagged title renders as "ffr¡sub¿ct¡/sub¿".
  - Acronyms are lower-cased (ct, pet, oct, cfd, ffr, ImageCAS).
  - Four titles are missing their subtitles and nine article numbers are missing.
  - Initials are dropped for six authors.
  - The dataset reference prints no DOI.
- **Citation support.**
  - **Verified correct:** the numbers attributed to fossan2026, johnson2015, dodge1992, fournier2021 and bransby2026 (DSC/HD95).
  - **Inaccurate:**
    - gamage2022's 13–15% (one OCT model gave 13% and the 15.5% came from an idealised model);
    - the 13–16% perfusion bound, which the cited schindler2023/brown2018 do not yield;
    - bransby2026's "every evaluated method", which rests on qualitative examples only;
    - colebank2019, which is placed as a geometry-vs-BC study but is a connectivity (topology) study and supports the paper's topological framing.
  - **Need qualification:** choy2008 (the paper's own flow–mass exponent implies D², not D^8/3), dalmaso2025 (iFR) and petraco2013 (the 0.018 is Johnson's).
  - **Cannot be checked without full text:** kim2010 for scaling laws and the primary text of young1973.

None of these changes the results. Fixes 1–3, 7, 9 and 15–16 should be made before submission.
