"""Reviewer's probe (NOT protocol-grade) for the discrete-outlet bed decision.
Usage: bedprobe.py [--scans 878 844 ...] [--all] [--out name]
For every tree: leaky reference; discrete bed at several truncation radii and outlet-weight schemes; healthy-network
flow fidelity at the main-vessel lesion sites; baseline FFR; a 65 %DS lesion; T1 (missed downstream branch) and
T4 (distal under-sizing) under protocols A/B/C, so that error-induced dFFR can be compared across bed structures.
"""
import sys, time, argparse, numpy as np, pandas as pd
from pathlib import Path
from scipy.optimize import minimize_scalar
CODE = Path("/Users/mzpi/Library/CloudStorage/GoogleDrive-Mohd.Zulhilmi@monash.edu/My Drive/Research/01 CollabProject-MonashIIUM/Imaging-Medical/Paper6-T6/code")
sys.path.insert(0, str(CODE))
import zerod_ffr as Z
from zerod_ffr import Tree, Segment
import severity_sweep as SS
HERE = Path(__file__).parent
DATA = Path.home() / "Datasets/imagecas-x/ImageCAS-X_dataset"
TRUNCS = (0.5e-3, 0.6e-3, 0.75e-3, 0.9e-3, 1.0e-3)
SCHEMES = ("share", "leaf3", "leaf266", "apport", "origin", "length")

def xyz_of(segments):
    segs = {s.sid: s for s in segments}; kids = {k: [] for k in segs}; root = None
    for s in segments:
        if s.parent is None: root = s.sid
        else: kids[s.parent].append(s.sid)
    order, q = [], [root]
    while q: u = q.pop(0); order.append(u); q += kids[u]
    X = [segs[root].pts[0]]
    for sid in order: X += list(segs[sid].pts[1:])
    return np.array(X)

def full_children(t):
    """children over ALL nodes (active or not) -- the untruncated centreline tree"""
    ch = [[] for _ in range(len(t.parent))]
    for v in range(1, len(t.parent)): ch[t.parent[v]].append(v)
    return ch

def weights(d: Tree, scheme: str):
    n = len(d.r); lv = d.leaves; w = np.zeros(n); r3 = d.r_ref ** 3
    if scheme == "share":
        return d.w.copy()                                   # as built by zerod_ffr (top-down Murray share)
    if scheme == "leaf3":
        w[lv] = r3[lv]
    elif scheme == "leaf266":
        w[lv] = d.r_ref[lv] ** 2.66
    elif scheme == "apport":
        # bottom-up: leaky-type weight at every active node of the TRUNCATED tree, apportioned to descendant leaves
        # in proportion to leaf r_ref^3 (total = r_root^3, same as leaky and share)
        wl = np.zeros(n); S = np.zeros(n)
        for v in np.where(d.active)[0]:
            wl[v] = max(r3[v] - sum(r3[c] for c in d.children[v]), 0.0) if d.children[v] else r3[v]
        for v in np.where(d.active)[0][::-1]:               # children after parents -> reverse = bottom-up
            S[v] = r3[v] if not d.children[v] else sum(S[c] for c in d.children[v])
        acc = np.zeros(n); acc[0] = wl[0]
        for v in np.where(d.active)[0]:
            for c in d.children[v]: acc[c] = wl[c] + acc[v] * S[c] / S[v]
        w[lv] = acc[lv]
    elif scheme == "origin":
        # Murray on the radius at the ORIGIN of the segment the leaf terminates (first node of that segment)
        for l in lv:
            sid = d.seg[l]; first = np.where(d.seg == sid)[0][0]
            w[l] = r3[first] if first != 0 else r3[0]
    elif scheme == "length":
        # Seiler-type: summed centreline length of the untruncated subtree below the leaf (+ leaf's own segment)
        fc = full_children(d); sub = np.zeros(n)
        for v in range(n - 1, 0, -1): sub[d.parent[v]] += sub[v] + d.ds[v]
        for l in lv:
            sid = d.seg[l]; own = d.ds[(d.seg == sid) & (np.arange(n) <= l)].sum()
            w[l] = sub[l] + own
    return w

def bedflow(d, C, f): return d.w / C * (f * Z.P_AORTA - Z.P_VEN)

def discrete(segs, name, T, scheme):
    d = Tree(segs, name, bed="discrete", r_trunc=T); d.w = np.where(d.active, weights(d, scheme), 0.0); d._C = {}; return d

