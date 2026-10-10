# Referee report: methodology (reduced-order hemodynamics and UQ)

Manuscript: "Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study" (IEEE JBHI)
Reviewer persona: computational hemodynamics / uncertainty quantification, 0D/1D coronary models.
Material read: manuscript.txt, supplement.txt, ms-page-3/5/6/7.png (Fig. 1, Table I, Figs. 2–5), supp-page-1/3.png (Fig. S1, Tables S4–S6).

## Summary

The authors insert idealized cosine stenoses (40–80% DS) into 150 lesion instances from 108 ImageCAS-X coronary trees. The cohort is stratified so that the leaky-bed baseline FFR spans 0.65–0.95 in six 0.05 bands. They then apply five segmentation errors one at a time: a missed side branch (T1), a vessel break (T2), lesion lengthening by HD95 (T3), a taper ×0.930 (T4) and a ±half-voxel throat error (T5). FFR is recomputed with a steady, hyperemic reduced-order network: Poiseuille elements plus a Young–Tsai expansion loss. Two microvascular bed laws are used, a leaky Murray-cube distributed outflow and a discrete r^2.66 outlet bed. Four boundary-condition protocols are compared: fixed (A), re-derived (B), one global tuning parameter fitted to clean territory flows (C), and per-territory tuning (D). Outcomes are the flip at 0.80, and "passes-and-wrong", defined as a perfusion residual below 10% with |ΔFFR| > 0.05.

The main findings are as follows. Topological and throat errors flip about one third of decisions under fixed boundary conditions, against 6–10% for off-throat caliber errors. Re-derivation or tuning removes most topological flips but not throat flips. Tuned models pass a main-branch perfusion check while materially wrong in 19–20% (discrete) and 5–8% (leaky) of topological-error cases and in 57–81% of throat-error cases. A finer perfusion check removes most topological concealment. One 3D CFD case confirms the direction of the T1 effect and its removal by prescribed flows.

The design is careful and the statistical reporting is unusually complete. I could reproduce every proportion, Wilson interval and exact McNemar p-value I checked. My concerns are about the physiological operating point: the primary demand is low, and the discrete-bed concealment finding does not replicate at twice the demand. They also concern an asymmetric comparison with the correct-anatomy floor, which uses noisy targets while the error models use noise-free ones, and the narrow 3D verification, which covers one instance and does not test the throat error.

## Strengths

1. **Clean ablation design.** Each error is applied one at a time against an instance-specific clean reference in the same bed. The outcome is the clinically relevant decision at 0.80 rather than a continuous sensitivity. Paired analysis by instance is used throughout.
2. **Error magnitudes are anchored to data where data exist.** T3 is set from HD95 = 2.46 mm. T4 comes from inverting the coaxial-cylinder DSC, which I verified: λ = 0.9304. T5 is set at half the in-plane voxel size. The authors state openly that T1 and T2 are design choices and that the inter-observer DSC is an upper bound.
3. **The boundary-condition protocols are well conceived.** Protocols A–D span fixed, re-derived, under-determined and exactly-determined tuning. The authors explain correctly why matching flow alone cannot be allowed to also match outlet pressure: the clean FFR would then be reproduced by construction. Territory targets include the bed of deleted vessels, which is the physiologically right choice.
4. **Two bed structures, with a both-beds rule for claims.** The authors also re-ran the analysis at a finer territory resolution and at three thresholds for the perfusion check (Tables S3, S8).
5. **Two noise floors are reported, and both are sensible.** One is an analytic repeat-FFR floor (SD 0.018 of the test–retest difference; my uniform-band approximation gives about 4.8%, consistent with the reported 5.0–6.5%). The other is a simulated physiological floor for correct anatomy, with 1 940 and 2 990 draws.
6. **Statistics are rigorous and fully reported.** Wilson intervals, exact McNemar tests with Holm adjustment, sign and Wilcoxon tests, and full denominators are given, and exclusions are tabulated (Table S1). The 36 discrete vessel breaks that lose all outflow under Protocol A are also scored as flips in a sensitivity analysis (40% → 43%).
7. **The verification effort is real.** Halving the centerline spacing changes FFR by ≤ 0.005. A 3D GCI study on an idealized stenosis gives 5.5×10⁻⁴, and patient-case throat refinement gives ≤ 0.0021. A reduced-order counterpart rebuilt on the meshed radius separates model fidelity from radius definition, which is good practice.
8. **Reproducibility is high.** The data are public (CC BY 4.0), the code is public, the selection seed (20260918) and the solver tolerance and relaxation are stated, and Fig. S1 shows a single automated pipeline.

