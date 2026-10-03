> **⚠ SUPERSEDED as the entry point on 2026-10-03: read `WORK-ORDER-2026-10-03.md` first.** This file stays binding
> wherever 10-03 does not change it.

# CFD work order — 2026-09-26. Read this before anything else in this folder.

**For:** the CFD machine (the one that produced `STAGE-A-VALIDATION (3).pdf`, 65 pp., built 2026-09-26).
**Paper:** T6 (Paper 6). **Supersedes** `WORK-ORDER-2026-09-24.md` as the entry point. Everything in 09-24 that
this file does not change is still binding: its standing rules, its §6 resource rules, its §7 "What NOT to do" and
the E0 guard. `WORK-ORDER-2026-09-19.md` stays as background.

**Standing rules (unchanged):** meshes, fields and STL files never go into Google Drive, only kilobyte files do.
Report failures and your own mistakes as results. Decide with the rules below. Do not come back for instructions
mid-task.

---

## 0. What the analysis side took from the 2026-09-26 report

Excellent work again. Task 1 is closed cleanly, and Gate M1 now has a scriptable no-repair path with both boundary
condition modes stable on a real multi-outlet lumen. That was the arm's biggest risk. The decisions in §1 settle every
question the report left with the analysis side.

Two things are still wrong, and both are **our** fault rather than yours. They are in §2. Nothing in Drive has
changed since 09-24, which is why Task 0 is still first (§3).

---

## 1. Analysis-side decisions (binding from now on)

**D1: U₃D is accepted, and the production recipe is fixed.**
U₃D = 0.00055 (sten70, larger GCI₂₁ of the two throat-zone families) is below the pre-registered 0.005, so H4 runs
as specified. **The production recipe for every cohort lesion case is the scan-14 recipe:** a 25 µm throat zone of
±4 mm along the host vessel around the throat, 50 µm at the inlet and outlets, 100 µm and coarser elsewhere, and
four boundary layers of ratio 1.2 whose stack scales with the local cell size. Do not use a 50 µm throat as
production. On sten70 it sits 0.003 above the finest level, and 25 µm sits 0.0008 above it. Both numbers are reported
beside U₃D. If a case cannot reach ≥ 12 cells across its throat at 25 µm, drop that case's throat zone to 12.5 µm and
record it.

**D2: Throat gate. The relative check is decisive and the absolute check is reported, with one condition.**
Your reasoning holds. The package radius (vmtk maximum inscribed sphere on the dataset surface) and your
marching-cubes surface are different radius definitions, so no as-built throat can match `r_target_mm` within 1 %.
The decisive gate is therefore: **as-built throat radius ÷ undeformed radius, against the package's `radial_scale`,
within 1 %.** Report the absolute check in every return, but it does not reject a case.
**The condition:** because the as-meshed lumen is larger than the package radius (scan 14: throat area-equivalent
radius 0.2756 mm against a target of 0.2306 mm), the 3D lesion is geometrically milder than the 0D lesion. The
analysis side will rebuild every 0D twin on the as-meshed radius (`code/ingest_cfd_radius.py`) before any 3D-vs-0D
comparison. **So `as_meshed_radius_<case>.csv` is now a required return for every case, including failed solves.**
Format in §3.

**D3: A self-intersection that comes from the mask is accepted and reported, not repaired.**
This applies only if the intersection is present in the raw marching-cubes surface **and** no mesh entity flagged by
`checkMesh -allGeometry -allTopology` lies within **2 mm** of the throat or of the measurement probe. If a flagged
entity lies within 2 mm of either, that case fails M1 and is reported. It is not repaired.

**D4: Strict checkMesh failures are accepted under the same 2 mm rule.** Report the counts per check and the
distance from the nearest flagged entity to the throat and to the measurement probe.

**D5: The E0 waiver is withdrawn, because the file was missing and the case itself was fine.**
The frozen subset is now in this folder: `cfd_handover/CFD-SUBSET-FROZEN-2026-09-18.csv`. Verify it first:
```
shasum -a 256 CFD-SUBSET-FROZEN-2026-09-18.csv
# must print 8e0079a0095ae4270974a04f7675fc42bd28c13b2983ec59525bf121c43d1118
```
The analysis side checked that scan 14 left is a member of the subset (`ffr_discrete` 0.761, `healthy_main` 0.951).
Run the 09-24 §7 assertion against the shipped file, record that it passed, and replace the waiver sentence in the
report with that record.

