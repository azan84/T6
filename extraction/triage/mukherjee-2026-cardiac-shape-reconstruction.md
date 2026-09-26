---
source_pdf_path: Resources/2603.27003v1.pdf
slug: mukherjee-2026-cardiac-shape-reconstruction
ledger_status: TRIAGED
---

# mukherjee-2026-cardiac-shape-reconstruction

## Bibliographic
- Title: AI-enabled cardiac shape reconstruction from routine magnetic resonance imaging
- First author / authors: Tanmay Mukherjee, Neil Gautam, Nikhil Kadivar
- Year: 2026 (preprint dated March 2026)
- Venue: arXiv (physics.med-ph)
- DOI: NOT REPORTED (arXiv:2603.27003v1)

## One-line claim
Presents NeuralMRI, a neural field-based reconstruction framework that recovers 3D cardiac geometries from sparse planar MRI contours, with rigorous validation on biomechanically realistic in-silico phantoms and in vivo murine hearts, enabling improved cardiac shape reconstruction for digital twin applications.

## T6 targeted questions
- **Q-A geometry perturbation**: Uses FE simulations to generate synthetic cardiac shapes with known deformation fields; synthetic perturbation but not focused on segmentation error magnitude or inter-observer disagreement.
- **Q-B decision flip**: Not mentioned; no FFR or diagnostic decision thresholds discussed.
- **Q-C BC tuning**: FE simulations performed with physiologically realistic pressure-volume loading conditions; tuning and re-tuning of FE boundary conditions are NOT explicitly discussed as a means to mask or absorb geometric errors.
- **Q-D fidelity / quantity**: FE biomechanical simulation (3D) with focus on geometry accuracy and mesh quality; not CFD for hemodynamics. No WSS/OSI reported. Discusses mesh element size (0.5 mm minimum, 1 mm internodal distance).
- **Q-E data**: Synthetic FE dataset (rodent biventricular LV/RV), in vivo murine MRI (n=5), human retrospective MRI (n=3); no invasive FFR ground truth or coronary data.
- **Q-F meshing**: Extensive discussion of segmentation→surface→volume meshing using Materialize 3-Matics, adaptive tetrahedral mesh strategy, mesh quality assessment; demonstrates robustness to complex anatomical regions (apex, basal). Not specifically about coronary segmentation error.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Cardiac shape reconstruction and meshing pipeline with rigorous FE validation framework; methodologies and mesh quality assessment directly relevant to T6's geometry-to-CFD pipeline, but applied to whole-heart LV/RV geometry, not coronary arteries or FFR decision outcomes.
- verdict: LIGHT
- revisit-if: T6 needs detailed methodology on geometry reconstruction from sparse imaging, mesh quality control, or FE validation frameworks for cardiac digital twins. Consider upgrading to FULL if mesh robustness to segmentation error is examined.
