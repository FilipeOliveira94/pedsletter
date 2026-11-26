# Status do projeto

Registro operacional da **fase atual**. O backlog de issues e o texto de aceite ficam em [`ROADMAP.md`](ROADMAP.md). Índice de decisões: [`DECISIONS.md`](DECISIONS.md). Histórico cronológico: [`docs/status-log.md`](docs/status-log.md).

| Projeto | Atual |
| --- | --- |
| Repositório | [FilipeOliveira94/pedsletter](https://github.com/FilipeOliveira94/pedsletter) |
| Início | 2026-11-14 |
| Plano final aprovado | 2026-11-15 |
| Última atualização | 2026-11-25 (F0-07: pipeline pela API do Claude) |
| Fase atual | Fase 0 — Pré-requisitos |
| Status da fase | Em andamento |

**Valores de status:** não iniciada · em andamento · entregue · verificada · bloqueada · retirada

**Verificada** quer dizer que o aceite foi conferido e a evidência está registrada (em `docs/status-log.md`, no ADR ou no documento de arquitetura). Arquitetura planejada não conta como pronta.

**O que entra aqui:** objetivo atual, progresso das issues da fase, aceite da fase, última validação, decisões que condicionam o trabalho, riscos ativos, bloqueios e próximos passos.

**O que não entra:** inventário acumulado de issues (`ROADMAP.md`), tabela completa de ADRs (`DECISIONS.md`), histórico longo (`docs/status-log.md`).

---

## Objetivo atual

**Fase 0** — contas criadas, ensaio de custo e qualidade da API do Claude registrado e ADR-001 a ADR-004 escritos.

Em 2026-11-25 a geração das edições passou da rotina do Grok para um script que chama a API do Claude a partir do GitHub Actions ([ADR-004](docs/decisions/0004-generation-by-claude-api.md)): Sonnet 5.5, até US$ 30 por mês, com notícias, diretrizes e alertas no MVP. O roadmap foi reescrito em F0-07. Não há código do site.

## Próximos passos

1. **F0-06** — Traduzir a documentação para inglês. Próxima issue, por decisão do Filipe.
2. **F0-03** — Revisão do Filipe sobre a lista inicial do ADR-001; o ADR passa a `aprovado`.
3. **F0-01** — Contas e repositório. Falta o projeto no Cloudflare Pages ligado ao repositório.
4. **F0-08** — Ensaio de custo e qualidade da API. Gera custo: o Filipe autoriza antes de rodar.
5. **F0-04** e **F0-05** — Conferir o aceite do ADR-002 e do ADR-003 reescrito.

---

## Progresso da fase 0

| ID | Título | Status | Evidência |
| --- | --- | --- | --- |
| F0-01 | Contas e repositório | Não iniciada | Adiantado no commit inicial: README com a descrição e o aviso de IA |
| F0-02 | Testar a rotina agendada do Grok | Retirada | Substituída por F0-08 ([ADR-004](docs/decisions/0004-generation-by-claude-api.md)) |
| F0-03 | ADR-001: fontes de curadoria | Em andamento | Lista inicial em duas faixas em [`0001`](docs/decisions/0001-fontes-de-curadoria.md), `proposto`; aguarda a revisão do Filipe |
| F0-04 | ADR-002: publicação sem revisão e sem indexação | Não iniciada | Adiantado no commit inicial: [`0002`](docs/decisions/0002-publicacao-sem-revisao-e-sem-indexacao.md) |
| F0-05 | ADR-003: formato e caminho de publicação | Não iniciada | [`0003`](docs/decisions/0003-formato-e-caminho-de-publicacao.md) reescrito em F0-07 para o GitHub App, `proposto` |
| F0-06 | Traduzir a documentação para inglês | Não iniciada | — |
| F0-07 | Reescrever o roadmap para o pipeline pela API do Claude | Entregue | PR de F0-07; [ADR-004](docs/decisions/0004-generation-by-claude-api.md) `aprovado` |
| F0-08 | Ensaio de custo e qualidade da API | Não iniciada | — |

Detalhe do aceite: `ROADMAP.md` → Fase 0.

### Aceite da fase 0

- [ ] Contas criadas: repositório público, projeto no Cloudflare Pages ligado a ele e conta na API do Claude com limite mensal de gasto.
- [ ] Ensaio da API registrado, com custo e qualidade medidos (F0-08).
- [ ] ADR-001 a ADR-004 escritos.

---

## Última validação

| Validação | Detalhe |
| --- | --- |
| Data | 2026-11-25 |
| Ambiente | Local, WSL2 |
| Verificações | `make docs-lint` |
| Resultado | Ver o PR de F0-07 |

---

## Decisões ativas

| ID | Tema | Estado | Efeito na fase |
| --- | --- | --- | --- |
| ADR-001 | Fontes de curadoria | `proposto` | Lista inicial aceita para começar; desbloqueia F0-08 e a fase 2 |
| ADR-002 | Publicação sem revisão e sem indexação | `aprovado` | Define as regras de conteúdo do AGENTS.md §4 |
| ADR-003 | Formato e caminho de publicação | `proposto` | PR pelo GitHub App; aprovação depende de F2-09 |
| ADR-004 | Geração pela API do Claude | `aprovado` | Sonnet 5.5, GitHub Actions, até US$ 30 por mês; define F0-08 e a fase 2 |

## Riscos ativos

- O custo por execução é estimativa (cerca de US$ 10 por mês com Sonnet), não medida. F0-08 mede antes de qualquer código do pipeline.
- Os domínios e feeds do ADR-001 não foram conferidos. F2-11 confere.
- Texto buscado pode trazer instrução injetada num site publicado sem revisão. Mitigação: saída estruturada, nenhuma ferramenta de escrita para o modelo e validação de fundamentação (F2-12, F2-13).
- Os limites dos planos gratuitos citados no plano são de memória. Conferir em F0-01.
- Um nome de profissional pode entrar por descuido em arquivo, issue ou commit antes de F1-06 existir. Até lá, a regra do AGENTS.md §4 é a única barreira.

## Bloqueios

Nenhum. F0-03 deixou de bloquear com a lista inicial do ADR-001.

## Perguntas em aberto

1. **Fontes de curadoria:** o Filipe revisa a lista inicial do ADR-001.
2. **Doses nos resumos:** a geração não escreve recomendação de dose enquanto não houver revisão. A regra vale até o Filipe dizer o contrário.
3. **README:** ainda descreve a rotina do Grok. Pela regra do AGENTS.md §12 ele só muda no fechamento de fase; F0-06 o traduz e pode corrigir.
