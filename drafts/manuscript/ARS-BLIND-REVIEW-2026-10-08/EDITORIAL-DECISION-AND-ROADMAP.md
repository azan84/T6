# Editorial Decision Package

## Manuscript Information
- **Title**: Topological Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study
- **Target venue**: IEEE Journal of Biomedical and Health Informatics (JBHI)
- **Manuscript ID**: n/a (simulated blind review)
- **Decision Date**: 2026-10-08
- **Review Round**: 1 (ARS `reviewer_full`, sprint contract `reviewer/reviewer_full/v2`)

## Review Panel Provenance (#540)

All five reviewer personas ran on a single model family (Anthropic Claude). Persona diversity is not model diversity — blind spots may be correlated across reviewers (Ren et al. 2026, arXiv:2607.13104 §5.2). The cross-model reviewer track was inactive (ARS_CROSS_MODEL not configured), so no cross-family check exists for any seat or for this decision. Blind condition: each reviewer received only the compiled manuscript and supplement (extracted text plus page images); no project notes, logs, study plans, earlier reviews or code were provided. The synthesizer read the same manuscript and supplement only to verify reviewer claims.

---

## Mechanical Decision (sprint contract, §8 three-step protocol)

### Step 1 — Role-scoped scoring matrix

| Dim | Name | Priority | Eligible seats | Assessed scores | Verdict |
|-----|------|----------|----------------|-----------------|---------|
| D1 | methodology_rigor | mandatory | methodology | methodology = warn | warn |
| D2 | domain_accuracy | mandatory | domain | domain = block (repairable) | block |
| D3 | argumentative_coherence | mandatory | da, methodology | da = block (repairable); methodology = block (repairable) | block |
| D4 | cross_disciplinary_relevance | high | perspective | perspective = warn | warn |
| D5 | writing_and_structure | normal | eic | eic = warn | warn |
| D6 | venue_fit_and_contribution | mandatory | eic | eic = warn | warn |

Ineligible `not_assessed` entries are excluded. No seat declared a fatal block.

### Step 2 — Failure conditions

| Condition | Severity | Quantifier | Expression | Evaluation | Fired |
|-----------|----------|------------|------------|------------|-------|
| F1 | 95 | any | any mandatory dimension has a fatal block | no fatal block on D1, D2, D3, D6 | no |
| F2 | 90 | any | any mandatory dimension scores 'block' | D2 (domain block) and D3 (da and methodology block) | yes |
| F3 | 70 | majority | two or more mandatory dimensions score 'warn' or worse | D1 (1/1 seat), D2 (1/1), D3 (2/2), D6 (1/1) all at warn or worse: 4 mandatory dimensions | yes |
| F4 | 60 | any | any high-priority dimension scores 'block' | D4 = warn | no |
| F5 | 40 | any | any dimension scores 'warn' or worse | all six dimensions | yes |
| F0 | 10 | all | every dimension scores 'pass' | no dimension passes | no |

### Step 3 — Precedence

Fired: F2 (90), F3 (70), F5 (40). Highest severity is F2, whose action is major revision. The action is not softened.

dimension_verdicts: [D1=warn, D2=block, D3=block, D4=warn, D5=warn, D6=warn]
fired_conditions: [F2, F3, F5]
da_critical_adjudications: [C1=VALIDATED]
editorial_decision=major_revision

---

## Part 1: Editorial Decision Letter

Dear Authors,

Thank you for submitting "Topological Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study" to IEEE JBHI. The manuscript was assessed by five reviewers: a Journal-Fit Reviewer (Associate Editor, EIC seat), Reviewer 1 (methodology, R1), Reviewer 2 (clinical coronary physiology, R2), Reviewer 3 (imaging informatics and model credibility, R3) and a Devil's Advocate (DA).

### Decision: Major Revision

Both blocks are repairable; no reviewer declared a fatal flaw. All reviewers credit the design: paired ablation, decision-level endpoint referenced to repeat-FFR and simulated noise floors, cross-bed replication rule, transparent exclusion accounting and Wilson intervals and Holm-adjusted McNemar p-values that R1 recomputed and reproduced (EIC S1–S3; R1 S1–S6; R2 S1–S4; R3 S2–S3). The revision concerns inference and framing, plus one physiological-regime question.

### Top Blocking Issues (ranked)

| Rank | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|------|----------------|--------------------|-----------------|------------------------|
| 1 | The 3D case shows removal of the missed-branch FFR error under prescribed flows, yet the text, abstract and Conclusion say it shows or reproduced concealment; the concealment claim is generalised beyond the one-scalar tuning tested | DA C1; R1 W1, W2; R2 W2, W3 | text: Results III-D "The 3D solution showed the same concealment." versus "by −0.0007 (0.892 in both geometries)" | R1, R2 |
| 2 | Hyperemic flow is well below human values (median demand 1.5 mL/s ≈ 90 mL/min per tree), and the ±30% demand sensitivity does not reach the physiological range while moving pass-while-wrong from 12% to 25% | R2 W1; R1 W6 | text: Sec. II-B "median demand was 1.5 mL/s (inlet radius 1.39 mm)" | R7 |
| 3 | Abstract and Discussion attribute concealment to tuning of topological errors, but Protocol A already passes-while-wrong more often in the leaky bed (20% vs 8%), and the tuned taper error reaches 24%, contradicting the "minor risk" guidance | R1 W3, W4; EIC W1; R3 W1; DA M2, M4 | table: Table I — T4, Protocol C, leaky bed, Passes and wrong 24 (18–31) | R4, R5 |

### Reviewer Summary

The v2 cards carry dimension scores, not an overall recommendation; the scores are listed instead.

| Reviewer | Role | Dimension scores | Per-finding confidence (range) |
|----------|------|------------------|--------------------------------|
| Journal-Fit Reviewer (EIC) | Associate Editor, JBHI computational/in silico medicine | D5 warn, D6 warn | 3–5 |
| Reviewer 1 (R1) | Computational hemodynamics and UQ | D1 warn, D3 block (repairable) | 3–5 |
| Reviewer 2 (R2) | Clinical coronary physiologist, CT-FFR | D2 block (repairable) | 3–5 |
| Reviewer 3 (R3) | Imaging informatics, topology-aware segmentation, V&V40 | D4 warn | 3–5 |
| Devil's Advocate (DA) | Senior sceptic, image-based modelling | D3 block (repairable) | 3–5 |

