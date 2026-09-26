# Gate N1 — novelty search log (Paper 6 / T6)

**Date:** 2026-09-17
**Status:** **PROVISIONAL PASS** — corpus-based. A live bibliographic-database sweep using the ACQUIRE-T6 search
strings has **not** been run yet; see §6. Do not record N1 as closed in STUDY-PLAN.md until that is done.
**Updated 2026-09-17 (late):** the single most serious prior-art risk — the four-paper HeartFlow/Sankaran thicket —
is now **fully resolved by full-text reads of all four**, and none of them occupies T6's error-type, reclassification
or BC-ablation ground. The 624-note pre-existing corpus has also been swept (`N1-PRIOR-CORPUS-RESCREEN.md`). The only
outstanding work is the formal database sweep; the substantive novelty question is settled as far as 827 papers and
10 deep reads can settle it.
**Analyst note:** verdicts below rest on full-text reads, not abstracts. Every claim is quotable from the linked
extraction note.

---

## 1. The N1 question, as set in ACQUIRE-T6.txt

> Beyond 10.1002/cnm.3822-type synthetic-perturbation FFR-CT sensitivity studies, has anyone (i) ranked *real*
> segmenter-disagreement error types by FFR 0.80 decision-flip effect, or (ii) shown that boundary-condition
> re-tuning in a reduced-order coronary flow model absorbs/masks topological segmentation error?

## 2. Evidence base

| Source | Count |
|---|---|
| New PDFs acquired 2026-09-17 and triaged | 168 (4 duplicate downloads excluded) |
| Prior corpus already extracted (2026-09-13 ideation run) | 624 |
| Stage-2 full-text deep reads commissioned for this gate | 5 (novelty) + 4 (feasibility, logged separately) |

Triage ledger: `../extraction/TRIAGE-LEDGER.tsv`. Per-paper notes: `../extraction/triage/`, `../extraction/full/`.
Triage buckets: METHOD 74, BACKGROUND 39, SUPPORT 35, IRRELEVANT 17, **THREAT 3**. All three THREAT flags were
escalated to full-text reads and all three were **downgraded** (§3).

## 3. The five closest works, and precisely where each stops short

