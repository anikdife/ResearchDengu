# ResearchDengu paper repair report

## Repair scope

This was a presentation, LaTeX, figure, table, and manuscript-engineering repair, followed by a human-author confirmation update. No new DGHS data, epidemiological analysis, scientific claim, numerical result, evidence contract, semantic interpretation, affiliation, ORCID, journal metadata, or submission action was introduced.

## Repairs completed

- `manuscript.tex` now owns the numbered top-level Introduction, Methods, Results, Discussion, and Conclusion sections.
- Methods, Results, and Discussion subsections now use LaTeX numbering without manually embedded `2.1`/`3.1`/`4.1` strings.
- The abstract is one conventional structured abstract with bold Background, Methods, Results, and Conclusions labels.
- The distracting affiliation/corresponding-author sentence was removed from the title page.
- Main tables 1--3 are retained; the full dense Table 4 is moved unchanged to Supplementary Table S8. Wide tables use landscape pages where appropriate.
- `paper/supplementary.tex` is a separate supplementary-material entry point with S1--S8 labels and repeated table headers.
- Four validated SVG figures were converted locally to PDF using headless Chromium with fixed dimensions and embedded as actual figures. The visible “PDF conversion is pending” placeholder was removed.
- Long SHA-256 strings remain character-for-character unchanged and are typeset as monospaced text.
- `paper/scripts/check_placeholders.py` and `paper/scripts/check_manuscript_structure.py` provide automated draft/structure checks; the placeholder checker now reports exactly `ETHICS_DETERMINATION_PENDING`.
- `paper/build.ps1` and `paper/Makefile` provide separate manuscript and supplementary build targets.

## Scientific preservation checks

The authoritative v0.4 source hash remains `ba1f457f82b4a2d55b8575e0532782b6161532504082a91698aa79dc8054c629`. The repaired source preserves the 27 historical states, 2024--2026 range, 9 dates/year, 16 retrieved-valid and 11 reused-verified statuses, 11 data families, 297 family rows, 108 headline values, 432 processed observations, 18 spot checks, all illustrative headline values, the structural signature `84efb756f47cbb24e1ad240bc2507576ead9cab3951e379ac0e618e7bb94a83d`, reconciliation classifications, revision limitations, and incomplete 2026 status.

## Build status

The repository's native LaTeX compiler is unavailable in this Windows execution environment; invocation returned `Unable to find standard directories for platform`. Therefore this repair does not claim a successful local LaTeX compilation. The source is prepared for Overleaf or a local TeX distribution using:

```powershell
.\paper\build.ps1 -Mode check
.\paper\build.ps1 -Mode draft
.\paper\build.ps1 -Mode supplementary
.\paper\build.ps1 -Mode manuscript
```

The `manuscript` mode intentionally fails while the ethics determination remains unresolved. The existing draft PDF is not represented as a successful LaTeX build.

## Remaining issues

Funding, conflicts, confirmed author contributions, authorship responsibility wording, AI disclosure, and conservative data/code release status are now resolved in the paper controls. Submission readiness remains pending only the formal Ethics/Data Governance determination, which is explicitly not inferred or resolved.

## Human-author confirmation update

The confirmed funding statement, no-conflicts statement, CRediT-style author contributions, human-author responsibility wording, and factual AI disclosure are now rendered without unresolved markers. Data and code availability use the documented conservative status: no public raw-data/code repository URL or release is claimed in this draft. Ethics remains factual and neutral, with `ETHICS_DETERMINATION_PENDING` as the sole unresolved control.
