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

`*-v6.5.patch` files document dest-only edits stacked on the v6.4 dest copies: the "tests that cannot see the defect" section (`test-driven-development`), the whole-tree guard step and the "a reading is not evidence" section (`verification-before-completion`), and the review rubric and lead-judgment lines (`interrogate`). Each is a plain `git diff` of the skill folder from the 6.4.0 tree.

`*-v6.6.patch` files document dest-only edits stacked on the v6.5 dest copies: the "a call that changes another system" section (`writing-plans`), the lost-answer reviewer bullets (`interrogate` rubric) and the lost-answer test shape (`test-driven-development`). Each is a plain `git diff` of the skill folder from the 6.5.0 tree.

`*-v6.7.patch` files document dest-only edits stacked on the v6.6 dest copies: the "suites nobody runs for you" and "no shared file is not independence" sections (`verification-before-completion`), the one-transaction setting case (`test-driven-development`), the hand-made break bullet (`interrogate` rubric) and the generated-lists section (`writing-plans`). Each is a plain `git diff` of the skill folder from the 6.6.1 tree.

Pins and sha256 hashes live in `/sources.lock.json`.
