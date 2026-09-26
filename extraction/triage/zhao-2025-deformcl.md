---
source_pdf_path: Resources/DeformCL_Learning_Deformable_Centerline_Representation_for_Vessel_Extraction_in_3D_Medical_Image.pdf
slug: zhao-2025-deformcl
ledger_id: C022
ledger_status: TRIAGED
---

# zhao-2025-deformcl

## Bibliographic
- Title: DeformCL: Learning Deformable Centerline Representation for Vessel Extraction in 3D Medical Image
- First author / authors: Ziwei Zhao, Zhixing Zhang, Yuhang Liu, Zhao Zhang, Haojun Yu, Dong Wang, Liwei Wang
- Year: 2025
- Venue: 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)
- DOI: 10.1109/CVPR52734.2025.02877

## One-line claim
Proposes DeformCL, a continuous deformable centerline representation for accurate 3D vessel segmentation that learns to iteratively deform template centerlines to match curvilinear vessel structures in medical images.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED
- **Q-B decision flip**: NOT REPORTED
- **Q-C BC tuning**: NOT REPORTED
- **Q-D fidelity / quantity**: NOT REPORTED for CFD. Pure segmentation task; no hemodynamic simulation, WSS/OSI, or 3D flow computation. However, paper notes centerlines are "indispensable component in various subsequent diagnostic tasks, such as curved planar reformation and computational hemodynamics."
- **Q-E data**: Multiple 3D medical imaging datasets (HaN-Seg, ASOCA, and comparative benchmarks). No clinical cohort with invasive FFR ground truth.
- **Q-F meshing**: NOT REPORTED for CFD meshing. Discusses centerline extraction from segmentation via "minimum spanning tree algorithm" followed by adaptive template deformation. No detail on segmentation-to-surface-to-volume mesh generation or robustness to poor/topologically incorrect geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Deep learning vessel segmentation producing continuous centerlines; downstream applicability to computational hemodynamics but no analysis of segmentation error impact on CFD predictions
- verdict: LIGHT
- revisit-if: Paper validates segmentation against ground truth annotations, demonstrating inter-observer variability, or traces error propagation from segmentation to downstream CFD hemodynamics

## Ideation opening
Paper states "the traditionally complex and time-consuming continuous centerlines extraction from segmentation for curved planar reformation is eliminated" by direct DeformCL prediction, suggesting potential for reducing errors in segmentation-dependent workflows, but does not examine how residual segmentation errors propagate into hemodynamic simulations or CFD results.
