---
name: workflow-profile
description: Use when starting a ticket or choosing merge, review, and pipeline order. Generic ticket refs, merge owner, and skill sequence.
license: MIT
disable-model-invocation: true
---

# Workflow profile

Generic team conventions. Override with repo docs when they exist. `safety-overrides` still win.

## Ticket references

- Cite tickets as `Refs #N` in commits and pull requests.
- Never use `Closes`, `Fixes`, or `Resolves`. The human merge owner closes tickets.

## Merge owner

The human who asked for the work (or the user on the ticket) is the merge owner. The agent opens a **draft** PR and stops. The merge owner reviews, marks ready, and merges.

## Pipeline order

`how` → `writing-plans` → `test-driven-development` → `verification-before-completion` → `code-review` → (`interrogate` when the change is a money-path or schema change) → `pr`.

Plans live in the pull request body.

## Optional model table

Used by `how` and `interrogate` when the Task tool accepts a `model` field. Omit `model` unless the user names a slug.

| Role | Model |
|------|-------|
| how explorer | omit `model` (parent) |
| how explainer | omit `model` (parent) |
| interrogate reviewers | omit `model` (parent), one reviewer per row the user adds |
