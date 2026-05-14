#!/usr/bin/env python3
"""Lightweight checks for this learning repository."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "LEARNING_PLAN.md",
    "SOURCE_MAP.md",
    "ROADMAP_A2A.md",
    "RULES.md",
    "AGENTS.md",
    "templates/session-log.md",
]


def main() -> int:
    ok = True
    print("Learning repo:", ROOT)
    for rel in REQUIRED:
        path = ROOT / rel
        if path.exists():
            print(f"OK   {rel}")
        else:
            print(f"MISS {rel}")
            ok = False

    hermes_src = os.environ.get("HERMES_SRC")
    if hermes_src:
        p = Path(hermes_src).expanduser()
        if p.exists():
            print(f"OK   HERMES_SRC={p}")
        else:
            print(f"WARN HERMES_SRC set but path does not exist: {p}")
    else:
        print("WARN HERMES_SRC is not set. Set it to your local hermes-agent clone for source reading.")

    try:
        result = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True, check=False)
        if result.returncode == 0:
            print("OK   git repository detected")
        else:
            print("WARN git status failed")
    except FileNotFoundError:
        print("WARN git not found")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
