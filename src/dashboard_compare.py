"""Comparison classifications for repeated immutable dashboard snapshots."""


def compare_values(old, new):
    if old == new:
        return "UNCHANGED"
    if old is None:
        return "NEWLY_APPEARED"
    if new is None:
        return "DISAPPEARED"
    if isinstance(old, (int, float)) and isinstance(new, (int, float)):
        return "REVISED_UP" if new > old else "REVISED_DOWN"
    return "SCHEMA_CHANGED"
