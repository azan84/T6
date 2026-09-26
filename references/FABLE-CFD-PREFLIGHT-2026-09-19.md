# Pre-flight audit — the CFD plan itself, before the 16-core machine is committed

**Reviewer:** Fable 5.1 (independent pre-flight; not a peer review) · **Date:** 2026-09-19
**Question:** is the CFD PLAN sound enough to spend ~12 days of a 16-core machine on? Not the exporter (reviewed twice
already, `FABLE-REVIEW-EXPORTER-2026-09-19.md`, `FABLE-VERIFY-EXPORTER-2026-09-19.md`).
**Read:** `cfd_handover/` (START-HERE, stageA/, bc/, returns/, packages/M1/ in full), CFD-ARM-SPEC v0.2, DETECTOR-SPEC
v0.2, STATISTICS-PLAN v1.0, STUDY-PLAN-v2, NEXT-PLAN-2026-09-19, `code/{zerod_ffr, stageA_benchmark_0d, ablation,
error_types, export_cfd_case, discrete_arm}.py`, the frozen 3D subset, the smoke results.
**Probes** (all in `FABLE-CFD-PREFLIGHT-2026-09-19-probe/`; nothing in `code/`, `protocol/`, `cfd_handover/` or
`results/` was modified; the ablation was not run at cohort scale):

| file | what it is |
|---|---|
| `expected_0D_REGENERATED.csv` | `stageA_benchmark_0d.py` re-run with today's `zerod_ffr.py`, output redirected |
| `probe1_stageA_stability_voxel.txt` | kinematic checks; 0D discretisation floor; resistance-BC loop gain; scan-14 voxel size; shipped inlet normal |
| `probe2_subset_T1_T2_outlets_Re.{txt,csv}` | surviving outlets/territories under T1/T2/T4 and throat Re for all 30 frozen instances |
| `probe3_cell_census_T4_closed.txt`, `probe3_ablation_rows_subset30_discrete.csv`, `probe3_T4_closed_outlets.csv` | `ablation.run_instance()` executed as-is on the 30 instances, discrete bed: which (error × protocol) cells exist |
| `probe4_T4_carry_fixed.{txt,csv}` | T4 under Protocol A: as coded vs territory-preserving vs radius-only |

---

## 0. Verdict: **GO-WITH-CHANGES** — start Stage A and Gate M1 today after two minutes of fixes; **do not launch the 12-day study batch as specified**

- **Stage A's acceptance numbers are NOT stale.** `expected_0D.csv` is byte-identical to a regeneration with the current
  code (§1.1). The Poiseuille, kinematic and geometric constants all check. The operator will not chase a phantom.
- **Two things in the handover will burn days for reasons that have nothing to do with real lumens**, and both are
  knowable now: the coded resistance BC as templated is *unstable on the mildest cases* (relax 0.2 against a stability
  bound of 0.134 on `sten00`, ≈ 0.10 on the real lumens — §1.3), and the M1 packages still ship the ostium normal 37°
  off-axis (the fix landed in `tangent()` but both call sites still pass `path[0]` — §3.1).
- **The study batch is not what §4 says it is.** Running the ablation's own `run_instance` on the 30 frozen instances
  (§2.1): only **407 of the 510 solves per tier** that §4 counts have a 0D counterpart; **T2 has no Protocol A or C
  cell on any RCA instance** (single-outlet stump); **T1 × C does not exist on 7/30**; and **T4 in the discrete bed is
  artefact-contaminated in both fidelities** — 66 of 133 outlets are written `closed` under Protocol A, 9/30 instances
  have no bed left, and the coded T4 × A ΔFFR is **+0.13 with the wrong sign** (§2.2). Add the 240 resting-state solves
  for a Fossan constraint the 0D side has declared *not implemented*, and the unspecified 3-day pulsatile Stage D, and
  roughly **40 % of the planned machine time produces nothing the paper can use**.
