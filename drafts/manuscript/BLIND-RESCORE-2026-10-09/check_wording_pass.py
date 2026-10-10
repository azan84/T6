#!/usr/bin/env python3
"""Check (and optionally apply) the OLD/NEW replacements in WORDING-PASS-G3.md.

Usage, from drafts/manuscript/:
  python3 BLIND-RESCORE-2026-10-09/check_wording_pass.py                 # verify every OLD matches exactly once
  python3 BLIND-RESCORE-2026-10-09/check_wording_pass.py --apply OUTDIR  # write patched copies of the three files to OUTDIR
  python3 BLIND-RESCORE-2026-10-09/check_wording_pass.py --apply OUTDIR --groups required,house   # subset

Groups: required, offset, house. Item ids can be excluded with --exclude M23,M31.
The md format: "### <ID>" heading, a line "File: <path> | Group: <group>", then "OLD:" and "NEW:" each
followed by a ```text fenced block whose content (without the fence lines) is the exact string.
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # drafts/manuscript
MD = os.path.join(HERE, "WORDING-PASS-G3.md")


def parse(md_text):
    items = []
    blocks = re.split(r"^### (?=[MST]\d\d\b)", md_text, flags=re.M)[1:]
    for b in blocks:
        iid = b.split("\n", 1)[0].split()[0]
        m = re.search(r"^File: `([^`]+)` \| Group: (\w+)", b, re.M)
        fences = re.findall(r"^(OLD|NEW):\n```text\n(.*?)\n?```", b, re.M | re.S)
        d = {k: v for k, v in fences}
        if not m or "OLD" not in d or "NEW" not in d:
            sys.exit(f"parse error in item {iid}")
        items.append(dict(id=iid, file=m.group(1), group=m.group(2), old=d["OLD"], new=d["NEW"]))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", metavar="OUTDIR")
    ap.add_argument("--groups", default="required,offset,house")
    ap.add_argument("--exclude", default="")
    a = ap.parse_args()
    groups = set(a.groups.split(","))
    exclude = set(x for x in a.exclude.split(",") if x)
    items = parse(open(MD, encoding="utf-8").read())
    files = sorted({it["file"] for it in items})
    texts = {f: open(os.path.join(ROOT, f), encoding="utf-8").read() for f in files}
    bad = 0
    for it in items:
        n = texts[it["file"]].count(it["old"])
        flag = "" if n == 1 else "  <-- MATCH ERROR"
        if n != 1: bad += 1
        print(f"{it['id']}  {it['group']:8}  {it['file']:40}  matches={n}{flag}")
    print(f"{len(items)} items, {bad} match errors")
    if a.apply and not bad:
        os.makedirs(a.apply, exist_ok=True)
        for f in files:
            t = texts[f]
            for it in items:
                if it["file"] == f and it["group"] in groups and it["id"] not in exclude:
                    t = t.replace(it["old"], it["new"], 1)
            out = os.path.join(a.apply, f)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "w", encoding="utf-8").write(t)
            print("wrote", out)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
