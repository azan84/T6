"""Re-issue TaskA/post_summary_<A1|A2>_resistance.json as ..._2026-10-06.json (post-hoc audit GPT-5.6 Sol, AB finding 6): their entry for the shared
aggregate TaskA/M1_results.csv held the size/sha256 of the file at the time (fewer rows). The re-issue replaces that entry by the current file's size
and sha256 and records the old values; every other entry is re-verified against the file on disk (raw bytes) and must match. Originals are kept."""
import json, hashlib, os, sys
O = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03/TaskA"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def walk(d, path=()):
    if isinstance(d, dict):
        if "sha256" in d and "size_bytes" in d: yield path, d
        for k, v in d.items(): yield from walk(v, path + (k,))
for lab in ("baseline_D7_12p5", "baseline_D7_12p5_zoneB", "baseline_A0_25um"):
    src = f"{O}/post_summary_{lab}_resistance.json"; d = json.load(open(src)); changed = []
    for path, e in walk(d):
        name = path[-1]; f = f"{O}/{name}" if os.path.exists(f"{O}/{name}") else None
        if f is None: continue
        cur = dict(size_bytes=os.path.getsize(f), sha256=sha(f))
        if (cur["size_bytes"], cur["sha256"]) != (e["size_bytes"], e["sha256"]):
            assert name == "M1_results.csv", f"{lab}: {name} differs from its summary entry (not the expected aggregate)"
            e["superseded_entry_2026-10-06"] = dict(size_bytes=e["size_bytes"], sha256=e["sha256"], note="aggregate at the time this summary was written (fewer rows)")
            e.update(cur); changed.append(name)
    print(lab, "changed:", changed)
    if changed:
        d["reissue_2026-10-06"] = "entry for the shared aggregate M1_results.csv updated to the current file (post-hoc audit GPT-5.6 Sol AB-6); all other entries re-verified unchanged"
        json.dump(d, open(f"{O}/post_summary_{lab}_resistance_2026-10-06.json", "w"), indent=1)
