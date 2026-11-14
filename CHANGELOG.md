# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.4.0] - 2026-11-14

### Changed

- `interrogate` (rubric, reviewer prompt, lead judgment, verdict format) and `code-review`: a change that adds or alters a finder or refuser (scanner, inventory, guard, lint rule, drift test, validator) cannot pass on a read of the code. The review needs an independent count or trace and a set of probes (mutants), each marked found or missed. A missed form that exists in real code today is at least high severity; one that does not is recorded as a stated limit.
- `verification-before-completion`: a "before you say ready" step. Read every comment and review on the PR and its ticket since your last review; a newer failing review or an unanswered finding means not ready. Claims such as none, all, safe and always name their method or are worded as what the check can see.
- `pr`: the body template gains a `## Review` section (head reviewed, kind of reviewer, comments read). A body with its own line `Class: finder` must name the independent check and the probes in `## Review`; `check_pr_body.py` enforces this and requires nothing new without that line.
- `patches/*-v6.4.patch` document the edits to the vendored skills; `sources.lock.json` dest hashes updated for the edited files.

## [6.3.0] - 2026-11-14

### Added

- Model-invoked `ama` (ask me anything): when the owner assigns work and something is unclear, the agent looks first, sorts each open point into ask, assume or look up, and asks only what changes the result. Questions come in batches of at most four, in plain words, with two to four options that say what you get, what it costs and what you give up, one marked Recommended, and a one-letter reply format. Answers are recorded through `owner-decisions`, and a short brief is sent back to confirm. The quality and safety bar is never a question.
- `ama/templates/QUESTIONS.md` (question sheet and confirming brief) and `ama/scripts/check_questions.py` (sheet validator), with tests.

### Changed

- `ticket-pipeline` lists `ama` first, before discovery. The README pipeline diagram and skills table list it too.

## [6.2.0] - 2026-11-14

### Added

- Model-invoked `owner-decisions`: finds the owner's decision record (a project decision skill, a `DECISIONS.md` ledger, or tracker decisions), reads it before asking, records a decision before acting, and reads authority from it.
- `owner-decisions/templates/DECISIONS.md`, `scripts/check_decisions.py` (ledger validator), and `scripts/authority.py` (prints the standing rule that grants an authority, or `DEFAULT: human`).

### Changed

- `safety-overrides`, `workflow-profile`, `ticket-pipeline`: merge and ready-for-review authority are read from the owner's decision record. `trust_level` stays 1 by default; only a recorded standing rule may raise it, for the scope it states.

## [6.1.1] - 2026-10-06

### Changed

- Claude marketplace `metadata.description` so `claude plugin validate --strict` passes for the marketplace as well as the plugin.
- Truthful wording for optional local helper scripts a skill may tell the agent to run (`git diff`/`git log`, a user-supplied verify-loop command, an existing Playwright install). The plugin makes no network calls, collects no telemetry, and does not read credentials.
- Plugin README logo uses Markdown instead of HTML.
- Codex listing: category Developer Tools, filled capabilities, three `defaultPrompt` entries, `extensions.com.openai.publication.release_notes`, and a `.codexignore`.
- ZIP builder also emits `dist/flat/` per-skill archives with `SKILL.md` at the zip root.

### Removed

- Committed `tests/__pycache__` bytecode.

## [6.1.0] - 2026-10-06

### Added

- Model-invoked `verify-loop` with `verify.py`, `verify.sh`, and a Playwright snapshot/console template that never installs Playwright.
- User-invoked `mistake-to-constraint`, `steer-miner`, `intake-triage`, `gardening`, and `sample-review`.
- Deterministic checkers: `pr/scripts/check_pr_body.py` and `ticket-pipeline/scripts/pipeline_status.py`.
- `trust_level` ladder (default 1) in `safety-overrides` and `workflow-profile`.
- README Philosophy section crediting the public Matt Pocock × Poteto conversation.
- A02 Crisp logo (SVG master, 512 PNG, 256/64/16 icons) and a 1280×640 GitHub social preview.
- Live GitHub URLs and install commands use `KunanonJ/superstacks`.
- Stacked pull request guidance in `pr` and `ticket-pipeline`.

## [6.0.0] - 2026-10-06

### Added

- Superstacks v6 plugin at `plugins/superstacks/` with Claude, Cursor, and Codex manifests.
- Root marketplaces for Claude, Cursor, and Codex/local agents.
- Vendored skills from obra/superpowers, mattpocock/skills, and pstack, plus original `ticket-pipeline`, `workflow-profile`, and `safety-overrides`.
- ZIP builder for claude.ai / ChatGPT skill uploads and the OpenAI plugin portal.
- Plugin linter, archive size check, and pull-request CI.

### Removed

- The v5 aggregated skill catalog (archived as git tag `archive/v5-catalog`).

[6.2.0]: https://github.com/KunanonJ/superstacks/compare/v6.1.1...v6.2.0
[6.1.1]: https://github.com/KunanonJ/superstacks/compare/v6.1.0...v6.1.1
[6.1.0]: https://github.com/KunanonJ/superstacks/compare/v6.0.0...v6.1.0
[6.0.0]: https://github.com/KunanonJ/superstacks/compare/archive/v5-catalog...v6.0.0
