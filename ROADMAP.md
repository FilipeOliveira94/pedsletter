# Roadmap

Plano do PedsLetter por issue. Este arquivo é a fonte de **escopo, dependências, status das issues e critérios de aceite**. O `PROJECT_STATUS.md` é o registro operacional da **fase atual**. O histórico fica em `docs/status-log.md`.

| Roadmap | Atual |
| --- | --- |
| Origem | Plano final aprovado em 2026-11-15; resumo em [`docs/project-genesis.md`](docs/project-genesis.md) |
| Última atualização | 2026-11-24 (F0-06) |
| Relacionados | `PROJECT_STATUS.md`, `DECISIONS.md`, `AGENTS.md` |

**Valores de status:** `não iniciada` · `em andamento` · `entregue` · `verificada` · `bloqueada` · `retirada`

- Marque uma issue como **entregue** só quando a mudança existir no repositório.
- Marque como **verificada** só quando o aceite tiver sido conferido e o resultado estiver em `docs/status-log.md`, no ADR ou no documento de arquitetura; o `PROJECT_STATUS.md` resume.
- Não comece uma fase antes de as dependências dela estarem satisfeitas, ou de uma dispensa explícita estar registrada no `DECISIONS.md`.
- Não crie diretórios vazios para fases que ainda não começaram.
- Uma issue por PR, em branch de feature (AGENTS.md §13).
- Nenhuma issue, PR ou commit cita profissional de saúde. O texto usa só o genérico "médico".

**Expected/Seen Risk e Size:** cada célula é `esperado/visto`. Risk é `Lo`, `Med` ou `Hi`; Size é `Sm`, `Md` ou `Lg` (escala em `~/.agents/claude/workflow.md`, repositório `FilipeOliveira94/agent-config`; risco alto aqui está em `AGENTS.md` §3). Uma issue aberta tem só a metade esperada (`Med/-`, `Md/-`); a metade vista é preenchida quando ela fecha. Substitui a antiga coluna Est. (P/M/G).

**Formato do aceite:** os critérios são os do plano final, na forma "dado … então …" quando ela se aplica. Uma issue tem um ou mais critérios; todos são obrigatórios.

---

## Visão das fases

| Fase | Entrega | Critério de saída | Depende de | Status |
| --- | --- | --- | --- | --- |
| 0 | Pré-requisitos | Contas criadas, rotina do Grok testada, ADRs escritos | — | Não iniciada |
| 1 | Base do site | Site em preview, não indexável, com aviso de IA | F0-01 | Não iniciada |
| 2 | Pipeline de conteúdo | Um arquivo real do Grok é publicado sem intervenção | Fase 1; F0-02 e F0-03 para F2-02 | Não iniciada |
| 3 | **MVP em uso** | Duas semanas de edições e o uso validado | Fase 2 | Não iniciada |
| 4 | Domínio | Site em `pedsletter.com.br`, ainda não indexável | F3-03 com decisão de seguir | Não iniciada |
| 5 | Motor e primeira calculadora | Holliday-Segar no ar, com casos de referência | F1-01 | Não iniciada |
| 6 | Calculadoras iniciais | Quatro calculadoras no ar | Fase 5 | Não iniciada |
| 7 | Melhorias 1 | Calculadoras simples adicionais | Fase 6 | Não iniciada |
| 8 | Melhorias 2 | Calculadoras de tabela e PWA | Fases 6 e 7 | Não iniciada |
| 9 | Publicação pública (futura) | Revisão, associação a um médico e indexação | Decisão explícita do Filipe | Não iniciada |

**MVP:** fases 0 a 3, com custo zero. O domínio (fase 4) é o único custo do projeto.

### Métricas do projeto

| Métrica | Alvo |
| --- | --- |
| Cadência | Edição publicada em pelo menos 10 de 12 datas previstas por mês |
| Automação | Pelo menos 80% das edições publicadas sem intervenção do Filipe |
| Qualidade | Zero link quebrado publicado; número de edições retiradas por mês |
| Uso | O usuário principal lê os resumos ao menos 3 vezes por semana e diz se atendem |
| Custo | Zero até a compra do domínio |
| Técnica | Lighthouse de 95 ou mais |

SEO só vira métrica na fase 9.

---

## Fase 0 — Pré-requisitos

