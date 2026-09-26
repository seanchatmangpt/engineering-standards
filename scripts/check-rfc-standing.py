#!/usr/bin/env python3
"""Standing court for RFC front matter, the R25-007 status sweep, and the RFC-0003 witness.

Four structural courts run on every invocation, each over the real files of the
repository (or of ``--root``):

1. **R25-007 status sweep** — every swept document carries exactly one
   ``**Status:**`` header, before its first ``## `` section, whose token is
   ``FINAL`` or ``PROPOSED``; a ``FINAL`` document may not carry a self-declared
   draft footer ("in active development"), and a ``PROPOSED`` document must carry
   one plus the "owed under R25-007" obligation.
2. **RFC front matter** — ``Status`` is ``FINAL_SPEC``, ``Authority`` is ``NONE``
   (never a DO grant), and ``Implementation standing`` uses the standing
   vocabulary.
3. **RFC-0003 witness** — every ``xaas@<sha>`` reference is a full 40-hex SHA
   named in ``semantic/witness/rfc-0003-xaas.witness.json``; every 64-hex digest
   is a recorded digest; both recorded digests and all recorded subjects are
   cited; the zoela element stays ``NOT_CLAIMED`` in the header, section 6 and
   section 9.2; falsifier F-CS1 is present; the ledger line count matches.
4. **RFC-0005 registry** — every ``R0xx`` requirement has a non-empty
   ``requirement``, ``falsifier`` and ``executable_check`` field, unique ids,
   and a versioned registry envelope.

A court that never refuses carries no bits, so each run also applies a fixed
set of in-memory mutants (missing/duplicated/reordered headers, contradicted
drafts, a DO authority, a stale subject, a truncated or wrong digest, a
reclaimed zoela element, a deleted falsifier, a wrong ledger count) and fails
unless every mutant is refused.

``--witness-repo PATH`` additionally replays the witness against a real xaas
git repository: subjects exist, recorded blobs match, the vocabulary files are
absent at the ledger's evidence subject, the ledger's ``cs:boundSubject`` and
line count match, and the receipt's digests and subject match, with the receipt
committed out-of-subject (a descendant of its subject).

Authority NONE; ceiling SELECT. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]

SWEEP = (
    "ai/claude-code/rules/engineering-standards.md",
    "code/database-standards.md",
    "code/python-standards.md",
    "code/web-application-standards.md",
    "docs/engineering/root-architecture.md",
    "process/documentation-standards.md",
    "process/project-planning-standards.md",
    "process/standards-change-control.md",
)
SWEEP_TOKENS = {"FINAL", "PROPOSED"}
DRAFT_MARKER = "in active development"

RFC_FRONT = (
    "docs/engineering/rfc/0002-v26.9.24-semantic-release-closure.md",
    "docs/engineering/rfc/0003-semantic-case-study.md",
    "docs/engineering/rfc/0004-v26.9.25-self-closing-release.md",
)
STANDING_TOKENS = {"PARTIAL", "ALIVE", "OPEN", "NOT_CLAIMED", "UNKNOWN", "BLOCKED", "UNSUPPORTED"}

RFC0003 = "docs/engineering/rfc/0003-semantic-case-study.md"
WITNESS = "semantic/witness/rfc-0003-xaas.witness.json"
RFC0005_REGISTRY = "docs/engineering/rfc/0005-autonomous-loop-requirements.json"
RFC_DIR = "docs/engineering/rfc"
RFC0006_AMENDMENT = "docs/engineering/rfc/0006-v26.9.25-autonomic-closure-amendment.md"

STATUS_LINE = re.compile(r"^\*\*Status:\*\*\s+(\S+)")
FIELD_LINE = re.compile(r"^\*\*([A-Za-z][A-Za-z ]*):\*\*\s*(.*)$")
XAAS_REF = re.compile(r"xaas@([0-9A-Za-z]+)")
LEDGER_CLAIM = re.compile(r"(\d+)-line\s+WD\s+claims\s+ledger")
HEXISH = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{48,80}(?![0-9a-fA-F])")
RFC_ID_TITLE = re.compile(r"^#\s+(RFC-\d{4}):")


# --------------------------------------------------------------------------- helpers


def first_section_index(lines: list[str]) -> int:
    """Index of the first heading after the title; front matter ends there.

    Any ATX level counts: RFC-0004 carries an operator RFC verbatim under a
    second ``# `` title with its own ``**Status:**`` line, which is body, not
    front matter.
    """
    for i, line in enumerate(lines):
        if i > 0 and re.match(r"#{1,6} ", line):
            return i
    return len(lines)


def front_fields(text: str) -> dict[str, str]:
    """``**Key:** value`` fields before the first ``## `` section, continuations joined."""
    lines = text.split("\n")
    fields: dict[str, str] = {}
    key = None
    for line in lines[: first_section_index(lines)]:
        match = FIELD_LINE.match(line)
        if match:
            key = match.group(1)
            fields[key] = match.group(2).strip()
        elif key and line.strip():
            fields[key] += " " + line.strip()
        else:
            key = None
    return fields


