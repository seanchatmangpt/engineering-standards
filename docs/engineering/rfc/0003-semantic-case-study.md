# RFC-0003: Semantic Case Study

**Status:** FINAL_SPEC — closed for v26.9.24; amended 2026-09-24 for the v26.9.25
machine-addressable form (§9, per the §8 amendment rule)
**Release:** v26.9.24 (amended for v26.9.25)
**Role:** normative definition of an admitted semantic case study and its projections
**Authority:** NONE
**Consequence:** documentation / admission contract only
**Implementation standing:** PARTIAL — applied by the xaas WD Case Study 2 / STOGAF episode
(cs: vocabulary + SHACL shapes + claims ledger, witnessed at
`seanchatmangpt/xaas@f9670f446537ddb882edf9cd7e0b6519de557e60`); the zoela ZOE digital-twin
case-study element is reclassified **NOT_CLAIMED** (terminal disposition in §9.2); the generic
case-study compiler is owed by the `semantic-case-study-pack` (§9.1), not claimed by this RFC
**Supersedes:** none. A search of every seanchatmangpt repository, every remote branch, and the
operator's local plan/migration directories on 2026-09-24 found no prior normative artifact titled
"Semantic Case Study" (the v26.9.21 requirement had no canonical file); this RFC is its first
normative form.

## 1. Purpose

A case study is the most persuasive projection an engineering organization produces and the
easiest one to over-claim. This RFC defines a *semantic* case study: an admitted, exact-subject
evidence object from which narratives, decks, PRDs, work graphs and receipts are manufactured as
projections, and which can never become the source of truth, authority, or external standing.

## 2. Definition

A semantic case study is the tuple

```text
CaseStudy = Subject × Provenance × Claims × Evidence × AuthorityCeiling
          × Falsifiers × Projections × Receipts × Replay × Standing
```

| Component | Meaning | Required binding |
|---|---|---|
| Subject | the system, episode, or change the case is about | exact identities (`owner/repo@40-hex`, ontology IRI, or artifact digest) |
| Provenance | where every input came from and when | source identity + retrieval time + admitting court per input |
| Claims | each assertion the case makes | stable claim id; one claim = one falsifiable statement |
| Evidence | observations supporting a claim | exact subject + validator identity/digest + result per claim |
| AuthorityCeiling | the most the case may authorize | one of `NONE`, `SELECT`, `CONSTRUCT` (never `DO`) |
| Falsifiers | the observation that would kill each claim | at least one executable or observable falsifier per claim |
| Projections | human/machine renderings (see §4) | each projection names the case revision and claim ids it renders |
| Receipts | records of courts that admitted evidence | BRCE receipt fields (RFC-0001): identity, authority, consequence, replay, standing |
| Replay | how to recompute projections and verdicts | commands + pinned inputs; byte-identical projection on replay |
| Standing | the derived status of each claim | `ALIVE`, `PARTIAL_ALIVE`, `BLOCKED(type)`, `REFUSED(type)`, `UNSUPPORTED(type)`, `UNKNOWN` |

Standing is derived from receipts bound to the exact subject; it is never stored as a literal
field that survives a subject change.

## 3. Invariants

1. `narrative != truth` — prose renders claims; it does not establish them.
2. `slide != source` — a deck is a projection of the case revision; editing a slide never edits
   the case.
3. `case study != authority` — the AuthorityCeiling is at most `CONSTRUCT`; consequential action
   flows only through BRCE (RFC-0001) with its own authority and receipt.
4. `projection != canonical state` — every projection is regenerable from the case + pinned
   generator; hand edits to a projection are refused on regeneration.
5. `adjacency != evidence` — co-location, shared vocabulary, or temporal proximity is not
   evidence for a claim.
6. Every claim binds exact supporting evidence (§2); a claim with no evidence has standing
   `UNKNOWN`.
7. `UNKNOWN` remains `UNKNOWN` — no projection may render an `UNKNOWN` claim as supported.
8. External or customer standing (acceptance, deployment, business outcome) cannot be inferred
   from repository-local evidence. Such claims carry an evidence ceiling
   (`REPO_LOCAL_FIXTURE`, `REPO_LOCAL_CI`, `EXTERNALLY_OBSERVED`) and are `BLOCKED(evidence:external)`
   until externally observed.

## 4. Projections

One admitted case revision may manufacture any number of projections:

```text
human narrative · executive summary · deck · PRD · ARD · sJira WorkOrders · STOGAF view
SA2A capability projection · machine receipt · replay artifact
```

Rules:

- a projection records `(case_id, case_revision_digest, generator_identity, claim_ids[])`;
- a projection may omit claims but may not add a claim absent from the case;
- a projection's rendering of a claim carries that claim's current standing and evidence ceiling;
- sJira WorkOrders projected from a case are admitted through the Semantic Jira pipeline
  (ggen_igniter RFC-SEMANTIC-JIRA) and never carry authority beyond the case ceiling.

## 5. Composition with the v26.9.24 architecture

```text
SemanticSubject
  ↓ admitted observations
SemanticCaseStudy
  ├── STOGAF architecture episode      (xaas RFC-STOGAF)
  ├── sJira work graph                 (ggen_igniter RFC-SEMANTIC-JIRA)
  ├── SA2A capability projections      (ash_a2a RFC-SA2A-001/002)
  ├── OCEL evidence                    (process-intelligence producers)
  ├── GALL courts                      (GALL-001..030 PRD/ARD)
  ├── human narrative / deck           (ggen-marketplace pptx-presentation-pack)
  └── receipts / replay                (RFC-0001 BRCE; affidavit adapter)
        ↓
chatman-ecosystem cross-product court (XPROD) evaluates correspondence across dimensions
```

