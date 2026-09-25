# RFC-0005: Autonomous Loop Qualification

**Status:** NORMATIVE — admission contract for autonomous-execution episodes; applied at
birth as the qualification contract of episode `ALOOP-ZCODE-DOGFOOD-001` (bootstrap
episode, classified ASSISTED — see §12)
**Release:** v26.9.25
**Role:** normative definition of autonomous episodes, autonomy epochs, recurrence,
typed terminality, and the machine-addressable requirements registry + crown that admit
or refuse an AUTONOMOUS_LOOP standing claim
**Authority:** NONE
**Consequence:** documentation / admission contract only; enforcement is the executable
crown `ALOOP-CROWN-001` (consumer: `seanchatmangpt/chatman-ecosystem`
`scripts/aloop_crown.py` + `tests/test_aloop_crown.py`)
**Implementation standing:** PARTIAL_ALIVE — crown implemented and executed against the
live multi-lane corpus of `ALOOP-ZCODE-DOGFOOD-001` in this episode; multi-episode
recurrence corpus not yet witnessed (§10)
**Supersedes:** none. No prior normative artifact in this repository or the operator's
repos defines "autonomous episode" or "autonomy epoch"; searched `docs/`, `process/`,
`rfc/*` on 2026-09-25. Companion (not superseded): RFC-0001 BRCE protocol (zero
unreceipted actuation is reused here as an axiom, not restated as law).

## 1. Purpose

"Autonomous" is the most over-claimed word in agent engineering and the least falsified.
A scheduled cron job, a workflow with no human keystrokes, and a receipt-bearing loop are
all routinely called autonomous. This RFC defines autonomous loop qualification so that
the claim is a *refusable standing* derived from evidence, never a description of intent.
An autonomy claim that cannot be refused is not a claim; it is decoration.

The RFC is dual-surface: this document is the human-normative form; the machine-addressable
form is the requirements registry
`0005-autonomous-loop-requirements.json` (same directory), in which every normative
requirement carries a numbered falsifier and an executable check. A requirement that
cannot carry a falsifier is prose and is marked UNSUPPORTED (falsifier law).

## 2. Definitions

### 2.1 Episode

An **episode** `E` is a bounded execution history with one objective, one authority
envelope, one OCEL log, and exactly one `episode.start` event. Everything an episode's
workers do between `episode.start` and an `episode.terminal` event is in scope for the
episode's standing. An episode is identified by its id (e.g. `ALOOP-ZCODE-DOGFOOD-001`),
never by a conversation, a session, or a directory.

### 2.2 Autonomy epoch

The **autonomy epoch** is the phase boundary at `episode.start`.

- **Before** `episode.start`: humans (or any external authority) may set the objective,
  policies, authority envelope, benchmark/stress/soak parameters, worker roster, and
  provider roster. These inputs are lawful and do not taint autonomy; they are recorded
  as pre-epoch causal edges with qualifier `phase="pre-epoch"`.
- **After** `episode.start`: any `Human -> NextAction` edge — an instruction, hint,
  course-correction, lane re-enumeration, manual retry order, or acceptance edit that
  influenced the episode's next action — invalidates full autonomy for the affected
  segment and MUST be recorded as a **human causal edge** in the episode's OCEL log
  (event class `observe` or `replan` with `originAuthority="human"`). Unrecorded human
  causality is fabrication of standing (§4, L5).

### 2.3 Human causal edge

A **human causal edge** is an OCEL edge whose origin authority is a human and whose
consequence is the selection, modification, or authorization of the episode's next action.
It is typed by phase: `pre-epoch` (lawful, does not taint), `post-epoch-execution`
(taints the segment; the segment is automation, not autonomy). A human *observing*
without influencing the next action is not a causal edge. A human *reading a report and
deciding what happens next* is.

### 2.4 Closed loop

An episode segment is a **closed loop** iff its next work is derived inside the loop:
`Receipt[n] -> Reobserve[n+1] -> Frontier[n+1] -> WorkOrder[n+1]`, with all four events
emitted by non-human workers and bound into the OCEL log. A loop whose next WorkOrder
came from a human prompt is, for that segment, **automation, not autonomy** (§4, L1).

### 2.5 Recurrence

**Recurrence** is demonstrated when the closed-loop transition of §2.4 is witnessed at
least twice in sequence (`n` and `n+1`) within the episode, each step carrying its own
receipt, reobservation, frontier delta, and issued WorkOrder. One iteration is an
execution, not a loop. Recurrence is the minimum evidence that the loop closes itself
rather than merely having closed once.

### 2.6 Provider independence

