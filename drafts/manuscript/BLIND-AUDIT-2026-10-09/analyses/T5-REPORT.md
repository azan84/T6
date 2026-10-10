# T5 report: caliber error at the stenosis throat (2026-10-09)

## 1. Design as run

Fixed before the full run; nothing was changed after the results were seen.

**Error definition.** T5 re-inserts the clean lesion with a changed severity. Centre c, length L, the insertion window and the modelled node set stay the same. The corrupted tree is rebuilt from the unchanged segment list with `trunc_ref` pinned to the clean tree, which is the path T3 and T4 take (`ablation.CALIBRE_ONLY`). Only the inserted diameter stenosis (DS) changes. At the throat, where the insertion weight is 1, this sets the throat radius to r_fit(c)(1 − DS).

**Variants.** Each sign is reported as its own error type, and each magnitude is also pooled over both signs.

| Variant | Change | Effect on the stenosis |
|---|---|---|
| `T5_ds_plus10` | DS + 10 percentage points (pp), e.g. 70% → 80% | over-read throat, more severe |
| `T5_ds_minus10` | DS − 10 pp, e.g. 70% → 60% | under-read throat, less severe |
| `T5_vox_narrow` | throat diameter − ½ voxel (radius − ¼ voxel), i.e. DS + (s/4)/r_fit(c) | more severe |
| `T5_vox_wide` | throat diameter + ½ voxel (radius + ¼ voxel), i.e. DS − (s/4)/r_fit(c) | less severe |

- **Primary magnitude:** ±10 pp DS.
- **Secondary magnitude:** ±½ voxel in throat diameter.
- **Voxel size s:** for each scan, the mean of the first two header zooms (in-plane spacing) of the ImageCAS-X label volume `segmentations/<scan>.coronary.nii.gz`. Over the 93 cohort scans:
  - in-plane spacing: median 0.352 mm (range 0.295–0.449, mean 0.357);
  - throat radius change s/4: median 0.088 mm, i.e. a diameter change of 0.176 mm;
  - resulting |ΔDS| per instance: median 7.3 pp (range 4.5–9.8).
- **Clipping:** DS was clipped to 0.05–0.95. No insertion needed clipping (0 of 2,384). Cohort DS spans 40–80%, so ±10 pp gives 30–90%.
- **Realised throat:** the insertion's `min(r, …)` guard never bound at the throat. The realised throat DS equalled the applied DS in all 2,384 insertions (tolerance 1e-9).

**Implementation.** Frozen files are imported and none was edited.

- `code/t5_throat_error_types.py` defines the four variant functions and a patched `insert`. A T5 function registers a pending DS transform, and the patched `severity_sweep.insert` applies it to the next call only. `install()` swaps the following in memory:
  - `error_types.ERROR_TYPES` and `ablation.ERROR_TYPES` (to the T5 set only);
  - `severity_sweep.insert` and `ablation.insert`;
  - `ablation.CALIBRE_ONLY`, extended with the T5 names so `trunc_ref` is pinned.
- `code/t5_throat_run.py` runs the frozen `ablation.run_instance` (Protocols A–C) and `ablation_per_territory.run_instance` (Protocol D) unchanged on the frozen cohort (`deposit-2026-10-08/protocol/COHORT-FROZEN-2026-09-18.csv`, 150 instances), both beds. The pending transform is reset before every call.
- `code/t5_throat_summarise.py` uses `summarise_revision.load` and `ci` unchanged. This keeps the same conventions:
  - discrete arm restricted to the 97 eligible instances;
  - Wilson 95% CIs;
  - passes-and-wrong (P&W) = residual < 0.10 and |ΔFFR| > 0.05, over models with a defined residual.
  - Grey-zone flips follow `grey_zone.py`: corrupted FFR outside 0.75–0.85, on the other side of 0.80 from the clean FFR.
  - The paired comparison is the `summarise_revision.py` sign test on per-instance class proportions: the T1+T2 flip proportion (frozen run) against the T5 flip proportion (one variant, or the mean of both signs when pooled), on instances that have both.

**Conventions inherited unchanged from the frozen code:**
- Protocol C fits on a search bound are logged as failed fits and excluded.
- Protocol D fits on the ±3-decade bound are kept, as in the frozen D run.
- Because T5 changes neither topology nor r_ref, Protocol B re-derives exactly the clean bed and C_b. So A ≡ B for T5, as for T3 in Table I.

## 2. Validation

All checks were run before the full run (`results/t5_throat-2026-10-09/validation.txt`). Six instances (4 left, 2 right) in both beds were used:
102_left_LAD_mid_20mm_80, 280_left_LAD_prox_20mm_80, 306_left_LAD_prox_20mm_80, 335_left_LAD_prox_10mm_70, 42_right_RCA_prox_20mm_70, 69_right_RCA_prox_10mm_70.

1. **Zero-magnitude identity.** With a T5 type of ΔDS = 0 routed through the full wrapper, max |ΔFFR| = 0 exactly, with 0 flips, under A, B, C and D (12 models each).
2. **Clean FFR reproduced exactly.**
   - Validation set: the clean-row FFR was bit-identical to `results/ablation-2026-10-07.csv`, with max |diff| = 0.0. The frozen CSV was read with `float_precision="round_trip"`; the default parser differs in the last ulp, 5.6e-17.
   - Full run: all 298 clean rows (150 leaky, 148 discrete) were bit-identical to the frozen clean FFR. All 298 Protocol D `ffr_clean` values were identical to `ablation-perterritory-2026-10-08.csv`.
