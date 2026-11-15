# Gênese do projeto

Resumo do plano final do PedsLetter, aprovado pelo Filipe em 2026-11-15. O plano completo fica fora do repositório. Este documento é histórico e não é fonte de regras: as regras estão no [`AGENTS.md`](../AGENTS.md), o escopo no [`ROADMAP.md`](../ROADMAP.md) e o trabalho atual no [`PROJECT_STATUS.md`](../PROJECT_STATUS.md).

O apêndice do plano, com as regras para associar um médico ao site, não foi trazido. Ele é contexto de F9-02 e entra no repositório nessa issue.

## 1. Objetivo

Um site de resumos de literatura pediátrica gerados por IA, publicado três vezes por semana, para uso pessoal, com calculadoras clínicas em seguida.

| Usuário | Necessidade | Implicação |
| --- | --- | --- |
| Usuário principal (médico) | Ver o que saiu de relevante sem garimpar; calcular rápido | Resumo curto com link para a fonte; calculadoras no celular |
| Filipe | Operar sem trabalho manual recorrente; mostrar o trabalho | Publicação automática, retirada simples e repositório público |

## 2. Decisões incorporadas

| Decisão | Efeito |
| --- | --- |
| O site não cita nenhum profissional | Sem assinatura, sem autoria, sem identificação profissional |
| Texto no genérico "médico" | Vale para site, repositório, issues, ADRs e commits |
| Repositório público | CI gratuito; nada que identifique alguém entra em arquivo, issue, PR ou commit |
| Sem etapa de revisão | O que passar na validação automática é publicado |
| Publicado pode ser retirado depois | Mecanismo de retirada no ADR-003 |
| Sem indexação, e o `noindex` basta | `noindex` em tudo, sem sitemap, sem Search Console, sem login |
| Quem sobe o arquivo: Filipe ou o Grok Bot | Mesmo caminho para os dois: PR com merge automático |
| Fontes de curadoria informadas depois | ADR próprio (F0-03) |
| Rotina no próprio dia | Segunda, quarta e sexta de manhã, com publicação direta |
| Aviso de curadoria por IA | Em toda edição, na home e no README |
| Domínio depois da fase 3 | Fase 4, após validar o uso do MVP |
| Curvas de prematuros validadas no início da issue | F8-03 começa por essa validação |
| Associar um médico, revisar e indexar | Fase 9 |
| Mantidas | Custo zero, sem e-mail, sem cadastro, sem publicidade, sem PALS, público médico |

O repositório público muda duas coisas além do custo:

- **O merge automático precisa de lista de autores.** Qualquer pessoa abre PR, então o workflow só publica PRs do Filipe ou do bot.
- **O conteúdo fica achável pelo GitHub.** O `noindex` cobre o site, não o repositório. O README leva o mesmo aviso de conteúdo gerado por IA.

## 3. Escopo

**MVP: fases 0 a 3, custo zero**

- Site estático em `*.pages.dev`, não indexável.
- Home com as edições recentes, página de edição, tags e RSS.
- Formato de arquivo para o Grok, validado automaticamente.
- Publicação automática por PR e retirada por mudança de status.
- Aviso de conteúdo gerado por IA e não validado.

**Depois do MVP**

- Domínio `pedsletter.com.br` (fase 4), ainda sem indexação.
- Calculadoras sem fármaco (fases 5 a 8).
- Revisão clínica, associação a um médico, indexação e calculadoras com fármaco (fase 9).

## 4. Métricas

- **Cadência:** edição publicada em pelo menos 10 de 12 datas previstas por mês.
- **Automação:** pelo menos 80% das edições publicadas sem intervenção do Filipe.
- **Qualidade:** zero link quebrado publicado; número de edições retiradas por mês.
- **Uso:** o usuário principal lê os resumos ao menos 3 vezes por semana e diz se atendem.
- **Custo:** zero até a compra do domínio.
- **Técnica:** Lighthouse de 95 ou mais.

SEO só vira métrica na fase 9.

## 5. Stack e custo

Astro + Markdown no Cloudflare Pages, com GitHub público e CI, Cloudflare Web Analytics sem cookies e a rotina agendada no Grok. Tudo gratuito; o domínio `pedsletter.com.br`, na fase 4, é o único custo. Alternativas e o desenho completo estão em [`architecture/visao-geral.md`](architecture/visao-geral.md).

## 6. Como um resumo vira post

Um arquivo Markdown com frontmatter YAML por edição chega por PR, passa pela validação no CI, entra na `main` por merge automático e é publicado pelo Cloudflare Pages. Uma edição sai do ar por `status: retirado`, por remoção do arquivo ou por reversão do deploy. Detalhe em [`architecture/visao-geral.md`](architecture/visao-geral.md) e no [ADR-0003](decisions/0003-formato-e-caminho-de-publicacao.md). As regras da rotina do Grok estão no `ROADMAP.md`, fase 2.

## 7. Catálogo de calculadoras

