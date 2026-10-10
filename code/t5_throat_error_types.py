"""
t5_throat_error_types.py - throat caliber error (T5): the same lesion re-inserted with a changed severity.

T5 keeps the lesion centre c, length L and the node set of the clean tree (trunc_ref pinned, as for T3/T4) and
changes only the inserted percent diameter stenosis (DS), i.e. the throat radius r_fit(c) * (1 - DS).

Variants (each sign is its own error type):
  T5_ds_plus10    DS + 10 percentage points  (throat over-read as narrower: stenosis more severe)
  T5_ds_minus10   DS - 10 percentage points  (throat under-read: stenosis less severe)
  T5_vox_narrow   throat diameter - 1/2 voxel, i.e. throat radius - 1/4 in-plane voxel  (DS up)
  T5_vox_wide     throat diameter + 1/2 voxel, i.e. throat radius + 1/4 in-plane voxel  (DS down)

The in-plane voxel size is the mean of the first two header zooms of the scan's ImageCAS-X label volume. DS is
clipped to [DS_MIN, DS_MAX]; every insertion is logged with the requested and applied DS.

Mechanism. The frozen run_instance functions call severity_sweep.insert(tree, path, s, c, L, ds) once for the clean
model and once per error type, immediately after the error-type function. A T5 function registers a pending DS
transform; the patched insert applies it to the next call only and then clears it. install() applies the patches to
the imported modules in memory; no source file is changed.
"""
from __future__ import annotations
import re
from functools import lru_cache
from pathlib import Path
import numpy as np

DS_DELTA = 0.10
VOXEL_FRACTION_OF_RADIUS = 0.25
DS_MIN, DS_MAX = 0.05, 0.95

DATA_ROOT = Path.home() / "Documents" / "Datasets" / "imagecas-x" / "ImageCAS-X_dataset"

_PENDING = None          # callable(ds_frac) -> (ds_new, meta) for the next insert call, or None
LOG: list = []           # one dict per T5 insertion
_ORIG_INSERT = None


def reset():
    global _PENDING
    _PENDING = None


@lru_cache(maxsize=None)
def inplane_spacing_mm(scan: int) -> float:
    import nibabel as nib
    img = nib.load(str(DATA_ROOT / "segmentations" / f"{scan}.coronary.nii.gz"))
    z = img.header.get_zooms()[:3]
    return float((z[0] + z[1]) / 2)


def _scan_of(tree) -> int:
    return int(re.match(r"(\d+)_", tree.name).group(1))


def _throat_node(path, s_arc, c):
    return int(path[int(np.argmin(np.abs(s_arc - c)))])


def _clip(ds):
    return float(min(max(ds, DS_MIN), DS_MAX))


def _make(kind: str, sign: int, ds_delta: float = DS_DELTA):
    def fn(segs, tree, path, s_arc, c, L):
        global _PENDING
        info = dict(t5_kind=kind, t5_sign=sign)
        if kind == "ds":
            dds = sign * ds_delta
        else:
            sp = inplane_spacing_mm(_scan_of(tree)) * 1e-3
            rf = float(tree.r_fit[_throat_node(path, s_arc, c)])
            # throat radius r_fit (1 - DS); a radius change of -sign * sp/4 is a DS change of +sign * sp/(4 r_fit)
            dds = sign * VOXEL_FRACTION_OF_RADIUS * sp / rf
            info.update(spacing_mm=sp * 1e3, r_fit_throat_mm=rf * 1e3)
        info["dDS_requested_pp"] = dds * 100
        name = tree.name

        def transform(ds_frac):
            req = ds_frac + dds; new = _clip(req)
            return new, dict(tree=name, ds_orig=ds_frac, ds_requested=req, ds_applied=new,
                             clipped=bool(new != req))
        _PENDING = transform
        return list(segs), info
    fn.__name__ = f"t5_{kind}_{'plus' if sign > 0 else 'minus'}"
    return fn


T5_TYPES = {
    "T5_ds_plus10": _make("ds", +1),
    "T5_ds_minus10": _make("ds", -1),
    "T5_vox_narrow": _make("vox", +1),
    "T5_vox_wide": _make("vox", -1),
}


def constant_ds_type(dds: float):
    """A T5-type function with a fixed DS change dds (fraction); used for checks."""
    return _make("ds", 1, dds)


def patched_insert(tree, path, s, c, L, ds_frac):
    global _PENDING
    if _PENDING is None:
        return _ORIG_INSERT(tree, path, s, c, L, ds_frac)
    tf, _PENDING = _PENDING, None
    ds_new, meta = tf(ds_frac)
    r_new, nodes = _ORIG_INSERT(tree, path, s, c, L, ds_new)
    th = _throat_node(path, s, c)
    meta.update(r_throat_mm=float(r_new[th] * 1e3), r_fit_throat_mm=float(tree.r_fit[th] * 1e3),
                ds_realised=float(1 - r_new[th] / tree.r_fit[th]))
    LOG.append(meta)
    return r_new, nodes


def install(types=None):
    """Swap the error-type set and the insertion function in the imported frozen modules (in memory only)."""
    global _ORIG_INSERT
    import severity_sweep, error_types, ablation
    types = dict(types or T5_TYPES)
    if _ORIG_INSERT is None:
        _ORIG_INSERT = severity_sweep.insert
    severity_sweep.insert = patched_insert
    ablation.insert = patched_insert
    error_types.ERROR_TYPES = types
    ablation.ERROR_TYPES = types
    ablation.CALIBRE_ONLY = tuple(ablation.CALIBRE_ONLY) + tuple(k for k in types if k not in ablation.CALIBRE_ONLY)
    return types
