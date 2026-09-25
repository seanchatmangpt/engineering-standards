# RFC-0003: Semantic Case Study

**Status:** FINAL_SPEC — closed for v26.9.24
**Release:** v26.9.24
**Role:** normative definition of an admitted semantic case study and its projections
**Authority:** NONE
**Consequence:** documentation / admission contract only
**Implementation standing:** NOT_CLAIMED (generic case-study compiler). Applications: the xaas
WD Case Study 2 / STOGAF episode (STOGAF court ALIVE at xaas `7c457827`, merged `f9670f44`) and the
zoela ZOE digital-twin case studies (branch-only application, not part of this closure)
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