def section(text: str, heading_prefix: str) -> str:
    """Body of the section whose heading starts with ``heading_prefix`` (## or ###)."""
    lines = text.split("\n")
    out: list[str] = []
    level = None
    for line in lines:
        if level is None:
            if line.startswith(heading_prefix):
                level = len(line) - len(line.lstrip("#"))
            continue
        hashes = len(line) - len(line.lstrip("#"))
        if line.startswith("#") and hashes <= level and line[hashes:hashes + 1] == " ":
            break
        out.append(line)
    return "\n".join(out)


# --------------------------------------------------------------------------- courts


def sweep_errors(rel: str, text: str) -> list[str]:
    lines = text.split("\n")
    cut = first_section_index(lines)
    status_at = [i for i, line in enumerate(lines) if line.startswith("**Status:**")]
    errors: list[str] = []
    if not status_at:
        return [f"{rel}: R25-007 status header missing"]
    if len(status_at) > 1:
        errors.append(f"{rel}: duplicate **Status:** header at lines {[i + 1 for i in status_at]}")
    first = status_at[0]
    if first > cut:
        errors.append(f"{rel}: **Status:** header at line {first + 1} is after the first section")
    token = STATUS_LINE.match(lines[first]).group(1) if STATUS_LINE.match(lines[first]) else ""
    if token not in SWEEP_TOKENS:
        errors.append(f"{rel}: status token {token!r} not in {sorted(SWEEP_TOKENS)}")
    value = []
    for line in lines[first:]:
        if not line.strip():
            break
        value.append(line)
    value_text = " ".join(value)
    body = "\n".join(lines[:first] + lines[first + len(value):])
    draft = DRAFT_MARKER in body.lower()
    if token == "FINAL":
        if draft:
            errors.append(f"{rel}: FINAL contradicts the document's own draft footer")
        if "R25-007" not in value_text:
            errors.append(f"{rel}: FINAL header does not cite its R25-007 disposition")
    if token == "PROPOSED":
        if not draft:
            errors.append(f"{rel}: PROPOSED claims a self-declared draft but no draft footer exists")
        if "owed under R25-007" not in value_text:
            errors.append(f"{rel}: PROPOSED header does not carry the R25-007 promotion obligation")
    return errors


def rfc_front_errors(rel: str, text: str) -> list[str]:
    fields = front_fields(text)
    errors: list[str] = []
    status = fields.get("Status", "").split()
    if not status or status[0] != "FINAL_SPEC":
        errors.append(f"{rel}: Status is not FINAL_SPEC ({fields.get('Status')!r})")
    authority = fields.get("Authority", "").split()
    if not authority or authority[0] != "NONE":
        errors.append(f"{rel}: Authority must be NONE, found {fields.get('Authority')!r}")
    standing = fields.get("Implementation standing")
    if standing is not None:
        token = standing.split()[0].rstrip(",;") if standing.split() else ""
        if token not in STANDING_TOKENS:
            errors.append(f"{rel}: Implementation standing token {token!r} not in vocabulary")
    return errors


