#!/usr/bin/env python3
"""Decide whether the plugin version on main still needs a release.

Reads the existing tag names from stdin (one per line) and prints one line:
`RELEASE v1.2.3` or `SKIP v1.2.3 already tagged`. No network, standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "plugins" / "superstacks" / ".claude-plugin" / "plugin.json"
VERSION_RE = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


def plan(version: str, tags: list[str]) -> str:
    if not VERSION_RE.fullmatch(version):
        raise ValueError(f"{version!r} is not a MAJOR.MINOR.PATCH version")
    tag = f"v{version}"
    if tag in {t.strip() for t in tags}:
        return f"SKIP {tag} already tagged"
    return f"RELEASE {tag}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="Version to plan (default: the plugin manifest version)")
    args = parser.parse_args(argv)
    version = args.version
    if version is None:
        version = json.loads(MANIFEST.read_text(encoding="utf-8"))["version"]
    tags = sys.stdin.read().splitlines()
    try:
        print(plan(version, tags))
    except ValueError as exc:
        print(f"release_plan: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
