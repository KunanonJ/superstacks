---
name: ama
description: Use when the owner assigns work and the outcome, audience, done-state, limits, risk or path is unclear. Look first, then ask plain-language questions with easy options.
license: MIT
---

# Ask me anything

The owner chooses what to build. The agent owns how well it is built. This skill closes the gap between a short assignment and a clear one. `safety-overrides` still win.

## 1. When it runs

Run when work is assigned and any of these is unclear: the outcome wanted, who it is for, what "done" looks like, what must not change, how much risk is accepted, or which of several real paths to take.

Skip when the work is already clear. Never re-ask what the owner's decision record answers: read it first with `owner-decisions`.

## 2. Look before asking

Re-read the request. Read the code, the ticket and its history, the docs and the decision record. Whatever looking can answer, looking answers.

Say what was found in one or two lines, so the owner sees the homework was done.

## 3. Sort every open point

- ASK: the owner's call. Money, security, privacy, legal, production, anything irreversible, anything a customer sees, a new cost or vendor, scope.
- ASSUME: low risk and easy to undo. State the assumption in one line and go on.
- LOOK UP: a fact. Go and find it.

Ask only when the answer changes what gets built or how risky it is. A technical question the owner cannot judge is not asked: decide it to the highest standard and say in one line what was chosen and why.

## 4. How to ask

Use `templates/QUESTIONS.md`. The reader is not technical.

- One screen. At most four questions, most important first. If more are needed, ask the next batch after the answers.
- One plain sentence per question, one decision per question, no code names. A technical word that cannot be avoided gets a five-word explanation in brackets.
- Two to four options that are real alternatives. Each says in everyday words what you get, what it costs (time, money, risk) and what you give up. Numbers over adjectives: "about 2 days", "about 20 USD a month".
- Exactly one option is marked Recommended, listed first, with one line of why. When no honest recommendation exists, say so and name the fact that would decide it.
- Offer "Not sure, you choose" (take the recommendation, record that it was taken) and a free answer in the owner's own words.
- Make answers one letter each, and show the reply format: "1A 2B 3A".
- A tiny before and after helps the owner picture the result.
- Ask neutrally. Show every risk. Do not steer toward yes.

Check the sheet: `python <this-skill>/scripts/check_questions.py QUESTIONS.md`. Send it when it prints nothing.

### Worked example

Assignment: "make sign-up faster".

Good:

1. Which sign-up step slows people down most? A (Recommended) Ask for an email only, and collect the rest later: about 2 days, you lose some details at the start. B Keep every field, make the page load quicker: about 1 day, people still fill a long form. C Let people sign in with an existing account: about 5 days, depends on an outside company. Why A: the long form is where people leave.
2. How fast is fast enough? A (Recommended) Under 30 seconds from tap to done. B Under 10 seconds: about 3 days more, some checks must wait until later.
3. Is it fine to change what new customers see this week? A (Recommended) Yes, to everyone. B Yes, to 10 in 100 new people first: about 1 day more, you see the result before everyone gets it.

Reply: "1A 2A 3B".

Bad:

1. Should we refactor the auth flow and optimize the signup endpoint, or use caching?
2. What are your performance requirements?
3. Do you want the new design, and should it be released gradually? (Yes or no)

The bad set uses jargon, offers no options, stacks two decisions in one question, and leads with a favourite. The owner cannot answer it without help.

## 5. After the answers

1. Record each answer through `owner-decisions`: the owner's exact words, what they select, what they do not cover.
2. Send a brief the owner can confirm at a glance: Goal (one sentence), Done when (checks that can be seen), Not included, Assumptions made, Quality and safety bar.
3. Start work when nothing in ASK is open. An answer that raises a new real question gets asked, never guessed.

## 6. The quality and safety bar is not a question

The owner never chooses whether work is correct or secure. Whatever the answers, the work is done test-first (`test-driven-development`), verified before it is called done (`verification-before-completion`), reviewed (`code-review`) and secure by default: inputs checked, permissions enforced, no secrets exposed, money exact. `safety-overrides` always apply.

When a chosen option would lower that bar, say so plainly, offer the nearest safe way to the same outcome, and ask again.

## 7. Stop rules

- Stop asking when every open point is ASSUME or LOOK UP.
- Do not ask to look thorough, and do not ask the same thing twice in other words.
- If the owner is away, do the parts no question blocks and leave the questions written and ready.
