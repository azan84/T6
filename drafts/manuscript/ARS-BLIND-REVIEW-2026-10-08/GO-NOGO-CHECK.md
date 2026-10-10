# Go/no-go blind verification read: JBHI SI (2026-10-08)

Inputs: blind2/manuscript.txt, blind2/supplement.txt, page images ms-page-5/6 and supp-page-5; roadmap lines 210–270 (R1–R8). No other files were opened.

## A. Must-fix items R1–R8

| # | Status | Evidence |
|---|---|---|
| R1 3D interpretation | RESOLVED | III-D: "so in this instance per-territory tuning removed the error." The abstract gives 0.074 → −0.0007. No sentence says the 3D case shows concealment. One residue remains: Fig. S1 box 3D-c says "outlets under Protocol A or C", but II-E says "per-outlet form of Protocol D". |
| R2 Concealment limited to the tuning tested | RESOLVED (full fix) | Protocol D was added. The abstract reads "with one global or one per-territory tuning parameter", and the D rates are reported per bed (Table I; III-B "21 of 104 (20%)… and 9 of 171 (5%)"). |
| R3 Calibration, not validation | PARTIAL | The main text is clean (IV-A: "The check measured agreement with the fitted targets, not the correctness"). The supplement still uses "validation": the S5-A heading is "Validation Threshold" and the Table S3 caption ends "BY VALIDATION THRESHOLD". There is no explicit context-of-use sentence; IV-C covers only the defer/treat bias direction. |
| R4 Caliber passes-and-wrong and the "minor risk" guidance | RESOLVED | Abstract: "4–18% of tuned caliber-error models passed"; "branching and caliber must be checked before tuning". IV-C step 2 is now conditional on tuning, and the mechanism is given in III-B. The phrase "minor risk" is gone. A residual point is listed in C-8. |
| R5 Tuning attribution and its test | PARTIAL | Protocol A rates are in the main text (III-B: "Under Protocol A they were 12% and 20%"). C vs B and D vs B are tested by McNemar. **The C vs A paired test on passes-and-wrong is still not reported** (II-F: "compared with Protocol B by the same test" only). The pre-tuning step was revised in IV-C, but its "22%" appears in no table. |
| R6 Conditional rates | PARTIAL | II-F: "its rates are conditional on that design and are not clinical prevalences". IV-A: "ranking holds for the magnitudes studied". **The abstract rates carry no conditional qualifier** (this was the acceptance criterion). Band counts for the discrete bed are not reported. IV-A still opens with "the decision risk of segmentation lay mainly in the branching". |
| R7 Flow regime | RESOLVED (acceptance met) | Demand ×2 and ×3 were run with re-selected cohorts (III-E, Table S5). II-B compares radii with normal values ("median inlet radius 1.60 mm" against 3.7 mm diameter). The half-voxel radius bias is still not quantified. The discrete arm is reported at ×2 only (n = 47). |
| R8 Open code and pre-specification | OPEN | Data statement: "The code and the frozen cohort list are available from the corresponding author on request." There is no DOI. The hash is truncated ("SHA-256 b8fe7909…"). Protocol D and the demand replication are flagged as post hoc. The 13%/16% thresholds, the ×0.7/×1.3 sensitivity, the simulated floor and the mixed model are not flagged. |

## B. Internal consistency audit

