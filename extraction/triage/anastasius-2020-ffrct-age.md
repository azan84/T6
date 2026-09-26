---
source_pdf_path: Resources/1-s2.0-S1934592520304147-main.pdf
slug: anastasius-2020-ffrct-age
ledger_status: TRIAGED
---

# anastasius-2020-ffrct-age

## Bibliographic
- Title: The clinical utility of FFRCT stratified by age
- First author / authors (first 3 + et al.): Malcom Anastasius, Paul Maggiore, Alex Huang et al.
- Year: 2020
- Venue: Journal of Cardiovascular Computed Tomography
- DOI: 10.1016/j.jcct.2020.08.006

## One-line claim
FFRCT demonstrates similar clinical utility and low MACE risk regardless of patient age, with comparable diagnostic performance in older and younger cohorts.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No synthetic or measured segmentation uncertainty studies.
- **Q-B decision flip**: Yes; FFR ≤0.80 defines hemodynamically significant stenosis. FFRCT positivity (≤0.80) observed in 26.7% of <65 year olds and 23.6% of ≥65 year olds with stenosis ≥50%.
- **Q-C BC tuning**: NOT REPORTED. No discussion of boundary condition tuning, optimization, or compensation for geometric error.
- **Q-D fidelity / quantity**: CT-FFR derived from CCTA (0D computational model); no full 3D CFD or WSS/OSI reported.
- **Q-E data**: ADVANCE registry (multicenter, international, real-world). N=4,553 (1,849 <65 years, 2,704 ≥65 years). Private clinical registry; no public access stated. Invasive FFR ground truth present: yes (reference standard mentioned for comparison).
- **Q-F meshing**: NOT REPORTED. No detail on segmentation→surface→volume meshing robustness.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Registry-based clinical validation of existing CT-FFR technology; demonstrates outcome-based evidence but does not address geometric uncertainty, BC tuning, or topological error absorption.
- verdict: LIGHT
- revisit-if: Sub-analysis comparing FFR reclassification across stenosis morphologies or exploring BC-related artifacts.