3. **Monotonicity.** ΔDS ∈ {−20, −15, −10, −5, 0, +5, +10, +15} pp was run under Protocols A and B on the same 6 instances in both beds. FFR at the measurement point decreased strictly with DS in all 168 steps, with 0 violations (`validation_monotonic.csv`).
4. **Full-run health.**
   - Solves: 0 non-converged; maximum mass error 4.6e-11.
   - Protocol C: 11 failed fits on the search bound (8 `ds_plus10` and 1 `vox_narrow` discrete; 1 of each in leaky), all for the more-severe variants.
   - Protocol D: 97 of 1,172 fits sat on the ±3-decade bound (frozen D: 2). All were more-severe variants, where a tight throat cannot pass the clean territory flow. Their residual is mostly ≥ 0.10, so they do not count as passes. Excluding them would raise the D passes-and-wrong rates (e.g. DS +10 discrete: 65% → 92%), so keeping them is the conservative choice.

## 3. Results

Table I format. "(D)" = discrete bed (97 eligible instances) and "(L)" = leaky bed (150). Values are % with Wilson 95% CIs. P&W denominators equal n except where shown in parentheses (the count with a defined residual). Beyond GZ = flips that end outside 0.75–0.85. The last two blocks are the frozen run's topological (T1+T2) and caliber (T3+T4) classes on the same instances, for reference; they reproduce `tab_greyzone.tex`.

| Error | Prot. | n (D) | Flip % (D) | P&W % (D) | Beyond GZ % (D) | med abs dFFR (D) | n (L) | Flip % (L) | P&W % (L) | Beyond GZ % (L) | med abs dFFR (L) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T5_ds_plus10 | A | 97 | 34 (25--44) | 11 (6--19) | 30 (22--40) | 0.230 | 150 | 34 (27--42) | 31 (24--38) | 26 (20--34) | 0.235 |
|  | B | 97 | 34 (25--44) | 11 (6--19) | 30 (22--40) | 0.230 | 150 | 34 (27--42) | 31 (24--38) | 26 (20--34) | 0.235 |
|  | C | 90 | 39 (29--49) | 34 (25--45) | 34 (25--45) | 0.287 | 149 | 36 (29--44) | 49 (41--57) | 32 (25--39) | 0.294 |
|  | D | 97 | 38 (29--48) | 65 (55--74) | 33 (24--43) | 0.400 | 150 | 37 (30--45) | 91 (86--95) | 31 (24--38) | 0.324 |
| T5_ds_minus10 | A | 97 | 45 (36--55) | 29 (21--39) | 25 (17--34) | 0.116 | 150 | 50 (42--58) | 49 (41--57) | 43 (36--51) | 0.106 |
|  | B | 97 | 45 (36--55) | 29 (21--39) | 25 (17--34) | 0.116 | 150 | 50 (42--58) | 49 (41--57) | 43 (36--51) | 0.106 |
|  | C | 97 | 49 (40--59) | 66 (56--75) | 39 (30--49) | 0.130 | 150 | 50 (42--58) | 74 (66--80) | 50 (42--58) | 0.116 |
|  | D | 97 | 52 (42--61) | 85 (76--90) | 47 (38--57) | 0.135 | 150 | 50 (42--58) | 80 (73--86) | 50 (42--58) | 0.117 |
| T5_ds_pooled | A | 194 | 40 (33--47) | 20 (15--26) | 27 (22--34) | 0.164 | 300 | 42 (37--48) | 40 (34--45) | 35 (30--40) | 0.144 |
|  | B | 194 | 40 (33--47) | 20 (15--26) | 27 (22--34) | 0.164 | 300 | 42 (37--48) | 40 (34--45) | 35 (30--40) | 0.144 |
|  | C | 187 | 44 (37--52) | 51 (44--58) | 37 (30--44) | 0.192 | 299 | 43 (38--49) | 62 (56--67) | 41 (35--46) | 0.165 |
|  | D | 194 | 45 (38--52) | 75 (68--80) | 40 (34--47) | 0.222 | 300 | 44 (38--49) | 86 (81--89) | 40 (35--46) | 0.166 |
| T5_vox_narrow | A | 97 | 28 (20--37) | 26 (18--35) | 16 (10--25) | 0.141 | 150 | 25 (19--33) | 43 (36--51) | 15 (10--22) | 0.155 |
|  | B | 97 | 28 (20--37) | 26 (18--35) | 16 (10--25) | 0.141 | 150 | 25 (19--33) | 43 (36--51) | 15 (10--22) | 0.155 |
|  | C | 96 | 30 (22--40) | 49 (39--59) | 23 (16--32) | 0.201 | 149 | 26 (19--33) | 68 (61--75) | 21 (15--28) | 0.203 |
|  | D | 97 | 30 (22--40) | 84 (75--90) | 25 (17--34) | 0.267 | 150 | 27 (21--35) | 91 (85--94) | 19 (14--26) | 0.217 |
| T5_vox_wide | A | 97 | 32 (24--42) | 32 (24--42) | 12 (7--20) | 0.092 | 150 | 47 (39--55) | 41 (34--49) | 26 (20--34) | 0.086 |
|  | B | 97 | 32 (24--42) | 32 (24--42) | 12 (7--20) | 0.092 | 150 | 47 (39--55) | 41 (34--49) | 26 (20--34) | 0.086 |
|  | C | 97 | 45 (36--55) | 65 (55--74) | 21 (14--30) | 0.102 | 150 | 49 (41--57) | 69 (61--76) | 38 (31--46) | 0.093 |
|  | D | 97 | 49 (40--59) | 77 (68--85) | 28 (20--37) | 0.108 | 150 | 49 (41--57) | 71 (64--78) | 39 (31--47) | 0.094 |
| T5_vox_pooled | A | 194 | 30 (24--37) | 29 (23--36) | 14 (10--20) | 0.112 | 300 | 36 (31--42) | 42 (37--48) | 21 (16--26) | 0.105 |
|  | B | 194 | 30 (24--37) | 29 (23--36) | 14 (10--20) | 0.112 | 300 | 36 (31--42) | 42 (37--48) | 21 (16--26) | 0.105 |
|  | C | 193 | 38 (31--45) | 57 (50--64) | 22 (17--28) | 0.141 | 299 | 37 (32--43) | 69 (63--74) | 29 (25--35) | 0.128 |
|  | D | 194 | 40 (33--47) | 80 (74--85) | 26 (21--33) | 0.162 | 300 | 38 (33--44) | 81 (76--85) | 29 (24--34) | 0.122 |
| T1T2_topo | A | 137 | 33 (26--41) | 12 (8--19) | 20 (15--28) | 0.104 | 265 (218) | 32 (26--38) | 20 (15--26) | 23 (18--28) | 0.067 |
|  | B | 173 (137) | 14 (10--20) | 1 (0--5) | 5 (2--9) | 0.036 | 267 (218) | 5 (3--8) | 5 (3--8) | 0 (0--1) | 0.005 |
|  | C | 104 | 19 (13--28) | 19 (13--28) | 9 (5--16) | 0.066 | 171 | 8 (5--13) | 8 (5--13) | 1 (0--3) | 0.011 |
|  | D | 104 | 8 (4--14) | 20 (14--29) | 2 (1--7) | 0.005 | 171 | 6 (3--10) | 5 (3--10) | 0 (0--2) | 0.005 |
| T3T4_cal | A | 194 | 10 (7--15) | 3 (1--7) | 0 (0--2) | 0.012 | 300 | 6 (4--9) | 3 (2--6) | 0 (0--1) | 0.014 |
|  | B | 194 | 8 (5--12) | 0 (0--2) | 0 (0--2) | 0.009 | 300 | 1 (1--3) | 0 (0--1) | 0 (0--1) | 0.006 |
|  | C | 194 | 8 (5--12) | 5 (2--9) | 1 (0--3) | 0.012 | 300 | 4 (2--7) | 12 (9--17) | 1 (0--2) | 0.010 |
|  | D | 194 | 11 (7--16) | 18 (13--24) | 1 (0--3) | 0.019 | 300 | 4 (2--6) | 4 (2--7) | 0 (0--1) | 0.011 |

