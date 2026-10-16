#!/usr/bin/env python3
"""Renders the journeys section of system/department.html from system/journeys.json.

  python3 _journeys.py --apply   render and splice between the markers in system/department.html
  python3 _journeys.py --check   exit 1 when the page's section differs from a fresh render (a guard)
  python3 _journeys.py           print the rendered section

The data file is the single source: edit system/journeys.json, then --apply, then the two site guards.
Three views of the same rows: the block diagram (blocks, links), one swimlane per journey (steps by lane,
edges in red under the step they hang on) and the tables (steps, edges, directions). Never edit the
rendered HTML or SVG by hand; --check will refuse the page. Standard notation: rounded box = a step,
diamond = your stamp, lane = who acts, solid arrow = the happy path, red dashed stub = an edge case
named by its row id. Charter: Engine Library ("stochastic reasoning rides on deterministic primitives").
"""
import json, os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "system", "journeys.json")
PAGE = os.path.join(HERE, "system", "department.html")
BEGIN, END = "<!-- journeys:begin (rendered by _journeys.py from system/journeys.json; do not edit by hand) -->", "<!-- journeys:end -->"
INK, MUTED, LINE, ACC, RED, OK = "#111827", "#6b7280", "#e5e7eb", "#1d4ed8", "#b91c1c", "#166534"


def esc(t):
    return html.escape(str(t), quote=True)


def swimlane(j, lanes):
    steps, edges = j["steps"], j["edges"]
    n = len(steps)
    lx, cw, bw, bh, lh, top = 96, 100, 84, 30, 40, 22
    W = lx + n * cw + 16
    lane_i = {k: i for i, (k, _) in enumerate(lanes)}
    used = sorted({lane_i[s["lane"]] for s in steps})
    row = {li: r for r, li in enumerate(used)}
    Hlanes = top + len(used) * lh
    # edges under the diagram: one red row per step column that has edges
    by_step = {}
    for e in edges:
        by_step.setdefault(e["at"], []).append(e)
    maxe = max([len(v) for v in by_step.values()] + [0])
    eh = 24  # two lines per edge: the row id, then a few words, kept inside the column
    H = Hlanes + 14 + (maxe * eh + 10 if maxe else 0)
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(j["title"])}: the happy path by lane, the edges in red">']
    o.append(f'<style>.jt{{font:10px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;fill:{INK}}}.jl{{font:9.5px -apple-system,sans-serif;fill:{MUTED};font-weight:700;letter-spacing:.04em}}.je{{font:9px -apple-system,sans-serif;fill:{RED}}}</style>')
    o.append(f'<defs><marker id="ah{j["id"]}" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{INK}"/></marker></defs>')
    for li in used:
        y = top + row[li] * lh
        o.append(f'<rect x="0" y="{y}" width="{W}" height="{lh}" fill="{"#f9fafb" if row[li] % 2 else "#fff"}"/>')
        o.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{LINE}"/>')
        o.append(f'<text class="jl" x="8" y="{y + lh / 2 + 3}">{esc(lanes[li][1].upper())}</text>')
    o.append(f'<line x1="0" y1="{Hlanes}" x2="{W}" y2="{Hlanes}" stroke="{LINE}"/>')
    pos = []
    for i, s in enumerate(steps):
        cx = lx + i * cw + cw / 2
        cy = top + row[lane_i[s["lane"]]] * lh + lh / 2
        pos.append((cx, cy))
        stamp = s["lane"] == "you" and s["short"].lower().startswith("stamp")
        if stamp:
            o.append(f'<polygon points="{cx},{cy - bh / 2 - 2} {cx + bw / 2 - 8},{cy} {cx},{cy + bh / 2 + 2} {cx - bw / 2 + 8},{cy}" fill="#fffbeb" stroke="#92400e" stroke-width="1.2"/>')
        else:
            fill = "#eef2ff" if s["lane"] == "engine" else "#fff"
            o.append(f'<rect x="{cx - bw / 2}" y="{cy - bh / 2}" width="{bw}" height="{bh}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="1"/>')
        words = s["short"].split()
        l1, l2 = (" ".join(words[:2]), " ".join(words[2:])) if len(words) > 2 else (s["short"], "")
        if l2:
            o.append(f'<text class="jt" x="{cx}" y="{cy - 2}" text-anchor="middle">{esc(l1)}</text><text class="jt" x="{cx}" y="{cy + 9}" text-anchor="middle">{esc(l2)}</text>')
        else:
            o.append(f'<text class="jt" x="{cx}" y="{cy + 3.5}" text-anchor="middle">{esc(l1)}</text>')
        o.append(f'<text class="jl" x="{cx - bw / 2}" y="{cy - bh / 2 - 3}">{esc(s["n"])}</text>')
    for i in range(1, n):
        (x0, y0), (x1, y1) = pos[i - 1], pos[i]
        if abs(y0 - y1) < 1:
            o.append(f'<line x1="{x0 + bw / 2}" y1="{y0}" x2="{x1 - bw / 2 - 1}" y2="{y1}" stroke="{INK}" stroke-width="1" marker-end="url(#ah{j["id"]})"/>')
        else:
            xm = x0 + bw / 2 + (cw - bw) / 2
            o.append(f'<polyline points="{x0 + bw / 2},{y0} {xm},{y0} {xm},{y1} {x1 - bw / 2 - 1},{y1}" fill="none" stroke="{INK}" stroke-width="1" marker-end="url(#ah{j["id"]})"/>')
    if maxe:
        o.append(f'<rect x="0" y="{Hlanes}" width="{W}" height="{H - Hlanes}" fill="#fff5f5"/>')
        o.append(f'<text class="jl" x="8" y="{Hlanes + 14}" style="fill:{RED}">IF IT GOES WRONG</text>')
        for i, s in enumerate(steps):
            es = by_step.get(s["n"], [])
            if not es:
                continue
            cx = pos[i][0]
            o.append(f'<line x1="{cx}" y1="{pos[i][1] + bh / 2 + 1}" x2="{cx}" y2="{Hlanes + 6}" stroke="{RED}" stroke-width="1" stroke-dasharray="3 2"/>')
            for k, e in enumerate(es):
                y = Hlanes + 14 + k * eh + 12
                short = e["short"] if len(e["short"]) <= 18 else e["short"][:17].rstrip() + "&#8230;"
                o.append(f'<text class="je" x="{cx}" y="{y}" text-anchor="middle" font-weight="700">{esc(e["id"])}</text>')
                o.append(f'<text class="je" x="{cx}" y="{y + 10}" text-anchor="middle">{short}</text>')
    o.append("</svg>")
    return "".join(o)


