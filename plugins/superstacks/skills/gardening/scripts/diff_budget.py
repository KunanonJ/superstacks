#!/usr/bin/env python3
"""Fail if the working tree diff exceeds a small gardening budget. Stdlib only."""

from __future__ import annotations

import argparse
import subprocess
import sys


def _diff_numstat(base: str) -> list[tuple[int, int, str]]:
    proc = subprocess.run(
        ["git", "diff", "--numstat", f"{base}...HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        proc = subprocess.run(
            ["git", "diff", "--numstat", base],
            check=False,
            capture_output=True,
            text=True,
        )
    if proc.returncode != 0:
        raise SystemExit(f"diff_budget FAIL: git diff failed\n{proc.stderr}")
    rows: list[tuple[int, int, str]] = []
    for line in proc.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, removed, path = parts
        if added == "-" or removed == "-":
            continue
        rows.append((int(added), int(removed), path))
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD")
    parser.add_argument("--max-lines", type=int, default=80)
    parser.add_argument("--max-files", type=int, default=6)
    args = parser.parse_args(argv)
    try:
        rows = _diff_numstat(args.base)
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2
    files = len(rows)
    lines = sum(added + removed for added, removed, _path in rows)
    print(f"gardening files: {files}")
    print(f"gardening lines: {lines}")
    print(f"gardening budget: {args.max_files} files / {args.max_lines} lines")
    if files > args.max_files or lines > args.max_lines:
        print("gardening FAIL: diff budget exceeded")
        for added, removed, path in rows:
            print(f"- {path}: +{added} -{removed}")
        return 1
    print("gardening PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
