from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
MD = ROOT / "manuscript" / "ResearchDengu-Manuscript-v0.4.md"

def esc(s: str) -> str:
    placeholders = {}
    def hold(value):
        key = f"ZZPLACEHOLDER{len(placeholders)}ZZ"
        placeholders[key] = value
        return key
    s = s.replace("[VERIFY BEFORE SUBMISSION]", hold(r"\verify{VERIFY BEFORE SUBMISSION}"))
    s = s.replace("[AUTHOR CONFIRMATION REQUIRED]", hold(r"\authorconfirm{AUTHOR CONFIRMATION REQUIRED}"))
    s = s.replace("[JOURNAL-SPECIFIC AUTHORSHIP WORDING TO VERIFY]", hold(r"\journalverify{JOURNAL-SPECIFIC AUTHORSHIP WORDING TO VERIFY}"))
    s = s.replace("[AI-ASSISTANCE DISCLOSURE TO FORMAT ACCORDING TO TARGET JOURNAL POLICY]", hold(r"\aiverify{AI-ASSISTANCE DISCLOSURE TO FORMAT ACCORDING TO TARGET JOURNAL POLICY}"))
    s = s.replace("[1–7]", hold(r"\citep{ref1,ref2,ref3,ref4,ref5,ref6,ref7}"))
    s = s.replace("[1,6]", hold(r"\citep{ref1,ref6}"))
    s = s.replace("[1–4,6,7]", hold(r"\citep{ref1,ref2,ref3,ref4,ref6,ref7}"))
    for n in range(1, 8):
        s = s.replace(f"[{n}]", hold(rf"\citep{{ref{n}}}"))
    s = s.replace("–", "--").replace("—", "---").replace("’", "'").replace("‘", "`").replace("“", "``").replace("”", "''")
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("^", r"\textasciicircum{}"), ("~", r"\textasciitilde{}")]:
        s = s.replace(a, b)
    s = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + m.group(1) + "}", s)
    s = re.sub(r"\*([^*]+)\*", lambda m: r"\emph{" + m.group(1) + "}", s)
    for key, value in placeholders.items():
        s = s.replace(key, value)
    return s

def convert(lines):
    out, paragraph = [], []
    def flush():
        if paragraph:
            out.append(esc(" ".join(x.strip() for x in paragraph)))
            out.append("")
            paragraph.clear()
    for line in lines:
        if not line.strip():
            flush(); continue
        if line.startswith("### "):
            flush()
            heading = re.sub(r"^\d+\.\d+\s+", "", line[4:].strip())
            out.append(r"\subsection{" + esc(heading) + "}"); out.append(""); continue
        if line.startswith("## "):
            flush(); out.append(r"\section{" + esc(line[3:].strip()) + "}"); out.append(""); continue
        if line.startswith("# "):
            flush(); out.append(r"\section*{" + esc(line[2:].strip()) + "}"); out.append(""); continue
        if line.startswith("- "):
            flush(); out.append(r"\begin{itemize}\item " + esc(line[2:].strip()) + r"\end{itemize}"); continue
        paragraph.append(line)
    flush()
    return "\n".join(out)

text = MD.read_text(encoding="utf-8")
parts = re.split(r"(?m)^(?=## )", text)
sections = {}
for part in parts:
    if not part.strip():
        continue
    m = re.match(r"## ([^\n]+)\n", part)
    if m:
        key = re.sub(r"[^a-z0-9]+", "-", m.group(1).lower()).strip("-")
        sections[key] = part.splitlines()[1:]