An episode has **provider independence** iff its recurrence, acceptance, receipts, and
replay bindings carry no provider identity — i.e. the WorkOrder identity, authority
reference, planner output, acceptance criteria, receipt schema, and replay binding are
formulated so that any qualified provider could execute them. Operationally: no provider
token appears in any WorkOrder id, acceptance predicate, or receipt schema field, and the
episode executed (or admitted replacement along) at least one `provider.replace` edge
with consequences preserved.

### 2.7 Worker independence

An episode has **worker independence** iff no single worker identity is load-bearing:
worker runs are interchangeable lanes whose evidence binds to the *subject* (repo, SHA,
paths), never to the worker's name; a crashed worker's WorkOrder is re-issuable to
another worker without semantic change. Worker independence is measured per WorkOrder:
`reissue(worker_a -> worker_b)` preserves identity, authority, acceptance, and receipt
schema.

### 2.8 Typed terminality

An episode terminates only in a typed terminal state, never by silence:
`goal.satisfied` (with standing AUTONOMOUS or ASSISTED as derived), `goal.blocked`
(with typed blockers), or refusal. The terminal event must carry the final standing,
the receipt chain, and the falsifier results. An episode with no `episode.terminal`
event is UNKNOWN, regardless of how much work it produced.

### 2.9 Self-recovery

**Self-recovery** is witnessed when the loop transitions through
`execution.crash|failure.detect -> replan|provider.replace|worker.reissue -> observed
success on the same WorkOrder identity` with zero human causal edges in the recovery
path. The recovery must be receipted like any other actuation. A crash followed by a
human typing "try again" is assisted remediation.

### 2.10 OCEL evidence

The episode's OCEL 2.0 log is the sole admissible evidence surface for autonomy claims:
object types (Episode, Objective, Requirement, WorkOrder, Authority, Repository, Subject,
Provider, Worker, WorkerRun, Plan, Capability, Candidate, Consequence, Evidence, Receipt,
Failure, Benchmark, Release) and event classes (`episode.start` … `episode.terminal`)
with qualifiers (`subject`, `originAuthority`, `provider`, `worker`, `input`, `output`,
`evidence`, `consequence`, `receipt`, `parentEpisode`, `predecessor`). Claims not bound
to OCEL events are O (raw claims), not O* (admissible evidence).

### 2.11 Benchmark / stress / soak standing

- **Benchmark standing:** the episode executed its declared benchmark on the admitted
  subject with receipted outcomes (event class `benchmark.run`).
- **Stress standing:** the episode survived its declared stress envelope (concurrency,
  failure injection, provider loss) with typed outcomes for every injected failure.
- **Soak standing:** the loop ran for its declared soak window with `dW/dt <= 0`
  (unmerged/refused-candidate backlog not growing) and no standing regression.
Each standing is independent and typed `PASS|FAIL|NOT_RUN`. NOT_RUN is an honest
outcome and fails any crown term that requires it; it is never assumed to be PASS.

### 2.12 Historical evidence vs current conformance

Prior receipts are **historical evidence**; they establish what was true of an exact
subject at an exact time. They never establish **current conformance**: the loop
standing of episode `E_t` is derived from `E_t`'s own OCEL log and receipts. Standing
is a cache with a validity scope (subject SHA + path); any change to the subject
invalidates it and re-enters the frontier. `Receipt[t]` is an input to
`Reobserve[t+1]`, never a substitute for it (§4, L4).

## 3. Machine-addressable requirements

Every normative requirement of this RFC is numbered in
`0005-autonomous-loop-requirements.json` with the tuple
`{id, requirement, falsifier, executable_check}`. The falsifier is the observation that
would overturn a claim of conformance; the executable check is a command or predicate a
machine can run against the episode's evidence surface. Requirements are grouped by
crown term (§6). The registry is the qualification surface; this section is its
narration.

## 4. Formal laws (refusable invariants)

Each law is stated with its refutation condition. A law whose refutation cannot be
witnessed is UNSUPPORTED and must not gate admission.

- **L1 — Automation != Autonomy.** A segment with zero human keystrokes but a
  human-authored next WorkOrder is automation. *Refuted by:* any OCEL edge
  `originAuthority=human -> WorkOrder[n+1]` inside a segment claimed autonomous.
- **L2 — WorkerIndependence != ProviderIndependence.** Re-issuing a WorkOrder across
  workers of the same provider proves nothing about provider lock-in. *Refuted by:* an
  episode claiming provider independence whose receipts all carry one provider and no
  `provider.replace` capability was admitted or exercised.
- **L3 — ScheduledExecution != ClosedLoop.** A cron/scheduler trigger is an external
  clock, not a frontier derivation. *Refuted by:* recurrence chain whose
  `WorkOrder[n+1]` predecessor is the scheduler event rather than `Frontier[n+1]`.
