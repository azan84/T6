# Referee report: methodology (reduced-order modelling, UQ, statistics)

Manuscript: "Topological Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study" (IEEE JBHI)
Reviewer persona: computational hemodynamics / UQ (0D/1D coronary models, sensitivity studies)
Material read: manuscript.txt, supplement.txt, ms-page-1..8, supp-page-1..6 (figures and tables inspected visually).

## Summary

The authors insert one idealized cosine stenosis into each of 150 instances (108 trees, 93 patients) from the ImageCAS-X test split, selected so that the leaky-bed clean FFR is stratified over 0.65–0.95. They then apply four segmentation errors: missed side branch (T1) and vessel break (T2), which are topological, and lesion lengthening by HD95 (T3) and a 0.93 taper (T4), which are caliber errors of inter-observer magnitude. FFR is recomputed with a steady hyperemic Poiseuille + Young–Tsai network model under four boundary-condition protocols: A fixed, B re-derived, C one global scaling tuned to clean territory flows, D per-territory tuning. Two microvascular bed laws are used: a leaky Murray-cube bed (n = 150) and a discrete r^2.66 outlet bed (n = 97). The outcomes are decision flips at 0.80 and "passes-and-wrong" (perfusion residual < 10% and |ΔFFR| > 0.05). These are compared against a repeat-FFR noise floor and a simulated correct-anatomy floor. A single 3D OpenFOAM case checks the direction of the missed-branch effect, and the pipeline is replicated at 0.7/1.3x demand and at 2x/3x demand with re-selected cohorts. The headline results are as follows. Topological errors flip 32–33% of decisions under fixed BCs, against 6–10% for caliber errors. Re-derivation and tuning reduce topological flips to 5–19%. After tuning, 19–20% (discrete) and 5–8% (leaky) of topological-error models pass the perfusion check while materially wrong, against 3–4% for correct anatomy.

The study is carefully executed, and the arithmetic is unusually clean: I reproduced essentially every proportion and Wilson interval I checked. My concerns are about what the "perfusion check" can show when its targets are noise-free oracle flows from the same model, the like-for-like status of the floor comparison, statistical dependence, and the model-structural reasons why caliber errors may look benign.

## Strengths

1. Decision-level outcome (flip at 0.80, material error > 0.05) is clinically interpretable and is benchmarked against repeat invasive FFR variability (SD of difference 0.018); my uniform-band approximation of that floor gives about 4.8%, consistent with the reported 5.0–6.5%.
2. Clean ablation design: one error at a time on otherwise identical anatomy, same measurement node matched by coordinate, own clean model as the reference.
3. The protocol ladder (fixed / re-derived / one-parameter over-determined / per-territory exactly-determined) is well conceived. The paper explicitly notes that matching flow and pressure would reproduce clean FFR by construction, so only flow is matched.
4. Two bed laws that treat deleted vessels differently, with claims restricted to findings whose direction agrees in both beds.
5. Exhaustive accounting: defined vs solved models (2 802 vs 2 599), Protocol D solves (769), exclusions by reason (Table S1), convergence and mass-conservation error. All counts reconcile.
6. The demand replication re-selects the cohort at 2x and 3x demand rather than only rescaling. This is the right way to keep the cohort spanning 0.80.
7. 3D mesh checks are disclosed honestly, including a failed acceptance criterion (Section S7, Table S8).
8. Caliber magnitudes are tied to measured inter-observer statistics (T4 from DSC via 2λ²/(λ²+1) = 0.928 → λ = 0.930, verified).

## Weaknesses

