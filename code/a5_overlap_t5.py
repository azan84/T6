"""
a5_overlap_t5.py - tube-model overlap and topology metrics for the two half-voxel throat errors (T5_vox_narrow,
T5_vox_wide), computed exactly as in a5_overlap_metrics.py.

The frozen modules are patched in memory only, as in t5_throat_run.py: the error-type set is swapped for the two
throat variants and the lesion-insertion function for the throat-modifying version. Patches are applied at import so
that spawned workers carry them.

usage: a5_overlap_t5.py <data_root> <cohort.csv> <out_dir> [--limit N] [--workers K]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import t5_throat_error_types as T5
import a5_overlap_metrics as A5
import ablation

TYPES = {k: T5.T5_TYPES[k] for k in ("T5_vox_narrow", "T5_vox_wide")}
T5.install(TYPES)
A5.insert = T5.patched_insert
A5.ERROR_TYPES = TYPES
A5.CALIBRE_ONLY = ablation.CALIBRE_ONLY
_RUN = A5.run_instance


def run_instance(args):
    T5.reset()
    return _RUN(args)


A5.run_instance = run_instance

if __name__ == "__main__":
    A5.main()
