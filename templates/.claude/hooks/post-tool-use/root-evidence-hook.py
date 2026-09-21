#!/usr/bin/env python3
"""Post-write reminder that construction is not verification or standing."""

from __future__ import annotations

import json
import os
import sys


def main() -> None:
    tool = os.environ.get("TOOL_NAME", "")
    if tool not in {"Write", "Edit", "MultiEdit"}:
        return
    try:
        tool_input = json.loads(os.environ.get("TOOL_INPUT", "{}"))
    except json.JSONDecodeError:
        return

    path = tool_input.get("file_path") or tool_input.get("path")
    if path:
        print(
            "CONSTRUCTED_NOT_VERIFIED: "
            f"{path}; run the narrowest repository-native court before promoting standing",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
