"""verify_exporter.py — package-level verification of export_cfd_case.py v0.2 (MUST 1, 2, 4, 6, 7, 8 + new items).
usage: verify_exporter.py <m1_dir> <extra14_dir> <extra102_dir> <withheld_dir>
"""
import sys, json, re, shutil, tempfile
from pathlib import Path
import numpy as np, pandas as pd, pyvista as pv
HERE = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(HERE / "code"))
import export_cfd_case as X
from severity_sweep import load

m1, ex14, ex102, wh = [Path(a) for a in sys.argv[1:5]]
pk = {}
for d in (m1, ex14, ex102):
    for p in sorted(d.iterdir()):
        if p.is_dir(): pk[p.name] = p
names = list(pk)
print("packages:", *names, sep="\n  ")

def section(t): print(f"\n{'='*100}\n{t}\n{'='*100}")

# ------------------------------------------------------------------------------------------------- MUST 1
section("MUST 1 — no prediction in any package file (substring grep, ALL files incl. vtp)")
hits = []
for n, d in pk.items():
    for p in sorted(d.rglob("*")):
        if not p.is_file(): continue
        txt = p.read_text(errors="ignore")
        for m in re.finditer(r"(?i)ffr|base_discrete|base_ffr", txt):
            ctx = txt[max(0, m.start()-40): m.end()+40].replace("\n", " ")
            hits.append((n, p.name, ctx))
for h in hits: print("  HIT", h)
print(f"substring hits: {len(hits)}")
print("MANIFEST keys:", list(json.loads((m1 / "MANIFEST.json").read_text()).keys()))
print("vtp point arrays:", pv.read(str(pk[names[0]] / "centreline.vtp")).point_data.keys())
# bypass tests on the shipped regex
bad = re.compile(r"\b(ffr|FFR|base_discrete|base_ffr|min_ffr|lesion_ffr)\b")
for s in ["ffr_discrete: 0.76", '"ffr_measurement": 0.86', "FFR_meas,0.76", "ffr,0.76", "ffr2 0.76", "Ffr: 0.76", "dFFR 0.1"]:
    print(f"  regex catches {s!r:32}: {bool(bad.search(s))}")
# would the check catch the withheld file if it were dropped into a package?
tmp = Path(tempfile.mkdtemp()); shutil.copytree(pk[names[0]], tmp / "p")
shutil.copy(next(wh.rglob("expected_0D.json")), tmp / "p" / "expected_0D.json")
try:
    X.check_no_predictions(tmp / "p"); print("  check_no_predictions on a package containing expected_0D.json: PASSED (i.e. NOT caught)")
except SystemExit as e:
    print("  check_no_predictions on a package containing expected_0D.json: caught ->", str(e)[:90])
(tmp / "p" / "expected_0D.json").unlink()
(tmp / "p" / "note.csv").write_text("scan,ffr_discrete\n14,0.7612\n")
try:
    X.check_no_predictions(tmp / "p"); print("  check_no_predictions on a CSV with column ffr_discrete: PASSED (i.e. NOT caught)")
except SystemExit as e:
    print("  check_no_predictions on a CSV with column ffr_discrete: caught")
(tmp / "p" / "note.csv").unlink()
m = pv.read(str(tmp / "p" / "centreline.vtp")); m.point_data["ffr"] = np.zeros(m.n_points); m.save(str(tmp / "p" / "centreline.vtp"))
try:
    X.check_no_predictions(tmp / "p"); print("  check_no_predictions on a vtp with a point array named 'ffr': PASSED (i.e. NOT caught)")
except SystemExit as e:
    print("  check_no_predictions on a vtp with a point array named 'ffr': caught")
shutil.rmtree(tmp)
print("withheld files:", [str(p.relative_to(wh)) for p in wh.rglob("*.json")])
print("withheld T1 content keys:", json.loads(next(p for p in wh.rglob("*.json") if "T1" in str(p)).read_text()).keys())

