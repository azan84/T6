"""
export_cfd_case.py — build a CFD case package for one (instance x error type x tier), per CFD-ARM-SPEC v0.2 §11.

A package is the ONLY thing that crosses to the CFD machine: kilobytes of centreline, boundary conditions and probe
positions. Meshes and fields never come back into Drive (CFD-ARM-SPEC §11, cfd_handover/START-HERE.md).

  usage:
    export_cfd_case.py <data_root> --m1 [--out <dir>]        the three Gate M1 packages (§7)
    export_cfd_case.py <data_root> --subset [--tier real]    every instance in CFD-SUBSET-FROZEN
    export_cfd_case.py <data_root> --instance <n> --error <type> --tier real|polyball

v0.2, 2026-09-19 — rewritten against an independent adversarial review
(references/FABLE-REVIEW-EXPORTER-2026-09-19.md, GO-WITH-CHANGES, MUST 1-8). What changed and why:
  1 MANIFEST carried ffr_discrete/base_discrete — a direct §13 blinding violation. Now an instance key only, and
    check_no_predictions() greps every written file for FFR-like fields and refuses to finish if one appears.
  2 The coordinate frame was never stated. Points are mm, LPS; the ImageCAS-X NIfTI affine is RAS. With the flip
    42/42 of the probe's deletion points landed in the lumen; without it, 0/42.
  3 The T1/T2 voxel deletion rule shredded the branch: 512 of 855 voxels removed and 67 disconnected islands on the
    real mask. Replaced by a protect-then-flood-fill rule, shipped with a reference implementation so "executable by
    someone with only the mask and this file" is literally true.
  4 --with-expected wrote withheld/ INSIDE cfd_handover/. Now results/cfd_withheld/, and writing under the handover
    tree is refused.
  5 No truncation rule for the real tier: the mask carries vessel below the 0.60 mm cut that 0D does not model and
    polyball does not have by construction — an unstated construction difference inside the |polyball - real| gap.
  6 NaN reached bc_A.csv for every T2 and T4 package (an outlet with no clean counterpart). Now an explicit
    mode column, resistance | closed, matching what ablation.py does with w = 0, plus an isfinite assert.
  7 T4 packages carried no taper instruction at all, and the vtp's MISR was the PRE-lesion radius, so a polyball
    built from the package was the unlesioned tube. Now every package ships per-point radial_scale and r_target_mm,
    and one surface rule covers baseline, T3 and T4 on both tiers.
  8 Protocol C's variant was unstated, and the claim that the territory variant is runnable from the package was
    false for T1/T2 (the deleted outlet's share is not in it). Now stated, with clean territory totals both ways.

WHAT IS DELIBERATELY NOT IN A PACKAGE (CFD-ARM-SPEC §13): expected_0D.json, any FFR, any pressure the 0D model
predicts. NOTE the reviewer's finding, to be reflected in §13: bc_A x bc_C_flows reconstructs the CLEAN outlet
pressures exactly, so what is blind is the CORRUPTED-geometry prediction and dFFR, not every 0D quantity.
"""
from __future__ import annotations
import argparse, json, sys, hashlib, re
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from zerod_ffr import Tree, P_AORTA, P_VEN, RHO, MU, MURRAY_EXP, R_RESOLVED
from severity_sweep import load, plan, insert, HOSTS, RUNOFF
from error_types import ERROR_TYPES, T3_LENGTH_DELTA
from ablation import node_map, bed_flow, territories, subtree, trunc_for, CALIBRE_ONLY

BED = "discrete"                      # the 3D arm replicates the discrete bed and only the discrete bed (§2.4/§2.5)
STATION_GRID_MM, STATION_CAP, STATION_MERGE_MM = 5.0, 40, 1.0
BIF_OFFSET_MM = None                  # set per station from the local diameter: >= 1 D proximal and distal
CLEAN_NOLESION, BASELINE = "clean_nolesion", "baseline"
FRAME = ("mm, LPS. The ImageCAS-X NIfTI affine is RAS: negate x and y before applying inv(affine) to reach voxel "
         "indices. Verified — with the flip 42/42 deletion points land inside the lumen, without it 0/42.")

PROTECT_R, CONNECTIVITY = 1.10, 1      # scipy generate_binary_structure(3, 1) == 6-connectivity

DELETION_RULE = (
    "PROTECT-THEN-FLOOD-FILL, applied ONCE to the union of everything being removed (sub-cut vessel from the "
    "truncation step and, if present, the missed branch). (1) protect = every voxel within 1.10*r_mm of any point in "
    "retained_points_mm; (2) candidates = mask AND NOT protect; (3) delete the 6-CONNECTED components of candidates "
    "that contain any point of the deletion set; (4) re-run marching cubes. "
    "TWO PARAMETERS THAT LOOK COSMETIC AND ARE NOT, both measured on scan 14: "
    "(a) 26-connectivity walks the lumen's surface shell past the protect radius and erodes the RETAINED vessel — "
    "2061 voxels removed against a ground truth of 760-772, i.e. 1298 voxels of the LAD, in one 26-connected web "
    "spanning 18x31x38 mm and touching 97 of 706 retained centreline points. 6-connectivity with protect 1.10 r "
    "removes 779 with 20 voxels of erosion and 13 remnant, and leaves the mask with its original 2 components. "
    "(b) a per-point radial ball instead of a flood fill removes 512 of 855 branch voxels and leaves 67 disconnected "
    "islands. Either way Gate M1 would then fail because of the RULE rather than because of the lumen.")

