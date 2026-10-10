# Referee report: domain reviewer (clinical coronary physiology / CT-FFR)

Manuscript: "Segmentation Error and Boundary-Condition Tuning in Computed Coronary FFR: A Controlled In Silico Study" (IEEE JBHI)

Reviewer persona: interventional cardiologist and coronary physiologist working on 3D CFD CT-FFR, side-branch flow, autoregulation and PET/CMR myocardial perfusion.

Material read: manuscript.txt, supplement.txt and the page images (Figs. 1-5, Tables S1-S12). I did not consult external sources. Where a literature statement below comes from memory, I flag it as uncertain.

---

## Summary

The authors insert one idealized cosine stenosis per vessel into 108 coronary trees from the ImageCAS-X test split. The 150 instances are stratified in six 0.05-wide bands of baseline FFR between 0.65 and 0.95. Five segmentation errors are then applied one at a time: a missed largest side branch beyond the lesion (T1), a vessel break 25 mm beyond the lesion (T2), a lesion 2.46 mm longer (T3), a 7% taper (T4) and a half-voxel throat-diameter error (T5). FFR is recomputed with a steady Poiseuille-plus-expansion-loss reduced-order network under four outlet protocols: fixed (A), re-derived from the corrupted tree (B), one global bed scaling tuned to clean territory flows (C), and per-territory tuning (D). Two microvascular bed structures are used: a "leaky" bed with distributed wall outflow and a "discrete" bed with outlets only. The endpoints are flips at FFR 0.80 and "passes-and-wrong", defined as a territory-flow residual below 10% with |dFFR| > 0.05. These are compared against a repeat-invasive-FFR floor (SD 0.018) and a simulated perfusion-noise floor. A single 3D OpenFOAM case checks the direction of the effect.

Main claims:
- With fixed BCs, topological errors and the half-voxel throat error flip about a third of decisions, against 6-10% for other caliber errors.
- Re-derived or tuned BCs reduce topological flips but not throat flips.
- After tuning, a perfusion check passes materially wrong models in 19-20% (discrete) and 5-8% (leaky) of topological-error cases and in 57-81% of throat-error cases. This falls to 2-7% for topological errors with finer territories.
- Dice does not rank errors by decision risk.

The study is careful, well controlled and unusually candid about its exclusions and replications. Its central conceptual message is sound: matching flow alone cannot identify a geometric error, and a tuned perfusion match is calibration evidence rather than validation evidence. My main concerns are physiological, not computational:
- **Flow regime.** The primary analysis runs at a flow regime well below hyperemia. This pushes the cohort towards near-occlusive throats and probably inflates the throat-error result.
- **Reference model.** The clean reference is generated with the same scaling-law bed that Protocol B re-applies, which gives re-derivation an oracle advantage over perfusion tuning.
- **Tuning practice.** Perfusion tuning is represented with territory definitions and parameter ranges that differ from how perfusion data are used in practice.
- **Clinical framing.** The 0.80 flips need clinical framing against CT-FFR's own error and the continuous FFR-outcome relationship.

---

## Strengths

