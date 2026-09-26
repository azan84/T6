# T6 extraction, batch 3 (2026-09-25)
43 PDFs that were in `Resources/` but in no ledger (added 2026-09-17/19, after the 09-17 manifest was built).
Manifest: `MANIFEST-BATCH3-2026-09-25.tsv` (C001–C043). Ledger: `TRIAGE-LEDGER-BATCH3.tsv`, rebuilt from the notes'
frontmatter (43/43, no missing ids, no path mismatches). Stage 1 by Haiku, Stage 2 by Sonnet.

## Result for T6
**No THREAT.** Gate N1 is unchanged.

Buckets: METHOD 12 · SUPPORT 10 · BACKGROUND 12 · IRRELEVANT 9. Haiku marked six FULL. Three were read in full; the
other three were downgraded on reading the triage notes (generic 3D–0D coupling or BC fitting, nothing T6 would quote).

| Paper | Stage 2 verdict | Use in T6 |
|---|---|---|
| choi-2026-bc-amortized (FalconBC) | METHOD | Contrast citation: "the pressure measured with a catheter is not reachable with boundary condition tuning due to imperfections in the segmented anatomy" (Conclusion, p. 24). They re-estimate anatomy when the target is unreachable; T6 asks what happens when tuning *does* reach it and hides the error. Synthetic stenoses only; no FFR, no 0.80 reclassification |
| richter-2024-windkessel-bayesian | METHOD | 0D surrogate fitted from one 3D run for Windkessel calibration; candidate for the BC re-tuning step |
| bertels-2021-volume-bias-soft-dice | SUPPORT | Training loss biases downstream volume in a fixed direction, growing with inherent uncertainty (soft Dice over-estimates; e.g. U-Net IS18 bias 3.57 ml CE vs 6.46 ml SD). Segmentation choices cause systematic, not only random, downstream error |
| chen-2025-eecp-multiscale, seo-2023-kawasaki-disease-cfd, bonini-2026-lvad-3d-0d | FULL → LIGHT on review | Triage notes suffice |

## Misrouted: belong to the main pipeline (P16/P04 evaluation literature), not T6
C007 maier-hein-2020-bias-guidelines (BIAS reporting guideline) · C009 poel-2021-segmentation-radiotherapy ·
C010 ross-2023-algorithm-validation-surgery · C011 wagner-2023-surgical-workflow-cholecystectomy.
Added 2026-09-19 with the MedIA evaluation papers. Marked IRRELEVANT for T6 only.

## Openings for CFD + imaging ideation (beyond T6)
Most "Ideation opening" lines restate T6's premise. The distinct ones:
- **Geometry-only clinical guidelines vs haemodynamics** (seo-2023, Kawasaki coronary aneurysms): guidelines rely on
  aneurysm size, but outcomes correlate poorly with geometry alone. A CFD-vs-size decision study in paediatric coronary
  aneurysms.
- **Sex-stratified virtual populations** (wardhana-2025): sex is "underrepresented"; no sex-stratified coronary
  geometry + CFD cohort.
- **Model complexity changes sensitivity rankings** (nishida-2026, 0D): which parameters matter depends on model
  complexity. The same question for 0D vs 1D vs 3D coronary FFR is open.
- **Segmentation under metal artefact** (bonini-2026, LVAD): automated segmentation failed; manual was used. The
  haemodynamic cost of artefact-degraded segmentation is unmeasured.
- **Circle of Willis validation** (liu-2020 review): "few patient-specific models of CoW … fully validated by in-vivo
  measurement".
- **Bertels → Paper 3:** soft-Dice-trained vessel segmenters may bias vessel width. Bertels reports that both losses
  "over-estimate small volumes and under-estimate large volumes" (p. 9), but never tests thin or tubular structures.
  Candidate extra factor or limitation for Paper 3.

Not yet screened against the topic bank or `Q1-Theme-Scan-2026-09/imaging-cfd-emerging-themes.md`.