**Direction of flips.** Under every protocol, every flip from DS+ variants went to positive (FFR lowered across 0.80), and every flip from DS− variants went to negative. Topological flips under A were all to negative (44/44 discrete, 84/84 leaky).

Flip rates by side of 0.80 under A:

| Variant | Instances eligible to flip | Discrete | Leaky |
|---|---|---|---|
| DS −10 | clean-positive | 44/52 (85%) | 75/75 (100%) |
| DS +10 | clean-negative | 33/45 (73%) | 51/75 (68%) |
| ½ voxel wide | clean-positive | 31/52 (60%) | 70/75 (93%) |
| ½ voxel narrow | clean-negative | 27/45 (60%) | 38/75 (51%) |

**Effect of tuning.** Tuning moved FFR further from the clean value for both signs:
- DS +10: mean ΔFFR −0.22 under A, −0.28 under C and −0.39 under D (discrete).
- DS −10: mean ΔFFR +0.12 under A, +0.14 under C and +0.15 under D.

The mechanism is the one the paper gives for the taper. Forcing the clean territory flow through a wrong throat enlarges the error in the pressure drop.

**Paired sign test, topological (T1+T2, frozen run) against T5, on per-instance flip proportions.** The first row of each block reproduces the paper's T1T2-vs-T3T4 test (A: p = 0.0014 discrete, 1.4e-8 leaky; B: p = 0.013 and 0.18), which confirms the procedure.

