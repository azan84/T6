# Statistics analysis plan — Paper 6 / T6

**v1.0, 2026-09-18. To be lodged with the OSF pre-registration BEFORE any ablation run.**
Cohort: `COHORT-FROZEN-2026-09-18.csv` (SHA-256 in `COHORT-FROZEN-2026-09-18.sha256`).
Design: `SEVERITY-SWEEP-SPEC.md`; 3D arm: `CFD-ARM-SPEC.md` v0.2; hypotheses: `STUDY-PLAN-v2.md` §4.
**Nothing in this document may be changed after the pre-registration is locked.** Anything not specified here and
reported later is labelled exploratory, in the paper, in those words.

---

## 1. What is being tested

For each instance (one lesion in one real coronary tree) the model is corrupted by a segmentation error type, the
boundary conditions are handled under one of three protocols, and FFR is recomputed at a measurement point 20 mm
distal to the lesion. The paper's claim is about **what happens to the clinical decision when the model is re-tuned
to match its validation targets**, so the estimand is a **within-instance contrast**, never a between-instance one.

**Primary estimand.** For instance *i*, error type *t*, protocol *p*, bed structure *b*:
```
ΔFFR(i,t,p,b) = FFR(corrupted, i,t,p,b) − FFR(clean, i,b)
```
and the decision outcome
```
flip(i,t,p,b) = 1[ FFR(corrupted) ≤ 0.80 ] ≠ 1[ FFR(clean) ≤ 0.80 ]
```
each judged against **that instance's own clean baseline in that bed structure** — never against a baseline from the
other structure or another instance.

## 2. Unit of analysis and clustering — fixed in advance

| level | n | why it matters |
|---|---|---|
| instance | 150 | the analysis unit |
| distinct slot (tree × vessel × location × length) | 134 | **16 slots contribute 2 instances** (two severities): 32 instances are not independent |
| tree (patient × side) | 108 | |
| **patient** | **93** | 15 patients contribute both left and right trees; 38 patients contribute 2 instances, 9 contribute ≥ 3, max 4 |

**The random effect is at PATIENT level** (`scan`), not tree and not instance. A tree-level effect would treat the two
coronary trees of one patient as independent when they share anatomy, image quality, dominance and acquisition.
Where a slot appears twice, a nested slot term is included: `(1 | scan/slot)`.

## 3. Declared structural confounding — **not** corrected by design

Band, severity and length are confounded **by physics, not by sampling**. FFR is a monotone function of stenosis
severity, so the FFR band a lesion lands in is largely determined by its severity. In the frozen cohort:

| %DS | 0.65–0.70 | 0.70–0.75 | 0.75–0.80 | 0.80–0.85 | 0.85–0.90 | 0.90–0.95 |
|---|---|---|---|---|---|---|
| 40 | 0 | 0 | 0 | 0 | 0 | 7 |
| 50 | 0 | 0 | 0 | 0 | 0 | 4 |
| 55 | 0 | 0 | 0 | 1 | 9 | 6 |
| 60 | 0 | 0 | 1 | 5 | 7 | 4 |
| 65 | 0 | 3 | 7 | 9 | 4 | 3 |
| 70 | 10 | 14 | 9 | 5 | 3 | 1 |
| 75 | 8 | 4 | 5 | 5 | 2 | 0 |
| 80 | 7 | 4 | 3 | 0 | 0 | 0 |

**Decision: declare, do not rebalance.** Forcing severity balance within band would require selecting lesions whose
FFR contradicts their severity — i.e. selecting on atypical host geometry — which would (i) destroy the cohort's
agreement with clinical practice (the 0.80 crossing currently falls at 65–70 %DS, where invasive FFR puts it),
(ii) make a quarter of the cohort anatomically unrepresentative, and (iii) replace a transparent confound with an
opaque one carried by host geometry. Because every endpoint is a within-instance contrast, the confound does **not**
bias the primary analysis; it limits only marginal statements comparing severity against length, which are therefore
**not made**. Length is better balanced (10 mm 80 / 20 mm 70, spread across all bands) and vessel is balanced by
construction (LAD 50 / LCx 50 / RCA 50, 8–9 per band).

