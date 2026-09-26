---
source_pdf_path: Resources/1-s2.0-S2949761224001202-main.pdf
slug: chan-2024-ct-ffr-applications
ledger_status: TRIAGED
---

# chan-2024-ct-ffr-applications

## Bibliographic
- Title: Clinical Applications of Fractional Flow Reserve Derived from Computed Tomography in Coronary Artery Disease
- First author / authors (first 3 + et al.): Cappi Chan, Min Wang, Luoyi Kong et al.
- Year: 2024
- Venue: Mayo Clinic Proceedings: Digital Health
- DOI: 10.1016/j.mcpdig.2024.100187

## One-line claim
Review of CT-FFR clinical applications, computational foundations, diagnostic performance, algorithm comparison, and limitations including sensitivity to boundary conditions and image quality.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No synthetic or measured segmentation uncertainty studies presented.
- **Q-B decision flip**: Yes; FFR ≤0.80 threshold extensively discussed. "It was established that CT-FFR of less than or equal to 0.80 was a reliable predictor of lesion-specific ischemia with improvement in specificity and positive predictive value (sensitivity, 82%; specificity, 94%; positive predictive value, 88%; negative predictive value, 92%)."
- **Q-C BC tuning**: Yes, central discussion. "HeartFlow, the CFD model for CT-FFR measurement... data are then uploaded to the HeartFlow cloud server and processed by artificial intelligence and technicians before simulating fluid dynamics." Discusses boundary conditions: "aorta and distal coronary artery resistance as these boundary conditions affect the flow rate through the coronary arteries and ultimately the pressure gradient along the diseased lesions." Key statement: "slight changes in outflow conditions may result in diagnosis change, especially in the 0.75–0.85 FFR range." No explicit statement on re-tuning after geometric change.
- **Q-D fidelity / quantity**: CFD-based (HeartFlow uses Navier-Stokes equations, incompressible flow model) and machine learning methods; does not report WSS/OSI as primary outcomes in coronary context.
- **Q-E data**: Review and case compilation; references ADVANCE, NXT, PACIFIC-1 trials. No single cohort presented. Invasive FFR reference standard.
- **Q-F meshing**: Discusses segmentation errors extensively: "Segmentation errors could also result in misleading CT-FFR values" and "When the modeling of the coronary artery is tighter than it should be, the extent of stenosis could be exaggerated." Also: "Inaccurate recognition of coronary arteries could also result in missing functional stenosis in small branches."

## Novelty bearing on T6
- bucket: THREAT
- one-line reason: Explicitly documents that "slight changes in outflow conditions may result in diagnosis change, especially in the 0.75–0.85 FFR range" and discusses segmentation errors causing FFR bias—both core to T6's hypothesis that BC/geometric error impacts decision-making. Potential Gate N1 conflict if BC tuning is shown to mask geometric error.
- verdict: FULL
- revisit-if: Quantitative sensitivity analysis of CFD-FFR to boundary condition perturbations in intermediate stenosis.
