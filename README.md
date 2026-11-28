# PedsLetter

AI-generated summaries of pediatric literature, guidelines, alerts and news, and of general medicine that affects pediatrics, published three times a week. A reference section for pediatricians (calculators, growth charts and other material) comes in later phases. A personal-use project with no sign-up, no e-mail and no ads; the only running cost is the Claude API, up to US$30 a month.

> **Aviso.** Curadoria e resumos gerados por IA, sem revisão por profissional de saúde. Confira sempre a fonte original.
>
> Conteúdo destinado a médicos e demais profissionais de saúde. É informativo: não é consulta, diagnóstico nem prescrição.

The notice above stays in Portuguese on purpose: it is the exact wording the site shows. In short, the summaries are AI-generated without review by a health professional, they are meant for physicians and other health professionals, and they are information, not a consultation, diagnosis or prescription. Always check the original source.

The site is not indexable: every page carries `noindex` and there is no sitemap. The `noindex` covers the site, not this repository, which is public. The summary files can be found through GitHub and search engines, and the notice above applies to them too.

---

## 📍 Status

| Status | Now |
| --- | --- |
| Current phase | Phase 1 — Site foundation. Not started; phase 0 closed on 2026-11-28 |
| Goal | A static site on `*.pages.dev`, not indexable, with the AI notice (F1-01, F1-03, F1-04, F1-06) |
| In the repository | Docs, ADR-001 to ADR-004 and the F0-08 trial script. No site code yet (it starts in F1-01) |
| Record | [`PROJECT_STATUS.md`](PROJECT_STATUS.md) · scope in [`ROADMAP.md`](ROADMAP.md) |

---

## ⚙️ What the project delivers

| Deliverable | State | Phases |
| --- | --- | --- |
| Static, non-indexable site with the AI notice | Planned | 1 |
| Content pipeline: collection from the sources → generation by the Claude API → PR → validation → automatic merge → publishing | Planned | 2 |
| MVP in use, with scheduled generation and news, guidelines and alerts | Planned | 3 |
| `pedsletter.com.br` domain | Planned | 9 |
| Drug-free calculators, growth charts and reference material | Planned | 5 to 8 |
| Clinical review, association with a physician, indexing and drug calculators | Future, only with an explicit decision | 9 |

The MVP is phases 0 to 3.

## 🧱 Planned stack

| Layer | Choice | Cost |
| --- | --- | --- |
| Site | Astro + Markdown, strict TypeScript | Free |
| Hosting | Cloudflare Pages (`*.pages.dev` until phase 9) | Free |
| Repository and CI | GitHub, public repository, GitHub Actions | Free |
| Analytics | None for now (F1-09 withdrawn); any future analytics stays cookieless | Free |
| Generation | A GitHub Actions script that calls the Claude API (Sonnet 5.5), Monday, Wednesday and Friday mornings ([ADR-004](docs/decisions/0004-generation-by-claude-api.md)) | Up to US$30 a month; one F0-08 run cost US$0.348 |
| Domain | `pedsletter.com.br` | Paid; phase 9 |

Details in [`docs/architecture/overview.md`](docs/architecture/overview.md).

## 🛠️ Commands

```bash
make help
```

`install`, `dev`, `build`, `lint` and `test` exist as placeholders and start working in F1-01.

## 🤝 How to contribute

1. Pick an issue from [`ROADMAP.md`](ROADMAP.md). One PR resolves one issue.
2. Create a feature branch from `main`, for example `feat/F1-03-site-nao-indexavel`.
3. Use Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `ci:`).
4. Open the PR citing the issue and the acceptance checked. Nobody commits straight to `main`.
5. Filipe reviews the PR, merges it and deletes the branch. The exception is content PRs, which the auto-merge workflow publishes when validation passes (F2-05).

Content rules that apply to files, issues, PRs and commits:

- The text uses only the generic "médico". No health professional's name, registration or training.
- No dose recommendation until there is review. A dose only appears attributed to the cited article.
- The AI curation notice is on every edition, on the home page and in this README.

The full rules are in [`AGENTS.md`](AGENTS.md).

## 📚 Documents

| Document | Contents |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Working rules for agents and contributors ([`CLAUDE.md`](CLAUDE.md) imports this file) |
| [`ROADMAP.md`](ROADMAP.md) | Phases 0 to 9, issues, acceptance and dependencies |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Operational record of the current phase |
| [`DECISIONS.md`](DECISIONS.md) | Decision index; full ADRs in [`docs/decisions/`](docs/decisions/) |
| [`docs/architecture/overview.md`](docs/architecture/overview.md) | Architecture: site, publishing and content pipeline |
| [`docs/project-genesis.md`](docs/project-genesis.md) | Summary of the final plan the project came from |
| [`docs/agent-workflow.md`](docs/agent-workflow.md) | Prompts to plan, implement and close an issue |
| [`docs/status-log.md`](docs/status-log.md) | Chronological history |

## 📄 License

[MIT](LICENSE). The license covers the code. The summarized articles belong to their authors and journals; each summary is written in our own words and links to the source.
