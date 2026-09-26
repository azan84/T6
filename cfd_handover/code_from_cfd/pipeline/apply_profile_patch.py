"""One-off patch: make the location/severity constants of the lesion pipeline come from lesion_profile.PR (default profile = the audited lesion80, so behaviour is unchanged).
Every replacement must match EXACTLY the expected number of times or the script aborts without writing that file. Originals are in profile_orig/."""
import sys
R = {
"build_lesion80_surface.py": [
 ('S_C, LEN, DS_FRAC = 23.5, 10.0, 0.80         # window centre (mm arc from ostium), length, diameter stenosis',
  'from lesion_profile import PR\nS_C, LEN, DS_FRAC = PR["S_C"], PR["LEN"], PR["DS"]   # window centre (mm arc from ostium), length, diameter stenosis (profile; default = audited lesion80)', 1),
 ('LAD_SID = 2                                    # 0D segment holding the window (seg2 = proximal LAD, arc 15.0-32.0)',
  'LAD_SID = PR["SID"]                            # 0D segment holding the window (lesion80: seg2 = proximal LAD, arc 15.0-32.0; lesion_mid: seg3, arc 32.9-70.7)', 1),
 ('keep = arc_poly < 60.0                         # only the proximal part is needed', 'keep = arc_poly < PR["KEEP"]                # only the part up to the profile\'s KEEP arc is needed', 1),
 ('f"{BASE}/lesion80/lesion80_open.vtp"', 'f"{BASE}/{PR[\'DIR\']}/{PR[\'OPEN\']}"', 1)],
"verify_lesion80_geometry.py": [
 ('pv.read(f"{BASE}/lesion80/lesion80_open.vtp")', 'pv.read(f"{BASE}/{G.PR[\'DIR\']}/{G.PR[\'OPEN\']}")', 1),
 ('open(f"{BASE}/lesion80/geometry_verification.json", "w")', 'open(f"{BASE}/{G.PR[\'DIR\']}/geometry_verification.json", "w")', 1)],
"verify_lesion80_extra.py": [
 ('pv.read(f"{BASE}/lesion80/lesion80_open.vtp")', 'pv.read(f"{BASE}/{G.PR[\'DIR\']}/{G.PR[\'OPEN\']}")', 1),
 ('open(f"{BASE}/lesion80/geometry_verification_extra.json", "w")', 'open(f"{BASE}/{G.PR[\'DIR\']}/geometry_verification_extra.json", "w")', 1)],
"lesion_sections.py": [
 ('from build_lesion80_surface import build_frames, f_of_s, S_C, LEN, LAD_SID', 'from build_lesion80_surface import build_frames, f_of_s, S_C, LEN, LAD_SID, PR', 1),
 ('a = np.arange(1.0, S_C - 6.0 - 1e-9, 1.5)', 'a = np.arange(PR["SEC_START"], S_C - 6.0 - 1e-9, 1.5)', 1),
 ('c = np.arange(S_C + 6.0 + 1.5, 50.0, 1.5)', 'c = np.arange(S_C + 6.0 + 1.5, PR["SEC_END"], 1.5)', 1),
 ('json.load(open(f"{BASE}/lesion80/geometry_verification.json"))', 'json.load(open(f"{BASE}/{PR[\'DIR\']}/geometry_verification.json"))', 1)],
"reattachment_wss.py": [
 ('S_JUNCTION = 30.0          # D1 ostium at arc 32.0, proximal edge ~30-30.5', 'S_JUNCTION = G.PR["JUNCTION"]   # lesion80: D1 ostium at arc 32.0, proximal edge ~30-30.5 (profile value)', 1),
 ('for st in np.arange(15.0, 45.0 + 1e-9, DS):', 'for st in np.arange(G.PR["WSS_START"], G.PR["WSS_END"] + 1e-9, DS):', 1)],
"compare_lesion.py": [
 ('from build_lesion80_surface import S_C', 'from build_lesion80_surface import S_C, PR', 1),
 ('dict(prox_to_throat=(18.5, S_C), throat_to_distal=(S_C, 29.5), prox_to_distal=(18.5, 29.5))', 'dict(prox_to_throat=(PR["S_UP"], S_C), throat_to_distal=(S_C, PR["S_DOWN"]), prox_to_distal=(PR["S_UP"], PR["S_DOWN"]))', 1),
 ('(ok_l.s_mm < 30.0)]', '(ok_l.s_mm < PR["JUNCTION"])]', 1),
 ('a.axvline(32.05, color="gray", ls=":", lw=0.7)', 'a.axvline(PR["JUNCTION_OSTIUM"], color="gray", ls=":", lw=0.7)', 3),
 ('a.axvline(30.0, color="gray", lw=0.5)', 'a.axvline(PR["JUNCTION"], color="gray", lw=0.5)', 1),
 ('a.set_xlim(15, 40)', 'a.set_xlim(*PR["XLIM"])', 3)],
"make_lesion_mesh.py": [
 ('from outlets_837 import build_tree', 'from outlets_837 import build_tree\nfrom lesion_profile import PR', 1),
 ('s0, s1 = 17.5, (36.0 if TUBE_END is None else TUBE_END)', 's0, s1 = PR["TUBE_START"], (PR["TUBE_END"] if TUBE_END is None else TUBE_END)', 1),
 ('    d1 = [sg for sg in T.segments if sg.label == "D1"][0]\n    Pd = d1.pts * 1e3\n    dd = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Pd, axis=0), axis=1))])\n    chain(Pd[dd <= 12.0], "d1", lambda a: ALL_REQ if ALL_REQ is not None else COARSE)\n',
  '    if PR["D1_CHAIN"]:      # the proximal-LAD lesion\'s jet impinges on the D1 ostium; the isolated lesion has no such junction\n        d1 = [sg for sg in T.segments if sg.label == "D1"][0]\n        Pd = d1.pts * 1e3\n        dd = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Pd, axis=0), axis=1))])\n        chain(Pd[dd <= 12.0], "d1", lambda a: ALL_REQ if ALL_REQ is not None else COARSE)\n', 1),
 ('("jet_zone_to_D1", G.S_C + 6, 32.0)', '("jet_zone_to_D1", G.S_C + 6, PR["JET_END"])', 1),
 ('json.load(open(f"{BASE}/lesion80/lesion80_open_info.json"))', 'json.load(open(f"{BASE}/{PR[\'DIR\']}/" + PR["OPEN"].replace(".vtp", "_info.json")))', 1)],
"build_lesion80_case.py": [
 ('from build_lesion80_surface import build_frames, f_of_s, S_C, LEN, LAD_SID', 'from build_lesion80_surface import build_frames, f_of_s, S_C, LEN, LAD_SID, PR', 1),
 ('json.load(open(f"{BASE}/lesion80/geometry_verification.json"))', 'json.load(open(f"{BASE}/{PR[\'DIR\']}/geometry_verification.json"))', 1)],
"mesh_local_verification.py": [
 ('for s in np.arange(17.5, 32.0 + 1e-9, 0.25):', 'for s in np.arange(G.PR["LOCAL_LO"], G.PR["LOCAL_HI"] + 1e-9, 0.25):', 1),
 ('for s in (8.0, 18.5, 21.0, 22.5, G.S_C, 24.5, 26.0, 28.5, 31.0):', 'for s in [G.S_C if x == "S_C" else x for x in G.PR["BL_STATIONS"]]:', 1)],
"mesh_failed_sets_general.py": [
 ('inside = (s >= 18.5) & (s <= 32.0) & (d < 3.0)', 'inside = (s >= G.PR["TUBE_LO"]) & (s <= G.PR["TUBE_HI"]) & (d < 3.0)', 1),
 ('bins=np.arange(18, 33, 1.0)', 'bins=np.arange(G.PR["TUBE_LO"] - 0.5, G.PR["TUBE_HI"] + 1.0, 1.0)', 1)],
}
for fn, reps in R.items():
    s = open(fn).read(); o = s
    for old, new, n in reps:
        c = s.count(old)
        if c != n: sys.exit(f"{fn}: expected {n} occurrence(s) of {old[:70]!r}, found {c}; nothing written for this file")
        s = s.replace(old, new)
    open(fn, "w").write(s); print("patched", fn, len(reps), "replacements")