**W1 (major): the perfusion check is evaluated against noise-free oracle targets that are the tuning targets, so "passes" is near-tautological under tuning and the floor comparison is not like-for-like.**
Evidence: "Tuning targets were error-free clean-model flows (noise entered only the simulated floor)" (Limitations). "Per-territory tuning passes almost every model by design" (IV-A). Abstract: "19–20% (discrete bed) and 5–8% (leaky bed) of topological-error models ... against 3–4% for correct anatomy". The 3–4% floor (Table S7) comes from correct anatomy tuned to noisy targets, where only 72% pass. The corrupted models were tuned to noise-free targets, so their pass probability is inflated relative to the floor condition. Under Protocol D, "passes-and-wrong" reduces to the rate of |ΔFFR| > 0.05.
Fix: (i) rerun Protocols C/D for corrupted anatomy with the same 20 noisy target draws per instance, and report passes-and-wrong per draw so it is directly comparable with Table S7; (ii) reword the abstract contrast or present it only for the like-for-like condition.

**W2 (major): passes-and-wrong conflates the pass rate and the error rate, and the conditional quantity the Discussion relies on is not reported.**
Evidence: "After one global scaling, about half of the models that passed were materially wrong" (IV-A). The number of passing models per cell is never given. In the leaky bed the median Protocol C residual of topological models is 0.02 (III-B), so at least half of 171 (≥ 86) pass, while only 14 are passes-and-wrong. That gives at most about 16% of passers, not about half. The claim can at most hold in the discrete bed. Comparisons with B are also confounded: B scores low partly because "only 22% of re-derived topological-error models in the discrete bed ... passed".
Fix: for every bed × error class × protocol, add pass n, wrong n, and P(wrong | pass) with Wilson CI (a 2×2 per cell). Restrict the "about half" sentence to the bed in which it holds.

**W3 (major): the inference ignores clustering. The Wilson CIs and "lower bound above the floor" statements are used inferentially although declared descriptive.**
Evidence: "Instances are clustered within patients, so the confidence intervals are descriptive". Yet the text states "Only the taper exceeded this noise floor with its lower confidence bound". The pooled counts (e.g. 45/137) mix two error types per instance and up to two instances per tree (150 instances / 93 patients). The simulated floor CIs (3.1%, 2.4–4.0) treat 20 draws per instance as independent. The Bayesian model is fitted by variational inference with "posterior mean ±1.96 posterior standard deviations", which typically understates posterior spread. It also omits Protocol D. The leaky T4-A cell, 9 (6–15), has a lower bound of 6 against a floor of "5.0–6.5% across cells", so the "only the taper in the discrete bed" statement depends on per-cell floors that are not reported.
Fix: use a patient-level cluster bootstrap for all headline proportions and contrasts (including the floor). Report the per-cell repeat-FFR floor. Either add D to the mixed model and verify with MCMC (or a frequentist GLMM), or drop the "agreed" claim.

**W4 (major): the ROM structure may mechanically suppress caliber effects, especially T3, which affects the topological-vs-caliber ranking.**
Evidence: the stenosis loss is "∆p = K Q|Q| ... K = ρKt (A0/As −1)²/(2A0²), Kt = 1.52". It has no length dependence, and only the expansion term is lumped. T3 ("2.46 mm longer about the same center") leaves A0/As unchanged, so its effect enters only through Poiseuille resistance over 2.46 mm of partially narrowed lumen. The near-null T3 rows in Table I (7% in all four protocols, discrete) are therefore expected from the model form. HD95 is a whole-tree surface-distance statistic, and its use as a lesion-extent error is a modelling choice.
Fix: add a sensitivity analysis with the full Young–Tsai form (viscous Kv term with lesion length, or a length-dependent loss such as Gould/Lance), or with a 3D T3 case. Qualify the ranking as conditional on the lesion-loss model, and justify the HD95 → lesion-length mapping.

