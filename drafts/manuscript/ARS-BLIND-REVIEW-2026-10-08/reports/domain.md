contract_role: domain
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: block
trigger: "A central quantitative claim depends on a physiologically implausible assumption (for example hyperemic flow or microvascular resistance outside reported human ranges"
block_class: repairable
rationale: The model runs at a hyperemic flow of roughly one third to one fifth of measured human per-tree hyperemic flow (cohort median 90 mL/min per tree; an 80% DS, 20 mm proximal LAD lesion yields FFR 0.870), and the only demand sensitivity (x0.7 and x1.3) does not reach the human range, while the headline pass-while-wrong proportion moved from 12% to 25% across that narrow range. Further domain defects (perfusion tuning and territory definitions that do not represent perfusion-informed practice, a 3D case that shows removal rather than concealment of the error, a decision endpoint that ignores the FFR grey zone) are repairable by re-analysis and reframing; none invalidates the direction of the topological-versus-caliber finding.

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

Reviewed as a clinical coronary physiologist with a CT-FFR modelling record. The question (can boundary-condition tuning hide a topological segmentation error that changes the decision at 0.80?) is clinically relevant, the paired ablation design is clean, and the qualitative physiology of side-branch loss is right: removing a branch distal to a stenosis removes flow through the stenosis and raises FFR, biasing toward deferral. My concerns are about whether the flow regime, the tuning protocol and the perfusion "check" correspond to human hyperemic physiology and to perfusion-informed CT-FFR practice, and therefore whether the concealment proportions (8–19%) transfer to real pipelines. Prior work I checked (Gamage 2022, Gosling 2020, Johnson 2015, Menon 2024, Choy and Kassab 2008, ImageCAS-X) exists; Gamage, Johnson (SD 0.018) and the ImageCAS-X inter-observer statistics (DSC 92.8, HD95 2.46 mm, DSC as upper bound, vessel breaks in all model outputs) are represented correctly. Reference [9] could not be confirmed as a JBHI publication and is off-topic (see W10).

### S1: Decision endpoint referenced to invasive repeatability
Judging segmentation error by reclassification at 0.80 and against a repeat-FFR noise floor built from Johnson 2015 (SD 0.018, which I verified) and the Petraco measurement-certainty approach is the right clinical frame and is more informative than continuous sensitivity indices.
**Evidence Anchor**: `text: Sec. II-F "following the measurement-certainty approach of [31]"`

### S2: Physiologically correct direction of the side-branch effect
The missed-branch result (loss of distal run-off lowers trans-stenotic flow and raises FFR) agrees with established side-branch physiology, and the clinical consequence is stated correctly as a bias toward under-treatment.
**Evidence Anchor**: `text: Sec. IV-C "biases the decision toward deferring treatment of a lesion that needs it"`

### S3: Accurate representation of the closest OCT side-branch study
The Gamage et al. figures (15.5% idealized; 13% in one of two OCT patients, 2% in the other; distal resistance held fixed) match the source.
**Evidence Anchor**: `text: Sec. I "lowered FFR by 15.5% in an idealized model and by 13% in one of two models built from optical coherence tomography"`

### S4: Candid limitation on right coronary applicability
The authors disclose that tuned results for topological errors effectively describe the left coronary tree, which is the clinically honest reading of Table S1.
**Evidence Anchor**: `text: Sec. IV-D "was undefined for most right coronary instances with a topological error"`

### W1: Hyperemic flow is far below human values, and the sensitivity range does not reach them
The demand law is anchored to a 3.7 mm proximal LAD (214 mL/min, consistent with Fournier 2021), but the cohort's own radii are much smaller: median inlet radius 1.39 mm (diameter 2.8 mm, below normal left main and proximal RCA diameters in Dodge 1992) and median demand 90 mL/min per tree. Normal hyperemic flow is about 230–290 mL/min per major vessel alone, so the left tree should carry several hundred mL/min. The 3D case confirms the low-flow regime: an 80% DS, 20 mm proximal LAD lesion gives FFR 0.870, whereas in FAME 80% of 71–90% angiographic stenoses had FFR ≤ 0.80 (Tonino 2010). At realistic flow the quadratic expansion loss dominates, so the FFR response to the flow lost with a branch, and the inserted DS needed to reach each baseline band, both change. The demand sensitivity (x0.7, x1.3) already moved the discrete-bed pass-while-wrong proportion from 12% to 25% (Table S4), so the headline proportions are not robust in the direction that matters. Fix: report the cohort's inlet and host-vessel diameters against Dodge norms and quantify the radius bias of the half-voxel subtraction (3D lumen was 0.14 mm wider); set demand from myocardial mass or a per-vessel flow consistent with Fournier; rerun at physiological flow (or x2–x3) and report Table I there.
**Severity**: Major | **Evidence Anchor**: `text: Sec. II-B "median demand was 1.5 mL/s (inlet radius 1.39 mm)"` | **Confidence**: 4 — core expertise: coronary hyperemic flow and CT-FFR boundary conditions

