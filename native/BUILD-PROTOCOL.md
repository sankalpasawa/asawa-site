# BUILD-PROTOCOL — how any agent session operates the Native doc site

> LIVE PROTOCOL (IA migration P1, 2026-06-12). Hand a Claude session this directory and say
> "continue" — `manifest.json` + this file carry all the project context.
> Template of record: `_template.html`. Frozen deep reference: `master/index.html` (never edited).

## The loop

```
1. READ   manifest.json
2. FILTER pages where version == current_version AND status below target
3. PICK   the highest node whose parent permits it (cascade rule; ENGINEERING
          needs a LOCKED PLATFORM parent)
4. LOAD   the page + its parent's contract + governance/ invariants
5. WORK   author / extend / fix — content must satisfy the page's own
          acceptance field; claims cite sources; unknowns go to "Open gaps"
6. VERIFY run the checkers (below); fix loop max 3, then stop + surface
7. FLIP   status one step (SEED→DRAFT→VERIFIED); only the founder
          flips to LOCKED
8. LOG    one line to the build log (`_build-log.jsonl`); pick the next node
```


## Design principles (founder-ratified 2026-06-12 — run these tests on any placement)

| # | Principle | Test |
|---|---|---|
| 1 | One flow, one direction | business -> products -> platform -> engineering -> code; every page sits ON the flow |
| 2 | Ownership decides placement | a page lives where its QUESTION belongs, not where it is used (matrix = a CoS question -> inside CoS) |
| 3 | Peers level, children below | same kind = same row; detail = one level under its owner |
| 4 | Box-in-box = zoom | a container means "open me"; every box clicks one level deeper; same map shape at every zoom |
| 5 | No shiny rows | nothing is elevated for being interesting; cross-cutting = wrap (governance) or lives with its owner |
| 6 | Earn the box | every map element answers a question someone asks; two boxes, same question -> merge |
| 7 | One home, cite the rest | every fact/gap/diagram has one primary page; others link (D54 for code) |
| 8 | Status is bookkeeping, not structure | lifecycle colors render on the hub only; the tree never rearranges on status flips |

v5 placements these produced: needs/design/matrix INSIDE product-cos (needs = documentation, not a blog) · platform = its own horizontal product · daemon IS runtime &#167;4 / S4 (contains orch+sop) · method S3 inside SoP · observability S7 = the ring around the machine · A+T = inner wrap · every page carries the left sidebar index + spine prev/next crumbs.

## Zoom bands (words, never L-numbers)

GOVERNANCE (wrap) · COMPANY/business · PRODUCTS · PLATFORM · ENGINEERING · CODE (sutra repo)
(WHY dissolved 2026-06-12: needs is documentation INSIDE each product, not a band)

L-numbers are BANNED for bands: `L0-L5` already means the change-cascade
hierarchy in `holding/HIERARCHY.md`, and `L0-L2` means build layers in D38.
Three L-namespaces guarantee confusion — bands are words.

GOVERNANCE is not a band you zoom through — it is the WRAP. On every map it
is the purple dashed border; `governance/index.html` is that border opened
up. Every page CITES governance invariants; no page restates them.
RUNTIME is the sutra repo — linked, never copied (D54). It has no pages here.

## Page anatomy (mandatory — understandability rule)

Every page renders in this exact order (see `_template.html`). Visual first,
text second; the prose explains the diagrams, it never replaces them.

| # | Section | Form |
|---|---|---|
| 1 | Company map with YOU-ARE-HERE highlight | SVG — copied from `_template.html`, only the highlight differs |
| 2 | Work-order header (id · parent · status · contract · acceptance) | table |
| 3 | This page's own block diagram (internal parts + labeled neighbor edges) | SVG — solid = mine, dashed = neighbor |
| 4 | The same content as tables (parts, contracts, mappings) | tables |
| 5 | Prose, open gaps, children, sources | text |

