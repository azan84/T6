"""Recommended lesion-term rule (probe only, code untouched). R4:
  * a stenosed RUN is a set of resolved DS >= 0.30 nodes connected by parent links (crosses segment boundaries, so a
    narrowing that continues past a bifurcation is one narrowing);
  * each FLOW PATH through a run (run root -> each run leaf) gets one expansion-loss term at its deepest node, so a
    trunk narrowing that continues into two daughters yields one term per daughter path (a shared trunk throat is
    counted once); a main-vessel throat can never migrate into a side branch unless the whole path's deepest point is
    there;
  * throats are merged only along the TREE PATH: a throat is dropped if a deeper kept throat is its ancestor or
    descendant within 5 mm of arc. |arc| alone (runrule2/3) wrongly merged lesions on different branches.
Discretisation-independent: run membership and throat choice depend on node values, not on where nodes fall."""
import numpy as np
from zerod_ffr import Tree, RHO, KT, DS_LESION

def _related_within(self, u, v, d=5e-3):
    """True if u and v are ancestor/descendant with |arc(u)-arc(v)| <= d."""
    a, b = (u, v) if self.arc[u] >= self.arc[v] else (v, u)          # a is the deeper (larger arc) node
    if self.arc[a] - self.arc[b] > d: return False
    while a >= 0 and self.arc[a] >= self.arc[b]:
        if a == b: return True
        a = self.parent[a]
    return False

def set_radius_r4(self, r):
    self.r = r
    self.stenosis = np.clip(1.0 - self.r / np.maximum(self.r_fit, 1e-9), 0.0, 0.99)
    n = len(r); K = np.zeros(n); cand = self.resolved & (self.stenosis >= DS_LESION)
    run = -np.ones(n, int); nrun = 0
    for v in range(n):                                  # BFS/chain numbering: parent index < child index
        if not cand[v]: continue
        p = self.parent[v]
        run[v] = run[p] if (p >= 0 and cand[p]) else nrun
        if run[v] == nrun: nrun += 1
    in_run_child = np.zeros(n, bool)
    for v in range(1, n):
        if cand[v] and cand[self.parent[v]]: in_run_child[self.parent[v]] = True
    throats = set()
    for leaf in np.where(cand & ~in_run_child)[0]:      # run leaves
        path, v = [], int(leaf)
        while v >= 0 and cand[v]: path.append(v); v = self.parent[v]
        throats.add(max(path, key=lambda u: self.stenosis[u]))
    kept = []
    for v in sorted(throats, key=lambda u: -self.stenosis[u]):
        if not any(_related_within(self, v, u) for u in kept): kept.append(v)
    for v in kept:
        A0 = np.pi * self.r_fit[v] ** 2; As = np.pi * self.r[v] ** 2
        K[v] = RHO * KT / (2 * A0 ** 2) * (A0 / As - 1.0) ** 2
    self.K = K

def activate():
    Tree._set_radius = set_radius_r4
