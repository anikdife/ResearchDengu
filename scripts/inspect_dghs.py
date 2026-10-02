#!/usr/bin/env python3
"""Inspect one normal unauthenticated DGHS dashboard response.

This script intentionally performs one request only. It does not authenticate,
guess endpoints, iterate dates, or bypass access controls.
"""

from __future__ import annotations

import sys
import json
import argparse
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPOSITORY_ROOT / "outputs"
SOURCE_URL = "https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php"
USER_AGENT = (
    "ResearchDengu-local-academic-dashboard-inspector/0.1 "
    "(single-page forensic inspection; contact via project documentation)"
)
TIMEOUT = (10, 30)
SEARCH_TERMS = (
    "Dengue",
    "Admitted",
    "Death",
    "EPI",
    "City Corporation",
    "Division",
    "age",
    "sex",
    "series",
    "categories",
    "data",
    "ajax",
    "fetch",
    "xhr",
    "json",
)


def print_startup() -> None:
    print(f"CURRENT_WORKING_DIRECTORY: {Path.cwd().resolve()}")
    print(f"RESOLVED_REPOSITORY_ROOT: {REPOSITORY_ROOT}")
    print(f"RESOLVED_OUTPUT_PATH: {OUTPUT_DIR / 'dghs_form_inventory.json'}")


def write_json_with_diagnostics(path: Path, payload: dict) -> None:
    data = (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    path.write_bytes(data)
    import hashlib

    print(f"WROTE: {path.resolve()}")
    print(f"SIZE: {len(data)}")
    print(f"SHA256: {hashlib.sha256(data).hexdigest()}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fetch-external-js",
        action="store_true",
        help="Fetch only the exact external script src URLs present in the HTML for reference inspection.",
    )
    args = parser.parse_args()
    print_startup()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"CHECKED_OUTPUT_DIRECTORY: {OUTPUT_DIR.resolve()}")
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
    encoding = response.encoding or response.apparent_encoding or "unknown"
    soup = BeautifulSoup(body, "lxml")
    write_form_inventory(soup, response.url, fetch_external_js=args.fetch_external_js)

    print(f"HTTP status: {response.status_code}")
    print(f"Final URL: {response.url}")
    print(f"Content type: {response.headers.get('Content-Type', 'unknown')}")
    print(f"Content length (bytes): {len(body)}")
    print(f"Encoding: {encoding}")
    print(f"Page title: {soup.title.get_text(' ', strip=True) if soup.title else ''}")
    print(f"Number of tables: {len(soup.find_all('table'))}")
    print(f"Number of script elements: {len(soup.find_all('script'))}")
    print(f"Number of forms: {len(soup.find_all('form'))}")
    print(f"Number of links: {len(soup.find_all('a'))}")

    print("Relevant caching headers:")
    for name in (
        "Cache-Control",
        "ETag",
        "Last-Modified",
        "Expires",
        "Age",
        "Vary",
        "Content-Encoding",
    ):
        print(f"  {name}: {response.headers.get(name, '')}")

    text = soup.get_text(" ", strip=True)
    lower_text = text.lower()
    print("Search-term occurrences in visible HTML text:")
    for term in SEARCH_TERMS:
        print(f"  {term}: {lower_text.count(term.lower())}")

    print("Script src URLs:")
    for index, script in enumerate(soup.find_all("script")):
        src = script.get("src")
        if src:
            print(f"  [{index}] {urljoin(response.url, src)}")
        else:
            print(f"  [{index}] [inline script; {len(script.get_text())} characters]")

    print("Ordinary publicly referenced resources:")
    seen: set[str] = set()
    for element, attribute in (
        (soup.find_all("link"), "href"),
        (soup.find_all("img"), "src"),
        (soup.find_all("iframe"), "src"),
        (soup.find_all("source"), "src"),
    ):
        for item in element:
            value = item.get(attribute)
            if value:
                absolute = urljoin(response.url, value)
                if absolute not in seen:
                    seen.add(absolute)
                    print(f"  {absolute}")

    print("Forms and ordinary parameters:")
    for index, form in enumerate(soup.find_all("form")):
        print(
            f"  [{index}] method={form.get('method', 'get').upper()} "
            f"action={urljoin(response.url, form.get('action', ''))}"
        )
        for control in form.find_all(["input", "select", "textarea", "button"]):
            print(
                f"      {control.name} name={control.get('name', '')} "
                f"value={control.get('value', '')}"
            )

    return 0


