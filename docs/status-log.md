# Histórico de status (arquivo)

Histórico cronológico das atualizações de status. O registro operacional é o [`PROJECT_STATUS.md`](../PROJECT_STATUS.md) (só a fase atual; **reescrito** a cada fase). Entradas de fases fechadas e narrativas longas vêm para cá. Documentos de arquitetura e ADRs citam este histórico, ou trazem os fatos no próprio texto, e não o `PROJECT_STATUS.md`.

Entradas novas no topo.

---

### 2026-11-25 — F0-07: pipeline pela API do Claude

O Filipe decidiu passar a geração das edições da rotina do Grok para a API do Claude, com Sonnet 5.5 para começar, até US$ 30 por mês, e com notícias, diretrizes e alertas no MVP. A decisão está no [ADR-004](decisions/0004-generation-by-claude-api.md), `aprovado`.

O roadmap foi reescrito: F0-02 e F2-06, que dependiam do Grok, foram retiradas; entraram F0-08 (ensaio de custo e qualidade), F2-10 a F2-15 (GitHub App, coleta, gerador, fundamentação, orçamento, alerta de falha), F3-05 (conjunto de avaliação) e F7-07 (material de consulta). F3-04 foi para a fase 1, e as curvas de crescimento vêm antes das demais calculadoras da fase 6. O ADR-001 recebeu a lista inicial em duas faixas e passou a `proposto`; o ADR-003 troca o Grok Bot pelo GitHub App, porque um PR aberto com o `GITHUB_TOKEN` do Actions não dispara a validação do PR. O `AGENTS.md` troca a regra de custo zero pela de até US$ 30 por mês na API e amplia o Hi risk.

A estimativa de custo (cerca de US$ 10 por mês com Sonnet em 13 execuções) não foi medida; F0-08 mede. Só documentação; `make docs-lint` passou.

---

### 2026-11-17 — Tabelas Markdown com cabeçalho nomeado

6 tabelas de chave e valor tinham a linha de cabeçalho vazia (`| | |`), que o GFM mostra como uma linha em branco no topo. O padrão veio dos documentos de planejamento de outro projeto, usados como modelo, e passou adiante por cópia. Cada tabela tem agora um cabeçalho tirado do contexto (`Projeto | Atual`, `Validação | Detalhe`, `Roadmap | Atual`, `Registro | Referência`, `ADRs | Local`). `scripts/check_markdown_tables.py` falha se algum arquivo Markdown versionado tiver um cabeçalho vazio, fora de blocos de código; roda com `make docs-lint`. A regra está no AGENTS.md §9.

---

### 2026-11-15 — Estrutura inicial do projeto

O plano final do PedsLetter foi aprovado pelo Filipe em 2026-11-15. A estrutura do repositório foi criada em um commit direto na `main`, `chore: estrutura inicial do projeto`, o último fora de branch de feature.

Criados: `README.md` (reescrito, com o aviso de IA e a nota de `noindex`), `AGENTS.md`, `CLAUDE.md` (importa `AGENTS.md`), `ROADMAP.md` (fases 0 a 9, 59 issues), `DECISIONS.md`, `PROJECT_STATUS.md`, `LICENSE` (MIT), `Makefile`, `.gitignore`, `docs/agent-workflow.md`, `docs/project-genesis.md`, `docs/architecture/visao-geral.md` e `docs/decisions/` com o modelo e três ADRs: ADR-001 `pendente` (aguarda a lista de fontes), ADR-002 `aprovado` (decisão do plano final) e ADR-003 `proposto` (depende de F0-02).

Os ADRs completos ficam em `docs/decisions/`, e não em `docs/adr/` como o plano previa, para seguir o esquema do projeto de referência. O apêndice do plano sobre identificação profissional não entrou no repositório.

Só documentação e esqueleto; nenhum código do site. `make help` lista os seis alvos. `install`, `dev`, `build`, `lint` e `test` são marcadores e saem com erro até F1-01. Nenhuma issue foi fechada: as da fase 0 fecham por PR.