# ------------------------------------------------------------------------------------------------- MUST 2
section("MUST 2 — frame stated")
for n in names[:1]:
    d = pk[n]
    for f in ("meta.json", "inlet.json", "mask_edit.json"):
        print(f"  {f}: frame = {json.loads((d/f).read_text()).get('frame','MISSING')[:40]}...")
    print(f"  README mentions LPS: {'LPS' in (d/'README.md').read_text()}")
    for f in ("outlets.csv", "probes.csv"):
        print(f"  {f} header: {(d/f).read_text().splitlines()[0][:80]}  (frame in file: {'LPS' in (d/f).read_text()})")

# ------------------------------------------------------------------------------------------------- MUST 6
section("MUST 6 — NaN and closed")
for n, d in pk.items():
    nan = {}
    for f in ("bc_A.csv", "bc_B.csv", "bc_C_flows.csv", "outlets.csv", "territories.csv", "probes.csv"):
        df = pd.read_csv(d / f); k = int(df.isna().sum().sum())
        if k: nan[f] = {c: int(v) for c, v in df.isna().sum().items() if v}
    a = pd.read_csv(d / "bc_A.csv"); c = pd.read_csv(d / "bc_C_flows.csv")
    closed = a[a["mode"] == "closed"]
    cz = c.set_index("outlet_id").loc[closed.outlet_id]
    print(f"  {n:<55} NaN: {nan or 'none in BC/outlet/territory files'}  | bc_A modes {a['mode'].value_counts().to_dict()}"
          f"  bc_C modes {c['mode'].value_counts().to_dict()}  closed R_SI={closed.R_SI.tolist()}"
          f"  -> same outlets in bc_C: mode {cz['mode'].tolist()} Q_target_mls {cz.Q_target_mls.tolist()}")

# ------------------------------------------------------------------------------------------------- MUST 7
section("MUST 7 — radial_scale / r_target reproduce the 0D lesioned radius")
clean = pv.read(str(pk[[n for n in names if "clean_nolesion" in n][0]] / "centreline.vtp"))
ckey = {tuple(np.round(p, 6)): r for p, r in zip(clean.points, clean.point_data["r_source_mm"])}
print(f"  clean_nolesion: radial_scale all == 1: {np.allclose(clean.point_data['radial_scale'], 1)}; "
      f"r_target == r_source: {np.allclose(clean.point_data['r_target_mm'], clean.point_data['r_source_mm'])}")
for n, d in pk.items():
    v = pv.read(str(d / "centreline.vtp")); pdata = v.point_data
    misr_ok = np.allclose(pdata["MaximumInscribedSphereRadius"], pdata["r_target_mm"])
    r_orig = np.array([ckey.get(tuple(np.round(p, 6)), np.nan) for p in v.points])
    ok = np.isfinite(r_orig)
    if not ok.any():                       # scan-102 packages have no clean_nolesion twin here
        print(f"  {n:<55} MISR==r_target {misr_ok}; (no clean twin exported for this scan — scale check skipped)"); continue
    recon = pdata["radial_scale"][ok] * r_orig[ok]
    err = np.abs(recon - pdata["r_target_mm"][ok]).max()
    src_vs_clean = np.abs(pdata["r_source_mm"][ok] - r_orig[ok]).max()
    ed = json.loads((d / "mask_edit.json").read_text())
    th = ""
    if ed["lesion"]:
        tab = pd.DataFrame(ed["lesion"]["table"]); k = tab.r_target_mm.idxmin()
        expect = tab.r_fit_mm[k] * (1 - ed["lesion"]["ds_pct"] / 100)
        th = (f"throat: min r_target {tab.r_target_mm.min():.4f} mm at s={tab.s_mm[k]:.2f} (c={ed['lesion']['centre_mm']:.2f}, "
              f"L={ed['lesion']['length_mm']:.2f}); r_fit(1-ds)={expect:.4f}; min radial_scale in vtp {pdata['radial_scale'].min():.4f}")
    print(f"  {n:<55} MISR==r_target {misr_ok}; unmatched pts {(~ok).sum()}; max|scale*r_clean - r_target| = {err:.2e} mm; "
          f"max|r_source - r_clean| = {src_vs_clean:.3f} mm\n      {th}")
    if "T4" in n:
        print(f"      T4 taper block: {ed.get('taper')}; radial_scale quantiles {np.quantile(pdata['radial_scale'],[0,.25,.5,.75,1]).round(4)}")
        print(f"      r_source_mm equals CLEAN radius: {src_vs_clean < 1e-9}  (docstring says r_source keeps the unedited value)")

