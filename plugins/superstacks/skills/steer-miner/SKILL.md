---
name: steer-miner
description: Use when mining local agent transcripts the user points to. Find repeated human corrections and propose skills, lint rules, or constraints as a report. Never edit files.
license: MIT
disable-model-invocation: true
---

# Steer miner

Read only the transcript files the user names. Find repeated human corrections. Propose environment changes. Stop.

## Do

1. Confirm the paths. If the user did not name files or a directory, stop and ask.
2. Run the miner:

```text
python <this-skill>/scripts/mine_transcripts.py --path <file-or-dir> [--min-count 2]
```

3. Read the report. Group hits into: new skill, lint/semgrep/ruff rule, `CONSTRAINTS.md` row, or ignore (one-off).
4. Return a report: pattern, examples (short), proposed guard, and which kind from `mistake-to-constraint`.

## Do not

- Do not edit files.
- Do not file tracker issues or send chat messages.
- Do not scan home directories or default transcript folders the user did not name.
- Do not paste secrets, tokens, or full transcripts into the report.
