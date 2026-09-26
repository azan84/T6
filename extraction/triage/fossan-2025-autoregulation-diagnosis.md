---
source_pdf_path: Resources/fossan-et-al-2025-relevance-of-autoregulation-in-the-diagnosis-of-coronary-artery-disease-with-ct-ffr.pdf
slug: fossan-2025-autoregulation-diagnosis
ledger_status: TRIAGED
---

# fossan-2025-autoregulation-diagnosis

## Bibliographic
- Title: Relevance of autoregulation in the diagnosis of coronary artery disease with CT-FFR
- First author / authors (first 3 + et al.): Fossan FE, Bråten AT, Lucca A, et al.
- Year: 2025 (published 2026)
- Venue: American Journal of Physiology - Heart and Circulatory Physiology
- DOI: 10.1152/ajpheart.00442.2025

## One-line claim
Microvascular autoregulation causes stenosis-severity-dependent variations in the adenosine-induced vasodilatory response, improving CT-FFR prediction variability (R² 0.398 vs. 0.179) but not overall diagnostic AUC when incorporated into reduced-order models.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No geometric perturbation studies; focuses on physiological response variation, not segmentation uncertainty.
- **Q-B decision flip**: YES, FFR ≤0.80 threshold used. N=280 lesions, invasive FFR gold standard (adenosine hyperemia). "If FFR is below 0.8, the stenosis is considered hemodynamically significant...If FFR is above 0.8, optimal medical therapy alone is recommended." Autoregulation model: "area under the curve (AUC) remained unchanged."
- **Q-C BC tuning**: YES, CRITICAL FINDING. "Most current CT-FFR models assume a fixed microvascular response to adenosine, treating vasodilation capacity as constant and optimal for all patients and lesions." Key discovery: autoregulation causes stenosis-severity-dependent microvascular response. "In the presence of coronary artery stenosis, part of this vasodilatory reserve may already be used, triggered by pressure-flow autoregulation mechanisms." Model: "microvascular response to adenosine was quantified...lower basal perfusion pressure accompanied by a reduced microvascular response to adenosine was regarded as indicative of exhausted vasodilatory capacity resulting from autoregulatory mechanisms." Microvascular response varies with stenosis (Pd/Pa), lesion location, sex, and heart rate. Quote: "Capturing coronary hemodynamics depended most on accurate geometry reconstruction and cardiac output measurement" suggests outlet BC is less dominant, but autoregulation couples geometry severity to outlet resistance in a nonlinear way that cannot be simply re-tuned post-hoc.
- **Q-D fidelity / quantity**: 1D + 0D hybrid (Windkessel). "machine learning-augmented reduced-order model" couples 1D/0D pressure drops with neural network refinement. Does NOT report WSS/OSI; focus on pressure-based FFR.
- **Q-E data**: N=280 lesions from multi-center prospective study at St. Olavs Hospital and collaborating centers. N patients not explicit but mixed sex (37% female, 63% male). Invasive FFR gold standard (adenosine). CCTA segmentation down to 1 mm vessel radius.
- **Q-F meshing**: YES, segmentation described. "coronary arteries were segmented down to the level at which they could no longer be reliably distinguished from the surrounding tissue, corresponding to a vessel radius of 1 mm. Postprocessing of the segmentations, including surface and centerline generation, was performed using the open-source software VMTK." No detail on robustness to topologically broken geometry or sensitivity to segmentation error.

## Novelty bearing on T6
- bucket: THREAT
- one-line reason: Demonstrates that outlet microvascular resistance (BC parameter) is physiologically coupled to stenosis severity via autoregulation, meaning tuning cannot be applied uniformly to "absorb" segmentation errors—error-induced geometry changes will trigger mismatched autoregulation response. AUC-unchanged result suggests compensation is incomplete.
- verdict: FULL
- revisit-if: CRITICAL for T6 hypothesis testing. Must determine whether autoregulation coupling means BC re-tuning can/cannot mask topological error; Fossan's unchanged AUC despite improved R² suggests residual error remains despite BC adaptation.
