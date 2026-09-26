---
source_pdf_path: Resources/ztaf129.pdf
slug: skalidis-2026-digital-twins-review
ledger_status: TRIAGED
---

# skalidis-2026-digital-twins-review

## Bibliographic
- Title: Digital twins and simulations in transcatheter coronary and structural heart interventions
- First author / authors (first 3 + et al.): Ioannis Skalidis, Nikolaos Stalikas, Carlos Collet et al.
- Year: 2026
- Venue: European Heart Journal - Digital Health
- DOI: 10.1093/ehjdh/ztaf129

## One-line claim
Comprehensive review of digital twin platforms (FFRCT, QFR, vFFR, FFRangio, FFRHARVEY) and simulations for coronary interventions, highlighting integration of imaging, CFD, and AI to support pre- and intra-procedural planning and risk stratification.

## T6 targeted questions
- **Q-A geometry perturbation**: Reviews both CT-based and angiography-derived FFR platforms; discusses need for accurate 3D reconstruction; mentions radiomics-based plaque characterization but no inter-observer disagreement quantification.
- **Q-B decision flip**: FFR ≤0.80 threshold extensively discussed; mentions FAVOR III China QFR-guided strategy trials and outcome-level signals; references CLARIFY and other multicenter validations.
- **Q-C BC tuning**: States that "changes (±10%, ±20%, ±30%) in clinical parameters have minimal impact <2% on computed FFRHARVEY"; discusses inlet/outlet boundary condition parameterization for resting vs hyperemic states; does NOT explicitly address whether BC tuning is re-done after geometry perturbation, but emphasizes importance of "accurate 3D reconstruction."
- **Q-D fidelity / quantity**: Discusses spectrum from simplified 1D models to full 3D CFD (lattice Boltzmann in HARVEY); notes WSS, velocity, longitudinal vorticity as additional biomarkers; mentions future integration of volumetric perfusion (V/M ratio) and microvascular resistance (angio-IMR).
- **Q-E data**: Reviews platforms and their published validation studies (FFRCT, QFR, FFRHARVEY validations); specific cohort sizes summarized at platform level, not a single primary study.
- **Q-F meshing**: Discusses reconstruction methods (angiography vs CT); mentions importance of complete coronary tree (full side branches) for accurate secondary hemodynamic metrics; notes that "omitting second/third generation side branches is inadequate"; discusses AI-assisted segmentation and automated coronary tree reconstruction.

## Novelty bearing on T6
- bucket: BACKGROUND
- one-line reason: Comprehensive landscape review of digital twin platforms and FFR simulation methodologies for coronary intervention planning; provides context for existing tools, their strengths/limitations, and emerging AI integration; supports T6 framing within broader clinical simulation ecosystem.
- verdict: LIGHT
- revisit-if: Check cited references to methodological papers on each platform (FFRCT Planner, HARVEY, QFR algorithms) for BC tuning protocols and sensitivity to segmentation error; review sections on model validation and regulatory status.
