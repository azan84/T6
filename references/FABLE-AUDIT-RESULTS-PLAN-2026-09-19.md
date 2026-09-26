# Independent audit — 0D results to date and `protocol/NEXT-PLAN-2026-09-19.md`

**Date:** 2026-09-19. **Scope:** Part A, every file in `results/` that a decision has been built on, checked against
what the protocol documents say about it; Part B, the new plan written after the ImageCAS-X lead author's reply.
**Out of scope** (audited concurrently by another agent): `CFD-ARM-SPEC` as a CFD document, `cfd_handover/`, Stage A.
`CFD-ARM-SPEC` §3 and §10 were read only as sources of numbers cross-quoted by the 0D documents.
**Nothing in the project was modified.** Probe scripts and their verbatim outputs are in
`references/FABLE-AUDIT-RESULTS-PLAN-2026-09-19-probe/`. The ImageCAS-X paper (arXiv 2608.30404), which is not in
the corpus, was fetched and read to verify the statistics the design rests on.

---

## Verdict: GO-WITH-CHANGES

The numbers in `results/` are sound: every count the documents build a decision on reproduces from the CSVs, the
frozen-cohort hash matches, and the cohort is exactly what `STUDY-PLAN-v2` and `STATISTICS-PLAN` §2 claim. What does
not hold up is the **prose around the numbers** — stale duplicates of superseded counts in three documents, a
statistics-plan section that describes an error model the code does not implement, and a smoke-test claim that
cannot be verified from anything on disk. None of this is fatal; all of it must be fixed before the registration is
lodged, because two of the affected documents are registration attachments.

The new plan gets the **direction** of the lower-bound argument right for the agreement statistics themselves, and
then over-extends it to "every injected magnitude is conservative", which is true of none of the four magnitudes as
actually coded. The C1 topological claim does have to be withdrawn — but for a reason the plan has not seen, which
also invalidates its proposed replacement wording. The CAS-Net/nnU-Net offer is worth accepting and is oversold in
one way that matters: a model-vs-official arm with "no injection" runs into the same wall E0 already hit.

**MUST before registration:** M1–M9 (§C). **SHOULD:** S1–S6.

---

## Part A — the results

### A1. `E0_prevalence_test.csv` + `E0-PREVALENCE-NOTE.md`

| claim | where | data (`E0_prevalence_test.csv`, current) | status |
|---|---|---|---|
| Murray ×1.0: trees in 0.70–0.90 | E0-NOTE headline | **20** | ✓ |
| flip-prone 0.75–0.85 / ≤ 0.80 | E0-NOTE | 4 / 2 | ✓ |
| territory ×1.0 in 0.70–0.90 | E0-NOTE table | **140** | ✓ table; ✗ text (below) |
| **"22 trees … vs 141"** | `STUDY-PLAN-v2` §6 E0 row; E0-NOTE §"Second finding" ("22 to 141"); **this audit's own brief** | 22 / 141 are the **pre-fix** counts — they reproduce exactly from `E0_prevalence_test_PRE-LESIONRULE.csv` and `_PRE-V9FIX.csv`, not from the current file | **STALE** |
| 320 trees / 160 scans / 73 disease-labelled / 0 failures | E0-NOTE | 320 / 160 / 73 / all converged | ✓ |
| tightest lesion: 175 trees ≥ 30 %DS; median 38, p90 50, max 62; 108/50/15/2/0 | E0-NOTE | 175; 37.9 / 49.8 / 62.2; 108/50/15/2/0 | ✓ |
| 247/320 trees with ≥ 1 lesion | E0-NOTE | 247 | ✓ |
| inlet radius median 1.39 (IQR 1.16–1.64) | E0-NOTE | 1.39 (1.16–1.64) | ✓ |
| disease yes/no median 0.944 / 0.951 | E0-NOTE | 0.944 / 0.951 | ✓ |
| inflow exceeds demand "up to +2.9 % (11/1,920 rows)" | `STATISTICS-PLAN` §10 | max 1.0288; 11 rows exceed **1.01**, 57 exceed 1.00 | ✓ with an undeclared 1 % threshold — say ">1 %" |

The E0 verdict (sweep required) is unaffected: 20 or 22, both are far below 40. But the 22 / 141 pair now appears in
a registration-adjacent document (`STUDY-PLAN-v2` §6) and in the note's own second-finding paragraph while the same
note's headline says 20. The sevenfold ratio (140/20) is still correct.

