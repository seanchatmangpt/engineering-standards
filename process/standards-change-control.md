# Standards Change Control

**Status:** FINAL — in force (R25-007 disposition, v26.9.25 sweep)

## Purpose

The root must obey the same evidence discipline it imposes downstream. A standards edit is not admitted root law merely because it was written, reviewed, or merged.

Machine contract: `semantic/schemas/normative-claim.schema.json`.

## Required change record

Every consequential root-law change should be reducible to a `NormativeClaim` with:

- exact claim;
- semantic scope;
- current status;
- supporting evidence;
- explicit falsifiers;
- prior-art search;
- reuse/compose/extend/invent/refuse/supersede disposition;
- evidence ceiling;
- superseded claims when applicable.

A PR description may project this record, but the machine contract owns the required fields.

## DfCM admission sequence

```text
Preserve
-> Fence
-> prior-art search
-> claim + evidence
-> exclusions
-> falsifiers
-> reuse / compose / extend / invent
-> ontology/schema/process change
-> repository court
-> exact-head receipt
-> downstream requalification
```

## Prior-art gate

Invent only when the required semantics cannot be satisfied by:

1. public standards/ontologies;
2. existing root vocabulary;
3. predecessor evidence;
4. downstream profiles;
5. framework/generator/process-science/formal-method machinery.

Record the exact failed edge. "Unfamiliar" is not a failed edge.

## Claim replacement

A corrected claim is a new claim. Evidence that refuted the old statement does not automatically verify its replacement.

When a claim changes:

```text
old claim
-> preserving evidence
-> explicit falsifier
-> replacement candidate
-> independent check
-> SUPERSEDE old claim
-> requalify dependent projections
```

Historical ADR bodies remain immutable; append dated amendments when standing decisions change.

## Downstream propagation

A root change is incomplete as ecosystem standing until affected downstream profiles requalify.

Repository-root conformance may be ALIVE while downstream adoption remains UNKNOWN/PARTIAL_ALIVE.

## Falsifiers for this process

This process fails if:
- a normative claim can be admitted with no evidence;
- a normative claim can be admitted with no falsifier;
- invention can bypass prior-art disposition;
- a replacement inherits standing solely from the proof that the old claim was wrong;
- merge status is treated as proof that downstream projections are correct.

Encode each discovered failure into the schema/verifier so the same reasoning is not purchased again.
