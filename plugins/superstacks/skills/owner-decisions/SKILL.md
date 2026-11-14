---
name: owner-decisions
description: Use when about to merge, mark ready, close a ticket, force push, deploy, change a rule, or ask the owner a question. Reads authority from the owner's decision record, or starts one.
license: MIT
---

# Owner decisions

Authority is what the owner's recorded decisions say. `safety-overrides` still win, and no record can lift a one-way door past a human plus `interrogate`.

## 1. Find the record

Take the first that exists. Never invent one silently.

1. A project decision skill: a skill in the project's skills folder whose name or description is about the owner's or founder's decisions.
2. A ledger file: `DECISIONS.md` at the repo root, or the path the project's agent instructions name.
3. Decisions on the tracker: the ticket itself and any issue the project names as its decision log.

Done when you can name the record you are using, or state that none exists.

## 2. Read before asking

Search the record for the question first. A question the record answers is not asked. When acting on a recorded decision, quote it: the owner's words, the date, where it is recorded.

## 3. Record before acting

Write a new decision to the record first, then act. An entry holds:

- the question as put, with its options
- the owner's exact words, quoted
- the option those words select
- the date (ISO)
- what the decision does not cover

Reading short answers:

- A bare "yes" or "follow your recommendation" selects every item that had exactly one recommendation, and nothing else.
- A yes to a question with several options and no recommendation selects nothing. Ask again.
- An approval given on a statement that turns out to be false is void. Say so, do not act, and ask again with the corrected facts.

## 4. Authority comes from the record

Authorities: merge, ready, close, force-push, deploy (and stack rebases, rule changes). Each is what the latest recorded decision says, within its scope and exceptions.

- With no recorded decision the default applies: drafts only, a human merges, no force push, no deploy.
- A decision never widens by analogy. "May merge its own PR after a passing review" does not cover a locked path, a one-way door, or a deploy.
- A ledger can be queried: `python <this-skill>/scripts/authority.py DECISIONS.md merge` prints the standing rule or `DEFAULT: human`.

## 5. No record yet

Create `DECISIONS.md` from `templates/DECISIONS.md` only when the owner asks for a record or answers the first decision question. Say that you created it and where. Validate it with `python <this-skill>/scripts/check_decisions.py DECISIONS.md` until it prints nothing.

## 6. Learn

When the ledger holds five or more decisions of the same kind, propose a standing rule that would have answered them. Do not apply it. Show a short table:

| Proposed rule | Scope | Exceptions | Decisions it rests on |
| --- | --- | --- | --- |

The owner's yes becomes a recorded standing rule with its source entry. One decision never becomes a rule.