**Consequences, all pre-specified:**
- No claim of the form "severity matters more than length" or any marginal severity-vs-length comparison.
- Severity enters every model as a covariate so that no protocol or error-type effect can be attributed to it.
- Any severity or length effect reported is **within band**, or explicitly labelled confounded.

## 4. Primary analyses

**P1 — decision flips by error type and protocol (H1, H2, H3).**
Mixed-effects logistic regression, all bed structures analysed separately:
```
flip ~ error_type * protocol + ds_pct + L_mm + band + (1 | scan/slot)
```
Reported as **P(flip | baseline-FFR band)** with Wilson 95 % intervals, per error type × protocol, plotted against the
physiological-noise floor of §6 on the same axes. Protocol contrasts (B−A, C−A, C−B) are **paired within instance**
and tested with McNemar's exact test; the ΔFFR analogue uses a paired mixed model
`ΔFFR ~ error_type * protocol + ds_pct + L_mm + (1 | scan/slot)`.

**P2 — absorption (the thesis).** The joint outcome (territory-perfusion residual after tuning, FFR error at the
measurement point), for **every** protocol — not Protocol C alone, because the comparison between protocols is the
evidence. Absorption is the region *residual small while |ΔFFR| remains large*.

**Definitions fixed before the run and before registration:**
- **"Passes its validation check" = territory-perfusion residual < 10 %.** **Citation resolved 2026-09-19**
  (`references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md`); the value stands, the justification is restated because
  the previous one conflated two statistics that differ by a factor of ~2.8:
  - the **within-subject coefficient of variation** (wsCV), the spread of one measurement about its own mean; and
  - the **repeatability coefficient** (RC ≈ 2.77 × within-subject SD), the 95 % bound on the difference between
    **two** independent measurements.

  The figure of "10–15 %" in the earlier text is a **wsCV** — traceable to Schindler et al., *JACC Cardiovasc
  Imaging* 2023;16(4):536–548 — while the sentence used it as an agreement bound. **Our residual compares a
  deterministic model output against one noisy measurement — one noise draw, not two — so the RC's √2 does not
  apply.** The statistically correct 95 % bound for this comparison is **≈ 0.13–0.16** at the published
  per-territory hyperaemic wsCV.

  **0.10 therefore sits just below the measurement-precision band: a stricter check than strictly required, and
  strict in the safe direction.** The headline proportion P(passes ∧ materially wrong) is **monotone non-decreasing
  in the threshold**, so any looser and equally defensible threshold could only *increase* the absorption count.
  **The number makes H2 conservative, and that — not the citation — is its defence.** A sensitivity at 0.13 and 0.16
  is reported alongside the primary.

  **Per-territory repeatability is ~1.5× worse than global**, and this check is per-territory: RC 15 % whole
  myocardium → 23 % regional → 27 % segmental (Lubberink et al., *EHJCI* 2024;25(Suppl 1):jeae142.093 — ¹⁵O-water,
  same-day, n = 10; **conference abstract, small n, "regional" undefined**). Brown et al., *JCMR* 2018;20:48 reports
  both statistics on one dataset — wsCV 11 % stress vs RC 29 % global / 30–37 % regional — and is the cleanest single
  citation for the distinction.

  **Scope correction: the claim is PET-based, not CT.** "CT perfusion" has been dropped — the only human test–retest
  CTP MBF study has its two scans a median 795 days apart and reports neither CV nor RC.

  **Still open:** no full peer-reviewed paper reports per-territory *hyperaemic* repeatability, and no systematic
  review of MBF test–retest repeatability exists; the strongest per-territory source is a conference abstract. The
  Schindler wording was retrieved via a proxy and should be checked against the publisher PDF before it is quoted in
  the manuscript.

  An earlier draft used 1 %; a 6-instance pilot showed that is unreachable with a single free parameter against
  2–3 targets, so it would have made H2 fail for a reason about the tuning parameterisation rather than about
  physiology. Changed on principle, before the ablation was run at scale.
