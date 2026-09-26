# FINAL pre-flight — B1 / B2 / B3 as applied, before the CFD machine is committed

**Reviewer:** Fable 5.1 (independent pre-flight) · **Date:** 2026-09-19, evening (code state 18:03–18:04)
**Scope:** the three decisions applied today and their follow-up correction (clean partition, `trunc_ref`), the smoke,
the M1 packages, and the six documents edited today. Nothing in `code/`, `protocol/`, `results/` or `cfd_handover/`
was modified. The 150-instance ablation was NOT run; the cohort census below is geometry + one clean solve per instance.
**Probes:** `references/FABLE-FINAL-PREFLIGHT-2026-09-19-probe/`

| file | what it is |
|---|---|
| `verify_{leaky,discrete}_14_306.txt` | `severity_sweep.py --verify` V1–V10, scans 14 + 306, both beds |
| `smoke_REPRO.{csv,log}` | `ablation.py --limit 6` re-run with the current code |
| `M1_REEXPORT/` | `export_cfd_case.py --m1` re-run with the current code, for diffing against the shipped packages |
| `PKG_scan14/` | T2 and T4 packages for the M1 instance (not shipped; built to check the 0D twin and the stump) |
| `probe_census.py`, `census_cohort.csv`, `analyse_census.py`, `analyse_census_output.txt` | all 150 instances × 2 beds × 4 error types: territory counts under the clean and the corrupted partition, node-set identity for T3/T4 under three truncation rules, T2 measurement-node survival |

---

## 0. Verdicts

**(a) Stage A + Gate M1 — GO.** The shipped M1 packages are byte-identical (all CSVs, JSON, README, `centreline.vtp`
arrays) to a re-export under the current code; only `meta.json` provenance (exporter hash, date) is stale because the
exporter was edited after the 17:40 export. Flood-fill rule executed verbatim from the shipped `mask_edit.json` on the
real scan-14 mask reproduces the README numbers (T1: 2089 voxels removed, baseline: 1310; 2→2 components; 0 erosion
inside 1.0 r; 163/163 and 121/121 kill points inside the lumen; 6-connectivity confirmed). Packages contain no
`ffr` token in any file or array name. Inlet normal = root tangent (0.9454, 0.2764, 0.1725) in `inlet.json` and
`probes.csv`. `measurement` station present in all three. The bc/START-HERE fixes from the previous pre-flight (α = 0.05
bound, "prescribe every outlet", RAM, Foundation line) are in. Nothing in B1–B3 touches Stage A, and M1's criterion
does not depend on the value of the T1 Protocol C target. Two cosmetic items the CFD operator will otherwise read
(§5.3): `meta.json` says B1 is both "settled" and "UNRESOLVED", and its `exporter_sha256` no longer matches the file.

**(b) 0D ablation — GO-WITH-CHANGES; do not lodge or run today.** The code is correct as far as I can test it and the
smoke reproduces bit-for-bit, but: the hashed manifest fails on three code files; B3 is not yet exact (6 of 298 T4
rows still drop 2–7 nodes); and B1's territory guard removes Protocol C — the thesis arm — from essentially the whole
RCA stratum for T1 and T2 (40 % / 33 % of those rows cohort-wide), which no registration document declares and which
the STATISTICS-PLAN's stated exclusion rule does not describe. Each fix is minutes; the declarations are what matter.
The full list is §7.

---

## 1. B1 — Protocol C's target (`protocol_c_targets`)

**1.1 Is the clean partition the right estimand?** Yes, and it is the only partition under which the target is
independent of the error: the clean tree's first-bifurcation territories are fixed anatomy; every corrupted node is
assigned to the territory of its clean counterpart by coordinate; the target is the clean subtree's full outflow.
`node_map` does the right thing for T1 (deleted subtree vanishes, everything else maps 1:1) and T2 (`t2_truncation`
keeps `pts[:i_cut+1]` unchanged, so surviving coordinates are identical). Corrupted nodes whose clean counterpart is
inactive (possible at the margin after a re-fit) get no owner and are excluded from both sides — negligible and
conservative. In the leaky bed the parent of a deleted branch gains the point leak and belongs to the same clean
territory, so `pred` picks it up — that is why T1 C_ratio lands at 0.93 in both beds.

**1.2 The exporter agrees with the ablation wherever both have a Protocol C cell.** Census: on all 335 T1/T2 rows
with ≥ 2 clean territories, the exporter's corrupted-partition targets equal the ablation's to 1e-6 and the territory
counts match. The "33 %" under-targeting rows are exactly the rows the clean partition now *excludes* (below).

