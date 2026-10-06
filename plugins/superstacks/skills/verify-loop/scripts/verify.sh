#!/usr/bin/env bash
# Run a verification command and print pass/fail evidence. No extra packages.
# Usage: bash verify.sh -- <command> [args...]

set -uo pipefail

if [[ "${1:-}" == "--" ]]; then
  shift
fi

if [[ $# -lt 1 ]]; then
  printf 'usage: %s -- <command> [args...]\n' "$0" >&2
  exit 2
fi

printf 'VERIFY command: %s\n' "$*"
printf 'VERIFY started: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

start_ns=0
if date +%s%N >/dev/null 2>&1; then
  start_ns=$(date +%s%N)
fi

set +e
"$@"
exit_code=$?
set -e

duration_ms="unknown"
if [[ "$start_ns" != 0 ]]; then
  end_ns=$(date +%s%N)
  duration_ms=$(( (end_ns - start_ns) / 1000000 ))
fi

printf 'VERIFY exit: %s\n' "$exit_code"
printf 'VERIFY duration_ms: %s\n' "$duration_ms"

if [[ "$exit_code" -eq 0 ]]; then
  printf 'VERIFY_PASS\n'
  exit 0
fi

printf 'VERIFY_FAIL\n'
exit "$exit_code"
