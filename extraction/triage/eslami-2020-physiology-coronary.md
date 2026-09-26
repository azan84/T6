---
source_pdf_path: Resources/s10554-020-01954-x.pdf
slug: eslami-2020-physiology-coronary
ledger_status: TRIAGED
---

# eslami-2020-physiology-coronary

## Bibliographic
- Title: Physiology and coronary artery disease: emerging insights from computed tomography imaging based computational modeling
- First author / authors: Parastou Eslami, Vikas Thondapu, Julia Karady et al.
- Year: 2020
- Venue: The International Journal of Cardiovascular Imaging
- DOI: 10.1007/s10554-020-01954-x

## One-line claim
Comprehensive review of coronary CT-based computational fluid dynamics modeling for assessment of hemodynamic indices (FFR, ESS, plaque stress) and their role in identifying high-risk coronary lesions.

## T6 targeted questions

- **Q-A geometry perturbation**: NOT REPORTED. Review does not systematically examine segmentation uncertainty or inter-observer disagreement impacts. Mentions image quality challenges (motion artifacts, calcification blooming) and segmentation labor-intensity but does not quantify geometric error.

- **Q-B decision flip**: Mentions FFR threshold concept and clinical use but does not report reclassification rates. States FFR ≤0.80 is "widely accepted as indicating a functionally significant lesion."

- **Q-C BC tuning**: YES, addressed in methods section. States: "Lumped parameter (0 or 1-order) models can be used as boundary conditions. The lumped parameters (e.g., resistance, compliance, etc.) may be tuned via numerical optimization and sensitivity analysis." Also discusses: "Suitable modifications to the boundary conditions such as including a pressure source in the LPN model can be implemented to impose an out of phase with the systemic circulation. Including an intramyocardial pressure source to impede flow during systole and relax during diastole adjusts the coronary circulation phase." Does NOT explicitly state whether tuning is re-done after geometry changes or whether it compensates for geometric error.

- **Q-D fidelity / quantity**: Reviews both reduced-order and 3D CFD approaches. Discusses ESS (endothelial shear stress), axial plaque stress (APS), and FFR as hemodynamic outputs. Mentions FSI (fluid-structure interaction) as computationally expensive alternative. Reviews Windkessel models, lumped parameter networks, and 1D/0D approaches.

- **Q-E data**: Review paper; does not present new cohort data. Discusses clinical trials (DISCOVER-FLOW, NXT, PROMISE) and their FFR-CT validation against invasive FFR.

- **Q-F meshing**: Brief discussion. States: "Quality control of the generated mesh is challenging and a crucial step to ensure that the mesh reflects the domain and geometry that bounds the blood flow." Mentions semiautomatic segmentation implementation and deep-learning tools emerging. Notes: "Imaging artifacts make it difficult to segment the images and detect the true lumen borders; Segmentation of the coronary artery lumen, plaque and wall is a tedious and time-consuming process."

## Novelty bearing on T6

- **bucket**: BACKGROUND
- **one-line reason**: Comprehensive methodological review of CFD-FFR workflows, boundary conditions, and segmentation challenges; foundational context for T6's reduced-order modeling and boundary condition framework.
- **verdict**: LIGHT
- **revisit-if**: Paper includes quantitative sensitivity analysis of BC tuning to geometry or reports inter-observer segmentation disagreement impact on FFR.