def associated_label(control) -> str:
    control_id = control.get("id", "")
    if control_id:
        label = control.find_previous("label", attrs={"for": control_id})
        if label:
            return label.get_text(" ", strip=True)
    parent_label = control.find_parent("label")
    if parent_label:
        return parent_label.get_text(" ", strip=True)
    previous = control.find_previous(["label", "legend"])
    return previous.get_text(" ", strip=True) if previous else ""


def control_inventory(control) -> dict:
    item = {
        "tag": control.name,
        "name": control.get("name", ""),
        "type": control.get("type", ""),
        "value": control.get("value", ""),
        "selected_default_value": "",
        "placeholder": control.get("placeholder", ""),
        "min": control.get("min", ""),
        "max": control.get("max", ""),
        "associated_label": associated_label(control),
        "surrounding_html": str(control.parent)[:4000],
    }
    if control.name == "select":
        options = []
        selected_values = []
        for option in control.find_all("option"):
            option_item = {
                "display_label": option.get_text(" ", strip=True),
                "submitted_value": option.get("value", ""),
                "selected": option.has_attr("selected"),
            }
            options.append(option_item)
            if option_item["selected"]:
                selected_values.append(option_item["submitted_value"])
        item["options"] = options
        item["selected_default_value"] = (
            selected_values[0] if selected_values else (options[0]["submitted_value"] if options else "")
        )
    return item


def javascript_reference_inventory(
    soup: BeautifulSoup, final_url: str, fetch_external_js: bool = False
) -> dict:
    terms = (
        "filter_year",
        "report_date_filter",
        "search_filter",
        "confirm_from",
        "confirm_to",
        "confirm_search",
    )
    inline = []
    external = []
    for index, script in enumerate(soup.find_all("script")):
        body = script.get_text()
        hits = [term for term in terms if term in body]
        if hits:
            inline.append({"script_index": index, "references": hits, "text": body})
        src = script.get("src")
        if not src:
            continue
        item = {
            "script_index": index,
            "src": urljoin(final_url, src),
            "fetched": False,
            "references": [],
        }
        if fetch_external_js:
            try:
                external_response = requests.get(
                    item["src"],
                    headers={"User-Agent": USER_AGENT},
                    timeout=TIMEOUT,
                    allow_redirects=True,
                )
                item["fetched"] = external_response.ok
                external_text = external_response.text
                item["references"] = [
                    term for term in terms if term in external_text
                ]
                item["status_code"] = external_response.status_code
                item["final_url"] = external_response.url
            except requests.RequestException as exc:
                item["error"] = str(exc)
        external.append(item)
    return {"inline": inline, "external": external}


def write_form_inventory(
    soup: BeautifulSoup, final_url: str, fetch_external_js: bool = False
) -> None:
    forms = []
    for form_index, form in enumerate(soup.find_all("form")):
        controls = [
            control_inventory(control)
            for control in form.find_all(["input", "select", "textarea", "button"])
        ]
        forms.append(
            {
                "form_index": form_index,
                "method": form.get("method", "GET").upper(),
                "action": urljoin(final_url, form.get("action", "")),
                "surrounding_html": str(form),
                "controls": controls,
            }
        )
    write_json_with_diagnostics(
        OUTPUT_DIR / "dghs_form_inventory.json",
        {
            "source_url": SOURCE_URL,
            "final_url": final_url,
            "forms": forms,
            "javascript_references": javascript_reference_inventory(
                soup, final_url, fetch_external_js=fetch_external_js
            ),
        },
    )


if __name__ == "__main__":
    raise SystemExit(main())