**W5 (minor–major): the 3D verification is a single case, and the per-territory result is largely by construction.**
Evidence: "With the clean territory flows prescribed at the outlets (the limit of Protocol D), the same error changed FFR by −0.0007". When the outlet flows are prescribed, the flow through the lesion is fixed by the targets, so a near-zero shift is expected in any solver. The meshed throat radius (0.276 vs 0.231 mm) implies an area 1.43× larger, which is an effective DS of about 76% rather than 80%. The baseline therefore moved from 0.761 to 0.870, across 0.80. The methods state a discretization uncertainty of "5.5 × 10−4", but the patient-specific refinement changed FFR by 0.0021, about 4× larger. The acceptance criterion "was not met" (S7), and the finest mesh did not reach the residual limit. The main text reports the 0.0021 but not that the criterion failed.
Fix: state in the main text that the GCI acceptance failed for the patient case, and quote the patient-case uncertainty (about 0.002) as the 3D uncertainty. Describe the Protocol D 3D result as a consistency check, not independent evidence. Ideally add a second 3D case with the meshed throat matched to the ROM throat.

**W6 (minor): demand and physiological realism.**
Evidence: median demand of 137 mL/min per tree (II-B), below thermodilution values for the LAD alone. An 80% DS proximal LAD lesion gives a baseline FFR of 0.761–0.870, which implies a lesion flow of the order of tens of mL/min. The 2×/3× replication is welcome, but the abstract states "The directions held at doubled and, in the leaky bed, tripled demand", while III-E reports that at 2× the excess of passes-and-wrong over B was significant "in no topological one". The headline topological passes-and-wrong finding is therefore directionally preserved but not supported inferentially at higher demand.
Fix: qualify the abstract sentence ("point estimates kept their direction; the topological excess was not significant at 2×"). Report the median lesion flow and throat Reynolds number for the cohort.

**W7 (minor): perfusion-check definition.**
Evidence: the residual is the "root mean square of the relative differences" over territories defined as subtrees below the first bifurcation. For a left tree this is usually two numbers (LAD/LCx). The 10% threshold is justified from a single-measurement bound "1.96 × (10–15%) ≈ 20–29%". A two-territory RMS check is coarse compared with segmental perfusion maps, and one parameter against two targets (Protocol C) is barely over-determined.
Fix: report the number of territories per tree (distribution), and add a sensitivity analysis with finer (e.g. per-outlet or segment-level) territories, at least for the discrete bed.

**W8 (minor): inconsistent conventions and rules.**
(a) Denominators. Table I/S3 exclude models without a defined residual, whereas the Table S5 footnote says "denominators include models without a defined residual, which do not pass". The same quantity, discrete topological passes-and-wrong under B, therefore appears as 1% (0–5) [S3, n = 137], 1% (0–4) [S5, n = 173] and 2% [III-B, n = 104 "same instances"]. In the leaky bed it is 5%, 4% and 6%. Table I also shows a single n column that is not the passes-and-wrong denominator for three T2 cells.
(b) The Fig. 3 caption ("Protocol D residuals lie below 0.01") contradicts S2/III-B (two D models at 0.08 and 0.11).
(c) A C fit at the search edge is a failure, but D fits at the 10³ bound "are retained".
(d) Protocol A T2 instances with no remaining bed outflow (36 discrete) are excluded, although physically such a model gives FFR → 1 (a flip for any clean FFR ≤ 0.80). This biases the A-T2 flip rate.
Fix: harmonize the denominators (or add the passes-and-wrong n as a column), correct the Fig. 3 caption, apply one bound rule, and report A-T2 with the zero-outflow cases scored as flips as a sensitivity analysis.

**W9 (minor): McNemar reporting.**
Evidence: "22 reversed, 12 created, p = 0.24". The exact two-sided McNemar p is 0.121, and 0.24 equals the Holm-adjusted value at rank 2. Fix: label all reported p as raw or Holm-adjusted.

**W10 (minor): reproducibility.**
Evidence: "The code is available from the corresponding author upon reasonable request." The pipeline is fully automated with a fixed seed (20260918), so releasing the code and the cohort list (scan ID, host vessel, position, length, DS) is low-cost and expected for JBHI.
Fix: deposit the code, cohort list, per-model outputs and the 3D case package (DOI).

## Recomputation log

