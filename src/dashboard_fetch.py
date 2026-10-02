"""Design-only dashboard capture helper for a future approved run.

This module intentionally does not run during B0.6A. Any future use must be a
normal unauthenticated public request and must preserve the response bytes.
"""

from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def write_snapshot_metadata(path: Path, metadata: dict) -> None:
    path.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