- **B1 does not block Stage A or M1** (§2.6). It blocks every Protocol C cell of T1/T2 in the study batch, and the
  packaging of those cells — which is fine, because the batch should not start before B1, the T2 stump decision (B2)
  and the T4 fix are settled anyway. Stage A + M1 take about a week; that is the window to settle them.

The MUST list is in §6. Items M1–M4 are minutes of work and gate today's start; M5–M7 gate the batch.

---

## 1. Stage A materials

### 1.1 `expected_0D.csv` — current, not stale
Regenerated with `zerod_ffr.py` as of 2026-09-18 19:57 (lesion-rule rewrite, discrete bed) and `ablation.py` as of
2026-09-19 (minimiser fix): **`diff` is empty** — every column, to the last digit. Why the three changes had no effect:
the lesion-rule rewrite (local-maximum throats, tree-distance merge) changes nothing on a single cosine lesion in a
straight tapering tube — one throat either way; the benchmark builds its bed by hand (`w[leaf] = r_ref³`), and
`Tree(bed="discrete")` gives the identical result (single outlet: the exponent is absorbed by C — checked, diff 0.0);
the minimiser fix touches only Protocol C, which Stage A never runs. The frozen subset's `ffr_discrete` also matches
today's code to 1e-16 (probe 2).

The 0D numbers carry their own discretisation floor, which the operator should know when tabulating A2: refining the
benchmark from 0.25 mm to 0.05 mm node spacing moves FFR_meas by 0.00000 / 0.00004 / 0.00033 / **0.00073** (sten00 /
50 / 70 / 80) and flow by ≤ 0.0012 mL/s. So the fourth decimal in the CSV is not meaningful, and the 3D-vs-0D gap
(expected to be tens of mmHg-equivalents at 70–80 %DS from the K_t = 1.52 lumping) will dwarf it. Fine as a
comparison; say "±0.001" in the note.

### 1.2 Constants — all check
ν = 0.004/1060 = 3.7736e-6 ✓ · P_a/ρ = 11.31979 ✓ · P_v/ρ = 0.62888 ✓ · R_kinematic = R/ρ ✓ · A1 Poiseuille
8μLQ/(πr⁴) = **90.541 Pa** ✓ · Re_pipe 168.7, entrance ≈ 0.06·Re·D ≈ 30 mm so x = 60–90 mm is fully developed even with a
uniform inlet ✓ · throat radii 1.4850 / 0.7425 / 0.4455 / 0.2970 mm ✓ · Re_throat 2ρQ/(πμr) ✓ (428 at sten70).
One bookkeeping item the operator will otherwise puzzle over: the 0D imposes P_aorta as a *static* pressure at x = −15 mm;
`totalPressure` in 3D gives static = p₀ − ½|U|², i.e. 11.5 Pa (uniform) to 23 Pa (parabolic) lower at the inlet plane
at Q = 1.5 mL/s — **0.001–0.002 FFR**, inside the tolerance, but it is a systematic offset in the direction "3D lower"
on sten00/sten50 and should be named in the A2 note rather than discovered.

### 1.3 `bc/resistanceOutlet.md` — plausible OpenFOAM, two defects that will bite on day one
The C++ is sound: `phi` on a boundary face is positive for outflow, `gSum` is parallel-safe, `operator==` assigns,
`const scalarField pOld(*this)` captures the previous iterate, `codedFixedValue` compiles on first run. Version notes
are adequate for ESI; add that **Foundation 11+ has no `simpleFoam` binary** (`foamRun -solver incompressibleFluid`),
so the operator should record the line before choosing.

**(a) The relaxation factor is not a tuning knob, it is a stability bound, and 0.2 is on the wrong side of it for the
easy cases.** The template is an explicit fixed-point iteration on p_out. Linearising: a change δ in p_out changes the
domain flow by −δ/R_epi (R_epi = epicardial resistance between the total-pressure inlet and the outlet), so the target
moves by −(R/R_epi)·δ. With loop gain g = R/R_epi the iteration p ← (1−α)p + α·target has linear gain 1 − α(1+g),
stable iff **α < 2/(1+g)**. From `expected_0D.csv` (probe 1):