- **L4 — Receipt != Verification.** A receipt records that an actuation happened under
  authority with a replay binding; it does not certify current conformance of the
  subject. *Refuted by:* a standing derived from receipts alone where the required
  verifier was not executed against the exact subject (inspection != execution).
- **L5 — NoHumanInput != Autonomous unless recurrence demonstrated.** Silence is not
  autonomy. *Refuted by:* an episode with zero recorded human causal edges, zero
  demonstrated recurrence, claiming AUTONOMOUS.
- **L6 — ASSISTED is never promoted.** Within an episode, standing moves only downward
  or stays (monotone non-increasing under taint). A new episode may classify differently
  from its own fresh evidence. *Refuted by:* any `ASSISTED -> AUTONOMOUS` transition on
  the same episode id without a new `episode.start`.
- **L7 — Zero unreceipted actuation.** Every actuation in the episode carries authority
  + receipt + replay binding (RFC-0001 axiom, reused). *Refuted by:* any command with
  external consequence lacking a receipt binding in the OCEL log.

## 5. The autonomy claim

```text
Autonomous(E) =
    ClosedLoop(E)
  ^ ZeroHumanCausality(E, post-epoch)
  ^ ZeroUnreceiptedActuation(E)
  ^ SemanticIntegrity(E)        // claims bound to OCEL subjects; no fabricated evidence
  ^ ProviderIndependence(E)
  ^ SelfRecovery(E)
  ^ Recurrence(E)
```

The derived outcome is exactly one of:

- `AUTONOMOUS` — all conjuncts witnessed in the episode's OCEL log;
- `ASSISTED` — loop ran with at least one post-epoch human causal edge, or any conjunct
  other than causality failed while work proceeded under human steering;
- `BLOCKED_AUTHORITY` — a required transition was refused for missing authority;
- `BLOCKED_INFORMATION` — the loop could not derive its next action for lack of evidence;
- `FAILED` — the episode terminated without goal satisfaction and without a lawful block.

Taint rule: one post-epoch human causal edge taints the segment containing it; if the
tainted segment includes the recurrence chain or the terminal derivation, the episode
outcome is ASSISTED regardless of all other conjuncts (L5, L6).

## 6. Crown contract: ALOOP-CROWN-001

The crown is an executable, deterministic, fail-closed consumer that derives the loop
standing from lane evidence. Implementation (this episode):
`seanchatmangpt/chatman-ecosystem scripts/aloop_crown.py`, tests
`tests/test_aloop_crown.py`.

**Terms (all ten must pass for `AUTONOMOUS_LOOP_ALIVE`):**

| term | admits |
|---|---|
| LOOP | at least one lane demonstrates the §2.4 recurrence chain with autonomy-class segments |
| CAUSALITY | no record claiming AUTONOMOUS carries a post-epoch human causal edge; ASSISTED lanes never classified AUTONOMOUS |
| AUTHORITY | every record declares origin authority; zero authority violations; blocks are honestly typed BLOCKED_AUTHORITY |
| RECEIPTS | every actuation-bearing lane carries receipts with provider execution id + consequence |
| RECOVERY | at least one witnessed self-recovery (crash -> replan/reissue -> success, zero human edges) |
| PROVIDERS | provider recorded on every receipt; work-order ids provider-neutral; >= 2 distinct providers witnessed or a provider.replace capability admitted |
| OCEL | every record's ocel_summary carries the required object types and event classes with count > 0 |
| PROCESS | purpose branches, valid SHAs, start != final (or documented read-only objective), atomic commit lists |
| STRESS | at least one benchmark/stress/soak result PASS on the admitted subject |
| REPLAY | every receipt carries a replay binding naming its verifier |

**Non-self-certification (mandatory):** the crown consumes only `lane-*/record.json`
files authored by lanes; it never reads its own verdicts, never cites files it generated
as lane evidence, and refuses an output path inside the evidence root's lane
directories. A crown that certifies the loop with facts it manufactured itself is
self-attestation and is refused by construction.

**Fail-closed:** a missing or incomplete lane record fails every term that lane's
evidence would have supported. Missing evidence is never assumed present; silence is
typed, never interpreted as success.

## 7. Manifest schema (normative)

Each lane writes exactly one machine-readable record at
`~/.zcode/workspace/default/aloop-dogfood-001/lane-<N>/record.json`:

