---
source_pdf_path: Resources/CVIA.2025.0020.pdf
slug: chen-2025-eecp-multiscale
ledger_id: C021
ledger_status: TRIAGED
---

# chen-2025-eecp-multiscale

## Bibliographic
- Title: Hemodynamic Evaluation of an Enhanced External Counterpulsation Strategy for Coronary Heart Disease with a Geometric Multiscale Model
- First author / authors: Sihan Chen, Mingjie Sun, Yangyang Chen, Youjun Liu, Jianhang Du, Bao Li
- Year: 2025
- Venue: Cardiovascular Innovations and Applications, Vol. 10 (2025), ISSN 2009-8618
- DOI: 10.15212/CVIA.2025.0020

## One-line claim
Develops a geometric multiscale model coupling 0D lumped-parameter circulation with 3D patient-specific coronary artery model to evaluate enhanced external counterpulsation (EECP) effectiveness, identifying wall shear stress (WSS) as a critical hemodynamic endpoint.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED on segmentation uncertainty or inter-observer variability
- **Q-B decision flip**: NOT REPORTED for FFR reclassification. Uses diastolic-to-systolic pressure ratio (DBP/SBP) as clinical surrogate; optimized EECP increased DBP/SBP from 0.88 to 1.25.
- **Q-C BC tuning**: YES, core methodology. Couples 0D and 3D via "boundary flow and pressure information at each time step"; 3D model includes "ten major coronary branches, each connected to a downstream 0D outlet model"; tuning variables include "inflation timing, deflation moment, and pressure amplitude"; states "multiscale model enables comprehensive analysis of local and systemic hemodynamic responses."
- **Q-D fidelity / quantity**: Both 0D and 3D. "0D lumped-parameter model...coupled with...3D coronary artery model." Explicitly reports WSS (wall shear stress: 3.25 Pa→6.51 Pa) and OSI (oscillatory shear index: "remained relatively stable across all tested configurations"). Spatial WSS/OSI fields computed in 3D domain.
- **Q-E data**: Patient-specific coronary artery model reconstructed from computed tomography of healthy adult (N=1). No clinical cohort; no invasive FFR ground truth.
- **Q-F meshing**: "3D model was constructed from computed tomography data...meshed by using high-resolution hexahedral elements" in ANSYS-CFX. Limited detail on segmentation-to-surface-to-volume workflow or robustness to poor/broken geometry.

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates 0D/3D multiscale coupling with explicit BC exchange at each time step; reports WSS/OSI sensitivity to control variables; validates multiscale architecture for coronary hemodynamics
- verdict: FULL
- revisit-if: Not needed; strong methodological fit to T6's framework

## Ideation opening
Paper states "multiscale model offers a flexible framework for future patient-specific modeling, which might enable personalized optimization...according to individual anatomy and physiology," but does not address how segmentation error or geometric uncertainty propagates through the BC tuning to affect downstream WSS/OSI predictions.