**Objetivo:** contas, teste da rotina agendada e decisões registradas antes de escrever código.

**Fora do escopo:** qualquer código do site.

**Aceite da fase (todos obrigatórios):**

- [ ] Contas criadas: repositório público e projeto no Cloudflare Pages ligado a ele.
- [ ] Rotina agendada do Grok testada, com o resultado registrado.
- [ ] ADR-001, ADR-002 e ADR-003 escritos.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F0-01 | Contas e repositório | Lo/- | Sm/- | — | Não iniciada | Repositório público no GitHub e projeto no Cloudflare Pages ligado a ele.<br>README com a descrição do projeto e o aviso de conteúdo gerado por IA.<br>Nenhum plano pago contratado. |
| F0-02 | Testar a rotina agendada do Grok | Med/- | Sm/- | — | Não iniciada | Registrado se a rotina roda no plano atual, se agenda para dias da semana e se entrega arquivo ou só texto.<br>Registrado se o Grok consegue chamar a API do GitHub com um token.<br>Se não conseguir, fica decidido que o Filipe faz o envio. |
| F0-03 | ADR-001: fontes de curadoria | Lo/- | Sm/- | Lista informada pelo Filipe | Bloqueada | Lista fechada de periódicos e entidades, com o critério de inclusão.<br>Não bloqueia a fase 1; bloqueia F2-02. |
| F0-04 | ADR-002: publicação sem revisão e sem indexação | Lo/- | Sm/- | — | Não iniciada | Registra a decisão, o motivo, as mitigações e as condições para rever (fase 9).<br>Não cita nenhum profissional. |
| F0-05 | ADR-003: formato e caminho de publicação | Lo/- | Sm/- | F0-02 | Não iniciada | Registra o formato `.md`, o PR com merge automático e o mecanismo de retirada. |
| F0-06 | Traduzir a documentação do repositório para inglês | Lo/- | Md/- | — | Não iniciada | ROADMAP, PROJECT_STATUS, DECISIONS, ADRs, `docs/` e README em inglês (decisão do Filipe, 2026-11-24; o `AGENTS.md` e os prompts já estão em inglês).<br>O conteúdo do site e os avisos obrigatórios do §4 ficam em português, inclusive no README.<br>IDs de issue e de decisão não mudam. |

O commit inicial adiantou o texto do README e dos três ADRs. As issues continuam abertas e fecham por PR, com o aceite conferido.

---

## Fase 1 — Base do site

**Objetivo:** site estático em `*.pages.dev`, não indexável, com aviso de IA.

**Fora do escopo:** validação de conteúdo e merge automático (fase 2), calculadoras (fase 5 em diante), domínio próprio (fase 4).

**Aceite da fase (todos obrigatórios):**

- [ ] Site em preview no Cloudflare Pages.
- [ ] Toda página com `noindex`, sem sitemap.
- [ ] Aviso de IA em toda edição e na home; aviso de público em toda página.
- [ ] Nenhuma autoria no HTML gerado nem nos arquivos do repositório.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F1-01 | Projeto Astro, TypeScript estrito e CI | Med/- | Sm/- | F0-01 | Não iniciada | Dado um commit com erro de tipo, quando o CI roda, então o build falha. |
| F1-02 | Deploy com preview | Hi/- | Sm/- | F1-01 | Não iniciada | Cada branch do próprio repositório gera uma URL de preview. |
| F1-03 | Site não indexável | Hi/- | Sm/- | F1-02 | Não iniciada | Dado `indexavel` desligado, então toda página responde com `noindex` na meta tag e no cabeçalho `X-Robots-Tag`.<br>Nenhum sitemap é gerado.<br>O `robots.txt` não tem `Disallow`.<br>Um teste percorre todas as páginas do build e falha se alguma não tiver `noindex`. |
| F1-04 | Layout, home e página de edição | Lo/- | Md/- | F1-01 | Não iniciada | A home lista as edições mais recentes.<br>A edição mostra o corpo e a lista de artigos com link, fonte, tipo e acesso. |
| F1-05 | Aviso de conteúdo gerado por IA | Hi/- | Sm/- | F1-04 | Não iniciada | Dado qualquer edição, então o aviso de IA aparece antes do texto.<br>O aviso aparece também na home.<br>Toda página mostra o aviso de público profissional. |
| F1-06 | Verificação de ausência de autoria | Hi/- | Sm/- | F1-04 | Não iniciada | Script no CI sobre o HTML gerado e sobre os arquivos do repositório.<br>Dado um termo da lista de bloqueio ("CRM", "RQE", "Dr.", "Dra.", "revisado por", "médico responsável", "médica responsável"), então o CI falha e aponta arquivo e linha.<br>Nomes próprios a bloquear entram por segredo do CI, nunca em arquivo.<br>A verificação roda também sobre o texto dos PRs de conteúdo. |
| F1-07 | Páginas "Sobre", "Aviso" e "Privacidade" | Hi/- | Sm/- | F1-04 | Não iniciada | "Sobre" descreve um projeto de curadoria automatizada e linka o repositório, sem citar profissional de saúde.<br>"Aviso" declara conteúdo informativo, sem validação clínica, sem consulta, diagnóstico ou prescrição.<br>"Privacidade" declara que o site não coleta dado pessoal. |
| F1-08 | RSS | Lo/- | Sm/- | F1-04 | Não iniciada | RSS válido, só com edições em `status: publicado`. |
| F1-09 | Analytics sem cookies | Med/- | Sm/- | F1-02 | Não iniciada | Nenhum cookie é criado ao navegar. |

