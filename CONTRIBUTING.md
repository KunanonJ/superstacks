# Contributing

Thanks for helping Superstacks stay small and installable.

## Development

1. Use a virtualenv and `pip install -r requirements.txt`.
2. Edit skills under `plugins/superstacks/skills/` or rules under `plugins/superstacks/rules/`.
3. If you change a vendored file, regenerate the matching patch in `patches/` against the pinned SHA in `sources.lock.json`.
4. Keep skill bodies product-neutral ("the model", "the agent"). Host names belong in install docs only.
5. Open a **draft** pull request. Do not merge, auto-merge, or mark ready.

## Checks

```bash
python -m app.plugin_lint
python -m pytest
python scripts/check_archive_size.py
python scripts/build_zips.py
```

`scripts/claude_validate.sh` runs `claude plugin validate --strict` with a pinned CLI when that CLI installs without secrets. CI skips it with a note otherwise.

## Naming

The plugin folder and every plugin/marketplace `name` is `superstacks`. Do not put `claude`, `cursor`, `openai`, `official`, `plugin`, `mcp`, or `test` in those identifiers. Upstream skill folder `test-driven-development` is an exception.

## License

By contributing you agree the work is MIT-licensed, same as [LICENSE](LICENSE).
