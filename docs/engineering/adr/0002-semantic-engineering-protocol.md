# ADR-0002: Unify APS, Semantic Jira, and SA2A as the Semantic Engineering Protocol

- **Status:** Accepted
- **Date:** 2026-09-21
- **Decision owners:** Engineering standards maintainers

## Context

Three systems had converged on the same execution boundary from different directions:

- the Agile Protocol Specification (APS) defined admitted semantics, DfCM, authority separation, receipts, replay, and standing;
- Semantic Jira (sJira) defined RDF-native WorkOrders and deterministic work projections with an OBSERVE/SELECT/CONSTRUCT ceiling;
- Semantic A2A (SA2A) defined capability transport with the explicit laws that message, identity, capability, plan, and proof are not authority.

Keeping these as separate engineering doctrines creates a repeated reasoning cost: every project must rediscover where a ticket ends, where transport begins, and where consequential authority lives.

The existing engineering standards also said that documentation is the source of truth and that GitHub issues are the primary tracker. Those statements remain useful in lightweight documentation mode, but become false when a project has adopted an admitted semantic work graph.

## Decision

Adopt the [Semantic Engineering Protocol](../../../process/semantic-engineering-protocol.md) as the canonical integration standard.

The protocol separates three planes:

1. **sJira work/evidence plane** — canonical semantic work identity and deterministic projections;
2. **SA2A interaction plane** — capability discovery and transport for exact semantic subjects;
3. **BRCE/CommandBus consequence plane** — explicit authority, consequential DO, receipts, replay, and standing.

The following equations are normative:

```text
Received != Admitted
Ticket != Authority
Agent != Authority
Capability != Authority
Plan != Authority
Proof != Authority
SELECT != CONSTRUCT != DO
```

Generated work artifacts have projection authority `NONE`. The maximum sJira authority ceiling is `CONSTRUCT`. Any consequential mutation must cross the project's authority broker / CommandBus boundary and emit evidence.

## Prior art and source identities

The decision was reconstructed from:

- APS `5c31d9d05fe36dc1eca3a26c9eb5cd267a2cf625`;
- AshA2A / SA2A `baa135d5c6129aea1d4b38d48a12ad87e132b638`;
- Semantic Jira PR #20 head `90cfd360bc6dfe041d35f7082f064716d22b4d99`;
- Semantic Jira SHACL reconciliation PR #24 head `e509b375dc84e7ac50935d0b53bcb44ea1935242`;
- engineering-standards base `610944c48bce6377291c088a3e07775e9ef2908b`.

Open or candidate implementation work is used as observed prior art only. This ADR does not inherit its runtime standing.

## Consequences

**Positive**

- one work identity can survive issue projection, SA2A transport, construction, execution, receipt, and replay;
- Jira/GitHub can remain useful interfaces without becoming semantic authority;
- agents can be replaceable because transport and capability no longer imply permission;
- the standards gain an executable RDF/SHACL/JSON conformance court rather than relying on prose alone;
- APS law is reused instead of locally re-invented.

**Costs**

- Semantic Work Mode requires a canonical graph and admission court;
- projects must bind exact repository/base identities and graph digests;
- adapters must carry subject identity through transport instead of reconstructing it from prose;
- existing issue-centric automation may require projection adapters.

## Alternatives rejected

### Keep APS, sJira, SA2A, and engineering standards as four independent doctrines

Rejected because the boundaries overlap and force each adopter to reconstruct precedence and authority repeatedly.

### Make Jira/GitHub tickets canonical

Rejected for Semantic Work Mode because mutable human projections cannot safely carry graph identity, formal admission, replay identity, and standing without becoming a competing authority surface.

### Let SA2A capabilities authorize their own execution

Rejected because capability describes what can be addressed, not who may create consequence.

### Copy APS implementation into this repository

Rejected because the useful result is the law and executable profile, not repository duplication. APS remains prior art and vocabulary source.

## Falsifiers

This decision should be reconsidered if evidence shows that:

- a single canonical work identity cannot be preserved across sJira and SA2A without lossy translation;
- the authority separation prevents necessary work that cannot be expressed through an explicit broker;
- public ontologies cannot represent the required semantics and the local residue becomes larger or less interoperable than the predecessor systems;
- replay cannot reconstruct work state from graph + receipts;
- maintaining the semantic profile costs more recurring interpretation than it removes.
