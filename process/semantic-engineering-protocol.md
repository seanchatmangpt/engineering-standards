# Semantic Engineering Protocol

**Version:** 26.9.21  
**Status:** Root standard  
**Authority:** `MANIFEST.json` + `semantic/semantic-engineering-profile.ttl`

## Root position

This repository is the root engineering constitution. It owns the stable semantics that downstream systems implement:

```text
engineering-standards
  ├─ profiles work/evidence -> sJira
  ├─ profiles transport/runtime -> SA2A
  ├─ profiles manufacture -> ggen / ggen-marketplace
  ├─ profiles consequence -> BRCE / CommandBus runtimes
  ├─ profiles process evidence -> OCEL/process intelligence
  └─ profiles human interfaces -> docs, Jira/GitHub, dashboards, agent context
```

APS is predecessor evidence. Useful APS law has been carried into the root namespace; APS no longer sits above this repository.

## Calculus

```text
O  -> observations
O* -> admitted, grounded, bounded observations
W  -> WorkOrder(O*)
C  -> formal closure / constraints / plan candidates
S  -> SELECT(C)
M  -> CONSTRUCT(S)
G  -> authority grant or typed refusal
D  -> DO(G, M)
R  -> receipt(D)
P  -> replay(O*, R)
T  -> standing(P)
K  -> reusable knowledge from verified boundary
```

Lawful artifact manufacture remains:

```text
A = mu(O*)
```

but an artifact does not acquire standing or authority merely because it was manufactured.

## Hard separations

```text
Received != Admitted
Message != Fact
Ticket != Authority
Agent != Authority
Capability != Authority
Plan != Authority
Proof != Authority
SELECT != CONSTRUCT
CONSTRUCT != DO
GeneratedArtifact != SemanticAuthority
Inspection != Execution
Workflow != Run
NamedReceipt != Receipt
UNKNOWN != ALIVE
```

## Root WorkOrder

`es:WorkOrder` is the canonical unit of engineering work. It binds:

- stable IRI and human identifier;
- repository identity and exact base SHA;
- semantic graph digest;
- subject/replay identity;
- standing and evidence ceiling;
- authority ceiling;
- required capabilities;
- required courts/evidence;
- falsifiers;
- projection authority.

A GitHub issue, Jira issue, PRD, ARD, plan, branch name, dashboard card, agent task, or generated source file is a projection or transport of the WorkOrder.

## Admission

Admission fails closed. Unknown is not admitted.

Use SHACL and other formal courts to establish structural admissibility. Use repository/source evidence to bind real identities. Admission does not grant DO.

A malformed identity, ambiguous subject, unsupported vocabulary construct, missing evidence requirement, or authority-smuggling projection is a typed refusal.

## Standing

Root standing vocabulary:

- `UNKNOWN` — exact subject has no admitted execution proof.
- `PARTIAL_ALIVE` — a required boundary executed, but the full claim is not closed.
- `ALIVE` — exact admitted subject has observed execution satisfying its declared court.
- `BLOCKED` — acceptance is unmet and no currently lawful authorized route remains at the tested boundary.
- `BUILD_BROKEN` — build prevents the declared verification boundary.
- `UNSUPPORTED` — required capability is absent.
- `REFUSED` — admission or authority rejected the request with a typed reason.

Keep observed, admitted, inferred, executed, changed, verified, refused, blocked, and unsupported state separate.

## DfCM

Use the seven-stage root sequence:

1. **守 Preserve** — exact identities, history, existing behavior, lawful reversible possibilities.
2. **柵 Fence** — reconstruct system, boundary, origin, function before replacement.
3. **算 Calculate** — objects -> morphisms -> state -> admission -> closure -> authority -> consequence -> receipt -> replay -> standing.
4. **除 Exclude** — record non-adopted assumptions.
5. **偽 Falsify** — define observations that overturn the claim.
6. **延 Extend** — reuse -> compose -> extend -> invent.
7. **実 Operationalize** — externalize recurring correctness into formal machinery.

A failed edge changes topology. It is not graph failure.

## Prior-art-first intelligence routing

Before general reasoning, route known classes:

| Class | Preferred machinery |
|---|---|
| Hierarchical planning | HDDL / HTN planner |
| Classical or FOND planning | PDDL/FOND solver |
| Constraint satisfaction | SAT / SMT / CP |
| Process conformance | OCEL + process mining |
| Rules / derivation | declarative rule engine |
| Repeatable source manufacture | ggen / framework-native generator |
| Semantic admission | RDF + SHACL/SPARQL |
| Provenance | PROV-O; SLSA for software-build provenance |
| Policy | ODRL where semantics fit |
| Lifecycle integration | OSLC/DCMI profiles |

Only unresolved semantic residue should continue to purchase general model reasoning.

## Public ontology rule

Use public terms where semantics are exact. Do not map by adjacency.

The root profiles PROV-O, SHACL, ODRL, DCMI, OSLC, PROF, and DCAT, and references OCEL and SLSA. Local residue is allowed for concepts such as evidence standing, authority ceilings, falsifiers, replay identities, and exact engineering work-subject binding when no public term is exact.

Never assert `owl:equivalentClass` or `owl:equivalentProperty` without an equivalence proof.

## sJira profile

Semantic Jira is the work/evidence projection of the root.

sJira MUST:
- conserve root WorkOrder identity;
- conserve exact repository/base and graph identity;
- fail closed before projection;
- keep generated ticket/PRD/ARD/plan authority at `NONE`;
- derive standing only from receipts for the same subject.

A Jira state change is not a standing promotion.

## SA2A profile

SA2A is the capability/transport projection of the root.

SA2A MUST conserve:
- WorkOrder IRI;
- graph digest;
- repository/base identity;
- exact capability;
- replay identity;
- bounded standing;
- authority ceiling.

Authentication proves identity. Capability proves addressability. Neither grants permission.

## Authority and BRCE

The only lawful consequential path is:

```text
parse -> route -> admit/refuse -> diagnose/repair -> construct
      -> authority -> DO -> receipt -> replay -> standing
```

No ambient DO authority. No unreceipted actuation.

The strongest authority a work projection may carry is `CONSTRUCT`. `DO` is admitted separately by an authority broker such as CommandBus/BRCE.

Detailed contract: [Authority and Actuation](./authority-and-actuation.md).

## Manufacture

Use existing manufacturing capital before handwriting repeatable surfaces.

Current admitted prior art includes ggen-marketplace packs for semantic documentation, semantic projection, semantic manufacture epochs, SHACL projection, GitHub cloud operating doctrine, and ggen pack specification.

Generated output is disposable inventory. Canonical semantics, generator law, verifier law, and receipts are durable capital.

If a generator cannot express required semantics, record `UNSUPPORTED(generator-capability)` and the exact missing capability. Do not silently treat hand-written output as generated.

Detailed contract: [Semantic Manufacturing](./semantic-manufacturing.md).

## Verification and replay

Verification ladder:

```text
narrow -> unit -> integration -> e2e -> chaos -> stress -> benchmark -> machine report
```

Use the cheapest high-information court first. Every failure produces a new hypothesis and, when learned, a permanent guard.

Replay must reconstruct claimed state from admitted inputs and receipts. A checkpoint is not a crown.

Exact-head evidence is required for source-bound claims. CI is supplementary evidence, not truth.

Detailed contract: [Verification, Replay, and Standing](./verification-replay-standing.md). Object-centric execution evidence: [Process Intelligence](./process-intelligence.md).

## Documentation mode vs Semantic Work Mode

Documentation Mode remains available for small repositories that have not adopted the root semantic graph. In that mode a maintained spec can be the practical source of truth.

Semantic Work Mode is the ecosystem default:
- canonical semantics live in the root/project graph;
- docs and tickets are projections;
- plans are candidate artifacts;
- generated source is projection inventory;
- receipts establish consequence;
- standing is evidence-bound.

Do not run both modes as independent authorities.

## Root learning loop

A downstream repository may discover a valid new law. The correct lifecycle is:

```text
downstream observation
  -> root candidate
  -> fence/equivalence/prior-art check
  -> root ontology/schema/verifier update
  -> qualification
  -> downstream profile regeneration/adoption
```

Success means the next repository does not need to rediscover the same reasoning.

Downstream adoption procedure: [Repository Adoption](./repository-adoption.md).