| Bed | Protocol | Comparison (a vs b) | instances | rate a | rate b | a>b | b>a | p |
|---|---|---|---|---|---|---|---|---|
| discrete | A | T1T2 vs T3T4 (frozen, check) | 97 | 34.5% | 10.3% | 36 | 13 | 0.0014 |
| discrete | A | T1T2 vs T5_ds_plus10 | 97 | 34.5% | 34.0% | 36 | 33 | 0.81 |
| discrete | A | T1T2 vs T5_ds_minus10 | 97 | 34.5% | 45.4% | 3 | 15 | 0.0075 |
| discrete | A | T1T2 vs T5_vox_narrow | 97 | 34.5% | 27.8% | 36 | 27 | 0.31 |
| discrete | A | T1T2 vs T5_vox_wide | 97 | 34.5% | 32.0% | 11 | 8 | 0.65 |
| discrete | A | T1T2 vs T5_ds_pooled | 97 | 34.5% | 39.7% | 32 | 44 | 0.21 |
| discrete | A | T1T2 vs T5_vox_pooled | 97 | 34.5% | 29.9% | 34 | 33 | 1 |
| discrete | A | T5_ds_plus10 vs T3T4 | 97 | 34.0% | 10.3% | 26 | 0 | 3e-08 |
| discrete | A | T5_ds_minus10 vs T3T4 | 97 | 45.4% | 10.3% | 44 | 13 | 4.7e-05 |
| discrete | A | T5_vox_narrow vs T3T4 | 97 | 27.8% | 10.3% | 20 | 0 | 1.9e-06 |
| discrete | A | T5_vox_wide vs T3T4 | 97 | 32.0% | 10.3% | 31 | 13 | 0.0096 |
| discrete | B | T1T2 vs T3T4 (frozen, check) | 97 | 14.9% | 7.7% | 14 | 3 | 0.013 |
| discrete | B | T1T2 vs T5_ds_plus10 | 97 | 14.9% | 34.0% | 9 | 30 | 0.0011 |
| discrete | B | T1T2 vs T5_ds_minus10 | 97 | 14.9% | 45.4% | 15 | 42 | 0.00046 |
| discrete | B | T1T2 vs T5_vox_narrow | 97 | 14.9% | 27.8% | 10 | 24 | 0.024 |
| discrete | B | T1T2 vs T5_vox_wide | 97 | 14.9% | 32.0% | 16 | 30 | 0.054 |
| discrete | B | T1T2 vs T5_ds_pooled | 97 | 14.9% | 39.7% | 5 | 53 | 3.5e-11 |
| discrete | B | T1T2 vs T5_vox_pooled | 97 | 14.9% | 29.9% | 6 | 36 | 2.8e-06 |
| discrete | B | T5_ds_plus10 vs T3T4 | 97 | 34.0% | 7.7% | 29 | 1 | 5.8e-08 |
| discrete | B | T5_ds_minus10 vs T3T4 | 97 | 45.4% | 7.7% | 44 | 10 | 3.4e-06 |
| discrete | B | T5_vox_narrow vs T3T4 | 97 | 27.8% | 7.7% | 23 | 1 | 3e-06 |
| discrete | B | T5_vox_wide vs T3T4 | 97 | 32.0% | 7.7% | 31 | 10 | 0.0015 |
| discrete | C | T1T2 vs T3T4 (frozen, check) | 66 | 20.5% | 7.6% | 15 | 2 | 0.0023 |
| discrete | C | T1T2 vs T5_ds_plus10 | 64 | 19.5% | 35.9% | 9 | 20 | 0.061 |
| discrete | C | T1T2 vs T5_ds_minus10 | 66 | 20.5% | 50.0% | 10 | 29 | 0.0034 |
| discrete | C | T1T2 vs T5_vox_narrow | 66 | 20.5% | 28.8% | 10 | 16 | 0.33 |
| discrete | C | T1T2 vs T5_vox_wide | 66 | 20.5% | 43.9% | 10 | 25 | 0.017 |
| discrete | C | T1T2 vs T5_ds_pooled | 66 | 20.5% | 43.9% | 6 | 36 | 2.8e-06 |
| discrete | C | T1T2 vs T5_vox_pooled | 66 | 20.5% | 36.4% | 7 | 28 | 0.00051 |
| discrete | C | T5_ds_plus10 vs T3T4 | 90 | 38.9% | 8.3% | 32 | 1 | 7.9e-09 |
| discrete | C | T5_ds_minus10 vs T3T4 | 97 | 49.5% | 7.7% | 48 | 11 | 1.2e-06 |
| discrete | C | T5_vox_narrow vs T3T4 | 96 | 30.2% | 7.8% | 26 | 1 | 4.2e-07 |
| discrete | C | T5_vox_wide vs T3T4 | 97 | 45.4% | 7.7% | 44 | 11 | 8.7e-06 |
| discrete | D | T1T2 vs T3T4 (frozen, check) | 66 | 9.1% | 12.1% | 5 | 8 | 0.58 |
| discrete | D | T1T2 vs T5_ds_plus10 | 66 | 9.1% | 37.9% | 2 | 23 | 1.9e-05 |
| discrete | D | T1T2 vs T5_ds_minus10 | 66 | 9.1% | 53.0% | 6 | 33 | 1.4e-05 |
| discrete | D | T1T2 vs T5_vox_narrow | 66 | 9.1% | 28.8% | 2 | 17 | 0.00073 |
| discrete | D | T1T2 vs T5_vox_wide | 66 | 9.1% | 50.0% | 6 | 31 | 4.1e-05 |
| discrete | D | T1T2 vs T5_ds_pooled | 66 | 9.1% | 45.5% | 4 | 52 | 1.1e-11 |
| discrete | D | T1T2 vs T5_vox_pooled | 66 | 9.1% | 39.4% | 4 | 44 | 1.5e-09 |
| discrete | D | T5_ds_plus10 vs T3T4 | 97 | 38.1% | 10.8% | 30 | 0 | 1.9e-09 |
| discrete | D | T5_ds_minus10 vs T3T4 | 97 | 51.5% | 10.8% | 50 | 14 | 7.1e-06 |
| discrete | D | T5_vox_narrow vs T3T4 | 97 | 29.9% | 10.8% | 22 | 0 | 4.8e-07 |
| discrete | D | T5_vox_wide vs T3T4 | 97 | 49.5% | 10.8% | 48 | 14 | 1.7e-05 |
| leaky | A | T1T2 vs T3T4 (frozen, check) | 150 | 33.3% | 5.7% | 63 | 14 | 1.4e-08 |
| leaky | A | T1T2 vs T5_ds_plus10 | 150 | 33.3% | 34.0% | 63 | 51 | 0.3 |
| leaky | A | T1T2 vs T5_ds_minus10 | 150 | 33.3% | 50.0% | 0 | 38 | 7.3e-12 |
| leaky | A | T1T2 vs T5_vox_narrow | 150 | 33.3% | 25.3% | 63 | 38 | 0.017 |
| leaky | A | T1T2 vs T5_vox_wide | 150 | 33.3% | 46.7% | 3 | 33 | 2.3e-07 |
| leaky | A | T1T2 vs T5_ds_pooled | 150 | 33.3% | 42.0% | 37 | 63 | 0.012 |
| leaky | A | T1T2 vs T5_vox_pooled | 150 | 33.3% | 36.0% | 40 | 48 | 0.46 |
| leaky | A | T5_ds_plus10 vs T3T4 | 150 | 34.0% | 5.7% | 48 | 0 | 7.1e-15 |
| leaky | A | T5_ds_minus10 vs T3T4 | 150 | 50.0% | 5.7% | 75 | 14 | 3e-11 |
| leaky | A | T5_vox_narrow vs T3T4 | 150 | 25.3% | 5.7% | 35 | 0 | 5.8e-11 |
| leaky | A | T5_vox_wide vs T3T4 | 150 | 46.7% | 5.7% | 70 | 14 | 4.1e-10 |
| leaky | B | T1T2 vs T3T4 (frozen, check) | 150 | 5.0% | 1.3% | 10 | 4 | 0.18 |
| leaky | B | T1T2 vs T5_ds_plus10 | 150 | 5.0% | 34.0% | 10 | 51 | 9.6e-08 |
| leaky | B | T1T2 vs T5_ds_minus10 | 150 | 5.0% | 50.0% | 0 | 70 | 1.7e-21 |
| leaky | B | T1T2 vs T5_vox_narrow | 150 | 5.0% | 25.3% | 10 | 38 | 6.2e-05 |
| leaky | B | T1T2 vs T5_vox_wide | 150 | 5.0% | 46.7% | 0 | 65 | 5.4e-20 |
| leaky | B | T1T2 vs T5_ds_pooled | 150 | 5.0% | 42.0% | 5 | 116 | 1.6e-28 |
| leaky | B | T1T2 vs T5_vox_pooled | 150 | 5.0% | 36.0% | 5 | 98 | 1.8e-23 |
| leaky | B | T5_ds_plus10 vs T3T4 | 150 | 34.0% | 1.3% | 51 | 0 | 8.9e-16 |
| leaky | B | T5_ds_minus10 vs T3T4 | 150 | 50.0% | 1.3% | 75 | 4 | 5.2e-18 |
| leaky | B | T5_vox_narrow vs T3T4 | 150 | 25.3% | 1.3% | 38 | 0 | 7.3e-12 |
| leaky | B | T5_vox_wide vs T3T4 | 150 | 46.7% | 1.3% | 70 | 4 | 1.3e-16 |
| leaky | C | T1T2 vs T3T4 (frozen, check) | 106 | 8.5% | 1.9% | 11 | 3 | 0.057 |
| leaky | C | T1T2 vs T5_ds_plus10 | 105 | 8.6% | 37.1% | 11 | 39 | 9e-05 |
| leaky | C | T1T2 vs T5_ds_minus10 | 106 | 8.5% | 49.1% | 0 | 45 | 5.7e-14 |
| leaky | C | T1T2 vs T5_vox_narrow | 105 | 8.6% | 26.7% | 11 | 28 | 0.0095 |
| leaky | C | T1T2 vs T5_vox_wide | 106 | 8.5% | 49.1% | 0 | 45 | 5.7e-14 |
| leaky | C | T1T2 vs T5_ds_pooled | 106 | 8.5% | 43.4% | 7 | 80 | 8.3e-17 |
| leaky | C | T1T2 vs T5_vox_pooled | 106 | 8.5% | 38.2% | 7 | 69 | 6.4e-14 |
| leaky | C | T5_ds_plus10 vs T3T4 | 149 | 36.2% | 4.0% | 53 | 1 | 6.1e-15 |
| leaky | C | T5_ds_minus10 vs T3T4 | 150 | 50.0% | 4.0% | 75 | 10 | 1.9e-13 |
| leaky | C | T5_vox_narrow vs T3T4 | 149 | 25.5% | 4.0% | 37 | 1 | 2.8e-10 |
| leaky | C | T5_vox_wide vs T3T4 | 150 | 49.3% | 4.0% | 74 | 10 | 3.3e-13 |
| leaky | D | T1T2 vs T3T4 (frozen, check) | 106 | 6.6% | 3.8% | 8 | 6 | 0.79 |
| leaky | D | T1T2 vs T5_ds_plus10 | 106 | 6.6% | 39.6% | 9 | 42 | 3.4e-06 |
| leaky | D | T1T2 vs T5_ds_minus10 | 106 | 6.6% | 49.1% | 0 | 47 | 1.4e-14 |
| leaky | D | T1T2 vs T5_vox_narrow | 106 | 6.6% | 29.2% | 9 | 31 | 0.00068 |
| leaky | D | T1T2 vs T5_vox_wide | 106 | 6.6% | 49.1% | 0 | 47 | 1.4e-14 |
| leaky | D | T1T2 vs T5_ds_pooled | 106 | 6.6% | 44.3% | 5 | 85 | 7.5e-20 |
| leaky | D | T1T2 vs T5_vox_pooled | 106 | 6.6% | 39.2% | 5 | 74 | 8e-17 |
| leaky | D | T5_ds_plus10 vs T3T4 | 150 | 37.3% | 3.7% | 54 | 1 | 3.1e-15 |
| leaky | D | T5_ds_minus10 vs T3T4 | 150 | 50.0% | 3.7% | 75 | 8 | 9.1e-15 |
| leaky | D | T5_vox_narrow vs T3T4 | 150 | 27.3% | 3.7% | 39 | 1 | 7.5e-11 |
| leaky | D | T5_vox_wide vs T3T4 | 150 | 48.7% | 3.7% | 73 | 8 | 3e-14 |

