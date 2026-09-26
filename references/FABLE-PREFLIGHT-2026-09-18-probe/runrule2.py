"""Tree-wide contiguous-run lesion rule (probe only): a run is a set of resolved DS >= 0.30 nodes connected by parent
links, regardless of segment boundaries (a lesion spanning a bifurcation is ONE lesion). One K term at each run's
throat; runs whose throats are < 5 mm apart along the tree are merged (deeper kept, distance measured by |arc diff|,
which is exact for nodes on one root path and conservative otherwise)."""
import numpy as np
from zerod_ffr import Tree, RHO, KT, DS_LESION

def set_radius_treerun(self, r):
    self.r = r
    self.stenosis = np.clip(1.0 - self.r / np.maximum(self.r_fit, 1e-9), 0.0, 0.99)
    K = np.zeros(len(r)); cand = self.resolved & (self.stenosis >= DS_LESION)
    run = -np.ones(len(r), int); nrun = 0
    for v in range(len(r)):                                        # nodes are numbered in BFS/chain order: parent < child
        if not cand[v]: continue
        p = self.parent[v]
        if p >= 0 and cand[p]: run[v] = run[p]
        else: run[v] = nrun; nrun += 1
    throats = [int(np.where(run == k)[0][np.argmax(self.stenosis[run == k])]) for k in range(nrun)]
    throats.sort(key=lambda v: -self.stenosis[v]); kept = []
    for v in throats:
        if all(abs(self.arc[v] - self.arc[u]) > 5e-3 for u in kept): kept.append(v)
    for v in kept:
        A0 = np.pi * self.r_fit[v] ** 2; As = np.pi * self.r[v] ** 2
        K[v] = RHO * KT / (2 * A0 ** 2) * (A0 / As - 1.0) ** 2
    self.K = K

def activate():
    Tree._set_radius = set_radius_treerun