### Synthesizer verification of reviewer claims against the manuscript

| Claim | Reviewer(s) | Verified in manuscript |
|-------|-------------|------------------------|
| 3D prescribed-flow ΔFFR −0.0007 (0.892 both geometries), twin −0.0005; text says "showed the same concealment"; Conclusion says "A three-dimensional case reproduced this concealment"; Discussion IV-A "showed the same mechanism" | DA C1; R1 W1; R2 W2 | Yes (Results III-D, IV-A, Conclusion) |
| Abstract: "A perfusion-matched coronary model can thus pass validation with a material error" placed after the 3D sentence | DA C1, M5; R2 W5; R3 W6 | Yes |
| Median demand 1.5 mL/s, inlet radius 1.39 mm | R1 W6; R2 W1 | Yes (Sec. II-B) |
| Table I leaky bed, Protocol C, passes and wrong: T1 11 (6–21), T2 6 (3–12), T4 24 (18–31) | EIC W1; R1 W4; DA M4 | Yes |
| Table I discrete T2 n = 60 / 96 / 60 (A/B/C) | R1 W5; EIC W8 | Yes |
| Supplement S2 "10 of 5 860 noise-floor draws": Table S5 gives 1 940 + 2 990 solved, i.e. 4 940 draws with the 10 failures | R1 W13 | Yes — 5 860 is inconsistent |
| Supplement S2 "2 856 corrupted models were attempted": 2 964 possible minus 162 not applicable = 2 802 = 2 599 solved + 203 Protocol-undefined (Table S1) | R1 W13 | Yes — 2 856 is inconsistent |
| Code and cohort list "available from the corresponding author on request" | EIC W5; R1 W17; R3 W8 | Yes |
| Ref. [9] is a patient-specific biomechanical (pulmonary-valve) study cited for coronary flow-split tuning | EIC W7; R2 W10 | Yes (reference list) |

### Consensus Analysis

Consensus is counted per sub-claim over the four non-DA reviewers (EIC, R1, R2, R3); DA findings are tracked separately. `not-mentioned` is silence, not agreement.

#### Sub-claim inventory (Step 1b, condensed)

