---
source_pdf_path: Resources/fcvm-13-1850945.pdf
slug: mora-2026-emerging-quantitative-ccta
ledger_status: TRIAGED
---

# mora-2026-emerging-quantitative-ccta

## Bibliographic
- Title: Emerging quantitative CCTA imaging biomarkers for cardiovascular risk stratification: a narrative review
- First author / authors (first 3 + et al.): Mora R, Irannejad K, Abbas N, et al.
- Year: 2026
- Venue: Frontiers in Cardiovascular Medicine
- DOI: 10.3389/fcvm.2026.1850945

## One-line claim
Narrative review synthesizing CCTA-based imaging biomarkers (plaque characteristics, FFR-CT, EAT, PCAT/FAI, hepatic steatosis) and their integration for cardiovascular risk stratification.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Review focuses on imaging biomarker measurement and prognostic value, not geometric perturbation studies or segmentation uncertainty quantification.
- **Q-B decision flip**: YES, FFR-CT threshold mentioned. "FFR-CT carries a Class 2a guideline recommendation for intermediate lesions and demonstrates superior vessel-level diagnostic accuracy compared with SPECT." Notes FFR threshold but does not report reclassification rates.
- **Q-C BC tuning**: NOT REPORTED. Review describes FFR-CT methodology ("provides lesion-specific physiological information by simulating coronary hemodynamics") but does not detail boundary condition tuning, Windkessel, resistance, or whether tuning compensates for geometric error.
- **Q-D fidelity / quantity**: Reduced-order CFD implied. FFR-CT calculation mentioned but mechanism not detailed. No WSS/OSI reported; focus is on diagnostic classification, not spatially-resolved hemodynamic fields.
- **Q-E data**: NOT REPORTED in abstract/intro/conclusion. Review cites multiple cohorts (SCOT-HEART, PARADIGM) but does not specify own cohort or ground truth validation.
- **Q-F meshing**: NOT REPORTED. Segmentation briefly mentioned ("automated coronary segmentation and quantitative plaque mapping") but no meshing details.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Clinical review of FFR-CT and CCTA biomarkers for risk stratification; establishes T6's context (FFR ≤0.80 diagnostic threshold) but does not address segmentation error or BC tuning effects.
- verdict: LIGHT
- revisit-if: If constructing literature narrative on FFR-CT validation and guideline status.
