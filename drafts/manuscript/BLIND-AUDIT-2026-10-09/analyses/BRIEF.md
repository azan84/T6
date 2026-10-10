# Shared brief: analyses A5, A6, A7, T5 (2026-10-09)

Paper 6 (T6) is an in silico study of coronary computed FFR. Submission to IEEE JBHI is due on 2026-10-15. Read these before starting:
- `drafts/manuscript/main.tex` and `drafts/manuscript/supplement.tex` (current text)
- `drafts/manuscript/BLIND-AUDIT-2026-10-09/PLAN.md`
- `drafts/manuscript/BLIND-AUDIT-2026-10-09/FABLE-PLAN-AUDIT.md`, especially §3, §8 and §9, which hold the design notes for each analysis

All paths are relative to `Paper6-T6/`, i.e. `/Users/mzpi/Library/CloudStorage/GoogleDrive-Mohd.Zulhilmi@monash.edu/My Drive/Research/01 CollabProject-MonashIIUM/Imaging-Medical/Paper6-T6/`.

## Environment
- Python: `~/.venvs/paper6-t6/bin/python`. It has numpy, pandas, scipy, statsmodels, networkx and pyvista.
- Data root: `~/Documents/Datasets/imagecas-x/ImageCAS-X_dataset`. This is local disk, not Drive.
- Frozen code is in `code/`:
  - `zerod_ffr.py`: solver
  - `imagecasx_loader.py`, `severity_sweep.py`: loading and lesion insertion
  - `error_types.py`: T1–T4
  - `ablation.py`: Protocols A–C, `territories()`, `protocol_c_targets()`
  - `ablation_per_territory.py`: Protocol D
  - `negatives.py`: simulated floor
  - `summarise_revision.py`: endpoints
- Frozen inputs:
  - cohort: `deposit-2026-10-08/protocol/COHORT-FROZEN-2026-09-18.csv`
  - discrete-arm eligibility: `results/discrete_arm_eligibility.csv`
- Frozen results:
  - `results/ablation-2026-10-07.csv` (A–C) and `results/ablation-perterritory-2026-10-08.csv` (D)
  - `results/negatives-2026-10-07.csv`
- Runtimes (8 CPUs shared by four parallel jobs):
  - `ablation.py`: about 5 s per instance
  - `ablation_per_territory.py`: about 3.3 s per instance
  - `negatives.py`: about 44 min for 20 draws

## Hard rules
1. **Do not modify existing files.**
   - This covers `code/*`, `results/*`, `deposit-*`, `github-repo/*`, `drafts/manuscript/*.tex`, the figures and the supplement tables.
   - Reuse frozen code by importing it. Change behaviour only through a wrapper or monkeypatch inside your own new script.
2. **Write only to your own locations:**
   - new scripts: `code/<your_prefix>_*.py`
   - outputs: `results/<your_prefix>-2026-10-09/`
   - your report: `drafts/manuscript/BLIND-AUDIT-2026-10-09/analyses/<ID>-REPORT.md`
   - scratch: `/private/tmp/claude-501/`
3. **Write no comments in your code that mention AI tools, reviewers, audits or internal plan IDs.**
4. **Validate before the full run.**
   - Show that your wrapper reproduces the frozen numbers where it should, e.g. the default settings give identical FFR on a few instances.
   - Report that check.
5. **Report the result honestly, whichever way it goes.** Never tune a design choice after seeing the outcome. Fix the design, record it in the report, then run.
6. **Do not read PDFs with the Read tool.** Use `pdftotext` if needed.

## Report format (`<ID>-REPORT.md`)
1. **Design as run:** exact definitions and any convention decided before the run.
2. **Validation:** what the check reproduced.
3. **Results:** tables with counts, Wilson 95% CIs and paired tests where relevant. Use the same denominators and conventions as Table I and Table S3: discrete arm restricted to the 97 eligible instances; models with a defined residual.
4. **What it means for the paper's claims:** which sentences stand, which must change, and in which direction. Quote the current sentence.
5. **Draft text:**
   - (a) at most 2 main-text sentences;
   - (b) a supplement paragraph plus a LaTeX table body that matches the style of `drafts/manuscript/supplement_tables/*.tex` (booktabs, `\%`, Wilson CIs as "x (lo--hi)").
   - Facts only, formal and concise. No "post hoc" labels.
6. **Runtime and files written.**

Reply to the coordinator with a 10-line summary: headline numbers and the implication for the claims.