def solve_pair(d):
    """calibrate on healthy; return C, healthy (ffr,Q), diseased (ffr,Q,info)"""
    C = d.calibrate(d.demand()); Ph, Qh, _ = d._solve(C, Z.P_AORTA, Z.P_VEN, healthy=True); fh = Ph / Z.P_AORTA
    f, Q, info, *_ = d.evaluate(C, None); return C, fh, Qh, f, Q, info

def side_branches(t, path, s, c, L, mi):
    pset = set(path.tolist()); out = []
    for k, v in enumerate(path):
        for ch in t.children[v]:
            if ch not in pset: out.append((s[k], t.r_ref[ch], ch, int(t.seg[ch])))
    return out

def delete_subtree(segments, sid0):
    dead = {sid0}; grew = True
    while grew:
        grew = False
        for sg in segments:
            if sg.parent in dead and sg.sid not in dead: dead.add(sg.sid); grew = True
    return [sg for sg in segments if sg.sid not in dead]

def scale_distal(segments, t, node_from, f):
    """T4: multiply radius by f on every centreline point strictly distal (arc) to node_from along its subtree"""
    fc = full_children(t); desc = set(); st = list(fc[node_from])
    while st:
        v = st.pop(); desc.add(v); st += fc[v]
    out = []
    for sg in segments:
        idx = np.where(t.seg == sg.sid)[0]
        if sg.parent is None: idx = idx  # includes node 0
        r = sg.r.copy()
        # node index -> position within segment: nodes of a segment are consecutive in t; first node of the root seg is 0
        pos0 = 0 if sg.parent is None else 1
        for k, v in enumerate(idx):
            if v in desc: r[k + pos0] *= f
        out.append(Segment(sg.sid, sg.parent, sg.pts, r, sg.label))
    return out

def protocols(cl, Cc, r_clean_lesion, bad, m, meas_b):
    """A: frozen (surviving weights + C from clean); B: re-derived and recalibrated; C: one scalar matched to the
    clean model's surviving-outlet flows. `m` maps bad node -> clean node. Returns dict of FFR at the measurement node."""
    fc, Qc, ic, *_ = cl.evaluate(Cc, r_clean_lesion)
    rb = r_clean_lesion[m]
    wB = bad.w.copy(); bad.w = np.where(bad.active, cl.w[m], 0.0); fA, *_ = bad.evaluate(Cc, rb); bad.w = wB
    bad._C = {}; Cb = bad.calibrate(bad.demand()); fB, *_ = bad.evaluate(Cb, rb)
    lv = bad.leaves; lv = lv[cl.active[m[lv]]]; q0 = bedflow(cl, Cc, fc)[m[lv]]; ok = q0 > 0
    def loss(lc):
        f, *_ = bad.evaluate(10 ** lc, rb); q = bedflow(bad, 10 ** lc, f)[lv]
        return np.mean(((q[ok] - q0[ok]) / q0[ok]) ** 2) if ok.any() else 0.0
    res = minimize_scalar(loss, bounds=(np.log10(Cb) - 1.5, np.log10(Cb) + 1.5), method="bounded", options=dict(xatol=1e-6))
    fC, *_ = bad.evaluate(10 ** res.x, rb)
    return dict(A=float(fA[meas_b]), B=float(fB[meas_b]), C=float(fC[meas_b]))

