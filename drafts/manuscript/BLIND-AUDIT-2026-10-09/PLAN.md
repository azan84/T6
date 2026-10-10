# Paper 6 (T6): plan to address the 2026-10-09 blind audit

Input: five blind reports (`reports/`), the scores in `SCORES.md`, and the upload set from 2026-10-08 23:05.
Constraints: the JBHI special-issue deadline is 2026-10-15 (6 days). The page limit is 14 pp including the supplement, and the paper is at 8 + 6 = 14. The abstract limit is 250 words, and the abstract is at 250.
Page budget:
- **Main text:** no guaranteed slack. Page 8 shows white space between the Acknowledgment and the reference list in the left column; measure it after a rebuild before counting on it. Any main-text addition must be offset by a cut.
- **Supplement:** page 6 is about 70% empty, roughly 0.7 page or 45 lines free.
- **Abstract:** every added word must be matched by a cut.

Earlier decisions still in force:
- `REVISION-PLAN-POST-SUBMISSION-2026-10-08.md` deferred two analyses to the revision: real segmentation-failure frequency and the T5 throat error.
- Under the IEEE norm we use no "post hoc" or "pre-registered" labels and no hash.
- The paired inter-observer masks were declined by the dataset authors on 2026-09-18.

---

## 1. Verification register (all items, de-duplicated)

Seats: E = editor, M = methodology, C = clinical, I = imaging informatics, D = devil's advocate.
Status:
- **CONFIRMED:** the defect exists in the upload set or data.
- **VALID-LIMIT:** a fair limitation, not an error.
- **PARTLY:** partly right.
- **NOT CONFIRMED:** the reviewer is wrong on the facts.

