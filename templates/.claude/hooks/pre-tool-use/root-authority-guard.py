#!/usr/bin/env python3
"""Deterministic local guard for the Engineering Standards authority boundary.

This hook is a refusal guard, not an authority broker. It blocks a small set of
known external/destructive DO-shaped shell commands and direct writes into
obvious generated projection directories. A passing hook does not grant DO.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

DO_PATTERNS = [
    (re.compile(r"(^|[;&|]\s*)git\s+push\b"), "REFUSED:EXTERNAL_GIT_PUSH_REQUIRES_AUTHORITY"),
    (re.compile(r"(^|[;&|]\s*)git\s+merge\b"), "REFUSED:MERGE_REQUIRES_AUTHORITY"),
    (re.compile(r"(^|[;&|]\s*)gh\s+pr\s+merge\b"), "REFUSED:PR_MERGE_REQUIRES_AUTHORITY"),
    (re.compile(r"(^|[;&|]\s*)kubectl\s+(apply|delete)\b"), "REFUSED:CLUSTER_DO_REQUIRES_AUTHORITY"),
    (re.compile(r"(^|[;&|]\s*)terraform\s+apply\b"), "REFUSED:INFRASTRUCTURE_DO_REQUIRES_AUTHORITY"),
]

GENERATED_SEGMENTS = {".generated", "generated", "dist", "build"}


def refuse(code: str, detail: str) -> None:
    print(f"{code}: {detail}", file=sys.stderr)
    sys.exit(2)


def write_path(tool_input: dict) -> str:
    return str(tool_input.get("file_path") or tool_input.get("path") or "")


def main() -> None:
    tool = os.environ.get("TOOL_NAME", "")
    try:
        tool_input = json.loads(os.environ.get("TOOL_INPUT", "{}"))
    except json.JSONDecodeError:
        refuse("REFUSED:MALFORMED_TOOL_INPUT", "cannot admit malformed tool input")

    if tool == "Bash":
        command = str(tool_input.get("command", ""))
        for pattern, code in DO_PATTERNS:
            if pattern.search(command):
                refuse(code, "local hook cannot manufacture consequential authority")
        return

    if tool not in {"Write", "Edit", "MultiEdit"}:
        return

    path = write_path(tool_input)
    if not path:
        return

    parts = set(Path(path).parts)
    if parts & GENERATED_SEGMENTS:
        refuse(
            "REFUSED:GENERATED_PROJECTION_EDIT",
            f"{path} is under an obvious generated projection path; edit canonical source/generator instead",
        )


if __name__ == "__main__":
    main()