| case | R_epi (Pa s m⁻³) | g = R/R_epi | α_max | template α = 0.2 → gain |
|---|---|---|---|---|
| sten00 | 5.00e8 | **13.96** | **0.134** | **−1.99 (diverges)** |
| sten50 | 8.12e8 | 8.59 | 0.209 | −0.92 (marginal) |
| sten70 | 2.97e9 | 2.35 | 0.60 | +0.33 |
| sten80 | 9.26e9 | 0.75 | 1.14 | +0.65 |
| M1 scan 14, clean (healthy_main 0.951 ⇒ epicardial share ≈ 5 %) | — | ≈ 15–20 | **≈ 0.10** | diverges |

SIMPLE's own under-relaxation lags the flow response and will damp this somewhat, so sten00 may oscillate rather than
blow up — but the point stands: **the case that fails first is the one with the *least* epicardial drop**, i.e. the
clean and mildly diseased cases that make up most of the study, not the 80 % throat. Every clean/baseline real-lumen
case has g ≈ 15–20. An operator who starts A3 on sten00 at α = 0.2, sees the outlet pressure ring, and reads §16's
"coupled resistance BC unstable on multi-outlet trees (→ lower relaxation)" has no number to lower it to and will
spend days on it. **Fix (MUST 3):** state the bound in the template, default α = 0.05, run sten00 first as the A3
acceptance case. Better still, replace the relaxed fixed point by the one-line Newton update, which converges in a
handful of outer iterations regardless of g: estimate R_epi from the previous iterate, `R_epi = (P_in − ρ·p̄_old)/Q_old`,
then set `p_new = (P_v·R_epi + R·P_in)/(R + R_epi)/ρ` (the fixed point of the linearised loop), with light relaxation
0.5 for safety. Keep α as a fallback.

**(b) "With several outlets, prescribe all but one and leave the last as a pressure outlet, or the system is
over-constrained" is wrong, and following it breaks Protocol C on every multi-outlet case.** With a total-pressure
inlet the pressure level is fixed by the inlet and the inlet flux is ΣQ_i by continuity; prescribing every outlet is
well-posed (the over-constrained combination is *velocity* inlet + all velocity outlets). If one outlet is left as a
pressure outlet its flow is whatever the solver returns, not the clean target — so its residual is not ~0 and its
R_i = (p_i − P_v)/Q_i is derived at the wrong flow. That is not the flow-matched Protocol C of §2.2/§2.3; the thesis
panel for that outlet is meaningless. **Delete the sentence (MUST 4).** A4 in Stage A is single-outlet and will not
catch this; M1's T1 Protocol C solve (5 outlets) is the first place it matters.

### 1.4 `make_stageA_geometry.py`, template CSV, START-HERE
Geometry generator: correct, radius law shared with the benchmark by import ✓. Return template: complete; add
`relax_used`, `outer_iters_to_0.1pct`, and a `station_area_ratio` column (§4.2). START-HERE: add the α bound and the
`simpleFoam`/Foundation-11 note; budget A5's fine level on sten80 explicitly (12 → ~24 → ~48 cells across a 0.594 mm
throat with the ±20 mm refinement box is several million cells — this is where a "quick" Stage A quietly eats a day).

---

## 2. Is the study design still worth 12 days?

### 2.1 The cell census — what actually exists to compare against
`ablation.run_instance(row, "discrete")` on the 30 frozen instances, unmodified (probe 3):

| error type | A ok | B ok | C ok | why the rest are missing |
|---|---|---|---|---|
| T1 missed branch | 30 | 30 | **23** | 7 RCA instances have 2 outlets; deleting the branch leaves 1 territory → "fewer than 2 shared territories" |
| T2 truncation | **20** | 30 | **16** | 10 RCA: the stump is the only leaf and is `closed` under A → "no bed left"; 14 lose their second territory |
| T3 length | 30 | 30 | 30 | — |
| T4 taper | **21** | 30 | **9** | §2.2 |

