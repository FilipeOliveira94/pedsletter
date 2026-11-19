# PedsLetter

Resumos de literatura pediátrica gerados por IA, publicados três vezes por semana, com calculadoras clínicas previstas para as fases seguintes. Projeto de uso pessoal, sem custo de operação, sem cadastro, sem e-mail e sem publicidade.

> **Aviso.** Curadoria e resumos gerados por IA, sem revisão por profissional de saúde. Confira sempre a fonte original.
>
> Conteúdo destinado a médicos e demais profissionais de saúde. É informativo: não é consulta, diagnóstico nem prescrição.

O site não é indexável: toda página leva `noindex` e não há sitemap. O `noindex` cobre o site, não este repositório, que é público. Os arquivos dos resumos ficam acháveis pelo GitHub e por buscadores, e o aviso acima vale também para eles.

---

## 📍 Status

| Campo | Agora |
| --- | --- |
| Fase atual | Fase 0 — Pré-requisitos. Não iniciada |
| Objetivo | Contas, teste da rotina agendada do Grok e ADRs (F0-01 a F0-05) |
| No repositório | Documentação e esqueleto. Nenhum código do site ainda (começa em F1-01) |
| Registro | [`PROJECT_STATUS.md`](PROJECT_STATUS.md) · escopo em [`ROADMAP.md`](ROADMAP.md) |

---

## ⚙️ O que o projeto entrega

| Entrega | Estado | Fases |
| --- | --- | --- |
| Site estático não indexável, com aviso de IA | Planejado | 1 |
| Pipeline de conteúdo: arquivo `.md` → PR → validação → merge automático → publicação | Planejado | 2 |
| MVP em uso, com a rotina agendada | Planejado | 3 |
| Domínio `pedsletter.com.br` | Planejado | 4 |
| Calculadoras sem fármaco | Planejado | 5 a 8 |
| Revisão clínica, associação a um médico, indexação e calculadoras com fármaco | Futuro, só com decisão explícita | 9 |

O MVP são as fases 0 a 3.

## 🧱 Stack prevista

| Camada | Escolha | Custo |
| --- | --- | --- |
| Site | Astro + Markdown, TypeScript estrito | Gratuito |
| Hospedagem | Cloudflare Pages (`*.pages.dev` até a fase 4) | Gratuito |
| Repositório e CI | GitHub, repositório público, GitHub Actions | Gratuito |
| Analytics | Cloudflare Web Analytics, sem cookies | Gratuito |
| Curadoria | Rotina agendada no Grok, segunda, quarta e sexta de manhã | Plano já em uso; F0-02 confirma |
| Domínio | `pedsletter.com.br` | Único custo; fase 4 |

Detalhe em [`docs/architecture/visao-geral.md`](docs/architecture/visao-geral.md).

## 🛠️ Comandos

```bash
make help
```

`install`, `dev`, `build`, `lint` e `test` existem como marcadores e passam a funcionar em F1-01.

## 🤝 Como contribuir

1. Escolha uma issue do [`ROADMAP.md`](ROADMAP.md). Um PR resolve uma issue.
2. Crie uma branch de feature a partir da `main`, por exemplo `feat/F1-03-site-nao-indexavel`.
3. Faça commits no padrão Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `ci:`).
4. Abra o PR citando a issue e o aceite conferido. Ninguém commita direto na `main`.
5. O merge é do Reviewer, sempre após o sim explícito do Filipe. A exceção são os PRs de conteúdo, que o workflow de merge automático publica quando a validação passa (F2-05).

Regras de conteúdo que valem para arquivo, issue, PR e commit:

- O texto usa só o genérico "médico". Nenhum nome, registro ou formação de profissional de saúde.
- Nenhuma recomendação de dose enquanto não houver revisão. Dose só aparece atribuída ao artigo citado.
- O aviso de curadoria por IA fica em toda edição, na home e neste README.

As regras completas estão em [`AGENTS.md`](AGENTS.md).

## 📚 Documentos

| Documento | Conteúdo |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Regras de trabalho para agentes e contribuidores ([`CLAUDE.md`](CLAUDE.md) importa este arquivo) |
| [`ROADMAP.md`](ROADMAP.md) | Fases 0 a 9, issues, aceite e dependências |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Registro operacional da fase atual |
| [`DECISIONS.md`](DECISIONS.md) | Índice de decisões; ADRs completos em [`docs/decisions/`](docs/decisions/) |
| [`docs/architecture/visao-geral.md`](docs/architecture/visao-geral.md) | Arquitetura: site, publicação e pipeline de conteúdo |
| [`docs/project-genesis.md`](docs/project-genesis.md) | Resumo do plano final que originou o projeto |
| [`docs/agent-workflow.md`](docs/agent-workflow.md) | Prompts de planejar, implementar e fechar uma issue |
| [`docs/status-log.md`](docs/status-log.md) | Histórico cronológico |

## 📄 Licença

[MIT](LICENSE). A licença cobre o código. Os artigos resumidos pertencem aos seus autores e periódicos; cada resumo é escrito em palavras próprias e leva o link para a fonte.
