---
source_pdf_path: Resources/1-s2.0-S0021929020301147-main.pdf
slug: gosling-2020-sidebranch-ffr
ledger_status: TRIAGED
---

# gosling-2020-sidebranch-ffr

## Bibliographic
- Title: Effect of side branch flow upon physiological indices in coronary artery disease
- First author / authors: Rebecca C. Gosling, Jacob Sturdy, Paul D. Morris
- Year: 2020
- Venue: Journal of Biomechanics
- DOI: 10.1016/j.jbiomech.2020.109698

## One-line claim
Leakage model based on Murray's law compensates for neglected side branch flow; despite 65% increase in inlet flow when branches included, vFFR accuracy unchanged due to boundary condition tuning.

## T6 targeted questions
- **Q-A geometry perturbation**: Does not perturb lumen or segmentation; instead systematically neglects modeled side branches. Asks: what is the effect of under-representing branching anatomy?
- **Q-B decision flip**: YES—diagnostic accuracy for FFR ≤ 0.80 threshold reported. "Median vFFR for the 1D and 1Dleaky models were 0.91 (0.82–0.95) and 0.92 (0.81–0.96) respectively." Sensitivity, specificity, positive/negative predictive value, overall accuracy on dichotomized data (FFR > or ≤ 0.80) reported. No flip rate given, but 43 of 146 arteries (29%) in gray zone 0.75–0.85; conclusion: "addition of a leakage term had no significant effect on the predictive accuracy of vFFR despite significant differences in the estimated volumetric flow rate."
- **Q-C BC tuning**: CRITICAL. 1D model uses pressure-matching and resistance-matching boundary conditions. Distal outlet resistance (CMVR) is model-specific, tuned from all cases: "The distal boundary represents the distal CMVR, which is unknown... a model-specific resistance (Rmodel) is applied... The value of Rmodel is the average of all CMVR values calculated from the volumetric flow in setting (i) for the given model (1D = 1.23e+10 Pa/m³s⁻¹ and 1Dleaky = 2.42e+10 Pa/m³s⁻¹)." KEY INSIGHT: "Lower outflow in the 1Dleaky model compared with the 1D model results in a higher average CMVR, which effectively tunes the boundary condition to achieve similar predictive accuracy for FFR. Thus the tuning of boundary conditions may obviate differences in predicted FFR that are expected if models predict flows quite different from the unknown physical flow... FFR is therefore unable to predict volumetric flow and, given an unchanged ratio of pressures, FFR will be similarly unchanged." This demonstrates that BC parameter tuning COMPENSATES for geometric (anatomical) under-representation.
- **Q-D fidelity / quantity**: 1D axisymmetric models (1D and 1Dleaky). No 3D CFD. Pressure and volumetric flow predicted; FFR, CFR (coronary flow reserve), CMVR reported. No WSS or OSI.
- **Q-E data**: N=80 patients, 146 arteries (84 LAD, 29 LCX, 31 RCA, 2 intermediate). Invasive coronary angiography + FFR measurement under adenosine-induced hyperemia. Invasive pressure and FFR gold standard. No invasive flow measurement.
- **Q-F meshing**: Single-lumen 1D models reconstructed from 2D angiography (two acquisitions); radius sampled 0.1 mm spacing. No 3D surface mesh or volume mesh. Stenosis detection filter applied. No detail on robustness to topologically incorrect geometry (e.g., bifurcation identification).

## Novelty bearing on T6
- bucket: SUPPORT
- one-line reason: Demonstrates that outlet BC parameter (CMVR) tuning can offset large differences in computed volumetric flow (inlet 1.53→2.52 mL/s, 65% increase) without affecting FFR diagnostic accuracy. Central to T6's hypothesis that BC tuning absorbs/masks upstream geometric error. However, error is branch neglect, not topological segmentation fault (e.g., false bifurcation).
- verdict: FULL
- revisit-if: Already FULL. This paper directly supports T6's premise that BC tuning can compensate for geometric simplifications. T6 should compare: (1) how much topological error (not just branch count) can BC tuning absorb, and (2) is there a threshold where tuning fails?

