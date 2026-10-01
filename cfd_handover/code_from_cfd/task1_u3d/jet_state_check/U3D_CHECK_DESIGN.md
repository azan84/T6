# U3D jet-state check (2026-10-01, written BEFORE any result of the re-run)
Question: were the U3D 3D levels (S50, S25A, S12A, S25B, S12B; fields deleted) on the axisymmetric or the wall-deflected steady state of the sten70 case (report sec. B3)?
Method: rebuild level S50 with the deposited tooling (u3d/make_sten70_fine_stl.py, make_sten70_mesh.py S50, build_sten70_case.py S50, U3D_END=3000 as the original), run it (8 ranks, --bind-to none: the host is shared with another project's 8 serial jobs; timing is not a result), keep the final fields, compute the jet offset (|U_x|-weighted centroid, jet_offset.py: x = 35..80 mm) and the FFR at x = 56.5 mm (last-100 mean).
Decision rule (fixed now):
 (a) re-run jet offset <= 10 um at x = 50 and 56.5 mm AND |FFR - 0.793362| <= 1e-4 -> the original S50 was on the axisymmetric state (same value on the same state); evidence for the other levels stays indirect (families A/B and wedge agreement), but the level that controls the observed order is verified.
 (b) re-run deflected (offset >= 30 um) -> report its FFR; if it differs from 0.793362 by > 5e-4, the original S50 was on the OTHER (axisymmetric) state; then run S50 again from a perturbed/mapped symmetric start is NOT done automatically (decision for the study lead).
 (c) symmetric but |FFR - 0.793362| > 1e-4 -> mesh-realisation effect larger than expected: report, no conclusion on the state of the original.
 (d) anything else (10-30 um, unsettled) -> inconclusive, report.
Then, if time allows and (a) holds: the same for S25A (U3D_END=4000).
