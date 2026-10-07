# Merge notes: Introduction and Methods, 2026-10-07

V1 = `main-backup-2026-10-07-pre-intro-methods-merge.tex` (Intro 446 words, Methods 1,055).
V2 = `ars_intro_methods.tex` (Intro 564, Methods 1,691).
Merged = `main.tex` (Intro 651, Methods 1,742). Compiled: 8 pages, page 8 is references only
(left column 70% filled, right column empty), so about 7.35 pages. No undefined references or
citations; one 3.2 pt overfull vbox (page-level, below the 5 pt limit).

Facts stated only in V2 were checked against `protocol/SEVERITY-SWEEP-SPEC.md`,
`protocol/STATISTICS-PLAN.md`, `protocol/CFD-ARM-SPEC.md`, `code/zerod_ffr.py`,
`code/severity_sweep.py`, `code/discrete_arm.py`, `code/error_types.py`, `code/ablation.py` and
`code/analyse_ablation.py` before being kept.

## Introduction

| | V1 | V2 |
|---|---|---|
| Better | Compact; cites the Fossan numbers (AUC 0.845, sensitivity 58.1 to 68.6%) and the Gamage 13-15% figure that Discussion B relies on; states the gap as "decision at 0.80 ... under controlled conditions". | Defines FFR, boundary condition and microvascular bed in plain clauses; separates calibre from topological error explicitly before the literature; states the open question as a mechanism (error disappears from the validation check but stays in the pressure field); contribution (1) names the error model. |
| Missing or wrong | No definitions of boundary condition, microvascular bed, reduced-order model, topological vs calibre error. Cites `murray1926` with `kim2010` for outlet scaling (acceptable) but V1's contribution list does not say two bed structures were used. | Cites `choy2008` with `murray1926` for scaling laws in general (Choy does not support arterial resistance derivation in general; dropped). Reads "FFR-guided intervention improves outcomes over angiographic guidance" from `tonino2009` (FAME showed fewer major adverse events; wording simplified to avoid over-claiming). Mentions "learned formulations" without definition. No Fossan numbers. |
| Taken | Fossan and Gamage numbers; the "has not been tested" closing; the explicit protocol list (fixed, re-derived, tuned) and "two bed structures, one instance in 3D" in the aim paragraph; CFD contribution (3). | Opening definition of FFR; definitions of boundary condition and microvascular bed; "segmentation enters twice"; calibre vs topological framing with the full citation set (adds `dalmaso2025`, which Discussion already cites); the mechanism sentence; contributions (1) and (2). |

Added by the merge: one-clause definitions of lumen, reduced-order model and ablation. Removed
from the intro: "cohort, design and analysis plan fixed" (now stated once, in Methods F).

## Methods A. Data and Cohort

| | V1 | V2 |
|---|---|---|
| Better | Inter-observer DSC and HD95 stated here, which Methods C needs; "frozen, hashed list". | Eligibility rules complete (image quality >= 2, 0.75 mm radius at the measurement point); exact severity levels; sweep size (6,944 instances, 280 hosts, 140 scans); selection rule (25 per band, at most two per tree); "vessel was never widened"; defines s, c, L. |
| Missing or wrong | Omits image-quality gate, the 0.75 mm rule, severity levels and the selection rule. "resolved measurement point" undefined. | Omits DSC/HD95 values; "smoothed along each segment" for the radius is not in the loader description used by V1 (dropped). V2's cosine uses pi(s-c)/(L/2), identical to V1's 2pi(s-c)/L (V1 form kept). |
| Taken | DSC/HD95 sentence (with plain definitions added); equation; "frozen, hashed list". | All eligibility rules; severity levels; sweep and selection numbers; "never widened". |

Added: "An instance is one lesion in one tree" (Results and Discussion use "instance" throughout).

## Methods B. Reduced-Order FFR Model

| | V1 | V2 |
|---|---|---|
| Better | Parameter block complete and compact; "bed constant and reference radii computed from the original tree". | Solver details (30% DS rule for the expansion loss, fixed-point iteration to 1e-8, mass-conservation error recorded, which Results A reports); leaky-bed truncation 0.50 mm; "healthy-equivalent network" defined; the 97-instance rule given in full (main-vessel FFR >= 0.90 and >= 2 outlets, matches `discrete_arm.py`); bands derived per bed; centreline-spacing check (0.005, matches SEVERITY-SWEEP-SPEC V8). |
| Missing or wrong | No leaky truncation radius; healthy-equivalent network not defined; 97-instance rule left to Results; `murray1926` cited for the leaky bed in a way that reads as a source of the bed itself. | Cites `gosling2020` as source of the leaky bed (dropped: Gosling studied side-branch flow, not this bed); cites `murray1926` for k = 562 (dropped: Murray supports the cube law only). |
| Taken | Parameter values; "lesion changes only the epicardial radius". | Everything else listed under "Better". |

Citation handling: `murray1926` now attached to "flow follows Murray's cube law" only; `choy2008`
attached to "the exponent follows the empirical scaling of myocardial mass with coronary vessel
size" without claiming the value 2.66 is Choy's; k = 562 and K_t = 1.52 left uncited as before.
"Conductance" defined as the inverse of resistance.

## Methods C. Segmentation Error Types

