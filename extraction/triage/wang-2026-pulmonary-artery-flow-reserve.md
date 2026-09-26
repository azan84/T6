---
source_pdf_path: Resources/wang-et-al-2026-evaluation-of-pulmonary-artery-flow-reserve-in-patients-with-chronic-thromboembolic-pulmonary.pdf
slug: wang-2026-pulmonary-artery-flow-reserve
ledger_status: TRIAGED
---

# wang-2026-pulmonary-artery-flow-reserve

## Bibliographic
- Title: Evaluation of Pulmonary Artery Flow Reserve in Patients With Chronic Thromboembolic Pulmonary Hypertension: A Pilot Study
- First author / authors (first 3 + et al.): Jinzhi Wang, Linfeng Xi, Xincao Tao et al.
- Year: 2026
- Venue: Journal of the American Heart Association
- DOI: 10.1161/JAHA.125.047624

## One-line claim
Angiography-derived pulmonary artery flow reserve (PFR), calculated via CFD without distal pressure-wire advancement, achieves high agreement with invasive FFR for physiologic assessment of pulmonary artery stenoses in chronic thromboembolic pulmonary hypertension.

## T6 targeted questions
- **Q-A geometry perturbation**: Patient-specific pulmonary artery geometry from selective pulmonary angiography (2 projections, ≥25 degree angular separation); no synthetic perturbation.
- **Q-B decision flip**: FFR ≤0.80 threshold (transferred from coronary to pulmonary artery context); PFR vs pressure-wire FFR: AUC 0.981, sensitivity 94.1%, specificity 87.5%, optimal PFR cutoff 0.77; 3-month follow-up maintained AUC 0.985; r=0.970, P<0.001.
- **Q-C BC tuning**: Proximal pressure (Pa) measured at target vessel ostium; flow velocity estimated by frame counting; pressure drop (ΔP) computed by proprietary CFD; PFR=(Pa − ΔP)/Pa. No explicit re-tuning after geometry change mentioned.
- **Q-D fidelity / quantity**: Reduced-order CFD approach (not full 3D lattice Boltzmann); 3D mesh reconstruction from angiography; does not report WSS or OSI.
- **Q-E data**: Prospective observational study, 29 patients with 52 vessels; CTEPH diagnosis; ring-like, web, and subtotal lesion types; invasive FFR gold standard; 3-month follow-up in 45 vessels (24 patients).
- **Q-F meshing**: 3D mesh reconstruction from 2D pulmonary angiographic images along vessel path from entrance to ≥1 cm downstream of farthest stenosis; quality control criteria for reconstruction applied (typically types A–C; type D/E excluded).

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Demonstrates angiography-derived FFR-like computation (PFR) on pulmonary rather than coronary arteries; methodology and CFD principles transferable but domain-specific (pulmonary hypertension, not coronary stenosis evaluation for revascularization).
- verdict: LIGHT
- revisit-if: If T6 extends to generalized vascular flow assessment; check whether multiscale/reduced-order hemodynamic models for CTEPH cited (refs 23–24) include segmentation robustness analysis.
