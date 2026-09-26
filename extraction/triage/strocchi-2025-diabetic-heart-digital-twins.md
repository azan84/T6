---
source_pdf_path: Resources/s12933-025-02839-w.pdf
slug: strocchi-2025-diabetic-heart-digital-twins
ledger_id: C039
ledger_status: TRIAGED
---

# strocchi-2025-diabetic-heart-digital-twins

## Bibliographic
- Title: Cardiac digital twins: a tool to investigate the function and treatment of the diabetic heart
- First author / authors: Marina Strocchi, Daniel J. Hammersley, Brian P. Halliday (et al.)
- Year: 2025
- Venue: Cardiovascular Diabetology 24:293
- DOI: https://doi.org/10.1186/s12933-025-02839-w

## One-line claim
Reviews cardiac computational models applied to diabetes and anti-diabetic treatment, covering multi-scale mechanisms from cardiomyocyte metabolism to whole cardiovascular system, with discussion of cardiac digital twins and in-silico trials for treatment optimization.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Review focuses on cardiac models for diabetes pathophysiology, not segmentation uncertainty or geometry perturbation testing.
- **Q-B decision flip**: NOT REPORTED. No FFR or diagnostic thresholds. Focus is on anti-diabetic drug effects on cardiac function and cardiovascular outcome trials.
- **Q-C BC tuning**: NOT EXPLICITLY ADDRESSED. Discusses multi-scale and multiphysics models including "interaction with the circulatory system" but no BC tuning methodology or parameter optimization details for coronary hemodynamics.
- **Q-D fidelity / quantity**: Review covers multi-scale cardiac modeling spanning "myocyte metabolism, electrophysiology, and calcium handling to blood flow and the whole cardiovascular system." Discusses 0D/1D/2D/3D CFD approaches but NOT focused on coronary artery WSS/OSI or stenosis hemodynamics.
- **Q-E data**: Discusses data availability challenges: "Cardiac computational models rely on the availability of high-quality datasets (e.g., imaging, invasive recordings) to be built and validated. However, clinical datasets are often imbalanced." NOT REPORTED: invasive FFR validation or coronary hemodynamics data.
- **Q-F meshing**: NOT REPORTED. No anatomical segmentation, meshing, or geometry robustness details for coronary models.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Reviews cardiac computational modeling for diabetes management, covering multi-scale and multiphysics approaches and digital twins for treatment optimization; not specific to coronary stenosis hemodynamics or FFR prediction.
- verdict: LIGHT
- revisit-if: Review extends to coronary disease-specific CFD or addresses FFR prediction in diabetic patients with coronary disease.

## Ideation opening (CFD + imaging)
- Paper emphasizes multi-scale diabetic remodeling: "Prolonged hyperglycaemia leads to a wide range of changes in the diabetic heart and circulation, from the single protein... to the whole circulatory system scale." Suggests comprehensive imaging + computational integration is necessary for patient-specific diabetes care, but does not specifically address coronary geometry-error cascading to hemodynamic outcomes or FFR decision-making.
