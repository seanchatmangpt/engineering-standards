# AGENTS.md — Project Root Constitution

This project inherits the Engineering Standards semantic root.

## Read order

1. project `MANIFEST.json` / project profile if present;
2. project semantic graph and admission shapes;
3. engineering-standards `AGENTS.md` and root protocol;
4. task-specific local standards;
5. implementation/tests.

## Laws

```text
Received != Admitted
Ticket != Authority
Agent != Authority
Capability != Authority
Plan != Authority
Proof != Authority
SELECT != CONSTRUCT != DO
GeneratedArtifact != SemanticAuthority
Inspection != Execution
UNKNOWN != ALIVE
```

## Work

Bind non-trivial work to one exact subject and base identity. Preserve that identity through plan, branch, PR, transport, execution, receipt, replay, and standing.

## DfCM

守 preserve -> 柵 fence -> 算 calculate -> 除 exclude -> 偽 falsify -> 延 extend -> 実 operationalize.

Reuse -> compose -> extend -> invent. Prefer public standards and specialized machinery.

## Consequence

No ambient DO authority. Use the project's explicit authority broker/policy. Emit receipts and bind standing to exact evidence.

## Git

Exact base; coherent diff; verify; draft PR; exact-head CI; explicit merge authority. Never merge merely because a plan/review/check is green.

## Learning

If this project discovers a reusable engineering law, upstream it to engineering-standards, qualify it there, and then consume the new root profile instead of keeping a permanent local doctrine fork.
