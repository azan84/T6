---
source_pdf_path: Resources/2308.04923v1.pdf
slug: hampe-2023-deep-learning-ffr
ledger_status: TRIAGED
---

# hampe-2023-deep-learning-ffr

## Bibliographic
- Title: Deep Learning-Based Prediction of Fractional Flow Reserve Along the Coronary Artery
- First author / authors (first 3 + et al.): Nils Hampe, Sanne G. M. van Velzen, Jean-Paul Aben
- Year: 2023
- Venue: arXiv:2308.04923
- DOI: NOT REPORTED

## One-line claim
A two-stage deep learning method predicts FFR curves along the coronary artery from CCTA using a variational autoencoder for artery characterization and a CNN for FFR drop prediction, validated on invasive FFR pullback measurements.

## T6 targeted questions
- **Q-A geometry perturbation**: The paper acknowledges "artery segmentations are needed" and discusses "Coronary artery lumen segmentation in CCTA scans is a highly challenging task due to the small scale of the structures, the variability in contrast enhancement in the lumen, and blooming caused by the contrast agent." Manual reference segmentations created. No systematic inter-observer perturbation study, but segmentation variability is documented.
- **Q-B decision flip**: FFR pullback measurements are used as reference (112 arteries, max 90 days from CCTA). Focal vs diffuse disease classification threshold reported: "median PPG of the reference pullbacks as threshold to classify the disease... this median equals 0.63." Accuracy 0.70, sensitivity 0.80, specificity 0.60 for focal/diffuse distinction. FFR values below 0.7 are overestimated by the model (worst case up to 0.6).
- **Q-C BC tuning**: The paper uses deep learning to bypass explicit CFD. It acknowledges that CFD methods "require an accurate segmentation of the artery lumen and accurate determination of boundary conditions, which remains challenging." No BC tuning or re-tuning discussed; the method avoids CFD computational burden by direct learning from data.
- **Q-D fidelity / quantity**: NOT 3D CFD. Uses deep learning (variational autoencoder + CNN) to predict FFR spatially without solving Navier-Stokes. Does not compute or report WSS, OSI, or other spatially-resolved hemodynamic fields.
- **Q-E data**: 110 patients (118 screened, 8 excluded for poor scan quality) with 112 invasive FFR pullback measurements. CCTA images from Siemens Somatom Definition Flash. In-plane resolution 0.28-0.70 mm², slice thickness 0.5-1.0 mm.
- **Q-F meshing**: No meshing required (deep learning approach). Uses "multi-planar reconstruction (MPR)" of arteries with 0.1 mm in-plane resolution and 0.5 mm slice distance for VAE input. Manual correction of coronary artery segmentations assisted by X-ray angiography (XRA) for 72 of 112 arteries to validate lumen boundary.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates deep learning for automatic FFR prediction without explicit BC determination, and highlights segmentation/lumen boundary uncertainty as a key challenge; relevant to T6's focus on segmentation error impact.
- verdict: LIGHT
- revisit-if: If paper or related work reports error sensitivity (i.e., how segmentation perturbations affect FFR predictions) or compares this learned approach to CFD with systematic BC tuning.
