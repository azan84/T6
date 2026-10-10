# Referee report: Associate Editor, IEEE JBHI (Computational and in silico medicine / digital twins)

**Manuscript:** "Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study"
**Material read:** manuscript.txt, supplement.txt, ms-page-1 to 9, supp-page-1 to 6, RUBRIC.md
**Date:** 2026-10-09

## Summary

The authors insert 150 idealized stenoses into 108 ImageCAS-X coronary trees, stratified across FFR 0.65–0.95. They apply five single segmentation errors: missed branch, vessel break, longer lesion, taper, and a half-voxel throat error. FFR is then recomputed with a reduced-order network model in two microvascular-bed structures (discrete, leaky) under four boundary-condition protocols (fixed, re-derived, global-tuned, per-territory-tuned). With fixed boundary conditions, topological and throat errors flip the 0.80 decision in about a third of models, compared with 6–10% for the other caliber errors. Re-deriving or tuning the boundary conditions removes most topological flips but no throat flips. A perfusion check passes models that are materially wrong (|ΔFFR| > 0.05) in 19–20% (discrete) and 5–8% (leaky) of topological cases and in 57–81% of throat cases. A single 3D CFD case agrees in direction. The paper argues that agreement with perfusion after tuning is calibration evidence, not validation evidence, for coronary digital twins.

## Strengths

1. **Decision-level framing.** Most CT-FFR uncertainty studies report continuous sensitivity. This paper judges every perturbation by the clinical decision at 0.80 and sets the result against a repeat-invasive-FFR noise floor. That is the right endpoint for a digital-twin credibility argument.
2. **Clean ablation design.** Errors are applied one at a time, each corrupted model is paired with its own clean reference, and the same corrupted anatomy is solved under four protocols. This isolates the error from the protocol. The paired tests (McNemar with Holm, sign, Wilcoxon) match the design.
3. **The "passes-and-wrong" construct is new and useful.** The paper shows quantitatively that tuning to perfusion can conceal a geometric error, and that how much it conceals depends on the error type and on territory resolution (Table S8). This speaks directly to digital-twin calibration and VVUQ practice [33].
4. **Robustness work is extensive.** Two bed structures, with a claim made only when both agree; demand scaling at 0.7, 1.3, 2 and 3 (Tables S4, S5); perfusion-check thresholds of 13% and 16% (Table S3); a finer territory partition (Table S8); a simulated physiological noise floor (Table S11); and a throat error at ±10 DS points (Table S7).
5. **Numbers are internally consistent.** I recomputed the headline counts and Wilson intervals: 45/137 = 32.8% (25.5–41.1), 20/194 = 10.3% (6.8–15.4), 84/265 = 31.7%, 17/300 = 5.7%, 20/104 = 19.2% (12.8–27.8), 21/104 = 20.2%, 9/171 = 5.3%, 14/171 = 8.2%, 20/39 = 51%, 14/154 = 9%. All match Table I and Tables S3/S6 to rounding. The abstract ranges (32–33%, 30–36%, 6–10%, 19–20%, 5–8%, 57–81%, 4–18%, 3–4%, 2–7%) all trace to table cells.
6. **Transparent exclusions** (Table S1), a public dataset, a fixed seed, and a public code repository.
7. **Limitations are candid.** The authors state that the topological magnitudes are design choices, that the cohort is threshold-stratified so its rates are not prevalences, and that the considerations are "not validated decision rules".

## Weaknesses

**W1 (major): The headline contrast with correct anatomy compares unlike conditions.**
Evidence: "Up to one in five tuned topological-error models … passed a main-branch perfusion check while materially wrong, against 3–4% for correct anatomy" (Conclusion; also the abstract). The Limitations add: "Tuning targets were error-free clean-model flows (noise entered only the simulated floor)." The error models are tuned to noise-free targets, while the 3–4% comparator (Table S11) is tuned to noisy targets. The same asymmetry affects the detector result in the main text, "AUC 0.77 against 0.22" (Sec. III-C). Table S10 notes that with matched noise the AUCs are 0.82 and 0.56, so the asymmetry changes the numbers.
Fix: Re-run Protocols C and D on the error models with the same 20 noisy target draws used for the floor, and report passes-and-wrong as error-with-noise against correct-with-noise. Report the matched-noise AUCs (0.82/0.56) in the main text in place of 0.77/0.22, or alongside them.

