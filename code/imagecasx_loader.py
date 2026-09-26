"""
imagecasx_loader.py — build zerod_ffr.Tree objects from ImageCAS-X centreline .vtk files.

Verified against the released data (2026-09-18, case 878):
  centerlines/<id>.coronary_{left,right}_centerline.vtk   PolyData polylines, NO radius array
      point_data: segment_label (int 1..14), segment_name (str), branch_points, end_points, start_points (0/1)
      coordinates are LPS (ITK/VTK convention)
  segmentations/<id>.coronary.nii.gz   14-class voxel labels, NIfTI affine is RAS  ->  negate x,y of the
      centreline before applying inv(affine)
  surfaces/<id>.coronary_surface.vtk
  Descriptors.xlsx: Scan ID | Image Quality (0 = excluded, 1..4) | Dominance (R/L/Co) | Disease (yes/no)

Radius: Euclidean distance transform of the lumen mask (mm, anisotropic spacing) sampled at the centreline,
minus half a voxel (EDT measures to the nearest BACKGROUND voxel centre, which overshoots the wall), then lightly
smoothed along each segment — r^4 in Poiseuille amplifies voxel-quantisation noise otherwise.

Topology: built on a point GRAPH (edges = consecutive polyline vertices, coincident points merged), so it is
indifferent to whether the file stores branch-to-branch pieces or overlapping root-to-tip paths.
"""
from __future__ import annotations
import sys
from functools import lru_cache
from pathlib import Path
import numpy as np
import networkx as nx
import pyvista as pv

sys.path.insert(0, str(Path(__file__).parent))
from zerod_ffr import Segment, Tree

def inspect(vtk_path: str):
    m = pv.read(vtk_path)
    print(f"{vtk_path}\n  type={type(m).__name__}  n_points={m.n_points}  n_lines={m.n_lines}")
    print(f"  bounds: {np.round(m.bounds,2)}")
    for k in m.point_data.keys():
        a = np.asarray(m.point_data[k]); u = np.unique(a)
        print(f"  point_data[{k!r}] dtype={a.dtype} uniq={u[:12]}{'...' if len(u)>12 else ''}")
    pls = _polylines(m); tot = sum(len(p) for p in pls)
    ids = np.concatenate(pls)
    print(f"  polylines={len(pls)} sum_len={tot} unique_point_ids={len(np.unique(ids))} "
          f"-> {'OVERLAPPING paths' if tot > 1.15*len(np.unique(ids)) else 'disjoint pieces'}")

def _polylines(m: pv.PolyData) -> list[np.ndarray]:
    L = np.asarray(m.lines); out = []; i = 0
    while i < len(L):
        n = int(L[i]); out.append(L[i + 1:i + 1 + n].astype(int)); i += n + 1
    return out