# ------------------------------------------------------------------------------------------------- MUST 8 + territories
section("MUST 8 / territories.csv arithmetic")
for n, d in pk.items():
    tr = pd.read_csv(d / "territories.csv"); c = pd.read_csv(d / "bc_C_flows.csv"); o = pd.read_csv(d / "outlets.csv")
    meta = json.loads((d / "meta.json").read_text())
    per_t = c[c["mode"] == "prescribed"].groupby("territory_id").Q_target_mls.sum()
    surv_ok = np.allclose(tr.set_index("territory_id").Q_clean_surviving_mls, per_t.reindex(tr.territory_id).fillna(0).values)
    print(f"  {n:<55} n_terr {len(tr)} sum n_outlets {tr.n_outlets.sum()} vs n_outlets {len(o)} | "
          f"Q_surv {tr.Q_clean_surviving_mls.round(4).tolist()} Q_full {tr.Q_clean_full_territory_mls.round(4).tolist()} | "
          f"Q_surv == sum(bc_C per territory): {surv_ok} | sum Q_full {tr.Q_clean_full_territory_mls.sum():.4f} | "
          f"protocol_C in meta: {'protocol_C' in meta}")

# ------------------------------------------------------------------------------------------------- probes.csv
section("probes.csv — inlet/outlet rows, bifurcation stations, tangents, measurement")
for n, d in pk.items():
    pr = pd.read_csv(d / "probes.csv"); o = pd.read_csv(d / "outlets.csv"); inl = json.loads((d / "inlet.json").read_text())
    meta = json.loads((d / "meta.json").read_text())
    kinds = pr.kind.value_counts().to_dict()
    inrow = pr[pr.kind == "inlet"].iloc[0]
    outs = pr[pr.kind == "outlet"].set_index("probe_id"); oo = o.set_index("outlet_id")
    out_match = np.allclose(outs[["x", "y", "z", "normal_x", "normal_y", "normal_z"]].values,
                            oo.loc[outs.index, ["x", "y", "z", "normal_x", "normal_y", "normal_z"]].values)
    meas = pr[pr.kind == "measurement"]
    print(f"  {n}\n    kinds {kinds}  total {len(pr)}")
    print(f"    inlet row: node {inrow.tree_node} normal ({inrow.normal_x:.3f},{inrow.normal_y:.3f},{inrow.normal_z:.3f})  "
          f"inlet.json normal {np.round(inl['inlet']['normal'],3).tolist()}  r_ref {inrow.r_ref_mm:.3f}")
    print(f"    outlet rows == outlets.csv (pos+normal): {out_match}")
    print(f"    measurement station: {meas[['s_mm','s_node_mm','tree_node']].values.tolist()}  meta.measurement {meta['measurement']['tree_node'], round(meta['measurement']['s_mm'],2)}")
    st = pr[pr.kind.isin(["grid", "lesion_prox", "throat", "lesion_dist", "measurement", "bif_prox", "bif_dist"])]
    print(f"    s_node_mm monotone: {np.all(np.diff(st.s_node_mm.values) > 0)}; min spacing {np.diff(st.s_node_mm.values).min():.3f} mm; "
          f"|s_mm - s_node_mm| max {np.abs(st.s_mm - st.s_node_mm).max():.3f} mm")

