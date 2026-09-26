# Project Root Adoption Templates

These files help a repository consume **engineering-standards as its semantic root**. They are projections/bootstrap material, not an independent standards source.

## Minimal adoption

Copy/adapt:

- `AGENTS.md` — cross-tool root constitution.
- `CLAUDE.md` — Claude-specific projection of the same root.
- `.claude/` — optional six-layer interaction baselines. The shipped hooks are a deterministic refusal guard, not an authority broker: a pre-tool-use hook emits typed `REFUSED:*` refusals for DO-shaped commands (`EXTERNAL_GIT_PUSH_REQUIRES_AUTHORITY` for `git push`, `MERGE_REQUIRES_AUTHORITY` for `git merge`, `PR_MERGE_REQUIRES_AUTHORITY` for `gh pr merge`, `CLUSTER_DO_REQUIRES_AUTHORITY` for `kubectl apply|delete`, `INFRASTRUCTURE_DO_REQUIRES_AUTHORITY` for `terraform apply`) and `GENERATED_PROJECTION_EDIT` for Write/Edit into generated projection paths (`.generated`/`generated`/`dist`/`build` path segments); a post-tool-use hook emits a `CONSTRUCTED_NOT_VERIFIED` reminder; `settings.json` replaces the broad `Bash(git:*)` allow with read-only git subcommands and denies push/merge/tag. A passing hook grants no authority.
- `semantic/project-profile.ttl` — project profile stub for Semantic Work Mode.

## Two modes

### Semantic Work Mode — ecosystem default

The project semantic graph and WorkOrders are canonical. Documentation, issues, plans, agent messages, and generated code are projections/candidates.

Adoption sequence:

```text
pin engineering-standards identity
-> define project profile
-> bind repository/exact base
-> declare authority policy and courts
-> adopt WorkOrder transport/projection
-> wire generator/verifier
-> manufacture docs/issues/code where derivable
-> receipt/replay
```

### Documentation Mode

Small projects may adopt the process/code standards without a semantic graph. Maintained specifications/issues may serve as the practical work record until the cost justifies promotion.

## Generator law

Templates should be replaced by framework-native/ggen generation once the transformation is stable. A copied template is bootstrap residue, not the desired terminal state.

Current reusable ggen-marketplace prior art includes semantic documentation, semantic projection, semantic manufacture epoch, SHACL projection, GitHub cloud doctrine, and pack protocol packs.

## Generated vs handwritten

Every adopting project should identify:
- canonical semantic/source inputs;
- generator/tool identity;
- generated projections;
- irreducible handwritten residue;
- verifier/court identity.

Do not hand-edit generated output.
