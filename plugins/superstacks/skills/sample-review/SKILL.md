---
name: sample-review
description: Use when sampling recently merged PRs against repo standards and CONSTRAINTS.md. Propose environment tightenings, not per-PR comments. Default 5 per day.
license: MIT
disable-model-invocation: true
---

# Sample review

Score a small sample of recently merged pull requests against this repo's standards and `CONSTRAINTS.md`. Improve the environment. Do not nibble at old diffs.

## Sequence

1. List the sample (default 5 for the last day):

```text
python <this-skill>/scripts/sample_merged.py --n 5 --since 1 day ago
```

2. For each hash, read the diff and the PR body. Score:
   - verify-loop evidence present?
   - CONSTRAINTS.md guards respected?
   - door labelled, one-way got `interrogate`?
   - draft discipline / `Refs #N`?
3. Do **not** leave per-PR review comments on merged work.
4. Propose tightenings: a lint rule, a test, a `CONSTRAINTS.md` row, a skill edit, or a `trust_level` change. Hand those to `mistake-to-constraint` or a gardening PR.

## Rules

- Sample, don't boil the ocean. If the user names N, use N.
- One-off style nits are not environment bugs. Repeated misses are.
- Do not merge, revert, or force-push as part of this skill.
