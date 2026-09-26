---
source_pdf_path: Resources/applsci-12-05573-v2.pdf
slug: gamage-2022-fractional-flow
ledger_status: TRIAGED
---

# gamage-2022-fractional-flow

## Bibliographic
- Title: Fractional Flow Reserve (FFR) Estimation from OCT-Based CFD Simulations: Role of Side Branches
- First author / authors: Peshala T. Gamage, Pengfei Dong, Juhwan Lee
- Year: 2022
- Venue: Applied Sciences, vol. 12, no. 11
- DOI: 10.3390/app12115573

## One-line claim
Investigates the effect of side branches (diameter and location) on FFR estimation using both idealized and OCT-reconstructed coronary models with electrical analogy (resistance modeling) approach.

## T6 targeted questions
- **Q-A geometry perturbation**: Geometric variations in side branch diameter and location tested. Not inter-observer disagreement but systematic geometric sensitivity. Text: "the effect of the side branches on FFR estimation was inspected with both idealized and optical coherence tomography (OCT)-reconstructed coronary artery models."
- **Q-B decision flip**: Outcome sensitivity to geometry reported. Text: "Results have shown that the side branches decrease the total resistance of the vessel tree, resulting in a higher inlet flowrate. The side branches located at the downstream of the stenosis led to a lower FFR value, while the ones at the upstream had a minimal impact on the FFR estimation." Implies FFR values change but threshold-crossing rate not quantified.
- **Q-C BC tuning**: Implicit via outlet resistance model. Text: "The electrical analogy of blood flow was further used to understand the impact of the side branches (diameter and location) on FFR estimation." Side branches reduce vessel tree resistance, affecting overall outlet conditions. Quote: "side branches decrease the total resistance of the vessel tree, resulting in a higher inlet flowrate." No explicit BC re-tuning after geometry change but demonstrates that geometric features (side branches) alter effective outlet resistance.
- **Q-D fidelity / quantity**: 3D CFD with electrical analogy (resistance network). No explicit WSS/OSI extraction reported.
- **Q-E data**: Idealized and OCT-reconstructed coronary models (dataset name NOT REPORTED, N NOT REPORTED). No invasive FFR ground truth mentioned.
- **Q-F meshing**: OCT-based surface reconstruction used; no meshing robustness analysis on poor geometry reported.

## Novelty bearing on T6
- bucket: METHOD
- one-line reason: Demonstrates that geometric details (side branch presence/size) alter the effective outlet resistance and propagate as FFR changes; relevant to T6's geometric error sensitivity hypothesis—shows one aspect of how anatomy alterations affect FFR predictions via resistance changes.
- verdict: LIGHT
- revisit-if: If paper includes quantitative analysis of how FFR flip rate varies with side branch perturbation magnitude or shows that side branch error can be masked by outlet resistance tuning.
