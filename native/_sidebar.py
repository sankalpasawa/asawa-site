#!/usr/bin/env python3
"""Sidebar consistency guard. Every eligible native page must carry the canonical
sidebar (_sidebar.html), depth-adjusted + current-marked. Fails (exit 1) on drift,
AND on ABSENCE for manifest-listed pages (2026-08-04: a page built from _template.html
shipped with no nav; the old 'continue' skipped it silently — codex-reviewed ADVISORY).
Run: python _sidebar.py --check   (or --apply to normalize + inject missing navs)."""
import re,glob,os,sys,json
ROOT=os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
canon=open("_sidebar.html").read()

SIDEBAR_CSS='''.layout{display:flex;gap:0;max-width:1240px;margin:0 auto;align-items:flex-start}
.sidebar{width:212px;min-width:212px;border-right:1px solid #e5e7eb;padding:22px 12px 40px 16px;font-size:12px;line-height:1.85;position:sticky;top:0;max-height:100vh;overflow:auto}
.sidebar a{color:#374151;text-decoration:none}.sidebar a:hover{color:#1d4ed8}
.sb-cur{font-weight:800;color:#b45309 !important}
.sb-band{font-size:9.5px;font-weight:800;letter-spacing:.07em;color:#9ca3af;margin-top:9px}
.sb-title{font-size:10px;font-weight:800;letter-spacing:.08em;color:#6b7280;margin-bottom:4px}'''

def excluded(rel):
    b=os.path.basename(rel)
    if b.startswith("_") or b.startswith("STATE-") or b.startswith("product-prd") or b.startswith("sutra-"): return True
    if re.match(r"\d{4}-\d{2}-\d{2}", b): return True
    for seg in ("master/","prd/","tech-design/","_ia-skeleton/","archive"):
        if seg in rel: return True
    return "archived" in rel

def manifest_paths():
    try:
        m=json.load(open("manifest.json"))
        return {p.get("path") for p in m.get("pages",[]) if p.get("path")}
    except Exception:
        return set()

def gen(rel):
    pre="../"*rel.count("/")
    n=re.sub(r'href="(?!https?:)([^"]+)"', lambda m: 'href="%s%s"'%(pre,m.group(1)), canon)
    tgt='href="%s%s"'%(pre,rel)
    return n.replace("<a "+tgt, '<a class="sb-cur" '+tgt)

def inject(rel,h):
    """Inject the canonical sidebar into a manifest page with no nav.
    Narrow by design (codex): exact '<body><div class="page">' shape only,
    idempotence guarded by nav/layout/CSS checks; anything else is reported."""
    if '<nav class="sidebar">' in h or 'class="layout"' in h: return None,"already has nav/layout"
    sb=gen(rel)
    if 'class="sb-cur"' not in sb: return None,"canonical sidebar has no row for this page — add one to _sidebar.html"
    if h.count('<body><div class="page">')!=1: return None,"page shape differs from '<body><div class=\"page\">'"
    if not h.rstrip().endswith('</div></body></html>'): return None,"page close differs from '</div></body></html>'"
    if '.layout{' not in h: h=h.replace("</style>", SIDEBAR_CSS+"\n</style>",1)
    h=h.replace('<body><div class="page">','<body><div class="layout">'+sb+'<div class="page">',1)
    h=re.sub(r'</div></body></html>\s*$','</div></div></body></html>\n',h)
    return h,None

files=glob.glob("*.html")+glob.glob("*/*.html")+glob.glob("*/*/*.html")+glob.glob("*/*/*/*.html")
apply="--apply" in sys.argv
manifest=manifest_paths()
drift=[]; missing=[]; skipped=[]; info=[]
for f in sorted(files):
    if excluded(f): continue
    h=open(f).read()
    if '<nav class="sidebar">' not in h:
        if f in manifest:
            if apply:
                new,why=inject(f,h)
                if new is None: skipped.append((f,why))
                else: open(f,"w").write(new); print("sidebar: injected ->",f)
            else:
                missing.append(f)
        else:
            info.append(f)
        continue
    want=gen(f); cur=re.search(r'<nav class="sidebar">.*?</nav>', h, re.S).group(0)
    if cur!=want:
        if apply: open(f,"w").write(h.replace(cur,want,1))
        else: drift.append(f)
if apply:
    print("sidebar: normalized")
    for f,why in skipped: print("  SKIPPED (needs manual fix): %s — %s"%(f,why))
    sys.exit(1 if skipped else 0)
fail=False
if drift:
    fail=True
    print("SIDEBAR DRIFT (%d pages differ from _sidebar.html):"%len(drift))
    for d in drift[:20]: print("  -",d)
if missing:
    fail=True
    print("SIDEBAR MISSING (%d manifest pages have NO nav — run --apply or fix shape):"%len(missing))
    for d in missing[:20]: print("  -",d)
if fail: sys.exit(1)
if info:
    print("note: %d non-manifest pages carry no sidebar (exempt): %s"%(len(info),", ".join(info[:6])))
print("OK: all eligible pages share the canonical sidebar")