### Verified (no action needed)
- **Abstract.** All of the following were recomputed from the Table I counts and match: 32–33% vs 6–10% (45/137, 20/194; 84/265, 17/300); 5–19% (B: 24/173 and 13/267; C: 20/104 and 14/171); 5–20% topological passes-and-wrong; 4–18% caliber (9/194, 35/194, ~37/300, 12/300); 3–4% floor (S6); "none" caliber under B (Table I T3/T4 B = 0 in both beds); 0.074 → −0.0007.
- **III-A.** 2 599 solves = sum of the Table I A–C n. Protocol D 8/11 and 6/4 match. The caliber flip range 1–14% matches. The undefined counts (33/77, 47/118, 36/96, 49/149) match the Table I n and Table S1.
- **III-B.** 20/104, 14/171, 21/104 and 9/171 match Table I and S3. "Under Protocol A 12% and 20%" matches S3. The caliber p ≤ 0.004 is consistent with exact McNemar on 9 vs 0 and 12 vs 0 discordant pairs.
- **III-C.** Medians 0.095/0.077 and 0.047/0.015 match Table S4. D 0.000/0.004 matches Fig. S3. 10/44 matches Table I T1 D at 23%.
- **III-E.** 33–50 vs 1–5, 3–20, 3–20 and 1–14 match the Table S5 rows at ×2 and ×3.
- **IV-A and Conclusion.** "Three to six times" (3.3×, 5.6×), "18–43% to 2–20%" and the Conclusion's 5–20% and 4–18% all match.
- **S3, S4 and S5 at scale 1.** These agree with Table I. The "All" rows of S3 recompute correctly.

### Mismatches
1. **III-B, "Under Protocol B the proportions were 2% and 6%."** Table S3 (T1+T2, B, 10%) gives 1 (0–5) discrete and 5 (3–8) leaky. Table S5 (topological B, scale 1) gives 1 (0–4) and 4 (2–7). Table I gives 2/137 = 1.5% and ~10/218 = 4.6%. The text matches neither table.
2. **Denominator convention differs between tables.** Table I and S3 use only models with a defined residual. The S5 footnote says "denominators include models without a defined residual". The same quantity therefore appears as 1/5 in S3 and 1/4 in S5. Use one convention or flag it in both captions.
3. **II-B demand.** "median inlet radius 1.60 mm" with k = 562 s⁻¹ gives k·r³ = 2.30 mL/s (138 mL/min). The text gives "2.1 mL/s (126 mL/min)". Because Q is monotone in r, the two medians cannot both be correct over the same set of trees.
4. **IV-D vs III-D.** IV-D says the meshed-lumen offset "shifts absolute FFR but not the paired differences". III-D reports a different paired difference on the requested radius: +0.127, against +0.074 (3D) and +0.081 (twin). The baseline also moves from 0.761 to 0.870 across 0.80.
5. **IV-A and Conclusion vs III-B and III-D.** IV-A says "A tuned model passes by construction"; the Conclusion says "passes the perfusion check whether or not its FFR is correct". III-B gives the median Protocol C residual for discrete topological models as 0.14, so most fail the 10% check. III-D reports that Protocol C left +0.107 "with a residual of 0.30, which fails the check". The statement is true only for Protocol D.
6. **IV-C vs III-A.** IV-C says caliber errors "flipped decisions about as often as repeat invasive measurement without tuning". III-A says the taper exceeded the floor by its lower confidence bound under fixed boundary conditions (13% discrete, 9% leaky).
7. **IV-A.** "one in five tuned topological-error models remained materially wrong". The 19–20% figure is passes-and-wrong. The materially-wrong fraction itself is not reported and would be higher.
8. **Abstract and III-E direction claims at higher demand.** "The directions held at doubled and tripled hyperemic demand" does not hold as written:
   - The discrete bed was not run at ×3; III-E says "reported at twice the demand only".
   - "against 0–5% with re-derived boundary conditions" relies on caliber passes-and-wrong under B, which is absent from Table S5 (topological B only: 5, 2 and 4).
   - No paired test is reported at ×2 or ×3. Discrete ×2: C 14 (7–26) vs B 5 (2–12), with overlapping CIs.
