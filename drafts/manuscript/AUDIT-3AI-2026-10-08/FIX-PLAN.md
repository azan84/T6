# Fix plan: three-AI audit of main.pdf (2026-10-08)

Source: `../AUDIT-main-2026-10-08.xlsx`. It has 119 findings: Claude Code 48, GPT Codex 31, Antigravity (agy) 40. They were cross-checked blind, and the consensus is in column Q.
The audit read the 17:48 build. After that build the paper moved to the JBHI class and the Data and Code Availability (DAS) text was rewritten. Every finding below was re-checked against the current `main.tex`.
Planner: Opus. Benchmark: published JBHI papers (`JBHI-BENCHMARK-AUDIT.md`). Fix audit: Fable.

## Constraint: net-neutral length
- The main text is 8 pp and the supplement 6 pp, which is the 14-page JBHI cap.
- Page 8: the right column ends at y = 731 pt and the left at 749 pt, so about two lines are free. Every line added must be paid for by a line cut.
- The abstract has 249 of the 250 words allowed. Abstract edits must therefore balance within the abstract itself.
- Supplement page 6 is about 70% empty (the text ends at y = 227 of 792 pt). Detail that does not need to be in the main text moves there.

## Facts verified before planning
| Finding | Check | Result |
|---|---|---|
| CL-38 / AG-16, 137 vs 138 mL/min | Median of k·r_in³ over the 150 selected instances (`sweep_test_selected.csv`) | Median r_in is 1.595 mm and median demand is 2.28 mL/s = 136.8 mL/min. The text is correct but rounds 2.28 to 2.3. **Fix:** print 2.28. |
| CL-11, cohort D −0.0007 equal to 3D −0.0007 | `ablation-perterritory-2026-10-08.csv`, scan 14 LAD, discrete, T1, D | −0.000695. The match is real, not a copy error. **Decline**, with this verification recorded. |
| AG-22, what does Protocol C scale? | `ablation.py`: C starts from `t2.calibrate(...)` on the corrupted tree | It scales the **re-derived** bed. **Fix:** say so. |
| AG-08, 0.50 vs 0.60 mm | `zerod_ffr.py` l.20; `CFD-ARM-SPEC.md` §2.4 | Leaky: the mask resolves radii only down to about 0.3–0.4 mm. Discrete: 0.60 mm was the smallest cut tested that left few single-outlet trees and kept a deletable branch at most lesion slots (74%). |
| CL-13, 6 944 ≠ 280 × 32 | `severity_sweep.py`, `sweep_test.log` | The eligibility criteria are applied per lesion slot (position × length), so some host vessels keep fewer than 32 instances. **Fix:** add "eligible". |
| CX-06, sampling | `severity_sweep.select` | Random order (seed 20260918); scarcest band first; vessel types rotated; at most two per tree and one per host per band; bands taken from the leaky-bed baseline FFR. |
| CL-43, Fig. 4 "p/Pa" | `fig5_case3d.py` l.102 | The label is already `$p/P_\mathrm{a}$` with a subscript. The finding is a text-extraction artefact. **Decline.** |
| AG-40, DOI unlinked | current `main.tex` | The DAS already cites [22], [23]. **Already fixed.** |
| CL-16 / AG-17 / AG-33, T2 denominators | Supplement §S2 | T2 was not applicable to one instance per bed. Under A, the break removed every bed node in 36 (discrete) and 2 (leaky) instances. B re-applies the bed rule to the corrupted tree, so its new vessel end carries outflow. |
| CL-17 / CX-11, failed fits | Supplement §S2 | No Protocol C fit hit a bound. Two D fits reached 10³ (residuals 0.08 and 0.11). |

## Plan (grouped; line cost: + adds, − saves, 0 neutral)