| SC | Sub-claim | Raised / corroborated by (severity, confidence) | Silent | Disputed | Count | Disposition |
|----|-----------|--------------------------------------------------|--------|----------|-------|-------------|
| SC-1 | 3D case shows removal, not concealment; "same concealment"/"reproduced" claims contradict the reported numbers | R1 W1 (Major, 5); R2 W2 (Major, 5) | EIC, R3 | — | 2/4 | Corroborated + DA C1 VALIDATED |
| SC-2 | Concealment rate is specific to one global scaling; not representative of per-territory perfusion tuning; claim generalised | R1 W2 (Major, 4); R2 W3 (Major, 4) | EIC, R3 | — | 2/4 | Corroborated + DA C1 VALIDATED |
| SC-3 | Post-calibration residual is called "validation" | R2 W5 (Major, 4); R3 W6 (Major, 4) | EIC, R1 | — | 2/4 | Corroborated (+ DA M5) |
| SC-4 | Concealment not specific to topological error (tuned taper 24%); "minor risk" guidance and abstract remedy unsupported | EIC W1 (Major, 4); R1 W4 (Major, 4); R3 W1 (Major, 4; "limit the caliber is minor conclusion") | R2 | — | 3/4 | CONSENSUS-3 (+ DA M4) |
| SC-5 | Attribution of concealment to tuning fails against Protocol A in the leaky bed; no paired test on pass-and-wrong | EIC W1 (Major, 4); R1 W3 (Major, 4) | R2, R3 | — | 2/4 | Corroborated (+ DA M2) |
| SC-6 | Concealment rate not tested against its own (demand-matched) noise floor; ablation targets noise-free | R1 W3 (Major, 4), W18 (Minor, 4) | EIC, R2, R3 | — | 1/4 | Single-reviewer (+ DA M3) |
| SC-7 | Abstract rates depend on the band-stratified cohort enriched near 0.80 | EIC W2 (Major, 4); R3 W3 (Major, 4); R1 W8 (Minor, 4) | R2 | R1 severity (Minor vs Major) | 3/4, severity split | SPLIT (severity) — arbitrated below |
| SC-8a | Topological-vs-caliber ranking rests on design-chosen magnitudes; state as conditional per-occurrence impact | EIC W3 (Major, 4); R3 W2/W3 (Major, 4); R1 W15 (Minor, 4) | R2 | R1 severity (Minor vs Major) | 3/4, severity split | SPLIT (severity) — arbitrated below (+ DA M1) |
| SC-8b | Measure T1/T2 incidence in real segmentation outputs on the ImageCAS-X test split | EIC W3 (Major, 4); R3 W2 (Major, 4) | R1, R2 | — | 2/4 | Corroborated |
| SC-9 | HD95/DSC mapped to lesion length/uniform taper; one-signed caliber errors | R1 W15 (Minor, 4); R2 W9 (Minor, 3); R3 W1 (Major, 4, mapping sub-point) | EIC | R3 severity | 3/4, severity split | SPLIT (severity) — arbitrated below |
| SC-10 | Throat-radius caliber error omitted | R3 W1 (Major, 4) | EIC, R1, R2 | — | 1/4 | Single-reviewer |
| SC-11 | Detection performance (sens/spec/AUC, threshold) of the pre-tuning residual not reported | EIC W4 (Major, 4); R3 W5 (Major, 4) | R1, R2 | — | 2/4 | Corroborated |
| SC-12 | Code, error generators, cohort list on request only; pre-specification unverifiable | EIC W5 (Major, 5); R1 W16, W17 (Minor, 4–5); R3 W8 (Minor, 4) | R2 | severity (Major vs Minor) | 3/4, severity split | SPLIT (severity) — arbitrated below |
| SC-13 | Hyperemic demand sub-physiological; radius definition biased low; demand sensitivity too narrow | R2 W1 (Major, 4); R1 W6 (Major, 3) | EIC, R3 | — | 2/4 | Corroborated; drives D2 block |
| SC-14 | 3D twin verifies the reduced-order model at a different radius; invariance assertion unsupported | R1 W7 (Major, 4) | EIC, R2, R3 | — | 1/4 | Single-reviewer |
| SC-15 | Protocol comparisons in Table I/abstract mix instance sets; no-outflow Protocol A exclusions not missing at random | R1 W5 (Major, 4) | EIC, R2, R3 | — | 1/4 | Single-reviewer (DA logic chain ii) |
| SC-16 | Perfusion territories (first-bifurcation subtrees) too coarse vs clinical segmental perfusion | R2 W4 (Major, 4) | EIC, R1, R3 | — | 1/4 | Single-reviewer |
| SC-17 | 0.80 crossing equated with a treatment change; grey zone ignored | R2 W6 (Major, 4) | EIC, R1, R3 | — | 1/4 | Single-reviewer |
| SC-18 | Tuned topological results describe the left tree; abstract/Conclusion lack qualifier | EIC W12 (Minor, 4); R3 W9 (Minor, 3) | R1, R2 | — | 2/4 | Corroborated |
| SC-19 | Caliber-vs-floor statements stronger than intervals; floor uses SD of a difference | R1 W12 (Minor, 4); R2 W8 (Minor, 3) | EIC, R3 | — | 2/4 | Corroborated |
| SC-20 | 3D mesh criterion missed (main text silent); "below 0.001" finer than case resolution | EIC W11 (Minor, 4); R1 W9 (Minor, 5) | R2, R3 | — | 2/4 | Corroborated |
| SC-21 | 3D "clean" ambiguous; 0.870 vs 0.892 baselines unexplained | R1 W19 (Minor, 3); R2 W13 (Minor, 3) | EIC, R3 | — | 2/4 | Corroborated |
| SC-22 | Ref. [9] off-topic for coronary flow-split tuning | EIC W7 (Minor, 4); R2 W10 (Minor, 3) | R1, R3 | — | 2/4 | Corroborated |
| SC-23 | Positioning omits segmentation-uncertainty and topology-metric literature | EIC W6 (Minor, 3); R3 W7 (Minor, 5) | R1, R2 | — | 2/4 | Corroborated |
| SC-24 | Missing side-branch/topology/FFR-outcome references | R2 W14 (Minor, 4) | EIC, R1, R3 | — | 1/4 | Single-reviewer |
| SC-25 | No segmentation-QC metric computed for corrupted trees | R3 W4 (Major, 5) | EIC, R1, R2 | — | 1/4 | Single-reviewer |
| SC-26 | Informatics contribution implicit; practical steps not operational | EIC D6 rationale, W4 (Major, 4); R3 W5 (Major, 4) | R1, R2 | — | 2/4 | Corroborated |
| SC-27 | Wilson intervals ignore clustering | R1 W10 (Minor, 4) | others | — | 1/4 | Single-reviewer |
| SC-28 | Table S2 Severity row identical across beds; variational intervals | R1 W11 (Minor, 3) | others | — | 1/4 | Single-reviewer |
| SC-29 | Supplement counts 5 860 and 2 856 do not reconcile | R1 W13 (Minor, 4) | others | — | 1/4 | Single-reviewer; synthesizer-verified |
| SC-30 | Leaky-bed damping explanation conflicts with Protocol A definition | R1 W14 (Minor, 3) | others | — | 1/4 | Single-reviewer |
| SC-31 | Gosling reconciliation mapped to the wrong protocol | R2 W7 (Minor, 3) | others | — | 1/4 | Single-reviewer |
| SC-32 | Ref. [2] is a methods paper, not a trial | R2 W11 (Minor, 4) | others | — | 1/4 | Single-reviewer |
| SC-33 | Commercial CT-FFR demand is mass-based, misdescribed | R2 W12 (Minor, 4) | others | — | 1/4 | Single-reviewer |
| SC-34 | Table I pass-and-wrong denominators only in footnote | EIC W8 (Minor, 5) | others | — | 1/4 | Single-reviewer |
| SC-35 | Fig. 2 per-band n/intervals missing | EIC W9 (Minor, 4) | others | — | 1/4 | Single-reviewer |
| SC-36 | Fig. 5 rainbow map, red/green cue, p/Pa label | EIC W10 (Minor, 4) | others | — | 1/4 | Single-reviewer |
| SC-37 | No schematic of bed structures and protocols | R3 W10 (Minor, 4) | others | — | 1/4 | Single-reviewer |

No sub-claim reached CONSENSUS-4. One reached CONSENSUS-3 without dispute (SC-4); four reached three reviewers with a severity split (SC-7, SC-8a, SC-9, SC-12).

#### Points of Agreement (Consensus)

**[CONSENSUS-3]**
1. SC-4 — The tuned taper result (Table I, T4, Protocol C, leaky bed, 24% passes and wrong, above T1 11% and T2 6%) contradicts the Discussion's "treat diameter errors of inter-observer size as a minor risk" and the abstract's remedy, which covers branching structure only. Agree: EIC W1, R1 W4, R3 W1. Silent: R2. DA M4 concurs (confidence 5).

**Corroborated findings (2/4, no conflict) that carry decision weight**
- SC-1 and SC-2 (R1, R2; DA C1) — the 3D reading and the generality of the concealment claim. See DA adjudication.
- SC-3 (R2 W5, R3 W6; DA M5) — "pass validation" describes a calibration-fit residual.
- SC-5 (EIC W1, R1 W3; DA M2) — the tuning attribution holds only against Protocol B.
- SC-13 (R2 W1, R1 W6) — sub-physiological hyperemic flow; owner-seat basis of the D2 block.
- SC-11 and SC-26 (EIC W4, R3 W5) — the checks the paper recommends have no reported detection performance.

#### Points of Disagreement

**Disagreement 1: Severity of the cohort-enrichment qualification (SC-7)**
- **EIC W2 / R3 W3**: Major — clinical readers will take the abstract percentages as risk estimates; lead with the topological/caliber ratio and, if possible, reweight to a clinical FFR distribution.
- **R1 W8**: Minor — qualify the abstract figures and report discrete-bed band counts; reweighting optional.
- **Disagreement type**: Severity disagreement (existence and remedy agree).
- **Editor's Resolution**: Required as a text fix (qualify all abstract rates as conditional on the band-stratified design; report discrete-bed band counts; lead with the ratio). Reweighting to a clinical distribution is optional (P2).
- **Resolution Rationale**: Three of four reviewers agree the qualification is needed; the disagreement concerns only whether reweighting is required. The text fix resolves the shared concern at low cost.

