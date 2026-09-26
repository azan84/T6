---
source_pdf_path: Resources/s00330-025-11747-2.pdf
slug: wang-2025-ffr-prognostic
ledger_status: TRIAGED
---

# wang-2025-ffr-prognostic

## Bibliographic
- Title: Long-term prognostic value of the CT-derived fractional flow reserve combined with atherosclerotic burden in patients with non-obstructive coronary artery disease
- First author / authors (first 3 + et al.): Zhiqiang Wang, Zhennan Li, Tingfeng Xu et al.
- Year: 2025
- Venue: European Radiology
- DOI: 10.1007/s00330-025-11747-2

## One-line claim
CT-FFR ≤ 0.80 provides independent and incremental prognostic value beyond CCTA-defined atherosclerotic burden for predicting long-term MACE in non-obstructive CAD.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Study uses clinical cohort with real anatomies, not synthetic perturbations.
- **Q-B decision flip**: FFR ≤ 0.80 threshold explicitly used (HR: 7.18; 95% CI: 4.25–12.12; p < 0.001 for MACE prediction). FFR >0.80 treated as non-significant. No reclassification rates across threshold provided.
- **Q-C BC tuning**: NOT REPORTED. Study reports CT-FFR calculations retrospectively on DEEPVESSEL FFR workstation but does not discuss boundary condition setting, tuning, or any statement about tuning compensating for geometric error.
- **Q-D fidelity / quantity**: Deep learning-based vessel-specific CT-FFR (algorithm details in prior validation papers). No direct CFD discussion or WSS/OSI reported.
- **Q-E data**: N=1944 patients, single-center Beijing Anzhen Hospital (2017–2018), invasive FFR ground truth absent (FFR-CT only), median follow-up 73.4 months.
- **Q-F meshing**: NOT REPORTED. No segmentation or meshing details provided.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Validates prognostic utility of CT-FFR in non-obstructive CAD; does not address boundary condition tuning, topological error masking, or CFD methodology.
- verdict: LIGHT
- revisit-if: Deep learning CT-FFR model details or downstream clinical outcomes by segmentation quality emerge.

