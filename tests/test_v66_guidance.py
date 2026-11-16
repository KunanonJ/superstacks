from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "superstacks" / "skills"


def _text(*parts: str) -> str:
    return SKILLS.joinpath(*parts).read_text(encoding="utf-8")


def test_writing_plans_has_call_that_changes_another_system() -> None:
    body = _text("writing-plans", "SKILL.md")
    assert "## A call that changes another system" in body
    assert "you never read the answer" in body
    assert "Write what you are about to do before you do it." in body
    assert "Count the requests sent (before each send)" in body
    assert "only when the two counts are equal" in body
    assert "Name a closing state by what was proven." in body
    assert "no verified time" in body
    assert "a fake of the other system that applies the change and then fails the call" in body


def test_writing_plans_section_sits_before_self_review() -> None:
    body = _text("writing-plans", "SKILL.md")
    assert body.index("## A call that changes another system") < body.index("## Self-Review")


def test_interrogate_walks_the_lost_answer() -> None:
    rubric = _text("interrogate", "references", "rubric.md")
    assert "walk the lost answer" in rubric
    assert 'close the work as "nothing to do", that is a finding' in rubric
    assert "name the reply that proves it" in rubric
    assert 'must not carry the same "verified" mark' in rubric
    assert "an old status can confirm a new request" in rubric
    assert "newer than a time the caller stored before sending" in rubric


def test_tdd_has_the_lost_answer_test_shape() -> None:
    body = _text("test-driven-development", "SKILL.md")
    assert "### The lost answer" in body
    assert "then fail the call with a timeout" in body
    assert 'not closed as "nothing to do"' in body
    assert "A mock that fails without applying the change cannot see this defect" in body
    section = body.index("## Tests That Cannot See the Defect")
    assert section < body.index("### The lost answer") < body.index("## Common Rationalizations")


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
    assert "- the plan has a step that deletes a record in another system" in _trigger_block("writing-plans")
    assert "- the call timed out after the other system applied the change" in _trigger_block("test-driven-development")
    assert "- the retry closed the work as nothing to do after a timeout" in _trigger_block("interrogate")
