> ## ⚠ SUPERSEDED as the entry point on 2026-09-24 — read `WORK-ORDER-2026-09-24.md` first.
> Kept for the physics constants, per-case relax table and background, which remain correct.

# CFD work order — 2026-09-19. Read this before anything else in this folder.

**For:** whoever runs the next CFD session, on any machine. **Paper:** T6 (Paper 6).
**Supersedes `START-HERE.md` as the entry point** — `START-HERE.md` describes Stage A as if it were unrun. It is not.
Full specification: `../protocol/CFD-ARM-SPEC.md` §8 (Stage A), §7 (Gate M1), §6.2 (production meshing).

**Everything in this folder is kilobytes. Meshes, fields and STL files stay on the local disk of the machine that
makes them and NEVER go into Google Drive. Only small CSVs come back, into `returns/`.**

---

## 0. Where the project actually stands

A Stage A validation pass ran 2026-09-18/19 on OpenFOAM **ESI v2406** with cfMesh `cartesianMesh` and `simpleFoam`
(steady, laminar, incompressible) and is reported in `../STAGE-A-VALIDATION (1).pdf`. Read its §2 running summary
if you want the detail; the short version:

| Check | Case | Status |
|---|---|---|
| A1 Poiseuille pipe | pipe | **PASS** — ΔP 89.86 Pa vs analytic 90.54 (−0.75 %, tol 1 %) |
| A3 resistance BC | sten00, sten50 | **PASS** — p_outlet = P_v + R·Q to machine precision |
| A3 resistance BC | sten80 | **flagged pass** — tolerance met, stricter residual criterion not; numerical-vs-physical left open |
| A4 flow→resistance round trip | sten70 | **PASS** — derived R reproduces the prescribed flow to −0.012 % (tol 0.5 %) |
| A5 mesh independence | sten80 | **PASS** — finest-pair ΔFFR 0.000874 (tol 0.005) |
| A5 mesh independence | **sten70** | **NOT ESTABLISHED — this is Task 1 below** |
| A2 0D-vs-3D gap | six severities | informational; the gap reverses sign between 50 and 60 %DS |

**The single most important outcome: the coded resistance-outlet boundary condition works.** It had never been
compiled or run anywhere when it was written; it now has four independent real-hardware confirmations. Do not
re-litigate it.

**Gate M1 did not complete.** It blocked at meshing and never reached a solve. That is Task 2.

---

## 1. BEFORE YOU RUN ANYTHING — verify your local fixes are still in place

**This work order assumes you are on the SAME machine that ran the 2026-09-18/19 pass**, so the corrections below
are already in your working copy and you do not need to re-derive them. They are listed so you can **verify nothing
has regressed** — and because the copies in Google Drive are still the *pre-fix* versions, so if you ever re-pull
from Drive, or a colleague picks this up on another machine, these are what must be re-applied (see Task 3).

**Fix 1 — `bc/resistanceOutlet.md`: relax against the previous iteration.**
The relaxation must be applied against `p.prevIter()`, **not** the raw patch field. Against the raw field it
compounds under non-orthogonal correctors and the outlet pressure will not settle. Also use the per-case settings
below rather than one global number — the stability bound is `α < 2/(1 + R_outlet/R_epicardial)`, and it is
**tightest for the mildest case**, so `sten00` is the hardest case for this BC, not the easiest.

| Case | R (Pa·s·m⁻³) | relax | initial value (m²/s²) |
|---|---|---|---|
| sten00 | 6.977581 × 10⁹ | 0.05 | 10.5028 |
| sten50 | 6.974906 × 10⁹ | 0.08 | 10.1106 |
| sten70 | 6.974826 × 10⁹ | 0.20 | 8.0694 |
| sten80 | 6.974430 × 10⁹ | 0.25 | 5.2002 |

Do **not** use `residualControl` with this BC (it interacts with the relaxation); run a fixed iteration budget and
read the monitors instead.

**Fix 2 — `stageA/make_stageA_geometry.py`: wall normals.** The shipped version has inverted wall normals. After
generating, verify outward orientation on 100 % of wall facets by direct check before meshing anything.

**Fix 3 — the case template needs `div((nuEff*dev2(T(grad(U)))))` in `fvSchemes`.** Its absence is not caught by
source review; it fails at run time.

