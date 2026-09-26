---
source_pdf_path: Resources/Numer Methods Biomed Eng - 2025 - Yildirim - Single‐Phase Blood Flow in a Stenosed Coronary Artery  A Clinical Model‐Based.pdf
slug: yildirim-2025-blood-flow-stenosis
ledger_status: TRIAGED
---

# yildirim-2025-blood-flow-stenosis

## Bibliographic
- Title: Single-Phase Blood Flow in a Stenosed Coronary Artery: A Clinical Model-Based Experimental and Numerical Study
- First author / authors (first 3 + et al.): Orhan Yildirim, Sendogan Karagoz, Fatin Sonmez
- Year: 2025
- Venue: International Journal for Numerical Methods in Biomedical Engineering
- DOI: 10.1002/cnm.70102

## One-line claim
Experimental validation and CFD simulation of pulsatile non-Newtonian blood flow in idealized stenosed coronary arteries (0% and 65% blockage) demonstrate location-dependent WSS, pressure drop, and energy dissipation sensitive to pulse rate and blood rheology.

## T6 targeted questions
- **Q-A geometry perturbation**: SYNTHETIC. Idealized geometries from CT templates (healthy 0% vs. diseased 65% stenosis); no inter-segmenter variation introduced.
- **Q-B decision flip**: YES, FFR threshold analysis. "Fractional flow reserve (FFR) analysis confirmed that a 65% luminal narrowing poses significant hemodynamic risk." FFR implications discussed but specific 0.80 threshold crossing not quantified numerically.
- **Q-C BC tuning**: Inlet: prescribed pulsatile flow waveforms (6 pulse rates: 72–156 bpm). Outlets: NOT SPECIFIED; assumed zero-pressure or similar. No BC tuning mentioned; fixed per simulation.
- **Q-D fidelity / quantity**: 3D CFD (ANSYS Fluent) with Casson non-Newtonian blood model. WSS computed and reported: "The highest wall shear stress (WSS) values were localized in the stenotic region." WSS sensitivity to flow rate and fluid properties emphasized; no geometry sensitivity for WSS studied.
- **Q-E data**: Idealized arterial models only (no patient cohort, no invasive FFR ground truth).
- **Q-F meshing**: Geometries from CT segmentation (no detail on segmentation method or robustness).

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Validates CFD methodology for coronary stenosis hemodynamics under pulsatile non-Newtonian conditions; establishes baseline WSS/pressure profiles. No geometry error or BC compensation analysis.
- verdict: LIGHT
- revisit-if: Extends to real patient geometries with segmentation uncertainty and analyzes WSS/FFR sensitivity to geometry vs. BC changes.