### W2: The 3D case shows removal of the FFR error, not concealment
With prescribed territory flows, the missed branch changed 3D FFR by −0.0007 (0.892 in both geometries); the reduced-order twin gave −0.0005. That is the opposite of concealment: per-outlet flow prescription restored trans-stenotic flow and therefore the correct FFR, as expected when flow through the lesion is fixed. The abstract places this result immediately before "A perfusion-matched coronary model can thus pass validation with a material error", and the Discussion says the 3D case "showed the same mechanism". The 3D case supports the fixed-resistance arm (+0.074) only. Fix: state that the per-outlet tuned 3D model had no material error, and either solve the 3D case under the same one-scalar Protocol C used in the cohort or drop the claim that 3D confirms concealment.
**Severity**: Major | **Evidence Anchor**: `text: Sec. III-D "The 3D solution showed the same concealment."` | **Confidence**: 5 — direct reading of reported values

### W3: Protocol C does not represent perfusion-informed tuning as practised
Perfusion-informed coronary models (Menon et al. 2024, ref [8], which I checked) assign flow per perfusion territory or outlet so that the patient-specific flow distribution is reproduced; they do not fit one global bed constant to two or three territory totals. A single scalar cannot redistribute flow between territories, which is why the residual and the FFR error survive in the cohort, whereas the per-outlet form (the 3D arm and its twin) removed both. The pass-while-wrong rates are therefore a property of the least flexible tuning, not of perfusion tuning in general, and the abstract and conclusion generalize them. Fix: add a per-territory (one constant per territory) or per-outlet tuning arm to the reduced-order cohort and report pass-while-wrong under it; restrict the abstract claim to global-scaling calibration if concealment disappears.
**Severity**: Major | **Evidence Anchor**: `text: Sec. II-D "one global scaling of C (one bed scaling) is fitted"` | **Confidence**: 4 — core expertise: perfusion-based coronary BC personalization

### W4: Perfusion territories are too coarse to represent a clinical perfusion check
Territories are the subtrees below the first bifurcation, so a left tree has two (LAD, LCx) or three. Clinical PET, CMR and CT perfusion report flow on a 17-segment model, and coronary-to-myocardium assignment is done per segment. A missed diagonal or obtuse marginal would leave an anterolateral or lateral segment with no supplying model vessel, which a segmental comparison flags; the two-territory sum cannot. For the RCA the first bifurcation is often a conus or RV branch, which is anatomically arbitrary. The pass-while-wrong numbers depend directly on this granularity. Fix: define territories by myocardial segment (or at least by major epicardial vessel and its first-order branches), report the residual per segment, and show how pass-while-wrong changes.
**Severity**: Major | **Evidence Anchor**: `text: Sec. II-D "A perfusion territory is the subtree below each child of the first bifurcation of the clean tree."` | **Confidence**: 4 — core expertise: myocardial perfusion imaging and territory assignment

### W5: A post-calibration residual is presented as "validation"
In perfusion-informed pipelines the perfusion data are calibration inputs; the residual to the same data after fitting is a goodness-of-fit, not an independent validation, and credibility frameworks (ASME V&V40, ref [33]) do not treat it as validation. The paper's headline that a model "can pass validation" therefore attacks a practice for which no published pipeline is cited. The finding that remains is narrower and still useful: the pre-tuning mismatch carries the error signal and the post-tuning residual cannot. Fix: cite pipelines that report post-calibration perfusion agreement as validation evidence, or rephrase the claim as "a calibration-fit check cannot detect" and reserve "validation" for comparison with independent data such as invasive FFR.
**Severity**: Major | **Evidence Anchor**: `text: Abstract "A perfusion-matched coronary model can thus pass validation with a material error in its fractional flow reserve."` | **Confidence**: 4 — core expertise: CT-FFR validation practice

### W6: A crossing of 0.80 is equated with a change in treatment decision, ignoring the grey zone
Fig. 2 shows flips concentrated in the bands adjacent to 0.80, so many flips are small crossings (for example 0.79 to 0.81). Clinically, FFR and CT-FFR values in the 0.75–0.85 grey zone (Petraco 2013, ref [31]) prompt integration with other data or invasive confirmation, and risk is continuous in FFR (Johnson 2014). Calling every crossing a "change in the treatment decision" overstates clinical consequence, particularly for the caliber errors whose flips sit at the threshold. Fix: report reclassification across the grey zone (crossing from below 0.75 to above 0.85 or vice versa) alongside the 0.80 flips, and describe 0.80 crossings as classification changes.
**Severity**: Major | **Evidence Anchor**: `text: Sec. II-F "A flip is a change of classification at 0.80 between the two, that is, a change in the treatment decision."` | **Confidence**: 4 — core expertise: invasive FFR interpretation

