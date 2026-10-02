# Professor-facing final presentation QA

## Current disposition

The presentation-only source repairs are implemented in `paper/`, but the
four binary figure PDFs have not yet been refreshed from the cleaned SVG
sources. The local LaTeX toolchain is unavailable in this environment, so the
compiled manuscript PDF and final visual layout remain unverified. The package
is therefore not yet presentation-ready.

## Source-level result

1. Ethics internal token hidden from rendered PDF: **UNVERIFIED_NO_LATEX**. The typesetting macro suppresses `ETHICS_DETERMINATION_PENDING`; no current professor-facing PDF was available for extraction.
2. Factual unresolved ethics statement retained: **PASS**.
3. Figure 1 internal prose removed: **PASS**.
4. Figure 2 internal prose removed: **PASS**.
5. Figure 3 internal prose removed: **PASS**.
6. Figure 4 internal prose removed: **PASS**.
   The existing binary figure PDFs still contain the earlier duplicated prose
   and must be regenerated with `paper/scripts/refresh_figures.ps1`.
7. Exactly one formal caption per figure: **PASS at source level**; PDF verification awaits compilation.
8. Figure scientific values preserved: **PASS**; only Source/Limitation/Caption artwork blocks were removed.
9. Table 1 display headers human-readable: **PASS**.
10. Table 2 display headers human-readable: **PASS**.
11. Table 3 display headers human-readable: **PASS**.
12. Underlying table values unchanged: **PASS**; header mapping is applied only during LaTeX generation and source CSVs are untouched.
13. Line numbering remains disabled: **PASS**.
14. Scientific prose unchanged: **PASS**, apart from authorized movement of figure notes and administrative token suppression.
15. Numerical values unchanged: **PASS**.
16. Final professor-facing PDF visual QA: **UNVERIFIED_NO_LATEX**.

## Automated checks

`paper/scripts/check_professor_facing.py` checks that:

- the factual ethics paragraph remains;
- raw schema headers do not remain in Tables 1--3;
- `Source:`, `Limitation:`, and `Caption:` blocks do not remain in figure SVG artwork;
- the expected figure labels/captions exist;
- a compiled professor-facing PDF, when present, does not contain `ETHICS_DETERMINATION_PENDING` or raw table headers.

The internal QA state continues to report exactly one unresolved item: `ETHICS_DETERMINATION_PENDING`.

## Files modified in this surgical correction

- `paper/manuscript.tex`
- `paper/build_sources.py`
- `paper/build.ps1`
- `paper/scripts/check_professor_facing.py`
- `paper/supplementary/table1_data_family_semantic_status.tex`
- `paper/supplementary/table2_snapshot_reproducibility.tex`
- `paper/supplementary/table3_quality_findings.tex`
- `paper/figures/figure1_acquisition_workflow.svg`
- `paper/figures/figure1_acquisition_workflow.pdf`
- `paper/figures/figure2_snapshot_structure.svg`
- `paper/figures/figure2_snapshot_structure.pdf`
- `paper/figures/figure3_quality_findings.svg`
- `paper/figures/figure3_quality_findings.pdf`
- `paper/figures/figure4_restricted_headline_observations.svg`
- `paper/figures/figure4_restricted_headline_observations.pdf`
- this QA report

No scientific source or repository artifact outside `paper/` was modified.

## Status

`PROFESSOR_FACING_PRESENTATION_NOT_READY`

## Required next local action

From the repository root, refresh the four binary figure assets:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\paper\scripts\refresh_figures.ps1
```

Then rerun the professor-facing QA script. After the figure PDFs are clean,
compile and visually inspect the manuscript in Overleaf or another verified
LaTeX environment before changing the status to
`PROFESSOR_FACING_SOURCE_READY_OVERLEAF_VERIFICATION_REQUIRED`.
