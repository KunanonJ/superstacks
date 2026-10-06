#!/usr/bin/env python3
"""Check a PR body for ticket refs, plan, evidence, and risk/door sections. Stdlib only."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING_PLAN = re.compile(r"(?im)^#{1,3}\s+Plan\b")
HEADING_EVIDENCE = re.compile(r"(?im)^#{1,3}\s+Evidence\b")
HEADING_RISK = re.compile(r"(?im)^#{1,3}\s+(Merge Danger|Risk)\b")
REFS = re.compile(r"(?i)\bRefs\s+#\d+")
FORBIDDEN_CLOSE = re.compile(r"(?i)\b(Closes|Fixes|Resolves)\s+#\d+")
DOOR = re.compile(r"(?im)(?:\*\*)?Door:(?:\*\*)?\s*(one-way|two-way)\b")
NEXT_HEADING = re.compile(r"(?m)^#{1,3}\s+\S")


def _section_body(text: str, heading: re.Pattern[str]) -> str | None:
    match = heading.search(text)
    if not match:
        return None
    rest = text[match.end() :]
    nxt = NEXT_HEADING.search(rest)
    body = rest[: nxt.start()] if nxt else rest
    return body.strip()


def check(text: str) -> list[str]:
    errors: list[str] = []
    if FORBIDDEN_CLOSE.search(text):
        errors.append("ticket links must be Refs #N; Closes/Fixes/Resolves are not allowed")
    if not REFS.search(text):
        errors.append("missing ticket ref (expected Refs #N)")
    plan = _section_body(text, HEADING_PLAN)
    if plan is None:
        errors.append("missing ## Plan section")
    elif not plan:
        errors.append("## Plan section is empty")
    evidence = _section_body(text, HEADING_EVIDENCE)
    if evidence is None:
        errors.append("missing ## Evidence section")
    elif not evidence:
        errors.append("## Evidence section is empty")
    elif "VERIFY_PASS" not in evidence and "VERIFY_FAIL" not in evidence:
        errors.append("## Evidence must include VERIFY_PASS or VERIFY_FAIL from the verify-loop runner")
    risk = _section_body(text, HEADING_RISK)
    if risk is None:
        errors.append("missing ## Merge Danger or ## Risk section")
    elif not risk:
        errors.append("risk/door section is empty")
    if not DOOR.search(text):
        errors.append("missing Door: one-way or Door: two-way")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        help="PR body file. Reads stdin when omitted.",
    )
    args = parser.parse_args(argv)
    if args.path:
        text = Path(args.path).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    errors = check(text)
    if errors:
        print("PR body check FAIL")
        for item in errors:
            print(f"- {item}")
        return 1
    print("PR body check PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
