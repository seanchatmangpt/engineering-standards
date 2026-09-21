# ADR-0002: Engineering Standards Is the Ecosystem Root

- **Status:** Accepted
- **Date:** 2026-09-21
- **Decision:** Make this repository the canonical engineering semantic root; treat APS as predecessor evidence and sJira/SA2A as downstream profiles.

## Context

The ecosystem had accumulated the same laws in several places:

- APS carried admission, DfCM, authority separation, evidence, replay, and standing.
- Semantic Jira carried RDF WorkOrders and non-authoritative work projections.
- SA2A carried semantic machine transport and CommandBus consequence fencing.
- ggen-marketplace carried mature projection, documentation, manufacturing, and GitHub operating packs.
- this repository carried the human engineering process and project templates.

The previous integration commit still typed the combined protocol as an `aps:Contract`. That preserved the wrong dependency direction: a predecessor remained semantically above the intended root.

## Decision

`engineering-standards` becomes the root.

The root machine authority is:

```text
MANIFEST.json
  -> semantic/semantic-engineering-profile.ttl
  -> semantic/semantic-engineering-shapes.ttl
  -> process/semantic-engineering-protocol.md
  -> downstream profiles
```

APS is represented only by an explicit compatibility graph. sJira, SA2A, manufacturing, and documentation are profiles of the root.

The root profiles public standards directly rather than importing APS. Public ontology terms are reused when exact; local residue is introduced only after failed-edge analysis.

## Consequences

- one root namespace owns WorkOrder, capability, authority, receipt, replay, standing, projection, and falsifier semantics;
- downstream systems may specialize implementation without redefining root law;
- documentation and tickets become projections in Semantic Work Mode;
- generated artifacts are explicitly non-sovereign;
- new ecosystem law returns here instead of multiplying across repositories;
- APS remains immutable predecessor evidence and does not need to be deleted.

## Public prior art

The root reuses or profiles PROV-O, SHACL, ODRL, DCMI, OSLC, PROF, and DCAT. It references OCEL for object-centric process evidence and SLSA for software provenance where those semantics fit.

No OWL equivalence assertion is admitted merely because two terms are adjacent in meaning.

## Falsifiers

Reconsider this decision if:

- downstream systems cannot conserve root WorkOrder identity without semantic loss;
- the root requires implementation-specific terms that cannot remain profiles/residue;
- profile maintenance produces more duplicated reasoning than independent standards did;
- authority separation makes a necessary consequence unrepresentable;
- replay cannot reconstruct standing from admitted semantic state and receipts.

## Evidence ceiling

This ADR establishes repository architecture. It does not itself prove runtime SA2A, sJira manufacture, CommandBus actuation, publication, deployment, or cross-repository ALIVE.
