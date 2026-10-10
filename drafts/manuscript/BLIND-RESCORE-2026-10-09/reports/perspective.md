# Referee report: "Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study" (IEEE JBHI)

Reviewer perspective: medical image segmentation and imaging informatics (topology-aware learning, clDice, coronary centerline benchmarks, model credibility under ASME V&V40 and FDA in silico evidence).

## Summary

The authors insert idealized cosine stenoses (150 instances, 108 trees, 93 patients, ImageCAS-X test split) and apply five synthetic segmentation errors one at a time: a missed side branch (T1), a vessel break (T2), a longer lesion (T3, +HD95), a uniform distal taper (T4, ×0.930 derived from inter-observer DSC) and a half-voxel throat error (T5). FFR is recomputed with a reduced-order network model in two microvascular-bed structures (discrete and leaky) under four boundary-condition protocols: fixed (A), re-derived (B), globally tuned to clean territory flows (C) and per-territory tuned (D). The main outcomes are decision flips at 0.80 and "passes-and-wrong", where a model passes a 10% territory-perfusion check while |ΔFFR| > 0.05. Under fixed boundary conditions, topological and throat errors flip about a third of the decisions in this threshold-stratified cohort, and caliber errors away from the throat flip 6–10%. Tuning hides a material error in 19–20% (discrete) and 5–8% (leaky) of topological-error models and in 57–81% of throat-error models. The tube-model DSC is about 0.97 for a missed branch. One 3D CFD case agrees in direction with the reduced-order model. The stated message is that neither overlap nor a perfusion match certifies the segmented lumen, and that agreement after tuning is calibration evidence, not validation evidence.

The design is careful and controlled, and the statistics are honest: paired tests, both beds, noise floors and a stated conditionality on the stratified cohort. The calibration-versus-validation point matters for digital-twin credibility. My concerns are mostly from the segmentation side. The error models are synthetic and in part circularly calibrated against overlap metrics. The overlap analysis uses a tube model rather than the voxel masks that segmentation work is scored on. The detector AUCs compare positives and negatives under unequal noise. The informatics take-home does not yet become a QC tool that has been tested. Several per-type summary statements overstate the table.

## Strengths

1. **Decision-level endpoint.** The study judges segmentation error by the classification at 0.80 against a repeat-FFR noise floor (SD 0.018), not by a continuous pressure change. Clinically and for regulators, this is the right framing, and it is rarely done in the segmentation-uncertainty literature.
2. **Protocol ablation on identical corrupted anatomy.** Fixed, re-derived, global-tuned and per-territory-tuned boundary conditions are compared on the same trees. This shows directly that an error's effect depends on the BC pipeline, which is the paper's central and novel contribution.
3. **The passes-and-wrong construct.** It gives a concrete, quantitative form to the non-identifiability of flow-only calibration. It also answers a credibility question that digital-twin developers face (Discussion IV-C: "agreement with perfusion after tuning is calibration evidence rather than validation evidence").
4. **Robustness work.** Two bed structures, with a claim made only where both agree. Demand sensitivity at ×0.7/×1.3 and replication with re-selected cohorts at ×2/×3. Threshold sensitivity at 13%/16%. Finer territory resolution. A simulated physiological noise floor (Table S11). A Bayesian mixed model for clustering.
5. **Transparent exclusions and denominators.** Table S1 and the Table I footnote account for every excluded model, and the authors show the effect of scoring the "no outflow" vessel breaks as flips (40% to 43%).
6. **Reproducibility.** Public data (ImageCAS/ImageCAS-X, CC BY 4.0), a fixed seed, one automated run producing all reduced-order outputs (Fig. S1), and public code.
7. **Honest limitations.** The section states that T1/T2 magnitudes are design choices, that the prevalence of errors was not measured, that the 3D validation is a single case, and that the inter-observer DSC is an upper bound.

## Weaknesses

### W1 (major): The error models are synthetic and not tied to the failures that segmentation networks actually produce
Anchor: Limitations, "The rates are conditional on an error being present; how often current segmentation methods produce each error at a lesion was not measured." Also: "T1 and T2 have no measured magnitude and are design choices."