| | V1 | V2 |
|---|---|---|
| Better | "For T3 and T4 the set of modelled nodes is fixed to that of the clean tree" (this is what `zerod_ffr.Tree(trunc_ref=...)` does). | Topological vs calibre defined at the head; T2 wording explains why the measurement point survives; DSC-to-radius equation 2k^2/(k^2+1) = 0.928; reason the statistics are an upper bound (same auto-generated centrelines); nodes matched by coordinate. Table I has definitions, not only operations. |
| Missing or wrong | Table I terse ("delete largest side branch"). | "truncation radius scaled by the same factor" describes an internal mechanism (`ablation.trunc_for`) that the final code makes a pre-filter; replaced by V1's node-set statement, with the consequence spelled out ("so a narrowed radius does not remove an outlet"). |
| Taken | Node-set sentence. | Paragraph structure, definitions, equation, upper-bound reason, coordinate matching, Table I layout (with T1/T4 labels aligned to the paper's terms: missed branch, vessel break, lesion length, taper). |

## Methods D. Boundary-Condition Protocols

| | V1 | V2 |
|---|---|---|
| Better | "Protocol C matches flow only: matching both flow and pressure ... reproduces the clean FFR by construction." | What each protocol represents (A: boundary conditions correct despite the error; B: automated pipeline); territory target explained (full clean territory, including the deleted share, "because the myocardium is perfused whether or not its artery was segmented"); node-to-territory assignment; loss function; "defined only when at least two territories retain a vessel" (which Results A previously had to state); perfusion residual defined here. |
| Missing or wrong | Residual defined only in F; the two-territory rule absent. | "mean squared relative error" confirmed against `ablation.py` loss. V2 did not say the search is centred on the re-derived C (added). |
| Taken | Flow-only sentence; "61-point scan over +-1.5 decades, bounded refinement, fit at a bound is a failure". | The rest. |

Term fixed: Protocol C is "tuned" everywhere (V1 had "flow-matched" in Methods while Results
and Discussion say "tuning").

## Methods E. Three-Dimensional Case Study

| | V1 | V2 |
|---|---|---|
| Better | "isolates the effect of model fidelity from that of radius definition" (why the twin exists). | Three lumens named (clean, baseline, T1); surface-edit method; rigid walls and aortic inlet pressure; per-outlet flow split in proportion to bed weights (matches STATISTICS-PLAN P2); FFR as area-averaged pressure on a cross-section. |
| Missing or wrong | Per-outlet split not described. | Names "scan 14" (dropped: no scan identifier elsewhere in the paper). Grid study did not list the cell sizes (50, 25, 12.5 um added from the task brief; Results D reports the 12.5 um check). |
| Taken | Twin sentence. | The rest. |

Checked against Results D: baseline and T1 lumens, 3.5-3.9 million cells, 25 um within +-4 mm,
four boundary layers, OpenFOAM ESI v2406, Protocol A resistances or prescribed clean territory
flows, twin on the area-equivalent radius, discretisation uncertainty 5.5e-4.

## Methods F. Outcomes and Statistical Analysis

| | V1 | V2 |
|---|---|---|
| Better | Model terms listed in full (error type x protocol, severity, length, band; patient and lesion-slot intercepts); "claim only where direction agrees in both beds"; "cohort, analysis plan and code fixed, cohort list hashed"; "departures listed in the Supplementary Material". | Explains why 10% is stricter than 13-16% (one deterministic output against one measurement) and that a looser threshold can only raise the count; 13% and 16% as sensitivities (Results B reports them); the noise floor stated as a per-instance probability. |
| Missing or wrong | Reads as if 13-16% came from the cited papers (reworded: "bound we derive ... at published repeatability"). | Lists the departures in the main text, including a 3D replication on 30 instances and a detector that are not reported (removed: no mention of follow-up work; departures stay in the supplement). Adds a GEE model beside the VB model (omitted from the main text: the brief lists the VB model only; the GEE output exists in `results/analysis-ablation-2026-10-07/P1_gee_*.csv` and could go in the supplement). Python package list dropped for length. |
| Taken | Model terms; both-beds rule; fixed-and-hashed sentence; departures sentence. | 10% justification; sensitivities; per-instance noise floor; "materially wrong" explained. |

## Results edits (allowed under 2a and 2b)

- Results A, first paragraph: removed the sentences repeating the 150/97 split and "Protocol C
  requires two territories with surviving vessels" (both now in Methods B and D). Numbers unchanged.
- "right coronary artery" -> "RCA" in that paragraph (RCA defined in Methods A).
- Nothing else outside the Introduction and Methods was changed.

## Open points for the authors

- `choy2008`: the text now says the exponent "follows the empirical scaling of myocardial mass
  with coronary vessel size" and does not attribute the number 2.66 to the paper. Confirm the
  value or cite its actual source.
- 50/25/12.5 um throat cell sizes for the grid study are from the task brief, not from a file in
  the repository I could find (CFD-ARM-SPEC gives the mesh rules, not the three sizes).
- GEE model: fitted (`analyse_ablation.py`) but not mentioned in the main text; decide whether
  the supplement reports it.
- "Linear taper fit" for r_fit: SEVERITY-SWEEP-SPEC calls it a robust linear taper fit; "robust"
  omitted for plain wording.