| ID | Item | Seats | Status | Evidence checked |
|---|---|---|---|---|
| V1 | Fig. 3 caption says "Protocol D residuals lie below 0.01", but two D models sit at 0.083 and 0.111 | E M | CONFIRMED | main.tex l.343; data: D residuals > 0.01 = [0.083, 0.111] |
| V2 | IV-A: "about half of the models that passed were materially wrong" after one global scaling | M D I | CONFIRMED (true in one bed only) | Recomputed: Protocol C topological, discrete 20 wrong of 39 passing = 51%; leaky 14 of 154 = 9% |
| V3 | Pass counts and P(wrong \| pass) per cell are never reported | M D I | CONFIRMED | Computed now (Table P below). Under D, P&W equals the wrong rate (D passes 103/104 and 171/171) |
| V4 | Abstract and III-E say "directions held at doubled… demand", but the topological excess over B was significant in no comparison at ×2 | M C D | CONFIRMED (overstatement) | main.tex l.50, l.382 |
| V5 | The discrete topological P&W under B appears as 1%, 1% and 2% across S3, S5 and the text because the denominators differ | E M C | CONFIRMED (consistent counts, three conventions) | S3 n = 137, S5 n = 173, text n = 104 |
| V6 | p = 0.24 is Holm-adjusted (raw 0.121) but is not labelled as such | M | PARTLY (the sentence is inside a "Holm-adjusted" clause, but the reading is ambiguous) | main.tex l.304–305 |
| V7 | The 3D "−0.0007" is relative to the prescribed-flow baseline 0.892; against the clean 0.870 it is +0.022, and the reason for the 0.892 baseline is not explained | C E | CONFIRMED | main.tex l.357 |
| V8 | Fig. 4 caption: "a shift that would move a decision near 0.80". 0.870 → 0.944 does not cross 0.80 | E C D | CONFIRMED (wording) | main.tex l.366 |
| V9 | Perfusion territories are first-bifurcation subtrees; the check is coarse and cannot see a diagonal missed inside the LAD territory | C D E M I | CONFIRMED + VALID-LIMIT | Data: median 2 territories per tree (max 3). Neither the count nor the granularity is stated in the paper |
| V10 | The topology-vs-caliber ranking ("3–6×") rests on design-chosen severe T1/T2 against inter-observer-size caliber errors; no throat error | all 5 | VALID-LIMIT | II-C says "design choices"; IV-A says "for the magnitudes studied", but the abstract and Conclusion carry no qualifier |
| V11 | T3 cannot move FFR much because the lumped loss K has no length term | M | PARTLY | zerod_ffr.py l.250: K has no length term, but the Poiseuille resistance is integrated along the narrowed lumen, which is the length-dependent viscous term of Young–Tsai. The text does not say so |
| V12 | HD95 is a whole-tree statistic, not a lesion-extent bound ("which bounds the disagreement in lesion extent") | M C I | CONFIRMED (overstated wording) | main.tex l.174 |
| V13 | "Overlap scores miss these errors" is asserted, not measured | I D E | CONFIRMED | No DSC, clDice or Betti values for corrupted trees anywhere |
| V14 | The P&W comparison against the floor is uneven: corrupted models use noise-free targets, the floor uses noisy targets | E M D | CONFIRMED (already a stated limitation, but the abstract sets the numbers side by side) | IV-D states it |
| V15 | The tuned excess over B is not significant in the leaky bed, nor at ×2 | C D E | CONFIRMED; the body states it, the abstract does not | III-B "p ≥ 0.12"; III-E |
| V16 | Low flow regime and narrow distance-map radius; 80% DS at FFR 0.87 is clinically atypical | C D E | VALID-LIMIT | II-B; the ×2/×3 replication partly answers it |
| V17 | The 3D radius-definition offset (0.045 mm at the throat moves FFR 0.761 → 0.870) shows that throat caliber matters more than the ranking implies | D I C | VALID point, not used in the paper | III-D, IV-D |
| V18 | Code on request only, no DOI | all 5 | CONFIRMED | Data statement. Package exists in `deposit-2026-10-08/` (code + frozen cohort), not yet published |
| V19 | No concrete informatics deliverable (detector ROC of the pre-tuning residual or of the tuning factor) | E I | VALID | Data exist (B residuals; floor draws; C factors) |
| V20 | Clustering (150 instances in 93 patients; 20 draws per instance) is ignored in inferential wording; the VI posterior is narrow; D is absent from the mixed model | M E D | VALID-LIMIT | II-F says CIs are descriptive, yet III-A argues from a lower bound |
| V21 | Leaky T4-A: lower bound 6 against a floor of 5.0–6.5% ("only the taper exceeded…") | M | PARTLY (the text limits the claim to the discrete bed and the leaky bed separately; the per-cell floor is not shown) | main.tex l.299 |
| V22 | "Flip = change in the indicated treatment" overstates; CT-FFR is a gatekeeper | C | VALID (wording) | main.tex l.227 |
| V23 | "Protocol A represents the case in which BCs were obtained correctly" is wrong, because the deleted bed is lost | I | CONFIRMED (wording) | main.tex l.183 |
| V24 | The ×0.7/×1.3 demand sensitivity table is never mentioned in the main text | I | CONFIRMED | No main-text pointer |
| V25 | The origin of the 13% and 16% thresholds is not stated | I | CONFIRMED | main.tex l.230 |
| V26 | Search-bound rule is inconsistent: a C fit at the bound counts as a failure, D fits at 10³ are retained | M | CONFIRMED (supplement wording) | supplement l.134–137 |
| V27 | Protocol A T2 with no remaining outflow is excluded (36 discrete); scored as flips it would raise A-T2 | M | VALID; would strengthen the topological claim | Table S1 |
| V28 | The patient-case GCI acceptance failure is not stated in the main text | M | CONFIRMED (main text gives 0.0021 only) | main.tex l.372 |
| V29 | Ref [9] (pulmonary-valve FSI) is used for coronary flow-split tuning; Vardhan 2019 (side branches, 3D) and CT-FFR reproducibility (Gaur 2014) are missing | E C | PARTLY ([9] supports "flow splits" generically; coronary fit is weak). The two references must be verified before citing | main.tex l.71 |
| V30 | Figures: Fig. 4 jet colormap, Fig. 2 has no per-band n and no Protocol D, Fig. 3 has no 0.10 line, small fonts | I E | CONFIRMED (cosmetic) | page images |
| V31 | "Taper" is a misleading name for a uniform ×0.930 narrowing | I | VALID (naming) | II-C defines it |
| V32 | "LOGO" placeholder in the header | E | NOT CONFIRMED as a defect | It is the official JBHI template's logo.eps (ieeecolor.cls l.3485); the template's own PDF shows it |
| V33 | No funding statement | E | OPEN (operator fact) | — |
| V34 | Use annotator-2 masks "already in the dataset" as real errors | I | NOT CONFIRMED | The paired masks are not released, and our request was declined on 2026-09-18 |
| V35 | Reweight the flip rates to a clinical FFR distribution | E | Declined | No defensible target distribution; the rates are already stated as conditional |
| V36 | The abstract leads with Protocol A (32–33%), which is unrealistic for automated pipelines; B should be co-equal | I D | VALID (emphasis) | Abstract |
| V37 | Abstract ends prescriptively ("should be checked") | D | VALID (tone rule: facts, not instructions) | Abstract l.51 |
| V38 | Microvascular dysfunction, collaterals and error–lesion correlation are not acknowledged | C D | VALID-LIMIT | IV-D |
| V39 | Throat Reynolds number / steady laminar assumption at higher flow; lesion flow not reported | C D | VALID (minor) | — |
| V40 | Identifiability framing: P&W is an expected non-identifiability; say what is new | E D | VALID | — |