| # | Work | What it establishes | Where it stops short of T6 |
|---|---|---|---|
| 058 | **Fernández-Martínez 2024**, 10.1002/cnm.3822 — designated closest prior work | Real-world segmentation-threshold variation propagates to FFR-CT, worst near 0.80 (severe distal 70%: FFR 0.879→0.860) | Single **global HU-threshold rescale** of the whole lumen — one error mechanism, not distinct types. 6%/15% magnitudes are **borrowed from Schepis 2010 / Leber 2006**, not measured on its own 14 patients; no Dice/Hausdorff anywhere. Continuous deltas only, no flip-rate table. Murray's-law re-tuning applied to every variant with **no untuned control** |
| 007 | **Gosling 2020**, 10.1016/j.jbiomech.2020.109698 — closest on the absorption *mechanism* | BC tuning demonstrably absorbs a large flow discrepancy: CMVR re-normalises 1.23e10→2.42e10 Pa/m³s⁻¹, absorbing ~65% inflow change; accuracy 75% vs 72%, AUC 0.84 vs 0.82. States tuning "may obviate differences in predicted FFR" | **Geometry never changes** — both models share one identical single-lumen geometry; the leakage term is a Murray's-law flow redistribution, not an added/removed/misconnected branch. Tuning is a **single cohort-averaged constant**, not per-case. **Aggregate metrics only**, zero per-case flip counts. Framed as *reassurance* for simpler models, not as a validation hazard |
| 093 | **Fossan 2025**, 10.1152/ajpheart.00442.2025 | **Strongest supporting precedent.** Swapping only the outlet BC model left **AUC unchanged (0.845 vs 0.845, p=0.915)** while sensitivity moved **58.1%→68.6% (p=0.0033)** and R² 0.179→0.398 — BC choice reclassified individual cases while the summary metric registered nothing | BC **model swap**, not re-tuning after geometric corruption. No per-case reclassification table. Geometry never perturbed |
| 072 | **Gamage 2022**, 10.3390/app12115573 — closest on the missed-side-branch error type | Branch-location asymmetry quantified: downstream removal 15.5% (idealised) / 13% (patient) FFR change vs upstream 0.002 / 2%. Analytical "<1/3 main-vessel diameter = negligible" rule | Held outlet resistance **fixed** across the with/without-branch comparison and merely *noted* that a differently-tuned external study reached the **opposite conclusion** — the contradiction is observed, never tested. Never reports an absolute FFR value, never mentions 0.80, no WSS/OSI, no diameter/location sweep |
| 092 | **Tanade 2022**, 10.3389/fmedt.2022.1034801 — flagged THREAT, downgraded | Physiological-input uncertainty alone reclassifies **50% of RCA / 25% of LCA cases at 1 SD** | "Geometry dominates" is an **asserted claim with no Sobol index behind it** — the analysis varied only cardiac output, distal location, stenosis degree and MAP on a **fixed geometry**. All three variants derive Windkessel resistance from each patient's own branch radii; "generalized" referred only to MAP/HR/hematocrit. No geometry-change-then-re-tune experiment exists |
| 075 | **Thondapu 2020**, 10.1115/1.4044095 — flagged as near-absorption, downgraded | Contrast-matched resistance optimisation holds FFR error <0.1% | **NOT-TESTED on geometry.** One fixed synthetic tree throughout; "generation of personalized geometrical models [is] outside the scope of this study." Absorbs resistance-parameter and measurement-noise error only. FFR "error" is CFD-vs-CFD self-consistency, not clinical validation |
| — | **Colebank et al. 2019**, R. Soc. Interface (`extraction/full/colebank-2019-segmentation-1d.md`) — **added 2026-09-17; structurally the closest precedent of all.** Mouse pulmonary micro-CT | The only prior work that propagates segmentation variation through a **reduced-order (1D)** haemodynamic model and decomposes the result into **geometry vs topology** — concluding **topology dominates** (~10 mmHg pressure discrepancy from 219→3-vessel pruning vs a narrower parameter-only spread). 25 networks, 185–505 vessels, 12–18 generations. Windkessel BCs **are recomputed after every geometry change** | **Threat is real but narrow, and confined to framing.** (i) Error source is 25 resamples of **two pre-segmentation algorithm parameters** in one automated pipeline — not real inter-observer disagreement, no second segmenter, no Dice/ICC. (ii) Decomposition is only "parameter" vs "network" via one monotonic smallest-volume-first pruning rule — no taxonomy of distinct error types; **taper is explicitly excluded from the model**. (iii) **No binary/threshold outcome anywhere** — all outcomes continuous (mmHg, flow, WI, PWV). (iv) BC recomputation is a **closed-form conservation rule, not an inverse fit to a target**, and the masking question is never posed; their own residual ~10 mmHg discrepancy survives re-adjustment, which argues *against* masking. **Reviewer risk to pre-empt:** "this was already shown in the pulmonary circulation; the coronary case is incremental." Cite it and distinguish on all four axes |
| — | **Sankaran, Grady & Taylor 2015**, 10.1109/TMI.2015.2445777 (IEEE TMI, HeartFlow) — **added 2026-09-17, the most serious prior work in this table.** Note: from the 2026-09-13 corpus, not the 203-paper batch | The strongest existing segmentation-uncertainty→FFR work: 240 patients (158 train / 82 test), adaptive stochastic collocation + ML surrogate, correlation 0.91 / MAE 0.0094. Ranks **regions** by geometric sensitivity σ*_FFR = max_x σ_FFR and uses it to direct human review. Quantifies allowable lumen-area c.o.v.: "less than a 6% coefficient of variation in lumen area will translate into a sensitivity of FFR_CT of less than 0.05 with 95% confidence" | **Wounds the "ranking" headline — it does not touch T6's other three axes.** (i) Perturbation is *one random variable per section*: "the entire section dilates or erodes in unison as we sample the stochastic space" — uniform radial dilation/erosion, **not distinct error types**, explicitly excluding local shape, asymmetric and topological error. (ii) Magnitudes are **assumed input dispersion**, never calibrated to measured inter-rater disagreement — no Dice/Hausdorff/surface-distance anywhere in the paper. (iii) Output is **continuous sensitivity (a standard deviation)**, never per-case reclassification across 0.80. (iv) BCs are **not re-tuned** after perturbation and there is no tuned-vs-untuned comparison. **Decisive gift:** its own limitations and future work name T6's contributions as open — "if a lumen narrowing is entirely missed in the initial segmentation, sensitivity information will not be captured"; "a missed bifurcation could change the sensitivity values"; and it calls for "a more accurate uncertainty model that accounts for image quality and initial lumen segmentation." T6 should cite these openings as its warrant |
| — | **Sankaran, Grady & Taylor 2015**, 10.1016/j.cma.2015.08.014 (CMAME 297:167–190) — **read 2026-09-17; the fourth and last paper of the HeartFlow thicket.** `extraction/full/sankaran-2015-cmame-geometric-uncertainty.md` | The methods paper behind the other three: adaptive Smolyak stochastic collocation accelerated by a bootstrap-decision-tree ML surrogate, trained on DiscoverFlow-90 / DeFACTO-240, plus a segment-granularity robustness check (55–600 segments) | **Leaves all four T6 legs intact — the weakest-grounded of the four siblings, not the strongest.** (a) **NOT COVERED**, and weaker than the 2016 paper: the perturbation magnitude u_max is "defined usually as a percentage of the radius" with **no citation to any measurement at all** — not inter-observer, not inter-modality, not elicited. (b) **NOT COVERED**: one error type only — a per-segment scalar radial dilation/erosion, circumferentially uniform — no eccentricity, no taper type, and **bifurcations are held fixed by construction**; the only variation tested is segment *granularity* (55–600), not error type. (c) **NOT COVERED**: all outputs continuous (σ_FFR, correlation, MAE/RMS); the 0.80 cutoff appears **exactly once, in the Introduction, motivationally**, with no reclassification count, table or confusion matrix anywhere. (d) **NOT COVERED**: outlet resistances computed once from anatomic/clinical scaling (Appendix B) and never re-derived after a perturbation; no tuned-vs-untuned comparison — the only "compensation" discussed is a passive series-circuit physics effect. **The sentence a hostile reviewer would quote, and it is a gift rather than a threat:** *"We limit the developments of this paper to uncertainty in lumen radius, since that is hypothesized to be the primary variable driving pressure loss near diseased regions... The validation of the perturbation model is restricted to deformation maps with fixed bifurcation locations."* That is HeartFlow drawing, in print, the exact boundary T6 crosses |
| — | **Sankaran, Kim, Choi & Taylor 2016**, J. Biomech. 49:2540–2547 (`Resources/1-s2.0-S0021929016000117-main.pdf`; `extraction/full/sankaran-2016-uncertainty-quantification.md`) — the fourth sibling, read 2026-09-17 | **The only one of the four that ranks geometry against boundary conditions**, and the only one grounded in any real measured error: ranks **MLD > boundary resistance > viscosity > lesion length** by continuous FFR_CT standard deviation / CI width against a ±0.03 measurement-reproducibility benchmark. MLD magnitude comes from real OCT-vs-CTA data (Choi 2015, 97 lesions / 23 patients) | **Wounds the "geometry vs BC ranking" claim; leaves (b), (c), (d) untouched.** T6 **cannot** claim to be first to rank geometry against boundary conditions — this paper did it. (a) **PARTIAL**: the real data is **inter-modality (OCT vs CTA), not inter-observer**; the lesion-length magnitude (±1 mm) cites an unspecified "inter-user variability study" with no N, annotators or metric; eccentricity/branch-loss/taper magnitudes are not sourced at all. (b) **NOT COVERED**: only two geometric scalars exist — global MLD and lesion length — and geometry is **axisymmetric by construction**. (c) **NOT COVERED**: no reclassification count anywhere; the one illustrative LAD case spanning ~0.6 to >0.8 is explicitly caveated by the authors as unrepresentative. (d) **NOT COVERED**: boundary resistance is an independent, fixed-distribution stochastic axis calibrated once from a separate 28-patient cohort and perturbed **in parallel with** — not in response to — geometry |
| — | **Korte et al. 2023**, Cardiovasc Eng Technol, 10.1007/s13239-023-00675-1 — **added 2026-09-18**, surfaced by the TAG novelty sweep, not by the corpus. *"Is Accurate Lumen Segmentation More Important than Outlet Boundary Condition in Image-Based Blood Flow Simulations for Intracranial Aneurysms?"* | **The closest anyone has come to T6's A-vs-B question using real multi-observer data.** 22 independent segmentations from 26 international groups (MATCH 2018 challenge, *"no instructions were given"* to maximise heterogeneity) crossed with **5 outlet BC models** (zero-pressure; Murray n=2; Murray n=3; Chnafa flow-splitting; Saalfeld anatomical). Headline: *"Excluding low fidelity segmentations... (a) reduces the deviation drastically (>43%) and (b) leads to a lower impact of the outlet BC on hemodynamic predictions"* → *"segmentation fidelity has a higher influence than outlet BC choice."* Deviation reductions on outlier exclusion: nAWSS 53–66%, LSA 54–59%, KER 60–78% | **Does not occupy T6's ground, but is the strongest "someone did geometry-vs-BC elsewhere" precedent yet.** (i) **Intracranial aneurysms**, 5 IAs from one patient; no FFR, no coronary, and **no generalisation claimed**. (ii) **No binary threshold or reclassification anywhere** — magnitudes and deviations only. (iii) BCs are **pre-computed from geometry before each simulation** (*"splitting values are calculated based on the geometric model prior to each simulation"*) — i.e. **Protocol B only; there is no Protocol C** target-matched re-tuning. (iv) Masking is never framed, and the paper finds the *opposite* direction: *"the presence of poor segmentation causes the influence of BC to be larger."* (v) No inter-observer agreement metric is reported in the paper itself (deferred to Berg et al.). (vi) Admits *"a ground truth is missing."* **Reviewer line to pre-empt:** this is now the fourth geometry-vs-BC comparison in a non-coronary bed (with Tanade, Colebank, Sankaran 2016) — the answer is that none of the four has a **decision threshold**, which is where the comparison stops being academic |

