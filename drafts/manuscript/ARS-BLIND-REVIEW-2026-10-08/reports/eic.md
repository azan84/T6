contract_role: eic

## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: warn
trigger: "captions that are not self-contained"

### D6: venue_fit_and_contribution
score: warn
trigger: "the informatics contribution is implicit rather than stated"

## Review Body

Journal-fit view (Associate Editor, JBHI, computational and in silico medicine track). The manuscript asks a sharp, decision-level question that is new to the CT-FFR literature: whether boundary-condition tuning to perfusion can hide a segmentation error that changes treatment at FFR 0.80. The design (one error at a time on 150 inserted lesions, three boundary-condition protocols, two bed structures, a 3D case with reduced-order twins) is clean, the claims are restricted to directions that hold in both beds, and the paper is short and readable for a mixed audience. It fits JBHI's computational-medicine and imaging-informatics readership better than a pure biomechanics venue would, because the outcome is a decision and a validation check rather than a pressure field. Length is within the JBHI limit (8 pp + 5 pp supplement against the 14-page limit including supplementary material), and the abstract is at the 250-word limit.

The contribution is, however, framed as a hemodynamic finding rather than an informatics deliverable. JBHI states that it publishes work "where information and communication technologies intersect with health". The reusable pieces here are an error-injection test for CT-FFR pipelines, a pre-tuning perfusion-residual check and a topology check. They appear only as advice in Section IV-C. The code is available on request only, and the detection performance of the proposed checks is never reported. The headline concealment message is also narrower than the data. Under tuning, the taper (a caliber error) is concealed more often in the leaky bed than either topological error, and without tuning (Protocol A) topological errors pass while wrong at least as often as with it. As a result, the abstract's remedy ("a check of the segmentation's branching structure") does not cover everything the tables show. None of this is fatal. Together these points make D6 a warn: fit and contribution are present but under-argued. D5 is a warn for figure and table presentation issues that a reader needs fixed to check the headline numbers.

### S1: Decision-level outcome benchmarked against measurement noise
The paper judges segmentation error by its effect on the 0.80 decision and compares every flip rate with a repeat-invasive-FFR floor and a simulated physiological floor. This turns a sensitivity study into a clinically interpretable one and is the paper's main conceptual advance over continuous-sensitivity work.
**Evidence Anchor**: text: Section I "segmentation error is judged by whether it changes the treatment decision at 0.80, not by a continuous sensitivity"

### S2: Controlled paired ablation with claims restricted to cross-bed agreement
The same corrupted anatomy is solved under all three protocols with paired exact tests. Findings are claimed only where both bed structures agree, which is a disciplined guard against model-structure artefacts.
**Evidence Anchor**: text: Section II-F "a finding is claimed only where its direction agrees in both"

### S3: Transparent exclusion accounting
Every excluded model is listed by cell and reason, so the varying denominators in Table I can be traced.
**Evidence Anchor**: table: Table S1 — exclusion counts by bed, error and protocol (e.g., 33 discrete and 47 leaky T1 models undefined under Protocol C)

### S4: 3D corroboration with reduced-order twins
The 3D case reproduces the mechanism (ΔFFR +0.074 under fixed resistances, −0.0007 under prescribed flows), and twins on the meshed radius separate model fidelity from radius definition.
**Evidence Anchor**: figure: Fig. 5 (e), (f) — 3D cross-section markers against reduced-order twin lines under the two outlet conditions

### S5: Accessible exposition and candid scoping
Technical terms (lumen, boundary conditions, microvascular bed, DSC, HD95) are defined at first use for non-CFD readers, and the practical steps are explicitly labelled as not validated decision rules.
**Evidence Anchor**: text: Section IV-C "These steps follow from the results but are not validated decision rules."

### W1: Concealment is neither specific to topological errors nor to tuning, but the abstract and conclusion present it as both
**Problem**: Table I shows that under Protocol C in the leaky bed the taper (a caliber error) passes while materially wrong in 24% of models. That is higher than T1 (11%) or T2 (6%) under the same protocol. Under Protocol A, without any tuning, topological models in the leaky bed pass while wrong in 20% (Table S3), compared with 8% under Protocol C. The abstract and conclusion nonetheless frame concealment as a property of tuning applied to topological errors, and they recommend a branching-structure check as the remedy. That check would not catch the caliber concealment the authors themselves report in Section III-B.
**Why it matters**: The take-home message and the recommended pipeline check are what JBHI readers will act on, and as written they are incomplete.
**Suggestion**: Restate the abstract and conclusion so that concealment is reported for all error types and both protocols, including the 24% taper result and the Protocol A rates. Then state which check detects which error class.
**Evidence Anchor**: table: Table I — T4 under Protocol C, leaky bed, passes and wrong 24 (18–31) against T1 C 11 (6–21) and T2 C 6 (3–12)
**Severity**: Major
**Confidence**: 4 — read directly from Table I and Table S3; editorial judgement of abstract–results alignment

