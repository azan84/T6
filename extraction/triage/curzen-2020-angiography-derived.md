---
source_pdf_path: Resources/icr-15-e06.pdf
slug: curzen-2020-angiography-derived
ledger_status: TRIAGED
---

# curzen-2020-angiography-derived

## Bibliographic
- Title: Coronary Physiology Derived from Invasive Angiography: Will it be a Game Changer?
- First author / authors (first 3 + et al.): Nick Curzen, Lavinia Gabara, Jonathan Hinton
- Year: 2020
- Venue: Interventional Cardiology Review
- DOI: 10.15420/icr.2019.25

## One-line claim
Review of angiogram-derived virtual FFR methods (vFFR, QFR, FFRangio) as alternatives to invasive FFR, highlighting computational and physiological challenges.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No measurement of segmentation uncertainty or inter-observer disagreement.
- **Q-B decision flip**: YES. Reports pooled diagnostic accuracy for FFR 0.80 cutoff across 1,842 vessels: AUC 0.84 (95% CI 0.66–0.94), sensitivity 89% (83–94%), specificity 90% (88–92%), but does not report reclassification rates specifically.
- **Q-C BC tuning**: CRITICAL DISCUSSION. Key quote: "vFFR computation was heavily dependent upon the tuning of the boundary condition of the distal vessels – the values used to represent microvascular resistance in an individual case" and "applying a 'one size fits all' approach to tuning the models (i.e. reflecting the microvascular resistance or hyperaemic flow on an individual case basis) results in error in cases where these parameters are different from population-averaged values." Also: "Without adequate physiological 'tuning', these models are little more than a sophisticated QCA, dependent only on stenosis geometry, ignoring the very things that make FFR superior to diagnostic angiography."
- **Q-D fidelity / quantity**: YES. Discusses CFD (Navier-Stokes, vFFR, virtual TIMI frame, QFR) and mathematical approaches; all focus on pressure/FFR, not spatially-resolved fields.
- **Q-E data**: Meta-analysis of 1,842 vessels across multiple studies; no single invasive FFR ground truth cohort specified.
- **Q-F meshing**: CFD models may suffer mesh generation or solver convergence failures; 6–31% attrition for QFR due to vessel suitability, but not explicitly tied to topological robustness.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Directly identifies tuning of boundary conditions (microvascular resistance) as leading source of error in virtual FFR; emphasizes that BC tuning is non-trivial and case-specific.
- verdict: FULL
- revisit-if: Quantitative sensitivity analysis of FFR to BC variation; data on error propagation when geometry is topologically wrong.
