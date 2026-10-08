Model: OpenAI Codex (GPT-5). Read-only audit; no files changed.

### 1. Volumetric flow — PARTLY

The design demand is \(562(1.082193\text{ mm})^3=0.712279\) mL/s, using the 0D healthy-reference/EDT inlet radius—not the requested surface radius 1.301 mm or meshed radius 1.710 mm.

From [M1_results.csv](/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_results.csv):

| Case/mode | Inlet / outlet sum (mL/s) | Target sum | Mass imbalance |
|---|---:|---:|---:|
| clean/resistance | 0.711856 / 0.711856 | 0.648971 | −4.35×10⁻⁶% |
| baseline/resistance | 0.681732 / 0.681732 | 0.648971 | +8.60×10⁻⁶% |
| T1/resistance | 0.579621 / 0.579621 | 0.648971 | +4.19×10⁻⁶% |
| all prescribed | 0.648971 / 0.648971 | 0.648971 | ≤2.00×10⁻⁶% |

Every resistance-mode outlet deviation exceeding 1%:

- clean: out_160 +33.49%, out_600 +32.78%, out_742 +1.95%, out_868 +1.71%.
- baseline: out_160 +16.03%, out_600 +15.42%, out_742 +1.96%, out_868 +1.73%.
- T1: out_383 +1.03%, out_558 −43.25%, out_700 +2.02%, out_826 +1.79%.

No prescribed-flow deviation exceeds 1%; imposed-flow errors are approximately \(10^{-6}\%\). Round-trip maxima are 0.00127% clean/baseline and 0.00510% T1 ([M1_roundtrip_*.csv](/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/M1_roundtrip_T1_missed_branch.csv)). Baseline and T1 receive identical territory totals; T1 transfers the deleted branch’s share into out_558.

The area-radius 0D twins give resistance inflows 0.719006, 0.685556 and 0.585213 mL/s—within 1% of 3D. Prescribed twins equal 0.648971 exactly. The manuscript’s BC description is broadly correct, but it does not disclose the outlet deviations; “clean tree’s resistances” is ambiguous because the clean-no-lesion package actually uses lesion-state baseline BCs.

### 2. Flow regime — CONFIRMED

Scan-14 flow is only 0.649–0.712 mL/s (38.9–42.7 mL/min; T1 resistance 34.8 mL/min), versus the stated cohort median 2.1 mL/s and 214 mL/min = 3.567 mL/s anchor. Baseline throat Reynolds number is 123 under resistance and 106 prescribed; T1 resistance is 60. Thus FFR 0.86976 for the synthetic 80% DS lesion is explicitly a low-flow result.

Scan 837 provides relevant sensitivity: at 3.157× demand, lesion-added loss rises 4.74→20.64 mmHg (4.35×), while the arc-40 FFR-like pressure ratio falls 0.944→0.762; healthy reference changes 0.996→0.983 ([STAGE-A-VALIDATION.tex:1427](/mnt/e/Paper6-T6/Paper6-T6/drafts/stageA_validation/STAGE-A-VALIDATION.tex:1427)). This supports strong flow dependence, but cannot numerically correct scan 14: it is another geometry, BC set and mesh, and lacks hyperaemic mesh sensitivity. The reviewer’s low-flow diagnosis holds; using FAME angiographic severity as direct proof is overstated.

### 3. Radius bias — PARTLY

Valid sections give median area-equivalent/centreline-radius ratios 1.179 clean, 1.179 baseline and 1.176 T1; median differences are +0.1408, +0.1365 and +0.1363 mm. The throat is 0.27564 versus 0.23058 mm (+19.5%), confirming the manuscript.

But “shifts absolute FFR but not paired differences” at [main.tex:482](/mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex:482) is not supported quantitatively. Protocol-A T1−baseline is +0.12736 on requested radii, +0.09903 inscribed, +0.08073 area-equivalent and +0.07386 in 3D. Only the direction is robust. Under prescribed flow all remain near zero (−0.00070, −0.00058, −0.00049, −0.00069).

### 4. “Concealment” — CONFIRMED

At the anatomical measurement plane \(s=49.8917\) mm:

- Protocol A: 0.869757→0.943617, Δ=+0.073859.
- Prescribed: 0.892295→0.891606, Δ=−0.000689.

Thus manuscript rounding at [main.tex:399](/mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex:399) is correct. The −0.0007 uses baseline p011 and T1 p010 because deletion renumbers probes; both are marked `measurement`. Comparing p011 labels gives −0.001042 but compares 49.89 with 55 mm and is invalid. At matched positions, the prescribed delta grows downstream: −0.000862 at 55 mm, −0.00121 at 60 mm, −0.00230 at 75 mm, −0.00777 at 110 mm.

The reviewers are correct conceptually: exact per-outlet flow prescription removes the measurement-point error, not conceals it. Current manuscript text already says this. A genuine 3D Protocol-C test requires one global resistance/bed scaling fitted to territory totals, followed by an independently evaluated FFR and residual.

### 5. Other CFD support — PARTLY

The 12.5-µm variants change p011 by +0.00189 and +0.00207; A0 reproduces 0.8697575 exactly. Both exceed \(U_{3D}=0.00055\), so this is sensitivity, not a converged-error estimate. All surfaces fail self-intersection; baseline/T1 fail D3/D4 with poor face-tets 1.43 mm from the throat. Main-text convergence wording is unsupported because original runs did not monitor measurement pressure per iteration; the settling record used an LAD-outlet proxy.

Ranked manuscript risks:

1. Unsupported radius-invariance claim ([main.tex:482](/mnt/e/Paper6-T6/Paper6-T6/drafts/manuscript/main.tex:482)).
2. Low-flow 3D case presented without a scan-14 physiological-flow rerun.
3. Failed D3/D4 and refinement criterion understated in the main text.
4. “Clean” BC terminology obscures lesion-state targets.
5. \(U_{3D}\) comes from an idealized sten70 case and should not be treated as scan-14 uncertainty.

Recommended fixes: report the flow table and deviations; replace “paired differences unaffected” with the four measured deltas; state that prescribed flow corrected FFR at the measurement plane but downstream profiles diverged; disclose D3/D4 and proxy convergence in the main text; add scan-14 ×2–×3-flow and true global-scaling Protocol-C runs.
