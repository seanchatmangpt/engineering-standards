#!/usr/bin/env python3
"""Qualification court for the Engineering Standards root profile."""

from __future__ import annotations

import argparse
import copy
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
SEMANTIC = ROOT / "semantic"
ES = Namespace("https://w3id.org/chatman/engineering-standards#")
PROF = Namespace("http://www.w3.org/ns/dx/prof/")

ROOT_ONTOLOGY = SEMANTIC / "semantic-engineering-profile.ttl"
SHAPES = SEMANTIC / "semantic-engineering-shapes.ttl"
DATA = SEMANTIC / "example-work-order.ttl"
MANIFEST = ROOT / "MANIFEST.json"

REQUIRED_PROFILES = {
    "semantic/compat/aps-v26.9.17.ttl",
    "semantic/profiles/sjira.ttl",
    "semantic/profiles/sa2a.ttl",
    "semantic/profiles/manufacturing.ttl",
    "semantic/profiles/documentation.ttl",
    "semantic/profiles/process-evidence.ttl",
}

PUBLIC_PROFILE_TARGETS = {
    URIRef("https://www.w3.org/TR/prov-o/"),
    URIRef("https://www.w3.org/TR/shacl/"),
    URIRef("https://www.w3.org/TR/odrl-model/"),
    URIRef("https://www.dublincore.org/specifications/dublin-core/dcmi-terms/"),
    URIRef("https://open-services.net/"),
    URIRef("https://www.w3.org/TR/dx-prof/"),
    URIRef("https://www.w3.org/TR/vocab-dcat-3/"),
}

SCHEMA_EXAMPLES = {
    "semantic/semantic-work-envelope.schema.json": "semantic/example-work-envelope.json",
    "semantic/schemas/actuation-intent.schema.json": "semantic/examples/actuation-intent.valid.json",
    "semantic/schemas/authority-decision.schema.json": "semantic/examples/authority-decision.valid.json",
    "semantic/schemas/refusal.schema.json": "semantic/examples/refusal.valid.json",
    "semantic/schemas/evidence-receipt.schema.json": "semantic/examples/evidence-receipt.valid.json",
    "semantic/schemas/standing-assertion.schema.json": "semantic/examples/standing-assertion.valid.json",
    "semantic/schemas/process-evidence-event.schema.json": "semantic/examples/process-evidence-event.valid.json",
    "semantic/schemas/normative-claim.schema.json": "semantic/examples/normative-claim.valid.json",
}


def parse_all_turtle() -> dict[Path, Graph]:
    parsed: dict[Path, Graph] = {}
    for path in sorted(SEMANTIC.rglob("*.ttl")):
        graph = Graph()
        graph.parse(path, format="turtle")
        parsed[path] = graph
    if not parsed:
        raise AssertionError("no semantic Turtle graphs found")
    return parsed


def root_contract(graph: Graph) -> None:
    root = URIRef("https://w3id.org/chatman/engineering-standards")
    if (root, RDF.type, PROF.Profile) not in graph:
        raise AssertionError("root ontology must be a prof:Profile")
    missing = PUBLIC_PROFILE_TARGETS - set(graph.objects(root, PROF.isProfileOf))
    if missing:
        raise AssertionError(f"root lost public profile targets: {sorted(map(str, missing))}")

    text = ROOT_ONTOLOGY.read_text()
    if "chatman/aps#" in text:
        raise AssertionError("APS namespace must not be normative in the root ontology")
    if "owl:equivalentClass" in text or "owl:equivalentProperty" in text:
        raise AssertionError("root may not assert equivalence without an explicit proof court")


def manifest_contract() -> dict:
    manifest = json.loads(MANIFEST.read_text())
    if manifest["authority"]["rootOntology"] != "semantic/semantic-engineering-profile.ttl":
        raise AssertionError("manifest rootOntology drift")
    for rel in REQUIRED_PROFILES:
        if not (ROOT / rel).is_file():
            raise AssertionError(f"manifest/profile surface missing: {rel}")
    for rel in manifest["authority"]["lifecycleSchemas"]:
        if not (ROOT / rel).is_file():
            raise AssertionError(f"manifest lifecycle schema missing: {rel}")
    claim_schema = manifest["authority"].get("normativeClaimSchema")
    if not claim_schema or not (ROOT / claim_schema).is_file():
        raise AssertionError("manifest normative claim schema missing")
    if manifest["generatedVsHandwritten"]["canonicalSemanticSource"] != "semantic/semantic-engineering-profile.ttl":
        raise AssertionError("canonical semantic source drift")
    return manifest


def shacl_conforms(data: Graph, shapes: Graph) -> tuple[bool, str]:
    conforms, _, report = validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="rdfs",
        advanced=True,
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
    )
    return bool(conforms), str(report)


def copy_graph(graph: Graph) -> Graph:
    candidate = Graph()
    for triple in graph:
        candidate.add(triple)
    return candidate


def shacl_contract(data: Graph, shapes: Graph) -> None:
    conforms, report = shacl_conforms(data, shapes)
    if not conforms:
        raise AssertionError(f"canonical root fixture must conform:\n{report}")

    work = next(data.subjects(RDF.type, ES.WorkOrder))
    generated = next(data.subjects(RDF.type, ES.GeneratedArtifact))
    mutations = [
        (work, ES.authorityCeiling, ES.DO, "DO authority ceiling"),
        (work, ES.projectionAuthority, ES.DO, "work projection authority"),
        (work, ES.graphDigest, URIRef("https://example.org/not-a-literal"), "graph digest shape"),
        (generated, ES.projectionAuthority, ES.DO, "generated artifact authority"),
    ]
    for subject, predicate, bad_value, label in mutations:
        candidate = copy_graph(data)
        candidate.set((subject, predicate, bad_value))
        conforms, _ = shacl_conforms(candidate, shapes)
        if conforms:
            raise AssertionError(f"SHACL falsifier did not fail closed: {label}")


