from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts import release_plan

ROOT = Path(__file__).resolve().parents[1]


def test_untagged_version_is_released() -> None:
    assert release_plan.plan("1.2.3", ["v1.2.2", "v1.0.0"]) == "RELEASE v1.2.3"


def test_tagged_version_is_skipped() -> None:
    assert release_plan.plan("1.2.3", ["v1.2.3", "v1.2.2"]) == "SKIP v1.2.3 already tagged"


def test_empty_tag_list_is_released() -> None:
    assert release_plan.plan("6.1.1", []) == "RELEASE v6.1.1"


@pytest.mark.parametrize("bad", ["", "1.2", "v1.2.3", "1.2.3-rc1", "1.2.x", " 1.2.3"])
def test_malformed_version_fails_clearly(bad: str) -> None:
    with pytest.raises(ValueError, match="not a MAJOR.MINOR.PATCH version"):
        release_plan.plan(bad, [])


def test_cli_reads_tags_from_stdin() -> None:
    script = ROOT / "scripts" / "release_plan.py"
    run = subprocess.run(
        [sys.executable, str(script), "--version", "2.0.0"],
        input="v1.0.0\nv2.0.0\n",
        check=False,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0
    assert run.stdout.strip() == "SKIP v2.0.0 already tagged"


def test_cli_fails_on_malformed_version() -> None:
    script = ROOT / "scripts" / "release_plan.py"
    run = subprocess.run(
        [sys.executable, str(script), "--version", "banana"],
        input="",
        check=False,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 1
    assert "not a MAJOR.MINOR.PATCH version" in run.stderr


def test_cli_defaults_to_the_plugin_version() -> None:
    script = ROOT / "scripts" / "release_plan.py"
    run = subprocess.run([sys.executable, str(script)], input="", check=False, capture_output=True, text=True)
    assert run.returncode == 0
    assert run.stdout.startswith("RELEASE v")