- T1 always removes the largest side branch beyond the lesion (median 27% of discrete-bed flow lost, Table S9). This is a worst-case choice. Networks more often drop small distal or ostial branches.
- T2 ends the host vessel at a fixed 25 mm beyond the lesion.
- T4 applies a uniform, systematic 7% radius shrinkage to the whole distal tree. Inter-observer disagreement (the source of its magnitude) is mostly local, random-signed boundary disagreement concentrated in small vessels and at calcified segments. It is not a coherent bias.
- Error types that are common at lesions are not modeled: calcium blooming (systematic throat over- or under-estimation that correlates with plaque), partial-volume throat collapse, and false merges or kissing vessels.

Because ImageCAS-X is a segmentation benchmark with published method outputs, the most obvious informatics experiment is missing: run the same pipeline on real network predictions, or on error fields sampled from them.

**Fix:** (a) Add a "realistic error" arm. Take predictions from at least one or two public ImageCAS/ImageCAS-X baselines (or train a standard nnU-Net). Map their errors at the inserted-lesion locations (branch detection, break positions, local radius bias) and report how often T1/T2/T5-like errors occur within the region that matters (from the lesion to the measurement point plus run-off). At minimum, report an empirical distribution of these errors and re-weight the flip rates. (b) Add a dose-response for T1: ΔFFR and flip probability against the deleted branch's flow share or radius (data already in Table S9). This turns the design choice into a usable QC threshold ("branches above X mm beyond a lesion must be present"). (c) For T4, add a random-signed, spatially correlated radius perturbation with the same DSC, so that systematic bias and noise can be separated.

### W2 (major): The overlap-metric analysis uses a tube model, part of the comparison is circular, and the clDice conclusion is overstated
Anchors: "In a tube model of each tree, the missed branch and the taper had the same median DSC (0.97)". "Overlap scores, including the topology-aware clDice [31], therefore did not rank these errors by decision risk." Abstract: "A missed branch kept a near-perfect Dice score (0.97, as high as a taper)".

- The T4 magnitude was defined so that two coaxial cylinders have DSC = 0.928. Its tree-level DSC (0.97) is then fixed by the share of volume it covers (S7: "about 40% of its volume"). The headline "as high as a taper" is therefore a property of the chosen magnitudes, not an empirical finding about Dice.
- The DSC is computed on cylinders of node radius, not on voxelized masks, and segmentation papers report Dice on voxels. Junction and overlap handling differs, and the "whole-scan" denominator dilutes local errors.
- clDice gives 1.000 for every caliber error and drops for every topological error (Table S9: 0.93–0.94 for T1, 0.85 for T2). clDice does separate the error classes. It is just insensitive to throat errors, which it was never designed to detect. The sentence quoted above collapses DSC and clDice into one claim, and no clDice AUC is reported.
- Lesion-local and topology metrics that a segmentation QC pipeline would actually use (local DSC or HD within a lesion-centred ROI, branch-detection recall, Betti-number error, centerline overlap/OV from the CAT08-style evaluation) are absent.

**Fix:** Recompute DSC, clDice and HD95 on voxelized corrupted masks using the ImageCAS-X evaluation code. Report an AUC for a decision change for each metric (DSC, clDice, HD95, Betti-0/1 error, branch recall, lesion-ROI DSC). Rephrase the claim as: clDice flags topological errors but neither metric ranks within-class decision risk or detects throat error. State explicitly that the T1-vs-T4 DSC equality follows from the chosen T4 magnitude.

### W3 (major): The detector AUCs compare positives and negatives under unequal noise
Anchor: "The perfusion residual before tuning separated topological errors from correct anatomy with noisy targets in the discrete bed only (AUC 0.77 against 0.22)". Supplement S8: "With the error models' targets carrying the same noise, the AUC for topological errors was 0.82 (discrete) and 0.56 (leaky)."

- The main-text AUC uses noise-free error models as positives against noisy correct-anatomy negatives. A leaky-bed AUC of 0.22 (well below 0.5) is largely an artefact of that asymmetry: the negatives carry noise that the positives do not.
- The noise-matched comparison (0.82/0.56) is the fair one and gives a different conclusion for the leaky bed (weak, not inverted).
- The same asymmetry affects passes-and-wrong. Error models are tuned to error-free targets ("Tuning targets were error-free clean-model flows"), whereas the correct-anatomy floor (3–4%) is tuned to noisy ones. The "against 3–4% for correct anatomy" comparison in the abstract and conclusion is therefore not like for like.

