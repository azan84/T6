# Referee report — domain reviewer (coronary physiology / CT-FFR)

Manuscript: "Topological Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study" (IEEE JBHI)
Reviewer persona: clinical coronary physiologist / interventional cardiologist, CT-FFR research (3D CFD, side-branch flow, autoregulation, PET/CMR perfusion).
Material read: manuscript.txt, supplement.txt, page images ms-page-6/7 (Figs. 2–4). Literature claims below are from my own knowledge; where I am uncertain I say so.

## Summary

The authors insert idealized cosine stenoses (40–80% DS) into 150 host vessels from 108 ImageCAS-X coronary trees, stratified by baseline FFR across 0.65–0.95, and apply four segmentation errors one at a time: two topological (T1 deletion of the largest side branch distal to the lesion; T2 truncation of the host vessel 25 mm beyond the lesion) and two caliber errors scaled to inter-observer statistics (T3 lesion length +2.46 mm from HD95; T4 uniform radius x0.930 from DSC). FFR is recomputed with a steady reduced-order (Poiseuille + Young–Tsai expansion loss) network under four boundary-condition protocols: A fixed clean-model bed, B bed re-derived on the corrupted tree, C one global bed scaling fitted to clean "territory" flows, D one scaling per territory. Two microvascular bed structures (discrete outlets; leaky distributed outflow) are analyzed. The endpoints are classification flips at 0.80 and "passes-and-wrong" (territory perfusion residual <10% while |dFFR| > 0.05). The main findings: under fixed BCs topological errors flip 32–33% versus 6–10% for caliber errors; re-derivation and tuning reduce topological flips; after tuning, 19–20% (discrete) and 5–8% (leaky) of topological-error models pass the perfusion check while materially wrong, as do 4–18% of caliber-error (mostly taper) models, against 3–4% for correct anatomy with noisy targets. One 3D CFD case reproduces the direction of the side-branch effect and its removal by prescribed territory flows. Demand is replicated at 2x and 3x.

The question is clinically relevant and well posed: perfusion-informed personalization is now promoted as the route to coronary digital twins, and showing that agreement with a coarse perfusion target does not certify the pressure field is useful. The design is careful and transparent about its conditionality. My main concerns are physiological. The flow–stenosis regime looks unrealistically low-flow because of radius underestimation. The "perfusion territory" is defined more coarsely than any perfusion modality. The topological and caliber errors are compared at asymmetric magnitudes, and the caliber errors omit the clinically dominant throat (MLA) error. The headline discrete-bed tuning result loses significance at physiological demand. In my view these need major revision rather than rejection, because most can be addressed by reanalysis and reframing without new data.

## Strengths

1. Clear, clinically meaningful endpoint. Judging segmentation error by classification at 0.80, benchmarked against invasive test–retest variability and the 0.75–0.85 grey zone (Table S6), is much closer to how a cardiologist uses FFR than continuous sensitivity indices.
2. The fixed / re-derived / tuned comparison on the same corrupted anatomy is the right experiment. It reconciles Gamage et al. (side-branch effect under fixed resistance) and Gosling et al. (little effect after recalibration) convincingly (Sec. IV-B).
3. The direction of the side-branch effect is physiologically correct: losing distal run-off reduces trans-stenotic flow and raises FFR; restoring territory flow restores the gradient. The 3D case (Fig. 4e–f) illustrates this clearly.
4. The mechanism for tuned taper errors becoming "passes-and-wrong" (forcing clean flow through a narrowed lumen enlarges the pressure drop) is physically sound and clinically important: tuning can bias toward treatment as well as deferral.
5. Good analytic hygiene: paired McNemar with Holm, Wilson CIs, both bed structures with a claim only where both agree, a simulated physiological noise floor for correct anatomy, demand sensitivity (0.7/1.3x) and full re-selected replications (2x/3x), exclusions fully tabulated (Table S1), all solves converged.
6. Honest limitations: T1/T2 magnitudes declared as design choices, inter-observer DSC described as an upper bound on agreement, the stratified rates explicitly "not clinical prevalences".

## Weaknesses

