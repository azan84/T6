---
source_pdf_path: Resources/fmedt-04-1034801.pdf
slug: tanade-2022-minimal-governing
ledger_status: TRIAGED
---

# tanade-2022-minimal-governing

## Bibliographic
- Title: Analysis identifying minimal governing parameters for clinically accurate in silico fractional flow reserve
- First author / authors (first 3 + et al.): Tanade C, Chen SJ, Leopold JA, Randles A
- Year: 2022
- Venue: Frontiers in Medical Technology
- DOI: 10.3389/fmedt.2022.1034801

## One-line claim
Sobol sensitivity analysis on patient-specific CFD FFR models (N=50) identifies that accurate geometry reconstruction and cardiac output are the dominant drivers of FFR accuracy; Windkessel outlet resistance parameters can be generalized without diagnostic loss.

## T6 targeted questions
- **Q-A geometry perturbation**: NOT REPORTED. No perturbation studies; focuses on parameter sensitivity but not segmentation error magnitude.
- **Q-B decision flip**: YES, FFR ≤0.80 threshold used. Baseline model: sensitivity 89.5%, specificity 93.6%, AUC 0.95 vs invasive FFR (N=50 patients). Semi-streamlined model maintains identical diagnostic performance. Streamlined model (no patient-specific distal location): sensitivity 79.0%, specificity 90.3%, AUC 0.90.
- **Q-C BC tuning**: YES, CRITICAL FINDING. "2-element Windkessel models were used at the outlet boundary conditions...resistances were related to terminal vessel anatomy." Key result: "FFRsemi-streamlined provided identical diagnostic performance with FFRbaseline"—achieved by using patient-specific geometry and cardiac output only, without patient-tuned Windkessel resistances. Quote: "mean arterial pressure, heart rate, and hematocrit did not tangibly influence FFR." Conclusion: "Capturing coronary hemodynamics depended most on accurate geometry reconstruction and cardiac output measurement." Does NOT address whether BC tuning can mask geometric error, but shows generalized outlet resistances sufficient when geometry is accurate.
- **Q-D fidelity / quantity**: 1D + 0D (Windkessel). Couples 1D full coronary tree with Windkessel outlet models; does not report WSS/OSI.
- **Q-E data**: N=50 patients from Brigham and Women's Hospital with invasive FFR gold standard (adenosine hyperemia). Angiography-derived 3D geometry reconstruction.
- **Q-F meshing**: Described. "1D full coronary tree models...vessel centerlines with corresponding hydraulic diameters extracted from reconstructed STL models" with 100 micrometer resolution. No detail on robustness to topologically broken geometry.

## Novelty bearing on T6
- bucket: THREAT
- one-line reason: Demonstrates that outlet BC tuning (Windkessel resistance) is less critical than accurate geometry for FFR diagnosis, potentially undermining T6's hypothesis that BC re-tuning can absorb topological error; suggests geometry dominates outlet boundary behavior.
- verdict: FULL
- revisit-if: Must compare Tanade's sensitivity ranking against T6's segmentation error ranking; if geometry dominance confirmed, may limit T6's claim about BC compensation mechanism.
