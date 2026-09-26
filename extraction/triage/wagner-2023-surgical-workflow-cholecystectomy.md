---
source_pdf_path: Resources/1-s2.0-S1361841523000312-main.pdf
slug: wagner-2023-surgical-workflow-cholecystectomy
ledger_id: C011
ledger_status: TRIAGED
---

# wagner-2023-surgical-workflow-cholecystectomy

## Bibliographic
- Title: Comparative validation of machine learning algorithms for surgical workflow and skill analysis with the HeiChole benchmark
- First author / authors: Martin Wagner, Beat-Peter Müller-Stich, Anna Kisilenko
- Year: 2023
- Venue: Medical Image Analysis, vol. 86
- DOI: 10.1016/j.media.2023.102770

## One-line claim
Presents HeiChole benchmark dataset (33 laparoscopic cholecystectomy videos from three centers) for validation of machine learning algorithms on surgical workflow recognition, instrument detection, and skill assessment.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT APPLICABLE. Surgical video analysis of laparoscopic cholecystectomy; no vascular geometry or segmentation variability.
- **Q-B decision flip**: NOT APPLICABLE. No diagnostic thresholds or reclassification.
- **Q-C BC tuning**: NOT APPLICABLE. No fluid dynamics or boundary conditions.
- **Q-D fidelity / quantity**: NOT APPLICABLE. Surgical workflow recognition (phases, instruments, actions), not CFD or hemodynamics.
- **Q-E data**: Multicenter cohort: 33 laparoscopic cholecystectomy videos (22 h total) from three surgical centers (Heidelberg, Salem, GRN-hospital Sinsheim). Labels include surgical phases, actions, instruments. No invasive ground truth or hemodynamic outcomes.
- **Q-F meshing**: NOT APPLICABLE. Surgical video analysis, no geometry processing or meshing.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Benchmark for machine learning on laparoscopic surgical workflow recognition; entirely outside cardiovascular imaging and CFD domains.
- verdict: LIGHT
- revisit-if: Paper demonstrates multi-task learning on video; cardio-vascular CFD might use similar approaches, but content is surgical, not hemodynamic.

## Ideation opening (CFD + imaging)
- None stated. Focus is laparoscopic cholecystectomy workflow recognition; no CFD or cardiovascular hemodynamics mentioned.
