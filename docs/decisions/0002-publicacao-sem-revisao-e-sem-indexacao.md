# ADR-0002: Publicação sem revisão e sem indexação

| Campo | Valor |
| --- | --- |
| Estado | `aprovado` |
| Aberto em | 2026-11-15 |
| Decidido em | 2026-11-15 (plano final) |
| Responsável | Filipe (dono do produto) |
| ID no índice | ADR-002 |
| Issues relacionadas | F0-04, F1-03, F1-05, F1-06, F2-07, F9-01 a F9-04 |
| Substitui | — |
| Substituído por | — |

## Contexto e problema

O site publica resumos de literatura pediátrica gerados por IA, três vezes por semana, para uso pessoal. Não há etapa de revisão clínica nesta versão e o site não cita nenhum profissional. Informação médica errada pode ir ao ar, e é preciso limitar o alcance e deixar claro o que o conteúdo é.

## Decisão

O que passa na validação automática é publicado, sem revisão humana. O site não é indexável: `noindex` em toda página, na meta tag e no cabeçalho `X-Robots-Tag`, sem sitemap e sem cadastro no Search Console. O `noindex` basta; não há controle de acesso nem login. O site não tem assinatura, autoria nem identificação profissional, e o texto usa só o genérico "médico".

## Mitigações

- **Aviso de IA** em toda edição, na home e no README: "Curadoria e resumos gerados por IA, sem revisão por profissional de saúde. Confira sempre a fonte original."
- **Aviso de público** em toda página: "Conteúdo destinado a médicos e demais profissionais de saúde."
- **Link para a fonte** em todo artigo; a validação confere se a URL responde e se o DOI resolve.
- **Sem recomendação de dose.** Dose só aparece atribuída ao artigo.
- **Retirada simples** por `status: retirado`, por remoção do arquivo ou por reversão do deploy ([ADR-0003](0003-formato-e-caminho-de-publicacao.md)).
- **Alcance limitado:** o site não é indexado nem divulgado.
- **Verificação de ausência de autoria** no CI (F1-06).
- **Sem `Disallow` no `robots.txt`:** um buscador bloqueado pelo `robots.txt` não chega a ler o `noindex`.

## Alternativas consideradas

| Opção | Prós | Contras | Por que não (se rejeitada) |
| --- | --- | --- | --- |
| Publicar sem revisão, sem indexação (escolhida) | Nenhum trabalho manual recorrente; custo zero | Erro pode ir ao ar | — |
| Revisão clínica antes de publicar | Reduz o erro publicado | Exige um médico associado e trabalho recorrente | Adiada para a fase 9 |
| Controle de acesso ou login | Alcance ainda menor | Função, autenticação e segredo para manter | O `noindex` basta |
| Indexar com aviso | Visibilidade | Amplia o alcance de conteúdo não revisado | Adiada para a fase 9 |

## Consequências

- Informação médica errada no ar é o risco aceito desta versão. Nada automático pega um número errado no resumo.
- O repositório é público: os arquivos dos resumos ficam acháveis pelo GitHub e por buscadores, mesmo com o site em `noindex`. O README leva o mesmo aviso.
- Texto retirado ou apagado continua no histórico do Git.
- SEO não é métrica até a fase 9. O Lighthouse CI ignora a categoria SEO (F3-04).

## Evidência

Decisão registrada no plano final aprovado em 2026-11-15 (resumo em [`docs/project-genesis.md`](../project-genesis.md)). Nenhuma implementação ainda; F0-04 confere o aceite deste ADR, e F1-03, F1-05 e F1-06 implementam as mitigações.

## Rever quando

- O Filipe decidir começar a fase 9. A ordem é: revisão clínica (F9-01), associação a um médico (F9-02), revisão retroativa ou arquivo (F9-03) e só então indexação (F9-04).
- O número de edições retiradas por mês mostrar que a validação automática não segura a qualidade.
- A validação do uso (F3-03) terminar em "parar".
