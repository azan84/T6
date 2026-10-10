# Audit of PLAN.md (blind audit 2026-10-09), Paper 6 (T6)

Auditor: independent (computational hemodynamics, JBHI editorial). Date: 2026-10-09.
Inputs read: PLAN.md, SCORES.md, RUBRIC.md, the five reports, main.tex, supplement.tex, the supplement table files, page images (ms-page-1, ms-page-8, supp-page-6), REVISION-PLAN-POST-SUBMISSION-2026-10-08.md. Code inspected: ablation.py (`territories()`, `protocol_c_targets()`, the Protocol C fit), ablation_per_territory.py, error_types.py, zerod_ffr.py (loss model), summarise_revision.py, negatives.py headers. Data recomputed from results/ablation-2026-10-07.csv, ablation-perterritory-2026-10-08.csv, negatives-2026-10-07.csv, discrete_arm_eligibility.csv, cfd_M1/M1_scan14_0D_vs_3D-2026-10-03.csv, and from the ImageCAS-X trees in ~/Documents/Datasets/imagecas-x (12-instance sample). No project file was modified; scratch under /private/tmp/claude-501/audit/.

---

## 1. Summary verdict

The register is accurate. Every status I spot-checked (V1, V2, V3, V5, V7, V9, V11, V24, V32, plus V26 and V27) reproduces from the frozen run or the source, and Table P reproduces in all 16 cells. The plan's tiering is sound in principle: wording fixes first, cheap measurements second, headline-changing analyses as an operator decision, the throat error and real-failure frequency deferred.

Three findings change the plan:

1. **T3-1 (finer territories) is decided by a code convention, not by physics.** `protocol_c_targets()` drops any territory with no surviving corrupted node. At first-bifurcation granularity this never matters (a dropped territory makes C/D undefined). At finer granularity a deleted branch that forms its own territory would silently vanish from the residual, and the check would pass *more* models, not fewer. The run is only meaningful if an unperfused territory counts as a 100% mismatch. That is a design decision to record before the run, and it makes the outcome predictable: topological passes-and-wrong will fall at finer granularity, taper passes-and-wrong will not. Run it, but with that convention and with the wording prepared for that outcome.

2. **T2-2 (analytic overlap) will partly contradict the current text.** On a 12-instance sample the tube-model DSC of T1 (median 0.977) equals that of T4 (0.974): DSC does not separate the decisive error from the benign one, which supports the paper. But a vessel break (T2) in the RCA removes up to half the tree volume (DSC 0.52–0.72), so "vessel breaks ... despite high overlap scores" cannot stand unqualified once this is measured. clDice is 1.000 for T3/T4 by construction (the centerline is unchanged) and 0.27–0.99 for T1/T2, so it flags the class, not the risk. The analysis is valid (corrupted ⊂ clean holds for all four types, T3 included) and should be run, but the IV-B sentence and the Conclusion's "which overlap scores miss" must be rewritten to what the numbers show.

3. **T2-3 (dose response) should be dropped.** The dose is flat: under Protocol A, Spearman(|ΔFFR|, lost inflow fraction) is −0.10 for T1 discrete (p = 0.38), +0.15 leaky (p = 0.09), and only T2 leaky shows a gradient (0.41). Flip rate by tertile is non-monotone in every cell. A post hoc tertile table would hand reviewers a new objection ("the magnitude is not the driver") without answering the one they raised (graded T1/T2 severities). Leave the sweep for the revision, designed properly.

Also: the main text has **zero** slack (page 8 ends on the last reference line, see §6), the abstract is at 249–250 words and the Tier 1 abstract edits are net +12 to +15 words, and the supplement has about 40 lines free, not 45. The plan under-funds the main text by 10–15 lines and the abstract by about 15 words. Cuts are listed in §6.

Projected panel mean for the go-list below: **7.0** (plan: 7.2–7.4). The remaining deductions are the ones the plan correctly defers (throat error, like-for-like noise, real failure frequency, radius bias), and no wording can remove them. Expect "major revision" from at least two of five seats at submission; that is acceptable for the SI deadline, and the deferred analyses are the revision.

---

## 2. Register check

Spot-verification against the source and the frozen run.

| ID | Plan status | Verified? | Evidence |
|---|---|---|---|
| V1 | CONFIRMED | **Yes** | ablation-perterritory csv: two converged D models with residual > 0.01: 0.083 and 0.111 (scan 984 right, T1, both `fit_at_bound = True`, |ΔFFR| 0.041 and 0.026). Caption at main.tex l.343 says "below 0.01". |
| V2 | CONFIRMED (one bed only) | **Yes** | Recomputed with the 97-instance discrete eligibility filter: discrete topological C: 39 pass, 20 P&W → 51%. Leaky: 154 pass, 14 P&W → 9%. IV-A l.398 is bed-unqualified. |
| V3 / Table P | CONFIRMED | **Yes, all 16 cells** | My recomputation matches Table P exactly (e.g. discrete topo A 137/21/119/17; D 104/103/21/21; leaky cal C 300/294/37/37). |
| V5 | CONFIRMED | **Yes** | Discrete topological B P&W: 2/137 (S3 basis), 2/173 (S5 basis, undefined counted as failures), 2/104 (text, C-defined instances). Leaky: 10/218 = 4.6, 10/267 = 3.7, 10/171 = 5.8 → printed 5 / 4 / 6. |
| V7 | CONFIRMED | **Yes** | cfd_M1 csv: baseline 3D resistance 0.8698, prescribed 0.8923; T1 prescribed 0.8916. Δ vs prescribed baseline −0.0007; vs clean fixed-resistance 0.870: +0.022. The 0D cohort counterpart also gives −0.0007 (0.7612 → 0.7605). Main text l.357 gives only the first. |
| V9 | CONFIRMED + VALID-LIMIT | **Yes** | `n_territories` over C-defined rows: 2 in 863 rows, 3 in 58 rows (median 2, max 3). Over A rows: 57 with 0 and 89 with 1 territory, which is where C/D become undefined. Nowhere stated in the paper. |
| V11 | PARTLY | **Yes** | zerod_ffr.py `_solve`: `R_lin = 8 μ ds/(π r_mid^4)` per element on the *actual* (narrowed) radius; `K` is the expansion term only. The viscous loss over the lengthened lesion is therefore in the model, and the reviewer's "no length term" is wrong on the physics but right that the text does not say so. T1-8 is the correct answer. T3's near-null is still expected: +2.46 mm of partially narrowed lumen adds little viscous resistance at the throat area ratio, and the reviewers will accept that once the model form is stated. |
| V24 | CONFIRMED | **Yes** | main.tex mentions only "k doubled and tripled" (l.157) and III-E; no pointer to Table S4 (×0.7/×1.3). |
| V26 | CONFIRMED | **Yes, and cheaper than planned** | supplement l.134–138: C fit at a bound = failure; D at 10^3 "retained". The two bound-hitting D models are exactly the two V1 outliers. Applying the C rule to D (exclude as failed fits) resolves V1 and V26 together: Fig. 3 caption becomes true as written, Table I T1-D discrete n goes 44 → 42 (flip 1/42, P&W 10/42), 104 → 102 in the pooled D cells. This is one rerun of summarise_revision.py / supplement_tables.py. Recommend this over the "state the bound is not limiting" wording, which is not true (residuals 0.08–0.11 show the bound *is* limiting). |
| V27 | VALID | **Yes** | 36 discrete (eligible) and 2 leaky zero-outflow A-T2 models; 17 and 1 have clean FFR ≤ 0.80 and would flip to FFR → 1. Scored as flips: discrete A-T2 (24+17)/96 = 43% (was 40%), leaky (63+1)/149 = 43% (unchanged). One line in the Table S1 note; direction unchanged. |
| V32 | NOT CONFIRMED | **Yes** | ieeecolor.cls l.3485 includes `\logoname.eps` in the first-page head; ms-page-1.png shows the template's blue "LOGO" placeholder. It is the template; leave it. |
| V20 | VALID-LIMIT | Status right, but a patient-clustered GEE already exists (results/analysis-ablation-2026-10-07/P1_gee_{discrete,leaky}.csv, 62/93 clusters) and is unreported. It has a separation problem (band 0.90 coefficient −3 × 10^139), so it cannot be cited as is. The cluster bootstrap (T2-5) is the cleaner route. |

**Mis-classifications.** None of the statuses is wrong. Two items are classified but not assigned to any plan item:
- **V36** (abstract leads with Protocol A; B should be co-equal; I W5, D C5): VALID, no T1 item. See §4.
- **V39** (throat Reynolds number, lesion flow): VALID (minor), no item, no decline reason. Note that the 3D case's lesion flow is 0.09 mL/s (5 mL/min) at a left-tree inflow of 0.71 mL/s (43 mL/min) in cfd_M1; throat Re ≈ 55. Reporting it would sharpen C W1 rather than answer it; decline for space and rely on the ×2/×3 replication, and say so in the log.

---

## 3. Item-by-item verdicts

Verdict key: KEEP / MODIFY / DROP / PROMOTE / DEFER.

### Tier 1