## 4. Verdict

**(i) Ranking real segmenter-disagreement error types by 0.80 decision-flip effect — NOT FOUND as a conjunction, but
the "ranking" half is no longer open ground.** No paper among the 827 examined works measures inter-segmenter
disagreement at matched quality, injects distinct error types at those magnitudes, and ranks them by decision-flip
rate. The field consistently reports *aggregate* accuracy/AUC or continuous uncertainty across a perturbation and
infers robustness from it.
**However — revised 2026-09-17, and this changes the framing:** HeartFlow has occupied the sensitivity-ranking
ground three times (TMI 2015 ranks *regions*; JBiomech 2016 ranks *variables* — MLD > boundary resistance >
viscosity > lesion length; MICCAI 2014 is the precursor), and Colebank 2019 already ranks *geometry vs topology* in
a 1D model. **A headline built on "ranking" is therefore wounded and should not lead the paper.** What none of them
does is the conjunction: real inter-*observer* magnitudes, distinct error *types* including topological, **per-case
reclassification across 0.80**, and a **tuned-vs-untuned ablation**. The last two are wholly untouched by every
paper examined, and the decision-flip outcome is the most clinically legible of the four.

**(ii) BC re-tuning absorbing topological error — NOT FOUND as a controlled test, but the ground is more
crowded than STUDY-PLAN.md assumes.** The mechanism is demonstrated for non-topological discrepancies (Gosling),
the aggregate-blind-to-case-level dissociation is published (Fossan), and the tuned-vs-untuned contradiction is
visible but untested (Gamage). T6's contribution is the **controlled ablation** none of them ran.

