from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins" / "superstacks" / "skills" / "owner-decisions"
CHECK = SKILL / "scripts" / "check_decisions.py"
AUTH = SKILL / "scripts" / "authority.py"

GOOD = """# Decisions

## Standing rules

| Rule | Scope | Exceptions | Date | Source |
| --- | --- | --- | --- | --- |
| merge: the agent may merge its own PR after review | docs | locked paths | 2026-02-01 | 2026-02-01 merge policy |

## Decision log

### 2026-02-01 merge policy

- Question and options: Who merges docs PRs? A) human B) agent after a passing review
- Owner's words: "B, but only for docs and tests"
- Selects: B for docs and tests
- Does not cover: locked paths, deploys
- Where recorded: ticket comment
"""


def _run(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _ledger(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "DECISIONS.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_ledger_passes(tmp_path: Path) -> None:
    proc = _run(CHECK, str(_ledger(tmp_path, GOOD)))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_template_passes() -> None:
    proc = _run(CHECK, str(SKILL / "templates" / "DECISIONS.md"))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_missing_field_fails(tmp_path: Path) -> None:
    text = GOOD.replace("- Does not cover: locked paths, deploys\n", "")
    proc = _run(CHECK, str(_ledger(tmp_path, text)))
    assert proc.returncode == 1
    assert "2026-02-01 merge policy" in proc.stdout
    assert "Does not cover" in proc.stdout


def test_empty_quote_fails(tmp_path: Path) -> None:
    text = GOOD.replace('"B, but only for docs and tests"', '""')
    proc = _run(CHECK, str(_ledger(tmp_path, text)))
    assert proc.returncode == 1
    assert "Owner's words" in proc.stdout


def test_unquoted_words_fail(tmp_path: Path) -> None:
    text = GOOD.replace('"B, but only for docs and tests"', "B, but only for docs and tests")
    proc = _run(CHECK, str(_ledger(tmp_path, text)))
    assert proc.returncode == 1
    assert "quoted" in proc.stdout


def test_bad_date_fails(tmp_path: Path) -> None:
    text = GOOD.replace("### 2026-02-01 merge policy", "### 2026-13-45 merge policy")
    proc = _run(CHECK, str(_ledger(tmp_path, text)))
    assert proc.returncode == 1
    assert "date" in proc.stdout


def test_unsourced_rule_fails(tmp_path: Path) -> None:
    text = GOOD.replace("| 2026-02-01 | 2026-02-01 merge policy |", "| 2026-02-01 | 2026-03-09 no such entry |")
    proc = _run(CHECK, str(_ledger(tmp_path, text)))
    assert proc.returncode == 1
    assert "source" in proc.stdout


def test_authority_granted(tmp_path: Path) -> None:
    proc = _run(AUTH, str(_ledger(tmp_path, GOOD)), "merge")
    assert proc.returncode == 0
    assert "merge: the agent may merge its own PR" in proc.stdout
    assert "locked paths" in proc.stdout
    assert "DEFAULT" not in proc.stdout


def test_authority_not_granted(tmp_path: Path) -> None:
    proc = _run(AUTH, str(_ledger(tmp_path, GOOD)), "deploy")
    assert proc.returncode == 0
    assert proc.stdout.strip() == "DEFAULT: human"


def test_authority_missing_file(tmp_path: Path) -> None:
    proc = _run(AUTH, str(tmp_path / "nope.md"), "merge")
    assert proc.returncode == 0
    assert proc.stdout.strip() == "DEFAULT: human"


def test_authority_unsourced_rule_is_ignored(tmp_path: Path) -> None:
    text = GOOD.replace("| 2026-02-01 | 2026-02-01 merge policy |", "| 2026-02-01 |  |")
    proc = _run(AUTH, str(_ledger(tmp_path, text)), "merge")
    assert proc.stdout.strip() == "DEFAULT: human"


def test_authority_unknown_name(tmp_path: Path) -> None:
    proc = _run(AUTH, str(_ledger(tmp_path, GOOD)), "launch")
    assert proc.returncode == 2