The case study is an evidence organizer. It owns none of the dimensions it references and is not
itself the source of truth for any of them.

## 6. Applications (non-normative)

- **WD Case Study 2 / STOGAF** (xaas `docs/case-studies/wd-fa/`, RFC-STOGAF-v26.9.22): episode
  bounded by `evidence_ceiling = REPO_LOCAL_FIXTURE`, `authority = SELECT_CONSTRUCT_ONLY`,
  `human_gate = ENGINEER_DISPOSITION_REQUIRED`; the WD deck is a pptx projection manufactured
  from `docs/case-studies/wd-fa/presentation/*.ttl`.
- **ZOE digital-twin case studies** (zoela `docs/case-studies/`,
  `ontology/digital-twin-case-studies.ttl`): application instances; not the universal ontology.
  Implementation standing for this RFC: `NOT_CLAIMED` (§9.2).

## 7. Falsifiers

This RFC is falsified if any of the following is observed without a refusal:

1. a projection renders a claim whose evidence is absent or bound to a different subject SHA;
2. a projection's claim standing differs from the standing derived from the case receipts;
3. a case or projection is used as the authority for a DO transition;
4. an `UNKNOWN` or `BLOCKED(evidence:external)` claim is rendered as supported;
5. regenerating a projection from the same case revision and generator does not reproduce it
   byte-for-byte.

## 8. Successor rule

New case-study semantics require RFC-0003 amendments. Implementation of a generic case-study
compiler is a typed sJira implementation obligation, not an open RFC question.

## 9. Machine-addressable form (v26.9.25)

This section exercises the §8 amendment rule. RFC-0004 (v26.9.25 self-closing release, §21/§24)
requires the Semantic Case Study to exist as machine-addressable structure —
`CaseStudyOntology → ggen → {Document, Presentation, ClaimsLedger, EvidenceManifest}` — rather
than prose maintained per episode.

### 9.1 Canonical implementation: `semantic-case-study-pack`

The canonical implementation of this RFC is **`semantic-case-study-pack`**
(`ggen-marketplace`, `packs/semantic-case-study-pack`), authored under RFC-0004 §24. It:

- **ports `cs:`** — the witnessed xaas case-study vocabulary `urn:xaas:case-study:`
  (`xaas/priv/packs/wd_cs2_pack/`: `case-study.ttl`, `case-study-shapes.ttl`, `claims.ttl` —
  a 268-line WD claims ledger bound to exact subject
  `seanchatmangpt/xaas@f9670f446537ddb882edf9cd7e0b6519de557e60` with evidence, falsifiers,
  non-claims, and assumptions) — from a repo-local instance pack into the reusable marketplace
  pack. The xaas `wd_cs2_pack` remains the first instance; the marketplace pack becomes
  canonical. Divergence between them is a failed edge to be recorded against the pack, not a
  fork;
- **composes**, per the reuse-before-invent ladder:
  `es:` evidence-standing-pack (`https://ggen.dev/ontology/evidence-standing#`) for the
  evidence/standing vocabulary, `do:` decision-optionality-pack
  (`https://ggen.dev/ontology/decision-optionality#`) for authority-ceiling and optionality,
  and `pres:` pptx-presentation-pack (`https://ggen.dev/ns/presentation#`) for deck
  projections (§4).

### 9.2 Terminal disposition: implementation-standing inconsistency

The v26.9.24 text claimed this RFC was "applied by … the zoela ZOE digital-twin case studies".
Disposition, terminal for v26.9.25: **that element is reclassified `NOT_CLAIMED`**; the xaas
WD element remains `PARTIAL` on witnessed evidence. An uncommitted edit attempting a wholesale
`NOT_CLAIMED` reclassification was lost from the worktree before admission; this amendment
restores its zoela element while preserving the witnessed xaas claim rather than discarding it.
Reasoning:

1. no receipt binds the zoela digital-twin artifacts to the §2 tuple — inspection of application
   instances is not implementation evidence (`inspection ≠ execution`, RFC-0001);
2. RFC-0004 Appendix A places ZOE vision work at strategy/specification standing, explicitly
   not implementation standing (§12 of the v26.9.25 requirements);
3. the honest split is therefore: xaas WD CS2 = `PARTIAL` (witnessed `cs:` implementation),
   zoela ZOE digital-twin = `NOT_CLAIMED` (application instance only, §6), generic compiler =
   owed by `semantic-case-study-pack` (§9.1) as the typed sJira obligation of §8.

### 9.3 Anti-vacuity falsifier (pack admission requirement)

A gate with no witnessed refusal carries no bits. `semantic-case-study-pack` is admitted only
if its gates fail the following mutant, derived from the witnessed instance-pack precedent
`cssh:SupportedClaimShape` (a `cs:Claim` must carry `cs:standing "UNKNOWN"` or at least one
`cs:supportedBy`):

> **Falsifier F-CS1:** mutate an admitted case so that a non-`UNKNOWN` claim loses its
> `supportedBy` evidence binding (equivalently: its evidence is re-bound to a different subject
> SHA). The pack gates MUST refuse the mutant. A pack whose gates pass this mutant is not
> admitted (`admission_vacuous`).

The witnessed refusal (command, exit code, subject SHA) is the pack's anti-vacuity evidence and
must be replayable from the pack's own fixtures.
