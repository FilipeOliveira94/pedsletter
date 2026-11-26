# Project status

Operational record of the **current phase**. The issue backlog and the acceptance text live in [`ROADMAP.md`](ROADMAP.md). Decision index: [`DECISIONS.md`](DECISIONS.md). Chronological history: [`docs/status-log.md`](docs/status-log.md).

| Project | Current |
| --- | --- |
| Repository | [FilipeOliveira94/pedsletter](https://github.com/FilipeOliveira94/pedsletter) |
| Started | 2026-11-14 |
| Final plan approved | 2026-11-15 |
| Last update | 2026-11-26 (F0-03: ADR-001 approved) |
| Current phase | Phase 0 — Prerequisites |
| Phase status | In progress |

**Status values:** not started · in progress · delivered · verified · blocked · withdrawn

**Verified** means the acceptance was checked and the evidence is recorded (in `docs/status-log.md`, in the ADR or in the architecture doc). Planned architecture does not count as done.

**What goes here:** the current goal, progress on the phase's issues, the phase acceptance, the last validation, decisions that shape the work, active risks, blockers and next steps.

**What does not:** the cumulative issue inventory (`ROADMAP.md`), the full ADR table (`DECISIONS.md`), long history (`docs/status-log.md`).

---

## Current goal

**Phase 0** — accounts created, a cost and quality trial of the Claude API recorded, and ADR-001 to ADR-004 written.

On 2026-11-25 edition generation moved from the Grok routine to a script that calls the Claude API from GitHub Actions ([ADR-004](docs/decisions/0004-generation-by-claude-api.md)): Sonnet 5.5, up to US$30 a month, with news, guidelines and alerts in the MVP. The roadmap was rewritten in F0-07. On 2026-11-26 the repository docs were translated to English (F0-06). There is no site code.

## Next steps

1. **F0-08** — Cost and quality trial of the API. Spend authorized by Filipe on 2026-11-26; the plan still needs his approval.
2. **F0-01** — Accounts and repository. The Cloudflare Pages project linked to the repository is still missing.
3. **F0-05** — Check the acceptance of the rewritten ADR-003.

---

## Phase 0 progress

| ID | Title | Status | Evidence |
| --- | --- | --- | --- |
| F0-01 | Accounts and repository | Not started | Done early in the initial commit: README with the description and the AI notice |
| F0-02 | Test the Grok scheduled routine | Withdrawn | Replaced by F0-08 ([ADR-004](docs/decisions/0004-generation-by-claude-api.md)) |
| F0-03 | ADR-001: curation sources | Delivered | F0-03 PR; [`0001`](docs/decisions/0001-curation-sources.md) `approved`; full review in F3-06 |
| F0-04 | ADR-002: publishing without review or indexing | Delivered | F0-04 PR; acceptance checked in [`0002`](docs/decisions/0002-publishing-without-review-or-indexing.md) → Evidence |
| F0-05 | ADR-003: publishing format and path | Not started | [`0003`](docs/decisions/0003-publishing-format-and-path.md) rewritten in F0-07 for the GitHub App, `proposed` |
| F0-06 | Translate the docs to English | Delivered | F0-06 PR; `make docs-lint` passes |
| F0-07 | Rewrite the roadmap for the Claude API pipeline | Delivered | F0-07 PR; [ADR-004](docs/decisions/0004-generation-by-claude-api.md) `approved` |
| F0-08 | Cost and quality trial of the API | Not started | — |

Acceptance detail: `ROADMAP.md` → Phase 0.

### Phase 0 acceptance

- [ ] Accounts created: public repository, a Cloudflare Pages project linked to it and a Claude API account with a monthly spend limit.
- [ ] API trial recorded, with cost and quality measured (F0-08).
- [ ] ADR-001 to ADR-004 written.

---

## Last validation

| Validation | Detail |
| --- | --- |
| Date | 2026-11-26 |
| Environment | Local, WSL2 |
| Checks | `make docs-lint`, relative-link check, §4 notice and name search on ADR-002 |
| Result | See the F0-04 PR |

---

## Active decisions

| ID | Topic | State | Effect on the phase |
| --- | --- | --- | --- |
| ADR-001 | Curation sources | `approved` | Unblocks F0-08 and phase 2; reviewed again in F3-06 |
| ADR-002 | Publishing without review or indexing | `approved` | Defines the content rules in AGENTS.md §4 |
| ADR-003 | Publishing format and path | `proposed` | PR through the GitHub App; approval depends on F2-09 |
| ADR-004 | Generation by the Claude API | `approved` | Sonnet 5.5, GitHub Actions, up to US$30 a month; defines F0-08 and phase 2 |

## Active risks

- The cost per run is an estimate (about US$10 a month with Sonnet), not a measurement. F0-08 measures it before any pipeline code.
- The ADR-001 domains and feeds have not been checked. F2-11 checks them.
- Fetched text may carry an injected instruction into a site published without review. Mitigation: structured output, no write tool for the model, and grounding validation (F2-12, F2-13).
- The free-plan limits cited in the plan are from memory. Check them in F0-01.
- A professional's name may slip into a file, issue or commit before F1-06 exists. Until then, the AGENTS.md §4 rule is the only barrier.

## Blockers

None.

## Open questions

1. **Doses in the summaries:** generation writes no dose recommendation until there is review. The rule holds until Filipe says otherwise.
