# Verification, Replay, and Standing

## Purpose

Separate "a check ran" from "the exact subject has evidence standing."

Machine contracts:
- `semantic/schemas/evidence-receipt.schema.json`
- `semantic/schemas/standing-assertion.schema.json`

## Evidence coordinates

Every consequential claim is indexed by:

```text
subject
x source identity
x candidate identity
x graph identity
x toolchain
x configuration
x environment
x verifier
x consequence boundary
```

Evidence can be reused only when the relevant coordinates match.

`VERIFIER_ALIVE` and `SUBJECT_ALIVE` are separate claims.

## Verification ladder

```text
narrow
-> unit
-> integration
-> e2e
-> chaos
-> stress
-> benchmark
-> machine report
```

Use the cheapest court with enough information to falsify the current hypothesis. Expand only after that boundary closes.

## Failure loop

```text
preserve failure
-> classify failed transition
-> new hypothesis
-> narrow repair
-> permanent guard/refusal/fixture/schema/theorem
-> rerun boundary
-> expand
```

Do not repeat an unchanged failure with no new hypothesis.

## Receipts

A receipt must bind real observed consequence. A filename containing "receipt" or a planned receipt is not a receipt.

Root receipts bind:
- WorkOrder;
- authority decision;
- repository/base/candidate identities;
- graph digest;
- execution identity;
- consequence digest;
- verifier identity;
- observed consequence;
- replay identity;
- time/process objects where relevant.

A receipt is evidence. It does not self-promote standing.

## Replay

Replay reconstructs claimed state from admitted inputs and receipts.

Replay is required when the claim depends on recoverability, crash-window correctness, deterministic manufacture, or durable process state.

Replay should fail if:
- a subject identity changes;
- a dependency/graph/consequence digest changes;
- an expected receipt is absent;
- selection among multiple subjects is ambiguous.

## Standing

### UNKNOWN

No admitted execution evidence for the exact claim. UNKNOWN is not a softer form of ALIVE.

### PARTIAL_ALIVE

A required boundary has executed, but another required boundary remains unproven.

### ALIVE

Requires observed execution for the exact admitted subject satisfying the declared court. The root standing schema additionally requires at least one receipt plus observed execution and verified replay for the root ALIVE example.

### BLOCKED

Acceptance remains unmet **and every currently lawful authorized relevant route has been exhausted**. A failed transport or principal alone is not BLOCKED.

### BUILD_BROKEN

Build prevents the declared court from executing.

### UNSUPPORTED

Required capability is absent. Do not report REFUSED when no capability exists to refuse.

### REFUSED

Admission/policy deliberately denied the request with a typed reason.

## Exact-head law

For source-bound GitHub claims, the PR head, evaluated commit, workflow head, and receipt candidate SHA must match.

An older green run has no authority over a newer head.

## CI

CI is a remote execution/evidence plane, not truth. Queue state, infrastructure failure, dependency failure, and branch regression are distinct classifications.

Prefer exact immutable artifacts/receipts so evidence can be independently inspected or replayed.
