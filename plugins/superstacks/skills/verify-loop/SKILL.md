---
name: verify-loop
description: Use when starting implementation or iterating a fix. Define a deterministic check for the acceptance criteria, run it red, then iterate until green.
license: MIT
---

# Verify loop

The engineer designs a runnable check. The model spends tokens on judgment, not on being a human who copies errors between tools.

## Before writing code

1. Name the acceptance criteria in one sentence.
2. Pick a **deterministic** check that would fail today and pass when the work is done: unit or integration test, CLI assertion, perf trace, or a snapshot/console script.
3. Copy a runner from `scripts/` next to this skill into the repo (or run it in place). Do not install packages.
4. Run the check. Confirm it is red. Paste the runner output (`VERIFY_FAIL`).
5. Change code. Re-run the same command. Repeat until `VERIFY_PASS`.
6. Hand the same command to `verification-before-completion` before any success claim.

Never retype compiler, test, browser, or linter errors from memory. Re-run the command.

## Runners

| File | When |
| --- | --- |
| `scripts/verify.py` | Python stdlib wrapper. Prints pass/fail evidence. |
| `scripts/verify.sh` | POSIX wrapper with the same evidence format. |
| `scripts/check-snapshot-console.cjs` | Page snapshot plus console-error check. Uses Playwright already in the project. Exits 2 if it is missing. Never installs it. |

```text
python <this-skill>/scripts/verify.py -- <project-check>
bash <this-skill>/scripts/verify.sh -- <project-check>
node <this-skill>/scripts/check-snapshot-console.cjs <url> [shot.png]
```

Replace `<project-check>` with the repo's real command (`pytest`, a compiler, a perf trace). The wrapper does not choose the check.

## Rules

- One command is the source of truth for this ticket. Do not swap it mid-loop without saying why.
- Red before green. A check that was never red does not prove the fix.
- If the check needs a browser, use the snapshot template or a CDP script the repo already runs. Do not add runtime installs.
- Paste fresh runner output. Screenshots without `VERIFY_PASS`/`VERIFY_FAIL` are not enough.
