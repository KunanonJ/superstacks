#!/usr/bin/env python3
"""Check an intake ticket brief for required headings. Stdlib only."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = ("Goal", "Scope", "Acceptance", "Verify", "Forbidden", "Door")
HEADING = re.compile(r"(?im)^#{1,3}\s+(Goal|Scope|Acceptance|Verify|Forbidden|Door)\b")
DOOR_VALUE = re.compile(r"(?im)\b(one-way|two-way)\b")
NEXT_HEADING = re.compile(r"(?m)^#{1,3}\s+\S")


def _bodies(text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    matches = list(HEADING.finditer(text))
    for index, match in enumerate(matches):
        name = match.group(1).title()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end].strip()
        found[name] = body
    return found


def check(text: str) -> list[str]:
    errors: list[str] = []
    bodies = _bodies(text)
    for name in REQUIRED:
        if name not in bodies:
            errors.append(f"missing ## {name} section")
        elif not bodies[name]:
            errors.append(f"## {name} section is empty")
    door = bodies.get("Door", "")
    if door and not DOOR_VALUE.search(door):
        errors.append("## Door must contain one-way or two-way")
    verify = bodies.get("Verify", "")
    if verify and "<exact command>" in verify:
        errors.append("## Verify still has the template placeholder")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Brief markdown file")
    args = parser.parse_args(argv)
    text = Path(args.path).read_text(encoding="utf-8")
    errors = check(text)
    if errors:
        print("brief check FAIL")
        for item in errors:
            print(f"- {item}")
        return 1
    print("brief check PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
