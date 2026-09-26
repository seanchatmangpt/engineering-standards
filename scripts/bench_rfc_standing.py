#!/usr/bin/env python3
"""Deterministic timing benchmark for scripts/check-rfc-standing.py.

Times the real court in-process over the real repository files:

- ``structural_court``: load + R25-007 sweep + RFC front matter + RFC-0003
  witness + all anti-vacuity mutants (the path CI runs on every PR);
- ``witness_replay``: the cross-repo replay against a real xaas git repository
  (only with ``--witness-repo``; it is dominated by ``git`` subprocesses).

Writes min / median / p95 / max in milliseconds to
``scripts/bench/rfc-standing.bench.json`` with ``--write``. The committed
``regression_bound_ms`` is enforced by scripts/tests/test_rfc_standing.py.

Usage: python scripts/bench_rfc_standing.py [--iterations N] [--witness-repo PATH] [--write]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scripts" / "bench" / "rfc-standing.bench.json"

spec = importlib.util.spec_from_file_location("rfc_standing", ROOT / "scripts" / "check-rfc-standing.py")
court = importlib.util.module_from_spec(spec)
spec.loader.exec_module(court)


def summarize(samples: list[float]) -> dict:
    ordered = sorted(samples)
    p95 = ordered[min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1))))]
    return {
        "n": len(samples),
        "min": round(ordered[0], 3),
        "median": round(statistics.median(ordered), 3),
        "p95": round(p95, 3),
        "max": round(ordered[-1], 3),
    }


def time_it(fn, iterations: int) -> list[float]:
    fn()  # warm the import and file caches once; not recorded
    samples = []
    for _ in range(iterations):
        started = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - started) * 1000)
    return samples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=200)
    parser.add_argument("--witness-repo", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    def structural():
        result = court.run_court(ROOT)
        assert not result["errors"] and not result["survivors"], result

    results = {"structural_court": summarize(time_it(structural, args.iterations))}
    texts, witness = court.load(ROOT)
    results["mutants_per_run"] = len(court.mutants(witness))

    if args.witness_repo:
        def replay():
            assert court.witness_replay_errors(args.witness_repo, witness) == []
        results["witness_replay"] = summarize(time_it(replay, max(5, args.iterations // 10)))

    previous = json.loads(OUT.read_text()) if OUT.exists() else {}
    report = {
        "schema": "engineering-standards.bench-receipt.v26.9.26",
        "subject": "scripts/check-rfc-standing.py",
        "unit": "ms",
        "results": results,
        "regression_bound_ms": previous.get("regression_bound_ms", {"structural_court_median": 250}),
        "host": {"python": platform.python_version(), "machine": platform.machine(),
                 "system": platform.system()},
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "authority": "NONE",
    }
    print(json.dumps(report, indent=2))
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
