from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
files = [ROOT / "manuscript.tex", *(ROOT / "sections").glob("*.tex")]
patterns = {
    "ETHICS_DETERMINATION_PENDING": r"\\ethicspending\{",
}
total = 0
for label, pattern in patterns.items():
    count = sum(len(re.findall(pattern, p.read_text(encoding="utf-8"))) for p in files if p.exists())
    if count:
        total += count
        print(f"{label}: {count}")
print(f"TOTAL_PLACEHOLDER_OCCURRENCES={total}")
if "--strict" in sys.argv and total:
    raise SystemExit("STRICT_CHECK_FAILED: unresolved placeholders remain")
