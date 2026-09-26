"""Alternative lesion-term rule (probe only, code under ROOT/code untouched): ONE expansion-loss term per CONTIGUOUS run
of DS >= 0.30 nodes along a segment; runs whose throats lie < 5 mm apart are merged (deeper throat kept). This is
discretisation-independent, unlike the fixed 5 mm radius around the throat, which lets the shoulders of a 20 mm lesion
(DS >= 0.30 out to 5.25-5.80 mm at 65-80 %DS) receive their own K terms whenever a node happens to land there."""
import numpy as np
from zerod_ffr import Tree, RHO, KT, DS_LESION

def set_radius_runrule(self, r):
    self.r = r
    self.stenosis = np.clip(1.0 - self.r / np.maximum(self.r_fit, 1e-9), 0.0, 0.99)
    K = np.zeros(len(r)); sten = self.stenosis >= DS_LESION
    for sid in np.unique(self.seg):
        nodes = np.where(self.seg == sid)[0]
        nodes = nodes[np.argsort(self.arc[nodes])]                     # segment is a chain: arc order == chain order
        runs, cur = [], []
        for v in nodes:
            if self.resolved[v] and sten[v]: cur.append(v)
            elif cur: runs.append(cur); cur = []
        if cur: runs.append(cur)
        throats = [max(run, key=lambda v: self.stenosis[v]) for run in runs]
        throats.sort(key=lambda v: -self.stenosis[v]); kept = []
        for v in throats:
            if all(abs(self.arc[v] - self.arc[u]) > 5e-3 for u in kept): kept.append(v)
        for v in kept:
            A0 = np.pi * self.r_fit[v] ** 2; As = np.pi * self.r[v] ** 2
            K[v] = RHO * KT / (2 * A0 ** 2) * (A0 / As - 1.0) ** 2
    self.K = K

def activate():
    Tree._set_radius = set_radius_runrule