**D6: Gate M1 verdict: PASS WITH DEVIATIONS, conditional.** The 5-day kill clock is stopped. M1 becomes a full PASS
when both of these land in Drive:
(a) the clean case's prescribed-flow round trip, within 0.5 % (Task A);
(b) `as_meshed_radius_<case>.csv` for all three cases, plus the M1 CSVs listed in 09-24 §4 (Task 0).
The deviations are D2, D3 and D4. They are declared in the paper, not hidden.

---

## 2. Corrections to the report. The cause is on our side, but the text must change.

**E1: The +33 % at territory 0 on the clean tree is not a 0D-vs-3D finding.**
`clean_nolesion/bc_A.csv` and `bc_C_flows.csv` are **byte-identical to the baseline package's**. Those are the
boundary conditions of the tree **with** the 80 %DS lesion. The 0.749 outlet pressure that bc_A × bc_C implies for
territory 0 is the lesioned tree's pressure. A lesion-free lumen given lesion-state resistances over-delivers to the
territory the lesion was throttling, by construction.
Therefore:
- **Remove** the reading "the package implies a path resistance to territory 0 about 17 times that of the 3D lumen"
  (§11.8 Findings (i)).
- Report the clean case's flows as a geometry and pipeline check only. The package gives no flow target for a
  lesion-free lumen.
- The comparable number is the **baseline**: +16.0 % (out 160) and +15.4 % (out 600). Report it as: "with the
  package resistances, the 3D lesioned tree delivers 15–16 % more to the lesioned territory than the package
  targets. Attribution between lesion geometry (as-meshed throat radius larger than the package radius, D2) and
  model fidelity is left to the analysis side." **Do not build a 0D twin to attribute it** (blinding, 09-24 §4).

**E2: The package README statement "bc_A × bc_C reconstructs the clean outlet pressures" is true only for the clean
and baseline packages.** For T1, Decision B1 sets out_558's target to the **full** territory-0 flow of the clean
tree, 0.1735 mL/s, including the share of the deleted branch. The surviving-outlet share is 0.0782 mL/s (ratio
2.218). That target is not reachable at that resistance by design, and your −43 % is the expected Protocol A result.
The package files are unchanged, because they are hash-locked in `MANIFEST.json`. **This paragraph is the erratum.**
Cite it in the report instead of the README sentence.

**E3: Replace the E0 waiver** with the D5 assertion record.

---

## 3. TASK 0 (required, FIRST, before any new compute): put the numbers and the code in Drive

This is carried over from 09-24 §1 and is still not done. `returns/` holds only the two templates and
`code_from_cfd/` does not exist. Every number in the 65-page report exists only as PDF text, and the analysis side
cannot use PDF text. **No new solve starts until Task 0 is in Drive.**

**0a. Code** into `cfd_handover/code_from_cfd/`. This is the full list in 09-24 §1 0a. Add the Task 1 tooling (U₃D
ladder, wedge generator, settled-criterion script, GCI script), the Task 3 scan-14 build/mesh/solve path and the
end-to-end runner, plus a README of about 20 lines.

**0b. Numbers** into `cfd_handover/returns/2026-09-26/`, one CSV per table, header row, SI or stated units:

| File | Content (report section) |
|---|---|
| everything in 09-24 §1 0b | Stage A, A2 sweep, A5 ladders, Item 1, Item 3 outlets and pullbacks, lesion80 WSS, timing, Item 5, Item 6, failures |
| `U3D_sten70.csv` | Table 16 + the wedge levels (incl. `W3_3000it`), with FFR, band, drift, settled flag and GCI per family (§11.7) |
| `lesion80_sensitivity.csv` | the ten quantities × W100/M50/T25a/T25b with labels (Table 13) |
| `lesion80_hyperaemic.csv`, `lesion80_E60.csv` | Tables 14 and 15, labelled `PILOT_OUT_OF_COHORT` |
| `M1_results.csv` | one row per case × BC mode, with the extra columns listed in 09-24 §4 |
| `M1_outlets_<case>_<mode>.csv` | Tables 19 and 20: per outlet R used or derived, Q, p̄ |
| `M1_probes_<case>_<mode>.csv` | area-averaged p **and** through-plane flux at every probe in `probes.csv` |
| `M1_geometry_gates.csv` | Table 17, including both throat checks and the D3/D4 distances |
| `as_meshed_radius_<case>.csv` | **required**, see below |
| `settle_iterations.csv` | Task B1 (§5) |
| `INDEX.csv` | every file above: name, report section or table, row count |
| `NOTE.md` | one page of caveats, with the M1 status line at the top |

