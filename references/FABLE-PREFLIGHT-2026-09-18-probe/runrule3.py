"""Variant 3 (probe only): runs are contiguous DS >= 0.30 chains WITHIN a segment (a run never crosses a bifurcation,
so a throat never migrates into a side branch), one throat per run, then throats are merged TREE-WIDE: a throat within
5 mm (|arc diff|) of a deeper kept throat is dropped. This removes both spurious-term modes (shoulder terms on long
lesions; the far-side-of-bifurcation term) without moving the main-vessel throat into a daughter."""
import numpy as np
from zerod_ffr import Tree, RHO, KT, DS_LESION

def set_radius_segrun_treemerge(self, r):
    self.r = r
    self.stenosis = np.clip(1.0 - self.r / np.maximum(self.r_fit, 1e-9), 0.0, 0.99)
    K = np.zeros(len(r)); cand = self.resolved & (self.stenosis >= DS_LESION); throats = []
    for sid in np.unique(self.seg):
        nodes = np.where(self.seg == sid)[0]; nodes = nodes[np.argsort(self.arc[nodes])]
        cur = []
        for v in nodes:
            if cand[v]: cur.append(v)
            elif cur: throats.append(max(cur, key=lambda u: self.stenosis[u])); cur = []
        if cur: throats.append(max(cur, key=lambda u: self.stenosis[u]))
    throats.sort(key=lambda v: -self.stenosis[v]); kept = []
    for v in throats:
        if all(abs(self.arc[v] - self.arc[u]) > 5e-3 for u in kept): kept.append(v)
    for v in kept:
        A0 = np.pi * self.r_fit[v] ** 2; As = np.pi * self.r[v] ** 2
        K[v] = RHO * KT / (2 * A0 ** 2) * (A0 / As - 1.0) ** 2
    self.K = K

def activate():
    Tree._set_radius = set_radius_segrun_treemerge
