---
name: ticket-pipeline
description: Use when running a ticket from discovery through a draft PR. Sequences how, plans, verify-loop, TDD, verification, review, optional interrogate, then pr.
license: MIT
disable-model-invocation: true
---

# Ticket pipeline

Run a ticket from discovery through a **draft** pull request. `safety-overrides` beat every step.

Put evidence in the PR body under the headings this skill names. Then run the status script. Do not argue in prose about which steps are done:

```text
python <this-skill>/scripts/pipeline_status.py --pr-body BODY.md
```

Re-run until the script prints `missing: 0`.

## Sequence

1. **how** — build a mental model before changing code. Heading: `## How`.
2. **writing-plans** — plan in the pull request body. Heading: `## Plan`.
3. **verify-loop** — define the deterministic check, run it red (`VERIFY_FAIL`), then iterate.
4. **test-driven-development** — if the check is a test: failing test, then minimal code. Heading: `## TDD` (include `red-green`).
5. **verification-before-completion** — paste fresh `verify-loop` runner output. Heading: `## Evidence`.
6. **code-review** — Standards and Spec axes on the branch diff. Heading: `## Code review`.
7. **interrogate** — required for one-way doors (money movement, schema or data migrations, auth, data deletion, infra or prod config, licences). Heading: `## Interrogate`, or write `N/A (two-way door)`.
8. **pr** — draft pull request body. Run `pr/scripts/check_pr_body.py`. Ticket links are `Refs #N` only.

## Hard rules (also in safety-overrides)

- Draft PRs. Never mark ready. Merge only as `trust_level` in safety-overrides allows.
- Push only this branch. Rewrite with `--force-with-lease` only.
- No production credentials, live infrastructure, runtime package installs, or secret-using CI jobs.
- No tracker or chat writes from a ticket.
- Skip a blocking approval gate only with `Ruling: what / why` in the PR body.
