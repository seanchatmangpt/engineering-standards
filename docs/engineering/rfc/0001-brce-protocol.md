# RFC-0001: BRCE Protocol v0.1

**Status:** FINAL_SPEC — v0.1 (v26.9.24)  
**Category:** Architecture / execution safety / interoperability  
**Protocol:** BRCE  
**Normative independence:** This RFC defines BRCE without requiring any particular repository, runtime, planner, ontology, formal method, receipt engine, or AI system.

## Abstract

BRCE defines a transport-neutral protocol for converting intent into an externally consequential action while preserving explicit admission, authority, provenance, verification, replay, and standing.

Its governing invariants are:

[
SELECT \neq CONSTRUCT \neq DO
]

and

[
\boxed{DO \Rightarrow ValidAuthority}
]

A component may choose an action without receiving authority to execute it. A component may construct an executable representation without executing it. Only `DO` may cross the governed consequence boundary.

BRCE further requires that every governed consequence have a recoverable receipt path:

[
\boxed{Consequence \Rightarrow RecoverableReceiptPath}
]

## 1. Scope

BRCE applies to operations that may change state outside the reasoning/construction boundary, including writes, deletes, sends, publishes, deployments, transfers, grants, revocations, package publication, infrastructure changes, and physical actuation.

BRCE does not prescribe how goals are selected, how planning works, which programming language is used, which persistence system is used, or which formal method verifies an implementation.

## 2. Normative terms

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

## 3. Core pipeline

A conforming implementation preserves the semantic separation of:

[
Parse
\rightarrow Route
\rightarrow Admit/Refuse
\rightarrow Diagnose/Repair
\rightarrow Construct
\rightarrow Authorize
\rightarrow DO
\rightarrow Receipt
\rightarrow Verify
\rightarrow Replay
\rightarrow Standing
]

Implementations may combine internal modules, but MUST preserve these distinctions in evidence and behavior.

## 4. Typed evidence

A conforming implementation MUST distinguish at least:

- observed
- admitted
- constructed
- authorized
- executed
- changed
- verified
- replayable
- refused
- blocked
- unsupported

These assertions are not interchangeable.

[
executed \not\Rightarrow changed
]

[
changed \not\Rightarrow verified
]

[
UNKNOWN \not\Rightarrow ADMITTED
]

## 5. Request

A request logically contains:

```text
Request
  request_id
  subject
  requested_operation
  requested_target
  parameters
  requester_identity
  created_at
```

A canonical digest SHOULD identify the request:

[
D_R = H(Canonical(Request))
]

## 6. Routing

Routing identifies a capability or executor class that could handle the request.

```text
RouteDecision
  request_id
  capability
  executor_class
  route_evidence
```

Routing MUST NOT grant execution authority.

## 7. Admission

Admission MUST yield exactly one of:

```text
ADMITTED
REFUSED(reason)
BLOCKED(reason)
UNSUPPORTED(reason)
```

- **ADMITTED** — known requirements are satisfied sufficiently to continue.
- **REFUSED** — the request is understood but policy or authority prohibits it.
- **BLOCKED** — the request may be valid, but a required dependency or fact is unresolved.
- **UNSUPPORTED** — the implementation lacks the capability to perform the requested semantics.

These outcomes MUST NOT be collapsed.

## 8. SELECT, CONSTRUCT, DO

### 8.1 SELECT

[
SELECT : O \rightarrow Candidate
]

SELECT MUST NOT create the governed external consequence.

### 8.2 CONSTRUCT

[
CONSTRUCT : Candidate \rightarrow Executable
]

CONSTRUCT MUST NOT create the governed external consequence.

### 8.3 DO

[
DO : Executable \times AuthorityGrant \rightarrow Result
]

Only DO may create the governed external consequence.

## 9. Constructed action

A constructed action logically contains:

```text
ConstructedAction
  construct_id
  request_digest
  subject
  operation
  target
  parameters
  declared_consequence
  preconditions
  idempotency_strategy
  construct_digest
```

Once an authority grant binds `construct_digest`, any material change to the construct requires a new authority evaluation.

## 10. Authority

Authority is a first-class object.

```text
AuthorityGrant
  grant_id
  issuer
  subject
  operation
  target
  construct_digest
  constraints
  issued_at
  expires_at
  maximum_uses
  consequence_scope
  grant_digest
```

A valid grant MUST bind the subject, operation, target, and, after construction, the construct digest.

Authority MUST NOT arise implicitly from:

- planner output;
- model output;
- workflow existence;
- a proof;
- a hook or callback;
- successful validation;
- a generated command;
- possession of credentials alone;
- a prior grant with a different bound subject or construct.

