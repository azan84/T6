# Paper 6 / T6 — Study Plan v2 (quality-first, deadline-unbound)

> ## DECISION 2026-10-03 — submit a reduced paper to the JBHI special issue before 15 October 2026
>
> **Decided by the corresponding author.** This reverses §11's "regular JBHI later is preferred" for this paper.
> - **Content:** C1 + C2 at 0D (error model and the three-protocol ablation on the frozen cohort, both beds, against
>   the noise floor), plus scan 14 as a 3D **case study**, not a replication. H4 and H5 are stated as registered and
>   pending (`drafts/registration-2026-10-03/PRE-LODGING-ADDENDUM-2026-10-03.md` §A5). The detector (C3) and E6 are
>   out of this submission.
> - **If desk-rejected:** finish the full 3D batch and go to another journal with the full CFD arm (TMI or MedIA,
>   per §11's upgrade path). If it is rejected after review, the same applies, with the reviews used.
> - **Length: do enough, within 8 pages** (the over-length charge threshold). Anything not needed for C2 stays out.
> - **No promise of a follow-up (operator, 2026-10-03).** Paper 1 states only the fact: H4 and H5 are registered and
>   their results are not part of this report. Neither the text nor the cover letter says they will be reported
>   separately, because that is not confirmed.
> - **During review:** CFD work continues. If reviewers ask for 3D results, they go into the revision (2-month window).
>   If the paper is accepted without them, whether the remaining work (H4, the radius-definition gap, H5, H7) becomes a
>   second paper is decided then, citing paper 1 and the same registration.
> - **Order:** lodge the OSF registration → run the ablation (not before) → write → co-author sign-off → submit by
>   2026-10-14. CFD work continues in parallel under `cfd_handover/WORK-ORDER-2026-10-03.md`.
> - **CFP verified 2026-10-03** on embs.org: deadline 15 October 2026. Guest editors include M. Colombo and S. Celi.
>   JBHI: IEEE double-column; 8 pages before over-length charges ($250/page for pp. 9–10, $350 beyond); 14 pages
>   max including supplementary; abstract ≤ 250 words with no abbreviations; single-blind review.
> - **Submission blocker still open:** ICMJE criterion 2 for Mohd Azan and Ming Kwang Tan. Send them the draft for
>   critical revision, not sign-off, and record what they change.
>
> ---
>
> ## RESUME HERE — state at 2026-09-26 (CFD report v3 read; supersedes the 2026-09-19 banner below where they differ)
>
> **`STAGE-A-VALIDATION (3).pdf` (65 pp.) was checked on 2026-09-26. The response is `cfd_handover/WORK-ORDER-2026-09-26.md`.**
>
> - **U₃D = 0.00055. This is a PASS under the pre-registered contingency** (`STATISTICS-PLAN` "PRE-REGISTERED CONTINGENCY on the 3D
>   discretisation floor"). It comes from a systematic 50/25/12.5 µm throat family plus a shifted zone and a 2D wedge. H4 runs as
>   specified. U₃D is the uncertainty of the *finest* solution: the 50 µm level is 0.003 above it and the 25 µm level 0.0008.
>   **Production recipe fixed at the 25 µm throat zone** (WO 09-26 D1). Report the 0.0008 production offset beside U₃D.
> - **Gate M1 (scan 14): PASS WITH DEVIATIONS, conditional** (WO 09-26 D6). The mask-to-solution path is scripted with no manual
>   repair, all solves converge, and prescribing all outlets at once is stable with round trips ≤ 0.005 %. Deviations: the throat gate is
>   relative, not absolute (D2), self-intersections come from the mask (D3), and strict checkMesh failures are localised (D4). The pass
>   becomes full when the clean case's round trip and the as-meshed radii reach Drive. **The M1 kill risk in §10 is retired.**
> - **The finding that matters for the paper: a radius-definition gap between the 0D and 3D lesions.** The as-meshed throat
>   (area-equivalent 0.2756 mm) is larger than the package target (0.2306 mm), about 43 % more area. The 3D lesion is therefore
>   milder than the 0D lesion, and baseline 3D delivers +15–16 % to the lesioned territory. This is the scan-837 finding again
>   (3D area-equivalent radius 23–44 % above the 0D EDT radius). It enters flow demand through r³ as well as resistance through r⁻⁴.
>   **Rule: every 3D-vs-0D comparison (H4, E3) uses a 0D twin rebuilt on the as-meshed radius (`code/ingest_cfd_radius.py`), with
>   both the area-equivalent and the inscribed variants reported.** Without this, H4 confounds radius definition with fidelity.
>   The same bias also belongs in the paper's limitations for the primary 0D arm: the cohort 0D radii are EDT-based. Check whether
>   `STATISTICS-PLAN` §10 already lists it before lodging the registration.
> - **Not a finding (our package design):** the clean-tree "+33 % / 17× path resistance" in report §11.8. `clean_nolesion` carries the
>   lesioned tree's boundary conditions (byte-identical bc_A/bc_C to baseline). Corrected in WO 09-26 E1. The T1 README's
>   "reconstructs clean pressures" line is wrong for T1 under B1; the erratum is WO 09-26 E2 (the packages are hash-locked, so they are not edited).
> - **Measured real-lumen cost is about 13× the CFD-ARM-SPEC §4 estimate:** ≈ 2.2 h, 16 ranks and 6 GB per 3.5–3.9 M-cell steady
>   solve. The re-cut real tier (≈ 400 solves) would take **≈ 40 machine-days**, not 5–6. WO 09-26 Task B collects the data to cut this
>   (settle-iteration stopping, 2×8 vs 1×16 layout, a portable setup for the other PCs). **Re-size the batch analysis-side
>   after Task B returns.** Options if it stays large: stop on convergence, spread over several PCs, drop the polyball tier to 10
>   instances (already planned), and shrink the real tier's error-type × protocol grid to the cells H4 actually tests.
> - **Score re-scored 2026-09-26: 68.0 → 75.0** (N6 E8 Ev8 V8 F8 I7 C8; `../research-pipeline/PRIOR-ART-VERDICTS.md`). Validation 8 assumes
>   the registration is lodged before the ablation runs. Otherwise the score is 73.5.
> - **Still blocking on the CFD side: Task 0.** Nothing has reached Drive (`returns/` holds only the templates, and there is no `code_from_cfd/`).
> - **Unchanged on the analysis side:** the pre-registration is **not lodged yet** (checklist §5). The ablation must not run before it is lodged.
>   Authors: **five** (Ming Kwang Tan added 2026-09-19, `PREREGISTRATION-CHECKLIST` §5). The "four authors" line in the 09-19
>   banner below is superseded. Frozen-file manifest re-verified 2026-09-26: 15/15 OK.
>
> ---
>
> ## RESUME HERE — state at 2026-09-19, ~01:30
>
> **Three defects were found in the PRIMARY experiment overnight. One is fixed; two are decisions only you can make.
> Do not lodge the pre-registration until B1 and B2 below are settled.** The 2026-09-18 banner said "everything is
> built and verified" — that was true of the cohort and the pipeline, and false of the ablation's Protocol C.
>
> ### B1, B2, B3 — SETTLED 2026-09-19, applied and verified
>
> All three were defects in the primary experiment. Each fix was verified on the 6-instance smoke set against the
> pre-fix run (`results/ablation_smoke_B1B2B3-2026-09-19.csv` vs `..._POSTFIX-...csv`).
>
> **B1 — Protocol C targets the clean tree's FULL territory outflow**, including the share of a branch the error
> deleted. `ablation.py` was summing only the **surviving** nodes' clean flow — a validation target contaminated by
> the very error it validates against, and one no clinic could produce without already knowing which branch was
> missed. The target represents what perfusion imaging measures *in the patient*, and the patient's myocardium is
> perfused whether or not the segmentation saw the vessel feeding it. This is `STATISTICS-PLAN` §P2 as written; the
> code, not the plan, was wrong.
> **Effect (n = 1 — read this before quoting it):** on the single smoke instance that has a deletable branch
> (scan 306; 5 of 6 smoke instances have none), T1's `C_ratio` flips from **1.049 → 0.928** — the bed must draw
> harder through fewer vessels, which is the thesis mechanism. The residual roughly doubles (0.048 → 0.097) because
> one global parameter can no longer hit the harder target, and it still passes the 10 % check while the FFR is wrong
> by 0.078. **That is the absorption finding in miniature, and it is one instance, not a result.** It sits *just*
> under the threshold, which makes `VALIDATED_RESIDUAL = 0.10`'s missing citation more consequential, not less.
>
> **The cost of B1, which is not small:** Protocol C needs ≥ 2 clean territories with surviving members to stay
> over-determined, and that guard now fires on **40 % of T1 rows and 33 % of T2 rows, overwhelmingly RCA** — 99 of
> 100 T2 × RCA rows have no surviving territory at all. **The tuned-protocol arm is effectively a left-coronary
> result for the topological error types.** Written up in `STATISTICS-PLAN` §9; it must not surface as unexplained
> missing cells in a vessel-stratified table.
>
> **B2 — `T2_KEEP_BEYOND` raised 15 mm → 25 mm** (= `RUNOFF` + 5 mm), so the measurement node is interior with a
> margin, as `error_types.py` always claimed it was. **Effect: `meas_same_point` goes from 0/36 to 36/36 T2 rows.**
> Every previous T2 number under Protocol A was reading a closed outlet — a wall — rather than a computed pressure.
> The two constants live in different modules and nothing connected them, so `ablation.py` now **asserts
> `T2_KEEP_BEYOND > RUNOFF` at import**: the contradiction cannot silently return.
> **Attrition cost, measured cohort-wide: none — T2 stays applicable to 100 % of instances in both beds.**
> Leaky 150/150, discrete 148/148 (2 slots ineligible under the discrete bed for unrelated reasons). Run-off still
> deleted: median **71.1 mm** leaky / **66.7 mm** discrete, and even the **worst decile still loses 39 / 34 mm**.
> The stricter constant costs nothing and T2 remains a substantial error.
> Two probes derived this independently and agree (`references/B2B3-EVIDENCE-2026-09-19/`): one measuring residual
> path length beyond the cut, one re-running T2's own applicability test.
>
> **B3 — a calibre-only error may no longer change which vessels are modelled.** `Tree` gained a `trunc_ref`
> parameter that pins the active node set, by coordinate, to the clean tree for T3 and T4. (Scaling the truncation
> radius by 0.930 was tried first and is only an approximation — `r_ref` is a robust taper fit made monotone and
> parent-capped, so it is not proportional to `r`; it is retained as a harmless pre-filter.) A fixed cut deleted
> leaves that T4 had merely shrunk, which is a modelling artefact: T4 says the lumen was read 7 % narrow, and those
> vessels still exist. **Effect: T4 × Protocol A in the discrete bed goes from ΔFFR +0.173 with 3 flips to −0.033
> with 0 flips** — the sign corrected, and now agreeing in direction with the leaky bed (−0.047).
> **`STATISTICS-PLAN` §P3's "6 flips leaky vs 43 discrete" was this artefact and has been withdrawn.**
> **Cohort-wide the defect was far worse than the 30-instance subset suggested:** under the old fixed cut, T4's 0.93
> scaling pushed **489 of 655 discrete outlets (75 %)** below the truncation radius, and **56 of 148 instances lost
> every outlet they had** — those trees cannot even be built (`no outlet survives truncation`). T4 in the discrete
> bed was not merely mis-signed, it was **unusable for roughly a third of the cohort**.
>
> (An earlier version of this banner credited B1 with rescuing a skipped smoke row and taking 113/124 to 114/124.
> That was wrong: **B3** rescued it — scan 335 / discrete / T4 / Protocol C. B1's own guard *removes* Protocol C
> from a third of the topological rows, as above. Corrected after independent audit.)
>
> ### Fixed overnight, needs your sign-off
>
> **Protocol C's minimiser was returning the wrong basin.** The loss is bimodal in log C; `minimize_scalar(bounded)`
> is a local method. On scan 341/RCA/leaky/T1 it returned C_ratio 0.077, ΔFFR **−0.52**, residual 0.050 — which would
> have been recorded as *"passes its validation check and is materially wrong"*: **a false absorption count in P2's
> headline number and a false positive for H5.** The true optimum is C_ratio 1.00, ΔFFR ≈ 0. Now a 61-point global
> grid scan → Brent refinement, with `fit_n_basins` / `fit_at_bound` recorded and a bound hit treated as a failed fit.
> Verified on scan 341 (`fit_n_basins = 2`, returns C_ratio 0.994). **Smoke re-run: 0 of 38 Protocol C rows changed,
> no multi-basin fits, no bound hits** — the pathology is simply not in the 6-instance smoke set, so *the smoke test
> would never have caught this*. That is the case for keeping the fit diagnostics on every row of the full run. The
> one extreme pre-fix value (scan 335, C_ratio 10.1) was checked and is **genuine**, not the bug, and it fails the
> 10 % check anyway. How many of the 150 instances are affected is unknown until the full run; scan 341 proves the
> rate is not zero.
>
> ### C3 (the detector) was designed, reviewed, and largely rebuilt
>
> `protocol/DETECTOR-SPEC.md` v0.2. v0.1 was returned **DO-NOT-RUN**: three of its four statistics were dead on
> arrival, for one reason — **in this model the bed is a deterministic function of `r_ref` and the output *is* the
> pressure field, so any flow statistic is (anatomy) × (the model's own solution) ÷ C.** The only deployment-time
> information is the tuned parameter `C`, the residual vector, and **the anatomy itself**.
> **The consequence you need to weigh: H5's AUC > 0.80 is arithmetically out of reach on the tuning side** (≈ 0.65 for
> T1, which supplies ≥ 85 % of positives). The honest lead is the *anatomical* check — a vessel that loses calibre
> without giving off a branch — which needs no haemodynamic model at all. Decide before registration whether to
> register the inverted finding as expected or to re-base H5 on the combined score.
>
> ### Shipped to the CFD machine
>
> **Gate M1's three packages are in `cfd_handover/packages/M1/` and are ready to run** (scan 14, left LAD, 80 %DS:
> clean lumen · lesion · missed branch). An independent pre-flight cleared **Stage A + M1 to start today** and
> confirmed Stage A's acceptance numbers are **not** stale (`expected_0D.csv` regenerates byte-identical against
> today's code). They are unaffected by B1–B3: M1's criterion is whether an edited mask meshes and converges without
> manual repair, not what the boundary values are.
>
> **But the 12-day study batch must NOT be launched as specified — about 40 % of it produces nothing usable.**
> Only 407 of 510 solves per tier have a 0D counterpart; T2 has no Protocol A or C cell on any RCA (single-outlet
> stump); T1 × C is missing on 7/30; T4 in the discrete bed is B3's artefact; and 240 resting-state solves exist for
> a Fossan constraint the 0D model **declares unimplemented**. Re-cut, the useful batch is **≈ 5–6 machine-days**,
> not 12. Stage D (pulsatile, 3 days) is unspecified and its mechanism figure is already produced by the steady
> solves — re-specify it as a steady-vs-cycle-mean check, or cut it.
>
> ### The registration is ready to lodge
>
> **All four blocking items are closed as of 2026-09-19:**
> 1. **B1, B2, B3** — settled, applied, independently audited, smoke re-run (§ above).
> 2. **`VALIDATED_RESIDUAL = 0.10`** — citation resolved. The value stands; the *justification* was wrong (a
>    within-subject CoV used as an agreement bound; they differ by ~2.8×). Because this residual compares a
>    deterministic model against **one** noisy measurement, the correct 95 % bound is ≈ 0.13–0.16, so **0.10 is
>    stricter than required and therefore conservative for H2**. `references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md`.
> 3. **Quality matching** — decided: register the design as-is (§E1).
> 4. **`STATISTICS-PLAN` §13** — re-specified for model-vs-official anatomy, with the "no injection" clause withdrawn
>    (E0 leaves 2 trees ≤ 0.80, so that flip table would be empty) and its own two-tree eligibility rule.
>
> **Also added before lodging, deliberately:** §P4's **pre-registered contingency for H4** against the 3D mesh
> discretisation figure U₃D, which the CFD machine is measuring now. Stage A showed FFR still moving ~0.0047 per
> refinement through 1.9 M cells, so a bad number is a live possibility — and fixing the response *now* makes it a
> reported result instead of a post-hoc deviation.
>
> **THEN, in order:** lodge the pre-registration → run the ablation (12 minutes) → S_A characterisation → analysis.
> The CFD machine runs Stage A Task 1 and Gate M1 independently throughout.
>
> **AUTHORSHIP SETTLED 2026-09-19 — nothing scientific now blocks the registration.** Four authors in order:
> Fadillah Yamin · Mohd Azan Mohammed Sapardi · Xin Wang · Mohd-Zulhilmi Paiz Ismadi (**corresponding**). Every
> author holds a CRediT block. What remains is mechanical: deposit the code for a DOI, attach the two frozen cohorts
> and the manifest, re-verify the manifest, and lodge. See `protocol/PREREGISTRATION-CHECKLIST.md` §5.
>
> *(Superseded, kept for the decision log:)* **BLOCKING the pre-registration (small, unchanged):**
> 1. Fadillah Yamin's **ORCID and email** (affiliation recorded as Monash Malaysia Mech Eng, per the lead author).
> 2. Byline form of **Mohamad Azan**'s name — the contacts file has "Mohd Azan Mohammed Sapardi".
> 3. **Corresponding author** — decide deliberately; see §7b.
> Author order is fixed: Fadillah Yamin · Mohamad Azan · Xin Wang · Mohd-Zulhilmi Ismadi.
>
> **THEN, in order:**
> 1. Lodge the pre-registration — `protocol/PREREGISTRATION-CHECKLIST.md` maps every document to its OSF field.
>    Attach `COHORT-FROZEN-2026-09-18.csv`, `CFD-SUBSET-FROZEN-2026-09-18.csv`, `.sha256`, `STATISTICS-PLAN.md`.
>    (Code DOI deferred to pre-submission, per the operator.)
> 2. **Run the ablation** — `python code/ablation.py <data_root>` (~10 min, 150 instances × 2 beds × 4 error types ×
>    3 protocols). **Do not run it before the registration is lodged** — that is the one hard ordering constraint.
> 3. Analyse per `protocol/STATISTICS-PLAN.md` P1–P5. Then write.
>
> **NOT YET BUILT — the third contribution.** The detector (C3) does not exist. Design it *before* the ablation runs,
> or the ablation must be repeated to record what it needs. Known constraint: Protocol C tunes to territory-perfusion
> targets, so the residual *at those targets* is near zero by construction — the detector must use something that was
> **not** tuned on (pullback pressure profile at intermediate nodes; tuned-parameter plausibility against a
> population prior).
>
> **TWO OPEN CITATIONS, both flagged in place:** `VALIDATED_RESIDUAL = 0.10` (test-retest repeatability of
> per-territory MBF — the paper's headline threshold, currently UNVERIFIED in `ablation.py` and `STATISTICS-PLAN.md`
> §P2); and Pfaller 2022 / Collet 2019, cited from outside the corpus.
>
> **RUNNING IN PARALLEL, needs nothing from this machine:** CFD Stage A (`cfd_handover/START-HERE.md`, 16-core
> machine — install, generate geometry, run checks A1–A5; the resistance BC is UNTESTED and A3 is its acceptance
> test); ASOCA terms (Gate D2, unverified, the detector's external validation depends on it); clinical-anchor
> outreach (E6, longest lead time in the project).
>
> **RESOLVED — the paired masks were declined (Gate D1b closed, 2026-09-18), and the reply carried something better:
> an offer of CAS-Net / nnU-Net predictions against the official labels, now Gate D1c, accepted 2026-09-19.**
> It also carried a caveat that cost us a claim: the published inter-observer statistics are an *upper bound on
> agreement* (both annotators edited the same auto-generated centrelines), and separately, **Betti error is β₀ + β₁
> and cannot see a missed side branch at all** — so C1's "measured topological disagreement rate" is withdrawn and
> T1's magnitude is now a declared design choice. See §1 C1, §9 attack 3, `protocol/NEXT-PLAN-2026-09-19.md`.
>
> *(Superseded note, kept for the decision log:)* Registering without them was
> decided — the amendment is pre-specified in `STATISTICS-PLAN.md` §13 as hypothesis H7.


**Written 2026-09-18.** Supersedes `STUDY-PLAN.md` on design and schedule; that file is retained as the decision log
(its §2, §9, §10 record how this version was reached). Gate evidence lives in `references/N1-SEARCH-LOG.md`.

**Governing decision (operator, 2026-09-18):** *"Don't worry about time. Even if we miss the CFP, we will submit it
still. Focus on making the paper strong, novel and impactful."* Every choice below follows from that. The JBHI
special-issue date (2026-10-15) is now an **opportunity**, not a constraint — see §11.

---

## 0. Thesis

**Error absorbed at calibration is error committed at deployment.**

A reduced-order coronary FFR model can be re-tuned after a segmentation error so that it matches its outlet
pressure/flow validation targets exactly — and still flip the FFR ≤ 0.80 revascularisation decision for individual
patients. Overlap metrics hide topological segmentation error at the imaging stage (ImageCAS-X: *"topological errors
such as vessel breaks are present in all model predictions despite high DSC and clDice"*); boundary-condition tuning
hides it again at the haemodynamic stage. This paper measures the second concealment, shows it is invisible to
aggregate validation, and gives a test that exposes it from outputs the pipeline already computes.

**Title (working):** *Matched at the outlet, wrong in the tree: boundary-condition tuning conceals topological
segmentation error in reduced-order coronary FFR, and a deployment-time test that exposes it*

## 1. Contributions — three, each defensible against the closest prior work

> **FRAMING DECISION, 2026-09-19 — the paper leads with C2 as a single thesis, not with three co-equal
> contributions.** The table below still describes what is being attempted and stays as the work plan. What changed
> is how it will be *written*, and the reason is that after this week's corrections C1 and C3 are both narrower than
> the table implies:
>
> - **C2 is intact and strong** — the controlled ablation at the decision threshold, pre-registered in both
>   directions, under two boundary-condition structures, against a physiological-noise floor. Nobody has run it.
> - **C1 is narrower:** T1 and T2 have no measured magnitude and are declared design choices, the quality-matching
>   claim was false and is withdrawn, and the Betti-based topological claim is withdrawn because β₀ + β₁ cannot see
>   a missed side branch. What survives — magnitudes that are demonstrable **floors** — is defensible, and smaller.
> - **C3 will probably not clear its own threshold.** H5 asks for AUC > 0.80; the tuning-side statistic is ≈ 0.65 by
>   construction, because in this model every flow statistic reduces to anatomy × the model's own pressure solution.
>
> **Three contributions of which two are soft reads as overreach, and a reviewer who catches one overclaim discounts
> the rest — including C2, which does not deserve it.** So the paper argues one thesis: *tuning to perfusion targets
> conceals topological segmentation error at the decision threshold, and the concealment is not recoverable from the
> tuning.* C1 becomes the method that makes the ablation credible. **C3's likely failure becomes a finding with a
> clinical implication** — the tuned parameter carries only a weak signature while the anatomy carries a strong one,
> so deployment-time QA should check anatomy rather than fit quality. That is citable, honest, and stronger than a
> third contribution that lands at AUC 0.65.
>
> Two things to foreground rather than bury, because reviewers respect declared scope and punish discovered scope:
> the **pre-registration** (few CFD papers have one, and §6's decision log is what makes it credible rather than
> decorative), and the **RCA scope limit** — the tuned-protocol arm is effectively a left-coronary result for the
> topological error types (`STATISTICS-PLAN` §9).
>
> **Structural rule that follows: the 3D arm must not become load-bearing.** C2 has to stand on the 0D result alone,
> with 3D as corroboration, so that if the cross-fidelity arm fails — M1 is blocked at meshing, and mesh convergence
> is not yet demonstrated — the paper is complete with a declared limitation rather than holed. §P4's contingency
> enforces this on the statistics side.

| # | Contribution | Closest prior work and why it stops short |
|---|---|---|
| **C1** | **Real-disagreement-driven, topology-explicit error model.** Four error types (two topological) with exact 0D and 3D definitions, magnitudes calibrated to *measured inter-observer* disagreement from 160 blind re-annotations (ImageCAS-X), including a **topological** disagreement rate (Betti number error 0.2 ± 0.4). If the paired masks are obtained (§6, Gate D1b): the two humans' actual segmentations are run directly — nothing injected | All four Sankaran/HeartFlow papers: one random variable per section, *"fixed bifurcation locations,"* assumed magnitudes. Fernández-Martínez 2024: single global HU threshold, magnitudes borrowed from other cohorts. Colebank 2019: algorithm-parameter resampling, no taxonomy. Sankaran 2016: real data but inter-*modality* |
| **C2** | **The three-protocol ablation, at the decision threshold.** Fixed / re-derived / target-matched boundary conditions crossed with error types; outcome is **per-case reclassification across 0.80**, reported as P(flip \| baseline-FFR band) against a physiological-noise floor; **replicated at 3D fidelity**; and it **resolves the Gamage 2022 contradiction** as an explicit sub-study | Gosling 2020: mechanism shown, but unchanged geometry, cohort-averaged tuning, aggregate metrics only. Fossan 2025: AUC-flat/sensitivity-moves dissociation for a BC *model swap*, not geometric corruption. Tanade / Colebank / Korte / Sankaran 2016: geometry-vs-BC compared in four vascular settings — **none with a decision threshold**, none with a tuned-vs-untuned ablation |
| **C3** | **A deployment-time detector of concealed geometric error**, built only from outputs the pipeline already produces (pullback pressure profile at untuned nodes; tuned-parameter plausibility against a population prior), developed on a training split, tested on a held-out split, and **externally tested on a second public dataset** | Phillips 2024 supplies the system-identification principle (fit ≠ system capture) but no cardiovascular instance. No FFR-CT paper proposes any check that tuning has masked anatomy; Menon 2024 dials geometry *and* BCs to the same targets and calls it a feature |

**Pre-registered, both directions** (§4). If tuning *cannot* rescue topological error — the Tanade/Korte direction —
the inverted result is the paper: *anatomical fidelity is irreducible, and here is the test that tells you when
you've lost it.* Either outcome is publishable; only an unregistered one is not.

## 2. Novelty position — the one-paragraph version for the introduction

Five groups have compared the influence of geometry against outlet boundary conditions: HeartFlow across four papers
(coronary, lumen-radius only, bifurcations fixed), Tanade 2022 (coronary, physiological inputs only), Colebank 2019
(mouse pulmonary, 1D), Korte 2023 (intracranial aneurysm, 22 segmenters × 5 BC models), and Sankaran 2016 (coronary,
MLD > boundary resistance > viscosity). All report **continuous** sensitivity. None asks the question a cardiologist
asks: *did the decision change for this patient?* Gosling 2020 showed that re-tuning distal resistance absorbs a 65%
flow discrepancy without moving aggregate accuracy — and framed it as reassurance. Fossan 2025 showed that a BC model
swap leaves AUC untouched (0.845 vs 0.845) while sensitivity moves ten points. Gamage 2022 held resistance fixed,
found downstream branch loss shifts FFR 13–15%, and noted that a differently-tuned study concluded the opposite.
Nobody has run the controlled ablation. This paper does, at the threshold, with real disagreement, and with a remedy.

Full evidence and quotes: `references/N1-SEARCH-LOG.md` (11-row closest-works table).

## 3. Experiments

### E0 — Data, pipeline, and the prevalence check (foundations)

**Data (primary):** ImageCAS-X — 800 CCTA scans from ImageCAS (volumes: Kaggle, Apache 2.0; annotations: Zenodo
10.5281/zenodo.21887809, CC BY 4.0). Provides voxel lumen labels, coronary **centrelines**, **mesh surfaces**,
segment labels, and scan-level descriptors (dominance, image quality Likert 1–4, CHD status).

> **THE WHOLE COHORT SITS IN THE DATASET'S HELD-OUT TEST SPLIT — verified 2026-09-19, and worth stating up front.**
> ImageCAS-X ships its own split files (`filelist/`: train 560, val 80, test 160, exclude 200). Checked against the
> frozen cohort: **all 93 cohort patients are in `test.txt`; none in train, val or exclude.**
>
> Two consequences, and the second is the one for the paper:
> - It was not engineered — the cohort was selected on image quality and anatomy, and the sweep drew from the test
>   split because that is where the re-annotation statistics live. But it is true, and it is checkable in one line.
> - **Any benchmark model's predictions on our scans are genuinely out-of-sample.** That settles the training-overlap
>   question for the D1c arm for *any* of the published weights, not merely the benchmark run — so if that arm
>   proceeds, "the segmentation model never saw these scans" is a fact about the design rather than an assurance
>   from a correspondent. **State it in the methods**: declared, it reads as a design property; discovered by a
>   referee, it reads as luck.

**Data (external test for C3):** ASOCA (MICCAI 2020 coronary segmentation challenge; 40 CCTA, 20 healthy / 20
diseased, multi-expert annotation). **VERIFY** licence, access terms, and annotator count before relying on it —
recorded as Gate D2. Fallback: a held-out ImageCAS-X split only.

**Pipeline (0D):** ImageCAS-X centreline + radii → svZeroDSolver network: vessel segments (Poiseuille resistance +
inertance + compliance), stenosis elements (nonlinear pressure-drop block), junctions, RCR Windkessel outlets, aortic
inlet pressure waveform (population), hyperaemia by scaling distal resistance. **The centrelines and surfaces are
already supplied — this is a build of the network-construction and corruption code, not a segmentation pipeline.**
Deposited code, hashed protocol (P16/T13 discipline).

**Pipeline (3D):** ImageCAS-X surface → corruption at surface level (§E1) → repair (pymeshfix / VMTK; **this step
does not exist in any source in the corpus and must be built**) → cfMesh or snappyHexMesh → OpenFOAM
(Mao 2025 `CoronaryHemodynamics` as backbone; **VERIFY its licence** — unstated in the paper). Steady laminar for FFR;
pulsatile only for the mechanism figure (§E3).

**Prevalence check (fatal-if-late, run first):** ImageCAS-X is a *segmentation* dataset. Compute baseline 0D FFR on
the diseased-flagged scans and inspect the distribution in 0.65–0.95. **Decision rule:** if fewer than ~40 trees have
a lesion with baseline FFR in 0.70–0.90, add a **virtual-stenosis severity sweep** (controlled insertion at 40/50/60/
70/80% diameter at standardised locations) as a second cohort. With no deadline: **do both** — the natural cohort
gives realism, the sweep gives controlled density where flips happen.

### E1 — The error model (C1)

Four error types, each with an exact 0D operation and an exact 3D surface operation:

| Type | Class | 0D operation | 3D surface operation | Magnitude source |
|---|---|---|---|---|
| **T1 Missed side branch** | topological | Delete a branch subtree and its outlet; redistribute nothing (A), re-derive (B), or re-tune (C). **Stratify by location** (upstream / downstream of the index lesion) and by branch-to-parent diameter ratio (Gamage's < 1/3 rule as a hypothesis) | Clip branch at bifurcation, cap, repair | **NO MEASURED MAGNITUDE — a design choice, declared.** ImageCAS-X's Betti error (β₀+β₁) **cannot** measure a missed branch: deleting a side branch leaves the tree with the same number of components and no new loop, so it moves neither. The code deletes the **largest** eligible downstream branch in every instance (a 100 % event rate, not a rate drawn from data) — and the dataset's per-segment DSC-vs-diameter ρ = +0.89 suggests real disagreement concentrates in the **smallest** branches, i.e. the choice is not conservative in the obvious direction. Side-branch DSC 70.9–83.6 % indicates only *which* branches are plausibly missed |
| **T2 Vessel break / truncation** | topological | Terminate the vessel early; distal subtree lost | Cut and cap distally | ImageCAS-X's own "vessel breaks"; distal DSC decline ρ = −0.36 |
| **T3 Stenosis-length error** | calibre/extent | Lengthen or shorten the stenotic segment at fixed MLD | Axial stretch/compress of the lesion region | Fernández-Martínez ± length; HD95 2.46 ± 3.62 mm |
| **T4 Taper / undersizing** | calibre | Scale radius along a segment or the distal tree by factor *f* | Radial offset of surface | HD95, per-segment DSC vs diameter ρ = +0.89 |

**Dropped:** eccentric/off-axis lumen — it has no 0D representation. May reappear as a 3D-only supplementary once
the pipeline exists.

**Quality matching — NOT IMPLEMENTED. Corrected 2026-09-19; this paragraph previously claimed it was.**
The former text read: *"injected magnitudes are conditioned on the ImageCAS-X stratifiers that drove real
disagreement — image-quality Likert, vessel diameter, lumen attenuation, disease status."* **`error_types.py`
conditions on nothing.** All four magnitudes are fixed constants applied identically to every instance: T1 deletes the
largest eligible downstream branch, T2 truncates at a fixed 15 mm, T3 adds a fixed 2.46 mm, T4 scales by a fixed
0.930. Image quality, diameter, attenuation and disease status enter the analysis **as covariates and strata**
(`STATISTICS-PLAN` §5) — they do not modulate the injected magnitude.

This was a **registration-critical correction**: quality matching is a C1 contribution claim, and the experiment as
coded cannot support it.

> **DECIDED 2026-09-19 — option (a): register the design as-is.** Fixed magnitudes, applied uniformly, with severity,
> diameter and image-quality effects recovered *post hoc* from the covariates and strata already in
> `STATISTICS-PLAN` §5.
>
> **Why not implement conditioning.** It would mean choosing a functional form for each stratifier — how magnitude
> scales with Likert score, with diameter, with attenuation — and every one of those choices is an **unregistered
> researcher degree of freedom**, which is the precise thing a pre-registration exists to remove. It would be adding
> discretion to a pre-specified design in order to buy back one sentence.
>
> **And it would not repair the real gap: T1 and T2 have no measured magnitude to condition on.** Conditioning would
> dress up T3 and T4 while the two error types the paper actually turns on remained design choices.
>
> **What replaces the claim is stronger than the claim was.** The magnitudes that *are* derived from measurement are
> **floors** — the dataset's own authors state the published agreement is an upper bound, because both annotators
> edited the same automatically generated centrelines from a shared initialisation. "Our injected errors are
> conservative, and the dataset authors say so in print" is verifiable by a reviewer in a way "quality-matched" never
> was, and it converts §9 attack 3 from a defence into an offensive point.

The same false claim appears in §9 attack 3 and in the `error_types.py` header, both corrected.

**If Gate D1b passes (paired masks obtained):** add the **natural-experiment arm** — build the 0D (and 3D) model from
*both* annotators' segmentations of the same scan and run the full A/B/C on the pair. No injection. This is the
strongest possible form of C1 and removes the "your errors are unrealistic" objection entirely. The injection arm
remains for controlled dose–response.

### E2 — The three-protocol ablation (C2, primary experiment, 0D)

> **⚠ CORRECTIONS REQUIRED BEFORE PHASE 1 FREEZES THIS SECTION (independent review, 2026-09-18 —
> `references/FABLE-REVIEW-CFD-2026-09-18.md`):**
> **(1) Protocol C must be FLOW-matched only.** As written below it matches outlet flows *and* pressures. In a steady
> tree that is self-defeating: if the outlets distal to the lesion reproduce the baseline's pressure and flow, the distal
> pressure — hence FFR — is the baseline's by construction, and **no decision can flip**. The thesis ("matched at the
> outlet, wrong in the tree") holds only when the validation targets are flows / perfusion — which are also the only
> targets a clinic actually has (no one measures outlet pressure). State this in the paper as the definition of
> "validated", not as a caveat.
> **(2) BC structure is a pre-registered factor.** The leaky bed re-inserts a deleted branch as a point leak at its
> parent node (consequence of w(v) = max(r_ref(v)³ − Σ children r_ref³, 0)), damping the missed-branch error by
> construction: reviewer's probe, mean |ΔFFR| under A/B/C = 0.059/0.017/0.036 leaky vs 0.112/0.051/0.120 discrete.
> Run the ablation under **both** leaky and discrete-outlet beds; claim only what holds in both. How each protocol
> treats the orphaned bed weight when a branch is deleted must be specified per protocol (A: baseline weights frozen,
> no re-insertion; B: recomputed from the corrupted geometry; C: flow-matched).
> **(3) This is itself a finding worth a sentence in the paper:** distributed-leak models are partly self-healing
> against missed branches; discrete-outlet models are not.

For every case × error type × magnitude:

- **A — fixed:** outlet RCR values from the clean baseline, unchanged.
- **B — re-derived:** outlets recomputed from the corrupted geometry by the deployment rule (Murray's law / outlet
  cap-area scaling). This is what a real pipeline does to wrong anatomy.
- **C — target-matched:** outlets re-tuned so the corrupted model reproduces the **clean baseline's own outlet
  flows and pressures** (the only targets available without invasive data — stated up front, see §9 attack 2),
  under the **Fossan constraints** written as numbered rules: (1) re-simulate the resting state first; (2)
  severity-to-resistance constants stay population-level; (3) **more targets than free parameters** — tune one
  global resistance scaling and one compliance scaling against all outlet flows *and* pressures, never a per-outlet
  free fit to a single target (pre-empts "one equation, one unknown").

**Outcomes per run:** lesion FFR; flip indicator (crossed 0.80 vs baseline); outlet-target residual after tuning
(≈ 0 in C by construction — that number *is* the concealment); interior/lesion pressure error.

**Reported as:** P(flip | baseline band), bands fixed in advance at 0.70–0.75 / 0.75–0.80 / 0.80–0.85 / 0.85–0.90;
net reclassification per error type × protocol; the **"matched here, wrong there" panel** — outlet residual vs lesion
error, per protocol.

**Noise floor (Tanade confound):** a no-injection Monte Carlo over cardiac output, MAP, heart rate, haematocrit at
Tanade 2022's published SDs, plotted on the same P(flip | band) axes. Tanade reports 50% RCA / 25% LCA reclassification
at 1 SD of physiological input alone — every injected-error flip rate is read against that.

### E3 — Cross-fidelity replication and the mechanism figure (C2, 3D, concurrent PCs)

**What changed from v1:** the 3D arm no longer computes WSS/OSI (a plaque-vulnerability question this paper does not
ask; pulsatile at 24 h / 8 cores / case; OSI not implemented in any available backbone). It now answers **"does the
0D result survive at 3D fidelity?"** — which is reviewer 3's exact objection.

- **E3a Steady FFR replication:** as many cases as mesh cleanly (target 30–50), full A/B/C × T1–T4 subset. Steady
  laminar; ~minutes per run; ~3,000 core-hours total — days of wall-clock on the multi-PC pool.
- **Protocol C in 3D — tune in 0D, transfer, verify.** A 3D inner tuning loop is ~15 full solves per condition and
  is infeasible. The 0D-tuned Windkessel parameters are transferred to the 3D outlets (standard 0D–3D coupling, cf.
  Kumar 2023, Chi 2022 in corpus); 3D verifies, it does not tune. This also sharpens the comparison: identical
  parameters, two fidelities.
- **Concordance:** flip agreement 0D vs 3D (Cohen's κ), Bland–Altman on lesion FFR.
- **E3b Mechanism figure:** 5 cases, pulsatile, Protocol C — the spatial pressure and velocity field showing the
  outlets matched and the interior wrong. One figure; the title's second half.
- **Attrition budget:** FAME's 14.8% surface-failure floor (RCA 26.6%) applies to *uncorrupted* geometry; corrupted
  will be worse. Over-sample candidates by ~40%. Meshing failures are themselves data — report the failure rate per
  error type as a supplementary finding (nobody has).

### E4 — The Gamage resolution (C2 sub-study)

Replicate Gamage 2022's design in the cohort: downstream vs upstream branch removal, under **fixed** resistance
(Gamage's own protocol → large downstream effect, 13–15%) and under **re-tuned** resistance (the external study's
protocol → small effect). Show that both published conclusions are reproduced by the choice of protocol. A clean,
citable resolution of a live disagreement, and the natural opening of the paper.

### E5 — The detector (C3)

**Principle (Phillips 2024):** a model that fits its outputs has not necessarily captured the system. Test the fit
where it was *not* imposed.

**Candidate statistics — all computable at deployment, none using the tuning targets:**
1. **Pullback-profile residual:** the pressure profile along the vessel (intermediate 0D nodes; 3D centreline
   pullback) compared with the profile expected from the model's own resistance distribution — shape mismatch
   indicates redistributed flow. Relation to the pullback pressure gradient index (Collet 2019 — **VERIFY** before
   citing).
2. **Parameter plausibility:** Mahalanobis distance of the tuned RCR values from the population prior; absorption
   pushes parameters out of the physiological envelope.
3. **Residual structure:** whiteness/independence of the multi-target tuning residual series (Phillips' test).

**Development:** train/held-out split of ImageCAS-X cases; null distribution from the no-injection sweep; ROC with
DeLong CIs per statistic and combined. **External test:** ASOCA (Gate D2) with the same corruption model. Pre-specify
the operating point (e.g., sensitivity ≥ 0.8 at the deployment prior).

**Failure mode to state honestly:** if the only targets are at outlets and the model is a single-path 0D chain, the
pullback residual may be uninformative — the detector is expected to work on *branched* trees where redistribution
leaves a signature. Report where it fails.

### E6 — Clinical anchor (extension; highest-impact upgrade, longest dependency)

ImageCAS-X has no invasive FFR, so every finding is "error-induced change relative to a clean baseline." A small
cohort with CCTA + invasive FFR (even 20–30 lesions) converts it to **error-induced misdiagnosis against clinical
truth** — the difference between a methods paper and a clinical-translation paper. Route: Monash / IIUM clinical
partners; ethics and data-access dependent. **Not on the critical path; pursue in parallel from Phase 0.** If it
lands, it becomes the paper's final figure and moves the venue conversation (§11).

## 4. Pre-registered hypotheses (both directions; register on OSF before Phase 2)

| # | Hypothesis | Counter-hypothesis (equally publishable) |
|---|---|---|
| H1 | Topological errors (T1, T2) produce higher P(flip) than calibre errors (T3, T4) at matched disagreement magnitude | Calibre dominates (Sankaran 2016: MLD is the primary driver) |
| H2 | Protocol C drives outlet residual → 0 while P(flip) remains ≥ Protocol A — **absorption** | C reduces P(flip) as well — tuning **rescues** (Tanade/Korte direction) |
| H3 | Protocol B (re-derived) yields P(flip) ≥ A — deployment rules compound topological error | B ≈ A |
| H4 | 0D and 3D flip patterns concordant (κ > 0.6) | Discordant — 0D findings do not transfer |
| H5 | Detector AUC > 0.80 held-out and > 0.70 external | Detector fails — absorption leaves no deployment-time signature |
| H6 | Downstream-branch-loss effect is large under fixed and small under re-tuned resistance — both Gamage and its contradicting study are reproduced | Effect is protocol-independent |

## 5. Statistics plan (frozen with the protocol)

**`protocol/STATISTICS-PLAN.md` v1.0 is the source of truth and supersedes this section entirely.** Cite that
document in the registration, not this one.

> **Corrected 2026-09-19.** This section contradicted the statistics plan on four points and was written earlier:
> unit (*case × lesion* vs **instance**), random effect (`(1 | case)` vs **`(1 | scan/slot)` at patient level**),
> N (*100–160 trees* vs **150 instances / 108 trees / 93 patients**) and the detectable difference (*~10* vs
> **~12** percentage points). Rather than restate the plan here and risk drifting again, this section is now a
> pointer. Likewise **§E2's Protocol C description is superseded** by `CFD-ARM-SPEC` §2.3 and `ablation.py`:
> Protocol C is **flow-matched only**, never flow *and* pressure.

## 6. Gates (updated)

| Gate | Question | Status 2026-09-18 | Action |
|---|---|---|---|
| **N1** | Novelty | Provisional pass — 827 papers, 11 closest works read in full, Sankaran thicket (4 papers) resolved | **Run the ACQUIRE-T6 database strings** (Scopus/WoS/PubMed/arXiv) and close formally. Also run the `research-ideation` `pursue T6` flow — no longer waived, since there is no deadline |
| **D1** | ImageCAS-X on disk | Downloading 2026-09-18 — **stored OUTSIDE Google Drive at `~/Datasets/imagecas-x/`** (operator is low on Drive space; large data never goes in the synced tree). `Datasets/imagecas-x/README-LOCATION.txt` in the Drive folder is a pointer only | Verify MD5 `7994f098…`; unzip; confirm centrelines + surfaces + Descriptors.xlsx; record in `Datasets/DATA-STATUS.tsv` with the local path. Code takes the data root as an argument; only small result CSVs live in the project |
| **D1b** | Paired re-annotation masks | **CLOSED — DECLINED 2026-09-18.** Bransby will not release the second annotation set: the first was checked and corrected by a senior analyst and is the ground truth, the second was deliberately left unchecked so inter-observer variability would not be *under*estimated, and releasing it risks users treating the two as equivalent. A considered position — **do not re-ask.** The 2026-09-18 decision to register without this arm was therefore correct | **No in-house fallback either.** A second annotator starting from the same automatically generated centrelines would reproduce the same shared-initialisation problem; starting from raw images is a different and much larger study. Dropped deliberately, not by omission |
| **D1c** *(new, 2026-09-19)* | **Algorithmic prediction variability** — CAS-Net / nnU-Net predictions against the official ImageCAS-X labels, offered unprompted by Bransby in the same reply | **Reply SENT 2026-09-19** (`drafts/EMAIL-IMAGECAS-X-REPLY-2026-09-19.md`, `.docx` alongside). Four questions asked: scope, **raw vs post-processed output** (the benchmark filtered components < 100 voxels, which would delete exactly the topological events we count), which training weights (the 160 test scans must be held out), and terms/attribution. Plus an optional ask for the **pre-edit automatic centrelines**, which would give a measured topological *correction* rate that appears nowhere in the literature | Nudge once after ~3 weeks, then let it go. **Purpose is error-type APPORTIONMENT** — which errors a real segmentor actually makes — not inter-observer variability, and **not** a no-injection arm (E0 leaves only 2 trees ≤ 0.80, so that flip table would be empty). Off the critical path; the registration does not wait. **A SELF-SERVE FALLBACK EXISTS — see below.** |
| **D2** | External test set | **CHECKED 2026-09-19** (`references/GATE-D2-ASOCA-2026-09-19.md`): ASOCA is obtainable but **gated** (UK Data Service registration + data-owner permission), and **only the majority-vote label of three annotators is released** — individual masks are not, so ASOCA cannot supply inter-observer disagreement either. 40 cases; after our eligibility filters expect ~20–25 usable | Register with UKDS and request record 855916; ask explicitly whether **derived** results may be redeposited as Source Data. Do **not** cite CC BY 4.0 for the ASOCA data — that is the article's licence. Fallback = held-out ImageCAS-X split, which is a weaker claim and is labelled as such |

> ### D1c has a self-serve fallback — recorded 2026-09-19 so it is not rediscovered in three weeks
>
> **The Zenodo record we already use carries a second file we never downloaded: `pretrained_weights.zip`, 1.6 GB,
> containing the weights for all six coronary segmentation methods benchmarked in the ImageCAS-X paper.** Only
> `ImageCAS-X_dataset.zip` (1.4 GB) is on disk, MD5 `7994f098…` verified.
>
> So D1c does **not** strictly depend on a reply: the weights that generate the predictions we asked for are public,
> on the record we already cite. Two things this changes:
>
> - **It quietly answers question 3 of the email.** The published benchmark weights are the ones trained on the 560
>   training scans with the 160 test scans held out, so the contamination worry is resolved for those weights.
> - **It is not free.** Weights without images are useless and **we do not hold the ImageCAS CT volumes** — those are
>   on Kaggle, tens of GB, and would then need inference over 160 scans × up to six models. Bransby's offer skips the
>   images, the inference and the GPU entirely.
>
> **Decision: do not download the weights yet.** Wait for the reply; the arm is off the critical path. If he declines
> or goes quiet after the ~3-week nudge, this is the fallback, and it is a complete one rather than a workaround.
>
> **Licence, verified on the record itself rather than from a paper** — the trap the ASOCA check caught:
> *"Creative Commons Attribution 4.0 International"*, quoted verbatim, applying to the record's files.
> DOI 10.5281/zenodo.21887809, **v1, published 11 August 2026**. Cite the version, not just the concept DOI.
>
> ### Read from the authors' own code, 2026-09-19 — `github.com/kitbransby/ImageCAS-X` (MIT)
>
> Three things the repository settles that we had been planning to ask about or infer:
>
> 1. **The post-processing filter is `min_size = 100`** — connected components below **100 voxels** are discarded
>    (`postprocessing/steps.py`, verbatim: `min_size = self.params.get("min_size", 100)`). It is **not**
>    largest-component-only. So the filter removes exactly the small fragments and breaks D1c exists to count, and
>    question 2 of the email no longer needs an answer — only the *raw* output does.
> 2. **Betti error is defined as `|components(pred) − components(gt)|` and `|loops(pred) − loops(gt)|`.** This is the
>    authors' own metric code, and it **independently confirms why C1's topological claim was withdrawn**: a missed
>    side branch changes neither the component count nor the loop count. Verified, no longer inferred.
> 3. **The benchmark code is MIT-licensed**, so their evaluation metrics are reusable for a like-for-like comparison
>    if D1c proceeds.
>
> Together with the public weights, this makes the D1c fallback genuinely complete: MIT code, public weights, a split
> we already hold. The only missing input is the ImageCAS CT volumes (Kaggle).
| **T1** | Tools | svZeroDSolver confirmed BSD-3; OpenFOAM present | Install; record versions; verify Mao's package licence; allocate cores per PC to T6 vs WindTurbine/DataCentre |
| **M1** | 3D pipeline on broken geometry | Unrun | 3-case pilot **including one deliberately broken surface**, through repair → mesh → steady solve. Hard gate for E3; E3 is no longer on the critical path, so failure here delays, not kills |
| **E0** | Stenosis prevalence | **RUN 2026-09-18 — verdict: ADD THE SEVERITY SWEEP.** 160-scan test split, 320 trees, 0 failures (`results/E0_prevalence_test.csv`, note in `results/E0-PREVALENCE-NOTE.md`). Primary model (Murray demand): only **20** trees with main-vessel min-FFR in 0.70–0.90, **4** in the flip-prone 0.75–0.85 band, **2** ≤ 0.80. Anatomy explains it: tightest resolved main-vessel lesion is median **38 %DS**, p90 50 %, max 62 % — **zero lesions ≥ 70 %DS**. "Disease: yes" in ImageCAS-X means *any visible plaque*, not flow-limiting stenosis | **The virtual-stenosis severity sweep is now a required cohort, not a fallback.** Natural cohort = anatomical realism + measured inter-observer disagreement; sweep = controlled density around 0.80. **Second finding, on-theme and to be frozen in WP-0:** the count is highly sensitive to the flow-demand model — fixed territory flow puts **140** trees in 0.70–0.90 vs Murray's 20, because it forces normal-heart flow through this cohort's small vessels (median inlet radius 1.39 mm). The demand model must be chosen on principle and its sensitivity reported |

**Progress log**
- **2026-09-19 (~00:30–01:30, unattended) — C3 specified, two primary-experiment defects found, one fixed.**
  Two independent adversarial reviews were run before anything was executed at scale, and both earned their keep.
  **`DETECTOR-SPEC.md` v0.1 → DO-NOT-RUN → v0.2.** v0.1's flow statistic S1 was shown to be an exact function of
  (r_ref, the model's own pressure solution, C) — the same identity that killed §E5's original statistic — and
  empirically at chance (AUC 0.23–0.56), with the T1 signature on the **wrong side and the wrong sign**; its S2
  "prior" turned out to be the closed form C = (P_in−P_v)·Σw/(K·r_root³) at R² = 0.9997, scoring physiological
  *negatives* at z ≈ 24–29; its S3 was bounded in [1, √2] on the 104/108 trees that have two territories; and its
  negative class was not constructible from any existing code and was degenerate where it was. v0.2 keeps only what
  survives — the tuned parameter, the residual vector, and an **anatomical** plausibility check — and states plainly
  that **H5's 0.80 threshold is out of reach on the tuning side**.
  **`ablation.py` Protocol C minimiser fixed** (wrong basin; see the banner). **`export_cfd_case.py` written**, reviewed
  (GO-WITH-CHANGES, MUST 1–8), rewritten, and re-verified; among the eight was a **§13 blinding violation** — the
  manifest carried `ffr_discrete` — and a mask-deletion rule that shredded the branch into 67 islands, which would
  have failed Gate M1 for the rule rather than for the lumen. `CFD-ARM-SPEC` §10/§11/§17 updated to match.
  A third review verified the rewrite before anything was sent, and returned **DO-NOT-SEND** on two more: the shipped
  deletion rule used 26-connectivity, which walks the lumen's surface shell and eroded the *retained* LAD by 1,298
  voxels (against ~770 of real branch); and every inlet normal was 32° off because the root has no parent and the
  tangent helper fell through to its (0,0,1) placeholder. Both fixed, plus three smaller defects the rewrite had
  introduced — named probe stations being silently dropped when a grid point fell within 1 mm of them, `prescribed`
  boundary conditions with a zero flow target (a divide-by-zero on the CFD side), and a blinding guard whose regex
  would have passed the real `expected_0D.json`. Re-verified by executing the shipped rule verbatim on the real
  mask: erosion 1,298 → 40 voxels, connected components preserved 2 → 2.
  **Gate M1's three packages are generated and ready** in `cfd_handover/packages/M1/`.
  **Nothing was run at scale and the ablation was not started.**
- **2026-09-18 (evening) — cohort FROZEN, statistics plan drafted, pre-flight passed.** An independent pre-flight
  review (`references/FABLE-PREFLIGHT-2026-09-18.md`) returned **DO-NOT-RUN**, finding that the lesion-term rule
  placed spurious expansion-loss terms (2,281/6,944 instances) and double-counted across bifurcations — fatal for the
  stenosis-length error type. Rule replaced with local-maxima-on-tree detection plus a true tree-distance merge;
  two further defects found while fixing it (an inserted lesion contiguous with a deeper native one lost its loss
  term; the 5 mm merge compared root-arc rather than tree distance, so a lesion on one branch erased one on another).
  E0, sweep and selection regenerated: **the fix moved 3,376/6,944 instances (max +0.144) and replaced 110 of the 150
  selected**. Verification passes on both beds and both disjoint scan sets (V8a 0.0012–0.0030, V10 = 0.0000,
  tolerance unchanged at 0.005). Review re-verified independently → **GO-WITH-CHANGES**.
  **Cohort frozen** as `protocol/COHORT-FROZEN-2026-09-18.csv` + SHA-256 manifest (150 instances, 25/band, LAD 50 /
  LCx 50 / RCA 50, 108 trees, 93 patients) — a hashed list, not a seed, because `select()` is chaotic.
  **Statistics plan** drafted (`protocol/STATISTICS-PLAN.md`): patient-level random effect with nested slot term,
  band × severity confounding **declared not rebalanced**, noise floor mandatory alongside every flip rate,
  per-structure bands, Holm across H1–H6.
  **Remaining before the pre-registration locks:** implement the discrete arm in the run pipeline with logged
  exclusions; E0 verdict re-confirmed at 20/4/2 trees (severity sweep still required).
- **2026-09-18 — Phase 0 largely done in one day.** D1 ✔ (ImageCAS-X local, MD5 verified) · D1b email sent · E0 ✔
  (verdict: severity sweep required) · 0D pipeline built and validated (`code/zerod_ffr.py`, `imagecasx_loader.py`) ·
  **severity-sweep cohort constructed**: 6,944 instances on 280 hosts, 0 failures; **150 instances selected, 25 per FFR
  band 0.65–0.95, balanced across LAD/LCx/RCA, no shortfall** (`protocol/SEVERITY-SWEEP-SPEC.md` §8b–8d). Ten-check
  verification suite run twice on disjoint scans before the sweep; first run failed (single-precision radius array),
  fixed at source, re-run clean.
- **3D arm specified at v0.2, operator-approved 2026-09-18** (`protocol/CFD-ARM-SPEC.md`; v0.1 archived). v0.1's two
  decisions were agreed, then an independent adversarial review returned MODIFY/REJECT and showed the arm did not test
  the thesis; the operator approved the revisions the same day. v0.2: three-rung ladder (0D → polyball control →
  **real-lumen primary replication**, 30 instances); Protocol C tuned **inside each fidelity** and **flow-matched only**;
  discrete Murray outlets (leaf r_ref^2.66) truncated at **0.60 mm**; **BC structure (leaky vs discrete) a pre-registered factor of the 0D
  experiment**. CFD machine: 16 physical cores → ~12 days unattended. Staged so the 3D arm is off the critical path, with
  a day-one real-lumen pilot (M1) and a pre-agreed fallback. **Supersedes §E3 above and corrects §E2 (see its banner).**
- **Still open in Phase 0:** N1 database search + `pursue T6` · D2 ASOCA terms · T1/M1 on the CFD machine · authorship ·
  E6 outreach. **Phase 1 is NOT started:** error-type operations, A/B/C rules, statistics and the OSF pre-registration
  must be frozen **before** any ablation run — the cohort exists, the experiment does not.

## 7. Work packages (phased; dependencies, not dates)

| Phase | Content | Depends on | Effort (person-weeks, rough) | Parallel track |
|---|---|---|---|---|
| **0 Foundations** | Gates N1 (DB search, `pursue T6`), D1, D2, T1; send D1b email; 0D pipeline on 5 trees; **prevalence check**; authorship agreed; E6 outreach begins | — | 2 | E6 ethics/data conversations start now |
| **1 Protocol** | Error model with exact operations; A/B/C with Fossan rules; stats plan; **OSF pre-registration**; hash + third-party deposit | 0 | 1–1.5 | M1 pilot runs here on the concurrent PCs |
| **2 Primary ablation** | Full 0D sweep (natural cohort + severity sweep; + natural-experiment arm if D1b passed); noise-floor Monte Carlo; Gamage sub-study | 1 | 2 | E3a starts as soon as M1 passes |
| **3 Cross-fidelity** | E3a steady replication on 30–50 cases; E3b mechanism figure | M1, 2 (tuned params) | 2–3 (mostly wall-clock and mesh QA) | Concurrent with 2 and 4 |
| **4 Detector** | E5 development, held-out ROC, external test | 2, D2 | 2 | — |
| **5 Analysis** | All figures; Source Data; number audit (P16 lesson) | 2, 3, 4 | 1.5 | — |
| **6 Writing & review** | Manuscript; `ars-reviewer` simulated panel; revise; cover letter; submission-check against the chosen venue's guide | 5 | 2–3 | — |
| **7 Clinical anchor** | E6 if data obtained | ethics | open-ended | Runs alongside everything; folds in at 5 if ready |

Rough total: **12–15 person-weeks** on the critical path (Phases 0–2, 4–6), with 3 concurrent. That is a
December-quarter paper done properly — see §11 for what the October date can still be used for.

## 7b. Team and authorship

**Four authors, in this order. Contacts and CRediT confirmed by the operator 2026-09-19.**

| # | Author | Affiliation and contact | ORCID |
|---|---|---|---|
| 1 | **Fadillah Yamin** | Dept of Mechanical Engineering, School of Engineering, Monash University Malaysia, Jalan Lagoon Selatan, Bandar Sunway, 47500 Selangor, Malaysia — `mohd.yamin@monash.edu` | **none** — confirmed 2026-09-19, not an omission. Optional for OSF; worth creating before journal submission, as several publishers now request one |
| 2 | **Mohd Azan Mohammed Sapardi** | Dept of Mechanical Engineering, Kulliyyah of Engineering, IIUM, Jalan Gombak, 53100 Kuala Lumpur — `azan@iium.edu.my` | 0000-0001-5278-014X |
| 3 | **Ming Kwang Tan** | **Dual:** Dept of Mechanical Engineering, School of Engineering, Monash University Malaysia, Jalan Lagoon Selatan, 47500 Bandar Sunway, Selangor **and** Dept of Mechanical Engineering, Ming Chi University of Technology, New Taipei City 243, Taiwan — `tanmingkwang@mail.mcut.edu.tw` | 0000-0002-1585-9358 |
| 4 | **Xin Wang** | Dept of Mechanical Engineering, School of Engineering, Monash University Malaysia — `Wang.xin@monash.edu` | 0000-0002-5854-5287 |
| 5 | **Mohd-Zulhilmi Paiz Ismadi** | Dept of Mechanical Engineering / Centre for Net Zero Technology, Monash University Malaysia — `mohd.zulhilmi@monash.edu` | 0000-0002-7724-114X |

> **Name settled, 2026-09-19:** author 2 was recorded as "Mohamad Azan" — the operator confirms that was his own typo
> and the given name is **Mohd Azan**. **Byline confirmed as the long form, "Mohd Azan Mohammed Sapardi."**
>
> **Corresponding author: Mohd-Zulhilmi Paiz Ismadi (author 4), decided 2026-09-19.** Recorded reason: the last
> position carries the senior/supervising signature in this field, and he holds the 0D model, the error-injection
> pipeline, the ablation, the detector and the analysis — so he is the person who can actually answer a reader's or
> a reviewer's question about any part of it. Last-and-corresponding is a coherent pairing; the alternative reading
> (first-author-by-labour) was considered and set aside deliberately rather than by default.

**Monash–IIUM collaboration** (the project folder's namesake), not Monash alone. C. R. Sarimuthu and M. E. Raghunandan
are **not** on this paper and remain on the sibling studies.

**Author added 2026-09-19: Ming Kwang Tan, third position** — CRediT *Investigation, Methodology, Validation*.
Affiliation taken from the sibling paper (P16), where he is an author on the same team: **dual Monash Malaysia
Mechanical Engineering and Ming Chi University of Technology, New Taipei City, Taiwan**. On P16 his CRediT was
*Investigation, Formal analysis, Writing – review & editing*; the roles here are different, which is normal and
needs no reconciliation.

**Contacts resolved 2026-09-19** from `Imaging-Medical/AuthorsDetails.docx`: `tanmingkwang@mail.mcut.edu.tw`,
ORCID **0000-0002-1585-9358**.

**Affiliation discrepancy RESOLVED 2026-09-19 — dual, and the evidence is decisive.**
`AuthorsDetails.docx` is a contacts list and gives only his external affiliation (Ming Chi). But
`Imaging-Medical/PreviousStudy/Updated Automation In Construction Manuscript.docx` is a **manuscript by this exact
team, with these exact five authors in this exact order**, and it lists him as **¹,³ — Monash Malaysia Mechanical
Engineering *and* Ming Chi**. A byline from a live manuscript by the same group outranks a contacts list for this
purpose, and it matches what P16 does. Recorded as dual above; no need to ask him.

> **Two things that manuscript also settles, worth carrying across rather than re-deriving:**
> - **The author order is already established for this team** — Fadillah Yamin · Ming Kwang Tan · Mohd Azan Mohammed
>   Sapardi · (Xin Wang) · Mohd-Zulhilmi Paiz Ismadi, corresponding. Paper 6's order differs only in placing Xin Wang
>   fourth rather than Ming Kwang Tan second. Worth a glance to confirm that difference is deliberate.
> - **Xin Wang's byline: "Xin Wang" is correct, Wang is the surname — confirmed 2026-09-19 against ORCID
>   0000-0002-5854-5287** (given-names "Xin", family-name "Wang", no credit-name, no variants). **This paper is
>   already right; the sibling manuscript's "Wang Xin" is the error** and should be corrected there before it is
>   submitted, since a reversed byline indexes to a different person.
>   *(Caution for anyone using that ORCID as a bibliography source: its 22 recorded works span concrete creep, CO2
>   capture, soft robotics and ventilation, which suggests auto-ingested name-matches — "Xin Wang" is a very common
>   name. The name fields are authoritative; the works list should not be assumed to be hers.)*

**One item still outstanding: which block of the work is his.** *Investigation, Methodology, Validation* are CRediT
**roles**, not a body of work, and the table above assigns work blocks precisely so ICMJE accountability is
nameable — each author must be able to say which part they vouch for. Plausible candidates are the **0D model and
verification suite** and the **CFD arm's validation**, but that is a guess, and guessing is what this table exists to
prevent. **Name it before lodging**; until then the row reads "TO BE NAMED" deliberately.

> **NAMED 2026-10-03 by the corresponding author: both.** Ming Kwang Tan vouches for the **verification of the 0D
> model** (the V1–V10 suite) **and the validation of the 3D CFD arm** (Stage A, Gate M1, U₃D). Criterion 2 is still
> open for him (see the ICMJE table).

Otherwise authorship is settled: order, byline forms, corresponding author, and a CRediT block for every author.

> **Note on adding an author at this point:** doing it *before* lodging is clean. Adding one *after* registration is
> a normal amendment rather than a deviation, but it must then be declared with its date — so if any further author
> is in prospect, now is materially cheaper than later.

**Contribution bar — CRediT. ASSIGNED 2026-09-19, and every author now holds a block.**

| Block | What it is | CRediT roles | Assigned to |
|---|---|---|---|
| 0D model + error injection | `zerod_ffr.py`, `error_types.py`, verification suite | Software, Methodology, Validation | **Ismadi** |
| Ablation + statistics | the A/B/C run, analyses P1–P5 | Software, Formal analysis, Investigation | **Ismadi** |
| Detector (C3) | parameter-plausibility and anatomical-plausibility statistics, splits, external test | Methodology, Software, Formal analysis | **Ismadi** |
| 3D CFD arm | Stage A → Gate M1 → Stages B–D on the 16-core machine | Investigation, Validation, Software, **Resources** (the compute) | **Mohd Azan** |
| Analysis and drafting | the manuscript; formal analysis alongside Ismadi | **Writing – original draft**, Formal analysis | **Fadillah Yamin** |
| **Method and verification** | **verification of the 0D model (the V1–V10 suite) and validation of the 3D CFD arm (Stage A, Gate M1, U₃D)** — named 2026-10-03 | Investigation, Methodology, Validation | **Ming Kwang Tan** |
| Study design and critical revision | the question, the framing, the method | **Conceptualization, Methodology, Writing – review & editing** | **Xin Wang** |
| Clinical anchor (E6) | invasive-FFR cohort, ethics, clinical interpretation | Resources, Investigation | **not pursued for this paper** — E6 is an extension; if it lands it brings its own author and that is a normal registration amendment |

### ICMJE form — and converting to it found a gap

CRediT *describes* contributions; ICMJE *gates* the byline. Restating the table above against ICMJE's four criteria,
which **every** author must meet, exposes something the CRediT view hid.

| Author | 1. Substantial contribution | 2. Drafting **or** critical revision | 3. Approval | 4. Accountable for |
|---|---|---|---|---|
| **Fadillah Yamin** | formal analysis | **drafting** — original draft | at submission | the analysis and the written account |
| **Mohd Azan Mohammed Sapardi** | the 3D CFD arm: Stage A, Gate M1, Stages B–D, and the compute | **⚠ NOT YET RECORDED** | at submission | the CFD arm and its reported failure rates |
| **Ming Kwang Tan** | verification of the 0D model and validation of the 3D CFD arm (named 2026-10-03) | **⚠ NOT YET RECORDED** | at submission | the 0D verification suite and the 3D validation results |
| **Xin Wang** | conception and design of the study | **critical revision** — review & editing | at submission | the question, framing and method |
| **Mohd-Zulhilmi Paiz Ismadi** | 0D model, error injection, ablation, detector, statistics | **drafting** | at submission | the model, the code and every reported number |

> **⚠ Two authors do not currently satisfy criterion 2 on the record.** Mohd Azan and Ming Kwang Tan hold substantial
> contributions (criterion 1) but neither has a drafting or critical-revision role recorded. **Under ICMJE that is
> not sufficient for authorship** — contribution alone is explicitly not enough, and a contributor who does not also
> draft or critically revise belongs in the acknowledgements rather than the byline.
>
> The fix is easy and must be *real*, not assumed: **both must review and critically revise the manuscript, and that
> must be recorded when they do.** Ask them for comments on a draft rather than a sign-off on a finished text. This
> is worth arranging now, while writing has not started — it is far more awkward to arrange retrospectively, and
> "they approved it" is not the same claim as "they critically revised it".

**Draft contributions statement, ICMJE form** (for the manuscript; refine once Tan's block is named):

> X.W. and M-Z.P.I. conceived and designed the study. M-Z.P.I. developed the reduced-order model, the error-injection
> pipeline and the detector, and performed the ablation and statistical analysis. M.A.M.S. designed and executed the
> three-dimensional computational fluid dynamics arm. M.K.T. contributed to [block], methodology and validation.
> F.Y. performed formal analysis and drafted the manuscript. All authors critically revised the manuscript for
> important intellectual content, approved the submitted version, and agree to be accountable for all aspects of the
> work. M-Z.P.I. is the corresponding author.

**CRediT is retained above**, not replaced: many journals — including Elsevier titles, as the sibling paper P16 used —
require a CRediT statement in addition. The two are complementary, and the ICMJE table is the one that decides who
appears on the byline at all.

Two further practical consequences, worth noting now rather than at submission:

- **Fadillah Yamin holds Writing – original draft**, so he needs the manuscript early enough to genuinely draft it,
  not to copy-edit a finished text. That is a scheduling commitment, not a formality.
- **Mohd Azan holds the CFD arm**, which is the arm most at risk — Gate M1 is currently blocked at meshing and mesh
  convergence is not yet demonstrated. If the §9 fallback is invoked the arm shrinks but his contribution does not
  disappear; the meshing-reliability finding is itself a reportable result (`CFD-ARM-SPEC` §12). Worth saying to him
  explicitly, because "the arm was cut" and "your contribution was cut" are different things and only the first is
  true.

ICMJE criteria apply: substantial contribution, drafting or critical revision, approval of the submitted version,
accountability. Adding an author later (e.g. if the clinical anchor lands) is a normal registration amendment, not a
deviation.
**Compute statement:** generic wording only, no hardware or OS names (standing rule across these papers).

## 8. Reproducibility and pre-registration

- **OSF pre-registration** of §3–§5 before any Phase 2 run: hypotheses, both directions, decision rules, bands,
  statistics. Few CFD papers do this; reviewers at a validation-themed SI will notice.
- **Code** (network construction, corruption, A/B/C, detector) deposited with DOI (Zenodo); protocol file hashed and
  lodged with a third party (P16/T13 discipline).
- **Data:** ImageCAS-X and (if used) ASOCA are public; every corrupted geometry and every run's outputs released as
  Source Data. If the paired masks are shared under conditions, honour them and state them.
- **Citations to verify before use:** Pfaller 2022 (svZeroDSolver lineage); Collet 2019 (pullback index); Mao 2025
  code licence; ASOCA terms.

## 9. Reviewer attacks and pre-emptions

| # | The objection, as a reviewer would write it | Pre-emption |
|---|---|---|
| 1 | "Gosling 2020 / Sankaran already showed BC tuning absorbs geometric discrepancy." | Four-axis differentiation in the introduction: topological (not flow under-representation); per-case (not cohort-averaged); reclassification (not aggregate); hazard (not reassurance). Quote HeartFlow's *"fixed bifurcation locations."* |
| 2 | "A 0D model re-tuned to its own consensus-label baseline is not ground truth." | Stated up front as the design; E3 replicates at 3D; E6 anchors clinically if obtained; the claim is about *error-induced change*, framed exactly as Fernández-Martínez framed theirs |
| 3 | "The injected errors are unrealistic." | **Rewritten 2026-09-19 — the old answer ("magnitudes from 160 blind re-annotations including a topological rate; quality-matched via the dataset's own stratifiers") was not true of the code.** Honest answer: T3 and T4 derive from measured disagreement statistics (HD95, DSC) which the dataset's authors state are an **upper bound on agreement** — both annotators edited the same auto-generated centrelines from a shared U-Net initialisation — so those two are floors *as statistics*, with the per-magnitude direction argued case by case. **T1 and T2 have no measured magnitude and are declared design choices.** Magnitudes are uniform, not quality-matched. D1b was declined; D1c (model-vs-reference predictions) would supply the missing **apportionment** across error types |
| 4 | "Protocol C is one equation, one unknown — the fit is trivial." | Fossan rules 1–3, fewer parameters than targets, pre-registered |
| 5 | "The flips are physiological noise." | Noise-floor Monte Carlo at Tanade's SDs on the same axes |
| 6 | "Already shown in pulmonary (Colebank) / aneurysm (Korte)." | None of the four non-coronary comparisons has a decision threshold; coronary autoregulation (Fossan) is territory-specific |
| 7 | "The detector is circular — trained on the same corruptions it detects." | Held-out split; external dataset; uses only untuned outputs; failure modes reported |
| 8 | "A null result." | Both directions pre-registered; the inverted finding is written into §0 as the alternative paper |
| 9 | "Why only FFR 0.80? Clinical practice uses a grey zone." | Bands reported, including 0.75–0.80 and 0.80–0.85; grey-zone flips separated from clear flips |

## 10. Risk register (v2)

| Risk | Likelihood | Mitigation |
|---|---|---|
| Paired masks refused | Medium | In-house second annotation on 30 cases (affordable without a deadline); published statistics as fallback |
| Prevalence too low in ImageCAS-X | Medium | Severity sweep cohort (run regardless) |
| 3D repair step fails on topological corruptions | Medium-High | E3 off the critical path; over-sample 40%; report failure rates as a finding |
| Detector uninformative on unbranched trees | Medium | Pre-specify branched-tree scope; report failure honestly; C1–C2 stand without C3 |
| H2 returns the rescue direction | Medium | Pre-registered; inverted paper written into §0 |
| Cross-project core contention (WindTurbine, DataCentre) | Medium | Allocate cores explicitly at T1; E3 is elastic |
| Authorship unsettled | — | Phase 0 item, not a placeholder |
| Radius-definition gap between 0D (EDT) and 3D (area-equivalent) lumens, 23–44 % (837) and throat +19.5 % (scan 14) | **Certain (measured)** | 0D twins for H4/E3 rebuilt on as-meshed radii (`ingest_cfd_radius.py`), both variants reported; state as a limitation of the EDT-based primary arm (added 2026-09-26) |
| 3D batch cost ≈ 13× estimate (≈ 40 machine-days) | **Certain (measured)** | Convergence-based stopping, multi-PC, re-cut grid; decided after WO 09-26 Task B (added 2026-09-26) |
| Scope creep now that the clock is off | **High** | Everything in §3 is in; anything not in §3 (WSS/OSI, TAG, eccentric lumen, new datasets) goes to a follow-up list, not this paper |

## 11. Venue

- **Baseline:** IEEE JBHI. The special issue's aims paragraph names this gap verbatim. If Phases 0–2 plus the
  mechanism figure are done by 2026-10-15, a reduced submission to the SI is possible — but **only if it would not
  weaken the paper**; a regular JBHI submission later with C3 and E3a complete is preferred to a rushed SI one.
- **Upgrade path:** with E3 replication + C3 external validation, IEEE TMI or Medical Image Analysis are credible.
  With E6 (invasive anchor), the conversation changes again. Decide at Phase 5 on what actually landed.
- T13 remains the Nature-family attempt; T6 should not be positioned to compete with it for that slot.

## 12. What was dropped, and why (so it is not re-litigated)

- **WSS/OSI secondary arm** — answers a plaque-vulnerability question the paper does not ask; pulsatile cost ~1000×
  steady; OSI unimplemented in any backbone; replaced by FFR-only cross-fidelity replication, which defends the primary
  claim instead of diluting it.
- **"Ranking error types" as the headline** — occupied five times (HeartFlow ×4, Colebank). Ranking survives as H1,
  not as the title.
- **TAG-based detector** — TAG AUC 0.50 vs FFR-CT 0.79 against invasive FFR; already used *as* a BC input elsewhere.
- **Eccentric-lumen error type** — no 0D representation.
- **BC-masking as a *new mechanism*** — Gosling 2020 has it; the paper claims the ablation, the threshold, the
  topology, and the remedy, not the mechanism.

## 13. First ten actions

1. Send the ImageCAS-X email (D1b) — the only item whose wait is outside your control.
2. Download ImageCAS-X + ImageCAS volumes; verify centrelines and surfaces; log MD5 (D1).
3. Check ASOCA terms (D2).
4. Install svZeroDSolver; verify Mao's package runs and check its licence; allocate cores per PC (T1).
5. Build the 0D network from 5 ImageCAS-X centrelines; compute baseline FFR (E0 start).
6. Run the prevalence check on all diseased-flagged scans; apply the §E0 decision rule.
7. Run the ACQUIRE-T6 database search strings; close N1; run `pursue T6`.
8. Agree authorship.
9. Draft the OSF pre-registration from §3–§5.
10. Open the E6 conversation with clinical partners — it has the longest lead time of anything here.