1. **The design is a clean, paired ablation.** Each error is applied alone to an otherwise correct model, and all four BC protocols are solved on the same corrupted anatomy. This isolates the error-by-protocol interaction that earlier work could not separate (Table I, Sections II-C and II-D).
2. **The endpoint is clinically anchored.** The authors use the decision at 0.80, report "beyond the grey zone" flips (Table S6) and use a materiality threshold of |dFFR| > 0.05. This is more useful to clinicians than the continuous sensitivity indices that dominate the literature.
3. **The hyperemic physiology is directionally correct.** Microvascular conductances are computed on the healthy-equivalent tree and held fixed when the lesion is inserted ("an inserted lesion changes only the epicardial radius"). This is the right representation of maximal vasodilation without autoregulation. The missed branch under fixed resistance raises FFR, as it should, and the 3D case confirms this (+0.074).
4. **Measurement noise is benchmarked twice.** One floor uses published test-retest invasive FFR. The other is a simulated physiological floor on correct anatomy tuned to noisy perfusion (Table S11). Having both is good practice and gives the passes-and-wrong figures a meaningful reference (3-4%).
5. **The two bed structures bracket how unresolved side branches are handled.** A finding is claimed only where both beds agree in direction, which is an appropriately conservative rule.
6. **Weaknesses are reported transparently.** Every exclusion is tabulated (Table S1). Protocol D fits at the bound are disclosed together with their effect. The demand replication is reported honestly, including that the tuned-over-re-derived excess for topological errors did not replicate at twice the demand. The 3D radius offset that moved the baseline across 0.80 is disclosed.
7. **Fidelity is separated from geometry.** The 3D check uses a reduced-order counterpart rebuilt on the meshed radius, so model fidelity and radius definition can be told apart. The mesh-sensitivity reporting is adequate for a single case.
8. **The overlap-score result is useful for the segmentation community.** A missed branch keeps a DSC of 0.97 while flipping twice as often as a taper (Fig. 4, Table S9).
9. **Open public data and code are provided, with a fixed seed and full pipeline (Fig. S1).**

---

## Weaknesses

### W1 (major): The primary flow regime is far below hyperemia. This inflates required lesion severity and probably the throat-error result.

**Anchors:**
- "Because the segmented arteries were narrower (median inlet radius 1.60 mm), the cohort's median demand was 137 mL/min per tree."
- 3D case: "a 20 mm lesion of 80% DS in the proximal LAD", with FFR 0.870 (3D) and 0.761 (reduced order), and throat radius "0.276 against 0.231 mm".

**Total flow.** A whole left coronary tree at adenosine hyperemia carries roughly 300-450 mL/min in a normal adult. That is about 2.5-4 mL/min/g over 100-150 g of myocardium. A per-tree median of 137 mL/min is close to resting total coronary flow. The justification that a 3.7 mm LAD would carry 214 mL/min applies to a vessel size the cohort does not have. The cohort is evaluated at its own segmented radius, which the authors acknowledge is biased low by about 0.14 mm (distance-map radius).

**Flow through the 3D-case lesion.** A back-of-envelope check with the authors' own expansion-loss term puts the flow through this lesion at only about 20-30 mL/min:
- Assumptions: Kt = 1.52, r_fit ≈ 1.15 mm, throat radius 0.23-0.28 mm (MLA ≈ 0.17-0.24 mm²), pressure drop 12-22 mmHg.
- An 80% DS proximal LAD lesion with an MLA well under 0.3 mm² would, at true hyperemic flow, give an FFR far below 0.6. IVUS-derived LAD MLA cut-offs for FFR ≤ 0.80 are of the order of 2-3 mm².
- An FFR of 0.76-0.87 at this geometry is only possible at near-resting flow.
- I may be off by a factor that depends on details not given, so I ask the authors to report the actual numbers (see fix).

**Consequence for the throat result.** In a stratified-by-FFR design, low demand means the lesions that populate the 0.75-0.85 bands are the near-occlusive ones. A half-voxel throat change of 0.088 mm in radius has a very different relative size at different throats:
- about 35-40% of a 0.23 mm throat;
- about 15% of a 0.6 mm throat.

Because the pressure drop scales roughly with r^-4, the 30-36% throat flip rate and the 57-81% throat passes-and-wrong are probably inflated by the flow regime. The demand replication (Table S5) does not report T5 at all. At twice the demand, the tuned-over-re-derived topological excess was "not significant in any topological comparison". At three times the demand, only 17 instances survived the discrete-bed criterion that the healthy-equivalent network have FFR ≥ 0.90. That itself indicates that the segmented healthy trees lose more than 10% of pressure at physiological flow. Normal coronaries have hyperemic FFR of about 0.95-0.99, which points to radius underestimation.