def run_tree(root, sid, side, rows_tree, rows_leaf, rows_slot):
    t = SS.load(root, sid, side)                            # leaky, 0.50 mm
    segs = t.segments; o = t.ffr("murray", 1.0); Cl = o["C"]; base_l = t.last["ffr"].copy(); Ql = t.last["Q"].copy()
    Phl, Qhl, _ = t._solve(Cl, Z.P_AORTA, Z.P_VEN, healthy=True)
    main = t.resolved & np.isin(t.label, Z.MAIN)
    slots, rej = SS.plan(t, side, base_l)
    # one slot per host vessel: prox, 10 mm preferred
    best = {}
    for sl in slots:
        key = sl["vessel"]; rank = (sl["loc"] != "prox", sl["L"])
        if key not in best or rank < best[key][0]: best[key] = (rank, sl)
    slots = [b[1] for b in best.values()]
    tree_row = dict(scan=sid, side=side, r_in=t.r_ref[0] * 1e3, Q_demand=o["Q_demand_mls"], leaky_minffr=o["min_ffr_main"],
                    leaky_Qin=o["Q_in_mls"], leaky_nout=len(t.leaves), leaky_healthy_outlet_ffr_min=float(np.nanmin(Phl[t.leaves] / Z.P_AORTA)),
                    leaky_leafw_frac=float(t.w[t.leaves].sum() / t.w.sum()), n_slots=len(slots))
    # ---- truncation x scheme
    for T in TRUNCS:
        for sc in SCHEMES:
            try:
                d = discrete(segs, t.name, T, sc)
            except Exception as e:
                tree_row[f"err_{T*1e3:.2f}_{sc}"] = repr(e); continue
            k = f"{T*1e3:.2f}_{sc}"
            if len(d.nr) == 0: tree_row[f"nout_{k}"] = 0; continue
            try:
                C, fh, Qh, f, Q, info = solve_pair(d)
            except Exception as e:
                tree_row[f"err_{k}"] = repr(e); continue
            mn = d.resolved & np.isin(d.label, Z.MAIN)
            tree_row[f"nout_{k}"] = len(d.leaves); tree_row[f"C_{k}"] = C
            tree_row[f"minffr_{k}"] = float(np.nanmin(f[mn])) if mn.any() else np.nan
            tree_row[f"Qin_{k}"] = info["inflow"] * 1e6; tree_row[f"hout_{k}"] = float(np.nanmin(fh[d.leaves]))
            tree_row[f"hmain_{k}"] = float(np.nanmin(fh[mn])) if mn.any() else np.nan
            tree_row[f"leafmin_{k}"] = d.r_ref[d.leaves].min() * 1e3; tree_row[f"leafmax_{k}"] = d.r_ref[d.leaves].max() * 1e3
            tree_row[f"conv_{k}"] = info["converged"]; tree_row[f"mass_{k}"] = info["mass_err"]
            # healthy flow fidelity at main resolved nodes vs leaky healthy flow
            both = mn & (Qhl > 0) & (d.active)
            if both.any():
                lr = np.log(Qh[both] / Qhl[both]); tree_row[f"lqr_med_{k}"] = float(np.median(lr)); tree_row[f"lqr_max_{k}"] = float(lr.max())
            if sc == "share" and T == 0.75e-3:
                for l in d.leaves:
                    rows_leaf.append(dict(scan=sid, side=side, T=T * 1e3, r_leaf=d.r_ref[l] * 1e3, label=str(d.label[l]),
                                          w_share=d.w[l] / d.r_ref[0] ** 3, w_leaf3=d.r_ref[l] ** 3 / d.r_ref[0] ** 3,
                                          origin_r=np.nan, is_main=bool(d.label[l] in Z.MAIN)))
            # slot-level records: healthy flow at the lesion node & measurement node, baseline & lesioned FFR
            for sl in slots:
                path, s, c, L, ci, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["ci"], sl["mi"]
                cn, mnode = path[ci], path[mi]
                r_les, _ = SS.insert(t, path, s, c, L, 0.65)
                srow = dict(scan=sid, side=side, vessel=sl["vessel"], T=T * 1e3, scheme=sc, nout=len(d.leaves),
                            meas_active=bool(d.active[mnode]), les_active=bool(d.active[cn]),
                            Qh_les_leaky=Qhl[cn] * 1e6, Qh_les=Qh[cn] * 1e6 if d.active[cn] else np.nan,
                            Qh_meas_leaky=Qhl[mnode] * 1e6, Qh_meas=Qh[mnode] * 1e6 if d.active[mnode] else np.nan,
                            hffr_meas=float(fh[mnode]) if d.active[mnode] else np.nan,
                            base_meas_leaky=float(base_l[mnode]), base_meas=float(f[mnode]) if d.active[mnode] else np.nan,
                            r_ref_les=t.r_ref[cn] * 1e3, r_ref_meas=t.r_ref[mnode] * 1e3)
                if d.active[mnode]:
                    fl, *_ = d.evaluate(C, r_les); srow["les65_meas"] = float(fl[mnode])
                    fll, *_ = t.evaluate(Cl, r_les); srow["les65_meas_leaky"] = float(fll[mnode])
                    # downstream side branches retained at this truncation
                    br = side_branches(t, path, s, c, L, mi)
                    srow["n_dn_br_ret"] = sum(1 for (sb, rb, ch, _) in br if sb >= c + L / 2 and d.active[ch])
                    srow["n_dn_br_all"] = sum(1 for (sb, rb, ch, _) in br if sb >= c + L / 2)
                    srow["runoff_ret_mm"] = float((s[d.active[path]].max() - (c + L / 2)) * 1e3)
                rows_slot.append(srow)
    rows_tree.append(tree_row)
    return t, segs, slots, Cl