**Table P: pass and wrong counts (computed 2026-10-09 from the frozen run; models with a defined residual)**

| Bed | Class | Protocol | n | Pass | Wrong | P&W | P(wrong \| pass) |
|---|---|---|---|---|---|---|---|
| discrete | topological | A | 137 | 21 | 119 | 17 | 81% |
| discrete | topological | B | 137 | 23 | 59 | 2 | 9% |
| discrete | topological | C | 104 | 39 | 64 | 20 | 51% |
| discrete | topological | D | 104 | 103 | 21 | 21 | 20% |
| discrete | caliber | A/B/C/D | 194 | 190/153/170/194 | 6/0/9/35 | 6/0/9/35 | 3/0/5/18% |
| leaky | topological | A | 218 | 108 | 124 | 43 | 40% |
| leaky | topological | B | 218 | 176 | 14 | 10 | 6% |
| leaky | topological | C | 171 | 154 | 21 | 14 | 9% |
| leaky | topological | D | 171 | 171 | 9 | 9 | 5% |
| leaky | caliber | A/B/C/D | 300 | 300/244/294/300 | 10/0/37/12 | 10/0/37/12 | 3/0/13/4% |

---

## 2. Plan

### Tier 1: text and figure fixes, page-neutral, do now (about 0.5 day)
Each fix corrects an error or a claim that goes beyond the evidence. Each is needed because a real referee would cite it, and none costs a page.

