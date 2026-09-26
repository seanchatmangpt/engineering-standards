# Repository Adoption

## Purpose

Make a downstream repository a lawful consumer of the Engineering Standards root without copying the root into a local doctrine fork.

## Adoption levels

### Level 0 — Documentation Mode

Use process/code standards and maintained specs/issues as practical work records. Appropriate for small/low-consequence repositories.

### Level 1 — Root-aware

Add `AGENTS.md`, pin the engineering-standards version/SHA, and identify exact repository verification/authority boundaries.

### Level 2 — Semantic Work Mode

Add a project RDF profile:

```text
project profile prof:isProfileOf engineering-standards
```

Use root `es:WorkOrder`, standing, authority, receipt, and projection semantics rather than redefining them.

### Level 3 — Manufactured

Wire framework/ggen generators and machine verifiers so derivable docs/issues/code/config are projections of canonical source.

### Level 4 — Closed-loop

Consequential work is authority-brokered, receipted, replayable, emits object-centric process evidence, and promotes recurring learning into reusable machinery.

## Required project declarations

Record:
- engineering-standards exact identity;
- project semantic profile location;
- canonical project source surfaces;
- generator identities;
- generated artifact paths;
- handwritten residue and reason;
- authority policy/broker;
- repository-native courts;
- process-evidence sink/projection;
- standing/replay policy.

Templates under `templates/` are bootstrap material for these declarations.

Adopted `.claude/` templates ship a deterministic pre-tool-use refusal guard for DO-shaped commands (typed `REFUSED:*` codes: `EXTERNAL_GIT_PUSH_REQUIRES_AUTHORITY` for `git push`, `MERGE_REQUIRES_AUTHORITY` for `git merge`, `PR_MERGE_REQUIRES_AUTHORITY` for `gh pr merge`, `CLUSTER_DO_REQUIRES_AUTHORITY` for `kubectl apply|delete`, `INFRASTRUCTURE_DO_REQUIRES_AUTHORITY` for `terraform apply`) and `GENERATED_PROJECTION_EDIT` for Write/Edit into generated projection paths, plus a post-tool-use `CONSTRUCTED_NOT_VERIFIED` reminder — a passing hook grants no authority.

`scripts/render-repository-adoption.py` emits `standing: "UNKNOWN"` in freshly rendered adoption manifests; local evidence upgrades it (`UNKNOWN` != `ALIVE` is ecosystem law).

## Do not fork shared semantics

Do not create project-local equivalents for:
- WorkOrder;
- evidence standing;
- authority levels;
- receipt/replay identity;
- generated-artifact sovereignty;
- DfCM stages.

Project profiles should add domain-specific residue only.

## Upgrade procedure

When adopting a newer root revision:

1. resolve old/new exact root identities;
2. diff root ontology/shapes/contracts;
3. identify project mappings/projections affected;
4. run project admission and falsifier courts;
5. regenerate projections;
6. run repository-native verification;
7. record new root identity and receipt.

A version bump alone does not transfer standing.

## Downstream-to-root learning

If a project discovers a reusable engineering law:
- preserve exact evidence;
- prove it is not project-specific;
- search prior art/public standards;
- propose root ontology/schema/verifier change;
- qualify it in this repository;
- update the downstream profile to consume it;
- delete redundant local doctrine.

The target is one learned law, one root representation, many projections.
