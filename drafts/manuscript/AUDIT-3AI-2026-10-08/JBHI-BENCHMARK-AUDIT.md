# JBHI benchmark of reviewer-style audit findings (Paper6-T6, JBHI special-issue paper)

Date: 2026-10-08. No project file edited. Working files: scratchpad/jbhi/.

## 0. Corpus and caveats

Full text read (12 papers). IDs used below:

| ID | Paper | Source of text | Note |
|---|---|---|---|
| B1 | Ericsson 2024, 4D Flow SR (in silico CFD-derived + in vivo) | PMC11735690 (NIH author manuscript) | author manuscript, not IEEE typeset |
| B2 | Fu 2021, iPhantom | PMC8502243 (author manuscript) | |
| B3 | Shenoy 2025, camera ECGI | PMC12272559 (author manuscript) | |
| B4 | Peng & Malik 2022, Gaussian-basis ECGI | arXiv 2102.00570 | preprint; final IEEE layout UNVERIFIED |
| B5 | Tasken 2026, autoStrain (synthetic TEE) | arXiv 2511.02210 v1 ("submitted 5 Nov 2025") | preprint; may differ from JBHI 30(1) |
| B6 | Arminio 2026, PPV FSI | abstract only (Europe PMC) | full text UNVERIFIED: IEEE Xplore returns HTTP 202/418 to scripted fetch, WebFetch empty |
| B7 | Viceconti 2025, position paper | abstract only | full text UNVERIFIED (same block); not an empirical study |
| E1 | Alsammani 2024, circular statistics under measurement bias (simulation + real HFO data) | PMC10964323 | |
| E2 | Ma 2022, parameter sensitivity of SIR/SEIR models (pure in silico) | PMC9328724 | |
| E3 | Gomez-Exposito 2021, Kalman-filter epidemic tracking (simulated case + real data) | PMC9088803 | |
| E4 | Chen 2023, StairFit MUNE (simulation study + experimental) | PMC10032645 | |
| E5 | Martinez 2023, confidence-aware particle filter BP (repeated beats per subject) | PMC10567135 | |
| E6 | Oliveira 2022, CirCor dataset (multiple recordings per patient) | PMC9253493 | |
| E7 | Liu 2024, CiGNN cuffless BP (leave-one-subject-out) | PMC11100861 | |

Limits of the benchmark (stated plainly):
- Europe PMC/PMC holds only a small, NIH/IEEE-sponsored slice of JBHI. I found NO open-access JBHI paper on coronary FFR, reduced-order haemodynamics with segmentation-error injection, or Bayesian mixed models. The extras (E1-E7) are the nearest in kind that could be read in full: simulation/uncertainty/sensitivity (E1, E2, E3, E4), repeated-measures-per-patient data (E5, E6, E7). Cardiovascular CFD/FSI JBHI papers (B6, plus "Comparison of Numerical Models ... Ascending Thoracic Aortic Aneurysm", 2026; "Centerline-Aggregated Aortic Hemodynamics", 2022) were located but not readable (not open in PMC/arXiv).
- B1-B3, E1, E4, E5 are accepted author manuscripts: heading text and wording are final, but typeset details (reference sorting, table layout) are author-prepared. Q12 is therefore weak evidence.
- Counts are small (n = 10 to 12 per question). "Norm" below means what appears in most of this set, not an editorial rule. No JBHI author guideline was consulted for these questions (UNVERIFIED whether JBHI enforces any of them).
- Terms were found by regex on extracted text, then read in context. "0 hits" means no occurrence in the text read, not proof of absence in the typeset PDF (e.g. a data-availability footnote could be missed in a PMC XML).

---

## Q1. Reference terminology in simulation studies

- B1: no "ground truth" anywhere (0 hits). Neutral wording: "comparing high-resolution velocities to super-resolved equivalents" (Methods, Performance evaluation); "In lack of high-resolution reference data" (Methods, in vivo).
- B2: both terms. "compared to the ground truth" (Results, fill-in accuracy); "the same program used for both reference and predicted phantoms" (Discussion). XCAT phantom truth is known by construction.
- B3: "within a Euclidean distance of 2cm from the ground truth" (Methods); Discussion: "without access to ground-truth data, we cannot definitively link the observed error patterns".
- B4: no "ground truth" or "true value" (0 hits). Calls test inputs "synthetic" and compares with "expected" signals.
- B5: "synthetic TEE (synTEE) dataset of 80 patients with ground truth myocardial motion" (Abstract). Uses "ground truth" 28 times.
- E1: "the goal is to estimate the PDF of the true values, p(y)" (Methods); "correctly recover the true values" (Conclusion). Truth known by simulation.
- E5: "initial ground truth PP, DBP, and SBP" (calibration cuff values; measured, not simulated).
- E6: "only a binary ground truth variable (normal vs abnormal)" (Intro).
- E2, E3, E4, E7: no "ground truth" or "true value" for the simulated reference (E4 compares to "true number of motor units" in its simulation).
- B7 (abstract only): defines credibility as the predicted value not differing "from what we would measure experimentally". Full-text terminology UNVERIFIED. B6 (abstract only): "good agreement with available clinical measurements".