| # | Change | Fixes | Page cost / offset | Why it is required |
|---|---|---|---|---|
| T1-1 | Fig. 3 caption: "Protocol D residuals lie below 0.01 except in two models (0.08, 0.11)", or drop the parenthesis and keep S2 | V1 | 0 | Factual contradiction between caption and supplement |
| T1-2 | IV-A: make the "about half" sentence bed-specific: "in the discrete bed, 20 of the 39 models that passed after one global scaling were materially wrong (9% in the leaky bed)" | V2 | +0.5 line; cut elsewhere in IV-A | The sentence is false in one bed |
| T1-3 | Abstract and III-E: replace "directions held at doubled and tripled demand" with the exact statement, e.g. "Flip-rate directions held at ×2 and ×3 demand; the tuned excess over re-derivation was significant only at the primary demand in the discrete bed." | V4, V15 | Abstract: word-neutral by trimming the 3D sentence (see T1-5) | Overstatement flagged by 3 seats; it lowers S3 |
| T1-4 | Abstract: put "in this threshold-stratified cohort" before the first rate, and add "for the error magnitudes studied" to the topology-vs-caliber sentence; Conclusion likewise | V10 | Abstract ±0 (trade words) | All 5 seats call the ranking design-set; the qualifier is in IV-A but not where readers look |
| T1-5 | 3D: report both references ("−0.0007 against the prescribed-flow baseline, +0.022 against the clean fixed-resistance value"). Explain in one clause that splitting the territory flow by bed weight moves the baseline to 0.892. Fig. 4 caption: replace "would move a decision near 0.80" with "raised FFR by 0.074". Abstract: shorten to "and removed it in one 3D case" | V7, V8 | ≈0 (caption shorter, III-D +1 line) | Factual (C W5) and an overclaiming caption (3 seats) |
| T1-6 | III-D or IV-D: state that the patient-case mesh acceptance criterion was not met and that the 3D uncertainty is about 0.002 | V28 | +1 line, offset by a cut in IV-D | Transparency; the supplement already says it, and the main text should not imply more |
| T1-7 | II-D: state that the check uses a median of 2 (max 3) territories per tree, i.e. main-branch level. IV-D: one sentence that a finer, segment-level check could detect within-territory errors that this one cannot | V9 | +2 lines; offset by cuts | The devil's advocate's strongest argument. Stating the granularity turns an exposed weakness into a declared scope |
| T1-8 | II-B: one clause noting that the viscous loss of the lesion is the Poiseuille resistance integrated along the narrowed lumen (length-dependent) and only the expansion loss is lumped | V11 | +0.5 line | Answers M W4 at near-zero cost |
| T1-9 | II-C: "HD95 (2.46 mm), used as a proxy for the disagreement in lesion extent" | V12 | 0 | Overstated wording |
| T1-10 | II-F: "a change in classification at 0.80, and hence potentially in referral or treatment" | V22 | 0 | Clinical accuracy |
| T1-11 | II-D: Protocol A wording: "the boundary conditions of the clean anatomy were kept despite the segmentation error" (not "obtained correctly") | V23 | 0 | Wording error |
| T1-12 | Harmonise P&W denominators: state the convention in the Table I, S3 and S5 captions (S5 includes undefined residuals as failures); make the III-B 2%/6% use the S3 basis or say "on the instances where C is defined" | V5 | 0 (caption words) | Same quantity printed three ways |
| T1-13 | Label p-values: "(Holm-adjusted p = 0.24)" | V6 | 0 | Statistical reporting |
| T1-14 | Supplement S2: one bound rule, i.e. state that D fits at 10³ are retained because the bound is not limiting (residual stays defined), or count them as failures and update the two models | V26 | 0 (supplement) | Internal rule conflict |
| T1-15 | Main text: one pointer to the ×0.7/×1.3 sensitivity table; II-F: origin of 13%/16% (1.96 × 6.5–8% repeatability CV, or state the source) | V24, V25 | +1 line | Unreferenced table; undocumented thresholds |
| T1-16 | IV-B or IV-D: one sentence using the 3D radius-definition offset: a 0.045 mm throat-radius difference moved FFR by 0.11, so the throat caliber, which this study did not perturb, can matter as much as branching | V17 | +2 lines, offset by cuts | Turns D C3 / I W7 into a limitation we state first. It also prepares the T5 revision |
| T1-17 | Abstract last sentence: rephrase as a finding, e.g. "…so the branching and caliber of the segmentation are not certified by a perfusion match." | V37 | 0 | Tone rule: facts, not instructions |
| T1-18 | IV-D: one clause listing microvascular dysfunction, collaterals and error–lesion correlation as untested | V38 | +1 line | Clinical completeness (C W8, D C8) |
| T1-19 | Fig. 4 colormap to viridis/cividis; Fig. 3 vertical line at 0.10; Fig. 2 note "Protocol D in Table I"; check fonts ≥ 8 pt | V30 | 0 | Cosmetic; JBHI production checks font size |

Candidate cuts to fund the main-text lines (about 8 lines needed): shorten IV-B's reconciliation of [20]/[21] by one sentence; merge two sentences in III-A on caliber floors; tighten IV-C's four considerations to three lines each.

### Tier 2: cheap analyses on existing data, supplement only plus one main-text sentence each (about 1.5–2 days)
Each fills an empty supplement page (about 45 lines free) and turns an assertion into a measurement.

