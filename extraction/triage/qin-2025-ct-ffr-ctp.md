---
source_pdf_path: Resources/qims-15-09-7909.pdf
slug: qin-2025-ct-ffr-ctp
ledger_status: TRIAGED
---

# qin-2025-ct-ffr-ctp

## Bibliographic
- Title: Fractional flow reserve calculation optimized by myocardial computed tomography perfusion information
- First author / authors: Peiming Qin, Yan Yi, Cheng Xu, Limiao Zou
- Year: 2025
- Venue: Quantitative Imaging in Medicine and Surgery
- DOI: 10.21037/qims-24-2172

## One-line claim
Myocardial blood flow (MBF) from CTP imaging optimizes CFD inlet and outlet boundary conditions, improving CT-FFR diagnostic accuracy from 88% to 94%.

## T6 targeted questions
- **Q-A geometry perturbation**: No—uses actual CCTA segmentation. Does not measure or impose geometry uncertainty.
- **Q-B decision flip**: YES—compares against FFR ≤0.80 threshold. Accuracy improved 88% → 93% (Method A) → 94% (Method B); sensitivity increased from 91.4% to 100% (Method B); specificity increased 86.2% → 93.8% → 90.8% (Method B).
- **Q-C BC tuning**: **KEY FINDING**—"The computed fluid dynamics calculation, guided by MBF values from stress CTP imaging, helps enhance the consistency between CT-FFR calculation and invasive fractional flow reserve measurements." Two approaches: (A) inlet flow optimization using MBF-derived total coronary flow, and (B) inlet & outlet flow optimization using blood supply area analysis. Direct statement: "CFD's high reliance on the accuracy of boundary conditions and the limitations of CT images in providing direct information about flow-related boundary conditions" → "researchers have been striving to achieve more accurate simulations of real blood flow states through enhanced modeling."
- **Q-D fidelity / quantity**: Reduced-order CFD (vessel-by-vessel 1D simulation). Pressure and flow fields computed but no explicit WSS/OSI reporting.
- **Q-E data**: 100 FFR measurement sites from 47 patients. Invasive FFR as reference (FFR ≤0.80). Private cohort (Peking Union Medical College Hospital, March 2016–June 2018).
- **Q-F meshing**: Mesh generation mentioned but no detail on robustness to segmentation error or poorly segmented geometries.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates two BC optimization protocols using perfusion imaging to refine inlet/outlet conditions, with documented sensitivity improvement especially in detection of ischemia-causing lesions, directly applicable to T6's BC-tuning arm.
- verdict: FULL
- revisit-if: None—prioritize for detailed Phase 2 read.
