"""Imaging-part figures for a finished solve (pairs the segmentation volume with the CFD result): generic for any package of the scan-14 / P5 family.
  cpr(pkg, mask, out_png, case=None, ...)  curved-planar reformation of the label volume along the lesion-vessel centreline (root -> farthest distal outlet through the throat node),
        two orthogonal CPR planes; with `case` (reconstructed fields) the CFD speed |U| and the section pressure profile are overlaid on the same plane.
  wall_pressure(case, out_png, ...)         3D render of the wall pressure (p / P_aorta), 3 views + throat close-up (pyvista off-screen).
Frame: package coordinates are mm LPS; the NIfTI affine is RAS: x and y are negated before inv(affine) (package README).
usage: viz_imaging.py cpr <package_dir> <mask.nii.gz> <out.png> [case_dir]    |    viz_imaging.py wall <case_dir> <package_dir> <out.png>"""
import sys, os, csv, json, collections
import numpy as np, nibabel as nib, pyvista as pv
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.ndimage import map_coordinates
pv.OFF_SCREEN = True
P_AORTA = 11998.98; RHO = 1060.0

def centreline(pkg):
    m = pv.read(f"{pkg}/centreline.vtp"); P = np.asarray(m.points); tn = np.asarray(m["tree_node"]); adj = collections.defaultdict(list); ln = m.lines; i = 0
    while i < len(ln): n = ln[i]; a, b = ln[i + 1:i + 3]; adj[int(a)].append(int(b)); adj[int(b)].append(int(a)); i += n + 1
    prev = {0: None}; q = [0]
    for u in q:
        for v in adj[u]:
            if v not in prev: prev[v] = u; q.append(v)
    thr = [r for r in csv.DictReader(open(f"{pkg}/probes.csv")) if r["kind"] == "throat"][0]; mea = [r for r in csv.DictReader(open(f"{pkg}/probes.csv")) if r["kind"] == "measurement"][0]
    idx = {int(t): k for k, t in enumerate(tn)}; kt = idx[int(thr["tree_node"])]; km = idx[int(mea["tree_node"])]
    def path(leaf):
        p = []; u = leaf
        while u is not None: p.append(u); u = prev[u]
        return p[::-1]
    outs = [idx[int(r["tree_node"])] for r in csv.DictReader(open(f"{pkg}/outlets.csv"))]
    cands = [path(o) for o in outs if kt in path(o) and km in path(o)] or [path(o) for o in outs if kt in path(o)]
    best = max(cands, key=lambda p: len(p)); pts = P[best]; s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    st = s[best.index(kt)]; sm = s[best.index(km)] if km in best else None
    return pts, s, st, sm, thr, mea

def resample(pts, s, step=0.25):
    q = np.arange(0, s[-1], step); Q = np.stack([np.interp(q, s, pts[:, k]) for k in range(3)], 1)
    from scipy.ndimage import gaussian_filter1d
    Qs = np.stack([gaussian_filter1d(Q[:, k], 2.0, mode="nearest") for k in range(3)], 1)
    T = np.gradient(Qs, axis=0); T /= np.linalg.norm(T, axis=1)[:, None]
    N = np.zeros_like(T); a = np.cross(T[0], [0, 0, 1.0]); a = a / np.linalg.norm(a) if np.linalg.norm(a) > 1e-6 else np.cross(T[0], [0, 1.0, 0]); N[0] = a
    for i in range(1, len(T)):                      # parallel transport of the normal
        n = N[i - 1] - np.dot(N[i - 1], T[i]) * T[i]; N[i] = n / np.linalg.norm(n)
    B = np.cross(T, N)
    return q, Qs, T, N, B

