# Project status

Operational record of the **current phase**. The issue backlog and the acceptance text live in [`ROADMAP.md`](ROADMAP.md). Decision index: [`DECISIONS.md`](DECISIONS.md). Chronological history: [`docs/status-log.md`](docs/status-log.md).

| Project | Current |
| --- | --- |
| Repository | [FilipeOliveira94/pedsletter](https://github.com/FilipeOliveira94/pedsletter) |
| Started | 2026-11-14 |
| Final plan approved | 2026-11-15 |
| Last update | 2026-11-27 (F0-08: API trial recorded; gate G0 passed) |
| Current phase | Phase 0 — Prerequisites |
| Phase status | In progress |

**Status values:** not started · in progress · delivered · verified · blocked · withdrawn

**Verified** means the acceptance was checked and the evidence is recorded (in `docs/status-log.md`, in the ADR or in the architecture doc). Planned architecture does not count as done.

**What goes here:** the current goal, progress on the phase's issues, the phase acceptance, the last validation, decisions that shape the work, active risks, blockers and next steps.

**What does not:** the cumulative issue inventory (`ROADMAP.md`), the full ADR table (`DECISIONS.md`), long history (`docs/status-log.md`).

---

## Current goal

**Phase 0** — accounts created, a cost and quality trial of the Claude API recorded and gate G0 decided, and ADR-001 to ADR-004 written.

On 2026-11-25 edition generation moved from the Grok routine to a script that calls the Claude API from GitHub Actions ([ADR-004](docs/decisions/0004-generation-by-claude-api.md)): Sonnet 5.5, up to US$30 a month, with news, guidelines and alerts in the MVP. The roadmap was rewritten in F0-07. On 2026-11-26 the repository docs were translated to English (F0-06). There is no site code.

On 2026-11-26 a plan review proposed changes, and Filipe decided on them: D1 otherwise, D2 to D13 as proposed. On 2026-11-27 he chose the GitHub App PR with GitHub's auto-merge for publishing. F0-09 recorded both in the roadmap, the ADRs and `AGENTS.md`; the review is [`docs/plan-review-2026-11-26.md`](docs/plan-review-2026-11-26.md). The first published edition now comes after 11 issues, under waiver W1.

## Next steps

1. **Dose rule correction** — Filipe allowed on 2026-11-27 a dose stated in the article and attributed to it; the D8 record, the roadmap generation rule and the F2-13 dose screen still ban every dose. A separate change corrects them.
2. **F0-01** — Accounts and repository: the Cloudflare Pages link, the free-plan limits, the `main` ruleset (PR required), a read-only default token and push protection.
3. **F0-05** — Check the acceptance of ADR-003, which F0-09 updated for GitHub's auto-merge.
4. **F0-10** — Trim the status docs; any time after F0-09.

---

## Phase 0 progress

| ID | Title | Status | Evidence |
| --- | --- | --- | --- |
| F0-01 | Accounts and repository | Not started | Done early in the initial commit: README with the description and the AI notice |
| F0-02 | Test the Grok scheduled routine | Withdrawn | Replaced by F0-08 ([ADR-004](docs/decisions/0004-generation-by-claude-api.md)) |
| F0-03 | ADR-001: curation sources | Delivered | F0-03 PR; [`0001`](docs/decisions/0001-curation-sources.md) `approved`; full review in F3-03 |
| F0-04 | ADR-002: publishing without review or indexing | Delivered | F0-04 PR; acceptance checked in [`0002`](docs/decisions/0002-publishing-without-review-or-indexing.md) → Evidence |
| F0-05 | ADR-003: publishing format and path | Not started | [`0003`](docs/decisions/0003-publishing-format-and-path.md) updated in F0-09 for GitHub's auto-merge, `proposed` |
| F0-06 | Translate the docs to English | Delivered | F0-06 PR; `make docs-lint` passes |
| F0-07 | Rewrite the roadmap for the Claude API pipeline | Delivered | F0-07 PR; [ADR-004](docs/decisions/0004-generation-by-claude-api.md) `approved` |
| F0-08 | Cost and quality trial of the API | Delivered | F0-08 PR; [`docs/spikes/F0-08-api-trial.md`](docs/spikes/F0-08-api-trial.md); gate G0 passed |
| F0-09 | Record the plan-review decisions | Delivered | F0-09 PR; [`docs/plan-review-2026-11-26.md`](docs/plan-review-2026-11-26.md) |
| F0-10 | Trim the status docs | Not started | — |

Acceptance detail: `ROADMAP.md` → Phase 0.

### Phase 0 acceptance

- [ ] Accounts created: public repository, a Cloudflare Pages project linked to it and a Claude API account with a monthly spend limit.
- [x] API trial recorded, with cost and quality measured (F0-08).
- [x] Gate G0 decided from the trial.
- [ ] ADR-001 to ADR-004 written.

---

## Last validation

| Validation | Detail |
| --- | --- |
| Date | 2026-11-27 |
| Environment | Local, WSL2 |
| Checks | F0-08: 66 unit tests of the trial script, `trial.py --dry-run`, three paid runs (the third produced the edition), `make docs-lint` |
| Result | See the F0-08 PR and [`docs/spikes/F0-08-api-trial.md`](docs/spikes/F0-08-api-trial.md) |

---

## Active decisions

| ID | Topic | State | Effect on the phase |
| --- | --- | --- | --- |
| ADR-001 | Curation sources | `approved` | Unblocks F0-08 and phase 2; reviewed again in F3-03 |
| ADR-002 | Publishing without review or indexing | `approved` | Defines the content rules in AGENTS.md §4 |
| ADR-003 | Publishing format and path | `proposed` | GitHub App PR merged by GitHub's auto-merge (Filipe's choice of 2026-11-27); approval depends on F2-09 |
| ADR-004 | Generation by the Claude API | `approved` | Sonnet 5.5, GitHub Actions, up to US$30 a month; amended on 2026-11-26 (Python from the F0-08 trial, budget split, tier 2 items without numbers) and on 2026-11-27 at G0 (two calls, edition slots); defines phase 2 |

Waiver W1 (`DECISIONS.md`): phase 2 issues follow their own dependencies, and Filipe merges the editions until F2-05 exists.

## Active risks

- One measured run cost US$0.348 (US$4.52 a month at 13 runs). Cost varies with the candidate count and the searches; F3-02 measures two weeks. The search call's worst-case bound is US$1.15 a run, so F2-12's per-run cap must stay well under it.
- Until F3-03, only Filipe's read catches an error that got past the checks; the main user is asked only once the MVP is live (Filipe's decision D1 of 2026-11-26).
- The ADR-001 domains and feeds have not been checked. F2-11 checks them.
- Fetched text may carry an injected instruction into a site published without review. Mitigation: structured output, no write tool for the model, and the pre-push gate (F2-12, F2-13).
- The free-plan limits cited in the plan are from memory. Check them in F0-01.
- Whether GitHub's auto-merge works on this repository is unverified; F2-05 checks it, and until then Filipe merges (W1).
- A professional's name may slip into a file, issue or commit before F1-06 exists. Until then, the AGENTS.md §4 rule is the only barrier; F1-06 now comes right after F1-01.

## Blockers

None.

## Open questions

1. **Doses in the summaries:** Filipe decided on 2026-11-27 that a summary may give a dose only as the article states it, attributed to it, and that no dose of our own appears (the calculators included). D8 as recorded bans every dose; the correction of D8, the generation rule and F2-13 is the next step above.