### W1 (major) — Hyperemic flow regime and radius bias: the stenosis–flow pairing is physiologically atypical
Anchor: "the cohort's median demand was 2.28 mL/s (137 mL/min) per tree"; "The meshed lumen was wider than the radius used by the reduced-order model (median difference 0.14 mm ...), and on the reduced-order radius the baseline was 0.761"; 3D case "a 20 mm lesion of 80% DS in the proximal LAD" with FFR 0.870.
- The radius is the distance from the centerline point to the nearest background voxel. This underestimates the lumen radius by roughly half a voxel, which the 3D comparison confirms (0.14 mm). Demand scales with r_in^3 and Poiseuille resistance with r^-4, so the model runs at about one-third to half of physiological left-tree hyperemic flow (a whole left tree at 137 mL/min is below the authors' own cited LAD-only thermodilution values of 228–293 mL/min) while overestimating viscous resistance.
- Consequence: to land near 0.80, the stratified selection must choose severe lesions. An 80% DS (96% area stenosis), 20 mm proximal-LAD lesion with FFR 0.87 is clinically atypical; such lesions are almost always well below 0.80 at true hyperemia. By my rough calculation with the stated loss coefficients and the 0.276 mm throat, FFR 0.87 implies a trans-stenotic flow of the order of tens of mL/min. Please check this. At low flow the pressure loss is dominated by the linear viscous term, whereas at clinical hyperemic flow the quadratic expansion term matters. dFFR/dQ, the quantity through which T1/T2 act, therefore differs between regimes.
- The 3x replication, the most physiological demand, could not be run for the discrete bed, "mostly because the healthy-equivalent network lost more than 10% of the aortic pressure". This is itself a sign that the segmented radii are too narrow for physiological flow.
Fix: (a) state explicitly that k is set low to offset narrow segmented radii, and report the trans-lesional flow (mL/min) and the DS distribution per baseline-FFR band against clinical DS–FFR data; (b) report the fraction of the lesion dP from viscous vs expansion terms; (c) correct the radius bias (e.g., add half a voxel, or use the area-equivalent radius of the meshed surface as in the 3D counterpart) and repeat the primary analysis, or make the 2x–3x analyses co-primary; (d) consider mass-based total flow (Q ∝ myocardial mass^0.75, as in clinical CT-FFR) as a further sensitivity.

### W2 (major) — "Perfusion territory" is not defined the way perfusion is measured or used for tuning in practice
Anchor: "A perfusion territory is the subtree below each child of the first bifurcation of the clean tree."
- In the left tree this gives essentially LAD vs LCx (± ramus). In the right tree the first child is typically the conus or an RV/SA-nodal branch, which explains why C and D were "undefined for most right coronary instances". PET/CMR/CT-perfusion-informed models assign myocardium (17-segment or voxel/Voronoi maps from the epicardial tree) to individual vessels, including diagonals and obtuse marginals. Flow targets are MBF (mL/min/g) x territory mass.
- A missed diagonal is invisible at LAD-subtree resolution but would usually register at segment resolution. The central claim ("A perfusion match after tuning does not show that the computed value is correct") is therefore partly an artifact of a check coarser than practice. It also makes Protocol D's flexibility (the "most flexible tuning") much lower than real per-segment tuning.
- Also, a "perfusion check" with an RMS-residual pass threshold is the authors' construct and not an established acceptance criterion in CT-FFR or digital-twin workflows. It should be presented as such.
Fix: repeat C/D and the passes-and-wrong analysis with territories at the level of second-generation branches (or a vessel-to-myocardium Voronoi assignment) to mimic segment-level perfusion. Report how passes-and-wrong scales with territory granularity, and state in the abstract that the check operates at main-branch territory level. Cite perfusion-coupled coronary models (e.g., Papamanolis et al., Ann Biomed Eng 2021; Montino Pelagi et al., Biomech Model Mechanobiol 2024; in addition to Menon et al. [8]).

### W3 (major) — Asymmetric error magnitudes make the topological-vs-caliber ranking overreach, and the dominant clinical caliber error (MLA) is not tested
Anchor (Abstract/Conclusion): "branching (topological) errors changed the decision in 32–33% of models, against 6–10% for vessel-size (caliber) errors of inter-observer magnitude"; "missed branches and vessel breaks changed the decision three to six times as often as caliber errors"; Discussion: "the decision risk of segmentation lay mainly in the branching structure of the lumen".
- T1 deletes the *largest* distal side branch (often a major diagonal/OM) and T2 removes all run-off 25 mm beyond the lesion. These are severe, near worst-case events and are not calibrated to how often or how large they are in practice. The caliber errors are calibrated to average whole-tree inter-observer agreement on largely healthy vessels.
- In clinical CT-FFR the caliber error that drives misclassification is at the throat (calcium blooming, motion, partial volume at the MLA), not a uniform 7% taper. The authors' own 3D case shows this: a 0.14 mm radius-definition difference (throat 0.276 vs 0.231 mm) shifted baseline FFR by 0.11 (0.870 vs 0.761). That is larger than any segmentation error in the study and on its own crosses 0.80. Refs [10]–[12] address MLA uncertainty, but the design does not.
Fix: add a throat-localized caliber error (e.g., MLA radius ±10–20%, or ±1 voxel) and a smaller-branch T1 variant (e.g., smallest, or median-sized, distal side branch), or graded T1/T2 severities. Otherwise, restate the ranking in abstract and conclusion as conditional on "deletion of the largest distal side branch versus uniform caliber errors of inter-observer magnitude", and drop "the decision risk of segmentation lay mainly in the branching structure".

### W4 (major) — The discrete-bed tuning result, which carries the headline, does not reach significance at physiological demand; the abstract says only that "directions held"
Anchor: Abstract "tuned models still passed ... 19–20% (discrete bed)"; "The directions held at doubled and, in the leaky bed, tripled demand"; Sec. III-E "at twice the demand the excess over re-derived boundary conditions was significant in three of four caliber comparisons and in no topological one".
- The topological passes-and-wrong excess over Protocol B is significant only in the discrete bed at the low primary demand. It is non-significant in the leaky bed at all demands and in the discrete bed at 2x. Table S4 also shows the leaky value falling to 3% at 0.7x, at the floor.
Fix: say in the abstract and conclusion that the topological excess over re-derivation was significant only in the discrete bed at the primary demand. Give the 2x discrete-bed numbers with their p-values next to the primary ones, and make the caliber (taper) result, which is more robust across demand, at least as prominent.

### W5 (major) — 3D "removal" is computed against a different baseline from the clean reference
Anchor: "With the clean territory flows prescribed at the outlets (the limit of Protocol D), the same error changed FFR by −0.0007 (0.892 in both geometries)"; clean baseline with fixed resistances 0.870; Abstract: "it reduced a shift of 0.074 to −0.0007".
- Prescribing territory flows split "by bed weight" does not reproduce the clean outlet distribution (baseline 0.892 vs 0.870). Against the clean reference that defines dFFR everywhere else in the paper, the tuned missed-branch model is +0.022, not −0.0007. The 3D case therefore does not show exact removal. It shows that the error vanishes relative to a prescribed-flow baseline, which itself differs from the clean model by 0.022. Fig. 4 caption ("a shift that would move a decision near 0.80") also overstates: 0.870 to 0.944 does not cross 0.80.
Fix: report both differences (vs. the prescribed-flow baseline and vs. the clean fixed-resistance reference), explain why the within-territory split changes the baseline, and correct the abstract and Fig. 4 caption. Alternatively, prescribe the clean model's per-outlet flows in the baseline geometry.

### W6 (minor) — "Flip" equated with a change in treatment; clinical decision framing
Anchor: "A flip is a change of classification at 0.80 between the two, that is, a change in the indicated treatment."
CT-FFR is used mainly as a gatekeeper to invasive angiography. Values in 0.75–0.80 (and lesion-specific dFFR, distance from the lesion, symptoms) usually lead to invasive confirmation, not directly to PCI. Fix: say "change in classification (and hence potentially in referral/treatment)"; make beyond-grey-zone flips (Table S6) a co-primary decision metric in the main text, since these are the clinically consequential ones. It is good that the measurement point is 20 mm distal, which matches current CT-FFR reading recommendations; say so and cite a reading-practice reference.

### W7 (minor) — Noise-floor comparator
Anchor: "the repeat is normal about the clean value ... with the published standard deviation of the test–retest difference, 0.018 [31]."
Invasive test–retest variability (I believe Johnson et al. report a test–retest SD near this value, but please check against the paper) is the floor for the invasive reference. For a computed FFR, the more relevant comparator is the inter-analyst/inter-scan reproducibility of CT-FFR itself (e.g., Gaur et al., Eur Heart J 2014, FFRCT reproducibility), which is larger than invasive repeatability. Fix: add CT-FFR reproducibility as a second comparator, or at least discuss it. Also note that 1.96 x within-subject CV is a single-measurement bound, whereas the residual is an RMS over 2–3 territories against model targets. The "stricter than measurement repeatability" wording should state that it applies to the RMS form.

### W8 (minor) — Physiological scope statements
Anchor: "The model is steady and represents maximal hyperemia (maximal flow) without autoregulation."
This is fine for FFR. But the Discussion should acknowledge that (i) diseased territories often do not reach full microvascular vasodilation (microvascular dysfunction lowers flow and raises FFR), (ii) collaterals are absent, and (iii) a missed side branch in vivo coexists with that branch's own perfusion, which a PET territory map would show. Item (iii) links back to W2. Brief text is sufficient.

### W9 (minor) — Missing or misplaced key references
- Vardhan M, et al. (Randles group), "The importance of side branches in modeling 3D hemodynamics from angiograms for patients with coronary artery disease", Sci Rep 2019. This is directly on the side-branch question and should be in the Introduction alongside [20], [21].
- Gaur S, et al., FFRCT reproducibility, Eur Heart J 2014 (see W7).
- Perfusion-coupled coronary modeling (see W2): Papamanolis et al. 2021; Montino Pelagi et al. 2024 (please verify the details).
- Fractal/Murray-law flow allocation in angiography-derived FFR (e.g., the QFR/Murray-fractal literature) and morphometric scaling exponents for human coronaries (Huo & Kassab; van der Giessen et al. 2011 on diameter–flow exponents of about 2.3–2.7). The leaky bed uses exponent 3 and the discrete bed 2.66; the choice of different exponents needs this context.
- Mass-based total flow in clinical CT-FFR (Taylor et al. [3] is cited, but the text should state that clinical pipelines set total flow from myocardial mass, not inlet radius).
- Ref [9] (pulmonary valve FSI) is an odd support for "measured flow splits" in coronary tuning. Replace it with a coronary example.
- I could not verify [5] (Fossan 2026, "58.1% to 68.6% sensitivity") or [18]/[23] (ImageCAS-X 2026) from memory. Please make sure they are exactly as published.

### W10 (minor) — Lesion-length error proxy
Anchor: "HD95 (2.46 mm), which bounds the disagreement in lesion extent, sets T3."
HD95 is a whole-surface boundary distance, dominated by distal tips and branch ends, and does not bound disagreement in lesion extent. Fix: call it a proxy, or derive lesion-extent disagreement from annotator masks around narrowings.

### W11 (minor) — Denominator conventions differ between tables
Table I/S3 exclude models without a defined residual, whereas Table S5 includes them as non-passing ("denominators include models without a defined residual, which do not pass"). So the same quantity differs (e.g., discrete topological B: 1 (0–5) in S3 vs 1 (0–4) in S5; leaky topological B: 5 (3–8) vs 4 (2–7)). Fix: use one convention throughout or flag the difference in each caption.

### W12 (minor) — Code availability
"The code is available from the corresponding author upon reasonable request." For a fully automated in silico pipeline on public data, JBHI readers would expect a public repository, i.e., the cohort list, seed, solver and protocol fits. This would greatly increase reuse of the proposed test.

## Rubric scores

| Code | Dimension | Score | Status | Justification |
|------|-----------|-------|--------|---------------|
| S1 | Novelty and contribution | 7 | pass | Fixed/re-derived/tuned BCs on identical corrupted anatomy at the 0.80 decision is new and useful; side-branch prior work (Vardhan 2019) under-cited. |
| S2 | Methodological rigour | 6 | warn | Strong paired statistics and replications, but low-flow/narrow-radius regime, coarse territories and a single 3D case limit inference. |
| S3 | Claims supported by evidence | 5 | warn | Topological-vs-caliber ranking rests on asymmetric magnitudes; discrete-bed tuning excess not significant at 2x demand; 3D "removal" relative to a shifted baseline. |
| S4 | Domain / physiological accuracy | 5 | warn | Physiology direction correct, but 80% DS at FFR 0.87, demand of about one-third physiological, first-bifurcation "territories" and no MLA error are not representative of clinical CT-FFR. |
| S5 | Internal consistency | 7 | pass | Abstract/text/table numbers cross-check well; 3D baseline (0.870 vs 0.892) and S3/S5 denominator conventions need reconciling. |
| S6 | Clarity, structure, readability | 7 | pass | Dense but precise; protocol definitions clear; some key qualifiers belong in the abstract. |
| S7 | Venue fit (JBHI) | 7 | pass | Segmentation QC and digital-twin calibration are relevant to health informatics; the decision-level framing suits JBHI. |
| S8 | Reproducibility and transparency | 6 | warn | Seed, exclusions, solver settings and pipeline well documented; code only on request. |

**Overall: 6.0 / 10**

**Recommendation: major revision.** The study is worthwhile and carefully executed. Before acceptance: the flow regime and radius bias must be addressed or made co-primary at physiological demand (W1); the perfusion check must be tested at clinically realistic territory granularity (W2); the error-type ranking must be qualified or made symmetric, including a throat-level caliber error (W3); and the abstract must state where the tuning result loses significance and report the 3D comparison against the true clean reference (W4, W5).
