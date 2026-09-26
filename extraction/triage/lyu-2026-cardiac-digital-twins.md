---
source_pdf_path: Resources/2606.01808v1.pdf
slug: lyu-2026-cardiac-digital-twins
ledger_status: TRIAGED
---

# lyu-2026-cardiac-digital-twins

## Bibliographic
- Title: Personalized 3D Myocardial Infarct Geometry Reconstruction from Cine MRI for Cardiac Digital Twins
- First author / authors (first 3 + et al.): Yilin Lyu, Mark YY Chan, Ching-Hui Sia
- Year: 2026
- Venue: arXiv preprint, Medical Image Analysis (submitted)
- DOI: NOT REPORTED (arXiv:2606.01808v1)

## One-line claim
Proposes GeoMo-Net, a contrast-free 3D myocardial infarct reconstruction framework from routine cine MRI for building cardiac digital twins that enable patient-specific electrophysiological simulation of post-MI arrhythmic risk.

## T6 targeted questions
- **Q-A geometry perturbation**: Reconstructs personalized 3D scar geometry from motion abnormalities; does not explicitly perturb geometry to measure uncertainty. Validation compares reconstructed scar against LGE-MRI ground truth. NOT REPORTED as magnitude of measured inter-observer segmentation disagreement.
- **Q-B decision flip**: Reports Dice scores (0.678 ± 0.011) and in-silico EP simulation consistency with LGE-derived ground truth. No threshold-based diagnostic reclassification (FFR-like) reported. NOT REPORTED.
- **Q-C BC tuning**: Addresses cardiac electrophysiological modeling via digital twins. Mentions "patient-specific computational modeling" but does not detail outlet BC tuning, Windkessel parameters, or whether fitting compensates for geometric error. NOT REPORTED.
- **Q-D fidelity / quantity**: 3D ventricular and scar reconstruction for in-silico EP simulation. No 3D CFD or WSS/OSI; focuses on electrophysiology (conduction, arrhythmia risk) not hemodynamics. NOT REPORTED.
- **Q-E data**: 225 cine MRIs from public dataset; invasive FFR ground truth NOT present. Validation via LGE-MRI and in-silico EP simulation results consistency, not clinical outcome data.
- **Q-F meshing**: Constructs 4D (3D+time) biventricular mesh; addresses geometry-motion integration and scar topology embedding into mesh. Does not report meshing robustness on topologically incorrect or broken geometries.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates digital twin construction and validation methodology for cardiac geometry (scar) using imaging-derived 3D reconstructions and in-silico simulation consistency as validation surrogate; methodologically relevant to T6's CDT validation framework even though application is cardiac electrophysiology not coronary hemodynamics.
- verdict: FULL
- revisit-if: Check whether paper discusses how fitting/calibration in EP models can mask geometric error, or uncertainty propagation from geometry to simulation output (relevant to T6 Gate N1 hypothesis).
