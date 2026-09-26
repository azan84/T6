---
source_pdf_path: Resources/s13239-023-00658-2.pdf
slug: malota-2023-comparative-ccta-ffr
ledger_status: TRIAGED
---

# malota-2023-comparative-ccta-ffr

## Bibliographic
- Title: The Comparative Method Based on Coronary Computed Tomography Angiography for Assessing the Hemodynamic Significance of Coronary Artery Stenosis
- First author / authors (first 3 + et al.): Małota Z, Sadowski W, Pieszko K, et al.
- Year: 2023
- Venue: Cardiovascular Engineering and Technology
- DOI: 10.1007/s13239-023-00658-2

## One-line claim
VCAST (Virtual Coronary Assessment Stress Test) compares pressure losses in stenosed vs. reconstructed normal coronary arteries via CFD to define hemodynamic parameters (FFRsten, EFRsten) for functional evaluation, validated in 25 patients.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED (uses actual patient stenosed geometry and constructs matched normal reference; no synthetic perturbation or inter-observer error quantification)
- **Q-B decision flip**: NOT REPORTED (FFRsten and EFR correlate with CCTA-FFR, r=0.88 and r=0.90 respectively; diagnostic reclassification not reported)
- **Q-C BC tuning**: NOT REPORTED (paper describes comparative CFD method under "stress test conditions" [maximum blood flow, minimal constant vascular resistance]; no explicit BC tuning/calibration protocol discussed)
- **Q-D fidelity / quantity**: **3D CFD**. "Medical image-based Computational Fluid Dynamic methods" on 3D segmented CCTA; simulates pressure drop under stress conditions. Reports FFR-like indices (FFRsten, EFR); no WSS or OSI reported despite 3D framework.
- **Q-E data**: 25 patients, retrospective CCTA collection, different stenosis degrees and locations. Private cohort; no invasive FFR ground truth. Comparison to CCTA-FFR software (implied HeartFlow or similar commercial reference).
- **Q-F meshing**: NOT REPORTED (3D segmentation from CCTA but no detail on mesh generation, boundary layer refinement, or robustness on complex geometries)

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Proposes comparative stress CFD method for FFR calculation; relevant to T6's CFD + boundary condition strategies but does not address error sensitivity or BC tuning for error compensation.
- verdict: LIGHT
- revisit-if: Paper discusses mesh robustness, BC sensitivity analysis, or error propagation in the VCAST method

