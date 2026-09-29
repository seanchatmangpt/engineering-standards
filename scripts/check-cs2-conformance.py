#!/usr/bin/env python3
"""RFC-CS2-001 enterprise information conformance engine.

This module is deliberately standard-library only. It evaluates the semantic
requirements that JSON Schema cannot express: cross-object references,
monotonic conformance levels, typed standing, falsifier presence, route
authority, process bindings, and deterministic semantic fingerprints.

It does not establish truth, external execution, provider acceptance, or
authority. It can be imported as a library or used as a CLI.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence


STANDARD = "RFC-CS2-001"
SCHEMA_VERSION = "cs2.conformance.v1"
LEVELS = ("C0", "C1", "C2", "C3", "C4")
LEVEL_RANK = {name: rank for rank, name in enumerate(LEVELS)}
STANDINGS = {
    "OBSERVED",
    "DERIVED",
    "REPORTED",
    "HYPOTHESIS",
    "REFUTED",
    "UNKNOWN",
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str
    requirement: str
    level: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ConformanceResult:
    standard: str
    requested_level: str
    actual_level: str
    conforms: bool
    semantic_fingerprint: str
    issues: tuple[ValidationIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "standard": self.standard,
            "requested_level": self.requested_level,
            "actual_level": self.actual_level,
            "conforms": self.conforms,
            "semantic_fingerprint": self.semantic_fingerprint,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def semantic_projection(document: Mapping[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(dict(document))
    conformance = projected.get("conformance")
    if isinstance(conformance, dict):
        conformance.pop("actual_level", None)
        conformance.pop("semantic_fingerprint", None)
        conformance.pop("issues", None)
    return projected


def semantic_fingerprint(document: Mapping[str, Any]) -> str:
    digest = hashlib.sha256(canonical_json(semantic_projection(document))).hexdigest()
    return f"sha256:{digest}"


def _issue(
    issues: list[ValidationIssue],
    code: str,
    path: str,
    message: str,
    requirement: str,
    level: str,
) -> None:
    issues.append(ValidationIssue(code, path, message, requirement, level))


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ids(items: Sequence[Any]) -> list[str]:
    return [
        item.get("id")
        for item in items
        if isinstance(item, dict) and _nonempty_string(item.get("id"))
    ]


def check_standard_identity(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if document.get("standard") != STANDARD:
        _issue(
            issues,
            "INVALID_SHAPE",
            "$.standard",
            f"standard must equal {STANDARD}",
            "CS2-R001",
            "C0",
        )
    if document.get("schema_version") != SCHEMA_VERSION:
        _issue(
            issues,
            "INVALID_SHAPE",
            "$.schema_version",
            f"schema_version must equal {SCHEMA_VERSION}",
            "CS2-R001",
            "C0",
        )
    return issues


def check_subject(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    subject = _mapping(document.get("subject"))
    for field, code, requirement in (
        ("id", "IDENTITY_MISSING", "CS2-R002"),
        ("kind", "IDENTITY_MISSING", "CS2-R002"),
        ("revision", "REVISION_MISSING", "CS2-R002"),
    ):
        if not _nonempty_string(subject.get(field)):
            _issue(
                issues,
                code,
                f"$.subject.{field}",
                f"subject.{field} must be a non-empty string",
                requirement,
                "C0",
            )
    return issues


def check_claim_identity(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    claims = _list(document.get("claims"))
    if not claims:
        _issue(
            issues,
            "INVALID_SHAPE",
            "$.claims",
            "at least one claim is required",
            "CS2-R003",
            "C0",
        )
        return issues

    seen: set[str] = set()
    for index, claim in enumerate(claims):
        path = f"$.claims[{index}]"
        if not isinstance(claim, dict):
            _issue(
                issues, "INVALID_SHAPE", path, "claim must be an object", "CS2-R003", "C0"
            )
            continue
        claim_id = claim.get("id")
        if not _nonempty_string(claim_id):
            _issue(
                issues,
                "IDENTITY_MISSING",
                f"{path}.id",
                "claim.id must be non-empty",
                "CS2-R003",
                "C0",
            )
        elif claim_id in seen:
            _issue(
                issues,
                "DUPLICATE_ID",
                f"{path}.id",
                f"duplicate claim id: {claim_id}",
                "CS2-R003",
                "C0",
            )
        else:
            seen.add(claim_id)

        if not _nonempty_string(claim.get("predicate")):
            _issue(
                issues,
                "INVALID_SHAPE",
                f"{path}.predicate",
                "claim.predicate must be non-empty",
                "CS2-R003",
                "C0",
            )
    return issues


def check_sources(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    sources = _list(document.get("sources"))
    if not sources:
        _issue(
            issues,
            "PROVENANCE_MISSING",
            "$.sources",
            "C1 requires at least one source",
            "CS2-R004",
            "C1",
        )
        return issues

    for index, source in enumerate(sources):
        path = f"$.sources[{index}]"
        if not isinstance(source, dict):
            _issue(
                issues, "INVALID_SHAPE", path, "source must be an object", "CS2-R004", "C1"
            )
            continue
        for field in ("id", "kind", "locator"):
            if not _nonempty_string(source.get(field)):
                _issue(
                    issues,
                    "PROVENANCE_MISSING",
                    f"{path}.{field}",
                    f"source.{field} must be non-empty",
                    "CS2-R004",
                    "C1",
                )
    return issues


def check_evidence(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    subject_id = _mapping(document.get("subject")).get("id")
    evidence = _list(document.get("evidence"))
    if not evidence:
        _issue(
            issues,
            "PROVENANCE_MISSING",
            "$.evidence",
            "C1 requires at least one evidence object",
            "CS2-R005",
            "C1",
        )
        return issues

    for index, item in enumerate(evidence):
        path = f"$.evidence[{index}]"
        if not isinstance(item, dict):
            _issue(
                issues, "INVALID_SHAPE", path, "evidence must be an object", "CS2-R005", "C1"
            )
            continue
        for field in ("id", "kind", "subject_ref", "source_ref", "locator"):
            if not _nonempty_string(item.get(field)):
                _issue(
                    issues,
                    "PROVENANCE_MISSING",
                    f"{path}.{field}",
                    f"evidence.{field} must be non-empty",
                    "CS2-R005",
                    "C1",
                )
        if _nonempty_string(subject_id) and item.get("subject_ref") != subject_id:
            _issue(
                issues,
                "BROKEN_REFERENCE",
                f"{path}.subject_ref",
                "evidence must bind to the exact bundle subject",
                "CS2-R005",
                "C1",
            )
    return issues


def check_references(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    sources = set(_ids(_list(document.get("sources"))))
    evidence = set(_ids(_list(document.get("evidence"))))
    claims = set(_ids(_list(document.get("claims"))))

    for index, item in enumerate(_list(document.get("evidence"))):
        if isinstance(item, dict):
            source_ref = item.get("source_ref")
            if _nonempty_string(source_ref) and source_ref not in sources:
                _issue(
                    issues,
                    "BROKEN_REFERENCE",
                    f"$.evidence[{index}].source_ref",
                    f"unknown source_ref: {source_ref}",
                    "CS2-R006",
                    "C1",
                )

    for index, claim in enumerate(_list(document.get("claims"))):
        if not isinstance(claim, dict):
            continue
        for ref in _list(claim.get("source_refs")):
            if ref not in sources:
                _issue(
                    issues,
                    "BROKEN_REFERENCE",
                    f"$.claims[{index}].source_refs",
                    f"unknown source ref: {ref}",
                    "CS2-R006",
                    "C1",
                )
        for ref in _list(claim.get("evidence_refs")):
            if ref not in evidence:
                _issue(
                    issues,
                    "BROKEN_REFERENCE",
                    f"$.claims[{index}].evidence_refs",
                    f"unknown evidence ref: {ref}",
                    "CS2-R006",
                    "C1",
                )
        for ref in _list(claim.get("contradicts")):
            if ref not in claims:
                _issue(
                    issues,
                    "BROKEN_REFERENCE",
                    f"$.claims[{index}].contradicts",
                    f"unknown contradicted claim ref: {ref}",
                    "CS2-R011",
                    "C2",
                )
    return issues


def check_claim_provenance(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, claim in enumerate(_list(document.get("claims"))):
        if not isinstance(claim, dict):
            continue
        if claim.get("standing") != "UNKNOWN":
            source_refs = _list(claim.get("source_refs"))
            evidence_refs = _list(claim.get("evidence_refs"))
            if not source_refs and not evidence_refs:
                _issue(
                    issues,
                    "PROVENANCE_MISSING",
                    f"$.claims[{index}]",
                    "non-UNKNOWN claim requires source_refs or evidence_refs",
                    "CS2-R007",
                    "C1",
                )
    return issues


def check_claim_standing(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, claim in enumerate(_list(document.get("claims"))):
        if not isinstance(claim, dict):
            continue
        standing = claim.get("standing")
        if standing not in STANDINGS:
            _issue(
                issues,
                "INVALID_SHAPE",
                f"$.claims[{index}].standing",
                f"standing must be one of {sorted(STANDINGS)}",
                "CS2-R008",
                "C2",
            )
    return issues


def check_falsifiers(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, claim in enumerate(_list(document.get("claims"))):
        if not isinstance(claim, dict) or claim.get("standing") == "REFUTED":
            continue
        observation = _mapping(claim.get("falsifier")).get("observation")
        if not _nonempty_string(observation):
            _issue(
                issues,
                "FALSIFIER_MISSING",
                f"$.claims[{index}].falsifier.observation",
                "non-REFUTED claim requires a falsifier observation",
                "CS2-R009",
                "C2",
            )
    return issues


def check_global_ids(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    owner: dict[str, str] = {}
    for namespace in ("sources", "evidence", "claims"):
        for index, item in enumerate(_list(document.get(namespace))):
            if not isinstance(item, dict) or not _nonempty_string(item.get("id")):
                continue
            local_id = item["id"]
            previous = owner.get(local_id)
            if previous is not None:
                _issue(
                    issues,
                    "DUPLICATE_ID",
                    f"$.{namespace}[{index}].id",
                    f"id {local_id!r} already belongs to {previous}",
                    "CS2-R010",
                    "C2",
                )
            else:
                owner[local_id] = f"{namespace}[{index}]"
    return issues


def check_route(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    route = document.get("route")
    if not isinstance(route, dict):
        _issue(
            issues,
            "ROUTE_MISSING",
            "$.route",
            "C3 requires a route object",
            "CS2-R012",
            "C3",
        )
        return issues

    for field in (
        "consumer",
        "workflow",
        "projection_id",
        "minimum_level",
        "delivery_semantics",
        "projection_authority",
    ):
        if not _nonempty_string(route.get(field)):
            _issue(
                issues,
                "ROUTE_MISSING",
                f"$.route.{field}",
                f"route.{field} must be non-empty",
                "CS2-R012",
                "C3",
            )

    if route.get("projection_authority") != "NONE":
        _issue(
            issues,
            "PROJECTION_AUTHORITY_VIOLATION",
            "$.route.projection_authority",
            "projection_authority must equal NONE",
            "CS2-R013",
            "C3",
        )

    minimum = route.get("minimum_level")
    requested = _mapping(document.get("conformance")).get("requested_level")
    if minimum not in LEVEL_RANK:
        _issue(
            issues,
            "ROUTE_MISSING",
            "$.route.minimum_level",
            "route.minimum_level must be a CS2 level",
            "CS2-R014",
            "C3",
        )
    elif requested in LEVEL_RANK and LEVEL_RANK[minimum] > LEVEL_RANK[requested]:
        _issue(
            issues,
            "ROUTE_MISSING",
            "$.route.minimum_level",
            "route.minimum_level cannot exceed bundle requested_level",
            "CS2-R014",
            "C3",
        )
    return issues


def check_process(document: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    process = document.get("process")
    if not isinstance(process, dict):
        _issue(
            issues,
            "PROCESS_BINDING_MISSING",
            "$.process",
            "C4 requires a process object",
            "CS2-R015",
            "C4",
        )
        return issues

    for field in ("ocel_ref", "receipt_schema", "replay_binding", "episode_id", "consequence_class"):
        if not _nonempty_string(process.get(field)):
            _issue(
                issues,
                "PROCESS_BINDING_MISSING",
                f"$.process.{field}",
                f"process.{field} must be non-empty",
                "CS2-R015",
                "C4",
            )

    if not _list(process.get("event_refs")):
        _issue(
            issues,
            "PROCESS_BINDING_MISSING",
            "$.process.event_refs",
            "C4 requires at least one process event reference",
            "CS2-R016",
            "C4",
        )

    consequence = process.get("consequence_class")
    if _nonempty_string(consequence) and consequence != "NONE":
        if not _nonempty_string(process.get("authority_requirement")):
            _issue(
                issues,
                "PROCESS_BINDING_MISSING",
                "$.process.authority_requirement",
                "consequential C4 process must name an authority requirement",
                "CS2-R017",
                "C4",
            )
    return issues


LEVEL_CHECKS = {
    "C0": (check_standard_identity, check_subject, check_claim_identity),
    "C1": (check_sources, check_evidence, check_references, check_claim_provenance),
    "C2": (check_claim_standing, check_falsifiers, check_global_ids, check_references),
    "C3": (check_route,),
    "C4": (check_process,),
}


def level_issues(document: Mapping[str, Any]) -> dict[str, list[ValidationIssue]]:
    evaluated: dict[str, list[ValidationIssue]] = {}
    accumulated: list[ValidationIssue] = []
    seen: set[tuple[str, str, str]] = set()

    for level in LEVELS:
        for check in LEVEL_CHECKS[level]:
            for issue in check(document):
                key = (issue.code, issue.path, issue.requirement)
                if key not in seen:
                    seen.add(key)
                    accumulated.append(issue)
        evaluated[level] = list(accumulated)

    return evaluated


def highest_level(document: Mapping[str, Any]) -> tuple[str, dict[str, list[ValidationIssue]]]:
    evaluated = level_issues(document)
    actual = "NONE"
    for level in LEVELS:
        if evaluated[level]:
            break
        actual = level
    return actual, evaluated


def check_requested_level(
    document: Mapping[str, Any],
    actual_level: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    requested = _mapping(document.get("conformance")).get("requested_level")
    if requested not in LEVEL_RANK:
        _issue(
            issues,
            "INVALID_SHAPE",
            "$.conformance.requested_level",
            "requested_level must be a CS2 level",
            "CS2-R018",
            "C0",
        )
        return issues

    actual_rank = -1 if actual_level == "NONE" else LEVEL_RANK[actual_level]
    if LEVEL_RANK[requested] > actual_rank:
        _issue(
            issues,
            "REQUESTED_LEVEL_UNSATISFIED",
            "$.conformance.requested_level",
            f"requested {requested} but highest achieved level is {actual_level}",
            "CS2-R018",
            requested,
        )
    return issues


def validate(document: Mapping[str, Any]) -> ConformanceResult:
    actual, evaluated = highest_level(document)
    requested = _mapping(document.get("conformance")).get("requested_level")
    requested_name = requested if isinstance(requested, str) else "UNKNOWN"

    if requested in LEVEL_RANK:
        semantic_issues = list(evaluated[requested])
    else:
        semantic_issues = list(evaluated["C0"])

    semantic_issues.extend(check_requested_level(document, actual))
    deduped: list[ValidationIssue] = []
    seen: set[tuple[str, str, str]] = set()
    for issue in semantic_issues:
        key = (issue.code, issue.path, issue.requirement)
        if key not in seen:
            seen.add(key)
            deduped.append(issue)

    return ConformanceResult(
        standard=STANDARD,
        requested_level=requested_name,
        actual_level=actual,
        conforms=not deduped,
        semantic_fingerprint=semantic_fingerprint(document),
        issues=tuple(deduped),
    )


def annotate(document: Mapping[str, Any], result: ConformanceResult) -> dict[str, Any]:
    output = copy.deepcopy(dict(document))
    conformance = output.setdefault("conformance", {})
    if not isinstance(conformance, dict):
        conformance = {}
        output["conformance"] = conformance
    conformance["actual_level"] = result.actual_level
    conformance["semantic_fingerprint"] = result.semantic_fingerprint
    conformance["issues"] = [issue.to_dict() for issue in result.issues]
    return output


def load_document(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return value


def iter_inputs(paths: Iterable[str]) -> Iterator[Path]:
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            yield from sorted(
                candidate
                for candidate in path.rglob("*.json")
                if candidate.is_file()
            )
        else:
            yield path


def validate_paths(paths: Iterable[str]) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []
    for path in iter_inputs(paths):
        try:
            document = load_document(path)
            result = validate(document)
            outputs.append(
                {
                    "path": str(path),
                    "result": result.to_dict(),
                }
            )
        except (OSError, ValueError, json.JSONDecodeError) as error:
            outputs.append(
                {
                    "path": str(path),
                    "result": {
                        "standard": STANDARD,
                        "requested_level": "UNKNOWN",
                        "actual_level": "NONE",
                        "conforms": False,
                        "semantic_fingerprint": "",
                        "issues": [
                            {
                                "code": "INVALID_SHAPE",
                                "path": "$",
                                "message": str(error),
                                "requirement": "CS2-R001",
                                "level": "C0",
                            }
                        ],
                    },
                }
            )
    return outputs


def _emit(value: Any, jsonl: bool) -> None:
    if jsonl and isinstance(value, list):
        for item in value:
            print(json.dumps(item, ensure_ascii=False, sort_keys=True))
    else:
        print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate RFC-CS2-001 enterprise information conformance."
    )
    parser.add_argument("paths", nargs="+", help="JSON bundle file or directory")
    parser.add_argument(
        "--jsonl",
        action="store_true",
        help="emit one compact JSON result per input path",
    )
    parser.add_argument(
        "--annotate",
        action="store_true",
        help="include derived conformance fields in output",
    )
    parser.add_argument(
        "--fail-below",
        choices=LEVELS,
        default=None,
        help="exit non-zero when any bundle achieves below this level",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = validate_paths(args.paths)

    if args.annotate:
        annotated: list[dict[str, Any]] = []
        for row in rows:
            path = Path(row["path"])
            try:
                document = load_document(path)
                result = validate(document)
                annotated.append(
                    {
                        "path": str(path),
                        "document": annotate(document, result),
                        "result": result.to_dict(),
                    }
                )
            except (OSError, ValueError, json.JSONDecodeError):
                annotated.append(row)
        rows = annotated

    _emit(rows, args.jsonl)

    for row in rows:
        result = row["result"]
        if not result.get("conforms", False):
            return 2
        if args.fail_below:
            actual = result.get("actual_level", "NONE")
            rank = -1 if actual == "NONE" else LEVEL_RANK.get(actual, -1)
            if rank < LEVEL_RANK[args.fail_below]:
                return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
