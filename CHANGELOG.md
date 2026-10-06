# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[6.1.0]: https://github.com/KunanonJ/superstacks/compare/v6.0.0...v6.1.0
[6.0.0]: https://github.com/KunanonJ/superstacks/compare/archive/v5-catalog...v6.0.0