- **"Materially wrong" = |ΔFFR| > 0.05**, an error large enough to matter near the 0.80 cut and five times the
  healthy-reference uncertainty floor (§10).
- **Targets are the CLEAN tree's FULL TERRITORY perfusion** — the total bed outflow of each subtree at the first
  bifurcation **including the share of any branch the segmentation error deleted** (decision B1, 2026-09-19; the code
  previously summed surviving nodes only, which is a target contaminated by the error it validates against). The
  partition is the **clean** tree's territories, which the error cannot move. In 3D, where flows are prescribed per
  outlet, that territory total is distributed across surviving outlets **in proportion to the corrupted tree's Murray
  bed weights** — which is what one global scaling does in 0D, and is therefore the split that makes the two
  fidelities the same procedure. (Splitting in proportion to each outlet's own *clean* flow was specified first and
  is undefined for a T2 stump, whose clean counterpart is an interior node with zero bed weight: it would be written
  as a wall in 3D while the 0D twin gives it a live outlet.) Targets are not per-outlet
  flow: outlet flow is not comparable across bed structures — in the leaky bed most flow leaves through the wall, and
  matching leaf flows alone is ill-posed (pilot residuals of 24.9 and 10.4). Territory flow reduces to the sum of
  outlet flows in the discrete bed and is what CT perfusion / PET MBF actually measures.
- **Protocol C has exactly ONE free parameter** (a global bed scaling) against **≥ 2 territory targets**, so the fit
  is over-determined — the answer to "one equation, one unknown". This is deliberately the *least* flexible tuning a
  pipeline could use: absorption demonstrated under it is a lower bound on what a more freely tuned pipeline achieves.

**Headline number:** the proportion of Protocol C instances that pass the validation check **and** are materially
wrong, with a Wilson interval, reported beside the same proportion for Protocols A and B.
**Note on Protocol A:** it retains the *clean* bed on surviving nodes. It is the reference arm — "what if the
boundary conditions had not been mis-derived" — and is reported as such, never as a naive comparator.

> **Corrected 2026-09-19.** This note previously said Protocol A "passes the perfusion check by construction".
> **That is false under decision B1.** Now that the target is the clean tree's FULL territory outflow including a
> deleted branch's share, Protocol A cannot deliver it through the vessels that remain, so its residual *is* the lost
> perfusion: measured T1/T2 Protocol A residuals run **0.10–0.17**, and in the discrete bed only 12 of 19 A rows pass.
> Protocol A passing is therefore an empirical result per error type, not an identity, and the "passes and is
> materially wrong" proportion must be reported for A on the same footing as B and C.
**Pre-specified sensitivity:** Protocol C repeated with one scaling parameter **per territory** (exactly determined).
Absorption should be stronger; reporting both brackets the effect between the least and most flexible tuning.

**P3 — bed-structure factor (pre-registered, per `CFD-ARM-SPEC` §2.5).** Every P1/P2 analysis is run under **both**
leaky and discrete beds. A claim is made **only where direction and ordering agree in both**; effect sizes are
reported per structure and never pooled. **Bands are re-derived per structure.** Measured on the frozen cohort
(`results/discrete_arm_eligibility.csv`): the discrete arm admits **97/150** instances (48 excluded by the
healthy-network gate, 5 with fewer than 2 outlets); the discrete bed shifts FFR by **−0.051 ± 0.071** and
**disagrees on the 0.80 decision in 19/97**; only **36/97** keep their leaky band, and **19 fall outside 0.65–0.95
altogether**. Carrying bands across structures would therefore mislabel most of the arm. The discrete arm is analysed
on its own 97 instances with its own bands, and is powered for **direction only**, not effect size.
> **WITHDRAWN 2026-09-19.** The example that stood here — "taper under Protocol A: 6 flips leaky vs 43 discrete in
> probe data" — was an **artefact (decision B3), not physiology.** T4 scales radii by 0.930, which dragged `r_ref`
> below the fixed 0.60 mm discrete truncation and deleted leaves the error had merely narrowed. Measured cohort-wide
> (`references/B2B3-EVIDENCE-2026-09-19/`): **489 of 655 discrete outlets (75 %)** fell below the cut, and **56 of
> 148 instances lost every outlet**, i.e. their trees could not be built at all. With the truncation radius scaled to
> match the calibre error, T4 × Protocol A in the discrete bed moves from ΔFFR +0.173 (3 flips) to **−0.032
> (0 flips)** and agrees in direction with the leaky bed (−0.047). **No taper-specific bed interaction is claimed.**
> Whether a genuine `error_type × bed` interaction exists is an open empirical question for the full run.

