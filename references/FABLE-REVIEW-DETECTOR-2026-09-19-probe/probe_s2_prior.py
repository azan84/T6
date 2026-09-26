"""Probe 2 (DETECTOR-SPEC review): the S2 anatomical prior  ln C ~ ln r_ref(root) + ln sum(w) + ln n_outlets + ln L_resolved
fitted on every tree of the frozen cohort, both beds. Reports R^2, residual sigma, collinearity, and the implied
S2_z for the smoke-test C_ratios and for a +-20 % cardiac-output perturbation. Also counts territories per tree.
Usage: probe_s2_prior.py <data_root>"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE / "code"))
from zerod_ffr import K_MURRAY, P_AORTA, P_VEN
from severity_sweep import load
from ablation import territories

root = Path(sys.argv[1])
coh = pd.read_csv(HERE / "protocol" / "COHORT-FROZEN-2026-09-18.csv")
trees = coh.drop_duplicates(["scan", "side"])[["scan", "side"]]
rows = []
for _, r in trees.iterrows():
    for bed in ("leaky", "discrete"):
        try:
            t = load(root, int(r.scan), r.side, bed); o = t.ffr("murray", 1.0)
        except ValueError as e:
            rows.append(dict(scan=int(r.scan), side=r.side, bed=bed, status=str(e)[:60])); continue
        Ph, Qh, inh = t._solve(o["C"], P_AORTA, P_VEN, healthy=True)
        terr = territories(t)
        rows.append(dict(scan=int(r.scan), side=r.side, bed=bed, status="ok", C=o["C"], r_root=t.r_ref[0],
                         w_sum=float(t.w.sum()), n_outlets=len(t.leaves), L_resolved=float(t.ds[t.resolved].sum()),
                         n_terr=len(terr), terr_share_min=float(min(t.w[s].sum() for s in terr) / t.w.sum()) if terr else np.nan,
                         healthy_min_ffr_main=t.healthy_main_ffr(),
                         # closed form if the healthy epicardial drop were zero: C0 = (P_in - P_v) sum(w) / (K r0^3)
                         C_closed=(P_AORTA - P_VEN) * t.w.sum() / (K_MURRAY * t.r_ref[0] ** 3)))
df = pd.DataFrame(rows); df.to_csv(Path(__file__).parent / "s2_prior_data.csv", index=False)
ok = df[df.status == "ok"]
for bed, g in ok.groupby("bed"):
    y = np.log(g.C.values)
    X = np.c_[np.ones(len(g)), np.log(g.r_root), np.log(g.w_sum), np.log(g.n_outlets), np.log(g.L_resolved)]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ beta
    sig = res.std(ddof=5); r2 = 1 - res.var() / y.var()
    print(f"\n=== bed {bed}: n_trees {len(g)}  ln C sd {y.std():.3f}  (C range {g.C.min():.1f}-{g.C.max():.1f})")
    print(f"  OLS beta [1, ln r_root, ln sum w, ln n_out, ln L_res] = {np.round(beta, 3)}")
    print(f"  R^2 = {r2:.4f}   sigma_resid = {sig:.4f}   (ln C_closed - ln C: mean {np.mean(np.log(g.C_closed) - y):+.4f}, sd {np.std(np.log(g.C_closed) - y):.4f})")
    cm = np.corrcoef(X[:, 1:].T); print("  covariate corr matrix (r_root, sum w, n_out, L_res):\n", np.round(cm, 3))
    # VIF
    for k, nm in enumerate(["ln r_root", "ln sum w", "ln n_out", "ln L_res"]):
        Xk = np.delete(X, k + 1, axis=1); b, *_ = np.linalg.lstsq(Xk, X[:, k + 1], rcond=None)
        rr = X[:, k + 1] - Xk @ b; vif = 1 / (1 - (1 - rr.var() / X[:, k + 1].var()))
        print(f"    VIF {nm}: {vif:.1f}")
    # two-covariate version (the design-note relation): ln C ~ ln r_root + ln sum w
    X2 = X[:, :3]; b2, *_ = np.linalg.lstsq(X2, y, rcond=None); r2b = 1 - (y - X2 @ b2).var() / y.var()
    print(f"  2-covariate (r_root, sum w) R^2 = {r2b:.4f}  beta = {np.round(b2, 3)}  (theory: -3, +1)")
    print(f"  implied S2_z for ln C_ratio of 0.04 / 0.10 / 0.20 / ln(1.2) CO perturbation: "
          f"{0.04/sig:.1f} / {0.10/sig:.1f} / {0.20/sig:.1f} / {np.log(1.2)/sig:.1f}")
    print(f"  territories per tree: {g.n_terr.value_counts().sort_index().to_dict()}   min territory weight share: "
          f"median {g.terr_share_min.median():.3f}, p10 {g.terr_share_min.quantile(.1):.3f}")
    print(f"  healthy main-vessel min FFR: median {g.healthy_min_ffr_main.median():.3f} min {g.healthy_min_ffr_main.min():.3f}")
print("\nnot ok:", df[df.status != "ok"].groupby("bed").size().to_dict())
