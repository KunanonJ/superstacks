---
name: intake-triage
description: Use when a coordinator has a batch of bug reports, feedback, or alerts. Deduplicate, group, score two-way vs one-way doors, and write ticket briefs ready to dispatch.
license: MIT
disable-model-invocation: true
---

# Intake triage

For coordinator agents. Turn a pile of reports into dispatchable ticket briefs. Do not implement the tickets here.

## Sequence

1. Read the batch the user pasted or named (files, not a tracker write-back).
2. Deduplicate: same symptom, same surface, same likely cause → one group.
3. Score the door:
   - **one-way**: money movement, schema or data migrations, auth, data deletion, infra or prod config, licences.
   - **two-way**: everything cheap to roll back.
4. Write one brief per group from `templates/BRIEF.md`.
5. Run the checker. Do not reason about missing headings.

```text
python <this-skill>/scripts/check_brief.py path/to/brief.md
```

A brief is ready to dispatch only when the script exits 0.

## Brief fields

- Goal
- Scope
- Acceptance
- Verify (the exact command `verify-loop` will run)
- Forbidden
- Door (`one-way` or `two-way`)

## Rules

- Do not file tracker issues or send chat. Hand briefs to the human or the next agent.
- One-way briefs must name `interrogate` in Forbidden-to-skip.
- Each brief names one verify command. That command is the verify-loop check.