**Fix:**
- (a) Report, per baseline-FFR band, the distribution of DS, throat radius/MLA, absolute hyperemic flow through the lesion, and territory MBF in mL/min/g, using myocardial or lumen-volume mass as available.
- (b) Make a physiologically calibrated demand co-primary: a radius-corrected inlet (for example +half voxel), or k×2-3, or a mass-based total flow such as Q ∝ M^0.75 with a hyperemic resistance factor.
- (c) Report T5 flips and passes-and-wrong at k×2 and ×3, and express the throat error as a relative change (dr/r or dMLA/MLA).
- (d) Temper the abstract's throat figures, or qualify them as conditional on the primary demand.

### W2 (major): The clean reference shares Protocol B's bed rule, so re-derivation has an oracle advantage. The clinical rationale for perfusion tuning is not represented.

**Anchors:**
- "Cb was calibrated on the healthy-equivalent network ... so that inflow equals the hyperemic demand Q = k r_in^3"
- "Under Protocol B (re-derived), the bed rule is applied to the corrupted tree and Cb is recalibrated"
- "Tuning raised these proportions relative to B in the discrete bed"
- Limitations: "microvascular dysfunction, collaterals ... were not modeled"

The "truth" here is generated by the same morphometric scaling law that Protocol B re-applies. Re-derivation is therefore correct by construction apart from the segmentation error. Perfusion tuning exists in practice precisely because scaling laws fail per patient: coronary microvascular dysfunction, diffuse disease, LVH, prior infarction, collaterals and dominance. In this design tuning can only absorb segmentation error, never correct a true physiological deviation. The B-versus-C/D comparison, and the message that tuning "turned caliber errors into passing models", is therefore partly built into the design. A clinician reading the Discussion could infer that re-derivation is safer than perfusion tuning. The study cannot support that conclusion.

**Fix:**
- Add an arm in which the clean truth has patient-level and territory-level microvascular heterogeneity. Examples: multipliers on Cb drawn from published IMR or hyperemic MBF distributions, with a CMD subgroup of about 20-30%, and a reduced-MBF territory beyond the stenosis.
- Then recompute flips and passes-and-wrong under B, C and D. This shows the trade-off (tuning fixes physiology but hides geometry) that a clinician needs.
- At minimum, state explicitly in the Abstract and Discussion that Protocol B benefits from a reference built on the same bed rule, and that the B-versus-C/D contrasts are not a recommendation against perfusion tuning.

### W3 (major): Territory definitions and targets do not match how perfusion data are used for tuning in practice.

**Anchors:**
- "A perfusion territory is the subtree below each child of the first bifurcation of the clean tree (a median of two and at most three per tree)"
- "Each corrupted node belongs to the territory of its clean counterpart"
- "Protocols C and D are defined only when at least two territories retain a vessel, which excluded most right coronary instances with a topological error"

**How perfusion data are used in practice.** In PET/CMR/CT-perfusion workflows, flow is reported per AHA 17-segment model or per voxel. It is mapped to the epicardial tree through myocardial Voronoi (nearest-vessel) territories built from the model's own segmented tree. Targets are MBF (mL/min/g) multiplied by segmented myocardial mass, not territory flows from an error-free twin.

**How this study differs.**
- **Territory assignment.** It uses an oracle: the territories and node assignments come from the clean tree. A real pipeline with a missed diagonal would reassign that myocardium to the LAD or neighbouring vessels by proximity. This study models that redistribution, but it does so with knowledge of the true branching.
- **Resolution.** Two or three territories per tree is coarser than any clinical perfusion read.
- **Right coronary artery.** Its first bifurcation is usually the conus or an RV branch, not the PDA/PL split, so the main-branch partition is anatomically meaningless there. This explains why most RCA topological instances drop out. The tuned results therefore describe the left tree only (acknowledged).
- **Headline resolution.** The finer partition, which is closer to clinical segmental resolution, reduces topological concealment to 2-7% (Table S8). Yet the abstract leads with the 19-20% main-branch figure.

