# AI Interaction Architecture

The six-layer model organizes AI tooling by **context cost and invocation pattern**. It is a downstream interaction profile of the repository's [Semantic Engineering Protocol](../../process/semantic-engineering-protocol.md), not the engineering semantic root.

Architectural history: [ADR-0001](../../docs/engineering/adr/0001-six-layer-ai-architecture.md).  
Root decision: [ADR-0002](../../docs/engineering/adr/0002-semantic-engineering-protocol.md).  
CE realization: [Compound Engineering Integration](../../process/compound-engineering-integration.md).

## Dependency direction

```text
root semantic graph / WorkOrder / authority / evidence
                    |
                    v
        AI interaction architecture
   +--------+--------+--------+--------+
   rules   skills  personas references
                     |
                  compound
                     |
                    hooks
```

A model, skill, persona, plan, review, or hook may observe, select, construct, validate, or request consequence according to its admitted capability. None acquires authority or standing by being in an AI layer.

## Six context-cost layers

| # | Layer | Function | Root relationship |
|---|---|---|---|
| 1 | Rules | Persistent compact context | pointers/guardrails to admitted root law |
| 2 | Workflow Skills | On-demand orchestration | transport/construct candidate workflows |
| 3 | Persona Agents | Focused perspectives | candidate observations, never authority |
| 4 | References | Progressive context | evidence/context inputs |
| 5 | Compound / Learnings | Captured outcomes | candidates for formalization into reusable machinery |
| 6 | Hooks | Deterministic local enforcement | guards/courts; never ambient DO authority |

### Layer 1 — Rules

Load small, durable pointers every session. A rule should point to canonical law rather than duplicate it. Project-root `AGENTS.md` is the preferred cross-tool constitution.

### Layer 2 — Workflow Skills

Load workflows on demand. Skills may discover, plan, construct, review, or prepare an authority request. A workflow definition is not a run and a successful run is not standing without evidence for the claimed subject.

### Layer 3 — Persona Agents

Produce specialized observations. Multiple personas improve search diversity but do not manufacture consensus authority.

### Layer 4 — References

Load deeper evidence only when the workflow needs it. References are observations until admitted at the relevant subject boundary.

### Layer 5 — Compound / Learnings

Capture what was learned, then **retire repeated reasoning**. Durable success is promotion into ontology, type, template, generator, planner, policy, verifier, fixture, or process control where practical. A prose solution that must be re-reasoned every time is intermediate capital, not the terminal form.

### Layer 6 — Hooks

Use deterministic hooks for mechanical invariants. Hooks can block/refuse local operations under declared policy; they do not independently confer external authority.

## Compound Engineering

Compound Engineering is one realization of Layers 2–5. The [integration standard](../../process/compound-engineering-integration.md) owns CE-specific inventory, paths, and version drift.

In Semantic Work Mode:
- CE plans project root WorkOrders;
- CE reviews are candidate evidence;
- CE work constructs candidates;
- merge/deploy/external mutation remains behind the project authority boundary;
- CE compound output should feed the root learning loop rather than become a parallel doctrine.

## Context economy

Context economy remains useful, but it is subordinate to semantic economy.

The stronger target is:

```text
known recurring class
  -> formalize
  -> deterministic machinery
  -> less model context and less model reasoning next time
```

The best context optimization is removing the need for model reasoning altogether when a class has become known.

## Baselines in this repository

- Rules: [`rules/`](./rules/)
- Skills: [`templates/.claude/skills/`](../../templates/.claude/skills/)
- Personas: [`templates/.claude/agents/`](../../templates/.claude/agents/)
- Hooks: [`templates/.claude/hooks/`](../../templates/.claude/hooks/)
- Root adoption: [`templates/AGENTS.md`](../../templates/AGENTS.md)

## Verification

AI review and hook success are bounded evidence. They do not replace repository-native courts, exact-head execution evidence, receipts, or replay.

When the work class is known, prefer non-AI verification machinery. When a new failure boundary is learned, encode it so subsequent runs do not need to rediscover it.
