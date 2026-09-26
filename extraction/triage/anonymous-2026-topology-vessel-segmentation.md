---
source_pdf_path: Resources/ssrn-7194679.pdf
slug: anonymous-2026-topology-vessel-segmentation
ledger_status: TRIAGED
---

# anonymous-2026-topology-vessel-segmentation

## Bibliographic
- Title: GTPM-Seg: Generative Topology Prior Memory for Vessel Segmentation
- First author / authors (first 3 + et al.): Anonymous (preprint)
- Year: 2026
- Venue: SSRN Preprint / Submitted to Elsevier
- DOI: https://ssrn.com/abstract=7194679

## One-line claim
Proposes GTPM-Seg, a deep learning framework for robust vessel segmentation across X-ray angiography, OCTA, and fundus imaging that uses a generative topology prior memory bank to preserve vascular continuity, suppress implausible predictions, and maintain topological correctness under weak contrast and fragmented branches.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT EXPLICITLY REPORTED as synthetic perturbation studies, but extensively evaluates robustness to degraded imaging conditions: "weak contrast, thin tubular structures, complex branching patterns, and frequent topological discontinuities." Tested under "Gaussian noise, uneven illumination, low contrast, boundary blur, motion blur, vessel dropout, branch occlusion" with reported metric degradation. These simulate real segmentation error sources.
- **Q-B decision flip**: NOT REPORTED. No diagnostic threshold or reclassification outcomes; focuses on segmentation accuracy and topology preservation.
- **Q-C BC tuning**: NOT REPORTED. No boundary condition tuning or model parameter calibration to compensate for geometric error.
- **Q-D fidelity / quantity**: NOT REPORTED. Segmentation method only; no CFD, WSS, OSI, or hemodynamic simulation reported.
- **Q-E data**: PARTIAL. Evaluated on "seven X-ray angiography, OCTA, and fundus vessel segmentation datasets" including coronary angiography but specific N and dataset names not explicitly listed in abstract/front matter extraction; does not report ground truth FFR data.
- **Q-F meshing**: STRONG. Explicitly addresses segmentation robustness: "Vessel segmentation remains challenging due to weak contrast, thin tubular structures, complex branching patterns, and frequent topological discontinuities." Reports Dice score, centerline-aware clDice metric, and Betti-number errors (β₀, β₁) to evaluate "topological consistency." Discusses handling of "fragmented branches" and provides "qualitative predictions under different synthetic degradations."

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Provides state-of-the-art coronary angiography vessel segmentation with explicit topology preservation mechanisms; directly applicable to T6's pipeline for generating segmentation variants and evaluating robustness to topological error.
- verdict: FULL
- revisit-if: Already identified for FULL; use for segmentation robustness evaluation and topology error metrics.