def validator_for(rel: str) -> tuple[Draft202012Validator, dict]:
    schema = json.loads((ROOT / rel).read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker()), schema


def validate_schema_examples() -> None:
    for schema_rel, example_rel in SCHEMA_EXAMPLES.items():
        validator, _ = validator_for(schema_rel)
        validator.validate(json.loads((ROOT / example_rel).read_text()))


def must_refuse(schema_rel: str, example_rel: str, mutate, label: str) -> None:
    validator, _ = validator_for(schema_rel)
    value = json.loads((ROOT / example_rel).read_text())
    candidate = mutate(copy.deepcopy(value))
    try:
        validator.validate(candidate)
    except ValidationError:
        return
    raise AssertionError(f"JSON falsifier did not fail closed: {label}")


def json_falsifiers() -> None:
    must_refuse(
        "semantic/semantic-work-envelope.schema.json",
        "semantic/example-work-envelope.json",
        lambda x: {**x, "authority_ceiling": "DO"},
        "transport DO ceiling",
    )
    must_refuse(
        "semantic/schemas/actuation-intent.schema.json",
        "semantic/examples/actuation-intent.valid.json",
        lambda x: {**x, "requested_authority": "SELECT"},
        "actuation intent non-DO request",
    )
    must_refuse(
        "semantic/schemas/authority-decision.schema.json",
        "semantic/examples/authority-decision.valid.json",
        lambda x: {**x, "decision": "REFUSED", "reason_code": "REFUSED:TEST", "reason": "test", "granted_authority": "DO"},
        "refusal that also grants DO",
    )
    must_refuse(
        "semantic/schemas/refusal.schema.json",
        "semantic/examples/refusal.valid.json",
        lambda x: {k: v for k, v in x.items() if k != "reason"},
        "refusal without reason",
    )
    must_refuse(
        "semantic/schemas/evidence-receipt.schema.json",
        "semantic/examples/evidence-receipt.valid.json",
        lambda x: {**x, "candidate_sha": "deadbeef"},
        "receipt with non-exact candidate SHA",
    )
    must_refuse(
        "semantic/schemas/standing-assertion.schema.json",
        "semantic/examples/standing-assertion.valid.json",
        lambda x: {**x, "receipt_iris": [], "observed_execution": False, "replay_verified": False},
        "ALIVE without receipt execution replay crown",
    )
    must_refuse(
        "semantic/schemas/process-evidence-event.schema.json",
        "semantic/examples/process-evidence-event.valid.json",
        lambda x: {**x, "objects": []},
        "process event without object identity",
    )
    must_refuse(
        "semantic/schemas/normative-claim.schema.json",
        "semantic/examples/normative-claim.valid.json",
        lambda x: {**x, "falsifiers": []},
        "normative root claim without falsifier",
    )


def compatibility_contract(parsed: dict[Path, Graph]) -> None:
    aps_path = SEMANTIC / "compat" / "aps-v26.9.17.ttl"
    if "owl:equivalent" in aps_path.read_text():
        raise AssertionError("APS compatibility may not manufacture OWL equivalence")

    root_iri = URIRef("https://w3id.org/chatman/engineering-standards")
    for rel in sorted(REQUIRED_PROFILES - {"semantic/compat/aps-v26.9.17.ttl"}):
        graph = parsed[ROOT / rel]
        if not list(graph.subjects(PROF.isProfileOf, root_iri)):
            raise AssertionError(f"{rel} is not explicitly a profile of the root")


def write_receipt(path: Path, parsed_count: int) -> None:
    sha = os.environ.get("GITHUB_SHA", "LOCAL_UNBOUND")
    receipt = {
        "schema": "engineering-standards.root-conformance-receipt.v26.9.21",
        "repository": os.environ.get("GITHUB_REPOSITORY", "seanchatmangpt/engineering-standards"),
        "candidate_sha": sha,
        "court": "scripts/check-semantic-standard.py",
        "standing": "ALIVE",
        "subject": "repository-semantic-conformance",
        "evidence_ceiling": [
            "all semantic Turtle graphs parse",
            "root public-profile direction and no APS normative import",
            "manifest authority surfaces exist",
            "root SHACL positive fixture",
            "4 root SHACL negative falsifiers",
            "8 JSON schemas + positive examples",
            "8 JSON negative falsifiers",
            "downstream profiles bind engineering-standards root",
            "APS compatibility has no OWL equivalence assertion"
        ],
        "turtle_graph_count": parsed_count,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "non_claims": [
            "SA2A runtime execution",
            "Jira/GitHub issue mutation",
            "CommandBus/BRCE DO",
            "deployment",
            "publication",
            "cross-repository standing"
        ]
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    parsed = parse_all_turtle()
    root_contract(parsed[ROOT_ONTOLOGY])
    manifest_contract()
    shacl_contract(parsed[DATA], parsed[SHAPES])
    validate_schema_examples()
    json_falsifiers()
    compatibility_contract(parsed)

    print(f"turtle-graphs: {len(parsed)} parsed")
    print("root-direction: PASS")
    print("shacl: PASS (positive fixture + 4 negative falsifiers)")
    print("json-schema: PASS (8 positive examples + 8 negative falsifiers)")
    print("compatibility: PASS")
    print("standing: ALIVE(repository-semantic-conformance)")
    if args.receipt:
        write_receipt(args.receipt, len(parsed))
        print(f"receipt: {args.receipt}")
    print("non-claims: runtime SA2A, Jira mutation, CommandBus DO, deployment, publication, cross-repository standing")


if __name__ == "__main__":
    main()
