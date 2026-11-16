from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "superstacks" / "skills"


def _text(*parts: str) -> str:
    return SKILLS.joinpath(*parts).read_text(encoding="utf-8")


def test_verification_has_suites_nobody_runs_for_you() -> None:
    body = _text("verification-before-completion", "SKILL.md")
    assert "## Suites Nobody Runs For You" in body
    assert "neither the pipeline nor the pre-push hook runs" in body
    assert "suites that need a real database or another service" in body
    assert "suites that compare against recorded output" in body
    assert "suites behind an environment flag" in body
    assert "fail silently on the main branch until someone runs them by hand" in body
    assert "for every folder your change touches and run them" in body
    assert "break a recorded suite in a folder you never opened" in body


def test_verification_has_no_shared_file_is_not_independence() -> None:
    body = _text("verification-before-completion", "SKILL.md")
    heading = "## No Shared File Is Not Independence"
    assert heading in body
    assert "list every exported function, type or file format whose signature or meaning each one changes" in body
    assert "search the other branch for each name" in body
    assert "each passes alone and the main branch fails after the second merge" in body
    assert "Report the result of the search, not the list of files." in body


def test_verification_sections_sit_in_order() -> None:
    body = _text("verification-before-completion", "SKILL.md")
    reading = body.index("## A Reading Is Not Evidence")
    suites = body.index("## Suites Nobody Runs For You")
    independence = body.index("## No Shared File Is Not Independence")
    assert reading < suites < independence < body.index("## Common Failures")


def test_tdd_has_a_setting_meant_to_last_for_one_transaction() -> None:
    body = _text("test-driven-development", "SKILL.md")
    heading = "### A setting meant to last for one transaction"
    assert heading in body
    assert "the next caller on that pooled connection inherits it" in body
    assert "Test it on a pool of exactly one connection" in body
    assert "read the setting and the connection's identity before the call and after it" in body
    assert "The identity check stops a silent reconnect from passing the test." in body
    assert "Then flip the scope by hand once and watch the test fail." in body
    section = body.index("## Tests That Cannot See the Defect")
    assert section < body.index("### The lost answer") < body.index(heading) < body.index("## Common Rationalizations")


def test_tdd_section_intro_counts_its_cases() -> None:
    body = _text("test-driven-development", "SKILL.md")
    assert "Five cases come up again and again." in body
    assert "Four cases come up again and again." not in body


def test_interrogate_rubric_reports_a_break_no_test_catches() -> None:
    rubric = _text("interrogate", "references", "rubric.md")
    assert "A break made by hand that no test catches is a finding even when the shipped code is right." in rubric
    assert "name the smallest test that would catch it" in rubric
    assert "say which flag or line you flipped, so the author can repeat the proof" in rubric


def test_writing_plans_has_generated_lists_section() -> None:
    body = _text("writing-plans", "SKILL.md")
    heading = "## Generated Lists That Every Open Change Rewrites"
    assert heading in body
    assert "holds whole-tree numbers makes each merge a conflict for every other open change" in body
    assert "Split it in two." in body
    assert "**Rows.**" in body
    assert "sorted by key, with an empty line between rows" in body
    assert "a test compares them with a fresh scan" in body
    assert "**Totals.**" in body
    assert "no test compares them" in body
    assert "two changes to one row" in body
    assert "it can merge without a conflict into a row that is wrong" in body
    assert "regenerate the rows after every merge of the main branch, not only when a conflict is reported" in body
    assert "no dates, no machine paths, no counts that another change can move" in body
    assert "Run its guard from every path that can change the source." in body
    assert body.index("## A call that changes another system") < body.index(heading) < body.index("## Self-Review")


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
    verification = _trigger_block("verification-before-completion")
    assert "- which test suites does neither the pipeline nor the pre-push hook run" in verification
    assert "- these two open PRs share no file, can I call them independent" in verification
    assert "- the statement time limit leaked to the next caller on the pooled connection" in _trigger_block(
        "test-driven-development"
    )
    assert "- I flipped the flag by hand and no test failed" in _trigger_block("interrogate")
    assert "- every open PR conflicts on the generated inventory file" in _trigger_block("writing-plans")
