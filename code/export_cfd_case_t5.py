"""
export_cfd_case_t5.py - CFD case packages for the half-voxel throat errors (T5_vox_narrow, T5_vox_wide), built
exactly as export_cfd_case.py builds any other error type.

The frozen modules are patched in memory only, as in t5_throat_run.py: the error-type set is swapped for the two
throat variants and the lesion-insertion function for the throat-modifying version, so the package's radial_scale
and r_target_mm carry the changed throat. The blinding check of export_cfd_case.py runs unchanged.

usage: export_cfd_case_t5.py <data_root> --instance <cohort row> --error T5_vox_narrow|T5_vox_wide --out <dir>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import t5_throat_error_types as T5
import export_cfd_case as E
import ablation

TYPES = {k: T5.T5_TYPES[k] for k in ("T5_vox_narrow", "T5_vox_wide")}
T5.install(TYPES)
E.insert = T5.patched_insert
E.ERROR_TYPES = TYPES
E.CALIBRE_ONLY = ablation.CALIBRE_ONLY

if __name__ == "__main__":
    T5.reset()
    E.main()