| # | Analysis | Fixes | Effort | Space | Why it earns its space |
|---|---|---|---|---|---|
| T2-1 | **Table P** (pass n, wrong n, P(wrong \| pass)) as a supplement table or as columns of Table S3 | V2, V3 | Done (numbers above) | About 10 lines | 3 seats asked; it shows that under D, P&W = wrong; costs no compute |
| T2-2 | **Overlap and topology metrics of every corrupted tree:** volume DSC and clDice computed exactly from the nested tube volumes and centerline lengths (corrupted ⊂ clean for T1–T4), plus fraction of bed flow lost; AUC of each metric for flip | V13 | About 0.5 day | About 10 lines + 1 sentence in IV-B | The paper's informatics claim ("overlap scores miss these errors") is currently unmeasured; 3 seats. If DSC does detect T1/T2, the sentence is softened; report either way |
| T2-3 | **Dose response from existing runs:** flip rate by tertile of deleted-branch radius (T1) and of length lost (T2), using the stored `info_branch_r_mm` / `info_length_lost_mm` | V10 | About 2 h | About 6 lines + half a sentence | Puts the topological errors on a dose axis without new solves; partly answers the "worst case" critique (5 seats) |
| T2-4 | **QC detector:** AUC, sensitivity and specificity of (a) the pre-tuning (B) perfusion residual and (b) the fitted factor \|log C\| for detecting a decision-changing error, against the correct-anatomy noise draws (false-alarm rate) | V19 | About 3 h | About 6 lines + 1 sentence in IV-C | Gives JBHI readers a measurable informatics result (E W3, I W4); S7 is the dimension most tied to venue fit |
| T2-5 | **Patient-level cluster bootstrap** CIs for the headline contrasts (A topo vs cal; P&W C/D vs B; floor) | V20 | About 2 h | Caption footnote or 4 lines | Removes the clustering objection (M W3) cheaply; replaces the "lower bound exceeds floor" inference with a proper one |
| T2-6 | A-T2 zero-outflow models scored as flips (sensitivity) | V27 | About 1 h | 1 line in Table S1 note | It strengthens the topological claim; costs nothing |

### Tier 3: moderate analyses, operator decision (each changes or tests a headline)

| # | Analysis | Fixes | Effort | Risk to the headline | Recommendation |
|---|---|---|---|---|---|
| T3-1 | **Finer-territory sensitivity:** territories = subtrees below every second-generation branch (or every branch with r_ref ≥ 1 mm); rerun C/D | V9 (strongest D argument; 5 seats) | Code ~0.5 day (`territories()` in ablation.py) + ~1 h runs | **High:** a missed side branch that forms its own territory will fail the check, so T1 P&W may fall sharply. That supports the "check the branching" message but weakens "a perfusion match can hide it" | Run it now as a supplement sensitivity. Knowing the answer before reviewers do is worth the risk; if T1 P&W collapses, the abstract must say the concealment needs a main-branch-level check |
| T3-2 | **Noisy targets for corrupted models:** C/D tuned to the same 20 noisy draws as the floor | V14 | ~2 h code + ~3–6 h runs | Medium: may lower pass rates (lower P&W) or raise wrong rates | Run if T3-1 is done by 10-11; otherwise reword the abstract to compare against B (same targets) and keep the floor as context |
| T3-3 | **T5 throat caliber error (±ΔDS)** | V10, V17 | ~1 day + citations for the magnitude | Medium: likely near topological rates; it reframes to "branching and the throat" | Keep in the revision as planned (2026-10-08). The deadline does not allow the reframing safely; T1-16 discloses it |
| T3-4 | **Code + cohort DOI (Zenodo)** from `deposit-2026-10-08/` (remove `__pycache__`, add README + licence) | V18 | ~2 h | None | **Do now.** All 5 seats raised it; it is the largest single score gain (S8). It is outward-facing, so the operator publishes |