(PAPER / "sections").mkdir(parents=True, exist_ok=True)
(PAPER / "supplementary").mkdir(parents=True, exist_ok=True)
for key, lines in sections.items():
    converted = convert(lines)
    if key == "abstract":
        converted = converted.replace(r"\subsection{Background}", r"\noindent\textbf{Background:}")
        converted = converted.replace(r"\subsection{Methods}", r"\medskip\noindent\textbf{Methods:}")
        converted = converted.replace(r"\subsection{Results}", r"\medskip\noindent\textbf{Results:}")
        converted = converted.replace(r"\subsection{Conclusions}", r"\medskip\noindent\textbf{Conclusions:}")
    if key == "funding":
        converted = "This research received no external funding."
    if key == "conflicts-of-interest":
        converted = "The authors declare no conflicts of interest."
    if key == "author-contributions":
        converted = ("Tajrian Sarwar: conceptualization, methodology, investigation, data curation, formal analysis, "
                     "validation, writing -- original draft, writing -- review \\& editing, and project administration. "
                     "Software is not attributed to Tajrian Sarwar.\n\n"
                     "Md Aminul Islam: software, data curation, validation, and writing -- review \\& editing.\n\n"
                     "Both authors reviewed and approved the manuscript and accept responsibility for their respective contributions.")
    if key == "ai-assistance-disclosure":
        converted = ("Generative AI-assisted tools, including Codex/ChatGPT, contributed to software/code development and "
                     "manuscript drafting/editing. The human authors directed the research, reviewed and validated scientific "
                     "outputs, and retain responsibility for the final analyses, interpretations, authorship, and accountability.")
    if key == "data-availability":
        converted = ("The source data were publicly accessible DGHS dashboard responses. ResearchDengu archived and reconstructed "
                     "selected historical responses and produced processed and derived research tables with project-level provenance. "
                     "Release of raw responses or a public repository package is not promised by this draft; no public repository URL is claimed.")
    if key == "code-availability":
        converted = ("The project contains reproducible acquisition, validation, provenance, extraction, and restricted-analysis scripts "
                     "under \\texttt{scripts/} and \\texttt{src/analysis/}. A public code repository is not claimed in this draft, and no public release URL is supplied.")
    if key == "ethics-data-governance":
        converted = ("This study used publicly accessible aggregate dashboard observations and did not process patient-level identifiers in the analyzed tables. "
                     "Formal institutional review or exemption status has not yet been determined. \\ethicspending{ETHICS_DETERMINATION_PENDING}")
    if key == "2-methods":
        converted = converted.replace(
            "A formal institutional review or exemption determination is not claimed; the applicable local governance requirements for any future submission are \\verify{VERIFY BEFORE SUBMISSION}.",
            "Formal institutional review or exemption status has not yet been determined.")
    (PAPER / "sections" / f"{key}.tex").write_text(converted, encoding="utf-8")

def table_tex(path: Path, label: str) -> str:
    rows = list(csv.reader(path.open(encoding="utf-8-sig", newline="")))
    if not rows:
        return ""
    display_headers = {
        "table1_data_family_semantic_status.csv": ["Data family", "Snapshots", "Present", "Not available", "Semantic status"],
        "table2_snapshot_reproducibility.csv": ["Snapshot", "Year", "Requested date", "Displayed date", "Headline observations", "Semantic status"],
        "table3_quality_findings.csv": ["Result ID", "Metric", "Value", "Classification", "Limitation"],
    }
    if path.name in display_headers:
        rows[0] = display_headers[path.name]
    cols = len(rows[0])
    width = 0.96 / cols
    widths = "".join([rf"P{{{width:.4f}\linewidth}}" for _ in range(cols)])
    out = [r"\begingroup\footnotesize\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.15}", rf"\begin{{longtable}}{{{widths}}}", r"\toprule"]
    out.append(" & ".join(esc(x) for x in rows[0]) + r" \\")
    out.append(r"\midrule\endhead")
    for row in rows[1:]:
        vals = row + [""] * (cols - len(row))
        out.append(" & ".join(esc(x) for x in vals[:cols]) + r" \\")
    out += [r"\bottomrule", r"\end{longtable}", r"\endgroup", ""]
    return "\n".join(out)

for folder in [ROOT / "manuscript" / "tables", ROOT / "manuscript" / "supplementary"]:
    for csv_path in sorted(folder.glob("*.csv")):
        out_name = re.sub(r"[^a-z0-9]+", "_", csv_path.stem.lower()).strip("_") + ".tex"
        (PAPER / "supplementary" / out_name).write_text(table_tex(csv_path, csv_path.stem), encoding="utf-8")
