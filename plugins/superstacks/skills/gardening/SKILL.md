---
name: gardening
description: Use when finding small maintenance work. One concern per PR, each with a verify command and a small diff budget.
license: MIT
disable-model-invocation: true
---

# Gardening

Small maintenance only: deprecated patterns, dead code, tiny perf fixes, lint debt. One concern per draft PR.

## Sequence

1. List candidate nits. Pick **one**.
2. Name a verify-loop command that fails on the nit and passes after the fix.
3. Stay inside the diff budget. Run:

```text
python <this-skill>/scripts/diff_budget.py --base <default-branch> --max-lines 80 --max-files 6
```

4. If the script fails, split the work. Do not raise the budget to fit a refactor.
5. Open a draft PR. Run `pr/scripts/check_pr_body.py` on the body.

## Budget defaults

- 80 changed lines
- 6 files
- No generated lockfile churn
- No behaviour change outside the named nit

## Rules

- Dead-code deletion needs a verify command that would fail if the symbol were still referenced, or a compile/test run that proves the tree still loads.
- Do not mix gardening with a feature. Do not "while I'm here".
- One-way doors are not gardening. Hand those to `intake-triage` / `interrogate`.