**Fix:**
- (a) Define territories by Voronoi or AHA-segment mapping on a myocardial surface, using the corrupted tree's own branches, if the dataset permits LV segmentation. Otherwise justify the proxy and state which partition corresponds to PET/CMR practice.
- (b) Give the finer-territory result equal prominence in the Abstract and Conclusion.
- (c) Discuss dominance (left-dominant LCx) and why RCA territories cannot be defined at the first bifurcation.
- (d) Note that targets in practice carry mass-segmentation error in addition to MBF noise.

### W4 (major): The tuning parameter ranges are not physiological, and models at the bound are retained.

**Anchors:**
- "The fit searched ±1.5 decades of Cb"
- "fitted (within 10^±3)"
- Supplement: "64 Protocol D fits at the parameter bound, all with an increased stenosis, were retained; excluding them would raise passes-and-wrong by up to 13 points"

A thousand-fold scaling of hyperemic microvascular conductance in a territory is outside anything physiological. Hyperemic microvascular resistance varies across patients by a factor of roughly 3-5, perhaps 10 in severe CMD. Practical twin calibration uses priors or bounded ranges, and an implausible fitted resistance is itself a red flag that an analyst would act on.

**Fix:**
- Rerun C and D with physiologically bounded factors (for example 0.2-5× the scaling-law value). Treat a fit at the bound as a failed QC rather than a pass.
- Report the distribution of fitted factors by error type.
- Extend the |ln C| detector analysis (Table S10) to Protocol D's per-territory factors.

I expect this to reduce throat passes-and-wrong under D materially, and it would be a clinically actionable safeguard.

### W5 (major): The meaning of an FFR 0.80 flip is not framed against CT-FFR's own error, its grey zone, or the continuous FFR-outcome relationship.

**Anchors:**
- "A flip is a change of classification at 0.80 between the two, and hence potentially in referral or treatment"
- "Each flip rate is compared with a noise floor ... 0.018 [32]"

**Clinical context.** Clinically, a CT-FFR value is not acted on as a binary at 0.80. Values of about 0.76-0.80 measured 1-2 cm distal to the lesion are a recognized grey zone. Decisions integrate anatomy, symptoms and often invasive confirmation. The prognostic relation between FFR and events is continuous: Johnson et al., JACC 2014, as I recall, showed risk rising smoothly as FFR falls. A flip from 0.81 to 0.79 therefore carries little clinical consequence.

**Comparator.** The appropriate comparator for "is this segmentation error clinically meaningful" is not only same-session invasive repeatability (SD 0.018, which is wire-on-wire). It is also:
- the agreement of CT-FFR with invasive FFR (per-vessel SD of differences of the order of 0.07-0.10 in NXT-era data);
- the inter-analyst or core-lab reproducibility of CT-FFR (I recall values of a few hundredths, uncertain).

**Prevalence.** The threshold-stratified design (25 per band) is acknowledged, but readers will quote "a third of decisions".

**Fix:**
- (a) Reweight flip and passes-and-wrong rates to a published clinical CT-FFR distribution to give an indicative per-patient rate.
- (b) Report flips into or out of the CT-FFR grey zone of 0.75-0.80 separately from those that cross it.
- (c) Place the |dFFR| distributions against CT-FFR-versus-invasive limits of agreement.
- (d) Add one sentence on the continuous outcome gradient.

### W6 (minor): Caliber-error flip rates are described as being "of the order of" the measurement floor when the taper exceeds it.

**Anchors:**
- "their flip rates of 1-14% were of the order of the 5.0-6.5% expected from repeat invasive measurement"
- "(the taper up to 14%)"

The discrete-bed taper rates of 13% (8-22) and 14% (9-23) have lower Wilson bounds above 6.5%.

**Fix:** State that the taper exceeded the floor in the discrete bed. Also note that comparing a deterministic error-induced flip with a stochastic test-retest probability is a benchmark, not an equivalence.

