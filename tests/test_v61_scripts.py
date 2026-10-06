from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "superstacks" / "skills"


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verify_py_pass_and_fail() -> None:
    script = SKILLS / "verify-loop" / "scripts" / "verify.py"
    ok = subprocess.run(
        [sys.executable, str(script), "--", sys.executable, "-c", "raise SystemExit(0)"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert ok.returncode == 0
    assert "VERIFY_PASS" in ok.stdout
    bad = subprocess.run(
        [sys.executable, str(script), "--", sys.executable, "-c", "raise SystemExit(3)"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert bad.returncode == 3
    assert "VERIFY_FAIL" in bad.stdout


def test_check_pr_body() -> None:
    mod = _load(SKILLS / "pr" / "scripts" / "check_pr_body.py")
    good = """
Refs #12

## Plan
Ship the verify runner.

## Evidence
VERIFY_FAIL
VERIFY_PASS

## Merge Danger
**Door:** two-way
"""
    assert mod.check(good) == []
    assert any("Refs" in e for e in mod.check("## Plan\nx\n## Evidence\nVERIFY_PASS\n## Risk\nDoor: two-way\n"))
    assert any("Closes" in e for e in mod.check(good.replace("Refs #12", "Closes #12")))
    missing_verify = good.replace("VERIFY_FAIL\nVERIFY_PASS", "looks fine")
    assert any("VERIFY_" in e for e in mod.check(missing_verify))


def test_pipeline_status() -> None:
    mod = _load(SKILLS / "ticket-pipeline" / "scripts" / "pipeline_status.py")
    body = """
## How
model

## Plan
do the thing

VERIFY_FAIL
VERIFY_PASS

## TDD
red-green

## Evidence
pasted

## Code review
ok

N/A (two-way door)

Refs #3
"""
    rows = dict(mod.evaluate(body))
    assert all(rows.values()), rows
    empty = dict(mod.evaluate("hello"))
    assert empty["how"] is False
    assert empty["pr"] is False


def test_check_brief() -> None:
    mod = _load(SKILLS / "intake-triage" / "scripts" / "check_brief.py")
    good = """
## Goal
Fix the leak.

## Scope
in: parser / out: rewrite

## Acceptance
no leak on sample

## Verify
python -m pytest tests/test_parser.py

## Forbidden
no runtime installs

## Door
two-way
"""
    assert mod.check(good) == []
    template = (SKILLS / "intake-triage" / "templates" / "BRIEF.md").read_text(encoding="utf-8")
    errors = mod.check(template)
    assert errors


def test_mine_transcripts(tmp_path: Path) -> None:
    script = SKILLS / "steer-miner" / "scripts" / "mine_transcripts.py"
    sample = tmp_path / "t.txt"
    sample.write_text(
        "don't use that API, use the other one instead\n" * 3
        + "hello world\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(script), "--path", str(sample), "--min-count", "2"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "don't use that api" in proc.stdout.lower() or "dont use that api" in proc.stdout.lower()


def test_snapshot_template_usage() -> None:
    script = SKILLS / "verify-loop" / "scripts" / "check-snapshot-console.cjs"
    proc = subprocess.run(
        ["node", str(script)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "usage:" in proc.stderr


def test_verify_loop_is_model_invoked() -> None:
    from app import plugin_lint

    assert "verify-loop" not in plugin_lint.USER_INVOKED
    fields = plugin_lint._frontmatter((SKILLS / "verify-loop" / "SKILL.md").read_text(encoding="utf-8"))
    assert fields.get("disable-model-invocation") != "true"