### W2: Headline flip rates depend on the stratified cohort design but are presented without that qualification
**Problem**: Instances were sampled uniformly across six baseline-FFR bands from 0.65 to 0.95, and Fig. 2 shows flips concentrated in the bands next to 0.80. The abstract figures ("32–33% of models", "6–10%", "8–19%") therefore depend on this sampling and are not rates expected in a clinical CT-FFR population. The supplement confirms the sensitivity: changing demand moves the clean FFR distribution and, with it, the flip rates (Table S4).
**Why it matters**: Clinical readers will read the percentages as risk estimates. The ratio between topological and caliber errors is the more robust quantity, and it is under-emphasised.
**Suggestion**: Label the abstract percentages as conditional on the band-stratified design. Report per-band rates (Fig. 2 with n) and, if possible, reweight to a published clinical distribution of FFR or CT-FFR values. Lead with the topological/caliber ratio.
**Evidence Anchor**: text: Section II-A "we drew 25 in each of six 0.05-wide bands of baseline FFR"
**Severity**: Major
**Confidence**: 4 — standard reading of stratified-sample prevalence; supported by Fig. 2 and Table S4

### W3: The practical significance of topological errors is not linked to how often real segmentation methods produce them
**Problem**: T1 deletes the largest distal side branch and T2 truncates 25 mm beyond the lesion. By the authors' own statement these are design choices with no measured magnitude, so the paper establishes conditional risk (if this error occurs) but not expected risk. ImageCAS-X, which the authors already use, is a segmentation benchmark. Counting T1- and T2-type events in the outputs of one or two benchmark methods on the same 160-scan test split would connect the ablation to practice.
**Why it matters**: For an informatics venue, the bridge from a segmentation-algorithm output to a decision-level consequence is the main contribution a reader would expect. Without it, the claim that decision risk "lies mainly in the branching structure" is a statement about the chosen magnitudes.
**Suggestion**: Report the frequency of missed distal side branches and early vessel terminations in at least one current method's output on the ImageCAS-X test split, or cite published rates, and relate them to the T1 and T2 definitions. Otherwise, qualify the Discussion's first finding.
**Evidence Anchor**: text: Section II-C "T1 and T2 have no measured magnitude and are design choices."
**Severity**: Major
**Confidence**: 4 — editorial assessment of significance; the dataset and benchmark are named in the manuscript

### W4: The proposed checks are recommended without any measure of how well they detect errors
**Problem**: Section IV-C recommends that users "record the mismatch before tuning, because a large mismatch marked a missing branch". The paper reports the residual's median shift (0.36 to 0.16 discrete), but it does not report how well the pre-tuning residual detects T1 or T2 against clean or caliber-error models. No sensitivity, specificity, ROC/AUC or threshold is given. This detection performance is the informatics deliverable the paper implies, and the data to compute it already exist for every instance.
**Why it matters**: Without operating characteristics, the "further checks a computed-FFR pipeline needs" remain advice rather than a decision-support result. With them, the contribution would be squarely within JBHI's scope.
**Suggestion**: For each bed, report the discrimination of the pre-tuning (Protocol B) perfusion residual for topological error, both against correct anatomy under noise (using the simulated-floor draws) and against caliber error, with a threshold and its sensitivity and specificity. State the contribution in the Introduction as a reusable pipeline test plus a validated pre-tuning check.
**Evidence Anchor**: absence: Results III-B and Discussion IV-C — expected detection performance (sensitivity, specificity or AUC) of the pre-tuning perfusion residual for topological error; checked Abstract, Sections III-A to III-D, IV-A to IV-D, Table I, Fig. 3, Supplementary S3–S5
**Severity**: Major
**Confidence**: 4 — the required quantities are computable from the reported design; judgement of venue expectations

### W5: Code, error generators and the pre-registered cohort list are available only on request
**Problem**: The paper proposes that developers "apply the same test to a pipeline", and it states that the cohort list was hashed before the ablation. The hash value, any registration record and the code are not public, and the supplement names modules (error_types.py, ablation.py, zerod_ffr.py) that readers cannot obtain.
**Why it matters**: The reusable test is the paper's main informatics value. An on-request route gives no concrete access, and the pre-registration claim cannot be verified.
**Suggestion**: Deposit the code, error generators, frozen cohort list and per-instance results in a public archive with a DOI (for example, Zenodo or a code repository) and cite it in the Data and Code Availability section. Report the cohort-list hash, or link a time-stamped registration.
**Evidence Anchor**: text: Data and Code Availability "The code and the frozen cohort list are available from the corresponding author on request."
**Severity**: Major
**Confidence**: 5 — direct reading of the availability statement and Section II-F

