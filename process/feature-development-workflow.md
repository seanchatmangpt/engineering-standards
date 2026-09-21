# Feature Development Workflow

*Spec-driven agile development for feature work*

## Overview

This workflow defines **feature work driven by product and business intent** under the root [Semantic Engineering Protocol](./semantic-engineering-protocol.md).

The canonical Semantic Work Mode sequence is:

```text
INTENT -> OBSERVE -> ADMIT -> WorkOrder -> CLOSURE
       -> SELECT -> CONSTRUCT -> AUTHORITY -> DO
       -> RECEIPT -> REPLAY -> STANDING -> REUSE
```

Documentation Mode may use the lighter **Intent → Spec → Plan → Execute → Validate** projection described by the phases below.

**For engineering-driven work** (bugs, tech debt, infrastructure, security), see [Technical Work Workflow](./technical-work-workflow.md).

### Workflow Diagram

```text
flowchart LR
    A[Phase 1:<br/>Product Concept] --> B[Phase 2:<br/>Requirements & UI]
    B --> C[Phase 3:<br/>Planning &<br/>Sequencing]
    C --> D[Phase 4:<br/>Technical Design]
    D --> E[Phase 5:<br/>Implementation]
    E --> F[Phase 6:<br/>Validation]
    F -.->|Iterate| B

    style A fill:#e1f5ff
    style B fill:#e1f5ff
    style C fill:#fff4e1
    style D fill:#ffe1f5
    style E fill:#e1ffe1
    style F fill:#f5e1ff
```

## Guiding Principles

1. **Admission before consequence** — clarify intent, exact subject, constraints, evidence, and falsifiers before DO.
2. **One canonical work identity** — conserve the WorkOrder through plans, branches, SA2A messages, construction, receipts, and replay.
3. **Formal machinery for known classes** — use planners/solvers/generators/verifiers instead of repeatedly reasoning over solved structure.
4. **Small coherent consequences** — scope work by semantic consequence and independently verifiable boundary, not arbitrary line count.
5. **Continuous evidence** — validate the exact claimed boundary and bind receipts to exact identities.
6. **Document decisions as projections** — preserve rationale without creating a second authority surface.
7. **Operationalize learning** — every recurring correct judgment should become reusable machinery.

---

## Phase 1: Product Concept

**Goal**: Articulate the problem and opportunity

**Process**: Identify the problem, define target users, articulate value proposition, consider constraints

**Output**: `docs/product/concepts/feature-name.md`

**Time**: Hours to days

> **When compound-engineering is in use**: Phase 0 (discovery) is realized by `ce-brainstorm`, which produces a requirements-only unified plan under `docs/plans/`. That artifact IS the Phase 0 / discovery output for CE-using projects, and Phase 1 (Product Concept) is seeded from it rather than starting cold. Legacy `docs/brainstorms/*-requirements.md` files remain valid input to `ce-plan` but are no longer written. See [`process/compound-engineering-integration.md`](./compound-engineering-integration.md).

**Example**:
```markdown
# Feature Concept: User Notification System

## Problem
Users miss important account activities because we only show updates
when they log in. Critical events go unnoticed for days.

## Opportunity
Real-time notifications via email, SMS, and mobile push to keep users
informed of important account activities.

## Value
Increase user engagement and reduce security incidents by notifying
users of suspicious activity immediately.

## Constraints
- Must respect user notification preferences
- High signal-to-noise ratio required to avoid notification fatigue
```

---

## Phase 2: Product Requirements & UI Design

**Goal**: Define what to build and how users interact with it

**Process**:
1. Write product spec: intent, functional/non-functional requirements, success criteria
2. Design UI/UX: user flows, wireframes (HTML mockups preferred), interaction patterns
3. Define acceptance criteria: behaviors, edge cases, performance targets

**Output**: `docs/product/features/feature-name.md` with wireframes

**Time**: Days to a week

**Checkpoint**: Review spec with stakeholders before proceeding

**Example**:
```markdown
# Feature Spec: User Notification System

## Intent
Deliver timely notifications to users about important account activities.

## Functional Requirements
- FR1: Support email, SMS, and mobile push notification channels
- FR2: Users configure notification preferences per event type
- FR3: Notifications include event details, timestamp, and action links
- FR4: Users can snooze or disable specific notification types

## Non-Functional Requirements
- NFR1: Notification delivery latency <30 seconds from event
- NFR2: 99.9% delivery success rate for high-priority notifications
- NFR3: Support 1M+ active users with notification preferences

## UI Design
[HTML mockup: Notification preferences screen]
[HTML mockup: Notification message templates]

## Success Criteria
- 70% of users enable at least one notification channel
- <2% unsubscribe rate from notification channels
- 40% click-through rate on notification action links
```

---

## Phase 3: Project Planning & Sequencing

**Goal**: Construct an admissible dependency/constraint graph and expose lawful parallelism.

**Semantic Work Mode process**:
1. Identify WorkOrders/checkpoints and exact dependency edges.
2. Route known planning classes to HDDL/HTN, PDDL/FOND, SAT/SMT/CP, or another formal solver.
3. Preserve unresolved alternatives until evidence justifies elimination.
4. Bind each unit to acceptance, falsifier, court, evidence, and authority ceiling.
5. Identify critical path, parallel frontier, resource constraints, and blockers.

**Documentation Mode / human coordination projection**:
- break work into tasks;
- optionally estimate with Fibonacci story points;
- sequence tasks and identify risks.

