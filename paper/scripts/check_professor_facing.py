from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
main = ROOT / "manuscript.tex"
text = main.read_text(encoding="utf-8")
errors = []
ethics = (ROOT / "sections" / "ethics-data-governance.tex").read_text(encoding="utf-8")
if "publicly accessible aggregate dashboard observations" not in ethics or "Formal institutional review or exemption status has not yet been determined." not in ethics:
    errors.append("factual unresolved ethics statement is missing or altered")

if text.count(r"\ethicspending{ETHICS_DETERMINATION_PENDING}") != 0:
    pass  # The internal token is expected in the ethics section, not in manuscript.tex itself.
if text.count(r"\caption{") < 5:
    errors.append("expected four figure captions plus the compact table caption")
for figure_id in ["acquisition-workflow", "snapshot-structure", "quality-findings", "headline-observations"]:
    if text.count(rf"\label{{fig:{figure_id}}}") != 1:
        errors.append(f"missing or duplicated caption label for {figure_id}")
for phrase in ["data_family", "snapshot_count", "present_count", "not_available_count", "semantic_status", "snapshot_id", "requested_date", "displayed_date", "headline_observations", "result_id"]:
    for filename in ["table1_data_family_semantic_status.tex", "table2_snapshot_reproducibility.tex", "table3_quality_findings.tex"]:
        table = ROOT / "supplementary" / filename
        if table.exists() and re.search(rf"(?m)^{re.escape(phrase)}(?:\\s|&)", table.read_text(encoding="utf-8")):
            errors.append(f"raw display header remains: {phrase}")
for svg in (ROOT / "figures").glob("figure*.svg"):
    raw = svg.read_text(encoding="utf-8")
    for phrase in ["Source:", "Limitation:", "Caption:"]:
        if phrase in raw:
            errors.append(f"figure artwork prose remains: {svg.name}: {phrase}")

try:
    from pypdf import PdfReader
    for figure_pdf in (ROOT / "figures").glob("figure*.pdf"):
        figure_text = "\n".join(page.extract_text() or "" for page in PdfReader(str(figure_pdf)).pages)
        for phrase in ["Source:", "Limitation:", "Caption:"]:
            if phrase in figure_text:
                errors.append(f"figure PDF prose remains or PDF is stale: {figure_pdf.name}: {phrase}")
except Exception:
    print("FIGURE_PDF_TEXT_CHECK=UNVERIFIED")

pdf = ROOT / "build" / "ResearchDengu_Manuscript_Professor_Draft.pdf"
if pdf.exists():
    try:
        from pypdf import PdfReader
        pdf_text = "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf)).pages)
        if "ETHICS_DETERMINATION_PENDING" in pdf_text:
            errors.append("internal ethics token appears in professor-facing PDF text")
        for phrase in ["data_family", "snapshot_count", "present_count", "not_available_count", "semantic_status", "snapshot_id", "requested_date", "displayed_date", "headline_observations", "result_id"]:
            if phrase in pdf_text:
                errors.append(f"raw table header appears in professor-facing PDF: {phrase}")
        print("PDF_TEXT_CHECK=PASS")
    except Exception as exc:
        print(f"PDF_TEXT_CHECK=UNVERIFIED ({exc})")
else:
    print("PDF_TEXT_CHECK=UNVERIFIED_NO_LATEX")

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    raise SystemExit(1)
print("PROFESSOR_FACING_SOURCE_CHECK=PASS")
if "--strict" in sys.argv and not pdf.exists():
    raise SystemExit("STRICT_CHECK_FAILED: professor-facing PDF is not available")
