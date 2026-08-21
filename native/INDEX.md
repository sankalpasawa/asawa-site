# Native — Documentation Portal

> **Multi-page IA live 2026-06-12** (migration P1). This file is the thin markdown portal;
> the site itself is HTML. Pick your entry point below.

| Entry | Path | What it is |
|---|---|---|
| Hub (human entry) | [`index.html`](./index.html) | status-colored company map + page board |
| Machine entry | [`manifest.json`](./manifest.json) + [`BUILD-PROTOCOL.md`](./BUILD-PROTOCOL.md) | one row per page + the agent operating loop |
| Frozen master | [`master/index.html`](./master/index.html) | v1 monolith, FROZEN — cite anchors, never edit |
| Resume entry | [`holding/RESUME-NATIVE-CHARTER.md`](../../RESUME-NATIVE-CHARTER.md) | fresh-session start point |

Bands are **words** — GOVERNANCE (wrap) · COMPANY · WHY · PRODUCTS · PLATFORM · ENGINEERING · RUNTIME.
Page status lives in `manifest.json` (SEED → DRAFT → VERIFIED → LOCKED → SHIPPED; LOCKED is founder-only).
RUNTIME = the sutra repo — linked per D54, never copied. Build log: `_build-log.jsonl`. Page shell: `_template.html`.

## Page tree (27 pages — from `manifest.json`)

| Band | Page | Path |
|---|---|---|
| GOVERNANCE | Governance — the wrap: doctrine · directions · charters · machinery · meta-rules | [`governance/index.html`](./governance/index.html) |
| GOVERNANCE | Sutra→Native Parity — coverage scoreboard + ledger pointer | [`governance/parity.html`](./governance/parity.html) |
| COMPANY | Native — Company Hub | [`index.html`](./index.html) |
| COMPANY | Roadmap — versions · phases · open questions · risks · assumptions · backlog | [`roadmap/index.html`](./roadmap/index.html) |
| COMPANY | Distribution — tiers · channels · pricing · onboarding · module distribution | [`distribution.html`](./distribution.html) |
| PRODUCTS | Needs — why Native exists (N1-N41 + problem statement) | [`needs/index.html`](./products/cos/needs.html) |
| PRODUCTS | Research foundations — findings grounding the WHY | [`needs/research.html`](./products/cos/needs-research.html) |
| PRODUCTS | Product — Chief of Staff (CoS): idea · persona · pillars B1-B5 · views · journey | [`products/cos/index.html`](./products/cos/index.html) |
| PRODUCTS | CoS Product Design — overview + §2.F.A foundations + §2.F.B input/intent | [`products/cos/product-design.html`](./products/cos/product-design.html) |
| PRODUCTS | CoS Design — §2.F.C journeys (task · query · directive · feedback · new-idea) | [`products/cos/design-journeys.html`](./products/cos/design-journeys.html) |
| PRODUCTS | CoS Design — §2.F.D-I (outputs · memory · trust · errors · pulse · lifecycle) | [`products/cos/design-surfaces.html`](./products/cos/design-surfaces.html) |
| PRODUCTS | Product — Senior Expert (v2 seed) | [`products/senior-expert/index.html`](./products/senior-expert/index.html) |
| PLATFORM | Platform — locked first-layer schema (§1.0) + layers · boundary · crosscuts · hierarchy · tech parts | [`platform/index.html`](./platform/index.html) |
| PLATFORM | Block — UI / Consumer Product | [`platform/ui.html`](./platform/ui.html) |
| PLATFORM | Consumer UI — Sutra Desktop design documentation (IA · decisions · day model · session model · data plane) | [`consumer-ui.html`](./consumer-ui.html) |
| PLATFORM | Design System — one skin for app · homepage · departments (tokens, 13 components, 50-task plan) | [`design-system.html`](./design-system.html) |
| PLATFORM | Block — Host (Claude CLI: agent runtime + model) | [`platform/host.html`](./platform/host.html) |
| PLATFORM | Block — Orchestration (translate request → find process) | [`platform/orchestration.html`](./platform/orchestration.html) |
| PLATFORM | Block — System of Process (the runtime) | [`platform/system-of-process.html`](./platform/system-of-process.html) |
| PLATFORM | The Model — ruled vocabulary, bottom-up (RULED 2026-08-05/06) | [`platform/the-model.html`](./platform/the-model.html) |
| PLATFORM | Model PRD — Particles | [`platform/model/particles.html`](./platform/model/particles.html) |
| PLATFORM | Model PRD — Work-Atom | [`platform/model/work-atom.html`](./platform/model/work-atom.html) |
| PLATFORM | Model PRD — Workflow + Engine | [`platform/model/workflow-engine.html`](./platform/model/workflow-engine.html) |
| PLATFORM | Model PRD — Assembly + System | [`platform/model/assembly-system.html`](./platform/model/assembly-system.html) |
| PLATFORM | Model PRD — Internal System | [`platform/model/internal-system.html`](./platform/model/internal-system.html) |
| PLATFORM | Model PRD — Shadow Systems | [`platform/model/shadow-systems.html`](./platform/model/shadow-systems.html) |
| PLATFORM | Model PRD — Properties (Charter · Domain · Tenancy) | [`platform/model/properties.html`](./platform/model/properties.html) |
| PLATFORM | Model — User Journeys (how things get created) | [`platform/model/user-journeys.html`](./platform/model/user-journeys.html) |
| PLATFORM | Model — Implementation (BuildAtoms + right questions) | [`platform/model/implementation.html`](./platform/model/implementation.html) |
| PLATFORM | Model PRD — Builders (PROPOSED, A13) | [`platform/model/builders.html`](./platform/model/builders.html) |
| PLATFORM | Model PRD — Evals (Eval Engine) | [`platform/model/evals.html`](./platform/model/evals.html) |
| PLATFORM | Block — System of Record (memory · provenance · audit) | [`platform/system-of-record.html`](./platform/system-of-record.html) |
| PLATFORM | Block — Authority + Tenancy (cross-cutting gate) | [`platform/authority-tenancy.html`](./platform/authority-tenancy.html) |
| PLATFORM | Block — External World (counterparties) | [`platform/external-world.html`](./platform/external-world.html) |
| PLATFORM | Connector — §5 transport (inventory · flow · acceptance) | [`platform/connector.html`](./platform/connector.html) |
| PLATFORM | Block — Compute (base layer) | [`platform/compute.html`](./platform/compute.html) |
| PLATFORM | Pillar × Block matrix (B1-B5 demands × 8 blocks + B1 traversal) | [`platform/matrix.html`](./products/cos/matrix.html) |
| PLATFORM | Runtime engine — §4.0-§4.11 (daemon · primitives · state machine · CSM · resilience · catalog) | [`platform/runtime.html`](./platform/runtime.html) |
| PLATFORM | HOW methodology — §3 (atom · axes · dynamic selection · acceptance) | [`platform/how-methodology.html`](./platform/how-methodology.html) |
| PLATFORM | Observability — §7 (daily pulse · coverage · token efficiency) | [`platform/observability.html`](./platform/observability.html) |
| ENGINEERING | Engineering — compiled detail per platform subsystem (190 mechanisms) | [`engineering/index.html`](./engineering/index.html) |
| RUNTIME | (no pages — the sutra repo itself; linked per D54, never copied) | `sutra/os/native/` · `sutra/os/decisions/` |