### A2. Frozen cohort vs `sweep_test*.csv` vs `.sha256`

- **Hash:** `COHORT-FROZEN-2026-09-18.csv` = `b8fe7909…` ✓; `CFD-SUBSET-FROZEN` = `8e0079a0…` ✓; `results/sweep_test.csv`
  = `5f4bcce4…` ✓; `results/E0_prevalence_test.csv` = `5aef8115…` ✓. Code: **`code/ablation.py` no longer matches the
  manifest** (`abe239d6…` → `b53ed254…`; the 2026-09-19 minimiser fix). Expected and documented in the manifest's own
  note, but `PREREGISTRATION-CHECKLIST` §1 says "hashes already in the manifest" — the manifest must be re-issued at
  registration (M6). All other code hashes match.
- **Cohort = `sweep_test_selected.csv`** on the (scan, side, vessel, loc, L, %DS) key: 150/150 both ways, FFR
  identical ✓.
- **Composition** (all ✓ against `STUDY-PLAN-v2` §6 log and `STATISTICS-PLAN` §2–3): 150 instances; 25 per band × 6;
  LAD 50 / LCx 50 / RCA 50 (8–9 per band per vessel); 108 trees; 93 patients; 134 distinct slots, 16 with two
  severities; 15 patients contribute both sides; 46 / 38 / 9 patients with 1 / 2 / ≥ 3 instances, max 4; length 10 mm
  80 / 20 mm 70; `bif_in_window` 26; Likert 2/3/4 = 22/40/88; every FFR in [0.65, 0.95). The **severity × band table
  in `STATISTICS-PLAN` §3 reproduces cell-for-cell.**
- **`SEVERITY-SWEEP-SPEC.md` §8d describes the PRE-LESION-RULE cohort, not the frozen one** — "LAD 48 · LCx 51 ·
  RCA 51; 107 trees, 85 scans; length 76/74; quality 16/39/95; disease 95/55; dominance 128/8/14; proximal 99 / mid 51;
  upstream stratum 38 of 150". Frozen cohort: 50/50/50; 108 trees; 93 patients; 80/70; 22/40/88; **89/61**;
  **R 125 / L 8 / Co 17**; **prox 104 / mid 46**; **upstream 37**. The sweep-level numbers in the same section (6,944
  instances, 280 hosts, medians by severity, rejection counts) *do* match the regenerated run. This document is listed
  in `PREREGISTRATION-CHECKLIST` §1 as the "Design and manipulations" attachment (M2).

### A3. `discrete_arm_eligibility.csv` vs `CFD-ARM-SPEC` §3 and `STATISTICS-PLAN` §P3/§8

| claim | data | status |
|---|---|---|
| 97/150 eligible; 48 fail healthy gate (E3); 5 with < 2 outlets (E4) | 97; 48; 5 (no other reason codes occur) | ✓ |
| discrete shift −0.051 ± 0.071 (min −0.317, max +0.057) | mean −0.0507, SD 0.0707 (ddof 1), min −0.3166, max +0.0567 | ✓ |
| 19/97 disagree on the 0.80 decision | 19 (same for ≤ and <) | ✓ |
| 36/97 keep their leaky band | 36 (by band index; label strings differ, "[0.8, 0.85)" vs "[0.80, 0.85)", which is why `discrete_arm.py` compares by index) | ✓ |
| 19 fall outside 0.65–0.95 | 19 | ✓ |
| 77 with a deletable downstream branch | 77 | ✓ |
| pool eligible ∧ deletable ∧ band holds = 33 (RCA 22, LCx 6, LAD 5) | 33 (22/6/5) | ✓ |
| "12 of the pool" outside 0.65–0.95 after dropping the band rule | 77 − 65 = 12 | ✓ |
| 3D subset: 30, 10 per vessel, one per tree, 29 patients; bands 5/4/4/7/5/5; lengths 10 mm × 20 / 20 mm × 10; all eligible and deletable; all in the cohort | all ✓ | ✓ |
| **`STATISTICS-PLAN` §8: "97 eligible; 38 if the band must hold"** | **36** | **✗** — contradicts §P3 of the same document (36) and the data |
| `DETECTOR-SPEC` §3.3 "n_territories = 2 in 99/103 (discrete)" | 108 trees build under discrete; 69 trees carry eligible instances | unverifiable from any file on disk (reviewer probe); not load-bearing |

