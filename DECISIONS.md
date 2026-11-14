# Decisions

Ledger of the owner's decisions about how this repository is maintained. Newest first.
Validate with `python plugins/superstacks/skills/owner-decisions/scripts/check_decisions.py DECISIONS.md`.

These rules are about this repository only. The rules the plugin gives to other projects are in
`plugins/superstacks/rules/safety-overrides.mdc` and are not changed by anything here.

## Standing rules

| Rule | Scope | Exceptions | Date | Source |
| --- | --- | --- | --- | --- |
| merge: a pull request from the owner's account merges by itself when the required check passes | This repository, any path | Other accounts, forks, a red or pending check | 2026-11-15 | 2026-11-15 automatic merging |
| ready: a pull request from the owner's account is opened ready for review, not as a draft | This repository | Other accounts | 2026-11-15 | 2026-11-15 automatic merging |
| deploy: a version bump on main is tagged and released automatically | This repository | A version whose checks fail is not released | 2026-11-15 | 2026-11-15 how a new version reaches projects |

## Decision log

### 2026-11-15 other people's pull requests

- Question and options: none put; the owner added this after choosing automatic merging
- Owner's words: "but incase if other people want to contribute would need me to review and merge it by myself which you shoul review it first make sure it safe"
- Selects: a pull request from any other account is never merged automatically; an agent reviews it for safety first and posts its findings, then the owner reviews and merges it
- Does not cover: who may be given write access, and what counts as a trusted contributor later
- Where recorded: the pull request that added the repository automation

### 2026-11-15 how a new version reaches projects

- Question and options: after a change merges, how should a new version reach the projects that use the plugin? A) tag and release automatically (recommended) B) the owner cuts releases himself
- Owner's words: "Tag and release automatically (Recommended)"
- Selects: A
- Does not cover: when a project picks the release up; each project updates the plugin itself
- Where recorded: the pull request that added the repository automation

### 2026-11-15 automatic merging

- Question and options: how far should automatic merging go? A) automatic with a locked core that still needs the owner (recommended) B) fully automatic, no exceptions C) automatic for text only
- Owner's words: "Fully automatic, no exceptions"
- Selects: B. Everything from the owner's account merges when the required check passes, the safety rules and the workflow files included
- Does not cover: pull requests from other accounts or from forks; removing the required check; a release of a version whose checks fail
- Where recorded: the pull request that added the repository automation

### 2026-11-15 set up the automation

- Question and options: none put; the owner asked for it
- Owner's words: "ok for superstack skills please setup cicd to let it do automerge with humanless and continue update seamlessly everytime"
- Selects: build automatic merging and automatic releases for this repository
- Does not cover: how far automatic merging goes, which the entry above settles
- Where recorded: the pull request that added the repository automation
