#!/usr/bin/env python3
"""Validate a decision ledger (DECISIONS.md). One line per problem; exit 0 or 1."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

FIELDS = (
    "Question and options",
    "Owner's words",
    "Selects",
    "Does not cover",
    "Where recorded",
)
HEADING_RE = re.compile(r"^###\s+(\S+)\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^-\s+([^:]+):\s*(.*)$")
RULE_HEADERS = ("rule", "scope", "exceptions", "date", "source")


def _valid_date(text: str) -> bool:
    try:
        date.fromisoformat(text)
    except ValueError:
        return False
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", text))


def parse(text: str) -> tuple[list[dict], list[list[str]]]:
    """Return (log entries, standing-rule rows)."""
    entries: list[dict] = []
    rules: list[list[str]] = []
    section = ""
    current: dict | None = None
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("## "):
            section = stripped[3:].strip().lower()
            current = None
            continue
        if section == "standing rules" and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if [c.lower() for c in cells] == list(RULE_HEADERS):
                continue
            if all(set(c) <= set("-: ") for c in cells):
                continue
            rules.append(cells)
        elif section == "decision log":
            match = HEADING_RE.match(stripped)
            if match:
                current = {"date": match.group(1), "title": match.group(2), "fields": {}}
                entries.append(current)
                continue
            field = FIELD_RE.match(stripped)
            if field and current is not None:
                current["fields"][field.group(1).strip()] = field.group(2).strip()
    return entries, rules


def check(text: str) -> list[str]:
    errors: list[str] = []
    entries, rules = parse(text)
    headings = set()
    for entry in entries:
        name = f"{entry['date']} {entry['title']}"
        headings.add(name)
        if not _valid_date(entry["date"]):
            errors.append(f"{name}: date must be ISO YYYY-MM-DD")
        for field in FIELDS:
            if not entry["fields"].get(field):
                errors.append(f"{name}: missing or empty field '{field}'")
        words = entry["fields"].get("Owner's words", "")
        if words and not re.fullmatch(r"[\"“].*\S.*[\"”]", words):
            errors.append(f"{name}: Owner's words must be quoted")
        elif words and not words.strip("\"“”").strip():
            errors.append(f"{name}: Owner's words must not be empty")
    for cells in rules:
        label = cells[0] if cells else "(empty rule)"
        if len(cells) != len(RULE_HEADERS):
            errors.append(f"standing rule '{label}': expected {len(RULE_HEADERS)} columns")
            continue
        if not _valid_date(cells[3]):
            errors.append(f"standing rule '{label}': date must be ISO YYYY-MM-DD")
        source = cells[4].strip("`")
        if source not in headings:
            errors.append(f"standing rule '{label}': source must name a decision log entry")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: check_decisions.py LEDGER.md", file=sys.stderr)
        return 2
    path = Path(args[0])
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{path}: cannot read ({exc})")
        return 1
    errors = check(text)
    for item in errors:
        print(item)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