**Nota para F1-06:** esta linha do roadmap cita os termos da lista de bloqueio porque são o aceite da issue. A implementação precisa tratar os arquivos que definem a própria lista.

---

## Fase 2 — Pipeline de conteúdo

**Objetivo:** um arquivo `.md` vira edição publicada por PR, com validação e merge automático, e pode ser retirado.

**Fora do escopo:** rotina agendada em produção (fase 3), revisão clínica (fase 9).

**Aceite da fase (todos obrigatórios):**

- [ ] Um arquivo real do Grok é publicado sem intervenção.
- [ ] Um arquivo inválido fica parado no PR, com o site inalterado.
- [ ] Um PR de conta fora da lista não é publicado.
- [ ] Uma edição pode ser retirada seguindo só o guia de operação.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F2-01 | Schema do post | Med/- | Sm/- | F1-04 | Não iniciada | Dado um arquivo sem `artigos` ou com artigo sem `url`, então a validação falha com mensagem que aponta o campo.<br>Dado `status: retirado` sem `motivoRetirada`, então a validação falha. |
| F2-02 | Modelo do arquivo e texto da rotina | Hi/- | Sm/- | F0-02, F0-03, F2-01 | Não iniciada | Três execuções seguidas da rotina passam em F2-01 sem correção manual.<br>O texto da rotina contém as regras da rotina (abaixo) e a lista do ADR-001. |
| F2-03 | Validação de links | Med/- | Sm/- | F2-01 | Não iniciada | Dado um artigo com URL que não responde ou DOI que não resolve, então a validação falha e nomeia o artigo. |
| F2-04 | Bloqueio de artigo repetido ou retirado | Med/- | Sm/- | F2-01 | Não iniciada | Dada uma URL já usada em edição publicada, então a validação avisa, sem falhar.<br>Dada uma URL de edição retirada, então a validação falha. |
| F2-05 | Merge automático | Hi/- | Md/- | F2-03, F2-04 | Não iniciada | Dado um PR de autor permitido, vindo de branch do próprio repositório, que só adiciona arquivos em `src/content/posts/` e passa na validação, então o workflow faz o merge sem ação humana.<br>Dado um PR de fork ou de autor fora da lista, então o workflow não faz o merge e não usa nenhum segredo.<br>Dado um PR que toca qualquer outro caminho, então o workflow não faz o merge.<br>Dada uma validação que falha, então o PR fica aberto e o Filipe é notificado. |
| F2-06 | Envio pelo bot (condicional) | Hi/- | Sm/- | F0-02, F2-05 | Não iniciada | Só se F0-02 mostrar que o Grok chama a API do GitHub.<br>Token com acesso só a este repositório e só a conteúdo, com validade definida.<br>O bot abre o PR com o arquivo no caminho certo. |
| F2-07 | Retirada de edição | Hi/- | Sm/- | F2-01 | Não iniciada | Dado `status: retirado`, então a edição some da home, das tags e do RSS.<br>A URL da edição mostra "edição retirada", a data e o motivo, sem o conteúdo.<br>Dado o arquivo apagado, então a URL responde 404. |
| F2-08 | Guia de operação | Lo/- | Sm/- | F2-05, F2-07 | Não iniciada | Descreve envio manual, retirada, correção, reversão de deploy e revogação do token.<br>O Filipe retira uma edição de teste seguindo só o guia. |
| F2-09 | Ensaio completo | Hi/- | Sm/- | F2-02, F2-05 | Não iniciada | Um arquivo real do Grok é publicado pelo fluxo, sem edição manual.<br>Um arquivo propositalmente inválido fica parado no PR, com o site inalterado.<br>Um PR aberto por uma conta fora da lista não é publicado. |

