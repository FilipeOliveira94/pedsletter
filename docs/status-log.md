# Status log (archive)

Chronological history of status updates. The operational record is [`PROJECT_STATUS.md`](../PROJECT_STATUS.md) (current phase only; **rewritten** every phase). Entries for closed phases and long narratives come here. Architecture docs and ADRs cite this log, or carry the facts in their own text, not `PROJECT_STATUS.md`.

Newest entries first.

---

### 2026-11-28 — F1-03: non-indexable site

`public/robots.txt` allows everything, with no `Disallow` and no `Sitemap` line. `public/_headers` keeps `X-Robots-Tag: noindex, nofollow` on `/*` and adds `Content-Security-Policy: script-src 'none'`. The two §4 notices moved from `src/config/site.ts` to `src/config/avisos.json`, which `site.ts` imports, so the checker reads the same copy. `scripts/site_check.py` (Python stdlib), run by `make site-check` in the CI `build` job after `make build`, walks `dist/` and fails, naming the file and the rule, on: a page without a robots meta that includes `noindex`; a page without the audience notice, or a page in `aiNoticePaths` without the AI notice (text hidden from the reader does not count); a `<script>` outside `scriptAllowedPaths`; a sitemap file or `<link rel="sitemap">`; a missing `robots.txt` or one with `Disallow` or `Sitemap`; a `_headers` without the header or the policy on `/*`, or one that detaches either with `!`; an empty build. The path rules live in `src/config/site-check.json`: the AI notice is required on `index.html`, and no page may have a script. F1-04 adds the edition route and phase 5 the calculators. The job names did not change, so the ruleset did not either.

Checks:

| Acceptance | Evidence |
| --- | --- |
| `noindex` in the meta tag and the `X-Robots-Tag` header | `make site-check` on the build passes. On the branch preview (`feat-f1-03-site-nao-indexave.pedsletter.pages.dev`) and the deployment preview, a GET of `/`, `/robots.txt` and an unknown path answers 200 with `x-robots-tag: noindex, nofollow`; `/` has `<meta name="robots" content="noindex, nofollow">` |
| No sitemap | `dist/` has only `index.html`, `_headers` and `robots.txt`; unit tests fail a `sitemap*.xml`, `.xml.gz`, `.txt` and a sitemap link |
| `robots.txt` has no `Disallow` | The preview serves the committed file. Before this change, production served the home page's HTML at `/robots.txt` (Cloudflare's fallback with no `404.html`) |
| The walker fails on a missing `noindex` or notice, or a `<script>` | 42 unit tests on temporary `dist/` folders, one per rule, plus passing cases (an allowed script path, entities and line breaks in a notice). A copy of the real build broken by hand (meta removed, a `<script>`, a `Disallow`, a sitemap file, the policy removed) failed with five findings and exit 1 |
| `_headers` sets `script-src 'none'` | The preview answers with `content-security-policy: script-src 'none'` on every path tried |

Also run: `make test` (all tests), `make lint`, `make build`, `make docs-lint` and `make authorship` with a placeholder name. Production (`pedsletter.pages.dev`) gets the new headers and `robots.txt` only after the merge, and is not checked here. Size seen Md: about 520 hand-written lines with the tests, over the Sm limit.

### 2026-11-28 — F1-06: absence-of-authorship check

`scripts/authorship_check.py` (Python stdlib) fails when a fixed term or a blocked proper name appears. The seven fixed terms live in `src/config/authorship.json`, each written with a JSON escape, so no file holds a term in plain text. The three docs that quoted the list (the ROADMAP F1-06 row, ADR-002 and the F0-04 entry below) now name it instead, by Filipe's decision; the check has no exemption. The names come only from the `AUTHORSHIP_BLOCKED_NAMES` environment variable; a missing or empty one is a setup error (exit 2). Matching ignores case, accents and runs of whitespace, decodes HTML entities, reads each line with and without its tags and catches a phrase split across two lines. The output gives the source, the line and the list index, never the term, the name or the line; a path that matches is redacted.

CI gains an `authorship` job (install, build, `make test`, then `make authorship` over the tracked files, `dist/` and the PR title and body, with the secret on that step only), and PR runs now also trigger on `edited`. `make hooks` points `core.hooksPath` at `scripts/hooks`, whose pre-commit hook runs the check on the staged files. `scan_text` is the API the generation job calls before any push (F2-13). `make test` now runs the unit tests.