| # | Verdict | Reason |
|---|---|---|
| T1-1 | **MODIFY** | Resolve with V26 by applying the C bound rule to D (exclude the two scan-984 models as failed fits). The caption then stands; Table I and the pooled D counts change by two models. If the operator prefers not to touch counts, the caption fix is fine, but then T1-14 must say the bound *was* limiting in two models. |
| T1-2 | KEEP | 20/39 = 51% discrete, 14/154 = 9% leaky; verified. Fold the Table P numbers into this sentence (so T2-1 costs no main-text line). |
| T1-3 | **MODIFY** | Right fix, wrong arithmetic. The replacement adds ~12 words; the 3D trim (T1-5) saves ~6. Fund it by cutting "and none for caliber errors with re-derived boundary conditions" (−10 words, it is secondary) and "(pooled)" (−1). |
| T1-4 | KEEP | 5/5 seats. "for the error magnitudes studied" (+5 words) is the single most protective phrase in the abstract; also add "away from the stenosis throat" to the Conclusion's caliber sentence (prepares T5 without running it). |
| T1-5 | KEEP | Verified numbers (+0.022 vs clean, −0.0007 vs prescribed baseline; the baseline moves because bed-weight sharing within a territory does not reproduce the clean per-outlet split). Caption: "raised FFR by 0.074" is factual. |
| T1-6 | KEEP | Supplement already says the criterion failed; the main text's "at most 0.0021" without it reads as better than it is. +1 line. |
| T1-7 | KEEP, and raise its priority | Median 2 (max 3) territories verified. This sentence is what makes the 19–20% a stated conditional rather than an exposed weakness, whichever way T3-1 goes. Put "at main-branch territory level" in the abstract if the word budget allows (T1-3 trade). |
| T1-8 | KEEP | Verified in `_solve`. Half a line; answers M W4 completely. |
| T1-9 | KEEP | 0 lines. |
| T1-10 | KEEP | 0 lines. |
| T1-11 | KEEP | 0 lines; also answers I W5's "when does A arise" if phrased "outlet resistances fixed independently of the segmented tree". |
| T1-12 | **MODIFY** | Three captions explaining three conventions is the weak fix. Use one convention (S3: models with a defined residual) everywhere and regenerate Table S5 on it (replication_table.py). If that script cannot, then captions. |
| T1-13 | KEEP | 0 lines. |
| T1-14 | **MODIFY** | See T1-1: one rule (bound = failure) for C and D. |
| T1-15 | KEEP | +1 line; the ×0.7/×1.3 pointer can ride on the existing l.157 sentence ("repeated with k scaled by 0.7 and 1.3 on the same cohort and doubled and tripled with re-selection"). The 13%/16% origin must be true; if it is 1.3× and 1.6× the 10% primary, say that. |
| T1-16 | KEEP, PROMOTE in wording | This is the T5 disclosure. State the number (0.045 mm at the throat moved FFR by 0.11) and that the throat was not perturbed. It is the honest substitute for T3-3 before the deadline. +2 lines. |
| T1-17 | KEEP | Tone rule. 0 lines. |
| T1-18 | **MODIFY** | Add "and the caliber errors were one-directional (narrowing and lengthening only)" (I W2 iii, missed by the register). +1.5 lines total. |
| T1-19 | **MODIFY** | Fig. 3 line and Fig. 2 note are 10 minutes. Fig. 4 colormap requires the CFD field data locally (check cfd_handover before promising); if not local, leave the colormap and note it. Font enlargement conflicts with any figure shrink used to fund lines (§6); choose one. Add Fig. 1(d) (I W8: T3/T4 curves indistinguishable from "With lesion") to the list only if fig1_errors.py can add an inset in under an hour. |

### Tier 2

