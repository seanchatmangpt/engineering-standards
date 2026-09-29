from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "check-cs2-conformance.py"
FIXTURE = ROOT / "semantic" / "examples" / "cs2-conformance-c4.json"

spec = importlib.util.spec_from_file_location("check_cs2_conformance", MODULE_PATH)
cs2 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(cs2)


def fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class CS2ConformanceTests(unittest.TestCase):
    def test_c4_fixture_reaches_c4(self):
        result = cs2.validate(fixture())
        self.assertTrue(result.conforms)
        self.assertEqual("C4", result.actual_level)

    def test_fingerprint_is_deterministic_across_key_order(self):
        document = fixture()
        reversed_document = dict(reversed(list(document.items())))
        self.assertEqual(
            cs2.semantic_fingerprint(document),
            cs2.semantic_fingerprint(reversed_document),
        )

    def test_derived_conformance_output_does_not_change_fingerprint(self):
        document = fixture()
        first = cs2.semantic_fingerprint(document)
        document["conformance"]["actual_level"] = "C4"
        document["conformance"]["issues"] = [{"anything": True}]
        document["conformance"]["semantic_fingerprint"] = "junk"
        self.assertEqual(first, cs2.semantic_fingerprint(document))

    def test_missing_revision_breaks_c0(self):
        document = fixture()
        document["subject"]["revision"] = ""
        result = cs2.validate(document)
        self.assertEqual("NONE", result.actual_level)
        self.assertIn("REVISION_MISSING", {issue.code for issue in result.issues})

    def test_no_sources_caps_at_c0_for_c1_request(self):
        document = fixture()
        document["sources"] = []
        document["conformance"]["requested_level"] = "C1"
        result = cs2.validate(document)
        self.assertEqual("C0", result.actual_level)
        self.assertFalse(result.conforms)

    def test_evidence_must_bind_exact_subject(self):
        document = fixture()
        document["evidence"][0]["subject_ref"] = "repo:other/service"
        document["conformance"]["requested_level"] = "C1"
        result = cs2.validate(document)
        self.assertEqual("C0", result.actual_level)
        self.assertIn("BROKEN_REFERENCE", {issue.code for issue in result.issues})

    def test_broken_source_reference_is_typed(self):
        document = fixture()
        document["evidence"][0]["source_ref"] = "src:missing"
        document["conformance"]["requested_level"] = "C1"
        result = cs2.validate(document)
        self.assertIn("BROKEN_REFERENCE", {issue.code for issue in result.issues})

    def test_non_unknown_claim_requires_provenance(self):
        document = fixture()
        document["claims"][0]["source_refs"] = []
        document["claims"][0]["evidence_refs"] = []
        document["conformance"]["requested_level"] = "C1"
        result = cs2.validate(document)
        self.assertIn("PROVENANCE_MISSING", {issue.code for issue in result.issues})

    def test_falsifier_is_required_at_c2(self):
        document = fixture()
        document["claims"][0].pop("falsifier")
        document["conformance"]["requested_level"] = "C2"
        result = cs2.validate(document)
        self.assertEqual("C1", result.actual_level)
        self.assertIn("FALSIFIER_MISSING", {issue.code for issue in result.issues})

    def test_refuted_claim_does_not_require_new_falsifier(self):
        document = fixture()
        document["claims"][0]["standing"] = "REFUTED"
        document["claims"][0].pop("falsifier")
        document["conformance"]["requested_level"] = "C2"
        result = cs2.validate(document)
        self.assertEqual("C4", result.actual_level)
        self.assertTrue(result.conforms)

    def test_duplicate_id_across_namespaces_breaks_c2(self):
        document = fixture()
        document["evidence"][0]["id"] = document["sources"][0]["id"]
        document["claims"][0]["evidence_refs"] = [document["evidence"][0]["id"]]
        document["conformance"]["requested_level"] = "C2"
        result = cs2.validate(document)
        self.assertEqual("C1", result.actual_level)
        self.assertIn("DUPLICATE_ID", {issue.code for issue in result.issues})

    def test_route_authority_must_be_none(self):
        document = fixture()
        document["route"]["projection_authority"] = "ADMIN"
        document["conformance"]["requested_level"] = "C3"
        result = cs2.validate(document)
        self.assertEqual("C2", result.actual_level)
        self.assertIn(
            "PROJECTION_AUTHORITY_VIOLATION",
            {issue.code for issue in result.issues},
        )

    def test_route_minimum_cannot_exceed_requested_level(self):
        document = fixture()
        document["route"]["minimum_level"] = "C4"
        document["conformance"]["requested_level"] = "C3"
        result = cs2.validate(document)
        self.assertEqual("C2", result.actual_level)

    def test_c4_requires_process_event_reference(self):
        document = fixture()
        document["process"]["event_refs"] = []
        result = cs2.validate(document)
        self.assertEqual("C3", result.actual_level)
        self.assertIn(
            "PROCESS_BINDING_MISSING",
            {issue.code for issue in result.issues},
        )

    def test_consequential_process_requires_authority_requirement(self):
        document = fixture()
        document["process"].pop("authority_requirement")
        result = cs2.validate(document)
        self.assertEqual("C3", result.actual_level)

    def test_none_consequence_does_not_require_authority_requirement(self):
        document = fixture()
        document["process"]["consequence_class"] = "NONE"
        document["process"].pop("authority_requirement")
        result = cs2.validate(document)
        self.assertEqual("C4", result.actual_level)

    def test_unknown_claim_may_have_no_evidence_at_c1(self):
        document = fixture()
        document["claims"][0]["standing"] = "UNKNOWN"
        document["claims"][0]["source_refs"] = []
        document["claims"][0]["evidence_refs"] = []
        document["conformance"]["requested_level"] = "C1"
        result = cs2.validate(document)
        self.assertTrue(result.conforms)

    def test_unknown_contradiction_reference_breaks_c2(self):
        document = fixture()
        document["claims"][0]["contradicts"] = ["claim:missing"]
        document["conformance"]["requested_level"] = "C2"
        result = cs2.validate(document)
        self.assertIn("BROKEN_REFERENCE", {issue.code for issue in result.issues})

    def test_annotation_preserves_input_and_adds_derived_fields(self):
        document = fixture()
        original = copy.deepcopy(document)
        result = cs2.validate(document)
        annotated = cs2.annotate(document, result)
        self.assertEqual(original, document)
        self.assertEqual("C4", annotated["conformance"]["actual_level"])
        self.assertTrue(
            annotated["conformance"]["semantic_fingerprint"].startswith("sha256:")
        )


if __name__ == "__main__":
    unittest.main()
