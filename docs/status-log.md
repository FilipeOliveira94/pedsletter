# Status log (archive)

Chronological history of status updates. The operational record is [`PROJECT_STATUS.md`](../PROJECT_STATUS.md) (current phase only; **rewritten** every phase). Entries for closed phases and long narratives come here. Architecture docs and ADRs cite this log, or carry the facts in their own text, not `PROJECT_STATUS.md`.

Newest entries first.

---

### 2026-11-26 — F0-03: ADR-001 approved

Filipe approved the ADR-001 source list as it stands, to be reviewed again before the MVP closes. ADR-001 is now `approved`, and the review is a new issue, F3-06 (Lo, Sm), in phase 3 after the two weeks of operation (F3-02) and before the usage decision (F3-03). The domains and feeds are still unchecked; F2-11 checks them. Docs only; `make docs-lint` passes.

---

### 2026-11-26 — F0-04: ADR-002 acceptance checked

ADR-002 records the decision, the rationale, the mitigations and the phase 9 review conditions, and names no professional. A search for names and for "CRM", "Dr." and "Dra." in the ADR finds nothing, and the two §4 notices match the `AGENTS.md` wording byte for byte. The ADR predated ADR-004, so the F2-13 grounding check was added to its mitigations and its consequences now say what that check does not catch. The decision and the `approved` state did not change. Docs only; `make docs-lint` passes.

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

### 2026-11-17 — Markdown tables with named headers

6 key-value tables had an empty header row (`| | |`), which GFM shows as a blank row on top. The pattern came from another project's planning docs, used as a template, and spread by copying. Each table now has a header taken from context (`Projeto | Atual`, `Validação | Detalhe`, `Roadmap | Atual`, `Registro | Referência`, `ADRs | Local`; English since F0-06). `scripts/check_markdown_tables.py` fails if any versioned Markdown file has an empty header outside code blocks; it runs with `make docs-lint`. The rule is in AGENTS.md §9.

---

### 2026-11-15 — Initial project structure

Filipe approved PedsLetter's final plan on 2026-11-15. The repository structure was created in a direct commit to `main`, `chore: estrutura inicial do projeto`, the last one outside a feature branch.

Created: `README.md` (rewritten, with the AI notice and the `noindex` note), `AGENTS.md`, `CLAUDE.md` (imports `AGENTS.md`), `ROADMAP.md` (phases 0 to 9, 59 issues), `DECISIONS.md`, `PROJECT_STATUS.md`, `LICENSE` (MIT), `Makefile`, `.gitignore`, `docs/agent-workflow.md`, `docs/project-genesis.md`, `docs/architecture/visao-geral.md` (now `overview.md`) and `docs/decisions/` with the template and three ADRs: ADR-001 `pendente` (waiting for the source list), ADR-002 `aprovado` (final-plan decision) and ADR-003 `proposto` (depends on F0-02).

The full ADRs live in `docs/decisions/`, not in `docs/adr/` as the plan said, to follow the reference project's scheme. The plan's appendix on professional identification did not enter the repository.

Docs and skeleton only; no site code. `make help` lists the six targets. `install`, `dev`, `build`, `lint` and `test` are placeholders and exit with an error until F1-01. No issue was closed: phase 0 issues close by PR.