### A4. `ablation_smoke.csv` — what may still be quoted

Facts: 124 rows, 6 instances (all **left LAD**, five at 80 %DS and one at 70 %DS — i.e. essentially one band), 113 ok,
11 skipped (10 "no deletable downstream branch" — only **one** of six instances has a T1 candidate — and 1 "fewer than 2
shared territories"). Protocol C: 38 rows, 37 solved. No `fit_n_basins` column: **this is the pre-fix file.**

**The post-fix re-run is not on disk.** No CSV anywhere in the project or the session scratchpad carries the new
fit-diagnostic columns. "Smoke re-run: 0 of 38 Protocol C rows changed, no multi-basin fits, no bound hits" appears in
`STUDY-PLAN-v2` (banner), `CFD-ARM-SPEC` §10 and `DETECTOR-SPEC` §0/§9 as *done* — but the only evidence is the
sentence itself. Until the re-run's CSV is written to `results/` (M4), every Protocol C number below is
"pre-fix, unconfirmed".

**Independently of the fix, every T2 row in the smoke is a stump measurement.** `meas_same_point` is `False` in
36/36 T2 rows, which is B2 (`T2_KEEP_BEYOND` 15 mm < `RUNOFF` 20 mm) observed in the data, not just in the code. Any
T2 ΔFFR or flip from this file (e.g. mean |ΔFFR| 0.37 / 4 flips under A-discrete, 0.21 / 5 flips under A-leaky) measures
a closed-outlet wall under Protocol A and must not be quoted for anything.

| number quoted from (or attributed to) the smoke | where | in the file? | ruling |
|---|---|---|---|
| scan 335 / discrete / T2, C_ratio 10.1, residual 0.62, "genuine, fails the 10 % check" | `CFD-ARM-SPEC` §10 | yes: C_ratio 10.106, residual 0.621 | safe as a structural fact; but it is a **T2 stump row**, so "genuine" means only "unimodal" |
| **C_ratio 9.3 and 33.3, "the last exactly at the search bound"** | `ablation.py` lines 174–176 (as "the pre-fix smoke run's C_ratio values"), `DETECTOR-SPEC` §9 ("the smoke test's C_ratio values") | **no** — max C_ratio in the file is 10.1; the values come from the reviewer's own probe (`FABLE-REVIEW-DETECTOR` line 45, "in the probe") | misattributed; and both places still call 10.1 "the same pathology", which `CFD-ARM-SPEC` §10 says is falsified. Three documents, three stories (M5) |
| "residuals of 24.9 and 10.4" (leaf-flow matching ill-posed) | `STATISTICS-PLAN` §P2, `ablation.py` docstring | no (earlier leaf-flow smoke, not retained) | design rationale only; label it "pilot, not retained" |
| 6-instance pilot showed 1 % residual unreachable | `STATISTICS-PLAN` §P2 | consistent: 37 C rows, median residual 0.03–0.04, only 5 below 0.01 | safe |
| 3 of 37 C rows "pass and materially wrong" (306 T1 both beds; 335 leaky T2) | not quoted anywhere | yes | **do not quote**: pre-fix, and one is a stump row |
| T3 |ΔFFR| ≈ 0.013–0.017, no flips, in both beds | not quoted | yes | safe as an order of magnitude — T3 is untouched by the fix and by B2 |

Nothing quantitative from the smoke has yet been written into a claim, which is the right state. Keep it so.

### A5. Drift between the documents and the code (the part that matters for registration)

1. **The error model the documents describe is not the one in `error_types.py`.** `STUDY-PLAN-v2` §E1 says T1's
   magnitude source is "Betti error 0.2 ± 0.4 per tree → topological event rate" and that magnitudes are
   "**quality-matched (operationalised)**: conditioned on Likert, vessel diameter, attenuation, disease status"; §9
   attack 3 repeats "quality-matched via the dataset's own stratifiers". The code has **no rate and no conditioning**:
   T1 deletes the **largest** eligible downstream branch in every instance (100 % event rate, `max(cand)` on radius);
   T2 truncates at a fixed 15 mm; T3 adds a fixed 2.46 mm; T4 scales by a fixed 0.930. This is a C1 contribution
   claim that the experiment as coded cannot support (M1). `NEXT-PLAN` §3b proposes to edit only the header of
   `error_types.py`; the header's *content* ("MAGNITUDES are derived from measured inter-observer disagreement … not
   chosen") is already false for T1 and T2, which have no measured magnitude behind them at all.
2. **`STUDY-PLAN-v2` §5 contradicts `STATISTICS-PLAN`** on unit (case × lesion vs instance), random effect
   (`(1 | case)` vs `(1 | scan/slot)` at patient level), N ("100–160 trees" vs 150 instances / 93 patients) and
   detectable difference (10 vs 12 points). §5 should be a one-line pointer to `STATISTICS-PLAN` (M3).
3. **`STUDY-PLAN-v2` §E2** body still specifies Protocol C as matching "flows *and* pressures" with a banner saying
   that is wrong; the registration source of truth is `CFD-ARM-SPEC` §2.3 / `ablation.py`. Acceptable only if the
   registration cites those, not §E2.
4. `STATISTICS-PLAN` §8 "38" vs §P3 "36" (A3).
5. `SEVERITY-SWEEP-SPEC` §8d pre-fix cohort descriptors (A2).
6. `STUDY-PLAN-v2` §6 E0 row and E0-NOTE second-finding paragraph: 22 / 141 (A1).
7. **B1 and B2 remain open** and both are visible in the data: B2 in the smoke (A4); B1 in `ablation.py` lines
   129–136, which still target the clean flow of the *surviving* nodes only, against `STATISTICS-PLAN` §P2's "total
   bed outflow of each subtree". `NEXT-PLAN` §3c correctly lists both as the true blockers.
8. `ablation.py` hash drift vs the manifest (A2).

---

## Part B — the new plan

### B0. What the reply actually establishes (verified against arXiv 2608.30404)

- The second annotator on the 160 test scans was **"blinded to the first set of labels"** and worked **"without review
  from the lead analyst"**, "following the same protocol". So "blind" is *true in the paper's own words*; what is
  not true is "independent": both started from the same automatic centrelines and the same 3D U-Net lumen
  initialisation. `NEXT-PLAN` §3b's instruction to "drop 'blind'" is an over-correction that deletes a true
  statement; replace with "blind to the other's labels, but sharing an automatic initialisation" (S1).
- The reference set was **checked and corrected by the lead analyst; the second set was deliberately not** — Bransby
  says this was intentional "to get a better estimate of the inter-observer variability", i.e. to avoid
  *under*-estimating disagreement. **The published pair therefore carries two opposing biases that the authors
  themselves name:** shared initialisation (pushes agreement up) and checked-vs-unchecked asymmetry (pushes
  disagreement up, and folds QA correction into "inter-observer"). `NEXT-PLAN` uses only the first.
- **Betti error in ImageCAS-X is β0 + β1 (connected components + loops), computed volumetrically per scan.** A missed
  side branch — a branch that is simply absent from one mask while the rest of the tree stays connected — changes
  **neither** Betti number. The 0.2 ± 0.4 counts breaks, islands and touching-vessel loops. It has never measured the
  T1 event, which is the paper's main effect.
- Benchmark models in the paper were trained on the **560 ImageCAS-X training scans** and evaluated on the same 160 test
  scans (80 validation); post-processing was "threshold at 0.5, then removal of connected components smaller than
  100 voxels" — **not** largest-component filtering. Model Betti errors: CAS-Net 1.9 ± 1.5, ADE-HTL 1.5 ± 1.5,
  nnU-Net 5.6 ± 3.5, nnU-Net+clDice 8.0 ± 4.4 — against 0.2 ± 0.4 inter-observer.
- All statistics the design quotes (DSC 92.8 ± 3.1, clDice 95.4 ± 3.6, HD95 2.46 ± 3.62, ASSD 0.53 ± 0.33, Betti
  0.2 ± 0.4, per-segment 70.9–95.3 %, side-branch 70.9–83.6 %, ρ = +0.89 / +0.90 / −0.36) **verify against the paper.**

### B1. The lower-bound argument, magnitude by magnitude

The plan's syllogism — DSC is an upper bound on agreement ⇒ measured disagreement is a lower bound on real
disagreement ⇒ every injected magnitude is conservative — is valid **only for the first arrow**, and only for the
overlap/topology metrics as metrics. It fails at the second arrow because each injected magnitude is reached from
its source statistic through a *conversion* that has its own direction of bias, and two of the four have no source
statistic at all.

| magnitude | source | does shared initialisation bias the source toward agreement? | does the conversion preserve "floor"? | net |
|---|---|---|---|---|
| **T4** `0.930` | DSC 92.8 % via DSC = 2k²/(k²+1) (algebra checked: k = 0.9304 ✓) | yes — unedited boundaries are identical | **no.** The formula attributes the *entire* DSC deficit to a coaxial, uniform calibre difference. The real deficit also contains side-branch disagreement (side-branch DSC 70.9–83.6 %) and zero-mean boundary jitter, neither of which is a calibre bias. So 7 % is an **upper** bound on the systematic-calibre share of a DSC of 92.8, while 92.8 is an upper bound on agreement. Opposite directions; net unknown. The checked-vs-unchecked asymmetry adds a third, upward bias | **not a floor** |
| **T3** `2.46 mm` | HD95 (lumen) | yes | **not applicable.** HD95 is the 95th-percentile surface distance over the whole tree; it is dominated by the largest discrepancies, which are topological (branch tips, break ends). With independent centrelines HD95 would rise *for topological reasons* — saying nothing about lesion-extent error, which ImageCAS-X never measures. The T3 link is by analogy; a bound on HD95 does not transfer | **no direction can be claimed** |
| **T2** `15 mm` | "vessel breaks present in all predictions" + ρ = −0.36 | — | **there is no measured inter-observer magnitude here.** The break statement is about *model* predictions; ρ is a correlation, not a length. 15 mm is a chosen constant (and it deletes the measurement node — B2) | "conservative" is empty |
| **T1** (no magnitude) | "Betti 0.2 ± 0.4 → event rate" | yes for Betti as a metric | **no rate is used**; every instance loses its **largest** eligible branch. ImageCAS-X's own stratifier (DSC vs diameter ρ = +0.89) says real disagreement concentrates in the *smallest* branches — the code injects the opposite tail. Defensible as Gamage's worst case; not as a "floor" | "conservative" is the wrong word; "worst-case downstream branch" is the right one |
| **Betti 0.2 ± 0.4** (C1 wording only) | inter-observer β0+β1 | plausibly yes (both inherit the same auto-centreline breaks; disagreement is differential editing) — but the unchecked second set also inflates it, and from-scratch human annotation rarely produces islands or loops at all, so fully independent annotation could plausibly score *lower* on β0+β1 | — | "certainly higher" (`NEXT-PLAN` §2) is unsupported; "unknown, plausibly higher" is supportable |

**Ruling.** The direction is right for the statistics and wrong as a statement about the magnitudes. The paper may
say: *"the dataset's authors state that the published agreement statistics are an upper bound of agreement; the
magnitudes we inject are derived from them under stated simplifying conversions, and we do not claim they bound the
true error in either direction."* It may not say "every injected magnitude is conservative" (M7). The offensive
rewrite of attack 3 proposed in `NEXT-PLAN` §3b should be toned to this.

A second-order consequence the plan does not raise: H1 is registered "at matched disagreement magnitude". If the
magnitudes are floors by *different unknown amounts per type*, "matched" is no longer a premise the design can
defend, and H1's wording should say "at the magnitudes derived in §E1" rather than "matched" (S2).

### B2. The C1 withdrawal

**Right conclusion, wrong reason, and the replacement wording is still wrong.**

- `NEXT-PLAN` withdraws "measured topological disagreement rate (Betti 0.2 ± 0.4)" because the shared centreline
  "largely determines topology". That is overstated: what was shared was the *automatic* centreline **before**
  editing, and each annotator then trimmed, removed and drew vessels separately (protocol verified in the paper).
  Topology was not inherited; the starting point was.
- The decisive reason is B0: **β0+β1 does not count missed branches.** C1 as written cites a component/loop statistic
  as if it were a missed-branch rate. That was never supportable, with or without the reply. It also means the
  plan's proposed replacement — "a floor on the topological disagreement rate, measured under shared-centreline
  initialisation" — still describes 0.2 ± 0.4 as a rate for the wrong event.
- **Defensible replacement (M8):** *"ImageCAS-X reports inter-observer Betti error (β0 + β1) of 0.2 ± 0.4 per scan
  under a shared automatic initialisation, which bounds break/island/loop disagreement from below; missed-branch
  disagreement is not captured by any published topological statistic and is evidenced instead by side-branch DSC of
  70.9–83.6 % and centreline HD95 of 4.58 ± 5.75 mm. The error model therefore injects fixed, pre-specified
  operations whose magnitudes are anchored to these statistics, and their apportionment across error types is
  assumed."* The last clause is already the paper's declared weakness in `STATISTICS-PLAN` §13; C1 must say the same
  thing, not the opposite.

### B3. The CAS-Net / nnU-Net offer

**Accept it. The plan is right that it is worth more than the paired masks — but not for the reason it gives, and it
oversells in four places.**

1. **"A genuine topological disagreement rate — the number C1 needs."** No. Model-vs-official yields a *model error*
   rate: CAS-Net β-err 1.9, nnU-Net 5.6, against inter-observer 0.2 — a regime ten to forty times more topologically
   wrong. It is a different estimand, and the paper must never present it as inter-observer variability (the plan
   half-acknowledges this in §5 Q3 but §2 still calls it "the number C1 needs").
2. **"A/B/C on model-predicted vs official anatomy, no injection."** This contradicts E0. The natural test cohort has
   **2 trees ≤ 0.80 and 4 in 0.75–0.85** under the primary demand model — that is why the severity sweep exists. A
   no-injection model-vs-official arm has essentially no decision-relevant instances; H7's flip endpoint would be
   empty. Either (a) the same virtual stenoses are inserted into *both* anatomies (real topological/calibre error +
   controlled severity — a good design, but a new one, and it needs its own eligibility rules on the model-predicted
   tree), or (b) the endpoint is ΔFFR only. The plan must choose and register the choice; "no injection" cannot stand
   (M9).
3. **Deployment framing.** "An FFR-CT pipeline is fed an automatic segmentation, not a human one" is not how
   regulated FFR-CT is deployed — the segmentation is analyst-edited before flow computation. Raw model output is the
   *pre-QA* input. The arm answers "what does unedited automatic segmentation error do to the decision" — a fair and
   interesting question, but the sentence in the paper must say pre-QA.
4. **"The reference is truth."** Model-vs-official differences include the official mask's own error (it is a checked
   annotation, not ground truth). State it.