JBHI norm: "ground truth" / "true value" is routine in JBHI when the reference is known by construction (phantom, synthetic generator, simulated parameter: B2, B3, B5, E1, E4). Neutral "reference" appears in B1/B2. No paper in the set uses "true value" for a reference that is itself a model output being compared with a perturbed version of itself. Distinction: in B5/E1/B2 truth is injected, in our design the "clean model" is a model of the same tree. So the wording is defensible by journal custom but the overstatement is real on the merits.

## Q2. Clustered data

- B1: avoids leakage by design: "data was partitioned model-wise rather than sample-wise to maintain integrity and independence" (Methods). Tests are plain and pooled: Kolmogorov-Smirnov tests "sampling 10% of all inferred data points" (Methods); voxels within a model are not independent and this is not discussed.
- B2: leave-one-phantom-out and five-fold cross-validation; no CIs, no clustering statement.
- B3: five patients, per-patient error tables (Table II); no inferential clustering.
- B4: 70-30 split of generated pairs; mean +/- SD; no clustering statement.
- B5: 80 patients x 3 sequences each ("240 synthetic TEE sequences from 80 patients"; four decorrelation versions share the same motion). Bland-Altman limits of agreement on pooled segments; patient-level clustering caveat not found.
- E1: bootstrap-style: "the 95%-tile of the distribution ... gives a direct, numeric estimate of the threshold" over "1,000 iterations", resampling per patient and vigilance state (Methods, Simulation 4). Closest to cluster-aware, but it is a method paper.
- E5: test = one trial per subject held out; no cluster-aware CI; metrics over "more than 3500 test data points" pooled across subjects.
- E6: 1568 participants, multiple recordings per patient; Mann-Whitney U on distributions of heart rate and durations, p-values only; "656 heart sound recordings from an unknown number of patients" for another database (Methods).
- E7: leave-one-subject-out; Student's t-test, p<0.05, on pooled errors; no clustering statement.
- E2, E3, E4: not clustered (model-level or small n); E4 uses two independent runs per trial.
- Cluster-aware CIs, mixed models, GEE or cluster bootstrap in the main text: 0 of 11 empirical papers (E1 resamples within patient but is a method). Clustering caveat stated explicitly: 0 of 11.

JBHI norm: design-level separation (patient/model-wise splits, LOSO) is common (B1, B2, E7, E5). Cluster-aware inference and an explicit clustering caveat are absent in this set; pooled per-sample tests and CIs are the norm. Our main-text Wilson CIs plus a supplementary mixed model plus a stated clustering caveat already exceed what these papers do.

## Q3. Code availability

- Public repository with URL: B1 ("Complete setup and trained weights are publicly available at https://github.com/LeonEricsson/Ensemble4DFlowNet", Methods); E1 ("Matlab code has been posted to https://github.com/sgliske/unfolding", own section "Code Availability"). Count 2.
- Public dataset (and partly code): B5 ("first publicly available dataset of synthetic TEE data", Intro; code link not found in preprint); E6 (dataset; "a MATLAB code is provided" for R-peaks). Count 2.
- "Available on request" wording: 0 hits in all 12.
- No availability statement found: B2, B3, B4, E2, E3, E4, E5, E7. Count 8.
- B6, B7: UNVERIFIED.

JBHI norm: not enforced. 8 of 12 are silent; 2 of 12 have a public code repository, 4 of 12 release code or data publicly. "Upon reasonable request" is not even used here; silence is the modal practice. A stated request route is therefore no worse than the modal paper, but the two newest in-silico-adjacent examples (B1, E1) show a repository is the better-looking choice.

## Q4. Pre-registration, analysis plan, hash, post hoc labelling

