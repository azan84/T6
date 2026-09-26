---
source_pdf_path: Resources/ssrn-5865902.pdf
slug: pietrobon-2026-digital-twins-ablation
ledger_status: TRIAGED
---

# pietrobon-2026-digital-twins-ablation

## Bibliographic
- Title: The Digital Twins Method: A Mechanistic Modeling Approach for Identifying Ablation Targets in Atrial Fibrillation (Motivated by the Personalized Substrate-Guided Ablation Strategy by Sakata et al.)
- First author / authors (first 3 + et al.): Ricardo Pietrobon, Aline Machiavelli, Luiza Paulsen Rodrigues, et al.
- Year: 2026
- Venue: SSRN Preprint
- DOI: https://ssrn.com/abstract=5865902

## One-line claim
Reviews the Digital Twins method for constructing patient-specific bi-atrial electromechanical models from late gadolinium enhancement (LGE-MRI) and electrophysiological data to simulate rotor dynamics, guide substrate-based ablation, and minimize lesion burden in persistent atrial fibrillation.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED specifically for segmentation error, but discusses "fibrosis density (FD) and fibrosis entropy (FE)" as quantifiable structural properties and how imaging-derived fibrosis quantification introduces variability ("variability in image acquisition or contrast dynamics can influence fibrosis quantification"). Recognizes uncertainty in structural inputs.
- **Q-B decision flip**: NOT REPORTED for FFR, but the method evaluates rotor inducibility (binary outcome: arrhythmia non-inducibility) and distinguishes "independent rotor-sustaining sites (LIRs) from contingent regions (LCRs)" - a mechanistic analog of threshold-based reclassification.
- **Q-C BC tuning**: NOT REPORTED for boundary conditions, but extensively discusses iterative virtual ablation testing and how "elimination of one rotor could extinguish others without direct intervention," demonstrating that substrate modification strategies are tested and refined in silico before clinical application. This is analogous to model parameter tuning.
- **Q-D fidelity / quantity**: PARTIAL. Uses "bi-atrial models" with "fiber orientation" and "electrophysiological remodeling"; reports simulations of "rotor propagation" but unclear if reports spatial fields like WSS/OSI. Emphasis on electrophysiological rather than hemodynamic fidelity.
- **Q-E data**: PARTIAL. Case study motivated by "prospective computational-clinical investigation by Sakata et al. (2024)" with patient-specific models but does not report specific N or name a public dataset; mentions "experimental validation against intra-procedural electrograms."
- **Q-F meshing**: PARTIAL. Discusses "LGE-MRI segmentation, fibrosis thresholding, and assumptions embedded in the electrophysiological models" and notes that "segmentation validation by experienced operators" is necessary; mentions dependency on "imaging quality metrics" but does not detail robustness to topologically incorrect geometries.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Cardiac digital twin validation framework highlighting how imaging-derived structural inputs (fibrosis quantification) have inherent variability, how mechanistic models can be iteratively refined through simulation before clinical use, and the importance of fit-for-purpose validation standards—methodological principles directly transferable to coronary FFR validation.
- verdict: FULL
- revisit-if: Already identified for FULL triage; key reference for digital twin methodology and uncertainty in structural model inputs.
