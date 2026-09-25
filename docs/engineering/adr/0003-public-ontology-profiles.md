# ADR-0003: Public Ontology Profiles with Explicit Local Residue

**Date:** 2026-09-21  
**Status:** Accepted

## Decision

The engineering root profiles and reuses public standards before creating local vocabulary. Local terms are permitted only for semantics that cannot be represented exactly without fabrication.

The root uses W3C Profiles Vocabulary to state profile relationships and explicit `es:CompatibilityMapping` resources for migration/downstream correspondence.

No `owl:equivalentClass` or `owl:equivalentProperty` assertion is admitted merely because terms are adjacent in meaning.

## Public substrates

Current root substrates include:

- PROV-O — provenance entities/activities/agents/derivations;
- SHACL — RDF admission constraints;
- ODRL — policy model where its semantics fit;
- DCMI Terms — identifiers/titles/descriptions/general metadata;
- OSLC — change/lifecycle interoperability where exact;
- PROF — profile relationships;
- DCAT — catalog/distribution interoperability;
- OCEL — object-centric process evidence projection;
- SLSA Provenance — software build/material provenance where exact.

## Residue

The root retains local vocabulary for engineering semantics not exactly supplied by those standards, including:

- evidence standing (`UNKNOWN`, `PARTIAL_ALIVE`, `ALIVE`, etc.);
- authority ceilings and SELECT/CONSTRUCT/DO distinction;
- WorkOrder exact engineering subject binding;
- falsifiers/courts;
- replay identity;
- generated-artifact sovereignty rule;
- explicit compatibility disposition.

Residue is not a failure. It is the typed remainder after exact public edges have been attempted.

## Mapping rule

For each candidate public mapping:

```text
local semantic requirement
-> candidate public term
-> equivalence/compatibility test
-> carry/profile if exact enough
-> otherwise record failed edge + retain residue
```

Do not weaken a requirement merely to eliminate a local term.

## Consequences

- downstream systems get one shared root vocabulary instead of private near-duplicates;
- public ecosystem tools can consume provenance/profile/policy/lifecycle data where standardized;
- failed mappings remain visible rather than silently coerced;
- future public standards can retire residue incrementally;
- ontology maintenance becomes an evidence-driven compatibility process.

## Falsifiers

Revisit this decision if:
- local residue grows because public prior art is not actually being searched;
- mappings require extensive semantic caveats that make the public term misleading;
- an admitted public standard now exactly covers a local residue term;
- interoperability costs exceed the benefit of the selected public profile.

## Evidence ceiling

This ADR records ontology design law. It does not prove external consumers implement or interpret every profile correctly.