- Regex for pre-registration, a priori, post hoc, exploratory, hash/SHA, analysis plan: no relevant hit in any of the 12 (hits were "a priori" in a model-class sense in E3, and a ClinicalTrials.gov/REB number for patient recruitment in B3).
- Abstract or conclusion labelling analyses as exploratory or post hoc: 0 of 12.
- E1/E2 describe pre-set simulation designs only as methods ("Experimental Design", E2), not as a plan.

JBHI norm: none. Pre-registration, hashing and post hoc labelling are absent from all papers read. Including them is extra rigour, not journal practice.

## Q5. Limitations

- B1: subsection "E. Limitations and future work" in Discussion, 537 words, 22 sentences, four numbered items ("First... Second... Third... Lastly"): synthetic-only training, no paired in vivo high/low-resolution data, ensemble compute cost, reduced interpretability.
- B2: one paragraph inside Discussion, 228 words, 12 sentences, four items: small/old XCAT dataset, global regularisation, error combined from separate parts, fixed-tube-current code validation.
- B3: no separate section; caveats woven into "Conclusion & Discussion" (five patients, larger cohort needed, electrode-occlusion by arms; "System Improvements").
- B4: no limitations section; future-work hedges only ("In the future, it can be hypothesized...").
- B5: subsection "Limitations and Future Work", 403 words, 18 sentences: 16-patient clinical set, synthetic data "may not fully capture the complex variability", single vendor (GE).
- E5: subsection "Limitations" (Discussion), 228 words: calibration point needed, test trials at most 8 minutes.
- E7: subsection "Limitation" (Discussion), 111 words, 3 items: mechanism not investigated, two-stage not end-to-end, confounders not modelled.
- E1-E4, E6: no labelled limitations; E4 has "Potential Pitfalls" and "Future Work".
- Typical item types: single/small dataset (B2, B3, B5, E7), synthetic target or simulation realism (B1, B5), no clinical or in vivo validation (B1, B5), single vendor or population (B5, E6), compute/interpretability (B1), missing confounders (E7).
- Length: labelled sections 111 to 537 words, median about 230 words; 5 of 12 have a labelled limitation block, 3 more have scattered caveats, 4 have none.

JBHI norm: a short Limitations paragraph or subsection (about 100-250 words, 3-5 items) is the modal practice; synthetic-reference and no-clinical-validation caveats are standard when a study is in silico. Not uniformly present (4 of 12 omit it), so thoroughness there is optional polish; a brief one is expected.

## Q6. Practical recommendations

- No paper uses "we recommend" or "recommendation" for practice (0 hits; E6 hit is "recommendation systems").
- E2 (pure model sensitivity): conclusion is a table "Summary of the Sensitivity Analysis and Implications for Prevention and Control"; abstract says findings "suggest that protection and isolation measures should always be implemented in conjunction and started as early as possible". Assertive, from model sensitivity only, with no "not validated" hedge.
- B1 and B5 hedge by direction: B5 "potentially improving patient outcomes", "Our next steps will involve further clinical validations"; B5 limitation: performance in real-world scenarios "may exhibit variability not captured in this study".
- E7: "has not been investigated yet" (mechanism); future-study sentence. B6 (abstract): "support the potential use of patient-specific FSI modelling".
- Explicit "not validated" hedge in abstract: 0 of 12.

JBHI norm: practice implications are phrased as "implications", "suggest", "potential", "next steps", not as "recommendations/steps". An explicit validation hedge is not conventional in the abstract; it appears, when at all, in the limitations. Calling items "considerations" or "hypotheses" is stricter than the set; calling them "steps" is stronger than any paper here except E2.

## Q7. Tables with differing denominators

- n in text or caption, not in cells: B1 ("three (n=3) different subjects", "25, 5, and 6 out of 36 assessed metrics"); B2 ("XCAT (n=50) and clinical (n=10)"; "140 kVp (n=1), 120 kVp (n=8)").
- n in column header: E7 Table VI "Age groups 20-40 (n=28) 40-60 (n=79) 60-80 (n=92) 80-100 (n=6)".
- Table notes/footnotes for definitions or standards: E7 ("Note: AAMI standard requires ..."), E7 Table II ("T, F indicates ..."). Not used for denominators.
- Separate n columns: not found. B3 gives per-patient rows (Table II).
- E6 reports percentages with mixed bases in prose and Table II ("1568 participants, 787 (50.2%) male").

JBHI norm: weak. Denominators are given in text or column headers; separate n columns and denominator footnotes are not seen. Any of the three is acceptable; n in the header is the most common table form.

## Q8. Identical Methods and Results subsection titles

