#!/usr/bin/env python3
"""Parse one saved dashboard page without network access or normalization."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

from bs4 import BeautifulSoup


JSON_SCRIPT_TYPES = {
    "application/json",
    "application/ld+json",
    "application/geo+json",
}
TIME_TERMS = ("date", "year", "month", "week", "epi")
DIVISION_TERMS = ("division",)


def text(node) -> str:
    return node.get_text(" ", strip=True)


def parse_snapshot(snapshot: Path) -> tuple[Path, BeautifulSoup]:
    page = snapshot / "page.html" if snapshot.is_dir() else snapshot
    if not page.is_file():
        raise FileNotFoundError(f"Saved page.html not found: {page}")
    return page, BeautifulSoup(page.read_bytes(), "lxml")


def table_records(soup: BeautifulSoup) -> list[dict]:
    records = []
    for table_index, table in enumerate(soup.find_all("table")):
        headers = [text(cell) for cell in table.find_all("th")]
        rows = []
        for row in table.find_all("tr"):
            cells = [text(cell) for cell in row.find_all(["th", "td"])]
            if cells:
                rows.append(cells)
        caption = table.find("caption")
        records.append(
            {
                "table_index": table_index,
                "caption": text(caption) if caption else "",
                "headers": headers,
                "rows": rows,
            }
        )
    return records


def write_tables_csv(records: list[dict], path: Path) -> None:
    rows = []
    width = 0
    for record in records:
        for row_index, cells in enumerate(record["rows"]):
            width = max(width, len(cells))
            rows.append((record["table_index"], row_index, cells))
    fieldnames = ["table_index", "row_index"] + [
        f"raw_column_{index}" for index in range(width)
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for table_index, row_index, cells in rows:
            record = {"table_index": table_index, "row_index": row_index}
            record.update({f"raw_column_{i}": value for i, value in enumerate(cells)})
            writer.writerow(record)


def script_inventory(soup: BeautifulSoup) -> tuple[list[dict], list[dict], list[dict]]:
    inventory, json_candidates, chart_candidates = [], [], []
    chart_terms = ("chart", "series", "categories", "dataset", "labels")
    for index, script in enumerate(soup.find_all("script")):
        source = script.get("src", "")
        body = script.get_text()
        stripped = body.strip()
        item = {
            "script_index": index,
            "src": source,
            "type": script.get("type", ""),
            "character_count": len(body),
            "has_json_type": script.get("type", "").lower() in JSON_SCRIPT_TYPES,
            "chart_terms_present": [term for term in chart_terms if term in body.lower()],
        }
        inventory.append(item)
        if item["has_json_type"] or (stripped.startswith(("{", "[")) and stripped.endswith(("}", "]"))):
            candidate = {"script_index": index, "raw_text": body}
            try:
                candidate["parsed_json"] = json.loads(stripped)
            except json.JSONDecodeError:
                candidate["parsed_json"] = None
            json_candidates.append(candidate)
        if any(term in body.lower() for term in chart_terms):
            chart_candidates.append({"script_index": index, "raw_text": body})
    return inventory, json_candidates, chart_candidates


def controls(soup: BeautifulSoup) -> dict:
    forms, date_selectors, year_selectors, month_selectors, division_selectors = [], [], [], [], []
    for form_index, form in enumerate(soup.find_all("form")):
        controls_in_form = []
        for control in form.find_all(["input", "select", "textarea", "button"]):
            item = {
                "tag": control.name,
                "name": control.get("name", ""),
                "id": control.get("id", ""),
                "type": control.get("type", ""),
                "value": control.get("value", ""),
                "options": [text(o) for o in control.find_all("option")],
            }
            controls_in_form.append(item)
            haystack = " ".join((item["name"], item["id"], item["value"])).lower()
            if any(term in haystack for term in TIME_TERMS):
                date_selectors.append(item)
            if "year" in haystack:
                year_selectors.append(item)
            if "month" in haystack:
                month_selectors.append(item)
            if "division" in haystack:
                division_selectors.append(item)
        action = form.get("action", "")
        forms.append(
            {
                "form_index": form_index,
                "method": form.get("method", "get").upper(),
                "action": action,
                "query_parameters_in_action": dict(parse_qsl(urlparse(action).query)),
                "controls": controls_in_form,
            }
        )
    return {
        "forms": forms,
        "date_selectors": date_selectors,
        "year_selectors": year_selectors,
        "month_selectors": month_selectors,
        "division_selectors": division_selectors,
    }


def assess_time(soup: BeautifulSoup, controls_data: dict, json_candidates: list, chart_candidates: list) -> dict:
    html = str(soup).lower()
    return {
        "A_embedded_in_current_html": bool(
            soup.find_all("table") or controls_data["date_selectors"] or "series" in html
        ),
        "B_selected_using_get_parameters": any(
            form["method"] == "GET" and form["query_parameters_in_action"]
            for form in controls_data["forms"]
        ),
        "C_selected_using_post_parameters": any(
            form["method"] == "POST" and form["controls"] for form in controls_data["forms"]
        ),
        "D_public_endpoint_referenced": False,
        "E_embedded_javascript_or_chart_data": bool(json_candidates or chart_candidates),
        "F_unavailable_from_current_response": not bool(
            soup.find_all("table") or controls_data["date_selectors"] or json_candidates or chart_candidates
        ),
        "note": "These are structural indicators only; no endpoint was guessed or requested.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", required=True, type=Path)
    args = parser.parse_args()
    _, soup = parse_snapshot(args.snapshot)
    output = args.snapshot / "extracted" if args.snapshot.is_dir() else args.snapshot.parent / "extracted"
    output.mkdir(exist_ok=True)

    tables = table_records(soup)
    scripts, json_candidates, chart_candidates = script_inventory(soup)
    control_data = controls(soup)
    control_data["embedded_json_candidates"] = json_candidates
    control_data["chart_configuration_candidates"] = chart_candidates
    control_data["time_representation_assessment"] = assess_time(
        soup, control_data, json_candidates, chart_candidates
    )

    (output / "tables.json").write_text(json.dumps(tables, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_tables_csv(tables, output / "tables.csv")
    (output / "scripts_inventory.json").write_text(
        json.dumps(scripts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output / "controls.json").write_text(
        json.dumps(control_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Parsed saved snapshot: {args.snapshot}")
    print(f"Extraction output: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
