#!/usr/bin/env python3
"""List recently merged commits for sample-review. Stdlib only. Prints hashes, nothing else."""

from __future__ import annotations

import argparse
import subprocess
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=5, help="Sample size (default 5)")
    parser.add_argument(
        "--since",
        default="1 day ago",
        help='git --since value (default "1 day ago")',
    )
    args = parser.parse_args(argv)
    proc = subprocess.run(
        [
            "git",
            "log",
            "--merges",
            f"--since={args.since}",
            f"-n{args.n}",
            "--format=%H %s",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        # Non-merge repos still have merged work as first-parent commits.
        proc = subprocess.run(
            [
                "git",
                "log",
                f"--since={args.since}",
                f"-n{args.n}",
                "--format=%H %s",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    print(f"sample-review n={args.n} since={args.since} got={len(lines)}")
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
