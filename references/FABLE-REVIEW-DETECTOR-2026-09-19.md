# Independent adversarial review — `protocol/DETECTOR-SPEC.md` v0.1 (C3 / H5)

**Reviewer:** Claude Fable 5.1, 2026-09-19. **Target:** DETECTOR-SPEC v0.1 (2026-09-19), read against
STATISTICS-PLAN v1.0, CFD-ARM-SPEC v0.2, STUDY-PLAN-v2 §E5/§4/§9, and `code/{zerod_ffr,ablation,error_types,severity_sweep}.py`.
**Probes:** `FABLE-REVIEW-DETECTOR-2026-09-19-probe/` — `probe_s1_qnorm.py` (9 cohort instances × 2 beds, Protocol C
reproduced from `ablation.py:156–170`), `probe_s1_decomp.py`, `probe_s2_prior.py` (all 108 cohort trees × 2 beds).
Outputs `s1_stats.csv`, `s1_profiles.csv`, `s1_decomp.csv`, `s2_prior_data.csv`, `s2_prior.log`. Nothing written to
`results/` or `protocol/`; no existing file modified; the full ablation was not run.

---

## Verdict: **DO-NOT-RUN**

Do not lodge §3–§4 or implement §7 as written. Four of the spec's load-bearing claims fail against the code and the
numbers, and one of the probes exposed a defect in `ablation.py` itself that contaminates the positive class and P2's
headline number:

1. **S1 is not ≈ 1 in clean trees, is not "free", and does not step distal to a deleted branch.** In a healthy
   uncorrupted tree, max |ln q_norm| along the host path is 0.02–1.46 (leaky) and 0.54–2.04 (discrete) — q_norm
   ranges over a factor of up to 7.7 with no lesion and no error. Algebraically, q_norm(v) is an exact function of
   (r_ref profile, the model's own pressure solution, C): it is the identity §9 rejects for E5 statistic 1, one step
   removed. Under Protocol C **as coded**, deleting a branch changes ln q_norm distal to the branch by 0.00 ± 0.07 and
   *lowers* it proximally by 0.10–0.63 — the opposite sign and the opposite side from §3. Crude probe-set AUCs for
   S1_max / S1_step / S1_range against physiology negatives: 0.23–0.56 in both beds (chance).
2. **The mechanism in §2 is not the experiment the code runs.** `ablation.py:130–135` sets each territory's target to
   the clean flow of the *surviving* nodes only; the deleted branch's perfusion is dropped from the target. The
   remaining vessels are therefore asked to carry exactly what they carried before — not "the missing branch's flow
   through the vessels that remain" (§2, lines 40–43). Every T1 C_ratio is > 1 (1.04–1.41), not < 1 as §2 implies. This
   is also a contradiction between `ablation.py` and STATISTICS-PLAN §P2 line 97 ("total bed outflow of each subtree")
   that must be resolved before registration, in either direction.
3. **The S2 prior is degenerate.** On all 108 trees, ln C is explained by ln r_ref(root) and ln Σw alone with
   R² = 0.9997 (leaky, σ_resid = 0.0076) and 0.991 (discrete, σ = 0.071); the coefficients are the closed form
   C ≈ (P_in − P_v)·Σw / (K·r_root³) (fitted −3.02/+1.03 vs theory −3/+1). The two other covariates add nothing
   (VIF 18–20 in the discrete bed, corr(ln Σw, ln n_out) = 0.972). With σ = 0.0076, a ±20 % cardiac-output
   perturbation — a *negative* — scores S2_z ≈ ±24–29, and T1 scores 6–31. The prior as specified flags every real
   patient.
4. **S3_conc is bounded in [1, 1.414] on 104/108 (leaky) and 99/103 (discrete) trees**, because n_territories = 2 in
   almost every tree; for the physiological negatives it is 0/0 (residual = 0.0000 to machine precision when CO is
   perturbed). Probe AUC 0.30–0.45.
5. **`ablation.py`'s Protocol C minimiser can land in the wrong basin.** For scan 341 / RCA / leaky / T1 the loss on
   log C is bimodal: global minimum at C_ratio = 1.00 (residual 0.004, FFR_meas 0.675, ΔFFR ≈ 0) and a local minimum at
   C_ratio = 0.08 (residual 0.050, FFR_meas 0.158, ΔFFR = −0.52). `minimize_scalar(method="bounded")`
   (`ablation.py:167–168`) returned the local one. That row would be recorded as *passes its check and is materially
   wrong* — a positive for H5 and an absorption count for P2 — when the correct answer is *passes and is not wrong*.
   1 of 16 T1 Protocol-C fits in the probe; T2 rows with C_ratio 9.3 and 33.3 (the latter at the search bound) look
   like the same pathology. **This is a DO-NOT-RUN on the ablation itself, independent of the detector.**

The negative class (§4) is also not constructible from existing code (no Monte Carlo exists; HR has no handle in a
steady model; Hct is a module constant), and as described it is degenerate: a truth-side CO or MAP perturbation is
absorbed exactly by the single scaling, so "residual > 0.001" alone separates the classes (probe AUC 0.82–0.90) — a
perfect detector that means nothing at deployment.

What survives: the *idea* that only C and the residual vector carry non-anatomical information at deployment is
correct — and it is precisely why S1 cannot work. The 3D probe change (§8) is harmless to blinding but its
justification is false: none of §3's statistics uses the 40 pressure planes.

---

## 1. S1 — calibre–flow consistency: not free, not ≈ 1, wrong sign

### 1.1 The algebra (why it cannot be "genuinely free")

`_solve` (`zerod_ffr.py:217, 228, 235`) is a resistive network with bed conductance g(u) = w(u)/C at every node. By
mass conservation the flow entering node v is the bed outflow of its subtree:

    Q(v) = Σ_{u ∈ sub(v)} w(u)·(P(u) − P_v) / C

so, with π(u) = (P(u) − P_v)/(P_in − P_v),

    q_norm(v) = Q(v) / (K r_ref(v)³) = [(P_in − P_v)/(C K)] · Σ_{u ∈ sub(v)} w(u) π(u) / r_ref(v)³

w is a function of r_ref only (`zerod_ffr.py:128–132` leaky, `:144` discrete); π is the model's own pressure
solution — i.e. the FFR pullback the pipeline already reports; C is S2. **S1 is (anatomy) × (the model's pressure
output) ÷ C, exactly.** Spec line 65 ("telescopes … so the flow a vessel carries is its subtree's r_ref³ demand") holds
only if (a) π ≡ 1 (no pressure drop — false with a lesion, and false by up to 22 % in healthy discrete trees, min
healthy main-vessel FFR 0.78), (b) the max(·,0) in w never binds (false: at most left-main bifurcations the daughters'
r_ref³ exceed the parent's — spec line 46 itself relies on this binding), and (c) in the discrete bed at all — there w
lives only at leaves with exponent 2.66 and interior Q(v)/r_ref(v)³ is the leaf-weight share of the subtree, not 1.

§9 deviation 1 (lines 244–250) rejects E5 statistic 1 because "the pressure profile *is* the solution of the
resistance distribution — comparing one against the other is an identity". The same sentence applies to S1 with
"flow" in place of "pressure": Q is the other half of the same solution.

### 1.2 The numbers (`s1_stats.csv`; 9 instances × 2 beds; 3 LAD, 3 LCx, 3 RCA; all with a deletable branch)

| bed | case | S1_max median [min, max] | S1_step (node) median | S1_range median |
|---|---|---|---|---|
| leaky | healthy, **no lesion** | 0.56 [0.02, 1.46] | 0.47 | 0.56 |
| leaky | clean + lesion | 0.94 [0.41, 1.86] | 0.47 | 0.56 |
| leaky | T1 under Protocol C | 0.98 [0.32, 1.75] | 0.27 | 0.34 |
| leaky | physiology negatives (4 kinds) | 0.84–1.07 | 0.47 | 0.56 |
| discrete | healthy, **no lesion** | 0.95 [0.54, 2.04] | 0.58 | 0.90 |
| discrete | clean + lesion | 0.93 [0.39, 2.08] | 0.58 | 0.91 |
| discrete | T1 under Protocol C | 0.84 [0.58, 1.99] | 0.40 | 0.88 |
| discrete | physiology negatives | 0.88–1.07 | 0.58 | 0.91 |

- **Clean q_norm is not ≈ 1.** Healthy, lesion-free trees already have |ln q_norm| up to 1.46 (leaky) / 2.04
  (discrete) on the host path, and node-to-node SD of ln q_norm 0.08–0.25 (leaky) / 0.15–0.62 (discrete). In the
  leaky bed q_norm *falls* along a tapering run (median ln q at the last resolved node −0.56): a run that enters with
  a Murray deficit α < 1 (from an upstream binding bifurcation) leaks r_ref³ differences regardless of what enters, so
  q_norm(last) ≈ 1 − (1 − α)(r_prox/r_last)³. In the discrete bed q_norm *rises* along a run (Q constant, r_ref³
  tapering; median +0.41). Neither is "≈ 1 by construction"; both are bed-structure artefacts of exactly the kind
  §2 says the detector should see through.
- **S1 is not blind to disease (spec line 79–81).** Adding the cohort lesion raises S1_max from 0.56 to 0.94 (leaky)
  — the increment is ≈ |ln FFR_clean| (0.37–0.42 for these instances). Since positives are defined by |ΔFFR| > 0.05,
  which scales with lesion resistance, S1_max is severity-confounded across classes.
- **S1_max is a level statistic, not a shape statistic.** Spec line 81–82 claims S1 is "unchanged by the global tuning
  parameter to first order … what it sees is the shape, not the level". S1_max = max |ln q_norm| moves one-for-one
  with ln C: the CO ±20 % negatives shift S1_max by ∓0.2 in every tree (C_ratio 0.83 / 1.25).
- **The T1 signature has the wrong sign and location.** At the deleted junction J (`s1_stats.csv`, columns
  `dlnq_prox_of_branch` / `dlnq_dist_of_branch`, corrupted minus clean at the same nodes):

  | scan | bed | branch r (mm) | Δ ln q proximal of J | Δ ln q distal of J | step across J, clean | step across J, T1 |
  |---|---|---|---|---|---|---|
  | 306 LAD | leaky / discrete | 1.07 | −0.63 / −0.44 | +0.10 / +0.10 | −0.78 / −0.59 | −0.05 / −0.05 |
  | 661 LAD | leaky / discrete | 0.83 | −0.38 / −0.58 | +0.07 / +0.09 | −0.77 / −0.99 | −0.31 / −0.31 |
  | 196 LCx | leaky / discrete | 0.83 | −0.34 / −0.41 | 0.00 / 0.00 | −0.47 / −0.55 | −0.13 / −0.13 |
  | 42 RCA | leaky / discrete | 0.96 | −0.57 / −0.38 | 0.00 / 0.00 | −0.62 / −0.43 | −0.05 / −0.05 |

  Distal to the loss nothing happens (0.00 ± 0.07 across all 16 runs); proximal to it q_norm *drops* by the branch's
  share of flow. And the **clean tree already has a large negative step at every bifurcation** (−0.78 … +0.09 here),
  because Q drops by the daughter's flow while the host's r_ref is refitted per segment — deletion *removes* a step
  rather than creating one. A detector with no same-tree clean profile cannot tell "a bifurcation with a small step"
  from "a run with no bifurcation".
- **Crude AUCs on the probe set** (8 T1-positives vs 36 physiology negatives, per bed): S1_max 0.52 / 0.52,
  S1_step 0.26 / 0.36, S1_step_5mm 0.35 / 0.41, S1_range 0.23 / 0.55 (leaky / discrete). n is small; the direction
  is not ambiguous.
- **T4 is not "no mechanism" (spec line 169–171).** T4 scales r_ref by 0.93 (r_ref³ by 0.80) from the shoulder distally
  and Protocol C restores the surviving flows, so q_norm should rise ×1.24 distal to the shoulder by the spec's own
  logic. It does: T4 S1_range 0.27–0.79 leaky, 0.53–1.01 discrete. The pre-registered expectation is contradicted by
  the model's arithmetic — but it is moot because the clean spread is as large.

### 1.3 Where the information actually is

The only quantity that changes when a branch is deleted and that a deployed pipeline can compute without a clean
model is **anatomical**: the orphan weight at the junction, (r_J³ − Σ_children r_c³)/r_J³ — the very quantity the
leaky bed uses to re-insert the branch (`zerod_ffr.py:132`). In the probe it moves from −1.17 → −0.05 (306),
−1.15 → −0.37 (661), −0.64 → −0.14 (196), −1.06 → −0.05 (42) at J, against a null of the same statistic at every other
resolved host-path junction with p95 = 0.006–0.049. That is a *segmentation-plausibility* check (a vessel that narrows
sharply without giving off a branch), not a signature of *tuning* — which is the honest statement of what a
deployment-time check can and cannot see in this model, and the paper should say so rather than claim a flow
statistic that reduces to it.

## 2. S2 — the prior is near-deterministic and its σ excludes the negatives' only source of variance

`s2_prior.log`, all 108 cohort trees, both beds, OLS of ln C on [1, ln r_root, ln Σw, ln n_out, ln L_resolved]:

| bed | SD ln C | R² (4 cov.) | σ_resid | R² (r_root, Σw only) | β(ln r_root), β(ln Σw) | VIF Σw / n_out |
|---|---|---|---|---|---|---|
| leaky | 0.435 | **0.9997** | **0.0076** | 0.9997 | −3.02, +1.03 | 7.3 / 3.2 |
| discrete | 0.738 | 0.9912 | 0.0708 | 0.9899 | −3.28, +1.14 | **20.4 / 18.2** |

- `calibrate()` (`zerod_ffr.py:244–270`) sets inflow = K r_root³ on the healthy network. With healthy epicardial drop
  small, inflow = (P_in − P_v)·Σw/C, so **C = (P_in − P_v)·Σw/(K r_root³) up to the healthy pressure factor**. The
  regression recovers this closed form; the residual is the healthy epicardial drop (leaky: healthy main-vessel min
  FFR 0.92–0.99 → σ 0.008; discrete: 0.78–0.99 → σ 0.07). ln n_outlets and ln L_resolved are inert (β 0.005, −0.014
  leaky) and, in the discrete bed, ln Σw and ln n_out are the same variable (corr 0.972; every leaf sits near the
  0.60 mm cut so Σw ≈ n_out·0.6^2.66).
- **Implied S2_z** (leaky σ): T1 ln C_ratio = 0.01–0.34 (median 0.10) → z = 2–45; a ±20 % CO perturbation (negative)
  → z = ±24–29; the discrete bed gives z ≈ 1.4 (T1 median) vs 2.6 (CO ±20 %). Either the z-scores explode for
  everyone (leaky) or the negatives out-score the positives (discrete). The prior fitted on nominal-physiology clean
  models (spec line 89–90) contains none of the variance the negative class is made of.
- The honest S2 is: `ln C_tuned − ln C_closed(corrupted anatomy)`, with σ taken from the **training-split negatives**
  (clean anatomy, perturbed physiology). Its discriminating power for T1 is then ln C_ratio(T1) ≈ 0.10 against the CO
  SD (≈ 0.15–0.20 if Tanade's SD is 15–20 %) — Cohen's d ≈ 0.5–0.7, AUC ≈ 0.64–0.69. **H5's 0.80 threshold is
  arithmetically out of reach for the error type that supplies ≥ 85 % of the positives (§3 below).** Whether that
  is registered as the expected inverted finding or the threshold is revised is the operator's call, but it must be
  computed and written down before registration, not discovered.
- Note also that under the coded targets (§1, finding 2) T1's C_ratio is > 1 in every run. If P2's targets are
  changed to full-territory perfusion, the sign flips and the magnitude changes; S2's expected effect size must be
  recomputed after that decision.

## 3. Labels — positives exist; negatives do not, and are degenerate as described

**Positive class size.** In the smoke test (`results/ablation_smoke.csv`, 6 instances, band 0.65–0.70, 80 %DS, LAD):
Protocol C rows that pass residual < 0.10: 18/19 leaky, 10/18 discrete; of those |ΔFFR| > 0.05: **2 leaky, 1 discrete**
(T1 ×2, T2 ×1). T1 existed in only 1/6 instances. In the probe (instances *selected* for a deletable branch): T1
passes in 12/16 rows, all 12 materially wrong (|ΔFFR| 0.08–0.18) — minus the scan-341 wrong-basin row (§5), 11/15.
T2 fails the check in 10/11 rows (residual 0.11–0.68); T4 passes in the leaky bed but is material only in the 3 RCA
rows (−0.05 … −0.10), and fails the check in the discrete bed (residual 0.25–0.55); T3 is never material
(|ΔFFR| ≤ 0.02). Availability: 118/150 cohort instances have a downstream bifurcation on the host path (leaky);
77/97 discrete-eligible have a deletable branch (`discrete_arm_eligibility.csv`). **Expect ≈ 55–85 positives per
bed, ≥ 85 % of them T1; a 1/3 held-out split gives ≈ 20–28.** Testable, with DeLong CI half-width ≈ 0.10–0.12 at
AUC 0.8 — but the "mandatory per-error-type ROC" (line 171) will have ≤ 10 positives for T2 and ≤ 5 for T3/T4 and is
descriptive only.

**The unclassified middle.** A Protocol C run that passes and is *not* materially wrong (T3 always; T4 leaky mostly;
T1 when the leaky re-insertion self-heals, e.g. 341 at the correct optimum) is neither positive nor negative under
§4. A run that *fails* the check is neither. The spec must say what happens to both (excluded with a logged reason,
presumably) — otherwise the class definition is incomplete and a reviewer will ask why ~40 % of Protocol C rows
vanished.

**Negatives are not constructible today.** `grep -i "tanade|hematocrit|monte"` over `code/` returns nothing; there is
no Monte Carlo. Handles that exist: CO → `demand(scale=)` (`zerod_ffr.py:241–242`); MAP → `P_in` argument; Hct →
`MU` is a module constant (`zerod_ffr.py:30`), not a parameter; **HR has no handle at all in a steady model.**
STATISTICS-PLAN §6's Monte Carlo is *specified*, not implemented, and the spec's "already pre-specified" (line 135)
elides that.

**Negatives are degenerate as described.** The spec does not say whether the perturbation enters on the truth side
(targets) or the model side (inputs). Either way, a global CO change is absorbed *exactly* by the single scaling:
probe residual = 0.0000 in all 18 CO runs, S3_conc = 0/0, and S1 identical to the clean profile up to the C shift.
MAP ±10 mmHg and μ +15 % leave residuals of 0.0004–0.024. So `residual > 0.001` alone separates positives from these
negatives (probe AUC 0.90 leaky / 0.82 discrete) — the detector would be "does the check pass *too* well", which is
not a deployable statistic and not what H5 claims. The negatives need a perturbation the single parameter **cannot**
absorb: per-territory demand heterogeneity (territory-level CO share noise), and measurement noise on the targets at
the test–retest repeatability that VALIDATED_RESIDUAL = 0.10 is itself derived from (`ablation.py:45–53`). That
design also makes the 10 % check meaningful for the first time: at present a clean model matches its targets to 1e-9.

## 4. S3 — bounded and uninformative on this cohort

Territories are the children of the first branching node (`ablation.py:65–83`). On the 108 cohort trees:
n_territories = 2 in 104 (leaky) / 99 (discrete), 3 in 4 / 4, 0 in 0 / 5. With n = 2, max|ρ|/rms(ρ) ∈ [1, 1.414]
identically; the probe values are 1.00–1.26 for T1 and 1.00–1.66 (n = 3 trees) for negatives, AUC 0.30–0.45. Under
CO-perturbed negatives it is 0/0. §9 deviation 2 correctly abandons the whiteness test for a 2-element series; it
then defines a statistic that is equally uninformative on a 2-element series. The signed vector ρ (line 113) is worth
recording; S3_conc is not worth pre-registering.

## 5. `ablation.py` Protocol C minimiser — wrong-basin convergence (affects P2, not only H5)

Scan 341 / right / RCA / leaky / T1, loss = mean((pred − target)/target)² on log C, scanned at 31 points over the
`ablation.py:167` bounds (`probe` output, this review):

| log10(C/C_clean) | residual | FFR_meas |
|---|---|---|
| −1.20 | 0.094 | 0.141 |
| **−1.10** | **0.050** | **0.158** ← returned by `minimize_scalar(bounded)` (C_ratio 0.077, ΔFFR −0.52) |
| −0.50 | 0.298 | 0.355 |
| **0.00** | **0.004** | **0.675** ← global minimum (ΔFFR −0.001) |
| +0.20 | 0.223 | 0.800 |

Two basins: as C → small the flows become epicardially limited and the *ratio* of territory flows happens to match
the target ratio again. Brent's bounded method is a local method and started at the wrong side. The recorded row
(residual 0.047 < 0.10, |ΔFFR| = 0.52) would count as **absorbed and materially wrong** in P2's headline proportion
and as an H5 positive, when the true fit is "self-healed, not wrong". T2 rows with C_ratio 9.3 and 33.3 (the latter
exactly at the +1.5 decade bound; `ablation_smoke.csv` also has 10.1) are suspect for the same reason. Fix before any
ablation run: coarse log-grid scan (e.g. 61 points over ±1.5 decades) → Brent refinement in the best bracket; record
the number of local minima, the loss at C_start, and whether the optimum sits at a bound; treat a bound hit as a
failed fit, logged. STATISTICS-PLAN §9 ("non-converged solves are failures") should name this case explicitly.

## 6. The 3D probe change (§7.2 / §8) against CFD-ARM-SPEC §11–§13

- **Blinding (§13): no leak.** `r_ref_mm` per station is anatomical (taper fit), already present per outlet in
  `outlets.csv` (§11 line 201); the lesion position is already in `meta.json`/`mask_edit.json` because the CFD side
  builds the lesion. Nothing in `probes.csv` is a 0D *prediction*. It must stay that way: the 0D-side pullback file
  (§7.2: `ffr, Q_mls, q_norm`) must never ship in the package — say so in §8.
- **The justification is false.** Line 220–222: "Without intermediate stations the 3D campaign returns data that
  cannot test C3 at 3D fidelity." S1 needs Q(station) and r_ref: Q at any station is the sum of downstream outlet
  flows, which §12 already returns; S2 needs the derived R_i / C′, already returned; S3 needs outlet flows. **None of
  §3's statistics uses a pressure plane.** The 40 planes serve a pullback *pressure* profile — the E5 statistic 1 that
  §9 abandons — and the mechanism figure. Keep them (they are cheap) but state what they are for.
- **"Post-processing only, sampling method unchanged" is optimistic.** `postProcess -func surfaces` with
  `cuttingPlane` cuts the entire domain: on a tortuous RCA or an LAD with parallel diagonals a plane at station k
  also slices other vessels, and a naive area-average is wrong. With 4 probes this is checked by eye; with
  ~40 × 1,260 it is not. §8 must specify the clipping rule (keep the connected cut component containing the
  centreline point, within a sphere of ~2·r_ref) and a QA column (cut area vs π r_local²). A `bifurcation` station
  is ill-defined for a single plane — sample ≥ 1 diameter proximal and distal instead. Add the through-plane flow
  integral ∫U·n dA per station: it is free, it is the 3D Q(station) directly, and it checks mass balance against
  the outlet sums.
- **Station count** on the 9 probe paths with a 5 mm grid + 5 anchors + bifurcations: 19–41; the 40 cap binds on
  RCA paths (path length 153–176 mm). Fine as specified.
- **Real tier:** q_norm at 3D must use the r_ref of the 0D twin rebuilt from as-meshed radii (§6.1b), not the
  pre-mesh `r_ref_mm` in `probes.csv`. Say which.

## 7. Other contradictions and post-hoc exposures

- §7.2 `Q_mls` at the vessel-origin station: for right trees the origin is the root, and `evaluate()` returns
  Q[0] = 0 (`zerod_ffr.py:236`; inflow is in `info`). As written the pullback file would carry q_norm = 0 → ln = −∞.
- §7.1 `run_id` has no value for the **clean** run, and `ablation.py` writes no clean row at all (clean fields are
  copied into every corrupted row). The negative class and the clean pullback need their own rows.
- §2's pre-registered expectation "S1 and the combined detector perform better under the discrete bed" has no
  support in the probe (chance in both) and rests on the §2 mechanism that the code does not implement.
- §5 negatives at "1,000 draws per instance" (STATISTICS-PLAN §6) against ≈ 60 positives is a 1,000:1 imbalance with
  within-instance correlation; DeLong's variance assumes independent negatives. Pre-specify one draw per instance
  per ROC (or a cluster-robust variance), and the patient-level split (§5) already handles the rest.
- §3 combined: logistic regression on 4 inputs with ≈ 40 training positives is at the edge of the 10-events-per-
  variable rule; with S1 and S3 removed it is comfortably inside it.
- §1 last row / line 30 rule is honoured by S2 and by the residual vector; it is not honoured *in spirit* by any
  statistic that is a deterministic function of the same solve — which is what S1 is (§1.1).

---

## Required changes

**MUST (blocking — the spec cannot be lodged or implemented without these)**

1. **Resolve the Protocol C target definition** between `ablation.py:130–135` (surviving-node clean flows) and
   STATISTICS-PLAN §P2 line 97 (total territory perfusion), decide which experiment the paper runs, and rewrite
   DETECTOR-SPEC §2 to describe that experiment. The sign of C_ratio under T1, the S2 effect size and the entire §2
   mechanism depend on it.
2. **Fix the Protocol C minimiser** (`ablation.py:167–168`): global grid scan on log C, then local refinement; log
   the number of basins, the loss at C_start, and bound hits as failed fits. Re-run the smoke test and report how
   many rows change. This blocks the ablation, not only the detector.
3. **Drop S1 as specified.** It is an exact function of (r_ref, the model's pressure output, C) — the identity §9
   deviation 1 already rejects — and it is not ≈ 1, not shape-only, not blind to disease, and at chance on the probe.
   If a calibre statistic is kept, it must be anatomy-only (the junction orphan weight, §1.3) and be described as a
   segmentation-plausibility check, not a signature of tuning.
4. **Respecify S2**: `ln C_tuned − ln[(P_in − P_v)·Σw/(K·r_root³)]` (or the two-covariate OLS), with σ estimated on
   the **training-split negatives**, never on nominal clean models. Drop ln n_outlets and ln L_resolved. State the
   expected effect size for T1 against the physiological SD before registration.
5. **Drop S3_conc** (bounded in [1, √2] on 2-territory trees, 0/0 for exactly-absorbed negatives). Record the signed
   ρ vector; if a residual-pattern statistic is wanted, pre-specify it only for n_territories ≥ 3 and count how many
   instances that is (4/108 trees).
6. **Specify the negative class constructively**: which parameters are perturbed, on which side (truth vs model),
   with which SDs (cite Tanade's numbers in the spec), and with at least one component the single scaling cannot
   absorb (per-territory demand share noise and/or target measurement noise at the test–retest SD). State that the
   Monte Carlo is *not yet implemented* and list the code changes (parameterise `MU`; HR has no handle — say so).
7. **Complete the label definition**: what happens to Protocol C runs that pass and are not material, and to runs
   that fail the check. Excluded with a logged reason and counted in the CONSORT flow, or assigned — but decided now.
8. **Correct §8's justification** for the 3D stations (none of §3's statistics needs a pressure plane; Q(station) is
   the downstream outlet sum already returned by §12), specify the plane-clipping rule and the QA column, replace
   `bifurcation` stations with ±1-diameter offsets, and state that the 0D pullback file (`ffr, Q_mls, q_norm`) never
   ships in the package.
9. **§7.2 implementation details**: use `info["inflow"]` for the root station; add a clean row per (instance, bed)
   with its own `run_id`; add the negative-class rows.

**SHOULD**

10. Pre-register the expected positive count per bed and per error type (≈ 55–85, ≥ 85 % T1; T2/T3/T4 ≤ 10 each) and
    state that per-type ROCs for T2–T4 are descriptive. Reconsider whether the primary H5 ROC is T1-only.
11. Pre-compute and write down the expected AUC for S2 on T1 from ln C_ratio vs the physiological SD; if it is < 0.80,
    either register the inverted finding as the *expected* outcome or revise the H5 threshold before lodging — not
    after.
12. Pre-specify one negative draw per instance per ROC replicate (or cluster-robust DeLong), and the number of
    replicates.
13. Add the through-plane flow integral to the 3D return set and use it as the 3D Q(station).
14. Remove the pre-registered "discrete > leaky" expectation for S1 (§2) or re-derive it under the corrected target
    definition.
15. Reproduce this review's probe numbers protocol-grade (as CFD-ARM-SPEC §10 does for the earlier review) before
    freezing.

**CONSIDER**

16. Reframe C3 honestly: in a model whose bed is a deterministic function of r_ref and whose output *is* the pressure
    field, the only non-anatomical deployment-time information is (C, ρ). "The tuned parameter and the residual
    vector carry [no / a weak] signature of absorbed anatomy, and only an anatomical plausibility check does" is a
    cleaner and more defensible contribution than a flow statistic that a reviewer can reduce to an identity in one
    line — and it answers attack 7 better than the current text.
17. The junction orphan-weight statistic (§1.3) has a clean null (p95 0.006–0.049 at non-deleted junctions) and a
    large signal (0.5–1.1 at deleted ones). It is also computable on the raw mask before any model is built — which is
    both its strength and the reason it belongs in a segmentation-QA paper as much as in this one.
18. Target measurement noise at the test–retest SD makes VALIDATED_RESIDUAL = 0.10 an operating characteristic
    rather than an arbitrary constant; that reads well against the [CITATION REQUIRED] flag.

---

*Probe caveats: 9 instances chosen for a deletable branch (3 per vessel), not the frozen cohort; AUCs on 8 vs 36 are
directional only; physiology perturbations were applied truth-side with model at nominal; Tanade's SDs were not
looked up (±20 % CO used as a placeholder). None of these caveats changes the algebra in §1.1, the closed form in §2,
the territory count in §4, or the bimodal loss in §5.*