Structure-dependent results are reported as
**interactions**, with `bed` entered as a fixed effect and an `error_type × bed` term.

**P4 — cross-fidelity replication (H4).** 0D vs 3D on the frozen 3D subset (`CFD-SUBSET-FROZEN-2026-09-18.csv`:
**30 instances, 10 per vessel, one per tree, 29 patients**, stratified across discrete bands). Cohen's κ for decision
agreement (pre-registered threshold κ > 0.6), Bland–Altman for ΔFFR with bias and 95 % limits of agreement, and the
ladder decomposition |0D − polyball| (physics gap) vs |polyball − real lumen| (geometric-reduction gap).
**One instance per tree by design**, so P4 needs no random effect — κ and the limits of agreement are computed on
independent units. The subset is drawn from the discrete-eligible pool **without** requiring the leaky band to hold
(decided 2026-09-18 pre-run, `CFD-ARM-SPEC` §3): the 3D arm replicates the discrete bed, so the leaky band is not a
validity condition for it. With n = 30, κ is estimated to roughly ±0.2 — **adequate for direction, not for a precise
agreement coefficient**, and reported as such.

> **PRE-REGISTERED CONTINGENCY on the 3D discretisation floor (added 2026-09-19, before any 3D result is in hand).**
> §10's discretisation floor (0.005 FFR, revised 2026-09-19) is a **0D** figure. **No 3D equivalent exists yet**, and the Stage A
> validation pass gives positive reason to doubt one can be assumed small: on the idealised 70 %DS case, successive
> mesh refinements moved FFR by +0.004732 then +0.004780 — *not shrinking* through 1.9 M cells — so Richardson
> extrapolation and GCI were both reported as untrustworthy rather than quoted. A production-resolution re-run is in
> progress (`cfd_handover/WORK-ORDER-2026-09-19.md`, Task 1) and will return a measured figure, **U₃D**.
>
> The rule is fixed now, before that number is known:
>
> - **U₃D clearly below the 0.005 mesh-independence tolerance** → H4 proceeds as specified: κ against its
>   pre-registered threshold of 0.6, plus Bland–Altman.
> - **0.005 ≤ U₃D < MATERIAL_DFFR (0.05)** → κ is still reported, with U₃D stated beside it, and **any instance whose
>   3D FFR lies within U₃D of the 0.80 threshold does not contribute to the flip-agreement count** — those are
>   reported separately as indeterminate, because their 3D decision is not resolvable at the achieved resolution.
> - **U₃D ≥ MATERIAL_DFFR (0.05)** → **H4 is reported as NOT ESTIMABLE at the achieved mesh resolution**, in those
>   words. The cross-fidelity comparison is then restricted to ΔFFR **bias and limits of agreement**, which remain
>   interpretable because a bias estimate averages discretisation error down while a per-case decision does not, and
>   **no decision-agreement claim is made in either direction**.
>
> In every branch U₃D is reported as a number and joins §10's uncertainty list beside the 0D floor. **Fixing this
> before the value is known is the entire point:** deciding it afterwards would make any of the three responses a
> post-hoc deviation rather than a pre-specified result.

**P5 — detector (H5).** ROC with DeLong 95 % CI on a held-out split, then on the external dataset. Operating point
pre-specified at sensitivity ≥ 0.80. Reported per error type; failure modes reported explicitly.