Two of the plan's concerns are partly resolved by the paper and its four questions should be adjusted:

- **Post-processing (Q3):** the benchmark applied threshold + removal of components < 100 voxels, not LCC filtering.
  Breaks survive; small islands do not. Ask for **raw probability maps or raw binarised output** *and* the
  post-processed version, so the paper can report both. The question as drafted ("largest-connected-component") will
  get the answer "no" and miss the 100-voxel filter.
- **Training overlap (add as Q5):** the paper's benchmark models were trained on the 560 ImageCAS-X training scans;
  the 160 are held out. That resolves the "may have seen these scans" concern **only if** the predictions come from
  those benchmark runs. CAS-Net has a prior public version trained on original ImageCAS labels with a different split.
  Ask explicitly for the run/weights used in Table 2.
- **Q4** (asking Bransby to confirm the caveat applies to topology) should be dropped or reworded: the audit above
  shows the topological statistic does not measure the event in question; his confirmation would not repair that.

What the offer *is* good for, and the plan undersells: it gives, for 160 scans × several models, a **measured
apportionment of error across the four types** (which branches go missing, how often vessels break, calibre bias by
diameter) — exactly the "error-type apportionment is assumed" weakness `STATISTICS-PLAN` §13 declares. Used to
*calibrate and justify* the injection design's apportionment, it strengthens C1 directly. Used as "the natural
experiment arm, no injection", it produces an empty flip table.

