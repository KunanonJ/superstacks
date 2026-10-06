#!/usr/bin/env python3
"""Find repeated correction-like phrases in local transcript files. Stdlib only.

Prints a report to stdout. Never writes files or files tracker issues.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

CORRECTION = re.compile(
    r"(?i)\b(no[,.]|don't|do not|stop|use .+ instead|not that|wrong|never)\b"
)
TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
SKIP_PARTS = {".git", "node_modules", ".venv", "dist"}
TEXT_SUFFIXES = {".txt", ".md", ".jsonl", ".json", ".log"}


def _iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.suffix == "":
            files.append(path)
    return files


def _normalize(line: str) -> str:
    words = TOKEN.findall(line.lower())
    return " ".join(words[:12])


def mine(paths: list[Path], min_count: int) -> list[tuple[int, str]]:
    counts: Counter[str] = Counter()
    for root in paths:
        for file_path in _iter_files(root):
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for raw in text.splitlines():
                line = raw.strip()
                if len(line) < 8 or not CORRECTION.search(line):
                    continue
                key = _normalize(line)
                if len(key) < 8:
                    continue
                counts[key] += 1
    ranked = [(n, phrase) for phrase, n in counts.most_common() if n >= min_count]
    return ranked


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Transcript file or directory. Repeatable. Only paths the user named.",
    )
    parser.add_argument("--min-count", type=int, default=2)
    args = parser.parse_args(argv)
    roots = [Path(p) for p in args.path]
    missing = [p for p in roots if not p.exists()]
    if missing:
        print("steer-miner FAIL: path not found:", file=sys.stderr)
        for path in missing:
            print(f"- {path}", file=sys.stderr)
        return 2
    ranked = mine(roots, args.min_count)
    print("steer-miner report (stdout only; no files written)")
    if not ranked:
        print("no repeated correction phrases at this min-count")
        return 0
    for count, phrase in ranked[:50]:
        print(f"{count}\t{phrase}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