### W7 (minor): The realism of the throat error and the actionability of "check the throat diameter".

**Anchors:**
- "Second, check the lumen caliber, above all the throat diameter."
- "a half-voxel error below the image resolution can"

**Realistic throat error.** In clinical CCTA the effective spatial resolution is about 0.5-0.6 mm, not the 0.35 mm voxel. The dominant throat error mechanisms are calcium blooming, partial volume and motion. These usually overestimate stenosis and are larger than half a voxel. The ±10-point DS sensitivity (Table S7) is closer to clinical CT-versus-QCA disagreement.

**Actionability.** An error below the voxel cannot be "checked" by a reader.

**Fix:** Recast this consideration as propagating throat uncertainty: report a CT-FFR interval or probability of ≤ 0.80. Mention calcium blooming and plaque composition as the dominant mechanisms, and describe the ±10-point analysis as the clinically realistic magnitude.

### W8 (minor): The clinical plausibility and frequency of the topological errors.

**Anchors:**
- "T1 and T2 have no measured magnitude and are design choices"
- "The rates are conditional on an error being present"

Deleting the largest side branch beyond a proximal lesion (typically a major diagonal or OM) or truncating the LAD 25 mm beyond the lesion is something analyst review in commercial CT-FFR workflows would usually catch. The clinical relevance lies in fully automated pipelines.

**Fix:** State this explicitly in the Introduction and the Implications section, and consider a smaller-branch variant (for example the first branch of ≥ 1.0-1.5 mm beyond the lesion). Clinically that is the more realistic miss, and it is where Dice-based QC is least sensitive.

### W9 (minor): The bed-structure contrast is confounded.

**Anchors:**
- leaky bed: "truncated at r_ref = 0.50 mm ... so that flow follows Murray's cube law"
- discrete bed: "truncated at r_ref = 0.60 mm ... with conductance r_ref^2.66/Cb"

The beds differ in exponent (3 against 2.66), in truncation radius and in outflow topology. The "leaky bed damped topological errors" finding therefore cannot be attributed to distributed outflow alone.

**Fix:** Run one cross-condition (for example the discrete bed with exponent 3, or the leaky bed with 2.66) or state the confound.

Also check the statement "exponent 2.66 is close to 8/3, so outlet flow is proportional to perfused myocardial mass". My recollection of the Kassab scaling work [25] is flow ∝ mass^~3/4 and a stem-diameter exponent that yields flow ∝ D^~7/3 rather than D^8/3. I am uncertain here, so please quote the exact relation from [25].

### W10 (minor): Representation of prior work and missing key references.

**Ref. [9].** It concerns pulmonary valve FSI. It is a weak support for "tuned so that the model reproduces ... measured flow splits" in a coronary digital-twin context.

**Possible coronary references to add (from memory; please verify):**
- **Coupled models and hyperemia scaling:** coupled coronary-myocardial perfusion models calibrated to perfusion imaging (for example Papamanolis et al., Ann Biomed Eng, around 2020-2021); the morphometry-based hyperemia approach of Taylor et al. [3] with the adenosine resistance-reduction factor.
- **Side-branch flow allocation:** side-branch flow-diameter exponents measured in human coronaries (for example van der Giessen et al., J Biomech 2011, exponent around 2.3).
- **Image quality:** effect of image quality and misregistration on CT-FFR accuracy (DISCOVER-FLOW/NXT image-quality analyses, Min/Leipsic).
- **Perfusion against CT-FFR:** the PACIFIC head-to-head comparison of CCTA-FFR, PET and SPECT against invasive FFR (Driessen et al., JACC 2019).
- **Outcomes:** the continuous FFR-outcome relationship (Johnson et al., JACC 2014).
- **Perfusion repeatability:** for hyperemic MBF test-retest, PET test-retest data in CAD patients (for example Kitkungvan et al., JACC CVI 2017) would support the 10% threshold more directly than an expert-panel statement [28] and a healthy-volunteer CMR study [29].