### 1. Errors and internal inconsistencies: fix all (cost ≈ 0)
| IDs | Fix | Cost |
|---|---|---|
| AG-07, CL-03 | "three boundary-condition protocols" → "four" | 0 |
| AG-01, CL-28 | Abstract: "reduced **pooled** topological decision changes to 5–19%" | +1 w |
| CL-07 | "Of Protocols A–C, re-deriving … produced the fewest flips" | +3 w |
| AG-26, CL-25 | "flipped equally often" → "flipped at similar rates" | 0 |
| AG-27, CL-24 | The taper claim is restricted to the discrete bed (13% fixed, 14% D). The leaky 9% (lower bound 6%) is dropped. | − |
| AG-35, CL-46 | "(the taper up to 13%)" → "up to 14%" | 0 |
| CX-21 | "whose FFR tuning lowered" → "in which tuning lowered FFR" | 0 |
| CX-20 | "Tuning raised them" → "Tuning raised these proportions" | +1 w |
| CL-36, AG-12 | Stray comma after [26] | 0 |
| CL-37 | "agreed to" → "agreed with" | 0 |
| CL-39, AG-11 | "the exponent approximates 8/3" → "2.66, close to 8/3" | 0 |
| CL-38, AG-16 | 2.3 → 2.28 mL/s | 0 |
| AG-37, CL-45 | Space before the comma after FFR_CT in the bib title | 0 |
| CL-40 | `\usepackage{cite}`: sorted and compressed citations ([10]–[13]) | − |
| CL-12 | "requested radius" → "reduced-order radius" | 0 |
| CL-26 | "ended beyond it" → "ended outside the zone" | 0 |
| CL-06 | r_fit becomes the "taper-fit radius" in II-A | 0 |
| CL-05, AG-23 | Radius ratio k → λ | 0 |
| CL-04, AG-22 | Bed constant C → C_b in main and supplement. "(one bed scaling)" deleted. C scales "the re-derived bed". | − |
| CL-48 | "least flexible tuning a pipeline could use" → "least flexible tuning tested" | − |
| CL-41, CX-31 | Ref [9] (Arminio, MRI flow split) is attached to "flow splits" and [8] (Menon, CT perfusion) to "perfusion". The claim now matches each source, and the JBHI citation is kept. | 0 |
| CL-42, CX-04 | "validated … in multicenter trials [2], [3]" → "validated for specific implementations against invasive measurement in a multicenter trial [3]". [2] moves to the 3D-form citation. | 0 |
| AG-06 | "mean blood pressure … mean aortic pressure" | +2 w |
| AG-14 | The expansion loss is "lumped at the stenosis" | 0 |
| AG-04, CL-35 | Split the run-on sentence in Introduction ¶3 | 0 |
| AG-05 | Serial comma in the affiliation footnote | 0 |
| CL-14 | "(50 each in the LAD, LCx and RCA)"; "93 patients" kept, with "140 scans" changed to "140 patients" | 0 |
| AG-18 | Move the missed-branch parenthetical to the T1 definition | 0 |
| AG-20 | T3 "2.46 mm longer about the same center" | +4 w |
| AG-10 | Native DS "relative to r_fit" | +2 w |
| CL-13 | "6 944 eligible instances" | +1 w |
| CL-15, CX-06 | "bands of leaky-bed baseline FFR, in random order with a fixed seed". The full algorithm goes to Supplement S1. | +8 w |
| AG-08 | One clause per bed on the truncation rationale | +12 w |
| CL-17, CX-11 | "(none occurred)" after the edge-of-range rule. The two D fits are already explained in Supplement S2, and the main text points there. | +2 w |
| AG-09 | "(r′ = r elsewhere; DS as a fraction)" | +5 w |