def rfc0003_errors(text: str, witness: dict) -> list[str]:
    errors: list[str] = []
    subjects = witness["subjects"]
    known_shas = set(subjects.values())
    for sha in XAAS_REF.findall(text):
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            errors.append(f"RFC-0003: malformed subject xaas@{sha} (not a full 40-hex SHA)")
        elif sha not in known_shas:
            errors.append(f"RFC-0003: stale or unwitnessed subject xaas@{sha}")
    for name, sha in subjects.items():
        if f"xaas@{sha}" not in text:
            errors.append(f"RFC-0003: witnessed {name} xaas@{sha} is not cited")

    receipt = witness["receipt"]
    digests = {receipt["case_revision_digest"], receipt["receipt_sha256"]}
    for token in HEXISH.findall(text):
        if len(token) != 64:
            errors.append(f"RFC-0003: malformed digest {token[:12]}... ({len(token)} hex, need 64)")
        elif token not in digests:
            errors.append(f"RFC-0003: digest {token[:12]}... is not a witnessed digest")
    for digest in sorted(digests):
        if digest not in text:
            errors.append(f"RFC-0003: witnessed digest {digest[:12]}... is not cited")
    for needle in (receipt["path"], receipt["case_iri"], receipt["generator_identity_prefix"]):
        if needle not in text:
            errors.append(f"RFC-0003: receipt field {needle!r} is not cited")

    fields = front_fields(text)
    standing = fields.get("Implementation standing", "")
    if "zoela" in standing and "NOT_CLAIMED" not in standing:
        errors.append("RFC-0003: header re-claims the zoela element (NOT_CLAIMED missing)")
    zoe_bullet = [b for b in section(text, "## 6.").split("\n- ") if "ZOE" in b]
    if not zoe_bullet or "NOT_CLAIMED" not in zoe_bullet[0]:
        errors.append("RFC-0003: section 6 ZOE application lost its NOT_CLAIMED standing")
    if "NOT_CLAIMED" not in section(text, "### 9.2"):
        errors.append("RFC-0003: section 9.2 terminal disposition lost NOT_CLAIMED")

    falsifier = section(text, "### 9.3")
    if "F-CS1" not in falsifier or "MUST refuse" not in falsifier:
        errors.append("RFC-0003: anti-vacuity falsifier F-CS1 (MUST refuse) missing from 9.3")

    lines = witness["claims_ledger"]["lines"]
    claims = re.findall(LEDGER_CLAIM, text)
    if not claims:
        errors.append("RFC-0003: the claims-ledger line count is no longer cited")
    for claimed in claims:
        if int(claimed) != lines:
            errors.append(f"RFC-0003: ledger claimed {claimed} lines, witness records {lines}")
    return errors


def rfc0005_registry_errors(registry_text: str) -> list[str]:
    """RFC-0005 requirements registry: every R0xx carries a non-empty falsifier
    and executable check, unique ids, and the versioned registry envelope."""
    errors: list[str] = []
    try:
        registry = json.loads(registry_text)
    except json.JSONDecodeError as exc:
        return [f"RFC-0005: registry unreadable: {exc}"]
    for field in ("registry_id", "version", "requirements"):
        if not registry.get(field):
            errors.append(f"RFC-0005: registry {field} missing or empty")
    seen: set[str] = set()
    for req in registry.get("requirements", []):
        rid = req.get("id", "")
        if not re.fullmatch(r"R\d{3}", rid):
            errors.append(f"RFC-0005: requirement id {rid!r} is not R0xx")
        elif rid in seen:
            errors.append(f"RFC-0005: duplicate requirement id {rid}")
        seen.add(rid)
        for field in ("requirement", "falsifier", "executable_check"):
            if not str(req.get(field, "")).strip():
                errors.append(f"RFC-0005: {rid} {field} is empty or missing")
    return errors


def rfc_id_errors(texts: dict[str, str]) -> list[str]:
    """Cross-file RFC-id uniqueness: within the RFC kind, a declared
    ``# RFC-NNNN:`` title names exactly one document in ``docs/engineering/rfc/``.

    Historical defect (repaired 2026-09-26): RFC-0005 was double-booked by the
    autonomous-loop qualification and the v26.9.25 autonomic-closure amendment;
    the amendment was renumbered RFC-0006. A file whose first ``# `` title does
    not declare an RFC id (for example an embedded verbatim RFC or a working
    note) is not part of the id set.
    """
    declared: dict[str, list[str]] = {}
    prefix = f"{RFC_DIR}/"
    for rel in sorted(texts):
        if not rel.startswith(prefix) or not rel.endswith(".md"):
            continue
        for line in texts[rel].split("\n"):
            match = RFC_ID_TITLE.match(line)
            if match:
                declared.setdefault(match.group(1), []).append(rel)
                break
    return [f"RFC id collision: {rid} is declared by {', '.join(rels)}"
            for rid, rels in sorted(declared.items()) if len(rels) > 1]


