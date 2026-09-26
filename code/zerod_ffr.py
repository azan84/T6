"""
zerod_ffr.py (v3) — steady-state 0D coronary FFR on a centreline tree, with Murray-consistent distributed leakage.

v3 (2026-09-18): root eliminated from the linear system (no per-iteration matrix surgery), convergence + mass-balance
reporting, `evaluate()` for solving with an overridden radius while the physiology (r_ref, bed weights, C) stays
frozen, and `vessel_path()` for locating a main vessel. Physics unchanged from v2 except that the root node's own bed
leak is now counted in the inflow (it was omitted; effect < 1 %).

Model
* Node per centreline point. Element between consecutive points: Poiseuille with the ACTUAL radius,
  R = 8 mu ds / (pi r_mid^4), plus a nonlinear expansion loss K Q|Q| at detected lesions,
  K = rho Kt / (2 A0^2) (A0/As - 1)^2, Kt = 1.52.
* Healthy reference: robust linear taper fit per segment (r_fit, used for %DS), and r_ref = r_fit made non-increasing
  along each path and capped at 1.15 x the parent's distal value (used for the bed).
* Microvascular bed, Murray (flow ~ r^3): conductance to venous pressure at every node
      g(v) = max( r_ref(v)^3 - sum_children r_ref(c)^3 , 0 ) / C
  = outlet at a leaf, distributed side-branch leak along a taper (Gosling 2020's leaky model in 0D), Murray mismatch
  at a bifurcation. Telescopes to ~ r_inlet^3 / C: demand is set by the inlet, not by segmentation reach.
* C calibrated on the HEALTHY-equivalent network so inflow = hyperaemic demand (Murray Q = k r_in^3, or territory).
* Mask-derived radii resolve ~0.3-0.4 mm: network truncated at r_ref < R_TRUNC; lesion terms and reported FFR only
  where r_fit >= R_RESOLVED.
Units: SI.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

MU, RHO, KT, MMHG = 0.004, 1060.0, 1.52, 133.322
R_FLOOR, R_TRUNC, R_RESOLVED = 0.15e-3, 0.50e-3, 0.75e-3
# Discrete-outlet bed (the structure 3D can represent). 0.60 mm, not 0.75: at 0.75 only 54 % of lesion slots keep a
# deletable downstream branch (the missed-branch error type needs one) and 43/140 trees collapse to a single outlet,
# vs 77 % and 18/140 at 0.60 mm. Pre-registered fallback 0.75 mm if Gate M1 cannot mesh 1.2 mm-diameter outlets.
# Independent review, 2026-09-18 (references/FABLE-REVIEW-DISCRETEBED-2026-09-18.md §3).
R_TRUNC_DISCRETE = 0.60e-3
# Leaf outlet weight w = r_ref^MURRAY_EXP. 8/3 = 2.667, and the fraction is the point.
#
# THIS IS A MASS EXPONENT, NOT A FLOW EXPONENT — the distinction was nearly lost on 2026-09-19 and matters.
# The weight allocates MICROVASCULAR BED to a truncated outlet: how much myocardium sits behind it. Choy & Kassab
# 2008 (J Appl Physiol, "Scaling of myocardial mass to flow and morphometry of coronary arteries") give myocardial
# mass M ~ A^(4/3), and area goes as D^2, so M ~ D^(8/3) = D^2.667. That is this constant.
#   [VERIFY against the paper before the manuscript quotes it — obtained from search summaries, and this project
#    has already been bitten once by an attribution recorded "from memory".]
#
# A CITATION SEARCH FLAGGED 2.66 AS "UNCITED AND OUTSIDE THE POOLED EXPONENT 2.39 (CI 2.24-2.54, Taylor 2024)".
# That comparison is category-mismatched and the flag was withdrawn: Taylor 2024 pools the FLOW-diameter exponent
# Q ~ D^n (close to Kassab's theoretical 7/3 = 2.33), which predicts flow THROUGH a vessel. A pooled estimate of a
# different exponent is not evidence against this one. Also aligned with the 3D arm, which imposes the same
# allocation on outlet caps (Mao 2025 Eq. 7), so 0D-discrete and 3D-discrete share boundary conditions exactly.
#
# MEASURED SENSITIVITY, on the 30 frozen 3D-subset trees: moving 2.66 -> 2.39 shifts any single outlet's share of
# its tree's flow by a median 0.33 pp (p90 0.94, max 1.95), against a validation check that passes at 10 pp.
# Truncation is why: every leaf sits just above the 0.60 mm cut (median within-tree radius spread 0.058 mm), so
# near-identical radii raised to different powers give near-identical shares. Reported as a sensitivity because it
# is a real modelling question -- allocate the bed by mass or by flow -- not because 2.66 is in doubt.
MURRAY_EXP = 2.66
DS_LESION = 0.30
K_MURRAY = 562.0                      # s^-1 : hyperaemic Q = k r^3  (r = 2.0 mm -> 4.5 mL/s)
MAIN = ("LM", "LAD", "LCX", "LCx", "RCA")
P_AORTA, P_VEN = 90 * MMHG, 5 * MMHG

@dataclass
class Segment:
    sid: int
    parent: int | None
    pts: np.ndarray                   # (n,3) m
    r: np.ndarray                     # (n,)  m
    label: str = ""

def robust_taper(s, r, n_iter=4):
    if len(s) < 4 or s[-1] - s[0] < 1e-9:
        return np.full_like(r, np.median(r))
    A = np.vstack([s, np.ones_like(s)]).T; w = np.ones_like(r)
    for _ in range(n_iter):
        coef, *_ = np.linalg.lstsq(A * w[:, None], r * w, rcond=None)
        fit = A @ coef
        w = np.where(r - fit >= -0.12 * np.maximum(fit, 1e-6), 1.0, 0.15)
    return np.maximum(fit, 0.5 * np.median(r))

class Tree:
    def __init__(self, segments: list[Segment], name: str = "", bed: str = "leaky", r_trunc: float | None = None,
                 reference: "Tree | None" = None, trunc_ref: "Tree | None" = None):
        """bed = "leaky"    Murray distributed leakage at every node (primary 0D model; truncation 0.50 mm)
           bed = "discrete" conductance ONLY at the leaves of the truncated tree, none through the wall — the
                            structure a 3D model can represent (CFD-ARM-SPEC v0.2 §2.4; truncation 0.75 mm).
           BC structure is a pre-registered FACTOR of the experiment: the leaky bed re-inserts a deleted branch as a
           point leak at its parent node, the discrete bed does not."""
        assert bed in ("leaky", "discrete")
        self.name = name; self.bed = bed
        self.r_trunc = r_trunc if r_trunc is not None else (R_TRUNC if bed == "leaky" else R_TRUNC_DISCRETE)
        segs = {s.sid: s for s in segments}; kids = {sid: [] for sid in segs}; roots = []
        for s in segments:
            (kids[s.parent].append(s.sid) if s.parent is not None else roots.append(s.sid))
        assert len(roots) == 1, f"need exactly one root segment, got {roots}"
        order, q = [], [roots[0]]
        while q:
            u = q.pop(0); order.append(u); q += kids[u]
        P, R, RF, RFIT, DSD, LAB, SEG, XYZ = [-1], [], [], [], [0.0], [], [], []
        end_node, end_ref = {}, {}
        self._seg_s, self._seg_fit, self._seg_ref = {}, {}, {}
        for sid in order:
            sg = segs[sid]
            d = np.linalg.norm(np.diff(sg.pts, axis=0), axis=1)
            s = np.concatenate([[0.0], np.cumsum(d)])
            r = np.maximum(sg.r, R_FLOOR)
            if reference is not None:
                # inherit the healthy reference from another discretisation of the SAME geometry (matched by arc
                # length), so a refinement test isolates solver discretisation from re-fitting the reference
                fit = np.interp(s, reference._seg_s[sid], reference._seg_fit[sid])
                ref = np.interp(s, reference._seg_s[sid], reference._seg_ref[sid])
            else:
                fit = robust_taper(s, r)
                cap = 1.15 * end_ref.get(sg.parent, np.inf)
                ref = np.minimum.accumulate(np.minimum(fit, cap))
            self._seg_s[sid], self._seg_fit[sid], self._seg_ref[sid] = s, fit, ref
            if sg.parent is None:
                R.append(r[0]); RF.append(ref[0]); RFIT.append(fit[0]); LAB.append(sg.label); SEG.append(sid)
                XYZ.append(sg.pts[0]); prev = 0
            else:
                prev = end_node[sg.parent]
            for j in range(1, len(r)):
                P.append(prev); DSD.append(max(d[j - 1], 1e-6)); R.append(r[j]); RF.append(ref[j]); RFIT.append(fit[j])
                LAB.append(sg.label); SEG.append(sid); XYZ.append(sg.pts[j]); prev = len(P) - 1
            end_node[sid] = prev; end_ref[sid] = ref[-1]
        # force float64 everywhere: inputs may arrive as float32 (mask-derived radii) and mixed precision is a bug
        self.parent = np.array(P); self.r = np.asarray(R, dtype=np.float64)
        self.r_ref = np.asarray(RF, dtype=np.float64); self.r_fit = np.asarray(RFIT, dtype=np.float64)
        self.ds = np.asarray(DSD, dtype=np.float64); self.label = np.array(LAB); self.seg = np.array(SEG)
        # node coordinates (m): the only stable identity across a corrupted topology, where node INDICES shift
        self.xyz = np.asarray(XYZ, dtype=np.float64)
        n = len(self.parent)
        self.active = self.r_ref >= self.r_trunc; self.active[0] = True
        if trunc_ref is not None:
            # PIN THE MODELLED NODE SET TO ANOTHER TREE, BY COORDINATE (v3.1, 2026-09-19, decision B3).
            # A CALIBRE error must not change WHICH vessels are modelled. T4 scales every distal radius by 0.930,
            # which drags r_ref down with it and pushes leaves below a fixed truncation radius, deleting vessels the
            # error merely narrowed -- 489 of 655 discrete outlets and 56 of 148 whole trees, cohort-wide. Scaling
            # the threshold by the same factor was tried first and is only an approximation: r_ref is a robust taper
            # fit made monotone and parent-capped, so it is NOT proportional to r, and the node set still differed
            # from clean in 23 of 50 probe instances (up to +7 % more nodes -- the opposite error, adding anatomy).
            # THE REFERENCE IS AUTHORITATIVE -- assignment, not intersection. An earlier version used `&=`, which
            # could only ever REMOVE nodes relative to the clean set, so the threshold still governed on the removing
            # side: 6 of 298 T4 rows still dropped 2-7 nodes because r_ref after the taper re-fit fell below the
            # scaled cut. Leaf counts were unchanged, so those were leaves sliding a few nodes proximally -- and
            # under Protocol A a moved leaf has clean w = 0 and is written `closed`, i.e. a miniature of the exact
            # artefact this pin exists to remove. With `=` the node set is the reference's, full stop, and
            # ablation.trunc_for's scaled threshold becomes a harmless pre-filter rather than load-bearing.
            # Coordinates are already this model's node identity (see ablation.node_map).
            key = {tuple(np.round(x, 9)) for x in trunc_ref.xyz[trunc_ref.active]}
            self.active = np.array([tuple(np.round(x, 9)) in key for x in self.xyz])
            self.active[0] = True
        for v in range(1, n):
            self.active[v] &= self.active[self.parent[v]]
        self.children = [[] for _ in range(n)]
        for v in range(1, n):
            if self.active[v]: self.children[self.parent[v]].append(v)
        self.arc = np.zeros(n)
        for v in range(1, n): self.arc[v] = self.arc[self.parent[v]] + self.ds[v]
        self.resolved = self.active & (self.r_fit >= R_RESOLVED)
        self._set_radius(self.r)
        self.leaves = np.array([v for v in np.where(self.active)[0] if not self.children[v]])
        # zero-outlet guard: if no child of the root survives truncation the network is a bare node and _solve would
        # build a 0x0 system and return silently (review §5.4)
        if len(self.leaves) == 0 or (len(self.leaves) == 1 and self.leaves[0] == 0):
            raise ValueError(f"{name}: no outlet survives truncation at r_ref >= {self.r_trunc*1e3:.2f} mm")
        if bed == "leaky":
            w = self.r_ref ** 3                               # leaf: Murray outlet; elsewhere: leak / Murray mismatch
            for v in range(n):
                if self.children[v]:
                    w[v] = max(self.r_ref[v] ** 3 - sum(self.r_ref[c] ** 3 for c in self.children[v]), 0.0)
        else:
            # DISCRETE: conductance only at the leaves, weighted by the leaf's OWN radius, w = r_ref^MURRAY_EXP.
            # A top-down Murray share was tried first, on the reasoning that truncation puts every leaf at ~the cut
            # radius so leaf-weighting would carry no information. The premise holds (leaf r spread is small) but the
            # conclusion does not: an independent probe over 140 trees found the two schemes give the same flow at the
            # lesion and measurement nodes (x1.19 vs x1.17, x1.49 vs x1.51) and the same 65 %DS offset (-0.048 vs
            # -0.046) — the offset against the leaky bed is STRUCTURAL (no wall leak), not allocational — while the
            # share scheme is worse tree-wide (-0.056 +/- 0.077 vs -0.044 +/- 0.054; 17 vs 11 decision disagreements)
            # and is discontinuous at the cut (a sibling just below it donates its whole share to the survivor).
            # Leaf r^n is also literature-standard, identical to what 3D receives, and telescopes to the leaky
            # subtree total. Review 2026-09-18 §1, §5.5.
            w = np.zeros(n); w[self.leaves] = self.r_ref[self.leaves] ** MURRAY_EXP
        self.w = np.where(self.active, w, 0.0)
        # solver index maps (root eliminated)
        act = np.where(self.active)[0]; self.nr = act[act != 0]
        loc = -np.ones(n, int); loc[self.nr] = np.arange(len(self.nr))
        self._i = loc[self.nr]; self._j = loc[self.parent[self.nr]]            # _j == -1  <=> parent is the root
        # Viscosity as an INSTANCE attribute, defaulting to the module constant. Identical behaviour by default;
        # it exists because DETECTOR-SPEC §5's negative class must vary haematocrit to build a physiologically
        # perturbed truth, and a module constant cannot be varied per draw. Changing mu invalidates any cached C,
        # so callers that vary it must clear _C (negatives.py does).
        self.mu = MU
        self._C = {}

    def _set_radius(self, r):
        """Place one expansion-loss term per lesion. A lesion is a CONTIGUOUS RUN of resolved nodes with
        DS >= DS_LESION, connected by parent links and crossing segment boundaries; its K sits at the run's throat.
        Runs whose throats are < 5 mm apart are merged (deeper kept).

        This replaces a per-segment rule with a fixed 5 mm exclusion radius, which was discretisation-dependent and
        wrong in two ways (independent pre-flight review, 2026-09-18 §2):
          * SHOULDER TERMS. A 20 mm cosine lesion has DS >= 0.30 out to |s-c| = 5.00 mm at 60 %DS, 5.25 at 65, 5.46 at
            70, 5.80 at 80 — so whether a node fell just outside the 5 mm radius was a coin toss at ~0.5 mm spacing,
            adding a spurious second/third term worth 0.003-0.01 FFR. 2,281 of 6,944 sweep instances carried >= 2 extra
            terms. This, not discretisation, was the V8a refinement jump (+0.00538 then +0.00013: a jump, not O(h^2)).
          * BIFURCATION DOUBLE-COUNTING. The per-segment loop restarted the exclusion at every segment boundary, so a
            lesion spanning a bifurcation got a second FULL-STRENGTH throat term in the child segment — 20 of the 26
            bif_in_window instances; worst case FFR_meas 0.778 vs 0.851 corrected.
        A run-based rule is discretisation-independent by construction and smooth in lesion length (the stenosis-length
        error type T3 previously showed -0.0055 steps; it is now -0.0025/mm, monotone)."""
        self.r = r
        self.stenosis = np.clip(1.0 - self.r / np.maximum(self.r_fit, 1e-9), 0.0, 0.99)
        n = len(r); K = np.zeros(n)
        cand = self.resolved & (self.stenosis >= DS_LESION)
        # A throat is a LOCAL MAXIMUM of stenosis along the tree (>= parent and >= every child, among candidates),
        # not simply the deepest node of a contiguous run. One-per-run was tried first and is too coarse: when an
        # inserted lesion happens to be contiguous with a deeper native narrowing, the single throat lands on the
        # native one and the inserted lesion contributes NO expansion loss (6 instances in scan set 2 at 40-55 %DS,
        # verification check V3). Local maxima handle all three cases at once — a cosine lesion's shoulders are
        # monotone and so are never maxima; a lesion spanning a bifurcation still has one maximum; two genuinely
        # distinct narrowings have two. The 5 mm merge then removes plateau duplicates.
        s = self.stenosis
        is_max = cand.copy()
        for v in range(n):
            if not cand[v]: continue
            p = self.parent[v]
            if p >= 0 and cand[p] and s[p] > s[v]: is_max[v] = False
            for c in self.children[v]:
                if cand[c] and s[c] > s[v]: is_max[v] = False; break
        # Merge throats closer than 5 mm ALONG THE TREE, keeping the deeper. Distance must be measured on the
        # ancestor chain, not as |arc difference|: arc is length from the root, so two lesions on DIFFERENT branches
        # can share an arc value and a deeper one would silently suppress the other (found on scan 993 left, where an
        # LAD narrowing at the same arc length erased a 40-55 %DS inserted LCx lesion entirely — verification V3).
        def near(a, b):                                       # True if a and b are within 5 mm on one root path
            lo, hi = (a, b) if self.arc[a] <= self.arc[b] else (b, a)
            v = hi
            while v >= 0 and self.arc[v] >= self.arc[lo] - 1e-12:
                if v == lo: return self.arc[hi] - self.arc[lo] < 5e-3
                if self.arc[hi] - self.arc[v] >= 5e-3: return False
                v = self.parent[v]
            return False
        throats = list(np.where(is_max)[0])
        throats.sort(key=lambda v: -s[v])
        kept = []
        for v in throats:
            if not any(near(v, u) for u in kept): kept.append(v)
        for v in kept:
            A0 = np.pi * self.r_fit[v] ** 2; As = np.pi * self.r[v] ** 2
            K[v] = RHO * KT / (2 * A0 ** 2) * (A0 / As - 1.0) ** 2
        self.K = K

    # ---------------------------------------------------------------- solve
    def _solve(self, C, P_in, P_v, healthy, max_iter=200, tol=1e-8):
        el, par, i, j = self.nr, self.parent[self.nr], self._i, self._j
        m = len(el); nrp = j >= 0
        rr = self.r_ref if healthy else self.r
        r_mid = np.maximum(0.5 * (rr[el] + rr[par]), R_FLOOR)
        R_lin = 8 * self.mu * self.ds[el] / (np.pi * r_mid ** 4)
        Kel = np.zeros(m) if healthy else self.K[el]
        g_bed = self.w[el] / C; g_root = self.w[0] / C
        Q = np.zeros(m); conv = False; it = 0
        for it in range(1, max_iter + 1):
            g = 1.0 / (R_lin + Kel * np.abs(Q))
            rows = np.concatenate([i, j[nrp], i[nrp], j[nrp]])
            cols = np.concatenate([i, j[nrp], j[nrp], i[nrp]])
            vals = np.concatenate([g + g_bed, g[nrp], -g[nrp], -g[nrp]])
            G = coo_matrix((vals, (rows, cols)), shape=(m, m)).tocsr()
            b = g_bed * P_v; b[~nrp] += g[~nrp] * P_in
            Pn = spsolve(G, b)
            Pp = np.where(nrp, Pn[np.maximum(j, 0)], P_in)
            Qn = (Pp - Pn) * g
            if healthy or not Kel.any():
                Q = Qn; conv = True; break
            if np.max(np.abs(Qn - Q)) <= tol * (np.max(np.abs(Qn)) + 1e-18):
                Q = Qn; conv = True; break
            Q = 0.5 * (Q + Qn)
        inflow = float(np.sum(Q[~nrp]) + g_root * (P_in - P_v))
        bed_out = float(np.sum(g_bed * (Pn - P_v)) + g_root * (P_in - P_v))
        n = len(self.r); Pf = np.full(n, np.nan); Pf[0] = P_in; Pf[el] = Pn; Qf = np.zeros(n); Qf[el] = Q
        self.info = dict(iters=it, converged=conv, inflow=inflow, bed_out=bed_out,
                         mass_err=abs(inflow - bed_out) / max(abs(inflow), 1e-18))
        return Pf, Qf, inflow

    def demand(self, mode="murray", scale=1.0, Q_territory=None):
        return (K_MURRAY * self.r_ref[0] ** 3 if mode == "murray" else Q_territory) * scale

    def calibrate(self, Q_demand, P_in=P_AORTA, P_v=P_VEN):
        """Bed constant C such that the HEALTHY-equivalent network draws Q_demand.

        Guarded (review §5.2): if the healthy epicardial resistance alone cannot pass Q_demand — possible on a
        single-outlet discrete tree, where the epicardial drop is a large share of the pressure budget — the old
        bisection walked `lo` down until C underflowed to ~1e-314, `_solve` returned NaN, and the tree silently
        reported FFR 1.000 with converged=True. The ceiling is now computed explicitly and an infeasible tree raises.
        """
        key = round(Q_demand * 1e12)
        if key in self._C: return self._C[key]
        f = lambda lc: self._solve(10 ** lc, P_in, P_v, healthy=True)[2] - Q_demand
        q_max = self._solve(1e-30, P_in, P_v, healthy=True)[2]          # C -> 0: bed offers no resistance
        if not np.isfinite(q_max) or q_max <= Q_demand:
            raise ValueError(f"{self.name}: healthy epicardial network passes at most {q_max*1e6:.3f} mL/s, "
                             f"below the demand {Q_demand*1e6:.3f} mL/s — tree ineligible for this bed/truncation")
        lo, hi = 0.0, 8.0
        while f(lo) < 0: lo -= 2
        while f(hi) > 0: hi += 2
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if f(mid) > 0: lo = mid
            else: hi = mid
        C = 10 ** (0.5 * (lo + hi))
        if not (np.isfinite(C) and C > 1e-12):
            raise ValueError(f"{self.name}: calibration failed, C = {C:.3e}")
        self._C[key] = C
        return C

    def healthy_main_ffr(self, mode="murray", scale=1.0, Q_territory=None, P_in=P_AORTA, P_v=P_VEN) -> float:
        """Minimum FFR over resolved main-vessel nodes of the HEALTHY-equivalent network (r_ref everywhere, no lesion
        terms). The discrete-arm eligibility gate: a tree whose healthy network already loses pressure epicardially is
        not a credible discrete model (review §2 — it predicts the leaky/discrete offset with corr 0.92)."""
        C = self.calibrate(self.demand(mode, scale, Q_territory), P_in, P_v)
        P, _, _ = self._solve(C, P_in, P_v, healthy=True)
        main = self.resolved & np.isin(self.label, MAIN)
        return float(np.nanmin(P[main] / P_in)) if main.any() else np.nan

    def evaluate(self, C, r_override=None, P_in=P_AORTA, P_v=P_VEN):
        """Solve the diseased network with bed constant C. If r_override is given, ONLY the epicardial radius changes:
        r_ref, r_fit, bed weights and C stay exactly as computed from the original geometry."""
        r0 = self.r
        if r_override is not None: self._set_radius(np.maximum(r_override, R_FLOOR))
        P, Q, inflow = self._solve(C, P_in, P_v, healthy=False); info = dict(self.info)
        sten, K = self.stenosis.copy(), self.K.copy()
        if r_override is not None: self._set_radius(r0)
        return P / P_in, Q, info, sten, K

    def vessel_path(self, labels):
        """Nodes along a main vessel: from its most proximal node, following same-label children (largest r_ref at
        forks), then continuing past the label's end along the largest child for run-off. Returns (nodes, n_same)."""
        cand = np.where(self.active & np.isin(self.label, labels))[0]
        if not len(cand): return None, 0
        v = cand[np.argmin(self.arc[cand])]; path = [v]; n_same = 1; in_label = True
        while self.children[v]:
            ch = self.children[v]
            same = [c for c in ch if self.label[c] in labels] if in_label else []
            if same: v = max(same, key=lambda c: self.r_ref[c]); n_same += 1
            else: in_label = False; v = max(ch, key=lambda c: self.r_ref[c])
            path.append(v)
        return np.array(path), n_same

    def ffr(self, mode="murray", scale=1.0, Q_territory=None, P_in=P_AORTA, P_v=P_VEN) -> dict:
        Qd = self.demand(mode, scale, Q_territory); C = self.calibrate(Qd, P_in, P_v)
        ffr, Q, info, _, _ = self.evaluate(C, None, P_in, P_v)
        main = self.resolved & np.isin(self.label, MAIN)
        out = dict(name=self.name, mode=mode, scale=scale, Q_demand_mls=Qd * 1e6, Q_in_mls=info["inflow"] * 1e6,
                   r_in_mm=self.r_ref[0] * 1e3, n_nodes=int(self.active.sum()),
                   resolved_len_mm=float(self.ds[self.resolved].sum() * 1e3),
                   min_ffr_main=float(np.nanmin(ffr[main])) if main.any() else np.nan,
                   lesion_ds_pct=np.nan, lesion_label="", lesion_ffr20=np.nan, n_lesions=int((self.K > 0).sum()),
                   C=C, iters=info["iters"], converged=info["converged"])
        les = np.where(main & (self.K > 0))[0]
        if len(les):
            v = les[np.argmax(self.stenosis[les])]; d = 0.0; u = v
            while d < 20e-3 and self.children[u]:
                u = max(self.children[u], key=lambda c: self.r_ref[c]); d += self.ds[u]
            out.update(lesion_ds_pct=float(100 * self.stenosis[v]), lesion_label=str(self.label[v]),
                       lesion_ffr20=float(ffr[u]))
        self.last = dict(ffr=ffr, Q=Q)
        return out

    def segment_table(self):
        f, Q, rows = self.last["ffr"], self.last["Q"], []
        for sid in np.unique(self.seg):
            nd = np.where((self.seg == sid) & self.active)[0]
            if len(nd) == 0: continue
            res = nd[self.resolved[nd]]; q0 = nd[1] if (nd[0] == 0 and len(nd) > 1) else nd[0]
            rows.append(dict(seg=int(sid), label=str(self.label[nd[0]]), len_mm=float(self.ds[nd].sum() * 1e3),
                             r_prox=float(self.r[nd[0]] * 1e3), r_dist=float(self.r[nd[-1]] * 1e3),
                             maxDS_resolved=float(100 * self.stenosis[res].max()) if len(res) else np.nan,
                             Q_prox=float(Q[q0] * 1e6), Q_dist=float(Q[nd[-1]] * 1e6),
                             ffr_dist=float(f[nd[-1]]), lesions=int((self.K[nd] > 0).sum())))
        return rows

