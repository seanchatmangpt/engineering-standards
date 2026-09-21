# Semantic Root

This directory contains the machine-readable root of the engineering standards.

## Authority

`semantic-engineering-profile.ttl` is the canonical vocabulary/profile. It is deliberately **not** a profile of APS. It profiles public standards directly and treats APS as predecessor evidence through `compat/aps-v26.9.17.ttl`.

`semantic-engineering-shapes.ttl` is the admission court for root WorkOrders, generated artifacts, and evidence receipts.

`semantic-work-envelope.schema.json` is a transport projection. A valid envelope is not authority.

## Profiles

- `profiles/sjira.ttl` — work/evidence projection into Semantic Jira.
- `profiles/sa2a.ttl` — machine transport/runtime projection into SA2A.
- `profiles/manufacturing.ttl` — reuse of ggen-marketplace manufacturing capital.
- `profiles/documentation.ttl` — documentation as revision-bound non-sovereign projection.
- `compat/aps-v26.9.17.ttl` — predecessor migration map.

Profiles use explicit `es:CompatibilityMapping` resources rather than OWL equivalence assertions. A mapping can be carried, profiled, residue, or superseded.

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

Generated artifacts must carry `es:projectionAuthority es:NONE`.

## Verification

```bash
python -m pip install --disable-pip-version-check -r scripts/requirements-semantic.txt
python scripts/check-semantic-standard.py
```

The verifier parses every Turtle graph under `semantic/`, validates JSON schemas, executes the positive SHACL fixture, and manufactures negative mutations for authority smuggling, bad identity, and non-sovereign projection violations.