## 5. Secondary and stratified analyses (pre-specified)

- **Branch location (Gamage stratifier).** Missed-branch instances split by branch position relative to the lesion
  (upstream / downstream) — defined on the **whole tree**, not the host vessel's own path (a sister vessel at the
  left-main bifurcation is haemodynamically upstream of an LAD lesion). Tests Gamage's "<1/3 main-vessel diameter is
  negligible" rule as a pre-registered hypothesis.
- **Bifurcation lesions.** The 26 `bif_in_window` instances analysed as a stratum, not excluded.
- **Image quality.** Likert 2 / 3 / 4 (n = 22 / 40 / 88) as a covariate; interaction with error type is exploratory.
- **Vessel.** LAD / LCx / RCA (50 each) as a fixed effect.
- **Grey zone.** Flips separated into grey-zone (0.75–0.85) and clear (outside) — clinical practice does not treat
  0.79 and 0.60 alike.

## 6. The physiological-noise floor (pre-specified control)

> **REWRITTEN 2026-09-19. The previous version of this section could not be executed as written and rested on a
> misattributed claim.** Both problems were found by checking the citation
> (`references/CITATION-PHYSIOLOGICAL-SDS-2026-09-19.md`) before the Monte Carlo was run, not after.
>
> **(a) Two of the four SDs do not exist.** Tanade et al. (*Front Med Technol* 2022;4:1034801,
> doi 10.3389/fmedt.2022.1034801) publishes SDs for **cardiac output (relative 0.153) and MAP (relative 0.056)
> only**. Heart rate and haematocrit were *fixed to cohort constants* there, because its own sensitivity analysis
> found they did not matter. A Monte Carlo "over cardiac output, MAP, heart rate and haematocrit at Tanade's
> published SDs" was therefore not a thing that could be done.
>
> **(b) The 50 % / 25 % figure is quoted correctly and attributed wrongly, and the error runs in the dangerous
> direction.** That reclassification rate comes from re-sampling cardiac output **together with stenosis degree**
> (SD 16.9 percentage points, itself parameterised from blinded inter-observer disagreement) — with MAP held fixed.
> **Stenosis degree is an anatomical error: it is the very quantity this study injects.** Tanade further attributes
> the RCA excess mainly to the stenosis-degree term. Using 50 %/25 % as a *physiological* floor would therefore
> inflate the floor with the effect the floor exists to exclude, and would understate our own result against it.
>
> **(c) The SDs must be within-subject, not population or inter-instrument.** A floor draw represents *the same
> patient measured again*, not a different patient. Tanade's cardiac-output CoV traces to a 1990
> Doppler-vs-thermodilution method comparison — instrument disagreement. The distinction is a factor of ~5.7:
> population CV of cardiac index ≈ 30.9 % against a within-subject 5.44 %.

**The floor has two components, and the first is now the primary.**

**6a — Direct repeat-FFR variability (primary).** The best available floor is not propagated through a model at all:
it is measured on the endpoint we report. **Johnson et al. 2015** (190 repeated FFR pairs) gives a repeat-FFR
**SD of 0.018** despite genuine variation in aortic pressure and heart rate between the measurements. **Petraco
et al. 2013** (DEFER, repeat FFR ~10 minutes apart) gives the classification certainty directly on our own axes:
**> 95 % outside FFR 0.75–0.85, < 80 % within 0.77–0.83, and a nadir of ~50 % at 0.80 itself.** These are reported
on the same P(flip | band) axes as every result, and they are a stronger comparator than any simulation because they
include every source of variation we do not model, heart rate among them.

**6b — Simulated physiological floor (supporting).** A no-injection Monte Carlo on the **clean** anatomy, perturbing
**cardiac output (within-subject SD 0.05), MAP (relative 0.056) and haematocrit → viscosity (relative 0.02)**, with
per-territory demand-share noise and target measurement noise at the per-territory hyperaemic within-subject CoV
(0.083). Implemented in `code/negatives.py`; sources for each constant in its header. **Heart rate is not
represented** — no SD exists to use and this is a steady model — and that is stated as a limitation rather than
omitted silently. 6b doubles as the detector's negative class (`DETECTOR-SPEC` §5), so the same draws serve both.

