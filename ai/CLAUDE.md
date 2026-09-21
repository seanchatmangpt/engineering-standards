# Engineering Standards — Agent Quick Reference

This file is an AI-facing projection of the repository root. It is **not** independent authority.

Read in order:

1. [`MANIFEST.json`](../MANIFEST.json)
2. [`AGENTS.md`](../AGENTS.md)
3. [root ontology](../semantic/semantic-engineering-profile.ttl)
4. [Semantic Engineering Protocol](../process/semantic-engineering-protocol.md)
5. task-specific process/code standards

## Root calculus

```text
OBSERVE -> ADMIT -> WORK -> CLOSURE -> SELECT -> CONSTRUCT
        -> AUTHORITY -> DO -> RECEIPT -> REPLAY -> STANDING -> REUSE
```

Do not collapse these boundaries:

```text
Received != Admitted
Message != Fact
Ticket != Authority
Agent != Authority
Capability != Authority
Plan != Authority
Proof != Authority
SELECT != CONSTRUCT != DO
GeneratedArtifact != SemanticAuthority
Inspection != Execution
UNKNOWN != ALIVE
```

## Before changing anything

- Resolve repository and exact base SHA.
- Resolve the canonical WorkOrder or establish the smallest lawful Documentation Mode subject.
- Read local `AGENTS.md` and nested doctrine.
- Reconstruct the existing system/boundary/function before replacement.
- Search prior art: standards, public ontologies, framework generators, marketplace packs, solvers, process/rule machinery.
- Preserve reversible possibilities; one failed route is not graph failure.

## Intelligence routing

Use the most specialized admitted machinery available:

| Known class | Preferred machinery |
|---|---|
| HTN | HDDL / HTN planner |
| Classical/FOND | PDDL / FOND solver |
| Constraints | SAT / SMT / CP |
| Process/conformance | OCEL + process mining |
| Rules | declarative rule engine |
| Derivable software | framework-native generator / ggen |
| Semantic admission | RDF + SHACL/SPARQL |
| Provenance | PROV-O; SLSA for software-build provenance |

General model reasoning belongs at unresolved semantic boundaries. When a recurring transformation becomes known, externalize it so the next run needs less reasoning.

## Work artifacts

In Semantic Work Mode the root/project semantic graph is canonical.

These are projections/candidates:
- specs and design documents;
- Jira/GitHub issues;
- CE plans and U-IDs;
- SA2A messages;
- generated code;
- AI reviews;
- dashboards and status labels.

They may describe or transport work. They do not grant DO or promote standing.

Documentation Mode remains valid for small repositories that have not adopted a semantic graph.

## AI interaction architecture

The [six-layer AI architecture](./claude-code/README.md) is an **interaction/context profile under the semantic root**:

1. Rules — persistent pointers/guardrails.
2. Skills — on-demand workflows.
3. Persona Agents — candidate perspectives.
4. References — progressive context.
5. Compound/Learnings — captured observations.
6. Hooks — deterministic local enforcement.

Compound Engineering may realize Layers 2–5. None of those layers owns semantic authority.

## Feature / technical work

Both feature and technical workflows use the same root consequence chain. Product docs, investigation docs, plans, and story points are human coordination projections.

Planning should bind:
- exact subject;
- dependencies/constraints;
- acceptance criteria;
- falsifiers;
- court/evidence;
- authority ceiling.

## GitHub

- exact base SHA first;
- one semantic subject per coherent change;
- draft PR is the default publication boundary;
- exact-head CI only;
- CI is evidence, not truth;
- merge is consequential DO and requires explicit authority;
- re-observe resulting identities and record receipts.

See [Git Branching Strategy](../process/git-branching-strategy.md).

## Verification

Use the cheapest high-information court first:

```text
narrow -> unit -> integration -> e2e -> chaos -> stress -> benchmark -> machine report
```

Do not rerun an unchanged failure without a new hypothesis. Convert learned boundaries into permanent guards/refusals/fixtures/schemas/verifiers.

`ALIVE` means observed execution for the exact admitted subject.

## Project-specific context

**Project:** Engineering Standards Root  
**Canonical namespace:** `https://w3id.org/chatman/engineering-standards#`  
**Current root manifest:** [`MANIFEST.json`](../MANIFEST.json)

Historical agent transcripts and archived proposals are evidence only. Active root law lives in the manifest, semantic graph, shapes, protocol, and task-specific active standards.

## Links

- [Semantic Engineering Protocol](../process/semantic-engineering-protocol.md)
- [Feature Workflow](../process/feature-development-workflow.md)
- [Technical Workflow](../process/technical-work-workflow.md)
- [Planning](../process/project-planning-standards.md)
- [Issue Projection](../process/issue-tracking.md)
- [Documentation Projection](../process/documentation-standards.md)
- [Compound Engineering Profile](../process/compound-engineering-integration.md)
- [Code Standards](../code/)
