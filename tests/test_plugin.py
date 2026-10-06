from __future__ import annotations

import json
import struct
import zipfile
from pathlib import Path

from app import plugin_lint
from scripts.build_zips import build

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "superstacks"


def test_linter_clean() -> None:
    assert plugin_lint.run() == 0


def test_plugin_name_matches_folder() -> None:
    assert PLUGIN.name == "superstacks"
    for rel in (
        ".claude-plugin/plugin.json",
        ".cursor-plugin/plugin.json",
        ".codex-plugin/plugin.json",
    ):
        data = json.loads((PLUGIN / rel).read_text(encoding="utf-8"))
        assert data["name"] == "superstacks"
        assert data["displayName"] == "Superstacks"
        assert data["version"] == plugin_lint.PLUGIN_VERSION


def test_no_root_plugin_json() -> None:
    assert not (ROOT / "plugin.json").exists()


def test_no_legacy_name_in_tree() -> None:
    needle = plugin_lint.LEGACY_NAME
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix not in {".md", ".json", ".yml", ".yaml", ".py", ".toml"}:
            continue
        if path.name == "plugin_lint.py":
            continue
        text = path.read_text(encoding="utf-8")
        assert needle not in text.lower(), path


def test_skill_frontmatter() -> None:
    for skill_dir in sorted((PLUGIN / "skills").iterdir()):
        if not skill_dir.is_dir():
            continue
        fields = plugin_lint._frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        assert fields["name"] == skill_dir.name
        assert fields["license"] == "MIT"
        assert len(fields["description"]) <= 200
        desc = fields["description"]
        assert desc.startswith("Use when") or desc.startswith("Use for")


def test_codex_interface() -> None:
    data = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert data["skills"] == "./skills/"
    iface = data["interface"]
    assert iface["displayName"] == "Superstacks"
    assert len(iface["shortDescription"]) <= 30
    assert iface["category"] == "Developer Tools"
    assert iface["capabilities"] == [
        "Plan in the PR body",
        "TDD and verify-loop",
        "Two-axis code review",
        "Draft PRs only",
    ]
    assert 1 <= len(iface["defaultPrompt"]) <= 3
    assert all(isinstance(item, str) and 0 < len(item) <= 128 for item in iface["defaultPrompt"])
    assert "screenshots" not in iface
    assert iface["composerIcon"] == "./assets/icon.png"
    assert iface["logo"] == "./assets/logo.png"
    notes = data["extensions"]["com.openai"]["publication"]["release_notes"]
    assert isinstance(notes, str) and notes.strip()


def test_marketplaces() -> None:
    claude = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    cursor = json.loads((ROOT / ".cursor-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    agents_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    agents = json.loads(agents_path.read_text(encoding="utf-8"))
    assert claude["plugins"][0]["source"] == "./plugins/superstacks"
    assert claude["metadata"]["description"] == (
        "Lean MIT skill stack for coding agents: plans, TDD, verify-loop, "
        "constraints, review, PRs, and ticket pipelines."
    )
    assert cursor["plugins"][0]["source"] == "plugins/superstacks"
    source = agents["plugins"][0]["source"]
    assert source == {"source": "local", "path": "./plugins/superstacks"}
    policy = agents["plugins"][0]["policy"]
    assert "installation" in policy and "authentication" in policy
    assert "category" in agents["plugins"][0]


def test_plugin_readme_word_count() -> None:
    text = (PLUGIN / "README.md").read_text(encoding="utf-8")
    # Strip fenced code blocks, then count words.
    stripped = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            stripped.append(line)
    words = [w for w in " ".join(stripped).split() if w]
    assert len(words) >= 40


def _png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", data[16:24])


def test_logo_assets() -> None:
    svg = PLUGIN / "assets" / "logo.svg"
    png = PLUGIN / "assets" / "logo.png"
    icon = PLUGIN / "assets" / "icon.png"
    icon64 = PLUGIN / "assets" / "icon-64.png"
    icon16 = PLUGIN / "assets" / "icon-16.png"
    assert svg.is_file()
    assert png.is_file()
    assert icon.is_file()
    assert icon64.is_file()
    assert icon16.is_file()
    width, height = _png_size(png)
    assert (width, height) == (512, 512)
    assert _png_size(icon) == (256, 256)
    assert _png_size(icon64) == (64, 64)
    assert _png_size(icon16) == (16, 16)
    assert 'viewBox="0 0 512 512"' in svg.read_text(encoding="utf-8")
    social = ROOT / ".github" / "social-preview.png"
    assert social.is_file()
    assert _png_size(social) == (1280, 640)


def test_no_banned_plugin_dirs() -> None:
    for name in ("commands", "agents", "hooks"):
        assert not (PLUGIN / name).exists()


def test_build_zips(tmp_path: Path) -> None:
    written = build(tmp_path)
    names = {path.name for path in written}
    assert "superstacks-plugin.zip" in names
    assert "writing-plans.zip" in names
    assert "verify-loop.zip" in names
    skill_zip = tmp_path / "writing-plans.zip"
    with zipfile.ZipFile(skill_zip) as zf:
        assert "writing-plans/SKILL.md" in zf.namelist()
    flat_zip = tmp_path / "flat" / "writing-plans.zip"
    with zipfile.ZipFile(flat_zip) as zf:
        names = zf.namelist()
        assert "SKILL.md" in names
        assert "writing-plans/SKILL.md" not in names
    plugin_zip = tmp_path / "superstacks-plugin.zip"
    with zipfile.ZipFile(plugin_zip) as zf:
        assert "superstacks/.codex-plugin/plugin.json" in zf.namelist()


def test_sources_lock_pins() -> None:
    lock = json.loads((ROOT / "sources.lock.json").read_text(encoding="utf-8"))
    shas = {entry["sha"] for entry in lock["sources"] if "sha" in entry}
    assert "8ca22dba9a94f28898bbce59f2537ff4d87c747d" in shas
    assert "4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d" in shas
    assert "e5a8186d7b43be8d6ac4452440fbead5f1a51c70" in shas
