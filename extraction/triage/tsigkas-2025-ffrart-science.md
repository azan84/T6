---
source_pdf_path: Resources/jcm-14-02086.pdf
slug: tsigkas-2025-ffrart-science
ledger_status: TRIAGED
---

# tsigkas-2025-ffrart-science

## Bibliographic
- Title: Image-Based Fractional Flow Reserve: Art and Science. Reply to Taylor et al. Single View Techniques for Modelling Coronary Pressures Losses
- First author / authors (first 3 + et al.): Grigorios G. Tsigkas, George C. Bourantas, Athanasios Moulias
- Year: 2025
- Venue: Journal of Clinical Medicine
- DOI: 10.3390/jcm14062086

## One-line claim
Methodological reply defending single-view FFR2D technique against 3D reconstruction criticism; analyzes sources of model error and boundary condition uncertainty.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Discusses geometric accuracy of 2D vs. 3D reconstruction and pixel resolution limits (0.10–0.20 mm/pixel, MLD 6–7 pixels) but not inter-observer disagreement quantification.
- **Q-B decision flip**: NOT REPORTED. Methodological discussion; no FFR reclassification rates at 0.80 threshold.
- **Q-C BC tuning**: EXTENSIVELY DISCUSSED. Key quote: "Most established software solutions employ fixed values of microvascular resistance, blood flow velocity, or some other generic boundary condition to simulate hyperemic flow conditions" and "the factor by which the microvascular resistance is reduced during hyperemia is the leading governor of the corresponding relative increase of blood flow Q... which in turn defines the magnitude of the measured or computed pressure drop." Also: "Stenosis severity was the primary determinant of FFR uncertainty analysis, but a plain 2D model with time-averaged flow had a high diagnostic accuracy (0.99)."
- **Q-D fidelity / quantity**: YES. Compares 2D/3D geometry reconstruction, steady vs. transient flow, CFD complexity vs. accuracy tradeoff; focuses on FFR (pressure), not spatially-resolved fields.
- **Q-E data**: NOT REPORTED (reply/commentary article, no primary data).
- **Q-F meshing**: Mentions CFD solver convergence failures (loss of data due to motion artifacts, mesh generation issues) but no systematic robustness analysis.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Methodological discussion of BC tuning (microvascular resistance reduction) as driver of FFR, and 2D vs. 3D geometry tradeoffs; valuable context but not primary research.
- verdict: LIGHT
- revisit-if: Quantitative data on FFR error vs. microvascular BC tuning; analysis of topologically broken geometry handling.
