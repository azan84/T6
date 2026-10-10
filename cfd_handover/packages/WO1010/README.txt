WORK ORDER 2026-10-10 packages. READY 2026-10-10. Read ../../WORK-ORDER-2026-10-10.md first.

14 packages, same format as M1 and P5. Start with README.md inside each package (frame, build order, return).

  T5_vox_narrow / T5_vox_wide   the stenosis throat radius changed by a quarter of the scan's in-plane voxel
                                spacing (half a voxel in diameter). Only r_target_mm / radial_scale inside the lesion
                                window differ from the baseline package of the same instance:
                                  scan 14   0.2306 -> 0.1510 / 0.3102 mm (34 points)
                                  scan 138  0.4026 -> 0.3016 / 0.5037 mm (40 points)
                                  scan 473  0.6097 -> 0.5143 / 0.7051 mm (36 points)
                                  scan 306  0.2696 -> 0.1802 / 0.3589 mm (44 points)
  T1_missed_branch              as in M1: a deleted side branch by mask edit (6-connected, protect 1.10 r, one pass).
  306 baseline                  new instance; its baseline is solved once in resistance mode and the case kept.

Baselines of scans 14, 138, 69, 473, 139 are the M1/P5 solves already returned: reuse them.

NOT IN THESE PACKAGES, deliberately: any 0D prediction (CFD-ARM-SPEC §13). The exporter's blinding check passed.
The word "expected_0D" appears in meta.json only as the name of the withheld file, as in the P5 packages.