def load(root: Path) -> tuple[dict[str, str], dict]:
    texts = {rel: (root / rel).read_text()
             for rel in set(SWEEP) | set(RFC_FRONT) | {RFC0005_REGISTRY}}
    texts.update({f"{RFC_DIR}/{path.name}": path.read_text()
                  for path in sorted((root / RFC_DIR).glob("*.md"))})
    witness = json.loads((root / WITNESS).read_text())
    return texts, witness


def structural_errors(texts: dict[str, str], witness: dict) -> list[str]:
    errors: list[str] = []
    for rel in SWEEP:
        errors += sweep_errors(rel, texts[rel])
    for rel in RFC_FRONT:
        errors += rfc_front_errors(rel, texts[rel])
    errors += rfc0003_errors(texts[RFC0003], witness)
    errors += rfc0005_registry_errors(texts[RFC0005_REGISTRY])
    errors += rfc_id_errors(texts)
    return errors


# --------------------------------------------------------------------------- mutants


def _swap(text: str, old: str, new: str, count: int = 1) -> str:
    if old not in text:
        raise AssertionError(f"mutant anchor not found: {old[:40]!r}")
    return text.replace(old, new, count)


def _move_status_after_first_section(text: str) -> str:
    lines = text.split("\n")
    i = next(k for k, line in enumerate(lines) if line.startswith("**Status:**"))
    block = [lines[i]]
    while i + len(block) < len(lines) and lines[i + len(block)].strip():
        block.append(lines[i + len(block)])
    rest = lines[:i] + lines[i + len(block):]
    cut = first_section_index(rest)
    return "\n".join(rest[: cut + 1] + [""] + block + rest[cut + 1:])


def _flip_last_hex(text: str, digest: str) -> str:
    flipped = digest[:-1] + ("0" if digest[-1] != "0" else "1")
    return _swap(text, digest, flipped, count=-1)


def mutants(witness: dict) -> list[tuple[str, str, callable]]:
    receipt = witness["receipt"]
    ledger = witness["subjects"]["ledger_evidence_subject"]
    vocab = witness["subjects"]["vocabulary_subject"]
    root_arch = "docs/engineering/root-architecture.md"
    python_std = "code/python-standards.md"
    return [
        ("RFC-0005 registry falsifier blanked", RFC0005_REGISTRY,
         lambda t: re.sub(r'"falsifier": "[^"]*"', '"falsifier": ""', t, count=1)),
        ("duplicate RFC id (historical RFC-0005 double-booking)", RFC0006_AMENDMENT,
         lambda t: _swap(t, "# RFC-0006: v26.9.25 Autonomic Closure Amendment",
                         "# RFC-0005: v26.9.25 Autonomic Closure Amendment")),
        ("missing status header", root_arch,
         lambda t: "\n".join(l for l in t.split("\n") if not l.startswith("**Status:**"))),
        ("duplicate status header (duplicate delivery)", root_arch,
         lambda t: _swap(t, "## Purpose", "**Status:** FINAL — in force (R25-007)\n\n## Purpose")),
        ("status header reordered after first section", root_arch, _move_status_after_first_section),
        ("FINAL on a self-declared draft", python_std,
         lambda t: _swap(t, "**Status:** PROPOSED", "**Status:** FINAL (R25-007)")),
        ("PROPOSED without a draft footer", python_std,
         lambda t: t.replace(DRAFT_MARKER, "in force")),
        ("PROPOSED without the promotion obligation", python_std,
         lambda t: _swap(t, "owed under R25-007", "pending")),
        ("malformed status token", root_arch,
         lambda t: _swap(t, "**Status:** FINAL", "**Status:** Final")),
        ("Authority DO (unauthorized action)", RFC0003,
         lambda t: _swap(t, "**Authority:** NONE", "**Authority:** DO")),
        ("unknown implementation-standing token", RFC0003,
         lambda t: _swap(t, "**Implementation standing:** PARTIAL", "**Implementation standing:** DONE")),
        ("stale subject SHA", RFC0003, lambda t: _swap(t, f"xaas@{vocab}", "xaas@" + "a" * 40)),
        ("truncated subject SHA", RFC0003, lambda t: _swap(t, f"xaas@{ledger}", f"xaas@{ledger[:12]}")),
        ("truncated digest", RFC0003,
         lambda t: _swap(t, receipt["case_revision_digest"], receipt["case_revision_digest"][:56])),
        ("wrong digest", RFC0003, lambda t: _flip_last_hex(t, receipt["receipt_sha256"])),
        ("zoela element re-claimed in header", RFC0003,
         lambda t: _swap(t, "case-study element is reclassified **NOT_CLAIMED**",
                         "case-study element is applied")),
        ("section 6 ZOE standing dropped", RFC0003,
         lambda t: _swap(t, "  Implementation standing for this RFC: `NOT_CLAIMED` (§9.2).\n", "")),
        ("anti-vacuity falsifier removed", RFC0003, lambda t: t.replace("F-CS1", "F-CS0")),
        ("ledger line count drift", RFC0003,
         lambda t: LEDGER_CLAIM.sub(
             lambda m: m.group(0).replace(m.group(1), str(int(m.group(1)) + 1)), t)),
    ]


