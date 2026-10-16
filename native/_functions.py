#!/usr/bin/env python3
"""Renders the five function pages from platform/model/functions/functions.json.

  python3 _functions.py --apply   validate the template, render each page between its markers (or write the page whole if it has none)
  python3 _functions.py --check   exit 1 when the template is malformed or a page differs from a fresh render
  python3 _functions.py           print what would be rendered for adaptation

The data file is the single source: edit functions.json, then --apply, then _sidebar.py --apply and the two site guards.
The template (the same fields for all five) is enforced here: a function missing a field, a step with an unknown
inside, a journey whose meta link names no journey on the department page, or a lane the swimlane does not know,
refuses the whole render. This is the doc-level enforcement; the app's own validate is the runtime's (a build row).
"""
import json, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _journeys import swimlane  # the same swimlane as the department page

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "platform", "model", "functions", "functions.json")
JOURNEYS = os.path.join(HERE, "system", "journeys.json")
OUTDIR = os.path.join(HERE, "platform", "model", "functions")
BEGIN, END = "<!-- fn:begin (rendered by _functions.py from functions.json; do not edit by hand) -->", "<!-- fn:end -->"
INK, MUTED, GREEN, GREENBG, AMBER, AMBERBG, RED = "#111827", "#6b7280", "#047857", "#ecfdf5", "#d97706", "#fffbeb", "#b91c1c"
STYLE = '.st{font:11px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;fill:#111827}.sh{font:12px -apple-system,sans-serif;fill:#111827;font-weight:700}.sm{font:10px -apple-system,sans-serif;fill:#6b7280}.sc{font:10px -apple-system,sans-serif;fill:#047857;font-weight:700}.sa{font:10px -apple-system,sans-serif;fill:#d97706;font-weight:700}'
REQUIRED = ["id", "name", "pill", "kicker", "lead", "goal", "done", "hears", "writes", "checks", "envelope", "settings", "files", "recipe", "journeys", "roadmap"]
KINDS = {"code", "ai", "module"}


def esc(t):
    return html.escape(str(t), quote=True)


def validate(d):
    errs = []
    lanes = {k for k, _ in d["lanes"]}
    jids = {j["id"].upper() for j in json.load(open(JOURNEYS))["journeys"]}
    seen = set()
    for f in d["functions"]:
        for k in REQUIRED:
            if k not in f or f[k] in ("", [], None):
                errs.append(f'{f.get("id","?")}: missing {k}')
        if f["id"] in seen:
            errs.append(f'{f["id"]}: duplicate id')
        seen.add(f["id"])
        for s in f["recipe"]["steps"]:
            if len(s) != 4 or s[1] not in KINDS:
                errs.append(f'{f["id"]}: recipe step {s[:1]} needs [name, code|ai|module, line, line]')
        if f["recipe"]["steps"][0][1] != "code" or f["recipe"]["steps"][-1][1] != "code":
            errs.append(f'{f["id"]}: the first and last recipe step must be code (the covering)')
        for fl in f["files"]:
            if len(fl) != 3:
                errs.append(f'{f["id"]}: file row needs [name, purpose, status]')
        for r in f["roadmap"]:
            if len(r) != 3:
                errs.append(f'{f["id"]}: roadmap row needs [feature, from, status]')
        for j in f["journeys"]:
            for k in ("id", "title", "meta", "status", "steps", "edges"):
                if k not in j:
                    errs.append(f'{f["id"]}/{j.get("id","?")}: journey missing {k}')
            if not any(j["meta"].upper().startswith(x) for x in jids):
                errs.append(f'{f["id"]}/{j["id"]}: meta "{j["meta"]}" names no journey on the department page')
            for s in j["steps"]:
                if s["lane"] not in lanes:
                    errs.append(f'{f["id"]}/{j["id"]}: lane {s["lane"]} unknown')
            ns = {s["n"] for s in j["steps"]}
            for e in j["edges"]:
                if e["at"] not in ns:
                    errs.append(f'{f["id"]}/{j["id"]}: edge {e["id"]} hangs on no step')
    return errs


