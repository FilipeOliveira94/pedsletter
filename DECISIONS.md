# Decision log

Short index of PedsLetter's decisions. **Rationale, alternatives, consequences and evidence live in the ADRs** in [`docs/decisions/`](docs/decisions/).

| Log | Reference |
| --- | --- |
| Contains | Decision index and state |
| Detail | [`docs/decisions/`](docs/decisions/) (one ADR per decision) |
| Related | `PROJECT_STATUS.md`, `ROADMAP.md`, `docs/project-genesis.md`, `AGENTS.md` |

**How to use it:** read the table for the direction and what already exists; open the ADR for the why. **Decision** is what was chosen or proposed; **Implemented** is what is verified in the repository, with evidence in the ADR or the architecture doc and in `docs/status-log.md`.

## Lifecycle

| State | Meaning |
| --- | --- |
| `pending` | Open decision, waiting for information; the ADR records what is missing |
| `proposed` | Preferred option for planning; not binding until approved |
| `approved` | Accepted by Filipe's decision or with evidence from a verified issue |
| `superseded` | Replaced by a later ADR |
| `rejected` | Turned down; kept for the record |

**Rules:** no ADR names a health professional; when the state or the implementation changes, update this index and the ADR together.

## Index

| ID | Topic | Decision | Implemented | State | ADR |
| --- | --- | --- | --- | --- | --- |
| ADR-001 | Curation sources | Closed list in two tiers: journals by feed and PubMed; organizations and news by domain-restricted search. Approved for now; Filipe reviews it again before the MVP closes (F3-03, which took F3-06) | — | `approved` | [ADR-0001](docs/decisions/0001-curation-sources.md) |
| ADR-002 | Publishing without review or indexing | What passes automatic validation is published; `noindex` everywhere, no sitemap; AI notice; simple withdrawal. Review, association with a physician and indexing wait for phase 9 | — | `approved` | [ADR-0002](docs/decisions/0002-publishing-without-review-or-indexing.md) |
| ADR-003 | Publishing format and path | Markdown with YAML frontmatter, one file per edition; PR opened by the project's GitHub App and merged by GitHub's auto-merge once the `main` ruleset's required checks pass (Filipe's choice of 2026-11-27); no merge workflow; withdrawal by `status: retirado`. Approval depends on F2-09 | — | `proposed` | [ADR-0003](docs/decisions/0003-publishing-format-and-path.md) |
| ADR-004 | Generation by the Claude API | A Python script in GitHub Actions, started from the F0-08 trial code, calls Sonnet 5.5 on candidates collected from the ADR-001 sources; structured output, each item checked before any push, up to US$30 a month split between scheduled runs, development and eval runs, and a reserve. Tier 2 items carry no numbers until F3-07. Amended on 2026-11-26, and on 2026-11-27 at gate G0 (two calls, edition slots; F0-08 measured US$4.52 a month). Replaces the Grok routine | — | `approved` | [ADR-0004](docs/decisions/0004-generation-by-claude-api.md) |

`—` means not implemented yet or not verified in the repository yet.

## Waivers

A waiver lets work skip a roadmap rule for a stated scope and time (`ROADMAP.md`: "Do not start a phase before its dependencies are met, or before an explicit waiver is recorded in `DECISIONS.md`").

| ID | Rule waived | What it allows | Decided | Ends |
| --- | --- | --- | --- | --- |
| W1 | Phase gate: phase 2 starts only after phase 1 | Phase 2 issues follow their own issue-level dependencies, so they can start before phase 1 closes. Until F2-05 exists, Filipe dispatches the generation run, uploads the validated file and merges the PR himself after CI passes. The checks are the same | Filipe, 2026-11-26 (D5 in [`docs/plan-review-2026-11-26.md`](docs/plan-review-2026-11-26.md)) | When F2-05 is verified |

## How to record a new decision

1. Copy [`docs/decisions/_template.md`](docs/decisions/_template.md) to `docs/decisions/NNNN-short-slug.md`.
2. Fill in context, decision, alternatives, consequences, evidence and review triggers.
3. Add a row to the index above.
4. In `PROJECT_STATUS.md` → **Active decisions**, list only those that shape the current phase or were approved in it. Do not copy the whole index.
5. Once the choice is built and verified, fill **Implemented** with what actually exists.

## Changelog

| Date | Change |
| --- | --- |
| 2026-11-27 | F0-08: ADR-004 amended at gate G0 with Filipe's decisions: two calls (search, then rank and write) and the edition slots applied by the script. Evidence: the measured cost, US$0.348 a run |
| 2026-11-27 | F0-09: ADR-003's path changes to the GitHub App PR merged by GitHub's auto-merge (Filipe's choice of 2026-11-27, after the job commit approved on 2026-11-26 proved incompatible with a "PR required" ruleset); still `proposed`. ADR-004 amended with Filipe's decisions of 2026-11-26: Python from the F0-08 trial, the budget split, no numbers in tier 2 items, the eval set before the first model or prompt change. New Waivers section with W1 (phase gate) |
| 2026-11-26 | F0-03: ADR-001 `approved` (Filipe's decision); the full review moves to F3-06 |
| 2026-11-26 | F0-06: index, ADRs and states translated to English (`pendente` → `pending`, `proposto` → `proposed`, `aprovado` → `approved`, `substituído` → `superseded`, `rejeitado` → `rejected`); ADR files 0001 to 0003 renamed to English slugs. No decision changed |
| 2026-11-25 | ADR-004 `approved` (Filipe's decision): generation by the Claude API instead of Grok. ADR-001 becomes `proposed`, with the initial two-tier list. ADR-003 swaps the Grok Bot submission for the GitHub App |
| 2026-11-15 | Initial log: ADR-001 `pending`, ADR-002 `approved` (final-plan decision), ADR-003 `proposed` |
