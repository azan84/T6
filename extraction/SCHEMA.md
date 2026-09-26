# T6 extraction schema (created 2026-09-17)

Two stages, following the house LIGHT/FULL triage discipline used in
`../../Proposal/ideation_run/2026-09-13/extraction_mapped/` and the deep-note format in
`../../Paper1-P16/references/`.

## Stage 1 — TRIAGE (one file per paper, `triage/<slug>.md`)

Read **abstract, intro's last paragraph, methods headings, results headings, conclusion only**. Do not read the
whole paper. Answer only what the scanned text supports; write `NOT REPORTED` otherwise. Never guess.

```markdown
---
source_pdf_path: Resources/<file>.pdf
slug: <firstauthor>-<year>-<3-word-topic>
ledger_status: TRIAGED
---

# <slug>

## Bibliographic
- Title:
- First author / authors (first 3 + et al.):
- Year:
- Venue:
- DOI:

## One-line claim
- <single sentence, the paper's own central claim>

## T6 targeted questions
- **Q-A geometry perturbation**: Does it perturb, or measure, lumen/segmentation uncertainty? If yes: SYNTHETIC
  (researcher-chosen amounts) or REAL (measured inter-observer/inter-segmenter disagreement)? Give the reported
  magnitude if stated.
- **Q-B decision flip**: Does it report FFR (or any diagnostic) reclassification at a threshold — the 0.80 FFR cut
  in particular? Give the reported flip/reclassification rate if stated.
- **Q-C BC tuning**: How are outlet boundary conditions set/tuned (Windkessel, resistance, Murray's law,
  allometric, optimisation-to-target)? Is the tuning **re-done after** a geometry change? Any statement that
  tuning compensates for, masks, or absorbs geometric/anatomical error?
- **Q-D fidelity / quantity**: Reduced-order (0D/1D) or 3D CFD or both? Does it report WSS / OSI or other
  spatially-resolved fields, and their sensitivity to geometry?
- **Q-E data**: Cohort/dataset name, N, public or private, invasive-FFR ground truth present? (yes/no)
- **Q-F meshing**: Any detail on segmentation→surface→volume meshing, and robustness on poor/broken/topologically
  incorrect geometry? (Gate M1 relevance)

## Novelty bearing on T6
- bucket: THREAT | SUPPORT | METHOD | BACKGROUND | IRRELEVANT
  - THREAT   = does something T6 claims as new (real-disagreement-derived error ranking, decision-flip ranking by
               error type, or BC-tuning-absorbs-topological-error) — a Gate N1 hit
  - SUPPORT  = evidence T6 will cite to justify its premise or frame its claims
  - METHOD   = a technique T6 will reuse (error injection, BC tuning protocol, svZeroDSolver/OpenFOAM setup,
               meshing, WSS/OSI extraction)
  - BACKGROUND = clinical FFR-CT context, trials, reviews
  - IRRELEVANT = not usable for T6
- one-line reason:
- verdict: FULL | LIGHT
- revisit-if: <condition that would upgrade LIGHT → FULL>
```

## Stage 2 — FULL (`full/<slug>.md`)

Only for Stage-1 `verdict: FULL`. Use the deeper P16 `references/` format (Bibliographic / Problem & claim /
Method / Data / Evaluation / Reproducibility / Limitations / Openings / Key references), **plus** the six T6
targeted questions above answered with verbatim quotes and section/page pointers.

## Ledger

`MANIFEST-2026-09-17.tsv` = the 168 unique PDFs added 2026-09-17 (4 duplicate `(1)` downloads excluded).
`TRIAGE-LEDGER.tsv` records `id / slug / bucket / verdict` as each triage note lands.
