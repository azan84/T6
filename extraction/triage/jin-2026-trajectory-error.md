---
source_pdf_path: Resources/A_Modified_Trajectory_Error_Modeling_Method_Integrating_Moving_Object_Velocity_and_Trajectory_Geometry.pdf
slug: jin-2026-trajectory-error
ledger_status: TRIAGED
---

# jin-2026-trajectory-error

## Bibliographic
- Title: A Modified Trajectory Error Modeling Method Integrating Moving Object Velocity and Trajectory Geometry
- First author / authors (first 3 + et al.): Yanmin Jin, Zhixian Luo, Xinyi Zheng et al.
- Year: 2026
- Venue: IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, Vol. 19
- DOI: 10.1109/JSTARS.2025.3646151

## One-line claim
Proposes a modified broad adaptive error ellipse (m-BAEE) model for GPS trajectory uncertainty quantification by integrating geometric features and moving object velocity to construct trajectory error bands more accurately.

## T6 targeted questions
- **Q-A geometry perturbation**: Addresses trajectory geometry uncertainty from measurement and sampling error in GPS data; application is outdoor object tracking, not medical imaging geometry. NOT REPORTED for T6 context.
- **Q-B decision flip**: No diagnostic application or threshold-based classification. NOT REPORTED.
- **Q-C BC tuning**: Not applicable; no CFD or boundary condition modeling. NOT REPORTED.
- **Q-D fidelity / quantity**: Trajectory error modeling for remote sensing; no 3D CFD or hemodynamic simulation. NOT REPORTED.
- **Q-E data**: Trajectory datasets from GPS/remote sensing; no medical imaging or invasive ground truth. NOT REPORTED.
- **Q-F meshing**: Not applicable. NOT REPORTED.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Remote sensing and GPS trajectory error modeling; no application to medical imaging, vascular segmentation, or hemodynamic simulation.
- verdict: LIGHT
- revisit-if: Not applicable; paper's domain (geospatial trajectory uncertainty) has no bearing on T6's coronary artery imaging or digital twin validation.
- possible-other-project: Remote sensing, GPS trajectory analysis, geospatial data uncertainty quantification.
