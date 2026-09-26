---
source_pdf_path: Resources/1-s2.0-S1746809425006822-main.pdf
slug: sooriamoorthy-2025-cnn-cardiovascular
ledger_id: C012
ledger_status: TRIAGED
---

# sooriamoorthy-2025-cnn-cardiovascular

## Bibliographic
- Title: An integrated convolutional neural network with zero-dimensional cardiovascular hemodynamics parameters for early cardiovascular disease detection
- First author / authors: Denesh Sooriamoorthy, Mohammed Ayoub Juman, Aaruththiran Manoharan
- Year: 2025
- Venue: Biomedical Signal Processing and Control, vol. 110
- DOI: 10.1016/j.bspc.2025.108171

## One-line claim
Proposes CNN-based framework for early CVD detection that combines blood pressure waveform analysis with parameters from Rideout's zero-dimensional cardiovascular model, trained on simulated aortic waveforms and validated on clinical MIMIC II and hospital datasets.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Paper does not address vascular geometry variability, segmentation uncertainty, or inter-observer differences. Focus is on extracting 0-D model parameters from BP waveforms.
- **Q-B decision flip**: NOT REPORTED. No FFR threshold or diagnostic reclassification analysis; focus is CVD classification (binary: CVD vs. healthy).
- **Q-C BC tuning**: NOT REPORTED. Paper uses Rideout's complete 0-D cardiovascular model but does not discuss BC tuning, re-parameterization after geometry changes, or optimization protocols.
- **Q-D fidelity / quantity**: 0-D lumped-parameter model only (Rideout model with 16 aortic-pressure-affecting parameters). No 3D CFD, no WSS, no spatially resolved hemodynamic fields.
- **Q-E data**: PhysioNet MIMIC II database (radial BP waveforms; 4 CVD, 19 non-CVD signals); HaeMod dataset (3365 healthy signals); Hospital Sultanah Bahiyah (HSB) Malaysia (40 CVD signals). No invasive FFR ground truth; outcomes are CVD diagnosis classification (80–82.5% accuracy reported).
- **Q-F meshing**: NOT APPLICABLE. Zero-dimensional lumped model; no geometry, segmentation, or meshing.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Demonstrates 0-D cardiovascular model parameter extraction as feature set for CVD detection; relevant to T6's framing of 0-D models but not addressing segmentation error, BC tuning, or FFR sensitivity.
- verdict: LIGHT
- revisit-if: If paper includes sensitivity of model parameters to input waveform noise or geometric assumptions underlying the 0-D model, or if 0-D output parameters are validated against invasive hemodynamic measurements.

## Ideation opening (CFD + imaging)
- None stated. Paper focuses on non-invasive CVD detection from peripheral pulse waveforms using machine learning and lumped-parameter modeling; no CFD or imaging-flow coupling discussed.