**How it is used.** **No injected-error flip rate is reported without the floor beside it.** An injected-error
effect that does not exceed it is reported as **not distinguishable from physiological noise**, in those words.
Where 6a and 6b disagree, 6a governs and the discrepancy is reported.

**Already measured on the smoke set, and it matters:** with correct anatomy, tuning to a noisy measurement still
moves FFR by a median **|ΔFFR| ≈ 0.022** — against `MATERIAL_DFFR` = 0.05. The floor is not negligible relative to
the effect, and it bounds what any detector can achieve.

## 7. Multiplicity

Holm–Bonferroni across the six pre-registered hypotheses H1–H6 (family-wise α = 0.05). Within a hypothesis, the
protocol contrasts (B−A, C−A, C−B) are three planned comparisons, Holm-corrected within family. Stratified and
secondary analyses are **not** included in the correction and are labelled exploratory wherever reported.

## 8. Power

No formal power calculation; N is set by cohort supply, and the design is paired, so the relevant quantity is the
detectable paired difference. With 150 instances and a patient-level random effect (93 patients, ICC assumed ≤ 0.3,
design effect ≈ 1.2), a paired difference in flip probability of ~12 percentage points is detectable at 80 % power,
α = 0.05. This is stated as a sensitivity, not a guarantee. The discrete arm is smaller (**97 eligible; 36 if the band
must hold under both structures**) and is powered only for direction, not for precise effect sizes — stated as such.

## 9. Missing data, exclusions, failures

- Exclusions are **rule-based and logged with reasons**: discrete-arm healthy-network gate (FFR ≥ 0.90), ≥ 2 outlets
  for missed-branch/truncation, calibration infeasibility, and the two Protocol C rules below. Counts reported in a
  CONSORT-style flow diagram from 6,944 swept instances → 150 selected → per-arm eligible.

> **CORRECTED AND EXPANDED 2026-09-19 — this is the largest exclusion in the study and it was previously
> mis-stated.** The rule for Protocol C is **not** "≥ 2 outlets". It is:
>
> **(i) ≥ 2 clean-partition territories with surviving members.** Protocol C fits ONE global bed scaling against the
> territory targets, so it needs at least two of them to stay over-determined (the Fossan constraint in §P2). A
> territory whose vessels the error removed entirely has no surviving member and cannot be matched, so it drops out.
> **(ii) The fit must not land on a search bound** — a Protocol C optimum at the edge of the ±1.5-decade search is a
> **failed fit**, logged as such and excluded, never reported as a result (`fit_at_bound`; see also the bimodal-loss
> note in `DETECTOR-SPEC` §9).
>
> **Consequence, measured cohort-wide, and it is not small:** Protocol C is lost on **47 of 118 T1 rows (40 %)** and
> **49 of 149 T2 rows (33 %)**, and the losses are **overwhelmingly RCA** — 99 of 100 T2 × RCA rows have zero
> surviving territories, so **T2 × RCA has no Protocol C cell at all**, and for those rows no protocol has a defined
> perfusion residual. In the frozen 3D subset, T1 × C exists on 19 of 30 instances.
>
> **This must be carried into §P1 and §P2's vessel stratification, which knows these cells are empty in advance.**
> The right-dominant anatomy of this cohort concentrates single-outlet trees in the RCA; the honest statement is that
> **the tuned-protocol arm is a left-coronary result for the topological error types**, and the paper says so rather
> than presenting a vessel stratification with silently missing cells.
- **Non-converged solves are failures, not missing data**: reported, never silently dropped. Current rate 0/6,944.
- **3D meshing and solve failures are a reported outcome by error type**, not an exclusion — no published base rate
  exists for deliberately corrupted coronary geometries.

## 10. Uncertainty floors to state alongside every result