### 2. Overclaim and scoping (high or confirmed): fix with wording that costs no more lines
| IDs | Fix | Cost |
|---|---|---|
| CX-01, CL-32 | "decides whether … is treated" → "guides whether … is treated" (abstract). The Introduction gets different wording ("used to decide on revascularization"). | 0 |
| CX-02 | "…is untested" → "has not, to our knowledge, been tested against a clean-model reference" | +6 w abstract (offset in the abstract) |
| CX-03, CX-10 | Target stated as "the clean model's territory flows (an error-free perfusion measurement)" in the abstract (short form) and II-D. Limitations: real targets are noisy, represented only by the simulated floor. | +~15 w |
| CX-05 | "whose FFR serves as the true value" → "the reference value" | 0 |
| CX-09 | Add to II-C: "so the topological results are conditional on these choices" | +7 w |
| CL-10, CX-22 | III-D: "The 3D case agreed in direction with the reduced-order result, and prescribed flows removed the error in both." | +6 w |
| AG-36 | Limitations: "(+0.127 against +0.081 on the meshed radius; 3D +0.074)" | +4 w |
| CL-09 | IV-B: "are both consistent with our results … so the protocol alone can produce both behaviours" | 0 |
| CX-25 | "restored, by construction of the targets, the flow …" | +4 w |
| CX-26 | "four steps" → "four considerations" | 0 |
| CL-01 (High) | Conclusion: "in the discrete bed up to one in five tuned topological-error models (5–8% in the leaky bed)" | +8 w |
| CL-02 (High) | "We have shown where safeguards are most effective" → "The results point to where safeguards are likely to matter most" | +2 w |
| CL-47 | "three to six times … **with fixed boundary conditions**" | +4 w |
| CX-27 | "Applied to 150 inserted stenoses in 108 trees" | +4 w |
| CX-28 | "can be applied to any … pipeline" → "can be adapted to other … pipelines" | 0 |
| CL-08, CX-24 | Abstract: "The directions held at doubled demand (both beds) and tripled demand (leaky bed)" | +6 w abstract |
| CL-31 | Abstract: "in one three-dimensional case" | +1 w |
| CL-29 | Abstract: name the beds at first use, "(discrete outlets; leaky, distributed outflow)" | +5 w abstract |
| CL-27, AG-34 | IV-A: "…and about half of the models that passed after one global scaling were materially wrong" | +4 w |
| CX-19 | III-A: give the numbers: "only 22% of re-derived topological-error models passed (89% leaky)". The duplicate clause in III-B is deleted. | 0 net |
| CX-13 | Show the derivation: "1.96 × 10–15% ≈ 20–29%"; "strict" → "conservative" | +3 w |
| AG-28 | Floor wording: the clean value stands for the first measurement and the draw for its repeat, with the test–retest SD of differences 0.018, as in [31] | 0 |
| CL-22 | Materially wrong: "half the width of the 0.75–0.85 grey zone [31]" | 0 |
| CL-18 | "HD95 … bounds the disagreement in lesion extent" | +5 w |
| CL-19 | "The taper (T4), a uniform narrowing from the lesion onwards, …" | +4 w |
| CL-33 | Limitations: one sentence covering one error at a time, a single dataset and model, clean-model targets, and Protocol D post hoc | +30 w |

### 3. Statistics and reproducibility (benchmark-dependent; see §5)
| IDs | Proposed | Cost |
|---|---|---|
| CX-07, CX-14, CL-23, AG-31, CX-15 | Replace the mixed-model sentence with: "Because instances are clustered within patients, Wilson intervals are descriptive; a Bayesian mixed-effects logistic model with patient and lesion-slot (vessel, position and length) random effects agreed with the paired tests (Supplementary Material)." The noise-floor CI note goes in the same sentence. No cluster-bootstrap rerun. | +15 w |
| CL-20, CX-17, AG-30 | The SHA-256 of the cohort list is printed in Supplement S1, and Methods points to it. The DAS stays as the operator decided. | +3 w main |
| CL-21, CX-16 | Protocol D is labelled "secondary" in III-B and in the Conclusion. The abstract is left alone (word cap). | +2 w |
| CL-34, CX-29 | **Operator decision stands** (code on request, decided 2026-10-08). Not changed. | 0 |
| CX-08 | The relaxation factor, initialization and iteration cap go to Supplement S1, one sentence. | 0 main |

### 4. Tables and figures
| IDs | Fix | Cost |
|---|---|---|
| AG-32, CX-18, AG-33, CL-16, AG-17 | Rewrite the Table I footnote. n is the flip denominator, and the passes-and-wrong denominators are given. Under A a break removed every bed node in 36 discrete and 2 leaky instances; under B the new vessel end carries outflow. T2 was not applicable to 1 instance per bed. The duplicate "Protocol D matched … 1%" sentence moves out of the footnote. The III-A "36 instances" clause is deleted. | ≈0 net |
| CX-12, AG-24, AG-25 | Fig. 1 caption: "host LAD in blue"; "25 mm beyond the distal edge of the lesion"; "Its clean, lesion and T1 models were also solved in 3D." | +5 w caption |
| CL-44 | Fig. 2 caption: "protocol (A–C; D in Table I)" | +3 w |
| CX-23 | n per panel: **decline** (Fig. 3 pools T1 and T2 by design; Table I gives n). Re-encoding is deferred. | 0 |