REFERENCE_IMPL = '''\
# reference implementation of the deletion rule (numpy + scipy + nibabel only).
# Applies ONE flood fill to the union of the truncation set and the branch set, per mask_edit.json.
import numpy as np, nibabel as nib, json
from scipy.ndimage import label, generate_binary_structure
img = nib.load(MASK_NII); mask = np.asarray(img.dataobj) > 0
inv = np.linalg.inv(img.affine); sp = np.array(img.header.get_zooms()[:3])
def to_ijk(pts):                              # LPS -> RAS -> voxel index
    ras = np.asarray([[p["x"], p["y"], p["z"]] for p in pts]) * np.array([-1.0, -1.0, 1.0])
    return (inv @ np.c_[ras, np.ones(len(ras))].T)[:3].T
def ball(c_ijk, r_mm):
    rad = np.ceil(r_mm / sp).astype(int); c = np.round(c_ijk).astype(int)
    sl = tuple(slice(max(c[d]-rad[d], 0), min(c[d]+rad[d]+1, mask.shape[d])) for d in range(3))
    g = np.mgrid[sl]; return sl, sum(((g[d]-c_ijk[d])*sp[d])**2 for d in range(3)) <= r_mm**2
e = json.load(open("mask_edit.json"))
protect = np.zeros_like(mask)
for p, q in zip(e["retained_points_mm"], to_ijk(e["retained_points_mm"])):
    sl, b = ball(q, 1.10 * p["r_mm"]); protect[sl] |= b       # 1.10 r, NOT 1.00 r
kill_pts = list(e["sub_cut_points_mm"]) + list(e.get("mask_edit", {}).get("deleted_points_mm", []))
lab, _ = label(mask & ~protect, structure=generate_binary_structure(3, 1))   # 6-connectivity, NOT 26
kill = {lab[tuple(np.clip(np.round(q).astype(int), 0, np.array(mask.shape)-1))] for q in to_ijk(kill_pts)}
out = mask & ~np.isin(lab, [k for k in kill if k > 0])
nib.save(nib.Nifti1Image(out.astype(np.uint8), img.affine), "mask_edited.nii.gz")
'''

TRUNCATION_RULE = (
    "The 0D model is truncated at r_ref < 0.60 mm (CFD-ARM-SPEC §2.4) and the 3D model must be truncated at the SAME "
    "place, or the |polyball - real| gap silently contains a construction difference rather than a geometry one. "
    "(1) Remove the sub-cut vessel that the active centreline does not cover: sub_cut_points_mm is the deletion set, "
    "retained_points_mm is the protect set, and the rule is the SAME protect-then-flood-fill as deletion_rule — run "
    "it ONCE over the union of both deletion sets, BEFORE marching cubes. (2) Then clip the lumen at every outlet "
    "plane in outlets.csv (position + outward normal), discard the distal component, and apply flow extensions to "
    "the clipped face per §6.2. (3) The polyball tier has none of this vessel by construction, so this step is what "
    "makes the two tiers comparable.")

# ------------------------------------------------------------------------------------------------------ helpers
def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def data_root(arg: str) -> Path:
    """Accept either the download directory or the dataset directory inside it (the documented invocation used the
    former and failed: centerlines/ lives one level down)."""
    p = Path(arg).expanduser()
    if (p / "centerlines").is_dir(): return p
    for c in sorted(p.glob("*")):
        if c.is_dir() and (c / "centerlines").is_dir(): return c
    raise SystemExit(f"no centerlines/ under {p}")

def tangent(t: Tree, v: int, n_back: int = 3) -> np.ndarray:
    """Flow-direction tangent averaged over a few edges — a single 0.4 mm edge is jittery and a flow extension
    inherits its direction.

    THE ROOT HAS NO PARENT. Walking backwards from it returned the (0,0,1) placeholder, which put the inlet normal
    32 degrees off the vessel axis in every package (cos 0.85 against the true root direction). At the root, walk
    FORWARD along the largest child instead — same parent->child convention, so inlet and outlet normals agree.
    """
    chain = [int(v)]
    while len(chain) <= n_back and t.parent[chain[-1]] >= 0:
        chain.append(int(t.parent[chain[-1]]))
    if len(chain) == 1:
        u = int(v)
        for _ in range(n_back):
            if not t.children[u]: break
            u = max(t.children[u], key=lambda c: t.r_ref[c])
        d = t.xyz[u] - t.xyz[int(v)]
    else:
        d = t.xyz[chain[0]] - t.xyz[chain[-1]]
    n = float(np.linalg.norm(d))
    return d / n if n > 1e-12 else np.array([0.0, 0.0, 1.0])

