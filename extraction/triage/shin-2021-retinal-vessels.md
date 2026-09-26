---
source_pdf_path: Resources/applsci-11-00320.pdf
slug: shin-2021-retinal-vessels
ledger_status: TRIAGED
---

# shin-2021-retinal-vessels

## Bibliographic
- Title: Topology-Aware Retinal Artery–Vein Classification via Deep Vascular Connectivity Prediction
- First author / authors (first 3 + et al.): Seung Yeon Shin, Soochahn Lee, Il Dong Yun, et al.
- Year: 2021
- Venue: Applied Sciences
- DOI: 10.3390/app11010320

## One-line claim
This paper presents a CNN-based method for retinal artery-vein classification that uses estimated vessel topology (via iterative vascular connectivity prediction) to improve classification accuracy, particularly for thin vessels, with validation on DRIVE and IOSTAR fundus image datasets.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper addresses vessel classification in fundus images, not geometry perturbation or segmentation error quantification.
- **Q-B decision flip**: NOT REPORTED. No diagnostic reclassification or clinical thresholds; endpoint is artery vs. vein classification accuracy.
- **Q-C BC tuning**: NOT APPLICABLE. No haemodynamic modeling or boundary condition tuning.
- **Q-D fidelity / quantity**: NOT APPLICABLE. Paper is image-based segmentation/classification; no CFD, reduced-order models, or hemodynamic fields (WSS, OSI).
- **Q-E data**: Public datasets: DRIVE (40 images, 40mm fundus camera) and IOSTAR (18 images, scanning laser ophthalmoscope). No hemodynamic ground truth; endpoint is artery-vein labeling accuracy.
- **Q-F meshing**: NOT APPLICABLE. Addresses 2D fundus image segmentation and topology, not 3D volume meshing or robustness to topologically incorrect geometry.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: While this paper addresses vascular topology estimation and segmentation in medical imaging (relevant to vascular analysis broadly), it is specific to retinal fundus imaging and does not address coronary arteries, haemodynamic modeling, boundary condition tuning, or the key T6 concern about segmentation error masking via re-fitting. The topology-aware approach may inform segmentation quality assessment but is not directly applicable to T6's coronary FFR modeling.
- verdict: LIGHT
- revisit-if: Paper demonstrates sensitivity of a hemodynamic or physiological model output to errors in vascular topology/segmentation, or if the topology-aware segmentation method is applied to coronary imaging and linked to hemodynamic decision-making

