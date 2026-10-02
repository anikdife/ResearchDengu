# ResearchDengu

ResearchDengu evaluates the reproducibility and data quality of Bangladesh's
public DGHS Dengue Dashboard as a research-data interface.

The study concerns dashboard observations and their provenance. It does not
claim to measure the underlying national surveillance system, population
incidence, infection burden, transmission risk, or causal effects.

## Manuscript

**Reproducibility and Data Quality of Bangladesh's Public DGHS Dengue Dashboard:
An Empirical Evaluation**

## Authors

- **Tajrian Sarwar, MBBS** — First author; conceptualization, methodology,
  investigation, data curation, formal analysis, validation, manuscript drafting,
  review/editing, and project administration.

- **Md Aminul Islam** — Software, data curation, validation, and manuscript
  review/editing.

Status: Manuscript prepared for submission.

## Methodological features

- historical dashboard-state reconstruction;
- provenance-preserving archival workflow;
- SHA-256 integrity records;
- semantic validation;
- reconciliation auditing;
- bounded revision and stability assessment;
- restricted descriptive analysis.

## Dataset scope

The validated study scope is:

- 27 historical dashboard states;
- 2024–2026;
- nine dates per year;
- 2026 is incomplete.

This is not continuous daily coverage.

## Repository structure

- `paper/` — self-contained LaTeX manuscript and supplementary material.
- `src/` — public extraction, validation, and analysis code.
- `scripts/` — bounded public-interface inspection and validation tools.
- `tests/` — offline and invariant tests.
- `provenance/` — selected public provenance records and hashes.
- `data/` — data-availability and redistribution policy.
- `docs/` — public methodological and release documentation.

## Reproducibility

The manuscript package can be compiled by opening `paper/manuscript.tex`
in Overleaf or a local LaTeX installation.

Raw DGHS response archives are not redistributed. The repository therefore does
not claim complete end-to-end raw-data reproduction.

The acquisition scripts are limited to publicly accessible interfaces and must
not be used to bypass authentication, CAPTCHA, access controls, or rate limits.

## Ethics and data governance

This study used publicly accessible aggregate dashboard observations and did
not process patient-level identifiers in the analyzed tables. Formal
institutional review or exemption status has not yet been determined.

## Limitations

Dashboard observations are not automatically equivalent to population incidence,
risk, or causal evidence. Geographic and case semantics remain bounded by the
documented source interface and provenance evidence. The 2026 period is
incomplete.

## Citation

See `CITATION.cff`.

## License

See `LICENSE`. Raw source materials and third-party content remain subject to
their own terms.
