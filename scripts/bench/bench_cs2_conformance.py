#!/usr/bin/env python3
"""Synthetic scale harness for RFC-CS2-001 conformance.

Maximum Code Mode writes this harness but does not execute it.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "check-cs2-conformance.py"

spec = importlib.util.spec_from_file_location("check_cs2_conformance", MODULE_PATH)
cs2 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(cs2)


def make_bundle(index: int, claim_count: int, level: str) -> dict:
    subject_id = f"repo:bench/service-{index}"
    source_id = f"src:{index}"
    evidence_id = f"ev:{index}"

    claims = []
    for claim_index in range(claim_count):
        claims.append(
            {
                "id": f"claim:{index}:{claim_index}",
                "predicate": "synthetic_metric",
                "object": claim_index,
                "source_refs": [source_id],
                "evidence_refs": [evidence_id],
                "standing": "DERIVED",
                "falsifier": {
                    "observation": "A deterministic regeneration produces a different value."
                },
                "contradicts": [],
            }
        )

    bundle = {
        "schema_version": "cs2.conformance.v1",
        "standard": "RFC-CS2-001",
        "subject": {
            "id": subject_id,
            "kind": "Repository",
            "revision": f"{index:040x}"[-40:],
        },
        "sources": [
            {
                "id": source_id,
                "kind": "Synthetic",
                "locator": f"bench://source/{index}",
            }
        ],
        "evidence": [
            {
                "id": evidence_id,
                "kind": "SyntheticObservation",
                "subject_ref": subject_id,
                "source_ref": source_id,
                "locator": f"bench://evidence/{index}",
                "value": index,
            }
        ],
        "claims": claims,
        "conformance": {"requested_level": level},
    }

    if cs2.LEVEL_RANK[level] >= cs2.LEVEL_RANK["C3"]:
        bundle["route"] = {
            "consumer": "bench-consumer",
            "workflow": "bench-workflow",
            "projection_id": "bench-v1",
            "minimum_level": "C3",
            "delivery_semantics": "SNAPSHOT",
            "projection_authority": "NONE",
        }

    if cs2.LEVEL_RANK[level] >= cs2.LEVEL_RANK["C4"]:
        bundle["process"] = {
            "ocel_ref": f"bench://ocel/{index}",
            "receipt_schema": "semantic/schemas/evidence-receipt.schema.json",
            "replay_binding": f"bench://replay/{index}",
            "episode_id": f"episode:{index}",
            "event_refs": [f"event:{index}:1"],
            "consequence_class": "NONE",
        }

    return bundle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundles", type=int, default=10_000)
    parser.add_argument("--claims", type=int, default=8)
    parser.add_argument("--level", choices=cs2.LEVELS, default="C4")
    args = parser.parse_args()

    started = time.perf_counter()
    conforming = 0
    fingerprint_xor = 0

    for index in range(args.bundles):
        result = cs2.validate(make_bundle(index, args.claims, args.level))
        conforming += int(result.conforms)
        fingerprint_xor ^= int(result.semantic_fingerprint[-16:], 16)

    elapsed = time.perf_counter() - started
    output = {
        "bundles": args.bundles,
        "claims_per_bundle": args.claims,
        "requested_level": args.level,
        "conforming": conforming,
        "elapsed_seconds": elapsed,
        "bundles_per_second": args.bundles / elapsed if elapsed else None,
        "claims_per_second": (args.bundles * args.claims) / elapsed if elapsed else None,
        "fingerprint_xor": f"{fingerprint_xor:016x}",
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
