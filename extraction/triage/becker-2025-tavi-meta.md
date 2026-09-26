---
source_pdf_path: Resources/s00330-024-11211-7.pdf
slug: becker-2025-tavi-meta
ledger_status: TRIAGED
---

# becker-2025-tavi-meta

## Bibliographic
- Title: Coronary CTA and CT-FFR in trans-catheter aortic valve implantation candidates: a systematic review and meta-analysis
- First author / authors: Leonie M. Becker, Joyce Peper, Dirk-Jan van Ginkel, Daniël C. Overduin
- Year: 2025
- Venue: European Radiology
- DOI: 10.1007/s00330-024-11211-7

## One-line claim
Meta-analysis of 34 articles (N=7235 CCTA, N=1269 CT-FFR) in TAVI patients shows CCTA rules out CAD effectively; CT-FFR performs better than CCTA in direct comparison but requires validation in TAVI populations using commercial software.

## T6 targeted questions
- **Q-A geometry perturbation**: No—systematic review; no primary geometry perturbation study.
- **Q-B decision flip**: YES—discusses FFR ≤0.80 threshold and CAD classification (≥50% diameter reduction as obstructive). Sensitivity/specificity pooled across studies: CCTA (patient level) sensitivity 94.0%, specificity 72.4%; CT-FFR sensitivity 93.2%, specificity 70.3%. In direct-comparison studies: CT-FFR sensitivity 83.9% vs. CCTA 74.9%; CT-FFR specificity 89.8% vs. CCTA 65.5%.
- **Q-C BC tuning**: NOT ADDRESSED—review does not detail BC methodologies; one study (Sasaki et al.) noted "no significant difference in diagnostic performance of pre-TAVI FFR-CT compared to post-TAVI FFR-CT" but individual-patient changes not reported. Zhang et al. reported 15/24 patients switched from positive pre-TAVI to negative post-TAVI FFR, hypothesizing sympathetic nervous system normalization.
- **Q-D fidelity / quantity**: Reviews both reduced-order and 3D CFD approaches but does not specify WSS/OSI extraction or sensitivity analyses.
- **Q-E data**: Meta-analysis covering 34 studies; no single cohort. Most studies used QCA, visual ICA, or invasive pressure measurements as reference.
- **Q-F meshing**: Identifies image quality as limitation: "high calcium burden and previous PCI are common and cause artifacts" and "CCTA image quality is essential… more challenging in the TAVI population." Does not address robustness of segmentation algorithms to poor or artifact-laden geometries.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive systematic review of CT-FFR in non-standard (TAVI) population; establishes diagnostic performance but does not address segmentation error, BC tuning, or topology-robustness—T6's core questions.
- verdict: LIGHT
- revisit-if: For epidemiological context on CT-FFR performance variability; not for methodology or error characterization.