**`as_meshed_radius_<case>.csv` format** (this is the contract with `code/ingest_cfd_radius.py`). One row per node of
the package's `centreline.vtp`, joined on its `tree_node` point array:
`tree_node, s_mm, r_asmeshed_mm, r_area_equiv_mm, r_max_inscribed_mm, section_area_mm2, covered`
where `r_asmeshed_mm` = `r_area_equiv_mm`. The other radius definition is kept so the analysis side can run both 0D
variants, as you did on 837. Use `covered = 0` for nodes the mesh does not reach, and leave the radii blank for them.
Do not interpolate.

---

## 4. TASK A (required): finish Gate M1

Finish the **clean** case's prescribed-flow solve and round trip (it was still running at the time of writing), and
return it in the M1 files. Criterion: every outlet within 0.5 %. The clean case's prescribed flows are the
lesion-state targets (E1), so read the result as a stability test, not a physiological one.

---

## 5. TASK B (required): the data that sizes the study batch

The measured real-lumen cost (≈ 2.1–2.3 h and ≈ 6 GB per 3.5–3.9 M-cell steady solve on 16 ranks) is about **13×**
the CFD-ARM-SPEC §4 estimate. At that rate the re-cut real-lumen batch (≈ 400 solves) would take ≈ 40 days on one
machine, not 5–6. Before the analysis side re-sizes the batch it needs three things from you. B1 costs no compute.

**B1 (no compute): the settle iteration of every real-lumen steady solve you have.** That means scan 14 × 5 and the
scan-837 set, including hyperaemic and E60. For each solve, apply your §11.7 SETTLED criterion (drift over 500
iterations ≤ 2 × 10⁻⁴ and last-100 band ≤ 10⁻⁴, on the measurement-probe p/P_aorta) **and** require every outlet
flow's last-100 band to be < 0.1 % and the BC error to be < 0.1 %. Return `settle_iterations.csv`: case, mode, cells,
iteration first settled, wall-clock to that iteration, FFR at that iteration and at the end of the run (difference),
and the budget used. If the difference is ≤ 10⁻⁴ everywhere, the study batch will stop on this rule instead of a
fixed 3000 iterations.

**B2 (one uncontended measurement): throughput layout.** Take scan 14 baseline, resistance mode, which you already
solved. Measure, uncontended, (i) one 16-rank job against (ii) two 8-rank jobs run side by side. For (ii), use two
copies of the same case with `--bind-to core` on disjoint cores. Report solves per hour for each layout. Stop both at
the B1 rule. This decides the batch layout.

**B3 (no compute): portability.** The operator has other PCs that can run OpenFOAM. Write
`code_from_cfd/SETUP.md`: exact versions (OpenFOAM ESI v2406, cfMesh, VMTK, Python packages), the install steps you
actually used, and a smoke test that a second machine can run in under 30 minutes to prove it reproduces one of
your results. The Item 1 tree in resistance mode is a good choice. The smoke-test pass criterion is agreement of
outlet flows within 0.1 %.

---

## 6. Still on hold, and what not to do

- **Stage B, C and D batches stay on hold.** The analysis side will ship the re-cut batch list with its size once
  Task 0 and Task B are in Drive. Do not start any part of it early.
- Everything in 09-24 §7 still applies: no new work on scan 837, no 0D predictions for cohort scans, no case selected
  from `E0_prevalence_test.csv`, and no meshes, fields or STL files in Drive.
- The audits of the Task 1 and Task 3 setups that Astra left pending should be completed when it is available. If an
  audit finding changes any returned number, re-issue that CSV with a dated suffix. Do not overwrite.

---

## 7. Report edits for the next build (documentation only)

1. §11.8 and §12: apply E1, E2 and E3. Change the M1 status to the D6 wording.
2. Abstract: add the M1 status and U₃D in one sentence each.
3. §11.7: add the D1 production recipe and the two production-level offsets (0.003 at 50 µm, 0.0008 at 25 µm) next
   to U₃D.
4. §12 "Beyond Stage A", Item 2: this still says "no trustworthy 3D discretisation uncertainty for sten70 exists
   yet". §11.7 has now answered that. Point to §11.7.

---

## 8. Priority if time runs short

Task 0 (numbers first, then code) → D5 assertion → Task A → Task B1 → Task B3 → Task B2 → report edits (§7).
Work down this list, not across it.
