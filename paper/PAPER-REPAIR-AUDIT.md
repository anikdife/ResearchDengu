# ResearchDengu paper repair audit

## Authoritative sources

- Scientific source: `manuscript/ResearchDengu-Manuscript-v0.4.md`.
- Source hash before repair: `ba1f457f82b4a2d55b8575e0532782b6161532504082a91698aa79dc8054c629`.
- LaTeX source repaired: `paper/manuscript.tex`.
- Bibliography source: `paper/references.bib`, derived from the seven-item `manuscript/references-v0.3.md` list.
- Prior visual draft: `paper/build/ResearchDengu-Manuscript-v0.4-DRAFT.pdf`.

No later authoritative v0.x manuscript was found. Frozen data, provenance, evidence contracts, and scientific source artifacts were not modified.

## Existing paper tree and defects found

The pre-repair tree contained `manuscript.tex`, section files, generated supplementary longtables, a bibliography, build helpers, and a draft PDF. Section files manually embedded numbers such as `2.1`, `3.1`, and `4.1` while the main document did not own the corresponding top-level sections. The abstract labels were subsection commands rather than one structured abstract. Supplementary longtables were included in the main document. Figure 1 was represented by a visible “PDF conversion is pending” fallback instead of an embedded figure.

## Figure inventory

The authoritative validated SVG set is present in `manuscript/figures/` and duplicated in the validated derived-figure locations. Four figures were copied into `paper/figures/` and converted locally to PDF with fixed-dimension headless Chromium rendering, without redrawing:

1. `figure1_acquisition_workflow`
2. `figure2_snapshot_structure`
3. `figure3_quality_findings`
4. `figure4_restricted_headline_observations`

The LaTeX manuscript embeds all four PDF conversions. Labels, values, arrows, and scientific annotations were not edited.

## Table inventory

The main-text presentation retains Tables 1--3: data-family semantic status (11 rows, 5 columns), snapshot reproducibility (27, 6), and quality findings (5, 5). The full restricted descriptive observations table (27 rows, 9 columns) is now Supplementary Table S8. Supplementary material also contains result provenance (10, 7), reconstruction criteria, snapshot sampling (27, 9), category anomalies (11, 7), reconciliation audit (9, 7), revision/stability audit (4, 6), and the supplementary registry index (9, 2). Raw labels and values are preserved.

## References and placeholders

The seven existing references are represented in `references.bib`; no literature or bibliographic fact was added. Following the subsequent human-author confirmation, the paper controls retain exactly one controlled unresolved marker: `ETHICS_DETERMINATION_PENDING`.

## Planned/modified presentation files

The repair modifies only files under `paper/` plus this audit and the repair report. Main and supplementary entry points are `paper/manuscript.tex` and `paper/supplementary.tex`. Paper-only QA scripts are under `paper/scripts/`. The existing scientific Markdown source and frozen artifacts remain outside the presentation repair scope.
