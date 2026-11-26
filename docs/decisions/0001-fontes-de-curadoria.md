# ADR-0001: Fontes de curadoria

| Campo | Valor |
| --- | --- |
| Estado | `proposto` |
| Aberto em | 2026-11-15 |
| Decidido em | — |
| Responsável | Filipe (dono do produto) |
| ID no índice | ADR-001 |
| Issues relacionadas | F0-03, F2-02, F2-11, F2-12 |
| Substitui | — |
| Substituído por | — |

## Contexto e problema

A geração pela API do Claude (ADR-004) escolhe os itens de cada edição: artigos, diretrizes, alertas e notícias. Sem uma lista fechada de onde ler, a curadoria fica imprevisível e a chance de fonte fraca ou de artigo inventado aumenta, num site publicado sem revisão (ADR-002). A lista entra no coletor (F2-11), na busca restrita por domínio (F2-12) e no prompt (F2-02).

A lista não decide quem escreve o resumo; ela decide de onde o pipeline pode ler.

## Decisão

Lista inicial proposta em 2026-11-25 e aceita pelo Filipe para começar, com revisão dele depois. O estado passa a `aprovado` quando ele revisar.

**Faixa 1 — periódicos (coleta por feed e PubMed, sem busca aberta)**

| Fonte | Escopo |
| --- | --- |
| Pediatrics | Pediatria |
| JAMA Pediatrics | Pediatria |
| The Lancet Child & Adolescent Health | Pediatria |
| Archives of Disease in Childhood | Pediatria |
| The Journal of Pediatrics | Pediatria |
| Jornal de Pediatria | Pediatria, Brasil |
| Revista Paulista de Pediatria | Pediatria, Brasil |
| NEJM, JAMA, The Lancet, BMJ | Medicina geral; só itens com impacto em pediatria |
| Cochrane Database of Systematic Reviews | Revisões sistemáticas; só itens pediátricos ou com impacto em pediatria |

**Faixa 2 — entidades e notícias (busca restrita aos domínios abaixo)**

| Fonte | Domínio | Escopo |
| --- | --- | --- |
| Sociedade Brasileira de Pediatria | `sbp.com.br` | Documentos científicos, notas e alertas |
| Ministério da Saúde | `gov.br/saude` | Calendário vacinal, notas técnicas, alertas |
| ANVISA | `gov.br/anvisa` | Alertas de segurança de medicamentos e produtos |
| American Academy of Pediatrics | `aap.org`, `publications.aap.org` | Diretrizes e declarações de posição |
| Organização Mundial da Saúde | `who.int` | Diretrizes e alertas |
| OPAS | `paho.org` | Alertas epidemiológicos nas Américas |
| CDC | `cdc.gov` | Alertas, recomendações de vacina, MMWR |
| FDA | `fda.gov` | Alertas de segurança |

**Critério de inclusão**

- Periódico com revisão por pares, ou entidade oficial ou sociedade médica.
- Publica com regularidade e tem página pública, com link estável, para cada item.
- Item de medicina geral entra só com impacto direto em pediatria, e o resumo diz qual.
- Notícia entra só se publicada por uma fonte da faixa 2. Imprensa geral e redes sociais ficam fora.

**Como a lista muda:** só por PR que edita este ADR e o arquivo de configuração das fontes (F2-11), com decisão do Filipe.

## Alternativas consideradas

| Opção | Prós | Contras | Por que não (se rejeitada) |
| --- | --- | --- | --- |
| Lista fechada em duas faixas, com critério de inclusão (escolhida) | Curadoria previsível; a validação confere a fonte; notícia só de fonte oficial | Exige manutenção da lista | — |
| Só periódicos (plano final) | Mais simples | Deixa de fora diretrizes, alertas e notícias, que estão no MVP | Superada pela decisão de 2026-11-25 |
| Busca aberta | Nenhuma manutenção | Fonte fraca e artigo inventado ficam mais prováveis | Rejeitada no plano final e no ADR-004 |

## Consequências

- Desbloqueia F2-02, F2-11 e F2-12.
- O coletor e a busca leem a lista de um arquivo de configuração, não do prompt solto.
- Uma fonte fora da lista faz a validação falhar (F2-13).

## Evidência

Lista inicial proposta no plano de F0-07 e aceita pelo Filipe em 2026-11-25 para começar, com revisão posterior. Os domínios e o acesso aos feeds ainda não foram conferidos; F2-11 confere.

## Rever quando

- O Filipe revisar a lista (o estado passa a `aprovado`).
- Uma fonte deixar de publicar, mudar de domínio ou passar a exigir acesso que o pipeline não tem.
- F3-02 mostrar faixa vazia ou fonte que só gera item fraco.
