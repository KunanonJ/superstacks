# Vendor patches

Each `*.patch` is a unified diff from the pinned upstream file (left) to the
file in `plugins/superstacks/` (right). Apply them only as documentation of
dest-only edits; the plugin tree is the source of truth.

`*-v6.1.patch` files document dest-only edits stacked on the v6.0.0 dest copies
(`verify-loop` pointers, PR body checker). The plugin tree is still the source
of truth. Stacked-PR guidance lives in `pr/SKILL.md` and `ticket-pipeline/SKILL.md`
as further dest-only text; it is not a vendor patch.

Pins and sha256 hashes live in `/sources.lock.json`.

Pins and sha256 hashes live in `/sources.lock.json`.
