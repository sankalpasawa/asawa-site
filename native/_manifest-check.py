#!/usr/bin/env python3
"""Native manifest completeness guard (2026-06-16). The hub index + status board render manifest.json,
so a LIVE page absent from the manifest is invisible/'missing' on the index (the bug this prevents).
FAILS (exit 1) if:
  (A) a manifest entry points at a file that does NOT exist  -> dead index link, AND
  (B) a LIVE page (native root + platform/ + products/cos/ + engineering/ + governance/ + roadmap/) is NOT in the manifest.
Archive/scaffold trees (master/, tech-design/, prd/, _ia-skeleton/) and dated/_-/archived working files are excluded.
Run: python3 holding/website/native/_manifest-check.py  (wire into ci-watcher for the 'all the time' guarantee)."""
import json, os, sys, glob, re
ROOT = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(os.path.join(ROOT, "manifest.json")))
paths = {p["path"] for p in man["pages"]}
LIVE_DIRS = ("", "platform", "platform/model", "platform/model/industry-imports", "products/cos", "products/senior-expert", "engineering", "governance", "roadmap")
def archived(name):
    return (name.startswith("_") or "archived" in name or name.startswith("STATE-")
            or name.startswith("sutra-") or name.startswith("product-prd") or name.startswith("product-design")
            or name.startswith("project-manager") or name.startswith("senior-expert-prd")
            or name in ("landing.html","native.html") or re.search(r"-2026-\d\d-\d\d", name))
live=set()
for d in LIVE_DIRS:
    for f in glob.glob(os.path.join(ROOT, d, "*.html")):
        rel=os.path.relpath(f, ROOT); 
        if not archived(os.path.basename(rel)): live.add(rel)
A=sorted(p for p in paths if not os.path.exists(os.path.join(ROOT,p)))     # dead links
B=sorted(live - paths)                                                     # live but unindexed
ok=True
if A: ok=False; print("FAIL (A) manifest entries with NO file on disk (dead index links):"); [print("   -",p) for p in A]
if B: ok=False; print("FAIL (B) LIVE pages missing from manifest (index won't list them):"); [print("   -",p) for p in B]
if ok: print("OK: %d live pages all indexed; 0 dead links."%len(live))
sys.exit(0 if ok else 1)
