"""Fixture-oriented extraction boundary.

Live dashboard access is deliberately outside this module until a permitted
immutable snapshot exists. Raw labels and values must be preserved unchanged.
"""


def preserve_observation(raw_label, raw_value, **metadata):
    return {"raw_label": raw_label, "raw_value": raw_value, **metadata}