## 4. What it means for the paper's claims

**Answer.** Yes. A ±10 %DS throat error changes decisions at rates comparable to the topological errors, and in the like-for-like direction it changes them more often.

Under fixed boundary conditions (A), flip rates were:

| Error | Discrete | Leaky |
|---|---|---|
| Topological (T1+T2) | 33% (26–41) | 32% (26–38) |
| T5 ±10 pp pooled | 40% (33–47) | 42% (37–48) |
| T5 ±½ voxel pooled | 30% (24–37) | 36% (31–42) |
| T3+T4 | 10% | 6% |

Paired sign tests of T1+T2 against T5 under A:
- ±10 pp pooled: p = 0.21 (discrete); p = 0.012 (leaky), where T5 is higher.
- ±½ voxel pooled: p = 1.0 and 0.46.
- DS +10 alone: p = 0.81 and 0.30.
- DS −10: higher than topological in both beds (p = 0.0075 and 7e-12). This is the variant that moves FFR in the same direction as a missed branch or break.

The ratio of topological to throat flip rates under A is 0.76–1.1, not 3–6.

**The throat flips are large, not grey-zone artefacts.**
- Median |ΔFFR| under A: 0.09–0.24 for T5, against 0.07–0.10 for topological errors and 0.01 for T3/T4.
- Flips ending beyond 0.75–0.85, ±10 pp pooled: 27% discrete and 35% leaky, against 20% and 23% for topological errors and 0% for T3/T4.