**299 of 360 cells; 407 of the 510 solves per tier that §4 counts** (30 baseline + 221 A/B + 2×78 C). Protocol C on
RCA exists for T3 only. The κ for T1 × C is on 23 instances, T2 × C on 16, T4 × C on 9 — ±0.25 to ±0.4, not ±0.2.
None of this is visible from `CFD-SUBSET-FROZEN`, which records outlets on the *clean* tree; the spec's own rule
("≥ 2 outlets for missed-branch/truncation instances and for any Protocol C run") was applied to the clean tree, not
to the corrupted one. Also, **T2's 20 mm measurement node survives in 0/30** (B2, `T2_KEEP_BEYOND` 15 < `RUNOFF` 20):
every T2 measurement is at the stump. In 3D the stump is an outlet patch, so under Protocol B the "measured" pressure
there *is the boundary value* P_v + R·Q — a number the BC sets, not one the flow field produces. 0D and 3D will agree
on T2 trivially. That is one more reason to resolve B2 as `T2_KEEP_BEYOND ≥ 20 mm` (plus the 3-D extension stub).

### 2.2 T4 in the discrete bed is a truncation artefact, in 0D and therefore in every T4 package — MUST fix before either arm runs it
`t4_taper` scales r by 0.93 from the lesion's proximal shoulder distally; `Tree()` re-fits r_ref, which also scales;
truncation is an *absolute* r_ref < 0.60 mm, so every branch that was between 0.60 and 0.645 mm now ends earlier — the
leaf moves proximally. Its clean counterpart is an interior node with w = 0, so `ablation.py` Protocol A (and the
exporter's `bc_A.csv`) writes **`closed` — a wall — for a territory that was merely under-sized**, and Protocol C
finds no clean flow in that territory and drops it. CFD-ARM-SPEC §11 names this case ("T4 new leaf") as if it were a
deliberate, minor edge. On the frozen 30 (probe 3/4):

| T4 under Protocol A, discrete bed, n = 30 | mean ΔFFR | flips vs 0.80 | notes |
|---|---|---|---|
| **as coded** (moved leaves closed) | **+0.130** | **13** | 66 of 133 outlets closed; **56 % of the clean bed weight lost on average, 100 % in 9/30** (unsolvable: "no bed left") |
| clean territory weight carried to the moved leaf | −0.025 | 5 | |
| radius override on the clean tree (pure 1/r⁴, r_ref frozen) | −0.021 | 4 | |
| Protocol B (exists for all 30) | −0.019 | — | |

Under-sizing a lumen must *lower* FFR (viscous resistance × 1/0.93⁴ = 1.34); the coded discrete T4 × A raises it by
0.13 because it walls off half the bed and sends the flow elsewhere. **STATISTICS-PLAN §P3's "taper under Protocol A:
6 flips leaky vs 43 discrete in probe data" is this artefact, not a bed-structure interaction** — the leaky bed
re-fits its leak weights on the same nodes and never closes anything. Consequences: H1 (topological vs calibre) is
contaminated in the discrete bed; the T4 packages ask the CFD operator to wall off outlets; T4 × C exists on 9/30.
**Fix direction (analysis side, before the pre-registration and before any T4 package is run):** T4 must not change
the active node set — build the tapered tree with the clean tree's truncation set (e.g. `Tree(..., reference=t)` for
the truncation decision only, or scale `r_trunc` with the taper on the tapered subtree), or carry the clean territory's
bed weight to the moved leaf under A. Then re-run the smoke, regenerate the T4 packages, and re-freeze the discrete
bands if they move. The DETECTOR-SPEC §3.2 claim "T4 scales r and r_ref together, leaving every ratio invariant" is
true of ratios and false of the absolute cut; say so there.

