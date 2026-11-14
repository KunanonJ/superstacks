# Vendor patches

Each `*.patch` is a unified diff from the pinned upstream file (left) to the
file in `plugins/superstacks/` (right). Apply them only as documentation of
dest-only edits; the plugin tree is the source of truth.

`*-v6.1.patch` files document dest-only edits stacked on the v6.0.0 dest copies
(`verify-loop` pointers, PR body checker). The plugin tree is still the source
of truth. Stacked-PR guidance lives in `pr/SKILL.md` and `ticket-pipeline/SKILL.md`
as further dest-only text; it is not a vendor patch.

`*-v6.4.patch` files document dest-only edits stacked on the v6.1 dest copies:
the finder and refuser review rules (`interrogate`, `code-review`), the "before you
say ready" step (`verification-before-completion`), and the `## Review` section and
`Class: finder` check (`pr`). Each is a plain `git diff` of the skill folder from the
6.3.0 tree. The plugin tree is still the source of truth.

Pins and sha256 hashes live in `/sources.lock.json`.
