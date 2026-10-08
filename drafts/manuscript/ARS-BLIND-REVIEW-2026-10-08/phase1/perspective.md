## Contract Paraphrase

D1 (methodology_rigor): The study design, data handling, statistical reporting and reproducibility affordances must reach the peer-review bar of the field; from a cross-disciplinary standpoint this includes whether an imaging-informatics reader could re-run the error-injection and evaluation pipeline from what is reported.

D2 (domain_accuracy): Claims must agree with current evidence, prior work must be represented correctly, and domain terminology and results must be free of factual error; for an adjacent-field reader this means segmentation and hemodynamics terms are used as each community uses them.

D3 (argumentative_coherence): The central thesis must be internally consistent, with evidence that actually supports each claim and no fallacy that undermines the main argument.

D4 (cross_disciplinary_relevance): Framing, definitions and implications must be accessible to readers in adjacent fields, here primarily medical image segmentation and health-informatics readers rather than CFD specialists, and any claim that crosses disciplines (for example, from simulated geometric error to real segmentation failure modes, or to credibility and regulatory evidence) must be substantiated rather than asserted.

D5 (writing_and_structure): Organisation, clarity of exposition, figure and table quality, and conformance with venue conventions must be adequate for the configured journal.

D6 (venue_fit_and_contribution): The work must fit the configured venue and make an original, significant contribution suited to that venue's readership.

## Scoring Plan

### D4: cross_disciplinary_relevance
dimension_id: D4
what_to_look_for: Whether each injected geometric error type is mapped, with cited evidence, to an observed failure mode of real coronary segmentation methods (e.g. false merges, branch omission, lumen narrowing at calcification, centerline breaks); whether results are expressed in segmentation-QC terms an informatics reader uses (Dice, Hausdorff, clDice, Betti or connectivity errors, centerline overlap) and linked to downstream FFR error; whether CFD and boundary-condition concepts are defined on first use for non-CFD readers; whether implications are actionable for pipeline design (QC thresholds, topology-aware losses, flagging rules); and whether any credibility claims are framed against ASME V&V40 or FDA in silico evidence concepts with stated context of use.
what_triggers_block: The error models are presented as representative of real segmentation failures with no citation, dataset evidence or failure-mode taxonomy supporting that correspondence, so the central informatics implication is unsubstantiated; or credibility or regulatory relevance is claimed without defining a context of use, question of interest or model-risk framing.
what_triggers_warn: The correspondence to real segmentation failures is argued but only partially evidenced or limited to one error class; standard segmentation-QC metrics are absent or not related to FFR error, leaving no practical threshold for imaging readers; or key CFD and boundary-condition terms are left undefined or rely on hemodynamics jargon that an adjacent-field reader cannot follow.

[CONTRACT-ACKNOWLEDGED]