**Fix:** Make the noise-matched AUCs primary in the main text and Discussion item "Third". Repeat passes-and-wrong for error models with the same simulated target noise as the floor, and report both. Do not present an AUC below 0.5 as "separation".

### W4 (major): Per-type summary statements overstate Table I
Anchors: Discussion IV-A, "A missed branch, a vessel break or a half-voxel error in throat diameter each changed about a third of decisions". Conclusion: "a missed branch, a vessel break or a half-voxel throat error each changed about a third of decisions".

Table I (Protocol A) gives T1 at 27% (discrete) and 18% (leaky), and T2 at 40% and 43%. Only the pooled topological rate (32–33%) is about a third. Similarly, "Caliber errors of inter-observer size away from the throat flipped decisions at rates near repeat invasive measurement (the taper up to 14%)" sets a 13–14% rate (95% CI 8–22%) beside a 5.0–6.5% floor. That is about double the floor, not near it.

**Fix:** State per-type ranges (T1 18–27%, T2 40–43%, T5 30–36%) or say "topological errors, pooled". Describe the taper as "about twice the repeat-measurement floor in the discrete bed".

### W5 (major): The informatics implications are not yet actionable, and no QC check has been tested
Anchor: Discussion IV-C, "the results suggest four considerations … These considerations are not validated decision rules."

For a JBHI audience, the deliverable should be something a segmentation pipeline can run. The four considerations ("check that the side branches … are present", "check the lumen caliber, above all the throat diameter", "take most care near 0.80") are generic. The paper has the data to test simple automated checks but does not:
- branch completeness beyond the lesion against an atlas or the contralateral tree;
- a lesion-ROI uncertainty metric (e.g., ensemble or test-time augmentation variance at the throat);
- the |ln C| tuning-scale flag (S8 AUC 0.47/0.12, which is negative and worth reporting in the main text);
- a "distance of baseline FFR to 0.80" flag combined with a throat-error sensitivity (∂FFR/∂r at the throat, which the reduced-order model can give cheaply).

Mapping to V&V40 is mentioned only in one sentence via [33].

**Fix:** Add a short subsection that evaluates two or three concrete, automatable QC rules on the existing models (sensitivity/specificity for flips). For example, flag if ∂FFR/∂r_throat × half-voxel > |FFR − 0.80|, and flag if any branch above radius X beyond the lesion is missing. Add a short table that maps findings to V&V40 credibility factors (input sensitivity of geometry, calibration vs validation, applicability) so that the regulatory implication is concrete.

### W6 (minor): Accessibility for non-CFD readers
Anchors: Abstract (about 250 words, more than 15 numeric ranges, two beds × four protocols). Sections II-B/II-D (Murray exponents, the 2.66 exponent, ±1.5 decades of C_b).

Readers from imaging informatics will struggle to keep track of "leaky vs discrete bed" and the four protocol letters.

**Fix:** Add a schematic figure (or a panel in Fig. 1) that shows the two bed structures and Protocols A–D: what is held fixed, what is refitted and which targets are used. Use descriptive labels in figures and tables instead of letters only ("A fixed", already used in legends, should also be used in Table I). Reduce the abstract to the pooled numbers in one bed and move the bed-specific ranges to Results.

### W7 (minor): Figure clarity
- **Fig. 2:** The band-level flip rates come from about 15–25 models per band and have no uncertainty shown. Protocol D, the most flexible tuning, is omitted. Add Wilson bands or error bars, include D (or a fourth line style), and give the n per band.
- **Fig. 3:** The hybrid linear/log x-axis ("linear below 0.01 and logarithmic above") is hard to read, and protocols overplot. Use a symlog axis with a visible break marker, or facet by protocol.
- **Fig. 4:** The points for four error types are heavily overplotted, and the marker shapes are hard to tell apart at print size. The x-axis is the tube-model "whole scan" DSC (see W2). Consider small multiples by error type, or a lesion-ROI DSC axis.
- **Fig. 5:** The rainbow (jet-like) colormap for wall pressure is not perceptually uniform and is not colour-blind safe. Use a sequential map (e.g., viridis/cividis). Panel (e) legend: "Lesion" markers vs lines is ambiguous. Label 3D markers and reduced-order lines explicitly in the legend.
- **Supplementary Fig. S1 caption:** "ran on the CFD machine" is informal. Name the software and hardware, or delete the phrase.

