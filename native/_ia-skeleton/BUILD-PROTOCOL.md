# BUILD-PROTOCOL — how any agent session operates this site

> DUMMY-DATA SKELETON. This file shows what the real protocol will contain.
> The point: you hand a Claude session this directory and say "continue" —
> nothing else. The manifest + this file carry all the project context.

## The loop

```
1. READ   manifest.json
2. FILTER pages where version == current_version AND status below target
3. PICK   the highest node whose parent is LOCKED (cascade rule)
4. LOAD   the page + its parent's contract + governance/ invariants
5. WORK   author / extend / fix — content must satisfy the page's own
          acceptance field; claims cite sources; unknowns go to "Open gaps"
6. VERIFY run the checkers (below); fix loop max 3, then stop + surface
7. FLIP   status one step (SEED→DRAFT→VERIFIED); only the founder
          flips to LOCKED
8. LOG    one line to the build log; pick the next node
```

## Zoom bands (words, never L-numbers)

GOVERNANCE (wrap) · COMPANY (zoom 0) · WHY (zoom 1) · PRODUCTS (zoom 2) ·
PLATFORM (zoom 3) · ENGINEERING (zoom 4) · RUNTIME (zoom 5)

L-numbers are BANNED for bands: `L0-L5` already means the change-cascade
hierarchy in `holding/HIERARCHY.md`, and `L0-L2` means build layers in D38.
Three L-namespaces guarantee confusion — bands are words.

GOVERNANCE is not a band you zoom through — it is the WRAP. On every map it
is the purple dashed border; `governance/index.html` is that border opened
up. Every page CITES governance invariants; no page restates them.

## Page anatomy (mandatory — understandability rule)

Every page renders in this exact order. Visual first, text second; the prose
explains the diagrams, it never replaces them.

| # | Section | Form |
|---|---|---|
| 1 | Company map with YOU-ARE-HERE highlight | SVG — same map everywhere, only the highlight moves |
| 2 | Work-order header (id · parent · status · contract · acceptance) | table |
| 3 | This page's own block diagram (internal parts + labeled neighbor edges) | SVG — solid = mine, dashed = neighbor |
| 4 | The same content as tables (parts, contracts, mappings) | tables |
| 5 | Prose, gaps, agent notes | text |

Diagram grammar (fixed): up = abstract (WHY, upstream) · down = concrete
(HOW, downstream) · solid arrow = contract flowing downstream · purple
dashed border = governance wrap · box colors = status (green LOCKED ·
amber VERIFIED · red DRAFT · gray dashed SEED) · every box has >=1 labeled
edge — orphan boxes fail verification.

## Status flow

| Status | Meaning | Who sets it |
|---|---|---|
| SEED | dir + manifest row exist, page empty | anyone |
| DRAFT | authored, self-consistent | agent |
| VERIFIED | adversarially checked (grounding + links + budget) | verifier agent |
| LOCKED | founder approved — downstream may build on it | **founder only** |
| SHIPPED | implemented in runtime + cited back | agent after canon merge |

## Two status vocabularies — do not conflate

| Vocabulary | Tracks | Values | Lives in |
|---|---|---|---|
| Page lifecycle (above) | how BUILT a page is | SEED→DRAFT→VERIFIED→LOCKED→SHIPPED | manifest.json |
| Parity coverage | whether a Sutra/Asawa CONCEPT is captured in Native | CAPTURED / PARTIAL / MISSING / EXCLUDED | holding/SUTRA-NATIVE-PARITY.md ledger |

They are orthogonal: a page can be LOCKED while a concept it should cover is
still MISSING in the parity ledger. Agents: never write one vocabulary's
values into the other's field.

## Cross-band projection (`projects_to`)

A concept lives on exactly ONE page (one band, one parent), but may PROJECT
onto another band — e.g. BLUEPRINT is a PLATFORM mechanism that also
surfaces as a DOWNSTREAM skill. The manifest row stores the primary home;
`projects_to` lists the secondary pages, rendered as dashed sideways links
on diagrams. Never duplicate content across the projection — link it.

## Verifiers (scripts, not opinions)

| Check | Rule |
|---|---|
| link-integrity | every relative href resolves; every cross-page claim links |
| cascade | page cites only its parent's contract upward; only existing children downward |
| grounding | sampled claims trace to cited sources (doc anchors or sutra canon) |
| budget | hub ≤400 lines; page ≤800 — over budget = split downward |
| manifest-sync | every page on disk has a manifest row and vice versa |
| band-words | no `L0`-`L5` band labels anywhere; bands are words |

## Version mechanics

- v2 work = new manifest rows tagged `v2` + a `roadmap/v2.html` gate page.
- v1 pages are never edited for v2 scope; v2 pages may supersede them
  explicitly (manifest field `supersedes`).
- A version ships when every row tagged with it reaches SHIPPED.

## Hard rules

1. One page, one band, one parent. No orphans — manifest-sync enforces.
2. ENGINEERING work starts only under a LOCKED PLATFORM parent.
3. RUNTIME is the sutra repo. Link to canon; never copy it (D54).
4. Founder voice cells are gaps until the founder fills them. No fabrication.
5. Governance is cited, never restated. The wrap page is the single home.