Checks:

| Acceptance | Evidence |
| --- | --- |
| A CI script over the built HTML and the repository files | `make build && make authorship` locally: 50 sources scanned, passed. The `authorship` CI run on the PR is the CI evidence |
| A block-list term fails and points to file and line | Unit tests for each of the seven terms, case, accents, nbsp, entities, tags, attributes and line breaks. A term appended to `README.md` locally failed with `README.md:92: term #3` and a file/line annotation |
| Names come from a secret; missing or empty fails | Unit tests; locally `make authorship` exits 2 with the variable unset and with it empty |
| Output gives file, line and index, never the term | Unit tests assert the term, the name and the line text are absent from the output, and that a matching path is redacted |
| Runs on PR text; the generation job calls it | A term in `PR_BODY` failed locally with `PR_BODY:1: term #3`. The generation job does not exist yet; F2-13 calls `scan_text` |
| Pre-commit hook reads names from the environment | Unit test in a temporary repository: a staged term is refused, an unset variable is refused, a clean commit passes |

`make test` (29 tests), `make docs-lint` and `make lint` pass. Not exercised here: the generation job's call (the job comes in F2-13) and the CI run with the real secret, which is the PR's `authorship` run once Filipe sets it. Size seen Md: about 520 hand-written lines with the tests, over the Sm limit.

### 2026-11-28 — F1-01: Astro project, CI and preview deploy

The repository now has a static Astro 7.4.13 site with strict TypeScript (the `strictest` preset; TypeScript 6.0.3, since `@astrojs/check` 0.9.12 supports only 5 and 6), installed with npm from exact pins and a lockfile, Node.js 22.23.4 (`.nvmrc`). The only page is a placeholder home with both §4 notices and the noindex meta tag. `src/config/site.ts` holds the `indexavel` switch (off) and the notice texts, and `public/_headers` sends `X-Robots-Tag: noindex, nofollow` on every path. There is no sitemap and no `robots.txt`. The Makefile `install`, `dev`, `build` and `lint` targets work; `test` stays a placeholder until F1-03.

CI (`.github/workflows/ci.yml`) runs `build` (install, `astro check`, build) and `docs-lint` on every PR and every push to `main`, with a read-only token, actions pinned by commit SHA, `persist-credentials: false`, no `paths:` filter and no secret. The "secrets set per step" criterion holds vacuously: the workflow has no secret, and its header says a later job sets one with `env:` on the step that uses it (F1-06, F2-05). Dependabot updates the actions and the npm packages weekly. `build` and `docs-lint` are required checks of the `protect-main` ruleset, reported by GitHub Actions only (integration 15368). Filipe set the Cloudflare Pages build (`docs/accounts.md`) and turned deployments on.

Checks:

| Acceptance | Evidence |
| --- | --- |
| A type error fails the build | On PR #19, a commit adding `export const quebra: number = "texto";` failed `build` at `make lint` with `ts(2322)` (run 46103108695); its revert passed (run 46103165990). Same result locally with `make lint` |
| A preview per branch, none for a fork PR | The `Cloudflare Pages` check passed on the branch, and `feat-f1-01-astro-ci-preview.pedsletter.pages.dev` answers 200. Fork PRs: Cloudflare's GitHub integration and known-issues pages say they get no preview and no setting changes it; not exercised, since there is no second account, and Filipe accepted the docs as evidence |
| Previews keep `noindex` | `curl -I` on the branch and the deployment preview URLs shows `x-robots-tag: noindex, nofollow`; the HTML has `<meta name="robots" content="noindex, nofollow">`, both notices and no `<script>` |
| Pinned actions, Dependabot, per-step secrets, no persisted credentials | `ci.yml` and `dependabot.yml` as above |
| CI jobs are required checks | A `gh api` read of ruleset 27377947 lists `build` and `docs-lint` with integration 15368; PR #19 merge state `CLEAN` |

Also run: `make docs-lint`, `make build`, a §4 term search of the diff.

---

### 2026-11-28 — Phase 0 closed