def mutant_survivors(texts: dict[str, str], witness: dict) -> tuple[int, list[str]]:
    survivors = []
    cases = mutants(witness)
    for label, rel, mutate in cases:
        candidate = dict(texts)
        try:
            candidate[rel] = mutate(texts[rel])
        except AssertionError as exc:
            survivors.append(f"{label}: {exc}")
            continue
        if candidate[rel] == texts[rel]:
            survivors.append(f"{label}: mutant is a no-op")
        elif not structural_errors(candidate, witness):
            survivors.append(label)
    return len(cases), survivors


# --------------------------------------------------------------------------- witness replay


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def _blob(repo: Path, rev_path: str) -> str:
    """Blob id at ``rev:path``, or "" when absent.

    Plain ``git rev-parse`` echoes an unresolvable argument back on stdout, so
    an absent file would read as a (wrong) id rather than as absent.
    """
    result = _git(repo, "rev-parse", "--verify", "--quiet", rev_path)
    return result.stdout.strip() if result.returncode == 0 else ""


def witness_replay_errors(repo: Path, witness: dict) -> list[str]:
    errors: list[str] = []
    subjects = witness["subjects"]
    for name, sha in subjects.items():
        if _git(repo, "cat-file", "-e", f"{sha}^{{commit}}").returncode != 0:
            errors.append(f"replay: {name} {sha} is not a commit in {repo}")
    if errors:
        return errors
    vocab, ledger = subjects["vocabulary_subject"], subjects["ledger_evidence_subject"]
    for path, blob in witness["vocabulary_files"].items():
        got = _blob(repo, f"{vocab}:{path}")
        if got != blob:
            errors.append(f"replay: {path} at {vocab[:12]} is {got or 'absent'}, witness {blob}")
        absent = _git(repo, "cat-file", "-e", f"{ledger}:{path}").returncode != 0
        if witness["vocabulary_files_absent_at_ledger_evidence_subject"] and not absent:
            errors.append(f"replay: {path} unexpectedly present at ledger subject {ledger[:12]}")
    cl = witness["claims_ledger"]
    ledger_text = _git(repo, "show", f"{vocab}:{cl['path']}").stdout
    if len(ledger_text.splitlines()) != cl["lines"]:
        errors.append(f"replay: ledger has {len(ledger_text.splitlines())} lines, witness {cl['lines']}")
    if f'cs:boundSubject "{cl["bound_subject"]}"' not in ledger_text:
        errors.append(f"replay: ledger cs:boundSubject is not {cl['bound_subject']}")

    rc = witness["receipt"]
    commit = subjects["receipt_commit"]
    got_blob = _blob(repo, f"{commit}:{rc['path']}")
    if got_blob != rc["blob"]:
        errors.append(f"replay: receipt blob {got_blob or 'absent'} != witness {rc['blob']}")
    if _git(repo, "cat-file", "-e", f"{rc['subject_sha']}:{rc['path']}").returncode == 0:
        errors.append("replay: receipt is inside its own subject (must be out-of-subject)")
    if _git(repo, "merge-base", "--is-ancestor", rc["subject_sha"], commit).returncode != 0:
        errors.append("replay: receipt commit does not descend from the receipt subject")
    try:
        body = json.loads(_git(repo, "show", f"{commit}:{rc['path']}").stdout)
    except json.JSONDecodeError:
        return errors + ["replay: receipt is not JSON"]
    case = body.get("case", {})
    checks = {
        "case_iri": (case.get("case_iri"), rc["case_iri"]),
        "case_revision_digest": (case.get("case_revision_digest"), rc["case_revision_digest"]),
        "receipt_sha256": (body.get("receipt_sha256"), rc["receipt_sha256"]),
        "subject_sha": (body.get("subject_sha"), rc["subject_sha"]),
    }
    for key, (got, want) in checks.items():
        if got != want:
            errors.append(f"replay: receipt {key} {got!r} != witness {want!r}")
    if not str(case.get("generator_identity", "")).startswith(rc["generator_identity_prefix"]):
        errors.append("replay: receipt generator identity prefix drift")
    if rc["subject_sha"] != vocab:
        errors.append("replay: witness receipt subject and vocabulary subject disagree")
    return errors