## 5. Required changes to the claim (STUDY-PLAN.md §1–2)

The current wording oversells on one axis and undersells on a better one.

1. **Do not claim BC-tuning-can-mask-error as new.** Gosling 2020 shows it for flow discrepancy; cite it prominently
   and differentiate on four specific axes: *topological* error (not flow under-representation), *per-case* re-tuning
   (not a cohort-averaged constant), *per-case reclassification* reporting (not aggregate accuracy), and
   *validation-hazard* framing (not modelling convenience).
2. **Lead with the Gamage contradiction.** "Whether a missed side branch matters depends on whether the outlet
   resistance was re-tuned — and the literature disagrees accordingly" is a stronger, evidenced opening than a
   speculative hypothesis, and it makes the ablation the resolution of a live disagreement.
3. **Pre-register both directions.** Tanade's (unevidenced) geometry-dominance position and Gosling's absorption
   position predict opposite outcomes. A null — "re-tuning cannot rescue topological error; anatomical fidelity is
   irreducible" — is equally publishable for this SI, but only if committed to in advance.
4. **Stratify the missed-branch arm by branch location relative to the stenosis.** Gamage's 15.5%-vs-0.002
   asymmetry means an unstratified design averages the effect away.

## 6. Outstanding before N1 can be closed

- [ ] Run the ACQUIRE-T6 database search strings against Scopus/WoS/PubMed + arXiv/bioRxiv. This log is
      corpus-derived; a corpus assembled by the operator is not a systematic search and cannot rule out a
      2026 paper nobody downloaded.