### W8 (minor): The T3 and T5 magnitude definitions are loose proxies
Anchors: "HD95 (2.46 mm), used as a proxy for the disagreement in lesion extent, sets T3". "The half-voxel throat error … changed the throat radius by a median of 0.088 mm and DS by 7.3 points".

HD95 is a whole-surface statistic dominated by distal and branch-end disagreement. It is not a lesion-length error. For T5, a half-voxel error is small relative to published CT-vs-QCA throat disagreement (SD about 12 DS points, as the supplement notes), so T5 is if anything conservative. This should be said in the main text, because it strengthens the throat finding. **Fix:** Justify T3 with a lesion-length agreement statistic from the CT literature, or label it explicitly as a sensitivity magnitude. State in the Results that the ±10-point T5 variant (S5) gives larger effects (flips 40–44%).

### W9 (minor): The single 3D case does not validate the reduced-order model
Anchor: "The 3D analysis covers one instance, whose meshed lumen was wider than the reduced-order radius … moved the baseline across 0.80 (0.761 against 0.870)".

That a 0.045 mm radius-definition offset moves the baseline FFR by 0.11 and across the threshold is itself a striking segmentation-sensitivity finding. It also shows that the reduced-order radius definition (distance map to the nearest background voxel, biased inward by about 0.14 mm) is a systematic segmentation-derived error that the cohort carries. **Fix:** Discuss the distance-map radius bias as a sixth, systematic caliber error, and quantify it on the cohort (e.g., recompute baseline with a +0.5-voxel radius offset). Add at least a T5 case to the 3D check, since the throat error is the paper's most robust finding.

### W10 (minor): Several near-duplicate ranges for the same contrast
The abstract says "reduced topological flips to 5–19%". Discussion IV-A says "from 18–43% to 2–20% per error type". The Conclusion says "Re-derived boundary conditions reduced topological decision changes to 5–18%". Each is defensible (pooled vs per-type, B only vs B–D), but readers will see three numbers for one claim. **Fix:** Use one definition, pooled or per-type, and state which protocols it covers each time.

## Rubric scores

| Code | Dimension | Score | Status | Justification |
|------|-----------|-------|--------|---------------|
| S1 | Novelty and contribution | 7 | pass | First decision-level ablation of topological, caliber and throat errors across fixed, re-derived and tuned BCs. The passes-and-wrong construct is new and useful. |
| S2 | Methodological rigour | 6 | warn | Paired design, two beds and noise floors are strong. However, the errors are synthetic and partly worst-case (W1), DSC is from a tube model (W2), and noise is applied asymmetrically to positives and negatives (W3). |
| S3 | Claims supported by evidence | 6 | warn | "Each changed about a third" overstates T1 (18–27%). The clDice conclusion is too broad. "As high as a taper" is partly a consequence of the chosen magnitudes. |
| S4 | Domain / physiological accuracy | 7 | pass | The physiology is reasonable and the limitations are acknowledged (low demand, idealized lesions, steady flow). The throat magnitude is conservative relative to the CT-vs-QCA spread. |
| S5 | Internal consistency | 7 | warn | Table I, the text and the supplement agree on the numbers I checked. There are two AUC versions (0.77/0.22 vs 0.82/0.56) and three ranges for the same topological-flip contrast. |
| S6 | Clarity, structure, readability | 6 | warn | Dense, with many numbers. No schematic of beds and protocols. Figs. 2–5 have overplotting, no uncertainty, a hybrid axis and a rainbow colormap. |
| S7 | Venue fit (JBHI) and informatics relevance | 6 | warn | The topic fits digital twins and segmentation QC. However, no automated QC rule or real-network error analysis is tested, and V&V40 mapping is minimal. |
| S8 | Reproducibility and transparency | 8 | pass | Public data, fixed seed, one automated run, open code, full exclusion accounting. 3D mesh and solver details are given. |

**Overall: 6.4 / 10. Recommendation: major revision.**

The core experiment is sound and publishable in JBHI. The revision needs to (i) connect the error models to failures that real networks produce, or at least to an empirical error distribution and a dose-response; (ii) redo the overlap analysis on voxel masks with lesion-local and topology metrics and correct the clDice claim; (iii) make the noise-matched detector and passes-and-wrong comparisons primary; and (iv) turn the four considerations into one or two QC rules that are tested. None of this needs new CFD. Most of it uses data the authors already have.
