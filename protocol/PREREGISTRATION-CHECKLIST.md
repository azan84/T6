# Pre-registration — what to lodge, and what is already locked

**Prepared 2026-09-18; revised 2026-09-19 after four blocking items were closed and nine defects were fixed.**
Everything below exists; this is an assembly and submission checklist, not new work. Target: OSF (or AsPredicted).
Register **before** any A/B/C ablation run.

## 1. What goes into the registration

| Section of the OSF form | Source in this repository |
|---|---|
| Title, authors | `STUDY-PLAN-v2.md` §7b — **five** authors in order, with a CRediT block table and a corresponding author. A registration may list the authors known at the time; adding one later is a normal amendment, not a deviation — but it must then be declared with its date, so any further author is materially cheaper added now |
| Research questions / hypotheses | `STUDY-PLAN-v2.md` §4 — H1–H6, each with its counter-hypothesis. H7 is a planned amendment (§13), not part of this registration |
| Study type | Computational / in-silico; simulation study on a public dataset; no human-subject contact |
| Data | **ImageCAS-X annotation layer only** — centrelines, voxel segmentations, surfaces, `Descriptors.xlsx` (Zenodo 10.5281/zenodo.21887809). **The ImageCAS CT image volumes are NOT required by this design and are NOT held**: the 0D pipeline reads centrelines + masks, and the 3D arm reads masks. *(Corrected 2026-09-19 — the previous version of this checklist claimed both were downloaded.)* **LICENCE VERIFIED 2026-09-19 on the Zenodo record itself**, not from a paper: *"Creative Commons Attribution 4.0 International"*, verbatim, applying to the record's files. **DOI 10.5281/zenodo.21887809, v1, published 11 August 2026 — cite the version, not just the concept DOI.** Note the record also holds `pretrained_weights.zip` (1.6 GB, six benchmarked segmentation methods) which we have NOT downloaded and do not need for this design; it is D1c's self-serve fallback (`STUDY-PLAN-v2` §6) |
| Cohort | `COHORT-FROZEN-2026-09-18.csv` (150 instances) and `CFD-SUBSET-FROZEN-2026-09-18.csv` (30) — **attach both, plus `COHORT-FROZEN-2026-09-18.sha256`** |
| Design and manipulations | `SEVERITY-SWEEP-SPEC.md` (error types, insertion law, eligibility) + `CFD-ARM-SPEC.md` v0.2 §2 (protocols A/B/C, bed structures) |
| Analysis plan | `protocol/STATISTICS-PLAN.md` — attach whole |
| Planned amendment | `STATISTICS-PLAN.md` §13 — the **paired-anatomy arm** (H7). *Renamed 2026-09-19: it was the "natural-experiment arm" built on paired human masks, which were declined; it is now model-prediction vs official reference, with the same lesion inserted into both anatomies* |
| Detector | `protocol/DETECTOR-SPEC.md` v0.2 — H5's statistics, splits and operating point. **Attach it**: §7's recording columns are implemented, so the ablation will not need repeating for C3 |
| Code | `code/` — deposit at registration time with a DOI (Zenodo). **Re-verify the manifest immediately before lodging** (below); it was re-issued several times on 2026-09-19 |

## 2. State plainly in the registration — each is a strength when disclosed and a weakness when found

1. **The data are public and in hand.** Baselines (E0, the sweep) are already computed. What is NOT computed, and
   what this registration commits, is **every A/B/C ablation result and every flip rate**.
2. **No invasive FFR ground truth exists in this cohort.** All endpoints are within-instance *changes*, never
   absolute accuracy. The single external check is that the 0.80 crossing falls at 65–70 %DS, matching clinical FFR.
3. **Band, severity and length are confounded by physics** and are deliberately not rebalanced (`STATISTICS-PLAN` §3).
4. **Bed structure is a factor, not a nuisance**: leaky and discrete disagree on the 0.80 decision in 19/97 instances.
5. **Uncertainty floors:** **0.005** FFR solver discretisation (0D) and 0.010 healthy-reference re-fit. The 0D
   figure was revised up from 0.003 on 2026-09-19 after V1-V10 was widened from 2 scans to 18 across both beds. **The 3D mesh
   discretisation figure U₃D is not yet measured**, and §P4 carries a pre-registered contingency fixing what happens
   to H4 at each magnitude it might take.