## Weaknesses

**W1 (major). The primary hyperemic demand is sub-physiological, and the discrete-bed concealment result does not replicate at higher demand.**
- *Evidence:* "the cohort's median demand was 137 mL/min per tree" (Methods B); "the excess of tuned over re-derived passes-and-wrong was not significant in any topological comparison at twice the demand" (Results D); Table S5, discrete k×2: topological passes-and-wrong B 6%, C 14%, D 20% on 47 instances.
- *Why it matters:* k is calibrated so that a 3.7 mm LAD carries 214 mL/min. It is then applied to distance-map radii that lie about 0.14 mm inside the lumen (Limitations). The demand per left tree is therefore roughly a third to a half of measured hyperemic flow to the whole left coronary tree. Pressure drops across a stenosis scale super-linearly with Q, so both the flip structure and the size of the tuning correction depend on this operating point. The abstract's "19–20% (discrete)" is the least robust headline number.
- *Fix:*
  - Make a physiologically calibrated demand co-primary. Either correct the radius bias before applying Q = k r_in³, or calibrate k to total coronary hyperemic flow per tree.
  - Report Table I at that demand.
  - Enlarge the discrete-bed replication cohort; n = 47 at ×2 is underpowered for a McNemar test against B. Relaxing the main-vessel FFR ≥ 0.90 criterion is one way to do this.
  - Qualify the discrete-bed concealment figure in the abstract.

**W2 (major). The comparison with "correct anatomy" is not like-for-like: error models are tuned to noise-free targets, the floor to noisy ones.**
- *Evidence:* "Tuning targets were error-free clean-model flows (noise entered only the simulated floor)" (Limitations); the abstract and conclusion contrast passes-and-wrong of 19–20% / 57–81% "against 3–4% for correct anatomy".
- *Why it matters:* With exact targets, an error model whose only mismatch is the error passes more easily than it would against a noisy measurement, which inflates passes-and-wrong. The correct-anatomy rate (3.1%/3.9%) is computed with target noise (CV 0.083) and demand, pressure and viscosity perturbations. The headline contrast mixes two conditions, so neither the excess nor its significance is established. The pipeline already supports noisy targets for error models: "With the error models' targets carrying the same noise, the AUC for topological errors was 0.82 (discrete) and 0.56 (leaky)" (S8).
- *Fix:* Re-run Protocols C and D for all error models with the same 20 noise draws per instance. Report passes-and-wrong as a paired excess over the correct-anatomy draw, matched by instance and draw, with a cluster-aware interval. Keep the noise-free run as an upper bound.

**W3 (major). The 3D verification is a single instance, covers only T1, and leaves untested the error the paper calls dominant (the throat).**
- *Evidence:* "The 3D analysis covers one instance"; the meshed lumen offset of 0.045 mm at the throat "moved the baseline across 0.80 (0.761 against 0.870)".
- *Why it matters:*
  - That sentence shows that a throat-radius change about half the size of T5 (0.088 mm) shifts FFR by about 0.11. This supports the throat finding, but it also means the reduced-order stenosis law (expansion loss with Kt = 1.52 above 30% DS, plus Poiseuille on r(s)) is doing the work in exactly the regime that matters most.
  - A steady laminar simpleFoam solve of an 80% DS jet is also reported without a throat Reynolds number and without evidence that the true flow is steady.
  - The 3D-versus-counterpart baseline agreement is only visible in Fig. 5e as roughly 0.86 against 0.855; it is not stated numerically.
- *Fix:*
  - Add 3D solves of T5 (± half voxel) on the existing instance, ideally on 3–5 instances spanning 50–80% DS and both lengths. Report the 3D-versus-0D baseline FFR and ΔFFR for each.
  - Report the throat Reynolds number and a transient check (pimpleFoam), or justify steady RANS-free laminar flow.
  - Consider adding the Young–Tsai viscous Kv term or a convective-acceleration term and showing that the T5 flip rates are insensitive to the change.

