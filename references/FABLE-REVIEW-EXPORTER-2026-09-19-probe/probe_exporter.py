"""
probe_exporter.py — adversarial checks on code/export_cfd_case.py output (review 2026-09-19).
Reads packages written to a scratch dir; writes NOTHING into results/, protocol/ or cfd_handover/.
usage: probe_exporter.py <data_root> <scratch_m1_dir> <scratch_extra_dir>
"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, pandas as pd, pyvista as pv, nibabel as nib

HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE / "code"))
from zerod_ffr import Tree, P_AORTA, P_VEN, RHO, MU, MURRAY_EXP, R_TRUNC_DISCRETE
from severity_sweep import load, plan, insert, HOSTS, RUNOFF
from ablation import node_map, bed_flow, territories
from error_types import ERROR_TYPES, T3_LENGTH_DELTA

root, M1, EXTRA = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
PY = str(Path.home() / ".venvs/paper6-t6/bin/python")
pk = {e: next(M1.glob(f"*__{e}__real")) for e in ("clean_nolesion", "baseline", "T1_missed_branch")}

def sec(t): print(f"\n{'='*100}\n{t}\n{'='*100}")

# ------------------------------------------------------------------------------------------------ 1 units
sec("1. BC arithmetic: R_i = C / w_i inverts g = w/C; units; order of magnitude vs Stage A")
t = load(root, 14, "left", "discrete"); o = t.ffr("murray", 1.0); C = o["C"]
print(f"r_ref[0] = {t.r_ref[0]*1e3:.3f} mm  Murray demand = {o['Q_demand_mls']:.4f} mL/s  inflow = {o['Q_in_mls']:.4f}  C = {C:.4f}")
print(f"w units: r_ref[m]^{MURRAY_EXP} -> leaf w ~ {t.w[t.leaves].mean():.3e} m^2.66; g = w/C [m^3/s/Pa] -> C has units Pa.s/m^3 * m^2.66")
bcA = pd.read_csv(pk["baseline"] / "bc_A.csv"); out = pd.read_csv(pk["baseline"] / "outlets.csv")
R_re = C / t.w[out.node.values]
print(f"max |R_A - C/w| / R = {np.max(np.abs(bcA.R_SI.values - R_re) / R_re):.2e}")
print(f"max |R_kin - R_SI/rho| = {np.max(np.abs(bcA.R_kinematic.values - bcA.R_SI.values / RHO)):.2e}")
# hand check: R = C / r^2.66
r0 = out.r_ref_mm.values[0] * 1e-3
print(f"hand: C / ({out.r_ref_mm.values[0]:.4f}e-3)^2.66 = {C / r0**MURRAY_EXP:.4e}  file = {bcA.R_SI.values[0]:.4e}")
stageA = pd.read_csv(HERE / "cfd_handover/stageA/expected_0D.csv")
Rst = stageA.R_out_SI.dropna().mean(); Qst = 1.5e-6
print(f"Stage A: R_out_SI = {Rst:.4e} Pa.s/m^3 for one outlet at Q = 1.5 mL/s -> p_out - P_v = {Rst*Qst:.0f} Pa")
q = pd.read_csv(pk["baseline"] / "bc_C_flows.csv")
print(f"M1: {len(bcA)} outlets, R_A = {bcA.R_SI.min():.3e}..{bcA.R_SI.max():.3e}; Q = {q.Q_target_mls.min():.4f}..{q.Q_target_mls.max():.4f} mL/s "
      f"(sum {q.Q_target_mls.sum():.4f}); R*Q = {(bcA.R_SI*q.Q_target_m3s).min():.0f}..{(bcA.R_SI*q.Q_target_m3s).max():.0f} Pa")
print(f"ratio R_M1/R_stageA ~ {bcA.R_SI.mean()/Rst:.1f}x ; ratio Q_stageA/Q_M1 ~ {Qst/q.Q_target_m3s.mean():.1f}x  (should be comparable)")
print(f"P_aorta = {P_AORTA:.2f} Pa -> {P_AORTA/RHO:.4f} m2/s2 (START-HERE says 11998.98 -> 11.3198); P_v {P_VEN:.2f} -> {P_VEN/RHO:.5f}")
print(f"nu = mu/rho = {MU/RHO:.4e} (START-HERE 3.774e-6)")

# ------------------------------------------------------------------------------------------------ 2 blinding arithmetic
sec("2. Blinding: does bc_A x bc_C_flows reveal the clean 0D outlet FFR?  p_i = P_v + R_i Q_i")
slots, _ = plan(t, "left", t.last["ffr"].copy())
sl = next(s for s in slots if s["vessel"] == "LAD" and s["loc"] == "prox" and abs(s["L"] - 20e-3) < 1e-9)
path, s_arc, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]; meas = int(path[mi])
r_clean, _ = insert(t, path, s_arc, c, L, 0.80)
ffr0, Q0, info0, _, _ = t.evaluate(C, r_clean)
p_from_files = (P_VEN + bcA.R_SI.values * q.Q_target_m3s.values) / P_AORTA
for i, r in out.iterrows():
    print(f"  {r.outlet_id:<8} terr {int(r.territory_id)}  (P_v + R_A*Q_C)/P_aorta = {p_from_files[i]:.4f}   0D clean FFR at that outlet = {ffr0[int(r.node)]:.4f}")
print(f"  0D clean FFR at the measurement node = {ffr0[meas]:.4f}  (withheld value)  -> LAD-territory outlet FFR brackets it")
manifest = json.loads((M1 / "MANIFEST.json").read_text())
print(f"  MANIFEST.json (inside the package tree) contains: {[k for k in manifest['instance'] if 'ffr' in k or 'base' in k or 'healthy' in k]} = "
      f"{[manifest['instance'][k] for k in manifest['instance'] if 'ffr' in k or 'base' in k]}")

# ------------------------------------------------------------------------------------------------ 3 vtp
sec("3. centreline.vtp: arrays, point ids vs `node` columns, inlet identity")
for e, d in pk.items():
    m = pv.read(d / "centreline.vtp")
    print(f"  {e}: n_points={m.n_points} n_lines={m.n_lines} arrays={list(m.point_data.keys())}")
m = pv.read(pk["baseline"] / "centreline.vtp")
act = np.where(t.active)[0]
print(f"  tree nodes {len(t.parent)}, active {t.active.sum()}, vtp points {m.n_points}; active indices contiguous? {bool(np.all(np.diff(act)==1))}")
pr = pd.read_csv(pk["baseline"] / "probes.csv")
# does probes.node index the vtp?
mis = 0
for _, r in pr.iterrows():
    v = int(r.node)
    if v >= m.n_points or np.linalg.norm(m.points[v] - np.array([r.x, r.y, r.z])) > 1e-6: mis += 1
print(f"  probes.csv `node` used as a vtp point id lands on the wrong point in {mis}/{len(pr)} rows")
xyz_mm = t.xyz * 1e3
print(f"  vtp point 0 == tree root (LM ostium)? {np.allclose(m.points[0], xyz_mm[0])}; root xyz = {np.round(xyz_mm[0],2)}; root r = {t.r[0]*1e3:.2f} mm; label {t.label[0]}")
print(f"  inlet.json has position/normal? {[k for k in json.loads((pk['baseline']/'inlet.json').read_text()) if k in ('x','y','z','normal_x')] or 'NO'}")
misr = np.asarray(m.point_data["MaximumInscribedSphereRadius"])
print(f"  baseline vtp MISR at throat node (clean r) = {misr[np.argmin(np.linalg.norm(m.points - xyz_mm[path[np.argmin(np.abs(s_arc-c))]], axis=1))]:.3f} mm; "
      f"0D lesioned target r2 = {r_clean[path[np.argmin(np.abs(s_arc-c))]]*1e3:.3f} mm  -> MISR is the PRE-lesion radius")

# ------------------------------------------------------------------------------------------------ 4 outlets
sec("4. outlets.csv: normals unit and outward; r_ref at cut")
for e, d in pk.items():
    o2 = pd.read_csv(d / "outlets.csv")
    n = o2[["normal_x", "normal_y", "normal_z"]].values
    print(f"  {e}: |n|-1 max {np.max(np.abs(np.linalg.norm(n,axis=1)-1)):.1e}; r_ref {o2.r_ref_mm.min():.3f}..{o2.r_ref_mm.max():.3f} mm; r_actual {o2.r_mm.min():.3f}..{o2.r_mm.max():.3f}")
# outward: dot(n, xyz[v]-xyz[grandparent]) > 0, and dot with a 3-edge mean tangent
o2 = pd.read_csv(pk["baseline"] / "outlets.csv")
for _, r in o2.iterrows():
    v = int(r.node); p = int(t.parent[v]); g = int(t.parent[p]); gg = int(t.parent[g])
    n = np.array([r.normal_x, r.normal_y, r.normal_z]); t3 = t.xyz[v] - t.xyz[gg]; t3 /= np.linalg.norm(t3)
    print(f"    {r.outlet_id}: cos(n, 3-edge tangent) = {float(n @ t3):.3f}   depth of last edge {np.linalg.norm(t.xyz[v]-t.xyz[p])*1e3:.2f} mm")

# ------------------------------------------------------------------------------------------------ 5 probes
sec("5. probes.csv: monotone s, on the centreline, inside the mask; grid s vs node s")
img = nib.load(str(root / "segmentations" / "14.coronary.nii.gz")); lab = np.asarray(img.dataobj); inv = np.linalg.inv(img.affine)
def in_mask(pts_lps_mm, flip=True):
    ras = pts_lps_mm * (np.array([-1., -1., 1.]) if flip else 1.0)
    ijk = np.round((inv @ np.c_[ras, np.ones(len(ras))].T)[:3]).astype(int).T
    ok = np.all((ijk >= 0) & (ijk < np.array(lab.shape)), axis=1)
    val = np.zeros(len(ras), int); val[ok] = lab[ijk[ok, 0], ijk[ok, 1], ijk[ok, 2]]
    return val > 0
for e, d in pk.items():
    p = pd.read_csv(d / "probes.csv")
    mono = bool(np.all(np.diff(p.s_mm.values) > 0))
    # actual arc of the node vs the s_mm written
    t2 = t  # same coordinates in all three, node ids differ; use coordinates
    P = p[["x", "y", "z"]].values
    d_cl = [np.min(np.linalg.norm(xyz_mm[act] - P[i], axis=1)) for i in range(len(P))]
    # true arc along the LAD path: match by coordinate to path nodes
    s_true = []
    for i in range(len(P)):
        k = np.argmin(np.linalg.norm(xyz_mm[path] - P[i], axis=1)); s_true.append(s_arc[k] * 1e3)
    ds = np.array(s_true) - p.s_mm.values
    print(f"  {e}: n={len(p)} monotone={mono} kinds={dict(p.kind.value_counts())}; max dist to a centreline point {max(d_cl):.1e} mm; "
          f"in mask {in_mask(P).sum()}/{len(P)}; |s_written - s_node| max {np.max(np.abs(ds)):.3f} mm (grid rows: {np.max(np.abs(ds[p.kind=='grid'])):.3f})")
print(f"  station kinds required by DETECTOR-SPEC 7.2: grid, lesion_prox, throat, lesion_dist, measurement, bifurcation, outlet;  CFD-ARM-SPEC 11: inlet ... every outlet")

# ------------------------------------------------------------------------------------------------ 6 mask edit executability
sec("6. mask_edit.json (T1): are the deletion points inside the NIfTI mask? (LPS->RAS flip needed?)")
me = json.loads((pk["T1_missed_branch"] / "mask_edit.json").read_text())["mask_edit"]
P = np.array([[q_["x"], q_["y"], q_["z"]] for q_ in me["points_mm"]])
print(f"  n_points {me['n_points']}; with LPS->RAS flip: {in_mask(P, True).sum()}/{len(P)} in lumen; WITHOUT flip (raw into NIfTI affine): {in_mask(P, False).sum()}/{len(P)}")
print(f"  frame stated in mask_edit.json? {'LPS' in json.dumps(me) or 'RAS' in json.dumps(me)};  in meta.json? {'LPS' in (pk['T1_missed_branch']/'meta.json').read_text()}")
sp = img.header.get_zooms()[:3]; print(f"  voxel spacing {np.round(sp,3)} mm; deleted branch r {min(q_['r_mm'] for q_ in me['points_mm']):.2f}..{max(q_['r_mm'] for q_ in me['points_mm']):.2f} mm "
      f"-> {2*min(q_['r_mm'] for q_ in me['points_mm'])/min(sp):.1f}..{2*max(q_['r_mm'] for q_ in me['points_mm'])/min(sp):.1f} voxels across")
# simulate the rule on the mask: how many voxels deleted, restored; does a stump remain?
ras_all = xyz_mm[act] * np.array([-1., -1., 1.]); ijk_all = (inv @ np.c_[ras_all, np.ones(len(ras_all))].T)[:3].T
ras_del = P * np.array([-1., -1., 1.]); ijk_del = (inv @ np.c_[ras_del, np.ones(len(ras_del))].T)[:3].T
nz = np.argwhere(lab > 0); lo = np.maximum(ijk_del.min(0).astype(int) - 8, 0); hi = np.minimum(ijk_del.max(0).astype(int) + 9, lab.shape)
vox_ijk = np.argwhere(lab[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]] > 0) + lo
vox_mm = (img.affine @ np.c_[vox_ijk, np.ones(len(vox_ijk))].T)[:3].T   # RAS mm
del_mm = ras_del; keep_pts = ras_all[[i for i in range(len(act)) if not any(np.allclose(xyz_mm[act][i], P[j]) for j in range(len(P)))]]
keep_r = t.r[act][[i for i in range(len(act)) if not any(np.allclose(xyz_mm[act][i], P[j]) for j in range(len(P)))]] * 1e3
rdel = np.array([q_["r_mm"] for q_ in me["points_mm"]])
dd = np.linalg.norm(vox_mm[:, None, :] - del_mm[None], axis=2); deleted = (dd <= 1.10 * rdel[None]).any(1)
dk = np.linalg.norm(vox_mm[:, None, :] - keep_pts[None], axis=2); restored = deleted & (dk <= 1.00 * keep_r[None]).any(1)
print(f"  rule simulated on the mask crop: {deleted.sum()} voxels flagged, {restored.sum()} restored by the parent rule -> {deleted.sum()-restored.sum()} removed; "
      f"branch voxels in the crop not reached by the rule (within 1.5 r of a deleted point but > 1.1 r): {((dd <= 1.5*rdel[None]).any(1) & ~deleted).sum()}")

# ------------------------------------------------------------------------------------------------ 7 truncation: what is in the mask but not in the package
sec("7. Truncation: centreline present in the mask but absent from the package (no rule ships for it)")
inact = ~t.active
stubs = [v for v in range(1, len(t.parent)) if inact[v] and t.active[t.parent[v]]]
print(f"  scan 14 left: {inact.sum()}/{len(t.parent)} centreline nodes inactive (r_ref < 0.60 mm), {t.ds[inact].sum()*1e3:.0f} mm of {t.ds.sum()*1e3:.0f} mm; "
      f"{len(stubs)} sub-cut branch roots hang off the active tree (side branches {sum(1 for v in stubs if len(t.children[t.parent[v]])>=1 and t.parent[v] not in t.leaves)}, "
      f"outlet continuations {sum(1 for v in stubs if t.parent[v] in set(t.leaves.tolist()))})")
win = [k for k, v in enumerate(path) if abs(s_arc[k] - c) < L / 2]
print(f"  sub-cut branch roots leaving the host path INSIDE the lesion window: {sum(1 for k in win for v in stubs if t.parent[v]==path[k])}; "
      f"radius of those: {[round(float(t.r[v]*1e3),2) for k in win for v in stubs if t.parent[v]==path[k]]}")
print(f"  rule for these in baseline/clean mask_edit.json: {'NONE' if 'truncat' not in (pk['baseline']/'mask_edit.json').read_text() else 'present'}")

# ------------------------------------------------------------------------------------------------ 8 other error types for the same instance (index 50)
sec("8. T2 / T3 / T4 packages for the same instance (cohort row 50): NaN in BCs? taper instruction present?")
EXTRA.mkdir(parents=True, exist_ok=True)
for et in ("T2_truncation", "T3_stenosis_length", "T4_taper", "T1_missed_branch"):
    r = subprocess.run([PY, str(HERE / "code/export_cfd_case.py"), str(root), "--instance", "50", "--error", et, "--tier", "real", "--out", str(EXTRA)],
                       capture_output=True, text=True)
    if r.returncode: print(f"  {et}: FAILED {r.stderr.strip().splitlines()[-1]}"); continue
    d = next(EXTRA.glob(f"*__{et}__real"))
    a = pd.read_csv(d / "bc_A.csv"); b = pd.read_csv(d / "bc_B.csv"); cc = pd.read_csv(d / "bc_C_flows.csv"); oo = pd.read_csv(d / "outlets.csv")
    me = json.loads((d / "mask_edit.json").read_text())
    print(f"  {et}: outlets {len(oo)}; NaN R_A {int(a.R_SI.isna().sum())}, NaN R_B {int(b.R_SI.isna().sum())}, NaN Q_C {int(cc.Q_target_m3s.isna().sum())}; "
          f"mask_edit keys {list(me.keys())}; 'scale' or 'taper' instruction in mask_edit: {('radius_scale' in json.dumps(me)) or ('0.93' in json.dumps(me))}")
    if a.R_SI.isna().any():
        print(f"     -> bc_A.csv rows written as EMPTY cells: {a[a.R_SI.isna()].outlet_id.tolist()}  (raw line: {[l for l in (d/'bc_A.csv').read_text().splitlines() if l.endswith(',')]})")
    if et == "T4_taper":
        print(f"     T4 vertex_deformation table rows: {len(me['vertex_deformation']['table'])} (lesion window only); centre {me['vertex_deformation']['centre_mm']:.2f} mm")
        vt = pv.read(d / "centreline.vtp"); print(f"     T4 vtp MISR max {np.asarray(vt.point_data['MaximumInscribedSphereRadius']).max():.3f} vs baseline {misr.max():.3f} -> vtp carries the scaled radius, mask_edit does not say to scale the surface")
    if et == "T2_truncation":
        print(f"     T2 mask_edit rule: {me['mask_edit']['rule'][:80]}...; n_points {me['mask_edit']['n_points']}; info {me['mask_edit']['info']}")

# ------------------------------------------------------------------------------------------------ 9 Protocol C: per-outlet vs territory totals (T1)
sec("9. Protocol C targets in the T1 package vs the 0D primary's TERRITORY totals")
segs2, info = ERROR_TYPES["T1_missed_branch"](list(t.segments), t, path, s_arc, c, L)
t2 = Tree(segs2, "t1", bed="discrete"); mm = node_map(t, t2)
q0_all = bed_flow(t, C, ffr0); terr = territories(t2); terr_clean = territories(t)
qt1 = pd.read_csv(pk["T1_missed_branch"] / "bc_C_flows.csv")
for j, sub in enumerate(terr):
    mc = mm[sub][mm[sub] >= 0]
    tot_clean = q0_all[mc].sum() * 1e6
    tot_clean_full = q0_all[terr_clean[j]].sum() * 1e6
    per_out = qt1[qt1.territory_id == j].Q_target_mls.sum()
    print(f"  territory {j}: 0D-primary target (clean total over surviving nodes' clean counterparts) = {tot_clean:.4f} mL/s; "
          f"clean territory total incl. deleted outlet = {tot_clean_full:.4f}; package per-outlet targets sum = {per_out:.4f}")
print(f"  ablation.py C target for the LAD territory = {q0_all[mm[terr[0]][mm[terr[0]]>=0]].sum()*1e6:.4f} mL/s  (it sums CLEAN flow over the surviving nodes only -> identical to per-outlet sum in the discrete bed)")
print(f"  => in the DISCRETE bed the territory total over surviving nodes == sum of surviving outlets' clean flows. The difference 0D-vs-3D is ONE scalar (over-determined) vs N exact.")
# quantify: 0D one-scalar C fit vs 0D per-outlet exact prescription -> FFR at measurement
from scipy.optimize import minimize_scalar
p2, _ = t2.vessel_path(HOSTS["left"]["LAD"]); s2 = t2.arc[p2] - t2.arc[p2[0]]
r2, _ = insert(t2, p2, s2, c, L, 0.80); cand = np.where(mm == meas)[0]; meas2 = int(cand[0])
t_pairs = [(sub, float(q0_all[mm[sub][mm[sub] >= 0]].sum())) for sub in terr]
t2._C.clear(); C_start = t2.calibrate(t2.demand("murray", 1.0))
def loss(lc):
    f, *_ = t2.evaluate(10 ** lc, r2); qq = bed_flow(t2, 10 ** lc, f)
    return float(np.mean([((qq[sub].sum() - qt) / qt) ** 2 for sub, qt in t_pairs]))
res = minimize_scalar(loss, bounds=(np.log10(C_start) - 1.5, np.log10(C_start) + 1.5), method="bounded", options=dict(xatol=1e-7))
C_c = 10 ** res.x; f_c, *_ = t2.evaluate(C_c, r2); qb = bed_flow(t2, C_c, f_c)
resid = np.sqrt(np.mean([((qb[sub].sum() - qt) / qt) ** 2 for sub, qt in t_pairs]))
# per-outlet exact: iterate R_i so that each leaf flow equals target (fixed point on R_i = (p_i - P_v)/Q_i^target)
leaves = t2.leaves; Qt = np.array([q0_all[mm[v]] for v in leaves])
w_save = t2.w.copy(); Rl = C_c / t2.w[leaves]
for it in range(200):
    t2.w = np.zeros_like(w_save); t2.w[leaves] = 1.0 / Rl          # C = 1 -> g = 1/R
    f_i, Q_i, inf_i, _, _ = t2.evaluate(1.0, r2)
    p_i = f_i[leaves] * P_AORTA
    R_new = (p_i - P_VEN) / Qt
    if np.max(np.abs(R_new - Rl) / Rl) < 1e-10: Rl = R_new; break
    Rl = 0.5 * (Rl + R_new)
t2.w = np.zeros_like(w_save); t2.w[leaves] = 1.0 / Rl; f_i, Q_i, inf_i, _, _ = t2.evaluate(1.0, r2)
qi = bed_flow(t2, 1.0, f_i)[leaves]; t2.w = w_save
f_B, *_ = t2.evaluate(C_start, r2)
print(f"  0D T1 FFR at measurement: clean {ffr0[meas]:.4f} | B re-derived {f_B[meas2]:.4f} | C one-scalar (territory) {f_c[meas2]:.4f} (resid {resid:.3f}, C/C_clean {C_c/C:.3f}) "
      f"| C per-outlet exact {f_i[meas2]:.4f} (max |Q-Qt|/Qt {np.max(np.abs(qi-Qt)/Qt):.1e}, {it+1} it)")
print(f"  per-outlet derived R_i / R_A: {np.round(Rl / (C / t.w[mm[leaves]]), 3)}  (what the 3D side would find, in 0D)")
print(f"  inflow: clean {info0['inflow']*1e6:.4f} | C one-scalar {np.nansum(bed_flow(t2, C_c, f_c))*1e6:.4f} | C per-outlet {inf_i['inflow']*1e6:.4f} mL/s")

# ------------------------------------------------------------------------------------------------ 9b islands after the T1 rule; T2 measurement node; T4 instruction
sec("9b. T1 rule leaves islands?  T2: where is the measurement node?  T4: any taper instruction?")
from scipy.ndimage import label as cc_label
crop = lab[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]] > 0
after = crop.copy(); rem = vox_ijk[deleted & ~restored] - lo; after[rem[:, 0], rem[:, 1], rem[:, 2]] = False
lbl0, n0 = cc_label(crop); lbl1, n1 = cc_label(after)
sizes = np.bincount(lbl1.ravel())[1:]
print(f"  crop around the deleted branch: components before {n0}, after the rule {n1}; component sizes after: {sorted(sizes.tolist(), reverse=True)[:8]}")
d2 = next(EXTRA.glob("*__T2_truncation__real")); meta2 = json.loads((d2 / "meta.json").read_text()); pr2 = pd.read_csv(d2 / "probes.csv")
print(f"  T2: meta.measurement_s_mm = {meta2['measurement_s_mm']:.2f}; probes 'measurement' station s_mm = {pr2[pr2.kind=='measurement'].s_mm.tolist()}; "
      f"last station s = {pr2.s_mm.max():.2f}; cut at {json.loads((d2/'mask_edit.json').read_text())['mask_edit']['info']['cut_arc_mm']:.2f}; "
      f"clean measurement s = {(c + L/2 + RUNOFF)*1e3:.2f}  (T2_KEEP_BEYOND 15 mm < RUNOFF 20 mm)")
o2t = pd.read_csv(d2 / "outlets.csv"); a2t = pd.read_csv(d2 / "bc_A.csv")
print(f"  T2 outlet with NaN R_A is node {int(o2t[a2t.R_SI.isna().values].node.iloc[0])} = measurement node {meta2['measurement_node']}? "
      f"{int(o2t[a2t.R_SI.isna().values].node.iloc[0]) == meta2['measurement_node']}")
d4 = next(EXTRA.glob("*__T4_taper__real")); txt4 = (d4 / "mask_edit.json").read_text()
print(f"  T4 mask_edit.json mentions radius_scale / segments_scaled / from_arc: {'radius_scale' in txt4}, {'segments_scaled' in txt4}, {'from_arc' in txt4}; keys {list(json.loads(txt4).keys())}")
o4 = pd.read_csv(d4 / "outlets.csv"); a4 = pd.read_csv(d4 / "bc_A.csv")
print(f"  T4 NaN-R_A outlet: {o4[a4.R_SI.isna().values][['outlet_id','r_ref_mm','r_mm']].to_dict('records')} (a new leaf: taper shrank r_ref below the cut one node earlier)")
ob = pd.read_csv(pk["baseline"] / "outlets.csv"); vb = pv.read(pk["baseline"] / "centreline.vtp")
print(f"  outlets.csv node ids {ob.node.tolist()} vs vtp n_points {vb.n_points}: usable as vtp point ids? {bool((ob.node < vb.n_points).all())}")

# ------------------------------------------------------------------------------------------------ 10 M1 instance choice
sec("10. M1 instance: scan 14 vs scan 306 (both 80%DS LAD prox 20 mm, 6 outlets, 1 deletable branch)")
for sid in (14, 306):
    tt = load(root, sid, "left", "discrete"); oo = tt.ffr("murray", 1.0); sl_, _ = plan(tt, "left", tt.last["ffr"].copy())
    s_ = next(s for s in sl_ if s["vessel"] == "LAD" and s["loc"] == "prox" and abs(s["L"] - 20e-3) < 1e-9)
    ci = s_["ci"]; rf = tt.r_fit[s_["path"][ci]] * 1e3
    segs_, inf_ = ERROR_TYPES["T1_missed_branch"](list(tt.segments), tt, s_["path"], s_["s"], s_["c"], s_["L"])
    imgx = nib.load(str(root / "segmentations" / f"{sid}.coronary.nii.gz")); spx = min(imgx.header.get_zooms()[:3])
    print(f"  scan {sid}: host r_fit {rf:.3f} mm -> throat r {0.2*rf:.3f} mm ({0.4*rf/spx:.1f} voxels across at {spx:.3f} mm); bif_in_window {s_['bif_in_window']}; "
          f"d_dn_bif {s_['d_dn_bif_mm']:.1f} mm; deletable branch r {inf_['branch_r_mm']:.3f} mm ratio {inf_['branch_to_host_ratio']:.2f}; "
          f"outlets {len(tt.leaves)}, min outlet r_ref {tt.r_ref[tt.leaves].min()*1e3:.3f} mm; inactive nodes {(~tt.active).sum()}/{len(tt.parent)}")
sub = pd.read_csv(HERE / "protocol/CFD-SUBSET-FROZEN-2026-09-18.csv")
print(f"  subset: max n_outlets {sub.n_outlets.max()} (scan {sub.loc[sub.n_outlets.idxmax(),'scan']} {sub.loc[sub.n_outlets.idxmax(),'vessel']} {sub.loc[sub.n_outlets.idxmax(),'ds_pct']}%DS, "
      f"{sub.loc[sub.n_outlets.idxmax(),'n_branch_ge_cut']:.0f} branches); max n_branch_ge_cut {sub.n_branch_ge_cut.max():.0f}")

# ------------------------------------------------------------------------------------------------ 11 sweep the whole 3D subset x error types for NaN / applicability
sec("11. Whole frozen 3D subset x 5 geometries: NaN BCs, non-applicable types, new-leaf outlets (dry, files to scratch)")
rows = []
for _, r in sub.iterrows():
    tt = load(root, int(r.scan), r.side, "discrete"); oo = tt.ffr("murray", 1.0); Cc = oo["C"]
    sl_, _ = plan(tt, r.side, tt.last["ffr"].copy())
    s_ = next((s for s in sl_ if s["vessel"] == r.vessel and s["loc"] == r["loc"] and abs(s["L"] * 1e3 - r.L_mm) < 1e-6), None)
    if s_ is None: rows.append(dict(scan=r.scan, vessel=r.vessel, etype="*", status="slot missing")); continue
    for et, fn in ERROR_TYPES.items():
        segs_, inf_ = fn(list(tt.segments), tt, s_["path"], s_["s"], s_["c"], s_["L"])
        if segs_ is None: rows.append(dict(scan=r.scan, vessel=r.vessel, etype=et, status=f"n/a: {inf_}")); continue
        try: t2_ = Tree(segs_, "x", bed="discrete")
        except ValueError as e: rows.append(dict(scan=r.scan, vessel=r.vessel, etype=et, status=f"tree: {e}")); continue
        m_ = node_map(tt, t2_)
        wcl = np.where(m_ >= 0, tt.w[np.maximum(m_, 0)], 0.0)
        newleaf = [int(v) for v in t2_.leaves if wcl[v] <= 0]
        rows.append(dict(scan=r.scan, vessel=r.vessel, etype=et, status="ok", n_out=len(t2_.leaves), n_out_clean=len(tt.leaves),
                         nan_RA=len(newleaf), lost=len(tt.leaves) - (len(t2_.leaves) - len(newleaf))))
df = pd.DataFrame(rows); df.to_csv(EXTRA / "subset_sweep.csv", index=False)
print(df.groupby("etype").status.value_counts().to_string())
ok = df[df.status == "ok"]
print(f"\n  packages with >=1 outlet whose Protocol-A resistance is NaN (new leaf with no clean counterpart): "
      f"{(ok.nan_RA>0).sum()}/{len(ok)}  by type: {ok[ok.nan_RA>0].etype.value_counts().to_dict()}")
print(f"  outlets lost vs clean by type (mean): {ok.groupby('etype').lost.mean().round(2).to_dict()}")