@lru_cache(maxsize=2)
def _edt(mask_path: str):
    """Cropped anisotropic EDT of the lumen mask. Returns (edt_mm, offset_ijk, inv_affine, min_spacing)."""
    import nibabel as nib
    from scipy.ndimage import distance_transform_edt
    img = nib.load(mask_path)
    lab = np.asarray(img.dataobj) > 0
    sp = tuple(float(z) for z in img.header.get_zooms()[:3])
    nz = np.argwhere(lab)
    lo = np.maximum(nz.min(0) - 4, 0); hi = np.minimum(nz.max(0) + 5, lab.shape)
    crop = lab[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    edt = distance_transform_edt(crop, sampling=sp).astype(np.float32)
    return edt, lo, np.linalg.inv(img.affine), min(sp)

def radius_from_mask(mask_path: str, pts_lps_mm: np.ndarray):
    from scipy.ndimage import map_coordinates
    edt, lo, inv, hmin = _edt(mask_path)
    ras = pts_lps_mm * np.array([-1.0, -1.0, 1.0])                      # LPS -> RAS
    ijk = (inv @ np.c_[ras, np.ones(len(ras))].T)[:3] - lo[:, None]
    # the EDT volume is float32 to save memory; promote the SAMPLED radii to float64 so the solver is uniformly
    # double precision (a float32 radius array silently rounds exact targets such as r_fit*(1-DS) by ~3e-8)
    r = map_coordinates(edt, ijk, order=1, mode="nearest").astype(np.float64)
    inside = r > 0
    # NO half-voxel correction: verified 2026-09-18 that raw EDT-at-point agrees with the independent
    # distance-to-surface-mesh measure to ~0.03 mm (0.73 vs 0.74, 0.87 vs 0.84, 0.77 vs 0.76 mm medians).
    # Subtracting 0.5 voxel would shrink a 0.6 mm vessel by 27% and inflate Poiseuille resistance 3.5x.
    return np.maximum(r, 0.15), inside

def _smooth(r: np.ndarray, sigma_pts: float = 2.0) -> np.ndarray:
    if len(r) < 5:
        return r
    from scipy.ndimage import gaussian_filter1d
    return gaussian_filter1d(r, sigma_pts, mode="nearest")

def load_tree(vtk_path: str, mask_path: str, name: str = "", verbose: bool = False, bed: str = "leaky") -> Tree:
    m = pv.read(vtk_path)
    pts = np.asarray(m.points, dtype=float)
    seg_name = np.asarray(m.point_data["segment_name"]).astype(str)
    start = np.asarray(m.point_data["start_points"]).astype(bool)
    r_mm, inside = radius_from_mask(mask_path, pts)

    # --- point graph with coincident points merged
    keys = {}; canon = np.empty(len(pts), int)
    for i, p in enumerate(pts):
        canon[i] = keys.setdefault(tuple(np.round(p, 2)), i)
    G = nx.Graph()
    for pl in _polylines(m):
        c = canon[pl]
        for a, b in zip(c[:-1], c[1:]):
            if a != b:
                G.add_edge(int(a), int(b))
    if G.number_of_nodes() == 0:
        raise ValueError("empty centreline")
    comp = max(nx.connected_components(G), key=len)
    if len(comp) < G.number_of_nodes() and verbose:
        print(f"  note: kept largest component {len(comp)}/{G.number_of_nodes()} points")
    G = G.subgraph(comp).copy()
    # --- root: flagged start point, else the widest degree-1 point (the ostium)
    cand = [int(canon[i]) for i in np.where(start)[0] if int(canon[i]) in G]
    if not cand:
        cand = [n for n in G if G.degree(n) == 1]
    root = max(cand, key=lambda n: r_mm[n])
    T = nx.bfs_tree(G, root)                                            # directed, breaks any cycle
    # --- segments: chains between root/junction and next junction/leaf
    segs = []; seg_of_endnode = {}
    stack = [(root, None)]
    while stack:
        node, parent_sid = stack.pop()
        for child in T.successors(node):
            chain = [node, child]
            while T.out_degree(chain[-1]) == 1:
                chain.append(next(T.successors(chain[-1])))
            idx = np.array(chain)
            names, counts = np.unique(seg_name[idx[1:]], return_counts=True)
            sid = len(segs)
            rs = _smooth(r_mm[idx])
            if parent_sid is None:
                # OSTIAL END-CAP ARTEFACT: the mask stops at the aorta, so the EDT treats that cut face as
                # background and under-reads the radius near the inlet (LM read 1.11 mm at the ostium rising to
                # 1.45 mm downstream — anatomically backwards). Hold the first ~4 mm at the value reached there.
                arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(pts[idx], axis=0), axis=1))])
                j = int(np.searchsorted(arc, 4.0))
                if 0 < j < len(rs):
                    rs[:j] = np.maximum(rs[:j], rs[j])
            segs.append(Segment(sid, parent_sid, pts[idx] * 1e-3, rs * 1e-3, str(names[np.argmax(counts)])))
            stack.append((chain[-1], sid))
    if verbose:
        tot_len = sum(np.linalg.norm(np.diff(s.pts, axis=0), axis=1).sum() for s in segs) * 1e3
        print(f"  {name}: {len(segs)} segments, {tot_len:.0f} mm, points-inside-mask={inside.mean():.1%}, "
              f"radius mm min/med/max = {r_mm.min():.2f}/{np.median(r_mm):.2f}/{r_mm.max():.2f}")
    tree = Tree(segs, name, bed=bed)
    tree.segments = segs                     # kept for resolution-independence checks (severity_sweep V8)
    return tree

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--inspect":
        for f in sys.argv[2:]:
            inspect(f)
    elif len(sys.argv) >= 4 and sys.argv[1] == "--check":
        root = Path(sys.argv[2])
        for sid in sys.argv[3:]:
            for side in ("left", "right"):
                v = root / "centerlines" / f"{sid}.coronary_{side}_centerline.vtk"
                k = root / "segmentations" / f"{sid}.coronary.nii.gz"
                t = load_tree(str(v), str(k), f"{sid}_{side}", verbose=True)
                o = t.ffr(mode="murray")
                print(f"    r_in={o['r_in_mm']:.2f}mm  demand={o['Q_demand_mls']:.2f}  inflow={o['Q_in_mls']:.2f} mL/s  "
                      f"minFFR(main,resolved)={o['min_ffr_main']:.3f}  lesions={o['n_lesions']}  "
                      f"tightest={o['lesion_label']} {o['lesion_ds_pct']:.0f}%DS -> FFR20={o['lesion_ffr20']:.3f}")
                for r in t.segment_table():
                    print(f"      seg{r['seg']:<2} {r['label']:<6} L={r['len_mm']:6.1f} r {r['r_prox']:.2f}->{r['r_dist']:.2f}mm "
                          f"maxDS={r['maxDS_resolved']:5.1f}% Q {r['Q_prox']:.2f}->{r['Q_dist']:.2f} FFRdist={r['ffr_dist']:.3f} les={r['lesions']}")
    else:
        print("usage: --inspect <vtk>... | --check <data_root> <scan_id>...")
