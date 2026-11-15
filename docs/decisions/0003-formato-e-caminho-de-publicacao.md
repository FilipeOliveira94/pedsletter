# ADR-0003: Formato do arquivo e caminho de publicação

| Campo | Valor |
| --- | --- |
| Estado | `proposto` |
| Aberto em | 2026-11-15 |
| Decidido em | — |
| Responsável | Filipe (dono do produto) |
| ID no índice | ADR-003 |
| Issues relacionadas | F0-02, F0-05, F2-01 a F2-09 |
| Substitui | — |
| Substituído por | — |

## Contexto e problema

Cada edição é gerada por uma rotina agendada no Grok e precisa chegar ao site sem trabalho manual recorrente. Quem sobe o arquivo é o Grok Bot ou o Filipe. O repositório é público, então qualquer pessoa pode abrir um PR. Um arquivo inválido não pode derrubar o site, e uma edição publicada precisa poder sair do ar.

## Decisão

**Formato.** Markdown com frontmatter YAML, um arquivo por edição, com nome `AAAA-MM-DD-resumo.md`, em `src/content/posts/`. O frontmatter traz `titulo`, `data`, `resumo`, `tags`, `status` (`publicado` ou `retirado`), `motivoRetirada` (obrigatório se retirado) e a lista `artigos`, cada um com `titulo`, `fonte`, `url`, `publicadoEm`, `tipo` e `acesso`.

**Caminho.** PR com merge automático, igual para o bot e para o Filipe:

1. A rotina gera o arquivo `.md`.
2. O Grok Bot abre o PR pela API do GitHub, ou o Filipe sobe pelo "Upload files".
3. O CI valida formato, links, duplicatas e o autor do PR.
4. O workflow faz o merge quando a validação passa. Só vale para autor da lista permitida, em branch do próprio repositório, em PR que só adiciona arquivos em `src/content/posts/`.
5. O Cloudflare Pages publica.
6. Se a validação falha, o PR fica aberto, nada é publicado e o GitHub avisa o Filipe.

**Retirada.**

| Forma | Quando usar | Efeito |
| --- | --- | --- |
| `status: retirado` (padrão) | Edição com erro ou conteúdo ruim | Some da home, das tags e do RSS; a URL mostra "edição retirada" e o motivo; os artigos entram na lista de bloqueio do bot |
| Apagar o arquivo | Conteúdo que não deve continuar visível no site | A URL passa a dar 404 |
| Reverter o deploy no Cloudflare Pages | Emergência | Volta à versão anterior em segundos, sem mexer no repositório |

## Alternativas consideradas

| Opção | Prós | Contras | Por que não (se rejeitada) |
| --- | --- | --- | --- |
| Markdown com frontmatter (escolhida) | Legível e corrigível à mão; um arquivo na pasta já é um post | — | — |
| MDX | Componentes no texto | Um `<` ou `{` solto em texto de IA quebra o build | Rejeitada |
| JSON | Fácil de validar | Ruim de ler e de corrigir à mão | Rejeitada |
| `.docx` ou PDF | Familiar | Exige conversão | Rejeitada |
| PR com merge automático (escolhida) | Arquivo inválido fica parado no PR; o site continua no ar; serve para o bot e para o Filipe | Um workflow a mais para escrever | — |
| Commit direto na `main` | Nenhum código | Um arquivo inválido trava todos os deploys seguintes | Rejeitada |
| Página de upload no site | Dispensa o GitHub para quem sobe | Função, autenticação e segredo para manter | Adiada; F7-06, condicional |

## Consequências

- O merge automático precisa de lista de autores e de bloqueio de forks, e não usa segredo em PR de fork (F2-05).
- A validação roda no PR, fora do build. Na `main` só entra arquivo válido.
- Com o repositório público, o texto retirado ou apagado continua no histórico do Git.
- O token do bot dá acesso só a este repositório, só a conteúdo, e tem validade (F2-06).

## Evidência

Nenhuma ainda. O estado fica `proposto` até F0-02 registrar o que a rotina agendada do Grok consegue fazer: se roda no plano atual, se agenda por dia da semana, se entrega arquivo ou só texto e se chama a API do GitHub com um token.

## Rever quando

- F0-02 mostrar que a rotina não entrega arquivo `.md`. O formato de entrada da etapa 1 muda.
- F0-02 mostrar que o Grok não chama a API do GitHub. A etapa 2 fica manual, F2-06 não é feita e o resto não muda.
- O envio manual incomodar depois de duas semanas de operação (F7-06).
- A fase 9 começar: o merge automático passa a exigir aprovação (F9-01).
