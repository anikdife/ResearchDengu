# ResearchDengu LaTeX manuscript

This is a journal-neutral, single-column LaTeX presentation of `manuscript/ResearchDengu-Manuscript-v0.4.md`. The Markdown manuscript and scientific artifacts remain authoritative and unchanged.

The main entry point is `manuscript.tex`; the separate supplementary entry point is `supplementary.tex`. Validated figures are supplied as both SVG and PDF under `figures/`.

Human-author confirmation has resolved funding, conflicts, author contributions, authorship responsibility wording, AI disclosure, and conservative data/code release status. Formal institutional review or exemption status has not yet been determined.

The professor-facing manuscript has no line numbering. Tables 1--3 remain in the main manuscript; the full restricted descriptive-observation table is Supplementary Table S8. Supplementary tables are compiled separately.

Use the repository-root commands:

```text
make draft
make check
make manuscript
```

`draft` permits unresolved controlled placeholders and makes them visible in red. `check` scans placeholders and references without network access. `manuscript` is intended to require a clean check before a submission build; current unresolved declarations therefore keep the workflow in draft status.

On Windows PowerShell, the equivalent commands are:

```powershell
.\paper\build.ps1 -Mode check
.\paper\build.ps1 -Mode draft
.\paper\build.ps1 -Mode manuscript
.\paper\build.ps1 -Mode supplementary
```