**Neither re-derivation nor tuning lowers throat flips.**
- A ≡ B for T5 by construction.
- C and D give pooled flip rates equal to or higher than A: 43–45% for ±10 pp and 37–40% for ±½ voxel.
- After tuning, 51–86% of throat-error models pass the perfusion check while materially wrong (pooled, C and D, both beds). This compares with 5–20% for topological errors and 3–4% on correct anatomy.
- Under B, C and D, T5 flips more often than T1+T2 in every comparison. All pooled comparisons are significant (p ≤ 5e-4). Three single-sign discrete cells are not (p = 0.054–0.33).

Throat errors therefore strengthen the paper's central thesis, that a perfusion match after tuning does not certify the model. They overturn its ranking claim, which holds only for caliber errors away from the throat.

**Magnitude caveats.**
- The ±½ voxel magnitude comes from the image alone: a median 0.088 mm in radius and 0.18 mm in diameter. That is about twice the 0.045 mm throat offset that moved the 3D baseline FFR by 0.11.
- The ±10 pp magnitude is a design choice. It is not derived from ImageCAS-X inter-observer statistics, because the dataset reports no stenosis-grade agreement, so it should be cited to published CT-grading variability if reported.
- Like Table I, the rates are conditional on the threshold-stratified cohort (clean FFR 0.65–0.95). This inflates every error type's flip rate near 0.80; it does not bias the paired comparison.

**Sentence by sentence.**

1. **Abstract:** "branching (topological) errors changed the decision in 32--33\% of models, against 6--10\% for vessel-size (caliber) errors of inter-observer magnitude, for the error magnitudes studied".
   - The numbers stay true for T3/T4. The implied contrast between topology and caliber does not survive, because a throat-caliber error of half a voxel flips 30–36%.
   - Change: restrict to "caliber errors away from the stenosis throat (lesion length, distal taper)" and add the throat result.
   - The next abstract sentence, "Re-derived or tuned boundary conditions reduced these to 5--19\%", must also be restricted to topological errors, since throat flips were not reduced.
   - The passes-and-wrong sentence ("4--18\% of caliber-error models") becomes "4--18\% of caliber-error models away from the throat and 51--86\% of throat-error models".
2. **IV-A:** "a topological error changed the decision at 0.80 three to six times as often as a caliber error of inter-observer magnitude ... This ranking holds for the magnitudes studied; no error type perturbed the stenosis throat alone."
   - The 3–6× ratio holds only against T3/T4.
   - The clause "no error type perturbed the stenosis throat alone" becomes false once T5 is reported, and the ranking must be stated as branching and throat against caliber elsewhere.
