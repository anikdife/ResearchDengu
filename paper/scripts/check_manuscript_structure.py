from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "manuscript.tex").read_text(encoding="utf-8")
errors = []
for required in [r"\\section\{Introduction\}", r"\\section\{Methods\}", r"\\section\{Results\}", r"\\section\{Discussion\}", r"\\section\{Conclusion\}", r"\\begin\{abstract\}", r"\\includegraphics\[width=0\.92\\linewidth\]\{figures/figure1_acquisition_workflow\.pdf\}"]:
    if not re.search(required, main):
        errors.append(f"missing {required}")
section_text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "sections").glob("*.tex"))
if re.search(r"\\sub(?:sub)?section\{\d+\.\d+", section_text):
    errors.append("manual subsection numbering remains")
if re.search(r"0\.0\.\d+", main + section_text):
    errors.append("0.0.x heading artifact remains")
if errors:
    for error in errors:
        print(f"ERROR: {error}")
    raise SystemExit(1)
print("STRUCTURE_CHECK_PASS")
