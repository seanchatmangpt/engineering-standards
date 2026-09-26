# Engineering Standards Root Rule

**Status:** FINAL — in force (R25-007 disposition, v26.9.25 sweep)

This project follows the root engineering constitution from
[seanchatmangpt/engineering-standards](https://github.com/seanchatmangpt/engineering-standards).

Read local `AGENTS.md` first. The root order is:

```text
MANIFEST -> semantic graph -> SHACL/admission -> process standard -> code profile
```

## Hard boundaries

- Received != Admitted
- Ticket != Authority
- Agent != Authority
- Capability != Authority
- Plan/Proof != Authority
- SELECT != CONSTRUCT != DO
- Generated artifact != semantic authority
- Inspection != execution
- UNKNOWN != ALIVE
- zero unreceipted actuation

## Work

In Semantic Work Mode, bind all work to the canonical WorkOrder and exact repository/base identity. Specs, issues, plans, messages, reviews, and generated code are projections/candidates.

In Documentation Mode, a maintained spec/issue can be the practical work record for small projects.

## Before invention

Search:
1. repository doctrine and solved-problem corpus;
2. public standards/ontologies;
3. framework-native generators;
4. ggen-marketplace/admitted reusable machinery;
5. formal planners/solvers/rule/process tools.

Reuse -> compose -> extend -> invent.

## Git

- exact base first;
- coherent subject-scoped branch;
- draft PR by default;
- exact-head CI;
- explicit authority for merge/deploy/external mutation;
- receipt/re-observe consequence.

## Verification

Use the narrowest high-information court first. A green check is bounded evidence only. Promote ALIVE only for the exact subject actually executed and verified.

Full root protocol: [process/semantic-engineering-protocol.md](../../../process/semantic-engineering-protocol.md).