**W4 (minor). The bed-structure contrast is confounded.**
- *Evidence:* the leaky bed uses exponent 3 truncated at 0.50 mm; the discrete bed uses exponent 2.66 truncated at 0.60 mm, on 97 instances, with "baseline FFR bands … derived separately for each bed".
- *Why it matters:* Statements such as "The leaky bed damped topological errors" attribute to bed structure an effect that may come from the exponent, the truncation radius or the cohort.
- *Fix:* Add one cross-run (a discrete bed at exponent 3, or a leaky bed at 2.66 with the same truncation), or restate the contrast as two bed models rather than two structures. Also state how a negative leaky conductance (r_ref³ < Σ r_child³ at non-Murray bifurcations) is handled.

**W5 (minor). The definition of the perfusion residual and its threshold needs tightening.**
- *Evidence:*
  - "A perfusion territory is the subtree below each child of the first bifurcation of the clean tree (a median of two and at most three per tree)."
  - The threshold is justified as "1.96 × (10–15%) ≈ 20–29% for one model output against one measurement".
  - Yet "Correct anatomy … with noise its median is 0.10", so about half of the correct models fail before tuning (S10: false alarm 48–50%).
- *Why it matters:*
  - In the RCA, the first bifurcation can isolate a small conus or RV branch, so the territory is anatomically arbitrary. This also produces the exclusion of most RCA topological instances under C and D.
  - The mapping from a per-region within-subject CV to an RMS taken over two or three territories is not derived.
  - A check that fails half of correct models is not a realistic clinical gate. Its strictness lowers passes-and-wrong for C. For D, which passes almost everything, the metric reduces to the materially-wrong rate.
- *Fix:*
  - Define territories by perfused-mass partitions closer to AHA segments, or justify the first-bifurcation rule per artery.
  - Derive the threshold distribution by simulation under the stated measurement CV.
  - Present passes-and-wrong as a curve over the threshold, rather than at three points.
  - State explicitly that, under D, passes-and-wrong is a wrong-rate. Table S3's footnote already implies this.

**W6 (minor). The statistics do not handle clustering, and the mixed model is incomplete.**
- *Evidence:* "Instances are clustered within patients, so the confidence intervals are descriptive". T5 pools two signs per instance (n = 194/300). Table S2 omits T5 and Protocol D and is "Fitted by variational inference; intervals are posterior mean ±1.96 posterior standard deviations".
- *Why it matters:* Mean-field variational inference typically understates posterior variance, and the mixed model does not cover the two findings the paper emphasizes most (throat, per-territory tuning).
- *Fix:*
  - Report patient-level cluster-bootstrap CIs for the key rates.
  - Refit the mixed model with MCMC, including T5 and Protocol D (and the bed as a factor if the data are pooled).
  - State the Holm family for the passes-and-wrong tests. For example, the reported p ≤ 0.004 for 9 vs 0 discordant pairs equals the raw exact p (0.0039), which is valid only if C is the second-ranked of two contrasts.

**W7 (minor). The wording understates some changes.**
- *Evidence:*
  - "tuning left its flip rate at 37–40%" and "left throat flips unchanged". In the discrete bed the T5 flip rate rose from 30% (A, B) to 38% (C) and 40% (D) (Table I), which is not unchanged, and no McNemar test is given for T5 A against C or D.
  - "their flip rates of 1–14% were of the order of the 5.0–6.5% expected". The discrete taper, 13% (8–22) and 14% (9–23), has a lower bound above the floor.
  - In Results A, "flip rates were unchanged (Supplementary Material)" for finer territories, while S6 says "Flip counts changed by at most five per cell".
- *Fix:* Test T5 A against C and D with McNemar, and reword "unchanged" to "not reduced (30% → 38–40% discrete)". State that the taper exceeds the repeat floor in the discrete bed. Replace "unchanged" with "changed by at most five per cell".

**W8 (minor). Details of the stenosis loss model.**
- *Evidence:* "Where the narrowing exceeds 30% DS, an expansion loss … is lumped at the stenosis"; "A0 and As the reference and throat areas".
- *Why it matters:* The switch at 30% is a discontinuity. The secondary DS −10 error applied to a 40% DS lesion lands exactly at 30%. A0 is not defined as r_fit or r_ref. Using the steady mean flow underestimates the mean convective loss under pulsatile flow by roughly (1 + CV_Q²).
- *Fix:* Apply the loss continuously, or show that no T5 model crosses the switch. Define A0. Add one sentence, or a pulsatile check on the 3D or 0D case, bounding the bias from steady flow near 0.80.

