# Registro de decisões

Índice curto das decisões do PedsLetter. **Motivo, alternativas, consequências e evidência ficam nos ADRs** em [`docs/decisions/`](docs/decisions/).

| | |
| --- | --- |
| Contém | Índice de decisões e estado |
| Detalhe | [`docs/decisions/`](docs/decisions/) (um ADR por decisão) |
| Relacionados | `PROJECT_STATUS.md`, `ROADMAP.md`, `docs/project-genesis.md`, `AGENTS.md` |

**Como usar:** leia a tabela para ver a direção e o que já existe; abra o ADR para o porquê. **Decisão** é o que foi escolhido ou proposto; **Implementado** é o que está verificado no repositório, com evidência no ADR ou no documento de arquitetura e em `docs/status-log.md`.

## Ciclo de vida

| Estado | Significado |
| --- | --- |
| `pendente` | Decisão aberta, à espera de informação; o ADR registra o que falta |
| `proposto` | Opção preferida para planejar; não vincula até ser aprovada |
| `aprovado` | Aceito por decisão do Filipe ou com evidência de issue verificada |
| `substituído` | Trocado por um ADR posterior |
| `rejeitado` | Recusado; mantido para auditoria |

**Regras:** nenhum ADR cita profissional de saúde; quando o estado ou a implementação muda, atualize este índice e o ADR juntos.

## Índice

| ID | Tema | Decisão | Implementado | Estado | ADR |
| --- | --- | --- | --- | --- | --- |
| ADR-001 | Fontes de curadoria | Lista fechada de periódicos e entidades, com critério de inclusão. A lista ainda não foi informada | — | `pendente` | [ADR-0001](docs/decisions/0001-fontes-de-curadoria.md) |
| ADR-002 | Publicação sem revisão e sem indexação | O que passa na validação automática é publicado; `noindex` em tudo, sem sitemap; aviso de IA; retirada simples. Revisão, associação a um médico e indexação ficam para a fase 9 | — | `aprovado` | [ADR-0002](docs/decisions/0002-publicacao-sem-revisao-e-sem-indexacao.md) |
| ADR-003 | Formato e caminho de publicação | Markdown com frontmatter YAML, um arquivo por edição; PR com merge automático para autores permitidos; retirada por `status: retirado`. Depende de F0-02 | — | `proposto` | [ADR-0003](docs/decisions/0003-formato-e-caminho-de-publicacao.md) |

`—` significa ainda não implementado ou ainda não verificado no repositório.

## Como registrar uma decisão nova

1. Copie [`docs/decisions/_template.md`](docs/decisions/_template.md) para `docs/decisions/NNNN-slug-curto.md`.
2. Preencha contexto, decisão, alternativas, consequências, evidência e gatilhos de revisão.
3. Acrescente uma linha ao índice acima.
4. Em `PROJECT_STATUS.md` → **Decisões ativas**, liste só as que condicionam a fase atual ou foram aprovadas nela. Não copie o índice inteiro.
5. Quando a escolha estiver construída e verificada, preencha **Implementado** com o que existe de fato.

## Changelog

| Data | Mudança |
| --- | --- |
| 2026-11-15 | Registro inicial: ADR-001 `pendente`, ADR-002 `aprovado` (decisão do plano final), ADR-003 `proposto` |