**1.3 The ≥ 2-territory guard: what it removes, cohort-wide.** Not ~17 %:

| error type | bed | ok rows | Protocol C lost (< 2 clean territories) | of which RCA |
|---|---|---|---|---|
| T1 missed branch | leaky | 118 (32 no deletable branch) | **47 (40 %)** | 45 |
| T1 missed branch | discrete | 109 (39 no deletable branch) | **42 (39 %)** | 40 |
| T2 truncation | leaky | 149 | **49 (33 %)** | 49 |
| T2 truncation | discrete | 147 | **50 (34 %)** | 50 |
| T3 / T4 | leaky | 150 | 0 | — |
| T3 / T4 | discrete | 148 | 5 (single-outlet RCA trees, already outside the 97-instance discrete arm) | 5 |

Mechanism: the modelled RCA's first bifurcation is the crux (small proximal branches are below the truncation
radius). T2's cut at c + L/2 + 25 mm is proximal to it, so **99 of 100 T2 × RCA rows have 0 territories**: not only is
Protocol C skipped, `outlet_flow_residual` is NaN for Protocols A and B too — P2's joint outcome does not exist for
T2 on the RCA under any protocol. T1 on the RCA deletes one crux child, i.e. an entire territory: it has no
surviving member, so it is dropped from the target rather than being targeted, and the survivor is the only pair.
This is the one case where B1's own estimand ("the patient's myocardium is perfused whether or not the segmentation
saw the branch") **cannot be represented**: the deleted territory's flow has no vessel to be delivered through, and in
the leaky bed the point leak lands on the trunk, which belongs to no territory.