- **Solver discretisation, 0D: ≤ 0.005 FFR** (verification V8a). **Revised upward from 0.003 on 2026-09-19, before
  lodging.** The 0.003 figure came from **two** scans. Re-running V1–V10 on **18 scans across both beds** — 149 and
  143 refinement slots rather than 16 — gives a maximum |ΔFFR| of **0.0045 (leaky) and 0.0048 (discrete)**, which
  exceeds the floor as previously declared. All 26 checks still pass; it is the *floor* that was too tight, not the
  solver that failed. V8b (healthy reference re-fitted) is 0.0040 / 0.0052 against its declared 0.010 and stands.
  **The binding statement below is unaffected** — no FFR difference under 0.01 is interpreted as meaningful — but a
  floor quoted from two scans and exceeded by eighteen would have been found by a referee, not by us.
- **Mesh discretisation, 3D — U₃D, TO BE MEASURED, not assumed.** There is no 3D counterpart to the line above, and
  Stage A gives reason not to assume one is small: on the idealised 70 %DS case successive refinements moved FFR by
  +0.0047 twice over, through 1.9 M cells, without shrinking. A production-resolution re-run will return the figure
  (`cfd_handover/WORK-ORDER-2026-09-19.md`, Task 1). **U₃D is reported as a number whatever it turns out to be**, and
  §P4's pre-registered contingency fixes in advance what happens to H4 at each magnitude.
- **Healthy-reference re-fit:** ≤ 0.010 FFR (V8b) — larger than the solver floor, and larger in the discrete bed.
  **No FFR difference below 0.01 is interpreted as meaningful** unless it is a paired within-instance contrast at
  fixed discretisation, where this error cancels to first order.
- **Demand-model sensitivity:** flow scaled ×0.7 / ×1.0 / ×1.3 on the selected instances; reported alongside.
- **Healthy-equivalent calibration:** the healthy solve uses `r_ref`, which is narrower than the actual radius where
  the taper fit rises, so inflow can exceed demand by up to +2.9 % (max 1.0288). **11 of 1,920 E0 rows exceed +1 %**
  and 57 exceed 0 — the 11 is a count above a **1 % threshold**, stated here because the threshold was previously
  left implicit. Reported as a ±3 % band.

## 11. Software, reproducibility, and what is frozen

Analysis in Python (numpy / scipy / pandas / statsmodels), environment pinned in `requirements.txt`. Code deposited
with a DOI; the protocol and cohort hashed (§ header). **The cohort is the hashed instance list, never "seed
20260918"** — `select()` is chaotic: a 16-band perturbation of the sweep produced a cohort sharing only 62/150
instances with the original. Every figure regenerable from the deposited code and the frozen cohort.

## 12. Deviations

Any deviation from this plan is reported in a "Deviations from the pre-registered analysis plan" subsection, with
the reason and the pre-registered alternative, whether or not it changes a conclusion.

## 13. Planned amendment — the paired-anatomy arm (re-specified 2026-09-19, BEFORE registration)

**This version registers the injection design only.**

> **RE-SPECIFIED 2026-09-19. The previous version of this section is void and must not be lodged.** It planned an
> arm built on the 160 paired human re-annotations behind ImageCAS-X's inter-observer statistics. **Those were
> requested and formally declined** (Gate D1b): the dataset lead will not release the second annotation set, because
> it was deliberately left unchecked so that inter-observer variability would not be under-estimated, and releasing
> it risks users treating it as a second ground truth. That is a considered position and will not change.
>
> The same reply offered something else — **model predictions (CAS-Net / nnU-Net) against the official labels** —
> which is now Gate D1c (accepted 2026-09-19). This section is re-specified around that offer. **Three things change
> substantively, and each is declared rather than carried over silently.**

**Change 1 — the estimand is different, and the paper must never blur the two.** Model-vs-reference is a **model
error** regime, not inter-observer variability: published Betti error ≈ 1.9 (CAS-Net) and 5.6 (nnU-Net) against 0.2
between annotators, i.e. ten to forty times more topologically wrong. It is also a **pre-QA** input — regulated
FFR-CT has an analyst edit the segmentation before flow computation — and the reference itself is a checked
annotation, not ground truth. All three qualifications are stated wherever this arm is reported.