def check_no_predictions(d: Path):
    """MUST 1. A package must contain no 0D prediction. The invariant is deliberately blunt and total:
    NO package file may contain the substring "ffr" in any case, anywhere, .vtp included.

    The first version matched \\b(ffr|FFR)\\b, which a probe showed is trivially bypassable — it does not match
    ffr_discrete, ffr_measurement, FFR_meas or dFFR, so the real withheld expected_0D.json dropped into a package
    would have PASSED. A blunt substring rule cannot be bypassed by a field name, which is worth more than the
    ability to use the word in a comment; package prose is written around it.
    """
    tokens = ("ffr", "base_discrete", "min_ffr", "lesion_ffr")
    for p in sorted(d.rglob("*")):
        if not p.is_file(): continue
        if p.suffix == ".vtp":
            # pyvista writes the arrays as zlib+base64 INSIDE the DataArray elements, so a raw byte scan hits the
            # encoded payload: a 3-character token over base64's 64-character alphabet matches by chance with
            # probability ~18 % per file at this size, and the first export duly tripped on one. A name-based leak
            # can only live in an array name, so check those; a numeric leak under an innocuous name is not
            # greppable in any encoding and is controlled by authoring the arrays here, not by this guard.
            import pyvista as pv
            mesh = pv.read(p)
            names = list(mesh.point_data.keys()) + list(mesh.cell_data.keys()) + list(mesh.field_data.keys())
            hits = [n for n in names if any(t in n.lower() for t in tokens)]
            if hits:
                raise SystemExit(f"BLINDING VIOLATION (CFD-ARM-SPEC §13): {p.relative_to(d)} array name(s) {hits}")
            continue
        blob = p.read_bytes().lower()
        for token in tokens:
            if token.encode() in blob:
                raise SystemExit(f"BLINDING VIOLATION (CFD-ARM-SPEC §13): {p.relative_to(d)} contains {token!r}")

# --------------------------------------------------------------------------------------------------- geometry out
def active_polydata(t: Tree, r_target: np.ndarray, scale_vs_clean: np.ndarray):
    """The active (non-truncated) tree as a VTK polyline set — CFD-ARM-SPEC §11 centreline.vtp. Frame: mm, LPS.

    radial_scale / r_target_mm (MUST 7) make ONE surface rule cover baseline, T3 and T4 on both tiers:
    scale each surface vertex's distance to its nearest centreline point by that point's radial_scale.
    MaximumInscribedSphereRadius is VMTK's name and is the AS-EDITED radius, so vmtkcenterlinemodeller builds the
    lesioned tube directly; r_source_mm keeps the unedited value for reference.
    """
    import pyvista as pv
    act = np.where(t.active)[0]
    remap = -np.ones(len(t.parent), int); remap[act] = np.arange(len(act))
    lines = []
    for v in act:
        p = t.parent[v]
        if p >= 0 and t.active[p]:
            lines += [2, int(remap[p]), int(remap[v])]
    m = pv.PolyData(t.xyz[act] * 1e3, lines=np.array(lines, dtype=np.int64))
    m.point_data["MaximumInscribedSphereRadius"] = r_target[act] * 1e3
    m.point_data["r_target_mm"] = r_target[act] * 1e3
    m.point_data["r_source_mm"] = t.r[act] * 1e3
    m.point_data["radial_scale"] = scale_vs_clean[act]
    m.point_data["r_ref_mm"] = t.r_ref[act] * 1e3
    m.point_data["r_fit_mm"] = t.r_fit[act] * 1e3
    m.point_data["segment_name"] = np.array([str(x) for x in t.label[act]])
    m.point_data["branch_id"] = t.seg[act].astype(np.int32)
    m.point_data["tree_node"] = act.astype(np.int32)          # tree index, NOT a vtp point id; coordinates are identity
    m.point_data["resolved"] = t.resolved[act].astype(np.int8)
    return m

