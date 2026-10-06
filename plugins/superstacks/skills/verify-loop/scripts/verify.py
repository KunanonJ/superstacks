#!/usr/bin/env python3
"""Run a verification command and print pass/fail evidence. Stdlib only."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime, timezone


def run_command(argv: list[str]) -> int:
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    t0 = time.perf_counter()
    print(f"VERIFY command: {' '.join(argv)}")
    print(f"VERIFY started: {started}")
    try:
        proc = subprocess.run(argv, check=False)
    except OSError as exc:
        print(f"VERIFY spawn error: {exc}", file=sys.stderr)
        print("VERIFY_FAIL")
        return 1
    duration_ms = int((time.perf_counter() - t0) * 1000)
    print(f"VERIFY exit: {proc.returncode}")
    print(f"VERIFY duration_ms: {duration_ms}")
    if proc.returncode == 0:
        print("VERIFY_PASS")
        return 0
    print("VERIFY_FAIL")
    return proc.returncode or 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run after --",
    )
    args = parser.parse_args(argv)
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("missing command. Usage: verify.py -- <command> [args...]")
    return run_command(command)


if __name__ == "__main__":
    sys.exit(main())
