# Native — the system, simply

**Status:** WORKING DRAFT (2026-06-15) · productization, not implementation · "create this much, then work more on it."
**What this is:** the whole connected model from one design session, in the simplest accurate form — the flow, the axes, each axis with an example, and basic walkthroughs of the flow running.
**Canon vs this doc:** canon is `sutra/os/engines/NATIVE-ENGINE.md` + the ADRs. This is a *product-level* synthesis — need / advantage / how-it-works — meant to be read, not built from.

---

## 0 · What it is, in one paragraph

Native is a **feedback loop for work**: it turns an intent into done work, **writes down what happened**, and **reads its own record to do better next time**. The record is the system's model of itself (the Good Regulator Theorem: to regulate something well you must model it — the record *is* that model). Everything below is detail inside that one loop.

---

## 1 · The two primitives

Build these two well; everything else is them, composed.

```
WORK-ATOM   GOAL -> dispatch(LLM | skill | code) -> verify          the NODE (the unit of doing)
            verify = [ asserted-done (the executor) + accepted (the counter-party) ]
RESOURCE    a finite STOCK the work spends: tokens . $ . attention . the record . an account
```

- **Work-Atom** = the smallest piece of real work. "Say what done is · do one thing · check it."
- **Resource** = what the work *spends*. Every atom debits resources; the record should be able to *reconcile* (balance), not just append.

---

## 2 · The flow (the loop)

```
  INTENT  a new thing arrives
    |
    v
  SHAPE      read the input -> a plan          (the front)
    |
    v
  RUN        the work-atoms execute            (the doing)
    |
    v
  RECORD     every atom, run, and resource-debit, written down
    |
    v
  GROW       read the record -> improve the work + the system   (over time)
    |
    v
  write state back -> next INTENT runs against the updated state -> LOOP

  GOVERN (authority) wraps every step — auto | ask | deny
```

Plain walk: an intent enters → SHAPE turns it into a plan of atoms → they RUN and leave a RECORD → GROW reads the record and improves things → the improvement reshapes the next run. Authority sits over every step.

---

## 3 · The axes — one open set, sorted by a single test

An **axis** is a dimension you read a piece of work against. They are **not a fixed list** — they are *minted on demand* from one primitive (`value <-> axis`, ADR-027). What is fixed is the **primitive** and the **families** (the slots an axis falls into). Sort any axis by one question:

```
THE SORTING TEST — ask of any axis:
  does it read the INPUT, fresh every run?          -> SHAPE
  does it accumulate on the UNIT, across runs?      -> GROW
  does it gate a transition (auto/ask/deny)?        -> GOVERN
  does it read the RELATIONSHIP between two atoms?   -> EDGE
  is it a finite STOCK the work spends?             -> RESOURCE
  is it about WHEN / over time?                     -> TIME
```

| Family | reads (WHAT) | fires (WHEN) |
|---|---|---|
| **SHAPE** | the input, fresh | front — before each run |
| **GROW** | the accumulated record | over time — after runs |
| **GOVERN** | every transition | throughout — around every gate |
| **EDGE** | the link between atoms | wired at SHAPE · grown at GROW |
| **RESOURCE** | a finite stock | spent at RUN · reconciled at RECORD |
| **TIME** | duration+graph / stocks+delay | schedule (plan) · dynamics (over the loop) |

---

## 4 · Each axis, with an example

### SHAPE — read the input, shape this run
| Axis | What it decides | Example |
|---|---|---|
| **TYPE** | what kind of ask | "ship onboarding" → *task* (vs question / direction) |
| **CERTAINTY** (Cynefin) | the posture: do / analyze / probe / stabilize | known cause → *analyze*; unknown → *probe* |
| **LENS** | where to cut | a product job → cut *by deliverable* (audit · draft · wire) |
| *(also)* pattern · depth · cadence | control-flow · effort · pace | parallel vs sequence; how deep to go |

> **Certainty is upstream of the lens.** It picks the *approach* (analyze vs probe), which decides *which lens fits* and how the pieces are wired — not a label on the lens's output.

### GROW — read the record, improve over time (each writes back)
| Axis | The ladder | Writes back to | Example |
|---|---|---|---|
| **SUBSTANCE** | C0 LLM → C1 skill → C2 code | the atom's **dispatch** | a proven step runs as *code*, not an LLM call |
| **SCALE** | S1 → S5 self-governing (VSM) | the **shapes** available | a pile of workflows grows coordination → a System |
| **CROSS-UNIT** | isolate → coordinate → delegate | **who-may-call-whom** | a branch delegates to a sibling via an explicit handoff |
| **CODIFY** | E0 one-off → E5 doctrine | the **FOLLOW catalog** | a repeated practice becomes a workflow you *follow* |

### GOVERN — authority over every transition
| Axis | What it does | Example |
|---|---|---|
| **AUTHORITY** | auto / ask / deny on every change; owns the *accept* half of verify | irreversible spend → *ask*; routine read → *auto* |

### EDGE — the typed link between atoms
| Edge | Meaning | Needs | Example |
|---|---|---|---|
| **handoff** | A's output → B's input | order + a usable output | audit → feeds → draft |
| **shared-resource** | A & B want one finite thing | an allocation rule (FCFS/priority/budget) | two atoms hit one rate limit → one waits |
| **must-cohere** | A & B each make a piece of one whole | a standard up-front, or an integration step | 3 screens must share one visual style |

### RESOURCE — the finite stock the work spends
| Where it comes from | The competition | Example |
|---|---|---|
| compute / rate-limit / budget / the human / the record / an account | atoms starve or clash | parallel atoms drain one token budget → it runs dry |

> Shared-resource *edges* and Scheduling *contention* are the same thing seen two ways — and they are the **S2 (coordination) / S3 (resource)** rungs of the maturation ladder.

