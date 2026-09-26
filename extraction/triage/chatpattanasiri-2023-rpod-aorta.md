---
source_pdf_path: Resources/1-s2.0-S0021929023003299-main.pdf
slug: chatpattanasiri-2023-rpod-aorta
ledger_status: TRIAGED
---

# chatpattanasiri-2023-rpod-aorta

## Bibliographic
- Title: Towards Reduced Order Models via Robust Proper Orthogonal Decomposition to capture personalised aortic haemodynamics
- First author / authors: Chotirawee Chatpattanasiri, Gaia Franzetti, Mirko Bonfanti
- Year: 2023
- Venue: Journal of Biomechanics
- DOI: 10.1016/j.jbiomech.2023.111759

## One-line claim
Robust POD (RPOD) filters noisy PIV data to enable accurate ROM construction for patient-specific aortic dissection haemodynamics, with 10 POD modes sufficient for flow reconstruction.

## T6 targeted questions
- **Q-A geometry perturbation**: No segmentation uncertainty perturbations. Single patient-specific aortic dissection geometry.
- **Q-B decision flip**: Not relevant (aortic dissection pathophysiology, not coronary FFR).
- **Q-C BC tuning**: Pulsatile outlet Windkessel (3-element) models at each of four outlets (brachiocephalic, LCC, LSA, descending aorta). Patient-specific flow/pressure waveforms prescribed. No evidence of re-tuning after geometry change; no discussion of tuning compensating for error.
- **Q-D fidelity / quantity**: 3D CFD (RANS, ANSYS-CFX) + POD/RPOD-based ROM. Velocity fields reconstructed. No WSS or OSI explicitly reported; focus on mode energy and reconstruction error.
- **Q-E data**: Single patient-specific aortic dissection (Type B) from clinical CT. Experimental PIV (in vitro phantom) and CFD datasets. No invasive hemodynamic ground truth beyond clinical imaging.
- **Q-F meshing**: 3D segmentation from patient CT (semi-automated thresholding); phantom 3D printed. CFD unstructured mesh (ANSYS meshing). PIV: cross-sectional plane, 10 cardiac cycles, 18 snapshots per cycle (180 total). No detail on segmentation robustness to geometry faults.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Aortic dissection pathology; not coronary. RPOD methodology for data denoising could potentially be applied to coronary CFD, but core findings on dissection flow and ROM energy distribution do not transfer to coronary segmentation error or FFR decision-making.
- verdict: LIGHT
- revisit-if: If T6 applies POD to noisy patient-specific coronary CFD data, revisit for RPCA denoising strategy and mode energy distribution under flow state variation.