### W7: Reconciliation of Gamage and Gosling is overstated
Gosling et al. 2020 (verified) added a taper-based (Murray) leakage function for unresolved side-branch flow and found vFFR essentially unchanged while volumetric flow changed. That construction is the analogue of the leaky bed, not of perfusion tuning, so the statement that Gosling's result "appears ... after tuning" maps it to the wrong protocol; in the present data the leaky bed damps the error before tuning. Fix: describe Gosling's method accurately and attribute the reconciliation to bed structure as well as protocol, or soften "reproduced".
**Severity**: Minor | **Evidence Anchor**: `text: Sec. IV-B "Both appear in our cohort, the first with fixed resistance and the second after tuning"` | **Confidence**: 3 — verified from the Gosling abstract; full methods not checked

### W8: Noise floor uses the SD of a difference where a single-measurement SD may apply
The 0.018 value from Johnson 2015 is the test–retest SD of the difference between two measurements. The clean model is a deterministic reference, so the analogue of one measurement against truth has an SD of about 0.018/√2 ≈ 0.013, which lowers the floor below 5.0–6.5% and moves more caliber cells (notably T4 under Protocol A) above it. Fix: justify the choice or report both floors; temper "close to the variability of repeat invasive measurement" accordingly.
**Severity**: Minor | **Evidence Anchor**: `text: Sec. II-F "the published standard deviation of the difference between repeat measurements, 0.018"` | **Confidence**: 3 — standard measurement-error reasoning

### W9: HD95 is not a measure of lesion-length disagreement
HD95 in ImageCAS-X is 2.46 ± 3.62 mm over the whole tree (verified); its large spread indicates it is dominated by distal and branch-level disagreement, not by stenosis extent. Using it as a lesion-lengthening magnitude labels T3 as "inter-observer" without evidence. Fix: describe T3 as a design choice of HD95 scale, or derive lesion-extent variability from stenosis-specific inter-observer data in CT angiography.
**Severity**: Minor | **Evidence Anchor**: `text: Sec. II-C "HD95 (2.46 mm) sets T3."` | **Confidence**: 3 — adjacent: segmentation metrics

### W10: Off-topic and unconfirmed citation for flow-split tuning
Ref. [9] is a pulmonary-valve fluid–structure interaction study; I could not confirm it as a JBHI 2026 article, and it does not support coronary perfusion or flow-split tuning. Fix: replace with coronary flow-split or perfusion-calibration work.
**Severity**: Minor | **Evidence Anchor**: `text: Sec. I "or measured flow splits [8], [9]"` | **Confidence**: 3 — web search did not locate the JBHI record

### W11: Validation trials cited with a methods paper
Ref. [2] (Taylor 2013) describes the scientific basis of FFRCT and is not a multicenter trial. Fix: cite DISCOVER-FLOW (Koo 2011) and DeFACTO (Min 2012) with NXT [3] [UNVERIFIED in-session; well-known trials, metadata to be checked by authors].
**Severity**: Minor | **Evidence Anchor**: `text: Sec. I "validated against invasive measurement in multicenter trials [2], [3]"` | **Confidence**: 4 — core expertise: CT-FFR trial literature

### W12: Demand setting in commercial CT-FFR is misdescribed
In the HeartFlow approach described in ref. [2], total coronary flow is set from myocardial mass and only its distribution follows lumen-based scaling; it is not derived purely from the segmented lumen. This matters because a mass-based total, like Protocol C, is unaffected by a missed branch. Fix: describe mass-based total flow and state which protocol corresponds to it.
**Severity**: Minor | **Evidence Anchor**: `text: Sec. I "Its resistance is not measured but derived from the segmented lumen through scaling laws"` | **Confidence**: 4 — core expertise: CT-FFR boundary conditions

### W13: 3D prescribed-flow baseline differs from fixed-resistance baseline without explanation
The 3D lesion baseline is 0.870 with clean resistances but 0.892 with prescribed "clean territory flows". In the 3D arm "clean" means no lesion, whereas in the cohort "clean" means lesion without segmentation error; prescribing no-lesion flows would raise trans-stenotic flow and lower, not raise, FFR. Fix: define the prescribed flows in the 3D arm and explain the 0.022 baseline difference.
**Severity**: Minor | **Evidence Anchor**: `text: Sec. III-D "(0.892 in both geometries)"` | **Confidence**: 3 — inference from reported values

### W14: Missing key references on side branches, model topology and angiographic–functional mismatch
Directly relevant work is not cited: Vardhan et al., Sci. Rep. 2019 (side branches in 3D coronary hemodynamics; verified); Fossan et al., J. R. Soc. Interface 2018 (topological complexity of 1D arterial networks; verified); Tonino et al., JACC 2010 (angiographic versus functional severity in FAME; verified); Johnson et al., JACC 2014 (continuous FFR–outcome relationship; verified).
**Severity**: Minor | **Evidence Anchor**: `absence: Sec. I and Sec. IV-B — expected citation of side-branch and topology studies and of FFR outcome continuity; checked reference list [1]–[33], Introduction and Discussion` | **Confidence**: 4 — core expertise: CT-FFR literature
