# ResearchDengu Public-Release Audit

Date: 2026-10-02

## Release boundary

The current workspace is a private/development evidence repository, not a
public-release repository and not a Git repository. It must not be published
directly. A separate staging tree is required before any Git initialization,
commit, or push.

## Workspace inventory

| Area | Observed contents | Initial classification |
|---|---|---|
| `paper/` | Self-contained LaTeX manuscript, supplementary material, local figures, bibliography, presentation QA | PUBLIC_INCLUDE_AFTER_SANITIZATION |
| `src/` | Dashboard extraction, validation, and analysis code; Python cache files also present | PUBLIC_INCLUDE_AFTER_SANITIZATION; exclude caches |
| `scripts/` | Local dashboard inspection, capture, parsing, POST forensics, historical acquisition, validation, and reporting scripts | Mixed; include only bounded/public-safe scripts after code audit |
| `tests/` | Offline and invariant tests plus Python cache files | PUBLIC_INCLUDE_AFTER_SANITIZATION; exclude caches |
| `data/historical_acquisition/` | Archived DGHS response bodies and extracted observations | UNRESOLVED_DO_NOT_PUBLISH pending redistribution review |
| `data/historical_pilot/` | Pilot response archives and failure logs | PRIVATE_EXCLUDE pending review |
| `data/post_tests/` | A/B/C response bodies and metadata | UNRESOLVED_DO_NOT_PUBLISH pending redistribution review |
| `data/date_semantics_retest/`, `data/year_validation/` | Response archives | UNRESOLVED_DO_NOT_PUBLISH pending redistribution review |
| `data/dashboard_snapshots/` | Raw dashboard response archive | UNRESOLVED_DO_NOT_PUBLISH pending redistribution review |
| `data/processed/`, `data/derived/` | Processed and derived research tables/figures | PUBLIC_INCLUDE_AFTER_SANITIZATION only after explicit redistribution decision |
| `metadata/` | Provenance, semantic contracts, manifests, hashes, and internal release-stage records | Mixed; curate individually |
| `outputs/` | Stage outputs, validation records, figures, tables, and internal evidence artifacts | Mixed; curate individually |
| `docs/` | Scientific methods/audits plus internal stage-gate and agent-directed reports | Mixed; retain public scientific documentation, exclude workflow chatter |
| `manuscript/` | Versioned Markdown manuscripts, review packages, traceability files, and older drafts | PRIVATE_EXCLUDE by default; public package should use current `paper/` |
| `notebooks/` | Notebook workspace | UNRESOLVED_DO_NOT_PUBLISH until reviewed for outputs, paths, and metadata |
| `tmp/` | Browser profiles, caches, rendered previews, conversion artifacts, and temporary files | PRIVATE_EXCLUDE |
| root `paper.zip` | Existing archive with unknown contents and release provenance | UNRESOLVED_DO_NOT_PUBLISH |
| root configuration files | `.gitignore`, `pyproject.toml`, `requirements.txt`, Makefile, Docker files | PUBLIC_INCLUDE_AFTER_SANITIZATION; verify actual public workflow |

## Candidate public package

The isolated staging package should contain, at minimum:

- a new public-facing `README.md`;
- the current `paper/` copied as a unit;
- `CITATION.cff` updated to the current manuscript identity;
- `LICENSE` with clearly stated scope;
- the reviewed public research code and offline tests;
- `data/README.md` documenting that raw DGHS responses are not redistributed;
- a curated provenance/methodology subset only after path and privacy review;
- `docs/public-release/` documentation.

The staging package should not contain raw dashboard responses, browser
profiles, temporary files, Codex prompts, internal stage instructions, private
notes, old review packages, or unreviewed generated outputs.

## Scientific and ethics status

The manuscript is prepared for submission. The public release must preserve
the scientific freeze, the author order, the presentation state, and the
factual ethics wording:

> This study used publicly accessible aggregate dashboard observations and did
> not process patient-level identifiers in the analyzed tables. Formal
> institutional review or exemption status has not yet been determined.

The release must not state or imply that ethics approval was unnecessary,
waived, obtained, or exempt.

## Data redistribution decision

No authorization to redistribute the archived raw DGHS responses was found in
the inspected workspace. Raw HTML responses and response archives are
therefore excluded from the initial public package. A public `data/README.md`
should describe the source, bounded acquisition workflow, validated scope,
provenance approach, and this non-redistribution decision without encouraging
access-control circumvention.

## Secret and privacy scan

The initial manual pattern scan of candidate source/document areas found no
matching credential or private-key pattern. This is not a substitute for a
final scan of the completed staging tree. The final release must scan the
staging tree again and must stop if any credential, cookie, token, private key,
or unnecessary personal information is found.

Author names are appropriate scholarly metadata. No personal contact details,
addresses, phone numbers, correspondence, or unrelated documents should be
included.

## Machine-path findings

Machine-specific paths occur in internal documentation and local tooling
instructions, including Windows paths used for local execution. These files
must be excluded, sanitized, or replaced with relative/public instructions in
the staging package. Frozen evidence artifacts must not be silently edited;
they should be excluded or represented by a documented sanitized derivative.

## Publication blockers

1. The workspace has no Git remote or repository metadata.
2. The isolated `release/github/ResearchDengu/` staging copy has not yet been
   created because the local execution approval quota was exhausted during the
   copy operation.
3. Raw-response redistribution has not been authorized.
4. The public README, curated data policy, dependency manifest, and final
   staging-tree secret/path scan remain to be completed.
5. No GitHub owner/account or target remote URL was supplied, so no external
   repository can be selected or pushed safely yet.

## Current release classification

`PUBLIC_RELEASE_BLOCKED_PENDING_STAGING_AND_REVIEW`

No public repository has been initialized, committed, or pushed by this task.
