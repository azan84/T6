"""Localise strict-checkMesh failed sets relative to the LAD tube s=18.5-32 mm (3 mm around the axis). Sets are searched in <mesh>/postProcessing/constant/<set>/<set>.vtp
or <mesh>/failed_sets/postProcessing/constant/... An EMPTY search is an error whenever the strict log reports failures (it must never count as a pass).
usage: mesh_failed_sets_general.py <mesh_dir> ...   -> per-set positions in <mesh_dir>/failed_sets_localisation.json; exit 1 if any flagged point lies inside the tube (informational for the T25 levels, see the design)"""
import sys, os, glob, json, re
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pyvista as pv
import build_lesion80_surface as G
from outlets_837 import build_tree
T = build_tree(); T.ffr(mode="murray"); dfm = G.Deformer(T); fr = dfm.fr
thr = fr["c"][np.argmin(np.abs(fr["s"] - G.S_C))]
lab = {sg.sid: sg.label for sg in T.segments}
inside_any = False
for mdir in sys.argv[1:]:
    strict = open(f"{mdir}/log.checkMesh.strict").read() if os.path.exists(f"{mdir}/log.checkMesh.strict") else ""
    m_ = re.search(r"Failed (\d+) mesh checks", strict); nfail = int(m_.group(1)) if m_ else 0
    files = sorted(glob.glob(f"{mdir}/postProcessing/constant/*/*.vtp") + glob.glob(f"{mdir}/failed_sets/postProcessing/constant/*/*.vtp"))
    if nfail > 0 and not files:
        raise SystemExit(f"{mdir}: strict checkMesh reports {nfail} failed checks but no failed-set VTK found - an empty search is not a pass")
    res = {}
    for f in files:
        name = os.path.basename(f)[:-4]; m = pv.read(f)
        pts = np.asarray(m.points) * 1e3; d, i, sid = dfm.project(pts); s = fr["s"][i]
        inside = (s >= G.PR["TUBE_LO"]) & (s <= G.PR["TUBE_HI"]) & (d < 3.0)
        ctr = np.asarray(m.cell_centers().points) * 1e3; dt = np.linalg.norm(ctr - thr, axis=1)
        res[name] = dict(n_polygons=int(m.n_cells), n_points=int(len(pts)), min_dist_to_throat_mm=float(dt.min()), n_points_inside_tube=int(inside.sum()),
                         positions=[dict(x_mm=[round(float(v), 3) for v in pts[k]], arc_s_mm=round(float(s[k]), 2), axis_dist_mm=round(float(d[k]), 2), branch=str(lab.get(int(sid[k]), sid[k])), inside_tube=bool(inside[k])) for k in range(len(pts))],
                         arc_histogram_inside_tube_1mm_bins=np.histogram(s[inside], bins=np.arange(G.PR["TUBE_LO"] - 0.5, G.PR["TUBE_HI"] + 1.0, 1.0))[0].tolist())
        inside_any |= bool(inside.any())
        print(f"{os.path.basename(mdir.rstrip('/'))}: {name}: {m.n_cells} polygons, nearest {dt.min():.2f} mm, points inside the tube: {int(inside.sum())}, arc histogram {res[name]['arc_histogram_inside_tube_1mm_bins']}")
    json.dump(dict(strict_failed_checks=nfail, sets=res), open(f"{mdir}/failed_sets_localisation.json", "w"), indent=1)
print("flagged entities inside the lesion tube: YES (see per-set counts)" if inside_any else "no flagged entity inside the lesion tube")
sys.exit(1 if inside_any else 0)
