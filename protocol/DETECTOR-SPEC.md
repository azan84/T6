# C3 — deployment-time detector of concealed geometric error: specification

**v0.2, 2026-09-19.** Supersedes v0.1 (same date), which an independent adversarial review returned **DO-NOT-RUN**
(`references/FABLE-REVIEW-DETECTOR-2026-09-19.md`). v0.1 is not archived as a separate file because it was never
acted on; what it proposed and why each piece failed is recorded in §10, so the reasoning is not lost and is not
re-litigated.

Governs STUDY-PLAN-v2 §E5 (C3) and STATISTICS-PLAN §P5 (H5). **Not yet lodgeable** — §0 lists what blocks it.

---

## 0. Status — what blocks this document

| # | Blocker | Owner | Effect if decided the other way |
|---|---|---|---|
| ~~**B1**~~ | **SETTLED 2026-09-19** — Protocol C targets the clean tree's **FULL** territory outflow, including the deleted branch's share (`STATISTICS-PLAN` §P2 as written). T1 `C_ratio` 1.049 → **0.928**, i.e. §2's mechanism now holds: the bed draws harder through fewer vessels. **S_C's effect size must be recomputed under this target before B3 below can be answered** — the reviewer's ≈ 0.65 AUC estimate was derived under the old one. | done | — |
| **B2** | `ablation.py` Protocol C minimiser lands in the wrong basin (§9 / review §5) | **fixed and re-run 2026-09-19** (`results/ablation_smoke_POSTFIX-2026-09-19.csv`: 0 of 38 rows changed — the pathology is absent from the smoke set, which is why the smoke never caught it) | contaminates the positive class *and* P2's headline number |
| **B3** | Expected AUC for S2 must be computed and written down **before** registration, not discovered after (review SHOULD 11) | analysis | if < 0.80, H5's threshold is revised or the inverted finding is registered as expected |
| ~~**B4**~~ | **RESOLVED 2026-09-19** — `VALIDATED_RESIDUAL = 0.10` stands, with a corrected justification: the old "10–15 % test–retest" was a **wsCV** used as though it were an agreement bound (they differ by ~2.8×). Because this residual compares a deterministic model against **one** noisy measurement, the correct 95 % bound is ≈ 0.13–0.16, so 0.10 is **stricter than required and conservative for H2** (P(passes ∧ wrong) is monotone non-decreasing in the threshold). `references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md` | done | — |

**B1 was the one that mattered most. It was settled and applied on 2026-09-19** — the recommendation in §11 was
accepted. §11 is retained as the reasoning behind the decision, not as a pending action.

## 1. The governing constraint — what the detector may see

**At deployment there is one model.** Built from one segmentation, which may be wrong, tuned to its perfusion
targets, which it now matches. There is no clean baseline, no second annotator, no invasive measurement. Every
statistic below is computable from that model alone plus a population prior.

Disqualified permanently: ΔFFR against the clean model; `C_ratio` (needs `C_clean`); the injected error type or
magnitude; **and any quantity Protocol C tuned on** — under Protocol C that quantity is zero by construction, and
matching it *is* the concealment.

## 2. What is actually knowable — the algebra that shapes this spec

The review's decisive finding, and the reason v0.1 collapsed. In this model the bed conductance is a deterministic
function of `r_ref` (`zerod_ffr.py:128–132, :144`) and the solver output *is* the pressure field. By mass
conservation, the flow entering any node is its subtree's bed outflow:

```
Q(v) = Σ_{u ∈ sub(v)} w(u)·(P(u) − P_v) / C
```

