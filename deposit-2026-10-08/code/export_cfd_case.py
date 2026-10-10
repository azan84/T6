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

BED = "discrete"
STATION_GRID_MM, STATION_CAP, STATION_MERGE_MM = 5.0, 40, 1.0
BIF_OFFSET_MM = None
CLEAN_NOLESION, BASELINE = "clean_nolesion", "baseline"
FRAME = ("mm, LPS. The ImageCAS-X NIfTI affine is RAS: negate x and y before applying inv(affine) to reach voxel "
         "indices.")

PROTECT_R, CONNECTIVITY = 1.10, 1

DELETION_RULE = (
    "Protect-then-flood-fill, applied once to the union of everything being removed (sub-cut vessel from the "
    "truncation step and, if present, the missed branch). (1) protect = every voxel within 1.10*r_mm of any point in "
    "retained_points_mm; (2) candidates = mask AND NOT protect; (3) delete the 6-connected components of candidates "
    "that contain any point of the deletion set; (4) re-run marching cubes.")

REFERENCE_IMPL = '''\
import numpy as np, nibabel as nib, json
from scipy.ndimage import label, generate_binary_structure
img = nib.load(MASK_NII); mask = np.asarray(img.dataobj) > 0
inv = np.linalg.inv(img.affine); sp = np.array(img.header.get_zooms()[:3])
def to_ijk(pts):
    ras = np.asarray([[p["x"], p["y"], p["z"]] for p in pts]) * np.array([-1.0, -1.0, 1.0])
    return (inv @ np.c_[ras, np.ones(len(ras))].T)[:3].T
def ball(c_ijk, r_mm):
    rad = np.ceil(r_mm / sp).astype(int); c = np.round(c_ijk).astype(int)
    sl = tuple(slice(max(c[d]-rad[d], 0), min(c[d]+rad[d]+1, mask.shape[d])) for d in range(3))
    g = np.mgrid[sl]; return sl, sum(((g[d]-c_ijk[d])*sp[d])**2 for d in range(3)) <= r_mm**2
e = json.load(open("mask_edit.json"))
protect = np.zeros_like(mask)
for p, q in zip(e["retained_points_mm"], to_ijk(e["retained_points_mm"])):
    sl, b = ball(q, 1.10 * p["r_mm"]); protect[sl] |= b
kill_pts = list(e["sub_cut_points_mm"]) + list(e.get("mask_edit", {}).get("deleted_points_mm", []))
lab, _ = label(mask & ~protect, structure=generate_binary_structure(3, 1))
kill = {lab[tuple(np.clip(np.round(q).astype(int), 0, np.array(mask.shape)-1))] for q in to_ijk(kill_pts)}
out = mask & ~np.isin(lab, [k for k in kill if k > 0])
nib.save(nib.Nifti1Image(out.astype(np.uint8), img.affine), "mask_edited.nii.gz")
'''

TRUNCATION_RULE = (
    "The 0D model is truncated at r_ref < 0.60 mm and the 3D model is truncated at the same place. (1) Remove the "
    "sub-cut vessel that the active centreline does not cover: sub_cut_points_mm is the deletion set, "
    "retained_points_mm is the protect set, and the rule is deletion_rule, run once over the union of both deletion "
    "sets, before marching cubes. (2) Clip the lumen at every outlet plane in outlets.csv (position + outward "
    "normal), discard the distal component, and add flow extensions to the clipped face.")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def data_root(arg: str) -> Path:
    p = Path(arg).expanduser()
    if (p / "centerlines").is_dir(): return p
    for c in sorted(p.glob("*")):
        if c.is_dir() and (c / "centerlines").is_dir(): return c
    raise SystemExit(f"no centerlines/ under {p}")

def tangent(t: Tree, v: int, n_back: int = 3) -> np.ndarray:
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
    tokens = ("ffr", "base_discrete", "min_ffr", "lesion_ffr")
    for p in sorted(d.rglob("*")):
        if not p.is_file(): continue
        if p.suffix == ".vtp":

            import pyvista as pv
            mesh = pv.read(p)
            names = list(mesh.point_data.keys()) + list(mesh.cell_data.keys()) + list(mesh.field_data.keys())
            hits = [n for n in names if any(t in n.lower() for t in tokens)]
            if hits:
                raise SystemExit(f"blinding check failed: {p.relative_to(d)} array name(s) {hits}")
            continue
        blob = p.read_bytes().lower()
        for token in tokens:
            if token.encode() in blob:
                raise SystemExit(f"blinding check failed: {p.relative_to(d)} contains {token!r}")

def active_polydata(t: Tree, r_target: np.ndarray, scale_vs_clean: np.ndarray):
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
    m.point_data["tree_node"] = act.astype(np.int32)
    m.point_data["resolved"] = t.resolved[act].astype(np.int8)
    return m

