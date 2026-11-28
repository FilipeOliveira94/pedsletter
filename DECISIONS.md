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
| W2 | Phase gate: phase 3 starts only after phase 2 | F3-08 (free-tier model survey) runs before phase 3. It is a check of provider docs with no code and no API call; F3-09 keeps its dependencies | Filipe, 2026-11-28, in the F3-08 thread | When F3-08 is delivered |

## How to record a new decision

1. Copy [`docs/decisions/_template.md`](docs/decisions/_template.md) to `docs/decisions/NNNN-short-slug.md`.
2. Fill in context, decision, alternatives, consequences, evidence and review triggers.
3. Add a row to the index above.
4. Once the choice is built and verified, fill **Implemented** with what actually exists.
