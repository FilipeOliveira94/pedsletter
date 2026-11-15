# ADR-0001: Fontes de curadoria

| Campo | Valor |
| --- | --- |
| Estado | `pendente` |
| Aberto em | 2026-11-15 |
| Decidido em | — |
| Responsável | Filipe (dono do produto) |
| ID no índice | ADR-001 |
| Issues relacionadas | F0-03, F2-02 |
| Substitui | — |
| Substituído por | — |

## Contexto e problema

A rotina agendada escolhe de 3 a 5 artigos por edição. Sem uma lista fechada de onde buscar, a curadoria fica imprevisível e a chance de fonte fraca ou de artigo inventado aumenta. A lista também entra no texto da rotina (F2-02).

## Decisão

Ainda não tomada. A lista de periódicos e entidades será informada pelo Filipe.

Quando for, este ADR registra:

- a lista fechada de periódicos e entidades;
- o critério de inclusão;
- como a lista muda depois (quem decide e onde fica registrado).

A rotina busca só nessa lista.

## Alternativas consideradas

| Opção | Prós | Contras | Por que não (se rejeitada) |
| --- | --- | --- | --- |
| Lista fechada com critério de inclusão (direção do plano) | Curadoria previsível; a validação pode conferir a fonte | Exige manutenção da lista | — |
| Busca aberta | Nenhuma manutenção | Fonte fraca e artigo inventado ficam mais prováveis | Rejeitada no plano final |

## Consequências

- Não bloqueia a fase 1.
- Bloqueia F2-02 (modelo do arquivo e texto da rotina).

## Evidência

Nenhuma ainda.

## Rever quando

- O Filipe informar a lista (o estado passa a `proposto` ou `aprovado`).
- Uma fonte da lista deixar de publicar ou passar a exigir acesso que a rotina não tem.