def stations(t: Tree, path, s_arc, c, L, meas_node):
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

    scale = np.ones(len(t2.parent))
    ok = m >= 0
    scale[ok] = r2[ok] / np.maximum(t.r[m[ok]], 1e-12)

    ffr0, Q0, info0, _, _ = t.evaluate(C_clean, r_clean)
    q0_all = bed_flow(t, C_clean, ffr0)
    terr2 = territories(t2)
    terr_of = {int(v): j for j, sub in enumerate(terr2) for v in sub}

    rows = []
    for v in t2.leaves:
        v = int(v); n = tangent(t2, v)
        rows.append(dict(outlet_id=f"out_{v}", tree_node=v,
                         x=t2.xyz[v][0] * 1e3, y=t2.xyz[v][1] * 1e3, z=t2.xyz[v][2] * 1e3,
                         normal_x=n[0], normal_y=n[1], normal_z=n[2],
                         r_ref_mm=t2.r_ref[v] * 1e3, r_mm=t2.r[v] * 1e3, territory_id=terr_of.get(v, -1)))
    out = pd.DataFrame(rows)
    w_clean = np.where(m >= 0, t.w[np.maximum(m, 0)], 0.0)

    mode_A = ["resistance" if w_clean[r.tree_node] > 0 else "closed" for r in out.itertuples()]
    R_A = np.array([C_clean / w_clean[r.tree_node] if w_clean[r.tree_node] > 0 else 0.0 for r in out.itertuples()])
    t2._C.clear(); C_B = t2.calibrate(t2.demand("murray", 1.0))
    R_B = np.array([C_B / t2.w[r.tree_node] for r in out.itertuples()])

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

    mode_C = ["prescribed" if q > 0 else "closed" for q in q_tgt]
    for name, arr in (("R_A", R_A), ("R_B", R_B), ("q_tgt", q_tgt)):
        if not np.isfinite(arr).all():
            raise SystemExit(f"non-finite value in {name}")

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

    inactive = np.where(~t2.active)[0]
    pts = lambda idx: [dict(x=float(t2.xyz[i][0] * 1e3), y=float(t2.xyz[i][1] * 1e3),
                            z=float(t2.xyz[i][2] * 1e3), r_mm=float(t2.r[i] * 1e3)) for i in idx]
    edit = dict(frame=FRAME, tier=tier, error_type=etype,
                surface_rule=("scale each surface vertex's distance to its NEAREST centreline point by that point's "
                              "radial_scale (centreline.vtp point array); radial_scale == 1 means unchanged"),
                truncation_rule=TRUNCATION_RULE, deletion_rule=DELETION_RULE,
                reference_implementation=REFERENCE_IMPL,

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
                         note="the node at which the 0D model reports FFR"),
        protocol_C=dict(
            variant="per-outlet prescribed flow, then R_i = (p_i - P_v)/Q_i; exactly determined, one target per outlet",
            target_definition="each territory's target is the clean tree's full outflow, including the share of any "
                              "branch the error deleted, distributed across surviving outlets in proportion to their "
                              "clean flow (see territories.csv)."),
        provenance=dict(centreline_vtk_sha256=sha256(vtk_p), mask_nii_sha256=sha256(nii_p),
                        exporter_sha256=sha256(Path(__file__)), exporter=Path(__file__).name,
                        exported=str(date.today())),
        blinding="0D predictions for the corrupted geometry are not included in the package.")
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
        f"   `r_target_mm` and reject the case if it differs by more than 1 %**.\n"
        f"6. Flow extensions, mesh, solve.\n\n"
        f"## Solver settings\n"
        f"- Resistance-outlet under-relaxation: alpha < 2 / (1 + R_outlet/R_epicardial); start at alpha = 0.05.\n"
        f"- Record the Reynolds number for every solve.\n\n"
        f"## Return\nas-meshed radius along the centreline; area-averaged pressure AND through-plane flow "
        f"integral at every probe; per-outlet flow and pressure; throat Re; `checkMesh` status; wall-clock.\n\n"
        f"`bc_A.csv` / `bc_C_flows.csv` `mode` column: `resistance` imposes R; `closed` means a WALL "
        f"(zero conductance — the 0D model's own treatment of an outlet with no clean counterpart); "
        f"`prescribed` imposes the flow for the first Protocol C solve.\n")
    check_no_predictions(d)

    if withheld_dir is not None:
        if "cfd_handover" in withheld_dir.parts:
            raise SystemExit("withheld predictions must not be written inside the handover folder")
        wd = withheld_dir / d.name; wd.mkdir(parents=True, exist_ok=True)
        ffr2, Q2, info2, _, _ = t2.evaluate(C_B, r2)
        (wd / "expected_0D.json").write_text(json.dumps(dict(
            note="0D predictions, withheld from the CFD side until its results are returned",
            measurement_tree_node=int(meas2),
            protocol_B=dict(C=C_B, ffr_measurement=float(ffr2[meas2]), converged=bool(info2["converged"])),
            clean=dict(C=C_clean, ffr_measurement=float(ffr0[meas_clean]))), indent=2))
    return dict(package=d.name, n_outlets=int(len(t2.leaves)), n_territories=int(len(terr2)),
                n_stations=int(len(st)), n_closed_outlets=int(sum(1 for x in mode_A if x == "closed")),
                sha256=sha256(d / "meta.json"))

def m1_instance(here: Path):
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

        (out / "MANIFEST.json").write_text(json.dumps(dict(
            gate="M1", exported=str(date.today()),
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
