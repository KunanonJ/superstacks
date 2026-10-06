"""Lint Superstacks plugin layout, manifests, and skill frontmatter."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "superstacks"
PLUGIN_NAME = "superstacks"
PLUGIN_VERSION = "6.1.1"
MAX_NAME = 64
MAX_DESC = 200
MAX_NON_IMAGE = 256 * 1024
MAX_PLUGIN_FILES = 512
MAX_SHORT_DESC = 30
IMAGE_SUFFIXES = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
BINARY_SUFFIXES = {".exe", ".dll", ".so", ".dylib", ".bin", ".wasm", ".o", ".a", ".class"}
LOCKFILES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "Cargo.lock",
    "poetry.lock",
    "Pipfile.lock",
}
FORBIDDEN_NAME_TOKENS = ("claude", "cursor", "openai", "official", "plugin", "mcp", "test")
LEGACY_NAME = "super" + "skills"
COMPANY_RE = re.compile(
    "go" + "gocash|" + "go" + "go.?cash|" + r"\bGO" + r"GO\b",
    re.I,
)
PRODUCT_RE = re.compile(r"\b(claude|cursor|codex)\b", re.I)
LFS_RE = re.compile(r"^version https://git-lfs\.github\.com/spec/v1", re.M)
SECRET_RE = re.compile(
    r"(AKIA[0-9A-Z]{16})|(-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)"
    r"|api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]"
    r"|secret\s*[:=]\s*['\"][^'\"]+['\"]"
    r"|password\s*[:=]\s*['\"][^'\"]+['\"]",
    re.I,
)
UNPINNED_NPX_RE = re.compile(r"\b(?:npx|uvx)\s+(?!-)")
TRIGGER_RE = re.compile(r"^Use (when|for)\b")
USER_INVOKED = {
    "how",
    "interrogate",
    "grill-with-docs",
    "ticket-pipeline",
    "workflow-profile",
    "mistake-to-constraint",
    "steer-miner",
    "intake-triage",
    "gardening",
    "sample-review",
}


class LintError(Exception):
    pass


def _load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LintError(f"{path}: invalid JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise LintError(f"{path}: expected object")
    return data


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        raise LintError("missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise LintError("unterminated YAML frontmatter")
    fields: dict[str, str] = {}
    for raw_line in parts[1].splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.startswith(" "):
            continue
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def _check_ident(name: str, where: str) -> list[str]:
    errors: list[str] = []
    if not name:
        errors.append(f"{where}: empty name")
        return errors
    if len(name) > MAX_NAME:
        errors.append(f"{where}: name longer than {MAX_NAME} chars")
    if "--" in name:
        errors.append(f"{where}: name contains '--'")
    if name != name.lower() or any(ch.isspace() for ch in name):
        errors.append(f"{where}: name must be lowercase kebab-case")
    lowered = name.lower()
    for token in FORBIDDEN_NAME_TOKENS:
        if token in lowered.split("-") or lowered == token:
            errors.append(f"{where}: name must not contain '{token}'")
        elif f"-{token}-" in f"-{lowered}-":
            errors.append(f"{where}: name must not contain '{token}'")
    return errors


def _iter_plugin_files() -> list[Path]:
    files: list[Path] = []
    for path in PLUGIN_DIR.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        files.append(path)
    return files


def check_layout() -> list[str]:
    errors: list[str] = []
    if (ROOT / "plugin.json").exists():
        errors.append("root plugin.json is not allowed")
    if PLUGIN_DIR.name != PLUGIN_NAME:
        errors.append(f"plugin folder must be {PLUGIN_NAME}")
    for banned in ("commands", "agents", "hooks"):
        if (PLUGIN_DIR / banned).exists():
            errors.append(f"plugin must not contain {banned}/")
    if (ROOT / ".DS_Store").exists() or (PLUGIN_DIR / ".DS_Store").exists():
        errors.append(".DS_Store must not be committed")
    return errors


def check_manifests() -> list[str]:
    errors: list[str] = []
    claude = _load_json(PLUGIN_DIR / ".claude-plugin" / "plugin.json")
    cursor = _load_json(PLUGIN_DIR / ".cursor-plugin" / "plugin.json")
    codex = _load_json(PLUGIN_DIR / ".codex-plugin" / "plugin.json")
    for label, data in (("claude", claude), ("cursor", cursor), ("codex", codex)):
        errors.extend(_check_ident(str(data.get("name", "")), f"{label} plugin.json name"))
        if data.get("name") != PLUGIN_NAME:
            errors.append(f"{label} plugin.json name must equal folder {PLUGIN_NAME}")
        if data.get("version") != PLUGIN_VERSION:
            errors.append(f"{label} plugin.json version must be {PLUGIN_VERSION}")
        desc = str(data.get("description", ""))
        if len(desc) > MAX_DESC:
            errors.append(f"{label} plugin.json description longer than {MAX_DESC}")
        if not TRIGGER_RE.match(desc):
            errors.append(f"{label} plugin.json description must start with Use when/Use for")
        for field in ("displayName", "author", "homepage", "repository", "license", "keywords"):
            if label != "codex" and field not in data and field != "displayName":
                errors.append(f"{label} plugin.json missing {field}")
        if data.get("displayName") != "Superstacks":
            errors.append(f"{label} plugin.json displayName must be Superstacks")
        for key, value in data.items():
            if isinstance(value, str) and ".." in Path(value).parts:
                errors.append(f"{label} plugin.json path traversal in {key}")
            if isinstance(value, str) and value.startswith("/") and key in {"logo", "skills"}:
                errors.append(f"{label} plugin.json {key} must be relative")
    if cursor.get("logo") in (None, ""):
        errors.append("cursor plugin.json missing logo")
    elif str(cursor["logo"]).startswith("/") or ".." in Path(str(cursor["logo"])).parts:
        errors.append("cursor plugin.json logo must be a relative path without ..")
    if codex.get("skills") != "./skills/":
        errors.append('codex plugin.json skills must be "./skills/"')
    iface = codex.get("interface")
    if not isinstance(iface, dict):
        errors.append("codex plugin.json missing interface object")
    else:
        for field in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
            "capabilities",
            "composerIcon",
            "logo",
        ):
            if field not in iface:
                errors.append(f"codex interface missing {field}")
        short = str(iface.get("shortDescription", ""))
        if len(short) > MAX_SHORT_DESC:
            errors.append(f"codex shortDescription longer than {MAX_SHORT_DESC}")
        if iface.get("displayName") != "Superstacks":
            errors.append("codex interface.displayName must be Superstacks")
        if iface.get("category") != "Developer Tools":
            errors.append('codex category must be "Developer Tools"')
        caps = iface.get("capabilities")
        if not isinstance(caps, list) or not caps or any(
            not isinstance(item, str) or not item.strip() for item in caps
        ):
            errors.append("codex capabilities must be a non-empty string array")
        prompts = iface.get("defaultPrompt")
        if not isinstance(prompts, list) or not (1 <= len(prompts) <= 3):
            errors.append("codex defaultPrompt must be 1-3 strings")
        elif any(not isinstance(item, str) or not item.strip() or len(item) > 128 for item in prompts):
            errors.append("codex defaultPrompt entries must be non-empty and at most 128 chars")
        if iface.get("screenshots"):
            errors.append("codex screenshots must be omitted")
        for key in ("composerIcon", "logo"):
            value = str(iface.get(key, ""))
            if not value.startswith("./"):
                errors.append(f"codex interface.{key} must start with ./")
        openai_ext = codex.get("extensions", {})
        if not isinstance(openai_ext, dict):
            openai_ext = {}
        openai = openai_ext.get("com.openai", {})
        publication = openai.get("publication", {}) if isinstance(openai, dict) else {}
        notes = publication.get("release_notes") if isinstance(publication, dict) else None
        if not isinstance(notes, str) or not notes.strip():
            errors.append("codex extensions.com.openai.publication.release_notes is required")
    return errors


def check_marketplaces() -> list[str]:
    errors: list[str] = []
    claude = _load_json(ROOT / ".claude-plugin" / "marketplace.json")
    cursor = _load_json(ROOT / ".cursor-plugin" / "marketplace.json")
    agents = _load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    for label, data, source in (
        ("claude marketplace", claude, "./plugins/superstacks"),
        ("cursor marketplace", cursor, "plugins/superstacks"),
    ):
        errors.extend(_check_ident(str(data.get("name", "")), f"{label} name"))
        plugins = data.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            errors.append(f"{label}: plugins array required")
            continue
        entry = plugins[0]
        errors.extend(_check_ident(str(entry.get("name", "")), f"{label} plugin name"))
        if entry.get("name") != PLUGIN_NAME:
            errors.append(f"{label} plugin name must be {PLUGIN_NAME}")
        if entry.get("source") != source:
            errors.append(f"{label} source must be {source}")
    meta = claude.get("metadata")
    if not isinstance(meta, dict) or not str(meta.get("description", "")).strip():
        errors.append("claude marketplace missing metadata.description")
    errors.extend(_check_ident(str(agents.get("name", "")), "agents marketplace name"))
    plugins = agents.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("agents marketplace: plugins array required")
        return errors
    entry = plugins[0]
    errors.extend(_check_ident(str(entry.get("name", "")), "agents marketplace plugin name"))
    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "local":
        errors.append("agents marketplace source must be local")
    elif source.get("path") != "./plugins/superstacks":
        errors.append("agents marketplace path must be ./plugins/superstacks")
    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append("agents marketplace missing policy")
    else:
        if "installation" not in policy or "authentication" not in policy:
            errors.append("agents marketplace policy needs installation and authentication")
    if "category" not in entry:
        errors.append("agents marketplace missing category")
    return errors


def check_skills() -> list[str]:
    errors: list[str] = []
    skill_root = PLUGIN_DIR / "skills"
    for skill_dir in sorted(p for p in skill_root.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue
        try:
            fields = _frontmatter(skill_md.read_text(encoding="utf-8"))
        except LintError as exc:
            errors.append(f"{skill_md}: {exc}")
            continue
        name = fields.get("name", "")
        if name != skill_dir.name:
            errors.append(f"{skill_md}: name '{name}' != folder '{skill_dir.name}'")
        if name != "test-driven-development":
            errors.extend(_check_ident(name, f"{skill_md} name"))
        if name == "test-driven-development":
            if len(name) > MAX_NAME or "--" in name:
                errors.append(f"{skill_md}: invalid name length or '--'")
        desc = fields.get("description", "")
        if len(desc) > MAX_DESC:
            errors.append(f"{skill_md}: description {len(desc)} > {MAX_DESC}")
        if not TRIGGER_RE.match(desc):
            errors.append(f"{skill_md}: description must start with Use when/Use for")
        if fields.get("license") != "MIT":
            errors.append(f"{skill_md}: missing license: MIT frontmatter")
        invoked = fields.get("disable-model-invocation") == "true"
        if skill_dir.name in USER_INVOKED and not invoked:
            errors.append(f"{skill_md}: expected disable-model-invocation: true")
        if skill_dir.name not in USER_INVOKED and invoked:
            errors.append(f"{skill_md}: unexpected disable-model-invocation")
    return errors


def check_files() -> list[str]:
    errors: list[str] = []
    files = _iter_plugin_files()
    if len(files) > MAX_PLUGIN_FILES:
        errors.append(f"plugin has {len(files)} files; max {MAX_PLUGIN_FILES}")
    for path in files:
        rel = path.relative_to(PLUGIN_DIR)
        if path.is_symlink() or rel.is_symlink():
            errors.append(f"{rel}: symlinks are not allowed")
            continue
        if path.name == ".DS_Store":
            errors.append(f"{rel}: .DS_Store is not allowed")
        if path.name in LOCKFILES:
            errors.append(f"{rel}: lockfile/package manifest is not allowed")
        suffix = path.suffix.lower()
        size = path.stat().st_size
        if suffix in BINARY_SUFFIXES:
            errors.append(f"{rel}: binary suffix is not allowed")
        if suffix not in IMAGE_SUFFIXES and size > MAX_NON_IMAGE:
            errors.append(f"{rel}: non-image file exceeds 256 KiB")
        data = path.read_bytes()
        if (
            data.startswith(b"\x7fELF")
            or data.startswith(b"MZ")
            or data.startswith(b"\xca\xfe\xba\xbe")
        ):
            errors.append(f"{rel}: binary contents are not allowed")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            if suffix not in IMAGE_SUFFIXES:
                errors.append(f"{rel}: non-utf8 non-image file")
            continue
        if LFS_RE.search(text):
            errors.append(f"{rel}: Git LFS pointer files are not allowed")
        if SECRET_RE.search(text):
            errors.append(f"{rel}: credential-like material is not allowed")
        if COMPANY_RE.search(text):
            errors.append(f"{rel}: company/infra name is not allowed")
        if LEGACY_NAME in text.lower():
            errors.append(f"{rel}: leftover {LEGACY_NAME} name")
        in_skill_or_rule = rel.parts[0] in {"skills", "rules"}
        if in_skill_or_rule and PRODUCT_RE.search(text):
            errors.append(f"{rel}: skill/rule body must be product-neutral")
        if in_skill_or_rule and UNPINNED_NPX_RE.search(text):
            errors.append(f"{rel}: unpinned npx/uvx is not allowed")
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if path.name == "plugin_lint.py":
            continue
        if COMPANY_RE.search(text):
            errors.append(f"{path.relative_to(ROOT)}: company/infra name is not allowed")
        if path.suffix in {".md", ".json", ".yml", ".yaml", ".py"} and LEGACY_NAME in text.lower():
            errors.append(f"{path.relative_to(ROOT)}: leftover {LEGACY_NAME} name")
    return errors


def always_loaded_report() -> str:
    bits: list[str] = []
    for skill_dir in sorted((PLUGIN_DIR / "skills").iterdir()):
        if not skill_dir.is_dir():
            continue
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        fields = _frontmatter(text)
        if fields.get("disable-model-invocation") == "true":
            continue
        bits.append(fields.get("description", ""))
    rule = PLUGIN_DIR / "rules" / "safety-overrides.mdc"
    bits.append(rule.read_text(encoding="utf-8"))
    blob = "\n".join(bits)
    words = len(re.findall(r"\S+", blob))
    tokens = max(1, round(words / 0.75))
    return f"always-loaded ~{tokens} tokens ({words} words, {len(blob)} chars)"


def run() -> int:
    errors: list[str] = []
    if not PLUGIN_DIR.is_dir():
        print(f"missing {PLUGIN_DIR}", file=sys.stderr)
        return 1
    for checker in (check_layout, check_manifests, check_marketplaces, check_skills, check_files):
        errors.extend(checker())
    if errors:
        for item in errors:
            print(f"error: {item}", file=sys.stderr)
        print(f"{len(errors)} error(s)", file=sys.stderr)
        return 1
    print("ok")
    print(always_loaded_report())
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    return run()


if __name__ == "__main__":
    sys.exit(main())