### 5. Decline (with reason)
- AG-13, AG-15, AG-38, AG-39 were rejected by both cross-checkers.
- AG-02: "typical" is accurate (median 0.000/0.004), and III-C gives 10 of 44.
- AG-03: the abstract word cap applies, and Table I gives the 36%.
- AG-19: the definition is generic. Most RCA exclusions are already stated.
- AG-21: the Methods and Results subsections share titles, as in published JBHI papers (see benchmark).
- AG-29: the patient-geometry throat check (0.0021) is already in III-D.
- CL-30: abstract word cap; Methods gives 97.
- CL-11, CL-43, AG-40: verified as non-errors or already fixed (see the facts table).

## Line-budget reserve (cuts that pay for the additions)
1. `cite` package compression (Intro ¶3: [10]–[13], [14]–[16]).
2. IV-C: delete the developer sentence ("For a developer, tuning is a trade-off: …"). It repeats the IV-A third finding. About 2.5 lines.
3. IV-A: delete "Three findings stand out."; merge "This ranking holds for the magnitudes studied …" into the CX-09 conditional clause.
4. III-A/III-B duplicates (36-outlet clause; 22%/89%; D 1% sentence).
5. II-D: drop "(one bed scaling)"; shorten "least flexible …" and "most flexible …".
6. Intro ¶4: the trailing "None of these studies compares …" sentence is tightened.

## Acceptance
- Main 8 pp, supplement ≤ 6 pp, abstract ≤ 250 words, no undefined references, no overfull boxes beyond the pre-fix log.
- No number changes except the 2.28 mL/s demand.
- Fable audits the diff against this plan and the xlsx findings, blind to my verdicts on whether each fix succeeded.

---
## Final plan after the JBHI benchmark and operator decision (2026-10-08)
Benchmark: `JBHI-BENCHMARK-AUDIT.md` (12 JBHI papers; B6/B7 abstracts only).

| Topic | JBHI norm (benchmark) | Final action |
|---|---|---|
| Q1 "true value" (CX-05) | "ground truth" is used only where the truth is injected; overstated in our design | Changed to "reference value". |
| Q2 clustering (CX-07/14, CL-23, CX-15, AG-31) | No JBHI paper uses cluster-aware CIs; a caveat is optional | One sentence: intervals descriptive, because instances are clustered within patients; the mixed model (lesion slot defined as host vessel, position and length) agreed with the paired tests. No rerun. |
| Q3 code (CL-34, CX-29) | 0/12 say "on request"; 8/12 make no statement | Kept "on request" (operator decision). |
| Q4 hash / plan / post hoc (CL-20, CX-17, AG-30, CL-21, CX-16) | 0/12 report any of these | **Operator decision: do not report.** Hash, pre-specification sentences and the "Protocol D run after…" statements were removed from the main text and supplement. "Frozen cohort" became "cohort". |
| Q5 limitations (CL-33) | A short block of 3–5 items, median ≈ 230 words | Limitations block of about 190 words: one-error-at-a-time, single dataset and error-free clean-model targets added. |
| Q6 recommendations (CX-26) | Framed as "implications" or "potential" | "four considerations … not validated decision rules". |
| Q8 identical headings (AG-21) | 0/10 papers repeat a heading | II-E renamed "Three-Dimensional CFD Setup". AG-21 changed from decline to fix. |
| Q9 conclusion (CL-01, CL-02, CX-28, CL-47) | Scoped claims; no "any pipeline" | Applied as planned. |
| Q10 abstract (CX-02) | "in silico" stated; "to our knowledge" used in 0/12 | "We tested in silico whether …" replaces the "untested" claim. |
| Q11 solver detail (CX-08) | 0/12 report it | Kept in the supplement only (S1, one sentence). |
| Q12 citations (CL-40) | Ascending and compressed | `cite` package. |

### Line budget outcome
- Cuts:
  - Methods outline paragraph; Fig. 1 is now cited in II-C.
  - Intro closing sentence.
  - The developer sentence in IV-C.
  - "Three findings stand out" in IV-A.
  - The bed-mechanism repeat in IV-A.
  - The demand clause in Limitations, and the 50% DS FFR values in III-E.
  - OpenFOAM scheme wording, the III-A outlet clause, and the 22%/89% duplicate in III-B.
  - The pre-specification sentences.
- Result: main 8 pp (page 8 right column ends at y = 695 pt, against 731 pt before the fixes), supplement 6 pp, abstract 246 words, overfull count unchanged (9).