# --------------------------------------------------------------------------- entry


def run_court(root: Path, witness_repo: Path | None = None) -> dict:
    texts, witness = load(root)
    errors = structural_errors(texts, witness)
    # Mutants are only meaningful against a subject that passes: a refused
    # subject already carries its bits, and its anchors may be the thing missing.
    total, survivors = mutant_survivors(texts, witness) if not errors else (0, [])
    replay = None
    if witness_repo is not None:
        replay = witness_replay_errors(witness_repo, witness)
    return {"errors": errors, "mutants": total, "survivors": survivors, "replay": replay}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--witness-repo", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    started = time.perf_counter()
    result = run_court(args.root, args.witness_repo)
    elapsed_ms = (time.perf_counter() - started) * 1000

    for error in result["errors"]:
        print(f"REFUSED: {error}", file=sys.stderr)
    for label in result["survivors"]:
        print(f"VACUOUS: mutant survived: {label}", file=sys.stderr)
    for error in result["replay"] or []:
        print(f"REFUSED: {error}", file=sys.stderr)

    ok = not result["errors"] and not result["survivors"] and not (result["replay"] or [])
    killed = result["mutants"] - len(result["survivors"])
    print(f"r25-007-sweep: {len(SWEEP)} documents; rfc-front: {len(RFC_FRONT)} RFCs; "
          f"rfc-0003 witness; rfc-0005 registry; rfc-id uniqueness")
    print(f"structural: {'PASS' if not result['errors'] else 'FAIL'} ({len(result['errors'])} refusals)")
    print(f"anti-vacuity: {killed}/{result['mutants']} mutants refused")
    if result["replay"] is None:
        print("witness-replay: NOT_RUN (no --witness-repo)")
    else:
        print(f"witness-replay: {'PASS' if not result['replay'] else 'FAIL'}")
    print(f"standing: {'ALIVE' if ok else 'REFUSED'}(rfc-standing) in {elapsed_ms:.1f} ms")

    if args.receipt:
        receipt = {
            "schema": "engineering-standards.rfc-standing-receipt.v26.9.26",
            "repository": os.environ.get("GITHUB_REPOSITORY", "seanchatmangpt/engineering-standards"),
            "candidate_sha": os.environ.get("GITHUB_SHA", "LOCAL_UNBOUND"),
            "court": "scripts/check-rfc-standing.py",
            "authority": "NONE",
            "standing": "ALIVE" if ok else "REFUSED",
            "refusals": result["errors"] + (result["replay"] or []),
            "mutants_total": result["mutants"],
            "mutants_refused": killed,
            "witness_replay": "NOT_RUN" if result["replay"] is None else ("PASS" if ok else "FAIL"),
            "elapsed_ms": round(elapsed_ms, 3),
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "non_claims": ["xaas runtime execution", "semantic-case-study-pack admission",
                           "cross-repository standing without --witness-repo"],
        }
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"receipt: {args.receipt}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
