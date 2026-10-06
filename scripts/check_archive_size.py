#!/usr/bin/env python3
"""Fail if a git archive of HEAD is too large or has too many files."""

from __future__ import annotations

import io
import subprocess
import sys
import tarfile

MAX_BYTES = 50 * 1024 * 1024
MAX_FILES = 10_000


def main() -> int:
    proc = subprocess.run(
        ["git", "archive", "--format=tar", "HEAD"],
        check=True,
        capture_output=True,
    )
    buf = io.BytesIO(proc.stdout)
    size = len(proc.stdout)
    with tarfile.open(fileobj=buf, mode="r:") as tar:
        files = [m for m in tar.getmembers() if m.isfile()]
    print(f"archive bytes={size} files={len(files)}")
    errors = []
    if size >= MAX_BYTES:
        errors.append(f"archive {size} bytes exceeds 50 MiB")
    if len(files) >= MAX_FILES:
        errors.append(f"archive {len(files)} files exceeds 10,000")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