Every phase 0 acceptance item is checked and every phase 0 issue is delivered or withdrawn (F0-01 to F0-11; F0-02 withdrawn). Gate G0 passed on 2026-11-27: proceed with Sonnet 5.5. The phase row in `ROADMAP.md` is `Delivered`. `PROJECT_STATUS.md` was rewritten for phase 1, and the README status table now names phase 1; its stack table also moves the domain to phase 9 (D13), drops the analytics that F1-09's withdrawal removed (D10), and gives the F0-08 run cost.

Checks: the phase 0 issue table read row by row; `make docs-lint`; a §4 term search of the diff.

---

### 2026-11-28 — F0-10: status docs trimmed

Issue status now lives only in the `ROADMAP.md` tables. `PROJECT_STATUS.md` dropped its phase 0 progress table, its copy of the phase acceptance, the "Last validation" table, the "Active decisions" table and its "Last update" row; it keeps the current goal, next steps, active risks, blockers and open questions. The "Changelog" tables in `ROADMAP.md` and `DECISIONS.md` were dropped, with the roadmap's "Last update" row: each row repeated `git log`, this log or an ADR's Evidence section. The only roadmap row with no entry here (2026-11-24) is copied below. This log stays, because it holds the checks behind each issue, which `git log` does not. `AGENTS.md` §12 lists only the files still updated when an issue closes (D12), and `DECISIONS.md` no longer asks for a copy of active decisions in `PROJECT_STATUS.md`.

Checks: `make docs-lint`; a search for references to the dropped sections; a §4 term search of the diff.

---

### 2026-11-28 — F0-05: ADR-003 acceptance checked

ADR-003 records the `.md` format, the PR opened by the GitHub App and merged by GitHub's auto-merge once the required checks pass, and the withdrawal mechanism; it stays `proposed` until F2-09. The check found the `status: retirado` row behind F2-07 and F2-11: the withdrawn page also shows the date, and the bot's block list is the F2-11 validation that fails a file reusing a withdrawn URL. The ADR and the architecture overview now say so; the decision did not change. With F0-05, every phase 0 acceptance item is checked; F0-10 is the last open issue.

Checks: `make docs-lint`; a §4 term search of the diff.

---

### 2026-11-28 — F0-01: accounts and repository

Filipe created the Cloudflare Pages project `pedsletter` on the free plan, linked to this repository, with no build command and the output directory `dist`, then paused automatic production and preview deployments (his confirmation; the agent cannot read that setting). The build Cloudflare runs on creation, on `09061f2`, failed as intended, and as of 2026-11-28 `pedsletter.pages.dev` serves nothing (522). F1-01 sets the build and turns deployments on.

The GitHub side was already in place and was only read: the `protect-main` ruleset (PR required with no approval, no force push, no deletion, no bypass actors), a read-only default `GITHUB_TOKEN` and secret scanning push protection. The free-plan limits from the Cloudflare and GitHub pages are in [`docs/accounts.md`](accounts.md); expected use fits them. Open for F2-05: the ruleset's `require_extra_approval_for_unattributed_changes` flag and App PRs. Open for F1-01: whether a fork PR gets a Cloudflare preview.

Checks: `gh api` reads of the repository, ruleset, Actions permissions and check runs; `curl` on `pedsletter.pages.dev`; `make docs-lint`.

---

### 2026-11-27 — F0-11: dose rule corrected

During F0-08 Filipe allowed a dose in a summary when the linked article states it and the summary attributes it to the article; no dose of our own appears, the calculators included. D8, the roadmap generation rule and F2-13 still banned every dose. F0-11 aligns them with `AGENTS.md` §4, which already allowed an attributed dose.

What changed in the docs:

- `ROADMAP.md`: the generation rule; F2-13 drops only an unattributed dose, with the attribution phrases and dose patterns in `src/config/` and four dose fixtures; F1-04 marks each dose with a visible "confira no artigo" mark and the same text on hover, at build time; F9-05 takes calculator doses from resolutions, guidelines and other public sources.
- D8 in the plan review, ADR-004 step 3, the architecture overview and the project genesis carry a dated amendment.

Accepted residual risk: the screen checks for an attribution phrase and, through the tier 1 number check, that the dose's numbers are in the abstract; it cannot compare the wording with the article.

Check: `make docs-lint`.

---

### 2026-11-27 — F0-08: API trial recorded, gate G0 passed

