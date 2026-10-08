## Contract Paraphrase

D1 (methodology_rigor, mandatory, owned by methodology): from a methods standpoint, the simulation design must be able to isolate the factor it claims to isolate. For a controlled in silico hemodynamics study this means a stated model hierarchy with its validity range, explicit and reproducible perturbation and calibration procedures, verification evidence (discretisation, solver tolerance, cross-model agreement), outcome definitions and thresholds fixed in advance, paired statistics appropriate to the design with uncertainty intervals and multiplicity control, and enough parameter, cohort and code detail for an independent group to rerun the pipeline.

D2 (domain_accuracy, mandatory, owned by domain): claims must agree with current coronary physiology and CT-FFR evidence, prior work must be represented correctly, and domain terms and reported results must be free of factual error. I do not score this dimension, but I will flag methodological choices whose domain basis appears misstated so the domain reviewer can weigh them.

D3 (argumentative_coherence, mandatory, owned by the devil's advocate, methodology eligible): the central thesis must follow from the evidence actually generated. From my side this means the inferential chain from simulated contrasts to conclusions holds: effect sizes exceed the numerical noise floor, conclusions stay within the tested parameter space and model fidelity, and no claim relies on a comparison the design did not perform.

D4 (cross_disciplinary_relevance, high, owned by perspective): framing, definitions and implications must be accessible to adjacent fields such as imaging, informatics and clinical cardiology, and interdisciplinary claims must be substantiated. Outside my scoring remit.

D5 (writing_and_structure, normal, owned by eic): organisation, clarity, figure and table quality, and venue conventions. Outside my scoring remit, though I will note where unclear methods exposition blocks reproduction.

D6 (venue_fit_and_contribution, mandatory, owned by eic): the work must fit the configured venue and make an original, significant contribution for its readers. Outside my scoring remit.

## Scoring Plan

### D1: methodology_rigor
dimension_id: D1
what_to_look_for: Stated governing equations and loss terms of any reduced-order model with its validity range and a 3D verification twin (mesh independence on pressure-ratio outcomes, solver tolerances, reported agreement metric); fully specified perturbation operator and calibration protocols with fitted parameters, targets and stopping rules; a priori definitions of each outcome, residual and pass threshold; cohort or geometry inclusion rules including any stratification band and its rationale; paired tests matched to the design (exact McNemar or sign tests for binary reclassification, Wilcoxon for continuous paired differences) with Holm or equivalent correction and Wilson or bootstrap intervals; an estimated numerical noise floor; registration timing versus analysis; and parameter tables plus code or data availability sufficient to rerun.
what_triggers_block: Any one of: no mesh or solver convergence evidence for the 3D reference while it anchors conclusions; reduced-order model used outside its stated validity range (e.g. severe or tandem stenoses, steady hyperemia assumed where transient effects matter) without a sensitivity check; outcome thresholds or calibration targets chosen after seeing results without disclosure; unpaired tests applied to paired designs or multiple endpoints tested without multiplicity control; reported effects smaller than the numerical noise floor yet interpreted as real; cohort selection rule that mechanically inflates reclassification rates near the decision cut-off without that bias being quantified.
what_triggers_warn: Methods are sound in principle but incompletely reported: missing boundary-condition parameter values, bed-law exponents or calibration tolerances; confidence intervals given for some but not all headline proportions; noise floor stated but not derived; single-mesh or single-solver verification without a cross-check; pre-registration claimed without a timestamp or a deviations table; code available only on request with no parameter tables to compensate.
what_triggers_fatal: The design cannot isolate the claimed causal factor: segmentation perturbation and boundary-condition calibration are confounded so their contributions cannot be separated, the reference solution against which errors are measured is itself unverified or derived from the same model being tested (circular validation), or headline results cannot be reproduced from the reported inputs even in principle.

### D3: argumentative_coherence
dimension_id: D3
what_to_look_for: Whether each conclusion maps to a specific simulated contrast and statistic; whether generalisation claims (to clinical CT-FFR, other vendors, other anatomies or patient populations) stay within the tested geometry set, perturbation magnitudes and model fidelity; whether any claim that calibration masks or corrects error is supported by a contrast that varies calibration with error held fixed; whether limitations stated in the methods are respected in the discussion and abstract.
what_triggers_block: A headline conclusion rests on a contrast the design did not run, or extrapolates from a synthetic or idealised cohort to clinical diagnostic performance without bridging evidence; or the abstract states a stronger or differently directed effect than the reported statistics support.
what_triggers_warn: Conclusions are directionally supported but overstated in wording (causal language for associational sensitivity results, "robust" without a robustness analysis), or a secondary claim lacks a corresponding statistic while the primary argument remains intact.
what_triggers_fatal: The central thesis is contradicted by the study's own reported results, or the argument is circular in that the calibration step guarantees the conclusion it is then used to demonstrate.

[CONTRACT-ACKNOWLEDGED]
