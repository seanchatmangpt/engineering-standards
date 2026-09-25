# Process Intelligence

## Purpose

Make engineering execution analyzable as an object-centric process rather than a sequence of narrative tickets.

The root machine envelope is `semantic/schemas/process-evidence-event.schema.json`. It is designed as an OCEL-oriented projection; the OCEL standard remains the external process-event substrate.

## Objects

Events should reference the real objects affected by work, for example:

- WorkOrder;
- Repository;
- Commit / branch / PR;
- semantic graph;
- generated artifact;
- authority decision;
- execution epoch/worker;
- receipt;
- verifier;
- deployment/runtime resource.

A single flat case ID loses cross-object causality.

## Activities

Prefer semantic transition names over UI clicks:

```text
observe
admit
refuse
select
construct
authorize
actuate
verify
replay
promote-standing
repair
publish-projection
```

## Required uses

Process evidence supports:
- conformance checking;
- variant discovery;
- bottleneck and rework analysis;
- authority exception analysis;
- failure propagation;
- throughput/WIP analysis;
- automation/generator opportunity discovery;
- replay/reconciliation;
- economic/process fitness analysis.

Process mining output is observational/analytical evidence. It does not itself grant authority.

## Conformance

The reference lifecycle is:

```text
OBSERVE -> ADMIT -> WORK -> SELECT/CONSTRUCT
        -> AUTHORITY -> DO -> RECEIPT -> REPLAY -> STANDING
```

Not every WorkOrder must visit every optional planning/construction activity, but no consequential DO may skip required authority/receipt edges.

## Learning from variants

A recurring successful variant is a candidate manufacturing pattern.

A recurring failure variant is a candidate refusal/guard/schema/falsifier.

The terminal action of process intelligence is not a dashboard; it is a change in the root/project formal machinery when evidence justifies it.

## Measurement discipline

Separate:
- process-valid;
- semantic/admission-valid;
- consequence-valid;
- postcondition-valid;
- standing-valid.

A conformant unsafe process is still unsafe. A successful consequence through an unauthorized path is still a protocol violation.
