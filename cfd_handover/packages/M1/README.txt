GATE M1 — three real-lumen case packages. READY 2026-09-19.

Instance: scan 14, left LAD, proximal, 20 mm lesion, 80 %DS. One instance in three conditions, chosen to exercise
the risky step hardest rather than to be typical (highest %DS in the frozen 3D subset, has a deletable side branch,
most outlets).

  14_..._clean_nolesion__real   the unmodified lumen: plain mask -> mesh. Tests the truncation clip alone.
  14_..._baseline__real         + the 80 %DS lesion by vertex deformation (radial_scale in centreline.vtp).
  14_..._T1_missed_branch__real + a deleted side branch by mask edit.

WHAT M1 IS TESTING (CFD-ARM-SPEC §7): that an edited CT lumen mask becomes a checkMesh-clean, converged case with
NO MANUAL GEOMETRY REPAIR. Pass = clean mesh + converged solve + as-meshed radius returned + both BC modes stable.
Kill = 5 working days of effort without a scriptable path, then the §9 fallback. Wall-clock must be recorded: it
replaces the estimates in spec §4 and sets the study's case count.

RETURN: fill ../../returns/M1_results_TEMPLATE.csv and save it as returns/M1_results.csv. Also return the as-meshed
radius along the centreline per case. Both BC modes (resistance and prescribed-flow) must be exercised and stable —
that is part of the pass criterion, not an extra.

START WITH README.md INSIDE EACH PACKAGE. It gives the frame, the build order and what to return, so you should not
need to open CFD-ARM-SPEC to run a case.

TWO THINGS THAT WILL BITE IF SKIPPED, both measured on this exact scan:

 1. FRAME. Points are mm, LPS. The ImageCAS-X NIfTI affine is RAS: negate x and y before inv(affine). With the flip,
    42/42 of the branch-deletion points land inside the lumen; without it, 0/42.

 2. THE DELETION RULE IS 6-CONNECTED, PROTECT RADIUS 1.10 r, and it is run ONCE over the union of the truncation set
    and the branch set. This is not a detail: with 26-connectivity the flood fill walks the lumen's surface shell and
    erodes the retained LAD — 2061 voxels removed against a ground truth of ~770, in one web spanning 18x31x38 mm.
    As shipped (6-connected, 1.10 r) the T1 case removes 2089 voxels with 40 of erosion and leaves the mask with its
    original 2 connected components; the two truncation-only cases remove 1310 with 25 of erosion, also 2 components.
    A reference implementation ships inside mask_edit.json and was executed verbatim to produce those numbers.

NOT IN THESE PACKAGES, deliberately: any 0D prediction (CFD-ARM-SPEC §13). The exporter refuses to write a package
containing one. Note the one thing that is NOT blind: bc_A x bc_C_flows reconstructs the CLEAN outlet pressures
exactly. What is blind is the corrupted-geometry prediction and the error-induced change in it.

Stage A in ../../START-HERE.md still does not depend on any of this and can run alongside.