## Archive (legacy files — kept on disk, never deleted)

| File(s) | Disposition |
|---|---|
| [`master/index.html`](./master/index.html) | Frozen v1 monolith — the deep reference; anchors stable for citation, never edited |
| `_block-*.html` · [`_matrix.html`](./_matrix.html) · [`_consumer-product.html`](./_consumer-product.html) | Standalone second-order drafts — FOLDED into `platform/` + `products/` pages 2026-06-12 |
| [`_arch-review.html`](./_arch-review.html) | Superseded by §1.0 pre-freeze (first-layer schema working render) |
| [`_verifier.html`](./_verifier.html) | Verifier Layer (2026-08-08) — declaration/binding/execution/judgment split, cutover scorecard; runtime linked per D54 (ADR-032 + VERIFIER-LEDGER in repos) |
| `_mockup-cascade.html` | Early cascade mockup — superseded by the locked `_ia-skeleton/` template (2026-06-11) and this live tree |
| [`_ia-skeleton/`](./_ia-skeleton/) | Dummy template demo (IA skeleton v3) |
| [`product-prd-native-v1.html`](./product-prd-native-v1.html) · `product-prd-2026-05-09-v2*.html` · `product-design-2026-05-09-*.html` · [`index-2026-04-29-archived.html`](./index-2026-04-29-archived.html) · [`STATE-2026-05-04.html`](./STATE-2026-05-04.html) · [`native.html`](./native.html) · [`landing.html`](./landing.html) · `sutra-v2-*.html` · [`sutra-blueprint-v2.html`](./sutra-blueprint-v2.html) · [`project-manager-prd-v2-test-draft.html`](./project-manager-prd-v2-test-draft.html) · [`senior-expert-prd-baseline-draft.html`](./senior-expert-prd-baseline-draft.html) | Historical, pre-freeze era |
| `prd/` · `tech-design/` | Scaffold dirs — `tech-design/` linked from [`engineering/index.html`](./engineering/index.html) |

---

**Last updated**: 2026-06-12 (IA migration P2 — portal rewritten for the multi-page site; monolith-era portal content lives in git history)
