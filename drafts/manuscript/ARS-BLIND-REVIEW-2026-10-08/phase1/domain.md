## Contract Paraphrase

D1 (methodology_rigor, mandatory, owned by methodology): from a domain standpoint, the study design must be capable of answering a coronary physiology question, meaning that the cases, perturbations, solver settings and statistics are reported fully enough that another CT-FFR group could reproduce the pressure-ratio results. I do not score this dimension, but domain errors in the setup (for example an unphysiological hyperemic flow assumption) feed into it.

D2 (domain_accuracy, mandatory, owned by domain): the claims about coronary hemodynamics, CT-FFR modelling and invasive FFR physiology must agree with current evidence. Prior image-based FFR work must be described correctly, terminology (FFR, CT-FFR, hyperemia, microvascular resistance, territory, lumped-parameter outlet) must be used in its accepted sense, and stated results must be physically and clinically plausible. This is the dimension I score.

D3 (argumentative_coherence, mandatory, owned by the devil's advocate): the central thesis must follow from the evidence presented without internal contradiction or overreach. From a physiology viewpoint, coherence fails when in silico sensitivity findings are presented as if they established clinical diagnostic performance.

D4 (cross_disciplinary_relevance, high): definitions and implications should be readable by imaging, informatics and clinical readers outside computational fluid dynamics, and any claim crossing into segmentation science or clinical decision-making must be substantiated.

D5 (writing_and_structure, normal): organisation, clarity, figure and table quality and adherence to IEEE JBHI conventions. Figures showing pressure fields or FFR distributions should be interpretable by a cardiologist.

D6 (venue_fit_and_contribution, mandatory): the work must suit the JBHI readership and add an original, significant contribution beyond existing CT-FFR sensitivity and uncertainty literature.

## Scoring Plan

### D2: domain_accuracy
dimension_id: D2
what_to_look_for: Physiologically realistic hyperemic demand (total and per-territory coronary flow, resistance reduction relative to rest, myocardial-mass or Murray-type scaling with the exponent stated and justified); correct definition of FFR as distal-to-aortic mean pressure ratio under hyperemia and of territory-based or perfusion-based outlet tuning as used in clinical CT-FFR pipelines; interpretation of the 0.80 threshold that acknowledges the invasive grey zone and test-retest variability (Johnson, Petraco) so that computed shifts are compared against measurement noise of about 0.01 to 0.03; accurate representation of Gamage, Gosling, Fossan, Sankaran and Menon and of HeartFlow-type validation trials; correct handling of side-branch flow steal and diffuse disease; no omitted landmark references on CT-FFR uncertainty, segmentation sensitivity or boundary-condition calibration.
what_triggers_block: A central quantitative claim depends on a physiologically implausible assumption (for example hyperemic flow or microvascular resistance outside reported human ranges, outlet resistances not scaled to territory, or neglect of side-branch outflow) without sensitivity testing, or a key prior study is misrepresented in a way that inflates the novelty or direction of the findings.
what_triggers_warn: Domain content is broadly correct but has fixable gaps, such as FFR changes reported without reference to invasive repeatability or the grey zone, imprecise terminology (CT-FFR, FFR-CT, virtual FFR, QFR used interchangeably), missing citations to one or two established CT-FFR sensitivity or calibration studies, or reclassification rates around 0.80 discussed without stating clinical consequences.
what_triggers_fatal: The work contains a fundamental physiological error that invalidates its conclusions, such as computing FFR under resting rather than hyperemic conditions while claiming hyperemic equivalence, defining FFR incorrectly, or presenting in silico perturbation results as clinical diagnostic accuracy without any invasive or validated reference.

[CONTRACT-ACKNOWLEDGED]