def engine_box(r):
    steps = r["steps"]; n = len(steps); W = 920
    bw = min(196, int((W - 60 - 18 * (n - 1)) / n)); bx0 = 40
    H = 214 + (14 if r.get("note") else 0)
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(r["title"])}: its recipe as an engine box">',
         f'<style>{STYLE}</style><defs><marker id="ah" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{INK}"/></marker></defs>',
         f'<rect x="20" y="14" width="880" height="{H - 26}" rx="10" fill="#f9fafb" stroke="{INK}" stroke-width="1.4"/>',
         f'<text class="sh" x="36" y="36">{esc(r["title"])}</text>',
         f'<text class="sm" x="36" y="50">starts on: {esc(r["starts"])} &#183; reads: {esc(r["reads"])}</text>']
    for i, (name, kind, l1, l2) in enumerate(steps):
        x = bx0 + i * (bw + 18); y = 60
        fill = GREENBG if kind == "code" else AMBERBG
        cls = "sc" if kind == "code" else "sa"
        lab = {"code": "code", "ai": "AI, an instruction", "module": "AI, a module"}[kind]
        o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="104" rx="6" fill="#fff" stroke="{INK}"/>')
        o.append(f'<rect x="{x + 6}" y="{y + 6}" width="{bw - 12}" height="14" rx="3" fill="{GREENBG}"/><text class="sc" x="{x + 12}" y="{y + 17}">cover: typed input</text>')
        o.append(f'<rect x="{x + 6}" y="{y + 26}" width="{bw - 12}" height="50" rx="3" fill="{fill}"/>')
        o.append(f'<text class="{cls}" x="{x + 12}" y="{y + 41}">{i + 1} {esc(name)} &#183; {lab}</text>')
        o.append(f'<text class="st" x="{x + 12}" y="{y + 56}">{esc(l1)}</text><text class="st" x="{x + 12}" y="{y + 70}">{esc(l2)}</text>')
        o.append(f'<rect x="{x + 6}" y="{y + 82}" width="{bw - 12}" height="14" rx="3" fill="{GREENBG}"/><text class="sc" x="{x + 12}" y="{y + 93}">cover: check, row, hand on</text>')
        if i < n - 1:
            o.append(f'<line x1="{x + bw}" y1="{y + 52}" x2="{x + bw + 16}" y2="{y + 52}" stroke="{INK}" marker-end="url(#ah)"/>')
    o.append(f'<text class="sm" x="36" y="184">writes: {esc(r["writes"])} &#183; check: {esc(r["check"])}</text>')
    if r.get("note"):
        o.append(f'<text class="sm" x="36" y="198">{esc(r["note"])}</text>')
    o.append('</svg>')
    return "".join(o)