- [x] **RESOLVED 2026-09-17 — and it exposes a flaw in this log's own method.** An independent review
      (`FABLE-REVIEW-2026-09-17.md`) flagged a HeartFlow paper by Sankaran/Grady/Taylor as missing. The citation it
      gave was wrong in the title, which is why the paper read as absent. The real paper is:
      **Sankaran S, Grady L, Taylor CA, "Fast Computation of Hemodynamic Sensitivity to Lumen Segmentation
      Uncertainty," IEEE Transactions on Medical Imaging 34(12):2562–2571, Dec 2015, DOI 10.1109/TMI.2015.2445777**
      (PMID 26087484; verified independently against Crossref and Semantic Scholar).
      **It was never missing.** The PDF is at
      `Resources/Fast_Computation_of_Hemodynamic_Sensitivity_to_Lumen_Segmentation_Uncertainty.pdf`, it was extracted
      in the 2026-09-13 run
      (`Proposal/ideation_run/2026-09-13/extraction_mapped/Fast_Computation_of_Hemodynamic_Sensitivity_to_Lumen_Segmentation_Uncertainty.md`,
      slug `sankaran-2015-hemodynamic-sensitivity`), and **`ACQUIRE-T6.txt` item 2 already named it as required
      reading.**
      **Method flaw, now corrected:** §2 of this log counted the 624 prior extractions in its evidence base, but the
      N1 analysis had only mined the 203 new papers plus the commissioned deep reads.