def stations(t: Tree, path, s_arc, c, L, meas_node):
    """Probe stations along the host vessel — DETECTOR-SPEC v0.2 §8.

    A `bifurcation` station is ill-defined for a single cutting plane, so each bifurcation contributes stations
    >= 1 local diameter proximal and distal instead of one at the carina (review MUST 8 of the detector review).
    """
    res = t.resolved[path]
    s_end = float(s_arc[res][-1]) if res.any() else float(s_arc[-1])
    anchors = [(float(c - L / 2), "lesion_prox"), (float(c), "throat"), (float(c + L / 2), "lesion_dist")]
    if meas_node in path:
        anchors.append((float(s_arc[int(np.argmin(np.abs(path - meas_node)))]), "measurement"))
    for k, v in enumerate(path):
        if len(t.children[int(v)]) >= 2:
            d_loc = 2.0 * float(t.r_ref[int(v)])
            anchors += [(float(s_arc[k] - d_loc), "bif_prox"), (float(s_arc[k] + d_loc), "bif_dist")]
    anchors = [(s, k) for s, k in anchors if 0.0 <= s <= s_end]
    # ANCHORS ARE PLACED FIRST AND NEVER DROPPED. Merging a single sorted list lost named anchors whenever a grid
    # point fell less than the merge distance BEFORE one: `measurement` went missing or came back relabelled `grid`
    # in 4 of 6 study-type packages, and `lesion_dist` and `throat` in one each. The named stations are the whole
    # point of the file, so they are laid down first and the grid fills the gaps that remain.
    for step in (STATION_GRID_MM * 1e-3, 2 * STATION_GRID_MM * 1e-3):
        merged = []
        for s, kind in sorted(anchors, key=lambda z: z[0]):
            if merged and abs(s - merged[-1][0]) < STATION_MERGE_MM * 1e-3: continue
            merged.append((s, kind))
        for s in np.arange(0.0, s_end + 1e-12, step):
            if all(abs(float(s) - m0) >= STATION_MERGE_MM * 1e-3 for m0, _ in merged):
                merged.append((float(s), "grid"))
        merged.sort(key=lambda z: z[0])
        if len(merged) <= STATION_CAP: break
    rows = []
    for s, kind in merged:
        k = int(np.argmin(np.abs(s_arc - s))); v = int(path[k])
        n = tangent(t, v)
        rows.append(dict(probe_id=f"p{len(rows):03d}", kind=kind, s_mm=s * 1e3, s_node_mm=float(s_arc[k] * 1e3),
                         s_from_lesion_mm=(s - c) * 1e3, tree_node=v,
                         x=t.xyz[v][0] * 1e3, y=t.xyz[v][1] * 1e3, z=t.xyz[v][2] * 1e3,
                         normal_x=n[0], normal_y=n[1], normal_z=n[2],
                         r_ref_mm=t.r_ref[v] * 1e3, resolved=int(t.resolved[v])))
    # tangent(t, 0), NOT tangent(t, path[0]): path[0] is the first node of the HOST VESSEL, which on a left tree is
    # 11 mm downstream of the ostium and points 37 degrees away from it. The inlet patch is at the tree root.
    root_n = tangent(t, 0)
    rows.insert(0, dict(probe_id="inlet", kind="inlet", s_mm=0.0, s_node_mm=0.0, s_from_lesion_mm=-c * 1e3,
                        tree_node=0, x=t.xyz[0][0] * 1e3, y=t.xyz[0][1] * 1e3, z=t.xyz[0][2] * 1e3,
                        normal_x=root_n[0], normal_y=root_n[1], normal_z=root_n[2],
                        r_ref_mm=t.r_ref[0] * 1e3, resolved=int(t.resolved[0])))
    for v in t.leaves:
        v = int(v); n = tangent(t, v)
        rows.append(dict(probe_id=f"out_{v}", kind="outlet", s_mm=np.nan, s_node_mm=float(t.arc[v] * 1e3),
                         s_from_lesion_mm=np.nan, tree_node=v,
                         x=t.xyz[v][0] * 1e3, y=t.xyz[v][1] * 1e3, z=t.xyz[v][2] * 1e3,
                         normal_x=n[0], normal_y=n[1], normal_z=n[2],
                         r_ref_mm=t.r_ref[v] * 1e3, resolved=int(t.resolved[v])))
    return pd.DataFrame(rows)

