# Semantic Root

This directory contains the machine-readable root of the engineering standards.

## Authority

`semantic-engineering-profile.ttl` is the canonical vocabulary/profile. It profiles public standards directly and treats APS as predecessor evidence through `compat/aps-v26.9.17.ttl`.

`semantic-engineering-shapes.ttl` is the RDF admission court for root WorkOrders, generated artifacts, and evidence receipts.

## Lifecycle contracts

The root lifecycle is machine-readable end to end:

```text
WorkOrder
  -> semantic-work-envelope
  -> actuation-intent
  -> authority-decision | refusal
  -> authorized execution
  -> evidence-receipt
  -> process-evidence-event
  -> standing-assertion
```

Schemas:

- `semantic-work-envelope.schema.json` — authority-free transport projection.
- `schemas/actuation-intent.schema.json` — request for DO; validity is not a grant.
- `schemas/authority-decision.schema.json` — explicit ADMITTED/REFUSED authority result.
- `schemas/refusal.schema.json` — durable typed fail-closed refusal.
- `schemas/evidence-receipt.schema.json` — exact execution/consequence evidence.
- `schemas/standing-assertion.schema.json` — bounded standing; ALIVE requires receipt + observed execution + replay.
- `schemas/process-evidence-event.schema.json` — object-centric process-evidence projection.

Positive fixtures live in `examples/`. The verifier also manufactures negative mutations.

## Profiles

- `profiles/sjira.ttl` — work/evidence projection into Semantic Jira.
- `profiles/sa2a.ttl` — machine transport/runtime projection into SA2A.
- `profiles/manufacturing.ttl` — reuse of ggen-marketplace manufacturing capital.
- `profiles/documentation.ttl` — documentation as revision-bound non-sovereign projection.
- `profiles/process-evidence.ttl` — OCEL-oriented object-centric process evidence.
- `compat/aps-v26.9.17.ttl` — predecessor migration map.

Profiles use explicit `es:CompatibilityMapping` resources rather than OWL equivalence assertions.

## Source / projection law

```text
engineering-standards root graph
  -> admitted profile
  -> deterministic manufacture / transport
  -> generated artifact
  -> explicit authority (if consequence is requested)
  -> DO
  -> receipt
  -> replay
  -> standing
```

Generated artifacts carry `es:projectionAuthority es:NONE`.

## Verification

```bash
python -m pip install --disable-pip-version-check -r scripts/requirements-semantic.txt
python scripts/check-semantic-standard.py
python scripts/check-semantic-standard.py --receipt /tmp/root-conformance.json
```

The court parses every Turtle graph under `semantic/`, validates all root JSON schemas and positive examples, executes SHACL, and exercises negative authority/identity/projection/standing falsifiers. CI uploads the success receipt as an exact-head artifact.

Repository semantic conformance does not prove downstream runtime execution, deployment, external mutation, or cross-repository standing.
