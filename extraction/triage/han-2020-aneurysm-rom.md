---
source_pdf_path: Resources/1-s2.0-S0021929020300609-main.pdf
slug: han-2020-aneurysm-rom
ledger_status: TRIAGED
---

# han-2020-aneurysm-rom

## Bibliographic
- Title: A reduced-order model of a patient-specific cerebral aneurysm for rapid evaluation and treatment planning
- First author / authors: Suyue Han, Clemens M. Schirmer, Yahya Modarres-Sadeghi
- Year: 2020
- Venue: Journal of Biomechanics
- DOI: 10.1016/j.jbiomech.2020.109653

## One-line claim
POD-based ROM for patient-specific cerebral aneurysm enables parametric study of WSS and OSI sensitivity to pulsatility index without repetitive full CFD.

## T6 targeted questions
- **Q-A geometry perturbation**: No segmentation uncertainty perturbations. Single patient-specific geometry from CTA.
- **Q-B decision flip**: Not relevant (cerebral aneurysm rupture risk, not coronary FFR threshold).
- **Q-C BC tuning**: Inlet pulsatile waveform scaled by parameter ε(t) to vary pulsatility index PI ∈ [0.5, 1.1]. Outlet not explicitly detailed beyond CFD solver defaults. No evidence of BC re-tuning after geometry change; no discussion of tuning compensating for geometric error.
- **Q-D fidelity / quantity**: 3D CFD (OpenFOAM pisoFOAM) + POD-based ROM. Wall shear stress (WSS) and oscillatory shear index (OSI) computed; 5 POD modes capture 99.8% energy for this case. Sensitivity to PI parameterized.
- **Q-E data**: Single patient-specific cerebral aneurysm (CT angiography). No invasive ground truth (aneurysm hemodynamics not invasively measured).
- **Q-F meshing**: VMTK for segmentation; ANSYS ICEM for volume mesh. Three-layer prism layer; mesh convergence study per case. Boundary layer mesh 1–3×10⁻⁴ mm. No detail on robustness to topologically incorrect aneurysm geometry.

## Novelty bearing on T6
- bucket: IRRELEVANT
- one-line reason: Cerebral aneurysm pathology; not coronary. POD-ROM methodology may be transferable, but findings on aneurysm rupture risk and WSS/OSI do not apply to coronary FFR or segmentation error ranking.
- verdict: LIGHT
- revisit-if: If T6 adopts POD-ROM for coronary sensitivity studies, revisit for ROM mode interpretation and error scaling under parameter variations, but core pathophysiology is distinct.