Three paid runs of the trial script ([`spikes/F0-08/trial.py`](../spikes/F0-08/trial.py)) on 2026-11-27, US$0.494 in all, matching the Console's US$0.49. Run 1 (one call, search and structured output together) produced 6 articles and no search. Filipe then set the two-call flow and the edition slots. Run 2 stopped before the write call: every search came back `too_many_requests`, because the `pedsletter` workspace's web search limit was 0; Filipe set it to 2 a second. Run 3 searched 8 times and produced 3 articles, 1 guideline and 2 news items for US$0.348, US$4.52 a month at 13 runs.

Filipe approved the edition with Sonnet 5.5 (gate G0) and asked for a page to review the selection log later (F7-08). The trial report is [`docs/spikes/F0-08-api-trial.md`](spikes/F0-08-api-trial.md). ADR-004 is amended with the two calls and the slots; F2-11 to F2-13 take the trial's findings. The edition and run outputs stay in the git-ignored `spikes/F0-08/out/`.

Checks: 66 unit tests of the trial script, the dry run, `make docs-lint`. The key file was deleted after each run and Filipe disabled the key.

---

### 2026-11-27 — F0-09: plan-review decisions recorded

On 2026-11-26 four agents reviewed the plan: three critics (security and risk, performance, minimalist) and one that combined their findings. Filipe decided D1 otherwise: the main user does not see the F0-08 trial edition, the MVP goes live without the main user's check, and the main user's answer stays in F3-03. He approved D2 to D13 as proposed. The combined plan, with his decisions, is in [`plan-review-2026-11-26.md`](plan-review-2026-11-26.md).

D9 had approved a job commit with the Actions `GITHUB_TOKEN`. GitHub's docs show that a ruleset cannot exempt that token, so the commit could not pass the "PR required" rule planned for F0-01. On 2026-11-27 Filipe chose the GitHub App PR with GitHub's auto-merge instead: no custom merge workflow, and the App's private key stays. ADR-003 now records that path and stays `proposed`.

What changed in the docs:

- `ROADMAP.md`: merged, cut, deferred and new issues, raised ratings, restated metrics, gates G0 to G3, phase 4 folded into phase 9, and F0-09 and F0-10 added.
- `DECISIONS.md`: a Waivers section with W1, the phase-gate waiver.
- ADR-004: amended for Python from the F0-08 trial, the budget split and no numbers in tier 2 items.
- `AGENTS.md`: the domain moves to phase 9 in §1; §4 now covers posts about the project; the line on removing a pushed name now matches GitHub's docs; the publishing, fork and analytics lines follow the new path.
- The architecture overview: the new path and checks.

F0-08's own changes from D2 go in F0-08's PR. Docs only. The checks were `make docs-lint`, a relative-link check, a roadmap consistency check and a §4 search of the diff; the PR has their output.

---

### 2026-11-26 — F0-03: ADR-001 approved

Filipe approved the ADR-001 source list as it stands, to be reviewed again before the MVP closes. ADR-001 is now `approved`, and the review is a new issue, F3-06 (Lo, Sm), in phase 3 after the two weeks of operation (F3-02) and before the usage decision (F3-03). The domains and feeds are still unchecked; F2-11 checks them. Docs only; `make docs-lint` passes.

---

### 2026-11-26 — F0-04: ADR-002 acceptance checked

ADR-002 records the decision, the rationale, the mitigations and the phase 9 review conditions, and names no professional. A search for names, the registration acronym and the forms of address in the ADR finds nothing, and the two §4 notices match the `AGENTS.md` wording byte for byte. The ADR predated ADR-004, so the F2-13 grounding check was added to its mitigations and its consequences now say what that check does not catch. The decision and the `approved` state did not change. Docs only; `make docs-lint` passes.

---

### 2026-11-26 — F0-06: docs translated to English

