# Project Root Adoption Templates

These files help a repository consume **engineering-standards as its semantic root**. They are projections/bootstrap material, not an independent standards source.

## Minimal adoption

Copy/adapt:

- `AGENTS.md` — cross-tool root constitution.
- `CLAUDE.md` — Claude-specific projection of the same root.
- `.claude/` — optional six-layer interaction baselines.
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
