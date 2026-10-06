---
name: workflow-profile
description: Use when starting a ticket or choosing merge, review, trust_level, and pipeline order. Generic ticket refs, merge owner, and skill sequence.
license: MIT
disable-model-invocation: true
---

# Workflow profile

Generic team conventions. Override with repo docs when they exist. `safety-overrides` still win.

## Ticket references

- Cite tickets as `Refs #N` in commits and pull requests.
- Never use `Closes`, `Fixes`, or `Resolves`. The human merge owner closes tickets.

## Merge owner

The human who asked for the work (or the user on the ticket) is the merge owner unless `trust_level` says otherwise. The implementing agent opens a **draft** PR and stops.

## Trust level

Set `trust_level` here or in repo docs. Default: `1`.

```text
trust_level: 1
```

| Level | Merge |
| --- | --- |
| 1 | Humans merge everything. The agent never merges. |
| 2 | A designated merge bot may merge green two-way-door PRs. |
| 3 | Autopilot may merge two-way-door PRs that have verify-loop evidence (`VERIFY_FAIL` then `VERIFY_PASS`). |

One-way doors always need a human plus `interrogate`, at every level: money movement, schema or data migrations, auth, data deletion, infra or prod config, licences.

## Pipeline order

`how` → `writing-plans` → `verify-loop` → `test-driven-development` → `verification-before-completion` → `code-review` → (`interrogate` on one-way doors) → `pr`.

Plans live in the pull request body. Run `ticket-pipeline/scripts/pipeline_status.py` instead of inferring which steps are done.

## Optional model table

Used by `how` and `interrogate` when the Task tool accepts a `model` field. Omit `model` unless the user names a slug.

| Role | Model |
|------|-------|
| how explorer | omit `model` (parent) |
| how explainer | omit `model` (parent) |
| interrogate reviewers | omit `model` (parent), one reviewer per row the user adds |
