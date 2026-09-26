---
source_pdf_path: Resources/1-s2.0-S004578252200500X-main.pdf
slug: feng-2022-reduced-order-ffr
ledger_status: TRIAGED
---

# feng-2022-reduced-order-ffr

## Bibliographic
- Title: Prediction of fractional flow reserve based on reduced-order cardiovascular model
- First author / authors (first 3 + et al.): Yili Feng, Ruisen Fu, Bao Li, et al.
- Year: 2022
- Venue: Computer Methods in Applied Mechanics and Engineering 400 (2022) 115473
- DOI: 10.1016/j.cma.2022.115473

## One-line claim
Develops a reduced-order (0D) cardiovascular model coupling lumped parameter model and stenosis resistance model to rapidly compute FFR with accuracy comparable to 3D CFD approaches.

## T6 targeted questions

- **Q-A geometry perturbation**: Does NOT perturb or measure segmentation uncertainty. Method is model-based without perturbation analysis.

- **Q-B decision flip**: YES. Reports FFR threshold at 0.8: "Using the clinical cut-off value of FFR (0.8), the accuracy, sensitivity, specificity, positive predictive value and negative predictive value of FFR0D were 89.8%, 79.2%, 92.6%, 73.1% and 94.6%, respectively" (100 patients, 118 lesions).

- **Q-C BC tuning**: YES. Uses Windkessel boundary conditions: "These blocks were developed based the three-element Windkessel (RLC) model [17]". Tuning: "Hyperemic CMR was then quantified by 0.24 times of resting CMR to model the hyperemic conditions [5]." Does NOT report re-tuning after geometry change or statement of error compensation.

- **Q-D fidelity / quantity**: Reduced-order (0D) model only. Does NOT report WSS, OSI, or other spatially-resolved fields. Authors note limitation: "The 0D model cannot fully consider the geometric features in the same way as the 3D model, which may affect coronary hemodynamics to some extent."

- **Q-E data**: 100 patients, 118 lesions, single-center (Peking University People's Hospital), invasive FFR ground truth present (yes). Data not public.

- **Q-F meshing**: Minimal detail. No discussion of segmentation→surface→volume meshing or robustness on poor/broken geometry. Assumes no stenosis in LPM construction then adds stenosis model.

## Novelty bearing on T6

- bucket: METHOD
- one-line reason: Reduced-order modeling technique reusable in T6's CFD pipeline; demonstrates BC tuning (Windkessel) strategy relevant to T6's investigation of boundary condition effects.
- verdict: LIGHT
- revisit-if: Expanded analysis showing how 0D model BC tuning changes with segmentation perturbation or topological error.
