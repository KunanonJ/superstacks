# Superstacks

<img src="plugins/superstacks/assets/logo.svg" alt="Superstacks" width="96" height="96">

Lean MIT skill stack for coding agents: discovery, plans, TDD, verification loops, review, draft PRs, and ticket pipelines.

[![CI](https://github.com/KunanonJ/superstacks/actions/workflows/ci.yml/badge.svg)](https://github.com/KunanonJ/superstacks/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-0B1F33.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-6.1.1-2EC4B6.svg)](CHANGELOG.md)

Superstacks is a small plugin, not a giant catalog. It vendors a handful of upstream skills at pinned git SHAs, applies documented patches, and adds a generic ticket pipeline plus hard safety overrides. The GitHub repository name is `KunanonJ/superstacks`.

## Philosophy

The engineer designs the environment. The model spends tokens on judgment.

- **Environment over prompting.** Put verification, constraints, and coordinators in the repo so the agent does not have to be reminded in prose.
- **Verification first.** Before writing code, name a deterministic check, run it red, then iterate until green. The agent should not be the human copying errors between tools.
- **Constraints in code.** When a mistake repeats, encode it as a type, lint rule, test, or directory convention. A rules line is last.
- **Skills as process.** A skill is a named loop with a script when the step is mechanical.

Themes drawn from the public Matt Pocock × Poteto conversation: [YouTube](https://www.youtube.com/watch?v=MN9dGgmLyso). Paraphrase only; this README does not invent quotations.

## Why this instead of raw upstream

- One folder you can list in Claude, Cursor, and Codex marketplaces.
- Descriptions stay short, trigger-first, and product-neutral in skill bodies.
- Safety overrides beat skill text: draft PRs, `Refs #N`, evidence before "done", and a `trust_level` ladder (default 1: humans merge everything).
- Vendored copies are hashed in `sources.lock.json`. Patches live in `patches/`.

## Quick start

Pick one row. The GitHub repository is [`KunanonJ/superstacks`](https://github.com/KunanonJ/superstacks).

| Surface | How |
| --- | --- |
| Claude Code | `/plugin marketplace add KunanonJ/superstacks` then `/plugin install superstacks@superstacks` |
| Cursor | Copy `plugins/superstacks/` to `~/.cursor/plugins/local/superstacks/` until the public listing exists |
| Codex | `codex plugin marketplace add KunanonJ/superstacks` |
| claude.ai ZIP upload | `python scripts/build_zips.py` and upload a per-skill ZIP from `dist/` (`<skill>/SKILL.md`) or `dist/flat/` (`SKILL.md` at zip root) |
| ChatGPT ZIP upload | Same per-skill ZIPs, or `dist/superstacks-plugin.zip` for the OpenAI plugin portal |
| `npx skills add` | `DISABLE_TELEMETRY=1 npx skills add KunanonJ/superstacks -g -s '*' --copy -y` |
| Plain copy | Copy `plugins/superstacks/skills/<name>/` into your agent's skills directory |

Attach `dist/` artifacts to a GitHub Release when you cut a version. This repo does not create the `v6.1.1` tag for you.

## What this plugin runs, sends or fetches

Skills may tell the agent to run optional local helper scripts: `git diff`/`git log`, a user-supplied test command via verify-loop, or an existing Playwright install. The plugin itself makes no network calls, collects no telemetry, and does not read credentials. Optional installers such as `npx skills add` are third-party; pass `DISABLE_TELEMETRY=1` if you use that path.

## Pipeline

```mermaid
flowchart LR
  how --> plans[writing-plans]
  plans --> vloop[verify-loop]
  vloop --> tdd[test-driven-development]
  tdd --> verify[verification-before-completion]
  verify --> review[code-review]
  review --> optional[interrogate if one-way door]
  optional --> pr[pr draft]
```

`ticket-pipeline` is the user-invoked router for that order. `verify-loop` is the extra always-loaded skill: define the check, run it red, then green. `safety-overrides` always apply.

Off-pipeline (user-invoked): `mistake-to-constraint`, `steer-miner`, `intake-triage`, `gardening`, `sample-review`.

## Skills

| Skill | Invocation | Source |
| --- | --- | --- |
| verify-loop | model | this repo |
| writing-plans | model | obra/superpowers |
| test-driven-development | model | obra/superpowers |
| verification-before-completion | model | obra/superpowers |
| diagnosing-bugs | model | mattpocock/skills |
| code-review | model | mattpocock/skills |
| pr | model | mattpocock/skills |
| writing-for-agents | model | mattpocock/skills |
| grilling | model | mattpocock/skills |
| domain-modeling | model | mattpocock/skills |
| grill-with-docs | user | mattpocock/skills |
| how | user | pstack (cursor/plugins) |
| interrogate | user | pstack (cursor/plugins) |
| ticket-pipeline | user | this repo |
| workflow-profile | user | this repo |
| mistake-to-constraint | user | this repo |
| steer-miner | user | this repo |
| intake-triage | user | this repo |
| gardening | user | this repo |
| sample-review | user | this repo |

Always-on rule: `plugins/superstacks/rules/safety-overrides.mdc`.

## Safety

- Draft pull requests. Never mark ready. Merge only as `trust_level` allows (default 1: humans merge everything).
- `Refs #N` never `Closes` / `Fixes` / `Resolves`.
- Push the working branch only. `--force-with-lease` only.
- No production credentials, live infrastructure, runtime installs, or secret CI jobs.
- Plans go in the PR body. "Done" needs pasted command output.
- One-way doors (money, schema or data migrations, auth, data deletion, infra or prod config, licences) always need a human plus `interrogate`.

See [SECURITY.md](SECURITY.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Run `python -m app.plugin_lint` and `python -m pytest` before opening a draft PR.

## Credits

Vendored under MIT from Jesse Vincent, Matt Pocock, Lauren Tan / pstack, and a confirmed MIT excerpt of HumanLayer `show-me` inside `pr`. Full notices: [plugins/superstacks/THIRD_PARTY.md](plugins/superstacks/THIRD_PARTY.md).

## License

[MIT](LICENSE) © 2026 Kunanon Jarat.
