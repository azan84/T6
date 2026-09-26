# Pre-flight review before the full-scale 0D cohort run and pre-registration lock

**Reviewer:** Fable 5.1 (adversarial pre-flight; not a peer review) · **Date:** 2026-09-18, 17:30–19:10
**Scope as briefed:** `code/zerod_ffr.py`, `imagecasx_loader.py`, `severity_sweep.py`, `run_prevalence.py`,
`stageA_benchmark_0d.py`; `protocol/SEVERITY-SWEEP-SPEC.md`, `protocol/CFD-ARM-SPEC.md` v0.2; `STUDY-PLAN-v2.md`;
`references/FABLE-REVIEW-DISCRETEBED-2026-09-18.md`; `results/E0-PREVALENCE-NOTE.md`; every CSV under `results/`
and `cfd_handover/stageA/`. Nothing under `code/`, `protocol/`, `results/` or `cfd_handover/` was modified by me.

**Provenance note — the target moved during the review.** The review started against `zerod_ffr.py` 17:20 and
`results/sweep_test.csv` 15:55. At 18:15–18:22 the operator replaced the lesion-term rule in `Tree._set_radius` and
added check V3b to `severity_sweep.py`, then regenerated E0 (18:39), the sweep and the selection (18:50;
`results/REGEN-2026-09-18.log`), keeping the old files as `*_PRE-LESIONRULE.csv`. That change implements the
blocking finding of §2 below (the new code's docstring cites this review). §1–§2 are therefore written twice: what
was wrong at 17:20, and what the 18:50 state looks like re-verified independently. The GO decision at the end refers
to the **18:50 state**.

**Evidence** (all in `references/FABLE-PREFLIGHT-2026-09-18-probe/`; every number below is traceable to one file):
`resweep.py` → `sweep_current.csv` (17:20 code), `sweep_cap3.csv` (17:20 code with the 3-lesion cap restored),
`sweep_treerule.csv` (probe rule R2); `compare_sweeps.py/.txt`, `compare_treerule.py/.txt`, `compare_regen.txt`,
`compare_selection_v2.txt`; `v8a_probe.py/.txt`; `physics_probe.txt`; `runrule.py`, `runrule2.py`, `runrule3.py`,
`runrule4.py` (probe-only monkey-patches of `_set_radius`) with `runrule*_effect.txt`, `t3_step_debug.txt`,
`purestock_kcensus.txt`; `discrete_cohort.py` → `discrete_cohort.txt` (17:20 state) and `discrete_cohort_v2.txt`
(18:50 state); `e0_current.txt`, `e0_treerule.txt`, `e0_r4.txt`; `verify_stock_*.txt` (the operator's suite,
both beds, both scan sets, 18:50 code); `stageA_probe.py` → `expected_0D_probe.csv`.

---

## Decision: **GO-WITH-CHANGES** for the 18:50 state (it was **DO-NOT-RUN** at 17:20)

The 17:20 code had a defect the request did not ask about: the expansion-loss placement rule (fixed 5 mm radius,
per segment) produced spurious second/third loss terms on 2,281 of 6,944 sweep instances and a discontinuous
dependence on node placement and lesion length. The V8a "marginal failure" was that defect, not discretisation. The
18:50 code replaces the rule (local-maximum throats, tree-path 5 mm merge), adds check V3b, and regenerates
everything; I re-ran the verification suite on both beds and both scan sets against the regenerated E0 and all
checks pass (V8a 0.0012–0.0030, V10 0.0000). What remains before the run is pre-registration content, not code:
the discrete-arm N and band rule, the frozen instance list, the statistics unit, and five document contradictions.

---

## 1. Must the sweep and the selected cohort be regenerated?

**They have been (18:50); the decision was correct, the stated reason was not the operative one.**

*What the lesion-cap removal alone did* (`compare_sweeps.txt`, 17:20 code vs 15:55 file). First, provenance:
`sweep_cap3.csv` (17:20 code with the old cap restored) is **bit-identical to `sweep_test.csv` 15:55 in all 6,944
rows**, so the 16:51 loader edit and every other v3 change were numerically inert for the sweep; the cap removal was
the only live difference. Its effect: 1,060 instances move, |ΔFFR_meas| p50 0, p90 4e-5, p99 0.0031, max 0.0099;
16 band changes in the whole sweep; **selected 150: 0 band changes, max |Δ| 0.0058, 0 decision changes, 25 per band
intact.** On the cap fix alone the cohort could have been kept. (Aside: `E0_prevalence_test_PRE-V9FIX.csv` lacks the
`C/iters/converged` columns — it is the v2-era file — so the "318 moved, 236 up" figure in the brief includes the
v2→v3 root-leak change; removing a cap cannot raise FFR. Say so in the change log.)

*What the lesion-rule fix did* (`compare_regen.txt`, `compare_selection_v2.txt`): 3,376 instances move, mean
+0.0015, max **+0.1439**, 426 by > 0.005, 171 by > 0.01, 62 by > 0.02; 162 band changes; 22 decision changes.
The PRE-LESIONRULE selection re-evaluated under the new rule has **10 band changes** (band counts 20/28/25/26/25/26)
and 2 decision changes — it could not have been kept. The new selection shares 40 of 150 instances and 89 trees
with the old one.

*Two things the pre-registration must absorb:*
1. **The selection is chaotic in its input.** `select()` (`severity_sweep.py` 224–244) shuffles once and walks
   `pool.vessel.unique()` greedily; on the 17:20 sweep (16 band changes of 6,944) it returned a cohort sharing only
   62/150 instances with the 15:55 one. "Seed 20260918" is not a reproducibility guarantee. **Freeze the 150 as an
   explicit, hashed list** (`scan, side, vessel, loc, L_mm, ds_pct, c_mm`) in `protocol/`, and pre-register that list.
2. **Every number in `SEVERITY-SWEEP-SPEC.md` §8b–8d is stale.** New run: supply per band 366/348/514/641/998/1611;
   150 from **108 trees, 93 scans**; loc prox/mid **104/46**; L 10/20 **80/70**; quality 4/3/2 = 88/40/22;
   `bif_in_window` 26; no downstream bifurcation on the host path 32; no upstream 113; **16 doubled slots
   (32 instances = same host lesion at two severities)**; 15 scans contribute both trees. Rewrite §8b–8d from
   `REGEN-2026-09-18.log` and `compare_selection_v2.txt`.

## 2. V8a marginal failure — **it was a defect, now fixed; do not widen the tolerance**

*Decomposition at 17:20* (`v8a_probe.txt`; 993_left LCX prox L = 20 mm, 60 %DS, discrete, reference inherited):

| refinement | FFR_meas | K terms on host path (arc mm) | window nodes | C |
|---|---|---|---|---|
| ×1 (median spacing 0.49 mm) | 0.79188 | 2 at [6.87, 19.90] | 41 | 51.995 |
| ×2 | 0.78650 | **3 at [7.12, 19.96, 25.12]** | 82 | 51.795 |
| ×4 | 0.78637 | 3 | 165 | 51.689 |
| ×8 | 0.78674 | 3 | 330 | 51.606 |

Successive differences +0.00538, +0.00013, −0.00038: a jump, not O(h²). The three candidates named in the brief are
each ≤ 0.0003 — window Poiseuille resistance 4.9371e8 → 4.9381e8 Pa·s/m³ (0.02 %), measurement-node snap −0.00019,
C shift < 0.001 (fine tree with the coarse C: 0.78731). The whole change is the third K term at **25.12 mm = 5.22 mm
distal of the throat**, just outside the fixed 5 mm exclusion (`zerod_ffr.py` 17:20 line 163). A 20 mm cosine
lesion has DS ≥ 0.30 out to |s − c| = 5.00 mm at 60 %DS, 5.25 at 65, 5.46 at 70, 5.64 at 75, 5.80 at 80
(`physics_probe.txt` C), so at 0.49 mm spacing whether a node lands in the annulus was a coin toss — which is why
the first two verification runs "passed marginally" at 0.0039 and 0.0047 (`SEVERITY-SWEEP-SPEC.md` §8b): the same
artefact, different coins. The shoulder term is 2–12 % of the throat term at 60–65 %DS, i.e. 0.003–0.01 FFR. Census
on the 17:20 sweep: **2,281 instances carried ≥ 2 extra K terms; 91 % of L = 20, DS ≥ 65 instances**
(`compare_sweeps.txt`). Second face of the same rule: the per-segment loop restarted the exclusion at every segment
boundary, so a window containing a bifurcation got a second full-strength term in the child (20 of the 26
`bif_in_window` instances; scan 341 LAD 10 mm 65 %DS: 0.778 → 0.851 corrected, `runrule2_effect.txt`). Third face:
the T3 error type — a continuous length sweep at 65 %DS stepped −0.0055 at L = 22 mm (a new term) where the
corrected rule gives −0.0025/mm throughout (`t3_step_debug.txt`, `runrule4_effect.txt`).

*Rule design — one caution on the fix.* I tested four probe rules. Merging throats by |arc difference| (my R2/R3)
is wrong: two lesions on different branches can share an arc value and the deeper silently erases the other — R2
lost the main-vessel term in 3 E0 trees and, applied tree-wide, moved throats into daughters (145 NaN `lesion_ffr20`
in `e0_r4.txt` under a one-per-run variant). The operator's 18:22 rule (local maxima of DS along the tree; merge only
along an ancestor chain, `zerod_ffr.py` 176–200) avoids both traps and matches my R4 on every case I checked.
One residual risk to state: a *plateau* lesion (flat throat over several nodes with equal DS to machine precision)
yields several local maxima; the 5 mm chain merge covers this for plateaus < 5 mm, which is every inserted lesion
and any plausible native one.

