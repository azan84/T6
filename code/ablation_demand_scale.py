"""ablation_demand_scale.py — STATISTICS-PLAN §10 demand-model sensitivity: run the frozen ablation.py unchanged with
the hyperaemic demand constant K_MURRAY scaled by a factor (0.7 / 1.3). zerod_ffr.Tree.demand reads the module global
at call time, so patching it before ablation.main() scales every Murray-demand calibration (clean, Protocol B, C
targets). usage: ablation_demand_scale.py <scale> <data_root> --out <csv>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import zerod_ffr
scale = float(sys.argv.pop(1))
zerod_ffr.K_MURRAY = 562.0 * scale
import ablation
ablation.K_MURRAY = zerod_ffr.K_MURRAY
print(f"demand scale {scale}: K_MURRAY = {zerod_ffr.K_MURRAY:.1f} s^-1", flush=True)
ablation.main()
