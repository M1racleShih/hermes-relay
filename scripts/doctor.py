#!/usr/bin/env python3
"""Lightweight checks for this learning repository."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HERMES_SRC = ROOT.parent / "hermes-agent"
REQUIRED = [
    "LEARNING_PLAN.md",
    "SOURCE_MAP.md",
    "ROADMAP_A2A.md",
    "RULES.md",
    "AGENTS.md",
    "templates/session-log.md",
]
FORMAL_DOCS = [
    ".hermes.md",
    "README.md",
    "LEARNING_PLAN.md",
    "RULES.md",
    "AGENTS.md",
    "notes/INDEX.md",
    "templates/session-log.md",
    "templates/source-reading-note.md",
]


def _resolve_note_ref(ref: str) -> Path | None:
    candidates = []
    if "/" in ref:
        candidates.append(ROOT / ref)
    else:
        candidates.extend(
            [
                ROOT / ref,
                ROOT / "notes" / ref,
                ROOT / "notes" / "source" / ref,
                ROOT / "notes" / "design" / ref,
                ROOT / "templates" / ref,
            ]
        )

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def check_note_index() -> bool:
    index = ROOT / "notes" / "INDEX.md"
    if not index.exists():
        print("MISS notes/INDEX.md")
        return False

    ok = True
    text = index.read_text(encoding="utf-8")
    refs = sorted(set(re.findall(r"`([^`]+\.md)`", text)))
    for ref in refs:
        if _resolve_note_ref(ref):
            print(f"OK   notes index ref {ref}")
        else:
            print(f"MISS notes index ref {ref}")
            ok = False
    return ok


def check_language_consistency() -> bool:
    ok = True
    banned = ["无人值守"]
    for rel in FORMAL_DOCS:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for term in banned:
            if term in text:
                print(f"WARN stale term {term!r} in {rel}")
                ok = False
    if ok:
        print("OK   formal docs use agent 自学 terminology")
    return ok


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
    elif DEFAULT_HERMES_SRC.exists():
        print("OK   HERMES_SRC fallback=../hermes-agent")
    else:
        print("WARN HERMES_SRC is not set. Set it to your local hermes-agent clone for source reading.")

    ok = check_note_index() and ok
    ok = check_language_consistency() and ok

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