# bifurcation stations: check against the tree
scan_of = lambda n: int(n.split("_")[0]); side_of = lambda n: n.split("_")[1]
for n in [x for x in names if "baseline" in x or "T1" in x or "T4" in x]:
    d = pk[n]; pr = pd.read_csv(d / "probes.csv"); t = load(HERE.parent / "x", 0, "left") if False else None
    v = pv.read(str(d / "centreline.vtp"))
    bif = pr[pr.kind.isin(["bif_prox", "bif_dist"])]
    print(f"  {n}: bif stations {len(bif)} at s_node {bif.s_node_mm.round(2).tolist()} kinds {bif.kind.tolist()} r_ref {bif.r_ref_mm.round(3).tolist()}")

# tangents: compare shipped normals to the last single edge
section("tangents (outlets): cos(shipped normal, last edge)")
import severity_sweep as ss
root = Path.home() / "Datasets" / "imagecas-x" / "ImageCAS-X_dataset"
for n in [x for x in names if "baseline" in x and x.startswith("14_")]:
    d = pk[n]; o = pd.read_csv(d / "outlets.csv"); t = load(root, 14, "left", "discrete")
    for r in o.itertuples():
        v = int(r.tree_node); p = int(t.parent[v]); e = t.xyz[v] - t.xyz[p]; e /= np.linalg.norm(e)
        nn = np.array([r.normal_x, r.normal_y, r.normal_z])
        print(f"    {r.outlet_id}: |n|={np.linalg.norm(nn):.6f} cos(last edge)={float(e@nn):.3f}  last edge {np.linalg.norm(t.xyz[v]-t.xyz[p])*1e3:.2f} mm")
    # inlet: X.tangent at node 0
    print(f"    X.tangent(t, 0) = {X.tangent(t, 0)}   (parent[0] = {t.parent[0]});  path2[0] for LAD = {t.vessel_path(ss.HOSTS['left']['LAD'])[0][0]}")
    p0 = int(t.vessel_path(ss.HOSTS['left']['LAD'])[0][0])
    print(f"    LAD path[0] node {p0} at {np.round(t.xyz[p0]*1e3,2)} vs root node 0 at {np.round(t.xyz[0]*1e3,2)}; arc(path0) = {t.arc[p0]*1e3:.2f} mm")
    ch = t.children[0]; e0 = t.xyz[int(ch[0])] - t.xyz[0]; e0 /= np.linalg.norm(e0)
    print(f"    true root downstream direction (node0 -> child) = {np.round(e0,3)}; shipped inlet normal = {np.round(X.tangent(t, p0),3)}; cos = {float(e0 @ X.tangent(t, p0)):.3f}")
    # do bifurcation children include INACTIVE (sub-cut) branches?
    path, _ = t.vessel_path(ss.HOSTS['left']['LAD'])
    for k, vv in enumerate(path):
        if len(t.children[int(vv)]) >= 2:
            print(f"    path bif at node {int(vv)} s={float(t.arc[int(vv)]-t.arc[int(path[0])])*1e3:.2f} mm: children {[ (int(c), bool(t.active[int(c)]), round(float(t.r_ref[int(c)])*1e3,3)) for c in t.children[int(vv)]]}")

# ------------------------------------------------------------------------------------------------- T2 specifics
section("T2 packages: measurement vs stump")
for n in [x for x in names if "T2" in x]:
    d = pk[n]; meta = json.loads((d / "meta.json").read_text()); a = pd.read_csv(d / "bc_A.csv"); o = pd.read_csv(d / "outlets.csv")
    pr = pd.read_csv(d / "probes.csv"); ed = json.loads((d / "mask_edit.json").read_text())
    print(f"  {n}: measurement {meta['measurement']}\n    closed outlets {a[a['mode']=='closed'].outlet_id.tolist()}; "
          f"lesion c={ed['lesion']['centre_mm']:.2f} L={ed['lesion']['length_mm']:.2f} -> c+L/2+20 = {ed['lesion']['centre_mm']+ed['lesion']['length_mm']/2+20:.2f}; "
          f"info {ed['mask_edit']['info']}; last host station s_node {pr[pr.kind!='outlet'].s_node_mm.max():.2f}")
print("\ndone")