3. **Conclusion:** "missed branches and vessel breaks changed the decision three to six times as often as caliber errors of inter-observer size, for the magnitudes studied". It stands only with "away from the stenosis throat" added, together with the throat result. The safeguard list should add a check of the throat diameter.
4. **Related sentences that also change:**
   - III-A: "The caliber errors rarely changed the decision" → "The caliber errors away from the throat rarely changed the decision".
   - Limitations: "A caliber error of this size at the throat may therefore matter as much as a topological one" → stated as a result. "caliber errors only narrowed or lengthened the lumen" → T5 also widens the throat.
   - IV-D practical use, "Second ... check the lumen caliber": add the throat.
   - The title can stand, since topology is still a decision risk, but the abstract's first result should no longer present topology as the dominant risk.

**Honest framing if reported.** With fixed boundary conditions, the decision risk lay in the branching and at the stenosis throat. A missed branch or vessel break, or a half-voxel error in throat diameter, each changed about one third of decisions. Caliber errors of inter-observer size away from the throat changed decisions at rates near repeat measurement. Boundary-condition re-derivation or tuning reduced topological flips but not throat flips. Tuning turned most throat-error models into passing models with a wrong FFR.

## 5. Draft text

**(a) Main text (2 sentences, Results III-A):**

> A throat caliber error, the same lesion re-inserted with its diameter stenosis changed by $\pm 10$ percentage points or its throat diameter by $\pm\tfrac{1}{2}$ voxel (median 0.18~mm), changed the decision in 40--42\% and 30--36\% of models with fixed boundary conditions, as often as the topological errors (paired sign test, $p \geq 0.21$, except $\pm 10$ points in the leaky bed, where throat errors flipped more often, $p = 0.012$). Re-derived or tuned boundary conditions did not reduce these rates, and after tuning 51--86\% of throat-error models passed the perfusion check while materially wrong (Supplementary Material).

**(b) Supplement paragraph:**

> \subsection{Caliber Error at the Stenosis Throat}\label{sec:throat}
> The throat error (T5) re-inserts each lesion at the same center, length and node set with a changed severity: the diameter stenosis is raised or lowered by 10 percentage points, or the throat radius is changed by a quarter of the in-plane voxel size of the scan (a throat diameter error of half a voxel). In-plane spacing had a median of 0.352~mm (0.295--0.449~mm), so the half-voxel error changed the throat radius by a median of 0.088~mm and the diameter stenosis by a median of 7.3 percentage points (4.5--9.8). No severity required clipping to 5--95\%. An increased stenosis lowers FFR and a reduced stenosis raises it, so each sign is reported separately and pooled (Table~\ref{tab:throat}). Because the topology and the reference radius are unchanged, Protocol B re-derives the clean bed and gives the same result as Protocol A. With fixed boundary conditions, the pooled throat errors changed the decision in 40\% (discrete) and 42\% (leaky) of models at $\pm 10$ points and in 30\% and 36\% at half a voxel, against 33\% and 32\% for topological errors on the same instances (paired sign test on per-instance proportions: $p = 0.21$ and 0.012 at $\pm 10$ points, $p = 1.0$ and 0.46 at half a voxel). Flips beyond the grey zone made up 27\% and 35\% of models at $\pm 10$ points. Every flip followed the sign of the error. Tuning moved FFR further from the clean value, because the clean territory flow was forced through a wrong throat, and 51--86\% of tuned throat-error models passed the perfusion check while materially wrong. Protocol C fits reached the search bound in 11 models with an increased stenosis and were excluded; Protocol D fits reached the parameter bound in 97 such models, mostly with a residual above 10\%, and were retained as in Table~I.

**LaTeX table (header + body; the body is also written to `results/t5_throat-2026-10-09/tab_t5_throat.tex`):**

```latex
\begin{table*}[!ht]
\caption{Throat Caliber Error (T5): Flips, Passes-and-Wrong and Flips Beyond the Grey Zone, \% of Models (Wilson 95\% Interval)}\label{tab:throat}
\centering\footnotesize\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}llrccc rccc@{}}
\toprule
 & & \multicolumn{4}{c}{Discrete bed (97 instances)} & \multicolumn{4}{c}{Leaky bed (150 instances)}\\
\cmidrule(lr){3-6}\cmidrule(l){7-10}
Error & Protocol & $n$ & Flip & Passes and wrong & Beyond zone & $n$ & Flip & Passes and wrong & Beyond zone\\
\midrule
BODY
\bottomrule
\end{tabular}
\\[3pt]
\parbox{0.95\textwidth}{\footnotesize DS $\pm10$: diameter stenosis raised or lowered by 10 percentage points. Throat $\mp\tfrac12$ voxel: throat diameter narrowed or widened by half the in-plane voxel size. Passes and wrong: perfusion residual below 10\% and $|\Delta\mathrm{FFR}| > 0.05$. Beyond zone: flips whose corrupted FFR lies outside 0.75--0.85. Protocol C fits on the search bound are excluded, which reduces $n$. For comparison, topological errors under Protocol A flipped 33\% (26--41\%) and 32\% (26--38\%) of models and caliber errors away from the throat 10\% (7--15\%) and 6\% (4--9\%).}
\end{table*}
```

with BODY =