# ----------------------------------------------------------------------------- self-test
def _ideal_vessel(ds_pct, r0_mm=1.8, L_mm=90.0, lesion_len_mm=10.0, r_end_mm=0.9, n=181):
    s = np.linspace(0, L_mm, n); r = r0_mm + (r_end_mm - r0_mm) * s / L_mm; c = L_mm * 0.35
    inl = np.abs(s - c) < lesion_len_mm / 2
    r = np.where(inl, r * (1 - ds_pct / 100 * 0.5 * (1 + np.cos(np.pi * (s - c) / (lesion_len_mm / 2)))), r)
    return Segment(0, None, np.stack([s, 0 * s, 0 * s], 1) * 1e-3, r * 1e-3, "LAD")

if __name__ == "__main__":
    print("self-test: tapering LAD-like vessel 1.8 -> 0.9 mm over 90 mm, Murray demand, distributed leakage")
    print(f"{'%DS':>4} {'DS_est':>7} {'Q_in':>6} {'minFFR':>7} {'FFR20':>7} {'iters':>6} {'conv':>5} {'mass_err':>9}")
    for ds in (0, 30, 50, 60, 70, 80, 90):
        t = Tree([_ideal_vessel(ds)]); o = t.ffr()
        print(f"{ds:>4} {o['lesion_ds_pct'] if o['n_lesions'] else 0:>7.1f} {o['Q_in_mls']:>6.2f} {o['min_ffr_main']:>7.3f} "
              f"{o['lesion_ffr20'] if o['n_lesions'] else float('nan'):>7.3f} {o['iters']:>6} {str(o['converged']):>5} {t.info['mass_err']:>9.1e}")