*18:50 state, re-verified* (`verify_stock_*.txt`, both beds × both scan sets): V3b max non-native K terms in window
= 1 everywhere; **V8a 0.0024 / 0.0030 (leaky) and 0.0012 / 0.0026 (discrete)**; V8b 0.0025–0.0038; V10 **0.0000**
against the regenerated E0; V4/V5/V9 zero violations; all converged ≤ 28 iterations. Residual V8a on the 993 slot
decomposes as +0.0018 Poiseuille discretisation, −0.0008 C recalibration (reference-inherited leaves move by half a
spacing), +0.0002 node snap (`compare_selection_v2.txt`) — that *is* the honest floor.

*Tolerance and wording.* Keep 0.005. Paper text: "one expansion-loss term per lesion, a lesion being a local maximum
of diameter stenosis along the tree; FFR at the measurement node changes by ≤ 0.003 when centreline spacing is
halved with the healthy reference held (solver discretisation) and ≤ 0.004 when the reference is re-fitted". Delete
§8b's "~0.005 is the honest noise floor of a single baseline value" — it attributed a rule artefact to resampling.

## 3. Faithfulness to the review — **code faithful; documents are not**

| item | review | code (18:50) | verdict |
|---|---|---|---|
| leaf weight r_ref^2.66 | §1 | `zerod_ffr.py` `MURRAY_EXP = 2.66`, `w[leaves] = r_ref**MURRAY_EXP` | ✔ |
| truncation 0.60 mm on r_ref, leaky 0.50 | §3 | `R_TRUNC_DISCRETE = 0.60e-3`, `R_TRUNC = 0.50e-3`, applied to `r_ref` | ✔ |
| healthy-network gate ≥ 0.90 | §2 | `healthy_main_ffr()` = nanmin healthy FFR over `resolved & MAIN` | ✔ defined; **applied nowhere** — `run()` is leaky-only, no discrete run path, no gate call, no exclusion log |
| calibration guard | §5.2 | `calibrate()` computes q_max at C = 1e-30 and raises if ≤ demand; raises on the review's 400 mm vessel; q_max equals analytic (P_in − P_v)/R_epi to 4 s.f. (`physics_probe.txt` A, A2) | ✔ |
| zero-outlet guard | §5.4 | raises on a 0.55 mm vessel (`physics_probe.txt` B) | ✔ |
| ≥ 2 outlets for T1/T2 and Protocol C | §2 | not implemented (Phase 1 code) | open, expected |