So: the guard is doing its job (the alternative — the corrupted partition — "rescued" 16 leaky / 12 discrete of these
T1 rows with a target that simply omits the deleted territory, ratio 0.36–0.85 in the leaky bed). It is correctly
declared per row (`status`, `n_territories`). It is **not** declared where it matters: STATISTICS-PLAN §9 states the
exclusion as "≥ 2 outlets for missed-branch/truncation and for Protocol C" — a different rule (an RCA with 3 outlets
beyond the cut has 0 territories), and P1/P2 stratify by vessel while the T1 × C and T2 × C cells are LAD/LCX-only
(n ≈ 66–71 and 92–100 per bed). On the frozen 3D subset (discrete): T1 × C exists on **19/30** (the previous
pre-flight's 23/30 was under the corrupted partition), T2 × C on 19/29, T3/T4 × C on 30/30.

**Verdict on B1:** correct estimand, correct code, correct per-row declaration; **undeclared at the registration
level**, and the loss is a whole vessel stratum, not a scattering of cells. Declare it (§7) or change the partition —
the latter is a design decision, not a fix, and I would not open it under a tight deadline.

**1.4 A side effect of B1 that makes two documents false.** Protocol A's residual is now measured against the full
territory target, so A no longer "passes the perfusion check by construction": in the FINAL smoke discrete A passes
12/19, and T1/T2 A residuals are 0.10–0.17 (the deleted share). STATISTICS-PLAN §P2's "Note on Protocol A" and the
footer printed by `ablation.summarise()` both still assert the opposite (§5).

---

## 2. B2 — `T2_KEEP_BEYOND` 15 → 25 mm

- Cohort-wide: the clean measurement node survives in **149/149 leaky and 147/147 discrete** T2 rows (census); T2
  applicable on 100 % (operator's probe reproduced by the same census: 1 row per bed "truncation point falls at the
  start of its segment", which is the pre-existing applicability test).
- The assert is real but **bypassable two ways**: `python -O` strips it (demonstrated: import succeeds with the
  constant set to 15 mm), and any script that builds T2 via `error_types` without importing `ablation` never sees it.
  Trivial hardening: `if T2_KEEP_BEYOND <= RUNOFF: raise ImportError(...)` in `error_types.py` itself (it can import
  `RUNOFF` from `severity_sweep`; no circularity — `severity_sweep` does not import `error_types`).
- Interactions: none with slot eligibility (run-off ≥ 20 mm is a slot rule; 25 mm only changes what T2 deletes).
  `d_dn_bif_mm`: 14 cohort instances have a downstream bifurcation in the 15–25 mm window, so T2 now *keeps* that
  branch and is a milder topological error on those 14 than at 15 mm — a consequence of the design intent, fine, but
  worth one sentence. 3D subset: 10 T2 packages (all RCA) still have a single-leaf stump, so under Protocol A the 0D
  has "no bed left" and the 3D package closes every outlet (unsolvable) — unchanged from the previous pre-flight.

---

## 3. B3 — `trunc_ref` and `trunc_for`

**3.1 What the current code does.** `Tree.__init__` computes `active = r_ref ≥ r_trunc` and then *intersects* it with
the reference tree's active coordinate set. So `trunc_ref` can only remove nodes relative to the clean set, never add;
`trunc_for` (0.93 × threshold) reduces how many the threshold removes before the intersection. Census, T4:

| rule | leaky: rows dropping nodes / adding nodes | discrete: rows dropping / adding |
|---|---|---|
| **current (trunc_for + trunc_ref)** | **1 / 0** (max 5 dropped) | **5 / 0** (max 7 dropped) |
| trunc_ref alone, base radius | 104 / 0 (max 165 dropped) | 133 / 0 (max 157) |
| trunc_for alone (the first B3) | 1 / 47 (max 38 added) | 5 / 82 (max 169 added) |

So `trunc_for` is **not redundant** — without it the intersection would delete nodes on two thirds of the cohort — and
the pair is far better than either alone. But it is **not exact**: 6 of 298 T4 rows (scans 698, 751, 789, 935; none
in the 3D subset) still drop 2–7 nodes because r_ref after the taper re-fit falls below 0.93 × cut on those nodes.
Leaf *counts* are unchanged, so these are leaves moving ≤ 7 nodes proximally — under Protocol A that moved leaf has
clean w = 0 and is written `closed`, i.e. a miniature of the artefact B3 was meant to remove. The docstring's "Pinning
by coordinate is exact" is true only on the adding side. **Fix (2 lines, `zerod_ffr.py` line 124):** make the
reference authoritative — `self.active = np.array([… in key …])` instead of `&=` — after which `trunc_for` is
genuinely redundant and can be dropped from `ablation.py` and the exporter (or kept harmlessly). T3 is exact already
(0/298 rows differ). The verify suite does not exercise `trunc_ref`, so V1–V10 cannot regress from this change; the
smoke would move only if one of the six scans were in it (none is).

**3.2 The verified core.** `zerod_ffr.py` self-test unchanged (0–90 %DS, 27–28 iterations, mass error ≤ 1e-11).
`severity_sweep.py --verify` on scans 14 + 306: **V1–V10 PASS on both beds** (leaky: V8a 0.0010, V8b 0.0025, V10
0.0000; discrete: V8a 0.0019, V8b 0.0022). No regression.

**3.3 T4 package = 0D twin.** Built the T4 package for the M1 instance: `centreline.vtp` point set == the ablation's
`Tree(..., r_trunc=trunc_for, trunc_ref=t)` active set == the clean active set, 748 = 748 = 748, 6 leaves each. Both
call sites pass the same two arguments, so this holds by construction; `meta.json.truncation_r_ref_mm` reads 0.558,
which is now only the pre-filter — the shipped `sub_cut_points_mm` is what the CFD side uses, so no harm.

---

## 4. Regression: the smoke

- **My re-run reproduces `ablation_smoke_FINAL-2026-09-19.csv` bit-for-bit** (all 45 columns, 124 rows).
- **POSTFIX → B1B2B3** (the operator's diff, checked): T2 rows all move (B2: measurement node now interior;
  `meas_same_point` 0/36 → 36/36); T4 discrete rows move with sign correction (B3); the single T1 instance's Protocol C
  moves (B1: C_ratio 1.049 → 0.928 leaky, 1.044 → 0.937 discrete); and **A/B residuals move on every T1/T2/T4 row**
  because the target changed (e.g. T2 × A discrete 0.0005 → 0.136 = the deleted run-off's share). All explained.
- **B1B2B3 → FINAL** (the follow-up `trunc_ref`): 0 status changes, 0 flips changed; **only T4 rows move** — discrete
  B/C by up to 0.03 FFR (scan 335 C: −0.034 → +0.003; C_ratio 0.75 → 0.95), discrete A by ≤ 0.002, leaky rows by
  ≤ 1e-5. This is `trunc_ref` removing the +7 % extra nodes `trunc_for` alone had added. Explained; **nothing
  unexplained.**
- Numbers quoted in the documents that survive FINAL: T4 × A discrete −0.032 (FINAL −0.0329), leaky −0.047 ✓; T1
  C_ratio 0.928 / residual 0.097 / ΔFFR 0.078 ✓ (leaky; discrete is 0.937 / 0.084 / 0.070). **T1 is n = 1** (scan 306)
  in the smoke — 5 of 6 smoke instances have no deletable branch — and the documents present it as a finding.
- The banner's "a fourth thing fixed itself: B1 removed the 'fewer than 2 shared territories' skip (113 → 114)" is
  wrong: the rescued row is 335/discrete/T4/C, which B3 rescued, and B1's guard fires on 40 %/33 % of T1/T2 rows.

---

## 5. The CFD packages and the exporter

**5.1 M1 (shipped):** consistent with current code (§0). Blinding, flood-fill, inlet normal, stations: re-verified.

**5.2 Exporter vs the 0D twin — batch-blocking, not M1-blocking.**
1. **T2 stump under Protocol C is a wall in 3D and a live outlet in 0D.** The intra-territory split "in proportion to
   their own clean flow" gives the stump 0 (its clean counterpart is interior, w = 0 in the discrete bed), so
   `bc_C_flows.csv` writes `closed` for it and puts the whole territory target on the other survivors — built and
   confirmed on scan 14 (`PKG_scan14/…T2…/bc_C_flows.csv`: `out_185 closed`, `out_160` carries 0.1735 = the full
   territory). The 0D twin gives the stump w = r_ref^2.66 > 0 and delivers the run-off's share through it. On the
   10 RCA subset instances the stump is the only outlet → every outlet `closed` → no case. The 3D Protocol C is not
   the 0D Protocol C for any T2 package. A blind rule that matches the 0D: split each territory's full target across
   its surviving outlets in proportion to the **corrupted** tree's Murray weights `t2.w` (what one global C does).
2. **Exporter still partitions by the corrupted tree** (`territories(t2)`, line 305). Wherever the 0D has a Protocol C
   cell the targets coincide (§1.2), but on the 12 discrete rows where the 0D has *no* cell (T1 deleting a whole
   territory) the exporter would still package a Protocol C with a target that ignores the deleted territory —
   **4 of them are in the frozen 3D subset (scans 196, 272, 341, 928)**. Either switch the exporter to
   `protocol_c_targets` or refuse to write `bc_C_flows.csv` when the 0D twin has < 2 territories.
3. `meta.json` line 448 still writes `open_decision: "... UNRESOLVED — DETECTOR-SPEC v0.2 §0 B1"` beside
   `target_definition: "DECISION B1, settled"`. Shipped in all three M1 packages.
4. `exporter_sha256` in shipped `meta.json` is the pre-18:03 hash; content identical. Re-export `--m1` (3 s) and
   re-issue `MANIFEST.json` when 3 is fixed.

---

## 6. What is now false or stale in the documents

| where | claim | status |
|---|---|---|
| STUDY-PLAN-v2 banner | "B1 removed the 'fewer than 2 shared territories' skip, so 114/124" | **false** — B3 rescued that row; B1's guard removes Protocol C on 47/118 T1 and 49/149 T2 rows cohort-wide |
| STUDY-PLAN-v2 banner, CFD-ARM-SPEC §17, manifest header | B3 = "the truncation radius now scales with T4's calibre error" | **incomplete** — the mechanism is now `trunc_ref` pinning with `trunc_for` as pre-filter; and it is not exact (6/298) |
| STUDY-PLAN-v2 banner | T1 C_ratio 1.049 → 0.928, residual 0.097, ΔFFR 0.078 "measured" | true numbers, **n = 1**; say so |
| STATISTICS-PLAN §P2 | "Protocol A … passes the perfusion check by construction" | **false under B1** (discrete A 12/19 pass; T1/T2 A residuals 0.10–0.17) |
| STATISTICS-PLAN §P2 | 3D target "distributed across surviving outlets in proportion to their own clean flow" | **undefined for a T2 stump** (clean flow 0 → wall; §5.2.1) |
| STATISTICS-PLAN §9 | exclusion "≥ 2 outlets for missed-branch/truncation and for Protocol C" | **not the coded rule** (≥ 2 clean territories with survivors); T1/T2 × C absent on RCA; T2 × RCA residual undefined under all protocols; "failed fit at search bound" class (DETECTOR-SPEC §9 says §9 must name it) absent |
| STATISTICS-PLAN §P3 withdrawn box | +0.173 → −0.032 | still true after `trunc_ref` (−0.0329) |
| CFD-ARM-SPEC §11 | "which one Protocol C targets is an open decision … `Q_clean_surviving_mls` is what `ablation.py` currently targets" | **false** |
| CFD-ARM-SPEC §11 | `closed` cases "(T2 stump, T4 new leaf)" | T4 new leaf no longer exists (except the 6 residual rows of §3.1) |
| CFD-ARM-SPEC §10 | `ablation.py:145–155`, `156–186` | stale line refs (now 227–234, 238–278) |
| CFD-ARM-SPEC §17 B1 | M1 T1 outlet prescribed 0.173 instead of 0.078 | true (shipped `bc_C_flows.csv`: `out_558` 0.1735) |
| DETECTOR-SPEC §0 | table: B1 "SETTLED"; paragraph below: "B1 … it has not been applied"; §11 item 1: "This has not been applied" | **self-contradictory / stale** |
| DETECTOR-SPEC §0 B2 row | cites `ablation_smoke_POSTFIX` | fine |
| `error_types.py` header lines 20–21 | "T2 truncates at a fixed 15 mm … shorter than RUNOFF" | **stale** (hashed file; the constant's own comment is correct) |
| `ablation.py` `summarise()` footer | "A keeps the CLEAN bed, so it passes the check by construction" | **false under B1** |
| `zerod_ffr.py` line 122 docstring | "Pinning by coordinate is exact" | exact only on the adding side (§3.1) |
| shipped `meta.json` ×3 | B1 "settled" and "UNRESOLVED"; `exporter_sha256` | contradiction; stale hash |
| `protocol/COHORT-FROZEN-2026-09-18.sha256` | code hashes | **FAILS on `zerod_ffr.py`, `ablation.py`, `export_cfd_case.py`** (edited 18:03–18:04 after the 17:42 re-issue); header's B3 description is the superseded mechanism; cohorts and results still verify |

---

## 7. MUST / SHOULD

**Stage A + M1 — nothing gates the start.** Cosmetic, when convenient: fix `open_decision` string (exporter line 448),
re-export `--m1`, re-issue `MANIFEST.json`.

**Before lodging the pre-registration / running the ablation (minutes each, then re-run the smoke once):**
1. `zerod_ffr.py` line 124: `trunc_ref` authoritative (`=` not `&=`); then drop or keep `trunc_for`. Re-run
   `--verify` (both beds) and the smoke; expect the smoke unchanged. Alternatively declare the 6 residual rows — but
   the fix is smaller than the declaration.
2. `error_types.py`: replace the import-time `assert` with a raise that `-O` cannot strip, located where the constant
   lives; fix header lines 20–21.
3. STATISTICS-PLAN §9: state the coded exclusion (≥ 2 clean-partition territories with surviving members), the
   cohort-wide consequence (T1 × C ≈ 66–71, T2 × C ≈ 92–100 per bed, RCA essentially absent from both; T2 × RCA has
   no residual under any protocol), and the failed-fit-at-bound class. §P2: reword the Protocol A note; define the 3D
   split rule for stumps. Then §P1/§P2's vessel stratification knows its empty cells in advance.
4. Re-issue the code manifest after 1–2 (the project's own rule: an edited hashed file re-issues the manifest).
5. DETECTOR-SPEC §7.1/7.2/7.4 columns and rows that `ablation.py` does not yet write (`w_sum`, `r_ref_root_mm`,
   `L_resolved_mm`, per-territory file with `Q_achieved`, clean rows with their own `run_id`): if the run must not be
   repeated after registration, add them before running. Twelve minutes of compute is cheap; a post-registration code
   change is a deviation.
6. Correct the stale statements of §6 (banner, CFD-ARM-SPEC §11, DETECTOR-SPEC §0/§11, `summarise()` footer).

**Before the study batch is packaged (not before M1):** §5.2 items 1–2 — the T2 stump split rule and the exporter's
partition — on top of the previous pre-flight's MUST 5.

**SHOULD:** state n = 1 wherever the smoke's T1 numbers are quoted; one sentence on the 14 instances where the
25 mm cut now keeps a 15–25 mm branch.

---

## 8. The single highest-risk item

**B1's territory guard removes the thesis arm from the RCA.** Protocol C — the "validated model" the paper is about —
does not exist for T1 on 40 % of rows and for T2 on 33 %, almost entirely the right coronary (T2: 99/100 RCA rows have
zero territories, so even Protocols A and B have no residual there). The code declares it row by row and the choice is
defensible (the alternative partition targeted a number that omitted the deleted territory), but the pre-registration
documents describe a different exclusion rule, stratify P1/P2 by vessel, and nowhere say that the absorption finding
will be an LAD/LCX finding. Lodging the registration in that state is the one thing today that a reviewer could later
call undeclared post hoc exclusion. It is a paragraph to write, not code to change — write it before lodging.
