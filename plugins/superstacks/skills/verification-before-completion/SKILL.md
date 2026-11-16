---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing. Run verification and paste output before any success claim.
license: MIT
---

# Verification Before Completion

## Overview

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

Use `verify-loop` to define that command before writing code. Run the wrappers in `verify-loop/scripts/` (`verify.py`, `verify.sh`, or `check-snapshot-console.cjs`). Paste the runner's `VERIFY_PASS` or `VERIFY_FAIL` line. Do not copy errors between tools by hand.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Before You Say Ready

"Ready" (to merge, to hand over, to ask for approval) is a claim about the whole pull request, not about your last run.

1. Read every comment and review posted on the PR and on its ticket since your own last review. Your review and the check status are only part of the state.
2. A newer failing review, or a finding nobody answered, means not ready. Say which one and who posted it.
3. Name the head you reviewed, and word each claim as what the check can see. "None", "all", "safe" and "always" need the method that established them: write "no outbound call between these two brackets", not "no outbound call runs in a transaction", when the check only read the text between the brackets.
4. Run the whole-tree guards as well as the tests for the folder you changed. Some tests scan the entire source tree: an inventory that requires a decision for every stored field of a certain kind, a sweep that bans a call or an option anywhere. A change in one folder can fail them, and a test run scoped to the changed folder never loads them. Find them before you push, run them, and name them in any brief you hand to another agent.

## A Reading Is Not Evidence

A reading of the source is a hypothesis; a failing test is evidence. When a reviewer concludes from reading library code that something is safe, and a test shows otherwise, do not side with the reading. Have a second reader trace the value to its last hop (the bytes on the wire or on disk), and write down where the first reading stopped. A frequent cause: the trace stops at a serializer that looks right, one step before a lower layer re-parses and reformats the value.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |
| PR is ready | Every comment and review since your last one, read | Your own review passing, checks green |
| A test result is reported as a finding | An assertion that can fail: an exact value, or a justified bound | A number the test only prints |
| Code is safe because the source reads that way | A test or a trace to the last hop (bytes on the wire or disk) | A read that stopped at a serializer |
| Change is ready to push | The whole-tree guard tests, run as well as the folder's own tests | A test run scoped to the changed folder |
| "None", "all", "safe", "always" | The method that established it, named beside the claim | A search that covers only part of the code |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness
