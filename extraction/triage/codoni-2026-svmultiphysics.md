---
source_pdf_path: Resources/2607.19631v1.pdf
slug: codoni-2026-svmultiphysics
ledger_id: C018
ledger_status: TRIAGED
---

# codoni-2026-svmultiphysics

## Bibliographic
- Title: svMultiPhysics: a finite element–based solver for cardiovascular simulations
- First author / authors: David Codoni, Sujal Dave, David W. Parker, Aaron L. Brown
- Year: 2026
- Venue: arXiv:2607.19631v1
- DOI: NOT REPORTED

## One-line claim
Presents svMultiPhysics, an open-source C++ finite element solver for patient-specific cardiovascular multiphysics simulations including fluid dynamics, solid mechanics, and cardiac electrophysiology with demonstrated applications to abdominal aortic aneurysm and biventricular geometry.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED
- **Q-B decision flip**: NOT REPORTED
- **Q-C BC tuning**: NOT REPORTED (limited). Paper states svMultiPhysics is "part of the SimVascular project, which provides a complete pipeline from medical image segmentation to patient-specific cardiovascular simulation" and references svZeroDSolver for boundary conditions, but does not discuss BC tuning strategies, Windkessel tuning, or sensitivity to geometry changes.
- **Q-D fidelity / quantity**: 3D CFD and FSI (fluid-structure interaction) on patient-specific geometries. Cardiac electrophysiology also demonstrated. States "detailed blood-flow patterns" and hemodynamic prediction capability; no explicit WSS/OSI spatial field extraction reported in extracted text.
- **Q-E data**: Patient-specific AAA (abdominal aortic aneurysm) CFD/FSI simulations and biventricular geometry with congenital heart disease (CHD). N not specified; validation mentioned against "in vitro 4D-flow MRI data" and "in vivo measurements" but no specific cohort size or FFR ground truth reported.
- **Q-F meshing**: NOT REPORTED. No detail on segmentation-to-surface-to-volume mesh generation, mesh quality, or robustness to poor/topologically incorrect geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Open-source CFD solver for cardiovascular applications with patient-specific capabilities; does not address geometry error propagation or BC tuning protocols
- verdict: LIGHT
- revisit-if: Detailed discussion of BC tuning methodology or WSS/OSI sensitivity to geometry perturbations

## Ideation opening
Paper emphasizes that "imaging alone cannot predict how a patient may respond to a proposed intervention" and describes physics-based models to integrate clinical data with governing equations of cardiovascular mechanics, but does not explicitly address segmentation uncertainty or geometry error impact on hemodynamic predictions.