6. **The cohort is a hashed list, not a seed** — `select()` is chaotic.
6b. **The entire cohort lies in ImageCAS-X's own held-out test split.** Verified 2026-09-19 against the dataset's
   `filelist/`: all 93 cohort patients are in `test.txt`, none in train (560), val (80) or exclude (200). Not
   engineered — the sweep drew from the test split because that is where the re-annotation statistics live — but it
   means any benchmark segmentation model's predictions on these scans are genuinely out-of-sample, which settles
   the training-overlap question for the planned D1c arm for *any* published weights. Declared here, it is a design
   property; found by a referee, it is luck.
7. **Protocol C is structurally unavailable on part of the cohort, and the paper says so up front.** It requires ≥ 2
   clean-partition territories with surviving members, which fails on **40 % of T1 rows and 33 % of T2 rows, almost
   all RCA**; 99 of 100 T2 × RCA rows have no surviving territory at all. **The tuned-protocol arm is effectively a
   left-coronary result for the topological error types** (`STATISTICS-PLAN` §9). Declared scope, not discovered.
8. **Error magnitudes are partly measured and partly chosen, and which is which is stated.** T3 and T4 derive from
   published disagreement statistics which the dataset's own authors describe as an **upper bound on agreement** —
   so those are floors. **T1 and T2 have no measured magnitude and are declared design choices**; Betti error is
   β₀ + β₁ and cannot detect a missed side branch at all.
