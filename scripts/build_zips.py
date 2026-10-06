#!/usr/bin/env python3
"""Build per-skill ZIPs and one plugin ZIP into dist/ for GitHub Releases."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "superstacks"
DIST = ROOT / "dist"


def _zip_dir(zip_path: Path, source: Path, arc_root: str) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            rel = path.relative_to(source)
            zf.write(path, Path(arc_root) / rel)


def build(dist: Path = DIST) -> list[Path]:
    dist.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    skills = PLUGIN / "skills"
    for skill_dir in sorted(p for p in skills.iterdir() if p.is_dir()):
        out = dist / f"{skill_dir.name}.zip"
        _zip_dir(out, skill_dir, skill_dir.name)
        written.append(out)
    plugin_zip = dist / "superstacks-plugin.zip"
    _zip_dir(plugin_zip, PLUGIN, "superstacks")
    written.append(plugin_zip)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dist",
        type=Path,
        default=DIST,
        help="Output directory (gitignored dist/ by default)",
    )
    args = parser.parse_args(argv)
    paths = build(args.dist)
    for path in paths:
        print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