9. **S2.** It says D "reached the bound of 10³ in two… models" and then "A fit that ends at a search bound is recorded as a failure; none did in the ablation". These contradict each other. The D search range is also not given in II-D (C uses ±1.5 decades).
10. **III-A, "All 2 599 corrupted-model solves converged".** This total covers A–C only. The ~769 Protocol D solves are not accounted for.
11. **"held in both beds", "significant" and "none" claims.**
    - The excess of tuned over re-derived passes-and-wrong is correctly limited to the discrete bed in IV-A.
    - The abstract sets "5–20%" against "3–4% for correct anatomy" without bed qualifiers. In the leaky bed, D 5 (3–10) and C 8 (5–13) sit at or near the 3.9 (3.2–4.6) floor, and S4 reports 3% at ×0.7.
    - III-A's "topological > caliber under A–C in both beds" is stated as direction only. The leaky-bed values for B and C are p = 0.18 and 0.057, which the text reports correctly.
    - "None" for caliber under B is correct (Table I).
12. **III-A floor claim.** "Only the taper exceeded this noise floor with its lower confidence bound … 9% leaky". The leaky T4 A interval is 6–15, and a lower bound of 6 does not clearly exceed a floor of 5.0–6.5%. Give the cell-specific floor or drop the leaky case.
13. **IV-C, "only 22% of re-derived topological-error models passed… in the leaky bed most did".** No table reports pass rates by protocol, so this cannot be checked. It is also in tension with III-A, "Protocol B models … failed their own perfusion check most often", and with the leaky B median residual of about 0.10 implied by III-B.
14. **III-B, "lowered the median perfusion residual … from 0.19 to 0.14".** The comparator protocol (A or B) is not named.
15. **Fig. S1.** The caption box says "Tables S1–S6"; the supplement has S1–S7. Box 3D-c gives the protocols as A/C (see R1).

## C. New issues introduced by the revision

