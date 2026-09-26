---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2024 - Fernández‐Martínez - Impact of minimal lumen segmentation uncertainty on patient‐specific.pdf
slug: fernandez-martinez-2024-segmentation-uncertainty-ffr
ledger_status: TRIAGED
---

# fernandez-martinez-2024-segmentation-uncertainty-ffr

## Bibliographic
- Title: Impact of minimal lumen segmentation uncertainty on patient-specific coronary simulations: A look at FFRCT
- First author / authors (first 3 + et al.): Daniel Fernández-Martínez, María Reyes González-Fernández, Juan Manuel Nogales-Asensio
- Year: 2024
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.3822

## One-line claim
Segmentation threshold variations (intra-operator 6%, inter-operator 15%) on CT lumen masks propagate nonlinearly into FFR-CT errors that are location- and severity-dependent; sensitivity increases distally and worsens at 0.80 threshold.

## T6 targeted questions
- **Q-A geometry perturbation**: REAL inter-operator and intra-operator threshold variations measured from clinical CT segmentation (6% intra, 15% inter). Reported as two separate threshold shifts (±6 HU intra, ±30 HU inter on 200 HU baseline).
- **Q-B decision flip**: YES, FFR reclassification near 0.80 threshold reported. "Cases with moderate or severe distal coronary lesions should undergo either exact and thorough segmentation operations or invasive FFR measurements, particularly if the FFRCT is close to the cutoff (0.80)." Moderate distal lesion: 50% stenosis → FFR 0.924 to 0.919 (±0.005 inter-op), severe distal 70% → FFR 0.879 to 0.860 (±0.019 inter-op). Near-threshold cases critical.
- **Q-C BC tuning**: "This tuning process was performed automatically for each patient segmentation threshold because branch diameters differ depending on the threshold considered. According to Murray's law, the vessel-specific resistances change with their diameter, and an update is required." BC tuning WAS re-done after geometry changes; outlets updated automatically per Murray's law.
- **Q-D fidelity / quantity**: 3D-0D CFD transient simulations (3D vessel geometry coupled to lumped 0D Windkessel periphery). Pressure fields computed; NO WSS/OSI reported.
- **Q-E data**: 14 patient-specific coronary models enrolled, invasive FFR ground truth present (measured 2 cm distal to stenosis during catheterization).
- **Q-F meshing**: Segmentation via 3D Slicer software using hybrid thresholding + region-growing algorithm; uncertainty quantified by varying threshold; no detail on mesh robustness to topology failure.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Directly validates T6's premise: real segmentation disagreement causes FFR uncertainty, especially near 0.80 threshold; demonstrates that BC re-tuning per Murray's law occurs but does not fully mask geometry error.
- verdict: FULL
- revisit-if: N/A – already gate-relevant evidence for T6.
