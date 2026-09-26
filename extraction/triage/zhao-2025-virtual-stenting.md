---
source_pdf_path: Resources/jcdd-12-00373-v2.pdf
slug: zhao-2025-virtual-stenting
ledger_status: TRIAGED
---

# zhao-2025-virtual-stenting

## Bibliographic
- Title: Virtual Stenting Based on Fractional Flow Reserve Derived from Computed Tomography in Predicting Post-Percutaneous Coronary Intervention Functional Outcomes
- First author / authors (first 3 + et al.): Han Zhao, Yanlong Ren, Jiang Li
- Year: 2025
- Venue: Journal of Cardiovascular Development and Diseases
- DOI: 10.3390/jcdd12090373

## One-line claim
Virtual stenting technique using 3D CFD on CCTA to predict post-PCI FFR ≥0.90, with blinded vs. non-blinded stent placement comparison.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Uses clinically available stent sizes/positions but no inter-segmenter disagreement measurement.
- **Q-B decision flip**: YES. Uses post-PCI FFR ≤0.90 (not 0.80) as functional success threshold; reports PPV >83% for both blinded/non-blinded methods vs. ≤50% in prior work.
- **Q-C BC tuning**: PARTIALLY REPORTED. States "A transient three-element Windkessel model... applied to the outlet boundary ΓO, and the resistance and capacitance of each coronary artery branch outlet are distributed according to Murray's law." No statement that BC is re-tuned or re-optimized after virtual stent placement; BC appears fixed from original geometry.
- **Q-D fidelity / quantity**: YES. 3D CFD with hybrid method, unstructured tetrahedral mesh (max 0.5 mm, refined to 0.1 mm near stenosis), over 2 million elements per case. Navier-Stokes equations solved; no WSS or OSI extraction mentioned.
- **Q-E data**: 75 patients (78 vessels), Beijing Anzhen Hospital, 2019-2022; invasive FFR ground truth; pre-PCI CCTA within 60 days.
- **Q-F meshing**: Mesh refinement strategy described (0.1 mm near stenosis for detail); no mention of robustness to topologically broken or poor segmentations.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Virtual stenting algorithm and CFD workflow reusable for T6; hybrid 3D CFD approach with allometric scaling and Murray's law outlet distribution; shows method stability across discovery/validation cohorts.
- verdict: FULL
- revisit-if: BC re-optimization after geometry change; sensitivity analysis of post-stent FFR to outlet BC perturbation; testing on poor or topologically aberrant segmentations.