### Tier 4: defer to the revision (reasons)
- Real segmentation-failure frequency from the ImageCAS-X pretrained weights (I W2, E W1). Needs a download of tens of GB and GPU inference; already planned.
- Half-voxel radius correction with cohort re-selection (C W1, E W6, D C3). Re-selects the whole cohort and changes every number; the ×2/×3 replication covers the flow side.
- MCMC refit and adding D to the mixed model (E W10, M W3). Low value; T2-5 covers the inference.
- A second 3D case with a matched throat (M W5). Weeks of CFD.
- CT-FFR reproducibility as a second comparator, and mass-based demand (C W7, W1d). Needs a citation check and a rerun; text mention only if space allows.
- Rename "taper" to "uniform distal narrowing" (I). Touches figures, tables and the supplement; risk of inconsistency within 6 days.

### Tier 5: decline (reasons)
- Annotator-2 masks: not released, and the request was declined (V34).
- "LOGO" header: it is the official template element (V32).
- Reweighting to a clinical distribution: no defensible target; the rates are stated as conditional (V35).

### Operator facts needed
- Funding statement (V33): is there a grant number, or "no specific funding"?
- Approval to publish the Zenodo deposit (T3-4).
- References (V29): add Vardhan et al. 2019 (Sci Rep; side branches in 3D coronary modelling) only after we verify it, and replace or supplement [9] with a coronary flow-split reference. Each reference costs about 2.5 lines of the main text, so add at most one.

---

## 3. Page budget

| Block | Main text lines | Supplement lines |
|---|---|---|
| Tier 1 additions | about +9 | +2 |
| Tier 1 offsets (cuts listed above) | about −9 | — |
| Tier 2 (T2-1 to T2-6) | +3 sentences (about 6 lines), offset by cuts | about 37 |
| Tier 3-1/3-2 if run | +1–2 lines | about 8 |
| Total | 0 net (main must stay 8 pp) | about 47 of about 45 free: tight; merge T2-1 into Table S3 to save about 6 lines |

---

## 4. Score projection (panel mean; simulated, about ±0.5 per dimension)

| Dim | Now | After Tier 1 | + Tier 2 + DOI | + Tier 3-1/3-2 | Main drivers |
|---|---|---|---|---|---|
| S1 Novelty | 6.8 | 6.8 | 7.0 | 7.1 | Detector (T2-4) and overlap (T2-2) add an informatics result; identifiability sentence (V40) |
| S2 Rigour | 6.0 | 6.1 | 6.5 | 7.0 | Cluster bootstrap, Table P, dose response; finer territories and noisy targets remove the two biggest design objections |
| S3 Claims vs evidence | 5.8 | 6.8 | 7.0 | 7.2 | Most S3 complaints are wording (V2, V4, V7, V8, V10, V15, V37) |
| S4 Physiology | 6.0 | 6.3 | 6.4 | 6.8 | Territory scope stated; T3-1 tests it; flow and radius stay deferred, which caps S4 near 7 |
| S5 Consistency | 7.8 | 8.5 | 8.6 | 8.6 | V1, V5, V6, V7, V26 |
| S6 Clarity | 7.0 | 7.2 | 7.2 | 7.2 | Figures; denominator captions |
| S7 Venue fit | 6.4 | 6.5 | 7.2 | 7.3 | Detector AUC and measured overlap metrics are the JBHI-relevant deliverables |
| S8 Reproducibility | 5.6 | 5.7 | 7.6 | 7.6 | Code + cohort DOI (5/5 seats) |
| **Overall** | **6.4** | **6.7** | **7.2** | **7.4** | Recommendation would likely move from major towards minor/major; T5 and real-failure frequency (revision) are the remaining major items |

## 5. Proposed schedule
- 10-09: Tier 1 text fixes; prepare the DOI package; start T2-1, T2-3 and T2-6.
- 10-10: T2-2, T2-4, T2-5; code the T3-1 territories.
- 10-11: run T3-1 (+ T3-2 if adopted); write supplement tables.
- 10-12: integrate; rebuild; page check.
- 10-13: blind re-score (same rubric) and consistency check.
- 10-14: upload set; operator read.
- 10-15: submit.