### B4. Pre-registered quantities the plan changes without saying so

Nothing is registered yet, so nothing has been changed *after* registration. But the plan says "magnitudes … are
already registered" (§3b) — they are pre-specified in code, not registered; the distinction matters for the wording
of the registration itself. Items that change what will be registered and need an explicit line:

| change | in the plan? | ruling |
|---|---|---|
| H7 estimand: human pair → model-vs-official | declared (§3b) | fine, but H7's text "magnitude measured in the *same data*" is false for model predictions; rewrite the comparator |
| H7 "no injection" | asserted (§4) | must be re-decided (B3-2) |
| Magnitudes reinterpreted as floors | asserted as no change | is a change to H1's "matched magnitude" premise (B1) — declare or reword |
| Dropping "blind" | proposed | over-correction (B0); the paper says blinded |
| Dropping the in-house re-annotation fallback (`STUDY-PLAN-v2` §6 D1b, §10 risk register) | recommended (§5 Q2) | right: a pair started from the same centrelines reproduces the problem; from raw images is a different study. Record the decision |
| Editing `error_types.py` header | proposed | changes a hashed file — re-issue the manifest; and the header needs a content fix (A5-1), not a caveat |
| Title/framing "segmentation error" → "pipeline error" (§5 Q3) | flagged as positioning | positioning only; no registered quantity moves |

