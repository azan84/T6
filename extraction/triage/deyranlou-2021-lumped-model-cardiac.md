---
source_pdf_path: Resources/2021.05.02.442367v1.full.pdf
slug: deyranlou-2021-lumped-model-cardiac
ledger_id: C014
ledger_status: TRIAGED
---

# deyranlou-2021-lumped-model-cardiac

## Bibliographic
- Title: A Coupled Flow-Thermoregulation Lumped Model to Investigate Cardiac Function
- First author / authors: Amin Deyranlou, Alistair Revell, Amir Keshmiri
- Year: 2021
- Venue: bioRxiv preprint (posted May 3, 2021)
- DOI: https://doi.org/10.1101/2021.05.02.442367

## One-line claim
Methodology paper presenting a coupled zero-dimensional lumped-parameter model for cardiovascular circulation (left/right hearts, systemic and pulmonary circulations with RCL elements) integrated with a two-node thermoregulation model, designed for assessing cardiac function under physiological conditions and as boundary conditions for multiscale modeling.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper develops lumped model methodology for healthy and diseased (atrial fibrillation) conditions but does not address vascular geometry uncertainty or segmentation error.
- **Q-B decision flip**: NOT REPORTED. Focus is on flow, pressure, and temperature outputs over a cardiac cycle; no diagnostic thresholds or reclassification.
- **Q-C BC tuning**: PARTIALLY RELEVANT. Paper builds lumped model with R, C, L elements for arteries, arterioles, capillaries, and veins (RCL compartments for large vessels, RC for venous, R only for microcirculation). States: "lumped models can be employed as boundary conditions in multiscale modelling of physiological flows." However, no explicit discussion of BC tuning protocols, optimization to match measurements, or re-tuning after geometry changes.
- **Q-D fidelity / quantity**: 0-D lumped model only (Windkessel-type circuit with time-varying elastance cardiac chambers). No 3D CFD, no spatially resolved fields (WSS, OSI). Model outputs: flow, pressure, temperature at different compartments.
- **Q-E data**: Proof-of-concept modeling study (no patient cohort). Model parameters (resistances, compliances, elastances) set to nominal physiological values. Paper is developed specifically for investigation of atrial fibrillation on cardiac performance; mentions it "can either be used for assessing cardiac function in different physiological conditions or provide input data for other investigations."
- **Q-F meshing**: NOT APPLICABLE. Zero-dimensional lumped model; no geometry, segmentation, or meshing.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates construction and parameterization of a coupled 0-D hemodynamic model (Windkessel-type with elastic hearts) for cardiac function assessment; relevant as reference for 0-D boundary condition practice and potential multiscale (0D/3D) integration strategies.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity analysis of lumped model outputs to parameter variations, or validation of 0-D predictions against experimental/clinical measurements, or use as BC for 3D CFD with demonstrated impact on 3D solutions.

## Ideation opening (CFD + imaging)
- Paper states lumped models "facilitate the assessment of relevant metrics such as flow, pressure, and temperature at different locations over a large network/domain" and "can be employed as boundary conditions in multiscale modelling of physiological flows." Implies a research direction: How do geometric errors in 3D reconstructed vessel geometry propagate through 0-D BC tuning and then influence downstream 3D CFD predictions? T6 hypothesizes that BC tuning may absorb or mask geometric errors.