def adaptation_parts():
    o = [f'<svg viewBox="0 0 920 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Adaptation in six parts inside the Pursue loop: sense, decide, and four hands: make, crystallize, grow, learn">',
         f'<style>{STYLE}</style><defs><marker id="ah2" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{INK}"/></marker></defs>',
         f'<rect x="300" y="10" width="320" height="34" rx="6" fill="#fff" stroke="{INK}"/><text class="sh" x="460" y="31" text-anchor="middle">IDENTITY: the goal, the rules, done when</text>',
         f'<line x1="460" y1="44" x2="460" y2="62" stroke="{INK}" marker-end="url(#ah2)"/>',
         f'<rect x="20" y="64" width="880" height="236" rx="10" fill="#f9fafb" stroke="{INK}" stroke-width="1.4"/>',
         f'<text class="sh" x="36" y="86">ADAPTATION: the department\'s intelligence &#183; the loop until the done line holds (name: placeholder, "Pursue" proposed)</text>',
         f'<rect x="40" y="100" width="180" height="60" rx="6" fill="{AMBERBG}" stroke="{AMBER}"/><text class="sa" x="52" y="118">SENSE</text><text class="st" x="52" y="133">where are we against the goal;</text><text class="st" x="52" y="147">what repeats, fails, costs</text>',
         f'<line x1="220" y1="130" x2="246" y2="130" stroke="{INK}" marker-end="url(#ah2)"/>',
         f'<rect x="248" y="100" width="180" height="60" rx="6" fill="{AMBERBG}" stroke="{AMBER}"/><text class="sa" x="260" y="118">DECIDE</text><text class="st" x="260" y="133">the next move; done when the</text><text class="st" x="260" y="147">done line holds; nothing too</text>',
         f'<line x1="428" y1="130" x2="454" y2="130" stroke="{INK}" marker-end="url(#ah2)"/>',
         f'<text class="sm" x="456" y="96">the four hands</text>']
    hands = [("MAKE", "a workflow, first version", "the Make module (S-26)", "-> ROOT checks, registers"),
             ("CRYSTALLIZE", "a step's inside up the ladder", "AI first, then code", "-> a proposal you stamp"),
             ("GROW", "the department out", "(founder; what exactly: placeholder)", "-> an ask to you"),
             ("LEARN", "what worked, what must change", "into the workflow steps", "-> ROOT checks steps")]
    for k, (name, a, b, c) in enumerate(hands):
        y = 100 + k * 48
        o.append(f'<rect x="456" y="{y}" width="424" height="40" rx="6" fill="#fff" stroke="{INK}"/>')
        o.append(f'<text class="sa" x="466" y="{y + 16}">{name}</text><text class="st" x="566" y="{y + 16}">{esc(a)}</text><text class="st" x="566" y="{y + 30}">{esc(b)}</text><text class="sc" x="742" y="{y + 23}">{esc(c)}</text>')
    o.append(f'<line x1="338" y1="160" x2="338" y2="318" stroke="{INK}" marker-end="url(#ah2)"/>')
    o.append(f'<rect x="200" y="320" width="520" height="30" rx="6" fill="{GREENBG}" stroke="{GREEN}"/><text class="sc" x="460" y="339" text-anchor="middle">the workflows, running: a result filed comes back to SENSE</text>')
    o.append(f'<path d="M 720 335 L 890 335 L 890 130 L 460 130" fill="none" stroke="{INK}" stroke-dasharray="4 3"/>')
    o.append('</svg>')
    return "".join(o)