### Regras para a rotina do Grok (entram no texto de F2-02)

- Buscar só na lista de fontes do ADR-001.
- De 3 a 5 artigos por edição, publicados nos últimos dias.
- Todo artigo com link direto e, quando houver, DOI.
- Resumo em palavras próprias, sem copiar o abstract.
- Declarar quando só o resumo do artigo estava acessível.
- Nenhum número que não esteja no artigo; na dúvida, omitir.
- Nenhuma recomendação de dose; dose só aparece atribuída ao artigo.
- Linguagem técnica, em português.
- Nenhum nome de profissional e nenhuma menção a autoria do site.

---

## Fase 3 — MVP em uso

**Objetivo:** a rotina roda em produção por duas semanas e o uso é validado.

**Aceite da fase (todos obrigatórios):**

- [ ] Duas semanas de edições publicadas pela rotina.
- [ ] O usuário principal respondeu se os resumos atendem.
- [ ] Decisão registrada: seguir, ajustar ou parar.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F3-01 | Rotina agendada em produção | Hi/- | Sm/- | F2-09 | Não iniciada | A rotina roda segunda, quarta e sexta de manhã. |
| F3-02 | Duas semanas de operação | Med/- | Sm/- | F3-01 | Não iniciada | Ao menos 5 de 6 edições publicadas.<br>Erros encontrados nas edições anotados, com ajuste no texto da rotina. |
| F3-03 | Validação do uso | Lo/- | Sm/- | F3-02 | Não iniciada | O usuário principal responde se os resumos atendem e o que mudar.<br>Decisão registrada: seguir, ajustar ou parar. |
| F3-04 | Lighthouse CI | Med/- | Sm/- | F1-04 | Não iniciada | Merge bloqueado com nota abaixo de 95, exceto na categoria SEO, que o `noindex` reduz. |

---

## Fase 4 — Domínio (após validar o uso)

**Objetivo:** site em `pedsletter.com.br`, ainda não indexável.

**Aceite da fase (todos obrigatórios):**

- [ ] Domínio registrado e servindo o site por HTTPS.
- [ ] O site continua com `noindex`.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F4-01 | Comprar `pedsletter.com.br` | Med/- | Sm/- | F3-03 com decisão de seguir | Não iniciada | Domínio registrado, com a zona DNS sob controle do Filipe. |
| F4-02 | Configurar o domínio | Hi/- | Sm/- | F4-01 | Não iniciada | Registros DNS criados, com o apex e o CNAME de `www` apontando para o projeto no Cloudflare Pages.<br>`https://pedsletter.com.br` serve o site com certificado válido e HSTS.<br>Dado um acesso por `http://`, por `www.` ou por `*.pages.dev`, então a resposta é 301 para `https://pedsletter.com.br`.<br>Canonical e RSS usam o domínio final.<br>O site continua com `noindex` depois da troca. |

---

## Fase 5 — Motor de calculadoras e primeira calculadora

**Objetivo:** contrato, componente, executor de casos e a calculadora de hidratação de manutenção.

**Fora do escopo:** qualquer calculadora com fármaco (fase 9).

**Aceite da fase (todos obrigatórios):**