| # | Issue | Rating |
|---|---|---|
| C-1 | "A tuned model passes by construction" (IV-A), "the perfusion check no longer carried information about the error" (IV-A) and the Conclusion's "passes … whether or not its FFR is correct" are contradicted by the paper's own Protocol C residuals (B-5). A referee will use this to argue that the conclusion overreaches. Restrict it to per-territory tuning, or rephrase as "a passing tuned model may still be wrong". Text-only fix. | BLOCKER (if left) |
| C-2 | The abstract leads on tuned-model rates without per-bed values. The tuning-specific excess holds only in the discrete bed; in the leaky bed tuned topological passes-and-wrong (5–8%) is near the correct-anatomy floor (3.9%). Give per-bed values, e.g. "19–20% discrete, 5–8% leaky", and keep the abstract at or under 250 words (it is now 248). | FIX-BEFORE-SUBMIT |
| C-3 | III-B gives the B passes-and-wrong as 2%/6%, which disagrees with S3 and S5 (B-1). Denominator conventions differ between tables (B-2). | FIX-BEFORE-SUBMIT |
| C-4 | The demand arithmetic is inconsistent (2.1 vs 2.30 mL/s; B-3). | FIX-BEFORE-SUBMIT |
| C-5 | The "directions held at doubled and tripled" claim (abstract, III-E) needs to say "both beds at ×2, leaky bed at ×3". Either add caliber B to Table S5 or drop "0–" (B-8). | FIX-BEFORE-SUBMIT |
| C-6 | The Limitations claim "not the paired differences" is contradicted by +0.127 vs +0.081 (B-4). The 3D baseline (0.870) and the requested-radius baseline (0.761) fall on opposite sides of 0.80. Say so plainly. | FIX-BEFORE-SUBMIT |
| C-7 | In the 3D case, "Protocol D" is an oracle: clean territory flows are prescribed per outlet, which is not a fitted per-territory scaling. "Per-territory tuning … in three dimensions it reduced a shift" (abstract) invites the objection that the result is trivial. Call it "prescribed clean territory flows (the limit of per-territory tuning)". | FIX-BEFORE-SUBMIT |
| C-8 | "Per-territory tuning corrected the typical missed branch" (abstract) does not mention that D gives the largest passes-and-wrong cell in Table I (T4 discrete 36%) and 23% for T1 discrete. The pooled caliber range 4–18% also hides the 24% (T4 C leaky) and 36% cells. Name the taper explicitly. | FIX-BEFORE-SUBMIT |
| C-9 | IV-C "about as often as repeat invasive measurement without tuning" contradicts the taper result in III-A (B-6). The "one in five … remained materially wrong" wording (B-7) should read "passed while materially wrong". | FIX-BEFORE-SUBMIT |
| C-10 | S2 contradicts itself on fits reaching the bound (B-9). The D search range is undefined in II-D. The III-A convergence count omits D (B-10). | FIX-BEFORE-SUBMIT |
| C-11 | The Fig. S1 leftovers (Protocol C in 3D-c; Tables S1–S6) and the "Validation" wording in S5-A and the Table S3 caption. | FIX-BEFORE-SUBMIT |
| C-12 | R5: no C vs A McNemar on passes-and-wrong. In the leaky bed A (20%) > C (8%), so tuning reduced passes-and-wrong relative to fixed boundary conditions; this belongs in the text. The "22%" figure in IV-C has no table source (B-13). Add pass rates by protocol to Table S3. | FIX-BEFORE-SUBMIT |
| C-13 | R6: the abstract has no qualifier stating that rates are conditional on a cohort stratified around 0.80. A five-word fix. | FIX-BEFORE-SUBMIT |
| C-14 | R8: the data statement is still "on request" and the hash is truncated. The paper offers a test "a developer can apply" (IV-C) but does not release it. JBHI does not mandate code release, but at least one referee will ask. Add a Zenodo DOI, the full SHA-256, and post hoc flags for the thresholds, the ×0.7/×1.3 runs, the simulated floor and the mixed model. | FIX-BEFORE-SUBMIT |
| C-15 | Protocol D is disclosed as run post hoc, yet it carries abstract and Conclusion claims. This is disclosed, but it is worth one clause in IV-D. | OPTIONAL |
| C-16 | At ×3 demand most healthy discrete networks lost more than 10% of aortic pressure. This suggests resistance is overestimated (radius bias), which cuts against "segmented arteries narrower than normal" as the sole explanation. Quantify the half-voxel bias, or add one sentence. | OPTIONAL |
| C-17 | III-A floor claim for leaky T4 (lower bound 6 vs floor up to 6.5; B-12). III-B residual comparator unnamed (B-14). | OPTIONAL |
| C-18 | The abstract's "must be checked before tuning" is prescriptive, while IV-C says "not validated decision rules". "Should" is safer. Ref [9] (pulmonary-valve FSI) is a weak support for coronary perfusion tuning. Table S2 gives identical severity coefficients in both beds (0.019 (0.016, 0.022)); confirm this is not a copy error. | OPTIONAL |

## D. Verdict: GO WITH FIXES

The revision resolves the substantive objections. The 3D result is now read correctly, per-territory tuning was added and reported, demand was replicated at ×2 and ×3 with re-selected cohorts, and caliber passes-and-wrong is in the abstract. The core numbers in the abstract, Results and Conclusion recompute from Table I and the supplement tables. What remains is text, plus one small computation:
- **C-1 (critical):** remove "passes by construction" and "whether or not" for Protocol C.
- **C-2, C-13:** per-bed values and the conditional qualifier in the abstract, within 250 words.
- **C-3, C-4:** correct the B rates (2/6 vs 1/5) and the demand arithmetic.
- **C-5, C-6, C-7, C-8:** bound the demand claim to the beds actually run, fix the 3D paired-difference limitation, and use oracle wording for the 3D Protocol D.
- **C-9, C-10, C-11:** IV-C wording, S2 contradiction, Fig. S1 and "Validation" leftovers.
- **C-12:** add the C vs A paired test and pass rates by protocol.
- **C-14 (R8):** DOI and full hash. This is not strictly required by JBHI but is cheap.

If C-1 to C-8 are fixed, I expect minor-to-major revision rather than rejection. The main remaining risks are scientific, not textual: there is one 3D case, and the tuning-specific concealment effect is limited to the discrete bed.