### 2.3 240 solves for a constraint that is not applied
§4 counts "+4 resting-state solves for the Fossan constraint on C" per tier per instance (240 solves, ~2 of the 12
days). §10 and `ablation.py`'s header both declare resting-state re-simulation **not implemented — this steady
hyperaemic model has no autoregulation.** A 3D quantity with no 0D counterpart cannot enter the ladder; it would be
computed, returned, and never used. **Drop them (MUST 5a).** If a rest→hyperaemia variant is ever wanted, it is a 0D
decision first.

### 2.4 Stage D (pulsatile, ~3 days) is unspecified and its stated purpose is already served
"3 instances × 2, pulsatile, real lumen" — no inlet waveform, no outlet model (pure R? RCR? tuned how? — the "15
solves per condition" the spec itself calls a pulsatile number), no convergence criterion. Its purpose is the
mechanism figure (DETECTOR-SPEC §8.1: the spatial pressure field with outlets matched and interior wrong) — **which a
steady Protocol C solve already produces**, and §15 forbids any pulsatile claim. The one thing pulsatile would add is
the steady-vs-cycle-mean FFR check that the CFD review §6.1 asked for against attack D (quadratic loss ⇒ steady at
mean flow under-reads the cycle-mean drop). **Either re-specify Stage D as that check (waveform, RCR values, 2 cases)
and queue it last, or cut it (SHOULD 1).** Do not let it run "because it was in the plan".

### 2.5 Polyball at n = 30, and before the real tier
The polyball tier's job is the physics-gap estimate (a continuous Bland–Altman) and insurance for the M1 kill. Neither
needs 30 instances × 5 geometries before the real tier exists. And the §5 order (Stage B polyball → Stage C real) puts
the *control* ahead of the *primary*: if M1's measured wall-clock is 3× the estimate (likely — §5.3), the machine has
spent two weeks on the rung the paper cannot lead with. **Once M1 passes, the real tier goes first; polyball runs on a
10-instance stratified subset (LAD/LCx/RCA 4/3/3, one per band) and expands only if time remains (MUST 5b).** Stage B's
other role — pipeline shakedown on surfaces that cannot fail — is already done by Stage A and M1.

### 2.6 What the 3D arm is worth now, and what B1 does to it
Given what is now known — the detector does not use the 3D arm at all (DETECTOR-SPEC §8: no §3 statistic needs a
pressure plane), H4's κ is direction-only at n = 30 and worse per cell (§2.1), and H5's tuning-side AUC ≈ 0.65 is
independent of fidelity — the arm's entire value is **C2's replication: the within-fidelity ΔFFR Bland–Altman per
error type × protocol, and the thesis panel (outlet-flow residual → 0 while FFR error persists) at 3D on real
lumens.** That is worth doing, and the continuous endpoint is what n = 30 can actually estimate. Register H4 as
descriptive (κ with CI), not as a κ > 0.6 test — the STATISTICS-PLAN already half-says this.
Proportionate spend: **real tier ≈ 340 useful solves** (baseline 30; T1 106; T2 82 where defined; T3 120 — T4 after the
fix) ≈ 3 days at the spec's own 20 min × 8 cores, two jobs side by side; polyball-10 ≈ 1 day; Stage A + M1 ≈ 1 week
wall-clock, mostly human. **~5–6 machine-days, not 12**, and the extra week is the buffer for M1's timings being wrong.

**B1 — does it change what the CFD arm computes or records?** *Computes:* yes. The per-outlet 3D Protocol C prescribes
`bc_C_flows.csv`; under the coded (surviving) definition each surviving outlet gets its own clean flow, under the
STATISTICS-PLAN (full-territory) definition the surviving outlets of the affected territory must also carry the deleted
branch's share. On M1's T1 case the surviving LAD-territory outlet `out_558` is prescribed **0.078 mL/s as shipped vs
0.173 under the full-territory definition — 2.2× the flow**, hence a different derived R and a different FFR. B1 also
needs a rule the spec does not have: **how the missing share is split among several surviving outlets in the per-outlet
variant** (proposal: scale every surviving outlet of that territory by Q_full/Q_surviving — the per-outlet analogue of
the 0D's single global scaling, and exact when one outlet survives). *Records:* no change — per-outlet Q and p, derived
R_i, station p̄ and flux are the same return set either way.
**Can M1 and Stage A start before B1 is settled? Yes, without reservation.** Stage A has no Protocol C target. M1's
pass criterion is a checkMesh-clean mesh, a converged solve, both BC modes stable, and the as-meshed radius returned —
the *value* of the T1 Protocol C prescribed flow is not part of it. Label that one solve "pilot — target definition
pending" in the return. **What must NOT start until B1:** packaging or solving any Protocol C cell of T1 or T2 (and T4)
in either tier. Baseline, A, B and all T3 cells are B1-independent — but with B2 and the T4 fix also open, the clean
rule is simply: **no study batch until B1, B2 and the T4 fix are settled and the exporter is re-run.** The week of
Stage A + M1 is the window.

---

## 3. Sequencing and kill criteria

### 3.1 The M1 packages still ship the wrong inlet normal — the fix did not reach the call sites (MUST 1)
`FABLE-VERIFY-EXPORTER` §3.2 found the ostium normal 32° off because `tangent(t, 0)` fell through to the placeholder
and the code substituted node 33 (the LAD's first node, 11.4 mm downstream). `tangent()` was fixed to walk forward at
the root — but `stations()` line 251 and `build()` line 366 still call `tangent(t2, int(path2[0]))`, i.e. node 33.
Probe 1 on the shipped `inlet.json`: normal (0.9399, −0.1334, −0.3143) = `tangent(t, 33)` exactly (cos 1.000);
`tangent(t, 0)` = (0.9454, 0.2764, 0.1725), **37.1° away**; first root edge (0.9565, 0.2897, 0.034), 31.8° away. The 5-D
inlet extension will be built 37° off the ostial axis on all three packages. Change both calls to `tangent(t2, 0)`,
re-export (3 s), re-check the SHA-256s in `MANIFEST.json`. Same false-kill class as the flood-fill: M1 would test the
package, not the lumen.

### 3.2 The lesion cannot be built from the package as written (MUST 2)
Scan 14's mask is **0.318 × 0.318 × 0.5 mm**. The 80 % throat is r = 0.2306 mm — a **0.46 mm diameter, 1.45 voxels**.
Marching-cubes triangles are ~0.38 mm on edge; the radial-deformation surface rule needs edges ≤ r_throat/8 = 0.029 mm
in the lesion window to reproduce the cosine law (**~13× subdivision per edge**), and §6.1a's "as-built throat radius
within 1 % of target" check. CFD-ARM-SPEC §17 lists both as open; the package `README.md` build order ("3. Marching
cubes, then apply surface_rule") does not. An operator following the README will deform a 0.38 mm-faceted tube and
"pass" M1 on a lesion that is not 80 %; the as-meshed radius return would reveal it a week later. Put "subdivide the
surface within |s − c| < L/2 + 2 mm to edge ≤ r_throat/8 (Loop or butterfly; then Taubin), then apply the surface rule,
then assert the as-built minimum radius = r_target_mm ± 1 %" into README step 3 and into `mask_edit.json.surface_rule`.

### 3.3 The 5-day kill and the §9 fallback
The kill is right. The fallback ("20 real-lumen instances × T1 + T2, plus the full polyball tier") needs two edits:
T2 on RCA has no A or C cell and its measurement is at the stump for every instance (§2.1), so the fallback's
topological content is **T1 (A/B/C) + T2 under B**; and "full polyball tier" becomes the 10-subset of §2.5.
Also pre-freeze a **hashed reserve list of 10 instances** from the 77-pool (the CFD review asked for 40 with attrition;
the frozen subset is 30 with no reserve), so a meshing failure is replaced by rule, not post hoc (SHOULD 2).

### 3.4 Days that would be burned on things knowable today — the list
1. Resistance-BC relaxation bound (§1.3a). 2. "Leave one outlet free" (§1.3b). 3. Inlet normal (§3.1). 4. Lesion
subdivision (§3.2). 5. **Laminar convergence at Re 300–580:** throat Re on the 30 baselines is median 314, max 579,
**17/30 > 300, 10/30 > 400** (probe 2). The CFD review §6.1 said post-stenotic jets go unsteady at a few hundred and
recommended flagging at ~300 with a pre-agreed fallback (`pimpleFoam`, steady BCs, time-average — never a turbulence
model); v0.2 kept the flag at ~1000 and has no fallback. Stage A sten70/sten80 (Re 428/395) are the test of exactly
this; **define the fallback now (MUST 6)** so a stalled `simpleFoam` residual on A2 is a recorded outcome with a
next step, not a stop. 6. **Timing:** the 20 min × 8 cores per solve is a 1 M-cell figure; 12 cells across a 0.46 mm
throat with the ±2 L refinement box, 4 boundary layers, 5–8 outlets with 3-D extensions, and ~4000 SIMPLE iterations
with a relaxed coupled BC is more like 2–5 M cells and 1–2 h. M1 measures it; what protects the paper is a **priority
order** so any stopping point is publishable: (1) real tier, baseline + T1 {A, B, C} on all 30 (≈ 136 solves);
(2) real T3 {A, B, C} (120); (3) real T2 where defined (82); (4) polyball-10 (≈ 110); (5) T4 after the fix; (6) polyball
remainder; (7) Stage D if re-specified. 7. The station script, validated on Stage A (§4.3).

---

## 4. The probe/station change (DETECTOR-SPEC v0.2 §8)

### 4.1 Is the plane-clipping rule implementable? Yes — but not in-solver
"Keep only the connected cut component containing the station's centreline point, within a sphere of ≈ 2·r_ref" is a
complete rule for a post-processor and not for a function object: OpenFOAM's `surfaceFieldValue` on a `plane` can
bound the cut (ESI: `bounds`) but cannot select a connected component. Recipe (pvpython, once per case, all stations):
`OpenFOAMReader → Slice(plane: station x, n) → Clip(sphere: centre station, radius 2·r_ref) → Connectivity(extraction
mode: closest point, seed = station) → IntegrateVariables` → p̄ = ∫p dA / A, Q = n·∫U dA (the flux through any
lumen-spanning surface equals Q, so a slightly oblique plane still gives the right flow; only the area QA is sensitive
to the normal). Keep the in-solver function objects for inlet/outlet `phi` sums and the convergence monitor.

### 4.2 The QA column needs the local radius, and `probes.csv` does not carry it (SHOULD 3, before the batch)
"Cut area vs π·r_local²" — `probes.csv` ships `r_ref_mm` only. At the throat r_ref = 1.15 mm against r_target = 0.23 mm:
the ratio would read 0.04 and flag every throat station in the study. Add `r_target_mm` (as-edited, already in
`centreline.vtp` by `tree_node`) to `probes.csv`; for M1 the operator can join on `tree_node`. Also: `bif_prox` /
`bif_dist` snap to 0.8–0.95 D (verify §3.4) and can share the carina's cut with the daughter — the closest-point
connectivity handles it, but the area ratio will show it; and for T2 the `measurement` station coincides with the
stump's outlet cap — state which plane is meant (the clipped face, before the extension).

### 4.3 Cost — negligible only if scripted, and it must be validated on Stage A
31–40 stations × ~400 useful real-tier solves ≈ 16 000 cuts; ≈ 1 s each with the case loaded once ≈ 4–5 CPU-hours for
the whole study, on spare cores during the batch. Interactive, it is weeks. Stage A is where the script gets its
acceptance test for free: on the analytic geometries the cut area is π·r(x)² exactly, so **"station_area_ratio within
2 % at all five planes" belongs in A2's deliverables (MUST 7)**.

---

## 5. Anything else

- **Blinding** (§13): `bc_A × bc_C_flows` reconstructs the clean outlet pressures — already noted in every package; the
  corrupted-geometry prediction stays blind. Adequate.
- **The analysis side is not ready to receive results:** `ingest_cfd_radius.py` (0D twin from as-meshed radii) and the
  per-outlet 0D Protocol C (§10, two open boxes) do not exist. Not machine-blocking; schedule them during Stage A/M1 so
  the first returned CSV can be compared the day it lands.
- **RAM:** 2 GB per M cells × 2–5 M cells × two side-by-side jobs — check the box has ≥ 32 GB before A5's fine level.
- **The M1 T1 package is fine to run as a meshing test** with the caveats in §2.6 and §3.1–3.2; its Protocol C solve's
  numbers are pilot-only.
- **Numbers that surprised me:** the mildest stenosis is the hardest case for the coded resistance BC (g = 14 at 0 %DS
  vs 0.75 at 80 %DS); the discrete-bed T4 × A cell closes half the coronary bed on average and 100 % of it on 9 of 30
  instances, and nobody would see it in the 3D results until the sign of ΔFFR came back positive; T2's measurement
  point is an outlet patch on all 30 instances, so 0D and 3D would have "agreed" on T2 by construction.

---

## 6. MUST / SHOULD

**MUST — today, before the machine starts (minutes each):**
1. `export_cfd_case.py`: `tangent(t2, 0)` at both inlet call sites (`stations()` root row, `build()` `inlet.json`);
   re-export `--m1`; new SHA-256s in `MANIFEST.json`. (§3.1)
2. Package README step 3 and `surface_rule`: subdivide the lesion window to edge ≤ r_throat/8 before the radial
   deformation; assert as-built throat radius = `r_target_mm` ± 1 %. (§3.2)
3. `bc/resistanceOutlet.md`: state the stability bound α < 2/(1 + R/R_epi); default α = 0.05 (or the Newton update);
   sten00 is the first A3 case. (§1.3a)
4. `bc/resistanceOutlet.md`: delete "prescribe all but one and leave the last as a pressure outlet"; with a total-pressure
   inlet every outlet is prescribed in the first Protocol C solve. (§1.3b)

**MUST — before the study batch (Stages B/C) is packaged or launched:**
5. Re-cut the batch: (a) drop the 240 resting-state solves; (b) real tier first, polyball on a 10-instance subset;
   (c) no T4 package runs until the discrete-bed T4 truncation artefact is fixed in `zerod_ffr`/`error_types`/
   `ablation`, the smoke re-run, and the packages regenerated; (d) T2 only where the cell exists in 0D and only after
   B2 (`T2_KEEP_BEYOND`) is decided; (e) no Protocol C cell of T1/T2 until B1 is decided, together with the
   intra-territory split rule for the per-outlet variant; (f) run in the priority order of §3.4. (§2)
6. Pre-agree the non-convergence fallback for Re > ~300 (`pimpleFoam`, steady BCs, time-averaged fields; never a
   turbulence model) and record the convergence history for every solve; Stage A sten70/80 is the test. (§3.4)
7. Station post-processing script (§4.1) written and validated on Stage A: area ratio within 2 % on all five planes;
   add `station_area_ratio` to the return template. (§4.3)

**SHOULD:**
1. Re-specify Stage D as the steady-vs-cycle-mean check with stated BCs, queued last — or cut it. (§2.4)
2. Freeze a hashed 10-instance reserve list for attrition. (§3.3)
3. Add `r_target_mm` to `probes.csv`; state the T2 measurement plane. (§4.2)
4. Register H4 as descriptive (κ with CI) and quote the per-cell n from §2.1 in the STATISTICS-PLAN; correct §P3's
   "43 discrete vs 6 leaky" T4 × A sentence once the artefact is fixed. (§2.2, §2.6)
5. Note the totalPressure dynamic-head offset (0.001–0.002 FFR) and the 0D discretisation floor (±0.001) in the A2
   note; add the Foundation-11 `simpleFoam` caveat and the RAM check to START-HERE. (§1.2, §1.4, §5)
6. Build `ingest_cfd_radius.py` and the per-outlet 0D Protocol C during Stage A/M1. (§5)
