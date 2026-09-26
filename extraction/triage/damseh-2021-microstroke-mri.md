---
source_pdf_path: Resources/s41598-021-93503-2.pdf
slug: damseh-2021-microstroke-mri
ledger_id: C040
ledger_status: TRIAGED
---

# damseh-2021-microstroke-mri

## Bibliographic
- Title: A simulation study investigating potential diffusion-based MRI signatures of microstrokes
- First author / authors: Rafat Damseh, Yuankang Lu, Xuecong Lu (et al.)
- Year: 2021
- Venue: Scientific Reports 11:14229
- DOI: https://doi.org/10.1038/s41598-021-93503-2

## One-line claim
Develops Monte-Carlo MRI simulations of cerebral microvasculature using optical coherence tomography (OCT)-derived vascular geometry and machine-learning-predicted hemodynamic parameters to investigate diffusion-weighted MRI biomarkers of microstrokes.

## T6 targeted questions
- **Q-A geometry perturbation**: Indirect relevance. Uses OCT-derived vascular geometry and simulates radial versus random vessel orientations. "Synthetic capillary beds, randomly- and radially-oriented" compared before and after photothrombosis. NOT explicit geometry perturbation or segmentation uncertainty testing; focus is on architectural reorientation.
- **Q-B decision flip**: NOT REPORTED. No FFR or diagnostic thresholds. Focuses on MRI biomarker detection (φ = 1 − max(R)) for microstroke presence vs. healthy tissue.
- **Q-C BC tuning**: NOT REPORTED. No fluid dynamics simulation or boundary condition tuning. Flow and partial pressure of oxygen (PO2) assigned via random forest regression on geometric features, not CFD-derived.
- **Q-D fidelity / quantity**: NOT 3D CFD hemodynamics. Uses Monte-Carlo MRI simulation combined with machine-learning-predicted flow/PO2 ("random forest model trained on experimental measurements"). No Navier-Stokes equations, no WSS/OSI computation. Focus is on spin diffusion, T2* effects, and advection-diffusion in microvascular networks.
- **Q-E data**: Experimental mice (n=5) with OCT angiography pre- and post-photothrombosis at multiple timepoints (weeks 1-4). NOT REPORTED: invasive hemodynamic measurements or coronary flow/pressure data.
- **Q-F meshing**: Uses segmentation and graph-based modeling from OCT. "Segmentation outputs were then processed with the VascGraph toolbox to produce final graphical models." Converts segmented vessels to graph skeletons with node/edge representation. NOT REPORTED: robustness on poor or topologically-incorrect geometry.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Focuses on MRI biomarker detection of cerebral microstroke vascular architecture; not relevant to coronary CFD hemodynamics, FFR prediction, or stenosis decision-making.
- verdict: LIGHT
- revisit-if: N/A (paper is outside T6's scope of coronary CFD + imaging + FFR).

## Ideation opening (CFD + imaging)
- None specific to T6. Paper demonstrates integration of OCT imaging + computational modeling (MRI simulation + machine learning) for cerebral stroke detection, but does not address coronary hemodynamics, geometry-error cascading to diagnosis, or FFR decision-making. Notes segmentation processing ("Segmentation outputs were then processed with the VascGraph toolbox") but applied to cerebral microvascular architecture, not coronary stenosis.
