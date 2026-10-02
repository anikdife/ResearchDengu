#!/usr/bin/env python3
"""Capture one exact unauthenticated DGHS dashboard response.

The response body is saved before any parsing. Existing snapshots are never
overwritten. No authentication, endpoint guessing, or date iteration occurs.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import requests


SOURCE_URL = "https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php"
USER_AGENT = (
    "ResearchDengu-local-academic-dashboard-capture/0.1 "
    "(single-page forensic capture; contact via project documentation)"
)
TIMEOUT = (10, 30)
COLLECTOR_VERSION = "0.1.0"


def atomic_bytes(path: Path, payload: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        with temporary.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_text(path: Path, text: str) -> None:
    atomic_bytes(path, text.encode("utf-8"))


def main() -> int:
    try:
        response = requests.get(
            SOURCE_URL,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
            allow_redirects=True,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"REQUEST_FAILED: {exc}", file=sys.stderr)
        return 1

    body = response.content
    digest = hashlib.sha256(body).hexdigest()
    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0)
    timestamp = retrieved_at.strftime("%Y%m%dT%H%M%SZ")
    root = Path("data") / "dashboard_snapshots"
    root.mkdir(parents=True, exist_ok=True)
    snapshot = root / timestamp
    staging = root / f".{timestamp}.staging"

    if snapshot.exists() or staging.exists():
        print(
            f"REFUSED: snapshot path already exists; no overwrite: {snapshot}",
            file=sys.stderr,
        )
        return 2

    staging.mkdir()
    try:
        metadata = {
            "source_url": SOURCE_URL,
            "final_url": response.url,
            "retrieved_at_utc": retrieved_at.isoformat().replace("+00:00", "Z"),
            "status_code": response.status_code,
            "content_type": response.headers.get("Content-Type", ""),
            "content_length": len(body),
            "encoding": response.encoding or response.apparent_encoding or "unknown",
            "sha256": digest,
            "collector_version": COLLECTOR_VERSION,
        }
        atomic_bytes(staging / "page.html", body)
        atomic_text(staging / "metadata.json", json.dumps(metadata, indent=2) + "\n")
        atomic_text(staging / "sha256.txt", f"{digest}  page.html\n")
        os.replace(staging, snapshot)
    except Exception:
        if staging.exists():
            for child in staging.iterdir():
                child.unlink()
            staging.rmdir()
        raise

    print(f"Saved immutable dashboard snapshot: {snapshot}")
    print(f"SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