[
Proposal \not\Rightarrow Authority
]

[
Admission \not\Rightarrow Authority
]

[
Construction \not\Rightarrow Authority
]

### 10.1 Authority conservation

Delegation MUST NOT increase authority.

If component (A) delegates authority set (P_A) to (B), then:

[
P_B \subseteq P_A
]

### 10.2 Expiry and use count

Expired grants MUST NOT authorize new actuation.

Single-use grants MUST prevent a second distinct consequence after consumption.

## 11. Authority broker

Every implementation MUST have a logical authority-broker function.

The broker may be local code, a policy service, a database constraint, a human approval boundary, hardware-backed capability system, or another defined source.

A planner, model, hook, or workflow engine is not an authority broker merely because it can emit executable instructions.

## 12. Consequence identity

Before actuation, the implementation SHOULD assign a scoped `consequence_id`.

Retries for the same intended effect SHOULD retain the same ID. A new intended effect MUST receive a new ID.

This supports:

[
AtMostOnceEffect(consequenceId)
]

even when:

[
AttemptCount(consequenceId) > 1
]

## 13. DO preconditions

At minimum:

[
ValidAuthorityGrant
\land SubjectMatch
\land OperationMatch
\land TargetMatch
\land ConstructDigestMatch
\land NotExpired
\land UseAvailable
]

must hold before DO.

If any predicate is false or unknown, DO MUST NOT create the consequence.

## 14. Crash-window handling

When consequence and durable receipt cannot be committed atomically, BRCE requires a recoverable pre-actuation record:

```text
ActuationIntent
  consequence_id
  grant_digest
  construct_digest
  status = PREPARED
```

The reconciled path is:

[
PREPARED
\rightarrow DO
\rightarrow RECONCILE
\rightarrow RECEIPTED
]

A crash after external consequence but before final receipt MUST NOT trigger blind non-idempotent re-execution. Ambiguous state MUST remain typed, e.g. `EXECUTION_UNKNOWN` or `BLOCKED(reconciliation)`, until evidence resolves it.

## 15. Receipt

A BRCE receipt logically records:

```text
Receipt
  receipt_version
  receipt_id
  run_id
  subject
  request_digest
  route_digest
  admission_digest
  construct_digest
  authority_grant_digest
  consequence_id
  actuation
    started_at
    completed_at
    executor_identity
    result_class
    result_digest
  observed_effect
  verification
  replay_identity
  parent_receipts
  integrity
```

A receipt MUST have deterministic identity, at minimum:

[
ReceiptID = H(CanonicalReceipt)
]

A data structure named `receipt` has no standing unless the applicable verifier accepts it.

## 16. Verification

Verification evaluates claims about what happened. A verifier SHOULD be logically independent of the actuator for high-assurance profiles.

Verification MUST identify:

```text
verifier_identity
subject
claim
evidence
verdict
```

A successful process exit alone does not establish external consequence verification.

## 17. Replay

Replay SHOULD reconstruct routing, admission, construction, verification, and receipt validation without reproducing the external consequence.

A replay identity SHOULD bind subject, inputs, tool identity/version, configuration, relevant environment identity, policy identity, and dependencies.

Actual consequence re-execution is a new DO evaluation unless the implementation proves it is the same idempotent consequence.

## 18. Standing

Standing is derived from typed evidence, not from a label alone.

A canonical evidence vector is:

[
E=(O,A,C,U,X,\Delta,V,P,S)
]

where (O)=observed, (A)=admitted, (C)=constructed, (U)=authorized, (X)=executed, (Delta)=changed, (V)=verified, (P)=replayable, and (S)=standing granted.

Local labels such as `UNKNOWN`, `PARTIAL_ALIVE`, `ALIVE`, or `CERTIFIED` MAY be used, but MUST expose enough evidence to justify the label.

## 19. Negative terminal states

`REFUSED`, `BLOCKED`, and `UNSUPPORTED` are materially different and MUST remain distinct.

`UNKNOWN` means insufficient evidence; it is neither permission nor failure:

[
UNKNOWN \neq REFUSED
]

[
UNKNOWN \neq UNSUPPORTED
]

[
UNKNOWN \neq ADMITTED
]

## 20. Core safety invariants

Every conforming implementation MUST preserve:

1. **No unauthorized consequence**
   [
   DO \Rightarrow ValidAuthority
   ]

2. **Exact construct binding**
   [
   DO(C,G) \Rightarrow G.constructDigest = H(C)
   ]

3. **No authority by implication**
   [
   PlannerOutput \lor ModelOutput \lor Hook \lor Proof \lor Workflow
   \not\Rightarrow AuthorityGrant
   ]