**Disagreement 2: Severity of the magnitude-dependence of the topological/caliber ranking (SC-8a, SC-9)**
- **EIC W3 / R3 W2–W3 / DA M1**: Major — the ranking is a statement about chosen magnitudes; measure incidence or sweep magnitudes.
- **R1 W15 / R2 W9**: Minor — justify or relabel the HD95/DSC mappings as design choices and add opposite-sign caliber errors.
- **Disagreement type**: Severity disagreement.
- **Editor's Resolution**: Required (text): restate the ranking as conditional, per-occurrence impact at the chosen magnitudes and describe T1–T4 magnitudes as design choices. Suggested (new computation): incidence measurement (SC-8b), magnitude sweeps and opposite-sign caliber errors.
- **Resolution Rationale**: All five seats agree the magnitudes are design choices (the manuscript says so, Sec. II-C); the text remedy is common to every position, while the computational remedies are not agreed as necessary.

**Disagreement 3: Severity of code/cohort-list access (SC-12)**
- **EIC W5**: Major (confidence 5) — the reusable test is the paper's main informatics value and cannot be adopted on request.
- **R1 W16–W17 / R3 W8**: Minor — standard reproducibility expectation.
- **Disagreement type**: Severity disagreement.
- **Editor's Resolution**: Required. Deposit code, error generators, frozen cohort list and per-instance results with a DOI; report the hash or time-stamped record; mark analyses as pre-specified or post hoc.
- **Resolution Rationale**: Venue fit is the EIC seat's owned dimension (D6), and the remedy is administrative and inexpensive.

**Note on EIC S4.** The EIC lists the 3D case as a strength ("reproduces the mechanism"). This credits the fixed-resistance arm (+0.074) and the reduced-order twins; it does not argue that the prescribed-flow arm shows concealment. It is recorded as not-mentioned on SC-1, not as a dispute.

### DA CRITICAL Adjudication

**C1 (D3) — Data-conclusion mismatch on the 3D/concealment headline, with an untested rival explanation.**
- **DA argument**: Under prescribed clean territory flows the 3D missed-branch error vanishes (ΔFFR −0.0007; twin −0.0005), the opposite of concealment as defined in Sec. II-D. Results III-D, Discussion IV-A and the Conclusion nonetheless say the 3D case showed or reproduced concealment, and the abstract leads from the 3D sentence to "A perfusion-matched coronary model can thus pass validation with a material error". The residual Protocol C error plausibly reflects the one-scalar global tuning and the 10% tolerance, which no per-territory arm tests.
- **Corroboration**: R1 W1 (Major, confidence 5) and R2 W2 (Major, confidence 5) independently reach the same reading of the 3D numbers; R1 W2 and R2 W3 (Major, confidence 4) independently request a per-territory tuning arm and restriction of the claim. No reviewer disputes it.
- **Evidence check**: Verified in the manuscript — Results III-D "The 3D solution showed the same concealment." followed by "the same error changed FFR by −0.0007 (0.892 in both geometries)"; Conclusion "A three-dimensional case reproduced this concealment."; Sec. II-D "the least flexible tuning a pipeline could use".
- **Adjudication**: VALIDATED. The data-conclusion mismatch is factual and on a headline claim. The rival explanation is not proven, but the manuscript currently asserts the 3D case as confirmation, so the burden is on the claim. Validation does not void the reduced-order result: the cohort shows pass-while-wrong under one-scalar tuning, and that narrower finding stands (DA "What survives"; R1, R2).
- **Required author action**: Correct every 3D statement (abstract, III-D, IV-A, Conclusion) to "per-outlet flow prescription removed the error; fixed resistances did not"; restrict the concealment claim to one-scalar global tuning unless a per-territory arm shows otherwise (R1, R2 below).

The DA's MAJOR items M1–M5 are each corroborated by at least one non-DA reviewer and enter the roadmap through SC-8a (M1), SC-5 (M2), SC-6 (M3), SC-4 (M4) and SC-3 (M5).

### Decision Rationale

The decision follows the contract mechanically. Two mandatory dimensions are at block: D3 (argumentative coherence), where both eligible seats (DA, R1) independently blocked on the abstract stating a stronger or differently directed effect than the data support, and D2 (domain accuracy), where R2 blocked on a hyperemic flow regime well below human values. F2 therefore fires and sets Major Revision; F3 and F5 also fire at lower severity. Both blocks are marked repairable, and no reviewer found a fatal flaw, so Reject is not indicated.

The substance is consistent with the mechanics. The paired ablation, statistics and accounting are sound (R1 reproduced the Wilson intervals and Holm-adjusted McNemar p-values). The problems are in what the paper claims from those results. (i) The 3D case contradicts the concealment wording attached to it (DA C1, validated; R1 W1; R2 W2). (ii) The concealment rate is shown only for one-scalar tuning (R1 W2; R2 W3). (iii) Concealment occurs for the caliber taper and without tuning, which the abstract, Discussion and practical advice omit (EIC W1; R1 W3, W4; R3 W1). (iv) "Pass validation" names a calibration residual (R2 W5; R3 W6). (v) The flow regime may set the magnitudes (R1 W6; R2 W1). Most of (i)–(iv) are text corrections; (ii) and (v) need new reduced-order runs to settle rather than to restate.

A lighter decision is not available because two mandatory dimensions block. A stricter one is not warranted because every block is repairable with the existing pipeline and the core design is endorsed by all seats.

### Required Revisions (Must Fix)

| # | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source Reviewer | Section | Work type |
|---|--------------|--------------|----------|-----------------|------------|----------------|---------|-----------|
| R1 | Correct all 3D statements: prescribed flows removed the error; drop "same concealment"/"reproduced this concealment"/"same mechanism"; stop using the 3D result to support the "pass validation" sentence | SC-1 | critical (DA C1) / major | text: Results III-D "The 3D solution showed the same concealment." | 5 — R1, R2 direct reading | DA C1; R1 W1; R2 W2 | Abstract, III-D, IV-A, V | Text only |
| R2 | Restrict the concealment claim to one-scalar global tuning; add a per-territory (one scaling per territory) Protocol C′ arm and report pass, wrong, pass-and-wrong | SC-2 | critical (DA C1) / major | text: Sec. II-D "so this is the least flexible tuning a pipeline could use" | 4 — R1, R2 core expertise | DA C1; R1 W2; R2 W3 | Abstract, II-D, III-B, IV-A, IV-D | Text (minimum) + new reduced-order runs (full fix) |
| R3 | Replace "pass validation" with calibration-fit/perfusion-fit check wording; add a V&V40 context-of-use sentence | SC-3 | major | text: Abstract "pass validation with a material error in its fractional flow reserve" | 4 — R2, R3 | R2 W5; R3 W6; DA M5 | Abstract, IV-A, IV-C | Text only |
| R4 | Report concealment for all error classes including tuned taper 24% (leaky); withdraw or condition the "minor risk" guidance and the branching-only remedy on whether boundary conditions are tuned; explain the mechanism | SC-4 | major | table: Table I — T4, Protocol C, leaky bed, Passes and wrong 24 (18–31) | 4 — EIC, R1, R3 | EIC W1; R1 W4; R3 W1; DA M4 | Abstract, IV-A, IV-C, V | Text only |
| R5 | State the tuning attribution relative to Protocol B only; report Protocol A pass-while-wrong rates; add paired exact McNemar (Holm) on pass-and-wrong for C vs B and C vs A; qualify the leaky-bed figure and the "record the mismatch before tuning" step (leaky B residual 0.04) | SC-5 | major | table: Table S3 — Leaky, T1+T2, 10% column: A 20 (15–26) vs C 8 (5–13) | 4 — EIC, R1 | EIC W1; R1 W3; DA M2 | Abstract, III-B, IV-A, IV-C | Text + computation from existing outputs |
| R6 | Qualify abstract and Discussion rates as conditional on the band-stratified cohort and on the chosen error magnitudes (per-occurrence impact); lead with the topological/caliber ratio; report discrete-bed band counts; describe T1–T4 magnitudes as design choices | SC-7, SC-8a | major (EIC, R3) / minor (R1) | text: Sec. II-A "we drew 25 in each of six 0.05-wide bands of baseline FFR" | 4 — EIC, R1, R3 | EIC W2, W3; R1 W8, W15; R3 W3; DA M1 | Abstract, II-A, II-C, IV-A, V | Text only |
| R7 | Address the flow regime: report inlet/proximal radii against normative values, quantify the half-voxel radius bias, extend demand sensitivity to the physiological range (about ×2–×3) or calibrate demand to vessel/mass norms, and report Table I (or its key cells) there | SC-13 | major | text: Sec. II-B "median demand was 1.5 mL/s (inlet radius 1.39 mm)" | 4 — R2 core expertise (R1: 3) | R2 W1; R1 W6 | II-B, III, IV-D, Supp. S4 | New reduced-order runs + text |
| R8 | Deposit code, error generators, frozen cohort list and per-instance results with a DOI; give the cohort-list hash or time-stamped record; mark each analysis pre-specified or post hoc | SC-12 | major (EIC) / minor (R1, R3) | text: Data and Code Availability "The code and the frozen cohort list are available from the corresponding author on request." | 5 — EIC | EIC W5; R1 W16, W17; R3 W8 | Data and Code Availability, II-F | Text/admin only |

### Required Item Details

**R1: Correct the 3D interpretation**
- **Problem**: With clean territory flows prescribed, the missed branch changed 3D FFR by −0.0007 (twin −0.0005), which is removal of the error, not concealment; the manuscript says the opposite in III-D, IV-A and V and uses the result to lead into the "pass validation" sentence.
- **Source**: DA C1; R1 W1; R2 W2.
- **Requirement**: Rewrite the 3D sentences: fixed resistances +0.074 (twin +0.081); per-outlet prescribed flows removed the error. Remove the 3D case as evidence of concealment. Optionally (new 3D runs) solve the 3D case under a one-scalar condition equivalent to Protocol C (R1 W1, R2 W2).
- **Acceptance criteria**: No sentence in the abstract, Results, Discussion or Conclusion states that the 3D case showed, reproduced or confirmed concealment.

**R2: Restrict the concealment claim to the tuning tested**
- **Problem**: Pass-while-wrong rates (8–19%) come from one global bed scaling, which cannot redistribute territory flow; perfusion-informed pipelines tune per territory or outlet.
- **Source**: DA C1; R1 W2; R2 W3.
- **Requirement**: Minimum (text): every concealment statement names one-scalar global tuning. Full fix (new runs): add Protocol C′ with one scaling per territory and report pass, wrong and pass-and-wrong rates per bed.
- **Acceptance criteria**: The abstract claim is limited to global-scaling tuning, or a per-territory arm is reported and the claim matches its result.

**R3: Calibration, not validation**
- **Problem**: The residual is computed against the same targets the scaling was fitted to; V&V40 does not treat this as validation.
- **Source**: R2 W5; R3 W6; DA M5.
- **Requirement**: Use "calibration-fit (perfusion-fit) check"; reserve "validation" for independent data; add one sentence on context of use (deferral vs revascularisation at 0.80).
- **Acceptance criteria**: "Pass validation" no longer describes the post-tuning residual anywhere in the manuscript.

**R4: Caliber concealment and the "minor risk" guidance**
- **Problem**: The tuned taper is the largest pass-while-wrong cell in Table I (24%, leaky), yet IV-C calls inter-observer diameter errors a minor risk and the abstract prescribes a branching-structure check only.
- **Source**: EIC W1; R1 W4; R3 W1; DA M4.
- **Requirement**: Report the concealment endpoint for caliber and topological errors together; state which check detects which error class; make the practical guidance conditional on tuning; give the mechanism (matching clean flows through a narrowed lumen enlarges the stenotic drop).
- **Acceptance criteria**: Abstract, IV-C and Conclusion are consistent with Table I T4 under Protocol C.

