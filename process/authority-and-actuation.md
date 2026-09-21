# Authority and Actuation

## Purpose

Define the sole lawful transition from a selected/constructed candidate to consequential DO.

```text
candidate
-> actuation intent
-> authority policy
-> ADMITTED | REFUSED
-> DO
-> evidence receipt
```

An agent, authenticated identity, capability, plan, proof, issue status, CI result, or generated artifact is never an authority grant.

Machine contracts:
- `semantic/schemas/actuation-intent.schema.json`
- `semantic/schemas/authority-decision.schema.json`
- `semantic/schemas/refusal.schema.json`

## Authority dimensions

A grant is bounded by at least:

- **subject** — exact WorkOrder/consequence identity;
- **principal** — who/what may execute;
- **capability** — what transition is addressable;
- **scope** — target resource/repository/environment;
- **time** — validity/expiry when relevant;
- **policy** — rule that admitted the consequence;
- **identity** — exact source/graph/base/candidate coordinates;
- **consequence** — what may change.

Authority is not transferable by narrative implication.

## BRCE

BRCE is the canonical consequence route:

```text
parse
-> route
-> admit | refuse
-> diagnose / repair
-> construct
-> authority decision
-> DO
-> receipt
-> replay / hook
-> standing
```

Implementations may name the broker differently. They must preserve the transitions.

### Hooks

Hooks express intent or deterministic guards. They never manufacture authority.

### Planner/proof boundary

A planner may prove reachability. A solver may prove satisfiability. A theorem prover may prove an invariant. None grants permission.

## Refusal

A refusal is a positive, durable system result, not an exception-shaped absence.

Use typed `REFUSED` when an existing capability is denied by admission/policy. Use:

- `UNSUPPORTED` when the capability does not exist;
- `BLOCKED` when acceptance is unmet and no lawful authorized route remains;
- `BUILD_BROKEN` when the build prevents the declared verification boundary.

Do not collapse those states.

## Idempotency and replay

Consequential commands should carry a stable replay/idempotency identity. Retrying after uncertainty must consult durable receipts/reconciliation state rather than blindly repeating consequence.

Crash windows are part of the authority design.

## GitHub as consequence

Creating blobs/trees/commits, updating refs, merging, publishing releases, changing issues, and modifying workflow state are distinct consequences.

A draft PR publication can be authorized while merge remains outside the grant.

For each GitHub mutation retain:
- previous identity;
- requested operation;
- acting authority;
- new identity;
- observed consequence.

## Emergency policy

Emergency response may use a pre-admitted policy with broader time-critical permissions. "Emergency" is not itself authority. The policy, scope, principal, and receipt requirements remain explicit.

## Falsifiers

The authority boundary is falsified if any of these can produce consequence:

- a work projection with `authority=NONE`;
- an authenticated but ungranted identity;
- an SA2A capability advertisement alone;
- a valid plan/proof alone;
- a refused decision that also grants DO;
- a retry that can duplicate an already receipted consequence without reconciliation.

Encode each observed failure permanently in schemas/tests/policy.
