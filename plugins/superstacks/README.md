# Superstacks

<img src="assets/logo.svg" alt="Superstacks" width="96" height="96">

Superstacks is a small, MIT-licensed plugin of coding-agent skills. It covers discovery, implementation plans, test-driven development, a verify-loop, two-axis review, draft pull requests, optional adversarial review, design grilling, and coordinator skills for constraints, intake, gardening, and sampling.

This plugin does not ship MCP servers, hooks, commands, or custom agents. Skills are markdown plus a few text helpers. Nothing in the pack runs in the background.

## What this plugin runs, sends or fetches

Nothing. Superstacks contains instructions and static assets only. It does not start processes, call network APIs, collect telemetry, or read credentials. Installing it copies files. Optional third-party installers such as `npx skills add` are documented below with a telemetry opt-out; they are not part of the plugin itself.

## Install

Install from [`KunanonJ/superstacks`](https://github.com/KunanonJ/superstacks).

| Surface | How |
| --- | --- |
| Claude Code | `/plugin marketplace add KunanonJ/superstacks` then `/plugin install superstacks@superstacks` (marketplace name is `superstacks`) |
| Cursor | Copy `plugins/superstacks/` to `~/.cursor/plugins/local/superstacks/` until the listing is public |
| Codex | `codex plugin marketplace add KunanonJ/superstacks` |
| claude.ai / ChatGPT ZIP upload | Build with `python scripts/build_zips.py` and attach the per-skill ZIP or the plugin ZIP from `dist/` |
| `npx skills add` | `DISABLE_TELEMETRY=1 npx skills add KunanonJ/superstacks -g -s '*' --copy -y` |
| Plain copy | Copy any `skills/<name>/` folder into your agent's skills directory |

Per-skill ZIPs use a `<skill>/SKILL.md` layout so they upload cleanly. The plugin ZIP is the OpenAI portal bundle. Attach `dist/` artifacts to a GitHub Release when you publish a version; this repository does not create tags for you.

## Skills

User-invoked skills (`disable-model-invocation: true`): `how`, `grill-with-docs`, `interrogate`, `ticket-pipeline`, `workflow-profile`, `mistake-to-constraint`, `steer-miner`, `intake-triage`, `gardening`, `sample-review`.

Model-invoked: `verify-loop`, `writing-plans`, `test-driven-development`, `verification-before-completion`, `diagnosing-bugs`, `code-review`, `pr`, `writing-for-agents`, `grilling`, `domain-modeling`.

Always-on rule: `rules/safety-overrides.mdc`.

## License

MIT. Upstream notices are in [THIRD_PARTY.md](THIRD_PARTY.md).
