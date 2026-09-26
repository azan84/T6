---
source_pdf_path: Resources/s10439-026-04158-x.pdf
slug: li-2026-ffrct-review
ledger_status: TRIAGED
---

# li-2026-ffrct-review

## Bibliographic
- Title: Non-invasive Computational Techniques for Diagnosing Myocardial Ischemia: Challenges and Future of FFRCT/iFRCT
- First author / authors (first 3 + et al.): Bao Li, Jincheng Liu, Yang Yang et al.
- Year: 2026
- Venue: Annals of Biomedical Engineering
- DOI: 10.1007/s10439-026-04158-x

## One-line claim
- Comprehensive review of FFRCT/iFRCT computational models, segmentation methods, and limitations; proposes digital twin technology combined with AI for dynamic real-time myocardial ischemia diagnosis.

## T6 targeted questions
- **Q-A geometry perturbation**: Review; does not perform original perturbation studies. Discusses role of geometry uncertainty (MLD—minimum lumen diameter) in FFR sensitivity.
- **Q-B decision flip**: Review of FFR/iFR thresholds (FFR <0.75 ischemic, >0.8 non-ischemic, 0.75–0.8 gray zone); discusses diagnostic accuracy vs. invasive FFR (90% target).
- **Q-C BC tuning**: Discusses limitations of conventional FFRCT rigid-wall assumption; notes that "plaque types affect stenosis resistance through neural regulation-induced vasodilation changes" and "compensatory mechanisms in coronary microcirculation lead to inaccuracies." Proposes future integration of compliant walls, neuroregulation, and microvascular compensation. No specific tuning protocol demonstrated; review of state-of-the-art.
- **Q-D fidelity / quantity**: Reviews 3D CFD with 0D/1D lumped parameter models, deep learning surrogates. Discusses need for WSS/OSI, tissue perfusion. Recommends high-fidelity integration of multiscale models.
- **Q-E data**: Review article; cites multiple clinical trials and datasets. Discusses PACIFIC, HEART, ADVANCE CAD trials and multi-center studies of FFRCT accuracy.
- **Q-F meshing**: Reviews coronary artery segmentation (traditional and deep learning methods); notes accuracy and speed improvements. Discusses mesh independence and uncertainty from geometric reconstruction; cites 0.5 mm cCTA resolution limit.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive FFR-CT background review; frames current limitations (rigid walls, microvascular compensation mechanisms) that T6 aims to address; contextualizes diagnostic accuracy and threshold effects.
- verdict: LIGHT
- revisit-if: Always as background reference for FFR-CT clinical context and known model limitations. Upgrade to FULL if T6 pursues digital twin or neuroregulation integration.