### TIME — two faces
| Face | Over | Key insight | Example |
|---|---|---|---|
| **SCHEDULE** | the work graph | the **critical path** is the deadline floor; effort off it changes nothing | speed a slack atom → deadline unmoved |
| **DYNAMICS** | the loop | stocks + delayed feedback → **oscillation**; every atom GREEN, whole still diverging | fan out to clear backlog → burst-finish → idle → repeat |

> Dynamics guardrail (already in canon as pitfalls #2 / #12): respond to *out-of-control* signals only — don't "tamper" against normal variance.

---

## 5 · The axes are open — minting and reworking (governance rule)

```
+-----------------------------------------------------------------------------+
| MINTING (on the fly, by anyone):                                            |
|   mint(interrogative x mechanism) -> a new axis                             |
|   pick(axis, test = "does it change what-you-build or who-reads?")          |
|   -> kept only if it passes the test (the gate that stops axis-spam)        |
|                                                                             |
| REWORKING THE FAMILIES (NOT on the fly):                                    |
|   if a user's minted axis falls OUTSIDE the families, the system SURFACES   |
|   it. Reworking the family set is done by the CORE AUTHOR of Native — a     |
|   deliberate, governed act, never automatic.                               |
+-----------------------------------------------------------------------------+
```

So there are **two tiers**: users mint *axes* freely (open set + quality gate); only the core author reworks the *families* (the closed skeleton), and only after the system flags that real usage outgrew them. **Families = closed skeleton. Axes = open, minted flesh.**

This mirrors the two primitives: just as the **Work-Atom** is the one *doing* primitive (everything is it, composed), **value↔axis** is the one *thinking* primitive (every axis is it, minted).

---

## 6 · Basic use-cases — the flow running (start here)

### A · Trivial — "summarize this doc"
```
INTENT -> SHAPE: TYPE=task, CERTAINTY=clear, LENS=none(one piece) -> 1 WORK-ATOM
       -> dispatch 1 LLM call -> verify -> RECORD -> done
```
One atom, one shot. No edges, no decomposition. The minimal flow.

### B · Medium — "ship the onboarding redesign"
```
SHAPE: task · Complicated · lens=by-deliverable -> 3 atom-goals
WORKFLOW:  [audit] --handoff--> [draft] --handoff--> [wire+verify]
  - audit:  one-shot LLM (analysis)
  - draft:  Complex -> 3 screens in PARALLEL, must-cohere (one style)
  - wire:   sequence+gate; "wire" runs as CODE (hardened from past runs)
RECORD -> EVIDENCE -> GROW may harden/codify -> next run is cheaper
```
Shows decomposition, all three edge kinds, a write-back (wire = code), recursion (each atom re-enters from classify with the parent's frame + new).

### C · Unknown — "why is retention dropping?" (no playbook)
```
SHAPE: CERTAINTY=Complex (cause unknown) -> posture = PROBE, don't plan
LENS in explore mode: candidate frames as PARALLEL bets (pricing? onboarding? support?)
  -> each probe leaves a RECORD -> SENSE which moved the metric -> AMPLIFY winner
  -> uncertainty drops: Complex -> Complicated -> Clear (the fix)
  -> CODIFY the path that worked -> a NEW workflow-type is BORN
  -> next time at RESOLVE it is FOLLOW-able (the playbook now exists)
```
Shows how a playbook is *made* when none exists, the probe loop, and CODIFY closing back into the front.

---

## 7 · Honest scope

- **Productization, not implementation.** Schemas, thresholds, solvers, and simulators are the implementation layer — deferred.
- **TIME is included as axes (the insight), not engines.** No scheduler, no system-dynamics simulator in v1 — the critical-path *idea* and the oscillation *warning*, yes.
- **The loop models the work graph + its evolution — NOT on-time or stability guarantees.** A fully-verified atom set can still miss a deadline (schedule) or oscillate (dynamics); the docs must not imply otherwise.

---

## 8 · Corrections kept honest (from the dual-vendor + adjacent-discipline research)

- **Native does NOT lack composition/coordination.** Canon already has 5 composition laws (interaction-not-safe · composite-needs-metasystem · variability-compounds) + the VSM metasystem. The gap was that the *website pages under-surface* it — this doc surfaces it. (An earlier research pass overstated "Native lacks it"; corrected.)
- **Native has more than one canon primitive.** The Work-Atom is the *hero* primitive of this narrative; canon lists 10 typed primitives (Domain, Charter, Workflow, Step, Trigger, ExecutionResult, EngineEvent, Tenant, DecisionProvenance, Approval). Tenant / Approval already carry isolation / counter-party load.

---

## 9 · Sources

- Canon: `sutra/os/engines/NATIVE-ENGINE.md`; ADR-026 (workflow-type resolution), ADR-027 (value↔axis single primitive), ADR-009 (Approval), ADR-006 (Tenant), ADR-012 (pre/post check).
- Science: `holding/research/2026-06-12-unit-work-record-science.md` (5 disciplines, ~16 formal results: Requisite Variety, Good Regulator, Little's Law, VSM Recursive System Theorem, workflow-net soundness, sagas).
- Adjacent disciplines (this session's sweep): Coordination Theory (Malone & Crowston), Org Design (Thompson · Galbraith · Lawrence-Lorsch), REA accounting (McCarthy), Scheduling (CPM/PERT/RCPSP), System Dynamics (Forrester · Sterman), Language-Action (Winograd & Flores · Suchman) — used for the EDGE, RESOURCE, and TIME additions; verified, no fabrication.
- Pages this seeds: `platform/{flow, evolution, crystallization, maturation, company-decomposed, authority-tenancy}.html`.
