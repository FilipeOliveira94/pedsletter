# Histórico de status (arquivo)

Histórico cronológico das atualizações de status. O registro operacional é o [`PROJECT_STATUS.md`](../PROJECT_STATUS.md) (só a fase atual; **reescrito** a cada fase). Entradas de fases fechadas e narrativas longas vêm para cá. Documentos de arquitetura e ADRs citam este histórico, ou trazem os fatos no próprio texto, e não o `PROJECT_STATUS.md`.

Entradas novas no topo.

---

### 2026-11-15 — Estrutura inicial do projeto

O plano final do PedsLetter foi aprovado pelo Filipe em 2026-11-15. A estrutura do repositório foi criada em um commit direto na `main`, `chore: estrutura inicial do projeto`, o último fora de branch de feature.

Criados: `README.md` (reescrito, com o aviso de IA e a nota de `noindex`), `AGENTS.md`, `CLAUDE.md` (importa `AGENTS.md`), `ROADMAP.md` (fases 0 a 9, 59 issues), `DECISIONS.md`, `PROJECT_STATUS.md`, `LICENSE` (MIT), `Makefile`, `.gitignore`, `docs/agent-workflow.md`, `docs/project-genesis.md`, `docs/architecture/visao-geral.md` e `docs/decisions/` com o modelo e três ADRs: ADR-001 `pendente` (aguarda a lista de fontes), ADR-002 `aprovado` (decisão do plano final) e ADR-003 `proposto` (depende de F0-02).

Os ADRs completos ficam em `docs/decisions/`, e não em `docs/adr/` como o plano previa, para seguir o esquema do projeto de referência. O apêndice do plano sobre identificação profissional não entrou no repositório.

Só documentação e esqueleto; nenhum código do site. `make help` lista os seis alvos. `install`, `dev`, `build`, `lint` e `test` são marcadores e saem com erro até F1-01. Nenhuma issue foi fechada: as da fase 0 fecham por PR.
