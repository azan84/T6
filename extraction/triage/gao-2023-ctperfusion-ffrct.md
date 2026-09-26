---
source_pdf_path: Resources/jcm-12-02154-v2.pdf
slug: gao-2023-ctperfusion-ffrct
ledger_status: TRIAGED
---

# gao-2023-ctperfusion-ffrct

## Bibliographic
- Title: A Novel CT Perfusion-Based Fractional Flow Reserve Algorithm for Detecting Coronary Artery Disease
- First author / authors (first 3 + et al.): Xuelian Gao, Rui Wang, Zhonghua Sun
- Year: 2023
- Venue: Journal of Clinical Medicine
- DOI: 10.3390/jcm12062154

## One-line claim
Novel CTP-FFR model combining CT perfusion (myocardial blood flow) with CFD to improve boundary condition accuracy and reduce FFR-CT error.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. Studies mild/moderate/severe stenosis categories but does not quantify inter-segmenter disagreement.
- **Q-B decision flip**: YES. Uses FFR ≤0.80 threshold; reports sensitivity 0.87, specificity 0.88, AUC 0.953 on 103 vessels; higher specificity than CCTA alone (0.88 vs. 0.54 for ≥50% stenosis).
- **Q-C BC tuning**: EXTENSIVELY DISCUSSED. Key quote: "Traditional FFR-CT based on computational fluid dynamics (CFD) and deep learning relies on a population-averaged physiological hypothesis model to estimate exit resistance to simulate boundary conditions. However, due to individual differences between patients, this quantification and distribution of total coronary blood flow can affect coronary exit resistance and therefore the accuracy of FFR-CT." Also: "MBF within the myocardial perfusion territory can directly quantify the total coronary blood flow better simulating the boundary conditions of FFR-CT" and "focusing on outlet resistance to improve boundary conditions may lead to the discovery of more experimental work on the cardiovascular system."
- **Q-D fidelity / quantity**: YES. 3D CFD model; discusses outlet resistance tuning; Pearson correlation with invasive FFR 0.89 reported; no WSS/OSI extraction mentioned.
- **Q-E data**: 93 patients, 103 vessels, invasive FFR gold standard within 2 weeks; public or private site unclear but Beijing Anzhen Hospital.
- **Q-F meshing**: NOT REPORTED. No meshing or solver detail provided.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Novel CTP-FFR approach explicitly targets boundary condition improvement by using patient-specific myocardial perfusion to estimate outlet resistance rather than population averages; directly addresses Q-C concern that BC tuning masks geometric error.
- verdict: FULL
- revisit-if: Validation on poor segmentations or topologically incorrect geometries; quantified sensitivity of FFR to outlet BC perturbation; comparison with fixed-BC FFR-CT.
