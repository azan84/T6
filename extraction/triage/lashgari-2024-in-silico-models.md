---
source_pdf_path: Resources/fcvm-11-1398290.pdf
slug: lashgari-2024-in-silico-models
ledger_status: TRIAGED
---

# lashgari-2024-in-silico-models

## Bibliographic
- Title: Patient-specific in silico 3D coronary model in cardiac catheterisation laboratories
- First author / authors (first 3 + et al.): Lashgari M, Choudhury RP and Banerjee A
- Year: 2024
- Venue: Frontiers in Cardiovascular Medicine
- DOI: 10.3389/fcvm.2024.1398290

## One-line claim
Review of patient-specific in silico models for coronary FFR/CFR prediction emphasizing segmentation, 3D reconstruction, and CFD simulation challenges in catheterization labs.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT perturbed in this review; discusses segmentation challenges and reconstruction uncertainties but as SOURCES OF ERROR rather than systematic perturbation studies.
- **Q-B decision flip**: Discusses FFR < 0.80 threshold and related indices (CFR, rCFR, iFR, RFR) as decision metrics. "70% of treatment decisions still depend on the visual assessment of angiographic stenosis...which has limited accuracy (about 60–65%) in predicting FFR < 0.80." Motivates need for non-invasive FFR prediction to reduce unnecessary invasive procedures.
- **Q-C BC tuning**: Discusses but does NOT deeply analyze. Notes: "lack of segmenting terminal vessels leads to a wrong boundary conditions assignment which invalidates assessment of the disease's impact on myocardial blood flow" and "it is crucial to consider patient-speciﬁc boundary conditions and the associated uncertainties." Acknowledges side branch impact on outlet BC. No detailed methodology for BC tuning or adaptive approaches.
- **Q-D fidelity / quantity**: Review covers both approaches: reduced-order CFD and full 3D CFD. Mentions FFR, CFR, relative CFR, isobaric microvascular resistance (IMR), iFR, RFR as outputs. Discusses potential for WSS/OSI but emphasizes computational burden.
- **Q-E data**: Review article; no patient cohort. Synthesizes evidence from multiple studies (N ranges cited: e.g., 317 patients from CT-FFR-CHINA, 126 from NXT trial).
- **Q-F meshing**: EXTENSIVELY DISCUSSES. "Limitations in segmenting small or terminal vessels limit coronary blood ﬂow simulation...the lack of segmenting terminal vessels leads to a wrong boundary conditions assignment" (line 738–742). Reviews challenges: "artifacts such as weak contrast between coronary arteries and the background...segmentation methods often face challenges with temporal changes and vessel appearance variations throughout the cardiac cycle." Table 2 compares segmentation methods (thresholding, tracking, CNN, U-Net, GAN, ensemble). NO explicit discussion of topological error robustness (e.g., broken vessel connections, reversed flow).

## Novelty bearing on T6
- bucket: BACKGROUND | METHOD
- one-line reason: Comprehensive review of in silico coronary modeling pipeline; highlights segmentation and BC challenges as critical sources of uncertainty; relevant to T6's premise that segmentation error impacts FFR prediction, but does NOT analyze error compensation via BC tuning
- verdict: LIGHT
- revisit-if: Review specifically addresses whether BC tuning can compensate for segmentation error, or includes case studies demonstrating error propagation and mitigation

