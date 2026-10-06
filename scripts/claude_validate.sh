#!/usr/bin/env bash
# Run `claude plugin validate --strict` with a pinned CLI when installable
# without secrets. Skip with a note otherwise.
set -u
PLUGIN_DIR="${1:-./plugins/superstacks}"
PINNED_VERSION="2.1.291"

echo "Attempting Claude plugin validate --strict with @anthropic-ai/claude-code@${PINNED_VERSION} (no secrets)."
if ! command -v npm >/dev/null 2>&1; then
  echo "SKIP: npm is not available, so the pinned Claude CLI cannot be installed without extra tooling."
  exit 0
fi

PREFIX="$(mktemp -d)"
cleanup() { rm -rf "${PREFIX}"; }
trap cleanup EXIT

if ! npm install --prefix "${PREFIX}" "@anthropic-ai/claude-code@${PINNED_VERSION}" --no-fund --no-audit; then
  echo "SKIP: pinned Claude CLI could not be installed without secrets or extra registry auth."
  exit 0
fi

CLAUDE_BIN="${PREFIX}/node_modules/.bin/claude"
if [[ ! -x "${CLAUDE_BIN}" ]]; then
  echo "SKIP: claude binary missing after npm install."
  exit 0
fi

set +e
OUTPUT="$("${CLAUDE_BIN}" plugin validate --strict "${PLUGIN_DIR}" 2>&1)"
STATUS=$?
set -e
printf '%s\n' "${OUTPUT}"
if [[ "${STATUS}" -eq 0 ]]; then
  exit 0
fi
if printf '%s\n' "${OUTPUT}" | grep -qiE 'auth|login|api key|unauthorized|not logged|native binary not installed'; then
  echo "SKIP: Claude CLI is installed but validate cannot run here without extra install/auth; not using secrets in CI."
  exit 0
fi
exit "${STATUS}"
