---
name: mistake-to-constraint
description: Use when a mistake repeats. Encode it as the strongest guard — type or runtime, lint, test, directory convention, then a rules line — and log it in CONSTRAINTS.md.
license: MIT
disable-model-invocation: true
---

# Mistake to constraint

A repeated mistake is an environment bug. Do not add another prompt paragraph first.

## Order (strongest first)

1. **Type narrowing or runtime guard** — make the illegal state unrepresentable. See `templates/runtime-guard.py`.
2. **Lint rule** — copy `templates/eslint-rule.cjs` or `templates/semgrep-rule.yml`. Prefer an existing ruff selector from `templates/ruff-snippet.toml` before a new plugin.
3. **Test** — a regression that fails if the mistake returns.
4. **Directory convention** — put the dangerous thing in a folder that review and CI already treat as special.
5. **Rules line** — last. Only when 1–4 cannot hold the line.

## Ledger

Keep `CONSTRAINTS.md` at the repo root of the consuming project. Start from the template next to this skill.

Each row: date, mistake, guard added, kind (`type` / `runtime` / `lint` / `test` / `directory` / `rules`).

## Rules

- One mistake, one guard. Do not stack a lint rule and a rules line for the same bug unless the lint cannot see it.
- Do not install ESLint, ruff, or semgrep. Wire the template into tools the repo already runs.
- Do not file tracker issues. Open a draft PR with the guard and a verify-loop command.