**Contradictions to fix before anything is frozen** (line numbers as of 17:24 spec / 16:22 plan):
1. `CFD-ARM-SPEC.md` §2.4 **heading (51) "truncation at 0.75 mm"**, body (54) 0.60, §10 (161) 0.75;
   `STUDY-PLAN-v2.md` 245 "0.75 mm"; `zerod_ffr.py` docstring line 66 "truncation 0.75 mm". Code is 0.60.
2. `CFD-ARM-SPEC.md` **53: R_i = C′/r_ref,i³** vs 62: leaf r_ref^2.66. The 3D side must impose one exponent.
3. `CFD-ARM-SPEC.md` **§8 (151): "tabulated against the 0D values 0.919 / 0.693 / 0.427"** — those are the *leaky*
   self-test numbers (`python zerod_ffr.py` prints exactly them). The Stage A cases are discrete single-outlet at
   1.5 mL/s and `expected_0D.csv` says **0.946 / 0.754 / 0.485**; `START-HERE.md` has the right numbers. The CFD
   operator reads the spec.
4. `CFD-ARM-SPEC.md` §3 "42 such instances among the 150": under the 18:50 state, both-structure 0.70–0.90 window
   = **61**; after the healthy gate + ≥ 2 outlets + a downstream bifurcation on the host path = **38** (RCA 21,
   LCX 11, **LAD 6**) (`discrete_cohort_v2.txt`). "10 per vessel" is unreachable for the LAD; pre-register the
   real count and its derivation.