Subsection titles extracted from the XML for 10 papers (B4, B5 not extracted; UNVERIFIED).
- B1: Methods = "Models and data preparation / Network setups / Performance evaluation"; Results = "Parametric in-silico validation and quantitative accuracy assessment / Quantifying generalizability into an unseen domain / In-vivo verification and clinical potential". Different.
- B2 (Validation vs Results): "Segmentation validation" vs "Geometry validation"; "Application to new CT data" vs "Application to new clinical CT data". Near-parallel, not identical.
- E1: Simulations 1-4 only under results. E5, E7: Methods and Results titles differ; E7 Results "Evaluation of BP Estimation Methods" vs Methods "Data Analysis and Model Evaluation".
- Only duplicate title in the corpus: E4 "StairFit MUNE" (Methods vs Discussion, not Results).
- Exact Methods/Results duplicates: 0 of 10.

JBHI norm: not seen; parallel (not identical) subsection naming is common. Because identical headings are rare and the page budget is binding, renaming is cheap and consistent with practice, but nothing here shows the journal rejects them.

## Q9. Conclusion claims

- "We have shown": B1 ("we have shown how ensemble learning enables ...", three sentences, no numbers, scope stated "across disparate flow domains"); B4 ("We have shown that a network trained on basis function HSPs ... can be used to predict experimental recordings"); B2 ("We showed that the framework precisely localized ..."); E1 ("simulations which demonstrate the method can correctly recover the true values").
- Restates numbers: B2 ("high accuracy (< 10% organ dose error)"); E5 ("more than 3500 test data points", Grade A); B5 abstract (0.65 +/- 0.20 mm); not in B1, B3, B5 and E7 conclusions.
- Generalisation: B1 "applicable across the heart, aorta, and brain" (the three tested domains); B2 "may be useful for other applications"; E1 "apply to a wide variety of analyses in basic, translational, and clinical biomedical research" (strongest); B5 "AI can play a crucial role in advancing cardiac diagnostic methodologies".
- Scoped or hedged: B5 ("promising clinical applicability", "potentially"), B7 abstract ("limited to the test sets used for the validation studies"), B6 abstract ("support the potential use").
- No paper claims "any pipeline"; none uses a scope sentence of the form "in this in silico setting".

JBHI norm: moderately confident declaratives ("we have shown/showed") scoped to the tested domains are standard; conclusions of 3-6 sentences mostly without numbers (numbers restated in 2 of 11). Hedged scope is common but not required.

## Q10. Abstract qualifiers

- B1: states "in-silico", "synthetic training data", "both in-silico and acquired in-vivo data"; per-condition split by domain (cardiac, aortic, cerebrovascular). No "to our knowledge".
- B4: "Synthetic pulses", "in-vitro pig hearts", per-condition effect ("A shift of the heart 40 mm toward the spine resulted in a 4% increase in signal feature localization error").
- B5: "highly realistic synthetic TEE", "ground truth", "Clinical validation on 16 patients" with agreement stated as mean difference and 95% limits of agreement.
- E1: "simulated ... several toy examples as well as ... a real-world example".
- E3: abstract states simulated case plus real data (UNVERIFIED wording beyond the limitations line "A hypothetical simulated case is used to show the adequacy and limitations").
- B6 (abstract): "Pulmonary artery ... geometries from four patients", "good agreement with available clinical measurements".
- "Untested" or "not validated" in abstract: 0 of 12. "To our knowledge": 0 of 12. Novelty is asserted by "first" or "novel": B2 ("for the first time"), B5 ("the first automated pipeline"), E6 ("for the first time"), many "novel" (B1, B2, B3, E1, E3, E4, E5).

JBHI norm: in silico/synthetic is stated in the abstract when the data are synthetic (B1, B4, B5, E1); per-condition qualifiers are present when results differ by condition (B1, B4). No "untested/to our knowledge"; hedging wording lives in the body.

## Q11. Solver reproducibility detail

- B1 (CFD-generated data): solver not described; "model and solver setup were identical to what has been presented in similar, previous work [28]" (Methods). No relaxation factor, iteration limit or initialisation for the CFD.
- Deep learning papers report optimiser and schedule (B1: Adam, lr 1e-4, 60/80 epochs; B2: "24,000 iterations", lr 10e-3 then 10e-4). These are training hyperparameters, not solver convergence settings.
- E3: forward Euler stated; filter gains "initialized to 1" (state initialisation reported). E1: "1,000 iterations" for the Monte Carlo threshold. E5: particle filter "initialized with a prior distribution", tolerance 0.5 mmHg.
- Relaxation factor, maximum iterations for a numerical solver: reported in 0 of 12.

