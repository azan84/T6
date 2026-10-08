## Contract Paraphrase

D1 (methodology_rigor): From an adversarial standpoint, this asks whether the study design could have produced its headline result by construction. I would press on whether design choices, analysis rules and reporting were fixed before results were seen, whether uncertainty is reported alongside point estimates, and whether another group could rerun the pipeline from what is disclosed. This dimension belongs to the methodology reviewer; I note it only where it feeds the coherence of the argument.

D2 (domain_accuracy): This asks whether the paper states the physiology, the computational modelling conventions and the prior literature correctly. A skeptic would check that cited findings are not stretched beyond what their sources showed and that terms such as validation, calibration and agreement carry their accepted meanings. The domain reviewer owns it.

D3 (argumentative_coherence): This is the dimension I own. It asks whether the central thesis survives an attempt to break it: whether every major conclusion follows from the evidence actually generated, whether alternative explanations are excluded rather than ignored, whether the claimed mechanism is shown rather than assumed, and whether the scope of the conclusions matches the scope of the experiments. Overreach, circularity and selective framing all fail here.

D4 (cross_disciplinary_relevance): This asks whether readers outside the core subfield, such as imaging-informatics or clinical readers, can follow the definitions and act on the implications, and whether claims made about those adjacent fields are supported rather than asserted. The perspective reviewer owns it.

D5 (writing_and_structure): This asks whether the manuscript is organised, readable and compliant with venue conventions, including figure and table quality. The editor role owns it; an adversarial reader cares only where unclear exposition hides a gap in the argument.

D6 (venue_fit_and_contribution): This asks whether the work belongs in the configured venue and is new and significant for its readers, rather than a restatement of known sensitivity results. The editor role owns it.

## Scoring Plan

### D3: argumentative_coherence
dimension_id: D3
what_to_look_for: Trace each headline conclusion back to a specific result and test it against the strongest rival explanation; check whether the claimed failure mode is demonstrated by a design that could have shown its absence, whether effect sizes depend on error magnitudes or lesion geometries chosen by the authors, whether a single-parameter global calibration is asked to carry inferences about patient-specific physiology, whether reduced-order findings are generalised to full three-dimensional or clinical settings on thin corroboration, and whether abstract, discussion and conclusion claim no more than the results table supports.
what_triggers_block: A central conclusion is stated more strongly than the evidence allows in a way that changes the paper's message, for example a general claim about clinical or 3D-model behaviour resting on a single corroborating case or on author-chosen perturbation sizes without a sensitivity sweep, or a key rival explanation (model-form error, calibration target choice, lesion idealisation) is acknowledged but never tested or bounded, so the argument has a repairable but material gap.
what_triggers_warn: The core argument holds but individual statements overreach locally, such as hedged results restated as unqualified facts in the abstract or conclusion, limitations listed without saying which conclusions they weaken, or a secondary claim supported by descriptive patterns rather than the pre-specified analysis.
what_triggers_fatal: The central thesis is circular or self-contradictory, for instance the error it reports is guaranteed by the way the perturbation or calibration was defined so the experiment could not have returned a negative result, or the paper's own reported numbers contradict its primary conclusion, such that no revision short of a new study design could rescue the argument.

[CONTRACT-ACKNOWLEDGED]