Story points are planning metadata, never semantic standing or execution evidence.

**Output**: `docs/planning/feature-name-implementation.md`

**Time**: Hours to days

**For detailed guidance on estimation, task breakdown, and risk management, see [Project Planning Standards](./project-planning-standards.md).**

**Example**:
```markdown
# Implementation Plan: User Notification System

Total: 30 story points

## Task Breakdown
- Define notification data schema (2 pts)
- Implement email notification channel (3 pts)
- Implement SMS notification channel (3 pts)
- Implement push notification channel (5 pts)
- Create notification routing service (5 pts)
- Build notification preferences API (3 pts)
- Implement preferences management UI (8 pts)
- End-to-end testing and validation (3 pts)

## Dependencies
- All notification channels depend on schema
- Routing service depends on channels
- UI depends on preferences API
- E2E testing depends on all components

## Risks
- SMS costs may exceed budget → implement rate limiting
- Push notification registration complexity → start with email/SMS MVP
- Notification fatigue if too noisy → conservative defaults
```

---

## Phase 4: Technical Design & Architecture

**Goal**: Specify how to implement the solution

**Process**:
1. Design system: components, data models, API contracts, data flow
2. Consider alternatives: what else was considered, why this approach, tradeoffs
3. Document key decisions: ADRs for significant technical choices
4. Define interfaces: API schemas (`.proto`, OpenAPI), service contracts

**Output**:
- `docs/engineering/designs/feature-name.md`
- `docs/engineering/adr/NNNN-decision-name.md` (when applicable)
- API schemas

**Time**: Days to a week

**Checkpoint**: Review design with technical team, validate against product spec

**Example**:
```markdown
# Technical Design: User Notification System

## Components
1. Event Processor Service - consume application events, trigger notifications
2. Notification Router Service - route to channels based on user preferences
3. Notification Preferences API - REST service for user preference CRUD
4. Channel Handlers - email, SMS, push notification implementations

## Data Models
[Schema definitions for NotificationPreference, NotificationEvent, DeliveryReceipt]

## Data Flow
App Events → Event Processor → Notification Router → Channel Handlers → External Services (SendGrid, Twilio, FCM)

## Key Decisions
- Use message queue vs direct calls (ADR-001): enables retry, handles bursts
- Separate routing from channel delivery: independent scaling, easier to add channels

## Testing Strategy
- Unit: preference matching logic with various configurations
- Integration: end-to-end notification flow with mock external services
- Load: 10k notifications/min sustained throughput
```

---

## Phase 5: Implementation

**Goal**: Manufacture the admitted consequence.

**Process**:
1. Work from the canonical WorkOrder/contract graph; specs and plans are projections.
2. Reuse framework-native generators and admitted ggen-marketplace capital before handwriting repeatable surfaces.
3. Keep SELECT, CONSTRUCT, and DO distinct.
4. Route consequence through explicit authority; a plan, proof, agent, or PR is not authority.
5. Emit durable execution/verification receipts bound to exact source and subject identities.
6. Review semantic scope, falsifiers, tests, and projection freshness.

**Artifacts**: Working code, tests, updated docs (if needed)

**Time**: Per implementation plan story point estimates

---

## Phase 6: Validation, Replay & Learning

**Goal**: Establish bounded standing for the exact subject and reduce future reasoning cost.

**Process**:
1. Run the narrowest high-information court, then expand through unit/integration/e2e/chaos/stress/benchmark as required.
2. Test acceptance criteria and explicit falsifiers.
3. Observe real consequence at the claimed boundary; inspection is not execution.
4. Seal receipts and replay the claimed state from admitted inputs + receipts.
5. Promote standing only for the exact subject supported by evidence.
6. Turn newly solved recurring judgment into ontology, schema, generator, planner, policy, verifier, fixture, or process control.

**Artifacts**: evidence receipts, replay result, bounded standing, process/OCEL evidence where applicable, updated root/project semantics, and regenerated projections.

---

## Workflow Variations

### Small Features
For very small features (1-2 points), a detailed PR description may suffice:
- **What**: Brief feature description
- **Why**: User/business value
- **How**: Implementation approach (if non-obvious)
- **Testing**: How verified

Use judgment - if the feature needs stakeholder review or has UI implications, write a lightweight spec.

### Experiments or Spikes
For exploratory technical work, write a lightweight experiment brief in `docs/experiments/`:
- **Question**: What are we trying to learn?
- **Approach**: How will we explore this?
- **Success**: What outcome answers the question?
- **Timebox**: How long before deciding?

Document findings afterward to inform future decisions.

### Non-Feature Work
For bugs, tech debt, infrastructure, and security work, see [Technical Work Workflow](./technical-work-workflow.md).

---

## Anti-Patterns

- **Big upfront design** - Don't write exhaustive specs for uncertain features
- **Skipping specs entirely** - "Just coding" leads to rework and misalignment
- **Stale specs** - Update specs when implementation diverges, or remove them
- **Process for process** - If a phase adds no value, skip it (but be intentional)

---

## Integration with AI Development

This workflow works well with AI-assisted development:
- Specs provide context for AI agents
- Small scopes reduce AI errors
- Validation catches AI-generated bugs
- Iteration is cheaper with AI

When using AI coding tools:
- Provide product spec and technical design as context
- Generate code in small, testable increments
- Always review and test AI-generated code
- Update specs when AI reveals better approaches