**R5: Tuning attribution and its test**
- **Problem**: In the leaky bed, Protocol A passes-while-wrong more often (20%) than Protocol C (8%); only C vs B agrees in both beds, and no paired test of pass-and-wrong is reported.
- **Source**: EIC W1; R1 W3; DA M2.
- **Requirement**: Phrase the claim relative to re-derived boundary conditions; report Protocol A rates in the main text; add exact McNemar with Holm on the pass-and-wrong indicator (C vs B, C vs A) per bed; revise the "record the mismatch before tuning" step to reflect that the pre-tuning mismatch flagged the error mainly in the discrete bed.
- **Acceptance criteria**: The abstract's tuning sentence is supported by a reported paired test in both beds, or it is restricted to where it holds.

**R6: Conditional rates and conditional ranking**
- **Problem**: Abstract percentages depend on a cohort enriched near 0.80 and on near-worst-case topological magnitudes; readers will take them as risks.
- **Source**: EIC W2, W3; R1 W8, W15; R3 W3; DA M1.
- **Requirement**: Label rates as conditional on the band-stratified design and chosen magnitudes; lead with the topological/caliber ratio; report discrete-bed band counts; describe the ranking as per-occurrence impact.
- **Acceptance criteria**: Each abstract rate carries the conditional qualifier, and IV-A no longer states population-level decision risk.

**R7: Physiological flow regime**
- **Problem**: Median demand 1.5 mL/s (≈ 90 mL/min) per tree is about one third to one fifth of human hyperemic flow; pass-while-wrong rises monotonically with demand (Table S4) and the sensitivity range stops at ×1.3.
- **Source**: R2 W1; R1 W6.
- **Requirement**: Report radii against normative values and the half-voxel radius bias; rerun at physiological demand (or ×2–×3) and report the key Table I cells; discuss how the regime affects magnitudes.
- **Acceptance criteria**: Results at a physiologically plausible hyperemic flow are reported, or the claims are explicitly bounded to the flow regime modelled with the bias quantified.

**R8: Open code and verifiable pre-specification**
- **Problem**: The proposed pipeline test cannot be reused, and the pre-specification claim cannot be checked.
- **Source**: EIC W5; R1 W16, W17; R3 W8.
- **Requirement**: Archive code, generators, cohort list and per-instance results with a DOI; report the hash or registration; flag post hoc analyses (13%/16% thresholds, demand sensitivity, simulated floor, mixed model); add missing rerun parameters (R1 W17).
- **Acceptance criteria**: The Data and Code Availability statement cites a DOI and the hash or registration record.

### Suggested Revisions (Should Fix)

| # | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source Reviewer | Priority | Section | Work type |
|---|--------------|--------------|----------|-----------------|------------|----------------|----------|---------|-----------|
| S1 | Report detection performance (threshold, sensitivity, false-alarm rate or AUC) of the pre-tuning residual for topological error vs correct anatomy (simulated floor) and vs caliber error; state the informatics contribution (reusable error-injection test + pre-tuning check) in the Introduction; name one implementable topology check | SC-11, SC-26 | major | absence: Results III-B and Discussion IV-C — expected detection performance of the pre-tuning perfusion residual | 4 | EIC W4; R3 W5 | P2 (highest-value P2 for D6) | I, III-B, IV-C | Computation from existing outputs + text |
| S2 | Common-instance-set comparisons for Table I/abstract; state treatment of no-outflow Protocol A models and add an FFR = 1 sensitivity | SC-15 | major | table: Table I — T2, discrete bed, n = 60 (A), 96 (B), 60 (C) | 4 | R1 W5 | P2 | Table I, III-A, Abstract | Computation from existing outputs |
| S3 | Report pass-and-wrong excess over a demand-matched simulated floor; optionally rerun Protocol C with noisy targets | SC-6 | major / minor | text: Results III-B "3.1% (2.4–4.0%) and 3.9% (3.2–4.6%) of draws" | 4 | R1 W3, W18; DA M3 | P2 | III-B, Supp. S4–S5 | Existing outputs (excess, test) + new runs (noisy targets) |
| S4 | Report the cohort-model ΔFFR for the 3D instance on the requested radius next to +0.081 and +0.074, or remove the invariance assertion | SC-14 | major | text: §IV-D "this offset shifts absolute FFR but not the paired differences" | 4 | R1 W7 | P2 | III-D, IV-D | One reduced-order solve, or text only |
| S5 | Add a throat-local caliber error (±0.5/±1 voxel at minimal lumen) or limit the caliber conclusion to T3/T4 | SC-10 | major | text: §III-D "throat area-equivalent radius 0.276 against" | 4 | R3 W1 | P2 | II-C, III-A, IV | New runs, or text only |
| S6 | Measure (or cite) incidence of missed distal branches and breaks in benchmark segmentation outputs on the ImageCAS-X test split | SC-8b | major | text: Section II-C "T1 and T2 have no measured magnitude and are design choices." | 4 | EIC W3; R3 W2 | P2 | II-C, IV | New analysis (heavy) — defer; text qualifier covered by R6 |
| S7 | Compute DSC, HD95, clDice, Betti and overlap-until-first-error for corrupted trees and relate to |ΔFFR| | SC-25 | major | text: §IV-B "branch removes few voxels, so the error types that carried the" | 5 | R3 W4 | P2 | III, IV-B | Computation from existing geometries |
| S8 | Territory granularity: justify first-bifurcation territories or test finer territories | SC-16 | major | text: Sec. II-D "A perfusion territory is the subtree below each child of the first bifurcation of the clean tree." | 4 | R2 W4 | P2 | II-D, IV-D | New runs, or limitation text |
| S9 | Report grey-zone reclassification (<0.75 ↔ >0.85) alongside 0.80 flips; call 0.80 crossings classification changes | SC-17 | major | text: Sec. II-F "A flip is a change of classification at 0.80 between the two, that is, a change in the treatment decision." | 4 | R2 W6 | P2 | II-F, III-A | Computation from existing outputs + text |
| S10 | Justify or relabel the HD95→lesion-length and DSC→taper mappings; optionally add opposite-sign caliber errors | SC-9 | minor (R1, R2) / major (R3) | text: §II-C "HD95 (2.46 mm) sets" | 4 | R1 W15; R2 W9; R3 W1 | P2 | II-C | Text (new runs optional) |
| S11 | Add left-coronary qualifier to tuned topological results in abstract and Conclusion; report dominance | SC-18 | minor | text: Section IV-D "so its results for these errors describe the left coronary tree" | 4 | EIC W12; R3 W9 | P2 | Abstract, V | Text only |
| S12 | Correct caliber-vs-floor statements (pooled discrete caliber 10.3%, CI 6.8–15.4%, above floor; leaky T4 A lower bound 5.6% inside floor); report or justify the 0.018 vs 0.018/√2 floor | SC-19 | minor | text: §III-A "Only the taper under fixed boundary conditions exceeded this noise floor" | 4 | R1 W12; R2 W8 | P2 | Abstract, III-A, II-F | Text (+ trivial recomputation) |
| S13 | State in III-D that the pre-set mesh criterion was missed; give the 3D prescribed-flow effect as zero within about 0.002 | SC-20 | minor | text: Section III-D "a regenerated mesh at 25 µm reproduced the baseline value" | 5 | EIC W11; R1 W9 | P2 | Abstract, III-D | Text only |
| S14 | Define the source of 3D outlet resistances and prescribed flows; explain the 0.870 vs 0.892 baselines | SC-21 | minor | text: §III-D "0.892 in both geometries" | 3 | R1 W19; R2 W13 | P2 | II-E, III-D | Text only |
| S15 | Position against segmentation-uncertainty propagation and topology/centerline metrics (Schaap 2009, clDice, Betti matching, ASOCA); add side-branch/topology/outcome references (Vardhan 2019, Fossan 2018, Tonino 2010, Johnson 2014) | SC-23, SC-24 | minor | absence: Introduction and Discussion IV-B — expected positioning against segmentation-uncertainty propagation and coronary topology-metric studies | 3–5 | EIC W6; R3 W7; R2 W14 | P2 | I, IV-B | Text only (verify citations) |
| S16 | Replace ref. [9] with coronary flow-split/perfusion-calibration work | SC-22 | minor | text: Section I "measured flow splits [8], [9]" | 4 | EIC W7; R2 W10 | P2 | I, references | Text only |
| S17 | Cluster-robust (patient bootstrap) or mixed-model intervals for pooled proportions | SC-27 | minor | text: §II-F "Proportions are reported with Wilson 95% confidence intervals" | 4 | R1 W10 | P2 | II-F, Table I | Computation from existing outputs |
| S18 | Verify Table S2 Severity row; give random-effect variances; MCMC or VI check | SC-28 | minor | table: Table S2 — Severity (% DS) row, 0.019 (0.016, 0.022) in both beds | 3 | R1 W11 | P2 | Supp. S3 | Check; refit optional |
| S19 | Correct "10 of 5 860" (Table S5 implies 4 940 draws) and "2 856 attempted" (Table S1 implies 2 802) | SC-29 | minor | text: §S2 "10 of 5 860 noise-floor draws did" | 4 (synthesizer-verified) | R1 W13 | P2 | Supp. S2 | Text only |
| S20 | Fix the leaky-bed damping explanation in IV-A to match the Protocol A definition | SC-30 | minor | text: §IV-A "damping the error before tuning" | 3 | R1 W14 | P2 | IV-A | Text only |
| S21 | Describe Gosling 2020 correctly (taper-based leakage, analogue of the leaky bed) and soften "reproduced" | SC-31 | minor | text: Sec. IV-B "Both appear in our cohort, the first with fixed resistance and the second after tuning" | 3 | R2 W7 | P2 | IV-B | Text only |
| S22 | Describe mass-based total flow in commercial CT-FFR and which protocol it corresponds to | SC-33 | minor | text: Sec. I "Its resistance is not measured but derived from the segmented lumen through scaling laws" | 4 | R2 W12 | P2 | I | Text only |
| S23 | Table I: separate n column for pass-and-wrong denominators, or k/n | SC-34 | minor | table: Table I — T2 rows, n column (96; 147, 149) against footnote denominators (n = 60; n = 100) | 5 | EIC W8 | P3 | Table I | Text/table only |
| S24 | Fig. 2: per-band n or Wilson error bars; minimum band size in caption | SC-35 | minor | figure: Fig. 2 — discrete-bed T1 and T2 panels | 4 | EIC W9 | P3 | Fig. 2 | Replot from existing outputs |
| S25 | Fig. 5: perceptually uniform colour map, no red/green cue, axis label p/P_a | SC-36 | minor | figure: Fig. 5 (a)–(c) colour bar and (e)–(f) vertical-axis label p/Pa | 4 | EIC W10 | P3 | Fig. 5 | Replot |
| S26 | Replace ref. [2] for "multicenter trials" with DISCOVER-FLOW and DeFACTO (verify metadata) | SC-32 | minor | text: Sec. I "validated against invasive measurement in multicenter trials [2], [3]" | 4 | R2 W11 | P3 | I, references | Text only |
| S27 | Add a schematic of bed structures and Protocols A/B/C (main or supplement) | SC-37 | minor | text: §II-B "In the leaky bed, flow leaves along the vessel" | 4 | R3 W10 | P3 | Fig. 1 or Supp. | New figure (no computation) |
| S28 | Conclusion: quote the cross-bed range rather than the most extreme cell (43% → 5%) | — | minor (DA, below table threshold) | text: Conclusion "from 43% of models with fixed boundary conditions to 5% with re-derived ones" | — | DA (cherry-picking note) | P3 | V | Text only |

---

## Part 2: Revision Roadmap

Submission deadline context: 2026-10-15 (7 days). Each item is marked **[TEXT]** (manuscript edit only), **[EXIST]** (new numbers computed from outputs the pipeline already holds) or **[RUN]** (new reduced-order or 3D solves). The contract outcome is Major Revision regardless; the work-type tags only inform scheduling.

### Priority 1 — Must Fix

