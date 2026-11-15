# Status do projeto

Registro operacional da **fase atual**. O backlog de issues e o texto de aceite ficam em [`ROADMAP.md`](ROADMAP.md). Índice de decisões: [`DECISIONS.md`](DECISIONS.md). Histórico cronológico: [`docs/status-log.md`](docs/status-log.md).

| | |
| --- | --- |
| Repositório | [FilipeOliveira94/pedsletter](https://github.com/FilipeOliveira94/pedsletter) |
| Início | 2026-11-14 |
| Plano final aprovado | 2026-11-15 |
| Última atualização | 2026-11-15 (estrutura inicial do projeto) |
| Fase atual | Fase 0 — Pré-requisitos |
| Status da fase | Não iniciada |

**Valores de status:** não iniciada · em andamento · entregue · verificada · bloqueada · retirada

**Verificada** quer dizer que o aceite foi conferido e a evidência está registrada (em `docs/status-log.md`, no ADR ou no documento de arquitetura). Arquitetura planejada não conta como pronta.

**O que entra aqui:** objetivo atual, progresso das issues da fase, aceite da fase, última validação, decisões que condicionam o trabalho, riscos ativos, bloqueios e próximos passos.

**O que não entra:** inventário acumulado de issues (`ROADMAP.md`), tabela completa de ADRs (`DECISIONS.md`), histórico longo (`docs/status-log.md`).

---

## Objetivo atual

**Fase 0** — contas criadas, rotina do Grok testada e ADRs escritos.

O plano final foi aprovado em 2026-11-15 e a estrutura do repositório foi criada no commit `chore: estrutura inicial do projeto`: documentação, licença, Makefile com marcadores e `.gitignore`. Não há código do site.

## Próximos passos

1. **F0-01** — Contas e repositório. Falta o projeto no Cloudflare Pages ligado ao repositório e a confirmação de que nenhum plano pago foi contratado.
2. **F0-02** — Testar a rotina agendada do Grok. Registrar o que ela consegue fazer. Não depende de nada.
3. **F0-03** — ADR-001. Bloqueada até o Filipe informar a lista de fontes.
4. **F0-04** — ADR-002. Conferir o aceite do ADR já escrito.
5. **F0-05** — ADR-003. Depende de F0-02.

A partir daqui, cada issue entra por branch de feature e PR (AGENTS.md §13).

---

## Progresso da fase 0

| ID | Título | Status | Evidência |
| --- | --- | --- | --- |
| F0-01 | Contas e repositório | Não iniciada | Adiantado no commit inicial: README com a descrição e o aviso de IA |
| F0-02 | Testar a rotina agendada do Grok | Não iniciada | — |
| F0-03 | ADR-001: fontes de curadoria | Bloqueada | Aguarda a lista do Filipe. Esqueleto em [`0001`](docs/decisions/0001-fontes-de-curadoria.md) |
| F0-04 | ADR-002: publicação sem revisão e sem indexação | Não iniciada | Adiantado no commit inicial: [`0002`](docs/decisions/0002-publicacao-sem-revisao-e-sem-indexacao.md) |
| F0-05 | ADR-003: formato e caminho de publicação | Não iniciada | Adiantado no commit inicial: [`0003`](docs/decisions/0003-formato-e-caminho-de-publicacao.md), `proposto` |

O commit inicial adiantou texto, não fechou issue. Cada uma fecha por PR, com o aceite conferido.

Detalhe do aceite: `ROADMAP.md` → Fase 0.

### Aceite da fase 0

- [ ] Contas criadas: repositório público e projeto no Cloudflare Pages ligado a ele.
- [ ] Rotina agendada do Grok testada, com o resultado registrado.
- [ ] ADR-001, ADR-002 e ADR-003 escritos.

---

## Última validação

| | |
| --- | --- |
| Data | 2026-11-15 |
| Ambiente | Local, WSL2 |
| Verificações | `make help` |
| Resultado | Lista os seis alvos. `install`, `dev`, `build`, `lint` e `test` são marcadores e saem com erro até F1-01 |

---

## Decisões ativas

| ID | Tema | Estado | Efeito na fase |
| --- | --- | --- | --- |
| ADR-001 | Fontes de curadoria | `pendente` | Não bloqueia a fase 1; bloqueia F2-02 |
| ADR-002 | Publicação sem revisão e sem indexação | `aprovado` | Define as regras de conteúdo do AGENTS.md §4 |
| ADR-003 | Formato e caminho de publicação | `proposto` | Aprovação depende de F0-02 |

## Riscos ativos

- A rotina do Grok pode não entregar o que o plano supõe. F0-02 testa antes; o envio manual cobre.
- Os limites dos planos gratuitos citados no plano são de memória. Conferir em F0-01.
- Um nome de profissional pode entrar por descuido em arquivo, issue ou commit antes de F1-06 existir. Até lá, a regra do AGENTS.md §4 é a única barreira.

## Bloqueios

- **F0-03:** lista de fontes de curadoria, a informar pelo Filipe.

## Perguntas em aberto

1. **Fontes de curadoria:** a lista entra no ADR-001 quando o Filipe informar.
2. **Doses nos resumos:** a rotina não escreve recomendação de dose enquanto não houver revisão. A regra vale até o Filipe dizer o contrário.
