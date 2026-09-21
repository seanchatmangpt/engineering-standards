# Semantic Engineering Protocol

**Version**: 26.9.21  
**Status**: Active profile; runtime standing remains adapter-specific  
**Scope**: Engineering work identity, machine coordination, authority, evidence, replay, and standing

## Purpose

This standard combines three previously adjacent systems into one engineering protocol:

1. the durable constitutional laws recovered by the **Agile Protocol Specification (APS)**;
2. **Semantic Jira (sJira)** as the canonical work/evidence graph and deterministic projection boundary; and
3. **Semantic A2A (SA2A)** as the machine-to-machine capability transport.

The combined protocol has one operational spine:

```text
OBSERVE
  -> ADMIT
  -> WORK ORDER
  -> FORMAL CLOSURE / PLAN
  -> SELECT
  -> CONSTRUCT
  -> AUTHORITY
  -> DO
  -> RECEIPT
  -> REPLAY
  -> STANDING
  -> REUSE
```

The purpose is not to make tickets smarter or agents more trusted. It is to make recurring engineering work progressively less dependent on runtime interpretation.

## Source reconstruction

This profile was reconstructed from exact repository subjects before the refactor:

| Source | Exact subject used | Role here |
|---|---|---|
| Agile Protocol Specification | `seanchatmangpt/agile-protocol-specification@5c31d9d05fe36dc1eca3a26c9eb5cd267a2cf625` | constitutional prior art: admission, DfCM, authority separation, receipts, replay, standing |
| SA2A / AshA2A | `seanchatmangpt/ash_a2a@baa135d5c6129aea1d4b38d48a12ad87e132b638` and RFC-SA2A-001/002 | capability projection and transport; CommandBus-only consequence boundary |
| Semantic Jira | `seanchatmangpt/ggen_igniter#20@90cfd360bc6dfe041d35f7082f064716d22b4d99` | RDF WorkOrder fabric and deterministic projections |
| Semantic Jira SHACL reconciliation | `seanchatmangpt/ggen_igniter#24@e509b375dc84e7ac50935d0b53bcb44ea1935242` | explicit pre-actuation SHACL court and refusal topology |
| This repository | `seanchatmangpt/engineering-standards@610944c48bce6377291c088a3e07775e9ef2908b` | existing human engineering standards being refactored |

The APS repository remains predecessor evidence and a reusable vocabulary source. This repository does **not** copy its implementation tree or inherit its runtime standing. SA2A and sJira remain independent implementations with their own verification and release boundaries.

## The three planes

### 1. Work and evidence plane — sJira

sJira owns the canonical identity of work.

A Semantic WorkOrder MUST be represented in an admitted graph before a projected ticket can claim to represent canonical work. The graph SHOULD reuse public vocabularies where the semantics are exact: DCTERMS for labels/identifiers, PROV-O for provenance, OSLC Change Management for change-request identity, SHACL for admission constraints, and ODRL or an equivalent explicit policy model for authority policy.

A work order MUST bind at least:

- stable work-order IRI and identifier;
- repository identity and exact base commit SHA;
- semantic graph digest;
- subject identity;
- replay identity;
- standing;
- evidence ceiling;
- authority ceiling;
- required courts and evidence;
- acceptance criteria;
- falsifiers;
- required capability identity for machine transport.

A Jira ticket, GitHub issue, PRD, ARD, plan, generated source file, or dashboard is a **projection**. A projection MUST NOT become an independent source of semantic truth merely because a person or agent edited it.

### 2. Interaction plane — SA2A

SA2A owns capability discovery and machine-to-machine transport.

An SA2A capability advertises what a machine can receive or perform. It does not grant authority. An inbound message MUST remain candidate information until the receiver admits the exact semantic subject it references.

For work transport, an SA2A envelope MUST bind:

- exact WorkOrder IRI;
- semantic graph digest;
- repository identity;
- exact base SHA;
- exact capability IRI;
- replay identity;
- current bounded standing;
- authority ceiling;
- projection authority `NONE`.

Authentication proves identity. Capability proves reachability. Neither proves permission.

### 3. Consequence plane — BRCE / CommandBus

Only the consequence plane may cross from proposal into consequential DO.

```text
message -> candidate
candidate -> admission
admission -> SELECT / CONSTRUCT
SELECT / CONSTRUCT -> authority request
authority request -> admit | refuse
admit -> CommandBus / BRCE DO
DO -> receipt
receipt -> independent verification
verification -> bounded standing
```

Projects MAY implement the authority broker differently, but they MUST preserve the separation between capability, plan, proof, authority, execution, receipt, and standing.

## Constitutional invariants

