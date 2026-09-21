# Engineering Standards

**The root engineering constitution for the Chatman ecosystem.**

This repository defines the canonical semantics and operating laws for engineering work: admission, work identity, planning, manufacture, authority, actuation, evidence, replay, standing, and the conversion of solved work into reusable machinery.

## Root topology

```text
                    engineering-standards
                           ROOT
                            |
          +-----------------+------------------+
          |                 |                  |
       sJira              SA2A          ggen / marketplace
   work/evidence       transport/runtime       manufacture
          |                 |                  |
          +----------- authority --------------+
                            |
                     BRCE / CommandBus
                            |
                           DO
                            |
                    receipt -> replay
                            |
                         standing
```

APS is predecessor evidence. Its durable laws have been carried into this root; it no longer sits above this repository.

## Start here

1. [`MANIFEST.json`](./MANIFEST.json) — machine authority map.
2. [`AGENTS.md`](./AGENTS.md) — agent/operator constitution.
3. [Root ontology](./semantic/semantic-engineering-profile.ttl) — canonical machine vocabulary.
4. [SHACL court](./semantic/semantic-engineering-shapes.ttl) — root admission constraints.
5. [Semantic Engineering Protocol](./process/semantic-engineering-protocol.md) — normative human-readable law.
6. Task-specific process or code standards.

## Core law

```text
OBSERVE -> ADMIT -> WORK -> CLOSURE -> SELECT -> CONSTRUCT
        -> AUTHORITY -> DO -> RECEIPT -> REPLAY -> STANDING -> REUSE
```

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

The design target is simple: **every solved class of engineering work should reduce the amount of exceptional intelligence required the next time it appears.**

## Repository structure

- **[`semantic/`](./semantic/)** — canonical ontology, SHACL court, transport schemas, downstream/compatibility profiles.
- **[`process/`](./process/)** — normative engineering processes projected from root law.
- **[`code/`](./code/)** — language/stack standards subordinate to root semantics.
- **[`ai/`](./ai/)** — agent/tooling profiles; AI is an interface to unresolved semantic boundaries, not the root authority.
- **[`templates/`](./templates/)** — adoption projections for repositories.
- **[`scripts/`](./scripts/)** — executable qualification courts.
- **[`docs/`](./docs/)** — ADRs, plans, solutions, and explanatory projections.
- **[`archive/`](./archive/)** and **[`agent-transcripts/`](./agent-transcripts/)** — historical evidence only.

## Downstream profiles

### Semantic Jira — work/evidence

sJira projects `es:WorkOrder` into Jira/GitHub/PRD/ARD/plan surfaces. The graph is canonical; generated work artifacts carry `projectionAuthority = NONE`.

### Semantic A2A — transport/runtime

SA2A carries exact semantic subject identity and capabilities between machines. Authentication and capability do not grant authority.

### BRCE / CommandBus — consequence

Only an explicit authority broker may cross into consequential DO. Every consequential execution emits a durable receipt.

### ggen / ggen-marketplace — manufacture

Repeatable projections should be manufactured from semantic source. Current marketplace prior art includes semantic documentation, semantic projection, semantic manufacture epochs, SHACL projection, GitHub cloud doctrine, and pack protocol packs.

## Public standards before local invention

The root uses W3C/industry standards where the semantics fit: PROV-O for provenance, SHACL for graph constraints, ODRL for policy, DCMI/OSLC for lifecycle metadata/interoperability, PROF/DCAT for profiles/distributions, OCEL for object-centric process evidence, and SLSA for software provenance. Local terms are residue for concepts those standards do not exactly express.

## Process standards

Start with the [process index](./process/README.md).

Root lifecycle:
- [Semantic Engineering Protocol](./process/semantic-engineering-protocol.md)
- [Authority and Actuation](./process/authority-and-actuation.md)
- [Verification, Replay, and Standing](./process/verification-replay-standing.md)
- [Semantic Manufacturing](./process/semantic-manufacturing.md)
- [Repository Adoption](./process/repository-adoption.md)
- [Process Intelligence](./process/process-intelligence.md)

Human coordination projections:
- [Feature Development Workflow](./process/feature-development-workflow.md)
- [Technical Work Workflow](./process/technical-work-workflow.md)
- [Project Planning Standards](./process/project-planning-standards.md)
- [Issue Tracking](./process/issue-tracking.md)
- [Documentation Standards](./process/documentation-standards.md)
- [Git Branching Strategy](./process/git-branching-strategy.md)
- [Compound Engineering Integration](./process/compound-engineering-integration.md)

Those documents are subordinate views of the root, not independent constitutions.

## Documentation Mode and Semantic Work Mode

**Documentation Mode** is retained for small projects: a maintained spec can act as the practical source of truth.

**Semantic Work Mode** is the ecosystem default: the admitted semantic graph is canonical, while specs, issues, plans, messages, generated source, and dashboards are projections.

Do not maintain two independent truths.

## Verification

```bash
cd scripts && npm ci --no-audit --no-fund && cd ..
node scripts/check-docs.mjs
python -m pip install --disable-pip-version-check -r scripts/requirements-semantic.txt
python scripts/check-semantic-standard.py
```

The semantic court parses every Turtle graph, validates every JSON schema, executes positive SHACL admission, and manufactures negative authority/identity/projection falsifiers.

CI runs the same semantic court and uploads an exact-head root-conformance receipt artifact on success.

Repository conformance does not by itself prove runtime SA2A, Jira mutation, CommandBus DO, deployment, publication, or cross-repository standing.

See [Root Architecture](./docs/engineering/root-architecture.md) for the authority/projection topology.

## Change law

When a downstream system learns something reusable:

```text
observe downstream
-> propose root law
-> prior-art/equivalence fence
-> ontology/schema/verifier
-> qualify
-> regenerate/re-adopt downstream
```

The root succeeds when downstream repositories need **less** repeated reasoning.