**Change 2 — "no synthetic insertion at all" is withdrawn; the same virtual stenoses are inserted into BOTH
anatomies.** The old text specified a no-injection arm. That is not viable and the reason is in our own E0: the
natural cohort has **2 trees ≤ 0.80 and 4 in 0.75–0.85**, which is precisely why the severity sweep exists. A
no-injection arm would have an essentially empty flip table, and H7's endpoint would be undefined. Instead:

- the **same lesion** — same vessel, same location, same length, same %DS — is inserted into the official
  segmentation's tree **and** into the model prediction's tree;
- the contrast is then **reference anatomy vs predicted anatomy carrying an identical lesion**, so the difference
  between them is real segmentation error and nothing else, while the lesion supplies decision-relevant density.

The alternative considered and rejected was to keep the arm injection-free and report ΔFFR only. It was rejected
because it would make H7 the single hypothesis in the family without a decision endpoint, which is both inconsistent
with H1–H6 and a weaker claim.

**Change 3 — the arm needs its own eligibility rule, because a prediction may not have the vessel.**
An instance enters this arm only if the slot is eligible on **both** trees under `severity_sweep.plan()`: host vessel
present and labelled, `r_fit ≥ 1.0 mm` at the lesion centre, ≥ 20 mm of run-off, measurement node resolved, native
stenosis < 40 %DS, baseline FFR ≥ 0.90. Instances eligible on the reference but not on the prediction are **not
discarded silently** — they are counted and reported as their own quantity, because *"the automatic segmentation lost
the vessel entirely"* is itself a result about deployment, and a more severe one than any ΔFFR.

### The amendment, as it will be registered

- **Unit:** one scan with two anatomies (official reference, model prediction) carrying the same inserted lesion;
  paired within scan; patient-level random effect as in §2.
- **Endpoint:** identical to §1 — ΔFFR and the 0.80 flip, each judged against **that anatomy's own clean baseline**,
  under both bed structures, under protocols A/B/C.
- **Hypothesis (new, H7):** anatomy from an automatic segmentation produces decision flips at a rate at least as high
  as the injected topological error types (T1, T2) at their registered magnitudes. Registered in **both** directions,
  as H1–H6 are. *(Note the comparator has changed: the old text said "injected errors of the magnitude measured in
  the same data", which is no longer true of anything — T1 and T2 have no measured magnitude, and the DSC/HD95
  figures are floors, not matched magnitudes.)*
- **Secondary, and the reason this arm is worth having:** the **apportionment** of error across the four types —
  which branches go missing and at what calibre, how often vessels break, how radius bias varies with diameter.
  This is what §3's declared weakness is about, and it is measurable from the predictions **whether or not H7 itself
  is testable**.
- **Training overlap is not a concern for this cohort, and that is checkable rather than asserted.** All 93 cohort
  patients lie in ImageCAS-X's own `test.txt` (160 scans); none are in the 560-scan training split. Any benchmark
  model's predictions on them are out-of-sample.
- **The post-processing filter is known from the authors' code, not from correspondence:** components below
  **100 voxels** are discarded (`postprocessing/steps.py`, `min_size = 100`) — not largest-component-only.
- **Raw and filtered predictions are analysed separately** if both are supplied. The published benchmark removed
  connected components below ~100 voxels; that filter deletes precisely the small fragments and breaks this arm
  counts, so the filtered set is expected to understate topological error and is reported as a lower bound.
- **Multiplicity:** H7 joins the Holm family, raising it from six hypotheses to seven; the correction is recomputed.
- **Status in the paper:** reported as a **registered amendment with its date**, never merged silently into the
  primary analysis. If the predictions never arrive, the injection design stands alone and §3's limitation — error
  *magnitudes* partly measured, error-*type* apportionment assumed — is the paper's stated weakness.

**Amendments are additive only.** No amendment may alter §1–§11 for the injection design; those are locked at
registration.