def cpr(pkg, mask, out, case=None, half_mm=4.0, du=0.1):
    pts, s, st, sm, thr, mea = centreline(pkg); q, Q, T, N, B = resample(pts, s)
    img = nib.load(mask); lab = np.asarray(img.dataobj) > 0; inv = np.linalg.inv(img.affine)
    off = np.arange(-half_mm, half_mm + du, du)
    fig, axs = plt.subplots(2 if case is None else 3, 1, figsize=(11, 4.2 if case is None else 6.4), constrained_layout=True, sharex=True)
    mesh = None
    if case is not None:
        open(f"{case}/case.foam", "a").close(); r = pv.OpenFOAMReader(f"{case}/case.foam"); r.set_active_time_value(r.time_values[-1]); mesh = r.read()["internalMesh"]
    for k, (V, lab_) in enumerate(((N, "plane 1 (normal direction)"), (B, "plane 2 (binormal direction)"))):
        X = Q[:, None, :] + off[None, :, None] * V[:, None, :]                       # (nq, noff, 3) mm LPS
        ijk = (inv @ np.c_[X.reshape(-1, 3) * np.array([-1.0, -1.0, 1.0]), np.ones(X.shape[0] * X.shape[1])].T)[:3]
        L = map_coordinates(lab.astype(np.uint8), ijk, order=0, mode="constant").reshape(X.shape[:2]).T
        ax = axs[k]; ax.imshow(L, extent=[q[0], q[-1], off[0], off[-1]], origin="lower", aspect="auto", cmap="gray", vmin=0, vmax=1.0, interpolation="nearest")
        if mesh is not None:
            smp = pv.PolyData(X.reshape(-1, 3) * 1e-3).sample(mesh); U = np.linalg.norm(smp.point_data["U"], axis=1).reshape(X.shape[:2]).T; ok = smp.point_data["vtkValidPointMask"].reshape(X.shape[:2]).T > 0
            Um = np.ma.masked_where(~ok, U); im = ax.imshow(Um, extent=[q[0], q[-1], off[0], off[-1]], origin="lower", aspect="auto", cmap="turbo", alpha=0.75, interpolation="bilinear", vmin=0, vmax=float(np.nanpercentile(U[ok], 99.5)) if ok.any() else 1)
        ax.axvline(st, color="r", ls=":", lw=1); ax.set_ylabel("offset (mm)", fontsize=8); ax.text(0.995, 0.93, lab_, transform=ax.transAxes, ha="right", va="top", fontsize=7, color="w")
        if sm is not None: ax.axvline(sm, color="c", ls="--", lw=1)
    if case is not None:
        fig.colorbar(im, ax=axs[:2], shrink=0.8, label="|U| (m/s)")
        ps = pv.PolyData(Q * 1e-3).sample(mesh); p = ps.point_data["p"] * RHO / P_AORTA; ok = ps.point_data["vtkValidPointMask"] > 0
        axs[2].plot(q[ok], p[ok], "k-", lw=1.2); axs[2].axvline(st, color="r", ls=":"); axs[2].set_ylabel("p / P_aorta on the axis"); axs[2].grid(alpha=0.3)
        if sm is not None: axs[2].axvline(sm, color="c", ls="--")
    axs[-1].set_xlabel("arc along the lesion vessel from the root (mm); red dotted: throat, cyan dashed: measurement probe")
    axs[0].set_title(os.path.basename(pkg.rstrip("/")) + ": curved-planar reformation of the segmentation (white = lumen label)" + ("" if case is None else " with the CFD speed"), fontsize=9, loc="left")
    fig.savefig(out, dpi=170); print("wrote", out)

def wall_pressure(case, pkg, out):
    open(f"{case}/case.foam", "a").close(); r = pv.OpenFOAMReader(f"{case}/case.foam"); r.set_active_time_value(r.time_values[-1])
    r.disable_all_patch_arrays(); r.enable_patch_array("patch/wall"); mb = r.read()                      # wall patch only (the internal mesh of a 6 M cell case is not needed for the wall render)
    wall = None
    for k in mb.keys():
        if isinstance(mb[k], pv.MultiBlock):
            for k2 in mb[k].keys():
                if k2.endswith("wall"): wall = mb[k][k2]
        elif k.endswith("wall"): wall = mb[k]
    if wall is None: raise SystemExit("no wall patch found: blocks " + str(list(mb.keys())))
    wall = wall.extract_surface(); wall = wall.cell_data_to_point_data() if "p" in wall.cell_data else wall; wall["pr"] = wall.point_data["p"] * RHO / P_AORTA
    pts, s, st, sm, thr, mea = centreline(pkg); c = np.array([float(thr[k]) for k in ("x", "y", "z")]) * 1e-3
    lo, hi = float(np.percentile(wall["pr"], 1)), float(np.percentile(wall["pr"], 99.5))
    pl = pv.Plotter(shape=(1, 4), off_screen=True, window_size=(2400, 700), border=False)
    views = [("front", (0, -1, 0)), ("side", (1, 0, 0)), ("top", (0, 0, 1))]
    for i, (nm, d) in enumerate(views):
        pl.subplot(0, i); pl.add_mesh(wall, scalars="pr", cmap="turbo", clim=(lo, hi), show_scalar_bar=(i == 0), scalar_bar_args=dict(title="wall p / P_aorta"), smooth_shading=True); pl.view_vector(d); pl.add_text(nm, font_size=9)
    pl.subplot(0, 3); cl = wall.clip_box(bounds=(c[0] - 3e-3, c[0] + 3e-3, c[1] - 3e-3, c[1] + 3e-3, c[2] - 3e-3, c[2] + 3e-3), invert=False)
    pl.add_mesh(cl, scalars="pr", cmap="turbo", clim=(lo, hi), show_scalar_bar=False, smooth_shading=True); pl.view_vector((1, 1, 1)); pl.add_text("throat close-up (6 mm box)", font_size=9)
    pl.screenshot(out); print("wrote", out)

if __name__ == "__main__":
    if sys.argv[1] == "cpr": cpr(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
    elif sys.argv[1] == "wall": wall_pressure(sys.argv[2], sys.argv[3], sys.argv[4])