so **any flow statistic along the tree is (anatomy) × (the model's own pressure solution) ÷ C, exactly.** It is not
independent information. This is the same identity that STUDY-PLAN-v2 §E5's original statistic 1 fell to, one step
removed — and v0.1's S1 fell to it too (§10).

**Therefore the only deployment-time information in this model is:**

| source | what it is | independent of the solve? |
|---|---|---|
| `C` | the one tuned parameter | yes — it is what the fit chose |
| `ρ` | the per-territory residual vector the fit could not remove | yes |
| **anatomy** | `r_ref`, `r_fit`, the branching structure — *before any model is built* | yes, entirely |

Everything else is a function of these. A statistic that a reviewer can reduce to an identity in one line is worse
than no statistic, and attack 7 ("the detector is circular") is answered by this table, not by a flow profile.

**Consequence for the contribution, stated plainly.** C3 is no longer "a test that the tuning concealed something".
It is two tests of different kinds, and the paper must say which is which:

- **S_C — a weak tuning-side signal** (§3.1). The tuned parameter is pushed off its anatomical closed form. Expected
  AUC ≈ 0.64–0.69 for T1 against physiological variation (review §2) — **below H5's 0.80 threshold, arithmetically,
  before any run.** See B3.
- **S_A — a strong anatomy-side signal** (§3.2). A missing branch leaves a geometric fingerprint that does not need
  the haemodynamic model at all, and is computable on the raw mask.

That S_A does not require the model is the honest and interesting finding, not a weakness: **the concealment is
detectable, but not from the tuning — from the anatomy the tuning was applied to.** §11 recommends leading with that.

## 3. The statistics

### 3.1 S_C — tuned-parameter implausibility (tuning-side)

`calibrate()` sets healthy inflow = K·r_root³, so up to the healthy epicardial drop,

```
C_closed(anatomy) = (P_in − P_v) · Σ_v w(v) / ( K · r_ref(root)³ )
S_C = [ ln C_tuned − ln C_closed(corrupted anatomy) ] / σ_neg
```

Verified on all 108 cohort trees (review §2): the four-covariate OLS of v0.1 recovers exactly this closed form
(β = −3.02, +1.03 against theory −3, +1; R² = 0.9997 leaky / 0.991 discrete). **The regression was therefore not a
prior, it was an identity with a rounding error.** `ln n_outlets` and `ln L_resolved` are inert and collinear
(VIF 18–20 discrete) and are dropped.

**σ_neg is estimated on the training-split negatives — clean anatomy, perturbed physiology — never on nominal clean
models.** v0.1 used the regression residual (σ = 0.0076), which contains none of the variance the negative class is
made of and scored a ±20 % cardiac-output *negative* at z ≈ 24–29. That error is the difference between a prior and
a tautology.

**Multivariate variant.** STATISTICS-PLAN §P2's pre-specified per-territory sensitivity yields a tuned vector;
S_C becomes its Mahalanobis distance from the same negatives. Recorded whenever that variant runs; never primary.

### 3.2 S_A — junction plausibility (anatomy-side)

**Principle:** a vessel that loses calibre without giving off a branch is anatomically implausible. Murray's law says
a parent's r³ is shared among its daughters; a missed branch breaks the books at exactly one junction, and a
truncation leaves a vessel ending while still wide. Neither needs the haemodynamic model — **S_A is computable on the
segmentation before any FFR pipeline runs**, which is both its strength and, honestly, the reason it also belongs to
segmentation QA.

The candidate is the **orphan weight** already central to the leaky bed (`zerod_ffr.py:132`):

```
orphan(J) = [ r_ref(J)³ − Σ_{children c of J} r_ref(c)³ ] / r_ref(J)³
```

with the per-tree statistic taken over resolved host-path junctions. The review's probe (4 instances) found deleted
junctions separating from the null by roughly an order of magnitude, with a tight null at non-deleted junctions.

> **S_A is specified here in principle and is NOT yet pre-registerable.** The probe is 4 instances, and the exact
> form (raw orphan, its change along the path, the tail statistic, and the null's dependence on vessel and image
> quality) has not been characterised. **Required before freezing:** a protocol-grade characterisation on the frozen
> cohort under both beds, reporting the null distribution at non-deleted junctions and the separation at deleted
> ones, per error type and per vessel. Until then no operating point and no AUC claim for S_A is registered.

**Expected scope, pre-registered as a directional claim:** S_A detects the **topological** error types (T1, T2) and
**cannot detect T4**, because T4 scales `r` and `r_ref` together, leaving every ratio invariant — and cannot detect
T3, which changes no anatomy at all. That is the boundary of the method and the paper reports it as such. It is also
the paper's thesis restated: what is hidden is topology.

### 3.3 ρ — the residual vector

Recorded in full, signed, per territory. **No scalar summary is pre-registered.** v0.1's concentration statistic is
dropped: `n_territories = 2` in 104/108 trees (leaky) and 99/103 (discrete), where `max|ρ|/rms(ρ)` is bounded in
[1, √2] identically, and it is 0/0 for exactly-absorbed negatives. If a residual-pattern statistic is wanted later it
is pre-specified for `n_territories ≥ 3` only — **4 trees of 108**, so it is not worth a hypothesis.

### 3.4 Combined

Logistic regression on `(S_C, S_A)`, fitted on the training split, evaluated once on held-out and once external.
Two inputs against ≈ 40 training positives sits inside the 10-events-per-variable rule (v0.1's four inputs did not).
Per-statistic and combined ROCs all reported.

## 3.5 ⚠ BOTH CLASSES MUST BE TUNED AGAINST THE SAME KIND OF TARGET — found 2026-09-19 by building §5

**Implementing the negative class exposed a confound that would have made H5's AUC meaningless. It is not a defect in
either class — it is a mismatch between them.**

The ablation's Protocol C tunes against the **clean model's exact territory flows**: deterministic and noiseless.
That is correct for the primary experiment, because it isolates the anatomical effect. The negatives, by construction
(§5), tune against a **noisy measurement**. So the classes differ in how their targets were built, not only in
whether their anatomy is right — and the target construction dominates. Measured on the smoke set
(`results/negatives_smoke-2026-09-19.csv` vs `results/ablation_smoke_DETECTORCOLS-2026-09-19.csv`):

| statistic | negatives (correct anatomy, **noisy** targets) | positives (corrupted anatomy, **clean** targets) |
|---|---|---|
| residual | **0.0721** | 0.0283 |
| `C_ratio` | **1.128** | 0.997 |
| \|ΔFFR\| | 0.0376 | 0.0890 |

**The negatives fit worse, and move their tuned parameter more, than the positives.** Both S_C and the residual
would classify **backwards**. Nothing about anatomy is being measured; the noise in the targets is.

**Required before any detector result: the positives must be re-tuned against targets carrying the same noise model
as the negatives** — corrupted anatomy *and* a noisy measurement, which is the deployment situation for a wrong
model. This is a **detector-specific pass, not a change to the ablation**: the registered Protocol C keeps its
noiseless targets, because its job is to isolate the anatomical effect and altering it would move a pre-registered
quantity for a reason unrelated to H1–H4.

Run order for C3: ablation (registered, noiseless) → negatives (§5) → **positives re-tuned under the §5 noise
model** → fit and evaluate. Only the third is new work, and it reuses `negatives.py`'s noise model on corrupted trees.

## 4. Labels — complete, with the middle assigned

```
positive   :=  Protocol C run  AND  territory residual < VALIDATED_RESIDUAL (0.10)   [passes its check]
                                AND  |ΔFFR| > MATERIAL_DFFR (0.05)                   [and is materially wrong]
negative   :=  clean anatomy, perturbed physiology (§5), tuned by the identical Protocol C procedure
excluded   :=  (a) Protocol C runs that pass the check and are NOT materially wrong
               (b) Protocol C runs that FAIL the check
               (c) instances with n_territories < 2 (no flow split to match)
```

Every exclusion is **logged with its reason and counted in the CONSORT flow** (STATISTICS-PLAN §9). v0.1 left (a) and
(b) in neither class, which would have silently removed ~40 % of Protocol C rows — a reviewer would have asked.

Class (b) is not a detector failure but its complement: a model that fails its own validation check **is already
caught by the check**, and needs no detector. The paper says so — it is the boundary between "the check works" and
"the check is fooled", and only the second is C3's territory.

**Expected positive count** (review §3, to be confirmed protocol-grade): ≈ 55–85 per bed, **≥ 85 % of them T1**;
T2/T3/T4 ≤ 10 each. Held-out third ≈ 20–28, DeLong CI half-width ≈ 0.10–0.12 at AUC 0.8. **Per-error-type ROCs for
T2–T4 are therefore descriptive, not inferential, and are labelled so.** Whether the primary H5 ROC should be T1-only
is an open question for the operator (§11).

## 5. The negative class — constructive specification

v0.1 pointed at STATISTICS-PLAN §6 and called it "already pre-specified". It is specified but **not implemented**:
there is no Monte Carlo in `code/`. Worse, as described it is degenerate — a global cardiac-output change is absorbed
*exactly* by a single global scaling (probe residual 0.0000), so `residual > 0.001` alone would separate the classes
at AUC 0.82–0.90. That is a perfect detector of nothing.

**Negatives must contain a perturbation the single scaling cannot absorb.**

| component | side | handle | status |
|---|---|---|---|
| cardiac output | truth | `demand(scale=)` | exists |
| mean arterial pressure | truth | `P_in` argument | exists |
| haematocrit → viscosity | model | `MU` is a **module constant** | **must be parameterised** |
| heart rate | — | **no handle in a steady model** | **stated as not represented, not silently omitted** |
| **per-territory demand-share noise** | truth | **none — must be built** | **required**: the component a global scaling cannot absorb |
| **target measurement noise** at the test–retest SD | truth | **none — must be built** | **required** |

The last two are what make the negatives non-degenerate, and the second of them makes `VALIDATED_RESIDUAL = 0.10` an
operating characteristic rather than an arbitrary constant: targets are noisy at the repeatability the threshold is
derived from, so a correct model misses them by about that much.

> **Which noise statistic — this is easy to get wrong by a factor of 2.8.** Target measurement noise is injected at
> the **within-subject SD** (per-territory hyperaemic wsCV ≈ **8.3 %**), **not** at the repeatability coefficient.
> The RC is the 95 % bound on the difference between *two* measurements and already carries a √2 for the second
> draw; here the model is deterministic and only the target is noisy, so one SD is the correct dispersion.
> Injecting at the RC would inflate the negatives' residuals ~2.8× and make the detector look far better than it is.
>
> **Consequence, and it is the answer B4 wanted:** at that wsCV, a threshold of 0.10 passes a correct-but-noisy
> model about **77 %** of the time. So "passes its validation check" has a stated false-reassurance rate rather than
> being a bare constant, and the 10 % check can be reported as an operating point with a known specificity.
> Derivation in `references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md`.

**Draws:** one negative draw per instance per ROC replicate, with the number of replicates pre-specified — not 1,000
draws against ≈ 60 positives, which is a 1,000:1 imbalance with within-instance correlation that violates DeLong's
independence assumption.

## 6. Splits, operating point, external test

- **Split unit is the patient (`scan`)**, never the instance (STATISTICS-PLAN §2's rule, same reason).
- **2:1 train / held-out**, stratified by vessel and discrete-bed band.
- **Frozen as an explicit hashed patient list** — `protocol/DETECTOR-SPLIT-FROZEN-<date>.csv` + SHA-256, lodged
  **before any fitting**, never a seed (STATISTICS-PLAN §11's lesson).
- **Operating point:** threshold on the training split at sensitivity 0.80, applied unchanged thereafter.
- **External test:** ASOCA if Gate D2 clears; otherwise held-out ImageCAS-X scans outside the cohort — **a split is
  not an external dataset and the paper will not call it one.**
- **Analysis:** ROC/AUC, DeLong 95 % CIs, per statistic and combined, **per bed structure, never pooled**.

## 7. What must be recorded — 0D

> **IMPLEMENTED 2026-09-19, before registration.** `ablation.py` now emits three streams per run: the main table,
> `<out>_territory.csv` and `<out>_pullback.csv`. Verified on the 6-instance smoke
> (`results/ablation_smoke_DETECTORCOLS-2026-09-19*.csv`): 12 clean rows (6 instances × 2 beds), `run_id` unique and
> non-null on all 136 rows, the territory file's RMS residual reproduces the main table's `outlet_flow_residual` to
> **6.6e-17**, no root station carries `Q = 0` (so no `ln q_norm = −∞`), and — the check that matters — **every
> corrupted row is bit-identical to the pre-change run** (max difference 0.0 across 30 numeric columns). The columns
> are additive; the experiment did not move.
>
> Done now rather than after lodging because twelve minutes of compute is cheap and a post-registration code change
> is a declared deviation.
>
> **`S_A` is recorded as its INGREDIENT, not as a statistic.** Every pullback station carries `orphan_frac` =
> (r_ref³ − Σ children r_ref³)/r_ref³ together with `n_children`, so the §3.2 characterisation can be done on stored
> data without re-running, and the eventual statistic can filter to true bifurcations (`n_children ≥ 2`) or not, as
> the characterisation decides. Recording the ingredient keeps §3.2's "not yet pre-registerable" honest.
>
> **The §5 negative class is now IMPLEMENTED too** — `code/negatives.py`, 2026-09-19. `MU` was parameterised as a
> `Tree` attribute to allow it (self-test unchanged; default behaviour identical). Heart rate remains unrepresented
> and is stated as such, not silently omitted — this is a steady model.
>
> **Verified non-degenerate on the smoke set**, which was the whole risk: residual median **0.072** (p10 0.016,
> p90 0.157) rather than ~1e-9, so the trivial separator "residual > 0.001" that would have given a meaningless
> AUC 0.82–0.90 is gone. **64 %** pass the 10 % check, against §5's predicted ~77 % — the difference is the
> territory-share noise, which §5 adds on top of the measurement wsCV the prediction was based on.
>
> **And it produced a number the study needs independently of the detector: |ΔFFR| ≈ 0.038 median on CORRECT
> anatomy.** That is the FFR error a perfectly segmented model still makes when tuned to a noisy measurement — the
> irreducible floor, against `MATERIAL_DFFR` = 0.05. It belongs beside every injected-error effect
> (`STATISTICS-PLAN` §6), and it bounds what any detector can achieve.
>
> **All the noise constants were searched on 2026-09-19 and the physiological three were corrected** (by factors of
> 2–8; `references/CITATION-PHYSIOLOGICAL-SDS-2026-09-19.md`). What remains is more interesting than what was fixed:
>
> **`SD_TERRITORY_SHARE` has no supportable single value, and it sets this arm's headline specificity almost
> alone.** Two independent sweeps agree: the pass rate at the 10 % check runs **92 / 85 / 68 / 53 / 43 / 40 %** across
> SD 0 → 0.25. So the specificity is reported across a **pre-registered band of 0.05 / 0.10 / 0.15 / 0.20**, never as
> a point estimate. Not extended past 0.20 — above it the share draw starts producing fits at the search bound.
> The closest direct measurement (Keulards 2020, 35 patients, anatomical volume prediction vs invasive hyperaemic
> flow share) implies **≈ 0.19 RMS**, so our pre-specified 0.10 sits at the **low** end.
>
> **⚠ AND THE CRITICAL ASYMMETRY: both remaining noise terms err in the same, flattering direction.**
> `SD_TERRITORY_SHARE` is low against Keulards, and `WSCV_TARGET = 0.083` is roughly **half** Kaufmann 1999's
> regional hyperaemic within-subject CV of 15–21 %. Too little noise makes the negative class easy, which **inflates
> specificity**. **The detector's reported specificity must therefore be read as an upper bound**, in those words,
> until both are resolved.
>
> **What is NOT fragile, and the distinction belongs in the paper:** across the same sweep the median |ΔFFR| on
> correct anatomy moves only **0.0190 → 0.0225**. So the physiological-noise-floor claim (`STATISTICS-PLAN` §6) is
> robust to this constant; it is only the *validation-gate specificity* that depends on it. Two different claims,
> two different levels of confidence, reported as such.

**7.1 New scalar columns** in the main ablation CSV: `run_id`; `C_abs` (the tuned C itself — `C_ratio` cannot serve,
it needs the clean model); `w_sum`, `r_ref_root_mm`, `n_outlets`, `L_resolved_mm` (S_C's closed form, from the
**corrupted** model); `S_A` candidates per §3.2 once characterised; `n_territories`; and the §9 fit-diagnostic
columns (`fit_n_basins`, `fit_loss_at_Cstart`, `fit_at_bound`).

**7.2 `results/ablation_territory_<tag>.csv`** — one row per (`run_id`, territory): `terr_id, root_node, root_xyz_mm,
Q_target_mls, Q_achieved_mls, residual, sum_w, n_nodes, n_outlets, contains_error`. `contains_error` is an
experiment-side analysis label, **never a detector input**.

**7.3 `results/ablation_pullback_<tag>.csv`** — the per-station profile (`ffr, Q_mls, r_mm, r_ref_mm, q_norm`).
**Retained, but demoted:** no §3 statistic uses it. It exists for the mechanism figure, for the 0D-vs-3D pullback
comparison, and so that the abandoned statistics remain checkable by a reviewer who asks. It is **not** a detector
input and **never ships in a CFD package** (§8).

**7.4 Rows that must exist and currently do not:** a **clean row per (instance, bed)** with its own `run_id`
(`ablation.py` writes clean values only as columns of corrupted rows), and the **negative-class rows** from §5.
The pullback file needs `info["inflow"]` for the root station — `evaluate()` returns `Q[0] = 0`, which would have
made `q_norm = 0` and `ln q_norm = −∞` at the origin of every right tree.

## 8. What must be recorded — 3D

**The justification in v0.1 was false and is corrected here.** None of §3's statistics needs a pressure plane:
`Q(station)` is the sum of downstream outlet flows, which CFD-ARM-SPEC §12 already returns, and S_C and S_A need no
station at all. The intermediate stations are kept — they are cheap — but for what they actually serve:

1. the **mechanism figure** (§E3b): the spatial pressure field showing outlets matched and interior wrong;
2. the **0D-vs-3D pullback comparison**, which is a fidelity check, not a detector input;
3. the **through-plane flow integral** `∫U·n dA`, which is free, gives 3D `Q(station)` directly, and **checks mass
   balance against the outlet sums** — added to the return set on the review's recommendation.

**Required additions to the station specification** (v0.1 asserted "sampling method unchanged", which is optimistic
at ~40 planes × 1,260 solves):
- **Plane clipping rule:** keep only the connected cut component containing the station's centreline point, within a
  sphere of ≈ 2·r_ref. A `cuttingPlane` cuts the whole domain — on a tortuous RCA or an LAD with parallel diagonals
  it also slices other vessels, and a naive area-average is then wrong. With 4 probes this is caught by eye; with
  50,000 it is not.
- **QA column:** cut area vs π·r_local², returned per station.
- **`bifurcation` stations are ill-defined for a single plane** — replaced by stations ≥ 1 diameter proximal and
  distal to each bifurcation.
- **Real tier:** `q_norm` at 3D uses the `r_ref` of the 0D twin rebuilt from **as-meshed** radii (§6.1b), not the
  pre-mesh `r_ref_mm` shipped in `probes.csv`.
- **Blinding:** `r_ref_mm` in `probes.csv` is anatomical and is **not** a leak (it is already in `outlets.csv` per
  §11). The 0D pullback file (§7.3) is a prediction and **never ships**.

## 9. `ablation.py` Protocol C minimiser — fixed 2026-09-19 (B2)

`minimize_scalar(method="bounded")` is a local method on a loss that is **bimodal in log C**. For scan 341 / RCA /
leaky / T1 it returned C_ratio 0.077 (residual 0.050, ΔFFR −0.52) when the global optimum is C_ratio 1.00
(residual 0.004, ΔFFR ≈ 0). As C → small the flows become epicardially limited and the *ratio* of territory flows
happens to match the target ratio again — a second basin with no physical meaning.

**That row would have been recorded as "passes its validation check and is materially wrong": a false absorption
count in P2's headline number and a false positive for H5.** 1 of 16 T1 fits in the reviewer's probe.

**Correction, 2026-09-19:** an earlier version of this paragraph attributed `C_ratio` values of 9.3 and 33.3 to the
smoke run. They are from the reviewer's probe, not the smoke — the smoke's largest is **10.1** (scan 335 / discrete /
T2), and that fit is **unimodal and genuine**, not this pathology; it also fails the 10 % check (residual 0.62) so it
never enters the positive class. Post-fix, the smoke changed **0 of 38** Protocol C rows: the pathology is not in the
6-instance smoke set at all. Its incidence across the 150-instance cohort is unknown until the full run, and scan 341
proves it is not zero.

**Fix applied:** coarse 61-point log-grid scan over ±1.5 decades → Brent refinement in the best bracket; record
`fit_n_basins`, `fit_loss_at_Cstart`, and `fit_at_bound`; **a fit at a search bound is a failed fit, logged, not a
result.** STATISTICS-PLAN §9 must name this case alongside non-converged solves. The smoke test must be re-run and
the number of changed rows reported before the ablation.

## 10. What v0.1 proposed, and why each piece failed

Kept so the reasoning is not repeated by a future reader — or by a reviewer asking "did you consider a flow
statistic?"

| v0.1 | Verdict | Why |
|---|---|---|
| **S1** — `q_norm = Q/(K·r_ref³)` along the host path, claimed ≈ 1 in clean trees and stepping distal to a deleted branch | **dead** | an exact function of (r_ref, the model's pressure solution, C) — §2's identity. Empirically: clean lesion-free trees span |ln q_norm| up to 1.46 (leaky) / 2.04 (discrete), a factor of 7.7 with no error present; the T1 change is 0.00 ± 0.07 **distal** to the branch and −0.10…−0.63 **proximal** — wrong sign, wrong side; probe AUC 0.23–0.56 (chance). Also not blind to disease (the lesion adds ≈ \|ln FFR\|) and not shape-only (it moves one-for-one with ln C) |
| **S1_step** | dead | clean trees already have a large negative step at every bifurcation; deleting a branch *removes* a step rather than creating one. Without a same-tree clean profile, "a bifurcation with a small step" is indistinguishable from "a run with no bifurcation" |
| **S2** as a 4-covariate OLS prior | **respecified** (§3.1) | the regression was the closed form C = (P_in−P_v)·Σw/(K·r_root³), R² = 0.9997 — an identity, not a prior; σ from its residual scored physiological negatives at z ≈ 24–29 |
| **S3_conc** | dead | bounded in [1, √2] wherever `n_territories = 2`, which is 104/108 trees; 0/0 for exactly-absorbed negatives |
| **negative class** "already pre-specified" | **rebuilt** (§5) | not implemented anywhere in `code/`; and globally absorbed, so `residual > 0.001` would have separated the classes at AUC 0.82–0.90 |
| §8's justification for 3D stations | **false, corrected** (§8) | no §3 statistic uses a pressure plane |
| "discrete performs better than leaky" pre-registered expectation | **withdrawn** | rested on the §2 mechanism the code does not implement (B1); at chance in both beds in the probe |

## 11. Recommendation to the operator

1. **B1 — resolve Protocol C's target as the clean tree's FULL territory perfusion, including the deleted branch's
   share** (i.e. STATISTICS-PLAN §P2 as written; `ablation.py` changed to match). **APPLIED 2026-09-19** — targets
   are now partitioned by the *clean* tree's territories (`ablation.protocol_c_targets`), and the guard that
   Protocol C needs ≥ 2 such territories with surviving members costs 40 % of T1 rows and 33 % of T2 rows, almost
   all RCA (`STATISTICS-PLAN` §9).
   Reason: the target represents what perfusion imaging measures *in the patient*, and the patient's myocardium is
   perfused whether or not the segmentation saw the branch. The coded alternative sets the target from the surviving
   nodes only — a target that is itself corrupted by the segmentation error, and one no clinic could produce without
   already knowing which branch was missed. Under the corrected definition the surviving vessels must carry the
   missing branch's share, C falls (C_ratio < 1), and §2's mechanism holds; under the coded definition C_ratio > 1 in
   every T1 run and the mechanism is inverted. **It changes what the paper claims, so it is your call, not mine.**
2. **Lead C3 with S_A, not with S_C**, and say what each is: the tuning carries only a weak signature (AUC ≈ 0.65),
   while the anatomy carries a strong one — *and the anatomical check needs no haemodynamic model at all*. This is a
   more defensible contribution than a flow statistic a reviewer reduces to an identity in one line, and it answers
   attack 7 better than v0.1 did.
3. **Decide H5 before registration** (B3): with S_C at AUC ≈ 0.65 for the error type supplying ≥ 85 % of positives,
   the 0.80 threshold is out of reach on the tuning side. Either register the inverted finding as the *expected*
   outcome, or set the threshold on the combined `(S_C, S_A)` score once S_A is characterised. Do not discover this
   after the run.
4. **Consider whether the primary H5 ROC is T1-only**, given the class composition.

## 12. Open items

- [ ] **B1** — Protocol C target definition (§11.1). Blocks §2, §3.1, and the S_A characterisation.
- [ ] **B2** — smoke re-run after the minimiser fix; report rows changed.
- [ ] **B3** — expected S2/S_C AUC written down before registration.
- [ ] **B4** — `VALIDATED_RESIDUAL = 0.10` citation (§5 offers a principled route).
- [ ] S_A protocol-grade characterisation on the frozen cohort, both beds (§3.2).
- [ ] Negative-class Monte Carlo implemented, including the two non-absorbable components (§5); `MU` parameterised.
- [ ] Collet 2019 — verify before citing (the pullback analogue is now demoted to §7.3, so this may no longer be needed).
- [ ] Gate D2 (ASOCA) — external dataset or split (§6).
- [ ] Reproduce the review's probe numbers protocol-grade before freezing (its SHOULD 15).
- [ ] Detector block remains **unassigned** in the CRediT table (STUDY-PLAN-v2 §7b).
