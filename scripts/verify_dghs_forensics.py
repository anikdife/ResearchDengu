#!/usr/bin/env python3
"""Verify required local DGHS forensic evidence without network access."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPOSITORY_ROOT / "outputs"
POST_TESTS_DIR = REPOSITORY_ROOT / "data" / "post_tests"


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def require_json(path: Path, failures: list[str]) -> dict | None:
    if not path.is_file():
        fail(f"missing JSON: {path}", failures)
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}", failures)
        return None
    print(f"OK: parsed {path.resolve()}")
    return value


def verify_archive(prefix: str, failures: list[str]) -> None:
    directories = []
    exact = POST_TESTS_DIR / prefix
    if exact.is_dir():
        directories.append(exact)
    directories.extend(
        path for path in POST_TESTS_DIR.glob(f"{prefix}_*")
        if path.is_dir() and path != exact
    )
    if not directories:
        fail(f"missing archive for {prefix} under {POST_TESTS_DIR}", failures)
        return
    for directory in directories:
        response = directory / "response.html"
        metadata = directory / "metadata.json"
        checksum = directory / "sha256.txt"
        for required in (response, metadata, checksum):
            if not required.is_file():
                fail(f"missing archive artifact: {required}", failures)
        if not response.is_file() or not metadata.is_file() or not checksum.is_file():
            continue
        try:
            metadata_value = json.loads(metadata.read_text(encoding="utf-8"))
            stored = checksum.read_text(encoding="utf-8").strip().split()[0]
            actual = hashlib.sha256(response.read_bytes()).hexdigest()
        except (OSError, json.JSONDecodeError, IndexError) as exc:
            fail(f"could not inspect archive {directory}: {exc}", failures)
            continue
        if stored != actual:
            fail(f"sha256.txt mismatch for {response}", failures)
        if metadata_value.get("sha256") != actual:
            fail(f"metadata sha256 mismatch for {response}", failures)
        else:
            print(f"OK: verified {response.resolve()} ({actual})")


def main() -> int:
    print(f"RESOLVED_REPOSITORY_ROOT: {REPOSITORY_ROOT}")
    failures: list[str] = []
    require_json(OUTPUT_DIR / "dghs_form_inventory.json", failures)
    post_report = require_json(OUTPUT_DIR / "dghs_post_forensics.json", failures)
    archive_presence = {}
    if not POST_TESTS_DIR.is_dir():
        fail(f"missing post-test directory: {POST_TESTS_DIR}", failures)
    else:
        print(f"OK: found {POST_TESTS_DIR.resolve()}")
        for prefix in (
            "test_A_get_baseline",
            "test_B_current_default",
            "test_C_earlier_supported",
        ):
            before = len(failures)
            verify_archive(prefix, failures)
            archive_presence[prefix] = len(
                [path for path in POST_TESTS_DIR.glob(f"{prefix}_*") if path.is_dir()]
            ) > 0 or (POST_TESTS_DIR / prefix).is_dir()
            if len(failures) == before and not archive_presence[prefix]:
                fail(f"no archive found for {prefix}", failures)
    complete_archives = all(archive_presence.values()) if archive_presence else False
    report_status = post_report.get("status") if isinstance(post_report, dict) else None
    if complete_archives and not failures:
        classification = "COMPLETE"
    elif archive_presence.get("test_A_get_baseline", False) or report_status == "PARTIAL":
        classification = "PARTIAL"
    else:
        classification = "FAILED"
    print(f"FORENSICS_STATUS: {classification}")
    if failures:
        print(f"VERIFICATION_FAILED: {len(failures)} issue(s)")
        return 1
    print("VERIFICATION_PASSED: all required DGHS forensic evidence exists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
