from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "superstacks" / "skills"


def _text(*parts: str) -> str:
    return SKILLS.joinpath(*parts).read_text(encoding="utf-8")


def test_tdd_second_path_for_stored_values() -> None:
    body = _text("test-driven-development", "SKILL.md")
    assert "## Tests That Cannot See the Defect" in body
    assert "second path" in body
    assert "not UTC" in body


def test_tdd_printed_is_not_asserted() -> None:
    body = _text("test-driven-development", "SKILL.md")
    assert "Printed is not asserted" in body
    assert "assertion that can fail" in body


def test_tdd_write_skew_and_gated_overlap() -> None:
    body = _text("test-driven-development", "SKILL.md")
    assert "write skew" in body
    assert "first-of-a-kind" in body
    assert "time limit" in body


def test_verification_reading_is_a_hypothesis() -> None:
    body = _text("verification-before-completion", "SKILL.md")
    assert "A reading of the source is a hypothesis" in body
    assert "last hop" in body


def test_verification_runs_whole_tree_guards() -> None:
    body = _text("verification-before-completion", "SKILL.md")
    assert "whole-tree guard" in body
    assert "scoped to the changed folder" in body


def test_interrogate_checks_logged_but_not_asserted() -> None:
    rubric = _text("interrogate", "references", "rubric.md")
    assert "logged and not asserted" in rubric
    assert "write skew" in rubric.lower()
    lead = _text("interrogate", "references", "lead-judgment.md")
    assert "failing test" in lead
    assert "last hop" in lead


def _trigger_block(skill: str) -> str:
    lines = (ROOT / "evals" / "triggers.yaml").read_text(encoding="utf-8").splitlines()
    block: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("  ") and not line.startswith("    ") and line.strip().endswith(":"):
            inside = line.strip() == f"{skill}:"
            continue
        if inside:
            block.append(line.strip())
    return "\n".join(block)


def test_triggers_cover_new_guidance() -> None:
    tdd = _trigger_block("test-driven-development")
    assert "- the test reads the timestamp back through the same code that wrote it" in tdd
    assert "- two requests insert the first row at the same time" in tdd
    assert "- the test prints the count but asserts nothing" in tdd
    assert "- my reading of the library says it is safe but a test fails" in _trigger_block("interrogate")
    assert "- my change passes its folder tests, what else runs before I push" in _trigger_block(
        "verification-before-completion"
    )