| # | Check | Source | Result |
|---|-------|--------|--------|
| 1 | Topological flips A, discrete: T1 21/77 + T2 24/60 = 45/137 = 32.8% (25.5–41.1) | III-A, Table I | Match (33%, 26–41) |
| 2 | Caliber A discrete: T3 7/97 + T4 13/97 = 20/194 = 10.3% (6.8–15.4) | III-A | Match |
| 3 | Leaky A: topological 21/118 + 63/147 = 84/265 = 31.7% (26.4–37.5); caliber 3+14 = 17/300 = 5.7% (3.6–8.9) | III-A, S6 | Match |
| 4 | Topological B/C/D pooled: d 24/173 = 13.9, 20/104 = 19.2, 8/104 = 7.7; l 13/267 = 4.9, 14/171 = 8.2, 10/171 = 5.8 | Abstract "5–19%", S6 | Match |
| 5 | Per-type range A 18–43%, after B–D 2–20% | IV-A | Match |
| 6 | D flips topological vs caliber: 8% vs 21/194 = 10.8% (d); 6% vs 11/300 = 3.7% (l) | III-A "8% and 11%, 6% and 4%" | Match |
| 7 | Every Table I Wilson CI recomputed from implied counts (e.g. T1-D d 1/44 → 2 (0–12); T1-C d 8/44 → 18 (10–32); T2-A l 63/147 → 43 (35–51)) | Table I | All match |
| 8 | Topological passes-and-wrong C: 9/44 + 11/60 = 20/104 = 19.2 (12.8–27.8); D 10 + 11 = 21/104 = 20.2 (13.6–28.9); leaky C 8 + 6 = 14/171 = 8.2 (4.9–13.3); D 3 + 6 = 9/171 = 5.3 (2.8–9.7) | III-B, abstract | Match |
| 9 | Caliber passes-and-wrong: C d 9/194 = 4.6; D d 35/194 = 18.0; C l 37/300 = 12.3; D l 12/300 = 4.0 → "4–18%" | III-B, abstract | Match |
| 10 | Table S3 totals: All-A d 23/331 = 6.9; All-C d 29/298 = 9.7; T1+T2 A l 43/218 = 19.7; All-A l 53/518 = 10.2; All-C l 51/471 = 10.8 | S3 | Match |
| 11 | Same quantity under different denominators: topological P&W B d 2/137 = 1.5 (0.4–5.2) [S3]; 2/173 = 1.2 (0.3–4.1) [S5]; 2/104 [text 2%]; leaky 10/218, 10/267, 10/171 | S3, S5, III-B | Internally consistent but conflicting conventions (W8a) |
| 12 | Solve counts: A–C solved, discrete 996 + leaky 1 603 = 2 599; defined 1 101 + 1 701 = 2 802; difference 203 = sum of Table S1 exclusions; D 298 + 471 = 769 | III-A, S2 | Match |
| 13 | Undefined C/D: 33/77, 47/118, 36/96, 49/149; n(C) = 44, 71, 60, 100 | II-D, S1 | Match |
| 14 | Floor draws: 97×20 = 1 940; 150×20 = 3 000 − 10 failed = 2 990; total 4 940 | S2, S7 | Match |
| 15 | Floor CIs: 120/1940 = 6.2 (5.2–7.3); 215/2990 = 7.2 (6.3–8.2); 60/1940 = 3.1 (2.4–4.0); 116/2990 = 3.9 (3.2–4.6) | Table S7 | Match (CIs ignore within-instance clustering, W3) |
| 16 | Demand: 562 × (1.85 mm)³ = 3.56 mL/s = 214 mL/min; median r_in 1.595 → 2.28 mL/s = 137 mL/min (1.60 → 2.30) | II-B | Match within rounding |
| 17 | T4 λ from 2λ²/(λ²+1) = 0.928 → 0.9304 | II-C | Match |
| 18 | Repeatability bound 1.96 × 10–15% = 19.6–29.4% | II-F | Match |
| 19 | Repeat-FFR floor, uniform 0.65–0.95 baseline, SD 0.018 → 4.8% | II-F, Table I note 5.0–6.5% | Consistent |
| 20 | McNemar exact, 22 vs 12 → p = 0.121 raw; 0.24 = Holm ×2 | III-A | Consistent only as Holm-adjusted (W9) |
| 21 | McNemar caliber P&W vs B, 9 vs 0 → p = 0.0039 | III-B "p ≤ 0.004" | Match |
| 22 | Protocol C vs A P&W discrete p = 0.07 (e.g. 7 vs 1 → 0.070) | III-B | Plausible |
| 23 | "Reversed 14–56 topological flips": d T1 21→7 (14), l T2 63→7 (56) | III-A | Match |
| 24 | Demand replication ranges: A topological 33–50, caliber 1–5; tuned flips 3–20; P&W topological 3–20, caliber 1–14; B 2–5 / 0 | III-E vs Table S5 | Match |
| 25 | S5 discrete 2× caliber: 0/94 (0–4), 1/94 (0–6), 13/94 = 13.8 (8.3–22.2) | Table S5 | Match |
| 26 | Missed-branch ΔFFR medians 0.095/0.077 and 0.047/0.015 | III-C vs Table S4 | Match |
| 27 | 3D: 0.944 − 0.870 = 0.074; throat area ratio (0.276/0.231)² = 1.43, i.e. effective DS about 76% | III-D | Match; physical offset noted (W5) |
| 28 | Mesh sizes 3.5–3.9 M vs control 3.66 M | II-E, Table S8 | Match |
| 29 | Cohort: 6 bands × 25 = 150; 50 per vessel; 280 vessels × ≤32 = 8 960 ≥ 6 944 | II-A, S1 | Match |
| 30 | "About half of passing models wrong after C": leaky median residual 0.02 → ≥ 86/171 pass, 14 P&W → ≤ 16% | IV-A | Mismatch (W2) |
| 31 | Fig. 3 caption "Protocol D residuals lie below 0.01" vs two D models at 0.08 and 0.11 | Fig. 3, S2 | Mismatch (W8b) |
| 32 | Abstract "directions held at doubled ... demand" vs III-E "in no topological one" significant | Abstract, III-E | Overstatement, not numeric (W6) |