The following are protocol laws:

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
GeneratedArtifact != SemanticTruth
Inspection != Execution
NamedReceipt != Receipt
UNKNOWN != ALIVE
```

The strongest permitted sJira projection ceiling is `CONSTRUCT`. `DO`, merge, publish, deploy, external mutation, or standing promotion MUST NOT be granted by a generated work artifact.

## Standing

Use one bounded standing vocabulary across work, transport, and receipts:

- `UNKNOWN` — no admitted execution evidence for the claimed subject;
- `PARTIAL_ALIVE` — some required boundary has executed, but the full claim has not;
- `ALIVE` — the exact admitted subject has observed execution satisfying its declared court;
- `BLOCKED` — a required transition cannot currently proceed;
- `BUILD_BROKEN` — the subject cannot reach its verification court because its build is broken;
- `UNSUPPORTED` — the required capability is absent;
- `REFUSED(reason)` — admission or authority rejected the request for a typed reason.

Standing MUST bind the exact subject and evidence scope. A repository-wide green check does not automatically promote a narrower or broader subject. A ticket marked done is not an ALIVE receipt.

## DfCM operating sequence

For non-trivial changes, use the seven-stage sequence recovered from APS:

1. **Preserve (守)** — retain observed behavior, history, current standards, exact source identities, and reversible options.
2. **Fence (柵)** — reconstruct system, boundary, origin, and function before replacing structure.
3. **Calculate (算)** — map objects, transitions, state, admission, closure, authority, consequence, receipt, replay, and standing.
4. **Exclude (除)** — record discarded assumptions so they cannot silently return.
5. **Falsify (偽)** — define the observation that would invalidate each consequential claim.
6. **Extend (延)** — reuse, compose, or extend admitted machinery before inventing a new mechanism.
7. **Operationalize (実)** — turn recurring judgment into ontology, schema, generator, planner, verifier, policy, or process control.

A failure on one edge changes the known topology. It does not prove the graph impossible.

## GitHub and Jira integration

The existing [Issue Tracking and Epic Organization](./issue-tracking.md) standard remains the human navigation layer.

There are two modes:

**Documentation mode**
- GitHub issues and Markdown specifications may be the primary work record.
- Existing three-tier milestone/epic/issue guidance applies directly.

**Semantic Work Mode**
- the admitted sJira graph is canonical;
- GitHub/Jira issues are generated or synchronized projections;
- branch/PR descriptions reference the WorkOrder identity and exact base SHA;
- ticket status changes do not promote semantic standing;
- projected tickets are regenerated from graph changes instead of edited as a second source of truth.

Do not run both modes as independent authorities.

## Public ontology before local vocabulary

Before introducing a local semantic term:

1. search the relevant public standard or ontology;
2. prove semantic equivalence before mapping;
3. carry the public term when the meaning is exact;
4. retain a local residue term when the public term would fabricate meaning;
5. record the failed mapping and the condition that would allow a future carry.

Known useful substrates include PROV-O, DCTERMS, OSLC CM/RM, SHACL, ODRL, SKOS, OWL, and the APS profile at `https://w3id.org/chatman/aps#`.

Adjacency is not equivalence. A generic `relation` property is not an acceptable replacement for an exact authority, dependency, digest, receipt, or standing relation.

## Admission and projection contract

The repository carries an executable profile in `semantic/`:

- `semantic-engineering-profile.ttl` — the integration vocabulary/profile;
- `semantic-engineering-shapes.ttl` — SHACL constraints for an sJira WorkOrder transported through SA2A;
- `semantic-work-envelope.schema.json` — JSON transport projection for the same subject;
- `example-work-order.ttl` and `example-work-envelope.json` — positive fixtures.

The repository court MUST also prove negative cases. At minimum these mutations must fail:

- changing the work-order authority ceiling to `DO`;
- changing projection authority away from `NONE`;
- supplying a malformed graph digest;
- changing the transport profile away from `SA2A`.

Run:

```bash
python -m pip install --disable-pip-version-check -r scripts/requirements-semantic.txt
python scripts/check-semantic-standard.py
```

This court proves repository profile conformance only. It does not prove an AshA2A runtime, Jira SaaS mutation, XaaS materialization, production CommandBus execution, deployment, or cross-repository ALIVE standing.

## Migration from APS

This refactor does not delete APS history or pretend its existing repository never existed.

The migration rule is:

```text
APS law
  -> reconstruct exact useful invariant
  -> map to this standard or public ontology
  -> executable profile/falsifier
  -> retain source identity
  -> stop requiring a parallel human interpretation of the same rule
```

New engineering process law SHOULD land here when it governs engineering work generally. Implementation-specific protocol details stay in SA2A, sJira, XaaS, ggen, or their owning repositories.

## Adoption criteria

A project may claim conformance to this profile only when:

- work identity has one canonical source;
- the source binds exact repository/base identities;
- admission fails closed;
- sJira projections carry no DO authority;
- SA2A messages bind the exact semantic subject and graph digest;
- consequential work crosses an explicit authority boundary;
- consequence emits a durable receipt;
- standing is promoted only from evidence for the same subject;
- replay can reconstruct the claimed state from admitted inputs and receipts;
- recurring solved work is moved from repeated inference into reusable formal machinery.

The target is not maximum ceremony. It is to make the next correct execution require less exceptional intelligence than the previous one.
