---
source_pdf_path: Resources/s11227-025-07939-8.pdf
slug: jain-2025-quantum-ecg
ledger_id: C038
ledger_status: TRIAGED
---

# jain-2025-quantum-ecg

## Bibliographic
- Title: Quantum-assisted cardiac diseases diagnosis and prediction using ECG images
- First author / authors: Vibha Jain, Nitin Arora, Aditya Gupta
- Year: 2025
- Venue: The Journal of Supercomputing 81:1439
- DOI: https://doi.org/10.1007/s11227-025-07939-8

## One-line claim
Develops hybrid quantum-classical machine learning pipeline combining ResNet50 deep feature extraction with quantum support vector machine (QSVM) and quantum convolutional neural network (QCNN) for multi-class ECG-based cardiovascular disease classification.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper focuses on ECG image classification, not anatomical geometry, segmentation, or hemodynamic analysis.
- **Q-B decision flip**: NOT REPORTED. No FFR or diagnostic thresholds. Focuses on multi-class disease classification (Normal, Myocardial Infarction, Abnormal Heartbeat, History of MI).
- **Q-C BC tuning**: NOT REPORTED. No fluid dynamics, boundary conditions, or hemodynamic parameter tuning.
- **Q-D fidelity / quantity**: NOT APPLICABLE. Uses machine learning on ECG images, not CFD or hemodynamic simulation. No fluid dynamics, WSS/OSI, or reduced-order/3D models.
- **Q-E data**: ECG image datasets. "Two publicly available multiclass ECG image datasets employed. A new binary dataset curated by integrating abnormal vs. normal classes." Dataset 1: 928 images, Dataset 2: 707 images. NOT REPORTED: invasive FFR ground truth or hemodynamic validation.
- **Q-F meshing**: NOT APPLICABLE. No CFD meshing, anatomical segmentation, or geometry processing relevant to T6.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Focuses on ECG image-based machine learning diagnosis; not relevant to CFD-based hemodynamic modeling, geometry segmentation, or FFR prediction.
- verdict: LIGHT
- revisit-if: N/A (paper is outside T6's scope of CFD hemodynamics and imaging-derived geometry).

## Ideation opening (CFD + imaging)
- None stated. Paper addresses ECG-based machine learning classification, not CFD + imaging integration, hemodynamic simulation, or segmentation-derived geometry uncertainty.