The repository docs are now in English: `README.md`, `ROADMAP.md`, `PROJECT_STATUS.md`, `DECISIONS.md`, `docs/architecture/`, `docs/decisions/` (ADRs 0001 to 0003, the index README and the template), `docs/project-genesis.md` and this log. The `Makefile` help text and messages and the comments and messages of `scripts/check_markdown_tables.py` were translated too (Filipe's decision). Code logic did not change.

What stays in Portuguese: the §4 mandatory notices with their exact wording (README included), quoted site and UI text, and the frontmatter field names and values. Issue and ADR IDs did not change, and no decision, rule or acceptance criterion changed.

Filipe approved renaming the Portuguese file names: `docs/architecture/visao-geral.md` → `overview.md`, `0001-fontes-de-curadoria.md` → `0001-curation-sources.md`, `0002-publicacao-sem-revisao-e-sem-indexacao.md` → `0002-publishing-without-review-or-indexing.md`, `0003-formato-e-caminho-de-publicacao.md` → `0003-publishing-format-and-path.md`. Every link was updated. ADR states are now `pending`, `proposed`, `approved`, `superseded` and `rejected`; roadmap and status values are in English too. `AGENTS.md` lost the line that kept older docs in Portuguese until F0-06. The ADR header tables got named headers (`ADR-0001 | Detail`) instead of the generic `Campo | Valor`.

Checks: `make docs-lint` and `make help` pass; a relative-link check over every versioned Markdown file finds no broken link; the two §4 notices are byte-identical to the `AGENTS.md` wording wherever they appear.

---

### 2026-11-25 — F0-07: Claude API pipeline

Filipe decided to move edition generation from the Grok routine to the Claude API, starting with Sonnet 5.5, up to US$30 a month, and with news, guidelines and alerts in the MVP. The decision is in [ADR-004](decisions/0004-generation-by-claude-api.md), `approved`.

The roadmap was rewritten: F0-02 and F2-06, which depended on Grok, were withdrawn; F0-08 (cost and quality trial), F2-10 to F2-15 (GitHub App, collector, generator, grounding, budget, failure alert), F3-05 (evaluation set) and F7-07 (reference material) were added. F3-04 moved to phase 1, and the growth charts come before the other phase 6 calculators. ADR-001 got the initial two-tier list and became `proposed`; ADR-003 swaps the Grok Bot for the GitHub App, because a PR opened with the Actions `GITHUB_TOKEN` does not trigger PR validation. `AGENTS.md` replaces the zero-cost rule with one of up to US$30 a month for the API and widens Hi risk.

The cost estimate (about US$10 a month with Sonnet over 13 runs) was not measured; F0-08 measures it. Docs only; `make docs-lint` passed.

---

### 2026-11-24 — Size and risk ratings

Size and risk replaced small/large in the workflow (`AGENTS.md` §3), and every issue got the Expected/Seen Risk and Size columns. New F0-06: translate the docs to English. (From the roadmap's Changelog, dropped in F0-10.)

---

### 2026-11-17 — Markdown tables with named headers

6 key-value tables had an empty header row (`| | |`), which GFM shows as a blank row on top. The pattern came from another project's planning docs, used as a template, and spread by copying. Each table now has a header taken from context (`Projeto | Atual`, `Validação | Detalhe`, `Roadmap | Atual`, `Registro | Referência`, `ADRs | Local`; English since F0-06). `scripts/check_markdown_tables.py` fails if any versioned Markdown file has an empty header outside code blocks; it runs with `make docs-lint`. The rule is in AGENTS.md §9.

---

### 2026-11-15 — Initial project structure

Filipe approved PedsLetter's final plan on 2026-11-15. The repository structure was created in a direct commit to `main`, `chore: estrutura inicial do projeto`, the last one outside a feature branch.

Created: `README.md` (rewritten, with the AI notice and the `noindex` note), `AGENTS.md`, `CLAUDE.md` (imports `AGENTS.md`), `ROADMAP.md` (phases 0 to 9, 59 issues), `DECISIONS.md`, `PROJECT_STATUS.md`, `LICENSE` (MIT), `Makefile`, `.gitignore`, `docs/agent-workflow.md`, `docs/project-genesis.md`, `docs/architecture/visao-geral.md` (now `overview.md`) and `docs/decisions/` with the template and three ADRs: ADR-001 `pendente` (waiting for the source list), ADR-002 `aprovado` (final-plan decision) and ADR-003 `proposto` (depends on F0-02).

The full ADRs live in `docs/decisions/`, not in `docs/adr/` as the plan said, to follow the reference project's scheme. The plan's appendix on professional identification did not enter the repository.

Docs and skeleton only; no site code. `make help` lists the six targets. `install`, `dev`, `build`, `lint` and `test` are placeholders and exit with an error until F1-01. No issue was closed: phase 0 issues close by PR.
