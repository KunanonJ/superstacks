"""Runtime guard template. Copy into the consuming repo. Stdlib only."""

from __future__ import annotations


class ConstraintError(ValueError):
    """Raised when a CONSTRAINTS.md guard is violated."""


def forbid_banned_state(value: str) -> str:
    if value == "BANNED":
        raise ConstraintError("BANNED is constrained. See CONSTRAINTS.md.")
    return value
