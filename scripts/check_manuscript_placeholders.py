from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
targets = [ROOT / "paper" / "manuscript.tex", *(ROOT / "paper" / "sections").glob("*.tex")]
patterns = [
    ("VERIFY BEFORE SUBMISSION", r"\\verify\{"),
    ("AUTHOR CONFIRMATION REQUIRED", r"\\authorconfirm\{"),
    ("JOURNAL-SPECIFIC AUTHORSHIP WORDING TO VERIFY", r"\\journalverify\{"),
    ("AI-ASSISTANCE DISCLOSURE TO FORMAT ACCORDING TO TARGET JOURNAL POLICY", r"\\aiverify\{"),
]
hits = []
for path in targets:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    for label, pattern in patterns:
        count = len(re.findall(pattern, text))
        if count:
            hits.append((label, path.relative_to(ROOT).as_posix(), count))

print("Controlled placeholder inventory:")
for label, path, count in hits:
    print(f"- {label}: {count} in {path}")
print(f"TOTAL_PLACEHOLDER_OCCURRENCES={sum(x[2] for x in hits)}")
if "--strict" in sys.argv and hits:
    print("STRICT_CHECK_FAILED: unresolved placeholders remain")
    raise SystemExit(1)
print("DRAFT_CHECK_PASS: placeholders are visible and inventoried")
