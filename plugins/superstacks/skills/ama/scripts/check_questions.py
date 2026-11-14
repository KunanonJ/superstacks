#!/usr/bin/env python3
"""Validate an owner question sheet (QUESTIONS.md). One line per problem; exit 0 or 1."""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_QUESTIONS = 4
MIN_OPTIONS = 2
MAX_OPTIONS = 4
MAX_EXPLAIN_WORDS = 5

QUESTION_RE = re.compile(r"^##\s+Q(\d+)\.?\s*(.*?)\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s")
OPTION_RE = re.compile(r"^\|\s*([A-Za-z])\b([^|]*)\|")
NO_REC_RE = re.compile(r"^no recommendation because\s+\S", re.I)
REPLY_RE = re.compile(r"^\W*reply\b.*\b\d+[A-Za-z]\b", re.I)
JARGON_RE = re.compile(
    r"`[^`]+`"
    r"|(?:\b[\w.-]+/)+[\w.-]+"
    r"|\b[\w-]+\.(?:py|ts|tsx|js|jsx|json|md|yml|yaml|toml|sql)\b"
    r"|\b(?:API|endpoint|schema|refactor|migration)s?\b",
    re.I,
)
EXPLAIN_RE = re.compile(r"\s*\(([^()]*)\)")


def _jargon(question: str) -> list[str]:
    found: list[str] = []
    for match in JARGON_RE.finditer(question):
        term = match.group(0)
        if term.lower() == "api" and term != "API":
            continue
        explain = EXPLAIN_RE.match(question, match.end())
        if explain and len(explain.group(1).split()) <= MAX_EXPLAIN_WORDS:
            continue
        found.append(term)
    return found


def _kind(term: str) -> str:
    if term.startswith("`"):
        return "words in backticks"
    if "/" in term or "." in term:
        return "file path"
    return "jargon"


def check(text: str) -> list[str]:
    problems: list[str] = []
    questions: list[dict] = []
    current: dict | None = None
    in_fence = False
    reply = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        found = QUESTION_RE.match(stripped)
        if found:
            current = {"n": found.group(1), "text": found.group(2), "opts": 0, "rec": 0, "none": False}
            questions.append(current)
            continue
        if HEADING_RE.match(stripped):
            current = None
            continue
        if REPLY_RE.match(stripped):
            reply = True
        if current is None:
            continue
        option = OPTION_RE.match(stripped)
        if option:
            current["opts"] += 1
            if "recommended" in option.group(2).lower() and "not recommended" not in option.group(2).lower():
                current["rec"] += 1
        elif NO_REC_RE.match(stripped):
            current["none"] = True
    if not questions:
        problems.append("no questions found: each starts with a line like '## Q1. <question>'")
    if len(questions) > MAX_QUESTIONS:
        problems.append(f"{len(questions)} questions in this batch, at most {MAX_QUESTIONS}")
    for q in questions:
        tag = f"Q{q['n']}"
        if not MIN_OPTIONS <= q["opts"] <= MAX_OPTIONS:
            word = "option" if q["opts"] == 1 else "options"
            problems.append(f"{tag}: {q['opts']} {word}, needs {MIN_OPTIONS} to {MAX_OPTIONS}")
        if q["rec"] > 1:
            problems.append(f"{tag}: {q['rec']} Recommended marks, needs exactly one")
        elif q["rec"] == 0 and not q["none"]:
            problems.append(
                f"{tag}: no Recommended option and no 'No recommendation because ...' line"
            )
        for term in _jargon(q["text"]):
            problems.append(f"{tag}: {_kind(term)} in the question: {term}")
    if not reply:
        problems.append("no reply-format line, for example 'Reply with: 1A 2B'")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_questions.py QUESTIONS.md", file=sys.stderr)
        return 2
    try:
        text = Path(argv[1]).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read {argv[1]}: {exc.strerror}")
        return 1
    problems = check(text)
    for item in problems:
        print(item)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
