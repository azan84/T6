---
source_pdf_path: Resources/Physics-Informed_Neural_Networks_for_Brain_Hemodynamic_Predictions_Using_Medical_Imaging.pdf
slug: sarabian-2022-physics-informed
ledger_status: TRIAGED
---

# sarabian-2022-physics-informed

## Bibliographic
- Title: Physics-Informed Neural Networks for Brain Hemodynamic Predictions Using Medical Imaging
- First author / authors: Mohammad Sarabian, Hessam Babaee, Kaveh Laksari
- Year: 2022
- Venue: IEEE Transactions on Medical Imaging, vol. 41, no. 9
- DOI: NOT REPORTED (available in text as IEEE Trans. Med. Imag., vol. 41, no. 9, Sep. 2022)

## One-line claim
Proposes a physics-informed deep learning framework that augments sparse clinical measurements with 1D reduced-order model (ROM) simulations to generate brain hemodynamic parameters, handling uncertainty in inlet/outlet boundary conditions.

## T6 targeted questions
- **Q-A geometry perturbation**: Synthetic perturbations only. Text: "We show this capability by generating synthetic blood flow data after cerebral vasospasm at various levels of stenosis." NOT measured inter-observer disagreement.
- **Q-B decision flip**: NOT REPORTED. No diagnostic threshold reclassification studied.
- **Q-C BC tuning**: Yes, addresses BC limitations. Key quote: "high accuracy despite lacking knowledge of inlet and outlet boundary conditions, which is a significant limitation for the accuracy of the conventional purely physics-based computational models." The method operates with sparse boundary conditions, not re-tuning after geometry change. This demonstrates reduced-order models can work with incomplete BC specification.
- **Q-D fidelity / quantity**: Reduced-order (1D ROM combined with deep learning). Validated against 4D flow MRI. No WSS/OSI reported explicitly (brain application, not coronary).
- **Q-E data**: Brain vasculature from TCD ultrasound and 3D angiography (dataset name NOT REPORTED). N = NOT REPORTED. Private clinical data. No invasive ground truth for brain (validation against 4D MRI).
- **Q-F meshing**: NOT REPORTED.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates that physics-informed ROMs can deliver accurate predictions despite incomplete/sparse boundary condition information, providing evidence that BC uncertainty is not insurmountable with appropriate learning architectures.
- verdict: LIGHT
- revisit-if: If paper includes quantitative sensitivity analysis on BC uncertainty or explicit comparison of outcomes with different BC specifications.