# --------------------------------------------------------------------------------------------------- the package
def build(root: Path, row, etype: str, tier: str, outdir: Path, withheld_dir: Path | None = None):
    t = load(root, int(row.scan), row.side, BED)
    o = t.ffr("murray", 1.0); C_clean = o["C"]
    slots, _ = plan(t, row.side, t.last["ffr"].copy())
    sl = next((s for s in slots if s["vessel"] == row.vessel and s["loc"] == row["loc"]
               and abs(s["L"] * 1e3 - row.L_mm) < 1e-6), None)
    if sl is None:
        raise SystemExit(f"instance not eligible under the {BED} bed: {row.scan} {row.side} {row.vessel}")
    path, s_arc, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]
    meas_clean = int(path[mi]); ds = row.ds_pct / 100
    r_clean, _ = insert(t, path, s_arc, c, L, ds)

    if etype in (CLEAN_NOLESION, BASELINE):
        t2, m, info = t, np.arange(len(t.parent)), {}
        r2 = t.r.copy() if etype == CLEAN_NOLESION else r_clean
        path2, s2, c2, L2, meas2 = path, s_arc, c, L, meas_clean
    else:
        segs2, info = ERROR_TYPES[etype](list(t.segments), t, path, s_arc, c, L)
        if segs2 is None: raise SystemExit(f"{etype} not applicable: {info}")
        # trunc_for, NOT the default: decision B3 scales the truncation radius with T4's calibre error, and the 3D
        # geometry must be truncated exactly where its 0D twin is or the |polyball - real| comparison silently
        # contains a construction difference. ablation.py:148 does the same.
        t2 = Tree(segs2, f"{t.name}_{etype}", bed=BED, r_trunc=trunc_for(BED, etype),
                  trunc_ref=t if etype in CALIBRE_ONLY else None)
        m = node_map(t, t2)
        path2, _ = t2.vessel_path(HOSTS[row.side][row.vessel])
        if path2 is None or len(path2) < 3: raise SystemExit(f"{etype}: host vessel lost")
        s2 = t2.arc[path2] - t2.arc[path2[0]]
        L2 = L + T3_LENGTH_DELTA if etype == "T3_stenosis_length" else L
        c2 = c
        cand = np.where(m == meas_clean)[0]
        meas2 = int(cand[0]) if len(cand) else int(path2[min(int(np.searchsorted(s2, c + L / 2 + RUNOFF)),
                                                             len(path2) - 1)])
        r2, _ = insert(t2, path2, s2, c2, L2, ds)

    # MUST 7: one surface rule for every calibre edit. scale is against the ORIGINAL mask radius at the same
    # anatomical point, because the CFD side starts from the original mask.
    scale = np.ones(len(t2.parent))
    ok = m >= 0
    scale[ok] = r2[ok] / np.maximum(t.r[m[ok]], 1e-12)

    ffr0, Q0, info0, _, _ = t.evaluate(C_clean, r_clean)
    q0_all = bed_flow(t, C_clean, ffr0)
    terr2 = territories(t2)
    terr_of = {int(v): j for j, sub in enumerate(terr2) for v in sub}

    # --- outlets and BCs
    rows = []
    for v in t2.leaves:
        v = int(v); n = tangent(t2, v)
        rows.append(dict(outlet_id=f"out_{v}", tree_node=v,
                         x=t2.xyz[v][0] * 1e3, y=t2.xyz[v][1] * 1e3, z=t2.xyz[v][2] * 1e3,
                         normal_x=n[0], normal_y=n[1], normal_z=n[2],
                         r_ref_mm=t2.r_ref[v] * 1e3, r_mm=t2.r[v] * 1e3, territory_id=terr_of.get(v, -1)))
    out = pd.DataFrame(rows)
    w_clean = np.where(m >= 0, t.w[np.maximum(m, 0)], 0.0)
    # MUST 6: an outlet with no clean counterpart has w = 0 in ablation.py Protocol A, i.e. zero conductance, i.e.
    # a WALL. Say so explicitly instead of writing an empty cell that a solver would read as a missing BC.
    mode_A = ["resistance" if w_clean[r.tree_node] > 0 else "closed" for r in out.itertuples()]
    R_A = np.array([C_clean / w_clean[r.tree_node] if w_clean[r.tree_node] > 0 else 0.0 for r in out.itertuples()])
    t2._C.clear(); C_B = t2.calibrate(t2.demand("murray", 1.0))
    R_B = np.array([C_B / t2.w[r.tree_node] for r in out.itertuples()])
    # Protocol C targets under DECISION B1 (2026-09-19): each territory must deliver the clean tree's FULL outflow,
    # including the share of any branch the error deleted. 3D prescribes per outlet, so that territory total needs an
    # INTRA-TERRITORY SPLIT RULE. Survivors are scaled by the territory's shortfall ratio, which preserves their
    # Murray proportions and makes the per-outlet sum equal the full territory target:
    #     Q_i = q_clean_i * (Q_full_territory / Q_surviving_territory)
    # The alternative (prescribe each survivor its own unchanged clean flow) is the pre-B1 definition and leaves the
    # deleted branch's perfusion simply unaccounted for.
    q_surv = np.array([q0_all[m[r.tree_node]] if m[r.tree_node] >= 0 else 0.0 for r in out.itertuples()])
    q_tgt = q_surv.copy()
    for j, sub in enumerate(terr2):
        idx = [i for i, r in enumerate(out.itertuples()) if r.territory_id == j]
        if not idx: continue
        root_clean = int(m[int(sub[0])])
        if root_clean < 0: continue
        q_full = float(q0_all[subtree(t, root_clean)].sum())
        q_s = float(q_surv[idx].sum())
        if q_s > 0 and q_full > 0:
            q_tgt[idx] = q_surv[idx] * (q_full / q_s)
    # An outlet whose clean counterpart is an INTERIOR node carries no bed flow in the discrete bed (w = 0 off the
    # leaves), so mapping alone is not enough: a T2 stump maps fine and still has Q_target = 0. Prescribing zero flow
    # would divide by zero when the CFD side derives R_i = (p_i - P_v)/Q_i on the second Protocol C solve. Zero
    # target means a wall, and is written as one.
    mode_C = ["prescribed" if q > 0 else "closed" for q in q_tgt]
    for name, arr in (("R_A", R_A), ("R_B", R_B), ("q_tgt", q_tgt)):
        if not np.isfinite(arr).all():
            raise SystemExit(f"non-finite value in {name} — refusing to write a BC file (review MUST 6)")

    d = outdir / (f"{row.scan}_{row.side}_{row.vessel}_{row['loc']}_{int(row.L_mm)}mm_"
                  f"{int(row.ds_pct)}ds__{etype}__{tier}")
    d.mkdir(parents=True, exist_ok=True)
    active_polydata(t2, r2, scale).save(d / "centreline.vtp")
    out.to_csv(d / "outlets.csv", index=False)
    pd.DataFrame(dict(outlet_id=out.outlet_id, mode=mode_A, R_SI=R_A, R_kinematic=R_A / RHO)).to_csv(
        d / "bc_A.csv", index=False)
    pd.DataFrame(dict(outlet_id=out.outlet_id, mode="resistance", R_SI=R_B, R_kinematic=R_B / RHO)).to_csv(
        d / "bc_B.csv", index=False)
    pd.DataFrame(dict(outlet_id=out.outlet_id, mode=mode_C, territory_id=out.territory_id,
                      Q_target_m3s=q_tgt, Q_target_mls=q_tgt * 1e6)).to_csv(d / "bc_C_flows.csv", index=False)

    # Both territory totals are shipped for audit. DECISION B1 is SETTLED (2026-09-19): the study targets
    # Q_clean_full_territory_mls. Q_clean_surviving_mls is retained only so the difference — exactly the deleted
    # branch's perfusion — is visible and checkable in the package.
    trows = []
    for j, sub in enumerate(terr2):
        mc = m[sub][m[sub] >= 0]
        root_clean = int(m[int(sub[0])]) if m[int(sub[0])] >= 0 else -1
        full = float(q0_all[subtree(t, root_clean)].sum()) if root_clean >= 0 else np.nan
        trows.append(dict(territory_id=j, root_tree_node=int(sub[0]), root_clean_node=root_clean,
                          Q_clean_surviving_mls=float(q0_all[mc].sum()) * 1e6,
                          Q_clean_full_territory_mls=full * 1e6,
                          n_outlets=int(sum(1 for v in sub if v in set(int(x) for x in t2.leaves)))))
    pd.DataFrame(trows).to_csv(d / "territories.csv", index=False)

    st = stations(t2, path2, s2, c2, L2, meas2)
    st.to_csv(d / "probes.csv", index=False)
    (d / "inlet.json").write_text(json.dumps(dict(
        frame=FRAME, P_aorta_Pa=P_AORTA, P_venous_Pa=P_VEN, P_aorta_kinematic=P_AORTA / RHO,
        P_venous_kinematic=P_VEN / RHO, rho=RHO, mu=MU, nu=MU / RHO,
        inlet=dict(x=t2.xyz[0][0] * 1e3, y=t2.xyz[0][1] * 1e3, z=t2.xyz[0][2] * 1e3,
                   r_mm=t2.r[0] * 1e3, normal=list(tangent(t2, 0)))), indent=2))

    # --- the geometry edits the CFD side must perform (§6.1b), with the frame and the rules stated
    inactive = np.where(~t2.active)[0]
    pts = lambda idx: [dict(x=float(t2.xyz[i][0] * 1e3), y=float(t2.xyz[i][1] * 1e3),
                            z=float(t2.xyz[i][2] * 1e3), r_mm=float(t2.r[i] * 1e3)) for i in idx]
    edit = dict(frame=FRAME, tier=tier, error_type=etype,
                surface_rule=("scale each surface vertex's distance to its NEAREST centreline point by that point's "
                              "radial_scale (centreline.vtp point array); radial_scale == 1 means unchanged"),
                truncation_rule=TRUNCATION_RULE, deletion_rule=DELETION_RULE,
                reference_implementation=REFERENCE_IMPL,
                # ONE protect set serves BOTH deletion steps (truncation and, if present, the missed branch):
                # the active centreline of THIS package's tree. Shipped at top level because the truncation step
                # needs it too and it previously lived only inside mask_edit, where a baseline package had none.
                retained_points_mm=pts(np.where(t2.active)[0]),
                sub_cut_points_mm=pts(inactive),
                lesion=(None if etype == CLEAN_NOLESION else dict(
                    centre_mm=float(c2 * 1e3), length_mm=float(L2 * 1e3), ds_pct=float(row.ds_pct),
                    law="w = 0.5*(1+cos(pi*(s-c)/(L/2))) for |s-c| < L/2; r_target = min(r_source, (1-w)*r_source + "
                        "w*r_fit*(1-ds)) — already applied in radial_scale and r_target_mm, given here for audit",
                    table=[dict(s_mm=float(s2[i] * 1e3), tree_node=int(path2[i]),
                                r_source_mm=float(t2.r[path2[i]] * 1e3), r_fit_mm=float(t2.r_fit[path2[i]] * 1e3),
                                r_target_mm=float(r2[path2[i]] * 1e3))
                           for i in np.where(np.abs(s2 - c2) < L2 / 2)[0]])))
    if etype == "T4_taper":
        edit["taper"] = dict(note="the 0.93 radius scale from the proximal shoulder through every descendant is "
                                  "already carried in radial_scale; no separate operation is needed",
                             radius_scale=float(info.get("radius_scale", np.nan)) if isinstance(info, dict) else None,
                             from_arc_mm=float(info.get("from_arc_mm", np.nan)) if isinstance(info, dict) else None)
    if etype in ("T1_missed_branch", "T2_truncation"):
        keep = set(int(x) for x in m[m >= 0].tolist())
        gone = [i for i in range(len(t.parent)) if t.active[i] and i not in keep]
        edit["mask_edit"] = dict(
            rule="see deletion_rule at top level; protect set is retained_points_mm, also at top level",
            deleted_points_mm=[dict(x=float(t.xyz[i][0] * 1e3), y=float(t.xyz[i][1] * 1e3),
                                    z=float(t.xyz[i][2] * 1e3), r_mm=float(t.r[i] * 1e3)) for i in gone],
            info={k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                  for k, v in (info.items() if isinstance(info, dict) else [])})
    (d / "mask_edit.json").write_text(json.dumps(edit, indent=2))

    vtk_p = root / "centerlines" / f"{row.scan}.coronary_{row.side}_centerline.vtk"
    nii_p = root / "segmentations" / f"{row.scan}.coronary.nii.gz"
    meta = dict(
        frame=FRAME,
        instance=dict(scan=int(row.scan), side=row.side, vessel=row.vessel, loc=row["loc"],
                      L_mm=float(row.L_mm), ds_pct=int(row.ds_pct), c_mm=float(c * 1e3)),
        error_type=etype, tier=tier, bed=BED,
        truncation_r_ref_mm=float(t2.r_trunc * 1e3), resolved_r_fit_mm=float(R_RESOLVED * 1e3),
        murray_exponent=MURRAY_EXP, n_outlets=int(len(t2.leaves)), n_territories=int(len(terr2)),
        measurement=dict(tree_node=int(meas2), s_mm=float(t2.arc[meas2] - t2.arc[int(path2[0])]) * 1e3,
                         note="the node the 0D model reports at; NOT necessarily c + L/2 + 20 mm if the error "
                              "type removed that point — see the T2 open item in CFD-ARM-SPEC §17"),
        protocol_C=dict(
            variant="per-outlet prescribed flow, then R_i = (p_i - P_v)/Q_i (CFD-ARM-SPEC §2.2) — EXACTLY "
                    "determined, one target per outlet",
            zerod_primary="ONE global bed scaling against territory totals (STATISTICS-PLAN §P2) — OVER-determined",
            target_definition="DECISION B1, settled 2026-09-19: each territory's target is the CLEAN tree's FULL "
                              "outflow, including the share of any branch the error deleted. Per-outlet targets "
                              "distribute that total across surviving outlets in proportion to their own clean flow "
                              "(see territories.csv for both totals; their ratio is the scaling applied).",
            comparability="these are DIFFERENT fits and must not be compared as if identical: the 0D twin must run "
                          "the identical per-outlet procedure for the ladder comparison. The difference is second "
                          "order for kappa but first order for the residual panel, where it would otherwise read "
                          "as a fidelity effect. Magnitudes are quantified analysis-side (they are 0D predictions "
                          "and are withheld under §13). See territories.csv for both clean totals.",
            settled="Decision B1 was settled 2026-09-19: the FULL territory total. No longer an open question."),
        provenance=dict(centreline_vtk_sha256=sha256(vtk_p), mask_nii_sha256=sha256(nii_p),
                        exporter_sha256=sha256(Path(__file__)), exporter=Path(__file__).name,
                        spec="CFD-ARM-SPEC.md v0.2", detector_spec="DETECTOR-SPEC.md v0.2 (station rule §8)",
                        exported=str(date.today())),
        blinding="expected_0D.json deliberately absent (CFD-ARM-SPEC §13). NOTE: bc_A x bc_C_flows reconstructs the "
                 "CLEAN outlet pressures exactly; what is blind is the CORRUPTED-geometry pressure prediction and "
                 "the error-induced change in it.")
    (d / "meta.json").write_text(json.dumps(meta, indent=2))
    (d / "README.md").write_text(
        f"# {d.name}\n\n**Frame:** {FRAME}\n\n**Tier:** {tier} · **Error type:** {etype}\n\n"
        f"Files: `centreline.vtp` (with `radial_scale`, `r_target_mm`), `outlets.csv`, `bc_A.csv`, `bc_B.csv`, "
        f"`bc_C_flows.csv`, `territories.csv`, `probes.csv`, `inlet.json`, `mask_edit.json`, `meta.json`.\n\n"
        f"## Build\n1. Apply `mask_edit.json.truncation_rule`.\n"
        f"2. Apply `mask_edit.json.mask_edit.rule` if present (a reference implementation ships with it).\n"
        f"3. Marching cubes.\n"
        f"4. **Subdivide the surface inside the lesion window (centre +/- L/2) to edge length <= r_throat/8 BEFORE\n"
        f"   deforming.** At 80 %DS on this cohort r_throat is ~0.23 mm, so the target edge is ~0.03 mm against a\n"
        f"   voxel of ~0.32 mm: roughly 13x refinement. Marching-cubes resolution alone cannot represent the throat\n"
        f"   and the deformation will simply not produce the intended stenosis.\n"
        f"5. Apply `surface_rule` using `radial_scale`, then **check the as-built throat radius against\n"
        f"   `r_target_mm` and reject the case if it differs by more than 1 %** (CFD-ARM-SPEC §6.1a).\n"
        f"6. Flow extensions, mesh, solve per CFD-ARM-SPEC §6.2.\n\n"
        f"## Solver settings that are NOT free choices\n"
        f"- **Resistance-outlet under-relaxation is a stability bound, not a preference:**\n"
        f"  `alpha < 2 / (1 + R_outlet/R_epicardial)`. On these lumens that bound is ~0.10, and the MILDEST cases\n"
        f"  fail first (a mild case has the largest R_outlet/R_epi). **Start at alpha = 0.05.** The 0.2 in the\n"
        f"  `bc/resistanceOutlet.md` template diverges on the Stage A `sten00` case.\n"
        f"- **Reynolds number:** record it for every solve. Many baselines in this cohort sit above Re 300 and some\n"
        f"  above 400; steady laminar may not converge. Do NOT silently switch turbulence model — use the agreed\n"
        f"  pimpleFoam time-average fallback and report those cases separately.\n\n"
        f"## Return\nas-meshed radius along the centreline; area-averaged pressure AND through-plane flow "
        f"integral at every probe; per-outlet flow and pressure; throat Re; `checkMesh` status; wall-clock.\n\n"
        f"`bc_A.csv` / `bc_C_flows.csv` `mode` column: `resistance` imposes R; `closed` means a WALL "
        f"(zero conductance — the 0D model's own treatment of an outlet with no clean counterpart); "
        f"`prescribed` imposes the flow for the first Protocol C solve.\n")
    check_no_predictions(d)

    if withheld_dir is not None:
        if "cfd_handover" in withheld_dir.parts:
            raise SystemExit("refusing to write withheld predictions inside cfd_handover/ (review MUST 4)")
        wd = withheld_dir / d.name; wd.mkdir(parents=True, exist_ok=True)
        ffr2, Q2, info2, _, _ = t2.evaluate(C_B, r2)
        (wd / "expected_0D.json").write_text(json.dumps(dict(
            note="WITHHELD — do not send to the CFD machine until its results CSV is returned (§13)",
            measurement_tree_node=int(meas2),
            protocol_B=dict(C=C_B, ffr_measurement=float(ffr2[meas2]), converged=bool(info2["converged"])),
            clean=dict(C=C_clean, ffr_measurement=float(ffr0[meas_clean]))), indent=2))
    return dict(package=d.name, n_outlets=int(len(t2.leaves)), n_territories=int(len(terr2)),
                n_stations=int(len(st)), n_closed_outlets=int(sum(1 for x in mode_A if x == "closed")),
                sha256=sha256(d / "meta.json"))

