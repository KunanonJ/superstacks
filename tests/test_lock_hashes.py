from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "superstacks"


def test_dest_sha256_matches_the_files() -> None:
    lock = json.loads((ROOT / "sources.lock.json").read_text(encoding="utf-8"))
    problems: list[str] = []
    for rel, recorded in sorted(lock["dest_sha256"].items()):
        path = PLUGIN_DIR / rel
        if not path.is_file():
            problems.append(f"missing file: {rel}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != recorded:
            problems.append(f"hash differs: {rel} (recorded {recorded}, actual {actual})")
    assert not problems, "sources.lock.json dest_sha256 is out of date:\n" + "\n".join(problems)
