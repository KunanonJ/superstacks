# Decisions

How this repository is maintained, as decided by the owner. These rules govern this repository's own pull requests and releases. They do not change `plugins/superstacks/rules/safety-overrides.mdc` or any skill, which are the rules the plugin gives to other projects.

## Standing rules

| Rule | What it means | Where it is enforced |
| --- | --- | --- |
| Owner pull requests merge by themselves | A non-draft pull request from the owner's account, from a branch in this repository, gets auto-merge (squash) and merges when the required check passes. No exceptions for safety rules or CI files. | `.github/workflows/automerge.yml` |
| Dependabot pull requests merge by themselves | Same mechanism, same required check. | `.github/workflows/automerge.yml` |
| A new version is tagged and released automatically | A plugin version on `main` with no `v<version>` tag is checked, built, tagged and released with its ZIPs. | `.github/workflows/release.yml`, `scripts/release_plan.py` |
| Other people's pull requests wait for the owner | An agent reviews the pull request for safety and posts a verdict, then the owner reviews and merges it himself. Never automatic. | `CONTRIBUTING.md`, `AGENTS.md` |

## Decision log

Newest first. All decisions are dated 2026-11-15.

### 2026-11-15: other people's pull requests

> "but incase if other people want to contribute would need me to review and merge it by myself which you shoul review it first make sure it safe"

Selects: a pull request from anyone else is reviewed by an agent for safety first, then reviewed and merged by the owner himself.
Does not cover: any automatic merge, label or comment on such a pull request. It does not let the agent merge it, whatever the verdict.

### 2026-11-15: how a new version reaches projects

Asked how a new version reaches projects, the owner chose: "Tag and release automatically (Recommended)".

Selects: a version bump that reaches `main` is tagged and published as a GitHub release with the built ZIPs, without a manual step.
Does not cover: publishing a version that failed the checks (the release job runs the linter, tests, size check and build first), re-releasing a version that is already tagged, or a release from any branch other than `main`.

### 2026-11-15: how far automatic merging goes

Asked how far automatic merging should go, with a recommended option that kept a locked core, the owner chose: "Fully automatic, no exceptions".

Selects: everything from the owner's own account merges when checks pass, including safety rules and CI files.
Does not cover: pull requests from other accounts or from forks; it does not remove the required check (auto-merge waits for it); it does not apply to drafts.

### 2026-11-15: automatic merging and updates

> "ok for superstack skills please setup cicd to let it do automerge with humanless and continue update seamlessly everytime"

Selects: CI/CD that merges without a human and keeps updates flowing on every change.
Does not cover: weakening the required check, or merging pull requests from other people.