# --------------------------------------------------------------------------------------------------- entry points
def m1_instance(here: Path):
    """Gate M1 tests the one risky step (CFD-ARM-SPEC §7), so the instance is chosen to EXERCISE it hardest, not to
    be typical: highest %DS available (the tightest throat any package will ask a mesher to resolve), a surviving
    deletable side branch (so the mask edit has something to delete), most outlets, lowest scan id to break ties."""
    sub = pd.read_csv(here / "protocol" / "CFD-SUBSET-FROZEN-2026-09-18.csv")
    cand = sub[(sub.ds_pct == sub.ds_pct.max()) & (sub.n_branch_ge_cut >= 1)]
    if cand.empty: cand = sub[sub.n_branch_ge_cut >= 1]
    return cand.sort_values(["n_outlets", "scan"], ascending=[False, True]).iloc[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--m1", action="store_true"); ap.add_argument("--subset", action="store_true")
    ap.add_argument("--instance", type=int, default=None); ap.add_argument("--error", default=BASELINE)
    ap.add_argument("--tier", default="real", choices=["real", "polyball"])
    ap.add_argument("--out", default=None); ap.add_argument("--with-expected", action="store_true")
    ap.add_argument("--withheld-dir", default=None)
    a = ap.parse_args(); root = data_root(a.root); here = Path(__file__).parent.parent
    wd = None
    if a.with_expected:
        wd = Path(a.withheld_dir) if a.withheld_dir else here / "results" / "cfd_withheld"

    if a.m1:
        row = m1_instance(here)
        out = Path(a.out) if a.out else here / "cfd_handover" / "packages" / "M1"
        print(f"Gate M1 instance: scan {row.scan} {row.side} {row.vessel} {row['loc']} "
              f"{row.L_mm:.0f}mm {row.ds_pct}%DS  (n_outlets={row.n_outlets}, branches>=cut={row.n_branch_ge_cut})")
        print("selected by: max %DS, has a deletable branch, most outlets, lowest scan id")
        man = []
        for etype in (CLEAN_NOLESION, BASELINE, "T1_missed_branch"):
            r = build(root, row, etype, "real", out, wd); man.append(r)
            print(f"  {r['package']}: {r['n_outlets']} outlets ({r['n_closed_outlets']} closed), "
                  f"{r['n_territories']} territories, {r['n_stations']} probes")
        # MUST 1: an instance KEY only. Never the CFD-SUBSET row, which carries ffr_discrete and base_discrete.
        (out / "MANIFEST.json").write_text(json.dumps(dict(
            gate="M1", spec="CFD-ARM-SPEC.md v0.2 §7", exported=str(date.today()),
            instance_key=dict(scan=int(row.scan), side=str(row.side), vessel=str(row.vessel), loc=str(row["loc"]),
                              L_mm=float(row.L_mm), ds_pct=int(row.ds_pct), n_outlets=int(row.n_outlets),
                              n_branch_ge_cut=float(row.n_branch_ge_cut)),
            packages=man), indent=2))
        check_no_predictions(out)
        print(f"\nwrote {len(man)} packages to {out}  (blinding check passed)")
        return

    coh = pd.read_csv(here / "protocol" / ("CFD-SUBSET-FROZEN-2026-09-18.csv" if a.subset
                                           else "COHORT-FROZEN-2026-09-18.csv"))
    outdir = Path(a.out) if a.out else here / "cfd_handover" / "packages"
    if a.subset:
        man = []
        for _, row in coh.iterrows():
            for etype in (BASELINE,) + tuple(ERROR_TYPES):
                try: man.append(build(root, row, etype, a.tier, outdir, wd))
                except SystemExit as e: man.append(dict(package=f"{row.scan}_{etype}", error=str(e)))
        (outdir / f"MANIFEST_{a.tier}.json").write_text(json.dumps(man, indent=2))
        print(f"{sum('error' not in x for x in man)}/{len(man)} packages written to {outdir}")
        return
    if a.instance is None: raise SystemExit("need --m1, --subset, or --instance <row index>")
    print(json.dumps(build(root, coh.iloc[a.instance], a.error, a.tier, outdir, wd), indent=2))

if __name__ == "__main__":
    main()