def make_module():
    o = [f'<svg viewBox="0 0 920 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The Make module: three levels, workflow, steps, how; go down only when not confident">',
         f'<style>{STYLE}</style><defs><marker id="ah3" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{INK}"/></marker></defs>',
         f'<rect x="20" y="10" width="880" height="230" rx="10" fill="#f9fafb" stroke="{INK}" stroke-width="1.4"/>',
         f'<text class="sh" x="36" y="32">MAKE: how to make a workflow (a module; its instructions are placeholders until it is designed)</text>',
         f'<text class="sm" x="36" y="48">in: Identity\'s goal, checks and constraints; the record; the Library\'s made workflows; the compass &#183; out: one workflow, first version, with a confidence</text>']
    lv = [("level 1 &#183; the workflow", "can I state one workflow with one output?", 64),
          ("level 2 &#183; its steps", "can I state the steps, one instruction each?", 118),
          ("level 3 &#183; the how", "for a step I cannot state: find a how in the Library, derive a method, or ask the person", 172)]
    for name, q, y in lv:
        o.append(f'<rect x="40" y="{y}" width="600" height="42" rx="6" fill="{AMBERBG}" stroke="{AMBER}"/><text class="sa" x="52" y="{y + 17}">{name}</text><text class="st" x="52" y="{y + 33}">{esc(q)}</text>')
        o.append(f'<rect x="660" y="{y}" width="220" height="42" rx="6" fill="{GREENBG}" stroke="{GREEN}"/><text class="sc" x="672" y="{y + 17}">confident -> out</text><text class="st" x="672" y="{y + 33}">not confident -> one level down</text>')
        o.append(f'<line x1="640" y1="{y + 21}" x2="658" y2="{y + 21}" stroke="{INK}" marker-end="url(#ah3)"/>')
    o.append(f'<line x1="120" y1="106" x2="120" y2="116" stroke="{RED}" stroke-dasharray="3 2" marker-end="url(#ah3)"/><line x1="120" y1="160" x2="120" y2="170" stroke="{RED}" stroke-dasharray="3 2" marker-end="url(#ah3)"/>')
    o.append(f'<text class="sm" x="36" y="232">at every level: the kind of situation (clear, complicated, complex, chaotic) and the uncertainty decide: stop, go down, try small, or ask. Both logics are named and empty today.</text>')
    o.append('</svg>')
    return "".join(o)


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Native &#8212; {title}, one of the five functions</title>
<style>
body{{font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#111827;margin:0;background:#fff}}
.page{{max-width:920px;margin:0 auto;padding:34px 24px 60px}}
.crumb{{font-size:12.5px;color:#6b7280;margin-bottom:6px}}
.crumb a{{color:#1d4ed8;text-decoration:none}}
h1{{font-size:23px;margin:0 0 4px;letter-spacing:-.01em}}
table{{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0}}
th,td{{border:1px solid #e5e7eb;padding:6px 9px;text-align:left;vertical-align:top}}
th{{background:#f9fafb;font-size:11px;text-transform:uppercase;color:#6b7280}}
.pill{{display:inline-block;font-size:10.5px;font-weight:700;border-radius:99px;padding:2px 9px;background:#ecfdf5;color:#047857;vertical-align:middle}}
h2{{font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:#6b7280;margin:24px 0 8px}}
h3{{font-size:15px;margin:18px 0 6px}}
.note{{background:#f8fafc;border-left:3px solid #64748b;padding:8px 12px;font-size:13px;margin:14px 0}}
.lead{{font-size:15px}}
.figcap{{font-size:11.5px;color:#9ca3af;margin:0 0 8px}}
svg{{width:100%;height:auto;display:block;margin:6px 0}}
a{{color:#1d4ed8;text-decoration:none}}a:hover{{text-decoration:underline}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style>
</head>
<body><div class="page">
"""
FOOT = "\n</div></body></html>\n"


def render(f, d, order):
    lanes = [tuple(x) for x in d["lanes"]]
    sibs = " &#183; ".join((f'<b>{esc(g["name"])}</b>' if g["id"] == f["id"] else f'<a href="{g["id"]}.html">{esc(g["name"])}</a>') for g in order)
    o = [BEGIN,
         f'<div class="crumb"><a href="../../../index.html">Native hub</a> &#8250; <a href="../internal-system.html">the five functions</a> &#8250; {esc(f["name"].lower())}</div>',
         f'<h1>{esc(f["name"])} <span class="pill">{esc(f["pill"])}</span></h1>',
         f'<p class="lead"><b>{esc(f["kicker"])}.</b> {esc(f["lead"])}</p>',
         '<div class="note"><b>One template for all five</b> (founder, 2026-09-30): each function is a system of its own, with its own goal, workflows and journeys, in the box shape; version 1 is one AI agent with .md files inside the covering (S-28). This page is rendered from <code>functions.json</code>; a field the founder has not ruled says placeholder; <code>_functions.py --check</code> refuses a malformed template or a hand edit.</div>']
    if f["id"] == "adaptation":
        o.append('<h2 id="parts">What it is, in six parts, inside the loop</h2>')
        o.append(adaptation_parts())
        o.append('<p class="figcap">Sense and Decide are the intelligence; Make, Crystallize, Grow and Learn are its hands; the dashed line is the loop: a result filed comes back to Sense until the done line holds. Amber is AI; green is code or Root\'s check.</p>')
        o.append('<h2 id="make">The Make hand: how to make a workflow</h2>')
        o.append(make_module())
        o.append('<p class="figcap">Three levels; a first version is always made; going down a level is the only move when not confident (S-26). The instructions at each level are placeholders until the module is designed.</p>')
        o.append('<h2 id="compass">The compass: the six families, and the department\'s how methodology</h2>')
        o.append('<p>Founder, 2026-09-30: the department carries a how methodology. It holds a compass of all six families and the values on them, so that when a workflow is being made, the next step is chosen with those values in view. The families are Native\'s (<a href="../../../axes.html">axes and families</a>); the values on each are yours to rule and are placeholders here.</p>')
        o.append('<table><tr><th>Family</th><th>What it covers (from the axes page)</th><th>The value this department holds</th></tr>')
        for fam, cov in [("SHAPE", "what the work is for, and how we know it is right"), ("GROW", "what accumulates across runs"), ("GOVERN", "who may do what; what needs a yes"), ("EDGE", "hand-offs, shared resources, what must cohere"), ("RESOURCE", "a finite stock the work spends"), ("TIME", "when, how often, how long")]:
            o.append(f'<tr><td><b>{fam}</b></td><td>{esc(cov)}</td><td><i>placeholder: the value, in your words</i></td></tr>')
        o.append('</table>')
        o.append('<p class="note"><b>Where the compass is read</b>: placeholder. Founder\'s words: "next time someone is producing a workflow, it takes account of various values which it needs to figure out for the next step."</p>')
    o.append(f'<div class="note" style="border-left-color:#047857"><b>In version 1</b> (make a site live, nothing more; founder 2026-09-30): {esc(f.get("v1", "placeholder"))}</div>')
    o.append('<h2 id="template">The template, filled for this function</h2>')
    o.append('<table><tr><th>Field</th><th>This function</th></tr>')
    o.append(f'<tr><td>goal</td><td>{esc(f["goal"])}</td></tr><tr><td>done</td><td>{esc(f["done"])}</td></tr>')
    o.append(f'<tr><td>hears</td><td>{"; ".join(esc(x) for x in f["hears"])}</td></tr><tr><td>writes</td><td>{"; ".join(esc(x) for x in f["writes"])}</td></tr>')
    o.append(f'<tr><td>checks (covering)</td><td>{"; ".join(esc(x) for x in f["checks"])}</td></tr><tr><td>envelope</td><td>{esc(f["envelope"])}</td></tr><tr><td>settings</td><td>{esc(f["settings"])}</td></tr></table>')
    o.append('<h3 id="files">Version 1: one AI agent and its .md files (S-28)</h3>')
    o.append('<table><tr><th>File</th><th>What it holds</th><th>Status</th></tr>')
    for name, purpose, st in f["files"]:
        o.append(f'<tr><td><code>{esc(name)}</code></td><td>{esc(purpose)}</td><td>{esc(st)}</td></tr>')
    o.append('</table>')
    o.append('<h2 id="recipe">Its recipe, as an engine box</h2>')
    o.append(engine_box(f["recipe"]))
    o.append('<p class="figcap">Green is the covering (code); amber is an inside (AI). Every inside is born AI and goes over the ladder to code (S-22).</p>')
    o.append('<h2 id="journeys">Its journeys, and the meta journey step each serves</h2>')
    o.append('<table><tr><th>#</th><th>Journey</th><th>Serves</th><th>Status</th></tr>')
    for j in f["journeys"]:
        o.append(f'<tr><td><a href="#{esc(j["id"])}">{esc(j["id"].upper())}</a></td><td>{esc(j["title"])}</td><td><a href="../../../system/department.html#{esc(j["meta"].split()[0].lower())}">{esc(j["meta"])}</a></td><td>{esc(j["status"])}</td></tr>')
    o.append('</table>')
    for j in f["journeys"]:
        o.append(f'<h3 id="{esc(j["id"])}">{esc(j["id"].upper())} &#183; {esc(j["title"])} <span style="font-size:11px;color:{MUTED}">serves {esc(j["meta"])} &#183; {esc(j["status"])}</span></h3>')
        jj = {"id": j["id"], "title": j["title"], "steps": j["steps"], "edges": j["edges"]}
        o.append(f'<div class="jflow" data-j="{esc(j["id"])}">{swimlane(jj, lanes)}</div>')
    o.append('<h2 id="screens">Its screens</h2>')
    o.append('<p>Every screen lives in one place: <a href="../screens.html">Screens, all in one place</a>. The ones that draw this function:</p>')
    if f.get("screens"):
        o.append('<table><tr><th>Screen</th><th>Note</th></tr>')
        for label, href, note in f["screens"]:
            o.append(f'<tr><td><a href="{esc(href)}">{esc(label)}</a></td><td>{esc(note)}</td></tr>')
        o.append('</table>')
    else:
        o.append('<p><i style="color:#b45309">needs to be filled</i>: no screen of its own yet; it appears in <a href="../screens-3-messages.html">Internal messages</a> (to confirm).</p>')
    o.append('<h2 id="roadmap">Roadmap: the structure added over time</h2>')
    o.append('<p>Founder, 2026-09-30: version 1 is the agent and its .md files; the features below are added over time and give the function its structure. Each row names where it came from and where it stands.</p>')
    o.append('<table><tr><th>#</th><th>Feature</th><th>From</th><th>Status</th></tr>')
    for k, (feat, frm, st) in enumerate(f["roadmap"], 1):
        o.append(f'<tr><td>R{k}</td><td>{esc(feat)}</td><td>{esc(frm)}</td><td>{esc(st)}</td></tr>')
    o.append('</table>')
    o.append('<h2 id="siblings">The five</h2>')
    o.append(f'<p>{sibs}</p>')
    o.append('<h2 id="sources">Sources</h2>')
    o.append('<p>functions.md and the docs set beside the code (sutra 50599599, ef0e8c39); the founder\'s rulings of 2026-09-29/30 (S-05 to S-28); <a href="../../../system/engines.html#box">the box</a>; <a href="../../../system/department.html#journeys">the department\'s journeys</a>.</p>')
    o.append('<h2 id="provenance">Provenance</h2>')
    o.append(f'<p style="font-size:12px;color:{MUTED}">author: claude, session 32a8a0a6, 2026-09-30 &#183; rendered from functions.json version {esc(d["version"])} &#183; every row says built, partly, to build or placeholder &#183; review: none by a second model &#183; confidence: high on what is built; the placeholders are the founder\'s to fill.</p>')
    o.append(END)
    return "\n".join(o)


def main():
    d = json.load(open(DATA))
    errs = validate(d)
    if errs:
        print("functions: the template is malformed:"); [print("  -", e) for e in errs]; sys.exit(1)
    order = d["functions"]
    apply, check = "--apply" in sys.argv, "--check" in sys.argv
    bad = 0
    for f in order:
        out = render(f, d, order)
        path = os.path.join(OUTDIR, f["id"] + ".html")
        if not (apply or check):
            if f["id"] == "adaptation": print(out)
            continue
        page = open(path).read() if os.path.exists(path) else ""
        i, k = page.find(BEGIN), page.find(END)
        if i < 0 or k < 0:
            if check:
                print(f"functions: {f['id']}.html has no markers"); bad += 1; continue
            open(path, "w").write(HEAD.format(title=f["name"]) + out + FOOT); print(f"functions: wrote {f['id']}.html whole"); continue
        cur = page[i:k + len(END)]
        if check:
            if cur != out:
                print(f"functions: {f['id']}.html differs from a fresh render"); bad += 1
            continue
        open(path, "w").write(page[:i] + out + page[k + len(END):]); print(f"functions: applied {f['id']}.html")
    if check:
        if bad: sys.exit(1)
        print(f"OK: {len(order)} function pages match functions.json; the template validates")


if __name__ == "__main__":
    main()
