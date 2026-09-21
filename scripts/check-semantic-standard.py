#!/usr/bin/env python3
"""Qualification court for the Engineering Standards root profile."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
SEMANTIC = ROOT / "semantic"
ES = Namespace("https://w3id.org/chatman/engineering-standards#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
PROF = Namespace("http://www.w3.org/ns/dx/prof/")

ROOT_ONTOLOGY = SEMANTIC / "semantic-engineering-profile.ttl"
SHAPES = SEMANTIC / "semantic-engineering-shapes.ttl"
DATA = SEMANTIC / "example-work-order.ttl"
SCHEMA = SEMANTIC / "semantic-work-envelope.schema.json"
ENVELOPE = SEMANTIC / "example-work-envelope.json"
MANIFEST = ROOT / "MANIFEST.json"

REQUIRED_PROFILES = {
    "semantic/compat/aps-v26.9.17.ttl",
    "semantic/profiles/sjira.ttl",
    "semantic/profiles/sa2a.ttl",
    "semantic/profiles/manufacturing.ttl",
    "semantic/profiles/documentation.ttl",
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

    targets = set(graph.objects(root, PROF.isProfileOf))
    missing = PUBLIC_PROFILE_TARGETS - targets
    if missing:
        raise AssertionError(f"root lost public profile targets: {sorted(map(str, missing))}")

    text = ROOT_ONTOLOGY.read_text()
    if "chatman/aps#" in text:
        raise AssertionError("APS namespace must not be normative in the root ontology")
    if "owl:equivalentClass" in text or "owl:equivalentProperty" in text:
        raise AssertionError("root may not assert equivalence without an explicit proof court")


def manifest_contract() -> None:
    manifest = json.loads(MANIFEST.read_text())
    if manifest["authority"]["rootOntology"] != "semantic/semantic-engineering-profile.ttl":
        raise AssertionError("manifest rootOntology drift")
    for path in REQUIRED_PROFILES:
        if not (ROOT / path).is_file():
            raise AssertionError(f"manifest/profile surface missing: {path}")
    if manifest["generatedVsHandwritten"]["canonicalSemanticSource"] != "semantic/semantic-engineering-profile.ttl":
        raise AssertionError("canonical semantic source drift")


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


def positive_and_negative_shacl(data: Graph, shapes: Graph) -> None:
    conforms, report = shacl_conforms(data, shapes)
    if not conforms:
        raise AssertionError(f"canonical root fixture must conform:\n{report}")

    work = next(data.subjects(RDF.type, ES.WorkOrder))
    generated = next(data.subjects(RDF.type, ES.GeneratedArtifact))

    mutations = [
        (work, ES.authorityCeiling, ES.DO, "DO authority ceiling"),
        (work, ES.projectionAuthority, ES.DO, "work projection authority"),
        (work, ES.graphDigest, URIRef("https://example.org/not-a-literal"), "graph digest type/shape"),
        (generated, ES.projectionAuthority, ES.DO, "generated artifact authority"),
    ]

    for subject, predicate, bad_value, label in mutations:
        candidate = copy_graph(data)
        candidate.set((subject, predicate, bad_value))
        conforms, _ = shacl_conforms(candidate, shapes)
        if conforms:
            raise AssertionError(f"SHACL falsifier did not fail closed: {label}")


def json_contract() -> None:
    schema = json.loads(SCHEMA.read_text())
    envelope = json.loads(ENVELOPE.read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    validator.validate(envelope)

    mutations = [
        ("authority_ceiling", "DO"),
        ("projection_authority", "COMMAND_BUS"),
        ("graph_digest", "not-a-digest"),
        ("base_sha", "deadbeef"),
    ]
    for key, bad_value in mutations:
        candidate = copy.deepcopy(envelope)
        candidate[key] = bad_value
        try:
            validator.validate(candidate)
        except ValidationError:
            continue
        raise AssertionError(f"JSON falsifier did not fail closed: {key}={bad_value!r}")


def compatibility_contract(parsed: dict[Path, Graph]) -> None:
    aps_path = SEMANTIC / "compat" / "aps-v26.9.17.ttl"
    aps_text = aps_path.read_text()
    if "owl:equivalent" in aps_text:
        raise AssertionError("APS compatibility may not manufacture OWL equivalence")

    root_iri = URIRef("https://w3id.org/chatman/engineering-standards")
    for rel in ["profiles/sjira.ttl", "profiles/sa2a.ttl", "profiles/manufacturing.ttl", "profiles/documentation.ttl"]:
        graph = parsed[SEMANTIC / rel]
        profiles = list(graph.subjects(PROF.isProfileOf, root_iri))
        if not profiles:
            raise AssertionError(f"{rel} is not explicitly a profile of the root")


def main() -> None:
    parsed = parse_all_turtle()
    root_contract(parsed[ROOT_ONTOLOGY])
    manifest_contract()
    positive_and_negative_shacl(parsed[DATA], parsed[SHAPES])
    json_contract()
    compatibility_contract(parsed)

    print(f"turtle-graphs: {len(parsed)} parsed")
    print("root-direction: PASS (public standards -> engineering-standards -> downstream profiles)")
    print("shacl: PASS (positive fixture + 4 negative falsifiers)")
    print("json-schema: PASS (positive envelope + 4 negative falsifiers)")
    print("compatibility: PASS (no APS equivalence; downstream profiles bind root)")
    print("standing: ALIVE(repository-semantic-conformance)")
    print("non-claims: runtime SA2A, Jira mutation, CommandBus DO, deployment, publication, cross-repository standing")


if __name__ == "__main__":
    main()
