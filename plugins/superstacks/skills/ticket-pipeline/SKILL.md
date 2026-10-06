---
name: ticket-pipeline
description: Use when running a ticket from discovery through a draft PR. Sequences how, plans, TDD, verification, review, optional interrogate, then pr.
license: MIT
disable-model-invocation: true
---

# Ticket pipeline

Run a ticket from discovery through a **draft** pull request. `safety-overrides` beat every step.

## Sequence

1. **how** — build a mental model before changing code.
2. **writing-plans** — plan in the pull request body, not a plans directory.
3. **test-driven-development** — failing test, then minimal code.
4. **verification-before-completion** — paste fresh command output before any success claim.
5. **code-review** — Standards and Spec axes on the branch diff.
6. **interrogate** — only for money-path or schema changes (payments, balances, migrations, authz).
7. **pr** — draft pull request body. Ticket links are `Refs #N` only.

## Hard rules (also in safety-overrides)

- Draft PRs. Never merge, auto-merge, or mark ready.
- Push only this branch. Rewrite with `--force-with-lease` only.
- No production credentials, live infrastructure, runtime package installs, or secret-using CI jobs.
- No tracker or chat writes from a ticket.
- Skip a blocking approval gate only with `Ruling: what / why` in the PR body.