**Also:** `pymeshfix`'s convenience wrapper `MeshFix.repair()` **silently caps every open boundary** — 6 intended
outlets became 0 in testing. Use the granular `degeneracy_removal()` / `intersection_removal()` methods instead.
This is undocumented upstream and will quietly destroy any surface that is supposed to have outlets.

**Common physics for every run below:** ρ = 1060 kg/m³, μ = 0.004 Pa·s → ν = 3.773585 × 10⁻⁶ m²/s. OpenFOAM
pressure is kinematic: P_aorta 11 998.98 Pa → **11.3198**, P_venous 666.61 Pa → **0.62888**. Inlet `totalPressure`.
FFR = (area-averaged static pressure at the measurement plane) / P_aorta. Report **area-averaged** section values,
never point values. Record throat Reynolds number for every solve.

---

## 2. TASK 1 (required) — re-run A5 mesh independence on sten70, at production resolution

### Why this is being redone

The 3-level A5 reported ΔFFR = 0.004732 against a 0.005 tolerance — a pass at 94.6 % of budget. A fourth level then
showed the pass was not measuring convergence:

| Level | Cells | FFR |
|---|---|---|
| coarse | 198,252 | 0.783960 |
| medium | 379,468 | 0.783200 |
| fine | 760,480 | 0.787932 |
| level4 | 1,886,884 | 0.792712 |

medium→fine = **+0.004732**; fine→level4 = **+0.004780**. The error is not shrinking despite 2.5× the cells, which
breaks the premise Richardson extrapolation and GCI both rest on. Celik gives apparent order p = 0.97 and absolute
U_FFR = **0.0175 — 3.5× the tolerance**; the Eça–Hoekstra fit is degenerate. The previous session reported this
honestly as "GCI not trustworthy" rather than quoting the passing number.

### The question this task must answer

**Is FFR still drifting because the throat is under-resolved, or because steady SIMPLE cannot converge this flow?**

This matters more than it looks. All of the previous pass's meshes were **deliberately coarser than the production
guidance in spec §6.2** — that pass was proving the pipeline, not producing study-grade numbers. So the drift may
simply be under-resolution. But if it persists at production resolution, then 3D FFR carries a discretisation
uncertainty **larger than the 0.005 that separates a decision flip from a non-flip**, and the study's cross-fidelity
comparison would be measuring mesh error rather than the geometric effect it exists to measure.

### What to run

Three levels, with the **production settings of spec §6.2 as the BASE level**, not as the finest:

- base cell ≈ D_local/20; refine the lesion region ±2 lesion lengths;
- **sten70's throat radius is 0.4455 mm (diameter 0.891 mm), so ≥ 12 cells across the throat means cells ≤ 0.074 mm
  there.** Record the achieved count — do not assume it.
- 4 boundary layers, growth ratio 1.2;
- `checkMesh` must report max non-orthogonality < 70°, max skewness < 4, no negative volumes;
- then refine ×~1.3 in linear cell size for levels 2 and 3.

Outlet: the coded resistance BC, R = 6.974826 × 10⁹, relax 0.20, initial value 8.0694. Inlet `totalPressure`
p0 = 11.3198. Measurement plane **x = 56.5 mm**.

Run a fixed iteration budget rather than `residualControl`, and for each level record: cell count, **cells across the
throat**, `checkMesh` summary, iterations, the **last-100-iteration mean FFR and its band**, outlet flow, and throat Re.
Expect a decaying transient early on — the previous pass saw a ~30-iteration swing at level4 that looked like a
persistent oscillation and turned out to be transient, settling to ±0.0003. Do not call an oscillation until you have
watched several hundred iterations.

### How to decide the outcome — do not come back for instructions

- **ΔFFR between the two finest < 0.005 AND successive differences shrinking** → **PASS.** The earlier drift was
  under-resolution. Record the production mesh settings; the study batch uses them.
- **Differences still flat (not shrinking) at production resolution** → **the effect is not numerical.** Do *not*
  keep refining. Run a **time-accurate `pimpleFoam`** on the finest mesh, time-average FFR over the last stable
  window, and report the mean and band. This settles the same open question hanging over sten80 (§A3 flagged pass).
- **Either way, report the number you get for the FFR discretisation uncertainty.** The analysis side currently
  declares a 0.003 FFR discretisation floor, and **that is a 0D figure with no 3D equivalent** — this task produces
  the 3D one, and it is needed before the study batch can be interpreted.