5. `E0-PREVALENCE-NOTE.md`: self-test values (line 12) are v2's; verdict line "22 trees in 0.70–0.90" is now **20**
   (4 in 0.75–0.85, 2 ≤ 0.80 unchanged; `REGEN-2026-09-18.log`). Verdict unchanged, numbers not.
`expected_0D.csv` is reproduced bit-identically by the code (`stageA_probe.py`); Stage A lesions are 10 mm and get
one K term under either rule (`physics_probe.txt` D) — unaffected.

## 4. Independent physics / numerics review (assuming nothing)

- **Picard** (`_solve`): secant linearisation g = 1/(R + K|Q|), damping 0.5, stop when max|Qn − Q| ≤ 1e-8·max|Qn|
  (tested against the damped iterate — fine at a fixed point; undamped Qn is kept on exit). 80 %DS/20 mm: 28
  iterations; tightening to 1e-13 changes pressures by 4.5e-12 of P_in (`physics_probe.txt` F). Sound. Minor: the
  criterion is relative to the tree's largest flow, so tiny branches converge only absolutely — irrelevant for FFR.
- **Expansion loss** K = ρK_t/(2A0²)(A0/As − 1)², ΔP = K Q|Q|, K_t = 1.52: Young–Tsai with U0 = Q/A0, A0 from r_fit.
  Correct. Viscous term = integrated Poiseuille on actual radius instead of Young's K_v (a stated modelling choice).
  Application at multiple lesions: was the defect of §2; now one term per local maximum — correct intent, and V3b
  guards it.
- **r_ref vs r_fit**: r_fit for %DS, A0, `resolved`; r_ref for truncation, bed weights and the healthy-equivalent
  epicardial resistance. Consistent. **The healthy solve uses r_ref**, which is ≤ r_fit and can be < actual r where
  the fit rises along a path (1.15× parent cap, monotone accumulate). The "healthy" network is then slightly narrower
  than the real vessel there, C is calibrated slightly low, and diseased inflow can exceed demand. **This is the
  explanation of the inflow > demand rows** (57 of 1,920 across modes, max +2.88 %; murray × 1.0: 10 rows, max
  +0.33 %): 837_left inflow with K = 0 on the actual radius is 1.0034 × demand while the healthy solve is 1.0000;
  39–57 % of active nodes have r > r_ref; the largest shortfalls (124_right −2.66 %, no lesions) are the mirror image
  (`physics_probe.txt` E). Acceptable — FFR is a pressure ratio and the target is met to 3 % — but report it as
  "inflow within ±3 % of demand on lesion-free trees" so a reviewer does not discover inflow > demand.
- **Poiseuille discretisation** (mean of endpoint radii then r⁻⁴): Jensen bias 0.02 % of window resistance at native
  spacing; the ≤ 0.003 residual in V8a is the true floor.
- **Robust taper / cap / monotone accumulate**: fine. `max(fit, 0.5·median)` can flatten a segment's reference — no
  consequence found.