**W9 (minor). Selection of the cohort and of the 97-instance discrete-bed subset is underspecified.**
- *Evidence:* "we drew 25 at random … in each of six 0.05-wide bands" yet "50 each in the LAD, LCx and RCA". The 6 944 eligible instances from 280 vessels are fewer than the 8 960 that 2 positions × 2 lengths × 8 DS would give. "baseline FFR bands were derived separately for each bed".
- *Why it matters:* An exact 50/50/50 split is unlikely under band-only stratification. The baseline distribution of the discrete subset, which drives flip rates, is not shown.
- *Fix:* State whether the vessel was a stratification factor and which criteria removed the remaining combinations. Add a histogram or table of discrete-bed baseline FFR by band.

**W10 (minor). Reproducibility and presentation details.**
- *Evidence:*
  - A GitHub URL with no archived release or DOI.
  - The 3D steps "ran on the CFD machine", and there is no statement that the OpenFOAM cases or meshes are shared.
  - The reduced-order centerline spacing is not given.
  - S10 uses "with a steady inlet pressure" as a convergence indicator although the inlet carries prescribed aortic pressure.
  - The Table S12 column "Flagged cell to throat, mm" is undefined.
  - The Table I column n is the flip denominator, while the passes-and-wrong denominators for T2 (60, 100) appear only in the footnote.
  - The Table S3 label "All" covers T1–T4 only (331 = 77+60+97+97), not T5.
  - The Table S3 footnote "Protocol D matches every territory flow" conflicts with "Pass 297 of 298" and "103 of 104".
- *Fix:* Archive a tagged release on Zenodo with the OpenFOAM cases and per-model result CSVs, and correct each of the labels above.

**W11 (minor). Retaining fits at the Protocol D bound and excluding Protocol A cases bias some cells.**
- *Evidence:*
  - "The 64 Protocol D fits at the parameter bound … were retained; excluding them would raise passes-and-wrong by up to 13 points".
  - "Per-territory tuning passes almost every model by design" (Discussion), yet 43 throat models failed the check under D.
  - The A-versus-B T2 comparison in the discrete bed loses 36 RCA breaks.
- *Fix:* Report T5-D with and without the bound fits in Table I, or in a footnote with numbers. Qualify "almost every model" as applying to non-throat errors.

## Recomputation log