Diagram grammar (fixed): up = abstract (WHY, upstream) · down = concrete
(HOW, downstream) · solid arrow = contract flowing downstream · purple
dashed border = governance wrap · every box has >=1 labeled edge — orphan
boxes fail verification.

**Status colors render on the HUB map only** (hub regenerates from the
manifest). Page maps are structural — neutral boxes + highlight — so 25
pages don't go stale on every status flip. This amends the skeleton's
colored-everywhere demo; single point of staleness is the hub.

## Status flow

| Status | Meaning | Who sets it |
|---|---|---|
| SEED | dir + manifest row exist, page empty or stub | anyone |
| DRAFT | authored, self-consistent | agent |
| VERIFIED | adversarially checked (grounding + links + budget) | verifier agent |
| LOCKED | founder approved — downstream may build on it | **founder only** |
| SHIPPED | implemented in runtime + cited back | agent after canon merge |

## Two status vocabularies — do not conflate

| Vocabulary | Tracks | Values | Lives in |
|---|---|---|---|
| Page lifecycle (above) | how BUILT a page is | SEED→DRAFT→VERIFIED→LOCKED→SHIPPED | `manifest.json` |
| Parity coverage | whether a Sutra/Asawa CONCEPT is captured in Native | CAPTURED / PARTIAL / MISSING / EXCLUDED | `holding/SUTRA-NATIVE-PARITY.md` ledger |

They are orthogonal: a page can be LOCKED while a concept it should cover is
still MISSING in the parity ledger. Agents: never write one vocabulary's
values into the other's field. The parity render lives at
`governance/parity.html`.

## Cross-band projection (`projects_to`)

A concept lives on exactly ONE page (one band, one parent), but may PROJECT
onto another band — e.g. Authority+Tenancy is a PLATFORM block that also
surfaces as the GOVERNANCE wrap. The manifest row stores the primary home;
`projects_to` lists the secondary pages, rendered as dashed sideways links
on diagrams. Never duplicate content across the projection — link it.

## Verifiers (scripts, not opinions)

| Check | Rule |
|---|---|
| link-integrity | every relative href resolves on disk; every cross-page claim links |
| cascade | page cites only its parent's contract upward; only existing children downward |
| grounding | sampled claims trace to cited sources (master/ anchors or sutra canon) |
| budget | ADVISORY (founder direction 2026-06-12): hub ~400 lines; page ~800 — a big page SPLITS into children, it never truncates or compresses content away. Completeness always wins over the cap. ENGINEERING may fan out into as many pages as the material needs. |
| manifest-sync | every page on disk has a manifest row and vice versa (exempt: `master/`, `_*`, `prd/`, `tech-design/`, `_ia-skeleton/`, and every file listed in the INDEX.md ARCHIVE table) |
| band-words | no `L0`-`L5` band labels anywhere; bands are words |
| gap-conservation | open-gap items are never silently dropped — they move pages or get resolved with evidence |
| spine-linearity | spine pages carry 0..N unique + gapless; WRAP pages (governance, governance-parity) carry spine:null by design — they are the border, not a stop; any re-parenting updates the spine so the prev/next chain stays one unbroken reading order (deepseek P2, 2026-06-12) |

## Version mechanics

- v2 work = new manifest rows tagged `v2` + a `roadmap/` gate entry.
- v1 pages are never edited for v2 scope; v2 pages may supersede them
  explicitly (manifest field `supersedes`).
- A version ships when every row tagged with it reaches SHIPPED.

## Hard rules

1. One page, one band, one parent. No orphans — manifest-sync enforces.
2. ENGINEERING work starts only under a LOCKED PLATFORM parent.
3. RUNTIME is the sutra repo. Link to canon; never copy it (D54).
4. Founder voice cells are gaps until the founder fills them. No fabrication.
5. Governance is cited, never restated. The wrap page is the single home.
6. `master/index.html` is FROZEN — cite its anchors, never edit it.
7. Native canon writes still route via `holding/skills/updating-native-canon.md` (D54);
   this site documents, canon decides.