### W6: Positioning omits segmentation-uncertainty and topology-aware work from the imaging-informatics literature
**Problem**: The prior work cited is mostly from CFD and physiology. It does not engage studies that propagate learned segmentation uncertainty into coronary hemodynamics (for example, dropout-network geometric uncertainty for coronary simulations in CMAME, 2021). It also gives a single sentence to topology-aware segmentation (clDice) and none to coronary topology or connectivity metrics in the JBHI, TMI or MedIA literature that readers of this journal will know.
**Why it matters**: The novelty claim (decision-level and topological rather than continuous and caliber-based) is credible, but JBHI readers need it placed against the segmentation-side literature that would act on it.
**Suggestion**: Add a short paragraph in Section I or IV-B covering learned segmentation-uncertainty propagation to CT-FFR and topology or connectivity metrics for coronary trees, and state the delta explicitly.
**Evidence Anchor**: absence: Introduction and Discussion IV-B — expected positioning against segmentation-uncertainty propagation and coronary topology-metric studies; checked Sections I, IV-B, IV-C and references [1]–[33]
**Severity**: Minor
**Confidence**: 3 — adjacent-field knowledge of the imaging-informatics literature; specific titles not exhaustively verified

### W7: Reference [9] does not support the coronary statement it is attached to
**Problem**: Reference [9] (pulmonary-valve fluid–structure interaction) is cited, together with [8], for the claim that coronary microvascular resistance is increasingly tuned to measured perfusion or flow splits. It does not address coronary outlet tuning.
**Suggestion**: Replace it with coronary flow-split or perfusion-tuning studies, or delete it.
**Evidence Anchor**: text: Section I "measured flow splits [8], [9]"
**Severity**: Minor
**Confidence**: 4 — reference title and venue read from the reference list

### W8: Table I does not show the denominators of the "Passes and wrong" column, and its footnote conflicts with the n column
**Problem**: The n column gives T2 under Protocol B in the discrete bed as 96 and T2 under Protocols A and B in the leaky bed as 147 and 149. The footnote says the pass-and-wrong denominators for these cells are 60 and 100. A reader cannot tell which n each percentage uses without the footnote, and the caption is not self-contained.
**Suggestion**: Add a separate n column for models with a defined residual, or give the percentages as counts (k/n).
**Evidence Anchor**: table: Table I — T2 rows, n column (96; 147, 149) against footnote denominators (n = 60; n = 100)
**Severity**: Minor
**Confidence**: 5 — direct reading of Table I

### W9: Fig. 2 plots per-band flip rates without per-band counts
**Problem**: Bands with as few as three models are plotted, and several points sit at 100% (for example, discrete T1 and T2 under Protocol A). Without n or intervals per point, the curves suggest more certainty than they carry.
**Suggestion**: Annotate n per band, or add Wilson intervals as error bars, and state the minimum band size in the caption.
**Evidence Anchor**: figure: Fig. 2 — discrete-bed T1 and T2 panels, points at 100% flip with no per-band n or interval
**Severity**: Minor
**Confidence**: 4 — visual inspection of the page image

### W10: Fig. 5 uses a rainbow colour map and red/green contrast in the caption
**Problem**: Panels (a)–(c) use a jet-type colour map, and the caption tells readers to distinguish the lesion and the missed-branch effect by "red" and "green". This combination is not colour-blind safe, and rainbow maps distort perceived pressure gradients. The axis label p/Pa also reads as "pressure in pascals" rather than p/P_a.
**Suggestion**: Use a perceptually uniform sequential map (for example, viridis or cividis), describe the regions by value rather than colour, and label the axis "p / P_a" or "Pressure / aortic pressure".
**Evidence Anchor**: figure: Fig. 5 (a)–(c) colour bar and (e)–(f) vertical-axis label p/Pa
**Severity**: Minor
**Confidence**: 4 — visual inspection of the page image against IEEE figure-accessibility practice

### W11: The main text does not say that the pre-set 3D mesh acceptance criterion was missed
**Problem**: Section III-D reports the throat-refinement changes (0.0019 and 0.0021) and that a regenerated mesh reproduced the baseline. Only the supplement states that these changes exceeded the pre-specified acceptance criterion (5.5 × 10⁻⁴) and that one refinement missed the residual limit.
**Suggestion**: Add one sentence to Section III-D saying that the pre-specified criterion was not met and that the deviation is about 0.2% of FFR against an effect of 0.074.
**Evidence Anchor**: text: Section III-D "a regenerated mesh at 25 µm reproduced the baseline value"
**Severity**: Minor
**Confidence**: 4 — comparison of main text with Supplementary S6

### W12: The abstract and conclusion do not state that tuned-model results for topological errors describe essentially the left coronary tree
**Problem**: Protocol C was undefined for most right coronary instances with a topological error. The Limitations section therefore restricts these results to the left tree, but the abstract's "8–19% of tuned models" and the conclusion carry no such qualifier.
**Suggestion**: Add "left coronary" or "where tuning was defined" to the concealment sentence in the abstract and conclusion.
**Evidence Anchor**: text: Section IV-D "so its results for these errors describe the left coronary tree"
**Severity**: Minor
**Confidence**: 4 — direct comparison of Limitations with Abstract and Conclusion
