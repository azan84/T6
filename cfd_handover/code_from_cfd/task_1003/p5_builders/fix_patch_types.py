"""cfMesh writes 'type wall;' for every patch it creates from the STL solids. The case builder (pf/build_m1_case.py) requires the inlet and out_<id> patches to be type 'patch'. This mesh-side step edits
constant/polyMesh/boundary of a mesh dir ONLY (text file; geometry/topology untouched) and records the change. usage: fix_patch_types.py <mesh_dir>"""
import sys, re, json, os
d = sys.argv[1]; f = f"{d}/constant/polyMesh/boundary"; t = open(f).read(); ch = []
def sub(m):
    name = m.group(1)
    if name in ("wall", "FoamFile"): return m.group(0)
    ch.append(name); return m.group(0).replace("type            wall;", "type            patch;").replace("type wall;", "type patch;")
new = re.sub(r"\n(\w+)\s*\n\{[^}]*\}", lambda m: sub(re.match(r"\n(\w+)", m.group(0)) and type("M", (), {"group": lambda self, i=0, _m=m: (_m.group(1) if i == 1 else _m.group(0))})()), t)
if not ch or new == t and "type patch" not in t: raise SystemExit("nothing changed / unexpected boundary format")
open(f, "w").write(new); json.dump(dict(patches_set_to_type_patch=ch, note="cfMesh writes type wall for all STL-solid patches; only the type keyword was edited"), open(f"{d}/patch_types_fixed.json", "w"), indent=1); print("set to patch:", ch)