- [ ] Hidratação de manutenção (Holliday-Segar) no ar, com casos de referência.
- [ ] Selo "Não validada clinicamente" visível.
- [ ] Nenhum valor digitado sai do navegador.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F5-01 | Contrato de definição de calculadora | Hi/- | Md/- | F1-01 | Não iniciada | Uma calculadora nova exige só definição, casos e página.<br>Os tipos impedem campo numérico sem unidade. |
| F5-02 | Componente `<Calculator>` | Hi/- | Md/- | F5-01 | Não iniciada | Dado "12,5" e "12.5" no mesmo campo, então o resultado é idêntico.<br>Dado um valor fora do limite rígido, então há erro no campo e nenhum resultado.<br>Dado um valor implausível, então o resultado só sai após confirmação.<br>Passa no axe e funciona só com teclado. |
| F5-03 | Executor de casos de referência | Hi/- | Sm/- | F5-01 | Não iniciada | Todo item de `cases.json` vira um teste e traz a referência de onde saiu.<br>Calculadora sem casos falha no CI.<br>Dado `status: suspensa`, então o formulário fica desativado, com aviso. |
| F5-04 | Template de página de calculadora | Med/- | Md/- | F5-02 | Não iniciada | Seções de como usar, fórmula, exemplo, limitações e referências, legíveis sem JavaScript.<br>Selo "Não validada clinicamente" e aviso de ferramenta de apoio junto ao resultado. |
| F5-05 | Teste de privacidade | Med/- | Sm/- | F5-02 | Não iniciada | Dado um cálculo completo, então nenhuma requisição de rede é feita e nada fica na URL ou em armazenamento local. |
| F5-06 | Hidratação de manutenção | Hi/- | Sm/- | F5-03, F5-04 | Não iniciada | Casos de 3, 10, 15, 20 e 35 kg conferem com o cálculo pela fórmula publicada.<br>Mostra mL/dia e mL/h, com a conta visível. |

---

## Fase 6 — Calculadoras iniciais

**Objetivo:** quatro calculadoras no ar e usadas de verdade.

**Aceite da fase (todos obrigatórios):**

- [ ] Quatro calculadoras no ar: hidratação, superfície corporal e IMC, dose por peso genérica e curva OMS 0–5 anos.
- [ ] Uma semana de uso real, com os problemas relatados.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F6-01 | Superfície corporal e IMC | Hi/- | Sm/- | F5-06 | Não iniciada | Ao menos 5 casos de referência com fonte. |
| F6-02 | Dose por peso genérica | Hi/- | Sm/- | F5-06 | Não iniciada | Mostra mg e mL por dose e mg por dia.<br>Dado o campo de concentração vazio, então não há resultado em mL.<br>A página não cita fármaco nem dose recomendada. |
| F6-03 | Tabelas LMS da OMS 0–5 anos | Hi/- | Md/- | F1-01 | Não iniciada | Script reproduzível, com checksum dos arquivos oficiais.<br>Termos de uso dos dados conferidos antes de publicá-los em repositório público. |
| F6-04 | Z-score e percentil 0–5 anos | Hi/- | Md/- | F6-03, F5-02 | Não iniciada | Concordância com `anthro` em mil casos, com tolerância de 0,01.<br>Dado idade acima de 5 anos, então a calculadora informa que está fora da faixa. |
| F6-05 | Gráfico de crescimento | Hi/- | Md/- | F6-04 | Não iniciada | Curvas de P3 a P97 em SVG gerado no build, com o ponto plotado e alternativa em texto. |
| F6-06 | Uso real | Lo/- | Sm/- | F6-01, F6-02, F6-05 | Não iniciada | O usuário principal usa as quatro calculadoras por uma semana e relata problemas. |

---

## Fase 7 — Melhorias 1

**Objetivo:** calculadoras simples adicionais.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F7-01 | Curva OMS 5–19 anos | Hi/- | Md/- | F6-04 | Não iniciada | Concordância com o pacote da OMS; peso/idade só até 10 anos. |
| F7-02 | Idade corrigida do prematuro | Hi/- | Sm/- | F6-06 | Não iniciada | Casos de referência com fonte. |
| F7-03 | Perda de peso do recém-nascido | Hi/- | Sm/- | F6-06 | Não iniciada | Casos com fonte; limiar e fonte exibidos. |
| F7-04 | Estatura-alvo familiar | Hi/- | Sm/- | F6-06 | Não iniciada | Casos com fonte. |
| F7-05 | TFG estimada (Schwartz) | Hi/- | Sm/- | F6-06 | Não iniciada | Casos com fonte; unidade da creatinina explícita. |
| F7-06 | Página de upload no site (condicional) | Hi/- | Md/- | F3-02 | Não iniciada | Envio sem GitHub que resulta no mesmo PR; só se o envio atual incomodar. |