- [x] **624-note corpus swept, 2026-09-17.** Only 17 of the 624 notes mention FFR at all. All 17 were themed-scored
      and the top 14 re-screened against T6's four contributions — results in `N1-PRIOR-CORPUS-RESCREEN.md`.
      **Outcome: no new threat.** Nothing in the prior corpus performs (b) distinct error types or (d) BC-retuning
      masking. Two PARTIALs were raised: `donnelly-2018` on (a) — **resolved to NO**, its own extraction records that
      no segmentation-level agreement metric (Dice/Hausdorff/diameter delta) appears anywhere, only downstream ICC on
      the CT-FFR value; and `menon-2024` on (c) — **resolved to NO**, verified 2026-09-17: it reports only incidental
      narrative crossings ("FFR computed using Murray's law was below clinically-used thresholds... while the FFR
      computed using flow distributions from MPICT was above this threshold"), across 6 patients, with **no count,
      rate, table or confusion matrix** of reclassifications. Criterion (c) remains wholly unoccupied.
      **But menon-2024 is now SUPPORT evidence for (d), and should be cited there.** Comparing two boundary-condition
      approaches on the same anatomy (Murray's law vs CT-perfusion-informed), it reports: *"We developed a novel
      iterative approach to personalizing synthetic vasculature that estimates not only the parameters at the coronary
      outlets, but also dilates or constricts the synthetic vessels to match patient-specific flow and pressure
      targets."* **This is geometry and boundary conditions being traded against each other to hit the same targets** —
      published evidence that outlet pressure/flow targets do not uniquely determine the anatomy. That
      non-identifiability is precisely the premise T6's A/B/C ablation tests, and here it is stated as a feature of a
      working pipeline rather than recognised as a validation hazard.
- [x] **Sankaran MICCAI 2014 located and read in full, 2026-09-17.** The operator supplied the whole MICCAI 2014
      proceedings (`Resources/978-3-319-10470-6.pdf`); the chapter is at **pages 30–37**. It is the conference
      precursor to the TMI 2015 paper — same 240 patients, same 158/82 split, same correlation 0.910, same
      one-random-variable-per-section scheme. **Subsumed by TMI 2015; adds no new threat.** Two details worth using:
      it claims a missed *lesion* is covered "as long as the family of geometries encompasses the new minimum lumen
      diameter" — a claim about MLD range, explicitly **not** about topology, which is the gap T6 occupies; and its
      future work proposes only to "rank parameters in terms of their importance and perform feature selection" —
      ranking *features*, not error types.
- [x] **CLOSED 2026-09-17 — the HeartFlow thicket is fully resolved.** The operator supplied
      `Resources/1-s2.0-S0045782515002728-main.pdf` = **Sankaran, Grady & Taylor, CMAME 297:167–190, 2015,
      DOI 10.1016/j.cma.2015.08.014**, and it has been read in full (§3 table above).
      **All four papers by this group are now read and none touches T6's (b), (c) or (d):**
      MICCAI 2014 (precursor) → IEEE TMI 2015 (ranks *regions*) → CMAME 2015 (the methods paper) → J Biomech 2016
      (ranks *variables*). Every one of them perturbs lumen radius as a per-section or per-segment scalar with
      bifurcations fixed, reports continuous sensitivity rather than threshold reclassification, and never re-tunes
      boundary conditions after a geometric change.
      **Consequence for the paper:** cite all four together and dispatch them in one paragraph — a JBHI reviewer who
      knows this literature will expect the thicket to have been untangled, and untangling it is itself evidence of
      command of the field.
- [ ] **Re-read Dalmaso 2025 (corpus id 061) with fresh eyes.** The same review reports it supplies real
      polynomial-chaos UQ evidence (52 patients) that *geometry dominates* — the evidence Tanade 2022 only asserts.
      It was triaged SUPPORT/FULL but never deep-read. It strengthens the null branch and belongs in §3's table.
- [ ] **D1 dependency, newly identified and material.** T6's contribution (a) requires *measured* inter-segmenter
      disagreement. ImageCAS-X appears to carry one annotation per case. If it holds no repeat/multi-annotator
      segmentations, T6 falls back to borrowed literature magnitudes — precisely the weakness it criticises in
      cnm.3822 — and the differentiator on (a) is lost. Verify on the Zenodo record before WP-0. Mitigation if
      absent: one trained annotator re-segments ~20 cases to yield a real disagreement distribution.
- [ ] **Confound to control (Tanade).** Physiological-input uncertainty alone reclassifies 50% of RCA cases at 1 SD.
      The error-injection effect must be reported against this baseline or a reviewer will attribute the flips to
      physiological noise.
- [ ] **Protocol constraints (Fossan).** Outlet resistance must be coupled to the resting pressure drop, so
      re-tuning after a geometry change must **re-simulate the resting state first**, not re-fit a free scalar;
      severity-to-resistance constants stay population-level, not per-case.

## 7. Provenance

Corpus triaged by fixed-schema extraction (`../extraction/SCHEMA.md`) over text obtained with
`../extraction/tools/t6slice.sh` (pdftotext; no page rendering). Stage-2 notes in `../extraction/full/` carry
verbatim quotes and section pointers for every decisive claim above.
