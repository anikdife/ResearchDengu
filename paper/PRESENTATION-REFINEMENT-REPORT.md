# Presentation refinement report

Scope was limited to the `paper/` presentation layer. No scientific source, data, analysis output, evidence contract, provenance artifact, or repository file outside `paper/` was modified.

## Checklist

| Item | Status | Evidence |
|---|---|---|
| Line numbering removed | PASS | `lineno` and `\\linenumbers` removed from `manuscript.tex` |
| Title block polished | PASS | Exact title/authors retained; prominent draft-status sentence removed |
| Abstract presentation | PASS | One unnumbered abstract with bold inline labels |
| Section hierarchy | PASS | Top-level sections owned by `manuscript.tex`; no manual numeric prefixes |
| Full Table 4 moved to supplement | PASS | Full 27-row, 9-column table is Supplementary Table S8 |
| Compact illustrative table retained | PASS | Three frozen snapshot rows remain in main manuscript |
| Tables 1--3 polished | PASS | Readable longtable sources, aligned columns, preserved values/statuses |
| Figure 1 cleaned | PASS | Source/Limitation/Caption blocks removed from artwork |
| Figure 2 cleaned | PASS | Source/Limitation/Caption blocks removed from artwork |
| Figure 3 cleaned | PASS | Source/Limitation/Caption blocks removed from artwork |
| Figure 4 cleaned | PASS | Source/Limitation/Caption blocks removed from artwork |
| Duplicated figure prose removed | PASS | No such blocks remain in `paper/figures/*.svg` |
| Supplementary tables configured | PASS | Separate `supplementary.tex`, landscape wide-table section, repeated headers |
| Reference presentation | PASS | Existing journal-neutral `references.bib` retained unchanged |
| Scientific text unchanged | PASS | No scientific paragraph edits made |
| Numerical values unchanged | PASS | Frozen values and structural signature retained |
| Visual QA of all compiled pages | NOT VERIFIED | Native LaTeX compiler unavailable: `latexmk` and standard TeX directories are absent |
| Unresolved submission placeholder preserved | PASS | Exactly one controlled marker remains: `ETHICS_DETERMINATION_PENDING` |

## Modified files

- `paper/manuscript.tex`
- `paper/supplementary.tex`
- `paper/supplementary/table4_restricted_descriptive_observations.tex` regenerated through the existing source workflow, without data edits
- `paper/figures/figure1_acquisition_workflow.svg`
- `paper/figures/figure1_acquisition_workflow.pdf`
- `paper/figures/figure2_snapshot_structure.svg`
- `paper/figures/figure2_snapshot_structure.pdf`
- `paper/figures/figure3_quality_findings.svg`
- `paper/figures/figure3_quality_findings.pdf`
- `paper/figures/figure4_restricted_headline_observations.svg`
- `paper/figures/figure4_restricted_headline_observations.pdf`
- `paper/PAPER-REPAIR-AUDIT.md`
- `paper/PAPER-REPAIR-REPORT.md`
- `paper/README.md`
- `paper/build.ps1`
- `paper/Makefile`
- `paper/build_sources.py`
- `paper/scripts/check_placeholders.py`
- `paper/scripts/check_manuscript_structure.py`

## Scientific preservation

The v0.4 source hash remains `ba1f457f82b4a2d55b8575e0532782b6161532504082a91698aa79dc8054c629`. The title, authors, abstract wording, methods, results, discussion, conclusion, citations, raw labels, classifications, unresolved limitations, and confirmed author contributions were preserved. The figure cleanup removed only duplicated Source/Limitation/Caption prose from artwork; those boundaries remain in LaTeX captions and manuscript text. The compact table values remain 82/0/82/0, 1,579/7/46,783/195, and 6,136/20/77,672/239.

## Build status

`paper/build.ps1 -Mode check` passes. `paper/build.ps1 -Mode draft` cannot run because `latexmk` is unavailable in this environment. Therefore the main and supplementary PDFs were not truthfully claimed as newly compiled or fully page-verified. Compile locally or on Overleaf with:

```powershell
.\paper\build.ps1 -Mode draft
.\paper\build.ps1 -Mode supplementary
```

Final status: `PRESENTATION_REFINEMENT_COMPLETE`

Submission status: `SUBMISSION_READINESS_PENDING_ETHICS_DETERMINATION`

The only unresolved substantive submission item is the formal Ethics/Data Governance determination. The local LaTeX toolchain is still unavailable, so newly compiled PDF page-level QA remains pending separately.