---

## Fase 8 — Melhorias 2

**Objetivo:** calculadoras de tabela e PWA.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F8-01 | Reidratação oral | Hi/- | Md/- | F6-06 | Não iniciada | Casos com fonte vigente do Ministério da Saúde. |
| F8-02 | Pressão arterial | Hi/- | Lg/- | F7-01 | Não iniciada | Concordância com as tabelas da AAP 2017. |
| F8-03 | Curvas de prematuros | Hi/- | Lg/- | F6-04 | Não iniciada | Primeiro passo: validar a escolha entre Intergrowth-21st e Fenton; depois, concordância com as tabelas publicadas. |
| F8-04 | Bilirrubina | Hi/- | Lg/- | F6-06 | Não iniciada | Concordância com os limiares da AAP 2022. |
| F8-05 | Curva CDC 2000 | Hi/- | Md/- | F6-04 | Não iniciada | Concordância com os arquivos LMS do CDC. |
| F8-06 | PWA offline | Med/- | Md/- | F6-06 | Não iniciada | Dado o site já visitado, quando fico sem rede, então as calculadoras calculam. |

---

## Fase 9 — Publicação pública (futura)

**Objetivo:** revisão clínica, associação a um médico, indexação e calculadoras com fármaco.

Nada desta fase começa sem decisão explícita do Filipe. A ordem importa: revisão antes de associar, associar antes de indexar.

"Apêndice" abaixo é o apêndice do plano final sobre as regras para associar um médico ao site. Ele não está no repositório; entra em F9-02. Nome, registro e áreas de pós-graduação ficam fora do repositório até lá.

### Issues

| ID | Título | Expected/Seen Risk | Expected/Seen Size | Depende de | Status | Aceite |
| --- | --- | --- | --- | --- | --- | --- |
| F9-01 | Etapa de revisão clínica | Hi/- | Md/- | Decisão do Filipe | Não iniciada | O post ganha `status: rascunho` e `aprovadoEm`; só aprovado é publicado.<br>O merge automático passa a exigir a aprovação.<br>As calculadoras ganham registro de revisão e perdem o selo "Não validada clinicamente" uma a uma. |
| F9-02 | Associar um médico ao site | Hi/- | Md/- | F9-01 | Não iniciada | Identificação conforme o apêndice, na home e em todas as páginas.<br>Verificação automática dos termos proibidos do apêndice.<br>Nomes oficiais das pós-graduações confirmados antes de qualquer menção a elas.<br>F1-06 é substituída pela verificação nova. |
| F9-03 | Revisão retroativa ou arquivo | Hi/- | Md/- | F9-01 | Não iniciada | Cada edição publicada antes da revisão é aprovada, retirada ou marcada como "anterior à revisão". |
| F9-04 | Indexação | Hi/- | Sm/- | F9-02, F9-03, F4-02 | Não iniciada | `indexavel` ligado, sitemap gerado e aceito no Search Console.<br>Auditoria de conformidade com o apêndice aprovada. |
| F9-05 | Antitérmicos com tabela de fármacos | Hi/- | Md/- | F9-01 e checagem regulatória | Não iniciada | Valor por fonte, SBP como padrão e bloco de divergência.<br>Teste garante que nenhuma dose passa do teto por tomada ou por dia. |
| F9-06 | Antibióticos por peso | Hi/- | Md/- | F9-05 | Não iniciada | Mesmo portão de F9-05. |

**Checagem regulatória de F9-05:** antes de começar, conferir a RDC 657/2022 e a RDC 96/2008 da ANVISA.

---

## Changelog

| Data | Mudança |
| --- | --- |
| 2026-11-24 | Nova F0-06: traduzir a documentação para inglês. Tamanho e risco substituem pequena/grande no fluxo (`AGENTS.md` §3); toda issue ganhou as colunas Expected/Seen Risk e Size |
| 2026-11-15 | Roadmap inicial: fases 0 a 9 e 59 issues, a partir do plano final aprovado. F0-03 nasce `bloqueada` à espera da lista de fontes |