## Rubric scores

| Code | Dimension | Score | Flag | Justification |
|------|-----------|-------|------|---------------|
| S1 | Novelty and contribution | 7 | pass | Decision-level, protocol-ladder test of topological vs caliber error and the "passes-and-wrong" concept are new and useful, though partly expected by construction. |
| S2 | Methodological rigour | 6 | warn | Clean ablation, but oracle noise-free tuning targets, non-like-for-like floor, clustering ignored in inference, length-free lesion loss. |
| S3 | Claims supported by evidence | 6 | warn | "About half of passers wrong" is contradicted in the leaky bed, the demand-robustness wording overstates it, and the 3D Protocol D removal is by construction. |
| S4 | Domain / physiological accuracy | 6 | warn | Standard steady-hyperemia ROM and scaling laws, but low demand, two-territory perfusion check, HD95 → lesion length mapping. |
| S5 | Internal consistency | 8 | pass | About 30 recomputations reproduce; only denominator-convention conflicts, one caption contradiction, and one Discussion claim. |
| S6 | Clarity, structure, readability | 7 | pass | Logical and concise. Dense in denominators, and the n column in Table I is not the P&W denominator. |
| S7 | Venue fit (JBHI) | 7 | pass | Digital-twin calibration and segmentation QA are relevant to JBHI. The informatics angle (QC rules) could be made more operational. |
| S8 | Reproducibility and transparency | 6 | warn | Seeds, parameters and exclusions are fully documented, but code is on request only and the 3D evidence is a single case. |

**Overall: 6.6 / 10**

**Recommendation: major revision.** Additional analyses are needed: corrupted models tuned to noisy targets, conditional P(wrong | pass), patient-cluster bootstrap, and a lesion-length-dependent loss sensitivity analysis. None of them is likely to overturn the direction of the findings, but they are required to support the abstract's quantitative contrasts.
