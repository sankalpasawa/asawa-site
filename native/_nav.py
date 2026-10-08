#!/usr/bin/env python3
"""The map of the department product, drawn at the top of system/department.html.

One data block below; `python3 _nav.py --apply` writes the SVG between
<!-- nav:begin --> and <!-- nav:end -->; `--check` fails if the markers are
missing, the rendered block is stale, or a link target does not exist.

The frame is the founder's (2026-10-01): we design from user journeys and
system journeys at once, and componentize into a system as we go; the themes
are what we are working on across them. User journeys are MEETINGS, system
journeys are LIFE, components are PARTS (platform/structure.html).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "system", "department.html")
BEGIN = "<!-- nav:begin (rendered by _nav.py; do not edit by hand) -->"
END = "<!-- nav:end -->"

# (code, label line 1, label line 2, href, status)  hrefs are relative to system/
USER = [  # a person sets out, from life
    ("J1", "I want a website for my thing:", "found it, name the department", "#j1", "built"),
    ("J3", "It is live: a change, a question,", "something wrong, an idea", "#j3", "drawn, your mark owed"),
    ("J6", "I want a second thing", "", "#j6", "drawn, your mark owed"),
    ("J7", "Pause it, update it, end it", "", "#j7", "drawn, your mark owed"),
    ("U2", "I run several things:", "one place to see them", "../platform/model/use-cases.html", "later, unruled"),
    ("U1", "The visitor of the site", "", "../platform/model/use-cases.html", "needs to be filled"),
]
SYSTEM = [  # what the system does inside a person's journey
    ("S1", "Root makes the department", "(inside J1)", "../platform/model/root-lifecycle.html", "built"),
    ("J2", "the five functions work", "toward the goal, J2.a-h", "#j2", "listed, detail later"),
    ("J4", "a rule is born from words", "(inside J3)", "#j4", "to confirm as system"),
    ("J5", "an engine is born from an idea", "(inside J3)", "#j5", "to confirm as system"),
    ("S2", "verification: Audit checks", "every outcome (S-30)", "#rulings", "ruled, to design"),
]
COMPONENTS = [  # what the department is made of
    ("Identity", "../platform/model/functions/identity.html"),
    ("Priority", "../platform/model/functions/priority.html"),
    ("Coordination", "../platform/model/functions/coordination.html"),
    ("Adaptation", "../platform/model/functions/adaptation.html"),
    ("Audit", "../platform/model/functions/audit.html"),
    ("Engines, from the Library", "engines.html"),
    ("Workflows and atoms", "../platform/model/workflow-engine.html"),
    ("Artifacts and versions", "../platform/model/versions.html"),
    ("Screens: Chat, Map, messages", "../platform/model/screens.html"),
]
THEMES = [  # what we are working on, across the three
    ("The structure: three faces, six levels", "../platform/structure.html", "ruled S-31"),
    ("Life cycle: born to retired", "../platform/model/system-lifecycle.html", "skeleton, needs to be filled"),
    ("Verification as a product", "#rulings", "ruled S-30, to design"),
    ("Workflows: the schema, the shapes between atoms", "../platform/model/workflow-engine.html", "open, P7"),
    ("From an ask to its kind", "../platform/model/functions/adaptation.html#roadmap", "roadmap row"),
    ("The journeys, step by step", "#journeys", "J1-J7, J2 sub-journeys"),
    ("Testing as a person", "../human-simulation.html", "runs 1-10"),
]

W = 920
INK, MUTE, LINE = "#111827", "#6b7280", "#9ca3af"
USER_C, SYS_C, PART_C, THEME_C = "#fffbeb", "#f0fdf4", "#eef2ff", "#f8fafc"
USER_S, SYS_S, PART_S, THEME_S = "#b45309", "#166534", "#3730a3", "#64748b"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(x, y, w, h, fill, stroke, href, lines, status=None, code=None):
    o = [f'<a href="{href}">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>']
    ty = y + 17
    tx = x + 9
    if code:
        o.append(f'<text x="{x+9}" y="{ty}" font-size="10" font-weight="700" fill="{stroke}">{esc(code)}</text>')
        tx = x + 9 + 7 * len(code) + 6
    first = True
    for ln in lines:
        if not ln:
            continue
        o.append(f'<text x="{tx if first else x+9}" y="{ty}" font-size="11.5" fill="{INK}">{esc(ln)}</text>')
        ty += 14
        first = False
    if status:
        o.append(f'<text x="{x+9}" y="{y+h-7}" font-size="9.5" fill="{MUTE}">{esc(status)}</text>')
    o.append("</a>")
    return "\n".join(o)


def render():
    o = []
    cx = [16, 332, 648]
    cw = 272
    top = 44
    o.append(f'<text x="{W/2}" y="20" text-anchor="middle" font-size="12" font-weight="800" letter-spacing=".06em" fill="{INK}">A DEPARTMENT, THE PRODUCT: WHAT IS BEING BUILT</text>')
    heads = [("A PERSON SETS OUT (user journeys)", USER_S), ("THE DEPARTMENT IS MADE OF (components)", PART_S), ("THE SYSTEM DOES, INSIDE (system journeys)", SYS_S)]
    for i, (h, c) in enumerate(heads):
        o.append(f'<text x="{cx[i]}" y="{top}" font-size="9.5" font-weight="800" letter-spacing=".05em" fill="{c}">{esc(h)}</text>')
    # user journeys
    y = top + 10
    for code, l1, l2, href, st in USER:
        h = 56 if l2 else 44
        o.append(box(cx[0], y, cw, h, USER_C, USER_S, href, [l1, l2], st, code))
        y += h + 8
    user_bottom = y
    # the department box holding its components
    y = top + 10
    fw, fh, gap = 80, 30, 6
    fx = cx[1] + 10
    parts = []
    parts.append(f'<text x="{cx[1]+10}" y="{y+16}" font-size="10.5" font-weight="800" fill="{PART_S}">the department: one system, five functions</text>')
    yy = y + 26
    for k, (name, href) in enumerate(COMPONENTS[:5]):
        col, row = k % 3, k // 3
        bx = fx + col * (fw + gap)
        by = yy + row * (fh + gap)
        parts.append(f'<a href="{href}"><rect x="{bx}" y="{by}" width="{fw}" height="{fh}" rx="5" fill="{PART_C}" stroke="{PART_S}" stroke-width="1"/><text x="{bx+fw/2}" y="{by+19}" text-anchor="middle" font-size="11" fill="{INK}">{esc(name)}</text></a>')
    yy += 2 * (fh + gap) + 6
    for name, href in COMPONENTS[5:]:
        parts.append(f'<a href="{href}"><rect x="{fx}" y="{yy}" width="{cw-20}" height="{fh}" rx="5" fill="{PART_C}" stroke="{PART_S}" stroke-width="1"/><text x="{fx+9}" y="{yy+19}" font-size="11.5" fill="{INK}">{esc(name)}</text></a>')
        yy += fh + gap
    dh = yy - y + 6
    o.append(f'<rect x="{cx[1]}" y="{y}" width="{cw}" height="{dh}" rx="8" fill="#fff" stroke="{PART_S}" stroke-width="1.6"/>')
    o.extend(parts)
    comp_bottom = y + dh
    # system journeys
    y = top + 10
    for code, l1, l2, href, st in SYSTEM:
        h = 56 if l2 else 44
        o.append(box(cx[2], y, cw, h, SYS_C, SYS_S, href, [l1, l2], st, code))
        y += h + 8
    sys_bottom = y
    # arrows between the columns
    mid = top + 10 + 28
    o.append(f'<defs><marker id="nav-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{LINE}"/></marker></defs>')
    o.append(f'<line x1="{cx[0]+cw+2}" y1="{mid}" x2="{cx[1]-3}" y2="{mid}" stroke="{LINE}" stroke-width="1.2" marker-end="url(#nav-arr)"/>')
    o.append(f'<line x1="{cx[1]+cw+2}" y1="{mid}" x2="{cx[2]-3}" y2="{mid}" stroke="{LINE}" stroke-width="1.2" marker-end="url(#nav-arr)"/>')
    o.append(f'<text x="{cx[0]+cw+4}" y="{mid-5}" font-size="8.5" fill="{MUTE}">words</text>')
    o.append(f'<text x="{cx[1]+cw+4}" y="{mid-5}" font-size="8.5" fill="{MUTE}">runs</text>')
    # themes strip
    ty = max(user_bottom, comp_bottom, sys_bottom) + 10
    o.append(f'<text x="16" y="{ty+10}" font-size="9.5" font-weight="800" letter-spacing=".05em" fill="{THEME_S}">THE THEMES WE ARE WORKING ON, ACROSS ALL THREE</text>')
    ty += 18
    tw, th, tg = 218, 44, 8
    for k, (name, href, st) in enumerate(THEMES):
        col, row = k % 4, k // 4
        bx = 16 + col * (tw + tg)
        by = ty + row * (th + tg)
        o.append(f'<a href="{href}"><rect x="{bx}" y="{by}" width="{tw}" height="{th}" rx="6" fill="{THEME_C}" stroke="{THEME_S}" stroke-width="1" stroke-dasharray="4 3"/><text x="{bx+9}" y="{by+17}" font-size="11" fill="{INK}">{esc(name)}</text><text x="{bx+9}" y="{by+34}" font-size="9.5" fill="{MUTE}">{esc(st)}</text></a>')
    H = ty + 2 * (th + tg) + 4
    out = [
        BEGIN,
        '<h2 id="map">The map: what is being built, and how to get to each part</h2>',
        '<p class="figcap">A person sets out from life (left); the department, one system made of parts (middle); what the system does inside that person\'s journey (right); the themes cut across all three. Every box is a link. The split of J1-J7 into a person\'s journeys and the system\'s is my reading, yours to confirm. Frame: <a href="../platform/structure.html#method">how we work</a>.</p>',
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="the map of the department product">',
        "\n".join(o),
        "</svg>",
        END,
    ]
    return "\n".join(out)


def targets():
    for lst in (USER, SYSTEM):
        for row in lst:
            yield row[3]
    for row in COMPONENTS:
        yield row[1]
    for row in THEMES:
        yield row[1]


def check_links():
    bad = []
    for href in targets():
        if href.startswith("#"):
            continue
        path = href.split("#")[0]
        if not os.path.exists(os.path.join(HERE, "system", path)):
            bad.append(href)
    return bad


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    s = open(PAGE).read()
    block = render()
    bad = check_links()
    if bad:
        print("nav: missing link targets:", bad)
        sys.exit(1)
    if mode == "--apply":
        if BEGIN in s:
            a, b = s.index(BEGIN), s.index(END) + len(END)
            s = s[:a] + block + s[b:]
        else:
            anchor = '<h2 id="built">'
            assert s.count(anchor) == 1, "anchor"
            s = s.replace(anchor, block + "\n" + anchor, 1)
        open(PAGE, "w").write(s)
        print("nav: applied")
    else:
        if s.count(BEGIN) != 1 or s.count(END) != 1:
            print("nav: markers missing or doubled")
            sys.exit(1)
        a, b = s.index(BEGIN), s.index(END) + len(END)
        if s[a:b] != block:
            print("nav: stale; run --apply")
            sys.exit(1)
        print("nav: ok")


if __name__ == "__main__":
    main()
