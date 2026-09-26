---
source_pdf_path: Resources/s00466-022-02206-6.pdf
slug: caforio-2022-3d-1d-coupling
ledger_id: C035
ledger_status: TRIAGED
---

# caforio-2022-3d-1d-coupling

## Bibliographic
- Title: A coupling strategy for a first 3D-1D model of the cardiovascular system to study the effects of pulse wave propagation on cardiac function
- First author / authors: Federica Caforio, Christoph M. Augustin, Jordi Alastruey (et al.)
- Year: 2022
- Venue: Computational Mechanics 70:703–722
- DOI: https://doi.org/10.1007/s00466-022-02206-6

## One-line claim
Develops a stable numerical coupling strategy for 3D cardiac electromechanics to 1D arterial blood flow model, validated on personalized left ventricle models under vascular perturbations (aortic stiffening, stenosis, bifurcations).

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Uses patient-specific LV geometry. Validation includes "variations in the arterial system affecting pulse wave propagation, comprising aortic stiffening, aortic stenosis or bifurcations" but does not test segmentation uncertainty or segmentation-derived geometry perturbation.
- **Q-B decision flip**: NOT REPORTED. Focuses on cardiac mechanics and hemodynamics; no FFR or diagnostic thresholds addressed.
- **Q-C BC tuning**: NOT EXPLICITLY REPORTED. Uses 1D arterial model as distributed vascular BC to replace lumped 0D models. "The parameters in the vascular model are identified and constrained by imaging-based measurements of the heart and blood flow and invasive blood pressure measurements." NOT REPORTED: sensitivity of tuning to geometry changes or compensation for geometric error.
- **Q-D fidelity / quantity**: Coupled 3D cardiac electromechanics + 1D arterial flow (not full 3D CFD of coronaries). Computes pressure and flow fields at heart-aorta interface. NOT REPORTED: WSS/OSI in coronary branches or sensitivity analysis of hemodynamics to geometry.
- **Q-E data**: Personalized LV models from "imaging-based measurements of the heart and blood flow and invasive blood pressure measurements." NOT REPORTED: invasive FFR ground truth, cohort size, or dataset name.
- **Q-F meshing**: NOT REPORTED. Finite element formulation described but no segmentation robustness or handling of poor/topologically-incorrect geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Develops stable multidimensional coupling strategy (3D cardiac EM to 1D arterial flow) for systemic vascular-cardiac interaction, applicable to hemodynamic modeling but focused on left ventricle, not coronary stenosis hemodynamics.
- verdict: LIGHT
- revisit-if: Full paper applies 3D-1D coupling to coronary artery hemodynamics with segmentation uncertainty quantification, or demonstrates FFR sensitivity to BC tuning under geometry perturbation.

## Ideation opening (CFD + imaging)
- Paper suggests that "effects related to pulse wave transmission" and "distributed properties, e.g., vessel branching, tapering, stenoses" require 1D or 3D coupling beyond lumped 0D models, implying that imaging-derived geometry alone is insufficient; distributed vascular BC representation adds clinical value, but this is demonstrated on systemic aorta, not coronary disease.
