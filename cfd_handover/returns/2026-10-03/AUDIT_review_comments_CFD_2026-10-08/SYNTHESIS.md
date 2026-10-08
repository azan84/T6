# Blind-review comments on CFD accuracy vs the scan-14 simulation files: synthesis (2026-10-08)
Auditors: GPT-5.6 Sol (codex, read-only), Gemini 3.7 Flash medium (agy, read-only), plus my own independent checks. Raw outputs: AUDIT_*.md; brief: BRIEF.md. No manuscript or simulation file was changed.

## Verdicts
| Reviewer comment | Verdict | Evidence (scan 14, returns/2026-09-26) |
|---|---|---|
| Domain W1: hyperaemic flow too low; 3D case is a low-flow regime | CONFIRMED | 3D inlet flow 0.649 (prescribed) to 0.712 (clean, resistance) mL/s = 39-43 mL/min (T1 resistance 35); 3.6x-5.5x below the 214 mL/min anchor, ~3x below the cohort median 2.1 mL/s; Re_throat 123 (resistance) / 106 (prescribed), T1 60. FFR 0.870 for an 80 % DS lesion is a low-flow result. |
| Domain W1: radius bias | CONFIRMED, text claim too strong | meshed area-equivalent radius exceeds the requested radius by a median 0.137-0.141 mm (ratio 1.18); throat 0.2756 vs 0.2306 mm (+19.5 %); the manuscript's 0.14 mm and 0.276/0.231 are right. But "shifts absolute FFR but not the paired differences" (main.tex ~482) is NOT supported quantitatively: Protocol A delta(T1-baseline) is +0.127 (requested radii), +0.099 (inscribed), +0.081 (area-equivalent 0D twin), +0.074 (3D): only the direction is robust. Under prescribed flow all stay near zero (-0.0007 to -0.0005). |
| Domain W2 / Methodology W1: the 3D case shows removal of the FFR error, not concealment | CONFIRMED (conceptually) | Protocol A: 0.869757 -> 0.943617 (+0.0739). Prescribed: 0.892295 -> 0.891606 (-0.00069) at the same anatomical plane (s = 49.89 mm). Per-outlet flow prescription fixes the transstenotic flow; one global scaling (Protocol C) was never run in 3D, so the 3D case cannot support "concealment". |
| (my own lead) manuscript's -0.0007 is wrong, p011 gives -0.0010 | REFUTED | the T1 tree has renumbered probes (two bifurcation probes deleted): the measurement plane is p011 in baseline but p010 in T1; comparing p011 with p011 compares 49.9 mm with 55 mm. Matched planes give -0.00069, so the manuscript's -0.0007 is correct. At matched positions the prescribed-flow difference grows downstream (-0.0009 at 55 mm, -0.0023 at 75 mm, -0.0078 at 110 mm). |

## Volumetric flow accuracy (the point the user asked about)
- Mass conservation: inlet = sum of outlets in every solve, imbalance <= 9e-6 %.
- Prescribed-flow BC: outlet flows equal the target to < 1e-4 %, round-trip errors 0.0013 % (clean, baseline) and 0.0051 % (T1); baseline and T1 receive identical territory totals; prescribed total 0.648971 mL/s in all three prescribed cases.
- Resistance mode (Protocol A) outlet deviations from the targets > 1 %: baseline out_160 +16.0 %, out_600 +15.4 %, out_742 +2.0 %, out_868 +1.7 %; clean out_160 +33.5 %, out_600 +32.8 %; T1 out_558 -43.3 % (the deleted branch's share). These follow from fixed resistances on a wider meshed lumen and are not reported in the manuscript.
- Inlet flow in resistance mode differs from the prescribed total: clean 0.712, baseline 0.682, T1 0.580 vs 0.649 mL/s (+9.7 %, +5.0 %, -10.7 %).
- Demand radius: demand = 562*r_ref^3 with r_ref = 1.082 mm (0D reference radius) = 0.712 mL/s, which the clean 3D resistance solve reproduces (0.7119). The segmentation-requested inlet radius is 1.301 mm and the meshed area-equivalent inlet radius is 1.710 mm (diameter 3.4 mm); the same law on the meshed radius would give 2.81 mL/s, i.e. the 3D case runs ~4x below Murray on its own lumen. The manuscript does not say which radius defines r_in for the 3D case nor the 3D flow.
- The "clean" prescribed flows are lesion-state flows (baseline BCs; total 0.649 mL/s, -8.8 % vs the no-lesion demand), also for the clean-no-lesion package: the manuscript's wording "clean tree's resistances / clean territory flows" is ambiguous.
- 0D area-radius twins give resistance inflows 0.719, 0.686, 0.585 mL/s, within 1 % of 3D.

## Other support issues the auditors found (not reviewer comments)
- Task A: halving the throat cells shifts p011 by +0.0019 / +0.0021, 3.4-3.8x the pre-registered criterion U_3D = 0.00055 (criterion failed; A0 control reproduces the value exactly); the manuscript quotes the shifts but not the failure; U_3D itself comes from the idealised sten70 tube, not scan 14.
- Baseline and T1 fail the strict D3/D4 mesh rule (flagged face-tets 1.43 mm from the throat) and all surfaces fail the self-intersection check; convergence of scan 14 was monitored on an outlet-pressure proxy, not the measurement pressure.
- agy's remark about "Domain W13" and the cohort-median wording rest on an older text and are not used.

## What the data allow, and what they do not
- The reviewers' two CFD criticisms are right: the 3D case is a low-flow case and it cannot show concealment.
- The scan-837 hyperaemic pair (3.16x flow: lesion-added loss 4.74 -> 20.64 mmHg, 4.35x) shows the strong flow dependence of the pressure drop but is another geometry and cannot correct scan 14 numerically.
- Closing the gaps needs new scan-14 runs (a x2-x3 flow run and a true one-global-scaling Protocol C run). These are new CFD work on scan 14 and need the analysis side's decision; none was started.

## Suggested manuscript fixes (analysis side to apply)
1. State the 3D case's inflow (0.65-0.71 mL/s, 39-43 mL/min), Re_throat 106-123 and which radius sets r_in; call it a low-flow case in Limitations.
2. Replace "paired differences unaffected" by the four measured deltas (+0.127, +0.099, +0.081, +0.074).
3. Say that per-outlet flow prescription restored the FFR in 3D and remove "same concealment" (abstract, III-D, IV-A, Conclusion); add the Protocol C 3D run if time allows.
4. Report the Protocol A outlet-flow deviations, the lesion-state meaning of "clean" flows, the D3/D4 and Task A criterion failures and the proxy convergence in the main text or the supplement.