| # | Verdict | Reason |
|---|---|---|
| T2-1 | KEEP (as columns of Table S3) | Verified. Add pass n and P(wrong \| pass) as two columns to Table S3 rather than a new table (saves ~6 supplement lines). Add the per-cell repeat-FFR floor as a third column if it fits (M W3 asked for it; it is already computed for the "5.0–6.5%" note). Main-text cost 0 (folded into T1-2). |
| T2-2 | **MODIFY** (run it; rewrite the claim to the result) | Validity: corrupted ⊂ clean holds for all four types in the tube model. T1/T2 delete nodes; T4 scales r by 0.93; T3 re-inserts with a longer L at the same centre and DS, and because w(s) increases with L at every s inside the shorter lesion and r' = min(r, ·), r'_long ≤ r'_short everywhere (asserted numerically on 12 instances). So DSC = 2V'/(V+V') and clDice = 2f/(1+f), f = centreline fraction retained, are exact for the tube model. Sample result (n = 12): DSC median T1 0.977, T2 0.911 (RCA 0.52–0.72), T3 0.997, T4 0.974; clDice T1 0.93, T2 0.87 (RCA 0.27–0.44), T3/T4 1.000 by construction. Betti-0 is unchanged by all four types. Consequences: (i) "a missing side branch removes few voxels" is supported; (ii) "vessel breaks despite high overlap" is not, for RCA breaks in this design; (iii) DSC does not rank T1 above T4 even though T1 flips 2–3× as often, which is the real informatics point; (iv) a reviewer will notice that the applied T4 gives a tube-DSC of ~0.97, above the 0.928 it was derived from, because the narrowing is applied from the lesion onwards only; say so in the caption. Call the metrics "tube-model DSC/clDice" and state that voxel DSC on masks would differ at partial-volume level. Report AUC of each metric for flip (expect ~0.5–0.6 for DSC). Cost: 0.5 day; ~10 supplement lines; main text net 0 if it replaces the IV-B sentence. |
| T2-3 | **DROP** (defer to revision) | Flat dose (§1, item 3). A tertile table would weaken S3, not raise S2. The reviewers asked for graded severities (branch rank, 10/25/50 mm), which is a new run, not a re-cut of this one. |
| T2-4 | **MODIFY** | Data support it: Protocol B residual median 0.196 (topological) vs 0.021 (caliber) in the discrete bed, 0.027 vs 0.012 leaky; \|log C ratio\| 0.047 vs 0.015 discrete. Two corrections: (a) the detector target must be the error class *and* the flip; against flip alone the AUC will be modest because flips depend on baseline proximity; (b) the false-alarm rate needs the pre-tuning residual of correct anatomy against noisy targets, which negatives-2026-10-07.csv does not hold (only post-tuning C residuals; and only 72% of those pass). Either rerun negatives.py with a B-residual column (~1–2 h compute) or state the expected noise-only residual analytically from the draw CVs (≈0.13 RMS, which already says a 10% pre-tuning gate false-alarms on most correct models). Realistic effort 0.5–1 day, not 3 h. Worth it: this is the JBHI deliverable the EIC and R3 asked for, and the honest result ("flags the class in the discrete bed at a high false-alarm rate under physiological noise; weak in the leaky bed") is still a result. |
| T2-5 | KEEP | 2 h is realistic (93 patient clusters, resample 2000×, headline proportions and paired differences). Do not use the existing GEE (separation). One clause in II-F ("patient-level cluster bootstrap intervals for the headline contrasts are in the Supplementary Material") and 4 supplement lines. |
| T2-6 | KEEP | 17 of 36 discrete and 1 of 2 leaky zero-outflow models would flip; A-T2 discrete 40% → 43%. One line in the Table S1 note. 1 h. |

### Tier 3

| # | Verdict | Reason |
|---|---|---|
| T3-1 | **MODIFY, then run** | (1) Fix the convention first: in `protocol_c_targets()` a territory with a clean target and no surviving member must enter the residual as a 100% mismatch (and count toward definedness as a failed territory), not be dropped. Without this, finer territories make the check *blinder* and the run is uninterpretable. (2) Define the partition unambiguously: children of the first bifurcation, each split again at its own first bifurcation (typically 4–6 territories); nodes on trunk segments between the two levels need an owner in the leaky bed (wall outflow is bed flow). (3) Effort is 1 day of code and validation, not 0.5, plus ~25 min of runs (ablation ≈ 5 s/instance, per-territory ≈ 3.3 s/instance from the logs). (4) Outcome handling: with the correct convention, T1 and T2 passes-and-wrong will fall sharply (a deleted branch that is its own territory fails by construction); taper passes-and-wrong will stay (more parameters, exact match, still wrong). Both outcomes are reportable in one supplement paragraph plus one IV-A sentence: "At a segment-level partition the missed branch formed its own territory and failed the check; the taper still passed while wrong." The abstract needs only T1-7's "at main-branch territory level". If the result instead shows persistent topological passes-and-wrong, the finding is robust and the sentence says so. Either way the current headline survives as a stated conditional. Decide and start on 10-10 at the latest; if not coded by 10-11 evening, drop it and rely on T1-7. |
| T3-2 | **DEFER** | Compute is realistic (~4 h: ~15k D fits at ~0.5 s and ~15k C fits at ~0.4 s), but the code is a day, and the result replaces the abstract's headline rates with per-draw rates on 10-12 with a re-score on 10-13. Too much headline motion for the slack available. Do it in the revision. Now: abstract compares C/D with B on the same targets (T1-3/T1-12), and the floor is given as context with "noisy targets" stated (IV-D already does). |
| T3-3 (T5 throat) | **DEFER the analysis; PROMOTE the disclosure** | 5/5 seats raised the asymmetry and two of them computed the 0.11 shift from the 3D case. A T5 result near topological rates would require rewriting the title emphasis, the abstract's first result, IV-A and the Conclusion in the same 6 days as everything above; a half-done reframing is the worst outcome. The post-submission plan is right to run it first after submission. Before submission: T1-16 with the number, "away from the stenosis throat" in the Conclusion, "for the error magnitudes studied" in the abstract. Optional, if the go-list is done by 10-12: code and run T5 internally (0.5 day) so the authors know the answer and can calibrate the ranking wording; report nothing. |
| T3-4 (DOI) | **KEEP, do first** | Largest gain per hour. Add to deposit-2026-10-08/: the three results CSVs (ablation, per-territory, negatives; a few MB), the demand-replication outputs, the CFD case package (cfd_handover.zip, if its contents are the authors' own), a README with software versions (Python, NumPy/SciPy, the VI package, OpenFOAM v2406, cfMesh) and the one-line run commands, and a licence (MIT for code, CC BY 4.0 for the cohort list). Zenodo issues a reserved DOI before publication, so the DOI can be in the Data statement on 10-14 and the record published the same day. Operator action. |

### Tier 4 (defer) — all **KEEP as deferred**, with two notes
- Real failure frequency, half-voxel radius correction, MCMC refit, second 3D case, mass-based demand, CT-FFR reproducibility: agree. The radius correction is the one most likely to be demanded at revision together with T5; start it right after T5.
- "Taper" rename: agree to defer; but add "(a uniform narrowing)" at first use in the abstract if the word budget allows, since I W8 and D C2 both tripped on it.

### Tier 5 (decline) — all **KEEP**
- Annotator-2 masks: declined by the dataset authors 2026-09-18; the log must say so.
- LOGO: template.
- Reweighting: no defensible target.

---

## 4. Missed items

Reviewer points not in the register, or in the register without a plan item.

| Item | Seats | Cost | Recommendation |
|---|---|---|---|
| V36: Protocol A leads the abstract; B (the automated-pipeline case) is pooled with tuning | I W5, D C5 | abstract words or +1 Conclusion line | At minimum, in the Conclusion: "with boundary conditions re-derived from the segmented tree, as automated pipelines do, topological decision changes fell to 5–18% per error type". In the abstract only if the "none for caliber errors" clause is cut. |
| Caliber errors are one-directional (no widening, no throat over-read) | I W2(iii) | +0.5 line | Add to T1-18. |
| IV-C "First, check that the side branches..." is stated without the Protocol A conditioning | D C5 | 0 lines | Insert "under fixed boundary conditions" in that sentence. |
| Fig. 1(d): T3/T4 curves indistinguishable from "With lesion" | I W8 | 1 h if fig1_errors.py supports an inset | Optional; add to T1-19 only if cheap. |
| Software versions (ROM solver, statistics, VI package) | I W9 | 0 main-text lines | Put in the deposit README and one clause in the Table S2 note. |
| Per-cell repeat-FFR floor is not shown ("only the taper exceeded…" depends on it) | M W3, V21 | 1 column in Table S3 | Add with T2-1. |
| "Stricter than measurement repeatability" applies to an RMS over 2–3 territories vs a single-measurement CV | C W7 | +0.5 line | One clause in II-F: "in root-mean-square form over the territories". Low priority. |
| Reference accuracy of [5] Fossan 2026 and [18]/[23] ImageCAS-X 2026 | C W9 | 0 | Confirm against REFERENCE-CHECK-2026-10-07.md; no text change expected. |
| Throat Reynolds number and lesion flow | C W8/D C6 (V39) | — | Decline for space; log the reason (×2/×3 replication covers the regime question). |
| Exponent context (2.66 vs 3; Huo & Kassab, van der Giessen), perfusion-coupled model citations (Papamanolis, Montino Pelagi), Fleeter (identifiability) | C W9, E W11 | ~2.5 lines per reference | Decline before the deadline except at most one (Vardhan 2019, after verification) as the plan says. Log the rest for the revision. |

---

## 5. Score projection

Panel mean per dimension. "Plan" is the plan's "+ Tier 3-1/3-2" column (7.4) and its "+ Tier 2 + DOI" column (7.2) where relevant; "Mine" is for the go-list in §7 (Tier 1 + T2-1/2/4/5/6 + T3-1 with the corrected convention + DOI; T3-2, T3-3 deferred).

| Dim | Now | Plan (T1+T2+DOI) | Plan (+T3-1/3-2) | Mine | Reason |
|---|---|---|---|---|---|
| S1 Novelty | 6.8 | 7.0 | 7.1 | 6.9 | Detector and overlap results are measurements, not new ideas; the EIC's "expected non-identifiability" view does not move without the identifiability framing (V40 sentence, +2 lines, worth adding if a cut is found). |
| S2 Rigour | 6.0 | 6.5 | 7.0 | 6.6 | Table P, cluster bootstrap, measured overlap, territory sensitivity. Still open: noisy targets (T3-2), throat (T5), design-chosen magnitudes, radius bias. Two of these are what every seat scored S2 on; they cap S2 below 7. |
| S3 Claims vs evidence | 5.8 | 7.0 | 7.2 | 6.8 | Most complaints are wording and are fixed; but the overlap claim will have to be *weakened* (T2-2), and the "3–6×" sentence keeps a design-set ratio with a qualifier. 7.0 only if the Conclusion also gives Protocol B its own number (V36). |
| S4 Physiology | 6.0 | 6.4 | 6.8 | 6.4 | Territory granularity declared and tested; flow regime, radius bias, no throat error remain. The clinical seat (5) will not move above 6 without T5 or the radius correction. |
| S5 Consistency | 7.8 | 8.6 | 8.6 | 8.5 | V1/V5/V6/V7/V26 fixed; one convention for denominators. Risk: new supplement tables introduce new inconsistencies; the 10-13 consistency check must cover them. |
| S6 Clarity | 7.0 | 7.2 | 7.2 | 7.0 | Main text gets denser (cuts to fund additions), supplement gains three tables. Net neutral. |
| S7 Venue fit | 6.4 | 7.2 | 7.3 | 7.0 | The detector result is modest (high false-alarm rate under noise; weak in the leaky bed), and the overlap result is "DSC blind to both" rather than "clDice catches it". Honest but less of a deliverable than the plan assumes. |
| S8 Reproducibility | 5.6 | 7.6 | 7.6 | 7.5 | DOI with code, cohort, per-model outputs and CFD cases. 8 needs the real-failure data or a container; not now. |
| **Overall** | **6.4** | **7.2** | **7.4** | **7.0** | Recommendation likely splits: EIC and methodology seats "minor/major", clinical and DA seats "major" (T5, noise symmetry, radius). That is the expected state at an SI submission with the deferred work already planned. |

The plan's 7.4 assumes T3-1 lands as a confirmation, T3-2 runs cleanly, and the measured informatics results read as positive deliverables. The first is a coin toss that the convention fix turns into a likely "topological P&W falls", the second is deferred, and the third is at best neutral.

---

## 6. Page budget

**Main text: zero slack.** ms-page-8.png shows the reference list ending on the last line of the right column; the gap between Acknowledgment and reference [1] in the left column is one line, not a reserve. Every added line, including each added reference (~2.5 lines), must be cut elsewhere.

**Additions (realistic line counts, two-column IEEE at ~10 words per line):**

| Source | Lines |
|---|---|
| Tier 1 (T1-2 +0.5, T1-5 +1, T1-6 +1, T1-7 +2, T1-8 +0.5, T1-15 +1, T1-16 +2, T1-18 +1.5) | +9.5 |
| Missed items (V36 Conclusion +1, D C5 0) | +1 |
| Tier 2 main-text sentences (T2-2 net 0 if it replaces the IV-B sentence; T2-4 +2; T2-5 +1; T2-1 0; T2-6 0, note in Table S1) | +3 |
| T3-1 one sentence in IV-A | +2 |
| One reference (Vardhan), if verified | +2.5 |
| **Total** | **+18** |

The plan funds about 8 (IV-B [20]/[21] sentence, III-A merge, IV-C tightening). It is short by about 10 lines. Candidate cuts, all page-neutral and content-preserving:

| Cut | Lines |
|---|---|
| Intro, last paragraph: "The approach is new in three respects: …" compress the three clauses to two sentences | −2 |
| II-E: "which computes the full velocity and pressure fields from the Navier–Stokes equations by the finite-volume method" → "(finite-volume Navier–Stokes)" | −1.5 |
| III-D, last sentence of the first paragraph: the cohort-model comparison (+0.127 / −0.0007 / +0.107, residual 0.30) → one line "In the cohort model of the same instance the error gave +0.127 (A), +0.107 (C, residual 0.30) and −0.0007 (D)." | −1.5 |
| IV-B, first paragraph: merge into the [20]/[21] paragraph | −1.5 |
| IV-A: merge "Bed structure set the magnitude…" into the preceding paragraph | −1 |
| Conclusion, last sentence: "The same test can be adapted to other pipelines, including perfusion-calibrated coronary digital twins." | −1 |
| IV-C: "These considerations follow from the results but are not validated decision rules." keep; shorten "Fourth, take most care near 0.80, where decision changes concentrated." to "Fourth, decision changes concentrated near 0.80." | −0.5 |
| Plan's own three cuts | −8 |
| **Total** | **−17** |

That funds +18 within rounding. If still short after the rebuild, reduce Fig. 1 from 0.93 to 0.88\textwidth (−2 lines; its labels are large), not Figs. 2–4, whose fonts V30 says are already at the limit. Do not move Fig. 2 to the supplement: it frees ~35 column-lines in the main text but costs the supplement more than it has.

**Abstract (limit 250; now 249–250 by word count):** T1-3 (+12), T1-4 (+5), T1-5 (−6), T1-17 (0) → net about +11. Fund with: cut "and none for caliber errors with re-derived boundary conditions" (−10), "(pooled)" (−1), and shorten the first sentence to "Fractional flow reserve can be computed from coronary computed tomography angiography" (−6). That leaves ~5 words for "at main-branch territory level" or "(a uniform narrowing)" — one of the two, not both.

**Supplement: about 40 lines free** (supp-page-6.png is ~75% empty at ~55 lines per one-column page), not 45.

| Addition | Lines |
|---|---|
| T2-1 as columns in Table S3 (+ per-cell floor column) | +3 (caption) |
| T2-2 overlap table (4 error types × DSC, clDice, AUC; by host vessel for T2) + 4 lines of text | +12 |
| T2-4 detector (AUC, sensitivity/specificity at 10%, false-alarm rate; per bed) | +8 |
| T2-5 cluster-bootstrap intervals (one small table or a note under Table S3) | +4 |
| T2-6 Table S1 note | +1 |
| T1-14 rule sentence | +1 (net 0 if the two models are excluded) |
| T3-1 territory-granularity paragraph + 6-row table | +10 |
| **Total** | **+39** |

Fits only if T2-3 is dropped (it is) and Table P is folded into S3 (it is). To create a margin of ~8 lines, scale the Fig. S1 pipeline flowchart by 0.9 and Fig. S2 by 0.9; both have headroom at one-column width. If T3-1 is dropped, the margin is comfortable.

---

## 7. Recommendation

### Ordered go-list (submit 10-15)

1. **10-09.** Zenodo package (T3-4): add results CSVs, replication outputs, CFD cases, README with versions, licence; reserve the DOI. Operator publishes on 10-14.
2. **10-09.** Decide the two conventions and record them in the log: (a) bound-hitting D fits are failed fits like C (resolves V1 + V26; n changes by two models); (b) one denominator convention (S3 basis) for Table I, S3, S5 and the text.
3. **10-09 to 10-10.** Tier 1 text fixes, with the cut list in §6 applied in the same pass so the rebuild is page-neutral. Include the missed items: one-directional caliber errors (T1-18), "under fixed boundary conditions" in IV-C, Protocol B's own number in the Conclusion (V36), "away from the stenosis throat" in the Conclusion, the T1-16 throat number.
4. **10-10.** T2-1 (columns in S3, per-cell floor), T2-6 (Table S1 note), T2-5 (cluster bootstrap).
5. **10-10 to 10-11.** T2-2 (tube-model DSC/clDice, AUC for flip, Betti-0 note), then rewrite IV-B and the Conclusion's "which overlap scores miss" to what it shows ("DSC did not separate the error types that changed decisions from those that did not; a vessel break in the RCA removed up to half the tree volume").
6. **10-10 to 10-11.** T3-1 with the corrected convention (unperfused territory = 100% mismatch) and a defined two-level partition; runs on 10-11 (~25 min). Write the supplement paragraph for the outcome obtained; one IV-A sentence.
7. **10-11 to 10-12.** T2-4 detector, including the negatives rerun for the pre-tuning residual (or the analytic noise-only residual if the rerun does not fit). Report the false-alarm rate honestly.
8. **10-12.** Integrate, rebuild, page and abstract word check (250), consistency check of every new table against the text.
9. **10-13.** Blind re-score (same rubric) and the consistency pass; fix only what the pass finds.
10. **10-14.** Upload set; operator read; publish the Zenodo record; DOI in the Data statement.
11. **10-15.** Submit.

If step 6 is not coded by 10-11 evening, drop it and rely on T1-7. If step 7 slips past 10-12 noon, report the detector on the error class only and state the false-alarm rate from the simulated-floor pass rate (28% fail after tuning), which is already in Table S7.

### Defer to the revision (keep in REVISION-PLAN-POST-SUBMISSION, in this order)
1. T5 throat error (±ΔDS, ±half voxel). Optionally run internally after step 8 so the ranking wording is known to be safe; report nothing before the review.
2. Noisy targets for corrupted models (T3-2), with a D floor.
3. Half-voxel radius correction with cohort re-selection (the clinical seat's W1; it will be asked for together with T5).
4. Graded T1/T2 severities (branch rank; 10/25/50 mm) — the proper dose response.
5. Real segmentation-failure frequency from the ImageCAS-X weights.
6. MCMC refit with D; second 3D case; mass-based demand; "taper" rename; extra references (Fleeter, Papamanolis, Montino Pelagi, Gaur, exponent literature).

### Decline (log with reasons)
- Annotator-2 masks (declined by the dataset authors 2026-09-18).
- LOGO header (template).
- Reweighting to a clinical FFR distribution (no defensible target; rates stated as conditional).
- Throat Reynolds number / lesion flow in the text (space; the ×2/×3 replication addresses the regime).
- T2-3 tertile dose response on the existing runs (flat dose; would mislead).

### Top risks
1. **T3-1 convention.** If run with the current `protocol_c_targets()` drop rule, the result will be wrong in the direction that flatters the paper. Fix the rule, record it, and expect topological passes-and-wrong to fall. The abstract must carry "at main-branch territory level" regardless.
2. **T2-2 contradicts the current overlap claim for RCA breaks.** Plan the rewrite before the numbers arrive, not after; the message is "DSC magnitude does not track decision risk", which is true and better.
3. **Abstract and main-text budgets.** Both are at the limit; a rebuild that spills to page 9 or 251 words on 10-14 cannot be fixed safely. Apply the cuts in the same pass as the additions and check after every rebuild.
4. **New inconsistencies.** Three new supplement tables and a two-model change in the D counts (if the C rule is applied) touch Table I, S3, S5, S6, Fig. 3 and five sentences. The 10-13 consistency pass must recompute every printed count from the CSVs, as the methodology seat did.
5. **Detector honesty.** The pre-tuning residual has a high false-alarm rate under physiological noise; if T2-4 is written as a positive QC rule, the DA seat will attack it. Write it as a measurement with its false-alarm rate.
6. **Schedule.** The go-list is ~4.5 person-days of analysis and writing in 5 days before the re-score; the DOI and the Tier 1 pass are the two items that must not slip, and T3-1 and T2-4 are the two to drop first if they do.

---

## 8. Final priority list and no-surprises check

Added 2026-10-09 (later the same day) at the operator's request. Everything below was verified against code, data or a scratch build in /private/tmp/claude-501/audit/ unless marked UNVERIFIED. Four statements in §§2–7 are corrected here: the page-8 slack (§8.2 f), the origin of the 13%/16% thresholds (§8.2 b), the Fig. 4 colormap feasibility (§8.2 a), and the V26 "apply the C rule to D" recommendation (§8.3, risk 3).

### 8.1 Priority list

Effort is person-hours of analysis plus writing. Page cost is main-text lines unless stated. "Headline" means the abstract's numbers, the title, or the Conclusion's claims.

**Phase A: before submission 10-15**

| Rank | What | Why (reviewer items; dimension) | Effort | Page cost | Expected effect on result/headline | Stop/drop rule |
|---|---|---|---|---|---|---|
| A1 | Zenodo deposit with reserved DOI: current code (re-strip fig5_case3d.py, which is stale), cohort list, the three results CSVs plus the two demand-replication folders, CFD packages, README with versions and run commands, licence; remove `__pycache__` | E W4, M W10, C W12, I W9, D (S8, 5/5 seats); S8 5.6 → ~7.5 | 3 h + operator publish | 0 (Data statement sentence replaces "on request") | None on results. Largest single score gain. | Must not slip. If the partner's `code_from_cfd` consent is not obtained by 10-13, deposit without it and say the OpenFOAM cases are available from the CFD co-author. |
| A2 | Tier 1 wording pass with the §6 cuts in the same edit (T1-2 to T1-13, T1-15 to T1-19 as modified in §3; plus: one-directional caliber errors; "under fixed boundary conditions" in IV-C; Protocol B's own number in the Conclusion; "away from the stenosis throat"; the T1-16 throat number). Fig. 3 caption fixed as written (see risk 3) | V1–V8, V10, V12, V15, V22–V25, V28, V36–V38; S3 5.8 → ~6.6, S5 7.8 → ~8.5 | 1 day | +10.5 lines, funded by −17 of cuts and the ~7 lines of page-8 slack now confirmed | Abstract: "directions held" becomes the exact statement; "for the error magnitudes studied" added; 3D sentence shortened. No number changes. | None; this is the floor of the submission. If a cut proves unsafe, use the page-8 slack first (≈7 lines). |
| A3 | Abstract rebalanced to exactly ≤250 words (now exactly 250): cut "and none for caliber errors with re-derived boundary conditions", "(pooled)", shorten sentence 1; add T1-3/T1-4 wording and "at main-branch territory level" | V4, V10, V15, V37, (V9) | 1 h | 0 | Headline numbers unchanged; qualifiers added. | Recount after every edit (PDF and tex both gave 250). |
| A4 | T2-1 + per-cell repeat-FFR floor as columns of Table S3; T2-6 note in Table S1; one denominator convention (S3 basis) in Table I, S3, text; S5 regenerated on that basis if replication_table.py can be changed in under 2 h, else caption | M W2/W3/W8a, E W9b, C W11, D C12; S5, S6 | 4 h | 0 main; +4 supplement | Table S5's B column shifts by ~1 point if regenerated (e.g. leaky B topological 4 → 5); III-E's "2–5%" may become "2–6%". Fig. 3 untouched. | If S5 regeneration changes any III-E range, update III-E in the same pass or keep captions instead. |
| A5 | T2-5 patient-level cluster bootstrap for the headline contrasts (A topo vs cal; P&W C/D vs B; floor) | M W3, E W10, D C10; S2 | 3 h | +1 line (II-F clause); +4 supplement | If a bootstrap interval for "P&W C/D vs B, discrete" includes 0, the "tuning raised these proportions… p < 0.001" sentence must soften to "point estimate; interval …". Unlikely (McNemar p < 0.001, 20 vs 2 of 104), but possible for the leaky caliber C contrast. | Report whatever it gives; no drop. |
| A6 | T2-2 tube-model DSC/clDice for every corrupted tree, AUC for flip, Betti-0 note; rewrite IV-B sentence and Conclusion "which overlap scores miss" | I W3, D C9, E W3 (S3, S7) | 0.5 day | 0 main (replaces a sentence); +12 supplement | **Will weaken one claim**: "vessel breaks despite high overlap" fails for RCA breaks (DSC 0.52–0.72 on the sample). Strengthens the other: DSC of T1 ≈ DSC of T4 although T1 flips 2–3× as often. Conclusion phrase becomes "which an overlap score does not rank by decision risk" or similar. | If not finished by 10-12 noon, soften the two sentences by wording alone (drop "despite high overlap scores" for breaks) and keep the analysis for the revision. |
| A7 | T3-1 territory-granularity sensitivity with the corrected convention (unperfused territory = 100% mismatch) and a two-level partition; supplement paragraph + table; one IV-A sentence | C W2, D C1, E W5, M W7, I W6 (S2, S4); the strongest DA argument | 0.5–1 day code + 23 min runs | +2 lines; +10 supplement | **Likely direction: topological passes-and-wrong falls sharply at finer granularity; taper passes-and-wrong unchanged.** Abstract keeps 19–20% with "at main-branch territory level"; IV-A gains "at a segment-level partition the missed branch formed its own territory and failed the check; the taper still passed while wrong". Conclusion's "one in five" gets the same clause. | Decide convention on 10-10. If the wrapper is not validated by 10-11 evening, drop; T1-7 wording carries the scope. Never run with the current drop rule. |
| A8 | T2-4 QC detector: AUC/sensitivity/specificity of the Protocol B residual and \|log C ratio\| for (i) error class and (ii) flip, per bed; false-alarm rate from the floor's pre-tuning residual (negatives.py rerun, 2-line change, 44 min) | E W3, I W4 (S7) | 0.5–1 day | +2 lines (IV-C); +8 supplement | Honest result: strong for class in the discrete bed (B residual median 0.196 vs 0.021), weak in the leaky bed (0.027 vs 0.012), and a high false-alarm rate under physiological noise (only 72% of correct-anatomy draws pass even after tuning). IV-C "Third, record the perfusion mismatch" gains "in the discrete bed" and the false-alarm figure. Conclusion's "a record of the perfusion mismatch before tuning" stays. | If the rerun does not fit by 10-12, report class-AUC only and quote the Table S7 28% post-tuning failure rate as the false-alarm bound. |
| A9 | Fig. 2 note "(D in Table I)", Fig. 3 vertical line at 0.10, fonts enlarged where scripts allow (Figs 1–3 render at 7 pt on 7.16 in and are printed at 0.93 width ≈ 6.5 pt; IEEE asks ≥ 8 pt) | E W9d, I W8 (S6) | 2 h | 0 if figure sizes unchanged | None on results. | Fig. 4 colormap is NOT changeable locally (see 8.2 a): ask the CFD side for a viridis re-render by 10-12 or leave turbo and log it. |
| A10 | Blind re-score and consistency pass (recompute every printed count from the CSVs, including the new tables) | S5 | 1 day (10-13) | 0 | Catches the knock-ons from A4–A8. | Fix only what it finds. |
| A11 | Optional, only if A1–A10 are done by 10-12: run T5 (throat ±ΔDS) internally; report nothing | prepares B1; protects the ranking wording | 0.5 day | 0 | If T5 flips at topological rates, the Conclusion's ranking sentence should already carry "away from the stenosis throat" (A2), so no change is forced before submission. | Drop without consequence. |

**Phase B: after submission / revision**

| Rank | What | Why | Effort | Page cost (revision; pp. 9–10 billable) | Expected effect | Stop rule |
|---|---|---|---|---|---|---|
| B1 | T5 throat caliber error (±ΔDS from CT-vs-QCA variability; ±half voxel), A–D, both beds | 5/5 seats (C W3, I W2 iv, D C3, E W1/W6, M W4); S2, S4 | 1 day + 15 min runs + 0.5 day citations | +0.5 page | **Likely reframes the ranking**: "branching and the throat carry the decision risk; caliber elsewhere does not". Abstract sentence 1 and the Conclusion change; title unaffected (topology remains the subject). | None; required. |
| B2 | Corrupted models tuned to the 20 noisy target draws (T3-2) with a Protocol D floor | E W2, M W1, D C4; S2 | 1 day code + 4 h runs | +0.3 page | Replaces 19–20% / 5–8% with per-draw rates; expect lower pass rates (lower P&W) under C, D unchanged. The floor comparison becomes like-for-like. | None; required. |
| B3 | Half-voxel radius correction with cohort re-selection | C W1, E W6, D C3; S4 | 2 days | +0.3 page | Changes every number; raises demand, lowers baseline FFR; expect the direction to hold (×2/×3 replication already shows it). | If the discrete arm loses eligibility as at ×3, report the leaky bed only. |
| B4 | Graded T1/T2 severities (branch rank largest/median/smallest; break at 10/25/50 mm) and the lost-bed-fraction axis | E W1, I W1, D C2, C W3 | 1 day + runs | +0.3 page | A proper dose response. The existing-run dose is flat (Spearman −0.10 to +0.41), so expect "flip depends on baseline proximity more than on branch size" unless graded by design. | — |
| B5 | Real segmentation-failure frequency from the ImageCAS-X weights (post-submission plan §1) | E W1, I W2 | 2–3 days + GPU | +0.5 page | Turns "impact" into "risk"; if rates are < 2% the clinical framing weakens; report either way. | — |
| B6 | MCMC refit including D; VI-vs-Laplace check | E W10, M W3 | 0.5 day | 0 | Interval widths; no headline change. | — |
| B7 | Second 3D case with the throat matched to the ROM radius; "taper" rename; extra references (Vardhan, Gaur, Fleeter, Papamanolis, Montino Pelagi, exponent literature); mass-based demand sensitivity | M W5, C W7/W9, E W11, I W8 | weeks (3D) / hours (rest) | +0.2 page | Fidelity and positioning only. | 3D case only if reviewers ask. |

### 8.2 No-surprises check

| Item | Status | What was checked / what would confirm it |
|---|---|---|
| (a) Fig. 4 CFD field data for a colormap change | **VERIFIED: not available locally.** | fig5_case3d.py l.62–66 loads `drafts/stageA_validation/figures/img_m1_wall_pressure.png` (87 KB, a rendering returned by the CFD side, "reversed turbo map over 0.86–1.00") and crops it; the colour bar is redrawn natively. No VTU/field files exist in cfd_handover/ (only centreline.vtp, probes/outlets CSVs, logs, JSON) or in results/cfd_*. A viridis version needs a re-render on the CFD machine. T1-19 is corrected accordingly in A9. |
| (b) Origin of the 13% and 16% thresholds | **VERIFIED, and my T1-15 guess ("1.3× and 1.6×") was wrong.** | protocol/STATISTICS-PLAN.md §P2 l.99–105, protocol/DETECTOR-SPEC.md B4, references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md: the published regional repeatability coefficient (18–23%) is a bound on the difference of *two* noisy measurements; our residual compares one deterministic output with one measurement, so the 95% bound is RC/√2 ≈ 0.13–0.16; 0.10 is stricter and conservative for the passes-and-wrong proportion (monotone in the threshold). The II-F sentence should say: "Thresholds of 13% and 16%, the 95% bound for one model output against one measurement implied by the published regional repeatability coefficients, were analyzed as sensitivities." Note a latent inconsistency: II-F currently derives "20–29%" from 1.96 × wsCV (10–15%), while the protocol's own derivation gives 13–16% from the RC; both say 10% is stricter, but the two numbers should not both appear without the link. One clause fixes it. |
| (c) Two-level territory partition implementable; runtime | **VERIFIED (design and runtime); code not written.** | `territories()` (ablation.py l.155) is a module-level function consumed by `protocol_c_targets()` (l.101–127) and, through `A.protocol_c_targets`, by ablation_per_territory.py l.68; negatives.py imports its own `territories`. A wrapper that monkeypatches `A.territories` reaches both C and D without editing the frozen files. Required changes: (1) new partition: split each first-level subtree at its own first branching node; the trunk between the two levels becomes a territory of its own (its clean target is its wall outflow; in the discrete bed non-leaf w = 0, so the existing `q_clean > 0` filter drops it, which is consistent with the current treatment of the root trunk); (2) the drop rule `if q_clean > 0 and len(members)` must keep territories with a positive target and no members, so that `qb[members].sum() = 0` enters the residual as −1 (100% mismatch) — ablation.py's residual loop already handles an empty index array; (3) in ablation_per_territory.py `apply()`/`resid()` iterate over t_pairs jointly, so empty-member territories must be excluded from the parameter vector but kept in the residual (a 10-line refactor); (4) definedness stays "≥ 2 territories with surviving members". Runtime from the logs: ablation 764 s (150 instances, both beds, A–C) + per-territory 599 s = **23 min**. Validation needed: with the two-level partition on a tree whose second-level bifurcations are absent, the result must reduce to the current one. Effort 0.5–1 day. |
| (d) negatives.py can emit the pre-tuning residual; runtime | **VERIFIED.** | `fit_global_scaling()` (negatives.py l.148–163) already evaluates the loss on a 61-point grid whose centre `grid[30]` is `C_start`, the re-derived calibration of the clean tree, i.e. the Protocol B state; `sqrt(lv[30])` is the pre-tuning RMS residual against the noisy targets. Returning it and writing one column is a 2-line change (ablation.py already records the analogous `fit_loss_at_Cstart`). Full rerun: 2 622 s (**44 min**) for 5 860 draws, seed 20260919, reproducible. |
| (e) Deposit package: size, content, redistribution | **VERIFIED with four actions needed.** | Size: deposit-2026-10-08 is 368 KB; adding ablation CSVs (1.7 + 15 + 1.2 MB), per-territory (0.4 MB), negatives (2.5 + 4.0 MB), demand replications (3.6 + 3.2 MB) and CFD packages (1.6 MB) gives ≈ 33 MB, far under Zenodo limits. Content: no absolute paths, no AI/assistant names, no internal review-document references in the deposit code (grep for `/Users/`, Claude, Fable, Codex, GPT, Gemini, review, STATISTICS-PLAN, DETECTOR-SPEC: zero hits except one harmless "given here for audit" string in export_cfd_case.py). The copies are docstring-stripped; an AST comparison with strings blanked shows logic identical to the frozen code except removed print statements and one removed metadata key, **but fig5_case3d.py is stale** (lacks the 10-08 throat close-up box and connection lines), so it would not regenerate Fig. 4 as published. Cohort CSV: scan IDs plus ImageCAS-X descriptor columns (quality, dominance, disease); ImageCAS volumes are Apache 2.0 (Kaggle) and ImageCAS-X annotations CC BY 4.0 (Zenodo 10.5281/zenodo.21887809), so IDs and descriptors may be redistributed with attribution; no personal data. Actions: (1) re-strip the current fig5_case3d.py; (2) delete `code/__pycache__` (5 files); (3) add README (versions, commands, data pointers) and LICENSE (none exist); (4) the pullback CSVs (19 MB) are model predictions that the pipeline notes say must not be *sent to the CFD side before their runs*; publishing them after the fact is fine, but confirm the operator wants them. UNVERIFIED: whether `cfd_handover/code_from_cfd` (6 MB, the CFD co-author's code) may be deposited; needs that co-author's consent. |
| (f) Abstract word count; main-text slack | **VERIFIED, and §6's "zero slack" is corrected.** | Scratch build in /private/tmp/claude-501/audit/build (copy of drafts/manuscript; pdflatex + existing .bbl): 8 pages main, 6 pages supplement. Abstract: 250 words from the PDF text and 250 tokens from the .tex (texcount agrees), so the limit is exactly met and every added word needs a cut. Page 8 text bounding boxes: left column ends at y = 749 pt (full), **right column ends at y = 660 pt, i.e. ≈ 90 pt ≈ 7–8 lines of body text free**, confirmed on ms-page-8.png (the right column stops at reference [33] about eight lines above the left column's end). Supplement page 6: lowest text at y = 227 pt → ≈ 41 lines free at 12 pt. Net: the §6 budget of −17 cut lines against +18 added is now comfortable (+7 slack); the supplement budget (+39 against 41) remains tight. |
| (g) Outcomes that could force title/abstract/conclusion changes | Listed in §8.3. | — |
| Runtimes quoted in §3 (ablation ≈ 5 s/instance, D ≈ 3.3 s/instance) | **VERIFIED** | Logs: 764 s / 150 and 599 s / 150. Negatives 2 622 s / 5 860 draws. |
| Table P, V1, V2, V5, V7, V9, V11, V24, V26, V27, V32 | **VERIFIED** (§2) | Recomputed from the CSVs and the source. |
| T2-2 nesting (corrupted ⊂ clean for T3) | **VERIFIED numerically on 12 instances** (`r_t3 ≤ r_clean` everywhere) and analytically (§3). | Full-cohort run will confirm; if any instance violates it, the DSC formula is still valid (it uses volumes of the two tubes and their intersection; for nested tubes the intersection is the corrupted tube). |
| T2-3 flat dose | **VERIFIED** | Spearman(\|ΔFFR\|, lost inflow fraction) under A: T1 discrete −0.10 (p 0.38), T1 leaky +0.15 (p 0.09), T2 leaky +0.41 (p 3e−7); T2 discrete undefined (constant). Tertile flip rates non-monotone in all four cells. |
| Figure fonts | **VERIFIED below IEEE's 8 pt** | fig_results.py, fig1_errors.py, fig5_case3d.py render at 7 pt (labels 5.8–6.5 pt) on 7.16 in and are placed at 0.93\textwidth. Enlarging is a script change for Figs 1–3; Fig. 4's matplotlib labels can be enlarged but its (a)–(d) panels are a PNG. Do not shrink figures to fund lines. |
| S5 regeneration on the S3 denominator basis | **UNVERIFIED** | replication_table.py has no basis flag and no obvious denominator switch (grep for notna/undefined/argparse found nothing). Confirm by reading how it counts P&W; if it is a one-line change, do it; else use captions (T1-12 fallback). |
| Fig. 1(d) inset | **UNVERIFIED** | fig1_errors.py l.81–95 plots the three radius profiles in one axis; an inset is ~20 lines of matplotlib. Optional. |
| Vardhan et al. 2019 (Sci Rep) and Gaur et al. 2014 (Eur Heart J) bibliographic details | **UNVERIFIED** (no literature access used in this audit) | Verify before citing, as the plan says. |
| JBHI SI limits (14 pp incl. supplement; 250-word abstract) | **UNVERIFIED by me** | Taken from PLAN.md; the CFP/author guide PDFs in the project root would confirm. |
| Funding statement | **UNVERIFIED** (operator fact) | — |

### 8.3 Known risks to the title, abstract numbers or conclusions (with likely direction)

1. **T3-1 (A7): topological passes-and-wrong falls at finer granularity.** Direction: weakens the generality of "19–20% (discrete) and 5–8% (leaky)" and the Conclusion's "one in five"; strengthens the caliber (taper) passes-and-wrong finding. Forced change: the clause "at main-branch territory level" in the abstract and Conclusion, one IV-A sentence. Title unaffected. If the opposite happens (topological P&W persists), nothing changes except a robustness sentence.
2. **T2-2 (A6): the overlap claim must be qualified.** Direction: the Conclusion's "a check of the branching near the lesion, which overlap scores miss" and IV-B's "vessel breaks … despite high overlap scores" become "DSC did not rank the error types by decision risk (T1 ≈ T4), and a break in the RCA removed up to half the tree volume". Also exposes that the applied T4 corresponds to a tube-DSC ≈ 0.97, above the 0.928 it was derived from; one caption clause explains it (the narrowing is applied from the lesion onwards only).
3. **V26 rule (correction to §2/§3).** Applying the Protocol C bound rule to the two scan-984 D fits would change n in Table I (T1-D discrete 44 → 42), the pooled D cell (21/104 → 21/102 = 20.6%), and hence the abstract's "19–20%" to "19–21%", and would unpair C from D on two instances. For the deadline, **do the caption fix as written in PLAN T1-1** ("except two models at 0.08 and 0.11") and make the S2 rule explicit: a D fit at the bound is retained because its residual remains defined and is scored by the check, whereas a C fit at the bound has an unidentified single parameter. No number changes. Record it as a decision.
4. **T1-12 single convention (A4).** Regenerating S5 on the S3 basis moves B-column values by about one point and may change III-E's "2–5% … with re-derived boundary conditions" to "2–6%". Abstract unaffected.
5. **T2-4 (A8): the pre-tuning residual is a weak detector in the leaky bed and false-alarms under noise.** Direction: IV-C's third consideration and the Conclusion's "a record of the perfusion mismatch before tuning" survive with "in the discrete bed" and the false-alarm figure attached; no number in the abstract changes.
6. **T2-5 (A5): a cluster-bootstrap interval could include zero for a contrast the text calls significant.** Most exposed: leaky caliber C vs B (37 vs 0 of 300, safe) and discrete topological C vs B (20 vs 2 of 104, safe); the leaky topological C vs B is already reported as not significant. Low risk.
7. **T2-6: A-T2 discrete flips 40% → 43% as a sensitivity.** Not a headline number; the "3–6×" ratio is unchanged in direction.
8. **Abstract at exactly 250.** Every A2/A3 edit must be word-neutral; the proposed cuts give ~17 words of room.
9. **Title.** No Phase A item touches it. B1 (T5) could later move emphasis to "branching and throat", which still fits the present title.

### 8.4 Decisions the operator must make

1. Publish the Zenodo record (A1), and whether to include the pullback CSVs and the CFD co-author's `code_from_cfd` (needs that co-author's consent).
2. V26: caption fix with no number changes (recommended), or exclude the two bound-hitting D fits (changes n and the abstract to 19–21%).
3. Run T3-1 with the 100%-mismatch convention (A7) and accept the "main-branch territory level" clause in the abstract either way.
4. Run T2-2 (A6) knowing it will qualify the "overlap scores miss" wording.
5. Rerun negatives.py (44 min) for the pre-tuning residual (A8), or report the detector on class only.
6. Denominator convention: regenerate S5 (numbers shift by ~1 point) or captions.
7. Fig. 4: request a viridis re-render from the CFD side by 10-12, or keep turbo and log it.
8. Funding statement text (V33).
9. Add Vardhan 2019 (after verification) at ~2.5 lines, now affordable from the page-8 slack, or defer.
10. Optional internal T5 run (A11).

### 8.5 Could not verify
- replication_table.py's denominator code path (whether an S3-basis regeneration of Table S5 is a one-line change).
- Consent to deposit `cfd_handover/code_from_cfd`.
- Bibliographic details of Vardhan 2019 and Gaur 2014.
- The JBHI SI page/abstract limits (taken from PLAN.md; CFP PDF not read).
- Whether the IEEE production check will object to the 6.5-pt effective figure fonts (it usually does at proof stage, not at review).
- That the scratch build equals the 10-08 23:05 upload build (same .tex and .bbl were used; the page images match; a byte-level comparison was not made).

---

## 9. Refinement against JBHI practice

Added 2026-10-09 after reading JBHI-PRACTICE-BENCHMARK.md (20 JBHI papers 2024–2026, open-access sample; mechanistic in-silico n = 3, modelling n = 6), the operator's preference (no figure scripts, no case files, no data extracted from other datasets), and the JBHI guide's confirmed limit (14 pages including supplementary material).

### 9.1 (a) A1 re-decided: what to release

Facts that bear on it:
- Benchmark: public code 8/20 (33% of modelling papers); "on request" 0/20; nothing stated 12/20; the three mechanistic models released nothing; no depositor had a DOI; 8 of 9 depositors released only their own method code; 0 released figure scripts or case files; 1 released re-processed third-party data.
- Policy: IEEE "encourages" sharing; JBHI requires only that public data sources be cited. No mandate.
- Reviewer pressure: all five blind seats raised code (E W4 "cheapest and most valuable change", M W10, C W12, I W9, D S8), and the paper's own Conclusion says "the same test can be adapted to other pipelines", which is a reuse claim. The paper also cites Viceconti's credibility position paper [33]. A referee for a digital-twin credibility special issue is more likely than the modal JBHI referee to ask.
- Operator preference: own analysis code only; no figure scripts, no case files, no extracted data.
- Verified in §8.2(e): the stripped copies in deposit-2026-10-08/code are logic-identical to the frozen code; the pipeline files are ours; `cfd_handover/code_from_cfd` is the CFD co-author's; the cohort CSV carries three ImageCAS-X descriptor columns (quality, dominance, disease; CC BY 4.0, redistributable with attribution but "extracted data" under the operator's rule).

| Option | What it contains | Effort | Fits benchmark? | Fits operator rule? | Likely S8 (panel mean) | Residual reviewer risk |
|---|---|---|---|---|---|---|
| O1. "On request", precisely worded | Statement naming what exists: analysis code (error models, reduced-order solver, protocols, statistics) and the cohort list (scan ID, side, host vessel, lesion position, length, DS) | 15 min | Yes (0/20 say it, but 60% say nothing; it is ahead of the modal paper) | Yes | 5.8–6.0 | High for this SI: 5/5 seats; the EIC seat scored S8 = 5 on exactly this; "reusable test" claim unsupported |
| O2. Own analysis code + cohort design list, public GitHub, MIT; optional Zenodo DOI snapshot | zerod_ffr.py, error_types.py, severity_sweep.py, imagecasx_loader.py, discrete_arm.py, ablation.py, ablation_per_territory.py, ablation_demand_scale.py, demand_replication.py, negatives.py, grey_zone.py, analyse_ablation.py, summarise_revision.py; COHORT list reduced to scan, side, vessel, loc, c_mm, L_mm, ds_pct, band; README (versions, commands, data pointers); LICENSE. Excluded: fig*.py, table2.py, supplement_tables.py, replication_table.py, demand_table.py (figure/table scripts), export_cfd_case.py, ingest_cfd_radius.py, m1_zerod_vs_3d.py (CFD bridge), the CFD co-author's code, all result CSVs, the ImageCAS-X descriptor columns | 2–3 h (strip already done; add README/LICENSE; delete `__pycache__`; smoke-run `ablation.py <root> --limit 2` from the repo) | Yes: matches what 8 of 9 depositors did | Yes | 6.8–7.0 (7.0–7.2 with a DOI snapshot) | Low: a referee can rerun every table from the public data; "per-model outputs" (M W10) remain on request |
| O3. Full deposit as in PLAN T3-4 (code + figure scripts + results CSVs + CFD cases + DOI) | Everything in deposit-2026-10-08 plus results and cfd_handover | 3 h + consents | Exceeds every paper in the sample | No | 7.5–7.6 | Lowest, but needs the CFD co-author's consent and publishes 19 MB of model predictions the operator does not want out |

**Recommendation: O2.** It is the benchmark-typical release (own method code, plain repository), it satisfies the operator's rule exactly, it answers the only unanimous reviewer item at a cost of one afternoon, and it leaves nothing that could be challenged later (no third-party data, no co-author code, no case files). Add the Zenodo DOI snapshot only if the operator does not mind; it is ten minutes, IEEE's Author Center names Zenodo, and reviewers read a DOI as permanence, but no benchmark paper had one, so it is optional. Data statement (Data and Code Availability, 0 net lines):

> "The data that support the findings of this study are the public ImageCAS [22] and ImageCAS-X [23] datasets (CC BY 4.0). The analysis code (segmentation-error models, reduced-order solver, boundary-condition protocols and statistical analysis) and the cohort list are available at <URL>."

If the operator declines any release, use O1 with the precise wording above; it is still ahead of the modal JBHI paper, and the release can be made at revision.

### 9.2 (b) Every other item re-checked against JBHI practice

Where the paper already exceeds the norm, the item is marked so that effort can be cut.

| Item | JBHI norm (benchmark) | Our current state | Decision |
|---|---|---|---|
| Confidence intervals | 2/20 report CIs; 0/6 modelling | Wilson CIs on every proportion | **Exceeds norm.** No change. |
| Clustering handled | 4/20; 0/6 modelling | CIs declared descriptive; Bayesian mixed model with patient and slot random effects (Table S2) | **Exceeds norm.** The remaining objection (M W3, V21) is one sentence that uses a lower bound inferentially. **A5 (cluster bootstrap) moves to Phase B**; replace the sentence now: "Only the taper's rate lay above the 5.0–6.5% floor, in the discrete bed under fixed boundary conditions (13%) and Protocol D (14%)." Saves 3 h, 1 main line and 4 supplement lines. |
| Multiplicity | 2/20 | Holm within triplets | **Exceeds norm.** Keep T1-13 (label p-values; 0 lines). The EIC's "state the family-wise scope" is one clause, already in II-F. |
| Inferential tests | 8/20 | McNemar, sign, Wilcoxon, mixed model | Exceeds norm. No change. |
| Supplementary material | 5/20 | 6 pages: exclusions, mixed model, four sensitivity tables, floors, mesh checks | **Exceeds norm.** The empty 70% of page 6 need not be filled for its own sake; only A4, A6, A7, A8 content goes there. |
| Mesh/GCI, convergence, mass-conservation reporting | Not seen in the 3 mechanistic papers | Reported, including a failed acceptance criterion | Exceeds norm. T1-6 (state the failed criterion in the main text) is still right: it is a consistency item, not a norm item. |
| Sensitivity and replication (demand ×0.7/×1.3, ×2/×3 re-selection, thresholds, grey zone) | Rare (#1 has sensitivity analyses) | Four sensitivity tables and two replications | Exceeds norm. T1-15 pointer only. |
| Pass/P(wrong \| pass) table (A4) | n/a | Missing | Keep: it corrects a bed-unqualified sentence (V2) and costs 4 h, 0 main lines. |
| Overlap metrics (A6) | Not a reporting norm; segmentation papers report DSC routinely | Claim asserted, unmeasured; sample shows it is partly wrong (RCA breaks) | **Keep, for integrity not norm**: the text currently asserts a measurable thing that the authors can now see is wrong for one case. Cheapest honest alternative if time fails: wording only (drop "despite high overlap scores" for breaks; keep "a missing side branch removes few voxels", which the sample supports). |
| Detector analysis (A8) | Not a norm; JBHI methods papers report AUC/sensitivity/specificity as their main result | Four qualitative "considerations" | **Keep, as the venue-fit deliverable** (S7; EIC W3 says the paper otherwise fits IJNMBE/ABME). Reduce if needed to class-AUC plus the Table S7 false-alarm bound (3 h) and skip the 44-min rerun. |
| Territory sensitivity (A7) | Not a norm | Scope unstated | Keep as an operator decision; it is a scientific-risk item (strongest DA argument), not a reporting item. T1-7 wording is the floor. |
| Dose response (T2-3) | Not a norm | Flat in the data | Dropped (§8). |
| Zero-outflow A-T2 as flips (T2-6) | Not a norm | 1 h, one supplement line | Keep (cheap, answers M W8d), or drop without loss. |
| Figure fonts (A9) | JBHI figures at 6–7 pt are common in the sample's PDFs | 6.5 pt effective | **Defer to proof** unless the script change is trivial; keep the Fig. 3 line and Fig. 2 note (10 min). |
| Fig. 4 colormap | Not a norm item | PNG from the CFD side | Leave turbo; log the reason. |
| Data statement placement | Separate section in 5/20 (all 2024–2026) | Separate section exists | No change. |
| MCMC refit (B6) | 0/20 | VI intervals, declared | **Drop unless a reviewer asks.** |
| Second 3D case (B7) | 0/3 mechanistic papers had more | One case | Only if asked. |
| Extra references (Vardhan, Gaur, Fleeter, perfusion-coupled models) | n/a | 33 references | Vardhan 2019 only, after verification; it is the one directly on-topic omission the clinical seat named. |

### 9.3 (c) Refined final plan

**Phase A: before submission 10-15** (ordered; effort in person-hours; page cost in main-text lines unless stated; the page-8 slack is ≈ 7 lines, the supplement has ≈ 41 lines)

| Rank | What | Fixes | Effort | Page cost | Risk to headline | Drop rule |
|---|---|---|---|---|---|---|
| A1 | Own analysis code + cohort design list on public GitHub (MIT), README, LICENSE; optional Zenodo DOI; Data statement as in §9.1 | 5/5 seats; S8 | 3 h | 0 | None | If not approved by 10-13: O1 wording. |
| A2 | Tier 1 wording pass with the §6 cuts; Fig. 3 caption fix as in PLAN T1-1 (no number change); missed items (one-directional caliber errors, "under fixed boundary conditions" in IV-C, Protocol B's own number in the Conclusion, "away from the stenosis throat", the T1-16 throat number); 13%/16% origin stated as in §8.2(b); lower-bound sentence reworded (replaces A5) | V1–V8, V10, V12, V15, V21–V25, V28, V36–V38; S3, S5 | 8 h | +10 lines, funded by cuts and slack | None (wording only) | None. |
| A3 | Abstract edits, word-neutral at 250 | V4, V10, V15, V37 | 1 h | 0 | None | Recount after every edit. |
| A4 | Pass n, P(wrong \| pass) and per-cell floor as columns of Table S3; T2-6 note in Table S1; one denominator convention (S3 basis) in Table I, S3 and text; S5 regenerated on that basis if a small change, else caption | V2, V3, V5, V21, V27 | 4 h | 0 main; +4 supplement | S5 B column ±1 point; III-E "2–5%" may become "2–6%" | If S5 cannot be regenerated in 2 h, caption. |
| A5 | T2-2 tube-model DSC/clDice, AUC for flip, Betti-0 note; rewrite the IV-B sentence and the Conclusion's "which overlap scores miss" | V13 (I W3, D C9, E W3); S3, S7 | 4 h | 0 main; +12 supplement | **Weakens** "vessel breaks despite high overlap" (RCA DSC 0.5–0.7); strengthens "DSC does not rank error types by decision risk" | If not done by 10-12 noon: wording only. |
| A6 | T3-1 finer-territory sensitivity with the 100%-mismatch convention and a two-level partition; supplement paragraph + table; one IV-A sentence | V9 (5 seats); S2, S4 | 6–8 h + 23 min runs | +2 main; +10 supplement | **Likely lowers topological passes-and-wrong at finer granularity**; abstract and Conclusion gain "at main-branch territory level" (added anyway) | Decide 10-10; if not validated by 10-11 evening, drop; T1-7 carries the scope. Never run with the current drop rule. |
| A7 | T2-4 detector: AUC of the Protocol B residual and \|log C ratio\| for error class and for flip, per bed; false-alarm rate from the negatives rerun (2-line change, 44 min) or from Table S7's 28% post-tuning failure rate | V19 (E W3, I W4); S7 | 4–6 h | +2 main; +8 supplement | IV-C's third consideration gains "in the discrete bed" and the false-alarm figure; no abstract change | If the rerun does not fit by 10-12: class-AUC + Table S7 bound. |
| A8 | Fig. 3 line at 0.10; Fig. 2 note "(D in Table I)" | V30 | 0.5 h | 0 | None | — |
| A9 | Integrate, rebuild, page/abstract check | — | 4 h (10-12) | — | — | — |
| A10 | Blind re-score (same rubric) + consistency pass recomputing every printed count from the CSVs | S5 | 1 day (10-13) | 0 | Catches knock-ons from A4–A7 | Fix only what it finds. |
| A11 | Upload set; operator read; publish repository; submit | — | 10-14/15 | — | — | — |
| A12 (optional) | Internal T5 run, unreported | protects the ranking wording | 4 h | 0 | None before submission | Only if A1–A10 are done by 10-12. |

Total Phase A: about 4 person-days of analysis and writing plus the re-score day, in the six days available; A6 and A7 are the first to drop if it slips.

**Phase B: revision**

| Rank | What | Why | Effort | Page cost (revision) | Risk to headline | Stop rule |
|---|---|---|---|---|---|---|
| B1 | T5 throat caliber error (±ΔDS, ±half voxel), A–D, both beds | 5/5 seats; S2, S4 | 1.5 days | +0.5 page | **Likely reframes the ranking** to "branching and the throat"; abstract sentence 1 and the Conclusion change; title stands | Required. |
| B2 | Corrupted models tuned to the noisy draws, with a D floor | E W2, M W1, D C4; S2 | 1.5 days | +0.3 page | Replaces 19–20% / 5–8% with per-draw rates; floor becomes like-for-like | Required. |
| B3 | Half-voxel radius correction with cohort re-selection | C W1, E W6, D C3; S4 | 2 days | +0.3 page | Every number changes; direction expected to hold | Leaky bed only if the discrete arm loses eligibility. |
| B4 | Graded T1/T2 severities and the lost-bed-fraction axis | E W1, I W1, D C2, C W3 | 1 day | +0.3 page | Proper dose response | — |
| B5 | Real segmentation-failure frequency from the ImageCAS-X weights | E W1, I W2 | 2–3 days + GPU | +0.5 page | Converts impact to risk; report either way | — |
| B6 | Patient-level cluster bootstrap for the headline contrasts (moved from A5) | M W3 | 3 h | +0.1 page | Low | Only if a reviewer asks; the paper already exceeds the JBHI norm here. |
| B7 | Per-model outputs on request; MCMC refit; second 3D case; "taper" rename; further references; mass-based demand | M W10, E W10, M W5, I W8, C W9, E W11 | hours to weeks | +0.2 page | None | Only if asked. |

**Updated score projection (panel mean, refined plan with A1 = O2 without DOI; ±0.5 per dimension)**

| Dim | Now | §5 "Mine" | Refined | Reason for the change |
|---|---|---|---|---|
| S1 Novelty | 6.8 | 6.9 | 6.9 | Unchanged. |
| S2 Rigour | 6.0 | 6.6 | 6.5 | Cluster bootstrap deferred (−0.1); the paper already exceeds the JBHI norm on inference, so the loss is small. |
| S3 Claims vs evidence | 5.8 | 6.8 | 6.8 | Unchanged; the overlap claim is corrected, the lower-bound sentence reworded. |
| S4 Physiology | 6.0 | 6.4 | 6.4 | Unchanged. |
| S5 Consistency | 7.8 | 8.5 | 8.5 | Unchanged. |
| S6 Clarity | 7.0 | 7.0 | 7.0 | Unchanged. |
| S7 Venue fit | 6.4 | 7.0 | 7.0 | Detector and overlap results kept. |
| S8 Reproducibility | 5.6 | 7.5 | 7.0 | Own code + cohort list on GitHub, no results or cases; 7.2 with a DOI snapshot; 5.9 under O1. |
| **Overall** | **6.4** | **7.0** | **6.9** | Expected split: EIC and methodology "minor/major", clinical and DA "major" (T5, noise symmetry, radius). With O1 instead of O2: 6.8. |

### 9.4 (d) Remaining operator decisions, with recommended answers

| # | Decision | Recommendation |
|---|---|---|
| 1 | Release code? Scope? | **Yes, O2**: own analysis code (13 files listed in §9.1) + cohort design list (8 columns), MIT, public GitHub. No figure scripts, no result CSVs, no CFD cases, no co-author code, no ImageCAS-X descriptor columns. |
| 2 | Zenodo DOI snapshot of the repository? | Yes if indifferent (10 min; IEEE names Zenodo; reviewers read a DOI as permanent); no benchmark paper had one, so "no" costs ~0.2 on S8 only. |
| 3 | V26: caption fix (no number change) vs. excluding the two bound-hitting D fits (abstract 19–20% → 19–21%)? | **Caption fix**, with the S2 rule stated explicitly. |
| 4 | Run A6 (finer territories) with the 100%-mismatch convention? | **Yes**, provided the wrapper is validated by 10-11 evening; the abstract clause "at main-branch territory level" goes in regardless. |
| 5 | Run A5 (overlap metrics) knowing it qualifies the "overlap scores miss" claim? | **Yes**; the current sentence is now known to be wrong for RCA breaks, and the corrected message is stronger. |
| 6 | A7 with the 44-min negatives rerun, or class-AUC only? | **With the rerun** (2-line change); fall back to class-AUC + Table S7 bound if 10-12 is reached. |
| 7 | Cluster bootstrap now or at revision? | **Revision** (B6); reword the lower-bound sentence now. |
| 8 | Denominator convention: regenerate S5 or captions? | Regenerate if under 2 h; otherwise captions. |
| 9 | Fig. 4 colormap | **Leave turbo**; log that the panels are CFD-side renders. |
| 10 | Figure fonts | **Defer to proof** unless trivial. |
| 11 | Add Vardhan 2019? | **Yes**, after verification, from the page-8 slack (2.5 lines). |
| 12 | Funding statement | Operator fact; "This work received no specific funding" if none. |
| 13 | Internal T5 run before submission (A12)? | Only if A1–A10 are finished by 10-12; otherwise first task after submission (B1). |
| 14 | "On request" fallback wording if no release | "The analysis code (segmentation-error models, reduced-order solver, boundary-condition protocols and statistical analysis) and the cohort list (scan identifiers, host vessel, lesion position, length and diameter stenosis) are available from the corresponding author on request." |
