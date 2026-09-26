"""Chicago-style tests for scripts/check-rfc-standing.py.

Every test runs the real court as a subprocess against real files: a temporary
copy of the documents it reads, mutated on disk where a test needs a defect.
Witness-replay tests run against a real xaas git repository located through
``ES_XAAS_REPO`` (or a sibling ``../xaas`` checkout) and are skipped by name when
none is present, which is the case on a GitHub runner.

Run: python -m unittest discover -s scripts/tests -v
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURT = ROOT / "scripts" / "check-rfc-standing.py"
BENCH = ROOT / "scripts" / "bench" / "rfc-standing.bench.json"

spec = importlib.util.spec_from_file_location("rfc_standing", COURT)
court = importlib.util.module_from_spec(spec)
spec.loader.exec_module(court)

RFC0003 = court.RFC0003
WITNESS = court.WITNESS


def xaas_repo() -> Path | None:
    for candidate in (os.environ.get("ES_XAAS_REPO"), str(ROOT.parent / "xaas")):
        if candidate and (Path(candidate) / ".git").exists():
            return Path(candidate)
    return None


XAAS = xaas_repo()
NO_XAAS = "no xaas git repository (set ES_XAAS_REPO) — cross-repo witness replay not run"


class CourtCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="rfc-standing-"))
        for rel in set(court.SWEEP) | set(court.RFC_FRONT) | {WITNESS, court.RFC0005_REGISTRY}:
            dest = self.tmp / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, dest)
        for rfc in sorted((ROOT / court.RFC_DIR).glob("*.md")):
            dest = self.tmp / court.RFC_DIR / rfc.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(rfc, dest)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_court(self, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(COURT), "--root", str(self.tmp), *extra],
            capture_output=True, text=True,
        )

    def edit(self, rel: str, old: str, new: str) -> None:
        path = self.tmp / rel
        text = path.read_text()
        self.assertIn(old, text, f"test anchor missing in {rel}")
        path.write_text(text.replace(old, new, 1))

    def assert_refused(self, needle: str, *extra: str) -> None:
        result = self.run_court(*extra)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(needle, result.stderr)
        self.assertIn("standing: REFUSED", result.stdout)


class StructuralCourt(CourtCase):
    def test_admitted_tree_is_alive_and_every_mutant_refused(self):
        result = self.run_court()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("structural: PASS (0 refusals)", result.stdout)
        self.assertIn("anti-vacuity: 19/19 mutants refused", result.stdout)
        self.assertIn("witness-replay: NOT_RUN", result.stdout)

    def test_receipt_records_standing_and_mutant_counts(self):
        receipt = self.tmp / "out" / "receipt.json"
        result = self.run_court("--receipt", str(receipt))
        self.assertEqual(result.returncode, 0, result.stderr)
        body = json.loads(receipt.read_text())
        self.assertEqual(body["standing"], "ALIVE")
        self.assertEqual(body["authority"], "NONE")
        self.assertEqual((body["mutants_total"], body["mutants_refused"]), (19, 19))
        self.assertEqual(body["refusals"], [])

    def test_head_tree_declares_unique_rfc_ids(self):
        # RFC-0005 belongs to the autonomous-loop qualification alone; the
        # v26.9.25 autonomic-closure amendment is RFC-0006 (renumbered
        # 2026-09-26 after the double-booking was caught).
        result = self.run_court()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("RFC id collision", result.stderr)

    def test_duplicate_rfc_id_refused(self):
        # The historical defect: a second document re-declaring RFC-0005.
        self.edit(court.RFC0006_AMENDMENT,
                  "# RFC-0006: v26.9.25 Autonomic Closure Amendment",
                  "# RFC-0005: v26.9.25 Autonomic Closure Amendment")
        self.assert_refused("RFC id collision: RFC-0005")

    def test_rfc_id_gate_ignores_files_without_declared_id(self):
        # A working note in the rfc/ directory declares no RFC-NNNN title and
        # must not crash (or be mis-parsed into) the id-uniqueness court.
        (self.tmp / court.RFC_DIR / "9000-working-note.md").write_text(
            "# A working note\n\nNo RFC id declared here.\n")
        self.assertEqual(self.run_court().returncode, 0)

    def test_missing_status_header_refused(self):
        self.edit("process/standards-change-control.md",
                  "**Status:** FINAL — in force (R25-007 disposition, v26.9.25 sweep)\n", "")
        self.assert_refused("R25-007 status header missing")

    def test_duplicate_status_header_refused(self):
        self.edit("process/documentation-standards.md", "## Philosophy",
                  "**Status:** FINAL — in force (R25-007)\n\n## Philosophy")
        self.assert_refused("duplicate **Status:** header")

    def test_status_header_reordered_after_first_section_refused(self):
        rel = "docs/engineering/root-architecture.md"
        self.edit(rel, "**Status:** FINAL — in force (R25-007 disposition, v26.9.25 sweep)\n\n", "")
        self.edit(rel, "## Purpose\n",
                  "## Purpose\n\n**Status:** FINAL — in force (R25-007 disposition, v26.9.25 sweep)\n")
        self.assert_refused("is after the first section")

    def test_final_on_self_declared_draft_refused(self):
        self.edit("code/database-standards.md", "**Status:** PROPOSED", "**Status:** FINAL (R25-007)")
        self.assert_refused("FINAL contradicts the document's own draft footer")

    def test_proposed_without_draft_footer_refused(self):
        rel = "code/web-application-standards.md"
        path = self.tmp / rel
        path.write_text(path.read_text().replace("in active development", "in force"))
        self.assert_refused("no draft footer exists")

    def test_rfc_authority_do_refused(self):
        self.edit(RFC0003, "**Authority:** NONE", "**Authority:** DO")
        self.assert_refused("Authority must be NONE")

    def test_rfc_0004_verbatim_body_status_is_not_front_matter(self):
        # The operator RFC carried verbatim in RFC-0004 has its own
        # "**Status:** Proposed" under a second title; only the front matter binds.
        text = (self.tmp / court.RFC_FRONT[2]).read_text()
        self.assertIn("**Status:** Proposed for v26.9.25", text)
        self.assertEqual(self.run_court().returncode, 0)

    def test_stale_subject_refused(self):
        self.edit(RFC0003, "xaas@c10cdab95b927ed82c5c212a3f36d02b52ed525e",
                  "xaas@0a5acd1fb3d9b5aeed26e87719cf8187429dfc69")
        self.assert_refused("stale or unwitnessed subject")

    def test_pr_original_subject_binding_refused(self):
        # The PR head bound the cs: vocabulary to the ledger's evidence subject,
        # a tree that does not contain it; the receipt subject went uncited.
        text = (self.tmp / RFC0003).read_text()
        text = text.replace("c10cdab95b927ed82c5c212a3f36d02b52ed525e",
                            "f9670f446537ddb882edf9cd7e0b6519de557e60")
        (self.tmp / RFC0003).write_text(text)
        self.assert_refused("witnessed vocabulary_subject")

    def test_wrong_digest_refused(self):
        self.edit(RFC0003, "d32afca859a3b633584532c40be44a46a5343c68516fc292f508862a538f6d40",
                  "d32afca859a3b633584532c40be44a46a5343c68516fc292f508862a538f6d41")
        self.assert_refused("is not a witnessed digest")

    def test_truncated_digest_refused(self):
        self.edit(RFC0003, "6bd9762edbdf7c8f2a267106343601c60eef8c5cf32f52e183b963cc6453806f",
                  "6bd9762edbdf7c8f2a267106343601c60eef8c5cf32f52e183b963cc")
        self.assert_refused("malformed digest")

    def test_zoela_reclaimed_refused(self):
        self.edit(RFC0003, "case-study element is reclassified **NOT_CLAIMED**",
                  "case-study element is applied")
        self.assert_refused("re-claims the zoela element")

    def test_falsifier_removed_refused(self):
        path = self.tmp / RFC0003
        path.write_text(path.read_text().replace("F-CS1", "F-CSX"))
        self.assert_refused("F-CS1")

    def test_ledger_count_across_line_wrap_is_checked(self):
        # The count is wrapped across a line break in the RFC; a regex that
        # only matched on one line would let this drift through.
        text = (self.tmp / RFC0003).read_text()
        self.assertNotIn("268-line WD claims ledger", text)
        self.edit(RFC0003, "268-line WD claims", "269-line WD claims")
        self.assert_refused("ledger claimed 269 lines")


@unittest.skipIf(XAAS is None, NO_XAAS)
class WitnessReplay(CourtCase):
    def rewrite_witness(self, mutate) -> None:
        path = self.tmp / WITNESS
        body = json.loads(path.read_text())
        mutate(body)
        path.write_text(json.dumps(body, indent=2))

    def test_real_xaas_replay_passes(self):
        result = self.run_court("--witness-repo", str(XAAS))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("witness-replay: PASS", result.stdout)

    def test_replay_refuses_vocabulary_at_ledger_subject(self):
        # Replay of the PR head's original claim: the vocabulary files do not
        # exist at the ledger's evidence subject.
        ledger = "f9670f446537ddb882edf9cd7e0b6519de557e60"

        def mutate(body):
            body["subjects"]["vocabulary_subject"] = ledger
            body["receipt"]["subject_sha"] = ledger

        self.rewrite_witness(mutate)
        text = (self.tmp / RFC0003).read_text().replace(
            "c10cdab95b927ed82c5c212a3f36d02b52ed525e", ledger)
        (self.tmp / RFC0003).write_text(text)
        result = self.run_court("--witness-repo", str(XAAS))
        self.assertEqual(result.returncode, 1)
        self.assertIn("is absent, witness", result.stderr)
        self.assertIn("receipt subject_sha", result.stderr)

    def test_replay_refuses_wrong_blob(self):
        path = "priv/packs/wd_cs2_pack/claims.ttl"
        self.rewrite_witness(lambda b: b["vocabulary_files"].__setitem__(path, "0" * 40))
        result = self.run_court("--witness-repo", str(XAAS))
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"replay: {path}", result.stderr)

    def test_replay_refuses_receipt_digest_mismatch(self):
        # Both the RFC and the witness agree on a digest the real receipt does not carry.
        real = "d32afca859a3b633584532c40be44a46a5343c68516fc292f508862a538f6d40"
        fake = "e" * 64
        self.rewrite_witness(lambda b: b["receipt"].__setitem__("receipt_sha256", fake))
        text = (self.tmp / RFC0003).read_text().replace(real, fake)
        (self.tmp / RFC0003).write_text(text)
        result = self.run_court("--witness-repo", str(XAAS))
        self.assertEqual(result.returncode, 1)
        self.assertIn("receipt receipt_sha256", result.stderr)

    def test_replay_refuses_unknown_subject(self):
        self.rewrite_witness(
            lambda b: b["subjects"].__setitem__("receipt_commit", "1" * 40))
        text = (self.tmp / RFC0003).read_text().replace(
            "6a63d891ea5ce046d23c1e00cc78a2f070aca617", "1" * 40)
        (self.tmp / RFC0003).write_text(text)
        result = self.run_court("--witness-repo", str(XAAS))
        self.assertEqual(result.returncode, 1)
        self.assertIn("is not a commit", result.stderr)


class Benchmark(unittest.TestCase):
    def test_structural_court_within_committed_regression_bound(self):
        bound = json.loads(BENCH.read_text())["regression_bound_ms"]["structural_court_median"]
        samples = []
        for _ in range(30):
            started = time.perf_counter()
            result = court.run_court(ROOT)
            samples.append((time.perf_counter() - started) * 1000)
            self.assertEqual(result["errors"], [])
            self.assertEqual(result["survivors"], [])
        self.assertLessEqual(statistics.median(samples), bound,
                             f"median {statistics.median(samples):.2f} ms > bound {bound} ms")


if __name__ == "__main__":
    unittest.main()