- **Discrete bed docstring** ("telescopes to the leaky subtree total"): true only for exponent 3; with 2.66 it does
  not. Harmless (C absorbs scale); soften the comment.
- **Calibration guard numerics**: at C = 1e-30 the bed conductance is ~1e20 and `mass_err` is meaningless (3e13), but
  only `inflow` is used and it equals the analytic value; fine.

## 5. What would embarrass the paper at review

1. **Discrete-arm N is not 150 and its bands are not 25 each** (`discrete_cohort_v2.txt`, 18:50 selection): 36 of
   108 trees fail the healthy gate (50 instances), 5 single-outlet, 40 without a downstream bifurcation on the host
   path; **eligible 97; with a branch to delete 77**. Discrete − leaky FFR_meas: mean −0.073, SD 0.086, min −0.333;
   28/150 decision disagreements; only **48 of 150 stay in the band they were selected into**. Pre-register: bands
   defined *per structure* by that structure's own baseline; discrete N = 97 (77 for T1); no "25 per band" under
   discrete. `run()` (`severity_sweep.py`) turns guard exceptions into "FAIL" lines — ineligible trees must be logged
   as exclusions with reasons, as slot rejections already are.
2. **Statistical unit**: 32 of 150 instances are 16 host lesions at two severities; 15 scans contribute both trees.
   `(1 | case)` must be patient (scan) with tree and slot nested, or N is overstated.
3. **Band × length × severity confounding is structural**: [0.90,0.95) is 19/6 L = 10/20 and 40–55 %DS;
   [0.65,0.70) is 11/14 and 70–80 %DS (`compare_selection_v2.txt`). The T3 effect is therefore not separable from
   band; say so and analyse T3 within band.
4. **Eligibility bias**: host r_fit ≥ 1.0 mm rejects 740/944 slots; host trees have inlet radius median 1.47 mm vs
   1.39 cohort-wide; loc 104/46 prox/mid; quality 4 is 59 % of instances vs 60 % of hosts (fine). The cohort is the
   cohort's larger, proximal vessels with 20 mm of run-off — report as a limitation, not a footnote.
5. **T1 strata**: no downstream bifurcation on the host path in 32 (leaky) / 40 (discrete) instances; upstream
   on-path bifurcation exists in only 37. Report strata sizes; "no branch to delete" is not a zero effect.
6. **Reproducibility**: freeze the instance list with a hash (§1).
7. **Documents**: three truncation radii and two exponents across frozen texts; wrong Stage A targets in the spec (§3).

## 6. What is fine and can be stated with confidence

E0 verdict stands (20 / 4 / 2 — "add the sweep"); the loader and solver refactors were numerically inert (bit-identical
sweep under the old rule); calibration and zero-outlet guards behave as specified; the discrete bed is exactly the
reviewed configuration; `expected_0D.csv` is reproducible; the 18:50 verification suite passes on both beds and both
scan sets with V8a ≤ 0.0030 and V10 = 0.

## 7. Ordered actions before the full-scale run (18:50 state)

1. **Freeze the cohort as a hashed instance list** from `results/sweep_test_selected.csv` (18:50) and cite the hash in
   the pre-registration; rewrite `SEVERITY-SWEEP-SPEC.md` §8b–8d from `REGEN-2026-09-18.log` (incl. the corrected
   V8 wording and the V3b check).
2. **Add the discrete arm to the pipeline** before pre-registering it: evaluate the frozen slots under
   `bed="discrete"`, apply `healthy_main_ffr() ≥ 0.90` and ≥ 2 outlets with logged exclusion reasons; pre-register
   discrete N (97 / 77), per-structure band definition, and T1 strata sizes.
3. **Reconcile the documents**: CFD-ARM-SPEC §2.4 heading, line 53 exponent, §3 eligible count (38, LAD 6), §8 Stage A
   values, §10 truncation; STUDY-PLAN-v2 line 245; `zerod_ffr.py` docstring line 66; E0-PREVALENCE-NOTE counts.
4. **Statistics plan**: patient-level random effect with nested tree/slot; declare the 16 doubled slots and the
   band × length confounding; state the ±3 % inflow-vs-demand tolerance.
5. Then lock the pre-registration and run.
