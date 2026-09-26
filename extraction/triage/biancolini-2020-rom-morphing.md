---
source_pdf_path: Resources/s12008-020-00694-5.pdf
slug: biancolini-2020-rom-morphing
ledger_status: TRIAGED
---

# biancolini-2020-rom-morphing

## Bibliographic
- Title: Fast interactive CFD evaluation of hemodynamics assisted by RBF mesh morphing and reduced order models: the case of aTAA modelling
- First author / authors: Marco Evangelos Biancolini, Katia Capellini, Emiliano Costa et al.
- Year: 2020
- Venue: International Journal on Interactive Design and Manufacturing (IJIDeM)
- DOI: 10.1007/s12008-020-00694-5

## One-line claim
Demonstrates combined use of radial basis function (RBF) mesh morphing and reduced-order modeling (ROM) to enable fast, interactive CFD hemodynamic evaluation of parametrically deformed aortic geometries in near real-time.

## T6 targeted questions

- **Q-A geometry perturbation**: NOT REPORTED for coronary arteries. Study focuses on ascending thoracic aortic aneurysm (aTAA), not coronary disease. Demonstrates systematic geometric variation via parametric shape morphing (5 shape parameters controlling bulge) but does not examine segmentation uncertainty or inter-observer disagreement.

- **Q-B decision flip**: NOT APPLICABLE. Study is on aortic hemodynamics, not FFR or revascularization decision thresholds.

- **Q-C BC tuning**: NOT ADDRESSED. Study is hemodynamics-focused, not on BC optimization. Does not discuss pressure or resistance tuning.

- **Q-D fidelity / quantity**: Reduced-order modeling (ROM) combined with RBF parametric mesh morphing. ROM built using proper orthogonal decomposition (POD) from CFD snapshots and Kriging interpolation. Full CFD solver (ANSYS Fluent) used for baseline snapshots. Study reports pressure contours but does not focus on FFR, WSS, or OSI.

- **Q-E data**: Synthetic models: statistically averaged healthy and aneurysmatic aortas from patient image data; no clinical FFR data.

- **Q-F meshing**: YES, extensively discussed. RBF morphing technique "enables the implementation of a parametric shape, which is used to build up the ROM framework." States: "Despite the large extent of shape modifications explored, the mesh morphing action allows to preserve a valid mesh with a reasonable increment of the skewness." Discusses: "the meshless property, the preservation of mesh consistency and the low disk usage" as advantages of RBF. Notes: "high performance in handling large models."

## Novelty bearing on T6

- **bucket**: METHOD
- **one-line reason**: Demonstrates RBF mesh morphing and ROM techniques for parametric geometry variation and fast hemodynamic evaluation; applicable methodology for T6's need to test multiple segmentation variants, though developed for aortic (not coronary) application.
- **verdict**: LIGHT
- **revisit-if**: Paper applies ROM+RBF to coronary geometries or uses it to systematically vary segmentation and measure FFR sensitivity.