def run_errors(root, sid, side, t, segs, slots, Cl, rows_err, T=0.75e-3, schemes=("share", "leaf3", "apport")):
    xyz = xyz_of(segs); key = {tuple(np.round(x, 9)): i for i, x in enumerate(xyz)}
    for sl in slots:
        path, s, c, L, ci, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["ci"], sl["mi"]; mnode = path[mi]
        r_les, _ = SS.insert(t, path, s, c, L, 0.65)
        br = [(rb, ch, sg, sb) for (sb, rb, ch, sg) in side_branches(t, path, s, c, L, mi) if sb >= c + L / 2 and rb >= T]
        errs = []
        if br:
            rb, ch, sg, sb = max(br); errs.append(("T1", delete_subtree(segs, sg), dict(r_branch=rb * 1e3, branch_before_meas=bool(sb <= s[mi]))))
        # T4: distal under-sizing f = 0.85 below the lesion's distal edge on the host path
        dn = path[int(np.searchsorted(s, c + L / 2))]
        errs.append(("T4", scale_distal(segs, t, dn, 0.85), dict()))
        for etype, segs_bad, meta in errs:
            for bed in ("leaky",) + tuple(schemes):
                try:
                    if bed == "leaky":
                        cl = Tree(segs, t.name, bed="leaky"); bad = Tree(segs_bad, t.name + "_bad", bed="leaky")
                    else:
                        cl = discrete(segs, t.name, T, bed); bad = discrete(segs_bad, t.name + "_bad", T, bed)
                    if not cl.active[mnode]: continue
                    Cc = cl.calibrate(cl.demand())
                    xb = xyz_of(segs_bad); m = np.array([key[tuple(np.round(x, 9))] for x in xb])
                    meas_b = int(np.where(m == mnode)[0][0])
                    if not bad.active[meas_b]:
                        rows_err.append(dict(scan=sid, side=side, vessel=sl["vessel"], err=etype, bed=bed, meas_lost=True, **meta)); continue
                    fc, *_ = cl.evaluate(Cc, r_les)
                    # for T4 under A the radius override must carry the scaled radii: rebuild override from bad tree's own r
                    if etype == "T4":
                        # same topology: node indices coincide. A = clean tree, frozen physiology, radii scaled+lesioned
                        r_over = np.minimum(bad.r, r_les)
                        fA, *_ = cl.evaluate(Cc, r_over)
                        bad._C = {}; Cb = bad.calibrate(bad.demand()); fB, *_ = bad.evaluate(Cb, r_over)
                        lv = bad.leaves; q0 = bedflow(cl, Cc, fc)[lv]; ok = q0 > 0
                        def loss(lc):
                            f, *_ = bad.evaluate(10 ** lc, r_over); q = bedflow(bad, 10 ** lc, f)[lv]
                            return np.mean(((q[ok] - q0[ok]) / q0[ok]) ** 2) if ok.any() else 0.0
                        res = minimize_scalar(loss, bounds=(np.log10(Cb) - 1.5, np.log10(Cb) + 1.5), method="bounded", options=dict(xatol=1e-6))
                        fC, *_ = bad.evaluate(10 ** res.x, r_over)
                        pr = dict(A=float(fA[meas_b]), B=float(fB[meas_b]), C=float(fC[meas_b]))
                    else:
                        pr = protocols(cl, Cc, r_les, bad, m, meas_b)
                    rows_err.append(dict(scan=sid, side=side, vessel=sl["vessel"], err=etype, bed=bed, meas_lost=False,
                                         clean=float(fc[mnode]), nout_clean=len(cl.leaves), nout_bad=len(bad.leaves), **pr, **meta))
                except Exception as e:
                    rows_err.append(dict(scan=sid, side=side, vessel=sl["vessel"], err=etype, bed=bed, error=repr(e), **meta))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--scans", nargs="*", default=None); ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default="probe"); a = ap.parse_args()
    meta = SS.scans_of(DATA, "test")
    if a.all: ids = [(int(s), side) for s in meta.index for side in ("left", "right")]
    else:
        ids = []
        for tok in a.scans:
            sid, side = tok.split("_"); ids.append((int(sid), side))
    RT, RL, RS, RE = [], [], [], []; t0 = time.time()
    for n, (sid, side) in enumerate(ids, 1):
        try:
            t, segs, slots, Cl = run_tree(DATA, sid, side, RT, RL, RS)
            run_errors(DATA, sid, side, t, segs, slots, Cl, RE)
        except Exception as e:
            print(f"FAIL {sid}_{side}: {e!r}", flush=True)
        if n % 10 == 0 or n == len(ids):
            print(f"{n}/{len(ids)} trees {time.time()-t0:.0f}s", flush=True)
            for nm, R in (("tree", RT), ("leaf", RL), ("slot", RS), ("err", RE)):
                pd.DataFrame(R).to_csv(HERE / f"{a.out}_{nm}.csv", index=False)
