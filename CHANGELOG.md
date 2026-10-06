# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.0.0] - 2026-10-06

### Added

- Superstacks v6 plugin at `plugins/superstacks/` with Claude, Cursor, and Codex manifests.
- Root marketplaces for Claude, Cursor, and Codex/local agents.
- Vendored skills from obra/superpowers, mattpocock/skills, and pstack, plus original `ticket-pipeline`, `workflow-profile`, and `safety-overrides`.
- ZIP builder for claude.ai / ChatGPT skill uploads and the OpenAI plugin portal.
- Plugin linter, archive size check, and pull-request CI.

### Removed

- The v5 aggregated skill catalog (archived as git tag `archive/v5-catalog`).

[6.0.0]: https://github.com/KunanonJ/superstacks/releases/tag/v6.0.0
