"""Structural-only validators; no epidemiological interpretation."""


def compatible_sum(parts, total):
    if any(value is None for value in parts) or total is None:
        return None
    return sum(parts) == total
