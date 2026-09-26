---
source_pdf_path: Resources/Remote_Respiratory_and_Cardiac_Motion_Patterns_Separation_With_4D_Imaging_Radars.pdf
slug: li-2023-radar-motion-separation
ledger_id: C028
ledger_status: TRIAGED
---

# li-2023-radar-motion-separation

## Bibliographic
- Title: Remote Respiratory and Cardiac Motion Patterns Separation With 4D Imaging Radars
- First author / authors (first 3 + et al.): Li Z, Jin T, Hu X
- Year: 2023
- Venue: IEEE Journal of Biomedical and Health Informatics
- DOI: 10.1109/JBHI.2022.3171554

## One-line claim
A variational mode separation (VMS) algorithm separates respiratory and cardiac motion signals from 4D imaging radar data for noncontact remote physiological monitoring with root mean square errors of 0.13 breaths/min and 1.7 beats/min.

## T6 targeted questions
- **Q-A geometry perturbation**: Not applicable. Domain is noncontact remote sensing and signal detection, not medical imaging-based segmentation or geometry assessment. NOT REPORTED.
- **Q-B decision flip**: Not applicable. No diagnostic decision-making framework, no clinical thresholds. NOT REPORTED.
- **Q-C BC tuning**: Not applicable. No hemodynamic modeling, no boundary condition framework. NOT REPORTED.
- **Q-D fidelity / quantity**: Not applicable. No CFD or hemodynamic modeling. Signal processing for respiratory and cardiac motion detection from radar; no spatially-resolved flow fields or WSS.
- **Q-E data**: Radar remote sensing data from real scenes. Multiple persons can be localized and monitored. No patient cohort data, no clinical measurements, no invasive gold standard.
- **Q-F meshing**: Not applicable. Domain is radar signal processing, not 3D mesh generation.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Paper focuses on noncontact physiological signal detection via radar-based remote sensing; no connection to coronary imaging, FFR-CT, hemodynamic modeling, or geometry sensitivity analysis.
- verdict: LIGHT (metadata only)
- revisit-if: None; this document belongs to radar-based vital signs monitoring, not cardiovascular CFD or imaging-based diagnosis.

## Ideation opening (CFD + imaging)
None stated. Paper addresses signal separation for remote health monitoring, not imaging-based anatomy or hemodynamic simulation.
