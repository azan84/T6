---
source_pdf_path: Resources/2603.19331v1.pdf
slug: choi-2026-bc-amortized
ledger_id: C017
ledger_status: FULL
---

# choi-2026-bc-amortized

## Bibliographic
- Title: FalconBC: Flow matching for Amortized inference of Latent-CONditioned physiologic Boundary Conditions
- Authors: Chloe H. Choi (Stanford Mechanical Engineering), Alison L. Marsden (Stanford ICME/Bioengineering/Pediatric Cardiology), Daniele E. Schiavazzi (Notre Dame Applied & Computational Math and Statistics)
- Year: 2026 (arXiv v1, "18 Mar 2026" per header — note: appears to be a future-dated/placeholder arXiv identifier, 2603.19331)
- Venue: arXiv:2603.19331v1 [cs.LG]
- DOI: NOT REPORTED
- Code URL: NOT REPORTED
- Data URL: NOT REPORTED
- Conflict of interest: NOT REPORTED (no COI statement in the extracted text; acknowledgments cite NSF #2105345, NIH #1R01HL167516, Yansouni Family Fellowship, AHA Predoctoral Fellowship 26PRE1550972)

## Problem & claim
- Imaging modality and domain: No clinical imaging cohort. Two synthetic/semi-synthetic vascular models: (1) an idealized aorto-iliac bifurcation with parametrically-inserted stenoses, (2) a single coronary arterial tree geometry taken from prior published work ("we consider a model of coronary artery disease (CAD) from [33]"), used only to vary boundary-condition (outlet resistance) values, not anatomy.
- Task: Method paper — amortized Bayesian inference of cardiovascular boundary conditions (Windkessel/RCR resistances and capacitances) via conditional flow matching (CFM), optionally jointly estimating inflow-waveform Fourier features and/or a learned point-cloud embedding of stenosed anatomy, conditioned on noisy clinical targets (systolic/diastolic pressure, flow split, mean branch flow).
- Central claim (abstract, p.1): "We introduce a general amortized inference framework based on probabilistic flow that treats clinical targets, inflow features, and point cloud embeddings of patient-specific anatomies as either conditioning variables or quantities to be jointly estimated." Three stated contributions (p.3): (i) an amortized-inference paradigm requiring no retraining across new targets/inflows/anatomies; (ii) a data-driven encoder-decoder point-cloud embedding of the lumen surface usable for conditioning or joint estimation; (iii) a CFM-based framework for "generalized boundary condition tuning problems, where additional relevant latent space features can be jointly estimated to improve reachability of clinical targets."

## Method
- Conditional flow matching (CFM): learns a velocity field transporting a Gaussian base distribution to the target posterior of BC parameters, conditioned on an auxiliary vector Y (clinical targets, inflow Fourier features, and/or anatomy embedding) — Eqs. 2.1–2.4, Section 2.
- Anatomy embedding: point clouds (N=1024 points, 50 augmented samples/geometry) of the lumen surface, normalized to a template (healthy) anatomy (Section 2.1.2). Two embedding schemes for stenosed anatomies (Section 2.1.3): (a) a hand-specified 6-D one-hot vector of stenosis location (6 possible sites A–F, left/right iliac) × severity percentage; (b) a learned PointNet-based permutation-invariant encoder predicting mode (location) and severity (Eqs. in Section 2.1.3).
- Aorto-iliac case: RCR-type BCs tuned at increasing dimensionality (2D total R+C; 4D per-outlet R+C; 6D per-outlet RCR), Section 3. Inflow curves generated/estimated jointly via Fourier-feature CFM (Section 3.3).
- Coronary case (Section 3.5, "Towards broader clinical application: coronary artery disease"): a single fixed 3D geometry with 14 labeled coronary outlets (left+right coronary artery), closed-loop LPN BCs; Nc=14 resistance random variables r1..r14 estimated from noisy branch-flow targets; training sets of N=100/500/1000 realizations of resistance-scaling perturbations (uniform prior [0.5ri, 2.0ri]).
- Ground truth for training/testing: all data are simulator-generated (0D LPN "ground truth" forward runs), not measured/clinical data with independent validation, except the coronary branch-flow targets which are drawn against literature values ("measured", yellow ellipse in Fig. 19) for comparison, not from an independent segmentation/imaging cohort.

## Data
- No patient imaging cohort, no segmentation dataset. Two synthetic/semi-synthetic geometric models (aorto-iliac bifurcation; one coronary tree from prior work [33]). N=100/500/1000 simulated training realizations (Fig. 18 caption: "14 coronary outlets (N=100/500/1000)"). No invasive-FFR or any clinical outcome ground truth. No mention of Dice, Hausdorff, Betti number, inter-observer, inter-rater, or annotator disagreement anywhere in the text (confirmed by full-text grep).

## Evaluation
- Aorto-iliac: marginal/posterior-predictive comparisons of estimated BC parameters and forward-simulated pressure/flow traces against "true" (simulator-generated) values across held-out stenosis geometries (Figs. 11–15); a remark on parameter non-identifiability / flow reversal encountered during training-set generation for high right-iliac stenosis (p.19, "Remark (Selection of seemingly equivalent RCR BCs)").
- Coronary: posterior predictive branch-flow distributions vs. literature-reported measured values (Fig. 19), not a decision-level (FFR) endpoint.
- No FFR value, no 0.80 threshold, no reclassification/decision-flip metric anywhere in the paper (confirmed by full-text grep for "FFR").

## Reproducibility
- Code/data URLs: NOT REPORTED in the extracted text.
- Hyperparameter search via Optuna, ranges given in an appendix (Section A / Table 6, referenced but not transcribed here).

## Limitations (author-stated, Conclusion, pp.23–25)
- "we assumed rigid wall"; single patient/geometry topology per case, "we leave as future work" incorporating "anatomies of patients with different topologies."
- 0D/LPN fidelity may be insufficient for "pulmonary models, with numerous branches, and more pronounced minor losses due to bifurcation."
- Exercise/stenosis interaction and larger patient cohorts flagged as future work.

## Openings for T6
- The paper's own "future work" (rigid geometry, single topology, no measured segmentation error, no clinical decision endpoint) is exactly the gap T6 targets: it neither uses real inter-segmenter disagreement nor evaluates a clinical binary-decision threshold.

## Key references
- [33] Menon, Zanoni, Khan, Geraci, Nieman, Schiavazzi, Marsden — source of the coronary CAD model reused here (personalized/uncertainty-aware coronary hemodynamics).
- [10] cited (p.2) as the source of the statement "segmentation uncertainty can influence simulation predictions" — worth checking if this is a T6-relevant prior work already in the corpus.

---

## T6 targeted questions

- **Q-A geometry perturbation**: SYNTHETIC only. Stenoses are researcher-parameterized: "we create a set of left and right iliac artery stenosis models" (p.3) at 6 named locations (A–F) with severities set by construction (e.g., test set "Location A with 56.7% stenosis, Location B with 66.7% stenosis..." p.17-18). The coronary case uses a single fixed real geometry from prior work with only outlet-resistance values perturbed, not the anatomy. No measured/real inter-segmenter or inter-observer geometric disagreement anywhere in the text (grep for Dice/Hausdorff/Betti/observer/annotator/rater: zero hits).

- **Q-B decision flip**: NOT REPORTED. No occurrence of "FFR" anywhere in the full text (grep confirmed zero hits). No diagnostic threshold, reclassification, or decision-flip metric of any kind is reported; all evaluation is in terms of BC-parameter posterior accuracy and forward-simulated pressure/flow traces against simulator ground truth.

- **Q-C BC tuning**: Central topic. RCR/Windkessel-type boundary conditions and closed-loop LPN resistances are estimated by CFM conditioned on clinical targets (pressure, flow split, mean flow). Joint (not just conditional) estimation of BCs together with inflow features and/or anatomy embedding is a headline contribution: "treats clinical targets, inflow features, and point cloud embeddings of patient-specific anatomies as either conditioning variables or quantities to be jointly estimated" (Abstract, p.1). On re-tuning after geometry/anatomy change: yes, in the sense that BC posteriors are conditioned on (or jointly inferred alongside) the anatomy latent for each new stenosed geometry (Section 3.4, Figs. 11-16) — this is not literally "re-tuning after a change" to one fixed patient's geometry but joint estimation across a family of differently-diseased geometries. Explicit statement that anatomy/segmentation imprecision limits what BC tuning alone can achieve: "the pressure measured with a catheter is not reachable with boundary condition tuning due to imperfections in the segmented anatomy. This approach holds the potential to instead estimate necessary changes in local anatomical features (e.g. diameter) that would lead to the desired pressures or flow splits" (Conclusion, p.24). This is framed as a target-reachability/parameter-identifiability limitation to be addressed by *also estimating anatomy*, not as a claim that BC tuning silently absorbs/masks anatomical error while looking validated.

- **Q-D fidelity / quantity**: Zero-dimensional (LPN) only for all reported simulations; 3D CFD is invoked only as background motivation ("computational resources has facilitated... high-fidelity, three-dimensional (3D) computational fluid dynamics (CFD) simulations", p.1) and as the source of the (rigid-wall, single-topology) geometries whose surface point clouds are embedded — no 3D CFD is run in this paper. No WSS, OSI, or any spatially-resolved field is reported; outputs are pressure, flow, and flow-split scalars/traces.

- **Q-E data**: No named clinical cohort/dataset. Aorto-iliac model: a single template ("healthy") anatomy with synthetically inserted stenoses at 6 locations, N=100/500/1000 (varies by experiment) simulated training realizations plus small held-out test sets (e.g., N=6 unseen geometries). Coronary model: a single geometry reused from reference [33], N=100/500/1000 simulated resistance realizations. All private/self-generated, no public-dataset name given, no invasive-FFR or other clinical ground truth (explicitly: pressure/flow "targets" are noisy simulated or literature values, not from a segmentation/imaging cohort with adjudicated ground truth).

- **Q-F meshing**: Minimal. "Each vascular geometry is provided as a tetrahedral mesh. We extract vertex coordinates from the surface mesh" (Section 2.1.2, p.6) — meshing itself is not described (no snappyHexMesh/segmentation-to-surface-to-volume pipeline detail), and there is no statement about robustness to poor, broken, or topologically incorrect geometry. LPN generation from centerlines is only mentioned generically in the Introduction ("LPNs can be automatically created from the three-dimensional model centerlines [11,12], e.g., using SimVascular [13]", p.2) as background, not as a method used/tested in this paper's own pipeline.

## THREAT assessment

**(1) BC tuning compensating for/masking geometry error; meaning of "target reachability"; what is said about anatomical error there.**
"Target reachability" in this paper means whether a clinical measurement (a catheter pressure, a flow split) is *achievable at all* by any setting of the boundary-condition parameters, given a fixed (possibly imperfect) anatomy — i.e., a parameter-identifiability / model-adequacy concept, not a validation-quality concept. Verbatim: "anatomies affected by vascular lesions where segmentation influences the reachability of pressure or flow split targets. In both cases, boundary conditions cannot be tuned in isolation" (Abstract, p.1); and most explicitly in the Conclusion: "the pressure measured with a catheter is not reachable with boundary condition tuning due to imperfections in the segmented anatomy. This approach holds the potential to instead estimate necessary changes in local anatomical features (e.g. diameter) that would lead to the desired pressures or flow splits" (p.24). The paper's stated response to anatomical/segmentation error is the *opposite* of masking: when BC tuning cannot reach the clinical target, the paper proposes to jointly estimate the anatomy itself (i.e., surface geometry corrections) so the mismatch is exposed and attributed to anatomy, not silently absorbed by the BC parameters. There is no statement anywhere that BC tuning "compensates for," "absorbs," or hides geometric/topological error while the model still appears well validated — the framing is the reverse: unreachable targets are treated as a *signal* of anatomical inaccuracy to be jointly corrected, not a discrepancy to be hidden.

**(2) Ranking error types by effect on a clinical decision (e.g., FFR 0.80 reclassification).**
Not present. The word "FFR" does not occur anywhere in the paper (confirmed by full-text search), there is no binary clinical-decision threshold, and no ranking of geometry-error types by their differential effect on any decision. All evaluation is BC-posterior accuracy and forward-simulated pressure/flow-trace agreement with simulator ground truth (Figs. 11–16, 19).

**(3) Real, measured segmentation disagreement vs. researcher-set stenosis changes.**
Only researcher-set stenosis changes. Stenosis severities and locations are explicitly parameterized/constructed by the authors ("we create a set of left and right iliac artery stenosis models, and encode the deformation from a point cloud representation of their lumen surface," p.3; six named locations A–F with author-assigned severities, e.g. p.17-18). No Dice, Hausdorff distance, Betti-number, clDice, inter-observer, inter-rater, inter-segmenter, or annotator-disagreement terminology occurs anywhere in the full text (confirmed by grep). There is no real, measured segmentation-disagreement data of any kind.

**Verdict: METHOD**

**Justification:** FalconBC is a boundary-condition-tuning method paper (conditional flow matching for amortized BC/inflow/anatomy-embedding inference) that never touches any of the three THREAT criteria for T6. It uses only researcher-parameterized synthetic stenosis geometries and a single reused coronary geometry with perturbed resistances — never real, measured inter-segmenter or inter-observer disagreement (Q-A/Q3 fails: SYNTHETIC only, zero hits for Dice/Hausdorff/Betti/observer/annotator anywhere in the text). It reports no FFR value, no 0.80 threshold, and no decision-level reclassification or error-type ranking of any kind (Q-B/Q2 fails: "FFR" occurs zero times). Its central "target reachability" concept is the mirror image of T6's headline hypothesis: when the anatomy is imprecise, the paper treats an unreachable clinical target as evidence to trigger *joint re-estimation of the anatomy itself* ("the pressure measured with a catheter is not reachable with boundary condition tuning due to imperfections in the segmented anatomy... estimate necessary changes in local anatomical features," p.24) rather than claiming or demonstrating that BC tuning can silently absorb, mask, or compensate for geometric/topological error while the model still looks well-validated (Q1 fails — no absorption/masking claim; the paper's incentive structure is to expose the mismatch, not hide it). The paper is therefore relevant to T6 only as a METHOD source (its point-cloud anatomy-embedding and CFM joint-estimation machinery is reusable, and its "reachability" framing is a useful contrast/citation for T6's introduction) and does not pre-empt or threaten any of T6's three novelty axes (real-disagreement-derived error ranking, FFR-decision-flip ranking by error type, BC-tuning-absorbs-topological-error). No Gate N1 hit.
