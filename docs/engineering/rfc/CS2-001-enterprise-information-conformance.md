# RFC-CS2-001: Enterprise Information Conformance

**Status:** NORMATIVE CANDIDATE  
**Release:** v26.9.26  
**Role:** canonical CS2 root contract for turning enterprise information into bounded,
machine-consumable engineering information without confusing information quality,
delivery, authority, execution, or standing  
**Authority:** NONE  
**Consequence:** documentation and machine-contract definition only; this RFC never grants
authority to mutate Jira, GitHub, source code, production systems, or any other external
state  
**Machine surfaces:** \`semantic/cs2/manifest.json\`,
\`semantic/cs2/cs2-profile.ttl\`, \`semantic/cs2/cs2-shapes.ttl\`,
\`semantic/schemas/cs2-conformance.schema.json\`,
\`docs/engineering/rfc/CS2-001-requirements.json\`,
\`scripts/check-cs2-conformance.py\`

## 1. Purpose

CS2 standardizes the boundary between **information available to an engineering system**
and **information qualified for a particular engineering consumer**.

The core problem is not lack of documents, tickets, logs, dashboards, traces, source code,
or model output. The problem is that those surfaces frequently omit one or more of the
bindings required for safe downstream use:

\`\`\`text
information
  -> exact subject
  -> provenance
  -> claim
  -> evidence
  -> falsifier
  -> consumer route
  -> process binding
  -> optional consequence request
\`\`\`

CS2 provides one monotonic conformance ladder for this progression. A higher level implies
all lower levels. A producer may stop at any level. A consumer MUST state the minimum
level it requires.

CS2 deliberately separates:

- **information conformance** from truth;
- **truth claims** from evidence;
- **evidence** from authority;
- **routeability** from authorization;
- **construction** from external consequence;
- **receipts** from current standing.

A CS2 bundle is therefore an information contract, not permission to act.

## 2. Exact subject

Every bundle MUST identify one exact subject through \`subject.id\`, \`subject.kind\`, and
\`subject.revision\`.

A revision MAY be a Git SHA, immutable object digest, document revision, dataset version,
run identifier, or another immutable revision token appropriate to the subject type.

If the producer cannot identify an exact revision, the bundle cannot exceed **C0**.

A human-readable name is optional and never substitutes for identity.

## 3. Sources, claims, and evidence

CS2 treats sources, claims, and evidence as different object types.

### 3.1 Source

A source identifies where information came from. It carries a stable source id, locator,
source kind, and revision when available.

Examples:

- repository file at an exact commit;
- execution log;
- benchmark corpus;
- issue or ticket;
- design document revision;
- incident timeline;
- database snapshot;
- interview or meeting record;
- generated artifact.

A source MAY contain false or incomplete information. Source identity is provenance, not
truth.

### 3.2 Claim

A claim is a proposition about the exact subject. Every claim has:

- unique \`id\`;
- \`predicate\`;
- JSON-compatible \`object\`;
- zero or more \`source_refs\`;
- zero or more \`evidence_refs\`;
- typed \`standing\`.

At **C2** and above every claim also has an explicit falsifier.

### 3.3 Evidence

Evidence is an observation that supports, contradicts, or bounds one or more claims.
Evidence MUST bind back to the exact subject and to a declared source.

Evidence references are local ids inside the bundle. External locators remain data and
never become implicit authority.

## 4. Standing vocabulary

Claim standing is one of:

- \`OBSERVED\` — directly observed on the exact subject;
- \`DERIVED\` — mechanically derived from admitted observations;
- \`REPORTED\` — asserted by a source but not independently observed by this bundle;
- \`HYPOTHESIS\` — proposed explanation or prediction;
- \`REFUTED\` — contradicted by admitted evidence;
- \`UNKNOWN\` — insufficient information.

CS2 does not collapse these values into boolean truth.

A consumer MAY apply a stricter policy than this vocabulary, but MUST NOT silently promote
a lower standing to a higher one.

## 5. Conformance ladder

Conformance is monotonic:

\`\`\`text
C0 ADDRESSABLE
  < C1 PROVENANCE_BOUND
  < C2 FALSIFIABLE
  < C3 ROUTABLE
  < C4 PROCESS_BOUND
\`\`\`

A bundle claiming \`Ck\` MUST satisfy every requirement of \`C0..Ck\`.

### 5.1 C0 — ADDRESSABLE

Minimum useful machine identity.

Required:

1. schema version;
2. standard id \`RFC-CS2-001\`;
3. exact subject id;
4. subject kind;
5. immutable subject revision;
6. at least one uniquely identified claim.

C0 answers: **what exact thing are we talking about?**

### 5.2 C1 — PROVENANCE_BOUND

C1 adds source/evidence provenance.

Required in addition to C0:

1. at least one source;
2. every source has a locator;
3. at least one evidence object;
4. every evidence object binds to the bundle subject;
5. every evidence object references an existing source;
6. every non-UNKNOWN claim references at least one source or evidence object.

C1 answers: **where did this information come from?**

### 5.3 C2 — FALSIFIABLE

C2 adds refutation surfaces.

Required in addition to C1:

1. every claim has typed standing;
2. every non-REFUTED claim carries a falsifier;
3. every falsifier states an observation that would overturn or downgrade the claim;
4. contradictions are explicit data, never silently discarded;
5. duplicate ids across sources, evidence, and claims are refused.

C2 answers: **what observation would make us change our mind?**

### 5.4 C3 — ROUTABLE

C3 makes the bundle consumable by a named workflow without granting authority.

Required in addition to C2:

1. one route object;
2. exact consumer id;
3. workflow id;
4. projection id;
5. minimum consumer conformance level;
6. delivery semantics;
7. explicit \`projection_authority = "NONE"\`.

The route tells a system where qualified information can go. It is not an authorization
decision and MUST NOT contain credentials or provider secrets.

C3 answers: **which consumer can use this information, and through what contract?**

### 5.5 C4 — PROCESS_BOUND

C4 binds the information bundle to process evidence and replay surfaces.

Required in addition to C3:

1. \`process.ocel_ref\`;
2. \`process.receipt_schema\`;
3. \`process.replay_binding\`;
4. \`process.episode_id\`;
5. at least one process event reference;
6. an explicit consequence class;
7. if consequence class is not \`NONE\`, an authority requirement is named but no authority
   is inferred.

C4 answers: **how does this information participate in a replayable engineering process?**

C4 still does not prove execution, verification, deployment, or standing.

## 6. Consumer requirements

A consumer declares a minimum level:

\`\`\`text
consumer.minimum_level <= bundle.actual_level
\`\`\`

Examples:

| Consumer | Typical minimum |
|---|---|
| search / discovery | C0 |
| provenance-aware knowledge retrieval | C1 |
| triage / hypothesis generation | C2 |
| engineer workflow projection | C3 |
| autonomous process planner / process mining / replay | C4 |

These are defaults, not mandatory mappings. A consumer may demand a higher level.

## 7. Projection law

Projection is non-sovereign.

\`\`\`text
qualified information
  -> projection
  -> consumer-specific representation
\`\`\`

A projection MUST preserve:

- subject identity;
- subject revision;
- claim ids;
- claim standing;
- evidence ids;
- source ids;
- falsifiers at C2+;
- bundle semantic fingerprint.

A projection MAY add presentation fields such as title, priority, assignee hints, labels,
or UI grouping. Those additions do not modify the source claim set unless represented as
new claims with their own provenance.

## 8. Duplicate and conflict handling

Identifiers are unique within each bundle.

Two claims with the same id but different content are a conflict and MUST be refused.

Two different claim ids MAY express contradictory propositions. Contradiction is modeled,
not erased. Producers SHOULD connect contradictory claims through
\`contradicts\` references.

Consumers MUST NOT resolve contradictions merely by arrival order.

## 9. Semantic fingerprint

The machine implementation computes a deterministic fingerprint from canonical JSON after
removing the derived \`conformance.actual_level\` and \`conformance.issues\` fields.

The fingerprint identifies the information contract, not a mutable delivery attempt.

Consumers may use the fingerprint for caching, deduplication, and replay binding.

## 10. Failure model

Validation emits typed issues rather than a single boolean.

Issue classes include:

- \`INVALID_SHAPE\`
- \`IDENTITY_MISSING\`
- \`REVISION_MISSING\`
- \`DUPLICATE_ID\`
- \`BROKEN_REFERENCE\`
- \`PROVENANCE_MISSING\`
- \`FALSIFIER_MISSING\`
- \`ROUTE_MISSING\`
- \`PROJECTION_AUTHORITY_VIOLATION\`
- \`PROCESS_BINDING_MISSING\`
- \`REQUESTED_LEVEL_UNSATISFIED\`

A bundle can be valid at C1 while failing a request for C3. The validator therefore
returns both the highest achieved level and typed issues.

## 11. Migration and compatibility

A producer using a predecessor representation SHOULD map into CS2 through an explicit
compatibility layer. Compatibility is directional and never implies semantic equivalence.

A migration MUST preserve the predecessor identifier in \`extensions.predecessor\` and
MUST NOT invent source or evidence bindings that were absent in the predecessor.

Unknown fields belong under \`extensions\`. Core CS2 fields have closed semantics.

## 12. Security and privacy

CS2 bundles can expose high-value internal relationships.

Producers SHOULD minimize data before projection:

- use stable ids instead of credentials;
- avoid embedding secrets in locators;
- avoid unrestricted raw transcripts when a bounded observation suffices;
- retain access-control classification in extensions where required;
- separate confidential source retrieval from portable claim/evidence identity.

Conformance never means a bundle is safe to disclose.

## 13. Machine-addressable requirements

The normative requirement registry is
\`docs/engineering/rfc/CS2-001-requirements.json\`.

Every requirement carries:

- stable id;
- minimum conformance level;
- requirement text;
- falsifier;
- machine check name.

The executable consumer is \`scripts/check-cs2-conformance.py\`.

The registry is intended for generators and downstream packs; consumer repositories
SHOULD depend on requirement ids rather than duplicating prose.

## 14. Non-claims

RFC-CS2-001 does not claim that:

- a conforming claim is true;
- a conforming source is trustworthy;
- a C4 bundle was executed;
- Jira, GitHub, or another provider accepted a projection;
- an agent has authority to act;
- a receipt proves current standing;
- an LLM must be used to manufacture or consume CS2 bundles.

## 15. Canonical next edge

The next dependency-closed edge after this root is a generated CS2 pack in
\`ggen-marketplace\` that consumes the machine registry and emits consumer projections
without rewriting the normative requirement set.
