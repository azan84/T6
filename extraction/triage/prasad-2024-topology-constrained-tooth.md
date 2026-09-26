---
source_pdf_path: Resources/2605.04201v2.pdf
slug: prasad-2024-topology-constrained-tooth
ledger_status: TRIAGED
---

# prasad-2024-topology-constrained-tooth

## Bibliographic
- Title: Topology-Constrained Quantized nnUNet for Efficient and Anatomically Accurate 3D Tooth Segmentation
- First author / authors (first 3 + et al.): Paarth Prasad, Ruchika Malhotra
- Year: 2024 (arXiv preprint)
- Venue: arXiv preprint
- DOI: NOT REPORTED

## One-line claim
Proposes a quantization-aware training framework integrating topological constraints into nnUNet for efficient and anatomically accurate 3D tooth segmentation from CBCT scans.

## T6 targeted questions
- **Q-A geometry perturbation**: Does not address coronary artery geometry perturbation or lumen uncertainty measurement. Application domain is dental (tooth) segmentation. NOT REPORTED for T6 context.
- **Q-B decision flip**: No diagnostic decision threshold or FFR-like binary classification reported. NOT REPORTED.
- **Q-C BC tuning**: Not applicable; no CFD, outlet boundary conditions, or Windkessel models discussed. NOT REPORTED.
- **Q-D fidelity / quantity**: 3D segmentation of tooth structures; no CFD or WSS/OSI reported. NOT REPORTED.
- **Q-E data**: CBCT dataset; dental application; no invasive ground truth or FFR data. NOT REPORTED.
- **Q-F meshing**: Addresses segmentation robustness under quantization-induced topological errors (fragmented segments, incorrect adjacency). Emphasis on preserving anatomical topology (tooth count, adjacency, cavity integrity) but applied to dental not vascular geometry. NOT REPORTED for coronary artery context.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Dental imaging segmentation with no bearing on coronary artery FFR or digital twin validation methodology.
- verdict: LIGHT
- revisit-if: Paper focused on dental CBCT; no plausible connection to coronary artery segmentation or FFR validation.
- possible-other-project: Medical image segmentation, dental imaging, quantization-aware training for anatomically accurate segmentation.