**W2 (major): The ranking of topological against caliber error depends on magnitudes that are not comparably grounded.**
Evidence: "T1 and T2 have no measured magnitude and are design choices" (Sec. II-C). T1 deletes "the largest side branch beyond the lesion" and T2 truncates at a fixed 25 mm. The caliber magnitudes come from whole-scan inter-observer statistics: HD95 is used as a lesion-length proxy, and the DSC is converted to a radius ratio that is then applied only from the lesion onwards. Because of that, the taper's tube DSC (0.971) is far above the 0.928 it was calibrated to (Table S9). The abstract nonetheless states the ranking unconditionally ("branching (topological) errors changed the decision in 32–33% … against 6–10% for vessel-size errors"). How often each error occurs at a lesion was not measured (Limitations).
Fix: (a) Add a magnitude sweep for T1 (e.g., the smallest, median and largest qualifying side branch, or flow-lost deciles; Table S9 already gives flow lost) and for T2 (e.g., 10/25/40 mm), and report flip rate against flow lost. (b) Apply the taper over the whole tree as well, or recalibrate so that the tube DSC equals 0.928. (c) Preferably, run two or three published segmentation networks from the ImageCAS-X benchmark on the 160 test scans and measure how often each error type occurs within, say, 30 mm of the lesion sites. This would turn conditional rates into an expected decision risk and is the most valuable addition for a JBHI readership (see W4). (d) Put "for the error magnitudes studied" in the abstract sentence.

**W3 (major): The overlap-score comparison uses a tube-model Dice and benchmarks it against a voxel-mask Dice.**
Evidence: "A missed branch kept a near-perfect Dice score (0.97, as high as a taper)" (abstract). The Fig. 4 caption says "The dashed line marks the inter-observer Dice score (0.928)". In the paper, "Each tree was represented as cylinders of node radius and element length (a tube model)" (S7), whereas 0.928 is a voxel-mask DSC from two human annotators. Tube DSC has no partial-volume boundary and is not on the same scale. Also, Sec. III-C quotes the tree-level median (0.97) but cites Fig. 4, which plots whole-scan DSC (T1 median 0.985).
Fix: Compute DSC and clDice on voxelized masks (rasterize the corrupted tube trees at native spacing, or delete the voxels of the branch/segment as in the 3D case) so they are commensurate with 0.928. Otherwise, remove the 0.928 reference line and say "tube-model Dice" in the abstract and Conclusion. Make the text match the plotted quantity in Fig. 4.

**W4 (major for JBHI): The health-informatics contribution is implicit.**
Evidence: The deliverables are rates plus "four considerations. … These considerations are not validated decision rules" (Sec. IV-C). There is no computable quality-control output, no evaluation on real automated segmentations, and no information-system element. The work as written suits IJNMBE, Ann Biomed Eng or (for the segmentation angle) MedIA as well as or better than JBHI.
Fix: State an explicit informatics contribution and evaluate it. Examples: (i) a topology/side-branch-presence check and a pre-tuning residual flag, packaged in the released code as a QC report and scored for sensitivity/specificity against decision flips (Table S10 is the start of this); (ii) the error-frequency study in W2(c); (iii) a short paragraph placing the "calibration evidence vs validation evidence" result within digital-twin credibility workflows (e.g., ASME V&V40-style credibility factors), with a concrete recommendation for what a twin pipeline should log.

**W5 (minor): Under Protocol D the "perfusion check" is vacuous.**
Evidence: "Protocol D matches every territory flow, so its passes-and-wrong proportion equals its materially wrong proportion" (Table S3 note); "Per-territory tuning passes almost every model by design" (Sec. IV-A). Yet Protocol D figures (80–81% throat, 20% topological) are reported in the abstract as "concealment".
Fix: Report Protocol D as residual error after exact calibration rather than passes-and-wrong, or say clearly in the abstract that the D rates are rates of being materially wrong.

**W6 (minor): Domain points to clarify.**
(a) "conductance r_ref^2.66/C_b. Outlet flow is then proportional to perfused mass [25]" (Sec. II-B). Please state the derivation. Choy and Kassab relate flow to mass by a sub-linear power law, so "proportional to mass" needs justification, or the citation should be qualified. (b) The expansion loss is switched on only "where the narrowing exceeds 30% DS". The DS −10-point throat error applied to 40% DS lesions crosses this switch, which creates a model discontinuity (Table S7, "DS ±10 pooled"). State how many models cross it, or smooth the switch. (c) The distance-map radius underestimates the meshed lumen by a median of 0.14 mm (Limitations), which is larger than the 0.088 mm T5 perturbation. Comment on what this implies for clinical pipelines, since the radius definition alone is a throat-scale "error". (d) The perfusion territories (children of the first bifurcation) are not the myocardial segments that PET/CMR report. Note the mapping assumption.

**W7 (minor): Different aggregations of the same quantity.**
Evidence: Topological flips after re-derivation or tuning are given as "5–19%" (abstract, pooled over B–D), "2–20% per error type" (Sec. IV-A) and "5–18%" (Conclusion, B per type; pooled B is 5–14%, Table S6).
Fix: Use one aggregation (pooled topological, as in Table S6) in the abstract and Conclusion.

**W8 (minor): Table I denominators.**
Evidence: Table I has a single n column, but the passes-and-wrong denominator differs for T2. For example, discrete T2 B shows n = 96, yet its 2% (0–9) corresponds to 1/60 (Wilson 0.3–8.9). With 2/96 the interval would be 0.6–7.3. The footnote explains this, but the table misleads on a first read. In S2, "scored as flips (FFR 1)" really means "scored with FFR = 1", of which about 17 of 36 flip (40% → 43% of 96).
Fix: Add a separate n column for passes-and-wrong, and reword S2.

