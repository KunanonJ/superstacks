# Contributing

Thanks for helping Superstacks stay small and installable.

## Development

1. Use a virtualenv and `pip install -r requirements.txt`.
2. Edit skills under `plugins/superstacks/skills/` or rules under `plugins/superstacks/rules/`.
3. If you change a vendored file, regenerate the matching patch in `patches/` against the pinned SHA in `sources.lock.json`.
4. Keep skill bodies product-neutral ("the model", "the agent"). Host names belong in install docs only.
5. Pull requests from the owner's account are opened ready for review and merge by themselves when the required check passes. A pull request from anyone else is opened as a draft or ready, and waits for the owner (see below).

## How this repository is maintained

The rules below describe how this repository's own pull requests and releases are handled. They do not change `plugins/superstacks/rules/safety-overrides.mdc` or any skill: those are the rules the plugin gives to other projects, and they stay as they are. The owner's standing decisions are in [DECISIONS.md](DECISIONS.md).

- A pull request from the owner's account, from a branch in this repository, that is not a draft, has auto-merge switched on by `.github/workflows/automerge.yml`. GitHub merges it (squash) only after the required `lint` check passes.
- A Dependabot pull request from this repository is treated the same way.
- A version bump of `plugins/superstacks/.claude-plugin/plugin.json` that reaches `main` is tagged `v<version>` and released automatically by `.github/workflows/release.yml`, after the linter, tests, size check and ZIP build pass. It attaches the ZIPs from `dist/`. A version that is already tagged is skipped.
- Release notes come from `.github/release-notes/v<version>.md` when that file exists, otherwise from generated notes.

## Checks

```bash
python -m app.plugin_lint
python -m pytest
python scripts/check_archive_size.py
python scripts/build_zips.py
```

`scripts/claude_validate.sh` runs `claude plugin validate --strict` with a pinned CLI when that CLI installs without secrets. CI skips it with a note otherwise.

## Pull requests from other people

A pull request from any account other than the owner, and any pull request from a fork, is never merged automatically. An agent reviews it for safety first (the checklist is in [AGENTS.md](AGENTS.md)) and posts its findings with a verdict. Then the owner reviews it and merges it himself. No workflow labels or comments on a fork's pull request, because a fork's token is read-only.

## Naming

The plugin folder and every plugin/marketplace `name` is `superstacks`. Do not put `claude`, `cursor`, `openai`, `official`, `plugin`, `mcp`, or `test` in those identifiers. Upstream skill folder `test-driven-development` is an exception.

## License

By contributing you agree the work is MIT-licensed, same as [LICENSE](LICENSE).