- [ ] R1 [TEXT] — Correct all 3D statements (abstract, III-D, IV-A, Conclusion): per-outlet prescribed flows removed the error. Sources: DA C1; R1 W1; R2 W2.
- [ ] R2 [TEXT minimum; RUN for full fix] — Restrict the concealment claim to one-scalar global tuning; full fix adds per-territory Protocol C′. Sources: DA C1; R1 W2; R2 W3.
- [ ] R3 [TEXT] — "Pass validation" → calibration-fit check; one V&V40 context-of-use sentence. Sources: R2 W5; R3 W6; DA M5.
- [ ] R4 [TEXT] — Report tuned taper concealment (24%) with topological; condition the "minor risk" guidance and the abstract remedy. Sources: EIC W1; R1 W4; R3 W1; DA M4.
- [ ] R5 [TEXT + EXIST] — Attribute concealment relative to Protocol B; add paired McNemar on pass-and-wrong (C vs B, C vs A); revise the pre-tuning step for the leaky bed. Sources: EIC W1; R1 W3; DA M2.
- [ ] R6 [TEXT] — Conditional qualifiers on abstract rates and on the ranking; lead with the ratio; discrete-bed band counts. Sources: EIC W2, W3; R1 W8, W15; R3 W3; DA M1.
- [ ] R7 [RUN + TEXT] — Physiological flow: radii vs norms, radius-bias quantification, demand at ×2–×3 or norm-calibrated, key Table I cells. Minimum if runs cannot finish: report radii and bias, and bound the claims to the modelled flow regime. Sources: R2 W1; R1 W6.
- [ ] R8 [TEXT/admin] — DOI deposit of code, generators, cohort list, per-instance results; hash or registration; pre-specified vs post hoc. Sources: EIC W5; R1 W16, W17; R3 W8.

### Priority 2 — Should Fix

- [ ] S1 [EXIST + TEXT] Detection performance of the pre-tuning residual; informatics contribution statement; one implementable topology check (EIC W4; R3 W5).
- [ ] S2 [EXIST] Common-instance-set comparisons; no-outflow Protocol A sensitivity (R1 W5).
- [ ] S3 [EXIST; RUN optional] Excess over demand-matched floor; noisy-target Protocol C (R1 W3, W18; DA M3).
- [ ] S4 [RUN, one solve; or TEXT] Cohort ΔFFR for the 3D instance on the requested radius (R1 W7).
- [ ] S5 [RUN; or TEXT] Throat-local caliber error, or limit the caliber conclusion (R3 W1).
- [ ] S6 [RUN, heavy — defer] Incidence of T1/T2-type events in benchmark outputs (EIC W3; R3 W2).
- [ ] S7 [EXIST] Segmentation-QC metrics vs |ΔFFR| (R3 W4).
- [ ] S8 [RUN; or TEXT] Finer perfusion territories, or limitation (R2 W4).
- [ ] S9 [EXIST + TEXT] Grey-zone reclassification; "classification change" wording (R2 W6).
- [ ] S10 [TEXT] HD95/DSC mapping relabelled as design choice; opposite-sign errors optional (R1 W15; R2 W9; R3 W1).
- [ ] S11 [TEXT] Left-coronary qualifier; dominance (EIC W12; R3 W9).
- [ ] S12 [TEXT] Caliber-vs-floor statements; floor SD choice (R1 W12; R2 W8).
- [ ] S13 [TEXT] Mesh criterion missed; 3D effect zero within ~0.002 (EIC W11; R1 W9).
- [ ] S14 [TEXT] 3D "clean" source and 0.870/0.892 baselines (R1 W19; R2 W13).
- [ ] S15 [TEXT] Positioning and missing references (EIC W6; R3 W7; R2 W14).
- [ ] S16 [TEXT] Replace ref. [9] (EIC W7; R2 W10).
- [ ] S17 [EXIST] Cluster-robust intervals (R1 W10).
- [ ] S18 [EXIST] Verify Table S2 Severity row (R1 W11).
- [ ] S19 [TEXT] Supplement counts 5 860 → 4 940-consistent and 2 856 → 2 802-consistent, or define "attempted" (R1 W13).
- [ ] S20 [TEXT] Leaky-bed damping explanation (R1 W14).
- [ ] S21 [TEXT] Gosling reconciliation (R2 W7).
- [ ] S22 [TEXT] Mass-based demand in commercial CT-FFR (R2 W12).

### Priority 3 — Optional

- [ ] S23 [TEXT] Table I denominators (EIC W8).
- [ ] S24 [EXIST] Fig. 2 per-band n or intervals (EIC W9).
- [ ] S25 [TEXT/replot] Fig. 5 colour map and axis label (EIC W10).
- [ ] S26 [TEXT] Ref. [2] trial citations (R2 W11).
- [ ] S27 [TEXT/figure] Bed and protocol schematic (R3 W10).
- [ ] S28 [TEXT] Conclusion quotes cross-bed range (DA).

### Scheduling note for the 2026-10-15 deadline

Pure text fixes: R1, R3, R4, R6, R8, S10–S16, S19–S23, S26, S28 (and the minimum versions of R2, R7, S4, S5, S8). Computation from existing outputs: R5, S1, S2, S3 (excess), S7, S9, S17, S18, S24. New solves: R2 full (Protocol C′), R7 (physiological demand), S3 (noisy targets), S4, S5, S8, S6 (heavy), optional 3D one-scalar run (R1). The two blocks map to R1–R6 (D3) and R7 (D2); R7's minimum text version bounds the claim but does not supply the result Reviewer 2 asked for.

### Handling of findings

These are simulated reviews. Each item above is to be recorded as fixed or declined, with a reason, in the revision log; no response-to-reviewers letter is prepared.

---

## Part 3: Reviewer Report Summary

- **Journal-Fit Reviewer (EIC)** — D5 warn, D6 warn. Fits JBHI; the contribution is framed as a hemodynamic finding, the proposed checks have no detection performance, code is on request, and the concealment message is narrower than Table I.
- **Reviewer 1 (Methodology)** — D1 warn, D3 block (repairable). Arithmetic and paired statistics reproduce; inference fails on the 3D reading, tuning parameterisation, Protocol A control, tuned caliber concealment, mixed instance sets and the flow regime.
- **Reviewer 2 (Domain)** — D2 block (repairable). Hyperemic flow well below human values with a narrow demand sensitivity; Protocol C and territories do not represent perfusion-informed practice; 3D shows removal; calibration called validation; grey zone ignored.
- **Reviewer 3 (Perspective)** — D4 warn. Throat-radius caliber error omitted; T1/T2 lack incidence data; no segmentation-QC metrics; practical steps not operational; V&V40 terminology.
- **Devil's Advocate** — D3 block (repairable). C1 VALIDATED (3D data contradict the concealment wording; rival explanation of under-parameterised tuning untested). M1–M5 all corroborated by at least one non-DA reviewer.

We encourage you to consider the reviewers' comments carefully and submit a substantially revised manuscript, which will undergo another round of review.
