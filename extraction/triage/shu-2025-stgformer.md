---
source_pdf_path: Resources/Gated-STGFormer_Spatiotemporal_Fusion_Network_for_Reconstructing_Aortic_Valve_Motion_Within_Coronary_Presence.pdf
slug: shu-2025-stgformer
ledger_id: C023
ledger_status: TRIAGED
---

# shu-2025-stgformer

## Bibliographic
- Title: Gated-STGFormer: Spatiotemporal Fusion Network for Reconstructing Aortic Valve Motion Within Coronary Presence
- First author / authors: Peng Shu, Daochun Li, Rui Lv, Yongkang Lee, Lingqi Kong, Shiwei Zhao, Jinwu Xiang
- Year: 2025
- Venue: IEEE Journal of Biomedical and Health Informatics, Vol. 29, No. 12, December 2025
- DOI: 10.1109/JBHI.2025.3611504

## One-line claim
Proposes Gated-STGFormer, a Graph Convolutional Network and Transformer-based deep learning framework to predict coronary-modulated aortic valve leaflet motion from simplified FSI simulations that omit coronary artery structures.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED
- **Q-B decision flip**: NOT REPORTED
- **Q-C BC tuning**: Partial relevance. Paper notes "incorporating coronaries into FSI simulations poses two challenges: their geometric complexity increases computational cost, and the lack of well-defined boundary conditions limits clinical applicability." Uses FSI simulations (which require BCs) but does not discuss explicit BC tuning strategies.
- **Q-D fidelity / quantity**: FSI (2D, simplified). Paper acknowledges "2D FSI dataset offers computational efficiency, yet it falls short in accurately representing the complex 3D structure of the valve." Mentions valve shear stress distribution but does not explicitly report WSS/OSI values in extracted text. States "coronary flow...plays a role in regulating shear stress distribution and turbulence characteristics."
- **Q-E data**: 2D FSI simulations only (not clinical data). States "Current clinical imaging techniques...still face limitations in resolution, continuity, and annotation, which restrict the availability of high-quality training data." No invasive FFR ground truth.
- **Q-F meshing**: Limited detail. Mentions FSI simulations use "valve finite element mesh points" and tests robustness to mesh discretization ("evaluated multiple subsampling rates...producing 85, 57, 22, and 15 nodes...prediction accuracy remained consistent"). No discussion of segmentation-to-surface-to-volume meshing workflow or handling poor/topologically incorrect geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Addresses systematic bias from anatomical simplifications in FSI (omitted coronary geometry); uses ML surrogate to compensate for simplified physics; demonstrates that geometry/structural omissions cause predictable errors
- verdict: LIGHT
- revisit-if: Paper validates model predictions against full FSI with coronaries, demonstrating error magnitude from anatomical omission; traces sensitivity of hemodynamic outputs (WSS/OSI) to predicted valve motion

## Ideation opening
Paper explicitly states "Conventional FSI models tend to neglect modeling coronary arteries due to their complexities, leading to bias in leaflet motion simulations" and notes omissions cause "systematic bias in predicted valve motion," directly supporting T6's premise that geometric simplifications/errors propagate through simulations; however, addresses this via deep learning compensation rather than error quantification or BC tuning analysis.