9a. **`MURRAY_EXP = 2.66` is cited, and an earlier flag against it was withdrawn.** It is **8/3**, the
   mass–diameter exponent of Choy & Kassab 2008 (M ∝ A^(4/3), A ∝ D², so M ∝ D^(8/3)) — it allocates **myocardial
   bed** to a truncated outlet. A citation search had flagged it as uncited and outside the pooled 2.39
   (CI 2.24–2.54, Taylor 2024); that comparison is **category-mismatched** — Taylor pools the *flow*–diameter
   exponent (Q ∝ D^n, near Kassab's 7/3), a different quantity. It also matches what the 3D arm imposes on outlet
   caps, so both fidelities share boundary conditions exactly. Measured sensitivity, 30 subset trees: moving to
   2.39 shifts any outlet's flow share by a median **0.33 pp** (max 1.95) against a 10 pp check, because truncation
   leaves every outlet within ~0.06 mm of the cut. Reported as a sensitivity — allocate the bed by mass or by
   flow — not as a correction. **[Choy & Kassab to be verified against the paper before the manuscript quotes it.]**
   `SD_TERRITORY_SHARE = 0.10` remains a genuinely *chosen* value with no supportable citation; its specificity is
   reported across a band of 0.05/0.10/0.15/0.20.
9b. **The detector's specificity is reported as an UPPER BOUND.** Both remaining noise constants sit at the low end
   of their plausible ranges — `SD_TERRITORY_SHARE` against Keulards 2020 (≈0.19), `WSCV_TARGET = 0.083` against
   Kaufmann 1999 (0.15–0.21) — and too little noise makes the negative class easy, which inflates specificity.
   **The physiological-noise-floor claim is NOT affected** (median |ΔFFR| on correct anatomy moves only
   0.019→0.023 across the whole band); only the validation-gate specificity is.
9. **Magnitudes are NOT quality-matched.** Nothing is conditioned on image quality, diameter, attenuation or disease
   status; those enter the analysis as covariates and strata only (decided 2026-09-19, `STUDY-PLAN-v2` §E1).
10. **Nine defects were found and fixed before any result was generated** (§4). Disclose the count and the practice.

## 3. Pre-run decisions already made and dated — none may be revisited after results

| Decision | Date | Where recorded |
|---|---|---|
| Protocol C is **flow-matched only** (matching pressure *and* flow makes a flip impossible by construction) | 2026-09-18 | `STUDY-PLAN-v2.md` §E2 banner |
| Bed structure is a **pre-registered factor**; claims require agreement in both | 2026-09-18 | `CFD-ARM-SPEC.md` §2.5 |
| Confounding **declared, not rebalanced** | 2026-09-18 | `STATISTICS-PLAN.md` §3 |
| Random effect at **patient** level, nested slot term | 2026-09-18 | `STATISTICS-PLAN.md` §2 |
| Bands **re-derived per bed structure** | 2026-09-18 | `STATISTICS-PLAN.md` §P3 |
| 3D subset drops the "band holds in both" requirement | 2026-09-18 | `CFD-ARM-SPEC.md` §3 |
| Physiological-noise floor mandatory alongside every flip rate | 2026-09-18 | `STATISTICS-PLAN.md` §6 |
| Both directions registered for every hypothesis | 2026-09-18 | `STUDY-PLAN-v2.md` §4 |
| **B1 — Protocol C targets the clean tree's FULL territory outflow**, including a deleted branch's share, partitioned by the **clean** tree's territories | 2026-09-19 | `ablation.py` `protocol_c_targets`, `STATISTICS-PLAN` §P2 |
| **B2 — `T2_KEEP_BEYOND` = 25 mm** (= RUNOFF + 5 mm), so T2 no longer deletes its own measurement node | 2026-09-19 | `error_types.py`, `CFD-ARM-SPEC` §17 |
| **B3 — calibre-only errors may not change the modelled node set** (`trunc_ref` pins it to the clean tree) | 2026-09-19 | `zerod_ffr.py`, `CFD-ARM-SPEC` §17 |
| **Protocol C fits by global grid scan then local refinement**; an optimum at a search bound is a **failed fit**, logged and excluded | 2026-09-19 | `ablation.py`, `STATISTICS-PLAN` §9 |
| **`VALIDATED_RESIDUAL` stays 0.10**, justified as *stricter* than the ≈ 0.13–0.16 measurement bound and therefore conservative for H2 | 2026-09-19 | `STATISTICS-PLAN` §P2, `references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md` |
| **Register the design without quality matching** | 2026-09-19 | `STUDY-PLAN-v2.md` §E1 |
| **H4 contingency on U₃D** fixed before the number is known | 2026-09-19 | `STATISTICS-PLAN` §P4 |
| **Register without the paired-mask arm** — Gate D1b **declined by the dataset lead**, not merely unanswered; §13 re-specified for model-vs-official anatomy | 2026-09-18 / re-specified 2026-09-19 | `STATISTICS-PLAN.md` §13 |

## 4. Development history to disclose (in the paper's methods, not necessarily the registration)

**Nine defects were found and fixed before any result was generated** — five during cohort construction, four in the
ablation itself — each of which would have biased outcomes.

*Cohort construction (2026-09-18):* single-precision radius arrays; a lesion cap that let an inserted stenosis evict
a native one (inflow rose after adding a stenosis); NaN-blind mass balance (`max(0.0, nan) == 0.0`); per-segment
lesion placement producing spurious shoulder terms and bifurcation double-counts (2,281/6,944 instances); and a merge
rule comparing root-arc rather than tree distance, so a lesion on one branch erased one on another. **The cohort was
regenerated after the last of these; 110 of 150 selected instances changed.**

*The ablation (2026-09-19, all found by independent adversarial review before the full run):* Protocol C's minimiser
was a local method on a **bimodal** loss and returned the wrong basin on a real instance (ΔFFR −0.52 against a true
≈ 0), which would have been recorded as "passes its validation check and is materially wrong" — a false absorption
count and a false H5 positive; Protocol C targeted a validation quantity **contaminated by the very error it
validates against** (B1); T2's truncation **deleted the measurement node it was defined to preserve**, so every T2
Protocol A number was reading a boundary condition rather than a computed pressure (B2); and a fixed truncation
radius deleted vessels that a calibre error had merely narrowed, giving T4 × Protocol A the **wrong sign** in the
discrete bed (B3).

Verification: `severity_sweep.py --verify`, V1–V10 on both bed structures and two disjoint scan sets, all passing
after every change. **Worth stating in the methods:** the minimiser defect was absent from the 6-instance smoke set,
so a subset test would never have found it — which is why fit diagnostics are recorded on every row of the full run.

## 5. Before pressing submit

- [x] **Authorship — order, byline forms and CRediT settled 2026-09-19** (`STUDY-PLAN-v2.md` §7b). **FIVE** authors
      in order: **Fadillah Yamin** (`mohd.yamin@monash.edu`, no ORCID — confirmed, not missing), **Mohd Azan Mohammed
      Sapardi** (0000-0001-5278-014X), **Ming Kwang Tan** (added 2026-09-19), **Xin Wang** (0000-0002-5854-5287),
      **Mohd-Zulhilmi Paiz Ismadi** (0000-0002-7724-114X, **corresponding**). Every author holds a CRediT block.
- [x] **Ming Kwang Tan — contacts found** in `Imaging-Medical/AuthorsDetails.docx`: `tanmingkwang@mail.mcut.edu.tw`,
      ORCID 0000-0002-1585-9358.
- [x] **Ming Kwang Tan — affiliation RESOLVED 2026-09-19: dual**, Monash Malaysia Mechanical Engineering and Ming
      Chi University of Technology, New Taipei City 243, Taiwan. Evidence: `Imaging-Medical/PreviousStudy/Updated
      Automation In Construction Manuscript.docx`, a manuscript by this same five-author team in this same order,
      which lists him as affiliations 1 and 3. `AuthorsDetails.docx` gives only his external affiliation because it
      is a contacts list.
- [ ] **Ming Kwang Tan — which block of the work he vouches for.** Roles (*Investigation, Methodology, Validation*)
      are not a body of work, and ICMJE accountability needs a nameable part. **The last authorship item.**
- [x] **Xin Wang's byline form CONFIRMED 2026-09-19 — "Xin Wang", Wang as surname.** ORCID 0000-0002-5854-5287
      records given-names "Xin", family-name "Wang", with no credit-name and no other-name variants. **This project
      is already correct.** The error is in the sibling manuscript `PreviousStudy/Updated Automation In Construction
      Manuscript.docx`, which writes "Wang Xin" — worth fixing there before that paper is submitted, since a
      reversed byline indexes to a different person.
- [ ] **ICMJE criterion 2 is not yet met by two authors** (`STUDY-PLAN-v2.md` §7b). Mohd Azan and Ming Kwang Tan
      hold substantial contributions but **no drafting or critical-revision role is recorded for either**, and ICMJE
      requires all four criteria of every author. Arrange it now, while writing has not started: send them a draft
      for comment rather than a finished text for sign-off, and record what they revise. Not a registration blocker —
      a registration lists authors known at the time — but a **submission** blocker, and cheaper to arrange early.
- [x] **Corresponding author: Mohd-Zulhilmi Paiz Ismadi** (2026-09-19), with the reason recorded in §7b.
      Byline for author 2 confirmed as the long form, **Mohd Azan Mohammed Sapardi**.
      **Authorship is fully settled — nothing in §5 now blocks lodging except the mechanical steps below.**
- [ ] Deposit `code/` and obtain the DOI; add it to the registration.
- [ ] Attach both frozen cohorts and the SHA-256 manifest.
- [ ] **Re-verify the manifest immediately before lodging:** `shasum -a 256 -c protocol/COHORT-FROZEN-2026-09-18.sha256`
      from the project root. It must print OK on all 13 entries. *(The command in the previous edition did not work —
      inline comments broke the path parsing and the paths mixed two bases. Both fixed 2026-09-19.)*
- [x] **ImageCAS-X licence confirmed 2026-09-19** from the Zenodo record itself: *"Creative Commons Attribution 4.0
      International"*. Quote the version DOI (v1, 11 August 2026), not only the concept DOI.
- [ ] Note Gate **D2 (ASOCA)** status: obtainable but **gated** (UK Data Service registration + data-owner
      permission), and **only the majority-vote label is released** — so the detector's external test may end up being
      a held-out ImageCAS-X split, which is a weaker claim and is labelled as such (`references/GATE-D2-ASOCA-2026-09-19.md`).
- [ ] Re-read `STATISTICS-PLAN.md` §6, §9, §10 and §P4 — the four places where the plan commits in advance to
      reporting a *negative*, *null* or *not-estimable* result in specific words. They are what make the registration
      worth having.

## 6. After registration

Run order: A/B/C ablation under both bed structures (150 instances, ~12 minutes) → S_A characterisation → detector
development on the train split → external test → 3D arm as the CFD machine returns results. **Do not analyse the
ablation before the registration is lodged**, even informally: the value of the registration is entirely in its
timing.