**Unverifiable references.** I could not verify refs [5], [18] and [23], which are 2026 items, nor the specific side-branch figures attributed to [20] and [21] (15.5%, 13%, "little change in accuracy after recalibration"). Please double-check that [21] is represented accurately. My recollection is that Gosling et al. examined the effect of accounting for side-branch flow on computed indices, and the direction of their conclusion should be quoted precisely.

**Fix:** Replace or supplement [9], add the coronary references above as appropriate, and verify the quoted numbers.

### W11 (minor): The mixed-effects model does not cover the headline contrasts.

**Anchors:**
- "A Bayesian mixed-effects logistic model agreed with the paired tests"
- Table S2 has no T5 and no Protocol D terms.

**Fix:** Include T5 and D, or narrow the claim to the terms modeled. Also report a convergence or diagnostic note for the variational fit.

### W12 (minor): Clinical wording in the Conclusion.

**Anchor:** "Safeguards are therefore most needed at the branching near the lesion and at the throat diameter"

This is reasonable, but given W1 and W3 it should be conditioned on demand and territory resolution. "Up to one in five tuned topological-error models (discrete bed ...)" should be paired in the same sentence with the finer-territory 2-7% figure, so that the take-home message is not the most pessimistic configuration.

---

## Rubric scores

| Code | Dimension | Score (1-10) | Status | Justification |
|------|-----------|:---:|:---:|---|
| S1 | Novelty and contribution | 7 | pass | First decision-level, paired comparison of fixed, re-derived and tuned BCs on identical corrupted anatomy. The non-identifiability concept is known, but quantifying it at 0.80 is new and useful. |
| S2 | Methodological rigour | 6 | warn | Paired design, two beds, two floors and exact tests are strong. However, the oracle reference shared with Protocol B, unphysiological tuning bounds and the oracle clean-tree territories weaken the protocol contrasts (W2-W4). |
| S3 | Claims supported by evidence | 6 | warn | Throat and topological-concealment headline figures rest on a sub-hyperemic regime and the coarsest territory partition. The topological tuned excess did not replicate at 2× demand. The taper is described as "of the order of" the floor although it exceeds it (W1, W3, W6). |
| S4 | Domain / physiological accuracy | 5 | block | A median per-tree flow of 137 mL/min and an 80% DS proximal-LAD lesion with FFR 0.76-0.87 imply near-resting flow. Lesion severity and throat sensitivity are distorted, and lesion flow and MBF must be reported and a physiological demand analysed (W1). |
| S5 | Internal consistency | 8 | pass | Spot checks of abstract, text, Table I and Tables S3/S5/S6/S8 (e.g. 20/104, 9/171, 20/39, 14/154, 5-19%, 2-7%) are consistent. Small wording differences exist between the B-only and B/C ranges. |
| S6 | Clarity, structure, readability | 7 | pass | Definitions are explicit and figures informative, but the text is very number-dense. The protocol and bed matrix needs a summary table for clinical readers. |
| S7 | Venue fit (IEEE JBHI) | 7 | pass | Segmentation QC, digital-twin credibility and reduced-order modelling fit JBHI. The clinical-decision framing is a plus. |
| S8 | Reproducibility and transparency | 8 | pass | Public data, open code, fixed seed, full exclusion table, solver and mesh settings, and honest reporting of non-replication. |

**Overall score: 6.2 / 10**

**Recommendation: major revision.** The computational work is careful and the core message is valuable. Before the clinical conclusions can be trusted, however, the flow regime must be shown to be physiological (or the results re-anchored to a physiological demand, including T5). Perfusion tuning must also be represented as it is used in practice: physiological bounds, a reference with patient-specific microvascular deviation, and clinically resolved territories. Finally, the 0.80 flips need framing against CT-FFR's own error and the continuous outcome relationship.