```json
{
  "schema_version": "1.0.0",
  "episode": "ALOOP-ZCODE-DOGFOOD-001",
  "lane": "lane-1",
  "author": "lane-1",
  "objective": "string",
  "standing": "AUTONOMOUS|ASSISTED|BLOCKED_AUTHORITY|BLOCKED_INFORMATION|FAILED|ALIVE|PARTIAL_ALIVE|BLOCKED|REFUSED|UNSUPPORTED|UNKNOWN",
  "repos": [{"repo": "name", "branch": "purpose-branch", "start_sha": "sha40",
             "final_sha": "sha40", "commits": ["sha40"]}],
  "commands": [{"cmd": "string", "exit": 0}],
  "tests": [{"cmd": "string", "exit": 0}],
  "falsifiers": [{"id": "Rxxx-F", "result": "PASS|FAIL|NOT_RUN"}],
  "receipts": [{"work_order_id": "provider-neutral-id", "provider": "name",
                "provider_execution_id": "string", "origin_authority": "string",
                "exit_status": "string", "replay_binding": "string",
                "consequence": "string"}],
  "provider_replace_admitted": false,
  "human_causal_edges": [{"ts": "iso8601", "phase": "pre-epoch|post-epoch-execution",
                          "description": "string"}],
  "recurrence": {"demonstrated": false, "chain": ["Receipt[n]", "Reobserve[n+1]",
                 "Frontier[n+1]", "WorkOrder[n+1]"], "iterations": 0},
  "recovery": [{"from": "execution.crash", "via": "replan|reissue|provider.replace",
                "to": "success", "human_edges": 0}],
  "stress": {"kind": "benchmark|stress|soak", "result": "PASS|FAIL|NOT_RUN"},
  "ocel_summary": {"object_types": ["Episode", "..."], "event_classes": ["episode.start", "..."],
                   "event_count": 0},
  "blockers": [{"type": "AUTHORITY_FAILURE|INFORMATION|...", "detail": "string"}],
  "authority": {"origin": "string", "ceiling": "string", "violations": []},
  "ts": "iso8601"
}
```

The crown validates this shape, refuses records failing it (`REFUSED[INVALID_RECORD]`),
and derives terms per §6.

## 8. Standing derivation

Loop standing = `AUTONOMOUS_LOOP_ALIVE` iff all ten crown terms pass on the corpus;
otherwise `AUTONOMOUS_LOOP_PARTIAL_ALIVE(missing:<terms>)` — a precise typed
alternative naming exactly which terms lacked admissible evidence. A corpus containing
a contradiction (an AUTONOMOUS claim over a tainted segment) yields
`AUTONOMOUS_LOOP_PARTIAL_ALIVE(missing:CAUSALITY)` plus the violation, never a silent
downgrade. The crown never emits an untyped verdict.

## 9. Provider neutrality

WorkOrder identity, authority reference, planner output, acceptance criteria, receipt
schema, and replay binding carry NO provider identity (tokens, endpoints, model names,
SDK names). Provider identity appears only in the typed `provider` field of execution
records and receipts. The crown enforces this mechanically: a WorkOrder id containing
its provider's name is refused (`REFUSED[PROVIDER_NEUTRALITY]`).

## 10. Falsifier suite and current implementation standing

The registry's executable checks run as: (a) the crown's unittest falsifier suite
(`tests/test_aloop_crown.py` — each test names the RFC law it guards, including the
admit path and the refusal paths); (b) live crown execution against the episode corpus.
Implementation standing is PARTIAL_ALIVE: admit/refuse paths witnessed in this episode;
multi-episode recurrence (Recurrence across `parentEpisode`/`predecessor` edges) is
UNSUPPORTED until a second episode derives its WorkOrders from this one's receipts.

## 11. Historical evidence vs current conformance (operational)

`Receipt[n]` feeds `Reobserve[n+1]`; it never skips it. Conformance of the loop at time
`t` requires the crown run at `t` against the corpus as it exists at `t`. A green crown
verdict from yesterday is historical evidence about yesterday's corpus.

## 12. Dogfood annex: classification of ALOOP-ZCODE-DOGFOOD-001

This RFC was manufactured inside episode `ALOOP-ZCODE-DOGFOOD-001`, a ten-lane
bootstrap fan-out. Honest self-classification per §5: **ASSISTED, at best.**

Grounds: (a) the launcher (external to the loop) enumerated the lanes, assigned
repo-sets, and prescribed the contract — pre-epoch authority, lawful, but it means the
frontier shape was human-derived; (b) no lane can demonstrate the §2.4 recurrence chain
from a prior episode's receipts (this is the first episode); (c) lane records carry
`human_causal_edges[].phase = "pre-epoch"` for the dispatch itself. Under L1 + L5, the
bootstrap is automation under human enumeration — a legitimate and useful corpus, and
exactly the corpus the crown must one day refuse to call autonomous. The episode's
value is that it manufactures the qualification machinery that future episodes will be
refused with until they genuinely pass it.
