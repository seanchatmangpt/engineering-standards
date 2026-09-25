# AGENTS.md — Engineering Standards Root Constitution

This repository is the root engineering constitution for the ecosystem. Read, in order:

1. `MANIFEST.json`
2. `semantic/semantic-engineering-profile.ttl`
3. `semantic/semantic-engineering-shapes.ttl`
4. `process/semantic-engineering-protocol.md`
5. the task-specific process/code standard

No downstream repository, ticket system, agent framework, planner, generator, or predecessor document outranks those surfaces.

## Root law

The canonical operational sequence is:

```text
OBSERVE -> ADMIT -> WORK -> CLOSURE -> SELECT -> CONSTRUCT
        -> AUTHORITY -> DO -> RECEIPT -> REPLAY -> STANDING -> REUSE
```

The following distinctions are mandatory:

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
UNKNOWN != ALIVE
```

## DfCM task order

For non-trivial work execute:

1. **Preserve (守)** — exact identities, history, live behavior, reversible options.
2. **Fence (柵)** — system, boundary, origin, function; same-system evidence before replacement.
3. **Calculate (算)** — objects -> transitions -> state -> admission -> closure -> authority -> consequence -> receipt -> replay -> standing.
4. **Exclude (除)** — state rejected assumptions so they cannot silently return.
5. **Falsify (偽)** — define observations that would overturn each consequential claim.
6. **Extend (延)** — reuse -> compose -> extend -> invent.
7. **Operationalize (実)** — move recurring judgment into ontology, schema, generator, planner, policy, verifier, or process control.

A failed edge is topology. Do not collapse the graph while another lawful route remains.

## Ontology-first

Prefer public standards before local vocabulary. The root profile currently uses or profiles PROV-O, SHACL, ODRL, DCMI, OSLC, PROF, DCAT, OCEL, and SLSA. A local term is admitted only when the public candidates are semantically insufficient. Record the failed mapping.

Do not use `owl:equivalentClass` or `owl:equivalentProperty` without an equivalence proof. Compatibility graphs are mappings, not authority shortcuts.

## Work and projections

`es:WorkOrder` is the root work subject. sJira, GitHub issues, Jira issues, PRDs, plans, generated source, dashboards, and agent messages are projections or transports.

A projection:
- MUST bind the root subject identity;
- MUST carry `projectionAuthority = NONE`;
- MUST NOT promote its own standing;
- MUST NOT create DO authority.

Edit the canonical semantic source and regenerate when a projection is derivable. Hand editing generated output is a defect.

## Planning

Known planning classes route to formal machinery where practical:
- HTN -> HDDL;
- classical/FOND planning -> PDDL/FOND solvers;
- constraints -> SAT/SMT/CP;
- process conformance -> OCEL/process mining;
- rules -> declarative rule engines;
- derivable software -> templates/generators.

Use general model reasoning at the unresolved semantic boundary, not as a permanent runtime for solved classes.

## Authority and actuation

BRCE/CommandBus or an equivalent explicit authority broker is the only lawful path to consequential DO.

No ambient DO authority. No unreceipted actuation. Authentication and capability do not imply authorization.

Detailed law: [Authority and Actuation](process/authority-and-actuation.md).

## Verification

Use the narrowest high-information court first, then expand:
narrow -> unit -> integration -> e2e -> chaos -> stress -> benchmark -> machine report.

Do not rerun an unchanged failure without a new hypothesis. Turn every learned boundary into a durable guard, refusal, fixture, schema, theorem, or verifier rule.

`ALIVE` requires observed execution for the exact admitted subject. CI is evidence, never truth by itself.

Detailed law: [Verification, Replay, and Standing](process/verification-replay-standing.md).

## GitHub work

Resolve the exact base SHA. Do not silently move it.

Default publication boundary:
```text
exact base -> coherent diff -> verification -> commit -> draft PR
          -> exact-head CI -> receipt
```

Do not merge unless explicitly requested.

## Predecessors and downstream profiles

- APS is predecessor constitutional evidence.
- sJira is a downstream work/evidence profile.
- SA2A is a downstream transport/runtime profile.
- ggen/ggen-marketplace are manufacturing infrastructure and reusable capital.
- XaaS and other runtimes consume this root; they do not redefine it.

When downstream reality discovers a valid new law, bring the law back here, qualify it, and remove the repeated reasoning from downstream consumers.

Adoption and manufacture: [Repository Adoption](process/repository-adoption.md) · [Semantic Manufacturing](process/semantic-manufacturing.md) · [Process Intelligence](process/process-intelligence.md).