**W9 (minor): The 3D evidence is a single case with a large radius offset.**
Evidence: "The 3D analysis covers one instance, whose meshed lumen was wider … moved the baseline across 0.80 (0.761 against 0.870)". The 3D check confirms direction only, and only for T1.
Fix: Add a T5 (throat) 3D case, since throat errors carry the largest concealment claim, or limit the stated role of the 3D work to "direction for T1".

**W10 (minor): Statistics.**
Evidence: "intervals are posterior mean ±1.96 posterior standard deviations from the variational approximation" (Table S2). Mean-field variational inference typically underestimates posterior variance. The mixed model also omits T5 and Protocol D.
Fix: Refit with MCMC (or state why VI is adequate), and include T5/D, or state that they are excluded.

**W11 (minor): IEEE format and length.**
(a) Page 1 shows a template placeholder "LOGO" above the running head (ms-page-1). (b) There is no funding or support statement in the first-page footnote and no competing-interests statement. (c) The main text runs to 9 pages (page 9 holds only references, one overlength page), and with the 6-page supplement the total is 15 pages, above the stated 14-page cap including supplementary material. (d) The abstract is about 250 words (at the IEEE limit) and introduces the undefined term "concealment". (e) Reference [9] (pulmonary-valve FSI) is weak support for "measured flow splits" in coronary tuning, and [18] (the central dataset benchmark) is an arXiv preprint. Cite peer-reviewed versions where they exist.
Fix: Remove the placeholder, add funding and COI statements, cut the main text to 8 pages (e.g., merge Figs. 3 and 4 or move Fig. 1(d) to the supplement), trim the supplement by one page, and define or replace "concealment".

**W12 (minor): Novelty positioning.**
Evidence: "Matching flow alone cannot identify a geometric error, because the fitted bed absorbs it" (Sec. IV-A). Non-identifiability of geometry from flow-only calibration is expected, and throat dominance is known [10], [12]. The new element is the decision-level size and its dependence on error type and resolution. Coverage of prior CT-FFR UQ in reduced-order/1D settings (e.g., the Fossan/Müller/Hellevik group's work beyond [5], [13]) is thin.
Fix: Sharpen the contribution statement to "quantifying decision-level concealment by error type and territory resolution", and broaden the related-work coverage of CT-FFR UQ in 1D/0D models.

**W13 (minor): Reproducibility details.**
Evidence: Data and code are on GitHub. S1 says the 3D steps "ran on the CFD machine", and the 3D case files and mesh settings are not stated as released.
Fix: Archive the code with a DOI (Zenodo) and a tagged release, include the OpenFOAM case directories and environment files, and state the Protocol C optimizer and objective (search method over ±1.5 decades).

## Rubric scores

| Code | Dimension | Score | Status | Justification |
|------|-----------|-------|--------|---------------|
| S1 | Novelty and contribution | 6 | warn | Decision-level ablation and quantified tuning concealment are new, but non-identifiability and throat sensitivity are expected; positioning needs sharpening (W12). |
| S2 | Methodological rigour | 6 | warn | Strong paired ablation and sensitivities, but noise-asymmetric comparator (W1), magnitudes that are design choices or mis-scaled (W2), and a tube-model Dice (W3). |
| S3 | Claims supported by evidence | 6 | warn | Most claims are hedged and trace to tables, but "against 3–4% for correct anatomy" and the unqualified Dice and ranking statements in the abstract overreach (W1–W3). |
| S4 | Domain / physiological accuracy | 7 | pass | Physiology is sensible and limitations are acknowledged; flow–mass exponent, 30% DS switch and radius-definition bias need clarification (W6). |
| S5 | Internal consistency | 8 | pass | All headline numbers and CIs recompute correctly; only aggregation and denominator presentation issues remain (W7, W8, Fig. 4 vs tree DSC). |
| S6 | Clarity, structure, readability | 7 | pass | Concise and well structured but dense with ranges; coined terms ("concealment", "passes-and-wrong") need consistent definition. |
| S7 | Venue fit (JBHI) and HI relevance | 5 | warn | Fits the in silico/digital-twin track only if the informatics contribution is made explicit (W4); format and length issues (W11). |
| S8 | Reproducibility and transparency | 8 | pass | Public data, fixed seed, exclusion table, public code; needs archived DOI and 3D case files (W13). |

## Overall

**Overall score: 6.4 / 10**

**Recommendation: Major revision.**

The core study is careful, the numbers hold up, and the message about calibration versus validation evidence for coronary digital twins is worth publishing. Acceptance in JBHI requires three things: (1) a matched-noise comparison for the correct-anatomy contrast; (2) a voxel-commensurate overlap analysis and better-grounded, or swept, error magnitudes; and (3) an explicit, evaluated health-informatics contribution, ideally the frequency of these errors in real automated segmentations at lesion sites.