```latex
DS $+10$ & A & 97 & 34 (25--44) & 11 (6--19) & 30 (22--40) & 150 & 34 (27--42) & 31 (24--38) & 26 (20--34) \\
 & B & 97 & 34 (25--44) & 11 (6--19) & 30 (22--40) & 150 & 34 (27--42) & 31 (24--38) & 26 (20--34) \\
 & C & 90 & 39 (29--49) & 34 (25--45) & 34 (25--45) & 149 & 36 (29--44) & 49 (41--57) & 32 (25--39) \\
 & D & 97 & 38 (29--48) & 65 (55--74) & 33 (24--43) & 150 & 37 (30--45) & 91 (86--95) & 31 (24--38) \\
\addlinespace[2pt]
DS $-10$ & A & 97 & 45 (36--55) & 29 (21--39) & 25 (17--34) & 150 & 50 (42--58) & 49 (41--57) & 43 (36--51) \\
 & B & 97 & 45 (36--55) & 29 (21--39) & 25 (17--34) & 150 & 50 (42--58) & 49 (41--57) & 43 (36--51) \\
 & C & 97 & 49 (40--59) & 66 (56--75) & 39 (30--49) & 150 & 50 (42--58) & 74 (66--80) & 50 (42--58) \\
 & D & 97 & 52 (42--61) & 85 (76--90) & 47 (38--57) & 150 & 50 (42--58) & 80 (73--86) & 50 (42--58) \\
\addlinespace[2pt]
DS $\pm10$ pooled & A & 194 & 40 (33--47) & 20 (15--26) & 27 (22--34) & 300 & 42 (37--48) & 40 (34--45) & 35 (30--40) \\
 & B & 194 & 40 (33--47) & 20 (15--26) & 27 (22--34) & 300 & 42 (37--48) & 40 (34--45) & 35 (30--40) \\
 & C & 187 & 44 (37--52) & 51 (44--58) & 37 (30--44) & 299 & 43 (38--49) & 62 (56--67) & 41 (35--46) \\
 & D & 194 & 45 (38--52) & 75 (68--80) & 40 (34--47) & 300 & 44 (38--49) & 86 (81--89) & 40 (35--46) \\
\addlinespace[2pt]
Throat $-\tfrac12$ voxel & A & 97 & 28 (20--37) & 26 (18--35) & 16 (10--25) & 150 & 25 (19--33) & 43 (36--51) & 15 (10--22) \\
 & B & 97 & 28 (20--37) & 26 (18--35) & 16 (10--25) & 150 & 25 (19--33) & 43 (36--51) & 15 (10--22) \\
 & C & 96 & 30 (22--40) & 49 (39--59) & 23 (16--32) & 149 & 26 (19--33) & 68 (61--75) & 21 (15--28) \\
 & D & 97 & 30 (22--40) & 84 (75--90) & 25 (17--34) & 150 & 27 (21--35) & 91 (85--94) & 19 (14--26) \\
\addlinespace[2pt]
Throat $+\tfrac12$ voxel & A & 97 & 32 (24--42) & 32 (24--42) & 12 (7--20) & 150 & 47 (39--55) & 41 (34--49) & 26 (20--34) \\
 & B & 97 & 32 (24--42) & 32 (24--42) & 12 (7--20) & 150 & 47 (39--55) & 41 (34--49) & 26 (20--34) \\
 & C & 97 & 45 (36--55) & 65 (55--74) & 21 (14--30) & 150 & 49 (41--57) & 69 (61--76) & 38 (31--46) \\
 & D & 97 & 49 (40--59) & 77 (68--85) & 28 (20--37) & 150 & 49 (41--57) & 71 (64--78) & 39 (31--47) \\
\addlinespace[2pt]
$\pm\tfrac12$ voxel pooled & A & 194 & 30 (24--37) & 29 (23--36) & 14 (10--20) & 300 & 36 (31--42) & 42 (37--48) & 21 (16--26) \\
 & B & 194 & 30 (24--37) & 29 (23--36) & 14 (10--20) & 300 & 36 (31--42) & 42 (37--48) & 21 (16--26) \\
 & C & 193 & 38 (31--45) & 57 (50--64) & 22 (17--28) & 299 & 37 (32--43) & 69 (63--74) & 29 (25--35) \\
 & D & 194 & 40 (33--47) & 80 (74--85) & 26 (21--33) & 300 & 38 (33--44) & 81 (76--85) & 29 (24--34) \\
```

## 6. Runtime and files written

**Runtime** (8 CPUs shared with other jobs; load average above 200 during the run):
- validation: 2 × 110 s (4 workers);
- full run: 1,163 s (4 workers, 300 instance-bed tasks; A–C and D in one pass);
- summary: under 10 s.

**Code** (new files; no frozen file was edited):
- `code/t5_throat_error_types.py`: T5 variants, patched insert, `install()`
- `code/t5_throat_run.py`: `validate` and `run`
- `code/t5_throat_summarise.py`: cells, sign tests, magnitude, LaTeX body

**Outputs** in `results/t5_throat-2026-10-09/`:
- `validation.txt` and `validation_monotonic.csv`
- `ablation_t5.csv`: A–C, 3,874 rows including 298 clean rows
- `perterritory_t5.csv`: D, 1,192 rows
- `t5_insert_log.csv`: 2,384 insertions, with requested, applied and realised DS
- `run.txt`
- `t5_cells.csv`, `t5_sign_tests.csv`, `t5_magnitude.txt` and `tab_t5_throat.tex`

**Scratch:** `/private/tmp/claude-501/t5_run.log`. `t5_throat_run.py run` now writes per-task checkpoints to `/private/tmp/claude-501/t5_throat_parts/`. That option was added during the run and the full run did not use it; the computation is unchanged.