---

## C. Required changes

**MUST (before the registration is lodged)**

- **M1** Reconcile the C1/§E1 description with `error_types.py`: remove "topological event rate", "quality-matched
  (operationalised)" and "conditioned on the stratifiers" from `STUDY-PLAN-v2` §E1 and §9 attack 3, or implement them
  (which would be a new design). Fix the `error_types.py` header so it does not claim measured magnitudes for T1/T2.
- **M2** Regenerate `SEVERITY-SWEEP-SPEC` §8d's cohort descriptors from the frozen file (50/50/50; 108; 93; 80/70;
  22/40/88; 89/61; R 125 / L 8 / Co 17; prox 104 / mid 46; upstream 37).
- **M3** Replace `STUDY-PLAN-v2` §5 with a pointer to `STATISTICS-PLAN`; fix §8 "38" → 36 in `STATISTICS-PLAN`.
- **M4** Write the post-fix smoke CSV (with `fit_n_basins`, `fit_at_bound`) to `results/` so "0 of 38 rows changed" is
  a checkable fact. Keep the pre-fix file, renamed `_PRE-MINIMISERFIX`.
- **M5** Make `ablation.py` lines 174–176 and `DETECTOR-SPEC` §9 agree with `CFD-ARM-SPEC` §10: 9.3 and 33.3 are
  reviewer-probe values, 10.1 is genuine and fails the check.
