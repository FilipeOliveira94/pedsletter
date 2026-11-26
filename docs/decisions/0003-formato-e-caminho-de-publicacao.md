# ADR-0003: Formato do arquivo e caminho de publicação

| Campo | Valor |
| --- | --- |
| Estado | `proposto` |
| Aberto em | 2026-11-15 |
| Decidido em | — |
| Responsável | Filipe (dono do produto) |
| ID no índice | ADR-003 |
| Issues relacionadas | F0-05, F0-07, F2-01 a F2-05, F2-07 a F2-13 |
| Substitui | — |
| Substituído por | — |

## Contexto e problema

Cada edição é gerada por um workflow agendado que chama a API do Claude (ADR-004) e precisa chegar ao site sem trabalho manual recorrente. Quem sobe o arquivo é o bot do projeto (um GitHub App) ou o Filipe. O repositório é público, então qualquer pessoa pode abrir um PR. Um arquivo inválido não pode derrubar o site, e uma edição publicada precisa poder sair do ar.

## Decisão

**Formato.** Markdown com frontmatter YAML, um arquivo por edição, com nome `AAAA-MM-DD-resumo.md`, em `src/content/posts/`. O frontmatter traz `titulo`, `data`, `resumo`, `tags`, `status` (`publicado` ou `retirado`), `motivoRetirada` (obrigatório se retirado) e a lista `artigos`, cada item com `titulo`, `fonte`, `url`, `publicadoEm`, `categoria` (`artigo`, `diretriz`, `alerta` ou `noticia`), `tipo` e `acesso`. A lista mantém o nome `artigos` do plano, embora traga também diretrizes, alertas e notícias (F2-01).

**Caminho.** PR com merge automático, igual para o bot e para o Filipe:

1. O workflow de geração coleta, gera e confere o arquivo `.md` (ADR-004).
2. O bot abre o PR com um token do GitHub App gerado na execução, ou o Filipe sobe pelo "Upload files".
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
| PR aberto por GitHub App (escolhida) | Token por execução, de uma hora; escopo só neste repositório; autor identificável na lista permitida; dispara a validação do PR | Um App para criar e uma chave privada para guardar | — |
| PR aberto pelo `GITHUB_TOKEN` do Actions | Nenhum segredo extra | O PR não dispara os workflows de validação | Rejeitada |
| Token pessoal de escopo fino | Simples de criar | Ligado à conta do Filipe; validade longa; autor do PR é o Filipe | Alternativa se o App não servir |

## Consequências

- O merge automático precisa de lista de autores e de bloqueio de forks, e não usa segredo em PR de fork (F2-05).
- A validação roda no PR, fora do build. Na `main` só entra arquivo válido.
- Com o repositório público, o texto retirado ou apagado continua no histórico do Git.
- O bot é um GitHub App instalado só neste repositório, com permissão só a conteúdo e a pull requests (F2-10). O token é gerado a cada execução e vale uma hora; o segredo guardado é a chave privada do App.
- O PR precisa ser aberto pelo App, e não pelo `GITHUB_TOKEN` do Actions: um PR aberto com o `GITHUB_TOKEN` não dispara os workflows de validação do PR.

## Evidência

Nenhuma ainda. Em 2026-11-25 a rotina do Grok foi substituída pela geração pela API do Claude (ADR-004), e F0-02 foi retirada. O estado fica `proposto` até F2-09 publicar um arquivo real pelo fluxo.

## Rever quando

- F2-10 mostrar que o GitHub App não serve. A alternativa é um token pessoal de escopo fino, com validade, e o autor do PR passa a ser o Filipe.
- O envio manual incomodar depois de duas semanas de operação (F7-06).
- A fase 9 começar: o merge automático passa a exigir aprovação (F9-01).
