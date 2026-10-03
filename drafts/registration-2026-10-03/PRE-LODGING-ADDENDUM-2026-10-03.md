# Pre-lodging addendum to STATISTICS-PLAN v1.0 — 2026-10-03

**Status:** written 2026-10-03, before the registration is lodged and before any A/B/C ablation is run on the
cohort. It is lodged with `STATISTICS-PLAN.md` and has the same standing. It records what changed between the plan's
last revision (2026-09-19) and lodging, with the date of each item and what had been seen when it was decided.
It is additive. Nothing in `STATISTICS-PLAN.md` §1–§11 is edited. Where an item supersedes a sentence there, the
sentence is named.

Items marked ⚑ need the corresponding author's confirmation before lodging.

---

## A1. U₃D has been measured (supersedes "TO BE MEASURED" in §10 and the opening of the §P4 contingency)

U₃D = **0.00055 FFR**. It is the larger Celik GCI₂₁ of two throat-zone refinement families (50/25/12.5 µm) on the
idealised 70 %DS stenosis, at the measurement plane. Both finest pairs differ by < 0.005. Production resolution is the
25 µm throat zone, which sits 0.0008 above the finest level. That offset is reported beside U₃D.

**The value is provisional.** The idealised case has two stable steady flow states (axisymmetric jet and
wall-deflected jet), differing by 0.0015 FFR on the coarsest mesh. Two of the five ladder levels are confirmed on the
axisymmetric state. The other three are being re-run. The §P4 rule applies to the **final** value as written. At the
provisional value, the first branch applies: H4 proceeds as specified, κ against 0.6, plus Bland–Altman.

U₃D is a verification quantity measured on an idealised geometry. It is not an outcome on any cohort instance.

## A2. ⚑ The radius definition in the 0D–3D comparison (adds to §P4)

**What is known, and when.** On 2026-09-26 the first real-lumen 3D case (scan 14, left LAD, 80 %DS, a cohort
instance in the 3D subset) showed that the meshed lumen is wider than the 0D radius. The 0D radius is the vmtk
maximum inscribed sphere on the dataset surface. The 3D lumen is a marching-cubes surface, and its area-equivalent
radius at the throat is 0.2756 mm against 0.2306 mm. The median shift along the tree is +0.14 mm. On 2026-09-26,
after seeing the 3D numbers and before any 0D comparison was solved, the analysis side decided that every 3D-vs-0D
comparison uses a 0D twin rebuilt on the as-meshed radius (`code/ingest_cfd_radius.py`). That twin keeps the
package's healthy reference, bed and boundary conditions, and only the epicardial radius differs.

**Registered H4 analysis (proposed):**
- **Primary H4 test (fidelity):** κ for flip agreement and Bland–Altman for ΔFFR between 3D and the 0D twin on the
  **as-meshed area-equivalent radius**, solved under the identical per-outlet boundary conditions the 3D case
  received (resistance per outlet for Protocols A and B, prescribed flow per outlet for Protocol C).
- **Reported beside it (total gap):** the same statistics between 3D and the primary 0D arm on the requested radius,
  and the twin on the as-meshed **inscribed** radius. The difference between total gap and fidelity gap is reported
  as the radius-definition gap, alongside the ladder decomposition already in §P4.
- Flips are judged within each fidelity against that fidelity's own clean baseline (§1, unchanged).

The reason for making the twin primary is that H4 asks whether the **physics** transfers. Without the twin, a
radius-definition difference between the 0D and 3D pipelines would be counted as a fidelity difference. The cost,
stated plainly, is that the primary 0D arm (on the inscribed-sphere radius) is not itself what the 3D arm tests.
That limitation is stated wherever H4 is reported.

## A3. Instances with results seen before lodging (adds to §9)

These instances were run during code verification or the 3D gate. All remain in the cohort.

| Instance(s) | What was computed | When | Why |
|---|---|---|---|
| Scans 102, 280, 306, 335, 368, 621 (left LAD) | 0D A/B/C ablation rows, both beds, and the noise-floor (negatives) smoke set | 2026-09-19 | Code verification. The minimiser, B1, B2 and B3 defects were found on this set |
| Scan 341 (right RCA) | 0D A/B/C ablation rows | 2026-09-19 | Verification of the Protocol C minimiser fix |
| Scan 14 (left LAD; also in the 3D subset) | 3D: clean, baseline and T1 lumens under per-outlet resistance and prescribed flow. 0D twins on three radius definitions under the same boundary conditions | 3D 2026-09-26; 0D twins 2026-10-03 | Gate M1 (mesh-to-solution path) and the radius-definition check in A2 |

Scan 837 was a 3D pilot and is outside the cohort.

**Pre-specified handling:** all eight instances stay in every analysis, since excluding them would change the frozen,
hashed cohort. A sensitivity analysis **excluding all eight** is reported for P1, P2 and P4. If a conclusion differs
between the two, both are reported and the difference is stated.

## A4. 3D gate status and the P5 baseline pilot (adds to §P4 and §9)

- **Gate M1 (scan 14)** passed its mesh-to-solution criteria with declared deviations: the throat gate is relative,
  not absolute (D2); a self-intersection comes from the mask (D3); and strict `checkMesh` flags are localised (D4).
  On the two lesion cases, flagged cells lie 1.43 mm from the throat centre, inside the 2 mm rule. ⚑ This is
  resolved by a pre-specified sensitivity test (D7): re-mesh the throat at 12.5 µm and accept only if the
  measurement-probe FFR changes by less than U₃D. The deviations are reported in the paper.
- **P5 pilot.** Five further 3D-subset instances (scans 138, 69, 473, 272 and 139, chosen by the fixed rule in
  `P5-PILOT-DECISION-RULE-2026-10-03.md`) are solved at baseline only, after lodging, to measure how far the
  radius definition moves 3D FFR across vessels. **Any change to the 3D subset or to the 3D lesion construction that
  follows from the pilot is lodged as a dated amendment before the 3D batch starts.** The pilot baselines are
  production solves, and they enter P4 like any other instance.

## A5. Staged reporting (adds to §12)

All six hypotheses H1–H6 are reported. The 3D batch (H4) and the detector (H5) take longer than the 0D ablation
(H1–H3, H6). If a manuscript is submitted before H4 or H5 data exist:
- it reports H1–H3 and H6 in full against this plan;
- it states H4 and H5 as registered and pending, in those words, with this registration cited;
- the Holm–Bonferroni correction (§7) stays over the full family of six, so the earlier report is not made less
  conservative by testing fewer hypotheses;
- H4 and H5 are reported when complete, in the revision or in a follow-up that cites this registration.

No hypothesis is dropped by staging.

## A6. Corrections to `PREREGISTRATION-CHECKLIST.md` (record only)

- §2 item 5 ("U₃D is not yet measured") is superseded by A1.
- The cohort manifest `COHORT-FROZEN-2026-09-18.sha256` lists 15 entries, not the 13 the checklist states.
  Verified 2026-10-03: 15/15 OK.
- `code/m1_zerod_vs_3d.py` (written 2026-10-03) is the 0D–3D comparison tool used in A2–A3. It is deposited with the
  code and is not in the 2026-09-18 manifest.
