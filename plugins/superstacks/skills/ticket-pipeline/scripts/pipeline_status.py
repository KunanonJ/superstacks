#!/usr/bin/env python3
"""Report which ticket-pipeline steps have evidence in a PR body. Stdlib only."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

STEPS: list[tuple[str, re.Pattern[str]]] = [
    ("how", re.compile(r"(?im)^#{1,3}\s+How\b")),
    ("writing-plans", re.compile(r"(?im)^#{1,3}\s+Plan\b")),
    ("verify-loop", re.compile(r"VERIFY_(?:PASS|FAIL)")),
    ("test-driven-development", re.compile(r"(?im)^#{1,3}\s+TDD\b|\bred-green\b")),
    ("verification-before-completion", re.compile(r"(?im)^#{1,3}\s+Evidence\b")),
    ("code-review", re.compile(r"(?im)^#{1,3}\s+Code review\b")),
    (
        "interrogate",
        re.compile(r"(?im)^#{1,3}\s+Interrogate\b|N/A \(two-way door\)"),
    ),
    ("pr", re.compile(r"(?i)\bRefs\s+#\d+")),
]


def evaluate(text: str) -> list[tuple[str, bool]]:
    return [(name, bool(pattern.search(text))) for name, pattern in STEPS]


def render(rows: list[tuple[str, bool]]) -> str:
    lines = ["Pipeline status"]
    missing = 0
    for name, present in rows:
        mark = "PRESENT" if present else "MISSING"
        if not present:
            missing += 1
        lines.append(f"- {name}: {mark}")
    lines.append(f"missing: {missing}/{len(rows)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr-body", required=True, help="Path to the PR body markdown")
    args = parser.parse_args(argv)
    text = Path(args.pr_body).read_text(encoding="utf-8")
    rows = evaluate(text)
    print(render(rows))
    return 0 if all(present for _name, present in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