| # | Check | Source | Result |
|---|-------|--------|--------|
| 1 | Topological A discrete 45/137 = 32.8%, Wilson 25.5–41.1 | text "33%, 26–41%" | OK |
| 2 | Caliber A discrete 20/194 = 10.3% (6.8–15.4) | "10%, 7–15%" | OK |
| 3 | n sums: 137 = 77+60; 265 = 118+147; 194 = 2×97; 300 = 2×150; 173 = 77+96; 267 = 118+149; 104 = 44+60; 171 = 71+100 | Table I vs S3/S6 | OK |
| 4 | Leaky topological A: T1 21/118 + T2 63/147 = 84/265 = 31.7% (26.4–37.5) | "32% (26–38%)" | OK |
| 5 | Leaky caliber A: 3/150 + 13–14/150 → 17–18/300 = 5.7–6.0% (3.6–9.3) | "6% (4–9%)" | OK |
| 6 | Table I T1-A d 21/77 = 27 (18.6–38.1); T2-A d 24/60 = 40 (28.6–52.6); T1-D d 1/44 = 2 (0.4–11.8); T2-B d 17/96 = 18 (11.4–26.5) | Table I | OK |
| 7 | Passes-and-wrong C discrete 20/104 = 19.2 (12.8–27.8); leaky 14/171 = 8.2 (4.9–13.3) | text "19%, 13–28%", "8%, 5–13%" | OK |
| 8 | Passes-and-wrong D discrete 21/104 = 20.2 (13.6–28.9); leaky 9/171 = 5.3 (2.8–9.7) | "20%, 14–29%", "5%, 3–10%" | OK |
| 9 | Passes-and-wrong decompositions: C d T1 9/44 + T2 11/60 = 20; D d 10/44 + 11/60 = 21; C l 8/71 + 6/100 = 14; D l 3/71 + 6/100 = 9 | Table I vs text | OK |
| 10 | "10 of 44 and 3 of 71 instances still above 0.05" under D = T1-D passes-and-wrong 23% and 4% | Table I | OK |
| 11 | T5 A,B: discrete 27/97 + 31/97 = 58/194 = 29.9 (23.9–36.7); leaky 38 + 70 = 108/300 = 36.0 (30.8–41.6) | Table I, S7 | OK |
| 12 | T5 passes-and-wrong: C d 110/193 = 57.0 (49.9–63.8); D d 156/194 = 80.4 (74.3–85.4); C l 206/299 = 68.9 (63.4–73.9); D l 243/300 = 81.0 (76.2–85.0) | Table I, S7 | OK |
| 13 | Taper passes-and-wrong D d 35/97 = 36.1 (27.2–46.0); C l 36/150 = 24.0 (17.9–31.4) | Table I | OK |
| 14 | Caliber passes-and-wrong C d 9/194 = 4.6% (2.5–8.6) → "5"; D d 35/194 = 18.0 (13.3–24.1) | text, S3/S5/S8 | OK |
| 15 | Exact McNemar for discrete T2 B vs A, 22 vs 12: raw two-sided p = 0.121; Holm (×2) = 0.243 | "p = 0.24" | OK (Holm-adjusted; label it so) |
| 16 | Exact McNemar, caliber passes-and-wrong C vs B discrete, 9 vs 0: p = 0.0039 | "p ≤ 0.004" | OK (raw = Holm only if second-ranked; clarify) |
| 17 | Exact McNemar, topological passes-and-wrong leaky C vs B, about 4 net discordant: minimum p = 0.125 | "p ≥ 0.12" | OK |
| 18 | S8 McNemar T5 A,B discrete 29%→25%, 7 vs 0: p = 0.0156 | "0.016" | OK |
| 19 | S8 D T5 discrete 80→78%, 4 vs 0: p = 0.125; leaky T1+T2 C 7 vs 1: p = 0.070; D 7 vs 2: p = 0.180; T5 C d 12 vs 1: p = 0.0034 | "0.12", "0.07", "0.18", "0.003" | OK (all reproducible with integer discordant counts) |
| 20 | B-vs-A McNemar consistency: T1-d A 21 → B 7 = 14 reversed (low end of "14–56"); T2-l A 63 → B 7 = 56 reversed (high end) | text | OK |
| 21 | S10 "Flip under B" discrete n = 36 = T1 7 + T2 14 (on 60; 24−22+12) + T3 7 + T4 8 | S10 vs Table I/text | OK |
| 22 | DSC kept ≥ 0.928: 41/45 = 91.1 (79.3–96.5); 52/84 = 61.9 (51.2–71.6) | S7 "91% (79–96)", "62% (51–72)" | OK |
| 23 | Pre-tuning sensitivity, discrete: 114/137 = 83.2 (76.1–88.5) | S10 "83 (76–89)" | OK |
| 24 | S3 wrong-among-passing: A 17/21 = 81.0 (60.0–92.3); B 2/23 = 8.7 (2.4–26.8); C 20/39 = 51.3 (36.2–66.1); leaky C 14/154 = 9.1 | S3, Discussion "20 of the 39", "14 of 154" | OK |
| 25 | Discrete B pass where tuning defined: 23/104 = 22.1%; leaky 152/171 = 88.9% | text "22%", "89%" | OK (consistent with S3 pass counts 23 and 176) |
| 26 | Floors: 120/1940 = 6.2 (5.2–7.3); 215/2990 = 7.2 (6.3–8.2); passes-and-wrong 60/1940 = 3.1 (2.4–4.0); 116/2990 = 3.9 (3.2–4.6) | S11 | OK |
| 27 | Draw counts: 97×20 = 1 940; 150×20 = 3 000; 3 000 − 10 failed C fits = 2 990; 1 940 + 3 000 = 4 940 | S2, S10, S11 | OK |
| 28 | Repeat-FFR floor: uniform baseline 0.65–0.95, SD 0.018 → mean flip probability 4.8% | "5.0–6.5%" | Plausible (bands non-uniform within) |
| 29 | Demand: 562 × (1.85 mm)³ = 3.56 mL/s = 213.5 mL/min | "214 mL/min" | OK |
| 30 | Demand: 562 × (1.60 mm)³ = 2.30 mL/s = 138 mL/min; reported 2.28 mL/s ↔ r = 1.595 mm | "2.28 mL/s (137 mL/min)", "1.60 mm" | OK (median rounding) |
| 31 | 214 within 1 SD of 228 ± 71 and 293 ± 102 | S4B | OK |
| 32 | Taper λ: 2λ²/(λ²+1) = 0.928 → λ = 0.9304 | "0.930", "×0.93", "7%" | OK |
| 33 | Perfusion bound 1.96 × 10–15% = 19.6–29.4% | "20–29%" | OK |
| 34 | Half-voxel: 0.352/2 diameter → 0.088 mm radius; 7.3 DS points implies a reference diameter of about 2.4 mm | S5 | OK, internally consistent |
| 35 | 3D: 0.944 − 0.870 = 0.074; 0.892 − 0.870 = 0.022; 0.276 − 0.231 = 0.045 mm | Results D, Limitations | OK |
| 36 | Grey zone: 2 of 6 uniform bands = 33% of leaky clean models within 0.75–0.85 | S6 "33%" | OK |
| 37 | "About half" of throat flips beyond zone: 14/30 = 47% d, 21/36 = 58% l | S7 | OK |
| 38 | Abstract ranges: 32–33, 30–36, 6–10, 5–19 (B/C/D pooled), 19–20 / 5–8, 57–81, 4–18, 3–4, 2–7 | Table I, S3, S6, S8, S11 | OK |
| 39 | Conclusion "5–18%" (B per type: 9, 18, 5, 5) vs abstract "5–19%" (B–D pooled) | different bases | OK numerically; inconsistent basis (W7/W10) |
| 40 | Discussion "18–43% to 2–20% per error type" | Table I T1/T2 | OK |
| 41 | Exclusions: 23 + 41 = 64 D bound fits; 43 + 21 = 64; C bound 2 (half-voxel) + 8 (±10) matches n 193/299 and 187/299 | S2, S5, S7 | OK |
| 42 | 40% → 43% when 36 no-outflow breaks are scored as FFR 1: 41/96 | S2 | OK (implies 17 of 36 flip) |
| 43 | Cohort: 6 bands × 25 = 150; ≤ 2 per tree → ≥ 75 trees (108 reported) | Methods A | OK |
| 44 | Taper "of the order of" the floor: 13 (8.0–21.6), 14 (8.8–22.8) | Results A | Lower CI bound above 6.5%: wording overreach (W7) |
| 45 | T5 flips under tuning: 30 → 38 → 40% discrete | "left … unchanged" | Wording mismatch (W7) |

