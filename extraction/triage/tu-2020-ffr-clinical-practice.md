---
source_pdf_path: Resources/eurheartj_41_34_3271.pdf
slug: tu-2020-ffr-clinical-practice
ledger_status: TRIAGED
---

# tu-2020-ffr-clinical-practice

## Bibliographic
- Title: Fractional flow reserve in clinical practice: from wire-based invasive measurement to image-based computation
- First author / authors: Shengxian Tu, Jelmer Westra, Julien Adjedj
- Year: 2020
- Venue: European Heart Journal
- DOI: 10.1093/eurheartj/ehz918

## One-line claim
Comprehensive clinical review of FFR (invasive wire-based and image-based computational approaches), highlighting principles, diagnostic performance, clinical applications, and challenges of computational physiology in the catheterization laboratory for stenosis assessment and procedural guidance.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED — Review article; no primary data on segmentation uncertainty or inter-observer disagreement.
- **Q-B decision flip**: GENERAL REFERENCE — States FFR <0.75–0.80 indicates lesions requiring intervention; discusses reclassification concept but does not report specific rates.
- **Q-C BC tuning**: MENTIONED AS LIMITATION — "FFR is related to the total sum of vascular resistances. When only evaluating the pressure drop, assessment of haemodynamically significant epicardial disease can be influenced by microvascular dysfunction." Notes that pressure wire measurements may overestimate severity in tortuous vessels via "accordion phenomenon." Does NOT discuss explicit BC tuning or re-tuning after geometry changes.
- **Q-D fidelity / quantity**: Reviews both invasive (pressure wire) and computational approaches (CFD, angiography-based); mentions full 3D Navier-Stokes and reduced-order methods; NO WSS/OSI in review focus.
- **Q-E data**: Review of multiple clinical trials and studies; no single primary cohort.
- **Q-F meshing**: NOT ADDRESSED — Computational approaches mentioned but no detail on meshing or robustness to poor geometry.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Clinical review establishing FFR as gold standard for functional stenosis assessment and discussing computational approaches; sets clinical context for T6's work on error sources and BC tuning.
- verdict: LIGHT
- revisit-if: Review included systematic analysis of how BC assumptions or geometric errors affect FFR computation accuracy

