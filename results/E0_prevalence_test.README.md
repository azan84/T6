# E0_prevalence_test.csv: read before using

**What it is:** the Gate E0 prevalence screen (`code/run_prevalence.py`). This is the baseline 0D FFR distribution over
the ImageCAS-X test split. It was used for the STUDY-PLAN-v2 §E0 decision rule and nothing else.

**How it was computed:** `load_tree(...)` with the default **`bed="leaky"`**. There are two demand models (`murray`,
`territory`) × three flow scales (0.7 / 1.0 / 1.3).

**What `min_ffr_main` is:** the minimum FFR over resolved main-vessel nodes of the network **as segmented** (native
lesions included), under the **leaky** bed.

**What it is NOT:**
- It is not `healthy_main_ffr`, the healthy-equivalent network with no lesion terms. This file has no such column.
- It is not a discrete-bed value.
- It is not a selection or eligibility file for anything.

**Do not select or gate cases from this file.** Across the 108 cohort trees, **34 pass ≥ 0.90 on `min_ffr_main` here
but fail the discrete healthy-network gate** (`Tree(..., bed="discrete").healthy_main_ffr()`, murray, scale 1.0).
Example, scan 828-left: 0.944 here. Under the discrete bed, `min_ffr_main` is 0.845 and `healthy_main_ffr` is 0.913.

**Where to get selection values instead:**
- The cohort (leaky bed, primary 0D model): `protocol/COHORT-FROZEN-2026-09-18.csv`
- Discrete-arm eligibility: `results/discrete_arm_eligibility.csv` (`code/discrete_arm.py`)
- 3D/CFD cases: `protocol/CFD-SUBSET-FROZEN-2026-09-18.csv` only (see `cfd_handover/WORK-ORDER-2026-09-24.md`, §7
  "E0 guard")

**Legitimate current use:** the regression check V10 in `severity_sweep.verify()`, which is guarded to run under the
leaky bed only.

**Column name deliberately unchanged:** renaming `min_ffr_main` would break V10, and this file is hashed in
`protocol/COHORT-FROZEN-2026-09-18.sha256`.

*Added 2026-09-24 after an independent audit of the CFD report's scan-828/837 selection. The audit reproduced every
number above.*
