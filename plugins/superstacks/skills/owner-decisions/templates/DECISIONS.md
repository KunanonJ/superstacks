# Decisions

Ledger of the owner's decisions. Newest first. Copy this file to the repo root.
Validate with `python <skill>/scripts/check_decisions.py DECISIONS.md`.

## Standing rules

Start the rule with the authority and a colon: `merge:`, `ready:`, `close:`, `force-push:`, or `deploy:`. Source is the heading of the log entry the rule rests on, written as `YYYY-MM-DD title`.

| Rule | Scope | Exceptions | Date | Source |
| --- | --- | --- | --- | --- |

## Decision log

Add entries below, newest first, in this shape:

```text
### YYYY-MM-DD short title

- Question and options: the question as put, with its options
- Owner's words: "the exact words, quoted"
- Selects: the option those words select
- Does not cover: what this decision leaves undecided
- Where recorded: ticket, comment, or chat reference
```