JBHI norm: reproducibility detail on optimisers and Monte Carlo sizes is reported; numerical-solver convergence settings are delegated to references or omitted. B6 (FSI) full text UNVERIFIED and is the most likely paper to report solver settings.

## Q12. Citation ordering and ranges in brackets

- Ascending in every group: B1 (11 sets), B2 ("[1, 2]", "[1-10]", "[7, 10-12]" style; older bracket format), B3, B5, E1, E2, E3, E4, E5, E7.
- Compressed ranges "[a]-[b]": B1 ("[17]-[20]"), B3 ("[6]-[9]", "[30]-[32]"), E2 (6), E3, E5 ("[7]-[9]"). 5 of 12.
- Non-ascending groups: B4 arXiv preprint (11 groups, e.g. "[7], [8], [3]", "[18], [14]", "[26], [25]"); E6 (1: "[33], [30]"). So 2 of 12 contain unsorted brackets, both in the author-prepared text.
- Final typeset IEEE copies not inspected: UNVERIFIED whether production sorted or compressed them.

JBHI norm: ascending order inside brackets and "[a]-[b]" for runs are the default (10 of 12 fully sorted). Unsorted groups survive in 2 author-prepared texts, so the journal does not visibly enforce it at manuscript stage; sorting is a minor typesetting concern, free to fix.

---

## Summary table

| Q# | JBHI norm | Strength (n papers) | Implication for the finding |
|---|---|---|---|
| Q1 | "Ground truth/true value" used freely when truth is injected by construction (phantom, synthetic generator); "reference" also used; no paper uses it for model-vs-perturbed-model | Mixed (n = 8 with relevant usage; 4 silent) | Not a norm violation; optional wording fix to "reference" is cheap and avoids an overstatement that exists on the merits |
| Q2 | Pooled per-sample CIs/tests plus patient-wise splits; no cluster-aware CI and no clustering caveat in the main text | Moderate (n = 11 empirical) | Optional (our cluster handling already exceeds the set); a one-line caveat is enough |
| Q3 | Mostly no statement (8 of 12); public repo 2 of 12; "on request" 0 of 12 | Moderate (n = 12) | Not a norm; repository preferred but "on request" is no worse than silence |
| Q4 | None report a plan, hash, or post hoc/exploratory labels | Strong for absence (n = 12) | Not a norm; do not spend pages |
| Q5 | Short limitations paragraph or subsection (about 110-540 words, median about 230), 3-5 items incl. synthetic target, small data, no clinical validation; 4 of 12 omit it | Moderate (n = 12) | Enforce a brief, specific limitations block; length beyond about 150-250 words is optional |
| Q6 | "Implications/potential/next steps"; no "recommendations"; no explicit "not validated" hedge in abstracts | Weak to moderate (n = 12; E2 is an assertive exception) | Optional; scope wording ("considerations") is safer than "steps" but not required by practice |
| Q7 | n in text/caption or column header; no separate n columns or denominator footnotes | Weak (n = 4 informative) | Optional; any clear method acceptable |
| Q8 | No identical Methods/Results titles (0 of 10) | Moderate for absence (n = 10; B4, B5 UNVERIFIED) | Cheap to fix, not a documented norm |
| Q9 | "We have shown/showed" scoped to tested domains; 3-6 sentences; numbers restated in 2 of 11; no "any pipeline" claim | Moderate (n = 11) | Enforce scoping (avoid "any pipeline"); restating numbers is optional |
| Q10 | In silico/synthetic stated in abstract when data are synthetic; per-condition qualifiers when results differ; no "untested"/"to our knowledge" | Moderate (n = 8 relevant; B6 abstract only) | Enforce "in silico" and per-condition scope in the abstract; do not add "untested"/"to our knowledge" |
| Q11 | Optimiser and Monte Carlo settings reported; numerical-solver convergence settings delegated to refs or omitted (0 of 12 report relaxation/max iterations) | Weak (n = 1 CFD-generating paper readable; B6 UNVERIFIED) | Not a norm; a citation to solver setup suffices |
| Q12 | Ascending order inside brackets and "[a]-[b]" ranges standard (10 of 12 sorted; 5 of 12 compressed ranges) | Weak (author-prepared text; typeset UNVERIFIED) | Optional but free: sort and compress at typesetting |