- **M6** Re-issue `COHORT-FROZEN-2026-09-18.sha256` for the code block at registration (`ablation.py` has moved; it
  will move again for B1/B2 and the header edit).
- **M7** Reword `NEXT-PLAN` §2 and the attack-3 pre-emption: the *statistics* are optimistic per the authors; the
  *magnitudes* are not claimed to be bounds in either direction (B1).
- **M8** Replace the C1 topological sentence with wording that names β0+β1 for what it measures (B2).
- **M9** Decide and register what the model-vs-official arm inserts (nothing → ΔFFR-only endpoint; or the same
  virtual stenoses → new eligibility rules), before `STATISTICS-PLAN` §13 is rewritten.

**SHOULD**

- **S1** Keep "blind" with the qualifier "to the other's labels; shared automatic initialisation".
- **S2** Reword H1 from "at matched disagreement magnitude" to "at the magnitudes specified in §E1".
- **S3** Fix 22/141 → 20/140 in `STUDY-PLAN-v2` §6 and E0-NOTE §"Second finding" (headline already 20).
- **S4** Amend the four questions to Bransby per B3 (raw + post-processed; which weights; drop Q4).
- **S5** Add to the paper's C1 paragraph that the checked-vs-unchecked asymmetry biases the published disagreement
  *upward* — cite Bransby's own reason for it. Naming both biases is more credible than naming one.
- **S6** Note in `STATISTICS-PLAN` §10 that "11/1,920" is the count exceeding +1 %.

---

## D. What was verified and how

Probe scripts and full outputs: `references/FABLE-AUDIT-RESULTS-PLAN-2026-09-19-probe/` (`probe_results.py`,
`probe2.py`, `*.txt`). Hashes by `shasum -a 256`. Email read with `pdftotext -layout`. ImageCAS-X paper: arXiv
2608.30404 (HTML), Zenodo record 21887809. No file in the project was modified; the full ablation was not run.
