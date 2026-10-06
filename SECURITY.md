# Security policy

## What this plugin runs, sends or fetches

Skills may tell the agent to run optional local helper scripts: `git diff`/`git log`, a user-supplied test command via verify-loop, or an existing Playwright install. The plugin itself makes no network calls, collects no telemetry, and does not read credentials. Installing it copies files. Third-party installers (`npx skills add`, host plugin CLIs) are outside this plugin; they are optional and documented with a telemetry opt-out where they offer one.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting on [KunanonJ/superstacks](https://github.com/KunanonJ/superstacks/security/advisories/new). Do not open a public issue for credential leaks or exploitable defects.

Include the affected path, a reproduction that does not require secrets, and the impact. We will acknowledge the report and ship a patched `plugin.json` version when a fix is needed.

## Scope

In scope: this repository, the `superstacks` plugin folder, and the ZIP artifacts built by `scripts/build_zips.py`.

Out of scope: upstream projects we vendor (report those upstream), and any host application that loads the plugin.