No hard numeric mismatch was found. The soft inconsistencies are wording and labelling problems: rows 39, 44 and 45, the Table S3 "All" label, the Table S3 footnote on Protocol D against the 297/298 passes, and "flip rates were unchanged" against "changed by at most five per cell".

## Rubric scores

| Code | Dimension | Score | Status | Justification |
|------|-----------|-------|--------|---------------|
| S1 | Novelty and contribution | 7 | pass | First decision-level ablation crossing topological and throat errors with fixed, re-derived and tuned boundary conditions, and quantifying calibration-not-validation concealment; clear digital-twin message. |
| S2 | Methodological rigour | 6 | warn | Sound design and paired statistics, but a sub-physiological primary demand, noise-free targets for error models, an unclustered CI and a one-case 3D check without T5. |
| S3 | Claims supported by evidence | 6 | warn | Discrete-bed concealment (19–20%) not replicated at ×2 demand; "against 3–4% for correct anatomy" is not like-for-like; "throat flips unchanged" and "of the order of the floor" understate. |
| S4 | Domain / physiological accuracy | 6 | warn | Bed laws and stenosis loss are standard, but demand is about ⅓–½ of physiological, the exponent and truncation differ between beds, the 30% DS loss switch is a discontinuity, steady flow is used, and RCA territory definitions are arbitrary. |
| S5 | Internal consistency | 9 | pass | 45 checks reproduced (Wilson intervals, exact McNemar, n sums, demand arithmetic); only labelling and wording inconsistencies remain. |
| S6 | Clarity, structure and readability | 7 | pass | Logical and well defined, but number-dense; the abstract carries about 15 ranges; Table I's n column does not apply to the passes-and-wrong column for T2. |
| S7 | Venue fit (JBHI) | 7 | pass | Digital-twin credibility and segmentation-to-decision informatics fit JBHI; the content leans toward computational biomechanics. |
| S8 | Reproducibility and transparency | 8 | pass | Public data, code, seed, tolerances and an exclusion table; needs an archived release, the 3D case files and the ROM node spacing. |

**Overall: 6.8 / 10. Recommendation: major revision** (borderline minor). The core finding on the throat error and topology under fixed boundary conditions is solid, and the numbers are internally consistent. The most quotable claim, that tuned models conceal topological errors at 19–20% in the discrete bed against 3–4% for correct anatomy, needs two things: re-analysis with noisy targets for the error models (W2), and a physiologically calibrated demand (W1). The 3D verification should also be extended to the throat error (W3).