| # | Calculadora | Valor | Esforço | Fonte de referência | Fase |
| --- | --- | --- | --- | --- | --- |
| 1 | Hidratação de manutenção | Alto | P | Holliday e Segar, Pediatrics 1957; nota sobre fluido isotônico, AAP, Feld et al., Pediatrics 2018 | 5 |
| 2 | Superfície corporal e IMC | Médio | P | Mosteller, NEJM 1987 | 6 |
| 3 | Dose por peso genérica | Alto | P | Aritmética; parâmetros informados pelo usuário | 6 |
| 4 | Curva OMS 0–5 anos | Alto | G | WHO Child Growth Standards 2006, tabelas LMS oficiais | 6 |
| 5 | Curva OMS 5–19 anos | Alto | M | WHO Reference 2007 (de Onis et al., Bull WHO 2007) | 7 |
| 6 | Idade corrigida do prematuro | Médio | P | SBP, Seguimento ambulatorial do prematuro de risco | 7 |
| 7 | Perda de peso do recém-nascido (%) | Médio | P | Aritmética; limiares de SBP e AAP | 7 |
| 8 | Estatura-alvo familiar | Médio | P | Tanner et al., Arch Dis Child 1970 | 7 |
| 9 | TFG estimada (Schwartz) | Médio | P | Schwartz et al., JASN 2009 | 7 |
| 10 | Reidratação oral, planos A, B e C | Médio | M | Ministério da Saúde, Manejo do paciente com diarreia | 8 |
| 11 | Curvas de prematuros | Médio | G | Intergrowth-21st (Villar et al., Lancet 2014), a validar | 8 |
| 12 | Percentil de pressão arterial | Médio | G | AAP 2017 (Flynn et al., Pediatrics) | 8 |
| 13 | Bilirrubina e fototerapia | Médio | G | AAP 2022 (Kemper et al., Pediatrics) | 8 |
| 14 | Curva CDC 2000 | Baixo no Brasil | M | CDC Growth Charts 2000, arquivos LMS | 8 |
| 15 | Antitérmicos | Alto | M | SBP como padrão; bula ANVISA, Harriet Lane e BNFc como comparação | 9 |
| 16 | Antibióticos comuns por peso | Alto | M | SBP como padrão; bula ANVISA e Harriet Lane como comparação | 9 |

As referências acima são autores de artigos e entidades citados como fonte das fórmulas; não são pessoas ligadas ao site.

**Regra de fontes para doses** (vale a partir da fase 9): a SBP é o padrão; o conflito entre fontes fica visível, em bloco que mostra cada fonte e o que difere; se a SBP não se posicionar, vale a bula da ANVISA, e a página diz isso.

## 8. Segurança do conteúdo

- **Aviso em toda edição, na home e no README:** "Curadoria e resumos gerados por IA, sem revisão por profissional de saúde. Confira sempre a fonte original."
- **Aviso de público:** "Conteúdo destinado a médicos e demais profissionais de saúde."
- **Artigo inventado ou link errado:** a validação confere se cada URL responde e se cada DOI resolve.
- **Número errado no resumo:** nada automático pega. O aviso, o link para a fonte e a retirada são a mitigação.
- **Alcance limitado:** o site não é indexado nem divulgado.
- **Direito autoral:** resumo em palavras próprias e link para a fonte.

As regras das calculadoras, de privacidade, de acessibilidade e de performance estão em [`architecture/visao-geral.md`](architecture/visao-geral.md).

## 9. Riscos

- **Informação médica errada no ar.** É o risco aceito desta versão. Mitigação: aviso de IA, link para a fonte, site não indexado e retirada simples.
- **O repositório público é achável.** Os resumos aparecem no GitHub e em buscadores, mesmo com o site em `noindex`. Mitigação: aviso de IA no README; o risco é aceito em troca da visibilidade.
- **PR de terceiros.** Mitigação: lista de autores e bloqueio de forks em F2-05.
- **O histórico do Git não esquece.** Edição retirada ou nome escrito por engano continuam no histórico. Mitigação: F1-06 barra antes do merge; reescrever o histórico fica como último recurso.
- **Nome de profissional entra por descuido.** Mitigação: F1-06 e a regra do genérico "médico".
- **O bot publica algo fora do padrão.** Mitigação: validação de formato e links, e merge restrito à pasta de posts.
- **Token do bot vazado.** Mitigação: acesso só a este repositório, com validade; revogação descrita no guia de operação.
- **A rotina do Grok não entrega o que o plano supõe.** Mitigação: F0-02 testa antes; o envio manual cobre.
- **Calculadora sem validação clínica.** Mitigação: casos de fonte publicada, selo visível e nenhuma tabela de fármacos antes da fase 9.
- **Direito autoral.** Mitigação: resumo em palavras próprias e link para a fonte.
- **Regulatório ANVISA.** Antes de F9-05, checar a RDC 657/2022 e a RDC 96/2008.

## 10. Ressalvas do plano

- Três pontos são recomendação de quem escreveu o plano, aceitos na aprovação: calculadoras com fármaco só na fase 9, resumos sem recomendação de dose e publicação por PR com merge automático.
- O que a rotina agendada do Grok consegue fazer não foi verificado. F0-02 testa.
- Os limites dos planos gratuitos foram citados de memória. F0-01 confere.

## 11. Perguntas em aberto

1. **Fontes de curadoria:** a lista entra no ADR-001 quando o Filipe informar; bloqueia F2-02.
2. **Doses nos resumos:** a rotina não escreve recomendação de dose enquanto não houver revisão. A regra vale até o Filipe dizer o contrário.
