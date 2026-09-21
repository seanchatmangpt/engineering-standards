#!/usr/bin/env python3
"""Repository-native court for the Semantic Engineering Protocol profile.

This court proves only the checked RDF/SHACL/JSON profile. It does not prove
runtime SA2A execution, Jira mutation, CommandBus actuation, deployment, or
cross-repository standing.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from pyshacl import validate
from rdflib import Graph, Literal, Namespace, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
SEMANTIC = ROOT / "semantic"

ESP = Namespace("https://w3id.org/chatman/engineering-standards#")
SJ = Namespace("https://ggen-igniter.dev/ontology/semantic-jira#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
APS = Namespace("https://w3id.org/chatman/aps#")

PROFILE = SEMANTIC / "semantic-engineering-profile.ttl"
SHAPES = SEMANTIC / "semantic-engineering-shapes.ttl"
DATA = SEMANTIC / "example-work-order.ttl"
SCHEMA = SEMANTIC / "semantic-work-envelope.schema.json"
ENVELOPE = SEMANTIC / "example-work-envelope.json"

SOURCE_REFS = {
    URIRef("https://github.com/seanchatmangpt/agile-protocol-specification/commit/5c31d9d05fe36dc1eca3a26c9eb5cd267a2cf625"),
    URIRef("https://github.com/seanchatmangpt/ash_a2a/commit/baa135d5c6129aea1d4b38d48a12ad87e132b638"),
    URIRef("https://github.com/seanchatmangpt/ggen_igniter/pull/20"),
    URIRef("https://github.com/seanchatmangpt/ggen_igniter/pull/24"),
}


def parse_turtle(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path, format="turtle")
    return graph


def require_profile_contract(profile: Graph) -> None:
    protocol = ESP.SemanticEngineeringProtocol
    if (protocol, RDF.type, APS.Contract) not in profile:
        raise AssertionError("SemanticEngineeringProtocol must remain an aps:Contract")

    ontology = URIRef("https://w3id.org/chatman/engineering-standards")
    observed_refs = set(profile.objects(ontology, DCTERMS.references))
    missing = SOURCE_REFS - observed_refs
    if missing:
        raise AssertionError(f"profile lost exact prior-art references: {sorted(map(str, missing))}")


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


def require_positive_shacl(data: Graph, shapes: Graph) -> None:
    conforms, report = shacl_conforms(data, shapes)
    if not conforms:
        raise AssertionError(f"canonical semantic fixture must conform:\n{report}")


def require_negative_shacl(data: Graph, shapes: Graph) -> None:
    work_orders = list(data.subjects(RDF.type, SJ.WorkOrder))
    if len(work_orders) != 1:
        raise AssertionError(f"expected exactly one fixture WorkOrder, got {len(work_orders)}")
    work_order = work_orders[0]

    mutations = [
        (SJ.authorityCeiling, Literal("DO"), "DO authority ceiling"),
        (ESP.projectionAuthority, Literal("COMMAND_BUS"), "projection authority"),
        (ESP.graphDigest, Literal("not-a-digest"), "graph digest"),
        (ESP.transportProfile, Literal("A2A"), "non-SA2A transport"),
    ]

    for predicate, bad_value, label in mutations:
        candidate = Graph()
        for triple in data:
            candidate.add(triple)
        candidate.set((work_order, predicate, bad_value))
        conforms, _ = shacl_conforms(candidate, shapes)
        if conforms:
            raise AssertionError(f"falsifier did not fail closed: {label}")


def require_json_contract() -> None:
    schema = json.loads(SCHEMA.read_text())
    envelope = json.loads(ENVELOPE.read_text())

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
    validator.validate(envelope)

    mutations = [
        ("authority_ceiling", "DO"),
        ("projection_authority", "COMMAND_BUS"),
        ("graph_digest", "not-a-digest"),
        ("transport_profile", "A2A"),
    ]

    for key, bad_value in mutations:
        candidate = copy.deepcopy(envelope)
        candidate[key] = bad_value
        try:
            validator.validate(candidate)
        except ValidationError:
            continue
        raise AssertionError(f"JSON falsifier did not fail closed: {key}={bad_value!r}")


def main() -> None:
    profile = parse_turtle(PROFILE)
    shapes = parse_turtle(SHAPES)
    data = parse_turtle(DATA)

    require_profile_contract(profile)
    require_positive_shacl(data, shapes)
    require_negative_shacl(data, shapes)
    require_json_contract()

    print("semantic-engineering-profile: ALIVE(repository-conformance)")
    print("evidence-ceiling: RDF parse + exact source refs + SHACL positive/negative + JSON Schema positive/negative")
    print("non-claims: runtime SA2A, Jira mutation, CommandBus DO, deployment, merge, publication, cross-repository standing")


if __name__ == "__main__":
    main()
