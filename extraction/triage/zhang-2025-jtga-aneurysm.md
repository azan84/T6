---
source_pdf_path: Resources/A_Joint_Geometric_Topological_Analysis_Network_JGTA-Net_for_Detecting_and_Segmenting_Intracranial_Aneurysms.pdf
slug: zhang-2025-jtga-aneurysm
ledger_id: C019
ledger_status: TRIAGED
---

# zhang-2025-jtga-aneurysm

## Bibliographic
- Title: A Joint Geometric Topological Analysis Network (JGTA-Net) for Detecting and Segmenting Intracranial Aneurysms
- First author / authors: Xinyue Zhang, Zonghan Lyu, Yang Wang, Bo Peng, Jingfeng Jiang
- Year: 2025
- Venue: IEEE Transactions on Biomedical Engineering, Vol. 72, No. 12, December 2025
- DOI: 10.1109/TBME.2025.3572837

## One-line claim
Proposes JGTA-Net, a point-cloud-based deep learning network combining persistent homology and geometric feature learning for automated detection and segmentation of intracranial aneurysms from medical imaging.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED
- **Q-B decision flip**: NOT REPORTED
- **Q-C BC tuning**: NOT REPORTED
- **Q-D fidelity / quantity**: NOT REPORTED for CFD. This is an imaging-based segmentation network (point clouds from MRA and X-ray rotational angiography). No CFD simulation, WSS/OSI, or hemodynamic computation reported.
- **Q-E data**: IntrA dataset (public; point clouds from MRA) plus two internal validation datasets (from X-ray rotational angiography). Dataset size N not specified; no invasive FFR ground truth.
- **Q-F meshing**: NOT REPORTED. Paper mentions "triangulated vessel surfaces obtained through semi-automated segmentation" but provides no detail on segmentation-to-mesh generation or robustness to poor geometry.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Deep learning segmentation network for aneurysm detection; no CFD, hemodynamics, BC tuning, or geometry error quantification
- verdict: LIGHT
- revisit-if: Paper demonstrates integration of segmentation output with hemodynamic/CFD modeling pipeline or error propagation analysis

## Ideation opening
Paper acknowledges that "aneurysmal hemodynamics plays an important role in the natural history of IAs" and proposes IA segmentation "can be used to delineate the extent of an IA for the automated computation of hemodynamic and morphological parameters," but does not address how segmentation error or geometric uncertainty propagates into hemodynamic predictions or CFD results.
