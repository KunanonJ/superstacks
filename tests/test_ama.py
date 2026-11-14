from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins" / "superstacks" / "skills" / "ama"
CHECK = SKILL / "scripts" / "check_questions.py"

HEAD = """# Questions

Batch 1 of 1. Most important first.

"""

TAIL = """
Reply with: 1A 2B
You can also answer "Not sure, you choose" or write your own answer in your own words.
"""


def _q(n: int, text: str = "Should new people sign up with just an email?", opts: int = 2, rec: int = 1) -> str:
    rows = []
    for i in range(opts):
        letter = "ABCD"[i]
        mark = " (Recommended)" if i < rec else ""
        rows.append(f"| {letter}{mark} | Short sign-up | About 2 days | Fewer details at first |")
    table = "\n".join(rows)
    return (
        f"## Q{n}. {text}\n\n"
        "| Option | What you get | What it costs | What you give up |\n"
        "| --- | --- | --- | --- |\n"
        f"{table}\n\n"
    )


def _sheet(*questions: str, tail: str = TAIL) -> str:
    return HEAD + "".join(questions) + tail


def _run(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECK), str(path)],
        check=False,
        capture_output=True,
        text=True,
    )


def _check(tmp_path: Path, text: str) -> subprocess.CompletedProcess:
    path = tmp_path / "QUESTIONS.md"
    path.write_text(text, encoding="utf-8")
    return _run(path)


def test_good_sheet_passes(tmp_path: Path) -> None:
    proc = _check(tmp_path, _sheet(_q(1), _q(2, opts=3), _q(3, opts=4)))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout == ""


def test_template_passes() -> None:
    proc = _run(SKILL / "templates" / "QUESTIONS.md")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_five_questions_fail(tmp_path: Path) -> None:
    proc = _check(tmp_path, _sheet(*[_q(i) for i in range(1, 6)]))
    assert proc.returncode == 1
    assert "5 questions" in proc.stdout
    assert "at most 4" in proc.stdout


def test_one_option_fails(tmp_path: Path) -> None:
    proc = _check(tmp_path, _sheet(_q(1, opts=1)))
    assert proc.returncode == 1
    assert "Q1" in proc.stdout
    assert "1 option" in proc.stdout


def test_five_options_fail(tmp_path: Path) -> None:
    text = _sheet(_q(1, opts=4)).replace(
        "| D | Short", "| D | Short sign-up | x | y |\n| E | Short", 1
    )
    proc = _check(tmp_path, text)
    assert proc.returncode == 1
    assert "5 options" in proc.stdout


def test_two_recommended_fail(tmp_path: Path) -> None:
    proc = _check(tmp_path, _sheet(_q(1, rec=2)))
    assert proc.returncode == 1
    assert "Q1" in proc.stdout
    assert "2 Recommended" in proc.stdout


def test_no_recommended_fails(tmp_path: Path) -> None:
    proc = _check(tmp_path, _sheet(_q(1, rec=0)))
    assert proc.returncode == 1
    assert "no Recommended" in proc.stdout


def test_explicit_no_recommendation_passes(tmp_path: Path) -> None:
    q = _q(1, rec=0) + "No recommendation because the cost of the email service is not known yet.\n\n"
    proc = _check(tmp_path, _sheet(q))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_no_reply_line_fails(tmp_path: Path) -> None:
    proc = _check(tmp_path, _sheet(_q(1), tail="\nNot sure, you choose.\n"))
    assert proc.returncode == 1
    assert "reply" in proc.stdout.lower()


def test_jargon_in_question_fails(tmp_path: Path) -> None:
    proc = _check(tmp_path, _sheet(_q(1, text="Should we change the schema for sign-up?")))
    assert proc.returncode == 1
    assert "Q1" in proc.stdout
    assert "schema" in proc.stdout


def test_backtick_and_path_jargon_fail(tmp_path: Path) -> None:
    proc = _check(tmp_path, _sheet(_q(1, text="Should `signup` in src/auth/login.ts stay?")))
    assert proc.returncode == 1
    assert "`signup`" in proc.stdout
    assert "path" in proc.stdout


def test_jargon_with_short_explanation_passes(tmp_path: Path) -> None:
    text = "Should the API (how the apps talk) stay the same?"
    proc = _check(tmp_path, _sheet(_q(1, text=text)))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_jargon_with_long_explanation_fails(tmp_path: Path) -> None:
    text = "Should the API (the way that all of our apps talk to us) stay the same?"
    proc = _check(tmp_path, _sheet(_q(1, text=text)))
    assert proc.returncode == 1
    assert "API" in proc.stdout


def test_no_questions_fails(tmp_path: Path) -> None:
    proc = _check(tmp_path, HEAD + TAIL)
    assert proc.returncode == 1
    assert "no questions" in proc.stdout


def test_missing_file_fails(tmp_path: Path) -> None:
    proc = _run(tmp_path / "nope.md")
    assert proc.returncode == 1
