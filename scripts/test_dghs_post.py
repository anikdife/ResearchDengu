#!/usr/bin/env python3
"""Run exactly three fail-closed DGHS POST-interface diagnostics.

Requests:
  A - ordinary GET baseline
  B - POST the form's current/default year and date
  C - POST the form's explicitly supported earlier date

No date is invented. If the HTML does not expose a current date and an earlier
supported date, the script stops before sending B or C.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPOSITORY_ROOT / "outputs"
POST_TESTS_DIR = REPOSITORY_ROOT / "data" / "post_tests"
SOURCE_URL = "https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php"
USER_AGENT = (
    "ResearchDengu-local-academic-post-forensics/0.1 "
    "(three-request diagnostic; no authentication)"
)
TIMEOUT = (10, 30)
COLLECTOR_VERSION = "0.1.0"
REQUIRED_REFERENCES = (
    "filter_year",
    "report_date_filter",
    "search_filter",
    "confirm_from",
    "confirm_to",
    "confirm_search",
)
MANUAL_REFERENCE_DATE = "2026-04-04"
MANUAL_REFERENCE_VALUES = {
    "weekly_case": "158",
    "weekly_death": "0",
    "cumulative_case": "1910",
    "cumulative_death": "4",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def timestamp() -> str:
    return utc_now().strftime("%Y%m%dT%H%M%SZ")


def atomic_write(path: Path, payload: bytes) -> str:
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    digest = hashlib.sha256(payload).hexdigest()
    print(f"WROTE: {path.resolve()}")
    print(f"SIZE: {len(payload)}")
    print(f"SHA256: {digest}")
    return digest


def print_startup() -> None:
    print(f"CURRENT_WORKING_DIRECTORY: {Path.cwd().resolve()}")
    print(f"RESOLVED_REPOSITORY_ROOT: {REPOSITORY_ROOT}")
    print(f"RESOLVED_OUTPUT_PATH: {OUTPUT_DIR / 'dghs_post_forensics.json'}")
    print(f"RESOLVED_POST_TESTS_PATH: {POST_TESTS_DIR}")


def parse_date(value: str) -> tuple[int, int, int] | None:
    for pattern in (
        r"^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})$",
        r"^(?P<d>\d{2})[-/](?P<m>\d{2})[-/](?P<y>\d{4})$",
        r"^(?P<d>\d{2})[.](?P<m>\d{2})[.](?P<y>\d{4})$",
    ):
        match = re.match(pattern, value.strip())
        if match:
            return int(match["y"]), int(match["m"]), int(match["d"])
    return None


def date_format(value: str) -> str:
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value.strip()):
        return "YYYY-MM-DD"
    if re.match(r"^\d{2}-\d{2}-\d{4}$", value.strip()):
        return "DD-MM-YYYY"
    if re.match(r"^\d{2}/\d{2}/\d{4}$", value.strip()):
        return "DD/MM/YYYY"
    if re.match(r"^\d{2}\.\d{2}\.\d{4}$", value.strip()):
        return "DD.MM.YYYY"
    return "UNRESOLVED"


def normalize_action(action: str) -> str:
    return urljoin(SOURCE_URL, action or "")


def load_verified_contract() -> dict:
    path = OUTPUT_DIR / "dghs_form_inventory.json"
    try:
        inventory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"verified form inventory unavailable or invalid: {exc}") from exc
    forms = inventory.get("forms")
    if not isinstance(forms, list) or not forms:
        raise RuntimeError("verified form inventory contains no forms")
    primary = None
    for form in forms:
        controls = form.get("controls", [])
        has_year = any(
            control.get("tag") == "select" and control.get("options")
            for control in controls
        )
        has_date = any(
            control.get("tag") == "input"
            and control.get("type") == "text"
            and "YYYY-MM-DD" in control.get("placeholder", "")
            for control in controls
        )
        if form.get("method") == "POST" and has_year and has_date:
            primary = form
            break
    if primary is None:
        raise RuntimeError("verified inventory has no POST form with year and date controls")
    controls = primary["controls"]
    year_contract = next(
        control for control in controls
        if control.get("tag") == "select" and control.get("options")
    )
    date_contract = next(
        control for control in controls
        if control.get("tag") == "input"
        and control.get("type") == "text"
        and "YYYY-MM-DD" in control.get("placeholder", "")
    )
    submit_contract = next(
        control for control in controls
        if control.get("tag") == "input"
        and control.get("type") == "submit"
        and control.get("value") == "Search"
    )
    return {
        "inventory_path": str(path.resolve()),
        "form_index": primary["form_index"],
        "method": primary["method"],
        "action": primary["action"],
        "controls": controls,
        "year": year_contract,
        "date": date_contract,
        "submit": submit_contract,
        "all_forms": forms,
    }


def validate_live_contract(soup: BeautifulSoup, contract: dict) -> dict:
    live_forms = soup.find_all("form")
    index = contract["form_index"]
    if index >= len(live_forms):
        raise RuntimeError("live form count/index differs from verified contract")
    form = live_forms[index]
    live_method = form.get("method", "GET").upper()
    live_action = normalize_action(form.get("action", ""))
    if live_method != contract["method"] or live_action != contract["action"]:
        raise RuntimeError("live primary form method/action differs from verified contract")
    live_controls = form.find_all(["input", "select", "textarea", "button"])
    live_names = [control.get("name", "") for control in live_controls if control.get("name")]
    expected_names = [
        control.get("name", "") for control in contract["controls"] if control.get("name")
    ]
    if live_names != expected_names:
        raise RuntimeError("live primary form control names/order differ from verified contract")
    for expected in (contract["year"], contract["date"], contract["submit"]):
        live = form.find(attrs={"name": expected["name"]})
        if live is None:
            raise RuntimeError(f"verified control missing from live form: {expected['name']}")
        if live.name != expected["tag"] or live.get("type", "") != expected.get("type", ""):
            raise RuntimeError(f"live control type differs: {expected['name']}")
    return {
        "form": form,
        "year": form.find(attrs={"name": contract["year"]["name"]}),
        "date": form.find(attrs={"name": contract["date"]["name"]}),
        "submit": form.find(attrs={"name": contract["submit"]["name"]}),
    }


def displayed_last_updated(soup: BeautifulSoup) -> str:
    match = re.search(
        r"Last Updated:\s*</span>\s*(\d{2}-[A-Za-z]{3}-\d{4})",
        str(soup),
        flags=re.IGNORECASE,
    )
    if not match:
        raise RuntimeError("live page has no extractable Last Updated date")
    return datetime.strptime(match.group(1), "%d-%b-%Y").strftime("%Y-%m-%d")


def form_options(select) -> list[dict]:
    return [
        {
            "display_label": option.get_text(" ", strip=True),
            "submitted_value": option.get("value", ""),
            "selected": option.has_attr("selected"),
        }
        for option in select.find_all("option")
    ]


def form_by_control(soup: BeautifulSoup, control_name: str):
    for form in soup.find_all("form"):
        if form.find(attrs={"name": control_name}):
            return form
    return None


def selected_option(select) -> tuple[str, str] | None:
    options = select.find_all("option")
    if not options:
        return None
    option = next((item for item in options if item.has_attr("selected")), options[0])
    return option.get("value", ""), option.get_text(" ", strip=True)


def successful_controls(form) -> dict[str, str]:
    values: dict[str, str] = {}
    for control in form.find_all(["input", "select", "textarea", "button"]):
        name = control.get("name")
        if not name or control.has_attr("disabled"):
            continue
        if control.name == "select":
            selected = selected_option(control)
            if selected:
                values[name] = selected[0]
        elif control.name == "button" and control.get("type", "submit").lower() not in (
            "submit",
            "button",
        ):
            continue
        else:
            values[name] = control.get("value", "")
    return values


def derive_submission(soup: BeautifulSoup, contract: dict) -> dict:
    live = validate_live_contract(soup, contract)
    year_select = live["year"]
    date_input = live["date"]
    submit = live["submit"]
    selected = selected_option(year_select)
    if selected is None:
        raise RuntimeError("verified year control has no options")
    current_date = displayed_last_updated(soup)
    if parse_date(current_date) is None:
        raise RuntimeError("displayed Last Updated date is not parseable")
    options = form_options(year_select)
    if not any(item["submitted_value"] == str(parse_date(current_date)[0]) for item in options):
        raise RuntimeError("displayed current year is not an option in the verified year control")
    if selected[0] != str(parse_date(current_date)[0]):
        raise RuntimeError("selected year does not match displayed current dashboard year")
    date_evidence = [
        {
            "source": "dashboard Last Updated display",
            "value": current_date,
            "form_default_value": date_input.get("value", ""),
        }
    ]
    for attribute in ("min", "data-date-start-date", "data-start-date", "data-min"):
        value = date_input.get(attribute, "").strip()
        if value and parse_date(value) is not None:
            date_evidence.append({"source": f"input@{attribute}", "value": value})
    earlier_candidates = [
        item["value"]
        for item in date_evidence
        if parse_date(item["value"]) < parse_date(current_date)
    ]
    if (
        MANUAL_REFERENCE_DATE < current_date
        and str(parse_date(MANUAL_REFERENCE_DATE)[0]) in [item["submitted_value"] for item in options]
        and date_input.get("placeholder") == "YYYY-MM-DD"
    ):
        earlier_candidates.insert(0, MANUAL_REFERENCE_DATE)
        date_evidence.append(
            {
                "source": "user-supplied manual UI evidence",
                "value": MANUAL_REFERENCE_DATE,
                "accepted_in_public_UI": True,
            }
        )
    if not earlier_candidates:
        raise RuntimeError(
            "No earlier supported date is exposed by the verified form or supplied "
            "manual UI evidence; refusing to invent TEST C"
        )
    earlier = earlier_candidates[0]
    base = successful_controls(live["form"])
    year_name = contract["year"]["name"]
    date_name = contract["date"]["name"]
    submit_name = contract["submit"]["name"]
    base[year_name] = selected[0]
    base[date_name] = current_date
    base[submit_name] = submit.get("value", "")
    earlier_fields = dict(base)
    earlier_fields[date_name] = earlier
    return {
        "form_action": contract["action"],
        "form_method": contract["method"],
        "form_index": contract["form_index"],
        "year_control": contract["year"],
        "date_control": contract["date"],
        "submit_control": contract["submit"],
        "year_options": options,
        "current_year": {"value": selected[0], "display_label": selected[1]},
        "current_date": current_date,
        "date_format": date_format(current_date),
        "earlier_date": earlier,
        "date_evidence": date_evidence,
        "test_b_fields": base,
        "test_c_fields": earlier_fields,
    }


def search_javascript(soup: BeautifulSoup) -> dict:
    inline = []
    external = []
    for index, script in enumerate(soup.find_all("script")):
        body = script.get_text()
        hits = [term for term in REQUIRED_REFERENCES if term in body]
        if hits:
            inline.append({"script_index": index, "references": hits, "text": body})
        if script.get("src"):
            external.append(
                {
                    "script_index": index,
                    "src": urljoin(SOURCE_URL, script["src"]),
                    "searched": False,
                    "reason": "External resource fetch is not part of the three diagnostic POST requests.",
                }
            )
    return {"inline_references": inline, "external_script_references": external}


def archive(test_id: str, method: str, url: str, fields: dict, response) -> Path:
    directory = POST_TESTS_DIR / test_id
    if directory.exists():
        raise RuntimeError(f"refusing to overwrite existing archive: {directory}")
    directory.mkdir()
    body = response.content
    digest = hashlib.sha256(body).hexdigest()
    request = {
        "method": method,
        "URL": url,
        "submitted_form_fields": fields,
        "timestamp": utc_now().isoformat().replace("+00:00", "Z"),
    }
    metadata = {
        "HTTP_status": response.status_code,
        "final_url": response.url,
        "content_type": response.headers.get("Content-Type", ""),
        "response_length": len(body),
        "sha256": digest,
    }
    atomic_write(directory / "request.json", (json.dumps(request, indent=2) + "\n").encode())
    atomic_write(directory / "response.html", body)
    atomic_write(directory / "metadata.json", (json.dumps(metadata, indent=2) + "\n").encode())
    atomic_write(directory / "sha256.txt", f"{digest}  response.html\n".encode())
    return directory


def headline_values(soup: BeautifulSoup) -> dict:
    updated = ""
    match = re.search(
        r"Last Updated:\s*</span>\s*(\d{2}-[A-Za-z]{3}-\d{4})",
        str(soup),
        flags=re.IGNORECASE,
    )
    if match:
        updated = match.group(1)
    items = [item.get_text(" ", strip=True) for item in soup.select(".item_one")]
    values = {
        "displayed_last_updated": updated,
        "weekly_case": None,
        "weekly_death": None,
        "cumulative_case": None,
        "cumulative_death": None,
    }
    if len(items) >= 4:
        values["weekly_case"] = re.sub(r"^[^:]*:\s*", "", items[0]).replace(",", "").strip()
        values["weekly_death"] = items[1].replace(",", "").strip()
        values["cumulative_case"] = items[2].replace(",", "").strip()
        values["cumulative_death"] = items[3].replace(",", "").strip()
    return values


def structural_summary(response, submitted_date: str | None = None) -> dict:
    soup = BeautifulSoup(response.content, "lxml")
    visible = soup.get_text(" ", strip=True)
    html_lower = response.content.decode(response.encoding or "utf-8", errors="replace").lower()
    return {
        "status": response.status_code,
        "final_url": response.url,
        "content_length": len(response.content),
        "title": soup.title.get_text(" ", strip=True) if soup.title else "",
        "table_count": len(soup.find_all("table")),
        "script_count": len(soup.find_all("script")),
        "form_count": len(soup.find_all("form")),
        "submitted_date": submitted_date,
        "submitted_date_occurrences_in_html": (
            html_lower.count(submitted_date.lower()) if submitted_date else 0
        ),
        "term_presence": {
            term: term.lower() in visible.lower()
            for term in ("Dengue", "Admitted", "Death", "City Corporation", "Division", "age", "sex")
        },
        "headline_values": headline_values(soup),
    }


def compare_structures(left: dict, right: dict) -> dict:
    fields = (
        "title",
        "table_count",
        "script_count",
        "form_count",
        "term_presence",
    )
    return {
        "changed_fields": [
            field for field in fields if left.get(field) != right.get(field)
        ],
        "structurally_changed": any(
            left.get(field) != right.get(field) for field in fields
        ),
        "submitted_date_evidence_in_right": right.get(
            "submitted_date_occurrences_in_html", 0
        ),
        "note": "This compares HTML structure and visible term presence only.",
    }


def manual_reference_comparison(date_value: str, values: dict) -> dict:
    if date_value != MANUAL_REFERENCE_DATE:
        return {"status": "NOT_APPLICABLE", "metrics": {}}
    metrics = {}
    for metric, expected in MANUAL_REFERENCE_VALUES.items():
        actual = values.get(metric)
        metrics[metric] = {
            "expected": expected,
            "actual": actual,
            "classification": (
                "MATCH_MANUAL_REFERENCE"
                if actual == expected
                else "MISMATCH_MANUAL_REFERENCE"
                if actual is not None
                else "NOT_EXTRACTABLE"
            ),
        }
    return {"status": "COMPARED", "metrics": metrics}


def write_report(report: dict) -> None:
    report_bytes = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    atomic_write(OUTPUT_DIR / "dghs_post_forensics.json", report_bytes)


def requested_date_display_matches(summary: dict) -> bool:
    displayed = summary.get("headline_values", {}).get("displayed_last_updated", "")
    requested = summary.get("submitted_date", "")
    if not displayed or not requested:
        return False
    try:
        return datetime.strptime(displayed, "%d-%b-%Y").strftime("%Y-%m-%d") == requested
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exactly A/B/C DGHS POST diagnostics.")
    parser.parse_args()
    print_startup()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    POST_TESTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"CHECKED_OUTPUT_DIRECTORY: {OUTPUT_DIR.resolve()}")
    print(f"CHECKED_POST_TESTS_DIRECTORY: {POST_TESTS_DIR.resolve()}")
    target_archives = (
        POST_TESTS_DIR / "test_A_get_baseline",
        POST_TESTS_DIR / "test_B_current_default",
        POST_TESTS_DIR / "test_C_earlier_supported",
    )
    if any(path.exists() for path in target_archives):
        print(
            "STOPPED_BEFORE_REQUEST_A: one or more fixed archive directories already exist; "
            "refusing to overwrite evidence",
            file=sys.stderr,
        )
        return 2
    try:
        contract = load_verified_contract()
    except RuntimeError as exc:
        print(f"STOPPED_BEFORE_REQUEST_A: {exc}", file=sys.stderr)
        return 2

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    try:
        baseline = session.get(SOURCE_URL, timeout=TIMEOUT, allow_redirects=True)
        baseline.raise_for_status()
    except requests.RequestException as exc:
        print(f"TEST_A_REQUEST_FAILED: {exc}", file=sys.stderr)
        return 1

    archives = {}
    try:
        archives["A"] = archive(
            "test_A_get_baseline", "GET", baseline.url, {}, baseline
        )
    except (OSError, RuntimeError) as exc:
        print(f"TEST_A_ARCHIVE_FAILED: {exc}", file=sys.stderr)
        return 1

    soup = BeautifulSoup(baseline.content, "lxml")
    try:
        submission = derive_submission(soup, contract)
    except RuntimeError as exc:
        print(f"STOPPED_BEFORE_TEST_BC: {exc}", file=sys.stderr)
        write_report(
            {
                "source_url": SOURCE_URL,
                "status": "PARTIAL",
                "verified_form_contract": contract,
                "archives": {"A": str(archives["A"])},
                "A": structural_summary(baseline),
                "B": None,
                "C": None,
                "errors": [str(exc)],
            }
        )
        return 2

    javascript = search_javascript(soup)
    try:
        response_b = session.post(
            submission["form_action"],
            data=submission["test_b_fields"],
            timeout=TIMEOUT,
            allow_redirects=True,
        )
        archives["B"] = archive(
            "test_B_current_default",
            "POST",
            submission["form_action"],
            submission["test_b_fields"],
            response_b,
        )
        if response_b.status_code != 200:
            raise RuntimeError(f"TEST B returned HTTP {response_b.status_code}")
        response_c = session.post(
            submission["form_action"],
            data=submission["test_c_fields"],
            timeout=TIMEOUT,
            allow_redirects=True,
        )
        archives["C"] = archive(
            "test_C_earlier_supported",
            "POST",
            submission["form_action"],
            submission["test_c_fields"],
            response_c,
        )
        if response_c.status_code != 200:
            raise RuntimeError(f"TEST C returned HTTP {response_c.status_code}")
    except (requests.RequestException, OSError, RuntimeError) as exc:
        print(f"TEST_B_OR_C_REQUEST_FAILED: {exc}", file=sys.stderr)
        write_report(
            {
                "source_url": SOURCE_URL,
                "status": "PARTIAL",
                "verified_form_contract": contract,
                "submission_evidence": submission,
                "archives": {key: str(value) for key, value in archives.items()},
                "A": structural_summary(baseline),
                "B": structural_summary(response_b, submission["current_date"]) if "response_b" in locals() else None,
                "C": structural_summary(response_c, submission["earlier_date"]) if "response_c" in locals() else None,
                "errors": [str(exc)],
            }
        )
        return 1

    summaries = {
        "A": structural_summary(baseline),
        "B": structural_summary(response_b, submission["current_date"]),
        "C": structural_summary(response_c, submission["earlier_date"]),
    }
    comparisons = {
        "A_vs_B": compare_structures(summaries["A"], summaries["B"]),
        "A_vs_C": compare_structures(summaries["A"], summaries["C"]),
        "B_vs_C": compare_structures(summaries["B"], summaries["C"]),
    }
    report = {
        "source_url": SOURCE_URL,
        "status": "COMPLETE",
        "verified_form_contract": contract,
        "session_cookies_preserved": True,
        "submission_evidence": submission,
        "javascript_references": javascript,
        "archives": {key: str(value) for key, value in archives.items()},
        "structural_summaries": summaries,
        "structural_comparisons": comparisons,
        "historical_post_confirmed": requested_date_display_matches(summaries["C"]),
        "manual_reference_comparison": manual_reference_comparison(
            submission["earlier_date"], summaries["C"]["headline_values"]
        ),
        "interpretation": "Structural comparison only; no epidemiological analysis.",
    }
    write_report(report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
