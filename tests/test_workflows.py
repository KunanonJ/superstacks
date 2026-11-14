"""Contract tests for the automation workflows. Parsed as text: no YAML dependency."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
NAMES = ("ci.yml", "automerge.yml", "release.yml")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _text(name: str) -> str:
    return (WORKFLOWS / name).read_text(encoding="utf-8")


def _jobs(text: str) -> dict[str, str]:
    """Split the `jobs:` block into {job id: body}."""
    body = text.split("\njobs:\n", 1)[1]
    parts = re.split(r"^  ([A-Za-z0-9_-]+):\n", body, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def _permissions(block: str) -> dict[str, str]:
    match = re.search(r"^\s*permissions:\n((?:\s+[a-z-]+: [a-z]+\n)+)", block, flags=re.M)
    assert match, "permissions block missing"
    return dict(re.findall(r"([a-z-]+): ([a-z]+)", match.group(1)))


def test_every_action_is_pinned_by_full_sha() -> None:
    for name in NAMES:
        uses = re.findall(r"^\s*(?:-\s*)?uses:\s*(\S+)", _text(name), flags=re.M)
        assert uses or name != "release.yml"
        for ref in uses:
            _, _, pin = ref.partition("@")
            assert SHA_RE.match(pin), f"{name}: {ref} is not pinned by a 40-character SHA"


def test_no_pull_request_target() -> None:
    for name in NAMES:
        assert "pull_request_target" not in _text(name), name


def test_no_new_third_party_actions() -> None:
    allowed = {"actions/checkout", "actions/setup-python", "actions/setup-node"}
    for name in NAMES:
        for ref in re.findall(r"^\s*(?:-\s*)?uses:\s*(\S+)", _text(name), flags=re.M):
            assert ref.split("@")[0] in allowed, f"{name}: {ref}"


def test_automerge_conditions() -> None:
    text = _text("automerge.yml")
    assert "github.event.pull_request.user.login == github.repository_owner" in text
    assert "github.event.pull_request.head.repo.full_name == github.repository" in text
    assert "github.event.pull_request.draft == false" in text
    assert "github.actor == 'dependabot[bot]'" in text
    for kind in ("opened", "reopened", "ready_for_review", "synchronize"):
        assert kind in text


def test_automerge_every_job_is_gated_and_least_privilege() -> None:
    jobs = _jobs(_text("automerge.yml"))
    assert len(jobs) == 2
    for job_id, body in jobs.items():
        assert _permissions(body) == {"contents": "write", "pull-requests": "write"}, job_id
        assert "gh pr merge --auto --squash" in body, job_id
        assert "github.event.pull_request.head.repo.full_name == github.repository" in body, job_id
        assert "github.event.pull_request.draft == false" in body, job_id


def test_automerge_passes_event_values_through_env() -> None:
    text = _text("automerge.yml")
    run_lines = [ln for ln in text.splitlines() if ln.strip().startswith("run:")]
    assert run_lines
    for line in run_lines:
        assert "${{" not in line, line
    assert "GH_TOKEN: ${{ github.token }}" in text
    assert "PR_URL: ${{ github.event.pull_request.html_url }}" in text


def test_ci_stays_read_only() -> None:
    assert _permissions("permissions:\n" + _text("ci.yml").split("permissions:\n", 1)[1]) == {"contents": "read"}


def test_release_permissions_and_triggers() -> None:
    text = _text("release.yml")
    jobs = _jobs(text)
    assert len(jobs) == 1
    assert _permissions(next(iter(jobs.values()))) == {"contents": "write"}
    assert "workflow_dispatch" in text
    assert re.search(r"^\s+schedule:\n\s+- cron: ", text, flags=re.M)
    assert re.search(r"^\s+push:\n\s+branches: \[main\]", text, flags=re.M)
    assert "concurrency:" in text
    assert "cancel-in-progress: false" in text


def test_release_runs_checks_before_creating_a_release() -> None:
    text = _text("release.yml")
    create = text.index("gh release create")
    for step in (
        "python -m ruff check app scripts tests",
        "python -m app.plugin_lint",
        "python -m pytest",
        "python scripts/check_archive_size.py",
        "python scripts/build_zips.py",
        "python scripts/release_plan.py",
    ):
        assert step in text, step
        assert text.index(step) < create, step


def test_release_only_from_main() -> None:
    assert "github.ref == 'refs/heads/main'" in _text("release.yml")


def test_no_contributor_triage_workflow() -> None:
    # A fork's token is read-only, so such a workflow could only fail. The rule lives in documents.
    assert not (WORKFLOWS / "contributor-triage.yml").exists()