4. **Receipt validity**
   [
   Standing \Rightarrow ValidReceipt
   ]

5. **Exact subject**
   [
   Standing(S) \Rightarrow Evidence(S)
   ]

6. **Construction cannot actuate**
   [
   CONSTRUCT \Rightarrow \neg Consequence
   ]

7. **Selection cannot actuate**
   [
   SELECT \Rightarrow \neg Consequence
   ]

8. **At-most-once consequence when declared**
   [
   count(effect(consequenceId)) \le 1
   ]

## 21. Progress property

A complete implementation SHOULD eventually classify admitted work:

[
Admitted
\leadsto
Receipted \lor Refused \lor Blocked \lor Unsupported
]

No ambiguous actuation should remain permanently hidden.

## 22. Required conformance cases

BRCE Core implementations MUST test at least:

- DO without authority → refused, zero consequence.
- expired grant → refused, zero consequence.
- construct digest substitution → refused.
- target substitution → refused.
- duplicate retry → at most one intended effect.
- crash before consequence → no confirmed effect.
- crash after consequence/before receipt → reconciliation before non-idempotent retry.
- receipt tampering → verification failure.
- hook attempts authority escalation → refused.
- verification replay → zero new external consequence.
- UNKNOWN/REFUSED/BLOCKED/UNSUPPORTED remain observable as distinct states.
- evidence for subject (S_1) cannot establish standing for (S_2).

## 23. Formal profile

Formal verification is optional in BRCE Core.

A `BRCE Formal` implementation SHOULD provide a machine-checkable transition model for at least:

[
DO \Rightarrow AuthorityValid
]

[
Standing \Rightarrow ReceiptValid
]

[
Standing \Rightarrow Verified
]

[
SELECT \Rightarrow \neg Consequence
]

[
CONSTRUCT \Rightarrow \neg Consequence
]

plus applicable duplicate-consequence constraints.

TLA+, Alloy, PlusCal, Promela/SPIN, theorem provers, or equivalent methods MAY be used. BRCE does not mandate one formal system.

## 24. Conformance levels

### BRCE Core

Requires SELECT/CONSTRUCT/DO separation, explicit authority, typed terminal outcomes, consequence identity, durable receipt path, receipt verification, crash-window handling, and exact-subject binding.

### BRCE Replay

Requires BRCE Core plus replay identity, consequence-free verification replay, bounded reconstruction, and configuration/dependency identity.

### BRCE Formal

Requires BRCE Replay plus a machine-checkable transition model, checked safety invariants, preserved counterexamples, and formal-model identity bound into evidence.

## 25. Independent implementability

A BRCE implementation MUST NOT require knowledge of the ecosystem that produced this RFC.

Conformance must be possible using only this specification plus an implementation's chosen serialization, persistence mechanism, authority system, actuator, and receipt verifier.

The following are optional adapters, not protocol dependencies:

- RDF/OWL
- SHACL/SPARQL
- TLA+
- Lean
- PDDL/HDDL
- OCEL/process mining
- Ash/Igniter
- ggen
- affidavit
- Kubernetes/GitHub
- LLMs

## 26. Primary falsifiers

A claimed BRCE Core implementation is non-conformant if any supported execution exists such that:

[
ExternalConsequence \land \neg ValidAuthority
]

or:

[
ExternalConsequence \land \neg RecoverableReceiptPath
]

Additional falsifiers:

[
Standing(S) \land \neg Evidence(S)
]

and:

[
Replay \land UnexpectedNewConsequence
]

## 27. Canonical law

[
\boxed{Intent \not\Rightarrow Authority}
]

[
\boxed{SELECT \not\Rightarrow DO}
]

[
\boxed{CONSTRUCT \not\Rightarrow DO}
]

[
\boxed{DO \Rightarrow ExplicitAuthority}
]

[
\boxed{Consequence \Rightarrow RecoverableReceiptPath}
]

[
\boxed{Standing \Rightarrow ExactSubject \land ValidReceipt \land RequiredVerification}
]

Everything else is implementation.


## 28. v26.9.24 specification closure

This protocol specification is complete at v0.1. Specification completion does not assert any implementation, deployment, or production standing.

A conforming implementation remains subject to the evidence ceilings defined above:

- BRCE Core requires executable evidence for the Core conformance cases.
- BRCE Replay additionally requires consequence-free replay evidence.
- BRCE Formal additionally requires machine-checked formal evidence bound to the exact model and verifier invocation.

Therefore:

[
FinalSpec(BRCE v0.1) 
otRightarrow ImplementationAlive
]

Future protocol changes require a new revision or an explicitly versioned amendment; implementation adapters may evolve independently while preserving this normative contract.