def blockdiagram(d):
    bl = {b["id"]: b for b in d["blocks"]}
    W = max(b["x"] + b["w"] for b in d["blocks"]) + 20
    H = max(b["y"] + b["h"] for b in d["blocks"]) + 20
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The department as blocks, with the journeys on each link">',
         f'<style>.bt{{font:10.5px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;fill:{INK};font-weight:700}}.bl{{font:8.5px -apple-system,sans-serif;fill:{MUTED}}}</style>',
         f'<defs><marker id="bah" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{MUTED}"/></marker></defs>']
    def c(b):
        return b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    def edge_pt(b, tx, ty):
        cx, cy = c(b)
        dx, dy = tx - cx, ty - cy
        if abs(dx) * b["h"] > abs(dy) * b["w"]:
            return (b["x"] + b["w"] if dx > 0 else b["x"]), cy + dy * (b["w"] / 2) / abs(dx) if dx else cy
        return cx + dx * (b["h"] / 2) / abs(dy) if dy else cx, (b["y"] + b["h"] if dy > 0 else b["y"])
    for l in d["links"]:
        a, b = bl[l["from"]], bl[l["to"]]
        (ax, ay), (bx, by) = c(a), c(b)
        x0, y0 = edge_pt(a, bx, by)
        x1, y1 = edge_pt(b, ax, ay)
        o.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{MUTED}" stroke-width="1" marker-end="url(#bah)"/>')
        horiz = abs(x1 - x0) > abs(y1 - y0)
        t = 0.5 if horiz else 0.5
        mx, my = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if horiz:
            my -= 9  # a short horizontal link: the label sits above the line, clear of both boxes
        tw = 4.2 * len(l["label"]) + 6
        o.append(f'<rect x="{mx - tw / 2:.1f}" y="{my - 9:.1f}" width="{tw:.1f}" height="12" rx="2" fill="#fff" opacity=".92"/>')
        o.append(f'<text class="bl" x="{mx:.1f}" y="{my:.1f}" text-anchor="middle">{esc(l["label"])}</text>')
    for b in d["blocks"]:
        fill = "#eef2ff" if b["id"] in ("line", "born") else ("#f9fafb" if b["id"] in ("record", "library") else "#fff")
        o.append(f'<rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="6" fill="{fill}" stroke="{INK}"/>')
        words, lines, cur = b["label"].split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > b["w"] / 6.2:
                lines.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        y0 = b["y"] + b["h"] / 2 - (len(lines) - 1) * 6 + 3.5
        for k, ln in enumerate(lines):
            o.append(f'<text class="bt" x="{b["x"] + b["w"] / 2}" y="{y0 + k * 12}" text-anchor="middle">{esc(ln)}</text>')
    o.append("</svg>")
    return "".join(o)


def render(d):
    lanes = [tuple(x) for x in d["lanes"]]
    o = [BEGIN,
         f'<h2 id="journeys">The journeys, step by step <span style="font-size:11px;color:{OK}">RECORD &#183; from the docs set</span> <span style="font-size:11px;color:{RED}">+ DIRECTED rows, founder 2026-09-29</span></h2>',
         '<p>The same code, read as what a person lives through. Every journey is drawn three ways from one data file: the block diagram (where the journeys cross the department), a swimlane per journey (the happy path by lane, and under it in red where it goes wrong, by row), and the tables (each step with its function and code; each edge with what the code does and a cell for your mark). A row tagged <b>DIRECTED</b> is your direction of today set against what is built; it is not built and says so. Nothing else here is proposed.</p>',
         '<div class="note"><b>How to edit this section.</b> Edit <code>system/journeys.json</code> only, then run <code>python3 _journeys.py --apply</code> and the two guards (<code>_sidebar.py --check</code>, <code>_manifest-check.py</code>). A new nuance is one row: a step (<code>n, lane, short, text, function, code</code>) or an edge (<code>id, at, short, edge, code_does, mark</code>) under its journey, or a direction (<code>id, direction, built, gap, mark</code>). A new journey is a new object with the next J number. Every claim names a function or file from <code>sutra-ui/docs/department/</code>; a direction not in the code is written DIRECTED in its text. The pictures and the tables are rendered from the rows; a hand edit to them is refused by <code>_journeys.py --check</code>. Notation: rounded box = a step; diamond = your stamp; lane = who acts; solid arrow = the happy path; red dashed stub = an edge case named by its row id; blue box = an engine.</div>',
         '<h3 id="j-blocks">The department as blocks, with the journeys on each link</h3>',
         blockdiagram(d),
         '<table><tr><th>Journey</th>' + "".join(f'<th>{esc(n)}</th>' for _, n in lanes) + '</tr>']
    for j in d["journeys"]:
        used = {s["lane"] for s in j["steps"]}
        o.append(f'<tr><td><a href="#{j["id"]}">{esc(j["id"].upper())} {esc(j["title"])}</a></td>' + "".join(f'<td>{"x" if k in used else "&#8212;"}</td>' for k, _ in lanes) + '</tr>')
    o.append('</table>')
    o.append('<h3 id="directed">Your directions of 2026-09-29, against the code</h3>')
    o.append('<table><tr><th>#</th><th>Direction (your words, shortened)</th><th>Built today</th><th>Gap</th><th>Your mark</th></tr>')
    for k, r in enumerate(d["directed"]):
        o.append(f'<tr><td>{esc(r["id"])}</td><td>{r["direction"]}</td><td>{r["built"]}</td><td>{r["gap"]}</td><td>{r["mark"] or ("keep / change / drop" if k == 0 else "")}</td></tr>')
    o.append('</table>')
    o.append("<p class=\"note\">Today's decision row on Root (the morning's \"found / create / supply / end\") is superseded by the row of this evening: Root founds the department and its five functions and hands over; Adaptation creates and fits engines; the engines start on their own triggers. Rows D-b, D-d and D-e are the build that the direction asks for; they are not on the Native to-build list until you mark them.</p>")
    if d.get("rulings"):
        o.append('<h3 id="rulings">Your rulings, logged</h3>')
        o.append('<p>Every instruction you gave in the sessions of 2026-09-29 and 2026-09-30, in your words shortened, with the level of the design spine it belongs to (L1 product, L2 model, L3 laws, L4 components, L8 governance), its status, and the contradiction it opens against this page or the code. The journeys below are rebuilt from these rows once you have marked them; until then a row that contradicts a journey step is flagged here, not silently applied.</p>')
        o.append('<table><tr><th>#</th><th>Level</th><th>Your ruling</th><th>Status</th><th>Contradiction it opens</th><th>Your mark</th></tr>')
        for k, r in enumerate(d["rulings"]):
            col = {"ruled": "#166534", "open": "#b91c1c", "parked": "#6b7280", "built": "#1d4ed8"}.get(r["status"], "#111")
            o.append(f'<tr><td>{esc(r["id"])}</td><td>{esc(r["level"])}</td><td>{r["words"]}</td><td><span style="color:{col};font-weight:700">{esc(r["status"].upper())}</span> &#183; {esc(r["date"])}</td><td>{r["contradiction"] or "none"}</td><td>{r.get("mark") or ("keep / change / drop" if k == 0 else "")}</td></tr>')
        o.append('</table>')
    for j in d["journeys"]:
        tag = f' <span style="font-size:11px;color:{RED}">{esc(j["tag"])}</span>' if j.get("tag") else ""
        o.append(f'<h3 id="{j["id"]}">{esc(j["id"].upper())} &#183; {esc(j["title"])}{tag}</h3>')
        if j.get("said"):
            o.append('<div class="note"><b>Founder said</b> (verbatim):' + "".join(f'<br>&#8220;{esc(q)}&#8221;' for q in j["said"]) + '</div>')
        if j.get("lead"):
            o.append(f'<p>{j["lead"]}</p>')
        o.append(f'<div class="jflow" data-j="{j["id"]}">{swimlane(j, lanes)}</div>')
        has_status = any(s.get("status") for s in j["steps"])
        o.append('<table><tr><th>#</th><th>Step</th><th>Function</th>' + ('<th>Status</th>' if has_status else '') + '<th>Code</th></tr>')
        for s in j["steps"]:
            st = ""
            if has_status:
                v = s.get("status", "")
                col = OK if v.startswith("built") else (RED if v.startswith("to build") else MUTED)
                st = f'<td><span style="color:{col};font-weight:700">{esc(v.upper())}</span></td>'
            o.append(f'<tr><td>{esc(s["n"])}</td><td>{s["text"]}</td><td>{s["function"]}</td>{st}<td>{s["code"]}</td></tr>')
        o.append('</table>')
        if j.get("sub"):
            o.append(f'<h4 id="{j["id"]}-sub" style="font-size:13px;margin:14px 0 4px">Its sub-journeys (kept as listed; detail later)</h4>')
            o.append('<table><tr><th>#</th><th>Sub-journey</th><th>What happens</th><th>Owner</th><th>Step</th><th>Drawn</th></tr>')
            for a, b, c, w, st, dr in j["sub"]:
                o.append(f'<tr><td>{esc(a)}</td><td><b>{esc(b)}</b></td><td>{esc(c)}</td><td>{esc(w)}</td><td>{esc(st)}</td><td>{dr}</td></tr>')
            o.append('</table>')
        o.append('<table><tr><th>#</th><th>Edge</th><th>What the code does</th><th>Your mark</th></tr>')
        for k, e in enumerate(j["edges"]):
            o.append(f'<tr><td>{esc(e["id"])}</td><td>{e["edge"]}</td><td>{e["code_does"]}</td><td>{e["mark"] or ("keep / change / drop" if k == 0 else "")}</td></tr>')
        o.append('</table>')
        if j.get("build"):
            o.append(f'<h4 id="{j["id"]}-build" style="font-size:13px;margin:14px 0 4px">How this gets built</h4>')
            o.append('<table><tr><th>#</th><th>Change</th><th>Where</th><th>Owner</th><th>Size</th></tr>')
            for k, b in enumerate(j["build"], 1):
                o.append(f'<tr><td>B{k}</td><td>{b["change"]}</td><td>{b["where"]}</td><td>{esc(b["owner"])}</td><td>{esc(b["size"])}</td></tr>')
            o.append('</table>')
        if j.get("today"):
            o.append(f'<details><summary style="cursor:pointer;font-size:13px;color:{MUTED}">How it runs today, before this change</summary><p style="font-size:13px">{j["today"]}</p></details>')
    o.append(f'<p class="note">Source for every row: {esc(d["source"])}. Data file version {esc(d["version"])}. Rows that say "not found in the docs set" were not read in the code either and stay open until someone reads it.</p>')
    o.append(END)
    return "\n".join(o)


def main():
    d = json.load(open(DATA))
    out = render(d)
    if "--apply" in sys.argv or "--check" in sys.argv:
        page = open(PAGE).read()
        i, k = page.find(BEGIN), page.find(END)
        if i < 0 or k < 0:
            print("journeys: markers not found in system/department.html"); sys.exit(1)
        cur = page[i:k + len(END)]
        if "--check" in sys.argv:
            if cur != out:
                print("journeys: the page's section differs from a fresh render; edit system/journeys.json and run --apply"); sys.exit(1)
            print("OK: journeys section matches system/journeys.json"); return
        open(PAGE, "w").write(page[:i] + out + page[k + len(END):])
        print(f"journeys: applied {len(d['journeys'])} journeys, {sum(len(j['steps']) for j in d['journeys'])} steps, {sum(len(j['edges']) for j in d['journeys'])} edges")
        return
    print(out)


if __name__ == "__main__":
    main()
