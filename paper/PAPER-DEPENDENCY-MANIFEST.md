# ResearchDengu Paper Dependency Manifest

This manifest covers the files required to compile the main manuscript and
the supplementary document from an isolated copy of `paper/`. Every active
project-specific compile dependency is physically inside `paper/`.

| TYPE | REFERENCED BY | LOCAL PATH | EXISTS | SOURCE ORIGIN | STATUS |
|---|---|---|---|---|---|
| Main manuscript | Overleaf main file | `manuscript.tex` | YES | existing paper asset | LOCAL |
| Supplementary manuscript | Overleaf supplementary file | `supplementary.tex` | YES | existing paper asset | LOCAL |
| Section files | `manuscript.tex` | `sections/*.tex` | YES | existing paper assets | LOCAL |
| Supplementary section files | `supplementary.tex` | `supplementary/*.tex` | YES | existing paper assets | LOCAL |
| Materialized tables | `manuscript.tex`, `supplementary.tex` | `supplementary/*.tex` | YES | existing paper assets | LOCAL |
| Figure 1 SVG/PDF | `manuscript.tex` | `figures/figure1_acquisition_workflow.svg`, `figures/figure1_acquisition_workflow.pdf` | YES | existing paper assets; PDF regenerated from local SVG | LOCAL |
| Figure 2 SVG/PDF | `manuscript.tex` | `figures/figure2_snapshot_structure.svg`, `figures/figure2_snapshot_structure.pdf` | YES | existing paper assets; PDF regenerated from local SVG | LOCAL |
| Figure 3 SVG/PDF | `manuscript.tex` | `figures/figure3_quality_findings.svg`, `figures/figure3_quality_findings.pdf` | YES | existing paper assets; PDF regenerated from local SVG | LOCAL |
| Figure 4 SVG/PDF | `manuscript.tex` | `figures/figure4_restricted_headline_observations.svg`, `figures/figure4_restricted_headline_observations.pdf` | YES | existing paper assets; PDF regenerated from local SVG | LOCAL |
| Bibliography | `manuscript.tex` | `references.bib` | YES | existing paper asset | LOCAL |
| Figure conversion wrappers | local maintenance only | `figure1.html`–`figure4.html` | YES | created under paper for portable local regeneration | LOCAL |

The Python/PowerShell maintenance helpers are not compile inputs for Overleaf.
They are retained for local regeneration and QA only. No active LaTeX command
loads a file outside `paper/`, and no symlink or junction is required.
