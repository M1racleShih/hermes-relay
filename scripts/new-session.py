#!/usr/bin/env python3
"""Create a timestamped learning session log from template."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "session-log.md"
JOURNAL = ROOT / "journal"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "session"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("title", help="Session title")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(args.title)
    out = JOURNAL / f"{today}-{slug}.md"
    if out.exists():
        raise SystemExit(f"Refusing to overwrite existing log: {out}")

    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("{{title}}", args.title).replace("{{date}}", today)
    out.write_text(text, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
