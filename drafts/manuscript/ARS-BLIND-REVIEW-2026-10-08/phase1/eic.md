## Contract Paraphrase

D1 (methodology_rigor, mandatory, owned by the methodology reviewer): the study design, data handling, statistical reporting and reproducibility provisions must clear the peer-review bar of the field. From an editorial standpoint this is the dimension that determines whether the reported numbers can be trusted at all; I do not score it, but I will weigh the methodology reviewer's verdict when judging whether the claimed contribution is real.

D2 (domain_accuracy, mandatory, owned by the domain reviewer): claims must agree with current domain evidence, prior work must be represented correctly, and domain terminology and results must be free of factual error. Editorially, misrepresentation of the prior literature also undermines any novelty claim, so this verdict feeds my contribution judgement without my scoring it.

D3 (argumentative_coherence, mandatory, scored by the devil's advocate and methodology reviewers): the central thesis must be internally consistent, the evidence must support the claims, and no fallacy may undercut the main argument. I treat an incoherent argument as a signal that the headline contribution may not survive review, but the score belongs to the eligible roles.

D4 (cross_disciplinary_relevance, high, owned by the perspective reviewer): framing, definitions and implications must be accessible to readers in adjacent fields, and interdisciplinary claims must be substantiated. For an informatics journal this bears on whether non-specialist readers can use the work, which I consider alongside venue fit without scoring it.

D5 (writing_and_structure, normal, owned by me): organisation, clarity of exposition, figure and table quality, and adherence to the venue's conventions. I score this against IEEE journal norms for length, structure, figure legibility, reference style and the reporting elements the venue expects.

D6 (venue_fit_and_contribution, mandatory, owned by me): the manuscript must fit the configured venue and make an original, significant contribution for that venue's readership. I score this by asking whether the work belongs in a biomedical and health informatics journal rather than a pure biomechanics, image-analysis or numerical-methods journal, and whether its advance over the existing CT-FFR uncertainty literature is both new and consequential.

## Scoring Plan

### D5: writing_and_structure
dimension_id: D5
what_to_look_for: IEEE-style organisation (abstract with quantitative results, introduction ending in explicit contributions, methods sufficient to reproduce, results separated from discussion, limitations, conclusion); length within the venue page budget with overlength justified; every figure and table cited in order, legible at single-column print size, with units, axis labels, colour-blind-safe palettes and self-contained captions; consistent symbols and abbreviations defined at first use; numbered IEEE reference style; data and code availability statement present.
what_triggers_block: The manuscript cannot be followed or checked as presented: methods or results sections are missing or merged so that the reported outcomes cannot be traced to a described procedure, key figures or tables are uncited, unreadable or mislabelled such that a headline number cannot be located, or the length exceeds the venue limit so far that a structural cut is required before review.
what_triggers_warn: Exposition is followable but needs editing: modest overlength, redundant or overlong sections, inconsistent notation or undefined abbreviations, captions that are not self-contained, figures cited out of order or with missing units, non-IEEE reference formatting, or a missing or vague data and code availability statement.

### D6: venue_fit_and_contribution
dimension_id: D6
what_to_look_for: An explicit statement of the health-informatics contribution (for example a decision-relevant uncertainty quantity, a reproducible pipeline, a benchmark, an open dataset or code release, or guidance usable by clinical or software developers) beyond a hemodynamic finding alone; positioning against recent CT-FFR, segmentation-uncertainty and boundary-condition calibration studies in IEEE JBHI, IEEE TMI, Med Image Anal, Ann Biomed Eng and IJNMBE; a clearly stated novelty delta over the closest prior work; clinical framing tied to diagnostic thresholds or decision reclassification; claims scaled to an in silico design without overreach to clinical validity.
what_triggers_block: Fit or contribution is too weak in its current form: the work reads as a pure CFD or numerical-sensitivity study with no stated informatics or decision-support contribution, the novelty over the closest prior CT-FFR uncertainty studies is not articulated or is incremental, or clinical claims are made that an in silico design cannot support, so that substantial reframing or added analysis is needed before the paper suits this readership.
what_triggers_warn: Fit and contribution are present but under-argued: the informatics contribution is implicit rather than stated, positioning omits several directly relevant recent studies, the novelty statement is vague, clinical relevance is asserted without linking effects to decision thresholds, or code and data release is promised without a concrete access route.
what_triggers_fatal: The manuscript is out of scope for a biomedical and health informatics journal or offers no original contribution: its central result duplicates prior published work without a new element, or the subject matter has no health-informatics or clinical decision dimension, so that no revision within this venue could make it suitable and redirection to another journal is the only remedy.

[CONTRACT-ACKNOWLEDGED]