---

## 3. TASK 2 — Gate M1, on the shipped packages this time

### Status

M1 blocked at meshing and never reached a solve. The failure is well characterised and **it is not a surface-repair
or geometry-editing problem** — both of those were built and verified working. It is this:

> Both cfMesh **and** snappyHexMesh lose exactly one branch. It is not patch mislabelling: a `topoSet` query at the
> missing outlet's cap found zero faces of any kind, `constant/polyMesh/points` had no points there, and
> `checkMesh`'s own bounding box does not reach that branch. Roughly **17 mm of one branch, flow extension included,
> is simply absent from the meshed domain** — as though the castellation flood-fill classified it as disconnected.
> Serial and parallel runs are byte-identical, ruling out an MPI decomposition race. Cap planarity, facet-normal
> orientation, self-proximity, inter-branch clearance and a physical pinch were all checked and ruled out.
> `nCellsBetweenLevels` 3 vs 8 made no difference.

### What to try, in this order

1. **Run the shipped M1 packages — they have never been attempted.** `packages/M1/` contains three real-lumen cases
   on **scan 14** (clean lumen · 80 %DS lesion · missed branch). The previous pilot used **scan 837** with a
   separately-built pipeline; scan 837 is not in this study's cohort at all. The shipped packages define outlet
   planes explicitly, ship their own truncation and mask-deletion rules, and place their truncation at different
   coordinates. Start with `packages/M1/README.txt`, then each package's own `README.md`.
2. **The grid-offset test** — the previous session's own lead, identified but not completed. The truncation
   coordinate sat within **0.7 % of an exact background-mesh cell boundary**, which suggests a marginal
   cell-classification event during castellation rather than a defect in the surface. Shift the background mesh
   origin by half a cell and re-mesh. This is cheap and would confirm or kill the hypothesis. (The previous attempt
   failed only because a regex-based `blockMeshDict` edit script corrupted unrelated numeric fields — edit it by
   hand.)
3. **Mesh each branch separately and join with `mergeMeshes`/`stitchMesh`.** This sidesteps the single flood-fill
   mechanism entirely and is the most likely structural fix if 1 and 2 do not resolve it.
4. Inspect the **pre-snap castellated mesh** in ParaView at the disconnection point.

Reusable scripts from the previous attempt (outlet coordinate/tangent mapping, locally-restricted truncation
clipping, multi-solid STL capping, mask-label isolation) were left under `scratchpad/item3_M1_pilot/` **on that
machine** — retrieve them if you are continuing there.

### Pass / kill

- **Pass:** a `checkMesh`-clean mesh and a converged solve **with no manual geometry repair**, for all three cases;
  as-meshed radius returned along the centreline; both BC modes (resistance and prescribed-flow) stable.
- **Kill:** 5 working days of effort without a scriptable path → the pre-agreed fallback in spec §9 (real-lumen
  tier reduced to the two topological error types, plus the full polyball tier; **never polyball-only**).
- **Track and report how much of the 5-day budget has been consumed.** Some has already been spent on scan 837.

Fill `returns/M1_results_TEMPLATE.csv` and save as `returns/M1_results.csv`.

---

## 4. TASK 3 — sync the corrected files back into Drive (do this first, it takes minutes)

The Stage A report cites `cfd_handover/bc/resistanceOutlet.md`, `cfd_handover/stageA/make_stageA_geometry.py` and
`cfd_handover/stageA/caseTemplate/` as the versions that produced its results. **None of those corrections are in
Drive** — the copies there are the pre-fix versions, and `caseTemplate/` does not exist there at all. Your machine
has the only copies.

Right now the repository of record does not reproduce the reported results. Please copy back:

- `bc/resistanceOutlet.md` (with the `p.prevIter()` fix and the per-case table)
- `stageA/make_stageA_geometry.py` (wall normals corrected)
- `stageA/caseTemplate/` (the full case skeleton, including the `fvSchemes` fix)
- any per-case `system/` dictionaries you want preserved

Kilobytes each. This matters for reproducibility and for the code deposit the paper will need.

---

## 5. What NOT to do

