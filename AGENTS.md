# Superstacks contributor notes

This repository is the Superstacks v6.1.1 plugin: a lean, MIT-licensed set of coding-agent skills at `plugins/superstacks/`.

## Layout

- Plugin code and skills: `plugins/superstacks/`
- Manifests: `plugins/superstacks/.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`
- Marketplaces: `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `.agents/plugins/marketplace.json`
- Vendor pins: `sources.lock.json`
- Dest-only diffs: `patches/`
- Checks: `python -m app.plugin_lint` and `python -m pytest`

Do not add a root `plugin.json`. Do not add `commands/`, `agents/`, or `hooks/`. Do not name the plugin or marketplaces with `claude`, `cursor`, `openai`, `official`, `plugin`, `mcp`, or `test`.

Skill bodies must stay product-neutral. Install docs may name hosts.

Open draft pull requests only. Safety overrides in `plugins/superstacks/rules/safety-overrides.mdc` beat skill text.
