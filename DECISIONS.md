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
| ADR-001 | Curation sources | Closed list in two tiers: journals by feed and PubMed; organizations and news by domain-restricted search. Approved for now; Filipe reviews it again before the MVP closes (F3-06) | — | `approved` | [ADR-0001](docs/decisions/0001-curation-sources.md) |
| ADR-002 | Publishing without review or indexing | What passes automatic validation is published; `noindex` everywhere, no sitemap; AI notice; simple withdrawal. Review, association with a physician and indexing wait for phase 9 | — | `approved` | [ADR-0002](docs/decisions/0002-publishing-without-review-or-indexing.md) |
| ADR-003 | Publishing format and path | Markdown with YAML frontmatter, one file per edition; PR opened by the project's GitHub App, auto-merged for allowed authors; withdrawal by `status: retirado`. Approval depends on F2-09 | — | `proposed` | [ADR-0003](docs/decisions/0003-publishing-format-and-path.md) |
| ADR-004 | Generation by the Claude API | A GitHub Actions script calls Sonnet 5.5 on candidates collected from the ADR-001 sources; structured output, grounding checked, up to US$30 a month. Replaces the Grok routine | — | `approved` | [ADR-0004](docs/decisions/0004-generation-by-claude-api.md) |

`—` means not implemented yet or not verified in the repository yet.

## How to record a new decision

1. Copy [`docs/decisions/_template.md`](docs/decisions/_template.md) to `docs/decisions/NNNN-short-slug.md`.
2. Fill in context, decision, alternatives, consequences, evidence and review triggers.
3. Add a row to the index above.
4. In `PROJECT_STATUS.md` → **Active decisions**, list only those that shape the current phase or were approved in it. Do not copy the whole index.
5. Once the choice is built and verified, fill **Implemented** with what actually exists.

## Changelog

| Date | Change |
| --- | --- |
| 2026-11-26 | F0-03: ADR-001 `approved` (Filipe's decision); the full review moves to F3-06 |
| 2026-11-26 | F0-06: index, ADRs and states translated to English (`pendente` → `pending`, `proposto` → `proposed`, `aprovado` → `approved`, `substituído` → `superseded`, `rejeitado` → `rejected`); ADR files 0001 to 0003 renamed to English slugs. No decision changed |
| 2026-11-25 | ADR-004 `approved` (Filipe's decision): generation by the Claude API instead of Grok. ADR-001 becomes `proposed`, with the initial two-tier list. ADR-003 swaps the Grok Bot submission for the GitHub App |
| 2026-11-15 | Initial log: ADR-001 `pending`, ADR-002 `approved` (final-plan decision), ADR-003 `proposed` |