- **Do not start the study batch (Stages B, C, D).** It is on hold pending an analysis-side re-cut — roughly 40 % of
  it as currently specified produces nothing usable, and three protocol decisions that change what the batch should
  compute were only settled on 2026-09-19. Running it now would waste roughly a week of machine time.
- **Do not reuse the validation pass's mesh sizes for study runs.** They were deliberately coarse.
- **Do not switch turbulence model** if a case will not converge. Flag it, record the throat Reynolds number, and use
  the time-accurate fallback in Task 1's decision tree. Steady, laminar, rigid-wall and Newtonian are the study's
  stated assumptions and are defended as such.
- **Do not put meshes, fields or STL files into Google Drive.**

## 6. What the analysis side needs back, and why it is needed

Ranked. If time runs short, work down this list rather than across it — items 1–3 each unblock something specific
that is currently stalled on the analysis machine.

**1. The 3D FFR discretisation uncertainty (from Task 1). The single most valuable number you can return.**
The statistics plan declares a discretisation floor of 0.003 FFR — **that is a 0D figure, and there is no 3D
equivalent anywhere in the project.** The cross-fidelity hypothesis (H4: 0D-vs-3D decision agreement, κ > 0.6) and
its Bland–Altman limits cannot be interpreted without it. If the figure comes back larger than **0.005**, the
comparison is measuring mesh error rather than the geometric effect the study exists to measure, and the arm has to
be re-scoped. I would rather know that from one honest number than discover it in the final analysis.

**2. Production mesh settings that actually achieve ≥ 12 cells across the throat, and the measured wall-clock per
solve at those settings.** The batch is costed from Mao 2025's published timings, which Gate M1 was always meant to
replace with measured numbers. The study batch is being re-cut right now and the cell count and wall-clock decide how
many instances are affordable. Please report cells, cells-across-throat, wall-clock, cores and RAM per job — not just
"it meshed".

**3. As-meshed radius along the centreline, per M1 case.** The 0D twin is rebuilt from the geometry that was
*actually meshed*, not from what was requested, so that 0D-vs-3D-real compares like with like. Without it the
real-lumen tier's comparison is not sound. Send it even if the solve fails — a meshed-but-unsolved surface still
gives a usable radius profile.

**4. Mesh and solve failure rate, by error type.** Not a nuisance statistic — spec §12 treats it as a **reportable
finding**, because no published base rate exists for deliberately corrupted coronary geometries. Every failure you
log is a result. Please record which error type, which stage it failed at, and what you ruled out.

**5. Throat Reynolds number for every solve.** The laminar assumption is the one a reviewer will attack; it is
defended with recorded Re, not with an assertion.

**6. Whether both outlet BC modes are stable on a MULTI-OUTLET tree — currently untested anywhere.**
Every Stage A case is single-outlet, so the resistance BC is confirmed only for one outlet. Protocol C in 3D
prescribes **every** outlet's flow simultaneously and then derives per-outlet resistances, and those outlets interact
through the shared tree. Item 1's branched idealised geometry already exists and is verified — **solving it in both
BC modes is probably a short job and would close a real gap**. If prescribed-flow mode turns out to be unstable on a
branched tree, Protocol C cannot be run in 3D at all and the whole replication arm changes shape, so this is worth
knowing early even though it is not formally part of A1–A5.

**7. Anything that surprised you, including your own mistakes.** The last pass's most useful output was the
disclosed failures — the meshing blocker, the `pymeshfix` boundary-capping hazard, the leaky-vs-discrete gate
mismatch. A tidy report with the problems smoothed out would have been worth much less.

### Where to put it

Into `returns/`, as small CSVs plus a short note:

- `stageA_A5_sten70_rerun.csv` — per level: cells, cells across throat, `checkMesh` summary, iterations, last-100
  mean FFR and band, outlet flow, throat Re, wall-clock, cores. Plus your verdict against Task 1's decision tree and
  the uncertainty figure from item 1 above.
- `M1_results.csv` — from `M1_results_TEMPLATE.csv`, plus as-meshed radius per case.
- If M1 is still blocked: what you tried, what it ruled out, and how much of the 5-day budget is spent.
- If you solve the branched tree (item 6): outlet flows and pressures in both BC modes, and whether the
  prescribed-flow solve converged with all outlets prescribed simultaneously.
- Your OpenFOAM version and line (`.com`/ESI vs `.org`/Foundation — the coded-BC API differs), mesher and version.
