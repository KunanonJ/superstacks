#!/usr/bin/env python3
"""Print the standing rule that grants an authority, or 'DEFAULT: human'."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_decisions import parse  # noqa: E402

AUTHORITIES = ("merge", "ready", "close", "force-push", "deploy")
DEFAULT = "DEFAULT: human"


def lookup(text: str, authority: str) -> str:
    """Latest sourced rule whose text starts with '<authority>:'; else DEFAULT."""
    entries, rules = parse(text)
    headings = {f"{e['date']} {e['title']}" for e in entries}
    best: tuple[str, list[str]] | None = None
    for cells in rules:
        if len(cells) != 5:
            continue
        rule, _scope, _exc, when, source = cells
        if not rule.lower().startswith(authority + ":"):
            continue
        if source.strip("`") not in headings:
            continue
        if best is None or when >= best[0]:
            best = (when, cells)
    if best is None:
        return DEFAULT
    rule, scope, exc, when, source = best[1]
    return f"{rule} | scope: {scope} | exceptions: {exc} | date: {when} | source: {source}"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2 or args[1] not in AUTHORITIES:
        print(f"usage: authority.py LEDGER.md {{{'|'.join(AUTHORITIES)}}}", file=sys.stderr)
        return 2
    try:
        text = Path(args[0]).read_text(encoding="utf-8")
    except OSError:
        print(DEFAULT)
        return 0
    print(lookup(text, args[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
