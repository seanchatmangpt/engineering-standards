# Code Construction Profiles

Language and stack-specific construction and verification profiles under the [Semantic Engineering Protocol](../process/semantic-engineering-protocol.md).

## Position in the root

```text
root/project admitted semantics
  -> construction profile
  -> framework/generator
  -> code/schema/config projection
  -> verifier
  -> authority
  -> runtime consequence
  -> receipt
```

These documents answer **how to construct and qualify a software projection in a particular stack**. They do not own work identity, semantic standing, or consequential authority.

## Cross-profile laws

- framework-native generator first when it preserves required semantics;
- reuse admitted ggen-marketplace capital before local reinvention;
- generated output is non-sovereign and should not be hand-edited;
- language types, database constraints, OpenAPI, linters, and tests prove only their declared boundary;
- integration/runtime ALIVE requires observed execution for the exact subject;
- external mutation remains behind explicit project authority.

## Active profiles

### [Python](./python-standards.md)

Python construction/tooling profile: uv, ruff, mypy, pytest, reproducible environments, packaging, CI, and deterministic qualification.

### [Database / PostgreSQL](./database-standards.md)

PostgreSQL projection profile for relational persistence and integrity. Database constraints are authoritative for admitted persisted-state invariants, while root/project semantics remain canonical for cross-system meaning.

### [Web Applications](./web-application-standards.md)

Next.js + FastAPI boundary profile. OpenAPI is the generated HTTP interface projection; clients are generated rather than manually synchronized.

## Shared construction contract

All profiles inherit [Construction, Generation, and Verification](./construction-generation-verification.md).

## Adding a code profile

Before creating a new language/framework standard:

1. prove an existing profile cannot express the required construction boundary;
2. inspect framework-native conventions/generators;
3. identify which root semantics project into the stack and which remain outside it;
4. define the narrowest verifier court;
5. identify generated vs irreducible handwritten residue;
6. add permanent falsifiers for observed failure classes.

A new profile should reduce future reasoning, not add another prose taxonomy.

## Standing

**Active profile documentation.** Runtime/tool-version claims remain subject to repository-native requalification at the exact version/head where they are used.
